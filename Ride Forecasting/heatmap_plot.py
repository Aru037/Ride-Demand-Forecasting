import  pandas as pd
import plotly.express as px

def get_location_heatmap_data(df, precision=3):
    df.columns = [col.lower() for col in df.columns]  # normalize names
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        return pd.DataFrame()  # return empty if no location data

    df['lat_bin'] = df['latitude'].round(precision)
    df['lon_bin'] = df['longitude'].round(precision)

    heat_df = df.groupby(['lat_bin', 'lon_bin']).size().reset_index(name='ride_count')
    return heat_df


def plot_demand_heatmap(df):
    if df.empty:
        return

    # Categorize ride counts
    def assign_color_group(count):
        if count < 30000:
            return "Low (<30k)"
        elif count < 40000:
            return "Medium (30k–40k)"
        elif count < 50000:
            return "High (40k–50k)"
        else:
            return "Very High (>50k)"

    df["demand_level"] = df["ride_count"].apply(assign_color_group)

    color_map = {
        "Low (<30k)": "yellow",
        "Medium (30k–40k)": "blue",
        "High (40k–50k)": "purple",
        "Very High (>50k)": "red"
    }

    fig = px.scatter_mapbox(
        df,
        lat="lat_bin",
        lon="lon_bin",
        size="ride_count",
        color="demand_level",
        color_discrete_map=color_map,
        hover_name="ride_count",
        zoom=10,
        height=500,
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r":0,"t":30,"l":0,"b":0},
        title="Ride Demand Hotspots"
    )

    import streamlit as st
    st.plotly_chart(fig, use_container_width=True)
