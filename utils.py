import requests
import pandas as pd
import numpy as np


def get_daily_data(AV_API_KEY, from_symbol, to_symbol='USD'):
    resp = requests.get('https://www.alphavantage.co/query', params={
        'function': 'DIGITAL_CURRENCY_DAILY',
        'symbol': from_symbol,
        'market': to_symbol,
        'apikey': AV_API_KEY
    })

    resp.raise_for_status()
    doc = resp.json()
    if 'Error Message' in doc:
        raise ValueError(doc['Error Message'])
    
    df = pd.DataFrame.from_dict(doc['Time Series (Digital Currency Daily)'], orient='index', dtype=np.float)
    df.drop(columns=[c for c in df.columns.values if 'b.' in c], inplace=True)
    df.reset_index(inplace=True)
    df['index'] = pd.to_datetime(df['index'])
    df.set_index('index', inplace=True)
    
    return df
    
    