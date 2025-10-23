# استخدم صورة Python الرسمية
FROM python:3.10

# اضبط مجلد العمل
WORKDIR /app

# انسخ ملفات المشروع
COPY . /app

# ثبّت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# أخبر Google Cloud Run أي منفذ يستخدمه Streamlit
ENV PORT 8080

# Streamlit يحتاج إلى تعطيل بعض الإعدادات في بيئة السيرفر
ENV STREAMLIT_SERVER_PORT 8080
ENV STREAMLIT_SERVER_HEADLESS true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS false

# شغّل التطبيق
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
