---
name: Cost Optimization Analyzer
description: This skill should be used when the user asks to "analyze costs", "optimize infrastructure spending", "reduce operational expenses", "monitor API costs", "audit cloud resources", "optimize database queries", or needs comprehensive cost analysis and optimization recommendations.
version: 1.0.0
---

# Cost Optimization Analyzer: ROI-Driven Infrastructure & Development Cost Management

## Overview

The Cost Optimization Analyzer provides comprehensive cost analysis, monitoring, and optimization recommendations across infrastructure, development, and operational expenses. This skill helps maximize ROI by identifying cost reduction opportunities and automating expense tracking.

## Core Cost Analysis Areas

### 1. Infrastructure Cost Analysis

**Railway/Cloud Infrastructure Monitoring:**
- Resource usage optimization (CPU, memory, storage)
- Database connection pooling efficiency
- Auto-scaling configuration analysis
- Traffic pattern analysis for right-sizing

**Cost Tracking Dashboard:**
```python
# Cost monitoring implementation
import psutil
import time
from datetime import datetime, timedelta

class InfrastructureCostAnalyzer:
    def __init__(self):
        self.cost_metrics = {
            'cpu_hours': 0,
            'memory_gb_hours': 0,
            'storage_gb': 0,
            'api_calls': 0,
            'database_queries': 0
        }

    def analyze_resource_usage(self):
        """Analyze current resource consumption patterns"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return {
            'cpu_utilization': cpu_percent,
            'memory_usage_gb': memory.used / (1024**3),
            'storage_used_gb': disk.used / (1024**3),
            'efficiency_score': self._calculate_efficiency_score(cpu_percent, memory.percent)
        }

    def _calculate_efficiency_score(self, cpu, memory):
        """Calculate resource efficiency score (0-100)"""
        # Optimal range: 60-80% utilization
        ideal_utilization = 70
        cpu_efficiency = 100 - abs(cpu - ideal_utilization)
        memory_efficiency = 100 - abs(memory - ideal_utilization)
        return (cpu_efficiency + memory_efficiency) / 2
```

### 2. Database Query Optimization

**Query Performance Analysis:**
```python
import time
import logging
from functools import wraps

class QueryCostAnalyzer:
    def __init__(self):
        self.query_metrics = {}
        self.cost_threshold_ms = 100  # Alert if query takes >100ms

    def monitor_query_cost(self, query_name):
        """Decorator to monitor query execution time and frequency"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = (time.time() - start_time) * 1000

                if query_name not in self.query_metrics:
                    self.query_metrics[query_name] = {
                        'total_executions': 0,
                        'total_time_ms': 0,
                        'avg_time_ms': 0,
                        'slow_queries': 0
                    }

                metrics = self.query_metrics[query_name]
                metrics['total_executions'] += 1
                metrics['total_time_ms'] += execution_time
                metrics['avg_time_ms'] = metrics['total_time_ms'] / metrics['total_executions']

                if execution_time > self.cost_threshold_ms:
                    metrics['slow_queries'] += 1
                    logging.warning(f"Slow query detected: {query_name} took {execution_time:.2f}ms")

                return result
            return wrapper
        return decorator

    def get_optimization_recommendations(self):
        """Generate query optimization recommendations"""
        recommendations = []

        for query_name, metrics in self.query_metrics.items():
            slow_query_ratio = metrics['slow_queries'] / metrics['total_executions']

            if slow_query_ratio > 0.1:  # >10% of queries are slow
                recommendations.append({
                    'query': query_name,
                    'issue': 'High slow query ratio',
                    'impact': 'Database performance degradation',
                    'recommendation': 'Add database indexes or optimize query structure',
                    'potential_cost_saving': f"${metrics['avg_time_ms'] * 0.001 * metrics['total_executions']:.2f}/month"
                })

            if metrics['total_executions'] > 1000 and metrics['avg_time_ms'] > 50:
                recommendations.append({
                    'query': query_name,
                    'issue': 'High-frequency expensive query',
                    'impact': 'Resource consumption',
                    'recommendation': 'Implement caching or query result pagination',
                    'potential_cost_saving': f"${metrics['total_executions'] * 0.01:.2f}/month"
                })

        return recommendations
```

### 3. API Cost Monitoring

**External API Usage Tracking:**
```python
import httpx
from datetime import datetime
import json

class APICostTracker:
    def __init__(self):
        self.api_costs = {
            'anthropic': {'rate': 0.003, 'units': 'per_1k_tokens', 'usage': 0},
            'openai': {'rate': 0.002, 'units': 'per_1k_tokens', 'usage': 0},
            'google_maps': {'rate': 0.005, 'units': 'per_request', 'usage': 0},
            'real_estate_api': {'rate': 0.01, 'units': 'per_request', 'usage': 0}
        }
        self.monthly_budget = 500  # $500 monthly API budget

    async def track_api_call(self, service_name, tokens_or_requests=1):
        """Track API usage and costs"""
        if service_name in self.api_costs:
            self.api_costs[service_name]['usage'] += tokens_or_requests

        current_spend = self.calculate_monthly_spend()
        if current_spend > self.monthly_budget * 0.8:  # 80% of budget
            await self.send_budget_alert(current_spend)

    def calculate_monthly_spend(self):
        """Calculate total monthly API spending"""
        total_cost = 0
        for service, config in self.api_costs.items():
            if config['units'] == 'per_1k_tokens':
                cost = (config['usage'] / 1000) * config['rate']
            else:  # per_request
                cost = config['usage'] * config['rate']
            total_cost += cost
        return total_cost

    def get_optimization_opportunities(self):
        """Identify API cost optimization opportunities"""
        opportunities = []
        total_spend = self.calculate_monthly_spend()

        for service, config in self.api_costs.items():
            service_cost = (config['usage'] / 1000) * config['rate'] if config['units'] == 'per_1k_tokens' else config['usage'] * config['rate']
            cost_percentage = (service_cost / total_spend) * 100 if total_spend > 0 else 0

            if cost_percentage > 30:  # Service represents >30% of API costs
                opportunities.append({
                    'service': service,
                    'monthly_cost': service_cost,
                    'percentage_of_total': cost_percentage,
                    'optimization': 'Consider caching responses or reducing call frequency',
                    'potential_saving': service_cost * 0.3  # 30% reduction potential
                })

        return opportunities
```

### 4. Development Time Cost Analysis

**Development Velocity Tracking:**
```python
from datetime import datetime, timedelta
import subprocess
import json

class DevelopmentCostAnalyzer:
    def __init__(self):
        self.hourly_rate = 150  # $150/hour developer rate
        self.automation_savings = {}

    def analyze_git_velocity(self, days_back=30):
        """Analyze development velocity from git history"""
        since_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

        # Get commit statistics
        cmd = f"git log --since='{since_date}' --pretty=format:'%h|%ad|%an|%s' --date=short"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        commits = result.stdout.strip().split('\n') if result.stdout else []

        # Categorize commits
        categories = {
            'features': 0,
            'bugs': 0,
            'refactoring': 0,
            'maintenance': 0
        }

        for commit in commits:
            if '|' in commit:
                _, _, _, message = commit.split('|', 3)
                message_lower = message.lower()

                if any(keyword in message_lower for keyword in ['feat', 'feature', 'add', 'implement']):
                    categories['features'] += 1
                elif any(keyword in message_lower for keyword in ['fix', 'bug', 'error']):
                    categories['bugs'] += 1
                elif any(keyword in message_lower for keyword in ['refactor', 'cleanup', 'improve']):
                    categories['refactoring'] += 1
                else:
                    categories['maintenance'] += 1

        total_commits = sum(categories.values())
        velocity_score = total_commits / days_back if total_commits > 0 else 0

        return {
            'commits_per_day': velocity_score,
            'category_breakdown': categories,
            'total_commits': total_commits,
            'efficiency_rating': self._calculate_efficiency_rating(categories)
        }

    def _calculate_efficiency_rating(self, categories):
        """Calculate development efficiency based on commit types"""
        total = sum(categories.values())
        if total == 0:
            return 0

        # Higher score for features and refactoring, lower for bug fixes
        feature_weight = 1.0
        refactor_weight = 0.8
        maintenance_weight = 0.6
        bug_weight = 0.4  # Bug fixes indicate tech debt

        weighted_score = (
            categories['features'] * feature_weight +
            categories['refactoring'] * refactor_weight +
            categories['maintenance'] * maintenance_weight +
            categories['bugs'] * bug_weight
        ) / total

        return min(100, weighted_score * 100)

    def calculate_automation_roi(self, task_name, manual_time_hours, automation_time_hours):
        """Calculate ROI for automation investments"""
        manual_cost = manual_time_hours * self.hourly_rate
        automation_cost = automation_time_hours * self.hourly_rate

        # Assume task happens monthly
        monthly_savings = manual_cost - (automation_cost / 12)  # Amortize automation over 12 months
        annual_savings = monthly_savings * 12

        roi_percentage = ((annual_savings - automation_cost) / automation_cost) * 100 if automation_cost > 0 else 0

        self.automation_savings[task_name] = {
            'manual_cost_per_occurrence': manual_cost,
            'automation_investment': automation_cost,
            'monthly_savings': monthly_savings,
            'annual_savings': annual_savings,
            'roi_percentage': roi_percentage,
            'payback_months': automation_cost / monthly_savings if monthly_savings > 0 else float('inf')
        }

        return self.automation_savings[task_name]
```

## Cost Optimization Dashboard

### Real-time Cost Monitoring
```python
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

def create_cost_optimization_dashboard():
    """Create comprehensive cost monitoring dashboard"""
    st.title("💰 Cost Optimization Dashboard")

    # Initialize analyzers
    infra_analyzer = InfrastructureCostAnalyzer()
    query_analyzer = QueryCostAnalyzer()
    api_tracker = APICostTracker()
    dev_analyzer = DevelopmentCostAnalyzer()

    # Current month costs summary
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        infra_cost = calculate_infrastructure_cost()
        st.metric("Infrastructure Cost", f"${infra_cost:.2f}", f"{infra_cost * 0.1:.2f}")

    with col2:
        api_cost = api_tracker.calculate_monthly_spend()
        st.metric("API Costs", f"${api_cost:.2f}", f"{api_cost * 0.05:.2f}")

    with col3:
        dev_cost = calculate_development_cost()
        st.metric("Development Cost", f"${dev_cost:.2f}", f"-{dev_cost * 0.2:.2f}")

    with col4:
        total_cost = infra_cost + api_cost + dev_cost
        st.metric("Total Monthly Cost", f"${total_cost:.2f}", f"{total_cost * 0.08:.2f}")

    # Cost breakdown chart
    st.subheader("📊 Cost Breakdown")
    cost_data = {
        'Category': ['Infrastructure', 'API Costs', 'Development'],
        'Amount': [infra_cost, api_cost, dev_cost]
    }

    fig_pie = px.pie(
        values=cost_data['Amount'],
        names=cost_data['Category'],
        title="Monthly Cost Distribution"
    )
    st.plotly_chart(fig_pie)

    # Resource utilization efficiency
    st.subheader("⚡ Resource Efficiency")
    resource_data = infra_analyzer.analyze_resource_usage()

    col1, col2 = st.columns(2)
    with col1:
        efficiency_score = resource_data['efficiency_score']
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = efficiency_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Resource Efficiency Score"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        st.plotly_chart(fig_gauge)

    with col2:
        # Cost optimization recommendations
        st.markdown("### 🎯 Optimization Opportunities")

        # Query optimization recommendations
        query_recommendations = query_analyzer.get_optimization_recommendations()
        if query_recommendations:
            for rec in query_recommendations[:3]:  # Top 3 recommendations
                with st.expander(f"🔍 {rec['query']} - Potential Saving: {rec['potential_cost_saving']}"):
                    st.write(f"**Issue:** {rec['issue']}")
                    st.write(f"**Impact:** {rec['impact']}")
                    st.write(f"**Recommendation:** {rec['recommendation']}")

        # API optimization opportunities
        api_opportunities = api_tracker.get_optimization_opportunities()
        if api_opportunities:
            for opp in api_opportunities[:2]:
                with st.expander(f"🌐 {opp['service']} API - Potential Saving: ${opp['potential_saving']:.2f}"):
                    st.write(f"**Monthly Cost:** ${opp['monthly_cost']:.2f}")
                    st.write(f"**Cost Share:** {opp['percentage_of_total']:.1f}% of total API costs")
                    st.write(f"**Optimization:** {opp['optimization']}")

    # Development velocity analysis
    st.subheader("🚀 Development Efficiency")
    velocity_data = dev_analyzer.analyze_git_velocity()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Commits per Day", f"{velocity_data['commits_per_day']:.1f}")
        st.metric("Efficiency Rating", f"{velocity_data['efficiency_rating']:.1f}%")

    with col2:
        # Commit type breakdown
        fig_bar = px.bar(
            x=list(velocity_data['category_breakdown'].keys()),
            y=list(velocity_data['category_breakdown'].values()),
            title="Commit Type Distribution (Last 30 Days)"
        )
        st.plotly_chart(fig_bar)

def calculate_infrastructure_cost():
    """Calculate estimated infrastructure costs"""
    # This would integrate with Railway API or cloud provider APIs
    base_cost = 25  # Base Railway plan
    usage_multiplier = 1.2  # Based on current usage
    return base_cost * usage_multiplier

def calculate_development_cost():
    """Calculate development costs based on time tracking"""
    hours_per_month = 40  # Average development hours
    hourly_rate = 150
    return hours_per_month * hourly_rate
```

## Automated Cost Optimization

### 1. Infrastructure Right-sizing
```bash
#!/bin/bash
# scripts/optimize-infrastructure.sh

echo "🔧 Infrastructure Optimization Analysis"

# Check current resource usage
echo "📊 Current Resource Usage:"
echo "CPU: $(top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | awk -F'%' '{print $1}')"
echo "Memory: $(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')"
echo "Disk: $(df -h / | awk 'NR==2{print $5}')"

# Database connection analysis
echo -e "\n🗄️  Database Connection Analysis:"
psql $DATABASE_URL -c "SELECT count(*) as active_connections FROM pg_stat_activity WHERE state = 'active';"

# Suggest optimizations
echo -e "\n💡 Optimization Recommendations:"
echo "1. Consider connection pooling if active connections > 10"
echo "2. Implement query caching for frequently accessed data"
echo "3. Use CDN for static assets if not already implemented"
echo "4. Review and optimize slow queries identified in logs"
```

### 2. API Cost Optimization
```python
# scripts/optimize-api-costs.py
import asyncio
import aioredis
import json
from datetime import datetime, timedelta

class APICostOptimizer:
    def __init__(self):
        self.redis = None
        self.cache_ttl = 3600  # 1 hour cache

    async def setup_redis(self):
        """Setup Redis connection for caching"""
        self.redis = aioredis.from_url("redis://localhost:6379")

    async def cached_api_call(self, api_function, cache_key, *args, **kwargs):
        """Wrapper for API calls with intelligent caching"""
        if not self.redis:
            await self.setup_redis()

        # Try to get from cache first
        cached_result = await self.redis.get(cache_key)
        if cached_result:
            return json.loads(cached_result)

        # Make API call if not cached
        result = await api_function(*args, **kwargs)

        # Cache the result
        await self.redis.setex(
            cache_key,
            self.cache_ttl,
            json.dumps(result, default=str)
        )

        return result

    async def batch_api_calls(self, api_function, requests, batch_size=10):
        """Batch multiple API calls to reduce costs"""
        results = []

        for i in range(0, len(requests), batch_size):
            batch = requests[i:i + batch_size]
            batch_results = await asyncio.gather(
                *[api_function(**request) for request in batch]
            )
            results.extend(batch_results)

            # Small delay to respect rate limits
            await asyncio.sleep(0.1)

        return results
```

## ROI Measurement Framework

### Cost Savings Tracking
```python
class ROITracker:
    def __init__(self):
        self.baseline_costs = {}
        self.optimized_costs = {}
        self.automation_investments = {}

    def record_baseline(self, category, monthly_cost):
        """Record baseline costs before optimization"""
        self.baseline_costs[category] = {
            'monthly_cost': monthly_cost,
            'recorded_date': datetime.now()
        }

    def record_optimization(self, category, new_monthly_cost, optimization_investment=0):
        """Record costs after optimization"""
        self.optimized_costs[category] = {
            'monthly_cost': new_monthly_cost,
            'optimization_investment': optimization_investment,
            'recorded_date': datetime.now()
        }

    def calculate_roi(self, category):
        """Calculate ROI for specific optimization"""
        if category not in self.baseline_costs or category not in self.optimized_costs:
            return None

        baseline = self.baseline_costs[category]['monthly_cost']
        optimized = self.optimized_costs[category]['monthly_cost']
        investment = self.optimized_costs[category]['optimization_investment']

        monthly_savings = baseline - optimized
        annual_savings = monthly_savings * 12

        if investment > 0:
            roi_percentage = ((annual_savings - investment) / investment) * 100
            payback_months = investment / monthly_savings if monthly_savings > 0 else float('inf')
        else:
            roi_percentage = float('inf')  # No investment required
            payback_months = 0

        return {
            'monthly_savings': monthly_savings,
            'annual_savings': annual_savings,
            'roi_percentage': roi_percentage,
            'payback_months': payback_months,
            'investment': investment
        }

    def generate_roi_report(self):
        """Generate comprehensive ROI report"""
        report = {
            'total_monthly_savings': 0,
            'total_annual_savings': 0,
            'total_investment': 0,
            'categories': {}
        }

        for category in self.baseline_costs.keys():
            if category in self.optimized_costs:
                roi_data = self.calculate_roi(category)
                if roi_data:
                    report['categories'][category] = roi_data
                    report['total_monthly_savings'] += roi_data['monthly_savings']
                    report['total_annual_savings'] += roi_data['annual_savings']
                    report['total_investment'] += roi_data['investment']

        if report['total_investment'] > 0:
            report['overall_roi'] = ((report['total_annual_savings'] - report['total_investment']) / report['total_investment']) * 100
        else:
            report['overall_roi'] = float('inf')

        return report
```

## Implementation Guidelines

### 1. Quick Start (15 minutes)
```bash
# Setup cost monitoring
pip install psutil plotly streamlit redis

# Initialize cost tracking
python scripts/setup-cost-monitoring.py

# Start monitoring dashboard
streamlit run cost_dashboard.py
```

### 2. Infrastructure Optimization (30 minutes)
```bash
# Run infrastructure analysis
./scripts/optimize-infrastructure.sh

# Implement recommended optimizations
python scripts/apply-infrastructure-optimizations.py
```

### 3. API Cost Reduction (20 minutes)
```python
# Implement API caching
from cost_optimization_analyzer import APICostOptimizer

optimizer = APICostOptimizer()

# Wrap existing API calls
async def optimized_api_call():
    return await optimizer.cached_api_call(
        your_api_function,
        "cache_key",
        *args,
        **kwargs
    )
```

## Cost Optimization Checklist

### Infrastructure (20-30% potential savings)
- [ ] Right-size compute resources based on actual usage
- [ ] Implement connection pooling for databases
- [ ] Enable compression for static assets
- [ ] Use CDN for frequently accessed content
- [ ] Optimize Docker image sizes
- [ ] Configure auto-scaling based on demand

### API Costs (30-50% potential savings)
- [ ] Implement intelligent caching for API responses
- [ ] Batch similar API requests
- [ ] Use cheaper API tiers for non-critical operations
- [ ] Cache frequently requested data locally
- [ ] Implement rate limiting to prevent overage charges
- [ ] Monitor and alert on API budget usage

### Development Efficiency (50-70% time savings)
- [ ] Automate repetitive tasks
- [ ] Implement comprehensive testing to prevent bugs
- [ ] Use code generation for boilerplate code
- [ ] Create self-service tools for common operations
- [ ] Implement CI/CD for faster deployments
- [ ] Use monitoring to prevent issues before they occur

### Database Optimization (15-25% performance gains)
- [ ] Identify and optimize slow queries
- [ ] Implement proper indexing strategies
- [ ] Use query result caching
- [ ] Optimize database schema for common access patterns
- [ ] Monitor connection usage and optimize pooling
- [ ] Regular database maintenance and vacuum operations

## Success Metrics

### Financial Metrics
- **Monthly Cost Reduction:** Target 20-30% reduction in infrastructure costs
- **API Cost Optimization:** Target 30-50% reduction in external API costs
- **Development Efficiency:** 50-70% reduction in time spent on manual tasks

### Performance Metrics
- **Response Time Improvement:** <200ms average response time
- **Resource Utilization:** 60-80% optimal resource usage
- **Query Performance:** <100ms average query execution time
- **Deployment Frequency:** Daily deployments with zero downtime

### ROI Calculation
```
Monthly Savings = (Baseline Costs - Optimized Costs)
Annual ROI = ((Annual Savings - Investment) / Investment) * 100
Payback Period = Investment / Monthly Savings
```

This cost optimization analyzer provides comprehensive monitoring, analysis, and optimization recommendations to maximize ROI while minimizing operational overhead. The automated tracking and dashboard provide real-time visibility into cost trends and optimization opportunities.