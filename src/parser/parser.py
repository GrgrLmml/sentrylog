import json
import re
from typing import Type

from pydantic import ValidationError, BaseModel

from parser.models import ResponseItem, ResponseItems


def parse_llm_response(text: str) -> ResponseItems:
    items = []

    errors = 0
    start_index = None  # Start index of a JSON object

    for i, char in enumerate(text):
        if char == '{':
            if start_index is not None:
                errors += 1
            start_index = i
        elif char == '}':
            if start_index is not None:
                substring = text[start_index:i + 1]
                start_index = None  # Reset start index
                try:
                    item = parse_custom_json(substring)
                    items.append(item)
                except ValidationError as e:
                    errors += 1
            else:
                errors += 1

    return ResponseItems(items=items, parsing_errors=errors)


def parse_custom_json(text: str) -> ResponseItem:
    fields = "|".join(ResponseItem.__fields__.keys())
    pattern = fr'(?:"({fields})"\s*:\s*"(.*?)(?:"(?=,\s*"(?:{fields})"\s*:)|"}}$))'

    matches = re.finditer(pattern, text, re.DOTALL)

    data = {}
    for match in matches:
        field, value = match.groups()
        data[field] = value

    try:
        return ResponseItem(**data)
    except ValidationError as e:
        raise e
