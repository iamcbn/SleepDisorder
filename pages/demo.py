"""
Demo App
"""

import streamlit as st
import pickle, sys, os, warnings
from helper.utils import UserDataCollector
import pandas as pd

# Setting directory to be parent root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transformers import BMICategorizer, pipeline, BPClassifier, SavedEncoderTransformer, SavedScalerTransformer, FeatureCorrecter
from config import MODEL_FILE, FEATURE_ENCODER, TARGET_ENCODER, BANNER_IMAGE, LOGO_IMAGE, SCALER_FILE


def load_model_and_encoders():
    """Fetches the neccessary files and load them"""
    with open(MODEL_FILE, 'rb') as f:
        model = pickle.load(f)

    with open(TARGET_ENCODER, 'rb') as f:
        t_encoder = pickle.load(f)

    with open(FEATURE_ENCODER, 'rb') as f:
        f_encoder = pickle.load(f)
    
    return model, t_encoder, f_encoder


def main():
    # Loading my models
    model, t_encoder, f_encoder = load_model_and_encoders()


    # Streamlit App Header
    st.image(r"data\banner_image.png")
    st.title("Sleep Disorder Prediction")
    st.caption("This is the demo page. Fill free to interact with the model. Your feedback will be appreciated")
    

    # Setting up session state to track changes.
    if 'predicted' not in st.session_state:
        st.session_state.predicted = False
    if 'inputed' not in st.session_state:
        st.session_state.inputed = {}
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame()
    

    # --------- Data Imputation -------------
    st.text("Fill the form")
    with st.expander("Basic Info", expanded= True, icon="ðŸ§"):
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.number_input("Age", 0, 120, 25)
        occupation = st.selectbox("Occupation", ['Software Engineer', 'Doctor', 'Sales Representative', 
                                             'Teacher', 'Nurse', 'Engineer', 'Accountant', 'Scientist', 
                                             'Lawyer', 'Salesperson', 'Manager', 'Others'], index= 0)

    with st.expander("Physical Well-being", expanded= True, icon="ðŸƒðŸ½â€â™‚ï¸"):
        sd = st.number_input("Sleep Duration", 0, 24,
                              value=7, help="How long do you sleep in a day?")
        qs = st.slider("Quality of Sleep", 1,10, value= 5,
                        step=1, help="On a scale of 1-10 rate your sleep quality")
        pal = st.slider("Physical Activity Level", 1,10, step=1,
                        value=5, help="On a scale of 1-10, how active are you?")
        sl = st.slider("Stress Level", 1,10, step=1,
                       value= 5, help="On a scale of 1-10 how stressed have you been?")
        ds = st.number_input("Daily Steps", min_value= 0, step=1, value=5000)

    with st.expander("Vitals", icon= ":material/heart_plus:", expanded=True):
        # Using 2 columns for weight/heights and units
        col1, col2 = st.columns([.8,.2])
        with col1:
            weight = st.number_input("Weight", value=85)
        with col2:
            wt_unit = st.selectbox("Unit", ["kg", "lbs"])
        with col1:
            height = st.number_input("Height", value= 1.75)
        with col2:
            hi_unit = st.selectbox("Unit", ["m","cm", "ft"])

        hr = st.number_input("Heart Rate", 30, 220, value= 90, step=1, help="Pulse")

        st.markdown("###### Blood Pressure")

        # Use three columns to mimic the BP format: SBP / DBP
        col1, col2, col3 = st.columns([3, 0.5, 3])

        with col1:
            sbp = st.number_input(
                label="Systolic (mmHg)", 
                min_value=50, 
                max_value=250,
                value= 110, 
                step=1, 
                format="%i", 
                help="Enter your Systolic Blood Pressure (e.g., 120)"
            )

        with col2:
            st.markdown("<div style='padding-top: 2.3rem; text-align: center;'>/</div>", unsafe_allow_html=True)

        with col3:
            dbp = st.number_input(
                label="Diastolic (mmHg)", 
                min_value=30, 
                max_value=150,
                value=80, 
                step=1, 
                format="%i", 
                help="Enter your Diastolic Blood Pressure (e.g., 80)"
            )


    raw = {
        "Gender"                    : gender,
        "Age"                       : age,
        "Occupation"                : occupation,
        "Sleep Duration"            : sd,
        "Quality of Sleep"          : qs,
        "Physical Activity Level"   : pal,
        "Stress Level"              : sl,
        "Weight"                    : weight,
        "Weight Unit"               : wt_unit,
        "Height"                    : height,
        "Height Unit"               : hi_unit,
        "Heart Rate"                : hr,
        "Daily Steps"               : ds,
        "Systolic BP"               : sbp,
        "Diastolic BP"              : dbp
    }

    
    # The user input section must be full before the predict button is enabled
    is_incomplete = any(not v for v in raw.values())

        
    # If there is any change to the data, session state should track it
    if raw != st.session_state.inputed:
        st.session_state.predicted = False
        st.session_state.df = pd.DataFrame()
        st.session_state.inputed = raw


    # Data Validation
    collector = UserDataCollector()
    error_message = ""

    # To validate each data that is collected
    if not is_incomplete:
        try:
            df = collector.validate(raw)
        except ValueError as e:
            error_message = str(e)

    # Display error message
    if error_message:
        st.error(error_message)

    # Updating session_state.df after data has been validated
    if not error_message.strip():
        if not st.session_state.df.empty:
            st.session_state.df = df.copy() 

    

    # Prediction
    col1, col2, col3 = st.columns([1, 3, 1], vertical_alignment='center', gap= 'small')
    with col2:
        if st.button("Predict", disabled= is_incomplete, type = 'primary', use_container_width=True):
                # Preprocessing
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=FutureWarning)
                    trans_data = pipeline.transform(df)
            except Exception as e:
                st.error(f"ðŸš¨ An error occurred: {e}")

            pred = model.predict(trans_data)
            proba = model.predict_proba(trans_data).max()
            result = t_encoder.inverse_transform(pred)

            st.success(f"ðŸ§  Sleep disorder prediction: **{result}** with **{proba:.2%}** confidence")
            st.session_state.predicted = True

    # Extra Information
    if st.session_state.predicted == True:
        with st.expander("See Health Insights", expanded=True, icon= "ðŸ”"):
            bmi_category = BMICategorizer().transform(df)
            bmi_value = bmi_category['BMI Category'].item()
            if bmi_value == "Obese":
                st.markdown(f":red-badge[ðŸš¨**BMI Category**: {bmi_value}]", help= "Energency: Visit a doctor!!!")
            elif bmi_value ==  "Overweight":
                st.markdown(f":orange-badge[âš ï¸**BMI Category**: {bmi_value}]", help= "Be at alert!: Check body fat ratio")
            else:
                st.badge(f"**BMI Category**: {bmi_value}", color= "green")

            bp_category = BPClassifier().transform(df)
            bp_value = bp_category.loc[0, 'BP Category']
            if bp_value in ['High BP (Stage 2)', 'High BP (Stage 1)', 'Low']:
                st.markdown(f":red-badge[ðŸš¨**BP Category**: {bp_value}]", help= "Energency: Visit a doctor!!!")

            elif bp_value == 'Elevated':
                st.markdown(f":orange-badge[âš ï¸**BP Category**: {bp_value}]", help= "Be at alert!: Something is wrong. Monitor yourself")
            else:
                st.badge(f"**BP Category**: {bp_value}", color= "green")
    


if __name__ == "__main__":
    main()