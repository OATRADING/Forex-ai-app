import streamlit as st
import pandas as pd
import yfinance as yf

# دالة لحساب RSI يدويًا بدون مكتبة ta
def calculate_rsi(close, period=14):
    delta = close.diff().dropna()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up = up.rolling(window=period).mean()
    roll_down = down.rolling(window=period).mean().abs()
    RS = roll_up / roll_down
    RSI = 100.0 - (100.0 / (1.0 + RS))
    return RSI

# تحميل البيانات من Yahoo Finance
@st.cache_data
def load_data(symbol="EURUSD=X", start="2023-01-01", end="2025-06-30"):
    try:
        data = yf.download(symbol, start=start, end=end, interval="1d")
        data['RSI'] = calculate_rsi(data['Close'])
        return data.dropna()
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None

# إعداد صفحة Streamlit
st.set_page_config(layout="centered", page_title="توصيات الفوركس بالذكاء الاصطناعي")
st.title("توصيات الفوركس باستخدام الذكاء الاصطناعي")

# تحميل البيانات وتحليلها
data = load_data()

if data is not None:
    latest_rsi = data['RSI'].iloc[-1]
    st.markdown(f"### 📊 القيمة الحالية لمؤشر RSI: {latest_rsi:.2f}")
                                                          
latest_rsi = data['RSI'].iloc[-1]
st.markdown(f"### 📊 الحالة الحالية RSI: {latest_rsi:.2f}")
                                                     
    if latest_rsi < 30:
        st.success("### قيمة RSI الحالية: `{round(latest_rsi, 2)}`")

    # توليد التوصية بناءً على RSI
    if latest_rsi < 30:
        st.success("التوصية: دخول السوق (العملة في منطقة بيع مفرط).")
    elif latest_rsi > 70:
        st.error("التوصية: لا تدخل السوق (العملة في منطقة شراء مفرط).")
    else:
        st.info("التوصية: ترقّب — السوق غير واضح حالياً.")

                         
    st.subheader("📈 عرض الشارت")
    st.subheader("سعر الإغلاق")
    st.line_chart(data['Close'], height=250, use_container_width=True)
    st.subheader("مؤشر RSI")
    st.line_chart(data['RSI'], height=150, use_container_width=True)
