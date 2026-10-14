import json
import re
import requests
from typing import Dict, Any, List
from .config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, DEFAULT_MODELS, FRENCH_LEVEL

SYSTEM_PROMPT = """You are a distinguished French linguist, journalist, and pedagogue.
Your objective is to produce an elegant daily French newsletter for an advanced French learner (Level C1/C2).

You will receive a list of the latest global news articles. Your task is to:
1. Select the top 3-4 most globally significant stories.
2. Rewrite and synthesize them in sophisticated, journalistic French with rich vocabulary, varied syntax (e.g., participes présents, gérondif, passif, subjonctif, inversion, connecteurs logiques soutenus).
3. Select 4-5 advanced vocabulary terms or idioms (des expressions idiomatiques ou termes soutenus) relevant to the news stories. Include definition in French, English translation, and an example sentence.
4. Craft a daily paragraph lesson ("La Leçon du Jour") explaining a subtle grammatical rule, a stylistic nuance of the French language, a false friend, or a high-register idiom.
5. Provide a quick daily challenge ("Le Défi du Jour") - a sentence to reformulate or a fill-in-the-blank requiring advanced linguistic precision, along with the answer.

Output MUST be strictly valid JSON matching this exact schema:
{
  "greeting": "Chers lecteurs / Bonjour à tous, ...",
  "news_items": [
    {
      "title_fr": "Titre soutenu en français",
      "summary_fr": "Résumé analytique et précis en 2 à 3 phrases au style soigné.",
      "source": "Nom de la source"
    }
  ],
  "vocabulary": [
    {
      "term": "mot ou locution (ex: l'achoppement (m.))",
      "definition_fr": "Définition concise en français soutenu",
      "translation_en": "English translation",
      "example_sentence": "Phrase d'illustration percutante."
    }
  ],
  "lesson_of_the_day": {
    "topic": "Titre du point de langue ou de style",
    "paragraph": "Paragraphe explicatif approfondi sur la nuance linguistique, les règles d'usage et un exemple concret."
  },
  "challenge": {
    "question": "Question ou phrase à compléter/reformuler",
    "answer": "Réponse détaillée avec justification stylistique ou grammaticale"
  }
}
"""

def extract_json(text: str) -> Dict[str, Any]:
    """Extract valid JSON from LLM response text, stripping markdown code fences if present."""
    if not text:
        raise ValueError("Cannot extract JSON from empty or null response.")
    text = text.strip()
    # Match ```json ... ``` or ``` ... ```
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if fence_match:
        text = fence_match.group(1).strip()
    return json.loads(text)

def generate_newsletter_content(articles: List[Dict[str, str]], api_key: str = None) -> Dict[str, Any]:
    """
    Generate the newsletter JSON payload via OpenRouter using free models with fallback.
    """
    key = api_key or OPENROUTER_API_KEY
    if not key:
        raise ValueError("OPENROUTER_API_KEY is not set. Please provide it in your .env or environment.")

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/french-practice-daily",
        "X-Title": "French Practice Daily Newsletter"
    }

    user_prompt = f"Target Level: {FRENCH_LEVEL.upper()} (C1/C2)\n\n"
    user_prompt += "Here are today's latest global news stories:\n"
    for idx, item in enumerate(articles, 1):
        user_prompt += f"{idx}. [{item['source']}] {item['title']}\n"
        if item.get("summary"):
            user_prompt += f"   Détails: {item['summary']}\n"

    last_error = None
    for model in DEFAULT_MODELS:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.5,
            "response_format": {"type": "json_object"}
        }

        try:
            print(f"-> Calling OpenRouter model: {model}...")
            response = requests.post(OPENROUTER_BASE_URL, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                msg = data["choices"][0]["message"]
                raw_content = msg.get("content") or msg.get("reasoning")
                if not raw_content:
                    raise ValueError(f"Model {model} returned an empty message payload.")
                parsed = extract_json(raw_content)
                print(f"[OK] Successfully generated content using {model}")
                return parsed
            else:
                print(f"[Warning] Model {model} returned status {response.status_code}: {response.text}")
                last_error = f"Status {response.status_code}: {response.text}"
        except Exception as e:
            print(f"[Warning] Failed with model {model}: {e}")
            last_error = str(e)

    raise RuntimeError(f"All free OpenRouter models failed. Last error: {last_error}")
