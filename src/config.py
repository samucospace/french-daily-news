import os
from pathlib import Path
from dotenv import load_dotenv

# Explicitly load project root .env with override enabled
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# Active free models on OpenRouter
# "openrouter/free" automatically load-balances across currently active free endpoints
CUSTOM_MODEL = os.getenv("OPENROUTER_MODEL")
DEFAULT_MODELS = [m for m in [
    CUSTOM_MODEL,
    "openrouter/free",
    "google/gemma-4-31b-it:free",
    "google/gemma-4-26b-a4b-it:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "nvidia/nemotron-3.5-lightning:free"
] if m]

# Gmail Configuration
GMAIL_USER = os.getenv("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")

# Support single or comma/semicolon-separated multiple recipients
def parse_recipients() -> list[str]:
    raw = os.getenv("EMAIL_RECIPIENTS") or os.getenv("EMAIL_RECIPIENT") or GMAIL_USER
    if not raw:
        return []
    import re
    return [email.strip() for email in re.split(r"[,;]+", raw) if email.strip()]

EMAIL_RECIPIENTS = parse_recipients()

# French settings
FRENCH_LEVEL = os.getenv("FRENCH_LEVEL", "advanced")

# High-quality French RSS news feeds
RSS_FEEDS = [
    "https://www.france24.com/fr/rss",
    "https://www.lemonde.fr/international/rss_full.xml",
    "https://www.rfi.fr/fr/monde/rss"
]
