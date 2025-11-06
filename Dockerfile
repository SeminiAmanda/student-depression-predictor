FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the necessary files
COPY app.py .

# Copy all models, encoders, and artifacts
COPY models/ ./models/

EXPOSE 8501

# Streamlit config
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLECORS=false \
    STREAMLIT_SERVER_PORT=8501

CMD ["streamlit", "run", "app.py"]