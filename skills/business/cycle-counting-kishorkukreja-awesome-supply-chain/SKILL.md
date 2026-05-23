---
name: cycle-counting
description: When the user wants to implement or optimize cycle counting programs, improve inventory accuracy, or design physical inventory processes. Also use when the user mentions "inventory accuracy," "physical inventory," "stock counting," "ABC cycle counting," "perpetual inventory," "inventory reconciliation," or "variance analysis." For inventory optimization, see inventory-optimization. For warehouse operations, see warehouse-design.
---

# Cycle Counting

You are an expert in cycle counting and inventory accuracy management. Your goal is to help design and optimize cycle counting programs that maintain high inventory accuracy while minimizing operational disruption and labor costs.

## Initial Assessment

Before implementing cycle counting, understand:

1. **Current State**
   - Current inventory accuracy level?
   - Existing cycle counting program? (frequency, method)
   - Last physical inventory? (annual, semi-annual)
   - Known accuracy pain points?

2. **Operational Context**
   - SKU count and warehouse size?
   - Warehouse management system (WMS) in place?
   - RF scanning and barcode infrastructure?
   - Labor availability for counting?

3. **Business Impact**
   - Cost of inaccuracy? (stockouts, excess, expediting)
   - Order fill rate and customer service impact?
   - Financial audit requirements?
   - Regulatory compliance (FDA, SOX, etc.)?

4. **Inventory Characteristics**
   - ABC classification of inventory?
   - High-value items requiring tight control?
   - Items with known accuracy issues?
   - Storage types (pallets, shelving, bulk)?

---

## Cycle Counting Framework

### Why Cycle Count?

**Benefits vs. Annual Physical Inventory:**

| Aspect | Annual Physical Inventory | Cycle Counting |
|--------|---------------------------|----------------|
| Accuracy | Once per year | Continuous improvement |
| Disruption | Shutdown operations (1-3 days) | No shutdown needed |
| Cost | High (labor spike, lost production) | Lower (spread over year) |
| Root Cause | Difficult (old variances) | Timely (find issues quickly) |
| Compliance | Meets minimum requirement | Exceeds (continuous verification) |

**Target Accuracy:**
- **Class A items**: 99%+ accuracy
- **Class B items**: 97%+ accuracy
- **Class C items**: 95%+ accuracy
- **Overall**: 98%+ accuracy

---

## Cycle Counting Methods

### 1. ABC Cycle Counting

**Most Common Method:**
- Count high-value items (A) more frequently
- Count medium-value items (B) moderately
- Count low-value items (C) less frequently

**Frequency Guidelines:**

| Class | % of Items | % of Value | Count Frequency | Counts per Year |
|-------|-----------|------------|-----------------|-----------------|
| A | 20% | 80% | Monthly | 12x |
| B | 30% | 15% | Quarterly | 4x |
| C | 50% | 5% | Semi-annually | 2x |

```python
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def abc_cycle_counting_schedule(inventory_df, counts_per_year={'A': 12, 'B': 4, 'C': 2}):
    """
    Create ABC cycle counting schedule

    Parameters:
    - inventory_df: DataFrame with columns ['sku', 'abc_class', 'location']
    - counts_per_year: Dict with counts per year by ABC class

    Returns:
    - Annual cycle counting schedule
    """

    # Calculate days between counts for each class
    days_between_counts = {
        cls: 365 / freq for cls, freq in counts_per_year.items()
    }

    # Create schedule
    schedule = []
    start_date = datetime.now()

    for _, item in inventory_df.iterrows():
        abc_class = item['abc_class']
        freq = counts_per_year[abc_class]
        interval = days_between_counts[abc_class]

        # Schedule count dates throughout year
        for count_num in range(freq):
            count_date = start_date + timedelta(days=interval * count_num)

            schedule.append({
                'sku': item['sku'],
                'abc_class': abc_class,
                'location': item['location'],
                'count_date': count_date.date(),
                'count_number': count_num + 1
            })

    schedule_df = pd.DataFrame(schedule)
    schedule_df = schedule_df.sort_values('count_date')

    return schedule_df

# Example
inventory = pd.DataFrame({
    'sku': [f'SKU_{i:03d}' for i in range(1, 101)],
    'abc_class': np.random.choice(['A', 'B', 'C'], 100, p=[0.2, 0.3, 0.5]),
    'location': [f'LOC-{np.random.randint(1, 50):03d}' for _ in range(100)]
})

schedule = abc_cycle_counting_schedule(inventory)

print(f"Total count events per year: {len(schedule)}")
print(f"\nCounts by class:")
print(schedule.groupby('abc_class')['sku'].count())

# Daily counting workload
daily_workload = schedule.groupby('count_date').size()
print(f"\nAverage counts per day: {daily_workload.mean():.1f}")
print(f"Max counts per day: {daily_workload.max()}")
```

### 2. Random Sample Cycle Counting

**Method:**
- Randomly select locations/SKUs to count each day
- Ensures all items counted over time
- Statistical sampling approach

```python
def random_sample_cycle_counting(inventory_df, target_counts_per_year=2,
                                working_days_per_year=250):
    """
    Random sampling cycle count schedule

    Parameters:
    - inventory_df: DataFrame with inventory items
    - target_counts_per_year: How many times each item should be counted
    - working_days_per_year: Working days available for counting

    Returns:
    - Daily random samples
    """

    total_items = len(inventory_df)
    total_count_events = total_items * target_counts_per_year

    # Counts per day
    counts_per_day = int(np.ceil(total_count_events / working_days_per_year))

    print(f"Total items: {total_items}")
    print(f"Target counts per year per item: {target_counts_per_year}")
    print(f"Total count events needed: {total_count_events}")
    print(f"Counts required per day: {counts_per_day}")

    return counts_per_day

# Example
counts_per_day = random_sample_cycle_counting(inventory, target_counts_per_year=2)
```

### 3. Process-Triggered Cycle Counting

**Count When:**
- **Zero balance**: Count when system shows zero on-hand
- **Order picking**: Count location after picking last item
- **Receiving**: Count upon putaway
- **Replenishment**: Count when replenishing forward pick
- **Negative on-hand**: Investigate immediately (system error)

```python
def process_triggered_counting_events(transactions_df):
    """
    Identify cycle count triggers from transaction data

    Parameters:
    - transactions_df: DataFrame with columns ['sku', 'location', 'transaction_type',
                                                'before_qty', 'after_qty']

    Returns:
    - List of triggered count events
    """

    count_triggers = []

    for _, txn in transactions_df.iterrows():
        trigger_reason = None

        # Zero balance trigger
        if txn['after_qty'] == 0:
            trigger_reason = 'Zero balance after transaction'

        # Negative balance trigger (error!)
        elif txn['after_qty'] < 0:
            trigger_reason = 'NEGATIVE BALANCE - Urgent'

        # Large variance trigger (>10% change)
        elif txn['transaction_type'] == 'Adjustment':
            if abs(txn['before_qty'] - txn['after_qty']) > txn['before_qty'] * 0.10:
                trigger_reason = 'Large adjustment (>10%)'

        if trigger_reason:
            count_triggers.append({
                'sku': txn['sku'],
                'location': txn['location'],
                'trigger_reason': trigger_reason,
                'system_qty': txn['after_qty'],
                'priority': 'URGENT' if 'NEGATIVE' in trigger_reason else 'High'
            })

    return pd.DataFrame(count_triggers)

# Example
transactions = pd.DataFrame({
    'sku': ['SKU_001', 'SKU_002', 'SKU_003', 'SKU_004'],
    'location': ['A-1-1', 'A-1-2', 'B-2-3', 'C-3-4'],
    'transaction_type': ['Pick', 'Adjustment', 'Pick', 'Pick'],
    'before_qty': [50, 100, 10, 5],
    'after_qty': [0, 80, -2, 4]
})

triggers = process_triggered_counting_events(transactions)
print("Count Triggers:")
print(triggers)
```

### 4. Opportunity Cycle Counting

**Count During:**
- Slow periods (avoid peak times)
- When location is already accessed (picking, replenishment)
- When item is moved (slotting changes)
- Empty locations (quick verification)

```python
def opportunity_counting_logic(current_activity, location_activity_log):
    """
    Identify opportunistic counting moments

    Parameters:
    - current_activity: Current warehouse activity level (0-100)
    - location_activity_log: Recent activity at locations

    Returns:
    - Recommended locations to count now
    """

    opportunities = []

    # Low activity period
    if current_activity < 30:
        opportunities.append({
            'opportunity': 'Low activity period',
            'recommendation': 'Count high-traffic locations while quiet',
            'priority': 'Medium'
        })

    # Location just accessed
    for location, last_access in location_activity_log.items():
        if last_access == 'just_now':
            opportunities.append({
                'opportunity': f'Location {location} just accessed',
                'recommendation': 'Count while already there (reduce travel)',
                'priority': 'High'
            })

    return opportunities
```

---

## Cycle Counting Process

### Step-by-Step Process

**1. Generate Count Sheet**
- Select items/locations to count (based on method)
- Print count sheets or load to RF device
- Include: SKU, location, expected quantity (optional)

**2. Physical Count**
- Counter goes to location
- Counts actual quantity
- Records on count sheet or in RF device
- Note any issues (damage, mislabeling, etc.)

**3. Variance Analysis**
- Compare physical count to system quantity
- Calculate variance (count - system)
- Investigate if variance exceeds tolerance

**4. Recount (if needed)**
- If variance exceeds threshold, recount
- Blind recount (no expected quantity shown)
- Different counter if possible

**5. Adjustment & Root Cause**
- Adjust system if count verified
- Document root cause (picking error, receiving error, etc.)
- Corrective action

```python
def cycle_count_variance_analysis(system_qty, counted_qty, unit_value,
                                 tolerance_qty=5, tolerance_value=100):
    """
    Analyze cycle count variance and determine action

    Parameters:
    - system_qty: System on-hand quantity
    - counted_qty: Physical count quantity
    - unit_value: Value per unit ($)
    - tolerance_qty: Tolerance in units (e.g., ±5 units)
    - tolerance_value: Tolerance in dollars (e.g., ±$100)

    Returns:
    - Variance analysis and recommended action
    """

    variance_qty = counted_qty - system_qty
    variance_value = variance_qty * unit_value
    variance_pct = (variance_qty / system_qty * 100) if system_qty > 0 else 0

    # Determine if within tolerance
    within_tolerance = (
        abs(variance_qty) <= tolerance_qty and
        abs(variance_value) <= tolerance_value
    )

    # Determine action
    if within_tolerance:
        action = 'Accept count, adjust system'
        priority = 'Low'
    elif abs(variance_qty) <= tolerance_qty * 2:
        action = 'Recount required'
        priority = 'Medium'
    else:
        action = 'Recount required (blind count, different counter)'
        priority = 'High'

    return {
        'system_qty': system_qty,
        'counted_qty': counted_qty,
        'variance_qty': variance_qty,
        'variance_value': round(variance_value, 2),
        'variance_pct': round(variance_pct, 1),
        'within_tolerance': within_tolerance,
        'action': action,
        'priority': priority
    }

# Example
variance = cycle_count_variance_analysis(
    system_qty=100,
    counted_qty=92,
    unit_value=50,
    tolerance_qty=5,
    tolerance_value=100
)

print(f"System quantity: {variance['system_qty']}")
print(f"Counted quantity: {variance['counted_qty']}")
print(f"Variance: {variance['variance_qty']} units (${variance['variance_value']})")
print(f"Action: {variance['action']}")
```

---

## Cycle Counting Metrics & KPIs

### Key Performance Indicators

```python
def calculate_cycle_count_kpis(total_counts, accurate_counts, total_variance_units,
                              total_variance_value, total_inventory_value):
    """
    Calculate cycle counting KPIs

    Parameters:
    - total_counts: Total count events
    - accurate_counts: Counts within tolerance
    - total_variance_units: Total unit variance (absolute)
    - total_variance_value: Total dollar variance (absolute)
    - total_inventory_value: Total inventory value

    Returns:
    - KPI dashboard
    """

    # Accuracy rate
    accuracy_rate = accurate_counts / total_counts if total_counts > 0 else 0

    # Average variance
    avg_variance_units = total_variance_units / total_counts if total_counts > 0 else 0

    # Variance as % of inventory value
    variance_pct_of_inventory = (total_variance_value / total_inventory_value * 100
                                if total_inventory_value > 0 else 0)

    kpis = {
        'Count_Accuracy_%': round(accuracy_rate * 100, 2),
        'Total_Counts': total_counts,
        'Accurate_Counts': accurate_counts,
        'Avg_Variance_Units': round(avg_variance_units, 2),
        'Total_Variance_Value': round(total_variance_value, 2),
        'Variance_%_of_Inventory': round(variance_pct_of_inventory, 3)
    }

    return kpis

# Example
kpis = calculate_cycle_count_kpis(
    total_counts=1000,
    accurate_counts=980,
    total_variance_units=150,
    total_variance_value=7500,
    total_inventory_value=5_000_000
)

print("Cycle Count KPIs:")
for metric, value in kpis.items():
    print(f"  {metric}: {value}")
```

### Benchmark Targets

| Metric | Target | World-Class |
|--------|--------|-------------|
| Overall Inventory Accuracy | 98%+ | 99.5%+ |
| A Item Accuracy | 99%+ | 99.9%+ |
| B Item Accuracy | 97%+ | 99%+ |
| C Item Accuracy | 95%+ | 98%+ |
| Counts per Day (per 1000 SKUs) | 5-10 | 10-15 |
| Time per Count | 3-5 min | 2-3 min |
| Recount Rate | <10% | <5% |

---

## Labor Planning for Cycle Counting

### Staffing Requirements

```python
def cycle_count_labor_planning(total_skus, abc_distribution={'A': 0.2, 'B': 0.3, 'C': 0.5},
                              counts_per_year={'A': 12, 'B': 4, 'C': 2},
                              time_per_count_min=5, working_days=250,
                              hours_per_day=8):
    """
    Calculate labor requirements for cycle counting program

    Parameters:
    - total_skus: Total number of SKUs
    - abc_distribution: % of SKUs in each class
    - counts_per_year: Count frequency by class
    - time_per_count_min: Minutes per count event
    - working_days: Working days per year
    - hours_per_day: Hours available per day for counting

    Returns:
    - Labor requirements
    """

    total_count_events = 0

    for abc_class, pct in abc_distribution.items():
        skus_in_class = total_skus * pct
        counts = skus_in_class * counts_per_year[abc_class]
        total_count_events += counts

        print(f"Class {abc_class}: {skus_in_class:.0f} SKUs × {counts_per_year[abc_class]} = {counts:.0f} counts")

    print(f"\nTotal count events per year: {total_count_events:.0f}")

    # Time required
    total_hours = (total_count_events * time_per_count_min) / 60
    hours_per_day_required = total_hours / working_days

    # FTE calculation
    fte_required = hours_per_day_required / hours_per_day

    # If dedicated counter vs. integrated into other roles
    if fte_required < 0.5:
        staffing_model = f"Integrate into existing roles ({fte_required:.2f} FTE)"
    elif fte_required < 1.5:
        staffing_model = f"1 dedicated counter + integrated tasks ({fte_required:.2f} FTE)"
    else:
        staffing_model = f"{np.ceil(fte_required):.0f} dedicated counters"

    return {
        'total_count_events': int(total_count_events),
        'total_hours_per_year': round(total_hours, 0),
        'hours_per_day': round(hours_per_day_required, 2),
        'fte_required': round(fte_required, 2),
        'staffing_model': staffing_model,
        'counts_per_day': round(total_count_events / working_days, 1)
    }

# Example
labor = cycle_count_labor_planning(
    total_skus=5000,
    time_per_count_min=5,
    working_days=250
)

print(f"\nLabor Requirements:")
print(f"  Total count events: {labor['total_count_events']}")
print(f"  Hours per day: {labor['hours_per_day']}")
print(f"  FTE required: {labor['fte_required']}")
print(f"  Staffing model: {labor['staffing_model']}")
```

---

## Root Cause Analysis

### Common Causes of Inaccuracy

**Top Causes:**
1. **Picking errors** (35-40%)
   - Wrong item picked
   - Wrong quantity picked
   - Not scanned properly

2. **Receiving errors** (25-30%)
   - Wrong quantity received
   - Putaway to wrong location
   - Not updated in system

3. **Replenishment errors** (10-15%)
   - Wrong quantity moved
   - Not recorded properly
   - Moved to wrong location

4. **System errors** (5-10%)
   - Transaction not processed
   - Duplicate transactions
   - Wrong SKU master data

5. **Theft/damage** (5-10%)
   - Shrinkage
   - Damaged goods not recorded
   - Returns not processed

```python
def root_cause_analysis(variance_log):
    """
    Analyze root causes of inventory variances

    Parameters:
    - variance_log: DataFrame with columns ['sku', 'variance_qty', 'root_cause',
                                            'variance_value', 'date']

    Returns:
    - Root cause analysis summary
    """

    # Summarize by root cause
    cause_summary = variance_log.groupby('root_cause').agg({
        'sku': 'count',
        'variance_qty': 'sum',
        'variance_value': 'sum'
    }).rename(columns={'sku': 'occurrences'})

    # Calculate percentages
    total_occurrences = cause_summary['occurrences'].sum()
    cause_summary['pct_of_occurrences'] = (
        cause_summary['occurrences'] / total_occurrences * 100
    )

    # Sort by occurrence
    cause_summary = cause_summary.sort_values('occurrences', ascending=False)

    # Pareto analysis (80/20)
    cause_summary['cumulative_pct'] = cause_summary['pct_of_occurrences'].cumsum()

    return cause_summary

# Example
variance_data = pd.DataFrame({
    'sku': [f'SKU_{i}' for i in range(1, 101)],
    'variance_qty': np.random.randint(-20, 20, 100),
    'variance_value': np.random.uniform(-500, 500, 100),
    'root_cause': np.random.choice(
        ['Picking Error', 'Receiving Error', 'Replenishment Error',
         'System Error', 'Damage/Shrinkage'],
        100,
        p=[0.40, 0.30, 0.15, 0.10, 0.05]
    ),
    'date': pd.date_range('2024-01-01', periods=100)
})

cause_analysis = root_cause_analysis(variance_data)
print("Root Cause Analysis:")
print(cause_analysis)
```

### Corrective Actions by Root Cause

```python
def corrective_actions_by_cause(root_cause):
    """
    Recommend corrective actions based on root cause
    """

    actions = {
        'Picking Error': [
            'Implement mandatory RF scanning verification',
            'Pick-to-light or voice picking technology',
            'Improve labeling and signage',
            'Picker training and refresher courses',
            'Quality audits (random pick verification)',
            'Picking metrics and accountability'
        ],
        'Receiving Error': [
            'Blind receiving (count without PO reference)',
            'Dual verification for high-value items',
            'Improve putaway processes',
            'Directed putaway in WMS',
            'Receiver training and accountability',
            'Vendor quality programs'
        ],
        'Replenishment Error': [
            'RF scanning for all moves',
            'Directed replenishment in WMS',
            'Standard work procedures',
            'Improve signage and location labels',
            'Quality checks on replenishment'
        ],
        'System Error': [
            'WMS system audit and cleanup',
            'Improve user training',
            'System validation testing',
            'IT controls and access management',
            'Transaction monitoring and alerts'
        ],
        'Damage/Shrinkage': [
            'Improve security (cameras, access control)',
            'Damage reporting and disposition process',
            'Better packaging and handling',
            'Regular security audits',
            'Investigate high-shrinkage items'
        ]
    }

    return actions.get(root_cause, ['Investigate further and document'])

# Example
print("Corrective Actions for Picking Errors:")
for action in corrective_actions_by_cause('Picking Error'):
    print(f"  - {action}")
```

---

## Blind vs. Informed Counting

### Counting Approaches

**Blind Counting:**
- Counter does NOT see expected quantity
- Pros: More accurate (no bias), catches systematic errors
- Cons: Takes longer, requires more training

**Informed Counting:**
- Counter sees expected quantity
- Pros: Faster, catches obvious discrepancies
- Cons: Bias (counter may not look carefully if numbers match)

**Best Practice:**
- Use informed for routine counts
- Use blind for recounts, high-value items, or problem locations

```python
def counting_approach_decision(abc_class, previous_accuracy, item_value):
    """
    Decide between blind or informed counting

    Parameters:
    - abc_class: 'A', 'B', or 'C'
    - previous_accuracy: Historical accuracy for this item (0-1)
    - item_value: Dollar value of item

    Returns:
    - Recommended counting approach
    """

    if abc_class == 'A' or item_value > 1000:
        approach = 'Blind count'
        reason = 'High value or Class A item'

    elif previous_accuracy < 0.90:
        approach = 'Blind count'
        reason = 'History of inaccuracy'

    else:
        approach = 'Informed count'
        reason = 'Routine count, good accuracy history'

    return {
        'approach': approach,
        'reason': reason
    }

# Example
decision = counting_approach_decision('A', 0.85, 1500)
print(f"Counting approach: {decision['approach']}")
print(f"Reason: {decision['reason']}")
```

---

## Technology & Tools

### Warehouse Management Systems (WMS)

**WMS Cycle Counting Features:**
- Automated count generation (ABC, random, triggered)
- RF-directed counting
- Variance workflow (tolerance, recount, adjustment)
- Count history and trending
- Root cause tracking
- Real-time accuracy dashboards

**Leading WMS with Strong Cycle Counting:**
- Manhattan Associates
- Blue Yonder (JDA)
- SAP EWM
- Oracle WMS
- HighJump (Korber)

### Mobile Technology

**RF Scanners:**
- Zebra TC series
- Honeywell Dolphin
- Rugged mobile computers

**Features Needed:**
- Barcode scanning
- WMS integration
- Wireless connectivity
- Long battery life

### Advanced Technologies

**RFID (Radio Frequency Identification):**
- Real-time inventory visibility
- Automatic counting (no manual scan)
- Expensive (tags cost $0.10-$1.00 each)
- Good for high-value items, apparel

**Drones:**
- Autonomous warehouse scanning
- Reads barcodes from high racks
- Fast (500+ reads per hour)
- Emerging technology ($50K-$200K)

**Computer Vision:**
- Camera-based counting
- Automatic pallet counting
- AI/ML for accuracy
- Emerging technology

---

## Implementation Best Practices

### Implementing a Cycle Counting Program

**Phase 1: Baseline (Month 1)**
- Conduct physical inventory to establish baseline
- Clean up WMS data (locations, SKU masters)
- ABC classify inventory
- Train staff on cycle counting process

**Phase 2: Pilot (Month 2)**
- Start with Class A items
- Test process and refine
- Build counting skills
- Establish tolerances and workflows

**Phase 3: Rollout (Months 3-6)**
- Expand to all ABC classes
- Monitor accuracy metrics
- Root cause analysis and corrective actions
- Continuous improvement

**Phase 4: Sustain (Ongoing)**
- Maintain discipline and frequency
- Regular performance reviews
- Ongoing training
- Technology upgrades

### Keys to Success

1. **Management Support**: Executive commitment to accuracy
2. **Accountability**: Track individual counter accuracy
3. **Root Cause Focus**: Don't just adjust, fix problems
4. **Technology**: RF scanning, WMS, automation
5. **Training**: Initial and ongoing education
6. **Discipline**: Follow the schedule consistently
7. **Metrics**: Track and report accuracy KPIs

---

## Cost-Benefit Analysis

### ROI of Cycle Counting

```python
def cycle_counting_roi(current_accuracy=0.90, target_accuracy=0.98,
                      annual_revenue=50_000_000, stockout_cost_pct=0.02,
                      excess_inventory_cost_pct=0.01,
                      cycle_count_labor_cost=60000,
                      technology_cost_annual=20000):
    """
    Calculate ROI of implementing cycle counting program

    Parameters:
    - current_accuracy: Current inventory accuracy
    - target_accuracy: Target accuracy with cycle counting
    - annual_revenue: Annual revenue ($)
    - stockout_cost_pct: Stockouts as % of revenue (due to inaccuracy)
    - excess_inventory_cost_pct: Excess inventory cost as % of revenue
    - cycle_count_labor_cost: Annual labor cost for cycle counting
    - technology_cost_annual: Annual technology costs (RF, WMS)

    Returns:
    - ROI analysis
    """

    # Current costs due to inaccuracy
    current_stockout_cost = annual_revenue * stockout_cost_pct * (1 - current_accuracy)
    current_excess_cost = annual_revenue * excess_inventory_cost_pct * (1 - current_accuracy)
    current_total_cost = current_stockout_cost + current_excess_cost

    # Future costs with improved accuracy
    future_stockout_cost = annual_revenue * stockout_cost_pct * (1 - target_accuracy)
    future_excess_cost = annual_revenue * excess_inventory_cost_pct * (1 - target_accuracy)
    future_total_cost = future_stockout_cost + future_excess_cost

    # Savings
    annual_savings = current_total_cost - future_total_cost

    # Costs of cycle counting
    annual_cc_cost = cycle_count_labor_cost + technology_cost_annual

    # Net benefit
    net_annual_benefit = annual_savings - annual_cc_cost

    # ROI
    roi = (net_annual_benefit / annual_cc_cost) * 100 if annual_cc_cost > 0 else 0

    return {
        'current_accuracy_%': current_accuracy * 100,
        'target_accuracy_%': target_accuracy * 100,
        'current_annual_cost': round(current_total_cost, 0),
        'future_annual_cost': round(future_total_cost, 0),
        'annual_savings': round(annual_savings, 0),
        'cycle_counting_cost': round(annual_cc_cost, 0),
        'net_annual_benefit': round(net_annual_benefit, 0),
        'roi_%': round(roi, 1),
        'payback_months': round(annual_cc_cost / (net_annual_benefit / 12), 1) if net_annual_benefit > 0 else 999
    }

# Example
roi = cycle_counting_roi(
    current_accuracy=0.90,
    target_accuracy=0.98,
    annual_revenue=50_000_000,
    stockout_cost_pct=0.02,
    excess_inventory_cost_pct=0.01
)

print("Cycle Counting ROI:")
print(f"  Current accuracy: {roi['current_accuracy_%']}%")
print(f"  Target accuracy: {roi['target_accuracy_%']}%")
print(f"  Annual savings: ${roi['annual_savings']:,.0f}")
print(f"  Cycle counting cost: ${roi['cycle_counting_cost']:,.0f}")
print(f"  Net annual benefit: ${roi['net_annual_benefit']:,.0f}")
print(f"  ROI: {roi['roi_%']}%")
print(f"  Payback: {roi['payback_months']} months")
```

---

## Common Challenges & Solutions

### Challenge: Resistance from Operations

**Problem:**
- "We're too busy to count"
- Seen as non-value-added activity
- Disrupts picking operations

**Solutions:**
- Show cost of inaccuracy (stockouts, expediting)
- Integrate counting into workflows (opportunity counting)
- Count during slow periods
- Dedicated counting staff
- Demonstrate quick wins (improved fill rate)

### Challenge: High Variance Rates

**Problem:**
- Many counts outside tolerance
- Constant recounting
- Lack of confidence in accuracy

**Solutions:**
- Root cause analysis (don't just adjust)
- Focus on prevention, not detection
- Improve processes (scanning, verification)
- Training and accountability
- Audit high-variance SKUs more frequently

### Challenge: Labor Constraints

**Problem:**
- Not enough staff to count regularly
- Competing priorities
- Turnover and training gaps

**Solutions:**
- Optimize count schedule (focus on ABC)
- Use technology (RFID, automation)
- Integrate into existing roles
- Simplified processes
- Outsource to 3PL if applicable

### Challenge: Large SKU Count

**Problem:**
- 10,000+ SKUs overwhelming
- Can't count frequently enough
- Resource intensive

**Solutions:**
- ABC focus (80/20 rule)
- Random sampling for C items
- Process-triggered counts
- Technology (RFID, drones)
- Consider product rationalization

### Challenge: System Issues

**Problem:**
- WMS doesn't support cycle counting well
- Manual process prone to errors
- Lack of reporting

**Solutions:**
- Upgrade or implement WMS
- Use spreadsheets/access databases as interim
- RF scanning integration
- Partner with IT for system improvements
- Consider cloud-based WMS

---

## Output Format

### Cycle Counting Program Design Document

**Executive Summary:**
- Program objectives (target accuracy)
- Recommended approach (ABC, frequency)
- Labor and technology requirements
- Expected ROI

**Program Design:**

| Component | Design |
|-----------|--------|
| Method | ABC cycle counting |
| Frequency | A: Monthly, B: Quarterly, C: Semi-annually |
| Daily Counts | 20 count events per day |
| Labor | 0.5 FTE (4 hours/day dedicated) |
| Technology | RF scanners, WMS cycle count module |
| Accuracy Target | 98% overall, 99% for A items |

**Count Schedule:**

| Class | SKUs | Counts/Year Each | Total Counts | Counts/Day |
|-------|------|------------------|--------------|------------|
| A | 1,000 | 12 | 12,000 | 10 |
| B | 1,500 | 4 | 6,000 | 5 |
| C | 2,500 | 2 | 5,000 | 4 |
| **Total** | **5,000** | - | **23,000** | **19** |

**Performance Metrics:**

| Metric | Target | Measurement Frequency |
|--------|--------|-----------------------|
| Overall Accuracy | 98% | Weekly |
| A Item Accuracy | 99% | Weekly |
| Time per Count | <5 min | Monthly average |
| Recount Rate | <10% | Monthly |
| Variance $ | <0.2% of inventory value | Monthly |

**Root Cause Tracking:**
- Track root cause for all variances >10%
- Monthly root cause analysis report
- Corrective action plans for top 3 causes
- Quarterly review with operations leadership

**Implementation Timeline:**
- Week 1-2: Physical inventory and data cleanup
- Week 3-4: WMS configuration and testing
- Week 5: Staff training
- Week 6: Pilot with A items
- Week 7-8: Full rollout
- Ongoing: Monthly performance reviews

---

## Questions to Ask

If you need more context:
1. What's the current inventory accuracy level?
2. What's the SKU count and ABC distribution?
3. Is there a WMS in place? RF scanning capability?
4. What's the current cycle counting method (if any)?
5. What's driving the initiative? (accuracy issues, audit requirement, cost reduction)
6. How much labor is available for counting?
7. What's the cost impact of inaccuracy? (stockouts, expediting, excess)
8. Are there specific items or areas with accuracy problems?

---

## Related Skills

- **inventory-optimization**: Optimize inventory levels and policies
- **warehouse-design**: Design warehouse layout and processes
- **order-fulfillment**: Pick-pack-ship operations that impact accuracy
- **supply-chain-analytics**: KPIs and performance dashboards
- **quality-management**: Quality control and continuous improvement
