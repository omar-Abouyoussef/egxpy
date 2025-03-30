from tvDatafeed import TvDatafeedLive, TvDatafeed, Interval
from retry import retry
import time
from datetime import timedelta, date
import datetime as dt
import pandas as pd
import numpy as np
import holidays
from datetime import datetime as dt
import streamlit as st


@retry((Exception), tries=20, delay=0.5, backoff=0)
@st.cache_data
def get_OHLCV_data(symbol,exchange,interval,n_bars, date):
    """fetches close prices for a single ticker

    Args:
        symbol (str): Ticker
        exchange (str): Exchange
        interval (str): ['Daily', 'Weekly','Monthly']
        n_bars (int): Last n bars
        date (date): date for caching

    Returns:
        pd.DataFrame: response
    """

    interval_dic = {'Daily':Interval.in_daily, 'Weekly':Interval.in_weekly, 'Monthly':Interval.in_monthly}


    tv = TvDatafeedLive()
    response = tv.get_hist(symbol=symbol,
                    exchange=exchange,interval=interval_dic[interval], n_bars=n_bars, timeout=-1)
    return response



@retry((Exception), tries=20, delay=0.5, backoff=0)
@st.cache_data
def _get_intraday_close_price_data(symbol,exchange,interval,n_bars, date):
    """fetches close prices for a single ticker

    Args:
        symbol (str): Ticker
        exchange (str): Exchange
        interval (str): ['1 Minute', '5 Minute','30 Minute']
        n_bars (int): Last n bars
        date (date): date for caching

    Returns:
        pd.DataFrame: response
    """

    interval_dic = {'1 Minute':Interval.in_1_minute, '5 Minute':Interval.in_5_minute, '30 Minute':Interval.in_30_minute}


    tv = TvDatafeedLive()
    response = tv.get_hist(symbol=symbol,
                    exchange=exchange,interval=interval_dic[interval], n_bars=n_bars, timeout=-1)['close']
    return response


@retry((Exception), tries=20, delay=0.5, backoff=0)
@st.cache_data
def _get_close_price_data(symbol,exchange,interval,n_bars, date):
    """fetches close prices for a single ticker

    Args:
        symbol (str): Ticker
        exchange (str): Exchange
        interval (str): ['Daily', 'Weekly','Monthly']
        n_bars (int): Last n bars
        date (date): date for caching

    Returns:
        pd.DataFrame: response
    """

    interval_dic = {'Daily':Interval.in_daily, 'Weekly':Interval.in_weekly, 'Monthly':Interval.in_monthly}


    tv = TvDatafeedLive()
    response = tv.get_hist(symbol=symbol,
                    exchange=exchange,interval=interval_dic[interval], n_bars=n_bars, timeout=-1)['close']
    return response



@st.cache_data
def get_EGXdata(stock_list:list, interval:str, start:date, end:date, date:date):

    date=dt.today().date()
    n = holidays.country_holidays('EG').get_working_days_count(start,end)



    close_prices_dic = {}
    try:
        for stock in stock_list:
            close = _get_close_price_data(symbol=stock,exchange='EGX',interval=interval,n_bars=n,date=date)
            close_prices_dic[stock]=close
    except:
        pass
    df = pd.concat(close_prices_dic,axis=1)
    df.index = pd.to_datetime(df.index.date)
    df.index.name = 'Date'


    return df.loc[start:end,:]


def get_EGX_intraday_data(stock_list:list, interval:str, start:date, end:date, date:date):

    date=dt.today().date()
    n =5000



    close_prices_dic = {}
    try:
        for stock in stock_list:
            close = _get_intraday_close_price_data(symbol=stock,exchange='EGX',interval=interval,n_bars=n,date=date)
            close_prices_dic[stock]=close
    except:
        pass
    df = pd.concat(close_prices_dic,axis=1)
    df.tz_localize("Europe/London").tz_convert("UTC+02:00")


    return df.loc[start:end,:].tz_localize("Europe/London").tz_convert("UTC+02:00")




# start=date(2025,3,1)
# end=dt.today().date()
# print(get_EGXdata(stock_list=['ABUK'],interval='Monthly',start=start,end=end,date=end))

# # print(_get_price_data('ABUK','EGX','Daily',25,end))
    
