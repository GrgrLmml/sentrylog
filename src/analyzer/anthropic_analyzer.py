import json

from analyzer.models import LogChunk, Template, Prompt
from config.config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL_ID

import anthropic

from handler.handlers import MessageSender
from parser.parser import parse_llm_response

client = anthropic.Anthropic(
    api_key=ANTHROPIC_API_KEY,
)


def create_prompt(logs: LogChunk, template: Template) -> Prompt:
    prompt = template.template.replace("YOUR_LOG_CHUNK_HERE", "\n".join(logs.lines))
    return Prompt(text=prompt)


async def analyze(logs: LogChunk, template: Template, sender: MessageSender):
    # Analyze log lines
    print("Analyzing log lines:")
    prompt = create_prompt(logs, template)
    message = client.messages.create(
        model=ANTHROPIC_MODEL_ID,
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
    )
    # sender.post_message(message.content[0].text)
    pared_output = parse_llm_response(message.content[0].text)
    sender.post_parsed_object(pared_output, logs)
