import streamlit as st
from datetime import datetime as dt
import pandas as pd
import numpy as np
from utils.download import get_EGXdata, get_EGX_intraday_data, get_OHLCV_data

# Inject custom CSS
st.markdown("""
    <style>
    /* Custom title */
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #FFD700; /* Gold */
        text-align: center;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #123524 !important; /* Sidebar with dark green */
    }
    
    /* Main content styling */
    .main-container {
        background-color: #0A1F12 !important;
        color: white;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #FFD700 !important;
        color: #0A1F12 !important;
        font-weight: bold;
        border-radius: 10px;
    }
    
    /* Table styles for financial data */
    .stTable {
        background-color: #0A1F12;
        color: white;
        border: 1px solid #FFD700;
    }
    
    /* Centered footer */
    .footer {
        position: fixed;
        bottom: 10px;
        width: 100%;
        text-align: center;
        font-size: 14px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.markdown("<h1 class='title'>EGX Stock Market Data Downloader</h1>", unsafe_allow_html=True)

# Your Streamlit app logic goes here...

# Footer
st.markdown("<p class='footer'>100% Free & Open Source | Powered by Streamlit</p>", unsafe_allow_html=True)
st.set_page_config(page_title="Download Data", layout='wide')



##############################
#inputs
##########################
#Tickers
tickers = st.text_input(label='Ticker(s): Enter all Caps',
                       key = 'tickers',
                       value='ABUK',
                      )
tickers = st.session_state.tickers.upper()

interval = st.selectbox(label='Interval',
                       options = ['Daily','Weekly','Monthly'],
                       key='interval',
                      )
interval = st.session_state.interval

start = st.date_input(label='Start date:',
              key='start')
start = st.session_state.start

end = st.date_input(label='End date:',
              key='end')
end = st.session_state.end

date = dt.today().date()

if start < end:
    if interval in ['1 Minute','5 Minute','30 Minute']:
            df = get_EGX_intraday_data(tickers.split(" "),interval,start,end,date)

    else:
        df = get_EGXdata(tickers.split(" "),interval,start,end,date)
    
    st.write(df)
else:
    pass

# st.write("Note: Intraday data is available for the last 3000 bars and delayed by 20 minutes. ")
