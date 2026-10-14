import re
import html
import feedparser
from typing import List, Dict, Any
from .config import RSS_FEEDS

def clean_html(raw_html: str) -> str:
    """Strip HTML tags and unescape HTML entities."""
    if not raw_html:
        return ""
    clean_text = re.sub(r"<[^>]+>", "", raw_html)
    return html.unescape(clean_text).strip()

def fetch_latest_headlines(max_items: int = 10) -> List[Dict[str, str]]:
    """
    Fetch and deduplicate the latest global news from configured RSS feeds.
    """
    all_articles = []
    seen_titles = set()

    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            source_name = getattr(feed.feed, "title", "Actualités").split("-")[0].strip()
            
            for entry in feed.entries:
                title = clean_html(getattr(entry, "title", ""))
                summary = clean_html(getattr(entry, "summary", getattr(entry, "description", "")))
                link = getattr(entry, "link", "")
                
                # Deduplication by title
                normalized_title = title.lower().strip()
                if not normalized_title or normalized_title in seen_titles:
                    continue
                seen_titles.add(normalized_title)

                all_articles.append({
                    "source": source_name,
                    "title": title,
                    "summary": summary,
                    "link": link
                })

                if len(all_articles) >= max_items:
                    break
        except Exception as e:
            print(f"[Warning] Failed to fetch feed {url}: {e}")

        if len(all_articles) >= max_items:
            break

    return all_articles
