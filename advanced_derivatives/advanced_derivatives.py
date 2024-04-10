import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Paramete
S0 = 100  # Initial price
T = 14.0  # Time to maturity
mu = 0.15  # Expected return
sigma = 0.15  # Volatility
dt = 0.02  # Time step
N = int(T / dt)  # Number of time steps
simulations = 1000  # Number of simulations

def simulate_gbm(S0, mu, sigma, dt, N, sim):
    dt = T/N
    t = np.linspace(0, T, N)
    W = np.random.standard_normal(size=(N, sim))
    W = np.cumsum(W, axis=0) * np.sqrt(dt)  # Brownian motion
    # Ensure t is broadcastable with W
    t = t.reshape(-1, 1)  # Reshape t to be a 2D column vector
    X = (mu - 0.5 * sigma**2) * t + sigma * W 
    S = S0 * np.exp(X)  # GBM formula
    return S

# Simulate asset prices
S = simulate_gbm(S0, mu, sigma, dt, N, sim)

# Plot the first 15 simulations
plt.figure(figsize=(15,9))
plt.plot(S[:, :15])
plt.title('Simulated GBM Asset Price Paths')
plt.xlabel('Time Steps')
plt.ylabel('Asset Price')
plt.show()
