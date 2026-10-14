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

def render_email_html(content: Dict[str, Any]) -> str:
    """Render HTML email from Jinja2 template."""
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("email.html")
    
    date_str = get_french_date()
    return template.render(content=content, date_str=date_str)

def send_daily_email(content: Dict[str, Any], preview_file: str = None, preview_only: bool = False) -> bool:
    """
    Render and send the email via Gmail SMTP to all configured recipients.
    If preview_only is True, save to preview_file and return without connecting to SMTP.
    """
    html_body = render_email_html(content)

    if preview_file:
        with open(preview_file, "w", encoding="utf-8") as f:
            f.write(html_body)
        print(f"[OK] Saved email preview to: {preview_file}")

    if preview_only:
        print("[Preview Mode] Skipping SMTP delivery.")
        return True

    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("[Notice] GMAIL_USER or GMAIL_APP_PASSWORD not set. Skipping SMTP delivery.")
        print("Set these in your .env or GitHub Secrets to enable automatic emailing.")
        return False

    recipients = EMAIL_RECIPIENTS
    if not recipients:
        print("[Notice] No recipient email specified. Defaulting to GMAIL_USER.")
        recipients = [GMAIL_USER]

    date_str = get_french_date()
    
    # Subject line
    first_title = ""
    if content.get("news_items"):
        first_title = f" : {content['news_items'][0].get('title_fr', '')}"
        # Truncate if too long for subject
        if len(first_title) > 60:
            first_title = first_title[:57] + "..."

    subject = f"La Gazette du Jour ({date_str}){first_title}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"La Gazette Francaise <{GMAIL_USER}>"
    msg["To"] = ", ".join(recipients)

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
    try:
        # Connect to Gmail SMTP using SSL (port 465)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD.replace(" ", ""))
            server.sendmail(GMAIL_USER, recipients, msg.as_string())
        print(f"[OK] Email successfully sent to {recipients_str}!")
        return True
    except Exception as e:
        print(f"[Error] Failed to send email via Gmail SMTP: {e}")
        raise e
