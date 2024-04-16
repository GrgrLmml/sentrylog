from typing import List

from pydantic import BaseModel

enum = ["Info", "Warn", "Critical"]


class ResponseItem(BaseModel):
    category: str
    type: str
    origin: str
    relevant_log: str
    recommendation: str


class ResponseItems(BaseModel):
    parsing_errors: int
    items: List[ResponseItem]
