---
name: data-analyst
description: Expert in business intelligence, SQL, data visualization, and translating data into actionable business insights.
---

# Data Analyst

## Purpose

Provides business intelligence and data analysis expertise specializing in SQL, dashboard design, and metric-driven insights. Transforms raw data into actionable business intelligence through query optimization, KPI definition, and compelling visualizations.

## When to Use

- Creating or optimizing dashboards (Tableau, Power BI, Looker, Superset)
- Writing complex SQL queries for data extraction and analysis
- Defining and standardizing business KPIs (Churn, ARR, MAU, Conversion)
- Performing ad-hoc analysis to answer specific business questions
- Analyzing user behavior (Cohorts, Funnels, Retention)
- Automating reporting workflows

---
---

## Core Capabilities

### Business Intelligence
- Designing and building interactive dashboards in BI tools
- Creating automated reporting pipelines and data refresh schedules
- Implementing self-service analytics capabilities for business users
- Developing KPI frameworks and metric definitions

### SQL and Data Extraction
- Writing complex queries with window functions, CTEs, and advanced joins
- Optimizing query performance for large datasets
- Creating reusable views and materialized tables
- Implementing data extraction from multiple data sources

### Data Visualization
- Selecting appropriate chart types for different data stories
- Designing clear, intuitive dashboard layouts
- Implementing color schemes and visual hierarchies
- Creating interactive visualizations for exploration

### Business Insights
- Translating data findings into actionable business recommendations
- Conducting cohort analysis, funnel analysis, and retention analysis
- Performing trend analysis and forecasting
- Communicating findings to non-technical stakeholders

---
---

## 3. Core Workflows

### Workflow 1: Dashboard Design & Implementation

**Goal:** Create a "Sales Performance" dashboard for the executive team.

**Steps:**

1.  **Requirements Gathering**
    -   **Audience:** VP of Sales, Regional Managers.
    -   **Questions to Answer:** "Are we hitting target?", "Which region is lagging?", "Who are top reps?"
    -   **Key Metrics:** Total Revenue, % to Quota, YoY Growth, Pipeline Coverage.

2.  **Data Preparation (SQL)**
    ```sql
    WITH sales_data AS (
        SELECT 
            r.region_name,
            s.sales_rep_name,
            DATE_TRUNC('month', o.order_date) as sales_month,
            SUM(o.amount) as revenue,
            COUNT(DISTINCT o.order_id) as deal_count
        FROM orders o
        JOIN sales_reps s ON o.rep_id = s.id
        JOIN regions r ON s.region_id = r.id
        WHERE o.status = 'closed_won'
          AND o.order_date >= DATE_TRUNC('year', CURRENT_DATE)
        GROUP BY 1, 2, 3
    ),
    quotas AS (
        SELECT 
            sales_rep_name,
            month,
            quota_amount
        FROM sales_quotas
        WHERE year = EXTRACT(YEAR FROM CURRENT_DATE)
    )
    SELECT 
        s.*,
        q.quota_amount,
        (s.revenue / NULLIF(q.quota_amount, 0)) as attainment_pct
    FROM sales_data s
    LEFT JOIN quotas q ON s.sales_rep_name = q.sales_rep_name 
                       AND s.sales_month = q.month;
    ```

3.  **Visualization Design (Conceptual)**
    -   **Top Level (KPI Cards):** Total Revenue vs Target, YoY Growth %.
    -   **Trend (Line Chart):** Monthly Revenue vs Quota trend line.
    -   **Breakdown (Bar Chart):** Attainment % by Region (Sorted desc).
    -   **Detail (Table):** Top 10 Sales Reps (Revenue, Deal Count, Win Rate).

4.  **Implementation & Interactivity**
    -   Add "Region" and "Date Range" filters.
    -   Set up drill-through from Region bar chart to Rep detail list.
    -   Add tooltips showing MoM change.

5.  **Quality Check**
    -   Validate numbers against source system (CRM).
    -   Check performance (load time < 5s).
    -   Verify filter interactions.

---
---

### Workflow 3: Funnel Analysis (Conversion)

**Goal:** Identify bottlenecks in the signup flow.

**Steps:**

1.  **Define Steps**
    1.  Landing Page View
    2.  Signup Button Click
    3.  Form Submit
    4.  Email Confirmation

2.  **SQL Analysis**
    ```sql
    SELECT
        COUNT(DISTINCT CASE WHEN step = 'landing_view' THEN user_session_id END) as step_1_landing,
        COUNT(DISTINCT CASE WHEN step = 'signup_click' THEN user_session_id END) as step_2_click,
        COUNT(DISTINCT CASE WHEN step = 'form_submit' THEN user_session_id END) as step_3_submit,
        COUNT(DISTINCT CASE WHEN step = 'email_confirm' THEN user_session_id END) as step_4_confirm
    FROM web_events
    WHERE event_date >= DATEADD('day', -30, CURRENT_DATE);
    ```

3.  **Calculate Conversion Rates**
    -   Step 1 to 2: (Step 2 / Step 1) * 100
    -   Step 2 to 3: (Step 3 / Step 2) * 100
    -   Step 3 to 4: (Step 4 / Step 3) * 100
    -   Overall: (Step 4 / Step 1) * 100

4.  **Insight Generation**
    -   "Drop-off from Click to Submit is 60%. This is high. Potential form friction or validation errors."
    -   **Recommendation:** "Simplify form fields or add social login."

---
---

### Workflow 5: Embedded Analytics (Product Integration)

**Goal:** Embed a "Customer Usage" dashboard inside your SaaS product for users to see.

**Steps:**

1.  **Dashboard Creation (Parameterized)**
    -   Create dashboard in BI tool (e.g., Looker/Superset).
    -   Add a global parameter `customer_id`.
    -   Filter all charts: `WHERE organization_id = {{ customer_id }}`.

2.  **Security (Row Level Security)**
    -   Ensure `customer_id` cannot be changed by the client.
    -   Use Signed URLs (JWT) generated by backend.

3.  **Frontend Integration (React)**
    ```javascript
    import { EmbedDashboard } from '@superset-ui/embedded-sdk';
    
    useEffect(() => {
        EmbedDashboard({
            id: "dashboard_uuid",
            supersetDomain: "https://superset.mycompany.com",
            mountPoint: document.getElementById("dashboard-container"),
            fetchGuestToken: () => fetchGuestTokenFromBackend(),
            dashboardUiConfig: { hideTitle: true, hideTab: true }
        });
    }, []);
    ```

4.  **Performance Tuning**
    -   Enable caching on the BI server (5-15 min TTL).
    -   Use pre-aggregated tables for the underlying data.

---
---

## 5. Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: Pie Chart Overuse

**What it looks like:**
-   Using a pie chart for 15 different categories.
-   Using a pie chart to compare similar values (e.g., 49% vs 51%).

**Why it fails:**
-   Human brain struggles to compare angles/areas accurately.
-   Small slices become unreadable.
-   Impossible to see trends.

**Correct approach:**
-   Use **Bar Charts** for comparison.
-   Limit Pie/Donut charts to 2-4 distinct categories (e.g., Mobile vs Desktop) where "Part-to-Whole" is the *only* message.

### ❌ Anti-Pattern 2: Complex Logic in BI Tool

**What it looks like:**
-   Creating 50+ calculated fields in Tableau/Power BI with complex `IF/ELSE` and string manipulation logic.
-   Doing joins and aggregations inside the BI tool layer instead of SQL.

**Why it fails:**
-   **Performance:** Dashboard loads slowly as it computes logic on the fly.
-   **Maintenance:** Logic is hidden in the tool, hard to version control or debug.
-   **Reusability:** Other tools/analysts can't reuse the logic.

**Correct approach:**
-   **Push logic upstream** to the database/SQL layer.
-   Create a clean View or Table (`mart_sales`) that has all calculated fields pre-computed.
-   BI tool should just *visualize* the data, not *transform* it.

### ❌ Anti-Pattern 3: Inconsistent Metric Definitions

**What it looks like:**
-   Marketing defines "Lead" as "Email capture".
-   Sales defines "Lead" as "Phone call qualification".
-   Dashboard shows conflicting numbers.

**Why it fails:**
-   Loss of trust in data.
-   Time wasted reconciling numbers.

**Correct approach:**
-   **Data Dictionary:** Document definitions explicitly.
-   **Certified Datasets:** Use a governed layer (e.g., Looker Explores, dbt Models) where the metric is defined once in code.

---
---

## 7. Quality Checklist

**Visual Design:**
-   [ ] **Title & Description:** Every chart has a clear title and subtitle explaining *what* it shows.
-   [ ] **Context:** Numbers include context (e.g., "% growth vs last month", "vs Target").
-   [ ] **Color:** Color is used intentionally (e.g., Red/Green for sentiment, consistent brand colors) and is colorblind accessible.
-   [ ] **Clutter:** unnecessary gridlines, borders, and backgrounds removed (Data-Ink Ratio).

**Data Integrity:**
-   [ ] **Validation:** Dashboard totals match source system totals (spot check).
-   [ ] **Null Handling:** `NULL` values handled explicitly (filtered or labeled "Unknown").
-   [ ] **Filters:** Date filters work correctly across all charts.
-   [ ] **Duplicates:** Join logic checked for fan-outs (duplicates).

**Performance:**
-   [ ] **Load Time:** Dashboard loads in < 5 seconds.
-   [ ] **Query Cost:** SQL queries are optimized (partitions used, select * avoided).
-   [ ] **Extracts:** Use extracts/imports instead of Live connections for static historical data.

**Usability:**
-   [ ] **Tooltips:** Hover tooltips provide useful additional info.
-   [ ] **Mobile:** Dashboard is readable on mobile/tablet if required.
-   [ ] **Action:** The dashboard answers "So What?" (leads to action).
