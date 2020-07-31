from nsepy import get_history
from datetime import date
import pandas as pd

# List of Stocks/Symbols you are interested in.
df_ticks = pd.read_csv("Nifty500_list.csv")
out_df = pd.read_csv("out.csv")

# DEFINE/SET these based on the 'mode' days observed per ticker.
# Ensure headers added!
days = 23


ticker_len = df_ticks.index.stop
i = 0
cell_pos = 0

# If failure displayed, there are missing days of ticker/entire Ticker missing!

while True:
    if i >= ticker_len:
        break
    cur = i * days
    max = (i+1) * days
    fail = 0
    while cur < max:
        if df_ticks['Ticker'][i] != out_df['Ticker'][cur]:
            print("FAILED:", df_ticks['Ticker'][i], out_df['Ticker'][cur])
            fail = 1
            break
        cur += 1
    if fail == 1:
        print("failed location:", cur)
        break
    i += 1
