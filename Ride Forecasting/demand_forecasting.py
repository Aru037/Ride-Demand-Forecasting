from prophet import Prophet
import matplotlib.pyplot as plt

def forecast_demand(df_prepped, periods=24):
    model = Prophet()
    model.fit(df_prepped)

    future = model.make_future_dataframe(periods=periods, freq='H')
    forecast = model.predict(future)

    return model, forecast

def plot_forecast(model, forecast):
    fig = model.plot(forecast)
    plt.title("Hourly Ride Demand Forecast")
    plt.xlabel("Time")
    plt.ylabel("Number of Rides")
    plt.tight_layout()
    plt.show()
