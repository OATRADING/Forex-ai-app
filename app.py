import streamlit as st
import pandas as pd
import numpy as np

class ForexAnalyzer:
    def __init__(self, data):
        self.data = data

        # التحقق من وجود عمود 'Close'
        if 'Close' not in self.data.columns:
            st.error("❌ لا يوجد عمود اسمه 'Close' في البيانات المدخلة. الرجاء التأكد من الملف.")
            self._close = None
            return
        else:
            # استخدام Series وليس DataFrame
            self._close = self.data['Close']

        self._calculate_indicators()

    def _calculate_indicators(self):
        if self._close is None:
            return  # لا تكمل إذا لم تكن البيانات صالحة

        # مثال لحساب RSI بسيط
        delta = self._close.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        average_gain = gain.rolling(window=14).mean()
        average_loss = loss.rolling(window=14).mean()

        rs = average_gain / average_loss
        rsi = 100 - (100 / (1 + rs))

        self._rsi = rsi  # من نوع Series 1D
        self.data['RSI'] = self._rsi

    def get_rsi(self):
        return self._rsi
