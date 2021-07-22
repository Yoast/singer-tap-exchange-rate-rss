import pandas as pd
import feedparser
from datetime import date
from pandas.io.json import json_normalize


url = 'https://www.ecb.europa.eu/rss/fxref-usd.html'
todays_date = date.today()

try:
    usd_feed = feedparser.parse(url)

    df_usd_feed = json_normalize(usd_feed.entries)

    keep_cols = ['id', 'cb_exchangerate']

    # Drop unwanted columns
    usd_cleaned = df_usd_feed[keep_cols]

    # Format the date columns
    usd_cleaned['Data_Date'] = usd_cleaned['id'].str.extract(r'(\d{4}-\d{2}-\d{2})')
    usd_cleaned['Data_Date'] = pd.to_datetime(usd_cleaned['Data_Date'])
    usd_cleaned['Retrieval_Date'] = todays_date

    # Script grabs the last 5 days, so drop everything that isn't today's date.
    drop_index = usd_cleaned[usd_cleaned['Data_Date'] != usd_cleaned['Retrieval_Date']].index
    usd_cleaned.drop(drop_index, inplace=True)

    # Split the exchange rate from the currency
    temp_values = usd_cleaned['cb_exchangerate'][0].split()

    # Convert exchange_rate to float, grab the currency
    exchange_rate = float(temp_values[0])
    currency = temp_values[1]

    # Add to dataframe
    usd_cleaned['Exchange_Rate'] = exchange_rate
    usd_cleaned['Currency'] = currency

    usd_cleaned.drop(['cb_exchangerate'], axis=1, inplace=True)
    usd_cleaned.reset_index(drop=True)

    # print(temp_values)
    # print(todays_date)
    # print(exchange_rate)

except:
    print('Something went wrong!')

# NOTE: The RSS feed doesn't appear to be updated on Saturday/Sunday.
