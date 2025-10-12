import pandas as pd
from supabase import create_client, Client

class MarketObject():
    def __init__(self, data: pd.DataFrame = None, year: int = None, verbosity=1):
        """
        data: DataFrame of market data
        year: Year of market data
        verbosity: 0 = silent, 1 = normal, 2+ = verbose
        """
        if data is None:
            raise ValueError("Data must be provided. Use fetch_from_supabase() to get it directly from the database.")

        # Remove duplicate columns and strip names
        data.columns = data.columns.str.strip()
        data = data.loc[:, ~data.columns.duplicated(keep='first')]

        # Ensure 'Ticker' and 'Year' columns
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

        # Clean data
        self.stocks.replace({'--': None}, inplace=True)
        self.stocks.set_index('Ticker', inplace=True)

        self.year = year
        self.verbosity = verbosity

    @staticmethod
    def fetch_from_supabase(supabase_url: str, supabase_key: str):
        """Fetch entire All table from Supabase as a DataFrame."""
        supabase: Client = create_client(supabase_url, supabase_key)
        result = supabase.table("All").select("*").execute()
        if result.data is None:
            raise ValueError("No data returned from Supabase")
        return pd.DataFrame(result.data)
