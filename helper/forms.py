import streamlit as st
import re
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo


# ------- Connecting to Google Sheet ----------
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data  # Cache the data fetching process
def fetch_data_from_sheet(worksheet_name):
    """Fetch the data from Google Sheet."""
    return conn.read(worksheet=worksheet_name)

def update_or_create_sheet(worksheet_name: str, new_data: dict):
    """
    Check if worksheet exists in Google Sheet.
    - If it doesn't, create it and add the first row.
    - If it does, append a new row.
    """
    if isinstance(new_data, dict):
        new_df = pd.DataFrame(new_data)
    else:
        new_df = new_data.copy()


    
    try:
        # Fetch the latest data from the sheet
        existing_data = fetch_data_from_sheet(worksheet_name)

        # If the worksheet is empty (None), just write the new data
        if existing_data is None:
            df = new_df.copy()
        else:
            df = pd.DataFrame(existing_data)
            df = pd.concat([df, new_df], ignore_index=True)

        # Update the worksheet
        conn.update(worksheet=worksheet_name, data=df)

        # Clear the cache to force the app to fetch fresh data next time
        st.cache_data.clear()

    except Exception as e:
        st.error(f"Error updating sheet: {e}")
        return




# ------------- STREAMLIT FORM --------------
def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9.-]+$"
    return re.match(pattern, email) is not None

# ----- Implementing Session State
if 'message' not in st.session_state:
    st.session_state.message = {}
message = {}

def contact_form():
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Your Message")
        submitted = st.form_submit_button("Send")

        if submitted:
            if not name or not email or not message:
                st.error("Please fill out all fields.")
                st.stop()
            elif not validate_email(email):
                st.error("Please enter a valid email address.")
                st.stop()
            else:
                message_data = {
                    'Name' : name,
                    'Email' : email,
                    'Message' : message,
                    'TimeStamp' : datetime.now(ZoneInfo("Africa/Lagos"))
                    }
                st.session_state.message = message_data
                update_or_create_sheet("Contact Form", message_data)

                st.success("Thanks for reaching out! I’ll get back to you soon.")
                
        

def doctor_form():
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        specialization = st.text_input("Area of Specialization")
        message = st.text_area("Your Feedback: Any symptoms or observations the model missed?")
        suggestions = st.text_area("Suggestions to improve the model (optional)")
        follow_up = st.checkbox("I’m open to being contacted for follow-up questions")
        submitted = st.form_submit_button("Send")

        if submitted:
            if not name or not email or not message:
                st.error("Please fill out all fields.")
                st.stop()
            elif not validate_email(email):
                st.error("Please enter a valid email address.")
                st.stop()
            else:
                message_data = {
                    'Name' : name,
                    'Email' : email,
                    'Specialization' : specialization,
                    'Feedback' : message,
                    'Suggestions': suggestions,
                    'Follow up'  : follow_up,
                    'TimeStamp' : datetime.now(ZoneInfo("Africa/Lagos"))
                    }
                st.session_state.message = message_data
                update_or_create_sheet("Doctors' Feedback Form", message_data)

                st.success("Thank you for your feedback!")


