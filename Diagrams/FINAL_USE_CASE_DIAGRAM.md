# Use-Case Diagram: Factor-Lake System

## Primary Actor: Portfolio Manager

### Use Cases

#### 1. Select Factors
- **Actor:** Portfolio Manager
- **Precondition:** Logged into Streamlit app
- **Main Flow:**
  1. Open factor selection sidebar
  2. Check/uncheck desired factors (ROE, Momentum, Value, etc.)
  3. Confirm selection
- **Postcondition:** Selected factors are stored in session state
- **Alternative:** "View Factor Descriptions" to understand each factor

#### 2. Choose Weighting Scheme
- **Actor:** Portfolio Manager
- **Precondition:** Factors selected
- **Main Flow:**
  1. Select weighting option: Equal-Weighted or Cap-Weighted
  2. Confirm selection
- **Postcondition:** Weighting scheme applied to portfolio construction

#### 3. Apply ESG Filters
- **Actor:** Portfolio Manager
- **Precondition:** None (optional step)
- **Main Flow:**
  1. Toggle "Exclude Fossil Fuels" checkbox
  2. System loads restricted ticker list from Supabase
- **Postcondition:** Fossil fuel companies removed from portfolio rankings

#### 4. Apply Sector Filters
- **Actor:** Portfolio Manager
- **Precondition:** None (optional step)
- **Main Flow:**
  1. Select desired sectors (Technology, Healthcare, Financials, etc.)
  2. Confirm selection
- **Postcondition:** Portfolio restricted to selected sectors

#### 5. Run Backtest
- **Actor:** Portfolio Manager
- **Precondition:** Factors selected (other options optional)
- **Main Flow:**
  1. Click "Run Backtest" button
  2. System processes:
     - Loads historical market data (2002–2025)
     - Calculates factor scores
     - Ranks securities
     - Constructs top-N, bottom-N, and index portfolios
     - Performs monthly rebalancing
     - Calculates performance metrics
  3. Display results (loading indicator shown during processing)
- **Postcondition:** Results displayed on dashboard
- **Exception:** If data unavailable, display error message with recovery options

#### 6. View Performance Metrics
- **Actor:** Portfolio Manager
- **Precondition:** Backtest completed
- **Main Flow:**
  1. Display metric cards: Annual Return, Volatility, Sharpe Ratio, Information Ratio, Max Drawdown
  2. Show comparison: Top-N vs Bottom-N vs Russell 2000
- **Postcondition:** Portfolio manager understands relative factor performance

#### 7. View Interactive Charts
- **Actor:** Portfolio Manager
- **Precondition:** Backtest completed
- **Main Flow:**
  1. Display dollar-invested line chart (2002–2025)
  2. Show sector exposure bar chart
  3. Show factor contribution stacked area chart
  4. Allow hover for tooltips
- **Postcondition:** Portfolio manager gains intuition about factor effectiveness

#### 8. Export Results to CSV
- **Actor:** Portfolio Manager
- **Precondition:** Backtest completed
- **Main Flow:**
  1. Click "Download Results" button
  2. Generate CSV with:
     - Monthly returns for each portfolio
     - Performance metrics summary
     - Sector allocations
  3. Browser downloads file
- **Postcondition:** Data available for further analysis in Excel/Python

---

## Secondary Actors & System Support Functions

### System: Market Data Loading
- **Trigger:** Run Backtest use case
- **Function:** 
  - Query Supabase for historical prices and factors
  - Cache frequently accessed tickers
  - Validate data integrity
- **Postcondition:** Market data ready for analysis

### System: Portfolio Construction Engine
- **Trigger:** Factor selection confirmed
- **Function:**
  - Rank securities by composite factor score
  - Apply constraints (ESG, sector filters)
  - Construct equal or cap-weighted portfolios
- **Postcondition:** Portfolio holdings determined

### System: Backtesting Engine
- **Trigger:** Run Backtest use case
- **Function:**
  - Monthly rebalancing from 2002–2025
  - Calculate returns, volatility, Sharpe ratio, etc.
  - Generate dollar-invested growth path
- **Postcondition:** Performance metrics calculated

### System: Data Validation Layer
- **Trigger:** Market data loaded
- **Function:**
  - Check for missing/anomalous data
  - Flag securities with insufficient history
  - Alert if portfolio diverges from expected range
- **Postcondition:** Data quality assurance before analysis

---

## Relationships Between Use Cases

```
                        ┌──────────────────────────────────┐
                        │    Portfolio Manager (Actor)     │
                        └────────────┬─────────────────────┘
                                     │
                  ┌──────────────────┼──────────────────┐
                  │                  │                  │
                  ▼                  ▼                  ▼
           ┌────────────┐     ┌────────────┐     ┌────────────┐
           │  Select    │     │  Choose    │     │  Apply     │
           │  Factors   │     │  Weighting │     │  ESG       │
           └──────┬─────┘     └──────┬─────┘     │  Filters   │
                  │                  │           └──────┬─────┘
                  │         (includes)                   │
                  └──────────────┬───────────────────────┘
                                 │
                          ┌──────▼──────┐
                          │   Apply     │
                          │   Sector    │ (optional)
                          │   Filters   │
                          └──────┬──────┘
                                 │
                          ┌──────▼──────────────┐
                          │   Run Backtest      │
                          │   (Main use case)   │
                          └──────┬──────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
          ▼                      ▼                      ▼
   ┌─────────────┐        ┌──────────────┐      ┌──────────────┐
   │   View      │        │   View       │      │   Export     │
   │   Metrics   │        │   Charts     │      │   Results    │
   └─────────────┘        └──────────────┘      └──────────────┘
```

---

## System Boundaries & External Systems

### Within System Scope (Factor-Lake):
- Factor selection UI
- Weighting scheme logic
- Portfolio ranking & construction
- Backtesting engine
- Metrics calculation
- Visualization generation
- CSV export

### Outside System Scope (External Systems):
- **Supabase Database:** Provides historical market data
- **Yahoo Finance API:** Optional external data source
- **User's Browser:** Renders Streamlit UI
- **User's Filesystem:** Receives downloaded CSV files

---

## Verification Points for Each Use Case

| Use Case | Verification Method |
|----------|-------------------|
| Select Factors | Unit test: verify factor selection logic |
| Choose Weighting | Integration test: equal vs cap-weighted portfolios |
| Apply ESG Filters | Regression test: restricted tickers not in portfolio |
| Apply Sector Filters | Integration test: portfolio composition by sector |
| Run Backtest | System test: full pipeline validation vs manual calc |
| View Metrics | UAT: portfolio managers confirm intuitive results |
| View Charts | Performance test: <2 second render time |
| Export CSV | Integration test: file format validation |

