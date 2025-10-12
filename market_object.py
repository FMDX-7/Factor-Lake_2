import pandas as pd
from supabase import create_client, Client
import os

# Supabase credentials
SUPABASE_URL = "https://xyzcompany.supabase.co"
SUPABASE_KEY = "your-public-anon-key"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_data(restrict_fossil_fuels=False):
    """
    Load market data from Supabase 'All' table and optionally filter fossil fuel industries.
    Returns a pandas DataFrame with all required columns.
    """
    # Fetch all rows from 'All'
    response = supabase.table("All").select("*").execute()

    if response.error:
        raise Exception(f"Supabase query failed: {response.error}")

    rdata = pd.DataFrame(response.data)

    # Ensure correct column names
    rdata.columns = rdata.columns.str.strip()
    rdata = rdata.loc[:, ~rdata.columns.duplicated()]

    # Add 'Ticker' column if missing
    if 'Ticker' not in rdata.columns and 'Ticker-Region' in rdata.columns:
        rdata['Ticker'] = rdata['Ticker-Region'].str.split('-').str[0].str.strip()

    # Convert 'Date' to datetime & extract 'Year'
    if 'Date' in rdata.columns:
        rdata['Date'] = pd.to_datetime(rdata['Date'])
        rdata['Year'] = rdata['Date'].dt.year

    # Fossil fuel filtering
    if restrict_fossil_fuels and 'FactSet Industry' in rdata.columns:
        fossil_keywords = ['oil', 'gas', 'coal', 'energy', 'fossil']
        rdata = rdata[rdata['FactSet Industry'].apply(lambda x: not any(kw in str(x).lower() for kw in fossil_keywords))]

    return rdata


class MarketObject:
    """
    Wraps a pandas DataFrame from Supabase to provide ticker/year-based lookups.
    """
    def __init__(self, data: pd.DataFrame, t: int, verbosity=1):
        data.columns = data.columns.str.strip()
        data = data.loc[:, ~data.columns.duplicated(keep='first')]

        # Ensure Ticker and Year columns exist
        if 'Ticker' not in data.columns and 'Ticker-Region' in data.columns:
            data['Ticker'] = data['Ticker-Region'].str.split('-').str[0].str.strip()
        if 'Year' not in data.columns and 'Date' in data.columns:
            data['Year'] = pd.to_datetime(data['Date']).dt.year

        # Keep only relevant columns
        available_factors = [
            'ROE using 9/30 Data', 'ROA using 9/30 Data', '12-Mo Momentum %', '1-Mo Momentum %',
            'Price to Book Using 9/30 Data', 'Next FY Earns/P', '1-Yr Price Vol %', 'Accruals/Assets',
            'ROA %', '1-Yr Asset Growth %', '1-Yr CapEX Growth %', 'Book/Price',
            "Next-Year's Return %", "Next-Year's Active Return %"
        ]
        keep_cols = ['Ticker', 'Ending Price', 'Year', '6-Mo Momentum %'] + available_factors
        data = data[[col for col in keep_cols if col in data.columns]].copy()
        data.replace({'--': None}, inplace=True)

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
                print(f"{ticker} - not found in market data for {self.t} - SKIPPING")
            return None
