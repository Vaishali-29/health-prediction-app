# Health Prediction Application

An AI-powered Health Prediction Application built using Python, Flask, SQLite, and Google Gemini API.

## Project Overview

Health Prediction Application allows users to manage patient records and generate AI-assisted health observations based on blood test values.

The application collects patient details, validates the entered information, stores records in an SQLite database, and uses the Gemini API to generate health-related remarks.

**Note:** This application provides informational support only. It does not provide medical diagnosis or treatment recommendations.

## Features

- Create, Read, Update, and Delete patient records (CRUD).
- Patient information management.
- Email address validation.
- Date of birth validation, including future-date detection.
- Numeric validation for blood test values.
- Persistent data storage using SQLite.
- AI-generated health observations using Google Gemini API.
- Simple and responsive user interface.
- Secure API key management using environment variables.

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Google Gemini API
- Python Requests
- python-dotenv

## Patient Information

The application stores:

- Full Name
- Date of Birth
- Email Address
- Glucose
- Haemoglobin
- Cholesterol
- AI-generated Remarks

## Project Structure

```text
health-prediction-app/
│
├── app.py
├── database.py
├── validators.py
├── ai_service.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add_patient.html
│   └── edit_patient.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Vaishali-29/health-prediction-app.git
cd health-prediction-app
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

Add your credentials:

```env
GEMINI_API_KEY=your_actual_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
FLASK_SECRET_KEY=your_unique_secret_key
```

Never upload your actual `.env` file or API key to GitHub.

### 6. Run the application

```bash
python app.py
```

Open your browser and visit:

http://127.0.0.1:5000

## AI Integration

The application integrates Google Gemini API to generate short health-related observations based on the patient's glucose, haemoglobin, and cholesterol values.

The AI prompt is designed to:
- Highlight values that may need medical attention.
- Avoid claiming that a patient has a disease.
- Avoid prescribing medicines or treatment.
- Mention limitations when units and testing conditions are unavailable.
- Recommend consulting a qualified healthcare professional.

## Validation and Testing

The application validates:
- Required patient fields.
- Email address format.
- Date of birth format and validity.
- Future date of birth.
- Numeric blood test values.

Invalid patient records are rejected with appropriate validation messages.

## Security

- API credentials are stored in environment variables.
- `.env` is excluded through `.gitignore`.
- SQLite database files are excluded from Git tracking.

## Disclaimer

This project is developed for educational and demonstration purposes. AI-generated remarks are not medical advice and must not be used as a substitute for professional medical evaluation.
