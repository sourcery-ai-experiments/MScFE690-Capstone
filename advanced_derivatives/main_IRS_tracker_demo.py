from trackers import FwdIRSTrackers
import pandas as pd
import matplotlib.pyplot as plt

# Initialize the Forward Interest Rate Swap (FwdIRSTrackers) tracker
irs_tracker = FwdIRSTrackers(currency='USD', tenor=10)

# Retrieve the tracker DataFrame
tracker_data = irs_tracker.get_tracker_data()

# Plot the tracker data
tracker_data.plot()
plt.show()
