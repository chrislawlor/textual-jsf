from unittest.mock import MagicMock

import pytest
from textual.widget import Widget
from textual.widgets import Select

from textual_jsf.form import create_input_widget


def test_input_widget_type_int():
    property = {"type": "integer"}
    widget = create_input_widget("age", property)
    result = widget.validate("1")
    assert result.is_valid is True
    result = widget.validate("1.1")
    assert result.is_valid is False
    assert result.failures[0].description == "Must be a valid integer."


def test_input_widget_type_int_with_maximum():
    property = {"type": "integer", "maximum": 100}
    widget = create_input_widget("age", property)
    result = widget.validate(101)
    assert result.is_valid is False
    assert result.failures[0].description == "Must be less than or equal to 100."


def test_input_widget_type_int_with_minimum():
    property = {"type": "integer", "minimum": 0}
    widget = create_input_widget("age", property)
    result = widget.validate("-1")
    assert result.is_valid is False
    assert result.failures[0].description == "Must be greater than or equal to 0."
    result = widget.validate("0")
    assert result.is_valid is True


def test_input_widget_type_number():
    property = {"type": "number"}
    widget = create_input_widget("age", property)
    result = widget.validate("1")
    assert result.is_valid is True
    result = widget.validate("1.1")
    assert result.is_valid is True
    result = widget.validate("one")
    assert result.is_valid is False
    assert result.failures[0].description == "Must be a valid number."


@pytest.mark.parametrize(
    ["constraints", "value", "expected_failure_description"],
    [
        ({"minimum": 0}, "-1", "Must be greater than or equal to 0."),
        ({"maximum": 100}, "101", "Must be less than or equal to 100."),
        ({"exclusiveMinimum": 0}, "0", "Must be greater than 0."),
        ({"exclusiveMaximum": 100}, "100", "Must be less than 100."),
        ({"minimum": 0, "maximum": 100}, "-1", "Must be in range [0, 100]."),
        ({"minimum": 0, "exclusiveMaximum": 100}, "100", "Must be in range [0, 100)."),
        ({"exclusiveMinimum": 0, "maximum": 100}, "0", "Must be in range (0, 100]."),
        (
            {"exclusiveMinimum": 0, "exclusiveMaximum": 100},
            0,
            "Must be in range (0, 100).",
        ),
        (
            {"exclusiveMinimum": 0, "exclusiveMaximum": 100},
            100,
            "Must be in range (0, 100).",
        ),
        ({"multipleOf": 2}, 1, "Must be a multiple of 2."),
    ],
)
@pytest.mark.parametrize("type_", ["integer", "number"])
def test_input_widget_range_validation_failures(
    type_, constraints, value, expected_failure_description
):
    property = {"type": type_, **constraints}
    widget = create_input_widget("percentile", property)
    result = widget.validate(value)
    msg = f"Expected {value} to be invalid for constraints {constraints}"
    assert result.is_valid is False
    assert result.failures[0].description == expected_failure_description


@pytest.mark.parametrize("value", ["inf", "nan", "-inf"])
def test_input_widget_float_validation_errors(value):
    property = {"type": "number"}
    widget = create_input_widget("test", property)
    result = widget.validate(value)
    assert result.is_valid is False


def test_create_input_widget_does_not_mutate_schema():
    original = {"type": "number"}
    property = {"type": "number"}
    assert property == original
    create_input_widget("test", property)
    assert property == original


@pytest.mark.parametrize(
    ["enum", "options"],
    [
        (
            ["choices", "are", "good"],
            [("choices", "choices"), ("are", "are"), ("good", "good")],
        ),
        ([1, 2, 3], [("1", 1), ("2", 2), ("3", 3)]),
    ],
)
def test_enum(enum, options):
    property = {"type": "string", "enum": enum}
    widget = create_input_widget("test", property)
    assert isinstance(widget, Select)
    assert widget._options == options


def test_pattern_validation():
    pattern = "[0-9]{3}-[0-9]{2}-[0-9]{4}"
    value = "123-45-6789"
    widget = create_input_widget("test", {"type": "string", "pattern": pattern})
    result = widget.validate(value)
    assert result.is_valid is True
    value = "11-22-33"
    result = widget.validate(value)
    assert result.is_valid is False


@pytest.mark.parametrize(
    ["constraints", "value", "expected_failure_description"],
    [
        ({"minLength": 3}, "ab", "Must be longer than 3 characters."),
        ({"maxLength": 3}, "abcd", "Must be shorter than 3 characters."),
    ],
)
def test_string_validation(constraints, value, expected_failure_description):
    property = {"type": "string", **constraints}
    widget = create_input_widget("test", property)
    result = widget.validate(value)
    assert result.is_valid is False
    assert result.failures[0].description == expected_failure_description


def test_const_validation(monkeypatch):
    # We patch watch_disabled because there is not active App running.
    monkeypatch.setattr(Widget, "watch_disabled", MagicMock())

    property = {"type": "string", "const": "test"}
    widget = create_input_widget("test", property)

    assert widget.value == "test"
    assert widget.disabled is True


def test_invalid_type_throws():
    property = {"type": "invalid"}
    with pytest.raises(ValueError):
        create_input_widget("test", property)


@pytest.mark.parametrize(
    ["default", "expected_value"], [(True, True), (False, False), (None, False)]
)
def test_boolean(default, expected_value):
    property = {"type": "boolean", "default": default}
    widget = create_input_widget("test", property)
    assert widget.value == expected_value
