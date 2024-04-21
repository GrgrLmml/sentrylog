import pytest

from analyzer.models import LogChunk
from config.config import SentryLogLevel
from parser.models import ResponseItems, ResponseItem
from connectors.connectors import SlackConnector


# class ResponseItem(BaseModel):
#     category: SentryLogLevel
#     type: str
#     origin: str
#     relevant_log: str
#     recommendation: str

@pytest.fixture
def log_data() -> (ResponseItems, LogChunk):
    return (ResponseItems(items=[
        ResponseItem(category="INFO", type="Type1", origin="Origin1", relevant_log="Log1",
                     recommendation="Recommendation1"),
        ResponseItem(category="Critical", type="Type2", origin="Origin2", relevant_log="Log2",
                     recommendation="Recommendation2"),
        ResponseItem(category="warning", type="Type3", origin="Origin3", relevant_log="Log3",
                     recommendation="Recommendation3"),
    ], parsing_errors=2),
            LogChunk(start_time="2024-01-01 00:00:00", end_time="2024-01-01 00:01:23", lines=["Line1", "Line2"]))


def test_markdown_formatter(log_data):
    md = SlackConnector.format_to_markdown(*log_data)
    assert md == """*Report:*

*Start time:* 2024-01-01 00:00:00
*End time:* 2024-01-01 00:01:23

✅ *INFO*
*Type:* Type1
*Origin:* Origin1
*Relevant Log:* Log1
*Recommendation:* Recommendation1

🔥 *CRITICAL*
*Type:* Type2
*Origin:* Origin2
*Relevant Log:* Log2
*Recommendation:* Recommendation2

⚠️ *WARNING*
*Type:* Type3
*Origin:* Origin3
*Relevant Log:* Log3
*Recommendation:* Recommendation3

*Parsing Errors:* 2
"""


