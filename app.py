# Main UI to display menus and handle user input
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.containers import Container
from textual.screen import Screen


class MainMenu(Static):
    def compose(self) -> ComposeResult:
        yield Button("Generate Graph", id="generate_graph")
        yield Button("Help", id="help")
    

class GraphTUI(App):
    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(MainMenu(), id="main_menu")
        yield Footer()
        self.theme = 'flexoki'

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "generate_graph":
            self.push_screen(GraphBuilderScreen())
        elif button_id == "help":
            self.push_screen(HelpScreen())
        

class GraphBuilderScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("Graph generation functionality goes here.")
        yield Button("Back", id="back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()


class HelpScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("Help information goes here.")
        yield Button("Back", id="back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()


if __name__ == "__main__":
    app = GraphTUI()
    app.run()