from abc import ABC, abstractmethod

from analyzer.models import LogChunk, Template


class LLMModel(ABC):

    def __init__(self, model_id: str):
        self.model_id = model_id

    def get_model(self) -> str:
        return self.model_id

    @abstractmethod
    async def run_chunk(self, chunk: LogChunk, template: Template) -> str:
        pass

