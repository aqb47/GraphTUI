# Main UI to display menus and handle user input
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Input, Label
from textual.containers import Container
from textual.screen import Screen

from math_engine import validate_function, parse_function, generate_points
from renderer import draw_axis, plot_points, add_labels, get_default_config

# My default values for testing purposes
TOTAL_X_UNITS: int = 12
TOTAL_Y_UNITS: int = 10
STEP: float = 0.05


def generate_complete_graph(function_str: str, total_x_units: int, total_y_units: int, step: float) -> list:
    # Validate function string
    validate_function(function_str)

    # Parse function string to a callable function
    function: callable = parse_function(function_str)

    # Generate points from the function
    points: list[list[float]] = generate_points(function, - total_x_units / 2, total_x_units / 2, step)

    # The scale is rows or cols per unit on x or y-axis respectively
    row_scale: float = get_default_config()[0] / total_y_units
    col_scale: float = get_default_config()[1] / total_x_units

    # Initialize graph 
    graph: list = draw_axis()

    # Plot the points and add labels to the graph
    graph = plot_points(graph, points, col_scale, row_scale)
    graph = add_labels(graph, total_x_units, total_y_units)

    return graph


class FunctionInput(Input):
    def __init__(self, placeholder: str = "Enter function of x (e.g sin(x), x**2 + 3*x, log(x) etc.)", **kwargs):
        super().__init__(placeholder=placeholder, **kwargs)


class MainMenu(Static):
    def compose(self) -> ComposeResult:
        yield Button("Generate Graph", id="graph_screen")
        yield Button("Help", id="help")
    

class GraphTUI(App):
    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(MainMenu(), id="main_menu")
        yield Footer()
        self.theme = 'gruvbox'

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "graph_screen":
            self.push_screen(GraphBuilderScreen())
        elif button_id == "help":
            self.push_screen(HelpScreen())
        elif button_id == "back":
            self.pop_screen()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "function_input":
            try: 
                function_str: str = event.value

                graph = generate_complete_graph(function_str, TOTAL_X_UNITS, TOTAL_Y_UNITS, STEP)

                self.push_screen(GraphDisplayScreen(graph))
            except Exception:
                self.push_screen(ErrorScreen('Something went wrong :P'))
        

class GraphBuilderScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("Graph generation functionality goes here.")
        
        yield FunctionInput(id = "function_input")

        yield Label("Press ENTER to generate")

        yield Button("Back", id="back")
        yield Button("Help", id="help")


class GraphDisplayScreen(Screen):
    def __init__(self, graph: list, **kwargs):
        super().__init__(**kwargs)
        self.graph = graph

    def compose(self) -> ComposeResult:
        yield Static("\n".join("".join(row) for row in self.graph))
        yield Button("Back", id="back")


class ErrorScreen(Screen):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        yield Static(self.message)
        yield Button("Back", id="back")


class HelpScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("Help information goes here.")
        yield Button("Back", id="back")


if __name__ == "__main__":
    app = GraphTUI()
    app.run()