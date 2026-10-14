import os
from dotenv import load_dotenv

# Load variables from .env if present
load_dotenv()

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# Primary free model with Paris-native French fluency, followed by capable free backups
DEFAULT_MODELS = [
    "mistralai/mistral-small-3.1-24b-instruct:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "google/gemini-2.0-flash-exp:free",
    "mistralai/mistral-7b-instruct:free"
]

# Gmail Configuration
GMAIL_USER = os.getenv("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", GMAIL_USER)

# French settings
FRENCH_LEVEL = os.getenv("FRENCH_LEVEL", "advanced")

# High-quality French RSS news feeds
RSS_FEEDS = [
    "https://www.france24.com/fr/rss",
    "https://www.lemonde.fr/international/rss_full.xml",
    "https://www.rfi.fr/fr/monde/rss"
]
