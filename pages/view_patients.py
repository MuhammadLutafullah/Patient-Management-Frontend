import streamlit as st
import pandas as pd
from api import get_patients, delete_patient

st.set_page_config(page_title="View Patients", layout="wide")
st.title("📋 Patients List")

# --------------------------
# Fetch patients
# --------------------------
patients = get_patients()

if isinstance(patients, dict) and "error" in patients:
    st.error("❌ Failed to fetch patients")
    st.write(patients["error"])
    st.stop()

if not isinstance(patients, list):
    st.error("❌ Invalid response from backend")
    st.write(patients)
    st.stop()

if len(patients) == 0:
    st.warning("⚠️ No patients found")
    st.stop()

# --------------------------
# Convert to DataFrame
# --------------------------
df = pd.DataFrame(patients)

# Desired column order
column_order = [
    "id",
    "name",
    "city_name",
    "age",
    "gender",
    "height",
    "weight",
    "bmi",
    "weight_category"
]

# Keep only columns that exist
available_columns = [
    col for col in column_order
    if col in df.columns
]

df = df[available_columns]

# --------------------------
# Show table
# --------------------------
st.subheader("All Patients")
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# --------------------------
# Delete Section
# --------------------------
st.divider()
st.subheader("🗑️ Delete Patient")

patient_map = {
    f"{row['id']} - {row['name']}": row
    for row in patients
}

selected_patient_label = st.selectbox(
    "Select Patient",
    list(patient_map.keys())
)

selected_patient = patient_map[selected_patient_label]

st.write("### Patient Details")
st.write(f"**ID:** {selected_patient['id']}")
st.write(f"**Name:** {selected_patient['name']}")
st.write(f"**Age:** {selected_patient['age']}")
st.write(f"**Gender:** {selected_patient['gender']}")

if "city_name" in selected_patient:
    st.write(f"**City:** {selected_patient['city_name']}")

confirm_delete = st.checkbox(
    "I understand this action cannot be undone"
)

if st.button("Delete Selected Patient"):
    if not confirm_delete:
        st.warning("Please confirm deletion first.")
        st.stop()

    response = delete_patient(selected_patient["id"])

    if isinstance(response, dict) and "error" in response:
        st.error("❌ Failed to delete patient")
        st.write(response["error"])
    else:
        st.success("✅ Patient deleted successfully!")
        st.rerun()