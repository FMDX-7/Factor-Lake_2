import pandas as pd
from supabase import create_client, Client
import os

class MarketObject:
    def __init__(self, data: pd.DataFrame, year: int = None, verbosity=1):
        self.year = year
        self.verbosity = verbosity

        # Clean columns and ensure 'Ticker' & 'Year'
        data.columns = data.columns.str.strip()
        data = data.loc[:, ~data.columns.duplicated(keep='first')]
        if 'Ticker' not in data.columns and 'Ticker-Region' in data.columns:
            data['Ticker'] = data['Ticker-Region'].str.split('-').str[0].str.strip()
        if 'Year' not in data.columns and 'Date' in data.columns:
            data['Year'] = pd.to_datetime(data['Date']).dt.year

        # Keep relevant columns
        available_factors = [
            'ROE using 9/30 Data', 'ROA using 9/30 Data', '12-Mo Momentum %', '1-Mo Momentum %',
            'Price to Book Using 9/30 Data', 'Next FY Earns/P', '1-Yr Price Vol %', 'Accruals/Assets',
            'ROA %', '1-Yr Asset Growth %', '1-Yr CapEX Growth %', 'Book/Price',
            "Next-Year's Return %", "Next-Year's Active Return %"
        ]
        keep_cols = ['Ticker', 'Ending Price', 'Year', '6-Mo Momentum %'] + available_factors
        self.stocks = data[[col for col in keep_cols if col in data.columns]].copy()
        self.stocks.replace({'--': None}, inplace=True)
        self.stocks.set_index('Ticker', inplace=True)

    @staticmethod
    def load_data(supabase_url: str = None, supabase_key: str = None):
        """
        Pulls the 'All' table from Supabase. If no keys provided, raises an error.
        """
        if supabase_url is None or supabase_key is None:
            raise ValueError("Supabase URL and KEY must be provided")
        client: Client = create_client(supabase_url, supabase_key)
        result = client.table("All").select("*").execute()
        if not result.data:
            raise ValueError("No data returned from Supabase")
        df = pd.DataFrame(result.data)

        # Process columns
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df['Year'] = df['Date'].dt.year
        if 'Ticker' not in df.columns and 'Ticker-Region' in df.columns:
            df['Ticker'] = df['Ticker-Region'].str.split('-').str[0].str.strip()

        return df
        
    def get_price(self, ticker):
        try:
            return self.stocks.at[ticker, 'Ending Price']
        except KeyError:
            if self.verbosity >= 2:
                print(f"{ticker} - not found in market data for {self.t} - SKIPPING")
            return None
