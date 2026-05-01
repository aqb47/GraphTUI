# Main UI to display menus and handle user input

import re

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Input, Label
from textual.containers import HorizontalGroup
from textual.screen import Screen

from math_engine import validate_function, parse_function, generate_points, ALLOWED_FUNCTIONS, ALLOWED_CONSTANTS
from renderer import draw_axis, plot_points, add_labels, get_default_config

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
        yield Static("This is GraphTUI", classes="title")
        yield Button("Generate Graph", id="graph_screen")
        yield Button("Help", id="help")
    

# Main App class 
class GraphTUI(App):
    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield MainMenu()
        yield Footer()

    # Button logic for navigation and graph generation
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "graph_screen":
            self.push_screen(GraphBuilderScreen())
        elif button_id == "help":
            self.push_screen(HelpScreen())
        elif button_id == "back":
            self.pop_screen()
        
        # Graph generation logic
        elif button_id == 'generate':
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
            if not step_input or not step_input.isnumeric() or not (MIN_STEP <= float(step_input) <= MAX_STEP):
                step_input = STEP
            
            # Function input is mandatory, show error if empty
            if not function_input:
                self.push_screen(ErrorScreen('Function input cannot be empty.'))
                return

            # Attempt graph generation, show error if something goes wrong
            try:
                graph = generate_complete_graph(function_input, int(total_x_units_input), int(total_y_units_input), float(step_input))
                self.push_screen(GraphDisplayScreen(graph))
            except Exception:
                self.push_screen(ErrorScreen('Something went wrong with your function.'))
        

# Graph building screen which takes user specification
class GraphBuilderScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("Graph Builder", classes="title")

        yield HorizontalGroup(Label('- Function Input:'),Input(id = "function_input", placeholder="Enter function of x (e.g sin(x), x**2 + 3*x, log(x) etc.)"))
        yield HorizontalGroup(Label('- Total X Units: '),Input(id = "total_x_units", placeholder=f"Enter total x units (default {TOTAL_X_UNITS})"))
        yield HorizontalGroup(Label('- Total Y Units: '),Input(id = "total_y_units", placeholder=f"Enter total y units (default {TOTAL_Y_UNITS})"))
        yield HorizontalGroup(Label('- Step Size:     '),Input(id = "step", placeholder=f"Enter step size (default {STEP})"))

        yield Button("Generate", id="generate")
        yield Button("Back", id="back")
        yield Button("Help", id="help")


# Graph display screen which shows generated graph list
class GraphDisplayScreen(Screen):
    def __init__(self, graph: list, **kwargs):
        super().__init__(**kwargs)
        self.graph = graph

    def compose(self) -> ComposeResult:
        yield Static("\n".join("".join(row) for row in self.graph))
        yield Button("Back", id="back")


# Error handling screen
class ErrorScreen(Screen):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        yield Static("ERROR", classes="title")
        
        yield Static(self.message)
        yield Static('\n')

        yield Button("Back", id="back")
        yield Button("Help", id="help")


# Help screen for displaying instructions
class HelpScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("This is GraphTUI, a terminal-based graphing calculator.\n", classes="title")

        yield Static("- To generate a graph, click on 'Generate Graph' and input the required details.\n\n", classes="bold")
        
        yield Static("- Your function has to be in terms of x.\n", classes="bold")
        yield Static("e.g f(x) = sin(x) or f(x) = x**2 + 3*x - 5\n\n", classes="italic")
        
        yield Static("- Total x/y units specify range of x/y axis respectively. \n", classes="bold")
        yield Static("e.g Total x units = 10 generates 10 units on x-axis, 5 on +ve x-axis and 5 on -ve x-axis.\n\n", classes="italic")

        yield Static("- Step size determines the granularity of the graph. Smaller step size results in a smoother graph.\n", classes="bold")
        yield Static("e.g Step size = 0.01 generates points at intervals of 0.01 on x-axis.\n\n", classes="italic")

        yield Static("- There is a maximum and minimum limit for these specifications.\n", classes="bold")
        yield Static(f"e.g 0 < Total x/y units <= {MAX_X_UNITS}, {MIN_STEP} <= Step size <= {MAX_STEP}\n\n", classes="italic")

        yield Static("- Default values are used when inputs are invalid or empty.\n", classes="bold")
        yield Static(f"e.g Default total x units = {TOTAL_X_UNITS}, Default total y units = {TOTAL_Y_UNITS}, Default step size = {STEP}\n\n", classes="italic")

        yield Static("- Multiplication should be denoted by '*', division by '/', exponentiation by '**'.\n", classes="bold")
        yield Static("e.g 6x -> 6*x, 6÷x -> 6/x, 6^x -> 6**x\n\n", classes="italic")

        yield Static("- Supported functions:\n", classes="bold")
        for func in ALLOWED_FUNCTIONS:
            yield Static(f"{func}(x)\n", classes="italic")
        yield Static("\n")

        yield Static("- Supported constants:\n", classes="bold")
        for const in ALLOWED_CONSTANTS:
            yield Static(f"{const}\n", classes="italic")
        yield Static("\n")
        
        yield Button("Back", id="back")


if __name__ == "__main__":
    app = GraphTUI()
    app.run()