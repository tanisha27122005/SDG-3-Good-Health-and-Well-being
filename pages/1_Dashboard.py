
import streamlit as st
import pandas as pd
from database import db_session

st.title("🧠 MindCare AI Dashboard")
st.caption("SDG 3 — Good Health and Well-being")


# ---------------- LOAD CHECK-IN DATA ----------------
@st.cache_data(ttl=10)
def load_checkins():
    with db_session() as conn:
        df = pd.read_sql_query(
            "SELECT * FROM checkins ORDER BY created_at DESC",
            conn
        )
    return df


# ---------------- NUMERIC CONVERSION ----------------
def numeric_series(df, column):
    """Convert numeric values safely; ignore text and missing values."""
    if column not in df.columns:
        return pd.Series(dtype="float64")

    return pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()


def average_value(df, column):
    values = numeric_series(df, column)

    if values.empty:
        return None

    return float(values.mean())


def show_metric(label, value, suffix=""):
    if value is None:
        st.metric(label, "N/A")
    else:
        st.metric(label, f"{value:.1f}{suffix}")


# ---------------- DASHBOARD ----------------
try:
    df = load_checkins()

    if df.empty:
        st.info("No wellness check-ins recorded yet.")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Check-ins", 0)
        col2.metric("Average Mood", "N/A")
        col3.metric("Average Stress", "N/A")
        col4.metric("Average Sleep", "N/A")

    else:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Check-ins", len(df))

        with col2:
            show_metric(
                "Average Mood (1–10)",
                average_value(df, "mood")
            )

        with col3:
            show_metric(
                "Average Stress (1–10)",
                average_value(df, "stress")
            )

        with col4:
            show_metric(
                "Average Sleep",
                average_value(df, "sleep_hours"),
                " hrs"
            )

        st.divider()
        st.subheader("📈 Wellness History")

        # Use a separate copy so original database values remain unchanged.
        chart_df = pd.DataFrame()

        for column in ["mood", "stress", "energy", "sleep_hours"]:
            if column in df.columns:
                values = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

                if values.notna().any():
                    chart_df[column] = values

        if not chart_df.empty:
            if "created_at" in df.columns:
                dates = pd.to_datetime(
                    df["created_at"],
                    errors="coerce"
                )
                chart_df.index = dates
                chart_df = chart_df[
                    ~chart_df.index.isna()
                ].sort_index()

            if not chart_df.empty:
                st.line_chart(chart_df)
            else:
                st.info("No valid dates available for the chart.")
        else:
            st.info(
                "No numeric wellness values are available for the chart yet."
            )

        st.divider()
        st.subheader("🗂️ Recent Check-ins")

        preferred_columns = [
            column for column in [
                "created_at",
                "mood",
                "stress",
                "sleep_hours",
                "energy",
                "support",
                "activity"
            ]
            if column in df.columns
        ]

        if preferred_columns:
            st.dataframe(
                df[preferred_columns].head(10),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.dataframe(
                df.head(10),
                use_container_width=True,
                hide_index=True
            )

except Exception as error:
    st.error("Unable to load the dashboard.")
    st.caption(
        "Check the database connection and the checkins table structure."
    )
    st.code(str(error))


# ---------------- REFRESH ----------------
if st.button("🔄 Refresh Dashboard"):
    load_checkins.clear()
    st.rerun()
