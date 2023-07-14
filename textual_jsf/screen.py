from typing import Type

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static

from .form import create_input_widgets


def create_screen(schema) -> Type[Screen]:
    class Form(Screen):
        def compose(self) -> ComposeResult:
            yield Static(schema.get("title", "Form"))
            yield from create_input_widgets(schema)

    return Form
