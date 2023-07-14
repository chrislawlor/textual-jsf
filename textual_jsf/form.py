from __future__ import annotations

import re
from enum import Enum
from typing import Dict, Generator, List, Tuple

from textual.containers import Horizontal
from textual.validation import Length, Regex, Validator
from textual.widgets import Checkbox, Input, Label, Select

from . import validation


class Types(str, Enum):
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    OBJECT = "object"
    ARRAY = "array"


def horizontal(schema) -> Generator[Horizontal, None, None]:
    for label, input in form_widgets(schema):
        yield Horizontal(label, input)


def form_widgets(
    schema,
) -> Generator[Tuple[Label, Input | Select | Checkbox], None, None]:
    required = schema.get("required", [])
    for key, property in schema["properties"].items():
        label = property.get("title", key.capitalize())
        is_required = key in required
        yield Label(label), create_input_widget(key, property, is_required)


def create_input_widget(
    key: str, property: Dict, required=True
) -> Input | Select | Checkbox:
    validators: List[Validator] = []
    type_ = Types(property.get("type", Types.STRING))
    default = property.get("default")

    value = str(default) if default is not None else None
    disabled = False

    if type_ == Types.INTEGER:
        validators.append(validation.JsfInteger(**property))

    elif type_ == Types.NUMBER:
        validators.append(validation.JsfNumber(**property))

    elif type_ == Types.STRING:
        pattern = property.get("pattern")
        if pattern is not None:
            validators.append(Regex(regex=re.compile(pattern)))
        maximum = property.get("maxLength")
        minimum = property.get("minLength")
        if maximum is not None or minimum is not None:
            validators.append(Length(maximum=maximum, minimum=minimum))

    elif type_ == Types.BOOLEAN:
        return Checkbox(value=bool(default))

    enum = property.get("enum")
    if enum is not None:
        return Select(
            options=[(str(item), item) for item in enum],
            name=key,
            value=value,
        )

    const = property.get("const")
    if const is not None:
        value = const
        disabled = True

    return Input(name=key, validators=validators, value=value, disabled=disabled)
