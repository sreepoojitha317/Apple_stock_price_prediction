import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Apple Stock Forecasting",
    page_icon="📈",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================

historical = pd.read_csv("apple_stock.csv")

future_forecast = pd.read_csv("future_forecast.csv")

# Date conversion
historical['Date'] = pd.to_datetime(historical['Date'])
future_forecast['Date'] = pd.to_datetime(future_forecast['Date'])

# Keep only required columns
historical = historical[['Date', 'Close']]

# ==================================================
# TITLE
# ==================================================

st.title("📈 Apple Stock Price Forecasting Dashboard")

st.markdown("""
This project forecasts Apple stock prices using:

- ARIMA
- Prophet
- XGBoost

After comparing all models, XGBoost was selected as the final forecasting model.
""")

st.markdown("---")

# ==================================================
# MODEL COMPARISON
# ==================================================

st.header("📊 Model Comparison")

comparison_df = pd.DataFrame({
    "Model": ["ARIMA", "Prophet", "XGBoost"],
    "RMSE": [33.30, 26.40, 3.50]
})

st.dataframe(
    comparison_df,
    use_container_width=True
)

best_model = comparison_df.loc[
    comparison_df['RMSE'].idxmin(),
    'Model'
]

st.success(
    f"🏆 Best Model: {best_model} (Lowest RMSE)"
)

st.markdown("---")

# ==================================================
# FORECAST TABLE
# ==================================================

st.header("📅 Next 30 Business Day Forecast")

st.dataframe(
    future_forecast,
    use_container_width=True
)

st.markdown("---")

# ==================================================
# FORECAST SUMMARY
# ==================================================

st.header("📌 Forecast Summary")

start_price = future_forecast['Forecast_Close'].iloc[0]
end_price = future_forecast['Forecast_Close'].iloc[-1]

change = end_price - start_price

growth = (
    change / start_price
) * 100

col1, col2, col3 = st.columns(3)

col1.metric(
    "Forecast Start",
    f"{start_price:.2f}"
)

col2.metric(
    "Forecast End",
    f"{end_price:.2f}"
)

col3.metric(
    "Expected Growth",
    f"{growth:.2f}%"
)

st.markdown("---")

# ==================================================
# INTERACTIVE FORECAST GRAPH
# ==================================================

st.header("📈 Historical vs Future Forecast")

# Show recent history only
historical_plot = historical.tail(60)

fig = go.Figure()

# Historical Line
fig.add_trace(
    go.Scatter(
        x=historical_plot['Date'],
        y=historical_plot['Close'],
        mode='lines',
        name='Historical Price',
        line=dict(
            color='royalblue',
            width=3
        ),
        hovertemplate=
        '<b>Date:</b> %{x}<br>' +
        '<b>Price:</b> %{y:.2f}<extra></extra>'
    )
)

# Forecast Line
fig.add_trace(
    go.Scatter(
        x=future_forecast['Date'],
        y=future_forecast['Forecast_Close'],
        mode='lines+markers',
        name='30-Day Forecast',
        line=dict(
            color='orange',
            width=5
        ),
        marker=dict(
            size=8
        ),
        hovertemplate=
        '<b>Date:</b> %{x}<br>' +
        '<b>Forecast Price:</b> %{y:.2f}<extra></extra>'
    )
)

fig.update_layout(
    title="Apple Stock Price Forecast",
    xaxis_title="Date",
    yaxis_title="Close Price",
    hovermode="x unified",
    template="plotly_white",
    height=650,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# ==================================================
# BUSINESS CONCLUSION
# ==================================================

st.header("💼 Business Conclusion")

st.info(
    """
• XGBoost achieved the best forecasting performance.

• It produced the lowest RMSE compared to ARIMA and Prophet.

• The forecast indicates a gradual upward trend in Apple stock prices over the next 30 business days.

• Based on model evaluation results, XGBoost was selected as the final forecasting model.
"""
)

st.markdown("---")

# ==================================================
# FOOTER
# ==================================================

st.caption(
    "Built using Python, XGBoost, Plotly and Streamlit"
)