---
name: executive-dashboard
description: Эксперт executive dashboards. Используй для KPI визуализации, business intelligence и reporting.
---

# Executive Dashboard Expert

Expert in designing and building executive dashboards that deliver actionable insights to C-level executives and senior leadership.

## Core Dashboard Principles

### Strategic Focus
- Lead with business outcomes, not data points
- Align KPIs directly to company objectives and strategic initiatives
- Prioritize forward-looking metrics over historical reporting
- Enable drill-down capabilities without overwhelming the main view
- Design for mobile and presentation contexts

### Information Hierarchy
- Follow the "5-second rule" - key insights visible immediately
- Use progressive disclosure: summary → trends → details
- Implement the "traffic light" system for status indicators
- Group related metrics into coherent business themes
- Maintain consistent terminology across all metrics

## Essential KPI Categories

### Financial Performance

```javascript
const financialKPIs = {
  revenue: {
    current: 'Monthly Recurring Revenue (MRR)',
    trend: 'Revenue Growth Rate (YoY)',
    health: 'Revenue per Employee',
    forecast: 'Pipeline Value & Conversion Rate'
  },
  profitability: {
    margin: 'Gross Margin %',
    efficiency: 'Operating Expense Ratio',
    cash: 'Cash Flow & Burn Rate',
    roi: 'Return on Investment by Initiative'
  },
  unit_economics: {
    cac: 'Customer Acquisition Cost',
    ltv: 'Customer Lifetime Value',
    ltv_cac_ratio: 'LTV:CAC Ratio (target: 3:1)',
    payback: 'CAC Payback Period'
  }
};
```

### Operational Excellence

```javascript
const operationalKPIs = {
  customers: {
    acquisition: 'Customer Acquisition Cost (CAC)',
    retention: 'Net Revenue Retention (NRR)',
    satisfaction: 'Net Promoter Score (NPS)',
    lifetime: 'Customer Lifetime Value (CLV)',
    churn: 'Monthly/Annual Churn Rate'
  },
  performance: {
    quality: 'Defect Rate & SLA Performance',
    speed: 'Time to Market & Cycle Time',
    capacity: 'Utilization Rates & Capacity Planning'
  },
  growth: {
    pipeline: 'Sales Pipeline Coverage',
    conversion: 'Stage Conversion Rates',
    velocity: 'Deal Velocity'
  }
};
```

## Dashboard Layout Patterns

### Executive Summary Layout

```html
<!-- Top-level executive view -->
<div class="executive-dashboard">
  <!-- Hero Metrics (top 20% of screen) -->
  <section class="hero-metrics">
    <div class="primary-kpi">Revenue: $2.3M ↗️ 12%</div>
    <div class="status-indicators">
      <span class="green">Growth</span>
      <span class="yellow">Margins</span>
      <span class="red">Churn</span>
    </div>
  </section>

  <!-- Key Trends (middle 60%) -->
  <section class="trend-charts">
    <div class="chart-grid">
      <chart type="line" data="revenue-trend" period="12mo"/>
      <chart type="gauge" data="nps-score" target="50"/>
      <chart type="funnel" data="sales-pipeline"/>
      <chart type="heatmap" data="regional-performance"/>
    </div>
  </section>

  <!-- Action Items (bottom 20%) -->
  <section class="action-items">
    <alert type="critical">Customer churn up 3% - immediate action required</alert>
    <insight>Marketing ROI improved 24% - scale successful campaigns</insight>
  </section>
</div>
```

### CSS Grid Layout

```css
.executive-dashboard {
  display: grid;
  grid-template-areas:
    "hero hero hero hero"
    "chart1 chart1 chart2 chart2"
    "chart3 chart4 chart5 chart6"
    "alerts alerts insights insights";
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: auto 1fr 1fr auto;
  gap: 24px;
  padding: 24px;
  min-height: 100vh;
}

.hero-metrics {
  grid-area: hero;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #1a365d 0%, #2d3748 100%);
  border-radius: 12px;
  padding: 32px;
}

.primary-kpi {
  font-size: 48px;
  font-weight: 700;
  color: white;
}

.status-indicator {
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
}

.status-indicator.green { background: #48bb78; }
.status-indicator.yellow { background: #ecc94b; color: #1a202c; }
.status-indicator.red { background: #f56565; }
```

## Data Visualization Best Practices

### Chart Selection Guidelines

```python
def select_chart_type(data_type, purpose):
    chart_mapping = {
        ('trend', 'time_series'): 'line_chart',
        ('comparison', 'categories'): 'bar_chart',
        ('part_to_whole', 'composition'): 'donut_chart',
        ('performance', 'target'): 'gauge_chart',
        ('correlation', 'scatter'): 'scatter_plot',
        ('geographic', 'regional'): 'choropleth_map',
        ('process', 'conversion'): 'funnel_chart',
        ('distribution', 'variance'): 'box_plot',
        ('ranking', 'top_n'): 'horizontal_bar',
        ('change', 'waterfall'): 'waterfall_chart'
    }
    return chart_mapping.get((data_type, purpose), 'table')

# Executive dashboard color palette
EXEC_COLORS = {
    'success': '#00A86B',    # Green - targets met/exceeded
    'warning': '#FFB000',    # Amber - attention needed
    'critical': '#D2222D',   # Red - immediate action required
    'neutral': '#708090',    # Gray - informational
    'primary': '#1f4e79',    # Navy - brand/emphasis
    'secondary': '#4a5568',  # Dark gray - secondary elements
    'background': '#f7fafc'  # Light gray - backgrounds
}
```

### Interactive Elements

```javascript
class ExecutiveDashboard {
  constructor() {
    this.filters = {
      timeframe: 'YTD',
      region: 'All',
      business_unit: 'All'
    };
    this.alertThresholds = {
      revenue_variance: 0.05,
      customer_churn: 0.02,
      margin_decline: 0.03
    };
  }

  // Auto-refresh critical metrics
  setupRealTimeUpdates() {
    setInterval(() => {
      this.updateMetrics(['revenue', 'active_users', 'system_health']);
      this.checkAlertConditions();
    }, 300000); // 5-minute intervals
  }

  // Contextual drill-downs
  enableDrillDown(metric, level = 'summary') {
    const drillPaths = {
      'revenue': ['total', 'by_product', 'by_region', 'by_customer'],
      'churn': ['rate', 'by_segment', 'by_reason', 'cohort_analysis'],
      'pipeline': ['total', 'by_stage', 'by_rep', 'by_source']
    };
    return drillPaths[metric] || ['summary'];
  }

  // Export for board presentations
  exportToPDF() {
    return {
      format: 'landscape',
      pages: ['executive_summary', 'financial', 'operational'],
      branding: true,
      timestamp: new Date().toISOString()
    };
  }
}
```

## Executive Communication Features

### Automated Insights

```python
def generate_executive_insights(metrics_data):
    insights = []

    # Trend analysis
    if metrics_data['revenue_growth'] > 0.15:
        insights.append({
            'type': 'opportunity',
            'message': f"Revenue accelerating at {metrics_data['revenue_growth']:.1%} - consider scaling successful initiatives",
            'action': 'Review top-performing channels for expansion'
        })

    # Anomaly detection
    if abs(metrics_data['current_vs_forecast']) > 0.1:
        insights.append({
            'type': 'alert',
            'message': 'Significant variance from forecast detected',
            'impact': 'May affect quarterly targets',
            'next_steps': 'Schedule forecast review meeting'
        })

    # Churn warning
    if metrics_data['churn_rate'] > metrics_data['churn_threshold']:
        insights.append({
            'type': 'critical',
            'message': f"Churn rate at {metrics_data['churn_rate']:.1%} exceeds threshold",
            'impact': f"Potential ARR loss: ${metrics_data['at_risk_arr']:,.0f}",
            'next_steps': 'Activate retention playbook'
        })

    return sorted(insights, key=lambda x: {'critical': 0, 'alert': 1, 'opportunity': 2}[x['type']])
```

### Board Presentation Export

```javascript
// Board presentation export
function exportToBoardDeck() {
  const slideTemplates = {
    'executive_summary': {
      layout: 'hero_metrics_with_trend',
      charts: ['revenue_trend', 'key_kpis_table'],
      insights: 'auto_generated'
    },
    'financial_performance': {
      layout: 'financial_grid',
      charts: ['revenue_waterfall', 'margin_analysis', 'cash_flow'],
      commentary: 'variance_explanation'
    },
    'operational_highlights': {
      layout: 'balanced_scorecard',
      charts: ['customer_metrics', 'efficiency_trends'],
      actions: 'priority_initiatives'
    },
    'forward_look': {
      layout: 'forecast_view',
      charts: ['pipeline_coverage', 'growth_projections'],
      risks: 'risk_register_summary'
    }
  };

  return generatePresentation(slideTemplates);
}
```

## Performance and Scalability

### Data Refresh Strategy

```sql
-- Executive dashboard data mart optimization
CREATE MATERIALIZED VIEW executive_kpis_daily AS
SELECT
    date_key,
    SUM(revenue) as total_revenue,
    COUNT(DISTINCT customer_id) as active_customers,
    AVG(satisfaction_score) as avg_nps,
    SUM(revenue) / COUNT(DISTINCT customer_id) as revenue_per_customer,
    SUM(CASE WHEN is_churned THEN arr ELSE 0 END) as churned_arr,
    SUM(CASE WHEN is_new THEN arr ELSE 0 END) as new_arr
FROM fact_daily_metrics
WHERE date_key >= CURRENT_DATE - INTERVAL '2 years'
GROUP BY date_key;

-- Create index for fast filtering
CREATE INDEX idx_exec_kpis_date ON executive_kpis_daily(date_key);

-- Refresh every 4 hours for near real-time executive view
SELECT cron.schedule('refresh-exec-dashboard', '0 */4 * * *',
    'REFRESH MATERIALIZED VIEW CONCURRENTLY executive_kpis_daily;');
```

### Caching Strategy

```javascript
const cacheConfig = {
  // Hero metrics - most viewed, short cache
  heroMetrics: {
    ttl: 300,  // 5 minutes
    preload: true
  },

  // Trend charts - moderate cache
  trendCharts: {
    ttl: 900,  // 15 minutes
    preload: false
  },

  // Historical data - long cache
  historicalData: {
    ttl: 3600,  // 1 hour
    preload: false
  },

  // Real-time metrics - no cache
  realTimeMetrics: {
    ttl: 0,
    streaming: true
  }
};
```

## Mobile Optimization

```css
/* Mobile-first executive dashboard */
@media (max-width: 768px) {
  .executive-dashboard {
    grid-template-areas:
      "hero"
      "chart1"
      "chart2"
      "alerts";
    grid-template-columns: 1fr;
    padding: 16px;
  }

  .primary-kpi {
    font-size: 32px;
  }

  .chart-container {
    min-height: 200px;
  }

  /* Touch-friendly controls */
  .filter-button {
    min-height: 44px;
    min-width: 44px;
  }
}
```

## Testing and Validation

### Dashboard Quality Checklist

- **5-Second Test**: Key insights visible immediately upon load
- **Mobile Compatibility**: Readable on executive mobile devices
- **Data Accuracy**: Automated validation against source systems
- **Performance**: < 3 second load times for all views
- **Accessibility**: Color-blind friendly palette and screen reader support
- **Stakeholder Validation**: Monthly review sessions with dashboard users

### Automated Testing

```python
def test_dashboard_accuracy():
    """Compare dashboard values to source systems."""

    dashboard_revenue = get_dashboard_metric('total_revenue')
    source_revenue = query_source_system('SELECT SUM(amount) FROM orders')

    variance = abs(dashboard_revenue - source_revenue) / source_revenue

    assert variance < 0.001, f"Revenue variance {variance:.2%} exceeds threshold"
```

## Лучшие практики

1. **5-second rule** — ключевые метрики видны сразу
2. **Progressive disclosure** — от общего к деталям
3. **Mobile-first** — работает на телефоне CEO
4. **Real-time where needed** — критичные метрики обновляются часто
5. **Actionable insights** — не просто данные, а рекомендации
6. **Consistent design** — единый визуальный язык
