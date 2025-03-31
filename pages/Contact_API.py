import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Load credentials from Streamlit secrets
creds_json = st.secrets["google_service_account"]
creds_dict = json.loads(json.dumps(creds_json))

# Authenticate with Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open Google Sheet
SHEET_NAME = "EGX_API_Requests"
sheet = client.open(SHEET_NAME).sheet1

def save_to_google_sheets(name, email, company, use_case):
    """Saves form responses to a Google Sheet."""
    try:
        sheet.append_row([name, email, company, use_case])
        return True
    except Exception as e:
        st.error(f"❌ Error saving data: {e}")
        return False

# Streamlit form
st.title("API Access Request Form")
with st.form("api_access_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    company = st.text_input("Company (if applicable)")
    use_case = st.text_area("Intended Use Case for API")
    
    submitted = st.form_submit_button("Request Access")
    if submitted:
        if name and email:
            if save_to_google_sheets(name, email, company, use_case):
                st.success(f"✅ Thank you, {name}! We'll contact you at {email} when the API is available.")
        else:
            st.warning("⚠️ Please fill in at least your name and email.")
