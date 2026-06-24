import streamlit as st
from api import get_patients, update_patient

st.set_page_config(page_title="Edit Patient", layout="centered")
st.title("✏️ Edit Patient")

# --------------------------
# Load patients
# --------------------------
patients = get_patients()

if isinstance(patients, dict) and "error" in patients:
    st.error("❌ Failed to load patients")
    st.write(patients["error"])
    st.stop()

if not isinstance(patients, list) or len(patients) == 0:
    st.warning("⚠️ No patients available to edit")
    st.stop()

# --------------------------
# Select patient
# --------------------------
patient_map = {f"{p['id']} - {p['name']}": p for p in patients}
selected_label = st.selectbox("Select Patient", list(patient_map.keys()))
patient = patient_map[selected_label]

# --------------------------
# Form UI with prefilled data
# --------------------------
st.subheader("Edit Details")

name = st.text_input("Name", value=patient.get("name", ""))
age = st.number_input("Age", value=patient.get("age", 0))

gender = st.selectbox(
    "Gender",
    ["male", "female", "other"],
    index=["male", "female", "other"].index(patient.get("gender", "male"))
)

height = st.number_input("Height", value=patient.get("height", 0.0))
weight = st.number_input("Weight", value=patient.get("weight", 0.0))

# --------------------------
# Update button
# --------------------------
if st.button("Update Patient"):
    if not name:
        st.error("Name is required")
        st.stop()

    payload = {
        "name": name,
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight
    }

    response = update_patient(patient["id"], payload)

    if isinstance(response, dict) and "error" in response:
        st.error("❌ Failed to update patient")
        st.write(response["error"])
    else:
        st.success("✅ Patient updated successfully!")
        st.json(response)
        st.rerun()