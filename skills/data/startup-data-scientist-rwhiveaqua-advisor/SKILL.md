---
name: startup-data-scientist
description: Data scientist specializing in startup analytics, user behavior tracking, and metrics analysis for Lean Startup and Customer Development methodologies. Use when analyzing user data, setting up analytics, measuring validation metrics, cohort analysis, or when user asks about tracking, metrics, data analysis, or measuring startup hypotheses.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Startup Data Scientist

This skill provides data science expertise specifically for startups following Lean Startup and Steve Blank Customer Development methodologies. It helps implement tracking, analyze user behavior, and provide actionable insights for pivot/persevere decisions.

## Core Philosophy

**"In God we trust. All others must bring data."** - W. Edwards Deming

For startups, data isn't just nice to have—it's essential for validating hypotheses, making pivot decisions, and finding product/market fit. This skill bridges the gap between methodology and measurement.

## What This Skill Does

### 1. Analytics Implementation
- Design tracking schemas for startup hypotheses
- Implement event tracking systems
- Set up databases for user behavior
- Create dashboards for key metrics
- Build data pipelines for analysis

### 2. Metrics Analysis
- Calculate Lean Startup metrics (AARRR, LTV, CAC, etc.)
- Perform cohort analysis
- Analyze retention and churn
- Statistical significance testing
- Growth accounting

### 3. Hypothesis Validation
- Translate business hypotheses into measurable metrics
- Design A/B tests and experiments
- Analyze experiment results
- Provide pivot/persevere recommendations
- Customer segmentation analysis

### 4. Data-Driven Advice
- Answer questions from lean-startup and steve-blank-adviser skills
- Provide data to support customer development decisions
- Identify patterns in user behavior
- Predict unit economics
- Forecast growth and runway

## Integration with Other Skills

This skill works in tandem with:
- **lean-startup skill:** Provides data for Build-Measure-Learn cycles
- **steve-blank-adviser skill:** Validates customer development hypotheses with data

**Example workflow:**
1. Steve Blank skill suggests customer interviews
2. You conduct interviews and track responses
3. Data scientist skill analyzes patterns in responses
4. Lean Startup skill uses data to design MVP
5. Data scientist skill tracks MVP metrics
6. All skills collaborate on pivot/persevere decision

---

## Part 1: Analytics Architecture

### The Startup Analytics Stack

**Phase 1: MVP Stage (<1,000 users)**
```
User Actions → Simple Event Log → Spreadsheet/Database → Manual Analysis
```

**Tools:**
- Event tracking: Custom PHP logging + MySQL
- Storage: Simple MySQL tables
- Analysis: Excel/Google Sheets + SQL queries
- Visualization: Google Sheets charts

**Phase 2: Growth Stage (1,000-10,000 users)**
```
User Actions → Event Tracking Library → Database → Analytics Dashboard
```

**Tools:**
- Event tracking: Mixpanel/Amplitude or custom
- Storage: PostgreSQL/MySQL
- Analysis: SQL queries + Python/R
- Visualization: Metabase/Redash or custom

**Phase 3: Scale Stage (10,000+ users)**
```
User Actions → Event Stream → Data Warehouse → BI Tools
```

**Tools:**
- Event tracking: Segment + Mixpanel/Amplitude
- Storage: Data warehouse (BigQuery/Snowflake)
- Analysis: SQL + Python + ML models
- Visualization: Tableau/Looker

### Essential Tracking Schema

Every startup should track these core entities:

#### 1. Users Table
```sql
CREATE TABLE users (
    user_id VARCHAR(36) PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    email VARCHAR(255),
    signup_source VARCHAR(50),
    utm_source VARCHAR(100),
    utm_medium VARCHAR(100),
    utm_campaign VARCHAR(100),
    customer_segment VARCHAR(50),
    activated BOOLEAN DEFAULT FALSE,
    activated_at TIMESTAMP,
    converted_to_paid BOOLEAN DEFAULT FALSE,
    converted_at TIMESTAMP,
    churned BOOLEAN DEFAULT FALSE,
    churned_at TIMESTAMP
);
```

#### 2. Events Table
```sql
CREATE TABLE events (
    event_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    event_name VARCHAR(100) NOT NULL,
    event_properties JSON,
    created_at TIMESTAMP NOT NULL,
    session_id VARCHAR(36),
    device_type VARCHAR(50),
    browser VARCHAR(50),
    country VARCHAR(2),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Index for fast queries
CREATE INDEX idx_events_user_date ON events(user_id, created_at);
CREATE INDEX idx_events_name_date ON events(event_name, created_at);
```

#### 3. Sessions Table
```sql
CREATE TABLE sessions (
    session_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    started_at TIMESTAMP NOT NULL,
    ended_at TIMESTAMP,
    duration_seconds INT,
    page_views INT DEFAULT 0,
    events_count INT DEFAULT 0,
    landing_page VARCHAR(255),
    exit_page VARCHAR(255),
    referrer VARCHAR(255)
);
```

#### 4. Experiments Table
```sql
CREATE TABLE experiments (
    experiment_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    hypothesis TEXT,
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    status VARCHAR(20) -- 'running', 'completed', 'stopped'
);

CREATE TABLE experiment_variants (
    variant_id VARCHAR(36) PRIMARY KEY,
    experiment_id VARCHAR(36),
    variant_name VARCHAR(50),
    description TEXT,
    FOREIGN KEY (experiment_id) REFERENCES experiments(experiment_id)
);

CREATE TABLE experiment_assignments (
    user_id VARCHAR(36),
    experiment_id VARCHAR(36),
    variant_id VARCHAR(36),
    assigned_at TIMESTAMP,
    PRIMARY KEY (user_id, experiment_id)
);
```

### Critical Events to Track

**For Lean Startup Metrics:**

```javascript
// Acquisition
trackEvent('user_signed_up', {
  source: 'google_ads',
  utm_campaign: 'spring_2024',
  landing_page: '/features'
});

// Activation
trackEvent('user_activated', {
  activation_action: 'completed_first_project',
  time_to_activation_minutes: 12
});

// Retention
trackEvent('user_returned', {
  days_since_signup: 7,
  return_session_number: 3
});

// Revenue
trackEvent('user_upgraded', {
  plan: 'pro',
  price: 49,
  billing_cycle: 'monthly'
});

// Referral
trackEvent('user_referred', {
  referral_method: 'email_invite',
  referred_user_id: 'user_xyz'
});
```

**For Customer Development:**

```javascript
// Problem validation
trackEvent('problem_survey_completed', {
  problem_severity: 8,
  current_solution: 'excel',
  willingness_to_pay: 'yes'
});

// Feature usage (validates solution)
trackEvent('feature_used', {
  feature_name: 'invoice_generator',
  usage_count: 1,
  time_spent_seconds: 120
});

// Customer feedback
trackEvent('feedback_submitted', {
  type: 'feature_request',
  sentiment: 'positive',
  text: '...'
});
```

---

## Part 2: Core Metrics Calculation

### Acquisition Metrics

#### 1. Conversion Rate by Channel

```sql
-- Signups by source
SELECT
    signup_source,
    COUNT(*) as signups,
    DATE(created_at) as date
FROM users
WHERE created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
GROUP BY signup_source, DATE(created_at)
ORDER BY date DESC, signups DESC;
```

#### 2. Customer Acquisition Cost (CAC)

```sql
-- CAC by channel (requires marketing spend data)
WITH channel_spend AS (
    SELECT channel, SUM(spend) as total_spend
    FROM marketing_spend
    WHERE month = '2024-01'
    GROUP BY channel
),
channel_signups AS (
    SELECT signup_source as channel, COUNT(*) as signups
    FROM users
    WHERE DATE_FORMAT(created_at, '%Y-%m') = '2024-01'
    GROUP BY signup_source
)
SELECT
    s.channel,
    s.total_spend,
    u.signups,
    ROUND(s.total_spend / u.signups, 2) as cac
FROM channel_spend s
JOIN channel_signups u ON s.channel = u.channel;
```

### Activation Metrics

#### 3. Activation Rate

```sql
-- Overall activation rate
SELECT
    COUNT(*) as total_signups,
    SUM(CASE WHEN activated = TRUE THEN 1 ELSE 0 END) as activated_users,
    ROUND(100.0 * SUM(CASE WHEN activated = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) as activation_rate_pct
FROM users
WHERE created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY);
```

#### 4. Time to Activation

```sql
-- Time to activation distribution
SELECT
    CASE
        WHEN TIMESTAMPDIFF(MINUTE, created_at, activated_at) <= 5 THEN '0-5 min'
        WHEN TIMESTAMPDIFF(MINUTE, created_at, activated_at) <= 15 THEN '5-15 min'
        WHEN TIMESTAMPDIFF(MINUTE, created_at, activated_at) <= 60 THEN '15-60 min'
        WHEN TIMESTAMPDIFF(HOUR, created_at, activated_at) <= 24 THEN '1-24 hours'
        ELSE '24+ hours'
    END as time_bucket,
    COUNT(*) as users,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as pct
FROM users
WHERE activated = TRUE
    AND created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
GROUP BY time_bucket
ORDER BY MIN(TIMESTAMPDIFF(MINUTE, created_at, activated_at));
```

### Retention Metrics

#### 5. Cohort Retention Analysis

```sql
-- Weekly retention cohorts
WITH cohorts AS (
    SELECT
        user_id,
        DATE_FORMAT(created_at, '%Y-%m-%d') as cohort_date,
        created_at
    FROM users
),
activity AS (
    SELECT DISTINCT
        user_id,
        DATE_FORMAT(created_at, '%Y-%m-%d') as activity_date
    FROM events
    WHERE event_name IN ('user_logged_in', 'feature_used', 'page_viewed')
)
SELECT
    c.cohort_date,
    COUNT(DISTINCT c.user_id) as cohort_size,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN DATEDIFF(a.activity_date, c.cohort_date) BETWEEN 0 AND 0 THEN a.user_id END) / COUNT(DISTINCT c.user_id), 2) as day_0,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN DATEDIFF(a.activity_date, c.cohort_date) BETWEEN 1 AND 1 THEN a.user_id END) / COUNT(DISTINCT c.user_id), 2) as day_1,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN DATEDIFF(a.activity_date, c.cohort_date) BETWEEN 7 AND 7 THEN a.user_id END) / COUNT(DISTINCT c.user_id), 2) as day_7,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN DATEDIFF(a.activity_date, c.cohort_date) BETWEEN 30 AND 30 THEN a.user_id END) / COUNT(DISTINCT c.user_id), 2) as day_30
FROM cohorts c
LEFT JOIN activity a ON c.user_id = a.user_id
WHERE c.created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 60 DAY)
GROUP BY c.cohort_date
ORDER BY c.cohort_date DESC;
```

#### 6. Churn Rate

```sql
-- Monthly churn rate
WITH monthly_active AS (
    SELECT
        DATE_FORMAT(created_at, '%Y-%m') as month,
        user_id
    FROM events
    WHERE created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 3 MONTH)
    GROUP BY DATE_FORMAT(created_at, '%Y-%m'), user_id
),
churned AS (
    SELECT
        m1.month,
        COUNT(DISTINCT m1.user_id) as active_start_of_month,
        COUNT(DISTINCT m2.user_id) as active_next_month,
        COUNT(DISTINCT m1.user_id) - COUNT(DISTINCT m2.user_id) as churned_users
    FROM monthly_active m1
    LEFT JOIN monthly_active m2
        ON m1.user_id = m2.user_id
        AND m2.month = DATE_FORMAT(DATE_ADD(STR_TO_DATE(CONCAT(m1.month, '-01'), '%Y-%m-%d'), INTERVAL 1 MONTH), '%Y-%m')
    GROUP BY m1.month
)
SELECT
    month,
    active_start_of_month,
    churned_users,
    ROUND(100.0 * churned_users / active_start_of_month, 2) as churn_rate_pct
FROM churned
ORDER BY month DESC;
```

### Revenue Metrics

#### 7. Conversion to Paid

```sql
-- Trial to paid conversion by cohort
SELECT
    DATE_FORMAT(created_at, '%Y-%m') as signup_month,
    COUNT(*) as total_signups,
    SUM(CASE WHEN converted_to_paid = TRUE THEN 1 ELSE 0 END) as converted,
    ROUND(100.0 * SUM(CASE WHEN converted_to_paid = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) as conversion_rate_pct,
    ROUND(AVG(CASE WHEN converted_to_paid = TRUE THEN DATEDIFF(converted_at, created_at) END), 1) as avg_days_to_convert
FROM users
WHERE created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 6 MONTH)
GROUP BY DATE_FORMAT(created_at, '%Y-%m')
ORDER BY signup_month DESC;
```

#### 8. Monthly Recurring Revenue (MRR)

```sql
-- MRR movements
WITH mrr_by_user AS (
    SELECT
        user_id,
        DATE_FORMAT(billing_date, '%Y-%m') as month,
        SUM(amount) as mrr
    FROM subscriptions
    WHERE status = 'active'
    GROUP BY user_id, DATE_FORMAT(billing_date, '%Y-%m')
),
previous_month AS (
    SELECT
        user_id,
        month,
        mrr,
        LAG(mrr) OVER (PARTITION BY user_id ORDER BY month) as prev_mrr
    FROM mrr_by_user
)
SELECT
    month,
    SUM(CASE WHEN prev_mrr IS NULL THEN mrr ELSE 0 END) as new_mrr,
    SUM(CASE WHEN mrr > prev_mrr THEN (mrr - prev_mrr) ELSE 0 END) as expansion_mrr,
    SUM(CASE WHEN mrr < prev_mrr THEN (prev_mrr - mrr) ELSE 0 END) as contraction_mrr,
    SUM(CASE WHEN mrr IS NULL AND prev_mrr IS NOT NULL THEN prev_mrr ELSE 0 END) as churned_mrr,
    SUM(mrr) as total_mrr
FROM previous_month
GROUP BY month
ORDER BY month DESC;
```

### Referral Metrics

#### 9. Viral Coefficient

```sql
-- Viral coefficient calculation
WITH referrals AS (
    SELECT
        referrer_user_id,
        COUNT(DISTINCT referred_user_id) as referred_count
    FROM referrals
    WHERE created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
    GROUP BY referrer_user_id
)
SELECT
    COUNT(DISTINCT r.referrer_user_id) as users_who_referred,
    SUM(r.referred_count) as total_referrals,
    ROUND(AVG(r.referred_count), 2) as avg_referrals_per_user,
    -- Viral coefficient = invites sent × conversion rate
    ROUND(AVG(r.referred_count) *
        (SUM(r.referred_count)::float /
        (SELECT COUNT(*) FROM referrals WHERE created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY))), 2
    ) as viral_coefficient
FROM referrals r;
```

---

## Part 3: Analysis Frameworks

### Framework 1: Hypothesis Testing

**Template for validating startup hypotheses:**

```
HYPOTHESIS: [Statement to test]
NULL HYPOTHESIS: [Opposite statement]
METRIC: [What to measure]
TEST: [How to measure it]
SAMPLE SIZE: [Minimum users needed]
SIGNIFICANCE LEVEL: [Usually p < 0.05]
DURATION: [How long to run test]
```

**Example:**

```
HYPOTHESIS: Adding onboarding tutorial will increase activation rate from 40% to 50%
NULL HYPOTHESIS: Tutorial has no effect on activation
METRIC: Activation rate (% who complete first core action)
TEST: A/B test - 50% see tutorial, 50% don't
SAMPLE SIZE: Minimum 385 users per variant (for 80% power)
SIGNIFICANCE LEVEL: p < 0.05
DURATION: 2 weeks or until sample size reached
```

**Statistical Significance SQL:**

```sql
-- A/B test results with statistical significance
WITH variant_results AS (
    SELECT
        ea.variant_name,
        COUNT(DISTINCT ea.user_id) as users,
        SUM(CASE WHEN u.activated = TRUE THEN 1 ELSE 0 END) as conversions,
        ROUND(100.0 * SUM(CASE WHEN u.activated = TRUE THEN 1 ELSE 0 END) / COUNT(DISTINCT ea.user_id), 2) as conversion_rate
    FROM experiment_assignments ea
    JOIN users u ON ea.user_id = u.user_id
    WHERE ea.experiment_id = 'onboarding_tutorial_test'
    GROUP BY ea.variant_name
)
SELECT
    variant_name,
    users,
    conversions,
    conversion_rate,
    -- Chi-square test would be computed in application layer
    CASE
        WHEN users < 100 THEN 'Insufficient sample size'
        ELSE 'Use chi-square test for significance'
    END as statistical_note
FROM variant_results;
```

### Framework 2: Cohort Analysis

**Purpose:** Track how groups of users behave over time

**Key Questions:**
- Are newer cohorts performing better? (Product improving)
- Where is retention curve flattening? (Core user base)
- Which cohorts have best LTV? (Target similar users)

**Advanced Cohort Query:**

```sql
-- Cohort retention with revenue
WITH cohorts AS (
    SELECT
        user_id,
        DATE_FORMAT(created_at, '%Y-W%u') as cohort_week,
        created_at
    FROM users
),
weekly_activity AS (
    SELECT
        user_id,
        DATE_FORMAT(created_at, '%Y-W%u') as activity_week,
        COUNT(*) as actions
    FROM events
    WHERE event_name IN ('feature_used', 'page_viewed')
    GROUP BY user_id, DATE_FORMAT(created_at, '%Y-W%u')
),
weekly_revenue AS (
    SELECT
        user_id,
        DATE_FORMAT(payment_date, '%Y-W%u') as revenue_week,
        SUM(amount) as revenue
    FROM payments
    GROUP BY user_id, DATE_FORMAT(payment_date, '%Y-W%u')
)
SELECT
    c.cohort_week,
    COUNT(DISTINCT c.user_id) as cohort_size,
    -- Retention
    COUNT(DISTINCT CASE WHEN wa.activity_week = c.cohort_week THEN wa.user_id END) as week_0_active,
    COUNT(DISTINCT CASE WHEN WEEK(STR_TO_DATE(CONCAT(wa.activity_week, '-1'), '%Y-W%u-%w')) = WEEK(c.created_at) + 1 THEN wa.user_id END) as week_1_active,
    -- Revenue
    SUM(CASE WHEN wr.revenue_week = c.cohort_week THEN wr.revenue ELSE 0 END) as week_0_revenue,
    SUM(wr.revenue) as total_revenue,
    ROUND(SUM(wr.revenue) / COUNT(DISTINCT c.user_id), 2) as revenue_per_user
FROM cohorts c
LEFT JOIN weekly_activity wa ON c.user_id = wa.user_id
LEFT JOIN weekly_revenue wr ON c.user_id = wr.user_id
GROUP BY c.cohort_week
ORDER BY c.cohort_week DESC
LIMIT 12;
```

### Framework 3: Funnel Analysis

**Purpose:** Identify where users drop off in key workflows

```sql
-- Signup to activation funnel
WITH funnel_steps AS (
    SELECT
        u.user_id,
        u.created_at as step_1_signup,
        MIN(CASE WHEN e.event_name = 'profile_completed' THEN e.created_at END) as step_2_profile,
        MIN(CASE WHEN e.event_name = 'first_action_completed' THEN e.created_at END) as step_3_first_action,
        u.activated_at as step_4_activated
    FROM users u
    LEFT JOIN events e ON u.user_id = e.user_id
    WHERE u.created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 7 DAY)
    GROUP BY u.user_id, u.created_at, u.activated_at
)
SELECT
    COUNT(*) as step_1_signups,
    COUNT(step_2_profile) as step_2_completed,
    COUNT(step_3_first_action) as step_3_completed,
    COUNT(step_4_activated) as step_4_completed,
    -- Conversion rates
    ROUND(100.0 * COUNT(step_2_profile) / COUNT(*), 2) as signup_to_profile_pct,
    ROUND(100.0 * COUNT(step_3_first_action) / COUNT(step_2_profile), 2) as profile_to_action_pct,
    ROUND(100.0 * COUNT(step_4_activated) / COUNT(step_3_first_action), 2) as action_to_activated_pct,
    ROUND(100.0 * COUNT(step_4_activated) / COUNT(*), 2) as overall_conversion_pct
FROM funnel_steps;
```

### Framework 4: Segmentation Analysis

**Purpose:** Identify which customer segments perform best

```sql
-- Performance by customer segment
SELECT
    u.customer_segment,
    COUNT(DISTINCT u.user_id) as users,
    ROUND(100.0 * SUM(CASE WHEN u.activated = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) as activation_rate,
    ROUND(100.0 * SUM(CASE WHEN u.converted_to_paid = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) as conversion_rate,
    ROUND(AVG(CASE WHEN u.converted_to_paid = TRUE THEN DATEDIFF(u.converted_at, u.created_at) END), 1) as avg_days_to_convert,
    ROUND(SUM(p.amount) / COUNT(DISTINCT u.user_id), 2) as revenue_per_user
FROM users u
LEFT JOIN payments p ON u.user_id = p.user_id
WHERE u.created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 90 DAY)
GROUP BY u.customer_segment
ORDER BY revenue_per_user DESC;
```

---

## Part 4: Implementation Guides

### PHP Implementation for Event Tracking

**IMPORTANT - Project Logging Structure:**
- **All log files** must be stored in the `/_logs/` directory
- **The logging function** is centralized in `_fun/function_logs.php`
- **Always use** the centralized logging function for consistency across the application

**Simple Event Logger:**

```php
<?php
// config/database.php
class Database {
    private static $instance = null;
    private $conn;

    private function __construct() {
        $this->conn = new PDO(
            "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME,
            DB_USER,
            DB_PASS
        );
        $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }

    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new Database();
        }
        return self::$instance;
    }

    public function getConnection() {
        return $this->conn;
    }
}

// classes/Analytics.php
class Analytics {
    private $db;

    public function __construct() {
        $this->db = Database::getInstance()->getConnection();
    }

    /**
     * Track an event
     */
    public function trackEvent($userId, $eventName, $properties = [], $sessionId = null) {
        $sql = "INSERT INTO events (event_id, user_id, event_name, event_properties, created_at, session_id, device_type, browser, country)
                VALUES (:event_id, :user_id, :event_name, :properties, NOW(), :session_id, :device_type, :browser, :country)";

        $stmt = $this->db->prepare($sql);
        $stmt->execute([
            'event_id' => $this->generateUUID(),
            'user_id' => $userId,
            'event_name' => $eventName,
            'properties' => json_encode($properties),
            'session_id' => $sessionId ?? $this->getSessionId(),
            'device_type' => $this->getDeviceType(),
            'browser' => $this->getBrowser(),
            'country' => $this->getCountry()
        ]);
    }

    /**
     * Track user signup
     */
    public function trackSignup($email, $source, $utmParams = []) {
        // Create user
        $userId = $this->generateUUID();
        $sql = "INSERT INTO users (user_id, created_at, email, signup_source, utm_source, utm_medium, utm_campaign)
                VALUES (:user_id, NOW(), :email, :source, :utm_source, :utm_medium, :utm_campaign)";

        $stmt = $this->db->prepare($sql);
        $stmt->execute([
            'user_id' => $userId,
            'email' => $email,
            'source' => $source,
            'utm_source' => $utmParams['utm_source'] ?? null,
            'utm_medium' => $utmParams['utm_medium'] ?? null,
            'utm_campaign' => $utmParams['utm_campaign'] ?? null
        ]);

        // Track signup event
        $this->trackEvent($userId, 'user_signed_up', [
            'source' => $source,
            'utm_campaign' => $utmParams['utm_campaign'] ?? null
        ]);

        return $userId;
    }

    /**
     * Mark user as activated
     */
    public function markActivated($userId, $activationAction) {
        $sql = "UPDATE users SET activated = TRUE, activated_at = NOW() WHERE user_id = :user_id AND activated = FALSE";
        $stmt = $this->db->prepare($sql);
        $stmt->execute(['user_id' => $userId]);

        $this->trackEvent($userId, 'user_activated', [
            'activation_action' => $activationAction
        ]);
    }

    /**
     * Track page view
     */
    public function trackPageView($userId, $page, $referrer = null) {
        $this->trackEvent($userId, 'page_viewed', [
            'page' => $page,
            'referrer' => $referrer,
            'url' => $_SERVER['REQUEST_URI'] ?? ''
        ]);
    }

    /**
     * Start a new session
     */
    public function startSession($userId = null) {
        $sessionId = $this->generateUUID();
        $_SESSION['analytics_session_id'] = $sessionId;
        $_SESSION['analytics_session_start'] = time();

        $sql = "INSERT INTO sessions (session_id, user_id, started_at, landing_page, referrer)
                VALUES (:session_id, :user_id, NOW(), :landing_page, :referrer)";

        $stmt = $this->db->prepare($sql);
        $stmt->execute([
            'session_id' => $sessionId,
            'user_id' => $userId,
            'landing_page' => $_SERVER['REQUEST_URI'] ?? '',
            'referrer' => $_SERVER['HTTP_REFERER'] ?? null
        ]);

        return $sessionId;
    }

    /**
     * End session
     */
    public function endSession() {
        $sessionId = $this->getSessionId();
        if ($sessionId) {
            $duration = time() - ($_SESSION['analytics_session_start'] ?? time());

            $sql = "UPDATE sessions SET ended_at = NOW(), duration_seconds = :duration, exit_page = :exit_page
                    WHERE session_id = :session_id";

            $stmt = $this->db->prepare($sql);
            $stmt->execute([
                'duration' => $duration,
                'exit_page' => $_SERVER['REQUEST_URI'] ?? '',
                'session_id' => $sessionId
            ]);
        }
    }

    // Helper methods
    private function generateUUID() {
        return sprintf('%04x%04x-%04x-%04x-%04x-%04x%04x%04x',
            mt_rand(0, 0xffff), mt_rand(0, 0xffff),
            mt_rand(0, 0xffff),
            mt_rand(0, 0x0fff) | 0x4000,
            mt_rand(0, 0x3fff) | 0x8000,
            mt_rand(0, 0xffff), mt_rand(0, 0xffff), mt_rand(0, 0xffff)
        );
    }

    private function getSessionId() {
        return $_SESSION['analytics_session_id'] ?? null;
    }

    private function getDeviceType() {
        $userAgent = $_SERVER['HTTP_USER_AGENT'] ?? '';
        if (preg_match('/mobile/i', $userAgent)) return 'mobile';
        if (preg_match('/tablet/i', $userAgent)) return 'tablet';
        return 'desktop';
    }

    private function getBrowser() {
        $userAgent = $_SERVER['HTTP_USER_AGENT'] ?? '';
        if (strpos($userAgent, 'Chrome') !== false) return 'Chrome';
        if (strpos($userAgent, 'Firefox') !== false) return 'Firefox';
        if (strpos($userAgent, 'Safari') !== false) return 'Safari';
        if (strpos($userAgent, 'Edge') !== false) return 'Edge';
        return 'Other';
    }

    private function getCountry() {
        // In production, use GeoIP database or service
        return 'US'; // Default
    }
}
```

**Usage Example:**

```php
<?php
// In your application code
require_once '_fun/function_logs.php'; // ALWAYS include the centralized logging function
require_once 'classes/Analytics.php';

$analytics = new Analytics();

// Track signup
if ($_POST['action'] == 'signup') {
    $userId = $analytics->trackSignup(
        $_POST['email'],
        'web_form',
        [
            'utm_source' => $_GET['utm_source'] ?? null,
            'utm_medium' => $_GET['utm_medium'] ?? null,
            'utm_campaign' => $_GET['utm_campaign'] ?? null
        ]
    );

    $_SESSION['user_id'] = $userId;
}

// Track page views
$analytics->trackPageView(
    $_SESSION['user_id'] ?? null,
    $_SERVER['REQUEST_URI'],
    $_SERVER['HTTP_REFERER'] ?? null
);

// Track activation
if ($userCompletedFirstAction) {
    $analytics->markActivated($_SESSION['user_id'], 'completed_first_invoice');
}

// Track custom events
$analytics->trackEvent($_SESSION['user_id'], 'invoice_created', [
    'amount' => $invoiceAmount,
    'currency' => 'USD',
    'client_name' => $clientName
]);
?>
```

---

## Part 5: Reporting & Dashboards

### Daily Metrics Dashboard (SQL Views)

```sql
-- Create view for daily dashboard
CREATE OR REPLACE VIEW daily_metrics AS
SELECT
    DATE(created_at) as date,
    -- Acquisition
    COUNT(DISTINCT CASE WHEN table_name = 'users' THEN id END) as new_signups,
    -- Activation
    COUNT(DISTINCT CASE WHEN activated = TRUE AND DATE(activated_at) = DATE(created_at) THEN user_id END) as activated_same_day,
    -- Engagement
    COUNT(DISTINCT CASE WHEN event_name IN ('feature_used', 'page_viewed') THEN user_id END) as active_users,
    -- Revenue
    SUM(CASE WHEN event_name = 'payment_completed' THEN JSON_EXTRACT(event_properties, '$.amount') ELSE 0 END) as revenue
FROM (
    SELECT user_id, created_at, activated, activated_at, NULL as event_name, NULL as event_properties, 'users' as table_name, user_id as id FROM users
    UNION ALL
    SELECT user_id, created_at, NULL as activated, NULL as activated_at, event_name, event_properties, 'events' as table_name, event_id as id FROM events
) combined
GROUP BY DATE(created_at);
```

### Weekly Executive Summary

```sql
-- Weekly summary for leadership
SELECT
    DATE_FORMAT(created_at, '%Y-W%u') as week,
    COUNT(DISTINCT CASE WHEN u.user_id IS NOT NULL THEN u.user_id END) as new_users,
    COUNT(DISTINCT CASE WHEN u.activated = TRUE THEN u.user_id END) as activated_users,
    COUNT(DISTINCT CASE WHEN u.converted_to_paid = TRUE THEN u.user_id END) as paid_users,
    COUNT(DISTINCT e.user_id) as active_users,
    SUM(CASE WHEN p.amount IS NOT NULL THEN p.amount ELSE 0 END) as total_revenue,
    ROUND(AVG(CASE WHEN u.converted_to_paid = TRUE THEN DATEDIFF(u.converted_at, u.created_at) END), 1) as avg_days_to_convert
FROM users u
LEFT JOIN events e ON u.user_id = e.user_id AND DATE_FORMAT(e.created_at, '%Y-W%u') = DATE_FORMAT(u.created_at, '%Y-W%u')
LEFT JOIN payments p ON u.user_id = p.user_id AND DATE_FORMAT(p.payment_date, '%Y-W%u') = DATE_FORMAT(u.created_at, '%Y-W%u')
WHERE u.created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 12 WEEK)
GROUP BY DATE_FORMAT(created_at, '%Y-W%u')
ORDER BY week DESC;
```

---

## Part 6: Providing Insights

### How to Answer Common Questions

#### "Should we pivot or persevere?"

**Data to analyze:**
1. **Retention curve:** Is it flattening or declining?
2. **Cohort trends:** Are newer cohorts better or worse?
3. **Conversion rates:** Improving or plateaued?
4. **Engagement:** Are activated users using product regularly?

**SQL to run:**
```sql
-- Trend analysis for pivot decision
WITH monthly_metrics AS (
    SELECT
        DATE_FORMAT(created_at, '%Y-%m') as month,
        COUNT(*) as signups,
        ROUND(100.0 * SUM(CASE WHEN activated = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) as activation_rate,
        ROUND(100.0 * SUM(CASE WHEN converted_to_paid = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) as conversion_rate
    FROM users
    GROUP BY DATE_FORMAT(created_at, '%Y-%m')
)
SELECT
    *,
    LAG(activation_rate) OVER (ORDER BY month) as prev_activation_rate,
    activation_rate - LAG(activation_rate) OVER (ORDER BY month) as activation_change
FROM monthly_metrics
ORDER BY month DESC
LIMIT 6;
```

**Recommendation framework:**
- **Persevere if:** Metrics improving month-over-month, retention curve flattening
- **Pivot if:** Metrics flat/declining for 3+ months, retention curve keeps dropping

#### "Which customer segment should we focus on?"

```sql
-- Segment performance comparison
SELECT
    customer_segment,
    COUNT(*) as users,
    ROUND(100.0 * SUM(CASE WHEN activated = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) as activation_rate,
    ROUND(100.0 * SUM(CASE WHEN converted_to_paid = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) as conversion_rate,
    ROUND(AVG(days_active), 1) as avg_days_active,
    ROUND(SUM(total_revenue) / COUNT(*), 2) as revenue_per_user,
    -- Calculate LTV/CAC if CAC data available
    ROUND(SUM(total_revenue) / SUM(acquisition_cost), 2) as ltv_cac_ratio
FROM (
    SELECT
        u.user_id,
        u.customer_segment,
        u.activated,
        u.converted_to_paid,
        DATEDIFF(COALESCE(u.churned_at, CURRENT_DATE), u.created_at) as days_active,
        COALESCE(SUM(p.amount), 0) as total_revenue,
        100 as acquisition_cost -- Replace with actual CAC
    FROM users u
    LEFT JOIN payments p ON u.user_id = p.user_id
    GROUP BY u.user_id
) user_metrics
GROUP BY customer_segment
ORDER BY revenue_per_user DESC;
```

**Recommendation:** Focus on segment with highest LTV/CAC ratio and good activation rate.

#### "Is our MVP working?"

**Key metrics to check:**
1. **Activation rate:** >40% is good for B2B, >25% for B2C
2. **Day 1 retention:** >40% is good
3. **Day 7 retention:** >20% is good
4. **Willingness to pay:** >10% trial-to-paid conversion

```sql
-- MVP health check
SELECT
    'Activation Rate' as metric,
    ROUND(100.0 * SUM(CASE WHEN activated = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) as value,
    CASE
        WHEN ROUND(100.0 * SUM(CASE WHEN activated = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) >= 40 THEN '✓ Good'
        WHEN ROUND(100.0 * SUM(CASE WHEN activated = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) >= 25 THEN '→ Acceptable'
        ELSE '✗ Needs work'
    END as assessment
FROM users
WHERE created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)

UNION ALL

SELECT
    'Conversion Rate' as metric,
    ROUND(100.0 * SUM(CASE WHEN converted_to_paid = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) as value,
    CASE
        WHEN ROUND(100.0 * SUM(CASE WHEN converted_to_paid = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) >= 10 THEN '✓ Good'
        WHEN ROUND(100.0 * SUM(CASE WHEN converted_to_paid = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) >= 5 THEN '→ Acceptable'
        ELSE '✗ Needs work'
    END as assessment
FROM users
WHERE created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 90 DAY);
```

---

## Summary

This skill provides:
1. **Tracking infrastructure:** Database schemas and PHP implementation
2. **Core metrics:** SQL queries for all Lean Startup and Customer Development metrics
3. **Analysis frameworks:** Cohort analysis, funnel analysis, hypothesis testing
4. **Insights:** Data-driven recommendations for pivot/persevere decisions
5. **Integration:** Works with lean-startup and steve-blank-adviser skills

**Remember:** Data without action is just numbers. Use these insights to make decisions, run experiments, and find product/market fit faster.

---

*"Without data, you're just another person with an opinion."* - W. Edwards Deming