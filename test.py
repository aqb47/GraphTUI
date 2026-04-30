from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Input, Label, Static, Button
from textual.screen import Screen


class ExampleScreen(Screen):
    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.message = message

    def compose(self) -> ComposeResult:
        yield Static(self.message)
        yield Button("Back", id="back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()

class InputApp(App):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Type something...")
        yield Label("Result will appear here", id="display")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        # Access the typed text via event.value or event.input.value
        self.query_one("#display", Label).update(f"You typed: {event.value}")
        self.app.push_screen(ExampleScreen(f"You typed: {event.value}"))


if __name__ == "__main__":
    InputApp().run()
