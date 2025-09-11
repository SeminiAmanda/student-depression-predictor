# Student Depression Predictor

# 🧪 Run the Project using Docker
---

__👋 Hey everyone!__

**This guide explains how to run our project using Docker after cloning the repo. It will launch a preconfigured Python environment with all dependencies and scripts, so no local setup is needed.**

---

## 📥 1. Clone the Repository

```bash
git clone https://github.com/SeminiAmanda/student-depression-predictor
cd student-depression-predictor
```
---

## 🐳 2. Build the Docker Image

> ✅ Make sure Docker Desktop is installed and running.
Docker Compose will handle building the image and creating necessary folders.
Run this command to build (needed the first time, or when requirements.txt changes):


```bash
docker-compose up --build
```

---

## ▶️ 3. Run the Project

Start the container:


```bash
docker-compose up
```

This will:

- Preprocess raw data if clean_data.csv is missing

- Train models if they do not exist

- Optionally run tests (RUN_TESTS=true)

- Optionally start JupyterLab (RUN_JUPYTER=true)

- Keep the container open for manual commands

- By default, JupyterLab is skipped and tests are run.

---

## 💡 Optional: Start JupyterLab

To run JupyterLab inside the container, set the environment variable:

```bash
export RUN_JUPYTER=true
docker-compose up

```
## 🛑 To Stop the Container
>Press `Ctrl + C` in the running terminal, or use:

```bash
docker-compose down
```
---

## 🔧 Optional: Run Scripts Manually

Once inside the container (bash shell):

```bash
# Preprocess data
python src/preprocess.py

# Train models
python src/train.py

# Run tests
python src/test.py

```
> This is useful if you want to rerun a specific step without rebuilding the container.
---
