import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📊 Smart Portfolio Analyzer")

tickers = st.text_input("Enter Assets (comma-separated)", "AAPL, BTC-USD, ETH-USD")

if st.button("Analyze Portfolio"):
    tickers_list = [t.strip() for t in tickers.split(",")]

    data = yf.download(tickers_list, period="1y")["Close"]

    if data.empty:
        st.error("Invalid tickers")
    else:
        returns = data.pct_change().dropna()

        # Portfolio metrics
        mean_returns = returns.mean() * 252
        volatility = returns.std() * np.sqrt(252)
        sharpe = mean_returns / volatility

        st.subheader("Portfolio Metrics")

        df_metrics = pd.DataFrame({
            "Return": mean_returns,
            "Volatility": volatility,
            "Sharpe Ratio": sharpe
        })

        st.dataframe(df_metrics)

        # Correlation heatmap
        st.subheader("Correlation Matrix")
        fig, ax = plt.subplots()
        sns.heatmap(returns.corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

        # Insights
        st.subheader("Insights")

        best_asset = mean_returns.idxmax()
        risky_asset = volatility.idxmax()

        st.write(f"🏆 Best Performing Asset: {best_asset}")
        st.write(f"⚠️ Most Risky Asset: {risky_asset}")