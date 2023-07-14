from __future__ import annotations

import math
from typing import Any, List

from textual.validation import Failure, Integer, Number, ValidationResult, Validator


class JsfNumber(Number):
    class NotAMultipleOf(Failure):
        """Indicates a failure due to the value not being a multiple of the given number."""

    def __init__(
        self,
        multipleOf=None,
        maximum=None,
        exclusiveMaximum=None,
        minimum=None,
        exclusiveMinimum=None,
        failure_description: str | None = None,
        **_,
    ):
        super().__init__(failure_description=failure_description)
        if maximum is not None and exclusiveMaximum is not None:
            maximum = None

        if minimum is not None and exclusiveMinimum is not None:
            minimum = None

        self.multipleOf = multipleOf
        self.maximum = maximum
        self.exclusiveMaximum = exclusiveMaximum
        self.minimum = minimum
        self.exclusiveMinimum = exclusiveMinimum

    def _validate_range(self, value: float) -> bool:
        if self.maximum is not None and value > self.maximum:
            return False

        if self.exclusiveMaximum is not None and value >= self.exclusiveMaximum:
            return False

        if self.minimum is not None and value < self.minimum:
            return False

        if self.exclusiveMinimum is not None and value <= self.exclusiveMinimum:
            return False

        return True

    def validate(self, value: str) -> ValidationResult:
        number_validation_result = super().validate(value)
        if number_validation_result.is_valid is False:
            return number_validation_result

        # super().validate checks math.nan, but not float("nan"). Since
        # NaN is not equal to itself, we explicitly check for it here.
        if value == "nan":
            return ValidationResult.failure([Number.NotANumber(self, value)])
        if self.multipleOf is not None:
            if not math.isclose(float(value) % self.multipleOf, 0):
                return ValidationResult.failure([JsfNumber.NotAMultipleOf(self, value)])
        return self.success()

    def describe_failure(self, failure: Failure) -> str | None:
        if isinstance(failure, Number.NotANumber):
            return f"Must be a valid number."
        if isinstance(failure, JsfNumber.NotAMultipleOf):
            return f"Must be a multiple of {self.multipleOf}."
        elif isinstance(failure, Number.NotInRange):
            if self.minimum is None and self.exclusiveMinimum is None:
                if self.exclusiveMaximum is not None:
                    return f"Must be less than {self.exclusiveMaximum}."
                if self.maximum is not None:
                    return f"Must be less than or equal to {self.maximum}."
            elif self.maximum is None and self.exclusiveMaximum is None:
                if self.exclusiveMinimum is not None:
                    return f"Must be greater than {self.exclusiveMinimum}."
                if self.minimum is not None:
                    return f"Must be greater than or equal to {self.minimum}."
            else:
                min_char = "(" if self.exclusiveMinimum is not None else "["
                max_char = ")" if self.exclusiveMaximum is not None else "]"
                lower_bound = (
                    self.exclusiveMinimum
                    if self.exclusiveMinimum is not None
                    else self.minimum
                )
                upper_bound = (
                    self.exclusiveMaximum
                    if self.exclusiveMaximum is not None
                    else self.maximum
                )
                return f"Must be in range {min_char}{lower_bound}, {upper_bound}{max_char}."
        return None


class JsfInteger(JsfNumber):
    def validate(self, value: str) -> ValidationResult:
        number_validation_result = super().validate(value)
        if not number_validation_result.is_valid:
            return number_validation_result

        # We know it's a number, but is it an integer?
        is_integer = float(value).is_integer()
        if not is_integer:
            return ValidationResult.failure([Integer.NotAnInteger(self, value)])
        return self.success()

    def describe_failure(self, failure: Failure) -> str | None:
        if isinstance(failure, Integer.NotAnInteger):
            return f"Must be a valid integer."
        return super().describe_failure(failure)
