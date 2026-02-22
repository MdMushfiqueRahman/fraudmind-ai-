"""
FraudMind AI — detector views: home, analyze (OpenAI Responses API).
"""
import json
import os
import re
import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

logger = logging.getLogger(__name__)

# Schema for AI output (for prompt and validation)
SCHEMA_FIELDS = [
    "risk_level",      # low|medium|high
    "scam_type",       # phishing|job_scam|romance_scam|crypto_scam|tech_support|delivery_scam|giveaway|tax_scam|other|not_scam
    "pressure_score",  # 0-100
    "confidence",      # low|medium|high
    "primary_tactics", # list of strings
    "red_flags",       # list of strings
    "manipulation_tactics", # list of strings
    "one_sentence_summary", # string
    "safe_reply",      # string
    "what_to_do",      # list of strings
    "what_not_to_do",  # list of strings
]

ANALYSIS_PROMPT = """You are a security analyst. Analyze the following message for social engineering and phishing. Reply with ONLY valid JSON, no other text.

Required JSON keys (use exactly these):
- risk_level: one of "low", "medium", "high"
- scam_type: one of "phishing", "job_scam", "romance_scam", "crypto_scam", "tech_support", "delivery_scam", "giveaway", "tax_scam", "other", "not_scam"
- pressure_score: integer 0-100
- confidence: one of "low", "medium", "high"
- primary_tactics: array of strings (e.g. ["Urgency", "Fear", "Authority"])
- red_flags: array of strings
- manipulation_tactics: array of strings
- one_sentence_summary: string
- safe_reply: string (example safe reply the user could send)
- what_to_do: array of strings
- what_not_to_do: array of strings

Message type: {message_type}

Message to analyze:
---
{message}
---

Output only the JSON object, no markdown and no explanation."""


def _parse_json_from_response(raw: str):
    """Extract JSON object from raw API response (strip markdown/code blocks if present)."""
    raw = raw.strip()
    # Remove optional markdown code block
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```\s*$", "", raw)
    return json.loads(raw)


def _ensure_schema(data: dict) -> dict:
    """Ensure all required keys exist with safe defaults."""
    defaults = {
        "risk_level": "low",
        "scam_type": "other",
        "pressure_score": 0,
        "confidence": "low",
        "primary_tactics": [],
        "red_flags": [],
        "manipulation_tactics": [],
        "one_sentence_summary": "",
        "safe_reply": "",
        "what_to_do": [],
        "what_not_to_do": [],
    }
    for k, v in defaults.items():
        if k not in data or data[k] is None:
            data[k] = v
        elif k in ("primary_tactics", "red_flags", "manipulation_tactics", "what_to_do", "what_not_to_do"):
            if not isinstance(data[k], list):
                data[k] = [str(data[k])] if data[k] else []
    return data


def home(request):
    """Home page: dark theme, message type dropdown, textarea, Load Demo, Analyze."""
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    return render(request, "index.html", {
        "has_api_key": bool(api_key),
    })


def analyze(request):
    """POST only: call OpenAI Responses API, return redirect to dashboard or home with error."""
    if request.method != "POST":
        return redirect("home")

    message = (request.POST.get("message") or "").strip()
    message_type = request.POST.get("message_type") or "email"

    if not message:
        return render(request, "index.html", {
            "has_api_key": True,
            "error": "Please enter a message to analyze.",
        })

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return render(request, "index.html", {
            "has_api_key": False,
            "error": "OPENAI_API_KEY is not set. Add it to your .env file. See README for setup.",
            "message": message,
            "message_type": message_type,
        })

    prompt = ANALYSIS_PROMPT.format(message_type=message_type, message=message)
    raw_response = None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        raw_response = None

        # Prefer OpenAI Responses API
        if hasattr(client, "responses"):
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=[{"role": "user", "content": prompt}],
            )
            if hasattr(response, "output_text") and response.output_text:
                raw_response = response.output_text
            elif hasattr(response, "output") and response.output:
                out = response.output
                if isinstance(out, list) and len(out) > 0:
                    item = out[0]
                    if hasattr(item, "content") and isinstance(item.content, list):
                        for block in item.content:
                            if getattr(block, "type", None) == "output_text" and hasattr(block, "text"):
                                raw_response = block.text
                                break
                    elif hasattr(item, "text"):
                        raw_response = item.text
                    if not raw_response and hasattr(item, "content"):
                        for c in (item.content or []):
                            if getattr(c, "type", None) == "output_text" and hasattr(c, "text"):
                                raw_response = c.text
                                break

        # Fallback: Chat Completions (same prompt, JSON output)
        if not raw_response:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            msg = completion.choices[0].message if completion.choices else None
            raw_response = msg.content if msg and getattr(msg, "content", None) else None

        if not raw_response:
            logger.warning("No text in API response")
            return render(request, "index.html", {
                "has_api_key": True,
                "error": "API returned an unexpected format. Check server console for raw response.",
                "message": message,
                "message_type": message_type,
            })
    except Exception as e:
        logger.exception("OpenAI API error")
        return render(request, "index.html", {
            "has_api_key": True,
            "error": f"API error: {str(e)}. If the model name is wrong, try gpt-4o-mini in views.py.",
            "message": message,
            "message_type": message_type,
        })

    # Parse JSON
    try:
        data = _parse_json_from_response(raw_response)
    except json.JSONDecodeError as e:
        logger.warning("Non-JSON response: %s", raw_response[:1000])
        import sys
        print("FraudMind raw API response (non-JSON):", file=sys.stderr)
        print(raw_response, file=sys.stderr)
        if request.headers.get("Accept", "").find("application/json") != -1:
            return HttpResponse(
                json.dumps({"error": "OpenAI returned non-JSON", "raw_preview": raw_response[:500]}),
                content_type="application/json",
                status=502,
            )
        return render(request, "index.html", {
            "has_api_key": True,
            "error": "AI returned invalid JSON. Check server console for raw response.",
            "message": message,
            "message_type": message_type,
        })

    data = _ensure_schema(data)
    data["original_message"] = message
    data["message_type"] = message_type
    # Risk percentage for donut (combine risk_level + pressure_score)
    pressure = max(0, min(100, data.get("pressure_score") or 0))
    if data.get("risk_level") == "high":
        data["risk_pct"] = max(75, pressure)
    elif data.get("risk_level") == "medium":
        data["risk_pct"] = max(40, min(74, pressure))
    else:
        data["risk_pct"] = min(39, pressure)

    # Per-tactic scores 0–100 for bar widths (from API or derived from pressure)
    tactics_raw = data.get("manipulation_tactics") or data.get("primary_tactics") or []
    tactic_scores = []
    api_scores = data.get("tactic_scores")
    if isinstance(api_scores, list) and len(api_scores) > 0:
        for item in api_scores:
            if isinstance(item, dict) and "name" in item and "score" in item:
                tactic_scores.append({
                    "name": str(item["name"]),
                    "score": max(0, min(100, int(item.get("score", 0)))),
                })
    if not tactic_scores and tactics_raw:
        for i, name in enumerate(tactics_raw):
            # Vary score by position so bars show different lengths (0–100)
            score = max(0, min(100, int(pressure * (1.0 - i * 0.12) + i * 3)))
            tactic_scores.append({"name": str(name), "score": score})
    data["tactic_scores"] = tactic_scores

    # JSON payload for dashboard script (avoids template syntax inside JS)
    data["dashboard_data"] = {
        "risk_level": data.get("risk_level", "low"),
        "risk_pct": data.get("risk_pct", 0),
        "pressure_score": data.get("pressure_score", 0),
        "primary_tactics": data.get("primary_tactics") or [],
        "tactic_scores": data["tactic_scores"],
    }

    return render(request, "dashboard.html", data)
