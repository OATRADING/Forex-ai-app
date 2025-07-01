import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# --- إعداد الصفحة ---
st.set_page_config(page_title="توصيات الفوركس بالذكاء الاصطناعي", layout="centered")
st.title("📊 توصيات الفوركس باستخدام الذكاء الاصطناعي")

# --- تحميل البيانات ---
@st.cache_data
def load_data():
    try:
        data = yf.download("EURUSD=X", period="1y", interval="1d")
        if not data.empty:
            data["RSI"] = compute_rsi(data["Close"], 14)
            return data
        return None
    except Exception as e:
        st.error(f"حدث خطأ أثناء تحميل البيانات: {e}")
        return None

# --- دالة حساب RSI ---
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# --- زر تحديث ---
if st.button("🔄 تحديث البيانات"):
    st.experimental_rerun()

# --- جلب البيانات ---
data = load_data()

if data is not None and not data.empty and 'Close' in data.columns:
    latest_price = data['Close'].iloc[-1]
    latest_rsi = data['RSI'].iloc[-1]

    st.markdown(f"💰 **السعر الحالي لـ EURUSD:** `{latest_price:.4f}`")
    st.markdown(f"📈 **مؤشر RSI الحالي:** `{latest_rsi:.2f}`")

    # --- التوصية ---
    if latest_rsi < 30:
        st.success("✅ التوصية: دخول السوق (العملة في منطقة بيع مفرط).")
    elif latest_rsi > 70:
        st.warning("⚠️ التوصية: لا تدخل السوق (العملة في منطقة شراء مفرط).")
    else:
        st.info("ℹ️ التوصية: لا توجد فرصة قوية حالياً (RSI في منطقة محايدة).")

    # --- الشارتات ---
    st.subheader("📉 الرسم البياني لسعر الإغلاق")
    st.line_chart(data["Close"], use_container_width=True)

    st.subheader("📊 مؤشر RSI")
    st.line_chart(data["RSI"], use_container_width=True)

else:
    st.error("❌ لم يتم تحميل البيانات. تأكد من الاتصال بالإنترنت أو من رمز العملة.")
