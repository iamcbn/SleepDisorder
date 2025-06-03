import streamlit as st
import sys, os
from helper.forms import contact_form

st.image(r"data\banner_image.png")
tab1, tab2 = st.tabs(["About the Project", "About Me"])

# ------- ABOUT THE PROJECT TAB ----------
with tab1:
    st.title("About the Project")
    with st.container():
        st.write("""
                 ### Purpose

                 Sleep disorders often go undiagnosed until they severely impact health 
                 and daily functioning. This project aims to provide a lightweight, early-screening
                 tool powered by machine learning to help users—and especially healthcare professionals—identify 
                 potential sleep-related risks based on basic health and lifestyle information.
                 """)
    with st.container():
        st.write("""
                ### How the App Works
                This app is structured into four main pages:

                - **`Home`**: Learn about the project, me, and how to get involved or collaborate.
                - **`Demo`**: Public-friendly version for quick predictions. Enter your health information and get a predicted sleep disorder status instantly.
                - **`Clinical Corner`**: Designed for healthcare professionals. Includes a feedback form to help evaluate the tool's performance in real-world settings.
                - **`Model Evaluation`**: Displays technical performance metrics like F1-macro, confusion matrix, classification report and SHAP for machine learning practitioners and clinical data analysts.

                Use the sidebar to navigate between pages.
                 """)
    with st.container():
        st.write(""" 
                ### Data & Modelling
                The model is trained on a dataset containing health-related and behavioural data (e.g., BMI, blood pressure, stress levels, sleep duration).
                Key steps include:

                - Preprocessing and encoding of input features
                - Handling class imbalance with techniques like SMOTE
                - Model selection and tuning (e.g., Support Vector Classifier with One-vs-One strategy)
                - Evaluation using F1-macro, prioritising multi-class balance
                """)
    with st.container():
        st.write('''
                ### Limitations
                - Not a diagnostic tool: This model is meant for educational and screening support only. It does not replace clinical judgment.
                - Limited generalisability: Model performance is based on specific data. Further testing and validation are required for broader clinical adoption.
                - Data bias risk: Predictions may reflect biases in the dataset used.
                ''')
    with st.container():
        st.write("""
                ### Disclaimer
                This tool should not be used to make medical decisions on its own. Always consult a qualified healthcare provider for medical advice, diagnosis, or treatment. The Clinical page is intended to help gather feedback from medical professionals for iterative improvement.
                """)

# ------- CONTACT FORM (CONTACT ME) HELPER FUNCTION -------
@st.dialog("Contact Me")
def show_contact_form():
    contact_form()

# ------- ABOUT THE ME TAB ----------
with tab2:
    with st.container():
        st.write("""
                ### 👋🏽 Hi! I’m **Bruno**
                A data scientist passionate about using machine learning to improve healthcare outcomes. I believe that by bridging data and medicine, we can support clinicians, reduce their cognitive load, and ultimately help prevent medical errors—especially in resource-constrained settings.
                \n
                 
                 With **1+ year of hands-on experience**, I’ve worked on real-world projects that span the full data science lifecycle—from data wrangling and analysis to building, evaluating, and deploying machine learning models. My recent focus has been on healthcare, particularly in developing solutions like this **sleep disorder screening app** to demonstrate how AI can assist in early detection and clinical decision support.
                """)
    with st.container():
        st.write("""
                ### Core Skills

                - **Machine Learning & Predictive Modelling**: Logistic Regression, Random Forest, SVM, KNN, etc.
                - **Programming Language**: Python, SQL
                - **Data Visualisation**: PowerBI, MS Excel, Matplotlip, Seaborn
                - **Streamlit for App Development**
                - **SQL for Database Management**
                - **Version Control with Git & GitHub**
                """)
    with st.container():
        st.write("""
                ### Let’s Connect

                Have a question, collaboration, or idea? 
                Use the contact form below to send me a direct message.\n           
                """)
        col1, col2, col3 = st.columns([1, 1, 1], vertical_alignment='center', gap= 'small')
        with col1:
            st.link_button("🔗 LinkedIn", "https://www.linkedin.com/in/bruno-nwagbo", use_container_width=True)

        with col2:
            st.link_button("💻 GitHub", "https://github.com/iamcbn", use_container_width=True)

        with col3:
            if st.button("Contact Me",  use_container_width=True, icon= ":material/mail:"):
                show_contact_form()









        