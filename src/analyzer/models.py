from typing import List

from pydantic import BaseModel


class LogChunk(BaseModel):
    start_time: str
    end_time: str
    lines: List[str]


class Template(BaseModel):
    name: str
    template: str


class Prompt(BaseModel):
    type: str = "text"
    text: str
