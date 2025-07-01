import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# إعداد الصفحة
st.set_page_config(page_title="توصيات الفوركس بالذكاء الاصطناعي", layout="centered")
st.title("📊 توصيات الفوركس باستخدام الذكاء الاصطناعي")

# تحميل البيانات
@st.cache_data
def load_data():
    try:
        data = yf.download("EURUSD=X", period="1y", interval="1d")
        if not data.empty:
            return data
        else:
            return None
    except:
        return None

# دالة حساب RSI
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# دالة حساب MACD
def compute_macd(series, short_window=12, long_window=26, signal_window=9):
    short_ema = series.ewm(span=short_window, adjust=False).mean()
    long_ema = series.ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal

# تحميل البيانات
data = load_data()

if data is not None and 'Close' in data.columns:
    # حساب RSI و MACD
    data["RSI"] = compute_rsi(data["Close"])
    data["MACD"], data["Signal"] = compute_macd(data["Close"])

    latest_price = data["Close"].iloc[-1]
    latest_rsi = data["RSI"].iloc[-1]
    latest_macd = data["MACD"].iloc[-1]
    latest_signal = data["Signal"].iloc[-1]

    st.markdown(f"💹 **سعر EURUSD:** `{latest_price:.4f}`")
    st.markdown(f"📊 **RSI الحالي:** `{latest_rsi:.2f}`")
    st.markdown(f"📈 **MACD:** `{latest_macd:.4f}` | **الإشارة:** `{latest_signal:.4f}`")

    # التوصيات بناءً على المؤشرات
    if latest_rsi < 30 and latest_macd > latest_signal:
        st.success("✅ التوصية: دخول شراء (العملة في منطقة بيع مفرط ويوجد تقاطع صاعد MACD)")
    elif latest_rsi > 70 and latest_macd < latest_signal:
        st.error("❌ التوصية: لا تدخل (العملة في منطقة شراء مفرط ويوجد تقاطع هابط MACD)")
    else:
        st.warning("⚠️ التوصية: لا توجد فرصة قوية حاليًا (المؤشرات غير متوافقة)")

    # رسم RSI
    st.subheader("📉 مؤشر RSI")
    st.line_chart(data["RSI"], use_container_width=True)

    # رسم MACD
    st.subheader("📈 مؤشر MACD")
    st.line_chart(data[["MACD", "Signal"]], use_container_width=True)

else:
    st.error("❌ لم يتم تحميل البيانات. تأكد من الاتصال بالإنترنت.")
