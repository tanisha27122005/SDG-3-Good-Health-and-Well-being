
import streamlit as st
import pandas as pd
import numpy as np
import joblib

from pathlib import Path
from database import db_session

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Wellness Pattern Explorer",
    page_icon="🔬",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "wellness_model.joblib"

st.title("🔬 Personal Wellness Pattern Explorer")
st.caption("SDG 3 — Good Health and Well-being")

# --------------------------------------------------
# 2. LOGIN VALIDATION
# --------------------------------------------------
user = st.session_state.get("user")

if not isinstance(user, dict):
    st.warning("Please log in through the main application.")
    st.stop()

user_id = user.get("id")

if user_id is None:
    st.error("User ID is missing. Please log in again.")
    st.stop()

# --------------------------------------------------
# 3. LOAD ONLY THE LOGGED-IN USER'S CHECK-INS
# --------------------------------------------------
@st.cache_data(ttl=10)
def load_user_checkins(uid):
    with db_session() as conn:
        schema = pd.read_sql_query(
            "PRAGMA table_info(checkins)", conn
        )

        available_columns = schema["name"].tolist()

        if "user_id" not in available_columns:
            return pd.DataFrame(), False

        data = pd.read_sql_query(
            """
            SELECT *
            FROM checkins
            WHERE user_id = ?
            ORDER BY created_at ASC
            """,
            conn,
            params=(uid,)
        )

    return data, True


try:
    df, user_scoped = load_user_checkins(user_id)
except Exception as exc:
    st.error("Could not load check-in records.")
    st.exception(exc)
    st.stop()

if not user_scoped:
    st.error(
        "The checkins table has no user_id column. "
        "Update the database schema before using this page. "
        "Records are not displayed without user filtering."
    )
    st.stop()

if df.empty:
    st.info(
        "No check-ins found for your account. "
        "Add a record using Daily Check-in first."
    )

    if st.button(
        "🔄 Refresh Data",
        key="wpe_empty_refresh"
    ):
        load_user_checkins.clear()
        st.rerun()

    st.stop()

# --------------------------------------------------
# 4. NORMALIZE AVAILABLE COLUMN NAMES
# --------------------------------------------------
column_map = {
    "sleep_hours": "sleep",
    "support": "social"
}

for source, target in column_map.items():
    if source in df.columns and target not in df.columns:
        df[target] = df[source]

for column in ["mood", "stress", "sleep", "energy", "social"]:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

st.success(
    f"Loaded {len(df)} check-in record(s) for your account."
)

# --------------------------------------------------
# 5. PERSONAL PATTERN DASHBOARD
# --------------------------------------------------
st.header("1. Your Personal Patterns")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Check-ins", len(df))

for container, column, label, suffix in [
    (c2, "mood", "Average Mood", ""),
    (c3, "stress", "Average Stress", ""),
    (c4, "sleep", "Average Sleep", " hrs")
]:
    if column in df.columns:
        values = df[column].dropna()
    else:
        values = pd.Series(dtype=float)

    if not values.empty:
        container.metric(
            label,
            f"{values.mean():.1f}{suffix}"
        )
    else:
        container.metric(label, "N/A")

# --------------------------------------------------
# 6. CHECK-IN HISTORY
# --------------------------------------------------
st.subheader("📈 Check-in History")

trend_columns = [
    col for col in ["mood", "stress", "sleep", "energy"]
    if col in df.columns and df[col].notna().any()
]

if trend_columns:
    chart_df = df[trend_columns].copy()

    if "created_at" in df.columns:
        dates = pd.to_datetime(
            df["created_at"], errors="coerce"
        )
        chart_df.index = dates
        chart_df = chart_df.loc[
            ~chart_df.index.isna()
        ].sort_index()

    if not chart_df.empty:
        st.line_chart(chart_df)
    else:
        st.info("Valid timestamps are not available.")
else:
    st.info("No numeric trend data is available.")

# --------------------------------------------------
# 7. SLEEP AND STRESS COMPARISON
# --------------------------------------------------
st.header("2. Sleep and Stress Comparison")

required_columns = {"sleep", "stress", "mood"}

if required_columns.issubset(df.columns):
    comparison = df[
        ["sleep", "stress", "mood"]
    ].dropna().copy()

    if len(comparison) >= 4:
        comparison["Sleep Group"] = np.where(
            comparison["sleep"] >= 7,
            "7+ hours",
            "Under 7 hours"
        )

        summary = comparison.groupby(
            "Sleep Group", observed=True
        ).agg(
            Checkins=("sleep", "size"),
            Average_Stress=("stress", "mean"),
            Average_Mood=("mood", "mean")
        ).round(2)

        st.write(
            "Compare recorded check-ins across sleep groups. "
            "This comparison shows association, not causation."
        )
        st.dataframe(
            summary,
            use_container_width=True
        )
    else:
        st.info(
            "At least four complete mood, stress and sleep "
            "records are needed for this comparison."
        )
else:
    st.info(
        "Numeric mood, stress and sleep columns are required."
    )

# --------------------------------------------------
# 8. WHAT-IF WELLNESS SIMULATOR
# --------------------------------------------------
st.header("3. 🧪 What-If Wellness Simulator")

st.write(
    "Change hypothetical values and run the trained "
    "educational machine-learning model."
)

if not MODEL_PATH.exists():
    st.error(f"Model file not found: {MODEL_PATH}")
    st.code(
        r"..\venv312\Scripts\python.exe train_model.py",
        language="powershell"
    )
    st.stop()

try:
    model = joblib.load(MODEL_PATH)
except Exception as exc:
    st.error("Could not load the trained model.")
    st.exception(exc)
    st.stop()


def recent_average(column, fallback):
    if column in df.columns:
        values = df[column].dropna()

        if not values.empty:
            return float(values.tail(10).mean())

    return fallback


col1, col2 = st.columns(2)

with col1:
    sleep_input = st.slider(
        "Hypothetical sleep (hours)",
        min_value=3.0,
        max_value=12.0,
        value=float(np.clip(
            recent_average("sleep", 7.0), 3.0, 12.0
        )),
        step=0.5,
        key="wpe_sleep"
    )

    stress_input = st.slider(
        "Hypothetical stress (1–10)",
        min_value=1,
        max_value=10,
        value=int(np.clip(
            round(recent_average("stress", 5)), 1, 10
        )),
        key="wpe_stress"
    )

with col2:
    energy_input = st.slider(
        "Hypothetical energy (1–10)",
        min_value=1,
        max_value=10,
        value=int(np.clip(
            round(recent_average("energy", 5)), 1, 10
        )),
        key="wpe_energy"
    )

    social_input = st.slider(
        "Hypothetical social connection (1–10)",
        min_value=1,
        max_value=10,
        value=int(np.clip(
            round(recent_average("social", 5)), 1, 10
        )),
        key="wpe_social"
    )

# IMPORTANT: This is the only simulation button in this file.
if st.button(
    "🧪 Run What-If Simulation",
    use_container_width=True,
    key="wpe_run_simulation"
):
    try:
        input_data = pd.DataFrame(
            [[
                sleep_input,
                stress_input,
                energy_input,
                social_input
            ]],
            columns=[
                "sleep",
                "stress",
                "energy",
                "social"
            ]
        )

        prediction = model.predict(input_data)[0]

        st.subheader("Model Output")

        labels = {
            0: "Category 0 — Lower educational score band",
            1: "Category 1 — Middle educational score band",
            2: "Category 2 — Higher educational score band"
        }

        st.success(
            labels.get(
                int(prediction),
                f"Model category: {prediction}"
            )
        )

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(
                input_data
            )[0]

            probability_df = pd.DataFrame({
                "Category": [
                    str(category)
                    for category in model.classes_
                ],
                "Estimated Probability (%)": [
                    round(float(probability) * 100, 2)
                    for probability in probabilities
                ]
            })

            st.subheader("Model Probability Estimates")

            st.bar_chart(
                probability_df.set_index("Category")
            )

            st.dataframe(
                probability_df,
                use_container_width=True,
                hide_index=True
            )

    except Exception as exc:
        st.error("Prediction failed.")
        st.exception(exc)

st.divider()

st.caption(
    "Educational demonstration using synthetic training data. "
    "Model categories and probabilities are not clinical "
    "assessments, diagnoses or treatment recommendations."
)

# Unique key for the page's single refresh button.
if st.button(
    "🔄 Refresh Explorer Data",
    key="wpe_refresh_data"
):
    load_user_checkins.clear()
    st.rerun()
