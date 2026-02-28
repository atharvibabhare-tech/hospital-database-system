import streamlit as st
import pandas as pd

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Hospital Dashboard",
    page_icon="🏥",
    layout="wide"
)

# ------------------ TITLE ------------------
st.markdown(
    "<h1 style='text-align: center; color: #2E86C1;'>🏥 Hospital Management Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown("---")

# ------------------ LOAD SAMPLE DATA ------------------
# (For deployment, you can replace this with CSV or database connection)

doctors = pd.read_csv("doctors.csv")
patients = pd.read_csv("patients.csv")
appointments = pd.read_csv("appointments.csv")
medicines = pd.read_csv("medicines.csv")

# ------------------ SIDEBAR ------------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["Dashboard Overview", "Doctors", "Patients", "Appointments", "Medicines"])

# ------------------ DASHBOARD OVERVIEW ------------------
if page == "Dashboard Overview":

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👨‍⚕️ Total Doctors", len(doctors))
    col2.metric("🧑‍🤝‍🧑 Total Patients", len(patients))
    col3.metric("📅 Total Appointments", len(appointments))
    col4.metric("💊 Total Medicines", len(medicines))

    st.markdown("---")

    st.subheader("📊 Appointments Status Distribution")
    st.bar_chart(appointments["status"].value_counts())

# ------------------ DOCTORS PAGE ------------------
elif page == "Doctors":

    st.subheader("👨‍⚕️ Doctors Information")

    search = st.text_input("Search Doctor by Name")

    if search:
        filtered = doctors[doctors["doctor_name"].str.contains(search, case=False)]
        st.dataframe(filtered, use_container_width=True)
    else:
        st.dataframe(doctors, use_container_width=True)

# ------------------ PATIENTS PAGE ------------------
elif page == "Patients":

    st.subheader("🧑 Patients Information")

    city_filter = st.selectbox("Filter by City", ["All"] + list(patients["city"].unique()))

    if city_filter != "All":
        filtered = patients[patients["city"] == city_filter]
        st.dataframe(filtered, use_container_width=True)
    else:
        st.dataframe(patients, use_container_width=True)

# ------------------ APPOINTMENTS PAGE ------------------
elif page == "Appointments":

    st.subheader("📅 Appointments Details")

    status_filter = st.selectbox("Filter by Status", ["All"] + list(appointments["status"].unique()))

    if status_filter != "All":
        filtered = appointments[appointments["status"] == status_filter]
        st.dataframe(filtered, use_container_width=True)
    else:
        st.dataframe(appointments, use_container_width=True)

# ------------------ MEDICINES PAGE ------------------
elif page == "Medicines":

    st.subheader("💊 Medicines")

    price_filter = st.slider("Show medicines cheaper than:", 0, 500, 200)

    filtered = medicines[medicines["price"] <= price_filter]
    st.dataframe(filtered, use_container_width=True)

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: grey;'>Developed by Atharvi Babhare | DBMS Internship Project</p>",
    unsafe_allow_html=True
)
