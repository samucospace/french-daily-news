# 🇫🇷 French Daily News & Practice Newsletter

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Daily Cron](https://img.shields.io/badge/cron-GitHub%20Actions-green.svg)](.github/workflows/daily_digest.yml)

An automated daily overnight newsletter delivered directly to your email inbox, completely in French. It curates the latest global news headlines from leading French press, synthesizes them with sophisticated journalistic French, and delivers a bite-sized French lesson and language challenge tailored for advanced learners.

Powered by **OpenRouter free-tier LLMs** (with automatic routing & multi-model failover) and **GitHub Actions** for zero-cost, serverless scheduling.

---

## 📬 What Each Daily Edition Delivers

Each daily email is delivered before morning wake-up with:

1. **🌍 L'Actualité Internationale**: 3–4 major global headlines synthesized in elegant, high-register French (Level C1/C2) using varied grammatical structures (*gérondif*, *subjonctif*, *participes présents*, advanced logical connectors).
2. **📖 Lexique & Tournures Choisies**: 4–5 advanced vocabulary terms, false friends, and idioms extracted directly from the day's stories, complete with grammatical gender, French definitions, English translations, and illustrative sentences.
3. **💡 La Leçon de Langue du Jour**: A focused paragraph lesson breaking down subtle grammar rules, nuances of register, or stylistic distinctions.
4. **🎯 Le Défi du Jour**: An interactive linguistic challenge (sentence completion or reformulation) with a clickable spoiler reveal for the solution.

---

## 🛠️ Technology Stack (100% Free Tier)

| Component | Technology | Description |
| :--- | :--- | :--- |
| **News Source** | French RSS Feeds | Real-time global coverage from France 24, Le Monde, and RFI. Completely free with zero rate limits. |
| **LLM Engine** | [OpenRouter](https://openrouter.ai) Free Tier | Automatic load balancing via `openrouter/free` with seamless failover to models like Gemma and Nemotron. |
| **Email Delivery** | Gmail SMTP (Port 587 STARTTLS) | Delivers formatted multi-part HTML & plain-text emails via your personal Google account. |
| **Automation** | GitHub Actions | Scheduled cron job running every night in the cloud at $0 cost—no computer needs to stay powered on. |
| **Templating** | Jinja2 & Mobile-Ready CSS | Responsive email template tested across desktop, mobile, Gmail, and Apple Mail. |

---

## 🚀 Quickstart & Local Setup

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/samucospace/french-daily-news.git
cd french-daily-news

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example file to `.env`:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```ini
# OpenRouter API Key (Free tier at https://openrouter.ai/keys)
OPENROUTER_API_KEY=sk-or-v1-...

# Gmail SMTP Configuration
GMAIL_USER=your_email@gmail.com
# 16-character Google App Password (https://myaccount.google.com/apppasswords)
GMAIL_APP_PASSWORD=abcdefghijklmnop

# Single recipient or comma-separated list of multiple recipients:
EMAIL_RECIPIENTS=your_email@gmail.com, friend@example.com

# Target French proficiency level (advanced by default: C1/C2)
FRENCH_LEVEL=advanced
```

> **How to get a Google App Password**:
> 1. Ensure 2-Step Verification is turned on in your [Google Account](https://myaccount.google.com/signinoptions/two-step-verification).
> 2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
> 3. Enter a label (e.g. `French Daily News`) and click **Create**.
> 4. Copy the generated 16-character code into `GMAIL_APP_PASSWORD`.

### 3. Run Locally

```bash
# Preview HTML generation without making LLM or email calls (dry run):
python main.py --mock --preview

# Generate today's live issue and save HTML to preview.html:
python main.py --preview

# Run the full pipeline and dispatch the live email:
python main.py
```

---

## ⏰ Cloud Automation (GitHub Actions Cron)

To have your newsletter dispatched automatically every morning at no cost:

### 1. Push to your GitHub Repository

```bash
git remote add origin https://github.com/samucospace/french-daily-news.git
git branch -M main
git push -u origin main
```

### 2. Add Repository Secrets

In your GitHub repository:
1. Navigate to **Settings** → **Secrets and variables** → **Actions** → **New repository secret**.
2. Add the following secrets:

| Secret Name | Value |
| :--- | :--- |
| `OPENROUTER_API_KEY` | Your OpenRouter API key |
| `GMAIL_USER` | Your Gmail address (`you@gmail.com`) |
| `GMAIL_APP_PASSWORD` | The 16-character Google App Password |
| `EMAIL_RECIPIENTS` | Recipient address(es) (e.g. `user1@gmail.com, user2@gmail.com`) |

### 3. Adjust the Overnight Schedule

The workflow is located in [`.github/workflows/daily_digest.yml`](.github/workflows/daily_digest.yml). By default, it runs every night at **21:00 UTC** (5:00 AM UTC+8):

```yaml
on:
  schedule:
    # 21:00 UTC corresponds to early morning wake-up in UTC+8
    - cron: '0 21 * * *'
  workflow_dispatch: # Allows manual trigger anytime from GitHub Actions tab
```

You can customize the cron schedule to match your local timezone:
- **05:00 AM UTC+8**: `0 21 * * *`
- **06:00 AM EST (UTC-5)**: `0 11 * * *`
- **07:00 AM CET (UTC+1)**: `0 6 * * *`

You can also trigger a manual dispatch at any time by going to the **Actions** tab on GitHub and clicking **"Run workflow"**.

---

## 📁 Repository Structure

```text
french-daily-news/
├── .github/
│   └── workflows/
│       └── daily_digest.yml     # Scheduled GitHub Actions cron workflow
├── src/
│   ├── __init__.py
│   ├── config.py                # Environment configs, model routing & fallback logic
│   ├── news.py                  # Live RSS ingestion from French international press
│   ├── llm.py                   # Structured OpenRouter prompts & JSON validation
│   ├── mailer.py                # Responsive Jinja2 renderer & SMTP transport (STARTTLS)
│   └── templates/
│       └── email.html           # Polished, responsive HTML email layout
├── .env.example                 # Template for required environment variables
├── .gitignore                   # Excludes .env, virtualenv, and test previews
├── LICENSE                      # MIT License
├── main.py                      # Main orchestrator CLI
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
