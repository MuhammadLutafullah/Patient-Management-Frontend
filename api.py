import requests

BASE_URL = "https://patient-management-backend-production-0a5b.up.railway.app"


# -------------------
# Safe request helper
# -------------------
def safe_request(method, url, data=None):
    try:
        if method == "GET":
            res = requests.get(url, timeout=10)
        elif method == "POST":
            res = requests.post(url, json=data, timeout=10)
        elif method == "PUT":
            res = requests.put(url, json=data, timeout=10)
        elif method == "DELETE":
            res = requests.delete(url, timeout=10)
        else:
            return {"error": "Invalid HTTP method"}

        res.raise_for_status()
        return res.json()

    except Exception as e:
        return {"error": str(e)}


# -------------------
# Patients APIs
# -------------------
def get_patients():
    return safe_request("GET", f"{BASE_URL}/")


def create_patient(data):
    return safe_request("POST", f"{BASE_URL}/create", data)


def update_patient(patient_id, data):
    return safe_request("PUT", f"{BASE_URL}/edit/{patient_id}", data)


def delete_patient(patient_id):
    return safe_request("DELETE", f"{BASE_URL}/delete/{patient_id}")


# -------------------
# Cities API
# -------------------
def get_cities():
    return safe_request("GET", f"{BASE_URL}/cities/")