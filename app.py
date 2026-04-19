import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load models
duration_model = joblib.load("duration_model.pkl")
eff_model = joblib.load("efficiency_model.pkl")

st.set_page_config(
    page_title="Aid Project Prediction System",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(
            rgba(0, 0, 0, 0.7), 
            rgba(0, 0, 0, 0.7)
        ),
        url("https://images.unsplash.com/photo-1521791136064-7986c2920216");
        
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    /* Make text white for visibility */
    h1, h2, h3, h4, h5, h6, p, label, div {
        color: white !important;
    }

    /* Style input boxes */
    .stTextInput input, .stNumberInput input {
        background-color: rgba(255,255,255,0.9);
        color: black;
        border-radius: 8px;
    }

    /* Style buttons */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .block-container {
        background: rgba(0, 0, 0, 0.6);
        padding: 2rem;
        border-radius: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* General input fields */
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        background-color: #1e1e1e !important;
        color: white !important;
        border: 1px solid #444 !important;
        border-radius: 8px;
    }

    /* Selectbox */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #1e1e1e !important;
        color: white !important;
        border-radius: 8px;
    }

    /* Dropdown menu */
    div[data-baseweb="popover"] {
        background-color: #1e1e1e !important;
        color: white !important;
    }

    /* Sliders */
    .stSlider > div {
        color: white !important;
    }

    /* Labels */
    label {
        color: #dddddd !important;
        font-weight: 500;
    }

    /* Placeholder text */
    input::placeholder, textarea::placeholder {
        color: #aaaaaa !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.title("Aid Project Prediction System")
st.markdown("Estimate project duration and efficiency using AI.")

# Inputs
text = st.text_area("Project Description")
reporting = st.text_input("Reporting Organization")

df = pd.read_csv("../Data/iati-activities-in-kenya-no-location-information.csv")

sectors = df["sector_group"].dropna().unique().tolist()
st.markdown("### Project Location")

country = st.text_input(
    "Country",
    value="Kenya",
    disabled=True
)

sector_group = st.selectbox(
    "Sector Group",
    sectors,
    help="Select the project sector from available categories"
)

st.markdown("**Sector Focus (%)**: How much of the project is in the selected sector")

sector_percent = st.slider("", 0, 100, 80)

st.markdown("**Country Focus (%)**: How much of the project is in the selected country")

country_percent = st.slider("", 0, 100, 90)

col1, col2 = st.columns(2)

with col1:
    start_year = st.number_input("Start Year", value=2020)

with col2:
    start_month = st.selectbox("Start Month", list(range(1, 13)))

if st.button("Predict"):

    input_df = pd.DataFrame([{
        'text': text,
        'reporting': reporting,
        'sector_group': sector_group,
        'start_year': start_year,
        'start_month': start_month,
        'sector_percent': sector_percent,
        'country_percent': country_percent
    }])

    # Predictions (arrays)
    dur_pred = duration_model.predict(input_df)
    eff_pred = eff_model.predict(input_df)

    # Convert from log scale
    dur_pred = np.exp(dur_pred)[0]   # <-- extract scalar
    eff_pred = np.exp(eff_pred)[0]   # <-- extract scalar

    # Convert duration
    months = dur_pred / 30
    years = dur_pred / 365

    st.subheader("Project Duration Estimate")
    st.write(
        f"Approximately {dur_pred:.0f} days "
        f"(~ {months:.1f} months or {years:.1f} years)"
    )

    # Efficiency (cap at 100%)
    efficiency_percent = min(eff_pred, 100)

    st.subheader("Project Efficiency")
    st.write(f"Estimated efficiency: {efficiency_percent:.1f}%")

    if efficiency_percent > 80:
        st.success("This project is expected to run very efficiently.")
    elif efficiency_percent > 50:
        st.info("This project has moderate efficiency.")
    else:
        st.warning("This project may face efficiency challenges.")

    with st.expander("What do these results mean?"):
        st.write("""
        - Duration: Estimated time to complete the project
        - Efficiency: How well resources are utilized
        """)

    # Debug / raw values
    st.success(f"Predicted Duration: {dur_pred:.3f}")
    st.success(f"Predicted Efficiency: {eff_pred:.3f}")