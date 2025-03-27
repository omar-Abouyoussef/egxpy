import streamlit as st
from datetime import datetime as dt
import pandas as pd
import numpy as np
from utils.download import get_EGXdata, get_EGX_intraday_data, get_OHLCV_data



st.set_page_config(page_title="Download Data")
st.title('Download Data')


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

st.write("Note: Intraday data is available for the last 3000 bars and delayed by 20 minutes. ")
