import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any
from .config import GMAIL_USER, GMAIL_APP_PASSWORD, EMAIL_RECIPIENTS
from typing import Dict, Any, List

FRENCH_MONTHS = [
    "", "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre"
]

FRENCH_DAYS = [
    "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"
]

def get_french_date(dt: datetime = None) -> str:
    """Format datetime into standard elegant French date string."""
    if dt is None:
        dt = datetime.now()
    day_name = FRENCH_DAYS[dt.weekday()]
    month_name = FRENCH_MONTHS[dt.month]
    return f"{day_name} {dt.day} {month_name} {dt.year}"

def render_email_html(content: Dict[str, Any], unique_id: str = None) -> str:
    """Render HTML email from Jinja2 template."""
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("email.html")
    
    date_str = get_french_date()
    uid = unique_id or f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
    return template.render(content=content, date_str=date_str, unique_id=uid)

def send_daily_email(content: Dict[str, Any], preview_file: str = None, preview_only: bool = False) -> bool:
    """
    Render and send the email via Gmail SMTP to all configured recipients.
    If preview_only is True, save to preview_file and return without connecting to SMTP.
    """
    if not isinstance(content, dict) or not content.get("news_items"):
        error_msg = f"Cannot dispatch newsletter: 'news_items' is missing or empty (keys: {list(content.keys()) if isinstance(content, dict) else 'none'})"
        print(f"[Error] {error_msg}")
        raise ValueError(error_msg)

    import uuid
    from email.utils import make_msgid
    unique_id = uuid.uuid4().hex[:8]

    html_body = render_email_html(content, unique_id=unique_id)

    if preview_file:
        with open(preview_file, "w", encoding="utf-8") as f:
            f.write(html_body)
        print(f"[OK] Saved email preview to: {preview_file}")

    if preview_only:
        print("[Preview Mode] Skipping SMTP delivery.")
        return True

    clean_password = GMAIL_APP_PASSWORD.strip().strip("'\"").replace(" ", "")
    
    if not GMAIL_USER or not clean_password:
        print("[Notice] GMAIL_USER or GMAIL_APP_PASSWORD not set. Skipping SMTP delivery.")
        print("Set these in your .env or GitHub Secrets to enable automatic emailing.")
        return False

    if "your_16_char" in clean_password.lower():
        print("[Error] GMAIL_APP_PASSWORD is still set to the placeholder text!")
        print("Please replace it with your 16-character Google App Password in .env")
        print("Generate one at: https://myaccount.google.com/apppasswords")
        return False

    if len(clean_password) != 16:
        print(f"[Warning] Google App Passwords are 16 letters long (detected {len(clean_password)} chars).")

    recipients = EMAIL_RECIPIENTS
    if not recipients:
        print("[Notice] No recipient email specified. Defaulting to GMAIL_USER.")
        recipients = [GMAIL_USER]

    date_str = get_french_date()
    
    # Subject line with top headline up front to guarantee unique threads in Gmail
    first_item = content["news_items"][0]
    headline = first_item.get("title_fr", "").strip()
    if len(headline) > 55:
        headline = headline[:52] + "..."

    subject = f"La Gazette : {headline} ({date_str})"

    # Diagnostic logging
    print("-> Newsletter summary to dispatch:")
    print(f"   Subject: {subject}")
    print(f"   News items count: {len(content.get('news_items', []))}")
    for idx, item in enumerate(content.get("news_items", []), 1):
        print(f"     {idx}. {item.get('title_fr')}")
    print(f"   Lesson topic: {content.get('lesson_of_the_day', {}).get('topic')}")
    print(f"   Vocabulary count: {len(content.get('vocabulary', []))}")
    print(f"   HTML payload size: {len(html_body)} bytes")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"La Gazette Francaise <{GMAIL_USER}>"
    msg["To"] = ", ".join(recipients)
    msg["Message-ID"] = make_msgid(domain="gazette.francophone")
    msg["Auto-Submitted"] = "auto-generated"
    msg["X-Entity-Ref-ID"] = unique_id

    # Fallback plain text
    plain_text = f"La Gazette du Jour - {date_str}\n\n"
    for item in content.get("news_items", []):
        plain_text += f"* {item.get('title_fr')}\n  {item.get('summary_fr')}\n\n"
    if content.get("lesson_of_the_day"):
        plain_text += f"\nLecon du Jour: {content['lesson_of_the_day'].get('topic')}\n"
        plain_text += f"{content['lesson_of_the_day'].get('paragraph')}\n"

    msg.attach(MIMEText(plain_text, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    recipients_str = ", ".join(recipients)
    print(f"-> Sending email to {len(recipients)} recipient(s): {recipients_str} via Gmail SMTP...")

    # Connect via Port 587 (STARTTLS) or fallback to Port 465 (SSL)
    server = None
    try:
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
            server.ehlo()
            server.starttls()
            server.ehlo()
        except Exception:
            # Fallback to SSL port 465
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15)
            server.ehlo()

        server.login(GMAIL_USER, clean_password)
        server.sendmail(GMAIL_USER, recipients, msg.as_string())
        server.quit()
        print(f"[OK] Email successfully sent to {recipients_str}!")
        return True
    except smtplib.SMTPServerDisconnected:
        print("[Error] Gmail closed the connection unexpectedly.")
        print("This typically means Google rejected the login credentials.")
        print("Make sure you are using an official 16-character Google App Password (not your normal Google account password).")
        print("Create one here: https://myaccount.google.com/apppasswords")
        return False
    except smtplib.SMTPAuthenticationError as e:
        print(f"[Error] Gmail authentication failed: {e}")
        print("Verify your GMAIL_USER and 16-character GMAIL_APP_PASSWORD.")
        return False
    except Exception as e:
        print(f"[Error] Failed to send email via Gmail SMTP: {e}")
        raise e
