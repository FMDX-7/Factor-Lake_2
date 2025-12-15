# SYSEN 5900 Final Report: Factor Lake
## A Factor Portfolio Software for the Cayuga Fund

---

## 1. Analysis of Context

### Problem Statement
The Cayuga Fund, a campus quantitative finance organization, required a software system to generate and analyze factor-based portfolios. Portfolio managers needed tools to:
- Isolate drivers of return through factor decomposition
- Calculate risk-adjusted performance metrics (Information Ratio, Sharpe ratio, Sortino ratio)
- Benchmark strategies against the Russell 2000
- Gain intuition about factor exposures and effectiveness
- Reduce manual analysis time and improve decision-making speed

### Stakeholder Analysis
**Primary Stakeholders:**
- Portfolio Managers (Cayuga Fund members): Need intuitive factor selection, quick backtests, performance visualization
- Quantitative Analysts: Require transparent calculations, customizable factors, reproducible results
- Fund Leadership: Demand scalable infrastructure, secure data handling, professional presentation

**Secondary Stakeholders:**
- Academic Advisor: Requires adherence to systems engineering principles
- IT Infrastructure: Campus servers and cloud resources
- External Data Providers: Yahoo Finance, Morningstar, internal databases

### Contextual Constraints
1. **Technical Infrastructure:** Campus network, limited IT support, preference for cloud solutions
2. **Data Availability:** Historical market data from 2002–2023, Russell 2000 universe (~2,000 securities)
3. **Operational Context:** Weekly fund meetings, monthly rebalancing cycles
4. **Regulatory/Compliance:** Secure data handling, audit trails for portfolio decisions
5. **Development Resources:** Small team (~2–3 developers), 2-semester timeline

### Development Philosophy: MVP and Agile Scrum
From the outset, the team adopted:
- **MVP (Minimum Viable Product)** thinking to validate assumptions early with portfolio managers
- **Agile Scrum** with weekly sprints, story points, demos, and retrospectives
- **INVEST Principles** to ensure user stories remained independent, negotiable, valuable, estimable, small, and testable
- **Continuous Integration** using Git and automated testing to catch regressions early

This approach allowed the team to build iteratively, gather early feedback, and pivot quickly when needed—a hallmark of systems engineering applied to software development.

---

## 2. Well-Defined Requirements

### Requirements Framework
Following systems engineering best practices, requirements are expressed as verifiable "shall" statements and traced to user stories. Each requirement includes:
- **Unique ID** for traceability
- **Shall Statement** for clarity and measurability
- **Verification Method** (test, inspection, demonstration, analysis)
- **Acceptance Criteria** for sign-off

### Functional Requirements

#### F1: Factor Portfolio Generation
- **F1.1** The system shall accept user selection of 1–13 investment factors from a predefined list
- **F1.2** The system shall generate equal-weighted or cap-weighted portfolios based on factor rankings
- **F1.3** The system shall construct portfolios from the Russell 2000 security universe
- **F1.4** The system shall rebalance portfolios monthly with data sourced from the current date back to 2002
- **Verification:** Automated unit tests validate portfolio construction; backtests compare results to manual calculations

#### F2: Portfolio Analysis and Metrics
- **F2.1** The system shall calculate annualized return, volatility, max drawdown, and Sharpe/Sortino ratios
- **F2.2** The system shall compute the Information Ratio to measure risk-adjusted excess return vs. Russell 2000
- **F2.3** The system shall provide dollar-invested charts comparing top-N, bottom-N, and benchmark portfolios
- **F2.4** The system shall display sector exposure and factor loading analysis
- **Verification:** Backtests compare outputs to industry-standard financial calculators (pandas, NumPy, scipy)

#### F3: Environmental, Social, and Governance (ESG) Filtering
- **F3.1** The system shall allow users to exclude fossil fuel companies from portfolio construction
- **F3.2** The system shall maintain a persistent list of restricted tickers
- **F3.3** The system shall apply fossil fuel filters during annual rebalancing
- **Verification:** Integration tests confirm restricted securities are excluded from generated portfolios

#### F4: Sector Filtering
- **F4.1** The system shall allow users to filter portfolios by sector (e.g., Technology, Healthcare, Financials)
- **F4.2** The system shall maintain a mapping of securities to sectors
- **F4.3** The system shall apply sector filters during portfolio generation
- **Verification:** Integration tests verify portfolio compositions respect sector selections

#### F5: Data Management
- **F5.1** The system shall provide a database interface to retrieve historical market data
- **F5.2** The system shall support data ingestion from multiple sources (Excel, Yahoo Finance, Supabase)
- **F5.3** The system shall cache frequently accessed data to reduce query latency
- **F5.4** The system shall enforce secure access controls via authentication tokens
- **Verification:** Integration tests validate query responses; performance benchmarks confirm <5-second retrieve times

### Non-Functional Requirements

#### Performance (NF1)
- **NF1.1** The system shall execute a complete backtest for up to 13 factors in <30 seconds
- **NF1.2** The system shall retrieve market data for 2,000+ securities in <5 seconds
- **NF1.3** The system shall render interactive visualizations in <2 seconds
- **Verification:** Load testing with production-scale data; performance profiling of critical paths

#### Usability (NF2)
- **NF2.1** Portfolio managers shall be able to select factors, run a backtest, and view results in <5 minutes
- **NF2.2** The UI shall display all critical information on a single screen or require <3 clicks to access advanced analytics
- **NF2.3** The system shall provide clear error messages for invalid inputs or data unavailability
- **Verification:** User acceptance testing (UAT) with portfolio managers; usability heuristics evaluation

#### Reliability (NF3)
- **NF3.1** The system shall maintain 99% uptime during operational hours (Mon–Fri, 8 AM–6 PM)
- **NF3.2** The system shall recover from network interruptions with transparent user notification
- **NF3.3** The system shall validate all market data for consistency and flag anomalies
- **Verification:** Uptime monitoring; automated restart procedures; data quality dashboards

#### Security (NF4)
- **NF4.1** The system shall encrypt all data in transit (HTTPS/TLS 1.2+)
- **NF4.2** The system shall authenticate users via secure credentials stored in Supabase
- **NF4.3** The system shall maintain an audit log of all portfolio decisions and data access
- **NF4.4** The system shall comply with FERPA (Family Educational Rights and Privacy Act) for student data
- **Verification:** Security audit; penetration testing; compliance checklist review

#### Maintainability (NF5)
- **NF5.1** The system codebase shall maintain code coverage >80% for all critical modules
- **NF5.2** All public functions shall be documented with docstrings and type hints
- **NF5.3** The system shall support modular deployment of independent components
- **Verification:** Static code analysis (Pylint, Bandit); code review checklists

---

## 3. Functional Definitions

Functional definitions describe **what** the system does—the alternative behaviors and capabilities that satisfy requirements.

### Evolution Through MVP Iterations

#### Iteration 1: Skateboard (First Semester MVP)
**Scope:** Validate core calculation engine  
**Functionality:**
- Single hardcoded factor (e.g., ROE)
- Basic Information Ratio calculation (later found to be inaccurate)
- Manual Excel-based data input
- Colab-based execution

**Outcome:** Confirmed that factor-based portfolio generation was feasible; identified need for multiple factors and improved accuracy.

#### Iteration 2: Scooter (First Semester Enhancement)
**Scope:** Add factor diversity and user control  
**Functionality:**
- Support for all 13 factors with user selection
- Refined Information Ratio calculation aligned with industry standards
- Colab UI with checkboxes for factor selection
- Verbosity levels (basic, intermediate, advanced outputs)
- GitHub-based code distribution for reproducibility

**Outcome:** Portfolio managers could experiment with factor combinations; identified need for persistent data storage and better UI/UX.

#### Iteration 3: Bicycle (First Semester Final)
**Scope:** Modularize codebase for collaboration  
**Functionality:**
- Separated concerns: market data loading, factor calculation, portfolio rebalancing, analysis
- Git repository for version control and team collaboration
- Enhanced visualization: basic performance charts
- Documented modules and function interfaces

**Outcome:** Reduced development friction; enabled parallel development; ready for UI/database upgrade.

#### Iteration 4: Motorcycle (Second Semester—Current)
**Scope:** Professional application with scalable backend  
**Functionality:**

**User Interface Layer:**
- Streamlit web application replacing Colab notebooks
- Interactive sidebar for factor, sector, and ESG filter selection
- Real-time portfolio metrics and performance charts
- Export-to-CSV functionality for downstream analysis
- Responsive design supporting desktop and tablet browsers

**Data Management Layer:**
- Supabase PostgreSQL backend replacing Excel sheets
- Automatic data synchronization from external sources
- Query optimization with caching for frequently accessed tickers
- Secure authentication for user access

**Analytics Engine:**
- Expanded metrics: annualized return, volatility, max drawdown, Sharpe ratio, Sortino ratio, Information Ratio
- Dollar-invested charts comparing top-N, bottom-N, and index portfolios (key discovery feature)
- Sector exposure breakdown
- Factor contribution analysis (which factors drove returns?)

**Robustness Enhancements:**
- Automated error handling and data validation
- Performance optimization: reduced runtime from 2:40 to <40 seconds for all 15 factors
- Regression testing to catch anomalies in portfolio construction logic

**Outcome:** Matured from prototype to production-ready application; portfolio managers now deploy weekly with confidence.

---

## 4. Structural Definitions

Structural definitions describe **how** the system realizes the functional capabilities through hardware, software, and procedural choices.

### Architecture Evolution

#### Early Phase: Monolithic Colab Notebooks
**Structure:**
- Single-file Python notebook with all logic (data loading, factor calculation, analysis)
- Hardcoded factor definitions
- Manual Excel file uploads
- Limited code reuse

**Trade-offs:** ✅ Fast to prototype, ❌ Hard to maintain, ❌ Difficult to collaborate

#### Intermediate Phase: Modular GitHub Repository
**Structure:**
- Separation of concerns into modules:
  - `market_object.py`: Market data loading and caching
  - `factor_function.py`: Factor calculation implementations
  - `portfolio.py`: Portfolio class and rebalancing logic
  - `calculate_holdings.py`: Portfolio construction and weighting
  - `user_input.py`: Prompts and user interaction
- Colab notebook pulls code from GitHub via `!pip install git+https://github.com/...`

**Trade-offs:** ✅ Improved maintainability, ✅ Easier collaboration via Git, ❌ Still limited to Colab UI

#### Current Phase: Full-Stack Web Application
**Structure:**

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│              Streamlit Web Application                       │
│  (Frontend: Python + HTML/CSS/JS, hosted on Streamlit Cloud)│
└────────────┬────────────────────────────────────────────────┘
             │ HTTP/REST API calls
┌────────────▼────────────────────────────────────────────────┐
│                  Business Logic Layer                       │
│         Python Application Server (Streamlit App)           │
│  ├─ Portfolio Generation Engine                             │
│  ├─ Factor Calculation Module                               │
│  ├─ Risk Analytics Module                                   │
│  └─ ESG/Sector Filtering Module                             │
└────────────┬────────────────────────────────────────────────┘
             │ SQL Queries
┌────────────▼────────────────────────────────────────────────┐
│                    Data Layer                               │
│             Supabase PostgreSQL Database                    │
│  ├─ Market Data (tickers, prices, factors)                  │
│  ├─ Portfolio Histories (backtesting records)               │
│  └─ User Sessions & Preferences                             │
└─────────────────────────────────────────────────────────────┘
```

**Technology Choices:**

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Frontend | Streamlit | Python-native, rapid development, built-in widgets for user input, zero JavaScript needed |
| Backend | Python 3.9+ | Statistical libraries (pandas, NumPy, scipy), existing codebase, team expertise |
| Database | Supabase (PostgreSQL) | Cloud-hosted (campus IT-friendly), scalable, free tier supports student projects, strong Python driver (psycopg2) |
| Deployment | Streamlit Cloud | Automatic scaling, GitHub integration for CI/CD, no infrastructure management |
| Version Control | Git + GitHub | Industry standard, enables pull requests, code review, CI/CD pipelines |
| Testing | pytest + pytest-cov | Python standard, integrates with CI/CD, tracks coverage |

### Module Breakdown

#### Market Object (`market_object.py`)
- **Responsibility:** Load, cache, and provide uniform access to market data
- **Inputs:** Ticker list, date range, data source preference (Supabase or Yahoo Finance)
- **Outputs:** DataFrame with OHLC prices and calculated factors
- **Structure:** Single `Market` class with methods:
  - `load_data()`: Fetch from database or API
  - `get_price(ticker, date)`: Point query with caching
  - `get_factor(factor_name)`: Return pre-calculated factor values

#### Factor Functions (`factor_function.py`)
- **Responsibility:** Implement factor calculation logic
- **Structure:** Separate function for each factor (e.g., `Momentum6m()`, `ROE()`)
- **Inputs:** Market DataFrame, lookback window
- **Outputs:** Factor DataFrame with scores for each security

#### Portfolio (`portfolio.py`)
- **Responsibility:** Represent a portfolio and calculate performance metrics
- **Structure:** Class with properties (holdings, weights) and methods:
  - `add_investment()`: Include a security with given shares
  - `calculate_return()`: Compute total return over period
  - `present_value()`: Calculate current market value

#### Calculate Holdings (`calculate_holdings.py`)
- **Responsibility:** Construct factor-based portfolios via ranking and weighting
- **Inputs:** Factor scores, weighting scheme (equal or cap-weighted), constraints (ESG, sector)
- **Process:**
  1. Rank securities by factor score
  2. Apply sector/ESG filters
  3. Assign weights (1/N or market-cap-weighted)
  4. Calculate rebalancing trades
- **Outputs:** Portfolio object ready for performance calculation

#### User Input & Streamlit App (`streamlit_app.py`, `user_input.py`)
- **Responsibility:** Provide intuitive interface for portfolio manager interactions
- **Streamlit Components:**
  - Sidebar: Factor selector (checkboxes), weighting scheme (radio buttons)
  - Main area: Performance metrics (cards), charts (line graphs, bar charts)
  - Export: CSV download button for raw results

#### Supabase Integration (`supabase_client.py`)
- **Responsibility:** Manage database connections, queries, and authentication
- **Methods:**
  - `fetch_market_data()`: Query historical prices
  - `fetch_factors()`: Retrieve pre-computed factor scores
  - `log_portfolio_decision()`: Audit trail entry

### Data Flow Diagram

```
User Input (Streamlit UI)
    │
    ├─ Selected Factors: [ROE, Momentum6m, Value]
    ├─ Weighting: Equal-Weighted
    ├─ ESG Filter: Exclude Fossil Fuels
    └─ Sector Filter: [Tech, Healthcare]
         │
         ▼
Load Market Data (market_object.py)
    ├─ Query Supabase for historical prices (2002–2025)
    ├─ Query Supabase for pre-computed factors
    └─ Cache results locally for fast access
         │
         ▼
Calculate Factors (factor_function.py)
    ├─ ROE = Net Income / Shareholder Equity
    ├─ Momentum6m = (Price[t] - Price[t-6m]) / Price[t-6m]
    └─ Value = P/E ratio (inverse)
         │
         ▼
Rank & Filter Securities (calculate_holdings.py)
    ├─ Rank all ~2,000 securities by composite factor score
    ├─ Remove restricted sectors & ESG exclusions
    └─ Select top-N and bottom-N for analysis
         │
         ▼
Construct Portfolios (portfolio.py)
    ├─ Top-N Portfolio: Long positions in top-ranked securities
    ├─ Bottom-N Portfolio: Short positions in lowest-ranked securities
    └─ Index Portfolio: Russell 2000 benchmark
         │
         ▼
Backtest & Calculate Metrics
    ├─ Historical rebalancing (monthly, 2002–2025)
    ├─ Calculate returns, volatility, Sharpe ratio, etc.
    └─ Generate dollar-invested graph
         │
         ▼
Display Results (Streamlit UI)
    ├─ Performance cards: Return, Volatility, Sharpe, Info Ratio
    ├─ Charts: Growth plot, sector exposure, factor contribution
    └─ Export: CSV download option
```

---

## 5. Analysis and Optimization

### Optimization Across Two Semesters

#### Semester 1: Computational Efficiency
**Problem:** Backtesting all 13 factors took 2 minutes 40 seconds per run.

**Root Cause Analysis:**
- Inefficient ticker indexing in `market_object.py`
- Repeated data lookups for same securities
- No caching between factor calculations

**Solution:**
- Refactored market data to use pandas `.loc[]` instead of `.iterrows()`
- Implemented in-memory caching with memoization
- Optimized factor calculation vectorization

**Result:** ✅ Runtime reduced to <40 seconds (>75% improvement)

**Verification:** Automated performance benchmarks track execution time per sprint

---

#### Semester 2: Data Accuracy & Feature Effectiveness

**Problem:** Dollar-invested graph for top-N, bottom-N portfolios revealed anomalies:
- Portfolio values diverged unexpectedly from theoretical expectations
- Factor rankings appeared unstable month-to-month

**Root Cause Analysis (Iterative Debugging):**
1. **Discovery:** Generated dollar-invested graph showed counter-intuitive patterns
2. **Investigation:** Compared manually calculated vs. system-generated portfolios
3. **Root Cause:** Inconsistent handling of missing data (NaN values) during factor calculation
4. **Secondary Issue:** Rebalancing logic wasn't properly accounting for survived vs. new positions

**Solution (Multi-Phase Fix):**
1. Enhanced data validation: Flag securities with missing factor data
2. Refined rebalancing: Distinguish between held, sold, and new positions
3. Added anomaly detection: Alert if portfolio diverges >5% from expected trajectory
4. Increased test coverage: Added 15+ regression tests to catch similar issues

**Result:** 
- ✅ Portfolio calculations now align with manual verification
- ✅ Dollar-invested graph provides accurate intuition about factor effectiveness
- ✅ Portfolio managers report higher confidence in results

**Verification:** Integration tests compare system output to independently calculated benchmarks

---

### Trade-off Analysis: Key Decisions

#### 1. Streamlit vs. Flask/Django
| Criterion | Streamlit | Flask | Django |
|-----------|-----------|-------|--------|
| **Development Speed** | Fastest (no HTML/CSS) | Moderate (need templates) | Slower (heavy framework) |
| **Learning Curve** | Minimal (Python-only) | Moderate | Steep |
| **Customization** | Limited CSS | Full control | Full control |
| **Hosting Simplicity** | Streamlit Cloud (1-click) | Heroku/AWS (more setup) | Heroku/AWS (more setup) |
| **Team Expertise** | ✅ (Python-focused) | ❌ (Web dev needed) | ❌ (Web dev needed) |

**Decision:** Streamlit ✅ → Prioritized rapid prototyping and portfolio manager feedback

---

#### 2. Supabase vs. Excel vs. Yahoo Finance
| Criterion | Supabase | Excel | Yahoo Finance API |
|-----------|----------|-------|-------------------|
| **Scalability** | Excellent (cloud DB) | Poor (single file) | Limited (API rate limits) |
| **Concurrent Access** | Yes (multiple users) | No (lock conflicts) | Rate-limited |
| **Data Consistency** | Strong (ACID) | Weak (manual sync) | Real-time only |
| **Security** | Enterprise (encryption, auth) | None (shared file) | Token-based (limited) |
| **Cost** | Free tier (adequate) | Free | Free with limits |
| **Backup/Recovery** | Automatic | Manual | N/A (ephemeral) |

**Decision:** Supabase ✅ → Provides production-grade reliability for minimal cost; Excel still used for manual data entry/verification

---

#### 3. Equal-Weighted vs. Cap-Weighted Factor Portfolios
| Aspect | Equal-Weighted | Cap-Weighted |
|--------|-----------------|--------------|
| **Simplicity** | ✅ Easy to explain & replicate | ❌ Complex weighting logic |
| **Factor Purity** | ✅ Pure factor exposure | ❌ Dominated by large-cap stocks |
| **Rebalancing Cost** | ❌ High (frequent rebalancing) | ✅ Lower (large caps stable) |
| **Real-World Implementation** | ❌ Difficult for actual trading | ✅ Practical & industry-standard |
| **Academic Validity** | ✅ Standard in research | ✅ Industry practice |

**Decision:** Support both ✅ → Allow portfolio managers to experiment; equal-weighted for academic rigor, cap-weighted for practical deployment

---

### Risk Mitigation Through Optimization

| Risk | Mitigation | Evidence |
|------|-----------|----------|
| Performance degradation | Automated load testing after each sprint | Benchmarks logged in CI/CD pipeline |
| Data corruption | Supabase automatic backups + validation layer | Weekly backup verification tests |
| Factor calculation errors | 15+ regression tests + manual spot-checks | Test coverage >85% |
| Unauthorized access | Supabase role-based access control (RBAC) + audit logs | Compliance checklist |
| User frustration with slow UI | Pre-calculated dashboards cached at midnight | Response time <2 seconds measured |

---

## 6. Implementation, Testing, and Development

### Agile Scrum Framework

#### Sprint Structure (1-week cycles)
1. **Monday: Sprint Planning**
   - Refinement of user stories from product backlog
   - Estimation using Scrum Poker
   - Commitment to sprint goal

2. **Tuesday–Thursday: Development**
   - Daily standups (5 min): "What did I do yesterday? What will I do today? Any blockers?"
   - Pair programming for high-risk tasks (e.g., database migrations)
   - Continuous integration: Every commit triggers automated tests

3. **Friday: Sprint Review & Retrospective**
   - Demo to stakeholders (portfolio managers, advisor)
   - Retrospective: "What went well? What could we improve?"
   - Backlog refinement for next sprint

#### Sample Sprint Goals (Semester 2)
| Sprint | Goal | Key User Stories | Outcome |
|--------|------|------------------|---------|
| Sprint 1 | Streamlit MVP | UI for factor selection, basic backtest | Portfolio managers can run backtests |
| Sprint 2 | Supabase Integration | Database schema, data ingestion | Data persists beyond session; query latency <5s |
| Sprint 3 | Dollar-Invested Graph | New visualization, bug discovery | Anomalies identified & investigated |
| Sprint 4 | Performance Optimization | Runtime improvement, caching | <40 seconds for all 13 factors |
| Sprint 5 | ESG/Sector Filters | Feature implementation & testing | Portfolio managers exclude fossil fuels |
| Sprint 6 | Documentation & Testing | Code coverage, docstrings, UML diagrams | Maintainability & knowledge transfer |

---

### Testing Strategy

#### Unit Tests (`UnitTests/` directory)
- **Coverage:** >85% of all critical modules
- **Framework:** pytest
- **Example Test:** `test_factor_function.py`
  - Tests each factor calculation against known-good values
  - Validates edge cases (missing data, extreme values)
  - Ensures numerical precision (within 0.01% of expected)

#### Integration Tests
- **Focus:** Component interactions (factor calc → portfolio construction → backtesting)
- **Example:** `test_portfolio_backtest.py`
  - Runs full backtest pipeline on sample data
  - Compares results to manually calculated portfolio
  - Validates output CSV format

#### Regression Tests
- **Purpose:** Detect unintended changes from updates
- **Approach:** Golden dataset with pre-computed results; flag if results differ by >1%
- **Frequency:** Automated on every Git commit (CI/CD)

#### System/Acceptance Tests
- **Method:** Portfolio managers run live backtests with their own factor selections
- **Acceptance Criteria:**
  - Results match expectations (e.g., "Tech factor should have high Tech exposure")
  - UI is intuitive (<5 minutes to run a backtest)
  - Export functionality works (CSV downloads)

#### Performance Tests
- **Benchmarks:**
  - Backtest time: <30 seconds for all 13 factors
  - Query latency: <5 seconds for 2,000 tickers
  - UI response time: <2 seconds after button click
- **Tracking:** Results logged in `performance_log.csv` after each sprint

---

### Version Control & CI/CD

#### Git Workflow
```
main (production)
 ├─ feature/streamlit-ui (Feature Branch)
 │  ├─ Commits: Implementation, bug fixes, code review
 │  └─ Pull Request: Code review by peer, automated tests
 └─ hotfix/data-validation (Hotfix Branch)
    └─ Merged to main after critical bug discovery
```

**Branching Rules:**
- Feature branches must pass all tests before PR
- Pull requests require ≥1 peer review approval
- Merges to `main` trigger deployment to Streamlit Cloud

#### CI/CD Pipeline (GitHub Actions)
```yaml
name: Factor-Lake CI/CD

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run unit tests
        run: pytest UnitTests/ -v --cov=src
      - name: Lint with Pylint
        run: pylint src/ --fail-under=7.0
      - name: Security check with Bandit
        run: bandit -r src/ -f sarif -o bandit-report.sarif
      - name: Deploy to Streamlit Cloud
        if: github.ref == 'refs/heads/main'
        run: streamlit deploy
```

**Pipeline Stages:**
1. **Checkout code** from GitHub
2. **Run unit tests** with coverage reporting
3. **Lint** with Pylint (code quality threshold: 7.0+)
4. **Security scan** with Bandit (identify vulnerabilities)
5. **Deploy** to Streamlit Cloud if all checks pass

---

### Collaboration Tools & Practices

#### Communication
- **Standups:** Daily 5-minute sync (async Slack updates if needed)
- **Design Reviews:** Weekly discussion of architecture decisions
- **Code Reviews:** GitHub PR reviews with constructive feedback
- **Documentation:** Shared Google Doc for meeting notes; Wiki for technical docs

#### Issue Tracking
- **GitHub Issues:** Bugs, feature requests, documentation gaps
- **Labels:** `bug`, `enhancement`, `documentation`, `tech-debt`, `blocked`
- **Prioritization:** P0 (blocking), P1 (high), P2 (medium), P3 (low)

#### Knowledge Sharing
- **Docstrings:** All public functions documented with inputs, outputs, examples
- **Type Hints:** Python 3.9+ type annotations for IDE support
- **Architecture Docs:** UML diagrams, data flow diagrams, deployment diagram
- **README.md:** Quick-start guide, feature overview, contribution guidelines

---

### MVP and Early Feedback Loop

#### Semester 1: "Skating" to Validate Concept
**Minimum Viable Product:**
- Single factor (ROE) backtester
- Colab notebook interface
- Information Ratio output

**Feedback from Portfolio Managers:**
- ❌ "Information Ratio numbers seem wrong"
- ❌ "Can't easily try different factors"
- ✅ "Concept is valuable; faster iteration on factors"

**Action Taken:** Refactored IR calculation; added user-selectable factors

---

#### Semester 2: "Biking" to Improve UX
**Enhanced MVP:**
- 13 factors, Streamlit UI, Supabase backend
- Interactive charts, export functionality

**Feedback:**
- ❌ "Dollar-invested graph shows weird patterns"
- ✅ "This is much easier to use than Colab"
- ✅ "We can now test factor combinations quickly"

**Action Taken:**
- Debugged portfolio calculation anomalies
- Added data validation layer
- Expanded analytics to include risk metrics (Sortino, max drawdown)

**Result:** System evolved from academic prototype to practical decision-support tool

---

## 7. System Evolution: Diagrams

### Use-Case Diagram
```
                          ┌─────────────────┐
                          │  Portfolio Mgr  │
                          └────────┬────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
            ┌──────────────┐ ┌────────────┐ ┌──────────────┐
            │ Select       │ │ Run        │ │ View         │
            │ Factors      │ │ Backtest   │ │ Results      │
            └──────────────┘ └────────────┘ └──────────────┘
                    │              │              │
                    └──────────────┼──────────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │ Factor-Lake     │
                          │ System          │
                          └────────┬────────┘
                                   │
                    ┌──────────────┼──────────────┬───────────────┐
                    │              │              │               │
                    ▼              ▼              ▼               ▼
            ┌──────────────┐ ┌────────────┐ ┌──────────┐ ┌──────────────┐
            │ Calculate    │ │ Filter     │ │ Query    │ │ Generate     │
            │ Factors      │ │ ESG/Sector │ │ Database │ │ Visualization
            └──────────────┘ └────────────┘ └──────────┘ └──────────────┘
                    │              │              │               │
                    └──────────────┼──────────────┴───────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
            ┌───────────────────┐       ┌─────────────────┐
            │ Supabase          │       │ Streamlit       │
            │ PostgreSQL DB     │       │ Web App         │
            └───────────────────┘       └─────────────────┘
```

---

### Class Diagram (Simplified)
```
┌─────────────────────────────┐
│         Market              │
├─────────────────────────────┤
│ - data: DataFrame           │
│ - cache: Dict               │
├─────────────────────────────┤
│ + load_data(...)            │
│ + get_price(ticker, date)   │
│ + get_factor(factor_name)   │
└────────────┬────────────────┘
             │ 1
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌──────────────┐  ┌──────────────────┐
│  Portfolio   │  │  Factor          │
├──────────────┤  ├──────────────────┤
│ - name       │  │ - name: str      │
│ - holdings[] │  │ - scores: Dict   │
├──────────────┤  ├──────────────────┤
│ + add_inv()  │  │ + calculate()    │
│ + calc_ret() │  │ + rank_secur()   │
└──────────────┘  └──────────────────┘
     │ many       │ many
     │            │
     └────────┬───┘
              │
              ▼
    ┌──────────────────────┐
    │  CalculateHoldings   │
    ├──────────────────────┤
    │ + rebalance_port()   │
    │ + apply_filters()    │
    │ + weight_portfolio() │
    └──────────────────────┘
```

---

### Deployment Diagram
```
┌────────────────────────────────────────────────────────────┐
│                       Internet                             │
└────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────┐
        │    Streamlit Cloud (SaaS)         │
        │  ┌─────────────────────────────┐  │
        │  │ Streamlit App Container     │  │
        │  │  - Python runtime           │  │
        │  │  - streamlit_app.py         │  │
        │  │  - /src modules             │  │
        │  └──────────────┬──────────────┘  │
        │                 │                 │
        │         (HTTPS/REST API)          │
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                          ▼
        ┌───────────────────────────────────┐
        │      Supabase (Cloud DB)          │
        │  ┌─────────────────────────────┐  │
        │  │  PostgreSQL Database        │  │
        │  │  - market_data table        │  │
        │  │  - factors table            │  │
        │  │  - audit_logs table         │  │
        │  └─────────────────────────────┘  │
        │  ┌─────────────────────────────┐  │
        │  │  Authentication (JWT)       │  │
        │  └─────────────────────────────┘  │
        └───────────────────────────────────┘
```

---

### Data Pipeline Activity Diagram
```
         Start
           │
           ▼
    ┌─────────────┐
    │ User selects│
    │ factors in  │
    │ Streamlit   │
    └──────┬──────┘
           │
           ▼
    ┌─────────────────────┐
    │ Load market data    │
    │ from Supabase       │
    │ (cached if recent)  │
    └──────┬──────────────┘
           │
           ▼
    ┌──────────────────────┐
    │ Calculate factor     │
    │ scores for all       │
    │ securities           │
    └──────┬───────────────┘
           │
           ▼
    ┌──────────────────────┐
    │ Apply ESG/sector     │
    │ filters              │
    └──────┬───────────────┘
           │
           ▼
    ┌──────────────────────┐
    │ Rank securities by   │
    │ composite score      │
    └──────┬───────────────┘
           │
           ▼
    ┌──────────────────────┐
    │ Construct top-N and  │
    │ bottom-N portfolios  │
    └──────┬───────────────┘
           │
           ▼
    ┌──────────────────────┐
    │ Backtest monthly     │
    │ rebalancing (2002–   │
    │ 2025)                │
    └──────┬───────────────┘
           │
           ▼
    ┌──────────────────────┐
    │ Calculate returns,   │
    │ volatility, Sharpe,  │
    │ IR, etc.             │
    └──────┬───────────────┘
           │
           ▼
    ┌──────────────────────┐
    │ Generate chart data  │
    │ (dollar-invested,    │
    │ sector exposure)     │
    └──────┬───────────────┘
           │
           ▼
    ┌──────────────────────┐
    │ Render Streamlit     │
    │ dashboard with       │
    │ results & export     │
    │ option               │
    └──────┬───────────────┘
           │
           ▼
         End
```

---

### System Engineering Process (SYSEN 5100 Tailoring)
```
┌─────────────────────────────────────────────────────────────┐
│          Systems Engineering V-Model Applied to Factor-Lake   │
└─────────────────────────────────────────────────────────────┘

    Requirements              Development              Testing
    (Left Side)              (Center)              (Right Side)

          │
    1. Context Analysis
    ├─ Stakeholders
    ├─ Constraints              
    └─ MVP Philosophy
          │
          ▼
    2. Requirements        
    ├─ Functional (F1–F5)       
    ├─ Non-Functional (NF1–NF5)
    └─ INVEST Principles
          │
          ▼
    3. Functional Defs        Sprint Planning
    ├─ Skateboard            ├─ Week 1–2: MVP
    ├─ Scooter               ├─ Week 3–4: UI/DB
    ├─ Bicycle               ├─ Week 5–6: Analytics
    └─ Motorcycle            └─ Week 7–8: Polish
          │                           │
          │                           ▼
          │                   4. Structural Defs
          │                   ├─ Modular code
          │                   ├─ Streamlit + Supabase
          │                   ├─ CI/CD pipeline
          │                   └─ Deployment
          │                           │
          │                           ▼
          │                   5. Implementation
          │                   ├─ Code development
          │                   ├─ Git commits
          │                   ├─ Peer review
          │                   └─ Merge to main
          │                           │
          └───────────────────────────┼────────────────────┐
                                      │                    │
                                      ▼                    ▼
                                  6. Testing          7. Validation
                                  ├─ Unit tests       ├─ UAT with
                                  ├─ Integration      │  portfolio mgrs
                                  ├─ Regression       ├─ Performance
                                  └─ System tests     │  benchmarks
                                      │              └─ Acceptance
                                      │
                                      ▼
                                 8. Release
                                 ├─ Deploy to
                                 │  Streamlit Cloud
                                 ├─ Notify team
                                 └─ Monitor metrics
                                      │
                                      ▼
                                 9. Iterate
                                 ├─ Gather feedback
                                 ├─ Backlog refinement
                                 └─ Next sprint
```

---

## Summary: From Prototype to Production

**Semester 1:** Built the foundation (skateboard → scooter → bicycle)
- Validated factor-based portfolio generation concept
- Established Agile Scrum workflow
- Achieved 75% performance optimization

**Semester 2:** Matured to production-ready application (motorcycle)
- Transitioned from Colab to Streamlit web app
- Integrated Supabase for scalable data management
- Discovered and fixed data accuracy issues via dollar-invested graph
- Expanded analytics with risk metrics and sector analysis
- Implemented comprehensive testing and CI/CD pipelines

**Key Systems Engineering Principles Applied:**
1. ✅ MVP thinking for early feedback and risk reduction
2. ✅ Tradeoff analysis (Streamlit vs. Flask, Supabase vs. Excel)
3. ✅ Requirements-driven development (functional vs. structural)
4. ✅ Iterative refinement (V-model adapted for Agile)
5. ✅ Cross-team collaboration (Git, code review, documentation)
6. ✅ Testing & validation at every stage (unit, integration, system, UAT)

**Result:** Portfolio managers now deploy Factor-Lake weekly with confidence, supporting data-driven investment decisions for the Cayuga Fund.

---

## References

- Systems Engineering Handbook, INCOSE (applied V-model and requirements framework)
- Henrik Kniberg, "Making Sense of MVP" (MVP framework: skateboard → motorcycle)
- Agile Scrum Guide (sprint structure, ceremonies, INVEST principles)
- Python Best Practices (PEP 8, type hints, docstrings)
- PostgreSQL Documentation (Supabase database design)

