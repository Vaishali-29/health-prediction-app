
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

from database import init_db, get_connection
from validators import validate_patient
from ai_service import generate_health_remarks


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "health-app-development-key")


# Create database and patients table
init_db()


@app.route("/")
def index():
    """Display all patient records."""

    connection = get_connection()

    try:
        patients = connection.execute(
            "SELECT * FROM patients ORDER BY id DESC"
        ).fetchall()
    finally:
        connection.close()

    return render_template("index.html", patients=patients)


@app.route("/add", methods=["GET", "POST"])
def add_patient():
    """Add a new patient record."""

    if request.method == "POST":
        data = request.form
        errors = validate_patient(data)

        if errors:
            return render_template(
                "add_patient.html",
                errors=errors,
                form_data=data
            )

        patient = {
            "glucose": float(data["glucose"]),
            "haemoglobin": float(data["haemoglobin"]),
            "cholesterol": float(data["cholesterol"])
        }

        # Generate AI health remarks
        try:
            remarks = generate_health_remarks(patient)
        except Exception as error:
            remarks = f"AI remarks unavailable: {error}"

        connection = get_connection()

        try:
            connection.execute(
                """
                INSERT INTO patients
                (full_name, dob, email, glucose, haemoglobin,
                 cholesterol, remarks)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data["full_name"].strip(),
                    data["dob"].strip(),
                    data["email"].strip(),
                    patient["glucose"],
                    patient["haemoglobin"],
                    patient["cholesterol"],
                    remarks
                )
            )

            connection.commit()

        finally:
            connection.close()

        flash("Patient added successfully!", "success")
        return redirect(url_for("index"))

    return render_template(
        "add_patient.html",
        errors={},
        form_data={}
    )


@app.route("/edit/<int:patient_id>", methods=["GET", "POST"])
def edit_patient(patient_id):
    """Update an existing patient record."""

    connection = get_connection()

    try:
        existing_patient = connection.execute(
            "SELECT * FROM patients WHERE id = ?",
            (patient_id,)
        ).fetchone()
    finally:
        connection.close()

    if existing_patient is None:
        flash("Patient record not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        data = request.form
        errors = validate_patient(data)

        if errors:
            return render_template(
                "edit_patient.html",
                patient=existing_patient,
                errors=errors,
                form_data=data
            )

        patient = {
            "glucose": float(data["glucose"]),
            "haemoglobin": float(data["haemoglobin"]),
            "cholesterol": float(data["cholesterol"])
        }

        # Generate updated AI remarks
        try:
            remarks = generate_health_remarks(patient)
        except Exception as error:
            remarks = f"AI remarks unavailable: {error}"

        connection = get_connection()

        try:
            connection.execute(
                """
                UPDATE patients
                SET full_name = ?,
                    dob = ?,
                    email = ?,
                    glucose = ?,
                    haemoglobin = ?,
                    cholesterol = ?,
                    remarks = ?
                WHERE id = ?
                """,
                (
                    data["full_name"].strip(),
                    data["dob"].strip(),
                    data["email"].strip(),
                    patient["glucose"],
                    patient["haemoglobin"],
                    patient["cholesterol"],
                    remarks,
                    patient_id
                )
            )

            connection.commit()

        finally:
            connection.close()

        flash("Patient updated successfully!", "success")
        return redirect(url_for("index"))

    return render_template(
        "edit_patient.html",
        patient=existing_patient,
        errors={},
        form_data=existing_patient
    )


@app.route("/delete/<int:patient_id>", methods=["POST"])
def delete_patient(patient_id):
    """Delete a patient record."""

    connection = get_connection()

    try:
        connection.execute(
            "DELETE FROM patients WHERE id = ?",
            (patient_id,)
        )

        connection.commit()

    finally:
        connection.close()

    flash("Patient deleted successfully!", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
