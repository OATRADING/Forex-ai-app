import streamlit as st
import yfinance as yf
import pandas as pd
import ta

# إعداد الصفحة
st.set_page_config(page_title="توصيات الفوركس", layout="centered")

st.title("📈 توصيات الفوركس باستخدام الذكاء الاصطناعي")

# اختيار الزوج
pair = st.selectbox("اختر زوج العملات:", ["EURUSD=X", "XAUUSD=X"])

# تحميل البيانات من Yahoo Finance
data = yf.download(pair, period="6mo", interval="1d")

# حساب مؤشر RSI
data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()

# السعر الحالي
latest_price = data['Close'].iloc[-1]
st.metric("💰 السعر الحالي", f"{latest_price:.2f}")

# مؤشر RSI الحالي
latest_rsi = data['RSI'].iloc[-1]
st.metric("📊 مؤشر RSI", f"{latest_rsi:.2f}")

# التوصية بناءً على RSI
st.subheader("📌 التوصية")

if latest_rsi > 70:
    st.warning("⚠️ لا تدخل السوق (العملة في منطقة شراء مفرط)")
elif latest_rsi < 30:
    st.success("✅ فرصة شراء قوية")
else:
    st.info("ℹ️ ترقب، لا توجد فرصة واضحة الآن")

# عرض الشارتات
st.subheader("📉 شارت السعر")
st.line_chart(data['Close'])

st.subheader("📊 شارت RSI")
st.line_chart(data['RSI'])
