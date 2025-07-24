import streamlit as st
import pandas as pd
from data_preprocessing import load_and_clean_data, prepare_prophet_df
from demand_forecasting import forecast_demand, plot_forecast
from heatmap_plot import get_location_heatmap_data, plot_demand_heatmap

st.set_page_config(page_title="Ride Demand Forecasting", layout="wide")
st.title("🚗 Ride Demand & Surge Price Forecasting")

# Sidebar Upload
st.sidebar.header("📁 Upload Ride Data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    df = load_and_clean_data("rides.csv")
else:
    st.sidebar.info("Loading sample dataset...")
    df = load_and_clean_data("rides.csv")

# ⏳ Time Filter UI
st.sidebar.subheader("⏱ Filter by Time")
start_date = st.sidebar.date_input("Start date", df['datetime'].min().date())
end_date = st.sidebar.date_input("End date", df['datetime'].max().date())
hour_range = st.sidebar.slider("Select Hour Range", 0, 23, (6, 22))

# Apply filters
df = df[
    (df['datetime'].dt.date >= start_date) &
    (df['datetime'].dt.date <= end_date) &
    (df['hour'] >= hour_range[0]) & (df['hour'] <= hour_range[1])
]

# Check if data available
if df.empty:
    st.warning("No data found for selected filters. Try a wider range.")
    st.stop()

# 📈 Demand Forecast
st.header("📈 Ride Demand Forecasting")
df_prophet = prepare_prophet_df(df)
model, forecast = forecast_demand(df_prophet, periods=48)

with st.expander("🔍 View Forecast Plot"):
    plot_forecast(model, forecast)


# 🌍 Heatmap (only if location data is present)
if 'latitude' in df.columns and 'longitude' in df.columns:
    st.header("🌍 Ride Demand Hotspots")
    loc_heat = get_location_heatmap_data(df)
    plot_demand_heatmap(loc_heat)
else:
    st.info("📍 No location data found. Skipping heatmap generation.")

# 🚖 Driver Time Slot Recommender
st.header("🧠 Recommended Time Slots for Drivers")

# Get top 5 hours with the highest ride count
top_slots = df.groupby('hour').size().sort_values(ascending=False).head(5)
st.markdown("📌 **Best Time Slots to Drive (based on demand):**")
for hour, count in top_slots.items():
    st.markdown(f"- ⏰ {hour}:00 - {hour+1}:00 → 🚘 Approx. {count} rides")
