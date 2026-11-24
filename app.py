import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# Page Configuration
st.set_page_config(
    page_title="CivicPulse — Public Complaint Resolution Intelligence",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1.1rem; color: #4B5563; margin-bottom: 1.5rem; }
    .metric-card { background: #F3F4F6; border-radius: 10px; padding: 1.2rem; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏛️ CivicPulse: Public Complaint Resolution Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Early-warning decision-support system to predict and triage prolonged administrative resolution delays.</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. Load Trained Model Pipeline
# -------------------------------------------------------------
@st.cache_resource
def load_model():
    model_paths = [
        "civicpulse_model.pkl",
        os.path.join(r"c:\ML PROJECT", "civicpulse_model.pkl"),
        os.path.join("/content", "civicpulse_model.pkl")
    ]
    for path in model_paths:
        if os.path.exists(path):
            try:
                return joblib.load(path)
            except Exception as e:
                st.error(f"Error loading model from {path}: {e}")
    return None

model = load_model()

# -------------------------------------------------------------
# 2. Category to Agency Default Mapping
# -------------------------------------------------------------
COMPLAINT_AGENCY_MAP = {
    "Street Condition": "DOT",
    "Curb Condition": "DOT",
    "Street Light Condition": "DOT",
    "Broken Parking Meter": "DOT",
    "Building/Use": "DOB",
    "Boilers": "DOB",
    "Cranes and Derricks": "DOB",
    "Water System": "DEP",
    "Air Quality": "DEP",
    "Sewer": "DEP",
    "HEAT/HOT WATER": "HPD",
    "PLUMBING": "HPD",
    "UNSANITARY CONDITION": "HPD",
    "Illegal Parking": "NYPD",
    "Noise - Residential": "NYPD",
    "Blocked Driveway": "NYPD",
    "Abandoned Vehicle": "NYPD",
    "Noise - Street/Sidewalk": "NYPD",
    "Commercial Disposal Complaint": "DSNY",
    "Consumer Complaint": "DCWP",
    "Lead": "DOHMH"
}

POPULAR_COMPLAINTS = list(COMPLAINT_AGENCY_MAP.keys())
ALL_AGENCIES = ["DOT", "DEP", "DOB", "HPD", "NYPD", "DSNY", "DOHMH", "DCWP", "DPR", "TLC", "DHS"]
ALL_BOROUGHS = ["BROOKLYN", "QUEENS", "MANHATTAN", "BRONX", "STATEN ISLAND"]
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# -------------------------------------------------------------
# 3. Main Navigation Tabs
# -------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🎯 Delay Radar (Live Predictor)",
    "📊 Bottleneck Overview",
    "🔍 Explainability Panel"
])

# =============================================================
# TAB 1: DELAY RADAR (LIVE PREDICTOR)
# =============================================================
with tab1:
    st.subheader("Intake Complaint Delay Risk Assessment")
    st.markdown("Input registration attributes as recorded by the intake operator. The assessment updates dynamically as you adjust parameters.")

    col_left, col_right = st.columns(2)

    with col_left:
        selected_complaint = st.selectbox(
            "Complaint Category",
            options=POPULAR_COMPLAINTS,
            index=0,
            help="Select the specific nature of the civic problem."
        )

        # Auto-suggest corresponding agency based on selected category
        suggested_agency = COMPLAINT_AGENCY_MAP.get(selected_complaint, "DOT")
        agency_index = ALL_AGENCIES.index(suggested_agency) if suggested_agency in ALL_AGENCIES else 0

        selected_agency = st.selectbox(
            "Assigned Agency / Department",
            options=ALL_AGENCIES,
            index=agency_index,
            help="Municipal department handling the request (automatically synchronized with category)."
        )

        selected_borough = st.selectbox(
            "Borough (Geographic District)",
            options=ALL_BOROUGHS,
            index=1, # Default QUEENS
            help="Borough where the complaint originated."
        )

    with col_right:
        selected_day = st.selectbox(
            "Day of Week Registered",
            options=DAYS_OF_WEEK,
            index=4, # Default Friday
            help="Day of registration. Weekend/Friday evening filings often incur scheduling backlogs."
        )

        selected_hour = st.slider(
            "Submission Hour (24-Hour Clock)",
            min_value=0,
            max_value=23,
            value=19, # Default 19:00 (7 PM)
            format="%d:00",
            help="Hour of the day complaint was submitted."
        )

        selected_month = st.slider(
            "Month of Submission",
            min_value=1,
            max_value=12,
            value=10, # Default October
            format="Month %d",
            help="Month of filing (captures seasonal demand surges)."
        )

    # Prepare DataFrame for Prediction
    input_data = pd.DataFrame([{
        "Problem (formerly Complaint Type)": selected_complaint,
        "Agency": selected_agency,
        "Borough": selected_borough,
        "Created_Hour": selected_hour,
        "Created_DayOfWeek": selected_day,
        "Created_Month": selected_month
    }])

    st.divider()

    # Model Evaluation & Real-Time Output
    if model is not None:
        try:
            delay_prob = model.predict_proba(input_data)[0][1]
            predicted_class = model.predict(input_data)[0]
            is_prolonged = delay_prob >= 0.50

            # Visual Display Columns
            mcol1, mcol2, mcol3 = st.columns([1.5, 2, 2])

            with mcol1:
                st.metric(
                    label="Estimated Delay Risk Probability",
                    value=f"{delay_prob * 100:.1f}%",
                    delta=f"{'+' if is_prolonged else '-'}{abs(delay_prob - 0.50) * 100:.1f}% vs Threshold",
                    delta_color="inverse"
                )

            with mcol2:
                if delay_prob >= 0.65:
                    st.error("🚨 **CRITICAL PROLONGED DELAY RISK**")
                    st.caption("Probability > 65%: Strong likelihood of exceeding the 75th percentile (>61 hours).")
                elif delay_prob >= 0.40:
                    st.warning("⚠️ **ELEVATED MONITORING RECOMMENDED**")
                    st.caption("Probability 40%–64%: Approaching delay threshold; review during daily backlog sweep.")
                else:
                    st.success("✅ **STANDARD RESOLUTION EXPECTED**")
                    st.caption("Probability < 40%: Routine complaint expected to resolve within acceptable shift turnaround.")

            with mcol3:
                st.markdown("**Operational Triage Recommendation:**")
                if is_prolonged:
                    st.info("📌 **Dispatch Action:** Route to supervisor priority queue. Alert field unit manager regarding infrastructure delay risk.")
                else:
                    st.write("🟢 **Standard Route:** Automated assignment to standard field queue; no emergency expediting needed.")

            # Live Progress / Risk Bar
            st.markdown(f"**Delay Risk Intensity Scale:**")
            st.progress(float(min(max(delay_prob, 0.0), 1.0)))

        except Exception as e:
            st.error(f"Error computing prediction: {e}")
    else:
        st.error("Model file 'civicpulse_model.pkl' not found. Please ensure the model file is present in the workspace.")

# =============================================================
# TAB 2: BOTTLENECK OVERVIEW
# =============================================================
with tab2:
    st.subheader("Historical Municipal Bottleneck Overview")
    st.markdown("Empirical benchmark analysis based on historical 311 resolution patterns:")

    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    with col_stat1:
        st.metric("Total Analyzed Records", "312,036", "NYC 311 Callset")
    with col_stat2:
        st.metric("Median Resolution Time", "6.9 Hours", "50% resolved < 7h")
    with col_stat3:
        st.metric("Prolonged Delay Threshold", "61.0 Hours", "75th Percentile (~2.5 Days)")
    with col_stat4:
        st.metric("Upper Outlier Boundary", "150.7 Hours", "IQR Multiplier Cutoff")

    st.divider()

    st.markdown("### Departmental Resolution Profiles")
    bcol1, bcol2 = st.columns(2)

    with bcol1:
        st.markdown("**Agency Risk Stratification:**")
        agency_data = pd.DataFrame({
            "Agency": ["DOT (Transportation)", "DEP (Environmental)", "DOB (Buildings)", "HPD (Housing)", "DSNY (Sanitation)", "NYPD (Police)"],
            "Typical Resolution Scope": ["Complex physical repairs", "Water/sewer infrastructure", "Code inspections", "Residential repairs", "Garbage/Obstruction", "Active patrol enforcement"],
            "Delay Risk Tier": ["High (45%–75%)", "Moderate-High (35%–60%)", "Moderate (30%–50%)", "Moderate (20%–45%)", "Low-Moderate (15%–30%)", "Very Low (0.1%–5%)"]
        })
        st.dataframe(agency_data, use_container_width=True)

    with bcol2:
        st.markdown("**Top Delay-Prone Complaint Categories:**")
        st.markdown("""
        1. 🚧 **Street Condition / Potholes (DOT):** Involves physical road resurfacing; average delay probability > 55%.
        2. 🚰 **Water System / Water Quality (DEP):** Requires specialized hydrologic crews and sample lab testing.
        3. 🏢 **Building/Use Violations (DOB):** Multi-stage legal notices and mandatory inspector physical visits.
        4. ❄️ **HEAT/HOT WATER (HPD):** Surges sharply in winter months (Nov–Feb); heavy weekend queue backlogs.
        5. 🚗 **Illegal Parking / Noise (NYPD):** Resolved rapidly by mobile patrol cars (typically under 3 hours).
        """)

# =============================================================
# TAB 3: EXPLAINABILITY PANEL
# =============================================================
with tab3:
    st.subheader("Model Explainability & Key Delay Drivers")
    st.markdown("""
    CivicPulse uses a **Tuned Logistic Regression** pipeline with balanced class weighting. 
    Because Logistic Regression is inherently linear, each feature's contribution can be directly understood through its **mathematical coefficient (log-odds ratio)**.
    """)

    ecol1, ecol2 = st.columns([1.5, 1])

    with ecol1:
        st.markdown("### Top Influential Feature Weights")
        feature_weights = pd.DataFrame({
            "Feature Factor": [
                "Agency: NYPD (Police Patrol)",
                "Complaint: Street Condition (DOT)",
                "Complaint: Food Establishment (DOHMH)",
                "Complaint: Curb Condition (DOT)",
                "Complaint: Green Infrastructure (DEP)",
                "Complaint: Street Light Condition (DOT)",
                "Registration: Friday Evening (Holdover)",
                "Registration: Weekend Submission",
                "Agency: DOT (Transportation)",
                "Complaint: Illegal Parking (NYPD)"
            ],
            "Effect on Delay": [
                "Strongly Decreases Delay (-6.18)",
                "Strongly Increases Delay (+3.49)",
                "Increases Delay (+3.53)",
                "Increases Delay (+3.49)",
                "Increases Delay (+2.99)",
                "Increases Delay (+2.78)",
                "Increases Delay (+0.85)",
                "Increases Delay (+0.62)",
                "Increases Delay (+1.15)",
                "Strongly Decreases Delay (-4.78)"
            ],
            "Operational Impact": [
                "Rapid mobile patrol resolution",
                "Requires asphalt asphalt crews",
                "Health inspector visit required",
                "Sidewalk/curb replacement labor",
                "Drainage/bioswale engineering",
                "Electrical repair crew required",
                "Administrative offices closed over weekend",
                "Skeleton staffing until Monday morning",
                "Backlog in capital infrastructure repair",
                "Immediate field summons issued"
            ]
        })
        st.dataframe(feature_weights, use_container_width=True)

    with ecol2:
        st.markdown("### Why Decision Support Matters (Cost Framing)")
        st.markdown("""
        * **False Negatives are Costly:**
          When the city misses a complaint that encounters prolonged delay, citizen trust collapses and municipal safety hazards escalate.
        * **False Positives are Cheap:**
          If the system flags a complaint that would have resolved normally, a dispatcher merely performs a 30-second verification check.
        * **Decision Support vs. Automation:**
          CivicPulse never automatically closes tickets. It provides early warning alerts to optimize staff allocation.
        """)

    st.divider()
    st.caption("CivicPulse CSE303 Capstone System • Built with Scikit-Learn and Streamlit")
