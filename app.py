from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from modules.assessment import (
    HealthAssessment,
    calculate_readiness_score,
    get_health_status,
    get_recommendation,
    missing_indicators,
    validate_assessment,
)
from modules.baseline import calculate_personal_baseline
from modules.insights import generate_insights
from modules.persistence import load_assessments, save_assessment


APP_ROOT = Path(__file__).parent
ASSESSMENTS_PATH = APP_ROOT / "data" / "assessments.csv"

st.set_page_config(
    page_title="AstroVital — Mission Health",
    page_icon="🛰️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background: #070d18;
        color: #e8f1ff;
        font-family: Inter, Roboto, Arial, sans-serif;
    }
    h1, h2, h3, p, label, [data-testid="stMarkdownContainer"] {
        color: #e8f1ff !important;
    }
    h1, h2, h3 {
        letter-spacing: 0.02em;
    }
    h1 {
        color: #66e3ff !important;
    }
    [data-testid="stSidebar"] {
        background: #0c1626;
        border-right: 1px solid #1f3a5b;
    }
    [data-testid="stMetric"] {
        background: #0e1b2d;
        border: 1px solid #214365;
        border-radius: 10px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.22);
        padding: 1rem;
    }
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
        color: #e8f1ff;
    }
    [data-baseweb="slider"] > div > div > div,
    [data-baseweb="slider"] [role="slider"] {
        background: #27c7e8;
        border-color: #27c7e8;
    }
    [data-testid="stForm"] {
        background: #0e1b2d;
        border: 1px solid #214365;
        border-radius: 10px;
        padding: 1rem;
    }
    [data-testid="stAlert"] {
        border-radius: 10px;
    }
    .insight-card {
        background: #0e1b2d;
        border: 1px solid #214365;
        border-left: 4px solid #27c7e8;
        border-radius: 8px;
        margin: 0.5rem 0;
        padding: 0.8rem 1rem;
    }
    .section-label {
        color: #7edff5;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def generate_simulated_history() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=7)
    return pd.DataFrame(
        {
            "Fecha": dates,
            "Heart_Rate": rng.integers(60, 121, size=7),
            "Sleep_Hours": np.round(rng.uniform(4, 9, size=7), 1),
            "source": "simulated",
        }
    )


def display_value(value: float | None, suffix: str = "") -> str:
    if value is None or pd.isna(value):
        return "Not recorded"
    return f"{value:.1f}{suffix}"


def plot_metric(
    history: pd.DataFrame, field: str, title: str, color: str, y_label: str
) -> None:
    if history.empty or field not in history or history[field].notna().sum() == 0:
        st.caption(f"No user-entered history available for {title.lower()}.")
        return
    chart = history[["recorded_at", field]].dropna()
    chart = chart.rename(columns={"recorded_at": "Date", field: y_label})
    figure = px.line(chart, x="Date", y=y_label, markers=True, title=title)
    figure.update_traces(line_color=color)
    figure.update_layout(
        plot_bgcolor="#0e1b2d",
        paper_bgcolor="#0e1b2d",
        font_color="#e8f1ff",
        margin=dict(l=20, r=20, t=50, b=20),
    )
    figure.update_xaxes(gridcolor="#214365")
    figure.update_yaxes(gridcolor="#214365")
    st.plotly_chart(figure, use_container_width=True)


try:
    user_history = load_assessments(ASSESSMENTS_PATH)
except RuntimeError as error:
    st.error(str(error))
    st.stop()

if "simulated_history" not in st.session_state:
    st.session_state.simulated_history = generate_simulated_history()
simulated_history = st.session_state.simulated_history

st.sidebar.header("Health Assessment")
st.sidebar.caption("User-entered values are saved separately from simulated mission data.")

with st.sidebar.form("health_assessment_form"):
    heart_rate = st.slider("Heart Rate (BPM)", 30, 220, 75)
    sleep_hours = st.slider("Sleep (hours)", 0.0, 24.0, 7.5, 0.5)
    stress_level = st.slider("Stress Level", 1, 10, 3)
    physical_activity = st.slider("Physical Activity (min)", 0, 240, 30)
    mood = st.slider("Mood", 1, 10, 7)

    st.caption("Optional indicators")
    systolic_bp = st.number_input(
        "Systolic BP (mmHg)", min_value=60, max_value=250, value=None
    )
    diastolic_bp = st.number_input(
        "Diastolic BP (mmHg)", min_value=30, max_value=150, value=None
    )
    body_temperature = st.number_input(
        "Body Temperature (°C)", min_value=30.0, max_value=45.0, value=None, step=0.1
    )
    blood_glucose = st.number_input(
        "Blood Glucose (mg/dL)", min_value=40.0, max_value=400.0, value=None, step=1.0
    )
    submitted = st.form_submit_button("Save assessment")

current_assessment = HealthAssessment(
    heart_rate=heart_rate,
    systolic_bp=systolic_bp,
    diastolic_bp=diastolic_bp,
    body_temperature=body_temperature,
    blood_glucose=blood_glucose,
    sleep_hours=sleep_hours,
    stress_level=stress_level,
    physical_activity=physical_activity,
    mood=mood,
)

if submitted:
    errors = validate_assessment(current_assessment)
    if errors:
        for error in errors:
            st.sidebar.error(error)
    else:
        try:
            save_assessment(ASSESSMENTS_PATH, current_assessment)
        except RuntimeError as error:
            st.sidebar.error(str(error))
        else:
            st.session_state.assessment_saved = True
            st.rerun()

if st.session_state.pop("assessment_saved", False):
    st.sidebar.success("Assessment saved to user history.")

if st.sidebar.button("Simulate next mission day"):
    previous_date = simulated_history["Fecha"].max()
    rng = np.random.default_rng()
    next_row = pd.DataFrame(
        {
            "Fecha": [previous_date + pd.Timedelta(days=1)],
            "Heart_Rate": [rng.integers(60, 121)],
            "Sleep_Hours": [np.round(rng.uniform(4, 9), 1)],
            "source": ["simulated"],
        }
    )
    st.session_state.simulated_history = pd.concat(
        [simulated_history, next_row], ignore_index=True
    )
    st.rerun()

status = get_health_status(current_assessment)
readiness_score = calculate_readiness_score(current_assessment)
baseline = calculate_personal_baseline(user_history)
insights = generate_insights(user_history, current_assessment, baseline)

st.title("AstroVital")
st.caption("ASTRONAUT SELF-HEALTH MONITORING SYSTEM  •  MONITOR → ANALYZE → UNDERSTAND → ACT")

if readiness_score < 50:
    readiness_color, readiness_label = "#ff5577", "HIGH RISK"
elif readiness_score < 80:
    readiness_color, readiness_label = "#ffd166", "CAUTION"
else:
    readiness_color, readiness_label = "#42e8a4", "OPTIMAL"

_, readiness_column, _ = st.columns([1, 2, 1])
with readiness_column:
    st.markdown('<div class="section-label">Mission Readiness · Experimental</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="background:#0e1b2d;border:1px solid {readiness_color};
        border-radius:12px;box-shadow:0 0 24px {readiness_color}22;
        padding:1.4rem;text-align:center;">
          <div style="color:{readiness_color};font-size:4rem;font-weight:800;">
            {readiness_score}<span style="font-size:1.4rem;"> / 100</span>
          </div>
          <div style="color:{readiness_color};font-weight:700;letter-spacing:.12em;">
            {readiness_label}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Experimental decision-support signal; not medical clearance for EVA.")

status_color = {
    "🔴 HIGH RISK": "#ff5577",
    "🟡 CAUTION": "#ffd166",
    "🟢 OPTIMAL": "#42e8a4",
}[status]
st.markdown(
    f'<h2 style="color:{status_color}!important;">Overall Status: {status}</h2>',
    unsafe_allow_html=True,
)

st.markdown("### Human Health Map")
health_columns = st.columns(5)
health_cards = [
    ("Cardiovascular", display_value(current_assessment.heart_rate, " BPM")),
    (
        "Sleep & Circadian",
        display_value(current_assessment.sleep_hours, " h"),
    ),
    (
        "Metabolism",
        display_value(current_assessment.blood_glucose, " mg/dL"),
    ),
    ("Behavioral Wellbeing", display_value(current_assessment.mood, "/10")),
    (
        "Activity & Fitness",
        display_value(current_assessment.physical_activity, " min"),
    ),
]
for column, (label, value) in zip(health_columns, health_cards):
    column.metric(label, value)

st.markdown("### Current Assessment")
metric_columns = st.columns(5)
metric_columns[0].metric("Heart Rate", display_value(current_assessment.heart_rate, " BPM"))
metric_columns[1].metric("Blood Pressure", (
    f"{display_value(current_assessment.systolic_bp)}/"
    f"{display_value(current_assessment.diastolic_bp)} mmHg"
    if current_assessment.systolic_bp is not None
    and current_assessment.diastolic_bp is not None
    else "Not recorded"
))
metric_columns[2].metric("Temperature", display_value(current_assessment.body_temperature, " °C"))
metric_columns[3].metric("Stress", display_value(current_assessment.stress_level, "/10"))
metric_columns[4].metric("Mood", display_value(current_assessment.mood, "/10"))

st.markdown("### Action Guidance")
if status == "🔴 HIGH RISK":
    st.error(get_recommendation(status))
elif status == "🟡 CAUTION":
    st.warning(get_recommendation(status))
else:
    st.success(get_recommendation(status))

missing = missing_indicators(current_assessment)
if missing:
    st.info("Missing indicators: " + ", ".join(missing))

st.markdown("### Personal Baseline")
if baseline.reliable:
    st.success(
        f"Baseline available from {baseline.record_count} user-entered assessments."
    )
    baseline_table = pd.DataFrame(
        [{"Indicator": field.replace("_", " ").title(), "Personal mean": value}
         for field, value in baseline.values.items()]
    )
    st.dataframe(baseline_table, hide_index=True, use_container_width=True)
else:
    st.info(
        f"Baseline not reliable yet: {baseline.record_count} records available; "
        f"{baseline.minimum_records} are required."
    )

st.markdown("### Health Insights")
for insight in insights:
    st.markdown(
        f"""
        <div class="insight-card">
          <strong>{insight.severity} · {insight.indicator}</strong><br>
          <span>Value: {insight.value} · Reference: {insight.reference}</span><br>
          {insight.explanation}<br>
          <small>{insight.reason} Action: {insight.action}</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### User-entered Trends")
if user_history.empty:
    st.info("Save an assessment to begin building personal trends.")
else:
    trend_columns = st.columns(2)
    with trend_columns[0]:
        plot_metric(user_history, "heart_rate", "Heart Rate", "#36a3ff", "BPM")
    with trend_columns[1]:
        plot_metric(user_history, "sleep_hours", "Sleep Hours", "#b58cff", "Hours")

st.markdown("### Simulated Mission Data")
st.caption("This dataset is synthetic and separate from user-entered assessments.")
simulated_columns = st.columns(2)
with simulated_columns[0]:
    simulated_chart = px.line(
        simulated_history,
        x="Fecha",
        y="Heart_Rate",
        markers=True,
        title="Simulated Heart Rate",
    )
    simulated_chart.update_traces(line_color="#36a3ff")
    simulated_chart.update_layout(
        plot_bgcolor="#0e1b2d",
        paper_bgcolor="#0e1b2d",
        font_color="#e8f1ff",
        yaxis_title="BPM",
    )
    st.plotly_chart(simulated_chart, use_container_width=True)
with simulated_columns[1]:
    sleep_chart = px.line(
        simulated_history,
        x="Fecha",
        y="Sleep_Hours",
        markers=True,
        title="Simulated Sleep",
    )
    sleep_chart.update_traces(line_color="#b58cff")
    sleep_chart.update_layout(
        plot_bgcolor="#0e1b2d",
        paper_bgcolor="#0e1b2d",
        font_color="#e8f1ff",
        yaxis_title="Hours",
    )
    st.plotly_chart(sleep_chart, use_container_width=True)
