import streamlit as st

# Set Page Title
st.title("📞 Contact & API Access")

# Contact Information
st.header("📩 Contact Us")
st.write("""
If you have any inquiries, feedback, or business opportunities, feel free to reach out!
- **Email**: anno.adham@gmail.com
- **Email**: o.abouyoussef73@gmail.com
- **WhatsApp**: +20 100 857 9698
""")

# API Access Information
st.header("🔑 API Access")
st.write("""
We are working on an API to provide and historical EGX stock market data for FREE. Stay tuned for updates!

**Coming Soon Features:**
- **Intraday & Historical Data** (1-min, 5-min, 30-min) - 100% open source and FREE
- **Portfolio Optimization and Index Tracking**
- **Other EGX Techsolution**
- **US Market data available on demand - 100% open source and FREE**
         
""")

st.markdown("### 📌 **Interested in API Access?**")
st.write("Fill out the form below to get early access when our API launches.")

# API Access Form
with st.form("api_access_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    company = st.text_input("Company (if applicable)")
    use_case = st.text_area("Intended Use Case for API")
    
    submitted = st.form_submit_button("Request Access")
    if submitted:
        st.success("✅ Thank you! We'll contact you when the API is available.")

# Footer
st.markdown("<p style='text-align: center; color: gray;'>© 2025 Data Solutions For EGX | 100% Free & Open Source</p>", unsafe_allow_html=True)
