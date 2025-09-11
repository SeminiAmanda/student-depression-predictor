FROM python:3.13-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create necessary directories upfront
RUN mkdir -p Data/processed/final models/Final models/Final/encoders

# Default command
CMD ["bash", "-c", "\
# 1️⃣ Preprocess if needed \
if [ ! -f Data/processed/final/clean_data.csv ]; then \
    python src/preprocess.py; \
fi && \
# 2️⃣ Train if models missing \
if [ ! -f models/Final/model_highrecall.pkl ]; then \
    python src/train.py; \
fi && \
# 3️⃣ Run tests if RUN_TESTS=true \
if [ \"$RUN_TESTS\" = \"true\" ]; then \
    python tests/test.py; \
fi && \
# 4️⃣ Start Jupyter Lab if RUN_JUPYTER=true \
if [ \"$RUN_JUPYTER\" = \"true\" ]; then \
    jupyter-lab --ip=0.0.0.0 --allow-root --no-browser; \
fi && \
# Keep bash open \
exec bash"]
