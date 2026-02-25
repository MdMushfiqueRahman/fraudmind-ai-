<p align="center">
  <img src="https://github.com/user-attachments/assets/edaa9be3-633a-42d4-8b8e-a26fbedbad86" 
       width="800" 
       alt="FraudMind AI Banner" />
</p>


<h1 align="center">
  <i>See through social engineering before it sees through you!</i>
</h1>

<h4 align="center">
  Analyze suspicious messages using structured AI risk assessment with a professional SOC-style cybersecurity dashboard.
</h4>

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![OpenAI API](https://img.shields.io/badge/OpenAI-Responses_API-412991?style=for-the-badge&logo=openai&logoColor=white)
![JSON Schema](https://img.shields.io/badge/JSON-Structured_Output-blue?style=for-the-badge)
![Architecture](https://img.shields.io/badge/Architecture-MTV-informational?style=for-the-badge)
![Security](https://img.shields.io/badge/Security-Environment_Variables-red?style=for-the-badge)
![Privacy](https://img.shields.io/badge/Privacy-No_Data_Storage-lightgrey?style=for-the-badge)
![UI](https://img.shields.io/badge/UI-SOC_Style-black?style=for-the-badge)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)

--- 

## Overview

FraudMind AI is a modern AI-powered cybersecurity platform designed to analyze suspicious messages and detect phishing, scam, and social engineering attacks using structured LLM-based risk assessment.

The platform integrates securely with the OpenAI API, enforces deterministic JSON output validation, and presents results through a professional SOC-style dashboard. It follows a privacy-first architecture with no persistent storage of user messages.

--- 

## Features

- **AI Risk Assessment:** Analyzes suspicious messages and generates structured cybersecurity evaluations.

- **Phishing & Scam Detection:** Detects common attack types including phishing, romance scams, IRS fraud, tech support scams, and delivery scams.

- **Manipulation & Urgency Detection:** Identifies psychological pressure tactics such as authority impersonation, fear triggers, and time-sensitive threats.

- **Structured JSON Output:** Produces deterministic, machine-readable AI responses using predefined security schema fields.

- **Risk Scoring System:** Provides risk level, pressure score, and confidence metrics for clear threat prioritization.

- **Safe Reply Generator:** Generates a secure, copyable response template to prevent engagement with malicious actors.

- **Action Guidance:** Clearly outlines “What To Do” and “What Not To Do” recommendations.

- **SOC-Style Dashboard:** Displays KPI cards, risk indicators, and tactic visualizations in a cybersecurity-themed interface.

- **Privacy-First Design:** No message storage, no tracking, and no persistent user data collection.

- **Secure API Integration:** All secrets are managed using environment variables with no hardcoded credentials.

---

## System Design

### Backend

- **Django (MTV Architecture):** Structured using Model–Template–View design pattern for scalability and separation of concerns.
- **Secure POST-Only Endpoint:** Accepts only POST requests to prevent unintended data exposure.
- **Structured JSON Validation:** Enforces strict schema validation for deterministic and reliable AI responses.
- **Defensive Error Handling:** Implements controlled exception handling to prevent information leakage.

---

### Frontend

- **Dark SOC-Style Interface:** Cybersecurity-themed dashboard inspired by Security Operations Center (SOC) environments.
- **KPI Metric Visualization:** Displays risk level, pressure score, and confidence metrics through visual components.
- **Risk Scoring Components:** Interactive UI elements that clearly communicate threat severity.

---

##  Security Controls

- **.env Excluded from Version Control:** Sensitive environment variables protected via `.gitignore`.
- **No Hardcoded API Keys:** All secrets are securely managed using environment variables.
- **No Persistent Message Storage:** User messages are processed in-memory and never stored.
- **Environment-Based Configuration:** Secure configuration management for development and production environments.

---

##  Technology Stack

- **Python**
- **Django**
- **OpenAI API**
- **HTML / CSS**
- **JSON Schema Validation**
- **Environment Variables**

---

## Team Members

- **Md Mushfique Rahman** – Full Stack Developer & AI Integration Engineer
- **Syeda Nawal** – Frontend Developer
- **Adita Haque Raisa** – UI Designer

---


## Dashboard Overview

### Main Dashboard (Pre-Analysis View)
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/f2a99261-9a5c-4428-8fae-603d384eb84d" />
<img width="1897" height="1077" alt="image" src="https://github.com/user-attachments/assets/cc0ad70f-3d16-4870-a944-3809646a8c87" />

This dashboard acts as the control center where users submit suspicious messages for AI evaluation.

---

### Threat Analysis Dashboard (Post-Analysis View)
<img width="1919" height="1072" alt="image" src="https://github.com/user-attachments/assets/5dd8dbb5-3009-46e6-a5c5-409e76b6ad6f" />
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/298cd580-9829-430a-be54-57451cc3ce77" />
This dashboard presents a full cybersecurity-style breakdown after analysis is completed.

---

### Manipulation & Psychological Tactics Analysis
This section focuses specifically on psychological attack patterns commonly used in social engineering scams.

<img width="1902" height="1074" alt="image" src="https://github.com/user-attachments/assets/4c0b5d9b-552e-4fd5-a449-76fa1cb41f64" />
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/1e35bed0-c67e-44f3-b9c0-24496563111c" />

- Detects urgency cues and time pressure tactics
- Identifies authority impersonation attempts
- Flags fear-based triggers
- Detects emotional manipulation (romance, sympathy, panic)
- Highlights coercion or intimidation patterns
- Displays manipulation severity indicators
  


---

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
