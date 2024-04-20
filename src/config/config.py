import os
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
        'file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'mode': 'a',  # Append mode
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file'],
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
