import numpy as np
import pickle
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import os
from streamlit_option_menu import option_menu

# Load models (adjust paths)
kidney_model = pickle.load(open(r'C:\Users\ASO\Desktop\Project\Medical\Kidney.pkl', 'rb'))
stroke_model = pickle.load(open(r'C:\Users\ASO\Desktop\Project\Medical\best_stroke_model.pkl', 'rb'))
alzheimers_model = pickle.load(open(r'C:\Users\ASO\Desktop\Project\Medical\alzheimers_disease.pkl', 'rb'))
diabetes_model = pickle.load(open(r'C:\Users\ASO\Desktop\Project\Medical\diabetes_model.pkl', 'rb'))

# Store results globally for PDF
results = {}

# Prediction function
def make_prediction(model, input_data, disease_name):
    input_array = np.array(input_data, dtype=float).reshape(1, -1)
    prediction = model.predict(input_array)
    result = "✅ Positive Diagnosis" if prediction[0] == 1 else "❌ Negative Diagnosis"
    results[disease_name] = result
    return result

# Generate PDF Report
def generate_pdf(results_dict):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp_file.name, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Medical Prediction Report")

    c.setFont("Helvetica", 12)
    y = height - 100
    for disease, outcome in results_dict.items():
        c.drawString(80, y, f"{disease}: {outcome}")
        y -= 30

    c.save()
    return temp_file.name

# Streamlit App
def main():
    with st.sidebar:
        selected = option_menu(
            "Disease Prediction System",  # title
            ["Welcome Page", "Kidney Disease", "Stroke Disease", "Alzheimer’s", "Diabetes"],
            icons=["home","droplet", "heart", "person", "activity", "brain"],
            menu_icon="hospital",  # main icon
            default_index=0,  # first one selected
            orientation="vertical"
        )

    # Welcome Page
    if selected == "Welcome Page":
        st.title("Welcome Page")
        st.markdown("Design by Segun Alabi Ojo")

    # Kidney Disease
    if selected == "Kidney Disease":
        st.title("🧪 Kidney Disease Prediction")
        st.markdown("Fill in the details below:")
        col1, col2 = st.columns(2)

        with col1:
            Age = st.text_input('Age')
        with col2:
            SystolicBP = st.text_input('SystolicBP')
        with col1:
            DiastolicBP = st.text_input('DiastolicBP')
        with col2:
            BMI = st.text_input('BMI')
        with col1:
            FamilyHistoryKidneyDisease = st.text_input('Family History (0=No,1=Yes)')
        with col2:
            Smoking = st.text_input('Smoking (0=No,1=Yes)')
        with col1:
            FastingBloodSugar = st.text_input('Fasting BloodSugar')
        with col2:
            ProteinInUrine = st.text_input('Protein In Urine')
        with col1:
            MedicalCheckupsFrequency = st.text_input('Medical Checkups Frequency')

        if st.button("Predict Kidney Disease"):
            try:
                input_data = [
                    float(Age), float(SystolicBP), float(DiastolicBP), float(BMI),
                    float(FamilyHistoryKidneyDisease), float(Smoking),
                    float(FastingBloodSugar), float(ProteinInUrine),
                    float(MedicalCheckupsFrequency)
                ]
                result = make_prediction(kidney_model, input_data, selected)
                st.success(result)
            except:
                st.error("⚠ Please enter valid numeric values.")


    # Stroke Disease
    elif selected == "Stroke Disease":
        st.title("🧠 Stroke Prediction")
        st.markdown("Fill in the details below:")
        col1, col2 = st.columns(2)

        # Collect categorical + numeric features
        with col1:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        with col2:
            age = st.number_input("Age", min_value=0, max_value=120, step=1)
        with col1:
            hypertension = st.selectbox("Hypertension", [0, 1])  # 0=No, 1=Yes
        with col2:
            heart_disease = st.selectbox("Heart Disease", [0, 1])  # 0=No, 1=Yes
        with col1:
            ever_married = st.selectbox("Ever Married", ["Yes", "No"])
        with col2:
            work_type = st.selectbox("Work Type", ["Private", "Self-employed", "Govt_job", "children", "Never_worked"])
        with col1:
            residence_type = st.selectbox("Residence Type", ["Urban", "Rural"])
        with col2:
            avg_glucose_level = st.number_input("Average Glucose Level", min_value=0.0, step=0.1)
        with col1:
            bmi = st.number_input("BMI", min_value=0.0, step=0.1)
        with col2:
            smoking_status = st.selectbox("Smoking Status", ["never smoked", "formerly smoked", "smokes", "Unknown"])

        if st.button("Predict Stroke"):
            try:
                # Encode categorical features as integers (must match training encoding!)
                gender_map = {"Male": 0, "Female": 1, "Other": 2}
                married_map = {"No": 0, "Yes": 1}
                work_map = {"Private": 0, "Self-employed": 1, "Govt_job": 2, "children": 3, "Never_worked": 4}
                residence_map = {"Rural": 0, "Urban": 1}
                smoking_map = {"never smoked": 0, "formerly smoked": 1, "smokes": 2, "Unknown": 3}

                input_data = [
                    gender_map[gender],
                    float(age),
                    float(hypertension),
                    float(heart_disease),
                    married_map[ever_married],
                    work_map[work_type],
                    residence_map[residence_type],
                    float(avg_glucose_level),
                    float(bmi),
                    smoking_map[smoking_status]
                ]

                result = make_prediction(stroke_model, input_data, selected)
                st.success(result)

            except Exception as e:
                st.error(f"⚠ Error: {e}")

    # Alzheimer’s
    elif selected == "Alzheimer’s":
        st.title("🧠 Alzheimer’s Prediction")
        st.markdown("Fill in the details below:")
        col1, col2 = st.columns(2)

        with col1:
            Age = st.text_input('Age')
        with col2:
            Gender = st.text_input('Gender (Male = 1, Female = 2, Others = 0)')
        with col1:
            BMI = st.text_input('Body Mass Index')
        with col2:
            Smoking = st.text_input('Smoking (0=No,1=Yes)')
        with col1:
            AlcoholConsumption = st.text_input('Alcohol Consumption Measure')
        with col2:
            PhysicalActivity = st.text_input('Physical Activity Measure')
        with col1:
            Hypertension = st.text_input('Hypertension Record (0=No,1=Yes)')
        with col2:
            SystolicBP = st.text_input('SystolicBP Value')
        with col1:
            DiastolicBP = st.text_input('SystolicBP Value)')
        with col2:
            Diabetes = st.text_input('Ever had a Diabetes Record? (0=No,1=Yes)')


        if st.button("Predict Alzheimer’s"):
            try:
                input_data = [float(Age), float(Gender), float(BMI), float(Smoking), float(AlcoholConsumption), float(PhysicalActivity),
                              float(Hypertension), float(SystolicBP), float(DiastolicBP), float(Diabetes)]
                result = make_prediction(alzheimers_model, input_data, selected)
                st.success(result)
            except:
                st.error("⚠ Please enter valid numeric values.")

        st.markdown("Primary Symptop:"
                    "1. Difficulty Speaking,   2. Loss of Balance, "
                    "3. Seizures, 4. Severe Fatigue,"
                    "5. Dizziness, 6. Confusion,"
                    "7. Numbness, 8. Weakness"
                    "9. Blurred Vision,10. Headache")

    # Diabetes
    elif selected == "Diabetes":
        st.title("🫁 Diabetes Prediction")
        st.markdown("Fill in the details below:")

        col1, col2 = st.columns(2)

        with col1:
            Pregnancies = st.text_input('Number of Pregnancies')
        with col2:
            Glucose = st.text_input('Glucose')
        with col1:
            BloodPressure = st.text_input('Blood Pressure')
        with col2:
            SkinThickness = st.text_input('Skin Thickness')
        with col1:
            Insulin = st.text_input('Insulin')
        with col2:
            BMI = st.text_input('BMI Level')
        with col1:
            DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function')
        with col2:
            Age = st.text_input('Patient Age')


        if st.button("Predict Diabetes"):
            try:
                input_data = [float(Pregnancies), float(Glucose), float(BloodPressure),
                              float(SkinThickness), float(Insulin), float(BMI),
                              float(DiabetesPedigreeFunction), float(Age)]
                result = make_prediction(diabetes_model, input_data, selected)
                st.success(result)
            except:
                st.error("⚠ Please enter valid numeric values.")

    # PDF Download button (only show if results exist)
    if results:
        pdf_path = generate_pdf(results)
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📄 Download Medical Report (PDF)",
                data=pdf_file,
                file_name="medical_report.pdf",
                mime="application/pdf"
            )

        # Cleanup temp file
        os.remove(pdf_path)

if __name__ == "__main__":
    main()
