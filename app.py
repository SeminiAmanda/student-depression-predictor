import streamlit as st
import pandas as pd
import joblib


st.set_page_config(
    page_title="Student Depression Predictor",
    page_icon="🧘‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 
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
        background-color: #2d3748;  /* Dark ash gray – adjust to #4a5568 for lighter ash */
        color: #e2e8f0;  /* Light text for contrast on dark bg */
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 6px solid #a0aec0;  /* Subtle silver accent for depth */
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);  /* Softer shadow on dark */
        margin-bottom: 1rem;
        font-size: 1.0rem;  /* Balanced text size */
    }
    .tip-box strong {
         color: #f7fafc;  /* Near-white for bold emphasis */
         font-weight: bold;
    }
    .tip-box em {
        color: #cbd5e0;  /* Muted light gray for source */
    }
    .contact-box {
        background-color: #fed7d7;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #e53e3e;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #2d3748 !important;  /* Matches your screenshot's dark ash */
    }

    .


    section[data-testid="stSidebar"] {
        background-color: #2d3748 !important;  /* Ash base for sidebar */
    }


    .tips-card {
        background-color: #2d3748;  /* Ash bg */
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);  /* Black-tinted inner shadow */
        border: 1px solid #4a5568;  /* Darker ash border */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }


    .tip-item {
        display: flex;
        align-items: flex-start;
        margin-bottom: 1rem;
        padding: 1rem;
        border-radius: 10px;
        background-color: #000000;  /* Pure black for blocks */
        transition: transform 0.2s ease, box-shadow 0.2s ease, background-color 0.2s ease;
        border: 1px solid #1a1a1a;  /* Near-black seam */
        color: #e2e8f0;  /* Light text on black */
    }

    .tip-item:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);  /* Deeper black shadow */
        background-color: #2d3748;  
        color: #2c5282;  /* Darker blue text on light bg */
    }

    .tip-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
        margin-top: 0.2rem;
        flex-shrink: 0;
        filter: drop-shadow(0 1px 2px rgba(0,0,0,0.5));  /* Icon depth */
    }

    .tip-content {
        flex: 1;
        line-height: 1.5;
    }

    .tip-content strong {
        display: block;
        color: #ffffff;  /* White on black/ash */
        font-size: 1.05rem;
        margin-bottom: 0.4rem;
    }

    .tip-content p {
        color: #cbd5e0;  /* Light ash-gray for descriptions */
        font-size: 0.95rem;
        margin: 0;
        word-wrap: break-word;
    }

/* Contact Card */
    .contact-card {
        background-color: #ebf8ff;  /* Light blue for empathy */
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);  /* Blue-tinted shadow */
        border: 1px solid #bee3f8;  /* Lighter blue border */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: left;
    }

/* Contact Items (Black Blocks with Light Blue Hover) */
    .contact-item {
        display: flex;
        align-items: flex-start;
        margin-bottom: 1rem;
        padding: 0.75rem;
        border-radius: 8px;
        background-color: #000000;  /* Black blocks */
        transition: transform 0.2s ease, box-shadow 0.2s ease, background-color 0.2s ease;
        border-left: 4px solid #2d3748;  /* Ash accent line */
        color: #e2e8f0;  /* Light text */
    }

    .contact-item:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        background-color:#2d3748;
        color: #2c5282;  /* Dark blue text */
    }

    .contact-icon {
        font-size: 1.4rem;
        margin-right: 0.75rem;
        margin-top: 0.25rem;
        flex-shrink: 0;
    }

    .contact-content {
        flex: 1;
        line-height: 1.4;
    }

    .contact-content strong {
        display: block;
        color: #ffffff;  /* White on black */
        font-size: 1rem;
        margin-bottom: 0.25rem;
    }

    .contact-content p {
        color: #cbd5e0;  /* Light ash-gray */
        font-size: 0.9rem;
        margin: 0;
        word-wrap: break-word;
    }

    .contact-content a {
        text-decoration: none;
        color: #3182ce;  /* Blue link */
        font-weight: bold;
    }

    .contact-content a:hover {
        text-decoration: underline;
        color: #2b6cb0;  /* Darker blue */
}   
    </style>
""", unsafe_allow_html=True)


# Load model and encoders
@st.cache_resource
def load_artifacts():
    model = joblib.load("models/final/model_highrecall.pkl")
    
    encoders = {
        col: joblib.load(f"models/final/encoders/{col}_encoder.pkl")
        for col in [
            "gender",
            "dietary_habits",
            "family_history_of_mental_illness",
            "have_you_ever_had_suicidal_thoughts",
        ]
    }
    
    # Load from saved artifacts.
    mean_cgpa = joblib.load("models/final/artifacts/mean_cgpa.pkl")
    final_features = joblib.load("models/final/artifacts/final_features.pkl")
    
    return model, encoders, mean_cgpa, final_features

model, encoders, mean_cgpa, final_features = load_artifacts()


# Inference function
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
                features_df[col + "_encoded"] = -1 
            features_df.drop(columns=[col], inplace=True)
    
    features_df = features_df.reindex(columns=final_features)
    features_df = features_df.fillna(0)
    
    prob = model.predict_proba(features_df)[0][1]
    pred = 1 if prob > 0.5 else 0
    return pred, prob

# Header with Image
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="main-header">🧘‍♀️ Student Depression Predictor</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Empowering Students for Better Mental Health</p>', unsafe_allow_html=True)


st.image("https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2071&q=80", 
         caption="Stay balanced amidst the books 📚")


# Sidebar: Prevention Tips
with st.sidebar:
    st.markdown("---")  
    
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <h2 style="color: #f7fafc; font-size: 1.4rem; margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
            💡 Prevention Tips
        </h2>
        <p style="color: #cbd5e0; font-size: 0.9rem; margin: 0; font-style: italic;">
            Simple steps for student well-being
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tips 
    st.markdown("""
    <div class="tips-card">
        <div class="tip-item">
            <span class="tip-icon">🥗</span>
            <div class="tip-content">
                <strong>Eat Balanced Meals</strong>
                <p>Focus on fruits, veggies, and whole grains for steady mental clarity.</p>
            </div>
        </div>
        <div class="tip-item">
            <span class="tip-icon">😴</span>
            <div class="tip-content">
                <strong>Get Enough Sleep</strong>
                <p>7-9 hours nightly supports better emotional regulation.</p>
            </div>
        </div>
        <div class="tip-item">
            <span class="tip-icon">🌳</span>
            <div class="tip-content">
                <strong>Spend Time in Nature</strong>
                <p>Even a short walk can reduce stress and refresh your mind.</p>
            </div>
        </div>
        <div class="tip-item">
            <span class="tip-icon">🤝</span>
            <div class="tip-content">
                <strong>Build Connections</strong>
                <p>Talk to friends or join support groups—you're not alone.</p>
            </div>
        </div>
        <div class="tip-item">
            <span class="tip-icon">🚫</span>
            <div class="tip-content">
                <strong>Avoid Substances</strong>
                <p>Limit alcohol and drugs to protect your mental health.</p>
            </div>
        </div>
        <div style="text-align: center; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #4a5568;">
            <em style="color: #a0aec0; font-size: 0.85rem;">Source: Mayo Clinic & CDC</em>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
 
   
    st.image("https://images.unsplash.com/photo-1502082553048-f009c37129b9?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", 
         caption="Nature heals 🌿", width=250)
    st.markdown("---")  


# Main: User Input Form
st.header("❤️ Enter Your Details")
with st.form("prediction_form", clear_on_submit=False):
    
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
    
    submit = st.form_submit_button("🔮 Predict My Risk")
    
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
        st.header("💙 Your Results")

       
        with st.container():
            col1, col_center, col3 = st.columns([1, 2, 1])
    
            with col_center:
                if pred == 1:
                   st.error("🚨 **High Risk of Depression Detected**")
                else:
                   st.success("✅ **Low Risk – Keep Up the Good Work!**")
        
                st.image("https://cdn.tinybuddha.com/wp-content/uploads/2013/07/Meditating-1.jpg" if pred == 0 else "https://images.squarespace-cdn.com/content/v1/5ff99155fcd25633938f2b4d/1664901185117-21YWWBPHPPA9LLMSKG73/unsplash-image-LaMnXPLz7qc.jpg", 
                 caption="Seek support—you're not alone 💙" if pred == 1 else "You're thriving! 🌟")
        
    
        st.metric("Depression Risk Probability", f"{prob:.1%}")

        # Interpretation 
        if pred == 1:
            st.warning("""
             **Next Steps:** This is a screening tool, not a diagnosis. Consider speaking to a counselor. 
              High factors like stress or poor sleep may be influencing this—try the prevention tips above!
             """)
        else:
            st.info("Continue monitoring your well-being. Small habits make a big difference.")

# Footer: Contact Details 
st.markdown("---")


col_left, col_right = st.columns([1, 1]) 

with col_left:
    st.image("https://images.unsplash.com/photo-1576092768241-dec231879fc3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", 
             caption="Support is a call away 📞")

with col_right:
    st.markdown("""
    <div class="contact-card">
        <div style="text-align: center; margin-bottom: 1rem;">
            <h3 style="color: #2d3748; font-size: 1.3rem; margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
                📞 Need Immediate Help?
            </h3>
            <p style="color: #80604d; font-size: 0.9rem; margin: 0; font-style: italic;">
                Support is just a call away
            </p>
        </div>
        <div class="contact-item">
            <span class="contact-icon">🇺🇸</span>
            <div class="contact-content">
                <strong>Helpline</strong>
                <p>Call 1926 (NIMH)</p>
            </div>
        </div>
        <div class="contact-item">
            <span class="contact-icon">🌍</span>
            <div class="contact-content">
                <strong>International</strong>
                <p>Befrienders Worldwide – <a href="https://www.befrienders.org" style="color: #c53030;">befrienders.org</a></p>
            </div>
        </div>
        <div class="contact-item">
            <span class="contact-icon">✉️</span>
            <div class="contact-content">
                <strong>CCCline</strong>
                <p>1333</p>
            </div>
        </div>
        <div style="text-align: center; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #fed7d7;">
            <em style="color: #c05621; font-size: 0.95rem;">You're valuable—reach out today.</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("⚠️ Disclaimer: This app is for informational purposes only. Consult a professional for medical advice. Built with ❤️ for student well-being.")