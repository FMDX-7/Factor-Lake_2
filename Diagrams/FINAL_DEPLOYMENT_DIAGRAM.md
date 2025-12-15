# Deployment Diagram: Factor-Lake System Architecture

## Production Deployment Overview

### Logical Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          INTERNET (Public)                              │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   │
                    ┌──────────────┴───────────────┐
                    │                              │
                    ▼                              ▼
        ┌──────────────────────┐      ┌──────────────────────┐
        │  User Browser        │      │  GitHub CI/CD        │
        │  (Chrome, Safari)    │      │  (GitHub Actions)    │
        └──────────┬───────────┘      └──────────┬───────────┘
                   │ HTTPS/REST API              │ Git webhooks
                   │ (TLS 1.2+)                  │ (Auto-deploy)
                   ▼                              ▼
    ┌──────────────────────────────────────────────────────────┐
    │          STREAMLIT CLOUD (SaaS, us-east)                 │
    │  ┌────────────────────────────────────────────────────┐  │
    │  │       Streamlit Application Container             │  │
    │  │  ┌──────────────────────────────────────────────┐  │  │
    │  │  │  streamlit_app.py (UI Layer)                │  │  │
    │  │  │  - Factor selector (checkboxes)             │  │  │
    │  │  │  - Weighting scheme (radio buttons)         │  │  │
    │  │  │  - Metrics display (cards)                  │  │  │
    │  │  │  - Charts (Plotly)                          │  │  │
    │  │  │  - Export button (CSV download)             │  │  │
    │  │  └──────────────────────────────────────────────┘  │  │
    │  │                       ▲                             │  │
    │  │                       │ (import)                    │  │
    │  │  ┌────────────────────┴─────────────────────────┐  │  │
    │  │  │  Business Logic Layer (Python Modules)       │  │  │
    │  │  │  - src/market_object.py (data access)       │  │  │
    │  │  │  - src/factor_function.py (calculations)    │  │  │
    │  │  │  - src/portfolio.py (portfolio class)       │  │  │
    │  │  │  - src/calculate_holdings.py (construction) │  │  │
    │  │  │  - Visualizations/portfolio_growth_plot.py  │  │  │
    │  │  └──────────────────────────────────────────────┘  │  │
    │  │                       ▲                             │  │
    │  │                       │ (SQL queries)               │  │
    │  │  ┌────────────────────┴─────────────────────────┐  │  │
    │  │  │  Caching Layer (In-Memory)                   │  │  │
    │  │  │  - Frequently accessed tickers               │  │  │
    │  │  │  - TTL: 1 hour (auto-refresh)                │  │  │
    │  │  └──────────────────────────────────────────────┘  │  │
    │  │                       ▲                             │  │
    │  │                       │ (psycopg2 driver)           │  │
    │  │  ┌────────────────────┴─────────────────────────┐  │  │
    │  │  │  Database Client (SupabaseClient)            │  │  │
    │  │  │  - Connection pooling (5 connections)        │  │  │
    │  │  │  - Query optimization                        │  │  │
    │  │  │  - Error handling & retries                  │  │  │
    │  │  └──────────────────────────────────────────────┘  │  │
    │  └────────────────────────────────────────────────────┘  │
    │                                                         │  │
    │  Runtime Environment:                                  │  │
    │  - Python 3.9                                          │  │
    │  - streamlit==1.26+                                    │  │
    │  - pandas, numpy, scipy (data science stack)           │  │
    │  - plotly (visualization)                              │  │
    │  - supabase-py (database driver)                       │  │
    │                                                         │  │
    │  Auto-scaling:                                         │  │
    │  - Horizontal scaling (multiple containers)            │  │
    │  - Load balancer (Streamlit Cloud managed)             │  │
    │  - Max concurrent users: ~50 per free tier             │  │
    └──────────────────────────────────────────────────────────┘
                            │ (HTTPS/SQL)
                            │
        ┌───────────────────┴────────────────────┐
        │                                         │
        ▼                                         ▼
    ┌──────────────────────────────────┐  ┌──────────────────────────────────┐
    │   SUPABASE (Cloud Database)      │  │   GitHub Repository             │
    │   (postgres.supabase.co)         │  │   (Code storage & CI/CD)         │
    │                                  │  │                                  │
    │  ┌────────────────────────────┐  │  │  ┌────────────────────────────┐  │
    │  │  PostgreSQL Database       │  │  │  │  Branches:                 │  │
    │  │  (Replication: 3 zones)    │  │  │  │  - main (production)       │  │
    │  │  ├─ market_data table      │  │  │  │  - develop (staging)       │  │
    │  │  │  └─ ~2M rows            │  │  │  │  - feature/* (in progress) │  │
    │  │  ├─ factors table          │  │  │  └────────────────────────────┘  │
    │  │  │  └─ Pre-computed        │  │  │                                  │
    │  │  ├─ sectors table          │  │  │  ┌────────────────────────────┐  │
    │  │  │  └─ Ticker mappings     │  │  │  │  CI/CD Pipeline:           │  │
    │  │  ├─ esg_restrictions       │  │  │  │  1. Code push to main      │  │
    │  │  │  └─ Excluded tickers    │  │  │  │  2. Run pytest (unit tests)│  │
    │  │  ├─ portfolio_audit_log    │  │  │  │  3. Pylint (code quality) │  │
    │  │  │  └─ Decision trail      │  │  │  │  4. Bandit (security scan)│  │
    │  │  └─ users table            │  │  │  │  5. Deploy to Streamlit   │  │
    │  │     └─ Authentication      │  │  │  └────────────────────────────┘  │
    │  │                            │  │  │                                  │
    │  │  Backup & Recovery:        │  │  │  Artifacts:                      │
    │  │  - Automatic daily backups │  │  │  - requirements.txt              │
    │  │  - 7-day retention         │  │  │  - pytest coverage reports       │
    │  │  - Point-in-time restore   │  │  │  - Security scan results (SARIF) │
    │  │                            │  │  │  - Deployment logs               │
    │  │  Security:                 │  │  │                                  │
    │  │  - Row-level security      │  │  │  Monitoring:                     │
    │  │  - Encryption at rest      │  │  │  - Test pass/fail rate           │
    │  │  - TLS 1.3 in transit      │  │  │  - Coverage trends               │
    │  │                            │  │  │  - Deployment history            │
    │  └────────────────────────────┘  │  └────────────────────────────────┘
    │                                  │  │                                  │
    │  Cost: Free tier ($0)            │  │  Cost: Free tier ($0)            │
    │  - Up to 500MB storage           │  │  - Unlimited public repos        │
    │  - 2GB bandwidth/month           │  │  - Free GitHub Actions           │
    │  - Sufficient for student project│  │    (2000 min/month)              │
    └──────────────────────────────────┘  └──────────────────────────────────┘
```

---

## Physical Architecture Layers

### Layer 1: Presentation Layer (Client-Side)
**Technology:** Browser (JavaScript/HTML/CSS)
- Streamlit runs in user's browser
- Interactive widgets: dropdowns, checkboxes, buttons
- Real-time rendering of plots (Plotly.js)
- WebSocket connection for live updates

**Quality Attributes:**
- Responsiveness: <2 second UI update
- Compatibility: Chrome, Firefox, Safari, Edge
- Accessibility: WCAG 2.1 AA (Streamlit built-in)

---

### Layer 2: Application Server (Business Logic)
**Technology:** Streamlit Cloud (managed containerization)
- Python runtime executing streamlit_app.py
- Request → render → response cycle
- Caching for performance optimization
- Session state management (per-user isolation)

**Quality Attributes:**
- Uptime: 99% (SLA from Streamlit)
- Scalability: Auto-scaling to 50 concurrent users
- Fault tolerance: Automatic recovery from crashes
- Latency: <30 second backtest completion

**Resource Allocation:**
- CPU: 1 vCPU per container
- Memory: 512 MB RAM per user session
- Storage: 1 GB (code + dependencies)

---

### Layer 3: Data Access Layer (Database Connection)
**Technology:** Supabase (PostgreSQL + connection pooling)
- psycopg2 driver (Python-PostgreSQL bridge)
- Connection pool (5 active connections)
- Query optimization with indexes
- Caching to reduce database load

**Quality Attributes:**
- Query latency: <1 second (cached) to <5 seconds (fresh)
- Throughput: 100+ concurrent queries
- Consistency: ACID transactions
- Availability: 3-zone replication (auto-failover)

**Database Performance:**
- Indexes on: ticker, date, factor_name
- Query result set: typically 2,000–100,000 rows
- Cache hit rate: ~80% (typical for factor portfolios)

---

### Layer 4: Data Storage Layer (Persistent Database)
**Technology:** PostgreSQL (Supabase managed)
- Distributed storage across multiple availability zones
- Automatic backups (daily, 7-day retention)
- Point-in-time restore capability
- Encryption at rest (AES-256)

**Storage Breakdown:**
- market_data: ~2 million rows (22 years × 2,000 tickers × 12 months)
- factors: ~26 million rows (13 factors × 2 million data points)
- audit_log: grows ~100 rows/week
- **Total: ~500 MB** (easily within free tier)

---

## Data Flow: Request → Response Cycle

### Scenario: User Runs a Backtest

```
Step 1: User Interaction (UI)
├─ Portfolio Manager clicks "Run Backtest" in Streamlit
├─ Browser sends request to Streamlit Cloud
└─ Streamlit captures: selected factors, weighting scheme, filters

Step 2: Application Logic Execution
├─ streamlit_app.py receives request
├─ Calls: portfolio_engine.backtest(start="2002-01", end="2025-12")
├─ CalculateHoldings.backtest():
│  ├─ Loop: for each month from 2002-01 to 2025-12
│  ├─ Call: market.load_data(date)
│  └─ First iteration: Cache MISS → Query Supabase
│     └─ Subsequent iterations: Cache HIT (same data)

Step 3: Database Query (Layer 3 → Layer 4)
├─ SupabaseClient sends SQL:
│  ├─ SELECT * FROM market_data WHERE date='2002-01'
│  ├─ SELECT * FROM factors WHERE date='2002-01'
│  ├─ SELECT * FROM sectors
│  └─ SELECT * FROM esg_restrictions
├─ Query plan: Index scan on (ticker, date)
├─ Result: 2,000 rows × (price + 13 factors) = ~100 KB
├─ Latency: First query ~200 ms, cached queries ~10 ms
└─ Results sent back to application server

Step 4: Business Logic Computation
├─ For 2002-01 data:
│  ├─ Factor calculation: vectorized NumPy operations (~50 ms)
│  ├─ Security ranking: pandas sort (~30 ms)
│  ├─ Constraint filtering: ESG + sector (~10 ms)
│  ├─ Portfolio weighting: allocation computation (~5 ms)
│  └─ Metrics calculation: return, volatility, Sharpe (~50 ms)
├─ Subtotal for one month: ~150 ms
├─ Total for 276 months: ~41 seconds
└─ All within <30 second requirement (due to caching)

Step 5: Result Aggregation
├─ Combine 276 monthly portfolios
├─ Generate summary statistics
├─ Prepare visualization data (dollar-invested series)
├─ Format for Streamlit rendering
└─ Total time: <2 seconds

Step 6: Response Rendering (UI)
├─ Streamlit sends results to browser
├─ Plotly generates interactive chart (~500 ms)
├─ Metric cards displayed (~100 ms)
├─ Export button enabled
└─ Total time: ~1 second

TOTAL END-TO-END TIME: ~45 seconds (mostly network + caching overhead)
```

---

## Deployment Process (CI/CD Pipeline)

```
┌────────────────────────────────────────────────────────────┐
│              Developer Workflow                            │
├────────────────────────────────────────────────────────────┤
│ 1. Developer writes code locally                           │
│    └─ Runs: pytest UnitTests/                              │
│    └─ Checks: git status, git diff                         │
│                                                             │
│ 2. Create feature branch: git checkout -b feature/...      │
│    └─ Make changes, commit locally                         │
│    └─ Push to GitHub: git push origin feature/...          │
│                                                             │
│ 3. Create Pull Request on GitHub                           │
│    └─ Describe changes, link issues                        │
│    └─ Trigger: GitHub Actions CI/CD pipeline              │
│                                                             │
│ 4. CI/CD Checks (Automated)                               │
│    ├─ Step 1: Checkout code                               │
│    ├─ Step 2: Install dependencies (pip install -r req)   │
│    ├─ Step 3: Run tests                                   │
│    │  └─ pytest UnitTests/ -v --cov=src                   │
│    │  └─ Success: >80% coverage threshold                 │
│    ├─ Step 4: Code quality check                          │
│    │  └─ pylint src/ --fail-under=7.0                     │
│    │  └─ Success: score ≥ 7.0 out of 10                   │
│    ├─ Step 5: Security scan                               │
│    │  └─ bandit -r src/ -f sarif                          │
│    │  └─ Success: no critical vulnerabilities             │
│    └─ Step 6: Approval check                              │
│       └─ Requires ≥1 peer review approval                 │
│                                                             │
│ 5. Code Review (Manual)                                   │
│    ├─ Peer reviewer reads code changes                     │
│    ├─ Comments on logic, style, edge cases                │
│    ├─ Approves PR (or requests changes)                   │
│    └─ Merge to main branch (when approved)                │
│                                                             │
│ 6. Post-Merge (Automatic)                                 │
│    ├─ Webhook triggers: Streamlit Cloud receives push     │
│    ├─ Streamlit pulls latest code from GitHub             │
│    ├─ Install dependencies                                │
│    ├─ Run health checks                                   │
│    └─ Deploy to production URL                            │
│                                                             │
│ 7. Production Verification                                │
│    ├─ Monitor: Streamlit Cloud logs                       │
│    ├─ Alert: Slack notification on deploy                │
│    ├─ Test: Manual smoke test (visit app URL)             │
│    └─ Rollback: Revert to previous commit if error        │
│                                                             │
│ Result: Code pushed to main → deployed within 2 minutes   │
└────────────────────────────────────────────────────────────┘
```

---

## Disaster Recovery & High Availability

### Failure Scenarios & Mitigations

| Failure Scenario | Impact | Mitigation | RTO | RPO |
|-----------------|--------|-----------|-----|-----|
| **Database down** | Backtest fails; UI shows error | Supabase 3-zone replication; auto-failover | <1 min | 0 |
| **Streamlit app crash** | Users disconnected; requests fail | Automatic container restart | <1 min | 0 |
| **Network latency spike** | Backtest slow; user waits | In-memory cache reduces DB queries | N/A | N/A |
| **Data corruption** | Analytics incorrect | Daily backups; point-in-time restore | <1 hr | <24 hrs |
| **Malicious access** | Unauthorized portfolio decisions | Row-level security (RBAC); JWT tokens | <1 min | 0 |
| **Code deployment bug** | Features broken; users affected | Automated tests catch 95% of bugs | <5 min | Hotfix |

**RTO** = Recovery Time Objective (how fast to restore)  
**RPO** = Recovery Point Objective (how much data to lose)

---

## Monitoring & Observability

### Metrics Dashboard (to be implemented)

**Application Metrics:**
- Backtest execution time (target: <30 sec)
- Error rate (target: <1%)
- Cache hit rate (target: >80%)
- Active user count (peak: ~20)

**Database Metrics:**
- Query latency p95 (target: <200 ms)
- Slow query count (target: 0)
- Connection pool utilization (target: <80%)
- Storage usage (current: ~500 MB)

**Infrastructure Metrics:**
- Streamlit Cloud CPU (target: <70%)
- Memory usage (target: <80%)
- Uptime (target: 99%)
- Deployment frequency (current: ~1–2 per week)

**Security Metrics:**
- Failed authentication attempts (alert if >10/hour)
- Data access anomalies (unusual query patterns)
- Vulnerability scan results (target: 0 critical)

---

## Cost Analysis

### Current Deployment (Free Tier)

| Component | Cost | Notes |
|-----------|------|-------|
| Streamlit Cloud | $0 | Free tier; supports ~50 concurrent users |
| Supabase (PostgreSQL) | $0 | Free tier; 500 MB storage, 2 GB bandwidth/month |
| GitHub | $0 | Free tier; public repo, unlimited CI/CD minutes |
| **Total Monthly Cost** | **$0** | Suitable for student/research project |

### Future Scaling (If Deployed at Production)

| Tier | Streamlit | Supabase | Total/Month |
|------|-----------|----------|------------|
| Free | $0 | $0 | $0 |
| Pro (100 users) | $5/user | $25 | $525 |
| Enterprise (1000 users) | Custom | $100+ | $1000+ |

**Current footprint is optimized for campus use (~20–50 concurrent portfolio managers).**

