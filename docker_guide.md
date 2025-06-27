# 🧪 Run the Project in JupyterLab using Docker
---

__👋 Hey everyone!__

**This guide explains how to run our project using Docker after cloning the repo. It will launch a preconfigured Python + JupyterLab environment so everyone can work in the same setup — no need to install anything locally.**

---

## 📥 1. Clone the Repository

```bash
git clone https://github.com/SeminiAmanda/student-depression-predictor
cd student-depression-predictor
```

---

## 🐳 2. Build the Docker Image

> ✅ Make sure Docker Desktop is installed and running.

We are using Docker Compose to build and run the container.
To build the image (only needed the first time, or when requirements.txt changes)

```bash
docker-compose up --build
```

---

## ▶️ 3. Run the JupyterLab Environment

After building, you can start the container like this:

```bash
docker-compose up
```
This will:

- Run the Docker container

- Start the JupyterLab environment inside it

 - Print a link (with a token) in the terminal to open JupyterLab in your browser

Open the link shown in the terminal (usually: http://localhost:8888/).

---
## 💡 Optional: Use Jupyter Kernel in VS Code

1. In VS Code, open the Command Palette(`ctrl + Shift + p`) → `"Jupyter: Select Interpreter to Start Jupyter Server"`

2. Choose `"Existing Jupyter Server"`

3. Paste the URL (with token) from the terminal

4. Select the kernel named something like:
`Python 3 (ipykernel) - /usr/local/bin/python`

---

## 🛑 To Stop the Container
>Press `Ctrl + C` in the running terminal, or use:

```bash
docker-compose down
```
---
