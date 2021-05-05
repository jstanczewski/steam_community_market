import pickle
import pandas as pd
import numpy as np

desired_width = 620
pd.set_option("display.width", desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option("display.max_columns", 20)

with open("730_price_data.pkl", "rb") as f:
    print(pickle.load(f).to_string())
