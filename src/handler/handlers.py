from abc import ABC, abstractmethod

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from analyzer.models import LogChunk
from parser.models import ResponseItems


class MessageSender(ABC):

    @abstractmethod
    def post_message(self, message: str) -> None:
        """
        Post a message to a channel.
        """
        pass

    @abstractmethod
    def post_parsed_object(self, response_items: ResponseItems, logs: LogChunk) -> None:
        """
        Post a parsed object to a channel.
        """
        pass


class Slack(MessageSender):
    def __init__(self, token: str, channel: str):
        self.client = WebClient(token=token)
        self.channel = channel

    def post_message(self, message: str, mrkdwn=False) -> None:
        try:
            self.client.chat_postMessage(
                channel=self.channel,
                text=message,
                icon_emoji=":flashlight:",
                username="SentryLog",
                mrkdwn=mrkdwn,
            )
        except SlackApiError as e:
            print(f"Error posting to Slack channel {self.channel}: {e.response['error']}")

    def post_parsed_object(self, response_items: ResponseItems, logs: LogChunk) -> None:
        markdown_text = self.format_to_markdown(response_items, logs)
        self.post_message(markdown_text, mrkdwn=True)

    @staticmethod
    def format_to_markdown(response_items: ResponseItems, logs: LogChunk) -> str:
        # Emoji definitions for different categories
        emoji_map = {
            "Info": "✅",
            "Warning": "⚠️",
            "Critical": "🔥"
        }

        # Start the markdown text with a section header.
        markdown_text = "*Report:*\n\n"
        markdown_text += "*Start time:* " + logs.start_time + "\n"
        markdown_text += "*End time:* " + logs.end_time + "\n\n"

        for item in response_items.items:
            # Assign emoji based on category
            emoji = emoji_map.get(item.category, "ℹ️")  # Default emoji if category is not found

            # Add the details of each item using Slack's mrkdwn format
            markdown_text += f"{emoji} *{item.category}*\n"
            markdown_text += f"*Type:* {item.type}\n"
            markdown_text += f"*Origin:* {item.origin}\n"
            markdown_text += f"*Relevant Log:* {item.relevant_log}\n"
            markdown_text += f"*Recommendation:* {item.recommendation}\n\n"

        # Append parsing errors at the end of the report
        markdown_text += f"*Parsing Errors:* {response_items.parsing_errors}\n"

        return markdown_text
