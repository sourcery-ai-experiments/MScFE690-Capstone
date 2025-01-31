from dataapi import FredAPI
import matplotlib.pyplot as plt

# Initialize the FRED API
fred_api = FredAPI()

# Define series IDs and their corresponding names
series_mapping = {'INDPRO': 'Industrial Production',
                  'CPILFESL': 'CPI Core Index'}

# Fetch data for the specified series
data_frame = fred_api.fetch_series(series_mapping)

# Plot the data
data_frame.plot()
plt.show()
