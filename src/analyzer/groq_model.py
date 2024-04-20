from groq import Groq

from analyzer.llm_model import LLMModel
from analyzer.models import LogChunk, Template
from config.config import GROQ_MODEL_ID, logger


# client = Groq()
def create_prompt(logs: LogChunk, template: Template) -> str:
    prompt = template.template.replace("YOUR_LOG_CHUNK_HERE", "\n".join(logs.lines))
    return prompt


class GroqModel(LLMModel):

    def __init__(self, model_id: str = GROQ_MODEL_ID):
        super().__init__(model_id)
        self.client = Groq()

    async def run_chunk(self, chunk: LogChunk, template: Template) -> str:
        message = create_prompt(chunk, template)
        messages = [{
            "role": "user",
            "content": message
        }]

        return self.client.chat.completions.create(model=self.model_id, max_tokens=4096, temperature=1, stream=False,
                                                   messages=messages).choices[0].message.content
