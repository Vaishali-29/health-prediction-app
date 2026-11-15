

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

API_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/"
    f"models/{MODEL}:generateContent"
)


def generate_health_remarks(patient):
    """Generate cautious health observations using Gemini AI."""

    if not API_KEY:
        raise ValueError(
            "Gemini API key is missing. Check your .env file."
        )

    prompt = f"""
You are an AI assistant providing general health information.

Review these patient blood test values:

Glucose: {patient['glucose']}
Haemoglobin: {patient['haemoglobin']}
Cholesterol: {patient['cholesterol']}

Provide a short health-risk observation in 3-4 sentences.

Instructions:
1. Mention values that may need medical attention.
2. Do not claim that the patient has a disease.
3. Do not prescribe medicines or treatment.
4. Blood test units and testing conditions are not provided.
   Clearly mention that interpretation is limited by this.
5. Recommend consulting a qualified healthcare professional.
6. Use simple, professional English.
7. This is informational support, not a medical diagnosis.
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        remarks = result["candidates"][0]["content"]["parts"][0]["text"]

        return remarks.strip()

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Gemini API request timed out. Please try again."
        )

    except requests.exceptions.HTTPError:
        try:
            details = response.json().get(
                "error", {}
            ).get(
                "message", "No details returned"
            )
        except ValueError:
            details = "No details returned"

        raise RuntimeError(
            f"Gemini API error: HTTP {response.status_code}: {details}"
        )

    except (KeyError, IndexError, TypeError):
        raise RuntimeError(
            "Gemini API returned an unexpected response."
        )

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Could not connect to Gemini API: {error}"
        )

