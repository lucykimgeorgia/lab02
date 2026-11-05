# This creates the page for displaying data visualizations.

import json
import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Build file paths from this file's location, so the app finds the data files
# whether it runs locally or on Streamlit Cloud.
LAB_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(LAB_FOLDER, "data.csv")
JSON_PATH = os.path.join(LAB_FOLDER, "data.json")

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Temperature Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---
with open(JSON_PATH) as f:
    data = json.load(f)

chart_title = data["chart_title"]
cities = [key for key in data if key != "chart_title"]  

# Visualization 1: STATIC (simple bar chart)
st.subheader(chart_title)

averages = {
    city: sum(item["value"] for item in data[city]) / len(data[city])
    for city in cities
}
avg_series = pd.Series(averages, name="Average Temperature (°F)")

st.bar_chart(avg_series, x_label="City", y_label="Average Temperature (°F)")

# Visualization 2: DYNAMIC + ADVANCED (Plotly line chart)
st.subheader("Monthly Temperature Trend (Dynamic)")

if "selected_city" not in st.session_state:
    st.session_state.selected_city = cities[0]

st.selectbox("Choose a city:", cities, key="selected_city")

city = st.session_state.selected_city
city_data = data[city]

fig = px.line(
    x=[item["label"] for item in city_data],
    y=[item["value"] for item in city_data],
    markers=True,
    title=f"Monthly Temperature in {city}",
    labels={"x": "Month", "y": "Temperature (°F)"},
)
st.plotly_chart(fig)


# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
st.divider()
st.header("Ideal Temperature Survey Results")

# Load the CSV data
if os.path.exists(CSV_PATH) and os.path.getsize(CSV_PATH) > 0:
    survey_df = pd.read_csv(CSV_PATH)
else:
    survey_df = pd.DataFrame(columns=["Category", "Value"])

survey_df["Value"] = pd.to_numeric(survey_df["Value"], errors="coerce")
survey_df = survey_df.dropna()

if survey_df.empty:
    st.info("No survey responses yet. Add some on the Survey page!")
else:
    
    st.subheader("Responses by City (Static)")

    counts = survey_df["Category"].value_counts().reset_index()
    counts.columns = ["City", "Responses"]

    pie = px.pie(
        counts,
        names="City",
        values="Responses",
        title="Number of Survey Responses by City",
    )
    st.plotly_chart(pie)

    
    st.subheader("Average Ideal Temperature by City (Dynamic)")

    if "min_temp" not in st.session_state:
        st.session_state.min_temp = 0.0

    st.slider(
        "Only include people whose ideal temperature is at least (°F):",
        min_value=0.0, max_value=110.0, step=5.0,
        key="min_temp",
    )

    filtered = survey_df[survey_df["Value"] >= st.session_state.min_temp]

    if filtered.empty:
        st.warning("No responses match this filter. Try a lower number.")
    else:
        avg_temp = filtered.groupby("Category")["Value"].mean()
        st.bar_chart(avg_temp, x_label="City", y_label="Average Ideal Temperature (°F)")

        # EXTRA CREDIT: mean and median that update with the slider
        current_mean = filtered["Value"].mean()
        current_median = filtered["Value"].median()

        if "prev_mean" not in st.session_state:
            st.session_state.prev_mean = current_mean
            st.session_state.prev_median = current_median

        col1, col2 = st.columns(2)
        col1.metric("Mean Ideal Temp", f"{current_mean:.1f} °F",
                    delta=f"{current_mean - st.session_state.prev_mean:.1f}")
        col2.metric("Median Ideal Temp", f"{current_median:.1f} °F",
                    delta=f"{current_median - st.session_state.prev_median:.1f}")

        st.session_state.prev_mean = current_mean
        st.session_state.prev_median = current_median
