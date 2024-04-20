import os
from enum import Enum, IntEnum
import logging
from logging.config import dictConfig

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

dictConfig(logging_config)

logger = logging.getLogger(__name__)

TEMPLATE_PATH = 'templates/'
TEMPLATE = os.getenv('TEMPLATE', 'nginx.md')
CHUNK_SIZE = 100
CHUNK_OVERLAP = 10
CONTAINER_TO_WATCH = os.getenv('CONTAINER_TO_WATCH', 'nginx')

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL_ID = os.getenv("ANTHROPIC_MODEL_ID", "claude-3-haiku-20240307")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_ID = os.getenv("GROQ_MODEL_ID", "mixtral-8x7b-32768")

SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")


class ModelType(Enum):
    GROQ = "groq"
    ANTHROPIC = "anthropic"


MODEL_TO_USE = os.getenv("MODEL_TO_USE", ModelType.ANTHROPIC.value)


class SentryLogLevel(IntEnum):
    INFO = 1
    WARNING = 2
    CRITICAL = 3


def get_log_level(level_str: str) -> SentryLogLevel:
    # Normalize the input string to match the Enum naming convention
    normalized_level = level_str.strip().upper()
    try:
        # Return the corresponding Enum member
        return SentryLogLevel[normalized_level]
    except KeyError:
        # If the provided level is not valid, default to INFO
        print(f"Warning: Invalid LOG_LEVEL '{level_str}'. Defaulting to INFO.")
        return SentryLogLevel.INFO


env_log_level = os.getenv("SENTRY_LOG_LEVEL", "INFO")
SENTRY_LOG_LEVEL = get_log_level(env_log_level)
