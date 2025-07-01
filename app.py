import streamlit as st
import pandas as pd

st.set_page_config(page_title="توصيات الفوركس باستخدام الذكاء الاصطناعي", layout="centered")

st.title("📈 توصيات الفوركس باستخدام الذكاء الاصطناعي")

# رفع ملف CSV
uploaded_file = st.file_uploader("📂 قم بتحميل ملف البيانات (CSV)", type=["csv"])

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)

        # التحقق من وجود العمود "Close"
        if 'Close' not in data.columns:
            st.error("❌ الملف لا يحتوي على عمود 'Close'. الرجاء التأكد من أن الملف يحتوي على هذا العمود.")
        else:
            # عرض البيانات
            st.success("✅ تم تحميل الملف بنجاح!")
            st.subheader("عرض أول 5 صفوف من البيانات:")
            st.dataframe(data.head())

            # مثال على تحليل بسيط: حساب المتوسط المتحرك
            data['SMA_5'] = data['Close'].rolling(window=5).mean()
            st.subheader("📊 المتوسط المتحرك لـ 5 أيام:")
            st.line_chart(data[['Close', 'SMA_5']])

            # يمكنك هنا إضافة الذكاء الاصطناعي لاحقًا...

    except Exception as e:
        st.error(f"🚨 حدث خطأ أثناء معالجة الملف:\n{e}")
else:
    st.info("⬆️ الرجاء تحميل ملف CSV يحتوي على عمود 'Close' لبدء التحليل.")
