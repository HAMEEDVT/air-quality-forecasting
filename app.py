# app.py
import streamlit as st
import pandas as pd
import requests
from prophet import Prophet
import plotly.graph_objs as go

# Page config
st.set_page_config(page_title="AQI Forecast", layout="wide")
st.title("Air Quality Forecasting for Indian Cities")
st.markdown("**PM2.5 → AQI Forecast** using **Prophet** | Data: OpenAQ v2")

# City mapping with coordinates (latitude, longitude)
city_coords = {
    "Delhi": (28.61, 77.20),
    "Mumbai": (19.07, 72.87),
    "Chennai": (13.08, 80.27),
    "Bangalore": (12.97, 77.59)
}

# Cache data fetch
@st.cache_data(ttl=3600)
def fetch_aq_data(city, start_date="2020-01-01"):
    """Fetch hourly PM2.5 from the Open-Meteo Air Quality API and return daily means.

    This provider is free and requires no API key. It returns modelled PM2.5 estimates.
    """
    lat, lon = city_coords[city]
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    end_date = pd.Timestamp.now(tz="UTC").date().isoformat()
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "pm2_5"
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code != 200:
            st.error(f"Air-quality API error {response.status_code}: {response.text[:200]}")
            st.caption(f"URL: {response.url}")
            return None

        payload = response.json()
        hourly = payload.get("hourly", {})
        times = hourly.get("time", [])
        pm25 = hourly.get("pm2_5", [])

        if not times or not pm25:
            st.warning(f"No PM2.5 hourly data returned for **{city}** from Open-Meteo.")
            return None

        df = pd.DataFrame({"date": pd.to_datetime(times), "pm25": pm25})
        df = df.set_index("date").sort_index()
        daily = df.resample("D").mean().dropna()

        if len(daily) < 30:
            st.warning(f"Only {len(daily)} days of data. Need ≥30 for forecast.")
            return None

        return daily

    except requests.exceptions.RequestException as e:
        st.error("Network error when contacting Open-Meteo. Check your internet connection.")
        st.caption(str(e))
        return None
    except Exception as e:
        st.error(f"Failed to fetch air-quality data: {e}")
        return None

# PM2.5 → AQI (Indian Standards)
def pm25_to_aqi(pm25):
    if pm25 <= 30:   return (50/30) * pm25
    if pm25 <= 60:   return 50 + (50/30)*(pm25-30)
    if pm25 <= 90:   return 100 + (50/30)*(pm25-60)
    if pm25 <= 120:  return 150 + (50/30)*(pm25-90)
    if pm25 <= 250:  return 200 + (100/130)*(pm25-120)
    return 300 + (100/130)*(pm25-250)

# Sidebar
st.sidebar.header("Settings")
selected_city = st.sidebar.selectbox("Select City", options=list(city_coords.keys()))
forecast_days = st.sidebar.slider("Forecast Days", 7, 60, 30)

# Fetch data
with st.spinner(f"Fetching PM2.5 data for **{selected_city}**..."):
    df = fetch_aq_data(selected_city)

if df is not None and len(df) >= 30:
    df["aqi"] = df["pm25"].apply(pm25_to_aqi)

    # Prophet model
    df_prophet = df["pm25"].reset_index()
    df_prophet.columns = ["ds", "y"]

    with st.spinner("Training Prophet model..."):
        m = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            seasonality_mode="multiplicative"
        )
        m.fit(df_prophet)

    future = m.make_future_dataframe(periods=forecast_days)
    forecast = m.predict(future)
    forecast["aqi"] = forecast["yhat"].apply(pm25_to_aqi)
    forecast["aqi_lower"] = forecast["yhat_lower"].apply(pm25_to_aqi)
    forecast["aqi_upper"] = forecast["yhat_upper"].apply(pm25_to_aqi)

    # Plot
    fig = go.Figure()

    # Historical AQI (rename index column to ds for consistency with forecast)
    hist = df["aqi"].reset_index().rename(columns={"date": "ds"})
    fig.add_trace(go.Scatter(x=hist["ds"], y=hist["aqi"],
                             mode="lines", name="Historical AQI",
                             line=dict(color="blue")))

    # Forecast AQI
    fore = forecast[["ds", "aqi", "aqi_lower", "aqi_upper"]].tail(forecast_days)
    fig.add_trace(go.Scatter(x=fore["ds"], y=fore["aqi"],
                             mode="lines", name="Forecast AQI",
                             line=dict(color="red", dash="dash")))

    # Uncertainty band
    fig.add_trace(go.Scatter(
        x=fore["ds"].tolist() + fore["ds"][::-1].tolist(),
        y=fore["aqi_upper"].tolist() + fore["aqi_lower"][::-1].tolist(),
        fill="toself", fillcolor="rgba(255,0,0,0.2)",
        line=dict(color="rgba(255,255,255,0)"), name="Uncertainty"
    ))

    fig.update_layout(
        title=f"AQI Forecast – {selected_city} (Next {forecast_days} days)",
        xaxis_title="Date", yaxis_title="AQI",
        hovermode="x unified", height=600
    )
    st.plotly_chart(fig, width='stretch')

    # Current stats
    latest_pm25 = df["pm25"].iloc[-1]
    latest_aqi = pm25_to_aqi(latest_pm25)

    col1, col2 = st.columns(2)
    col1.metric("Latest PM2.5", f"{latest_pm25:.1f} µg/m³")
    col2.metric("Current AQI", f"{latest_aqi:.0f}")

    # AQI Category
    categories = [
        (50, "Good", "Green"),
        (100, "Moderate", "Yellow"),
        (150, "Unhealthy for Sensitive", "Orange"),
        (200, "Unhealthy", "Red"),
        (300, "Very Unhealthy", "Purple"),
        (9999, "Hazardous", "Black")
    ]
    for lim, label, color in categories:
        if latest_aqi <= lim:
            st.markdown(f"### {color} **{label}**")
            break

    # Forecast Table
    st.subheader("Forecast Table")
    tbl = forecast[["ds", "yhat", "aqi"]].tail(forecast_days).copy()
    tbl["Date"] = tbl["ds"].dt.strftime("%Y-%m-%d")
    tbl["PM2.5"] = tbl["yhat"].round(1)
    tbl["AQI"] = tbl["aqi"].round(0).astype(int)
    st.dataframe(tbl[["Date", "PM2.5", "AQI"]], width='stretch')

else:
    st.error("Not enough data. Try **Delhi** (most reliable) or check internet.")

# Footer
st.caption("Data: [OpenAQ v2](https://docs.openaq.org) | Model: Prophet | Made in VS Code")