import json

import jsonschema

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
        "personalData": {
            "type": "object",
            "properties": {
                "age": {"type": "integer", "description": "Please enter your age."},
                "height": {"type": "number"},
                "drivingSkill": {
                    "type": "number",
                    "maximum": 10,
                    "minimum": 1,
                    "default": 7,
                },
            },
            "required": ["age", "height"],
        },
        "occupation": {"type": "string"},
        "postalCode": {"type": "string", "maxLength": 5},
    },
    "required": ["occupation", "nationality"],
}


DATA = {
    "name": "Xix",  # minLength 3
    "vegetarian": False,
    "birthDate": "1978-05-05",
    "nationality": "US",
    "personalData": {
        "age": 42,  # required
        "height": 1.76,  # required
        "drivingSkill": 11,
    },
    "occupation": "Hacker",
    "postalCode": "11104",
}


if __name__ == "__main__":
    error = None
    try:
        jsonschema.validate(instance=DATA, schema=SCHEMA)
    except jsonschema.ValidationError as ve:
        error = ve
    import ipdb

    ipdb.set_trace()
