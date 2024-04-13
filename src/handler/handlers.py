from abc import ABC, abstractmethod

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class MessageSender(ABC):

    @abstractmethod
    def post_message(self, message: str) -> None:
        """
        Post a message to a channel.
        """
        pass


class Slack(MessageSender):
    def __init__(self, token: str, channel: str):
        self.client = WebClient(token=token)
        self.channel = channel

    def post_message(self, message: str) -> None:
        try:
            self.client.chat_postMessage(
                channel=self.channel,
                text=message,
                icon_emoji=":flashlight:",
                username="SentryLog",
            )
        except SlackApiError as e:
            print(f"Error posting to Slack channel {self.channel}: {e.response['error']}")
