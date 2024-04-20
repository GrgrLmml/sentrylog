from typing import List

from pydantic import BaseModel, field_validator

from config.config import SentryLogLevel


class ResponseItem(BaseModel):
    category: SentryLogLevel
    type: str
    origin: str
    relevant_log: str
    recommendation: str

    @field_validator('category', mode='before')
    def convert_category(cls, value):
        # Normalize the string input to title case to match the enum names
        normalized = value.strip().upper()
        try:
            # Attempt to map the normalized string to an enum value
            return SentryLogLevel[normalized]
        except KeyError:
            raise ValueError(f"Invalid category: {value}")


class ResponseItems(BaseModel):
    parsing_errors: int
    items: List[ResponseItem]
