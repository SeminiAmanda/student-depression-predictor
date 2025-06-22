# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and project files
COPY requirements.txt ./
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Set environment variables (optional, for Streamlit)
ENV PYTHONUNBUFFERED=1

# Run Streamlit app (replace 'your_streamlit_app.py' with your actual Streamlit file)
CMD ["streamlit", "run", "src/your_streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]