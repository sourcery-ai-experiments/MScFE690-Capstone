import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Parameter
S0 = 100  # Initial price
T = 14.0  # Time to maturity
mu = 0.15  # Expected return
sigma = 0.15  # Volatility
dt = 0.02  # Time step
N = int(T / dt)  # Number of time steps
sim = 1000  # Number of simulations

def simulate_gbm(S0, mu, sigma, dt, N, sim):
    dt = T/N
    t = np.linspace(0, T, N)
    W = np.random.standard_normal(size=(N, sim))
    W = np.cumsum(W, axis=0) * np.sqrt(dt)  # Brownian motion
    # Ensure t is broadcastable with W
    t = t.reshape(-1, 1)  # Reshape t to be a 2D column vector
    X = (mu - 0.5 * sigma**2) * t + sigma * W 
    S = S0 * np.exp(X)  
    return S

# Simulate stocks prices
S = simulate_gbm(S0, mu, sigma, dt, N, sim)

# Plot the first 15 simulations
plt.figure(figsize=(15,9))
plt.plot(S[:, :15])
plt.title('Simulated GBM stock Price Paths')
plt.xlabel('Time Steps')
plt.ylabel('Stock Price')
plt.show()


# Assuming all assets have the same initial price and parameters for simplicity
asset_returns = np.log(S[1:] / S[:-1])
mean_returns = asset_returns.mean(axis=0)
cov_matrix = np.cov(asset_returns.T)

# Portfolio optimization: Minimize volatility
from scipy.optimize import minimize

num_assets = simulations
weights = np.array(num_assets * [1. / num_assets,])

def portfolio_volatility(weights, mean_returns, cov_matrix):
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

def check_sum(weights):
    return np.sum(weights) - 1

constraints = ({'type': 'eq', 'fun': check_sum})
bounds = tuple((0, 1) for asset in range(num_assets))

opts = minimize(portfolio_volatility, weights, args=(mean_returns, cov_matrix), method='SLSQP', bounds=bounds, constraints=constraints)

# Print optimized weights
print(f"Optimized Weights: {opts.x}")


import yfinance as yf
import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Define tickers and the historical period
tickers = ['AAPL', 'MSFT', 'GOOGL', 'META', 'TSLA', 'AMZN', 'NVDA']
start_date = '2010-01-01'
end_date = '2024-04-01'

# Fetch historical data
data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']

# Display the first few rows
print(data.head())


# Calculate daily returns
returns = data.pct_change().dropna()

# Display the first few rows of returns
print(returns.head())

# Calculate expected returns and the covariance matrix
mean_returns = returns.mean()
cov_matrix = returns.cov()

# Define the optimization problem
def portfolio_volatility(weights):
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

def check_sum(weights):
    # The weights must sum up to 1.
    return np.sum(weights) - 1

# Constraints and bounds
constraints = ({'type': 'eq', 'fun': check_sum})
bounds = tuple((0, 1) for _ in range(len(tickers)))
initial_weights = np.array(len(tickers) * [1. / len(tickers),])

# Optimize
opts = minimize(portfolio_volatility, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)

# Display optimized weights
optimized_weights = opts.x
for ticker, weight in zip(tickers, optimized_weights):
    print(f"{ticker}: {weight:.3f}")
