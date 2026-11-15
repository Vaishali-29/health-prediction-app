
import re
from datetime import datetime, date


def validate_patient(data):
    errors = {}

    # Full Name validation
    full_name = data.get("full_name", "").strip()

    if not full_name:
        errors["full_name"] = "Full name is required."

   
    # Date of Birth validation
    dob = data.get("dob", "").strip()

    date_of_birth = None

    for date_format in ("%d/%m/%Y", "%d.%m.%Y"):
        try:
            date_of_birth = datetime.strptime(
                dob, date_format
            ).date()
            break
        except ValueError:
            continue

    if date_of_birth is None:
        errors["dob"] = "Enter a valid date in DD/MM/YYYY format."
    elif date_of_birth > date.today():
        errors["dob"] = "Date of birth cannot be in the future."

    # Email validation
    email = data.get("email", "").strip()

    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.match(email_pattern, email):
        errors["email"] = "Enter a valid email address."

    # Blood test values validation
    numeric_fields = ["glucose", "haemoglobin", "cholesterol"]

    for field in numeric_fields:
        value = data.get(field, "").strip()

        try:
            number = float(value)

            if number < 0:
                errors[field] = f"{field} cannot be negative."

        except (ValueError, TypeError):
            errors[field] = f"{field} must be a valid number."

    return errors
