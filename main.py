from market_object import MarketObject
from calculate_holdings import rebalance_portfolio
from user_input import get_factors 
from verbosity_options import get_verbosity_level
from fossil_fuel_restriction import get_fossil_fuel_restriction
from Visualizations.portfolio_growth_plot import plot_portfolio_growth

def main(supabase_url, supabase_key):
    # Ask user if they want fossil fuel exclusion
    restrict_fossil_fuels = get_fossil_fuel_restriction()

    # Load data
    rdata = MarketObject.load_data(supabase_url, supabase_key)

    # Optional filtering
    if restrict_fossil_fuels and 'FactSet Industry' in rdata.columns:
        excluded = ["Integrated Oil","Oilfield Services/Equipment","Oil & Gas Production"]
        rdata = rdata[~rdata['FactSet Industry'].isin(excluded)]

    # Factor selection
    available_factors = [
        'ROE using 9/30 Data', 'ROA using 9/30 Data', '12-Mo Momentum %', '6-Mo Momentum %',
        '1-Mo Momentum %', 'Price to Book Using 9/30 Data', 'Next FY Earns/P', '1-Yr Price Vol %',
        'Accruals/Assets', 'ROA %', '1-Yr Asset Growth %', '1-Yr CapEX Growth %', 'Book/Price',
        "Next-Year's Return %", "Next-Year's Active Return %"
    ]
    factors = get_factors(available_factors)
    factor_objs, factor_names = zip(*factors) if factors else ([], [])

    verbosity = get_verbosity_level()

    # Rebalance portfolio
    results = rebalance_portfolio(
        rdata, list(factor_objs),
        start_year=2002, end_year=2023,
        initial_aum=1,
        verbosity=verbosity,
        restrict_fossil_fuels=restrict_fossil_fuels
    )

    # Plot results
    plot_portfolio_growth(
        years=results['years'],
        portfolio_values=results['portfolio_values'],
        selected_factors=list(factor_names),
        restrict_fossil_fuels=restrict_fossil_fuels
    )
