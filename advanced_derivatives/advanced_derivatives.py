import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize

S0 = 100  # Initial price
T = 10.0  # Time to maturity
mu = 0.15  # Expected return
sigma = 0.15  # Volatility
dt = 0.02  # Time step
N = int(T / dt)  # Number of time steps
sim = 2000  # Number of sims

def simulate_gbm(S0, mu, sigma, dt, N, sim):
    dt = T/N
    t = np.linspace(0, T, N)
    W = np.random.standard_normal(size=(N, sim))
    W = np.cumsum(W, axis=0) * np.sqrt(dt)  # Brownian motion
    
    t = t.reshape(-1, 1)  
    X = (mu - 0.5 * sigma**2) * t + sigma * W 
    S = S0 * np.exp(X)  
    return S


S = simulate_gbm(S0, mu, sigma, dt, N, sim)

plt.figure(figsize=(15,9))
plt.plot(S[:, :15])
plt.title('Simulated GBM stock Price Paths')
plt.xlabel('Time Steps')
plt.ylabel('Stock Price')
plt.show()

asset_returns = np.log(S[1:] / S[:-1])
mean_returns = asset_returns.mean(axis=0)
cov_matrix = np.cov(asset_returns.T)

num_assets = sim
wts = np.array(num_assets * [1. / num_assets,])

def port_vol(wts, mean_returns, cov_matrix):
    return np.sqrt(np.dot(wts.T, np.dot(cov_matrix, wts)))

def check_sum(wts):
    return np.sum(wts) - 1

tickers = ['AAPL', 'AMZN', 'GOOGL', 'META',  'MSFT', 'NVDA', 'TSLA']
start_date = '2014-01-01'
end_date = '2024-04-01'

data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']

rtns = data.pct_change().dropna()

mean_rtns = rtns.mean()
cov_mtx = rtns.cov()

def port_vol(wts):
    return np.sqrt(np.dot(wts.T, np.dot(cov_mtx, wts)))


init_wts = np.array(len(tickers) * [1. / len(tickers),])

opts = minimize(port_vol, init_wts, method='SLSQP', bounds=bounds, constraints=consts)

opt_wts = opts.x
for ticker, weight in zip(tickers, opt_wts):
    print(f"{ticker}: {weight:.3f}")
