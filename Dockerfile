FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["jupyter-lab", "--ip=0.0.0.0", "--allow-root", "--no-browser"]