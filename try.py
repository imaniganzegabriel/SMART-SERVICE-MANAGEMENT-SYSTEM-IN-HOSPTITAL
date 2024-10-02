import streamlit as st
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load the saved model
model = pickle.load(open('SSMS.pkl', 'rb'))

# Label encoder for 'Female' and 'Male' columns
label_encoder = LabelEncoder()
label_encoder.fit(['no', 'yes'])  # Assuming only 'no' and 'yes' exist

# Helper function to convert time from hours to minutes
def time_to_minutes(time_str):
    h, m = map(int, time_str.split('h'))
    return h * 60 + m

# Streamlit UI setup
st.title("Patient Wait Time Prediction")
st.write("""
### Input the patient details to predict wait time.
""")

# Input fields
patient_age = st.number_input("Patient Age", min_value=0, max_value=120, step=1, value=30)
gender = st.selectbox("Gender", ['Male', 'Female'])
visit_duration = st.text_input("Visit Duration (e.g., '10h30')", value="10h00")
nurse_id = st.number_input("Nurse ID", min_value=5410, max_value=9999, step=1, value=5410)

# Convert gender to numeric values
female = 1 if gender == 'Female' else 0
male = 1 if gender == 'Male' else 0

# Convert visit duration to minutes
visit_duration_minutes = time_to_minutes(visit_duration)

# Prepare the input DataFrame
input_data = {
    'Patient_Age': patient_age,
    'Female': female,
    'Male': male,
    'Visit_Duration': visit_duration_minutes,
    'Nurse_ID': nurse_id
}
input_df = pd.DataFrame([input_data])

# Prediction button
if st.button('Predict Wait Time'):
    predicted_wait_time = model.predict(input_df)
    st.write(f"**Predicted Wait Time: {predicted_wait_time[0]:.2f} minutes**")
