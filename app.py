import streamlit as st
import pandas as pd
import numpy as np

class ForexAnalyzer:
    def __init__(self, data):
        self.data = data

        # التأكد من وجود عمود Close
        if 'Close' not in data.columns:
            st.error("❌ لا يوجد عمود باسم 'Close' في البيانات.")
            self._close = None
            return

        # تأكد أن self._close عبارة عن Series (وليس DataFrame)
        self._close = data['Close'].squeeze()

        self._calculate_indicators()

    def _calculate_indicators(self):
        if self._close is None:
            return

        # حساب RSI بسيط
        delta = self._close.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        # تأكد أن rsi عبارة عن Series 1D بنفس index
        self._rsi = pd.Series(rsi.values, index=self._close.index)
        self.data['RSI'] = self._rsi

    def get_data(self):
        return self.data


# --- Streamlit واجهة التطبيق ---

st.title("📉 توصيات الفوركس باستخدام الذكاء الاصطناعي")

uploaded_file = st.file_uploader("📂 ارفع ملف بيانات الفوركس (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    analyzer = ForexAnalyzer(df)
    processed_data = analyzer.get_data()

    if processed_data is not None and 'RSI' in processed_data.columns:
        st.subheader("📊 بيانات مع مؤشر RSI")
        st.dataframe(processed_data.tail(20))

        st.line_chart(processed_data[['Close', 'RSI']])
