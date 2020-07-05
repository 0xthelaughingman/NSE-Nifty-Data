from nsepy import get_history
from datetime import date
import pandas as pd

# List of Stocks/Symbols you are interested in.
df_ticks = pd.read_csv("Nifty500_list.csv")

for ticker_ind in df_ticks.index:
    print(df_ticks['Ticker'][ticker_ind])
    stock_df = get_history(symbol=df_ticks['Ticker'][ticker_ind], start=date(2020, 6, 1), end=date(2020, 6, 30))

    # Clear Excess Columns, one might have different requirements. Read the NSEpy's docs.
    stock_df.drop(stock_df.iloc[:, 1:5], inplace=True, axis=1)
    stock_df.drop(stock_df.iloc[:, 4:10], inplace=True, axis=1)
    stock_df.drop(['Low', 'Last'], inplace=True, axis=1)

    # Compute Returns for each day, taking base cost as the Closing price of first day
    # + Adding fields from the csv/list if any.
    Returns = []
    Sectors = []
    MarketCaps = []
    day1_close = 0
    counter = 0
    for ind in stock_df.index:
        if counter == 0:
            day1_close = stock_df['Close'][ind]
        cur_return = (stock_df['Close'][ind] - day1_close) / day1_close * 100
        Returns.append(cur_return)
        MarketCaps.append(df_ticks['MarketCap'][ticker_ind])
        Sectors.append(df_ticks['Sector'][ticker_ind])
        counter += 1
    stock_df['Return'] = Returns
    stock_df['MarketCap'] = MarketCaps
    stock_df['Sector'] = Sectors
    stock_df.rename(columns={'Symbol': 'Ticker'}, inplace=True)

    # Outputting with headers(Column names) as false, otherwise
    # we'll have row entries with column names for each Stock/Symbol
    stock_df.to_csv('out.csv', header=False, index=True, date_format="%d-%m-%Y", mode="a")
