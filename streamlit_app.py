import streamlit as st
import yfinance as yf

# ---------------------- CONFIGURATION ---------------------- #
st.set_page_config(page_title="Daily Stock Viewer", layout="wide")

# ---------------------- APP TITLE -------------------------- #
st.title("📈 Daily Stocks Viewer")
st.markdown("Get real-time and historical stock data with charts and key metrics.")

# ---------------------- SIDEBAR ---------------------------- #
st.sidebar.header("📌 Options")

# Ticker options
stock_options = {
    "Apple (AAPL)": "AAPL",
    "Tesla (TSLA)": "TSLA",
    "Google (GOOGL)": "GOOGL",
    "Amazon (AMZN)": "AMZN",
    "Microsoft (MSFT)": "MSFT"
}

selected_stock = st.sidebar.selectbox("Select Stock", options=list(stock_options.keys()))
ticker_symbol = stock_options[selected_stock]

# Date range options
date_range = st.sidebar.selectbox(
    "Select Date Range",
    options=["1d", "5d", "1mo", "3mo", "6mo", "1y"],
    index=0
)

# Set interval based on range
interval_map = {
    "1d": "1m",
    "5d": "5m",
    "1mo": "30m",
    "3mo": "1d",
    "6mo": "1d",
    "1y": "1d"
}
selected_interval = interval_map[date_range]

# ---------------------- DATA FETCH -------------------------- #
stock_data = yf.download(ticker_symbol, period=date_range, interval=selected_interval)

if not stock_data.empty:
    # Latest data
    latest = stock_data.iloc[-1]
    open_price = float(latest['Open'])
    close_price = float(latest['Close'])
    high_price = float(latest['High'])
    low_price = float(latest['Low'])
    volume = int(latest['Volume'])

    # Price change calculations
    price_change = close_price - open_price
    percentage_change = (price_change / open_price) * 100

    # ------------------ METRICS DISPLAY ------------------- #
    st.subheader(f"📊 {selected_stock} Overview")
    st.metric(
        label="🔁 Change",
        value=f"${price_change:.2f}",
        delta=f"{percentage_change:.2f}%",
        delta_color="normal" if price_change == 0 else ("inverse" if price_change < 0 else "off")
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"${close_price:.2f}")
    col2.metric("Open", f"${open_price:.2f}")
    col3.metric("High", f"${high_price:.2f}")

    col4, col5 = st.columns(2)
    col4.metric("Low", f"${low_price:.2f}")
    col5.metric("Volume", f"{volume:,}")

    # ------------------ CHART DISPLAY --------------------- #
    st.write("### 📈 Price Chart")
    st.line_chart(stock_data['Close'], use_container_width=True)

else:
    st.warning("⚠️ No data available for the selected period. The market may be closed.")

# ---------------------- FOOTER ---------------------------- #
st.subheader(f"🧾 Showing Data for: {selected_stock} ({ticker_symbol})")

st.markdown("""---""")
st.markdown(
    """
    <div style="text-align: center; font-size: 14px; color: gray;">
        Built with ❤️ using <b>Streamlit</b><br>
        Created by <b>Barthez Moses</b><br>
        📧 Contact: <a href="mailto:barthezmoses18@gmail.com">barthezmoses18@gmail.com</a> |
        💼 GitHub: <a href="https://github.com/skipperForREAL" target="_blank">skipperForREAL</a>
    </div>
    """,
    unsafe_allow_html=True
)
