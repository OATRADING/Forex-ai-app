import streamlit as st
import yfinance as yf
import pandas as pd
import ta
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

st.title("📈 توصيات الفوركس باستخدام الذكاء الاصطناعي")

# اختيار زوج العملات
pair = st.selectbox("اختر زوج العملات", ["EURUSD=X", "USDJPY=X", "GBPUSD=X", "AUDUSD=X", "USDCAD=X"])

# تحميل البيانات
data = yf.download(pair, period="6mo", interval="1d")

# التحقق من وجود البيانات
if data.empty or 'Close' not in data.columns:
    st.error("❌ فشل تحميل بيانات السوق. يرجى التأكد من الاتصال بالإنترنت أو اختيار زوج عملات مختلف.")
    st.stop()

# حساب المؤشرات الفنية بأمان
if data['Close'].isnull().sum() > 0:
    st.error("❌ بيانات الإغلاق تحتوي على قيم مفقودة، لا يمكن حساب المؤشرات الفنية.")
    st.stop()

try:
    # RSI
    data['rsi'] = ta.momentum.RSIIndicator(close=data['Close']).rsi()

    # MACD
    macd = ta.trend.MACD(close=data['Close'])
    data['macd_line'] = macd.macd()
    data['macd_signal'] = macd.macd_signal()
    data['macd'] = data['macd_line'] - data['macd_signal']

    # المتوسط المتحرك
    data['ma10'] = data['Close'].rolling(window=10).mean()

    # الهدف (هل السعر سيرتفع غدًا)
    data['target'] = (data['Close'].shift(-1) > data['Close']).astype(int)

    # حذف القيم الفارغة
    data.dropna(inplace=True)
except Exception as e:
    st.error(f"❌ حدث خطأ أثناء حساب المؤشرات الفنية: {e}")
    st.stop()

# عرض البيانات
st.subheader("📊 البيانات بعد المعالجة")
st.dataframe(data.tail())

# تدريب النموذج
features = ['rsi', 'macd', 'ma10']
X = data[features]
y = data['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# التقييم
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
st.write(f"🎯 دقة النموذج: {acc:.2%}")

# التوصية لليوم الحالي
latest = data.iloc[-1]
latest_features = latest[features].values.reshape(1, -1)
prediction = model.predict(latest_features)[0]

if prediction == 1:
    st.success("✅ التوصية: شراء")
else:
    st.error("⚠️ التوصية: بيع أو الانتظار")

# رسم بياني للسعر
st.line_chart(data['Close'])
