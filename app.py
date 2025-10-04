import streamlit as st
import pandas as pd
import joblib

# Page config for nicer UI
st.set_page_config(
    page_title="Student Depression Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for nice fonts and shapes
st.markdown("""
    <style>
    .main-header {
        font-family: 'Georgia', serif;
        font-size: 3rem;
        color: #4a5568;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-family: 'Arial', sans-serif;
        font-size: 1.5rem;
        color: #2d3748;
        text-align: center;
    }
    .tip-box {
        background-color: #e6fffa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #38b2ac;
    }
    .contact-box {
        background-color: #fed7d7;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #e53e3e;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Load model and encoders
# -------------------------------
@st.cache_resource
def load_artifacts():
    model = joblib.load("models/Final/model_highrecall.pkl")
    
    encoders = {
        col: joblib.load(f"models/Final/encoders/{col}_encoder.pkl")
        for col in [
            "gender",
            "dietary_habits",
            "family_history_of_mental_illness",
            "have_you_ever_had_suicidal_thoughts",
        ]
    }
    
    train_df = pd.read_csv("Data/processed/final/clean_data.csv")
    mean_cgpa = train_df["cgpa"].mean()
    
    return model, encoders, mean_cgpa

model, encoders, mean_cgpa = load_artifacts()

# -------------------------------
# Inference function
# -------------------------------
def predict_depression(features_df):
    features_df["cgpa"] = features_df["cgpa"].fillna(mean_cgpa)
    
    categorical_columns = [
        "gender",
        "dietary_habits",
        "family_history_of_mental_illness",
        "have_you_ever_had_suicidal_thoughts",
    ]
    for col in categorical_columns:
        if col in features_df.columns:
            le = encoders[col]
            try:
                features_df[col + "_encoded"] = le.transform(features_df[col])
            except ValueError:
                features_df[col + "_encoded"] = 0
            features_df.drop(columns=[col], inplace=True)
    
    prob = model.predict_proba(features_df)[0][1]
    pred = 1 if prob > 0.5 else 0
    return pred, prob

# -------------------------------
# Header with Image
# -------------------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="main-header">🧠 Student Depression Predictor</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Empowering Students for Better Mental Health</p>', unsafe_allow_html=True)

# Header image (student studying/mental health theme)
st.image("https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2071&q=80", 
         caption="Stay balanced amidst the books 📚", use_column_width=True)

# -------------------------------
# Sidebar: Prevention Tips
# -------------------------------
with st.sidebar:
    st.header("💡 Prevention Tips")
    st.markdown("""
    <div class="tip-box">
    <strong>Evidence-based ways to prevent depression:</strong><br><br>
    • **Exercise Regularly**: Aim for 30 minutes a day to boost mood.<br>
    • **Eat Balanced Meals**: Focus on fruits, veggies, and whole grains.<br>
    • **Get Enough Sleep**: 7-9 hours nightly for better emotional regulation.<br>
    • **Spend Time in Nature**: Even a short walk can reduce stress.<br>
    • **Build Connections**: Talk to friends or join support groups.<br>
    • **Avoid Substances**: Limit alcohol and drugs to protect mental clarity.<br>
    <em>Source: Mayo Clinic & CDC</em>
    </div>
    """, unsafe_allow_html=True)
    
    # Tip image
    st.image("https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", 
             caption="Nature heals 🌿")

# -------------------------------
# Main: User Input Form
# -------------------------------
st.header("📝 Enter Your Details")
with st.form("prediction_form", clear_on_submit=False):
    # Use columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Demographics")
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.number_input("Age", min_value=18, max_value=40, value=22)
        degree_encoded = st.selectbox("Degree Level", options=[0,1,2,3,4], 
                                      format_func=lambda x: ["Others", "Class 12", "Bachelor's", "Master's", "PhD"][x])
    
    with col2:
        st.subheader("Academics")
        academic_pressure = st.slider("Academic Pressure (1-5)", 1, 5, 3)
        cgpa = st.number_input("CGPA (0-4 scale)", min_value=0.0, max_value=4.0, value=3.0)
        study_satisfaction = st.slider("Study Satisfaction (1-5)", 1, 5, 3)
        work_study_hours = st.number_input("Weekly Work/Study Hours", min_value=0, max_value=50, value=10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Lifestyle")
        dietary_habits = st.selectbox("Dietary Habits", ["Healthy", "Moderate", "Unhealthy"])
        sleep_duration_encoded = st.selectbox("Sleep Duration", options=[0,1,2,3], 
                                              format_func=lambda x: ["<5 hours", "5-6 hours", "7-8 hours", ">8 hours"][x])
        financial_stress = st.slider("Financial Stress (1-5)", 1, 5, 2)
    
    with col2:
        st.subheader("Mental Health History")
        family_history = st.selectbox("Family History of Mental Illness", ["Yes", "No"])
        suicidal_thoughts = st.selectbox("Ever Had Suicidal Thoughts", ["Yes", "No"])
    
    submit = st.form_submit_button("🔮 Predict My Risk", use_container_width=True)
    
    if submit:
        input_data = {
            "gender": [gender],
            "age": [age],
            "academic_pressure": [academic_pressure],
            "cgpa": [cgpa],
            "study_satisfaction": [study_satisfaction],
            "dietary_habits": [dietary_habits],
            "have_you_ever_had_suicidal_thoughts": [suicidal_thoughts],
            "work_study_hours": [work_study_hours],
            "financial_stress": [financial_stress],
            "family_history_of_mental_illness": [family_history],
            "degree_encoded": [degree_encoded],
            "sleep_duration_encoded": [sleep_duration_encoded],
        }
        features_df = pd.DataFrame(input_data)
        
        pred, prob = predict_depression(features_df)
        
        # Results Section
        st.header("📊 Your Results")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if pred == 1:
                st.error("🚨 **High Risk of Depression Detected**")
                st.image("https://images.unsplash.com/photo-1531297484001-80022131f5a1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", 
                         caption="Seek support—you're not alone 💙", use_column_width=True)
            else:
                st.success("✅ **Low Risk – Keep Up the Good Work!**")
                st.image("https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", 
                         caption="You're thriving! 🌟", use_column_width=True)
        
        # Probability gauge
        st.metric("Depression Risk Probability", f"{prob:.1%}")
        
        # Interpretation
        if pred == 1:
            st.warning("""
            **Next Steps:** This is a screening tool, not a diagnosis. Consider speaking to a counselor. 
            High factors like stress or poor sleep may be influencing this—try the prevention tips above!
            """)
        else:
            st.info("Continue monitoring your well-being. Small habits make a big difference.")

# -------------------------------
# Footer: Contact Details
# -------------------------------
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col2:
    st.markdown("""
    <div class="contact-box">
    <strong>Need Immediate Help?</strong><br><br>
    • **US Hotline:** Call 988 (Suicide & Crisis Lifeline)<br>
    • **International:** Befrienders Worldwide – befrienders.org<br>
    • **Email Support:** contact@mentalhealth.org (or your local service)<br>
    <em>You're valuable—reach out today.</em>
    </div>
    """, unsafe_allow_html=True)

# Contact image
st.image("https://images.unsplash.com/photo-1551836022-ef6fc6b4b6e5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", 
         caption="Support is a call away 📞", use_column_width=True)

st.markdown("---")
st.caption("⚠️ Disclaimer: This app is for informational purposes only. Consult a professional for medical advice. Built with ❤️ for student well-being.")