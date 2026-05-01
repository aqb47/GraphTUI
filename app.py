# Main UI to display menus and handle user input

import re
from tokenize import TokenError

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Input, Label
from textual.containers import HorizontalGroup, VerticalGroup
from textual.screen import Screen

from math_engine import validate_function, parse_function, generate_points, ALLOWED_FUNCTIONS, ALLOWED_CONSTANTS
from renderer import draw_axis, plot_points, add_labels, get_default_config
from utils import is_float

# Default configuration values for graph generation
TOTAL_X_UNITS: int = 12
TOTAL_Y_UNITS: int = 10

MAX_X_UNITS: int = 100
MAX_Y_UNITS: int = 100

STEP: float = 0.05
MIN_STEP: float = 0.0001
MAX_STEP: float = 5.0


# Input function string and return the complete graph list
def generate_complete_graph(function_str: str, total_x_units: int, total_y_units: int, step: float) -> list:
    # Sympy recognizes Euler's number as E
    function_str = re.sub(r'\be\b', 'E', function_str)

    # Validate function string
    validate_function(function_str)

    # Parse function string to a callable function
    function: callable = parse_function(function_str)

    # Generate points from the function
    points: list[list[float]] = generate_points(function, -total_x_units/2, total_x_units/2, step)

    # The scale is rows or cols per unit on x or y-axis respectively. Get default config gets current screen size

    row_scale: float = get_default_config()[0] / total_y_units
    col_scale: float = get_default_config()[1] / total_x_units

    # Initialize graph 
    graph: list = draw_axis()

    # Plot the points and add labels to the graph
    graph = plot_points(graph, points, col_scale, row_scale)
    graph = add_labels(graph, total_x_units, total_y_units)

    return graph


# Main menu of App
class MainMenu(Static):
    def compose(self) -> ComposeResult:
        yield Button("Generate Graph", id="graph_screen")
        yield Button("Help", id="help")
    

# Main App class 
class GraphTUI(App):
    CSS_PATH = "app.tcss"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.AUTO_FOCUS = None

    def compose(self) -> ComposeResult:
        yield Header()

        yield Static("This is GraphTUI.", classes="title")
        yield MainMenu()

        yield Footer()

    # Button logic for navigation 
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "graph_screen":
            self.push_screen(GraphBuilderScreen())
        elif button_id == "help":
            self.push_screen(HelpScreen())
        elif button_id == "back":
            self.pop_screen()


class GraphInputContainer(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield HorizontalGroup(Label('- Function Input:'),Input(id = "function_input", placeholder="Enter function of x (e.g sin(x), x**2 + 3*x, log(x) etc.)"))
        yield HorizontalGroup(Label('- Total X Units: '),Input(id = "total_x_units", placeholder=f"Enter total x units (default {TOTAL_X_UNITS})"))
        yield HorizontalGroup(Label('- Total Y Units: '),Input(id = "total_y_units", placeholder=f"Enter total y units (default {TOTAL_Y_UNITS})"))
        yield HorizontalGroup(Label('- Step Size:     '),Input(id = "step", placeholder=f"Enter step size (default {STEP})"))


# Graph building screen which takes user specification
class GraphBuilderScreen(Screen):
    BINDINGS = [('ctrl+g', 'generate', 'Start generation')]

    def compose(self) -> ComposeResult:
        yield Static("Graph Builder", classes="title")

        yield GraphInputContainer()

        yield Button("Generate", id="generate")
        yield Button("Back", id="back")
        yield Button("Help", id="help")

        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        # Graph generation logic
        if button_id == 'generate':
            # Get graph specifications
            function_input = self.screen.query_one("#function_input", Input).value
            total_x_units_input = self.screen.query_one("#total_x_units", Input).value
            total_y_units_input = self.screen.query_one("#total_y_units", Input).value
            step_input = self.screen.query_one("#step", Input).value

            # Validate inputs and use default values if invalid
            if not total_x_units_input or not total_x_units_input.isnumeric() or not (0 < int(total_x_units_input) <= MAX_X_UNITS):
                total_x_units_input = TOTAL_X_UNITS
            if not total_y_units_input or not total_y_units_input.isnumeric() or not (0 < int(total_y_units_input) <= MAX_Y_UNITS):
                total_y_units_input = TOTAL_Y_UNITS
            if not step_input or not is_float(step_input) or not (MIN_STEP <= float(step_input) <= MAX_STEP):
                step_input = STEP
            
            # Function input is mandatory, show error if empty
            if not function_input:
                self.app.push_screen(ErrorScreen('Function input cannot be empty.'))
                return

            # Attempt graph generation, show error if something goes wrong
            try:
                graph = generate_complete_graph(function_input, int(total_x_units_input), int(total_y_units_input), float(step_input))
                
                self.app.push_screen(GraphDisplayScreen(graph, function_input, int(total_x_units_input), int(total_y_units_input), float(step_input)))
            except ValueError:
                self.app.push_screen(ErrorScreen("Invalid function input. Check for unsupported functions, constants or syntax."))
            except SyntaxError:
                self.app.push_screen(ErrorScreen("Invalid syntax used in function. Consult the help screen for supported syntax."))
            except TypeError:
                self.app.push_screen(ErrorScreen("Invalid function input. Check function arguments."))
            except TokenError:
                self.app.push_screen(ErrorScreen("Invalid function input. Check for uncompleted parentheses."))

    def action_generate(self) -> None:
        self.screen.query_one("#generate", Button).press()



# Graph display screen which shows generated graph list
class GraphDisplayScreen(Screen):
    def __init__(self, graph: list, function: str, total_x_units: int, total_y_units: int, step: float, **kwargs):
        super().__init__(**kwargs)
        self.graph = graph
        self.function = function
        self.total_x_units = total_x_units
        self.total_y_units = total_y_units
        self.step = step

    def compose(self) -> ComposeResult:
        yield Static("\n".join("".join(row) for row in self.graph), id="graph_output")
        yield Button("Back", id="back")
    
    # Regenerate graph on screen resize to fit new dimensions
    def on_resize(self, event) -> None:
        # Debouncing by delaying regeneration
        self.set_timer(0.2, self._regenerate_graph)
    
    def _regenerate_graph(self) -> None:
        try:
            graph = generate_complete_graph(self.function, self.total_x_units, self.total_y_units, self.step)
    
            self.query_one("#graph_output", Static).update("\n".join("".join(row) for row in graph))
            self.refresh()
        except IndexError:
            self.query_one("#graph_output", Static).update("Graph cannot be displayed at this size.")
            self.refresh()


# Error handling screen
class ErrorScreen(Screen):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        yield Static("ERROR", classes="title")
        
        yield Static(self.message, id="error_message")
        yield Static('\n')

        yield Button("Back", id="back")
        yield Button("Help", id="help")


class HelpContainer(Static):
    def __init__(self, message: str, example: str, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.example = example
    
    def compose(self) -> ComposeResult:
        yield Static(self.message, classes="bold")

        if self.example:
            yield Static(self.example, classes="italic")


# Help screen for displaying instructions
class HelpScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("This is GraphTUI, a terminal-based graphing calculator.\n", classes="title")

        yield HelpContainer("- To generate a graph, click on 'Generate Graph' and input the required details.", "")
        
        yield HelpContainer("- Your function has to be in terms of x.", "e.g f(x) = sin(x) or f(x) = x**2 + 3*x - 5")
        
        yield HelpContainer("- Total x/y units specify range of x/y axis respectively.", "e.g Total x units = 10 generates 10 units on x-axis, 5 on +ve x-axis and 5 on -ve x-axis.")

        yield HelpContainer("- Step size determines the granularity of the graph. Smaller step size results in a smoother graph.", "e.g Step size = 0.01 generates points at intervals of 0.01 on x-axis.")

        yield HelpContainer("- There is a maximum and minimum value for these specifications.", f"e.g 0 < Total x/y units <= {MAX_X_UNITS}, {MIN_STEP} <= Step size <= {MAX_STEP}")

        yield HelpContainer("- Default values are used when inputs are invalid or empty.", f"e.g Default total x units = {TOTAL_X_UNITS}, Default total y units = {TOTAL_Y_UNITS}, Default step size = {STEP}")

        yield HelpContainer("- Multiplication should be denoted by '*', division by '/', exponentiation by '**'.", "e.g 6x -> 6*x, 6÷x -> 6/x, 6^x -> 6**x")

        func_example = ""
        for func in ALLOWED_FUNCTIONS:
            func_example += f"{func}(x)\n"
        yield HelpContainer("- Supported functions:", func_example)

        const_example = ""
        for const in ALLOWED_CONSTANTS:
            const_example += f"{const}\n"
        yield HelpContainer("- Supported constants:", const_example)

        yield Button("Back", id="back")


if __name__ == "__main__":
    app = GraphTUI()
    app.run()