import yfinance as yf
import pandas as pd
import ta
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout="centered", page_title="AI توصيات فوركس")
st.title("📈 توصيات الفوركس باستخدام الذكاء الاصطناعي")

@st.cache_data
def load_data():
    data = yf.download("EURUSD=X", start="2023-01-01", end="2025-06-30", interval="1d")
    
    # ✅ حل المشكلة: اجعل البيانات 1D فقط
    data = data[['Close']]  # نأخذ فقط عمود الإغلاق

    # حساب المؤشرات الفنية
    data['rsi'] = ta.momentum.RSIIndicator(data['Close']).rsi()
    macd = ta.trend.MACD(data['Close'])
    data['macd_line'] = macd.macd()
data['macd_signal'] = macd.macd_signal()
data['macd'] = data['macd_line'] - data['macd_signal']
    data['ma10'] = data['Close'].rolling(window=10).mean()

    # إنشاء الهدف (Target)
    data['target'] = (data['Close'].shift(-1) > data['Close']).astype(int)
    
    return data.dropna()

# تحميل البيانات وتدريب النموذج
data = load_data()
X = data[['rsi', 'macd', 'ma10']]
y = data['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)
accuracy = accuracy_score(y_test, model.predict(X_test))

# اتخاذ القرار بناءً على آخر صف
last = X.iloc[-1]
decision = model.predict(last.values.reshape(1, -1))[0]

# عرض النتائج في Streamlit
st.markdown(f"### 🔍 دقة النموذج: `{round(accuracy*100, 2)}%`")

if decision == 1:
    st.success("✅ توصية: ادخل السوق — احتمال صعود.")
else:
    st.warning("⛔ لا تدخل الآن — إشارات غير كافية.")

st.line_chart(data[['Close']], height=250)
st.line_chart(data[['rsi']], height=150)
