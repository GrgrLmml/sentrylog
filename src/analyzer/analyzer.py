from analyzer.llm_model import LLMModel
from analyzer.models import LogChunk, Template
from handler.handlers import MessageSender
from parser.parser import parse_llm_response


async def analyze(logs: LogChunk, template: Template, sender: MessageSender, model: LLMModel) -> None:
    message = await model.run_chunk(logs, template)
    parsed_output = parse_llm_response(message)
    sender.post_parsed_object(parsed_output, logs)
