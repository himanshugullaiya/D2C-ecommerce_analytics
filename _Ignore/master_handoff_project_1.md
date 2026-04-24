# Master Handoff — Rich (Himanshu Gullaiya)
## DA Job Prep + Project 1 Complete
### Last Updated: April 16, 2026

---

## WHO IS RICH

- **Name:** Himanshu Gullaiya (goes by Rich)
- **GitHub:** himanshugullaiya
- **Education:** CSE 2021, MSIT Janakpuri, Delhi
- **Gap:** 5 years — full-time systematic trader (built broker API scalper, tkinter backtesting toolbox, automated Google Drive photo pipeline)
- **Goal:** Data Analyst role — stable hours, low pressure, ~10 LPA, product-based company. Job = runway to fund trading, not a career end goal.
- **Trading hours:** 6:30–9:30 PM daily. Deep work: morning + afternoon blocks.
- **Teaching style:** Direct, no fluff, fintech examples, attempt first then correct

---

## CLAUDE BEHAVIOUR RULES

1. Call him Rich, never Himanshu
2. Direct — no fluff, no over-encouragement
3. He writes code himself — guide, hint, provide code only after 2 failed attempts
4. One thing at a time
5. Strict accountability — keep on track with deadlines
6. All measure names prefixed with `_M_` in Power BI
7. Power BI canvas: 1280×720, white background, Samsung aesthetic (#1B2A4A navy)

---

## DEADLINE: MAY 1, 2026 (Application Day)

---

## SPRINT PLAN — REMAINING

| Task | Status |
|------|--------|
| Project 1 — HG Analytics D2C Dashboard | ✅ DONE |
| Project 1 — README pushed to GitHub | ✅ DONE |
| Project 1 — GIFs + Video | After Project 2 half done |
| Project 2 — Stock Market (NSE Bhavcopy) | 🔄 STARTING NOW |
| GitHub READMEs — both projects | Project 1 done, Project 2 pending |
| CV + LinkedIn overhaul | NOT STARTED |
| SQL revision — top 100 questions | NOT STARTED |
| KPIs + Power BI + Excel revision | NOT STARTED |
| Communication prep + mock interview | NOT STARTED |
| First applications sent | May 1, 2026 |

---

## REFERENCES & NETWORK

- Brother — SDE-3 at large MNC (potential referral)
- Friend — Product Analyst at Zomato (potential referral)
- MSIT Janakpuri alumni network
- Target companies: Amex, Mastercard, Airblack, PolicyBazaar, Chegg, Scry AI, similar

---

## GITHUB STATUS

- Profile: github.com/himanshugullaiya
- Bio updated to: "Data Analyst | Python · SQL · Power BI | Ex-Derivatives Trader. Long-Term Gain & Self-Discipline"
- Project 1 repo: himanshugullaiya/D2C-ecommerce_analytics — LIVE
- README pushed ✅
- .pbix NOT pushed yet — push May 1 (application day) to prevent copying
- Pinned repos: Update to show D2C project prominently

---

## BEFORE APPLYING — REVISION CHECKLIST

- [ ] SQL top interview questions + concepts
- [ ] Excel (important functions, pivot tables)
- [ ] Python/Pandas revision
- [ ] Power BI tools revision
- [ ] Business KPIs (must know)
- [ ] Interview narrative — gap explanation, background framing
- [ ] Communication prep
- [ ] Mock interview with Claude

---

## PROJECT 1 — HG ANALYTICS D2C DASHBOARD
### Status: ✅ COMPLETE

**Repo:** himanshugullaiya/D2C-ecommerce_analytics  
**Local:** D:\DATA ANALYST JOB PREP\MY PROJECTS\D2C E-Commerce Analytics\  
**Branding:** HG Analytics (circular logo, navy #1B2A4A, bar chart icon)

---

### DATA

| Table | Rows | Notes |
|-------|------|-------|
| customers | ~13,000 | city, state, age, acquisition_channel |
| products | 80 | 3 categories, subcategory, brand, unit_price, cost_price |
| orders | ~125,000 | order_id, customer_id, order_date, order_status, net_amount |
| order_items | ~300,000 | order_item_id, product_id, qty, unit_price_at_purchase |
| returns | ~12,500 | return_id, order_id, return_reason, return_amount |

**Key Numbers:**
- Revenue: ₹6.8bn
- Orders: 125K
- Customers: 13K
- AOV: ₹54.6K (electronics skew — ₹76.8K electronics vs ₹2-3K clothing)
- Profit Margin: ~46.8%
- Return Rate: 9.96% (orders), 22.88% (revenue)
- Total Return Value: ₹1.56bn
- Active Customer Rate: 85%
- Best Month: December 2025 — ₹869M

---

### PYTHON SCRIPTS

| Script | Purpose |
|--------|---------|
| generate_data.py | Generate realistic Indian D2C data using Faker |
| inject_dirty_data.py | Inject 9 dirty data categories |
| clean_data.py | Full cleaning pipeline |
| testing_data_after_cleaning.py | Validation checks |

**Key generation decisions:**
- Faker('en_IN') for Indian names
- Poisson(lam=10) for orders per customer
- `random.choices(weights=[40,40,20])` for acquisition channel
- Category-weighted return reasons
- `np.random.uniform(0.40, 0.70, size=len(df))` for cost price (must use size= or all rows get same value)
- Electronics limited to 1 per subcategory per order (AOV fix)
- Two unit_prices: catalog price + price at purchase (SCD Type 2)

**9 Dirty Data Issues Injected:**
1. Null values (email, phone, qty, payment_method)
2. Duplicate rows (5% customers, 5% orders, 2% order_items)
3. Mixed date formats (YYYY-MM-DD, YYYY/MM/DD, DD Month YYYY)
4. Outliers (unit_price 1000x, order_amount 0.001x)
5. Orphan records (fake customer_ids in orders)
6. Inconsistent categorical values (city case, payment_method case)
7. Invalid values (negative age, qty=0)
8. Wrong data types (dates as strings)
9. Inconsistent string formats

**Cleaning sequence (industry standard):**
1. Drop rows with too many nulls (thresh=4)
2. Fix data types
3. Fix nulls (fillna / impute)
4. Fix inconsistent formats
5. Fix invalid values
6. Fix outliers — IQR **subcategory-wise** (not global — global failed for shirts)
7. Fix orphan records
8. Remove duplicates — **LAST** (earlier steps create apparent duplicates)

---

### POSTGRESQL

- Database: project
- Schema silver: customers, orders, order_items, products, all_returns
- Schema gold: 6 materialized views + 6 wrapper views (v_ prefix for Power BI)

| Materialized View | Wrapper View | Purpose |
|---|---|---|
| gold.cohort_retention | v_cohort_retention | Monthly retention % per cohort |
| gold.rfm_segmentation | v_rfm_segmentation | RFM scores + segments |
| gold.product_performance | v_product_performance | Revenue, profit, returns by product |
| gold.revenue_monthly | v_revenue_monthly | Monthly revenue, orders, MOM% |
| gold.returns_analysis | v_returns_analysis | Return trends by subcategory + reason |
| gold.executive_kpis | v_executive_kpis | All executive metrics per month |

**Why wrapper views?** Power BI navigator doesn't show materialized views.

**Fan-out problem (most important SQL lesson):**
Joining orders → order_items (one-to-many) then SUM(order_amount) = 2x revenue inflation.
Fix: Always aggregate from `order_items.total_sales_curr_order`

**SQL Fixes Made:**
- executive_kpis: Changed sum(o.net_amount) to sum(oi.total_sales_curr_order)
- executive_kpis: Returns in separate CTE to avoid fan-out from LEFT JOIN all_returns
- product_performance: Fixed PROD_080 (Yoga Mat) unit_price causing revenue < profit
- product_performance: revenue_rank_in_category uses DESC (was missing)
- returns_analysis: LAG partitioned by subcategory, return_reason (was product_name — too granular)
- returns_analysis: return_condition_flag = Worsening (>5%), Improving (<-5%), Stable

**returns_analysis SQL (final version):**
```sql
WITH base_metrics AS (
    SELECT
        date_trunc('month', o.order_date) AS for_sorting,
        to_char(o.order_date, 'FMMonth YYYY') AS month_year,
        p.category, p.subcategory,
        ar.return_reason,
        COUNT(DISTINCT ar.return_id) AS total_returns,
        SUM(ar.return_amount) AS total_return_value,
        AVG(ar.return_amount) AS avg_return_value
    FROM silver.orders o
    LEFT JOIN silver.all_returns ar ON o.order_id = ar.order_id
    LEFT JOIN silver.order_items oi ON oi.order_id = o.order_id
    LEFT JOIN silver.products p ON p.product_id = oi.product_id
    WHERE o.order_status = 'Returned'
    GROUP BY 1,2,3,4,5
),
with_window_funcs AS (
    SELECT *,
        LAG(total_returns) OVER (
            PARTITION BY subcategory, return_reason
            ORDER BY for_sorting
        ) AS prevm_total_returns
    FROM base_metrics
),
with_flags AS (
    SELECT *,
        (total_returns - prevm_total_returns) * 1.00 / NULLIF(prevm_total_returns, 0) AS mom_return_change
    FROM with_window_funcs
)
SELECT *,
    CASE
        WHEN mom_return_change > 0.05 THEN 'Worsening'
        WHEN mom_return_change < -0.05 THEN 'Improving'
        ELSE 'Stable'
    END AS return_condition_flag
FROM with_flags
```

---

### POWER BI — DATA MODEL

**Active Relationships:**
- Date_Table[Start_of_Month] → v_executive_kpis[for_sorting] (many-to-1, Both)
- Date_Table[Start_of_Month] → v_revenue_monthly[for_sorting] (many-to-1, Both)
- Date_Table[Date] → orders[order_date] (many-to-1)
- Date_Table[Start_of_Month] → v_returns_analysis[for_sorting] (many-to-1, Both)
- customers[customer_id] → orders[customer_id] (1-to-many)
- customers[customer_id] → v_rfm_segmentation[customer_id]

**Standalone (intentional — no date relationship):**
- v_cohort_retention — date slicer would filter out retention months for old cohorts
- v_product_performance — standalone

---

### POWER BI — ALL MEASURES

**BASE:**
- `_M_total_revenue = SUM(v_executive_kpis[total_revenue])`
- `_M_total_orders = SUM(v_executive_kpis[total_orders])`
- `_M_total_customers = DISTINCTCOUNT(orders[customer_id])`
- `_M_AOV = DIVIDE([_M_total_revenue], [_M_total_orders])`
- `_M_profit_margin_pct = AVERAGE(v_executive_kpis[profit_margin_pct_decimal])`
- `_M_return_rate_pct = AVERAGE(v_executive_kpis[return_rate_pct_decimal])`
- `_M_active_customers`
- `_M_exec_total_orders`
- `_M_exec_total_revenue`
- `_M_total_profit = SUM(v_revenue_monthly[total_profit])`
- `_M_latest_npm_pct = CALCULATE(AVERAGE(...profit_margin...), LASTDATE(Date_Table[Date]))`

**MTD:**
- `_M_MTD_revenue`, `_M_MTD_orders`, `_M_MTD_profit`

**MOM:**
- `_M_mom_revenue_pct`, `_M_mom_orders_pct`, `_M_mom_customers`
- `_M_mom_profit_margin_pct`, `_M_mom_profit_pct`

**MOM Pattern:**
```dax
_M_mom_X =
VAR last_date = LASTDATE(Date_Table[Date])
VAR current = CALCULATE([_M_X], DATESMTD(last_date))
VAR previous = CALCULATE([_M_X], PREVIOUSMONTH(last_date))
RETURN DIVIDE(current - previous, previous, 0)
```

**RETURNS:**
- `_M_return_total_pct = DIVIDE(SUM(v_returns_analysis[total_return_value]), [_M_revenue_total_revenue], 0)`

**REVENUE_View:**
- `_M_revenue_total_revenue = SUM(v_revenue_monthly[total_revenue])`
- `_M_best_month_revenue = MAXX(ALL(v_revenue_monthly[month_year]), [_M_revenue_total_revenue])`
- `_M_best_month_name` (TOPN + FIRSTNONBLANK pattern)

**Field Parameters:**
- `Product_metric_Selector` — total_revenue, total_profit, profit_margin_pct_decimal, total_orders, total_qty
- `Revenue_metric_Selector` — Revenue, Orders, Customers, Profit
- `Map_metric_Selector` — Revenue, Orders, Customers
- `MOM_metric_Selector` — Revenue MOM%, Profit MOM%

---

### POWER BI — 6 TABS (ALL COMPLETE)

**Page order: Executive → Products → Revenue → Cohort → RFM → Returns**

#### Tab 1 — Executive Overview ✅
- Logo: HG Analytics (transparent horizontal on Executive, circular on all others)
- Title: "D2C E-Commerce Dashboard" next to logo
- 6 KPI cards: Revenue (MOM, MTD, CUR NPM%), Orders (MOM, MTD), Customers (MOM, Active C.), AOV, C. Repeat Rate, O. Return Rate
- Total Revenue Trend — field parameter switcher: Revenue/Orders/Customers/Profit
- Time Period Selector (between date slicer + custom clear "Selection" button)
- Map with bookmark toggle — Revenue by State (blue, 💰) ↔ Return % by State (red, 💸)
- AOV by Category donut
- Customers by Acquisition Channel donut

#### Tab 2 — Products ✅
- Title: "What's Driving The Revenue"
- Category Revenue donut (electronics 79.2%)
- Field parameter buttons: T. Profit / T. Orders / T. Revenue / NPM% / T. Qty
- Subcategory bar chart (switches with parameter)
- Brand treemap — Samsung ₹1bn, Apple ₹597M, Xiaomi ₹972M
- Top 3 Products Per Category table
- High Return Products table

#### Tab 3 — Revenue ✅
- Title: "Revenue Trends & Leakage Analysis"
- Revenue Trend + field parameter
- YOY Revenue Comparison grouped bar (2023/2024/2025)
- Bookmark toggle: TOTALS / YOY Comparison / MOM% Growth
- Profit MOM% Change Trend bar + Revenue/Profit switcher
- KPI cards: Total Revenue ₹6.8bn | Best Month ₹869M Dec 2025 | Latest MOM% 46.5%

#### Tab 4 — Cohort ✅
- Title: "Customer Retention Analysis by First Order Month"
- Subtitle: "Tracking When Each Month's New Customers Return Over Time"
- Cohort heatmap M1–M16, green→red
- Total New Customers per Cohort bar
- Pre-written insights text box (5 insights)

**Key cohort insights:**
1. 2025 M3 retention 69% vs 27% in 2023 — 2.5x improvement
2. Jan 2023 shows ~6-month oscillation — seasonal reactivation
3. Jan 2023 range 11-34% vs Jan 2025 47-59% — 4x higher floor
4. Retention stabilizes ~25% after M6
5. Cohort sizes plateaued ~400/month through 2024 — acquisition stalled

#### Tab 5 — RFM ✅
- Title: "Customer RFM (Recency, Frequency & Monetary) Segment Analysis"
- Subtitle: "For Strategic Decisions to prioritize Retention & Growth"
- Customers by Segment bar — Growth 60% / Concern 40%
- Avg Revenue per Segment bar
- Top 10 Customers by ₹ table
- Segments & Actions table
- Customers State-wise Distribution stacked bar

**RFM Segments:**
| Segment | Count | % | Action |
|---------|-------|---|--------|
| Loyal | 3,314 | 26% | Upsell & Cross-sell |
| Lost | 2,480 | 19% | Deprioritize — sunset campaign |
| At Risk | 2,017 | 16% | Win Back — urgent re-engagement |
| Promising | 1,859 | 15% | Nurture — first repeat discount |
| Champion | 1,715 | 13% | Reward & Retain — loyalty program |
| New Customer | 761 | 6% | Engage — welcome series |
| Needs Attention | 603 | 5% | Reactivate — targeted offer |

#### Tab 6 — Returns ✅
- Title: "Return Patterns & Risk Detection Analysis"
- Return % KPI: 9.96% orders wise / 22.88% revenue wise
- Total Return Value by Category donut (₹1.56bn)
- Total Returns vs Return Reason donut (24K)
- Category slicer (tile) + Sub-Category dropdown — isolated to top donuts
- Return Value by Revenue Monthly % Trend bar — conditional green/red, 25% reference line
- Return Trend by Subcategory & Reason bar — colored by return_condition_flag (red/green/grey)
- Sub-Category dropdown + Return Reason slicer — isolated to bottom-right chart only

---

### KNOWN DATA LIMITATIONS (Interview Answers Ready)

1. Revenue from order_items not net_amount — discount (~4.5%) not deducted
2. Repeat Rate 99.92% — Poisson lam=10 artifact. Real D2C = 40-60%
3. AOV high — electronics skew. Category-level tells real story
4. Return rate uniform across categories — synthetic artifact
5. Cost price not historically tracked — SCD Type 2 noted as future enhancement
6. 0.004% floating point variance Python vs PostgreSQL — numeric precision
7. Returns at order level not product level — category bias partially diluted

---

### KEY INTERVIEW ANSWERS

**Fan-out problem:**
"I identified a fan-out issue where joining orders to order_items multiplied order-level columns by item count, causing 2x revenue inflation. Fixed by always aggregating from order_items directly."

**Why Medallion Architecture?**
"Bronze = raw dirty data intact. Silver = clean. Gold = analytical aggregations. Each layer is independently rerunnable."

**Why synthetic data?**
"Programmatically generated realistic synthetic data using Faker, modeled after real D2C e-commerce patterns, then intentionally introduced 9 categories of data quality issues to simulate production-level messy data."

**Why subcategory level for returns?**
"Product level is too granular — 1-2 returns per product per month creates noise. Category level is too broad. Subcategory is the sweet spot — 'Laptop Damaged returns worsening' triggers a packaging fix."

**Why IQR for outliers?**
"IQR is robust — not affected by outliers themselves. Z-score uses mean and std which both get distorted."

**Why IQR subcategory-wise?**
"Global IQR failed — a ₹93K shirt price passed because electronics pulled the upper bound."

**Why cohort_retention standalone?**
"Date slicer would filter out retention months for old cohorts."

**Why wrapper views?**
"Power BI doesn't show materialized views in navigator."

**On AOV being high:**
"AOV skewed by electronics. Clothing AOV ₹2-3K, electronics ₹76K+."

**On Repeat Rate 99.92%:**
"Synthetic artifact — Poisson lam=10. Real D2C = 40-60%."

**On discount not in revenue:**
"~4.5% discount not deducted. In production would implement proportional discount allocation per product."

---

## PROJECT 2 — NSE BHAVCOPY STOCK ANALYTICS
### Status: 🔄 PLANNING

**NOT STARTED. Starting next.**

Tech stack planned: Python (NSE Bhavcopy download) → PostgreSQL → Power BI

---

## PENDING TASKS — EXACT ORDER

1. **Project 2** — Start immediately
2. **GIFs for Project 1** — After Project 2 is half done (serves as revision)
   - Map toggle Revenue ↔ Returns
   - Return trend chart conditional coloring
   - Field parameter switcher Products tab
   - Cohort heatmap + YOY toggle
3. **YouTube video** — Both projects, facecam, proof of trading background (80 subs, 50+ videos on trading channel)
4. **Power BI Publish to Web** — May 1 morning (free, File → Publish → Publish to Web)
5. **Push GIFs + video link + .pbix** — May 1
6. **CV + LinkedIn** — After Project 2
7. **SQL revision** — Top 100 questions
8. **Mock interview** — Claude
9. **Apply** — May 1 afternoon

---

## IMPORTANT NOTES

- SQLAlchemy removed from README — Rich doesn't know it, not working on his system
- Data Quality tab — dropped from dashboard. Content goes in README only
- .pbix NOT pushed to GitHub — push May 1 to prevent copying
- YouTube trading channel is proof of gap legitimacy — use in interviews
- Duplicate tab "Duplic..." exists in Power BI — delete before May 1
- All percentage values in PostgreSQL kept as decimals (0.01 scale) — formatted in Power BI

---

*For next chat: Upload this file at the start. Current task: Plan and start Project 2 — NSE Bhavcopy Stock Analytics.*
