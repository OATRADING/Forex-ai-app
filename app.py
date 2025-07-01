import streamlit as st import pandas as pd import numpy as np import matplotlib.pyplot as plt import datetime import yfinance as yf from io import BytesIO from fpdf import FPDF import base64 import os import time

تحديث الصفحة تلقائياً كل 60 ثانية 

st.set_page_config(page_title="تحليل الذهب XAUUSD", layout="wide") st.experimental_set_query_params(refresh=str(time.time())) st.experimental_rerun() time.sleep(60)

st.title("📊 توصيات الذهب (XAUUSD) باستخدام الذكاء الاصطناعي")

تحميل بيانات الذهب الحقيقية 

data = yf.download("XAUUSD=X", period="3mo", interval="1d") data.dropna(inplace=True)

حساب RSI 

delta = data['Close'].diff() gain = delta.clip(lower=0) loss = -delta.clip(upper=0) avg_gain = gain.rolling(window=14).mean() avg_loss = loss.rolling(window=14).mean() rs = avg_gain / avg_loss data['RSI'] = 100 - (100 / (1 + rs))

حساب MACD 

ema12 = data['Close'].ewm(span=12, adjust=False).mean() ema26 = data['Close'].ewm(span=26, adjust=False).mean() data['MACD'] = ema12 - ema26 data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

حساب المتوسطات المتحركة 

data['MA50'] = data['Close'].rolling(window=50).mean() data['MA200'] = data['Close'].rolling(window=200).mean()

حذف القيم الفارغة 

data.dropna(inplace=True)

حساب التوصية 

latest_rsi = data['RSI'].iloc[-1] latest_macd = data['MACD'].iloc[-1] latest_signal = data['Signal'].iloc[-1] price = data['Close'].iloc[-1] ma50 = data['MA50'].iloc[-1] ma200 = data['MA200'].iloc[-1]

if latest_rsi < 30 and latest_macd > latest_signal and price > ma50 > ma200: recommendation = "📈 فرصة شراء قوية: RSI منخفض، MACD إيجابي، السعر أعلى من MA50 وMA200" elif latest_rsi > 70 and latest_macd < latest_signal and price < ma50 < ma200: recommendation = "📉 احتمال هبوط قوي: RSI مرتفع، MACD سلبي، السعر تحت MA50 وMA200" else: recommendation = "⏳ لا توجد إشارة واضحة حالياً، انتظر مزيداً من التأكيدات"

عرض التوصية 

st.subheader("🔍 التوصية الحالية:") st.success(recommendation)

رسم بياني للشموع + RSI + MACD + MA 

fig, axs = plt.subplots(3, 1, figsize=(14, 10), sharex=True) fig.suptitle("تحليل فني شامل لزوج الذهب XAUUSD", fontsize=16)

الرسم الأول: الشموع اليابانية + MA 

dates = data.index open_prices = data['Open'] high_prices = data['High'] low_prices = data['Low'] close_prices = data['Close'] for i in range(len(data)): color = 'green' if close_prices[i] >= open_prices[i] else 'red' axs[0].plot([dates[i], dates[i]], [low_prices[i], high_prices[i]], color=color) axs[0].plot([dates[i], dates[i]], [open_prices[i], close_prices[i]], color=color, linewidth=6) axs[0].plot(dates, data['MA50'], label='MA50', color='blue', linewidth=1.5) axs[0].plot(dates, data['MA200'], label='MA200', color='purple', linewidth=1.5) axs[0].set_ylabel("السعر") axs[0].legend() axs[0].grid(True)

الرسم الثاني: RSI 

axs[1].plot(dates, data['RSI'], label="RSI", color="orange") axs[1].axhline(70, color='red', linestyle='--', linewidth=1) axs[1].axhline(30, color='green', linestyle='--', linewidth=1) axs[1].set_ylabel("RSI") axs[1].legend(loc="upper left") axs[1].grid(True)

الرسم الثالث: MACD 

axs[2].plot(dates, data['MACD'], label="MACD", color='blue') axs[2].plot(dates, data['Signal'], label="Signal", color='red') axs[2].axhline(0, color='gray', linewidth=1) axs[2].set_ylabel("MACD") axs[2].legend(loc="upper left") axs[2].grid(True)

plt.xticks(rotation=45) plt.tight_layout(rect=[0, 0, 1, 0.95])

حفظ الشكل كصورة PNG 

img_buffer = BytesIO() fig.savefig(img_buffer, format="png") img_buffer.seek(0)

عرض الرسم 

st.pyplot(fig)

زر لتحميل البيانات كـ Excel 

excel_data = BytesIO() data.to_excel(excel_data, index=True) st.download_button( label="⬇️ تحميل البيانات كملف Excel", data=excel_data.getvalue(), file_name="xauusd_analysis.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" )

زر لتحميل التوصية كنص 

st.download_button( label="📄 تحميل التوصية كنص", data=recommendation, file_name="recommendation.txt", mime="text/plain" )

زر لتحميل الشارت كصورة PNG 

st.download_button( label="🖼️ تحميل الشارت كصورة", data=img_buffer.getvalue(), file_name="xauusd_chart.png", mime="image/png" )

إنشاء تقرير PDF 

pdf = FPDF() pdf.add_page()

إضافة شعار 

logo_path = "logo.png" if os.path.exists(logo_path): pdf.image(logo_path, x=10, y=8, w=33) pdf.set_xy(50, 15)

pdf.set_font("Arial", size=14) pdf.cell(0, 10, txt="تقرير تحليل الذهب XAUUSD", ln=True, align="C") pdf.ln(10)

pdf.set_font("Arial", size=12) pdf.multi_cell(0, 10, recommendation)

حفظ صورة الشارت وإضافتها إلى PDF 

img_path = "chart.png" with open(img_path, "wb") as f: f.write(img_buffer.getvalue()) pdf.image(img_path, x=10, y=70, w=180)

توقيع 

pdf.set_y(-30) pdf.set_font("Arial", size=10) pdf.cell(0, 10, txt="تحياتي: مطور التطبيق | Forex AI Analyzer", ln=True, align="R")

حفظ ملف PDF في الذاكرة 

pdf_buffer = BytesIO() pdf.output(pdf_buffer) pdf_buffer.seek(0)

زر تحميل PDF 

st.download_button( label="📥 تحميل التقرير الكامل PDF", data=pdf_buffer.getvalue(), file_name="xauusd_report.pdf", mime="application/pdf" )

