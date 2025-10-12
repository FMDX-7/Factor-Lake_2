import pandas as pd
from supabase import create_client, Client

class MarketObject:
    def __init__(self, data, t, verbosity=1):
        """
        data (DataFrame): Market data with columns like 'Ticker', 'Ending Price', etc.
        t (int): Year of market data.
        verbosity (int): Controls verbosity
        """
        # Remove duplicate columns & whitespace
        data.columns = data.columns.str.strip()
        data = data.loc[:, ~data.columns.duplicated(keep='first')]

        # Ensure 'Ticker' and 'Year' columns
        if 'Ticker' not in data.columns and 'Ticker-Region' in data.columns:
            data['Ticker'] = data['Ticker-Region'].str.split('-').str[0].str.strip()
        if 'Year' not in data.columns and 'Date' in data.columns:
            data['Year'] = pd.to_datetime(data['Date']).dt.year

        # Set index for fast lookup
        data.set_index('Ticker', inplace=True)
        self.stocks = data
        self.t = t
        self.verbosity = verbosity

    def get_price(self, ticker):
        try:
            return self.stocks.at[ticker, 'Ending Price']
        except KeyError:
            if self.verbosity >= 2:
                print(f"{ticker} not found in market data for {self.t}")
            return None

    # Optional: helper to fetch all market data from Supabase
    def fetch_market_data(supabase_url, supabase_key):
        supabase: Client = create_client(supabase_url, supabase_key)
        response = supabase.table("All").select("*").execute()
        df = pd.DataFrame(response.data)
    
        # Ensure 'Date' and 'Ticker'
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df['Year'] = df['Date'].dt.year
        if 'Ticker' not in df.columns and 'Ticker-Region' in df.columns:
            df['Ticker'] = df['Ticker-Region'].str.split('-').str[0].str.strip()
            return df
