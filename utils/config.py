import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON", "")  # path or content
NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

DEFAULT_WEEKLY_HOURS = int(os.getenv("DEFAULT_WEEKLY_HOURS", "8"))
DEFAULT_TOTAL_WEEKS = int(os.getenv("DEFAULT_TOTAL_WEEKS", "12"))
