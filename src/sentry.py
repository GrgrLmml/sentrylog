import asyncio

import docker
from docker.errors import NotFound

from analyzer.analyzer import analyze
from analyzer.anthropic_model import AnthropicModel
from analyzer.groq_model import GroqModel
from analyzer.llm_model import LLMModel
from config.config import CHUNK_OVERLAP, CHUNK_SIZE, TEMPLATE, TEMPLATE_PATH, SLACK_CHANNEL, SLACK_TOKEN, \
    CONTAINER_TO_WATCH, logger
from analyzer.models import Template
from handler.handlers import Slack, MessageSender
from utils.prepocessing import log_chunk_preprocessor

client = docker.from_env()


def find_container(name: str) -> str:
    logger.info(f"Searching for a container with name containing '{name}'...")
    for container in client.containers.list():
        if name.lower() in container.name.lower():
            logger.info(f"Found container: {container.name}")
            return container.name
    raise Exception(f"Container with name containing '{name}' not found.")


def load_template() -> Template:
    with open(TEMPLATE_PATH + TEMPLATE, 'r', encoding='utf-8') as file:
        content = file.read()
    return Template(name=TEMPLATE, template=content)


async def watch_container_logs(container_name: str, template: Template, sender: MessageSender, model: LLMModel):
    try:
        container = client.containers.get(container_name)
        logger.info(f"Starting to watch logs from {container.name}...")
        log_lines = []
        for line in container.logs(stream=True):
            log_lines.append(line.decode().strip())

            if len(log_lines) >= CHUNK_SIZE:

                chunk = log_chunk_preprocessor(log_lines[:CHUNK_SIZE])
                await analyze(chunk, template, sender, model)
                log_lines = log_lines[CHUNK_SIZE - CHUNK_OVERLAP:]  # Retain 'm' lines for overlap

    except NotFound:
        raise Exception(f"Container with name '{container_name}' not found.")


async def main():
    nginx = find_container(CONTAINER_TO_WATCH)
    template = load_template()
    sender = Slack(SLACK_TOKEN, SLACK_CHANNEL)
    model = GroqModel()
    await watch_container_logs(nginx, template, sender, model)


if __name__ == "__main__":
    asyncio.run(main())
