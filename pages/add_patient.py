import streamlit as st
from api import create_patient, get_cities

st.set_page_config(page_title="Add Patient", layout="centered")
st.title("➕ Add Patient")

# --------------------------
# Load cities
# --------------------------
cities = get_cities()

# Handle API errors safely
if isinstance(cities, dict) and "error" in cities:
    st.error("❌ Failed to load cities from backend")
    st.write(cities["error"])
    st.stop()

if not isinstance(cities, list):
    st.error("❌ Invalid response from backend")
    st.write(cities)
    st.stop()

if len(cities) == 0:
    st.warning("⚠️ No cities found. Please add cities first.")
    st.stop()

# Create city map (name -> id)
city_map = {
    city.get("city_name"): city.get("id")
    for city in cities
    if isinstance(city, dict)
}

# --------------------------
# Form UI
# --------------------------
with st.form("add_patient_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, step=1)
    gender = st.selectbox("Gender", ["male", "female", "other"])
    city_name = st.selectbox("City", list(city_map.keys()))

    st.subheader("📏 Height")
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("Height Value")
    with col2:
        height_unit = st.selectbox("Unit", ["cm", "inch", "feet"])

    st.subheader("⚖️ Weight")
    col3, col4 = st.columns(2)
    with col3:
        weight = st.number_input("Weight Value")
    with col4:
        weight_unit = st.selectbox("Unit", ["kg", "lbs"])

    submitted = st.form_submit_button("Create Patient")

# --------------------------
# Submit logic
# --------------------------
if submitted:
    # Validation
    if not name:
        st.error("❌ Name is required")
        st.stop()

    if height <= 0 or weight <= 0:
        st.error("❌ Height and Weight must be greater than 0")
        st.stop()

    payload = {
        "name": name,
        "city_id": city_map[city_name],
        "age": age,
        "gender": gender,
        "height": height,
        "height_unit": height_unit,
        "weight": weight,
        "weight_unit": weight_unit
    }

    response = create_patient(payload)

    # Handle API response
    if isinstance(response, dict) and "error" in response:
        st.error("❌ Failed to create patient")
        st.write(response["error"])
    else:
        st.success("✅ Patient created successfully!")
        st.json(response)