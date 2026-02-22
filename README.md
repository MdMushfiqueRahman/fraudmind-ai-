# FraudMind AI

AI-powered social engineering and phishing analyzer with a dark cybersecurity dashboard (SOC-style UI). Django app that runs locally; no login or database history required.

## Setup (Windows)

```powershell
cd fraudmind-ai
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and set your OpenAI API key:

```
OPENAI_API_KEY=sk-your-key-here
```

Then:

```powershell
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Secrets & environment

- **Never commit real keys.** All secrets are loaded from environment variables.
- **`.env`** is in `.gitignore` and is never uploaded. Use it only for local development.
- **`.env.example`** is the template (no real values). Copy to `.env` and fill in:
  - `OPENAI_API_KEY` — required for analysis ([get one](https://platform.openai.com/api-keys)).
  - `DJANGO_SECRET_KEY` — optional for local dev; **set in production**.
- Before pushing to GitHub, confirm no `.env` or hardcoded keys are in the repo.

## Usage

- **Home:** Paste a message, choose type (email, SMS, etc.), click **Analyze** or **Load Demo** to try sample messages.
- **Analyze:** POST-only; calls OpenAI and shows the **Risk Dashboard** with risk level, scam type, pressure score, red flags, safe reply, and action plan.
- **Dashboard:** Dark SOC-style UI with KPI cards, donut chart, tactic bars, and copyable safe reply.

## Demo messages (Load Demo)

The app includes at least 8 demo messages, for example:

- Account suspended / verify link (phishing)
- Gift card / prize claim
- Romance scam (oil rig, gift card)
- Apple ID / sign-in alert
- IRS / tax debt
- Package delivery / re-delivery fee
- Work-from-home job / bank details
- Tech support / virus remote fix

## API / model

- **OpenAI Responses API:** `client.responses.create(...)` with model `gpt-4.1-mini`. If that model is not available, change in `detector/views.py` to `gpt-4o-mini` (or another model you have access to).
- Output is strict JSON with: `risk_level`, `scam_type`, `pressure_score`, `confidence`, `primary_tactics`, `red_flags`, `manipulation_tactics`, `one_sentence_summary`, `safe_reply`, `what_to_do`, `what_not_to_do`.

## Error handling

- **Missing API key:** Friendly message on home with instructions to add `.env`.
- **OpenAI returns non-JSON:** Friendly error on home; raw response is printed to the server console.

## Disclaimer

**AI-based assessment. Verify with official sources.** This tool is for awareness and education; always confirm through official channels before taking action.

## Exact Windows commands (copy-paste)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Then paste your key into `.env`, and run:

```powershell
python manage.py migrate
python manage.py runserver
```
