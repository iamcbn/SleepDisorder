import streamlit as st
import pickle, sys, os, warnings
from helper.utils import UserDataCollector
import pandas as pd

# Setting directory to be parent root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transformers import BMICategorizer, pipeline, BPClassifier, SavedEncoderTransformer, SavedScalerTransformer, FeatureCorrecter
from config import MODEL_FILE, FEATURE_ENCODER, TARGET_ENCODER, BANNER_IMAGE, LOGO_IMAGE, SCALER_FILE
from helper.forms import doctor_form, update_or_create_sheet



def load_model_and_encoders():
    """Fetches the neccessary files and load them"""
    with open(MODEL_FILE, 'rb') as f:
        model = pickle.load(f)

    with open(TARGET_ENCODER, 'rb') as f:
        t_encoder = pickle.load(f)

    with open(FEATURE_ENCODER, 'rb') as f:
        f_encoder = pickle.load(f)
    
    return model, t_encoder, f_encoder


@st.dialog("Feedback Form")
def show_feedback_form():
    doctor_form()

def main():
    # Loading my models
    model, t_encoder, f_encoder = load_model_and_encoders()


    # Streamlit App Header
    st.image(BANNER_IMAGE)
    st.logo(LOGO_IMAGE, size= "large")
    col1, col2, col3 = st.columns([1, 1, 1], vertical_alignment='center', gap= 'small')
    with col3:
        if st.button("Feedback Form",  use_container_width=True):
            show_feedback_form()

    st.title("Sleep Disorder Prediction")

    
    # Setting up session state to track changes.
    if 'predicted' not in st.session_state:
        st.session_state.predicted = False
    if 'inputed' not in st.session_state:
        st.session_state.inputed = {}
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame()
    
    

    # Data Imputation
    st.text("Fill the form")
    with st.expander("Basic Info", expanded= True, icon=":material/person:"):
        gender = st.selectbox("Gender", ["Male", "Female"], placeholder= "Choose an option", index=None)
        age = st.number_input("Age", 0, 120, placeholder= "Enter a value", value=None)
        occupation = st.selectbox("Occupation", ['Software Engineer', 'Doctor', 'Sales Representative', 
                                             'Teacher', 'Nurse', 'Engineer', 'Accountant', 'Scientist', 
                                             'Lawyer', 'Salesperson', 'Manager', 'Others'],
                               placeholder= "Choose an option", index=None)


    with st.expander("Physical Well-being", expanded= True, icon=":material/exercise:"):
        sd = st.number_input("Sleep Duration", 0, 24,value=None, placeholder= "Enter a value",
                              help="How long do you sleep in a day?")
        qs = st.slider("Quality of Sleep", 1,10, value=None,
                        step=1, help="On a scale of 1-10 rate your sleep quality")
        pal = st.slider("Physical Activity Level", 1,10, step=1,value=None,
                        help="On a scale of 1-10, how active are you?")
        sl = st.slider("Stress Level", 1,10, step=1, value=None,
                       help="On a scale of 1-10 how stressed have you been?")
        ds = st.number_input("Daily Steps", min_value= 0, step=1, placeholder= "Enter a value", value=None)

    with st.expander("Vitals", icon= ":material/heart_plus:", expanded=True):
        # Using 2 columns for weight/heights and units
        col1, col2 = st.columns([.8,.2])
        with col1:
            weight = st.number_input("Weight", placeholder= "Enter a value", value=None)
        with col2:
            wt_unit = st.selectbox("Unit", ["kg", "lbs"], placeholder= "Unit", index=None)
        with col1:
            height = st.number_input("Height", placeholder= "Enter a value", value=None)
        with col2:
            hi_unit = st.selectbox("", ["m","cm", "ft"], placeholder= "Unit", index=None)

        hr = st.number_input("Heart Rate", 30, 220, step=1, help="Pulse", value=None, placeholder= "Enter a value")

        st.markdown("###### Blood Pressure")

        # Use three columns to mimic the BP format: SBP / DBP
        col1, col2, col3 = st.columns([3, 0.5, 3])

        with col1:
            sbp = st.number_input(
                label="Systolic (mmHg)", 
                min_value=50, 
                max_value=250, 
                step=1, 
                format="%i", 
                help="Enter your Systolic Blood Pressure (e.g., 120)",
                value=None,
                placeholder= "Enter a value"
            )

        with col2:
            st.markdown("<div style='padding-top: 2.3rem; text-align: center;'>/</div>", unsafe_allow_html=True)

        with col3:
            dbp = st.number_input(
                label="Diastolic (mmHg)", 
                min_value=30, 
                max_value=150,
                value=None, 
                step=1, 
                format="%i", 
                help="Enter your Diastolic Blood Pressure (e.g., 80)",
                placeholder= "Enter a value"
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
        st.session_state.predicted_value = ""
        st.session_state.probability = ""



    # Data Validation
    collector = UserDataCollector()
    error_message = ""

    if not is_incomplete:
        try:
            df = collector.validate(raw)
        except ValueError as e:
            is_valid = False
            error_message = str(e)

    # Display error message
    if error_message:
        st.error(error_message)
        st.stop()

    # Updating session_state.df after data has been validated
    if st.session_state.df.empty and not is_incomplete and not error_message:
        st.session_state.df = df.copy() 

    

    # Prediction
    col1, col2, col3 = st.columns([1,3,1], vertical_alignment='center', gap= 'small')
    with col2:
        if st.button("Predict", disabled= is_incomplete, type = 'primary', use_container_width=True):
                # Preprocessing
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=FutureWarning)
                    trans_data = pipeline.transform(df)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.stop()

            pred = model.predict(trans_data)
            proba = model.predict_proba(trans_data).max()
            result = t_encoder.inverse_transform(pred)[0]
            st.session_state.predicted_value = result
            st.session_state.probability = f"{proba:.2%}"

            st.success(f"ðŸ§  Sleep disorder prediction: **{result}** with **{proba:.2%}** confidence")
            st.session_state.predicted = True

 
    # After Prediction - Collect Doctor Feedback
    if st.session_state.predicted:
        st.markdown("---")
        st.expander("Prediction Evaluation", expanded=True)

        feedback_correct = st.radio("Was the prediction correct?", ["Yes", "No"], index=None)
        correct_diagnosis = None
    
        if feedback_correct == "No":
            correct_diagnosis = st.selectbox("What is the correct diagnosis?", 
                                            ["Sleep Apnea", "Insomnia", "No sleep disorder"],
                                            index=None, 
                                            placeholder="Choose correct diagnosis")

        if st.button("Submit Evaluation", disabled=feedback_correct is None or (feedback_correct == "No" and correct_diagnosis is None)):
            # Attach feedback to input data
            data_to_save = st.session_state.df.copy()
            data_to_save["Predicted"] = st.session_state.predicted_value
            data_to_save["Confidence"] = st.session_state.probability
            data_to_save["Prediction_Correct"] = feedback_correct
            data_to_save["Correct_Diagnosis"] = correct_diagnosis if correct_diagnosis else st.session_state.predicted_value
            update_or_create_sheet("Sleep Data", data_to_save.to_dict())


        


def login():
    st.title("Doctors Page Access")
    dr_name = st.text_input("Enter your name:")
    password = st.text_input("Enter your password to continue:", type="password")

    if password in st.secrets.get("doctors_password"):
        if dr_name is not None:
            st.session_state["logged_in"] = True
            return True, dr_name
        else:
            st.error("Please type your name")
            return None, None
    elif password:
        st.error("Incorrect password! Not Authorized!!")
        return False, None
    else:
        return False, None


# Initial session state
if 'doctor_name' not in st.session_state:
    st.session_state.doctor_name = ""


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    with st.popover("Sign In"):
        success, dr_name = login()
        st.session_state.doctor_name = dr_name
        button = st.button("Sign In")

        if button:
            if success:
                st.session_state["logged_in"] = True
                st.toast(f"Welcome Dr. {dr_name}!", icon="ðŸ’š")
                st.rerun()

            else:
                st.stop()
        else:
            st.stop()

            st.header("Welcome Doctor!")


# Proceed to main content
main()