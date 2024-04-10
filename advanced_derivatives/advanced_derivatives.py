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

num_assets = simulations
weights = np.array(num_assets * [1. / num_assets,])

def portfolio_vol(weights, mean_returns, cov_matrix):
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

def check_sum(weights):
    return np.sum(weights) - 1

consts = ({'type': 'eq', 'fun': check_sum})
bounds = tuple((0, 1) for asset in range(num_assets))

opts = minimize(portfolio_vol, weights, args=(mean_returns, cov_matrix), method='SLSQP', bounds=bounds, consts=consts)

print(f"Optimized Weights: {opts.x}")

tickers = ['AAPL', 'AMZN', 'GOOGL', 'META',  'MSFT', 'NVDA', 'TSLA']
start_date = '2014-01-01'
end_date = '2024-04-01'

data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']

returns = data.pct_change().dropna()

mean_returns = returns.mean()
cov_matrix = returns.cov()

def portfolio_vol(weights):
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

def check_sum(weights):
    return np.sum(weights) - 1

consts = ({'type': 'eq', 'fun': check_sum})
bounds = tuple((0, 1) for _ in range(len(tickers)))
initial_weights = np.array(len(tickers) * [1. / len(tickers),])

opts = minimize(portfolio_vol, initial_weights, method='SLSQP', bounds=bounds, consts=consts)

optimized_weights = opts.x
for ticker, weight in zip(tickers, optimized_weights):
    print(f"{ticker}: {weight:.3f}")
