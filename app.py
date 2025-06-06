import streamlit as st
import sys, os

# Setting directory to be parent root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import LOGO_IMAGE


# --- Define Pages ---
home_page = st.Page("pages/home.py", title="Home")
demo_page = st.Page("pages/demo.py", title="Demo")
eval_page = st.Page("pages/evaluation.py", title="Model Evaluation")
doctors_page = st.Page("pages/doctors.py", title="Clinician Portal")

# --- Setup Navigation With Sections---
pages = {
    "": [home_page],
    "Projects": [demo_page, doctors_page],
    "Performance": [eval_page]
}

navigation = st.navigation(pages)

# --- App Add-ins ---
st.logo(LOGO_IMAGE, size= "large")
st.sidebar.text("Made with ❤ by Bruno")
st.sidebar.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/bruno-nwagbo)")
st.sidebar.markdown("[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/iamcbn)")


# ---- Sidebar Customi
navigation.run()
