import numpy as np
import pickle
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# Load trained model
loaded_model = pickle.load(open(r'C:\Users\ASO\Desktop\Project\Medical\Kdiney.pkl', 'rb'))

#-------------------------------------- Kidney----------
def kidney_prediction(input_data):
    input_data_array = np.array(input_data, dtype=float)
    input_reshaped = input_data_array.reshape(1, -1)
    prediction = loaded_model.predict(input_reshaped)

    if prediction[0] == 1:
        return "Kidney Disease Confirmed"
    else:
        return "Patient Free of Kidney Disease"

# Function to generate PDF
def generate_pdf(report_text, filename="Kidney_Report.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 100, "Kidney Prediction Report")
    c.drawString(100, height - 120, "-" * 200)
    y = height - 160
    for line in report_text.split("\n"):
        c.drawString(100, y, line)
        y -= 20
    c.save()
    return filename

def main():
    st.title('Kidney Prediction System')
    st.markdown("Fill in the details below:")

    col1, col2 = st.columns(2)

    with col1:
        Age = st.text_input('Age')
    with col2:
        SystolicBP = st.text_input('SystolicBP')
    with col1:
        DiastolicBP = st.text_input('DiastolicBP')
    with col2:
        BMI = st.text_input('BMI Values')
    with col1:
        FamilyHistoryKidneyDisease = st.text_input('Family History Kidney Disease (0=No, 1=Yes)')
    with col2:
        Smoking = st.text_input('Smoking (0=No, 1=Yes)')
    with col1:
        FastingBloodSugar = st.text_input('Fasting BloodSugar')
    with col2:
        ProteinInUrine = st.text_input('Protein In Urine')
    with col1:
        MedicalCheckupsFrequency = st.text_input('Medical Checkups Frequency')

    Diagnosis = ''

    if st.button('Predict'):
        try:
            input_data = [
                float(Age),
                float(SystolicBP),
                float(DiastolicBP),
                float(BMI),
                float(FamilyHistoryKidneyDisease),
                float(Smoking),
                float(FastingBloodSugar),
                float(ProteinInUrine),
                float(MedicalCheckupsFrequency)
            ]

            Diagnosis = kidney_prediction(input_data)
            st.success(Diagnosis)

            # Generate medical report text
            report_text = f"""
            Kidney Prediction Report

            Patient Information:
            Age: {Age}
            Systolic BP: {SystolicBP}
            Diastolic BP: {DiastolicBP}
            BMI: {BMI}
            Family History Kidney Disease: {FamilyHistoryKidneyDisease}
            Smoking: {Smoking}
            Fasting Blood Sugar: {FastingBloodSugar}
            Protein In Urine: {ProteinInUrine}
            Medical Checkups Frequency: {MedicalCheckupsFrequency}

            Prediction Result:
            {Diagnosis}
            """

            # Generate PDF
            pdf_file = generate_pdf(report_text)

#------------------------- Stroke ------------------------

            # Add download link
            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="📄 Download Medical Report (PDF)",
                    data=f,
                    file_name="Kidney_Report.pdf",
                    mime="application/pdf"
                )

        except ValueError:
            st.error("⚠ Please enter valid numeric values for all fields.")

if __name__ == '__main__':
    main()
