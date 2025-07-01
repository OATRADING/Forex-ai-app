
import streamlit as st
import pandas as pd
import ta

st.set_page_config(page_title="توصيات الفوركس باستخدام الذكاء الاصطناعي", layout="wide")

st.title("📈 توصيات الفوركس باستخدام الذكاء الاصطناعي")

uploaded_file = st.file_uploader("📤 قم برفع ملف البيانات (CSV)", type=["csv"])

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        st.success("✅ تم تحميل البيانات بنجاح.")

        # التحقق من وجود العمود 'Close'
        if 'Close' not in data.columns:
            st.error("❌ الملف لا يحتوي على عمود 'Close' المطلوب لحساب المؤشرات الفنية.")
            st.stop()

        # التحقق من وجود قيم مفقودة
        if 'Close' not in data.columns:
    st.error("❌ العمود 'Close' غير موجود في الملف المرفوع. تأكد من رفع ملف يحتوي على هذا العمود.")
    st.stop()
elif data['Close'].isnull().sum() > 0:
    st.warning("⚠️ يوجد بيانات ناقصة في عمود 'Close'.")
            st.error("❌ بيانات الإغلاق تحتوي على قيم مفقودة، لا يمكن حساب المؤشرات الفنية.")
            st.stop()

        # حساب مؤشرات فنية
        try:
            data['rsi'] = ta.momentum.RSIIndicator(close=data['Close']).rsi()
            macd = ta.trend.MACD(close=data['Close'])
            data['macd_line'] = macd.macd()
            data['macd_signal'] = macd.macd_signal()
            st.success("✅ تم حساب المؤشرات الفنية بنجاح.")
        except Exception as e:
            st.error(f"❌ تعذر حساب المؤشرات الفنية: {e}")
            st.stop()

        st.subheader("📊 بيانات مع مؤشرات فنية")
        st.dataframe(data.tail())

        # توليد توصية بسيطة
        def get_recommendation(row):
            if row['rsi'] < 30 and row['macd_line'] > row['macd_signal']:
                return 'شراء'
            elif row['rsi'] > 70 and row['macd_line'] < row['macd_signal']:
                return 'بيع'
            else:
                return 'انتظار'

        data['التوصية'] = data.apply(get_recommendation, axis=1)

        st.subheader("📌 آخر توصية")
        st.write(f"🔔 التوصية: **{data['التوصية'].iloc[-1]}**")

    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء معالجة البيانات: {e}")
else:
    st.info("📎 الرجاء رفع ملف CSV يحتوي على بيانات الأسعار (يجب أن يحتوي على عمود 'Close').")
