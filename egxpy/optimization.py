import datetime as dt
import pandas as pd
import numpy as np
import plotly.express as px
import scipy.optimize as sc




def stock_performance(close):
    """Calculates Expected mean returns and variance of a single stock

    Args:
        close (pd.DataFeame): close price list

    Returns:
        np.array: mean returns and covariance matrix 
    """
    returns = close.pct_change()
    mean_returns = returns.mean()
    cov = returns.cov()
    return mean_returns, cov

def portfolio_performance(W, mean_returns, cov, n):
    """Portfolio preformance. a weighted average of stock returns

    Args:
        W (list): _description_
        mean_returns (np.array):mean vector
        cov (np.array): covariance matrix
        n (int): holding period

    Returns:
        float: portfolio_returns, portfolio_risk
    """
    W = np.asarray(W)
    portfolio_returns = (np.dot(W, mean_returns) * n)
    portfolio_risk = np.sqrt(W.T @ cov @ W) * np.sqrt(n)
    return portfolio_returns, portfolio_risk

############################
def _negative_sharpe_ratio(W, mean_returns, cov, risk_free_rate,n):
    portfolio_return, portfolio_risk = portfolio_performance(W, mean_returns, cov, n)
    neg_sharpe_ratio = -(portfolio_return - risk_free_rate)/portfolio_risk
    return neg_sharpe_ratio

def _optimize_portfolio(mean_returns, cov, upper_bound, risk_free_rate,n):
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
    result = sc.minimize(_negative_sharpe_ratio,
                        W,
                        args=(mean_returns, cov, risk_free_rate,n),
                        method='SLSQP',
                        bounds= bounds,
                        constraints=constraint_set)
    neg_sharpe_ratio, optimal_weights = result['fun'], result['x'].round(4)
    return -neg_sharpe_ratio, optimal_weights

def _minimum_risk_portfolio(mean_returns, cov, upper_bound, risk_free_rate,n):
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


def optimize(type, close, n, risk_free_rate:float,  upper_bound:float):
    """optimize portoflio weights based on the selected objective function (Sharpe or MinRisk). Note MinRisk minimizes the standard deviation of Portfolio

    Args:
        type (str): ['Sharpe','MinRisk']
        close (pd.DataFrame): close prices dataframe
        n (int): holding preiod
        risk_free_rate (float): risk free rate
        upper_bound (float): max allocation per equity.

    Returns:
        pd.DataFrame: optimal weights
    """
    close = pd.read_csv(close, index_col=0, header=0)

    # close, mean_returns, cov = liquid_data(close)
    mean_returns, cov = stock_performance(close)

    #maximum Sharpe Ratio portfolio
    if type == 'Sharpe Ratio':
        metric, optimal_weights = _optimize_portfolio(mean_returns, cov, upper_bound, risk_free_rate,n)
    elif type=='MinRisk':
        metric, optimal_weights = _minimum_risk_portfolio(mean_returns, cov, upper_bound, risk_free_rate,n)
                               
    portfolio_returns, portfolio_risk = portfolio_performance(optimal_weights, mean_returns, cov,n)
    st.write(f'Expected return: {portfolio_returns.round(3)}, Risk: {portfolio_risk.round(3)} with {type}:{metric.round(3)}\n')
 
    df = pd.DataFrame({"ticker":close.columns.to_list(), "weight": optimal_weights})
    best_weights = df.loc[df['weight']>0,:].reset_index(drop=True)

    return best_weights


