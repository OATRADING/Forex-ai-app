import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

# حساب RSI (مؤشر القوة النسبية)
def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# تحميل بيانات السوق
@st.cache_data
def load_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

# الواجهة
st.set_page_config(page_title="توصيات الفوركس باستخدام الذكاء الاصطناعي", layout="wide")
st.title("📉 توصيات الفوركس باستخدام الذكاء الاصطناعي")

# اختيارات المستخدم
symbol = st.text_input("أدخل رمز العملة (مثل EURUSD=X):", "EURUSD=X")
start_date = st.date_input("تاريخ البداية:", pd.to_datetime("2023-01-01"))
end_date = st.date_input("تاريخ النهاية:", pd.to_datetime("today"))

if st.button("ابدأ التحليل"):
    data = load_data(symbol, start_date, end_date)

    if 'Close' not in data.columns:
        st.error("❌ لا يوجد عمود اسمه 'Close' في البيانات")
    else:
        close = data['Close']
        rsi = calculate_rsi(close)

        # التوصية بناءً على RSI
        latest_rsi = rsi.iloc[-1]
        recommendation = "🔍 لا توجد توصية حاليًا"

        if latest_rsi < 30:
            recommendation = "✅ اشترِ (العملة في منطقة بيع مفرط)"
        elif latest_rsi > 70:
            recommendation = "❌ بيع (العملة في منطقة شراء مفرط)"

        st.subheader("مؤشر RSI")
        st.line_chart(rsi)

        st.subheader("التوصية:")
        st.success(recommendation)

        st.write("آخر قيمة RSI:", round(latest_rsi, 2))
