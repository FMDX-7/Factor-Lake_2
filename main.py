# main_supabase.py
import pandas as pd
from calculate_holdings import rebalance_portfolio
from user_input import get_factors
from verbosity_options import get_verbosity_level
from fossil_fuel_restriction import get_fossil_fuel_restriction
from Visualizations.portfolio_growth_plot import plot_portfolio_growth
from market_object import MarketObject

# ===============================
# Supabase settings
# ===============================
SUPABASE_URL = "https://ozusfgnnzanaxpcfidbm.supabase.co"
SUPABASE_KEY = "sb_publishable_PyVKM3BdygFWVdeZrirAVA_AxZFyNAA"

def main(year=2023):
    # ===============================
    # STEP 1: Ask about fossil fuel restriction
    # ===============================
    restrict_fossil_fuels = get_fossil_fuel_restriction()  # Prompt user (Yes/No)

    # ===============================
    # STEP 2: Fetch data from Supabase
    # ===============================
    market_df = MarketObject.fetch_from_supabase(SUPABASE_URL, SUPABASE_KEY)
    market = MarketObject(market_df, year=year, verbosity=1)

    # ===============================
    # STEP 3: Optional fossil fuel filtering
    # ===============================
    if restrict_fossil_fuels:
        excluded_industries = [
            "Integrated Oil",
            "Oilfield Services/Equipment",
            "Oil & Gas Production"
        ]
        if 'FactSet Industry' in market.stocks.columns:
            original_len = len(market.stocks)
            market.stocks = market.stocks[~market.stocks['FactSet Industry'].isin(excluded_industries)]
            print(f"Filtered out {original_len - len(market.stocks)} fossil fuel-related companies.")

    # ===============================
    # STEP 4: Define available factors
    # ===============================
    available_factors = [
        'ROE using 9/30 Data', 'ROA using 9/30 Data', '12-Mo Momentum %',
        '6-Mo Momentum %', '1-Mo Momentum %', 'Price to Book Using 9/30 Data',
        'Next FY Earns/P', '1-Yr Price Vol %', 'Accruals/Assets', 'ROA %',
        '1-Yr Asset Growth %', '1-Yr CapEX Growth %', 'Book/Price',
        "Next-Year's Return %", "Next-Year's Active Return %"
    ]
    # Ensure only columns that exist in Supabase data are kept
    market_data = market.stocks[['Ending Price', 'Year'] + [f for f in available_factors if f in market.stocks.columns]].copy()

    # ===============================
    # STEP 5: User selects factors & verbosity
    # ===============================
    factors = get_factors(available_factors)
    verbosity_level = get_verbosity_level()
    factor_objects, factor_names = (zip(*factors) if factors else ([], []))

    # ===============================
    # STEP 6: Rebalance portfolio
    # ===============================
    print("\nRebalancing portfolio...")
    results = rebalance_portfolio(
        market_data,
        list(factor_objects),
        start_year=2002,
        end_year=2023,
        initial_aum=1,
        verbosity=verbosity_level,
        restrict_fossil_fuels=restrict_fossil_fuels
    )

    # ===============================
    # STEP 7: Plot results
    # ===============================
    plot_portfolio_growth(
        years=results['years'],
        portfolio_values=results['portfolio_values'],
        selected_factors=list(factor_names),
        restrict_fossil_fuels=restrict_fossil_fuels
    )

    print("Done!")

# Entry point
if __name__ == "__main__":
    main()
