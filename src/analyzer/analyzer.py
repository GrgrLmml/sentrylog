from analyzer.llm_model import LLMModel
from analyzer.models import LogChunk, Template

from config.config import SentryLogLevel, SENTRY_LOG_LEVEL
from handler.handlers import MessageSender
from parser.models import ResponseItems
from parser.parser import parse_llm_response


async def analyze(logs: LogChunk, template: Template, sender: MessageSender, model: LLMModel,
                  min_level: SentryLogLevel = SENTRY_LOG_LEVEL) -> None:
    message = await model.run_chunk(logs, template)
    parsed_output = parse_llm_response(message)

    filtered_items = [item for item in parsed_output.items if item.category >= min_level]

    sender.post_parsed_object(ResponseItems(items=filtered_items, parsing_errors=parsed_output.parsing_errors), logs)
