import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Set page title
st.set_page_config(page_title="Contact & API Access", page_icon="📞")

st.markdown("<h1 style='text-align: center;'>📞 Contact & API Access</h1>", unsafe_allow_html=True)

# Contact Information
st.subheader("📩 Contact Us")
st.write("""
If you have any inquiries, feel free to reach out!  
- 📧 **Email**: support@egxdata.com  
- 🔗 **LinkedIn**: [EGX Data Solutions](https://www.linkedin.com)  
- 🐦 **Twitter/X**: [@EGXData](https://twitter.com)
""")

# API Access Information
st.subheader("🔑 API Access")
st.write("""
🚀 **Coming Soon Features:**  
✅ Intraday & Historical Data (1-min, daily, weekly, monthly)  
✅ Stock Market Indicators  
✅ JSON & CSV Support  
""")

st.markdown("### 📌 **Interested in API Access?**")
st.write("Fill out the form below to get early access when our API launches.")

# Load credentials directly from Streamlit secrets
creds_dict = st.secrets["google_service_account"]

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
    fname = st.text_input("First Name")
    lname = st.text_input("Last Name")
    email = st.text_input("Email Address")
    company = st.text_input("Company (if applicable)")
    use_case = st.text_area("Intended Use Case for API")
    
    submitted = st.form_submit_button("Request Access")
    if submitted:
        if fname and email:
            if save_to_google_sheets(fname, lname, email, company, use_case):
                st.success(f"✅ Thank you, {name}! We'll contact you at {email} when the API is available.")
        else:
            st.warning("⚠️ Please fill in at least your name and email.")
