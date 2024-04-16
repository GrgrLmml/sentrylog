import json

from pydantic import ValidationError

from parser.models import ResponseItem, ResponseItems


def parse_llm_response(text: str) -> ResponseItems:
    items = []
    stack = []  # To track the position of nested curly braces
    errors = 0
    for i, char in enumerate(text):
        if char == '{':
            stack.append(i)
        elif char == '}' and stack:
            start_index = stack.pop()
            if not stack:  # All braces are closed, this is a complete JSON object
                try:
                    substring = text[start_index:i + 1]
                    obj = json.loads(substring)  # Parse the JSON string
                    model_instance = ResponseItem(**obj)  # Validate against Pydantic model
                    items.append(model_instance)
                except (json.JSONDecodeError, ValidationError) as e:
                    # raise Exception(f"Error parsing or validating JSON: {e}")
                    errors += 1

    return ResponseItems(items=items, parsing_errors=errors)
