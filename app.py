import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

# دالة لحساب RSI يدويًا بدون مكتبة ta
def calculate_rsi(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# تحميل البيانات من Yahoo Finance
@st.cache_data
def load_data(symbol="EURUSD=X", start="2023-01-01", end="2025-06-30"):
    data = yf.download(symbol, start=start, end=end, interval="1d")
    data['RSI'] = calculate_rsi(data['Close'])
    return data.dropna()

# إعداد صفحة Streamlit
st.set_page_config(layout="centered", page_title="📈 توصيات الفوركس بالذكاء الاصطناعي")
st.title("📉 توصيات الفوركس باستخدام الذكاء الاصطناعي")

# تحميل البيانات وتحليلها
data = load_data()
latest_rsi = data['RSI'].iloc[-1]

st.markdown(f"### 🔢 قيمة RSI الحالية: `{round(latest_rsi, 2)}`")

# توليد التوصية بناءً على RSI
if latest_rsi < 30:
    st.success("✅ التوصية: دخول السوق (العملة في منطقة بيع مفرط).")
elif latest_rsi > 70:
    st.error("⛔ التوصية: لا تدخل السوق (العملة في منطقة شراء مفرط).")
else:
    st.info("🔍 التوصية: ترقّب — السوق غير واضح حالياً.")

# عرض الشارت
st.subheader("📊 سعر الإغلاق")
st.line_chart(data['Close'], height=250, use_container_width=True)

st.subheader("📉 مؤشر RSI")
st.line_chart(data['RSI'], height=150, use_container_width=True)
