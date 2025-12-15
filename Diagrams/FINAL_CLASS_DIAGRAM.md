# Class Diagram: Factor-Lake Architecture

## Overview
This diagram shows the key classes and their relationships in the Factor-Lake system, illustrating how components interact to deliver portfolio analysis functionality.

---

## Core Classes

### 1. Market Class
**File:** `src/market_object.py`

```
┌───────────────────────────────────────────────────┐
│              Market                               │
├───────────────────────────────────────────────────┤
│ Attributes:                                       │
│  - data: DataFrame                                │
│    └─ Columns: Ticker, Date, Price, Factors      │
│  - cache: Dict[str, DataFrame]                    │
│    └─ Caches frequently accessed tickers          │
│  - supabase_client: SupabaseClient                │
│    └─ Database connection                         │
│  - last_refresh: datetime                         │
│    └─ Timestamp of last data load                 │
├───────────────────────────────────────────────────┤
│ Methods:                                          │
│  + load_data(date_range, use_supabase) → None    │
│    └─ Load historical market data from DB/API    │
│  + get_price(ticker, date) → float               │
│    └─ Return stock price on specific date        │
│  + get_factor(factor_name, date) → Series       │
│    └─ Return factor scores for all tickers       │
│  + get_all_tickers() → List[str]                 │
│    └─ Return list of ~2,000 Russell 2000 tickers│
│  + validate_data() → bool                        │
│    └─ Check for missing/anomalous data           │
│  + cache_ticker(ticker) → None                   │
│    └─ Pre-load ticker data into memory cache     │
└───────────────────────────────────────────────────┘
```

**Responsibilities:**
- Unified access point for historical market data
- Performance optimization through caching
- Data validation and error handling
- Connection to Supabase backend

---

### 2. Factor Base Class (Abstract)
**File:** `src/factor_function.py`

```
┌───────────────────────────────────────────────────┐
│         <<abstract>> Factor                        │
├───────────────────────────────────────────────────┤
│ Attributes:                                       │
│  - name: str                                      │
│    └─ e.g., "ROE", "Momentum6m", "Value"         │
│  - lookback_window: int                           │
│    └─ Historical period for calculation (months)  │
│  - scores: Dict[str, float]                       │
│    └─ Factor score for each security              │
├───────────────────────────────────────────────────┤
│ Methods:                                          │
│  + calculate(market: Market) → Series             │
│    └─ Compute factor scores (abstract)            │
│  + rank_securities() → List[str]                  │
│    └─ Sort by factor strength (best to worst)     │
│  + normalize_scores(min, max) → None              │
│    └─ Scale scores to 0–1 range for comparison    │
│  + validate_scores() → bool                       │
│    └─ Check for NaN, outliers, data quality       │
└───────────────────────────────────────────────────┘
```

**Concrete Implementations:**

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Momentum6m   │  │     ROE      │  │    Value     │
├──────────────┤  ├──────────────┤  ├──────────────┤
│ lookback: 6  │  │ lookback: 12 │  │ lookback: 12 │
│ calculate(): │  │ calculate(): │  │ calculate(): │
│  (P[t] -     │  │  Net Inc /   │  │  P/E inverse │
│   P[t-6m])   │  │  Equity      │  │  (low PE =   │
│              │  │              │  │   value)     │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

### 3. Portfolio Class
**File:** `src/portfolio.py`

```
┌───────────────────────────────────────────────────────────┐
│              Portfolio                                    │
├───────────────────────────────────────────────────────────┤
│ Attributes:                                               │
│  - name: str                                              │
│    └─ e.g., "Top-N ROE Portfolio", "Russell 2000"        │
│  - date: datetime                                         │
│    └─ Rebalancing date                                    │
│  - holdings: List[Dict]                                   │
│    └─ [{ticker: "AAPL", shares: 100, price: 150}, ...]   │
│  - weights: Dict[str, float]                              │
│    └─ {ticker: 0.05, ...}  (sum = 1.0)                   │
│  - returns_history: List[float]                           │
│    └─ [0.02, -0.01, 0.05, ...]  (monthly returns)        │
│  - sector_allocation: Dict[str, float]                    │
│    └─ {Technology: 0.30, Healthcare: 0.25, ...}          │
├───────────────────────────────────────────────────────────┤
│ Methods:                                                  │
│  + add_investment(ticker, shares) → None                 │
│    └─ Add security to portfolio                           │
│  + remove_investment(ticker) → None                       │
│    └─ Remove security from portfolio                      │
│  + set_weight(ticker, weight) → None                      │
│    └─ Set portfolio weight for security                   │
│  + present_value(prices: Dict) → float                    │
│    └─ Calculate current portfolio market value            │
│  + calculate_return(t1_value, t2_value) → float           │
│    └─ Compute period return (%)                           │
│  + get_volatility() → float                               │
│    └─ Calculate annualized volatility from returns        │
│  + get_sharpe_ratio(risk_free_rate=0.02) → float         │
│    └─ Calculate Sharpe ratio                              │
│  + get_sortino_ratio(risk_free_rate=0.02) → float        │
│    └─ Calculate Sortino ratio (downside risk only)        │
│  + get_max_drawdown() → float                             │
│    └─ Calculate max cumulative loss                       │
│  + get_sector_exposure() → Dict                           │
│    └─ Return sector allocation                            │
└───────────────────────────────────────────────────────────┘
```

**Relationships:**
- Aggregates multiple Investment objects (composition)
- References Market for pricing (association)

---

### 4. CalculateHoldings Class (Portfolio Constructor)
**File:** `src/calculate_holdings.py`

```
┌──────────────────────────────────────────────────────────┐
│          CalculateHoldings                               │
├──────────────────────────────────────────────────────────┤
│ Attributes:                                              │
│  - market: Market                                        │
│  - factors: List[Factor]                                │
│  - constraints: Dict                                     │
│    └─ {esg_restricted: [...], sectors: [...]}            │
│  - weighting_scheme: str                                 │
│    └─ "equal" or "cap-weighted"                          │
│  - n_long: int                                           │
│    └─ Number of top securities (e.g., 100)               │
│  - n_short: int                                          │
│    └─ Number of bottom securities (e.g., 100)            │
├──────────────────────────────────────────────────────────┤
│ Methods:                                                 │
│  + rebalance_portfolio(date) → Portfolio                 │
│    └─ Generate portfolio for specific month              │
│  + rank_securities(date) → Series                        │
│    └─ Composite factor score rank all ~2,000 tickers    │
│  + apply_constraints(rankings) → Series                  │
│    └─ Remove ESG-excluded & sector-filtered securities   │
│  + construct_top_n(rankings, n) → Portfolio              │
│    └─ Create long portfolio (top N ranked)               │
│  + construct_bottom_n(rankings, n) → Portfolio           │
│    └─ Create short portfolio (bottom N ranked)           │
│  + assign_weights(portfolio) → None                      │
│    └─ Equal-weight or cap-weight securities              │
│  + backtest(start_date, end_date) → List[Portfolio]      │
│    └─ Run monthly rebalancing over period                │
└──────────────────────────────────────────────────────────┘
```

**Key Processes:**
1. **Rank Securities:** Composite score = weighted average of normalized factor scores
2. **Apply Constraints:** Remove restricted tickers; filter by sector
3. **Select Holdings:** Top-N and Bottom-N after constraints
4. **Assign Weights:** Distribute capital across selected securities

---

### 5. SupabaseClient Class
**File:** `src/supabase_client.py`

```
┌──────────────────────────────────────────────────────┐
│          SupabaseClient                              │
├──────────────────────────────────────────────────────┤
│ Attributes:                                          │
│  - url: str                                          │
│    └─ Supabase project URL                           │
│  - api_key: str                                      │
│    └─ Authentication token                           │
│  - db: Connection                                    │
│    └─ Active database connection                     │
│  - connection_pool: Pool                             │
│    └─ Connection pooling for performance             │
├──────────────────────────────────────────────────────┤
│ Methods:                                             │
│  + connect() → bool                                  │
│    └─ Establish database connection                  │
│  + fetch_market_data(ticker, start, end) → DataFrame │
│    └─ Query historical prices                        │
│  + fetch_all_factors(date) → DataFrame               │
│    └─ Query factor scores for all securities         │
│  + fetch_sector_map() → Dict                         │
│    └─ Get ticker-to-sector mapping                   │
│  + fetch_esg_restrictions() → List[str]              │
│    └─ Get list of ESG-restricted tickers             │
│  + log_portfolio_decision(portfolio, timestamp)      │
│    └─ Write audit trail entry                        │
│  + cache_data(key, value, ttl=3600) → None           │
│    └─ Store in Redis for quick retrieval              │
│  + get_cached(key) → Optional[Any]                   │
│    └─ Retrieve from cache if available                │
│  + close() → None                                    │
│    └─ Close database connection                      │
└──────────────────────────────────────────────────────┘
```

**Database Tables:**
- `market_data(ticker, date, open, high, low, close, volume)`
- `factors(ticker, date, factor_name, score)`
- `sectors(ticker, sector)`
- `esg_restrictions(ticker, restriction_type, restriction_date)`
- `portfolio_audit_log(portfolio_id, timestamp, user_id, action, result)`

---

### 6. StreamlitApp Class (UI Controller)
**File:** `streamlit_app.py`

```
┌────────────────────────────────────────────────────┐
│         StreamlitApp                               │
├────────────────────────────────────────────────────┤
│ Attributes:                                        │
│  - market: Market                                  │
│  - portfolio_engine: CalculateHoldings             │
│  - session_state: Dict                             │
│    └─ Persistent user selections across reruns     │
│  - available_factors: List[str]                    │
│  - available_sectors: List[str]                    │
├────────────────────────────────────────────────────┤
│ Methods:                                           │
│  + render_sidebar() → Dict                         │
│    └─ Display factor/sector/ESG selectors          │
│  + render_main_panel() → None                      │
│    └─ Display metrics & charts                     │
│  + handle_backtest_click() → None                  │
│    └─ Button click: trigger backtest               │
│  + display_metrics(portfolio) → None               │
│    └─ Show return, vol, Sharpe, IR, etc.           │
│  + plot_growth(portfolios) → None                  │
│    └─ Dollar-invested line chart                   │
│  + plot_sector_exposure(portfolio) → None          │
│    └─ Sector allocation bar chart                  │
│  + export_csv(portfolio) → bytes                   │
│    └─ Generate downloadable CSV                    │
│  + run() → None                                    │
│    └─ Main loop (Streamlit reruns on each input)   │
└────────────────────────────────────────────────────┘
```

---

## Relationships & Interactions

### Composition (Strong Ownership)
```
Portfolio              contains            Investment
   │◆─────────────────────────────────┘ (1..*)
   │
   └─ A portfolio owns its holdings
   └─ If portfolio deleted, holdings discarded
```

### Aggregation (Weak Ownership)
```
CalculateHoldings       uses             Market
   │◇─────────────────────────────────┘ (1..*)
   │
   └─ Portfolio engine references market
   └─ Market can exist independently
```

### Dependency (Temporary Use)
```
StreamlitApp            invokes           CalculateHoldings
   │┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅ (calls methods)
   │
   └─ UI depends on portfolio engine
   └─ Calls backtest() to generate results
```

### Association (Collaboration)
```
Factor                  calculates      Market
   │──────────────────────────────────┘ (reads from)
   │
   └─ Factor needs market data to compute scores
```

---

## Class Interaction Flow: Running a Backtest

```
1. User Input (StreamlitApp)
   └─ Selects: ROE, Momentum6m, ESG Filter ON
   └─ Calls: portfolio_engine.backtest(start="2002-01", end="2025-12")

2. CalculateHoldings.backtest()
   └─ For each month from 2002-01 to 2025-12:
      ├─ 2.1. Load Market Data
      │       └─ market.load_data(date)
      │       └─ Calls supabase_client.fetch_market_data()
      │       └─ Returns DataFrame with prices & factors
      ├─ 2.2. Calculate Factors
      │       └─ roe_factor.calculate(market)
      │       └─ momentum_factor.calculate(market)
      │       └─ Returns Series with factor scores
      ├─ 2.3. Rank Securities
      │       └─ Composite score = avg(normalize(ROE), normalize(Momentum))
      │       └─ Sort all ~2,000 tickers
      ├─ 2.4. Apply Constraints
      │       └─ supabase_client.fetch_esg_restrictions()
      │       └─ Remove fossil fuel stocks
      ├─ 2.5. Construct Portfolios
      │       └─ Top-100: best ranked securities
      │       └─ Bottom-100: worst ranked securities
      │       └─ Index-2000: Russell 2000 (all)
      ├─ 2.6. Assign Weights
      │       └─ equal_weight = 1 / len(holdings)
      │       └─ cap_weight = market_cap / sum(all market_caps)
      └─ 2.7. Store Portfolio
          └─ portfolio.returns_history.append(monthly_return)

3. Calculate Metrics
   └─ portfolio.get_volatility()
   └─ portfolio.get_sharpe_ratio()
   └─ portfolio.get_information_ratio()
   └─ Accumulate 276 monthly portfolios (2002–2025)

4. Return Results
   └─ List of 3 Portfolio objects (Top-N, Bottom-N, Index)
   └─ Each with 276 monthly returns & metrics

5. Display (StreamlitApp)
   └─ render_metrics(portfolios)
   └─ plot_growth(portfolios)
   └─ export_csv(portfolios)
```

---

## Data Flow Between Classes

### Market Data Flow
```
Supabase Database
    │
    ▼ (query: fetch_market_data, fetch_all_factors)
SupabaseClient
    │ (parse results, apply caching)
    ▼
Market (DataFrame: Ticker, Date, Price, Factor1, Factor2, ...)
    │ (provide methods: get_price, get_factor)
    ▼ (call: calculate(market))
Factor (compute scores)
    │ (return: Series with scores)
    ▼
CalculateHoldings (rank, filter, weight)
    │ (return: Portfolio with holdings)
    ▼
Portfolio (calculate metrics)
    │ (return: metrics Dict)
    ▼
StreamlitApp (display & export)
```

---

## Testing & Verification Points

| Class | Unit Test | Integration Test |
|-------|-----------|-----------------|
| Market | Load sample data; validate cache | Query Supabase; compare to Yahoo Finance |
| Factor | Calculate known-good values; edge cases | Multiple factors on same market data |
| Portfolio | Add/remove holdings; calculate returns | Full backtest pipeline |
| CalculateHoldings | Rank, filter, weight functions | Backtest vs manual calculation |
| SupabaseClient | Mock queries; error handling | Real database connection; transaction rollback |
| StreamlitApp | Sidebar rendering; button clicks | UAT with portfolio managers |

---

## Extensibility & Future Enhancements

### Adding a New Factor
1. Create subclass of Factor (e.g., `class Dividend(Factor)`)
2. Implement `calculate(market) → Series` method
3. Register in `streamlit_app.py` available_factors list
4. Unit test the new factor
5. Deploy (CI/CD automatically tests)

### Adding a New Constraint
1. Add constraint method to CalculateHoldings (e.g., `apply_dividend_yield_filter()`)
2. Call in `apply_constraints()` pipeline
3. Add Streamlit widget (checkbox or slider)
4. Test & deploy

### Supporting Additional Data Sources
1. Add method to SupabaseClient (e.g., `fetch_from_alpha_vantage()`)
2. Normalize to same DataFrame format
3. Add configuration option in streamlit_app.py
4. Fallback strategy if primary source unavailable

