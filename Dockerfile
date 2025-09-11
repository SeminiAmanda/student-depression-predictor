FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "-c", "if [ ! -f Data/processed/final/clean_data.csv ]; then python src/preprocess.py; fi && if [ \"$RUN_JUPYTER\" = \"true\" ]; then jupyter-lab --ip=0.0.0.0 --allow-root --no-browser; fi"]
