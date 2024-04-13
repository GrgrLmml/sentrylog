from typing import List

from pydantic import BaseModel


class LogChunk(BaseModel):
    lines: List[str]


class Template(BaseModel):
    name: str
    template: str


class Prompt(BaseModel):
    type: str = "text"
    text: str
