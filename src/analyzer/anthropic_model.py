import json

from analyzer.llm_model import LLMModel
from analyzer.models import LogChunk, Template, Prompt
from config.config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL_ID, logger

from anthropic import Anthropic

from handler.handlers import MessageSender
from parser.parser import parse_llm_response


def create_prompt(logs: LogChunk, template: Template) -> Prompt:
    prompt = template.template.replace("YOUR_LOG_CHUNK_HERE", "\n".join(logs.lines))
    return Prompt(text=prompt)


class AnthropicModel(LLMModel):
    def __init__(self, model_id: str = ANTHROPIC_MODEL_ID):
        super().__init__(model_id)
        self.client = Anthropic()

    async def run_chunk(self, chunk: LogChunk, template: Template) -> str:
        prompt = create_prompt(chunk, template)
        return self.client.messages.create(
            model=self.model_id,
            max_tokens=4096,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": [
                        prompt.dict()
                    ]
                }
            ]
        ).content[0].text

