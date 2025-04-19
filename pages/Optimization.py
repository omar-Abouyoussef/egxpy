import datetime as dt
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy.optimize as sc
import streamlit as st




def stock_performance(close):
    returns = close.pct_change()
    mean_returns = returns.mean()
    cov = returns.cov()
    return mean_returns, cov

def portfolio_performance(W, mean_returns, cov, n):
    W = np.asarray(W)
    portfolio_returns = (np.dot(W, mean_returns) * n)
    portfolio_risk = np.sqrt(W.T @ cov @ W) * np.sqrt(n)
    return portfolio_returns, portfolio_risk

############################
def negative_sharpe_ratio(W, mean_returns, cov, risk_free_rate,n):
    portfolio_return, portfolio_risk = portfolio_performance(W, mean_returns, cov, n)
    neg_sharpe_ratio = -(portfolio_return - risk_free_rate)/portfolio_risk
    return neg_sharpe_ratio

def optimize_portfolio(mean_returns, cov, upper_bound, risk_free_rate,n):
    """
    returns
    -------
    sharpe_ratio, optimal_weights
    """
    #assign random weights
    np.random.seed(1)
    W = np.random.random(len(mean_returns))
    W = [weight/ np.sum(W) for weight in W]

    #add bounds
    bound = (0,upper_bound)
    bounds = tuple(bound for w in range(len(W)))

    #constraint
    def constraint(W):
        return np.sum(W) - 1


    constraint_set = [{'type': 'eq', 'fun': constraint}]
    #minimize negative SharpeRatio
    result = sc.minimize(negative_sharpe_ratio,
                        W,
                        args=(mean_returns, cov, risk_free_rate,n),
                        method='SLSQP',
                        bounds= bounds,
                        constraints=constraint_set)
    neg_sharpe_ratio, optimal_weights = result['fun'], result['x'].round(4)
    return -neg_sharpe_ratio, optimal_weights

def minimum_risk_portfolio(mean_returns, cov, upper_bound, risk_free_rate,n):
    """
    returns
    -------
    sharpe_ratio, optimal_weights"""
     #assign random weights
    np.random.seed(1)
    W = np.random.random(len(mean_returns))
    W = [weight/ np.sum(W) for weight in W]

    #add bounds
    bound = (0,upper_bound)
    bounds = tuple(bound for w in range(len(W)))

    #constraint 
    def constraint(W):
        return np.sum(W) - 1
    constraint_set = [{'type': 'eq', 'fun': constraint}]
    
    def portfolio_variance(W,cov,n):
        return (np.sqrt(W.T @ cov @ W) * np.sqrt(n))

    result = sc.minimize(portfolio_variance,
                        W,
                        args = (cov,n),
                        bounds = bounds,
                        constraints = constraint_set,
                        method = 'SLSQP')

    min_risk, optimal_weights = result['fun'], result['x'].round(4)
    return min_risk, optimal_weights


def main(type, close, n, risk_free_rate:float,  upper_bound:float):
    # close, mean_returns, cov = liquid_data(close)
    mean_returns, cov = stock_performance(close)

    #maximum Sharpe Ratio portfolio
    if type == 'Sharpe Ratio':
        metric, optimal_weights = optimize_portfolio(mean_returns, cov, upper_bound, risk_free_rate,n)
    else:
        metric, optimal_weights = minimum_risk_portfolio(mean_returns, cov, upper_bound, risk_free_rate,n)
                               
    portfolio_returns, portfolio_risk = portfolio_performance(optimal_weights, mean_returns, cov,n)
    st.write(f'Expected return: {portfolio_returns.round(3)}, Risk: {portfolio_risk.round(3)} with {type}:{metric.round(3)}\n')
 
    df = pd.DataFrame({"ticker":close.columns.to_list(), "weight": optimal_weights})
    best_weights = df.loc[df['weight']>0,:].reset_index(drop=True)

    return best_weights




##################
#Streamlit app
####################

st.set_page_config(page_title='Portfolio Optimization', layout='wide')
st.title('Portfolio Optimization')


#########
#inputs
##########

close = st.file_uploader(label='Upload CSV:',
                 type='csv',
                 key='close')
close = st.session_state.close

upper_bound = st.number_input(label='Diversification Threshold:',
                              value = 0.1,
                              key='upper_bound')
upper_bound = st.session_state.upper_bound


risk_free_rate = st.number_input(label='Risk Free Rate:',
                              value = 0.2,
                              key='risk_free_rate')
risk_free_rate = st.session_state.risk_free_rate

holding_period = st.number_input(label='Holding Period:',
                              value = 252,
                              key='Holding Period:')

type = st.selectbox(label='Optimization Type',
                   options=['Sharpe Ratio','Minimum Risk'])

benchmark = st.file_uploader(label='Upload CSV Of Desired Benchmark',
                 type='csv',
                 key='benchmark')
benchmark = st.session_state.benchmark
###########
#############

if close:
    close = pd.read_csv(close, index_col=0, header=0)
    portfolio_weights = main(type, close,holding_period,
        risk_free_rate=risk_free_rate,
        upper_bound=upper_bound
        )
    
    cols = st.columns([0.7,0.3])
    with cols[0]:
        fig = px.pie(portfolio_weights, values='weight', names='ticker', title='Portfolio Weights')
        st.plotly_chart(fig)
        
    with cols[1]:
        st.dataframe(portfolio_weights)
    

    portfolio = close.loc[:,portfolio_weights.ticker] @ portfolio_weights.weight.values.reshape((-1,1))

    if benchmark:
        benchmark = pd.read_csv(benchmark, index_col=0, header=0)
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=portfolio.index, y=portfolio.sum(axis=1)/portfolio[0])
                     )
        fig.add_trace(
            go.Scatter(x=benchmark.index, y=benchmark.sum(axis=1)/benchmark[0])
        )          
        st.plotly_chart(fig)



