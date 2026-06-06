import streamlit as st
import pandas as pd
import numpy as np

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="MediCore Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
    /* ---- Google Fonts ---- */
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    /* ---- Root Variables ---- */
    :root {
        --bg-main:       #f0f4f8;
        --bg-card:       #ffffff;
        --bg-card2:      #f8fafc;
        --accent-teal:   #0891b2;
        --accent-blue:   #2563eb;
        --accent-pink:   #db2777;
        --accent-amber:  #d97706;
        --accent-green:  #059669;
        --text-primary:  #1e293b;
        --text-muted:    #64748b;
        --border:        #e2e8f0;
        --shadow:        0 4px 20px rgba(0,0,0,0.08);
    }

    /* ---- Global Reset ---- */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
    }

    /* ---- Hide Streamlit Branding ---- */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }

    /* ---- App Background ---- */
    .stApp {
        background: #f0f4f8 !important;
        background-color: #f0f4f8 !important;
    }

    /* ---- Sidebar ---- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%) !important;
        border-right: 1px solid var(--border);
        box-shadow: 2px 0 12px rgba(0,0,0,0.05);
    }
    [data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem; }

    /* ---- Sidebar Logo Area ---- */
    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 1rem 0.5rem 1.5rem;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    }
    .sidebar-logo-icon {
        width: 44px; height: 44px;
        background: linear-gradient(135deg, var(--accent-teal), var(--accent-blue));
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 22px;
        box-shadow: 0 4px 16px rgba(0,212,177,0.35);
    }
    .sidebar-logo-text {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 1.25rem;
        color: #1e293b;
        line-height: 1.1;
    }
    .sidebar-logo-sub {
        font-size: 0.7rem;
        color: var(--accent-teal);
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    /* ---- Nav Buttons ---- */
    .nav-section-label {
        font-size: 0.65rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #94a3b8;
        padding: 0 0.5rem;
        margin-bottom: 0.5rem;
    }
    .stButton > button {
        width: 100%;
        background: #f1f5f9 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        color: #475569 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        padding: 0.65rem 1rem !important;
        margin-bottom: 6px !important;
        text-align: left !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    .stButton > button:hover {
        background: #e0f2fe !important;
        border-color: var(--accent-teal) !important;
        color: var(--accent-teal) !important;
        transform: translateX(4px) !important;
        box-shadow: 0 2px 12px rgba(8,145,178,0.15) !important;
    }

    /* Active nav button override via class */
    .nav-active > button {
        background: linear-gradient(135deg, #e0f2fe, #dbeafe) !important;
        border-color: var(--accent-teal) !important;
        color: var(--accent-teal) !important;
        box-shadow: 0 2px 10px rgba(8,145,178,0.2) !important;
    }

    /* ---- Main Content ---- */
    .main .block-container {
        padding: 2rem 2.5rem;
        max-width: 1400px;
    }

    /* ---- Page Header ---- */
    .page-header {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #e2e8f0;
    }
    .page-header-icon {
        font-size: 2.2rem;
        line-height: 1;
        margin-top: 2px;
    }
    .page-header-title {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 2rem;
        color: #1e293b;
        line-height: 1.15;
        margin: 0;
    }
    .page-header-sub {
        font-size: 0.85rem;
        color: #64748b;
        margin-top: 2px;
    }

    /* ---- Metric Cards ---- */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.2rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.4rem 1.5rem;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 16px 16px 0 0;
    }
    .metric-card.teal::before  { background: linear-gradient(90deg, var(--accent-teal), var(--accent-blue)); }
    .metric-card.blue::before  { background: linear-gradient(90deg, var(--accent-blue), #6366f1); }
    .metric-card.pink::before  { background: linear-gradient(90deg, var(--accent-pink), #a855f7); }
    .metric-card.amber::before { background: linear-gradient(90deg, var(--accent-amber), #f97316); }
    .metric-card:hover { transform: translateY(-3px); box-shadow: var(--shadow); }
    .metric-label {
        font-size: 0.72rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #64748b;
        margin-bottom: 0.6rem;
    }
    .metric-value {
        font-family: 'Syne', sans-serif;
        font-size: 2.4rem;
        font-weight: 800;
        color: #1e293b;
        line-height: 1;
        margin-bottom: 0.4rem;
    }
    .metric-icon {
        position: absolute;
        right: 1.2rem; top: 1.2rem;
        font-size: 1.8rem;
        opacity: 0.2;
    }
    .metric-delta {
        font-size: 0.75rem;
        color: var(--accent-teal);
    }

    /* ---- Section Cards ---- */
    .section-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .section-card-title {
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        color: #1e293b;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* ---- Dataframe ---- */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e2e8f0 !important;
    }
    [data-testid="stDataFrame"] > div {
        border-radius: 12px;
        background: #f8fafc !important;
    }
    .dataframe { background: transparent !important; }
    .dataframe th {
        background: #e0f2fe !important;
        color: #0891b2 !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        border: none !important;
        padding: 0.8rem 1rem !important;
    }
    .dataframe td {
        background: #ffffff !important;
        color: #1e293b !important;
        border-bottom: 1px solid #f1f5f9 !important;
        font-size: 0.85rem !important;
        padding: 0.7rem 1rem !important;
    }
    .dataframe tr:hover td { background: #f0f9ff !important; }

    /* ---- Inputs ---- */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        color: #1e293b !important;
        font-family: 'DM Sans', sans-serif !important;
        padding: 0.6rem 1rem !important;
    }
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border-color: #0891b2 !important;
        box-shadow: 0 0 0 3px rgba(8,145,178,0.15) !important;
    }
    .stSelectbox [data-baseweb="select"] > div {
        background: #ffffff !important;
        border-color: #cbd5e1 !important;
        color: #1e293b !important;
        border-radius: 10px !important;
    }

    /* ---- Slider ---- */
    .stSlider [data-baseweb="slider"] {
        padding: 0.5rem 0;
    }
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background: #0891b2 !important;
        border-color: #0891b2 !important;
    }
    .stSlider [data-baseweb="slider"] div[data-testid="stThumbValue"] {
        background: #0891b2 !important;
        color: #fff !important;
        border-radius: 6px !important;
    }

    /* ---- Labels ---- */
    .stTextInput label, .stSelectbox label, .stSlider label {
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        color: #475569 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        margin-bottom: 4px !important;
    }

    /* ---- Status Badge ---- */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    .badge-green  { background: rgba(16,185,129,0.15); color: #10b981; }
    .badge-red    { background: rgba(239,68,68,0.15);  color: #ef4444; }
    .badge-yellow { background: rgba(251,191,36,0.15); color: #fbbf24; }

    /* ---- Chart ---- */
    .stBarChart { border-radius: 12px; overflow: hidden; }

    /* ---- Divider ---- */
    hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

    /* ---- Footer ---- */
    .footer {
        text-align: center;
        padding: 1.5rem 0 0.5rem;
        color: #64748b;
        font-size: 0.78rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 2rem;
    }
    .footer span { color: #0891b2; font-weight: 600; }

    /* ---- Alert/Info Boxes ---- */
    .info-box {
        background: rgba(59,130,246,0.08);
        border: 1px solid rgba(59,130,246,0.2);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        font-size: 0.85rem;
        color: #93c5fd;
        margin-bottom: 1rem;
    }

    /* ---- Scrollbar ---- */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #0891b2; }
</style>
""", unsafe_allow_html=True)

# ------------------ SAMPLE DATA (fallback if CSVs missing) ------------------
def load_data():
    try:
        doctors = pd.read_csv("doctors.csv")
    except:
        doctors = pd.DataFrame({
            "doctor_id":   [f"D{i:03d}" for i in range(1, 9)],
            "doctor_name": ["Dr. Priya Sharma","Dr. Arjun Mehta","Dr. Sneha Rao",
                            "Dr. Vikram Joshi","Dr. Anjali Nair","Dr. Rahul Patil",
                            "Dr. Meera Iyer","Dr. Suresh Desai"],
            "specialization": ["Cardiology","Orthopedics","Neurology","Pediatrics",
                               "Dermatology","ENT","Gynecology","General Surgery"],
            "experience_yrs": [12,8,15,6,10,9,11,14],
            "contact": ["9876543210","9123456789","9988776655","9871234567",
                        "9001122334","9876512345","9345678901","9654321987"],
        })
    try:
        patients = pd.read_csv("Patient.csv")
    except:
        patients = pd.DataFrame({
            "patient_id":   [f"P{i:03d}" for i in range(1, 13)],
            "patient_name": ["Ravi Kumar","Sunita Devi","Amit Gupta","Priya Verma",
                             "Rohit Singh","Kavya Reddy","Anil Tiwari","Deepa Nair",
                             "Sunil Pandey","Meena Joshi","Rahul Das","Pooja Malhotra"],
            "age":          [34,52,28,41,60,23,47,35,55,30,45,38],
            "gender":       ["M","F","M","F","M","F","M","F","M","F","M","F"],
            "city":         ["Pune","Mumbai","Delhi","Hyderabad","Pune","Bangalore",
                             "Mumbai","Chennai","Delhi","Pune","Hyderabad","Bangalore"],
            "blood_group":  ["A+","B+","O+","AB+","A-","B-","O-","AB-","A+","B+","O+","A-"],
        })
    try:
        appointments = pd.read_csv("appointments.csv")
    except:
        statuses = ["Completed","Scheduled","Cancelled","Pending"]
        appointments = pd.DataFrame({
            "appt_id":      [f"A{i:03d}" for i in range(1, 21)],
            "patient_name": np.random.choice(patients["patient_name"].tolist(), 20),
            "doctor_name":  np.random.choice(doctors["doctor_name"].tolist(), 20),
            "date":         pd.date_range("2024-01-01", periods=20, freq="7D").strftime("%Y-%m-%d"),
            "status":       np.random.choice(statuses, 20, p=[0.5,0.3,0.1,0.1]),
        })
    try:
        medicines = pd.read_csv("medicines.csv")
    except:
        medicines = pd.DataFrame({
            "medicine_id":   [f"M{i:03d}" for i in range(1, 16)],
            "name":          ["Paracetamol","Amoxicillin","Ibuprofen","Cetirizine","Metformin",
                              "Omeprazole","Amlodipine","Atorvastatin","Azithromycin","Pantoprazole",
                              "Losartan","Vitamin D3","Dolo 650","Crocin","Aspirin"],
            "category":      ["Analgesic","Antibiotic","NSAID","Antihistamine","Antidiabetic",
                              "PPI","CCB","Statin","Antibiotic","PPI",
                              "ARB","Supplement","Analgesic","Analgesic","Antiplatelet"],
            "stock":         [500,200,350,180,420,300,150,220,190,310,140,600,400,380,250],
            "price":         [10,85,35,40,55,60,120,150,90,65,110,200,25,20,15],
            "manufacturer":  ["Cipla","Abbott","Sun Pharma","GSK","Mankind","Torrent",
                              "Lupin","Pfizer","Zydus","AstraZeneca","Wockhardt","HealthKart",
                              "Micro Labs","GSK","Bayer"],
        })
    return doctors, patients, appointments, medicines

doctors, patients, appointments, medicines = load_data()

# ------------------ SESSION STATE ------------------
if "page" not in st.session_state:
    st.session_state.page = "Dashboard Overview"

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🏥</div>
        <div>
            <div class="sidebar-logo-text">MediCore</div>
            <div class="sidebar-logo-sub">Hospital System</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-section-label">Main Navigation</div>', unsafe_allow_html=True)

    nav_items = [
        ("📊", "Dashboard Overview"),
        ("👨‍⚕️", "Doctors"),
        ("🧑", "Patients"),
        ("📅", "Appointments"),
        ("💊", "Medicines"),
    ]

    for icon, label in nav_items:
        active_class = "nav-active" if st.session_state.page == label else ""
        col = st.container()
        with col:
            if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True):
                st.session_state.page = label
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="nav-section-label">System Info</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:#f0fdf4;border:1px solid #bbf7d0;
                border-radius:10px;padding:0.9rem 1rem;font-size:0.78rem;color:#475569;line-height:1.8;">
        🗓️ <b style="color:#1e293b">June 2025</b><br>
        🔄 Data refreshed<br>
        🟢 <span style="color:#059669">System Operational</span>
    </div>
    """, unsafe_allow_html=True)

page = st.session_state.page

# ------------------ DASHBOARD OVERVIEW ------------------
if page == "Dashboard Overview":
    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">📊</div>
        <div>
            <div class="page-header-title">Dashboard Overview</div>
            <div class="page-header-sub">Real-time hospital metrics and operational summary</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Metric Cards
    total_docs  = len(doctors)
    total_pats  = len(patients)
    total_appts = len(appointments)
    total_meds  = len(medicines)

    completed = len(appointments[appointments["status"] == "Completed"]) if "status" in appointments.columns else 0
    scheduled = len(appointments[appointments["status"] == "Scheduled"]) if "status" in appointments.columns else 0

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card teal">
            <div class="metric-icon">👨‍⚕️</div>
            <div class="metric-label">Total Doctors</div>
            <div class="metric-value">{total_docs}</div>
            <div class="metric-delta">↑ Active Specialists</div>
        </div>
        <div class="metric-card blue">
            <div class="metric-icon">🧑</div>
            <div class="metric-label">Total Patients</div>
            <div class="metric-value">{total_pats}</div>
            <div class="metric-delta">↑ Registered Records</div>
        </div>
        <div class="metric-card pink">
            <div class="metric-icon">📅</div>
            <div class="metric-label">Appointments</div>
            <div class="metric-value">{total_appts}</div>
            <div class="metric-delta">✓ {completed} Completed</div>
        </div>
        <div class="metric-card amber">
            <div class="metric-icon">💊</div>
            <div class="metric-label">Medicines</div>
            <div class="metric-value">{total_meds}</div>
            <div class="metric-delta">↑ In Inventory</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Charts Row
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-card-title">📈 Appointment Status Breakdown</div>', unsafe_allow_html=True)
        if "status" in appointments.columns:
            status_counts = appointments["status"].value_counts().rename_axis("Status").reset_index(name="Count")
            st.bar_chart(status_counts.set_index("Status"), color="#00d4b1", height=230)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-card-title">🏙️ Patients by City</div>', unsafe_allow_html=True)
        if "city" in patients.columns:
            city_counts = patients["city"].value_counts().rename_axis("City").reset_index(name="Patients")
            st.bar_chart(city_counts.set_index("City"), color="#3b82f6", height=230)
        st.markdown('</div>', unsafe_allow_html=True)

    # Recent Appointments
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-card-title">🕐 Recent Appointments</div>', unsafe_allow_html=True)
    st.dataframe(appointments.tail(8), use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ DOCTORS PAGE ------------------
elif page == "Doctors":
    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">👨‍⚕️</div>
        <div>
            <div class="page-header-title">Doctors</div>
            <div class="page-header-sub">Manage and view doctor profiles and specializations</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍  Search by Name or Specialization", placeholder="e.g. Cardiology, Dr. Sharma…")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:rgba(0,212,177,0.08);border:1px solid rgba(0,212,177,0.2);
                    border-radius:10px;padding:0.75rem 1rem;font-size:0.85rem;color:#94a3b8;">
            Total: <b style="color:#00d4b1">{len(doctors)} Doctors</b> on record
        </div>
        """, unsafe_allow_html=True)

    filtered_docs = doctors.copy()
    if search:
        mask = doctors.apply(lambda col: col.astype(str).str.contains(search, case=False)).any(axis=1)
        filtered_docs = doctors[mask]

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-card-title">📋 Doctor Records ({len(filtered_docs)} shown)</div>', unsafe_allow_html=True)
    st.dataframe(filtered_docs, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if "specialization" in doctors.columns:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-card-title">🏷️ Doctors by Specialization</div>', unsafe_allow_html=True)
        spec_counts = doctors["specialization"].value_counts().rename_axis("Specialization").reset_index(name="Count")
        st.bar_chart(spec_counts.set_index("Specialization"), color="#00d4b1", height=200)
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------ PATIENTS PAGE ------------------
elif page == "Patients":
    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">🧑</div>
        <div>
            <div class="page-header-title">Patients</div>
            <div class="page-header-sub">Browse and filter patient records by location and demographics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        city_options = ["All"] + sorted(patients["city"].unique().tolist()) if "city" in patients.columns else ["All"]
        city_filter = st.selectbox("🏙️  Filter by City", city_options)
    with col2:
        gender_options = ["All"] + sorted(patients["gender"].unique().tolist()) if "gender" in patients.columns else ["All"]
        gender_filter = st.selectbox("👤  Filter by Gender", gender_options)
    with col3:
        search_pat = st.text_input("🔍  Search Patient", placeholder="Name or ID…")

    filtered_pats = patients.copy()
    if city_filter != "All" and "city" in patients.columns:
        filtered_pats = filtered_pats[filtered_pats["city"] == city_filter]
    if gender_filter != "All" and "gender" in patients.columns:
        filtered_pats = filtered_pats[filtered_pats["gender"] == gender_filter]
    if search_pat:
        mask = filtered_pats.apply(lambda col: col.astype(str).str.contains(search_pat, case=False)).any(axis=1)
        filtered_pats = filtered_pats[mask]

    # Stats row
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="section-card" style="text-align:center;padding:1rem">
            <div style="font-size:1.8rem;font-family:'Syne',sans-serif;font-weight:800;color:#2563eb">{len(filtered_pats)}</div>
            <div style="font-size:0.75rem;color:#64748b;text-transform:uppercase;letter-spacing:.1em">Filtered Patients</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        avg_age = int(filtered_pats["age"].mean()) if "age" in filtered_pats.columns and len(filtered_pats) > 0 else "—"
        st.markdown(f"""<div class="section-card" style="text-align:center;padding:1rem">
            <div style="font-size:1.8rem;font-family:'Syne',sans-serif;font-weight:800;color:#db2777">{avg_age}</div>
            <div style="font-size:0.75rem;color:#64748b;text-transform:uppercase;letter-spacing:.1em">Avg Age</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        cities_count = filtered_pats["city"].nunique() if "city" in filtered_pats.columns else "—"
        st.markdown(f"""<div class="section-card" style="text-align:center;padding:1rem">
            <div style="font-size:1.8rem;font-family:'Syne',sans-serif;font-weight:800;color:#0891b2">{cities_count}</div>
            <div style="font-size:0.75rem;color:#64748b;text-transform:uppercase;letter-spacing:.1em">Cities</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-card-title">📋 Patient Records ({len(filtered_pats)} shown)</div>', unsafe_allow_html=True)
    st.dataframe(filtered_pats, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ APPOINTMENTS PAGE ------------------
elif page == "Appointments":
    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">📅</div>
        <div>
            <div class="page-header-title">Appointments</div>
            <div class="page-header-sub">Track and manage all scheduled patient appointments</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        status_options = ["All"] + sorted(appointments["status"].unique().tolist()) if "status" in appointments.columns else ["All"]
        status_filter = st.selectbox("🏷️  Filter by Status", status_options)
    with col2:
        doc_options = ["All"] + sorted(appointments["doctor_name"].unique().tolist()) if "doctor_name" in appointments.columns else ["All"]
        doc_filter = st.selectbox("👨‍⚕️  Filter by Doctor", doc_options)
    with col3:
        search_appt = st.text_input("🔍  Search Appointment", placeholder="Patient, doctor…")

    filtered_appts = appointments.copy()
    if status_filter != "All" and "status" in appointments.columns:
        filtered_appts = filtered_appts[filtered_appts["status"] == status_filter]
    if doc_filter != "All" and "doctor_name" in appointments.columns:
        filtered_appts = filtered_appts[filtered_appts["doctor_name"] == doc_filter]
    if search_appt:
        mask = filtered_appts.apply(lambda col: col.astype(str).str.contains(search_appt, case=False)).any(axis=1)
        filtered_appts = filtered_appts[mask]

    # Status summary badges
    if "status" in appointments.columns:
        status_vals = appointments["status"].value_counts()
        badges_html = " ".join([
            f'<span class="badge badge-{"green" if s=="Completed" else "yellow" if s=="Scheduled" else "red"}">{s}: {c}</span>'
            for s, c in status_vals.items()
        ])
        st.markdown(f'<div style="margin-bottom:1rem;display:flex;gap:8px;flex-wrap:wrap">{badges_html}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-card-title">📋 Appointment Records ({len(filtered_appts)} shown)</div>', unsafe_allow_html=True)
    st.dataframe(filtered_appts, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ MEDICINES PAGE ------------------
elif page == "Medicines":
    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">💊</div>
        <div>
            <div class="page-header-title">Medicines</div>
            <div class="page-header-sub">Inventory management and pricing overview</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.5, 1])
    with col1:
        max_price = int(medicines["price"].max()) if "price" in medicines.columns else 500
        price_filter = st.slider("💰  Max Price (₹)", 0, max_price, max_price, step=5)
    with col2:
        cat_options = ["All"] + sorted(medicines["category"].unique().tolist()) if "category" in medicines.columns else ["All"]
        cat_filter = st.selectbox("🏷️  Filter by Category", cat_options)
    search_med = st.text_input("🔍  Search Medicine", placeholder="Name, manufacturer…")

    filtered_meds = medicines.copy()
    if "price" in medicines.columns:
        filtered_meds = filtered_meds[filtered_meds["price"] <= price_filter]
    if cat_filter != "All" and "category" in medicines.columns:
        filtered_meds = filtered_meds[filtered_meds["category"] == cat_filter]
    if search_med:
        mask = filtered_meds.apply(lambda col: col.astype(str).str.contains(search_med, case=False)).any(axis=1)
        filtered_meds = filtered_meds[mask]

    # Summary stats
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="section-card" style="text-align:center;padding:1rem">
            <div style="font-size:1.8rem;font-family:'Syne',sans-serif;font-weight:800;color:#fbbf24">{len(filtered_meds)}</div>
            <div style="font-size:0.75rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.1em">Medicines</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        avg_price = f"₹{filtered_meds['price'].mean():.0f}" if "price" in filtered_meds.columns and len(filtered_meds) > 0 else "—"
        st.markdown(f"""<div class="section-card" style="text-align:center;padding:1rem">
            <div style="font-size:1.8rem;font-family:'Syne',sans-serif;font-weight:800;color:#00d4b1">{avg_price}</div>
            <div style="font-size:0.75rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.1em">Avg Price</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        total_stock = f"{filtered_meds['stock'].sum():,}" if "stock" in filtered_meds.columns and len(filtered_meds) > 0 else "—"
        st.markdown(f"""<div class="section-card" style="text-align:center;padding:1rem">
            <div style="font-size:1.8rem;font-family:'Syne',sans-serif;font-weight:800;color:#f472b6">{total_stock}</div>
            <div style="font-size:0.75rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.1em">Total Stock</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-card-title">📋 Medicine Inventory ({len(filtered_meds)} shown)</div>', unsafe_allow_html=True)
    st.dataframe(filtered_meds, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if "category" in filtered_meds.columns and len(filtered_meds) > 0:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-card-title">📊 Medicines by Category</div>', unsafe_allow_html=True)
        cat_counts = filtered_meds["category"].value_counts().rename_axis("Category").reset_index(name="Count")
        st.bar_chart(cat_counts.set_index("Category"), color="#fbbf24", height=200)
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------ FOOTER ------------------
st.markdown("""
<div class="footer">
    Developed by <span>Atharvi Babhare</span> &nbsp;|&nbsp; DBMS Internship Project &nbsp;|&nbsp; MediCore Hospital Management System
</div>
""", unsafe_allow_html=True)
