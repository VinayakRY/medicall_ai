import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

API_URL = "http://127.0.0.1:8000"

# ===================================
# PAGE CONFIG
# ===================================

st.set_page_config(
    page_title="MediCall AI",
    layout="wide"
)

# ===================================
# SIDEBAR
# ===================================

with st.sidebar:

    selected = option_menu(
        menu_title="🏥 MediCall AI",

        options=[
            "Dashboard",
            "Patients",
            "Appointments",
            "AI Calling",
            "AI Assistant"
        ],

        icons=[
            "house",
            "people",
            "calendar",
            "telephone",
            "robot"
        ],

        default_index=0
    )

# ==========================================
# DASHBOARD
# ==========================================

if selected == "Dashboard":

    st.title("🏥 MediCall AI Dashboard")

    # =========================
    # FETCH DATA
    # =========================

    patients = requests.get(
        f"{API_URL}/patients"
    ).json()

    appointments = requests.get(
        f"{API_URL}/appointments"
    ).json()

    total_patients = len(patients)

    total_appointments = len(appointments)

    total_calls = total_patients * 3

    revenue = total_appointments * 500

    # =========================
    # TOP CARDS
    # =========================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👨‍⚕️ Total Patients",
            total_patients,
            "+12%"
        )

    with col2:
        st.metric(
            "📞 AI Calls",
            total_calls,
            "+18%"
        )

    with col3:
        st.metric(
            "📅 Appointments",
            total_appointments,
            "-4%"
        )

    with col4:
        st.metric(
            "💰 Revenue",
            f"₹{revenue}",
            "+9%"
        )

    st.divider()

    # =========================
    # CHARTS
    # =========================

    left, right = st.columns([2, 1])

    with left:

        st.subheader(
            "📈 AI Call Analytics"
        )

        chart_data = pd.DataFrame({
            "Day": [
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat"
            ],

            "Calls": [
                120,
                200,
                170,
                250,
                310,
                280
            ]
        })

        st.line_chart(
            chart_data.set_index("Day")
        )

    with right:

        st.subheader(
            "📊 Call Status"
        )

        status_data = pd.DataFrame({
            "Status": [
                "Completed",
                "Missed",
                "Pending"
            ],

            "Count": [
                70,
                20,
                10
            ]
        })

        st.bar_chart(
            status_data.set_index("Status")
        )

    st.divider()

    # =========================
    # RECENT PATIENTS
    # =========================

    st.subheader(
        "🧾 Recent Patients"
    )

    if patients:

        patient_df = pd.DataFrame(
            patients
        )

        st.dataframe(
            patient_df,
            use_container_width=True
        )

    else:
        st.info(
            "No Patients Found"
        )

    st.divider()

    # =========================
    # RECENT APPOINTMENTS
    # =========================

    st.subheader(
        "📅 Upcoming Appointments"
    )

    if appointments:

        appointment_df = pd.DataFrame(
            appointments
        )

        st.dataframe(
            appointment_df,
            use_container_width=True
        )

    else:
        st.info(
            "No Appointments Found"
        )

# ===================================
# PATIENTS
# ===================================

elif selected == "Patients":

    st.title("👨‍⚕️ Patients")

    name = st.text_input(
        "Patient Name"
    )

    phone = st.text_input(
        "Phone Number"
    )

    language = st.selectbox(
        "Language",
        [
            "Hindi",
            "English"
        ]
    )

    if st.button("Add Patient"):

        response = requests.post(
            f"{API_URL}/add-patient",
            params={
                "name": name,
                "phone": phone,
                "language": language
            }
        )

        st.success(
            response.json()["message"]
        )

    # =========================
    # PATIENT RECORDS
    # =========================

    st.subheader("📋 Patient Records")

    response = requests.get(
        f"{API_URL}/patients"
    )

    patients = response.json()

    st.dataframe(
        patients,
        use_container_width=True
    )

    # =========================
    # DELETE PATIENT
    # =========================

    st.markdown("---")

    st.subheader("🗑 Delete Patient")

    delete_id = st.number_input(
        "Enter Patient ID to Delete",
        min_value=1,
        step=1
    )

    if st.button("Delete Patient"):

        response = requests.delete(
            f"{API_URL}/delete-patient/{delete_id}"
        )

        st.warning(
            response.json()["message"]
        )

        st.rerun()

# ===================================
# APPOINTMENTS
# ===================================

elif selected == "Appointments":

    st.title("📅 Appointments")

    patient_id = st.number_input(
        "Patient ID",
        min_value=1
    )

    doctor_name = st.text_input(
        "Doctor Name"
    )

    appointment_date = st.text_input(
        "Appointment Date",
        value="2026-05-21 10:30"
    )

    if st.button("Book Appointment"):

        response = requests.post(
            f"{API_URL}/add-appointment",
            params={
                "patient_id": patient_id,
                "doctor_name": doctor_name,
                "appointment_date": appointment_date
            }
        )

        st.success(
            response.json()["message"]
        )

    # =========================
    # APPOINTMENT RECORDS
    # =========================

    st.subheader("📋 Appointment Records")

    response = requests.get(
        f"{API_URL}/appointments"
    )

    appointments = response.json()

    st.dataframe(
        appointments,
        use_container_width=True
    )

# ===================================
# AI CALLING
# ===================================

elif selected == "AI Calling":

    st.title("📞 AI Voice Calling")

    phone = st.text_input(
        "Phone Number"
    )

    if st.button("Call Patient"):

        response = requests.post(
            f"{API_URL}/call-patient",
            params={
                "phone": phone
            }
        )

        st.success(
            response.json()["message"]
        )

# ===================================
# AI ASSISTANT
# ===================================

elif selected == "AI Assistant":

    st.title("🤖 AI Assistant")

    message = st.text_area(
        "Ask AI"
    )

    if st.button("Ask AI"):

        response = requests.post(
            f"{API_URL}/ai-chat",
            params={
                "message": message
            }
        )

        st.success(
            response.json()["response"]
        )