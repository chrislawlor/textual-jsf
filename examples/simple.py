import jsonschema
from pydantic import BaseModel
from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header

from textual_jsf.form import form_widgets, horizontal

SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 3,
            "description": "Please enter your name",
        },
        "vegetarian": {"type": "boolean"},
        "birthDate": {"type": "string", "format": "date"},
        "nationality": {
            "type": "string",
            "enum": ["DE", "IT", "JP", "US", "RU", "Other"],
        },
        # "personalData": {
        #     "type": "object",
        #     "properties": {
        #         "age": {"type": "integer", "description": "Please enter your age."},
        #         "height": {"type": "number"},
        #         "drivingSkill": {
        #             "type": "number",
        #             "maximum": 10,
        #             "minimum": 1,
        #             "default": 7,
        #         },
        #     },
        #     "required": ["age", "height"],
        # },
        "occupation": {"type": "string"},
        "postalCode": {"type": "string", "maxLength": 5},
    },
    "required": ["occupation", "nationality"],
}


class SimpleApp(App):
    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
        grid-columns: 1fr 5fr;
    }

    """

    def compose(self):
        yield Header("Simple Form")
        for label, input in form_widgets(SCHEMA):
            yield label
            yield input
        yield Footer()


if __name__ == "__main__":
    # data = {"name": "Chris", "age": 45}
    # jsonschema.validate(instance=data, schema=SCHEMA)
    app = SimpleApp()

    app.run()
