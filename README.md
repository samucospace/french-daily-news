# 🇫🇷 Daily French Practice & Global News (GitHub Actions Cron)

An automated overnight newsletter delivered directly to your Gmail inbox. Powered by **OpenRouter free-tier LLMs** (native French-fluent Mistral models) and live RSS feeds from French international press (France 24, Le Monde, RFI).

---

## 📬 What Each Daily Email Delivers (Advanced C1/C2 Level)

1. **🌍 L'Actualité Internationale**: 3–4 major global headlines synthesized in elegant, journalistic French with advanced syntactic structures (subjonctif, participes présents, connecteurs soutenus).
2. **📖 Lexique & Tournures Choisies**: 4–5 advanced vocabulary terms and idioms with French definitions, English translations, and context sentences.
3. **💡 La Leçon de Langue du Jour**: A high-level paragraph lesson exploring nuanced grammar rules, stylistic distinctions, false friends, or high-register idiomatic expressions.
4. **🎯 Le Défi du Jour**: An interactive challenge (reformulation or sentence completion) with a clickable reveal for the solution.

---

## ⚙️ Architecture & Free Stack

- **Global News Source**: Live French RSS feeds (France 24, Le Monde, RFI) — *Free, real-time, no rate limits*.
- **LLM Engine**: OpenRouter Free Tier (default: `mistralai/mistral-small-3.1-24b-instruct:free` with automatic fallbacks to `llama-3.3-70b` and `gemini-2.0-flash`).
- **Templating**: Responsive HTML designed for Gmail, Apple Mail, and mobile screens.
- **Delivery**: Gmail SMTP using an App Password.
- **Automation / Cron**: GitHub Actions (`daily_digest.yml`) running daily overnight at $0 cost without needing your computer powered on.

---

## 🚀 Quick Setup Guide

### 1. Prerequisites & API Keys

1. **OpenRouter API Key** (Free):
   - Sign up / sign in at [openrouter.ai](https://openrouter.ai).
   - Go to **Keys** and create a key.
2. **Google App Password** (for Gmail SMTP):
   - Go to your Google Account: [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
   - *(Note: 2-Step Verification must be enabled on your Google account).*
   - Name the app password (e.g. `French Daily Digest`).
   - Copy the generated 16-character password (e.g. `abcd efgh ijkl mnop`).

---

### 2. Local Testing

To test locally on your machine:

```powershell
# 1. Activate the virtual environment
.\venv\Scripts\Activate.ps1

# 2. (Optional) Create .env from template and add your keys
copy .env.example .env

# 3. Test HTML generation without making LLM or SMTP calls
python main.py --mock --preview

# 4. Open preview.html in your browser to inspect the newsletter
Start-Process preview.html

# 5. Test with your real OpenRouter key (once added to .env)
python main.py --preview
```

---

### 3. Deploy to GitHub Actions (Daily Overnight Cron)

1. **Initialize Git & Push to GitHub**:
   ```powershell
   git init
   git add .
   git commit -m "Initial commit: French practice daily newsletter"
   git branch -M main
   # Add your remote and push:
   # git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   # git push -u origin main
   ```

2. **Add GitHub Secrets**:
   - In your GitHub repository, navigate to:
     **Settings** → **Secrets and variables** → **Actions** → **New repository secret**.
   - Add the following secrets:
     - `OPENROUTER_API_KEY`: Your OpenRouter API key.
     - `GMAIL_USER`: Your Gmail address (e.g. `user@gmail.com`).
     - `GMAIL_APP_PASSWORD`: The 16-character Google App Password.
     - `EMAIL_RECIPIENT`: (Optional) The email where you want to receive the digest (defaults to `GMAIL_USER`).

3. **Adjust the Overnight Schedule**:
   - The workflow is defined in `.github/workflows/daily_digest.yml`.
   - By default, it runs at `0 21 * * *` (21:00 UTC).
   - For example:
     - **05:00 AM UTC+8**: `cron: '0 21 * * *'` (21:00 UTC)
     - **06:00 AM EST (UTC-5)**: `cron: '0 11 * * *'` (11:00 UTC)
     - **07:00 AM CET (UTC+1)**: `cron: '0 6 * * *'` (06:00 UTC)
   - You can also test it immediately at any time by clicking **"Run workflow"** under the **Actions** tab in GitHub!

---

## 📂 Project Structure

```text
french-practice/
├── .github/
│   └── workflows/
│       └── daily_digest.yml     # GitHub Actions cron definition
├── src/
│   ├── __init__.py
│   ├── config.py                # Environment configs & model fallbacks
│   ├── news.py                  # Live RSS ingestion & deduplication
│   ├── llm.py                   # OpenRouter structured JSON generation
│   ├── mailer.py                # Jinja2 email renderer & Gmail SMTP sender
│   └── templates/
│       └── email.html           # Responsive HTML newsletter template
├── .env.example                 # Configuration template
├── main.py                      # CLI entrypoint
├── requirements.txt             # Project dependencies
└── preview.html                 # Generated HTML preview
```
