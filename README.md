# 🧘‍♀️ Student Depression Predictor
This project uses a machine learning model to predict the risk of depression in students.
---

**It's built with a robust MLOps pipeline using Docker Compose, which separates our project into two main services:**
* `train` 🚂: A service for preprocessing data, training the model, and running tests.
* `app` 🚀: A lightweight Streamlit app for production inference.
---
## 🚀 How to Run This Project

### Prerequisites
* [Git](https://git-scm.com/downloads)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)

---
## 📥 Clone the Repository

```bash
git clone https://github.com/SeminiAmanda/student-depression-predictor
cd student-depression-predictor
```
---

## Step 1: Train the Model 🚂
Before we can run the app, we need to train our model. This command builds the `train` service and runs the preprocessing and training scripts.

> ✅ Make sure Docker Desktop is installed and running.

```bash
docker-compose up --build train
```
This will:

  1. Build the `Dockerfile.dev` image.
  2. Run `src/preprocess.py` to create `clean_data.csv`.
  3.  Run `src/train.py` to create all the model artifacts (.pkl files).
  4. You will see all the new files appear in your local `./models/final` and `./Data/processed/final` folders.
---

## Step 2: Test the Model (Optional but Recommended) 🧪
After training, you should validate your model's performance. You have two ways to do this:

### **Method A: Run the test script manually (*✅ Recommended*)**  
This is the fastest way to run only the tests. In your terminal, run:
```bash
docker-compose run train python src/test.py
```

### **Method B: Enable automatic testing**  
You can also configure Docker Compose to run tests automatically every time you run the train service.  

  1. Open your docker-compose.yml file.
  2. Find the train service.
  3. Change the environment variable RUN_TESTS=false to RUN_TESTS=true.

## Step 3: Launch the Streamlit App 🚀
Once your models are trained and tested, you're ready to launch the production application.

```bash
docker-compose up --build app
```
> This builds the lightweight streamlit_app image, copies in the models you just trained, and starts the web server.

✅ **You can now view the live application at:**  🔗 [http://localhost:8501](http://localhost:8501)

## 🛑 How to Stop Everything
To stop all running services (both the app and train), simply run:

>Press `Ctrl + C` in the running terminals, or use:

```bash
docker-compose down
```
---

## 🔧 Developer Guide (Advanced)
### **Run JupyterLab**
The `train` service has JupyterLab installed for data exploration.

  1. Open the `docker-compose.yml` file.

  2. Find the `train` service.

  3. Change the environment variable `RUN_JUPYTER=false` to `RUN_JUPYTER=true`.

  4. Run `docker-compose up train`. The terminal will provide a link to open JupyterLab in your browser.

### Run Scripts Manually
You can get a `bash` shell inside the train container to run any command you want.

```bash
docker-compose run train bash
```

> Once inside the container's shell, you can run scripts individually:

```bash
# (You are now inside the container)
python src/preprocess.py
python src/train.py
python src/test.py
```
