import asyncio

import docker
from docker.errors import NotFound

from config.config import CHUNK_OVERLAP, CHUNK_SIZE, TEMPLATE, TEMPLATE_PATH, SLACK_CHANNEL, SLACK_TOKEN
from analyzer.models import Template, LogChunk
from analyzer.anthropic_analyzer import analyze
from handler.handlers import Slack, MessageSender

client = docker.from_env()


def find_nginx() -> str:
    print("Listing all running containers:")
    for container in client.containers.list():
        if 'nginx' in container.name:
            return container.name
    raise Exception("Nginx container not found.")


def load_template() -> Template:
    with open(TEMPLATE_PATH + TEMPLATE, 'r', encoding='utf-8') as file:
        content = file.read()
    return Template(name=TEMPLATE, template=content)


async def watch_container_logs(container_name: str, template: Template, sender: MessageSender):
    try:
        container = client.containers.get(container_name)
        print(f"Starting to watch logs from {container.name}...")
        log_lines = []
        for line in container.logs(stream=True):
            log_lines.append(line.decode().strip())

            if len(log_lines) >= CHUNK_SIZE:
                chunk = LogChunk(lines=log_lines[:CHUNK_SIZE])
                await analyze(chunk, template, sender)
                log_lines = log_lines[CHUNK_SIZE - CHUNK_OVERLAP:]  # Retain 'm' lines for overlap

    except NotFound:
        print(f"Container {container_name} not found.")


async def main():
    nginx = find_nginx()
    template = load_template()
    sender = Slack(SLACK_TOKEN, SLACK_CHANNEL)
    await watch_container_logs(nginx, template, sender)


if __name__ == "__main__":
    asyncio.run(main())
