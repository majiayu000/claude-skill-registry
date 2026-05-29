---
name: hospital-logistics
description: When the user wants to optimize hospital supply chain operations, manage medical materials, optimize PAR levels, or improve hospital inventory management. Also use when the user mentions "hospital supply chain," "materials management," "PAR levels," "OR inventory," "clinical logistics," "hospital distribution," "medical supplies," "stockroom management," "two-bin system," "floor stock," or "hospital warehousing." For pharmacy-specific operations, see pharmacy-supply-chain. For medical device distribution, see medical-device-distribution.
---

# Hospital Logistics

You are an expert in hospital logistics and healthcare materials management. Your goal is to optimize the flow of medical supplies, pharmaceuticals, and equipment throughout healthcare facilities while maintaining patient safety, regulatory compliance, and cost efficiency.

## Initial Assessment

Before optimizing hospital logistics, understand:

1. **Facility Characteristics**
   - Type of facility? (acute care, specialty hospital, health system)
   - Number of beds and patient volume?
   - Departments and service lines? (OR, ER, ICU, med-surg)
   - Number of locations? (main campus, clinics, satellite facilities)

2. **Current Supply Chain Structure**
   - Centralized vs. decentralized inventory?
   - Materials management system in use? (ERP, MMM system)
   - PAR level methodology current state?
   - Distribution model? (requisition, exchange cart, case cart)

3. **Inventory & Cost Profile**
   - Total inventory investment?
   - Inventory turns by category?
   - Annual supply spend? (% of operating budget)
   - High-dollar items? (implants, specialty devices)

4. **Challenges & Goals**
   - Current pain points? (stockouts, excess, expiry, waste)
   - Service level targets?
   - Cost reduction goals?
   - Compliance concerns? (Joint Commission, FDA)

---

## Hospital Logistics Framework

### Supply Chain Models in Healthcare

**1. Traditional Requisition Model**
- Departments order from central storeroom
- Staff shops from supply room
- High labor cost, variable inventory
- Pros: Flexibility
- Cons: Inefficient, overstocking, poor control

**2. Exchange Cart System**
- Pre-filled carts exchanged on schedule
- Departments receive full cart, return empty
- Better control and efficiency
- Ideal for: Med-surg floors, standard supplies

**3. Case Cart System**
- Custom kits for each surgical procedure
- Assembled in central supply or by vendor
- Used primarily in OR
- Reduces waste, improves efficiency

**4. Just-In-Time (JIT) Delivery**
- Supplies delivered directly to point of use
- Minimal on-hand inventory
- Requires reliable supplier performance
- Examples: Stockless programs, vendor-managed inventory

**5. Two-Bin (Kanban) System**
- Visual replenishment system
- When bin 1 empty, use bin 2 and trigger reorder
- Simple, effective for high-use items
- Reduces stockouts and overstock

---

## PAR Level Optimization

### Understanding PAR Levels

**PAR (Periodic Automatic Replenishment):**
- Target inventory level maintained at point of use
- Replenished to PAR on regular schedule
- Key metric in hospital materials management

**PAR Formula:**
```
PAR Level = (Average Daily Usage × Replenishment Cycle Days) + Safety Stock
```

**Example:**
```
Item: IV Start Kit
Average daily usage: 15 kits
Replenishment cycle: 3 days (Monday, Wednesday, Friday)
Lead time variability: 1 day safety buffer
PAR Level = (15 × 3) + (15 × 1) = 45 + 15 = 60 kits
```

### Python Implementation

```python
import pandas as pd
import numpy as np
from scipy import stats

def calculate_par_level(avg_daily_usage, replenishment_cycle_days,
                        service_level=0.95, usage_variability=None):
    """
    Calculate optimal PAR level for hospital supply item

    Parameters:
    - avg_daily_usage: Average daily consumption
    - replenishment_cycle_days: Days between replenishment
    - service_level: Target service level (e.g., 0.95 for 95%)
    - usage_variability: Std dev of daily usage (if known)

    Returns:
    - Dictionary with PAR level and components
    """

    # Expected usage during cycle
    expected_usage = avg_daily_usage * replenishment_cycle_days

    # Safety stock calculation
    if usage_variability is not None:
        # Statistical approach if variability known
        z_score = stats.norm.ppf(service_level)
        std_during_cycle = usage_variability * np.sqrt(replenishment_cycle_days)
        safety_stock = z_score * std_during_cycle
    else:
        # Rule of thumb: 1 day's worth for weekly replenishment
        # 0.5 days for more frequent (2-3x/week)
        if replenishment_cycle_days >= 7:
            safety_stock = avg_daily_usage * 2
        elif replenishment_cycle_days >= 3:
            safety_stock = avg_daily_usage * 1
        else:
            safety_stock = avg_daily_usage * 0.5

    par_level = expected_usage + safety_stock

    return {
        'par_level': round(par_level, 0),
        'expected_usage': round(expected_usage, 0),
        'safety_stock': round(safety_stock, 0),
        'replenishment_qty_avg': round(expected_usage, 0)
    }

# Example usage
result = calculate_par_level(
    avg_daily_usage=15,
    replenishment_cycle_days=3,
    service_level=0.95,
    usage_variability=5  # daily std dev
)

print(f"PAR Level: {result['par_level']} units")
print(f"Expected cycle usage: {result['expected_usage']} units")
print(f"Safety stock: {result['safety_stock']} units")
```

### PAR Level Optimization Across Locations

```python
def optimize_par_levels_multi_location(usage_data_df):
    """
    Optimize PAR levels across multiple hospital locations

    usage_data_df: DataFrame with columns:
        - location: Department/floor name
        - item_id: Product identifier
        - daily_usage: Historical daily usage list
        - replenishment_days: Days between replenishment
        - unit_cost: Cost per unit
    """

    results = []

    for idx, row in usage_data_df.iterrows():
        usage_array = np.array(row['daily_usage'])

        avg_daily = np.mean(usage_array)
        std_daily = np.std(usage_array)

        # Calculate PAR
        par_calc = calculate_par_level(
            avg_daily_usage=avg_daily,
            replenishment_cycle_days=row['replenishment_days'],
            service_level=0.95,
            usage_variability=std_daily
        )

        # Calculate inventory metrics
        avg_inventory = par_calc['par_level'] / 2  # On average
        inventory_value = avg_inventory * row['unit_cost']
        annual_usage = avg_daily * 365
        turns = annual_usage / avg_inventory if avg_inventory > 0 else 0

        results.append({
            'location': row['location'],
            'item_id': row['item_id'],
            'avg_daily_usage': round(avg_daily, 1),
            'std_daily_usage': round(std_daily, 1),
            'cv': round(std_daily / avg_daily, 2) if avg_daily > 0 else 0,
            'current_par': row.get('current_par', 0),
            'recommended_par': par_calc['par_level'],
            'par_change': par_calc['par_level'] - row.get('current_par', 0),
            'avg_inventory': round(avg_inventory, 0),
            'inventory_value': round(inventory_value, 2),
            'annual_turns': round(turns, 1)
        })

    results_df = pd.DataFrame(results)

    # Summary statistics
    summary = {
        'total_current_value': results_df['inventory_value'].sum() if 'current_par' in usage_data_df.columns else 0,
        'total_recommended_value': results_df['inventory_value'].sum(),
        'potential_savings': 0,  # Calculate based on current vs recommended
        'avg_turns': results_df['annual_turns'].mean()
    }

    return results_df, summary

# Example usage
usage_data = pd.DataFrame({
    'location': ['OR-1', 'OR-1', 'ICU', 'ICU', 'ER'],
    'item_id': ['IV-001', 'Suture-003', 'IV-001', 'Cath-002', 'Gloves-L'],
    'daily_usage': [
        [12, 15, 10, 18, 14],
        [5, 6, 4, 7, 5],
        [25, 30, 22, 28, 26],
        [8, 10, 7, 9, 8],
        [45, 50, 42, 48, 46]
    ],
    'replenishment_days': [3, 7, 2, 3, 2],
    'unit_cost': [15.50, 8.75, 15.50, 125.00, 0.25],
    'current_par': [60, 45, 75, 35, 120]
})

results_df, summary = optimize_par_levels_multi_location(usage_data)
print(results_df[['location', 'item_id', 'current_par', 'recommended_par', 'par_change']])
```

---

## Operating Room (OR) Supply Management

### Case Cart Optimization

**Case Cart Process:**
1. Physician preference cards define items per procedure
2. Carts picked and assembled in central supply
3. Delivered to OR before case
4. Unused items returned, cleaned, restocked

**Optimization Opportunities:**
- Standardize preference cards
- Reduce variation in similar procedures
- Track utilization rates
- Eliminate rarely-used items

```python
def analyze_case_cart_utilization(procedure_data_df):
    """
    Analyze OR case cart utilization and identify waste

    procedure_data_df: DataFrame with:
        - procedure_type: Type of surgery
        - item_id: Product on preference card
        - quantity_picked: Items placed on cart
        - quantity_used: Items actually used
        - unit_cost: Cost per item
        - num_cases: Number of times procedure performed
    """

    results = []

    for idx, row in procedure_data_df.iterrows():
        qty_picked = row['quantity_picked']
        qty_used = row['quantity_used']

        utilization_rate = qty_used / qty_picked if qty_picked > 0 else 0
        waste_qty = qty_picked - qty_used
        waste_per_case = waste_qty
        annual_waste_qty = waste_per_case * row['num_cases']
        annual_waste_value = annual_waste_qty * row['unit_cost']

        # Recommendation
        if utilization_rate < 0.5:
            recommendation = "Remove from standard cart - order as needed"
        elif utilization_rate < 0.8:
            recommendation = f"Reduce quantity to {int(qty_used * 1.1)}"
        else:
            recommendation = "Appropriate level"

        results.append({
            'procedure': row['procedure_type'],
            'item_id': row['item_id'],
            'picked': qty_picked,
            'used': qty_used,
            'utilization_rate': round(utilization_rate * 100, 1),
            'waste_per_case': waste_per_case,
            'annual_cases': row['num_cases'],
            'annual_waste_value': round(annual_waste_value, 2),
            'recommendation': recommendation
        })

    results_df = pd.DataFrame(results)

    # Summary
    total_annual_waste = results_df['annual_waste_value'].sum()
    low_utilization_items = len(results_df[results_df['utilization_rate'] < 50])

    summary = {
        'total_annual_waste': round(total_annual_waste, 2),
        'low_utilization_items': low_utilization_items,
        'avg_utilization_rate': round(results_df['utilization_rate'].mean(), 1)
    }

    return results_df, summary

# Example data
or_data = pd.DataFrame({
    'procedure_type': ['Total Hip', 'Total Hip', 'Total Hip', 'Lap Chole', 'Lap Chole'],
    'item_id': ['Implant-A', 'Suture-3-0', 'Sponges', 'Trocar-5mm', 'Clip-Applier'],
    'quantity_picked': [1, 4, 20, 4, 2],
    'quantity_used': [1, 3, 12, 3, 1],
    'unit_cost': [3500, 8, 2, 45, 125],
    'num_cases': [250, 250, 250, 400, 400]
})

or_results, or_summary = analyze_case_cart_utilization(or_data)
print(f"\nTotal annual waste: ${or_summary['total_annual_waste']:,.2f}")
print(f"Items with <50% utilization: {or_summary['low_utilization_items']}")
print("\nTop waste opportunities:")
print(or_results.nlargest(5, 'annual_waste_value')[['item_id', 'procedure', 'utilization_rate', 'annual_waste_value']])
```

### Implant Consignment Optimization

**Consignment Model:**
- Vendor owns inventory until used
- Hospital pays only for what's used
- Vendor manages replenishment

**Financial Analysis:**

```python
def consignment_vs_purchase_analysis(item_data):
    """
    Compare consignment vs. purchase model for implants

    item_data: dict with:
        - annual_usage: Units used per year
        - purchase_price: Price if purchased
        - consignment_fee_pct: Consignment fee (% of price)
        - purchase_holding_cost_rate: Annual holding cost rate
        - avg_inventory_months: Months of inventory if purchased
    """

    # Purchase model costs
    avg_inventory = (item_data['annual_usage'] / 12) * item_data['avg_inventory_months']
    inventory_value = avg_inventory * item_data['purchase_price']
    annual_holding_cost = inventory_value * item_data['purchase_holding_cost_rate']
    annual_purchase_cost = item_data['annual_usage'] * item_data['purchase_price']
    total_purchase_cost = annual_purchase_cost + annual_holding_cost

    # Consignment model costs
    consignment_price = item_data['purchase_price'] * (1 + item_data['consignment_fee_pct'])
    annual_consignment_cost = item_data['annual_usage'] * consignment_price
    consignment_inventory_value = 0  # Vendor-owned

    # Comparison
    savings = total_purchase_cost - annual_consignment_cost

    return {
        'purchase_model': {
            'annual_product_cost': round(annual_purchase_cost, 2),
            'annual_holding_cost': round(annual_holding_cost, 2),
            'total_annual_cost': round(total_purchase_cost, 2),
            'avg_inventory_value': round(inventory_value, 2)
        },
        'consignment_model': {
            'annual_cost': round(annual_consignment_cost, 2),
            'consignment_fee': round(consignment_price - item_data['purchase_price'], 2),
            'inventory_value': 0
        },
        'comparison': {
            'annual_savings': round(savings, 2),
            'inventory_freed': round(inventory_value, 2),
            'recommendation': 'Consignment' if savings > 0 else 'Purchase'
        }
    }

# Example: Hip implant analysis
hip_implant = {
    'annual_usage': 200,
    'purchase_price': 3500,
    'consignment_fee_pct': 0.05,  # 5% consignment fee
    'purchase_holding_cost_rate': 0.20,  # 20% annual holding cost
    'avg_inventory_months': 2  # 2 months safety stock
}

analysis = consignment_vs_purchase_analysis(hip_implant)
print("Purchase Model:")
print(f"  Annual product cost: ${analysis['purchase_model']['annual_product_cost']:,.2f}")
print(f"  Annual holding cost: ${analysis['purchase_model']['annual_holding_cost']:,.2f}")
print(f"  Total: ${analysis['purchase_model']['total_annual_cost']:,.2f}")
print(f"  Inventory value: ${analysis['purchase_model']['avg_inventory_value']:,.2f}")
print("\nConsignment Model:")
print(f"  Annual cost: ${analysis['consignment_model']['annual_cost']:,.2f}")
print(f"  Inventory value: $0 (vendor-owned)")
print(f"\nRecommendation: {analysis['comparison']['recommendation']}")
print(f"Annual savings: ${analysis['comparison']['annual_savings']:,.2f}")
print(f"Cash freed: ${analysis['comparison']['inventory_freed']:,.2f}")
```

---

## Inventory Classification & Management

### ABC-VEN Analysis for Healthcare

**ABC Classification:** Value-based (standard)
- A: High-value items (70-80% of spend)
- B: Medium-value items
- C: Low-value items

**VEN Classification:** Criticality-based (healthcare-specific)
- V (Vital): Life-saving, essential for patient care
- E (Essential): Important but not immediately life-threatening
- N (Non-essential): Desirable but not critical

**Combined ABC-VEN Matrix:**

```python
def abc_ven_classification(items_df):
    """
    Perform ABC-VEN analysis for hospital inventory

    items_df: DataFrame with:
        - item_id: Product identifier
        - annual_usage: Units per year
        - unit_cost: Cost per unit
        - criticality: 'V', 'E', or 'N'
    """

    # ABC analysis
    items_df = items_df.copy()
    items_df['annual_value'] = items_df['annual_usage'] * items_df['unit_cost']
    items_df = items_df.sort_values('annual_value', ascending=False)

    total_value = items_df['annual_value'].sum()
    items_df['cumulative_value'] = items_df['annual_value'].cumsum()
    items_df['cumulative_pct'] = (items_df['cumulative_value'] / total_value) * 100

    def classify_abc(pct):
        if pct <= 80:
            return 'A'
        elif pct <= 95:
            return 'B'
        else:
            return 'C'

    items_df['abc_class'] = items_df['cumulative_pct'].apply(classify_abc)
    items_df['ven_class'] = items_df['criticality']

    # Combined classification
    items_df['abc_ven'] = items_df['abc_class'] + items_df['ven_class']

    # Management strategy
    def management_strategy(abc_ven):
        strategies = {
            'AV': 'Tight control, high safety stock, continuous review, dual sourcing',
            'AE': 'Tight control, medium safety stock, weekly review',
            'AN': 'Standard control, cost optimization priority',
            'BV': 'High safety stock, weekly review, backup supplier',
            'BE': 'Standard control, medium safety stock',
            'BN': 'Relaxed control, minimal safety stock',
            'CV': 'High safety stock despite low value, vendor-managed',
            'CE': 'Standard control, economic order quantities',
            'CN': 'Minimal control, bulk purchasing, consider not stocking'
        }
        return strategies.get(abc_ven, 'Standard management')

    items_df['management_strategy'] = items_df['abc_ven'].apply(management_strategy)

    # Service level recommendations
    def service_level(abc_ven):
        levels = {
            'AV': 99.9, 'AE': 99, 'AN': 97,
            'BV': 99, 'BE': 97, 'BN': 95,
            'CV': 99, 'CE': 95, 'CN': 90
        }
        return levels.get(abc_ven, 95)

    items_df['target_service_level'] = items_df['abc_ven'].apply(service_level)

    return items_df

# Example hospital inventory
hospital_items = pd.DataFrame({
    'item_id': ['Cardiac-Stent', 'IV-Catheter', 'Gauze-4x4', 'Surgical-Gloves-S',
                'Defib-Pads', 'Band-Aid', 'Suture-4-0', 'Trauma-Shears'],
    'annual_usage': [150, 50000, 200000, 75000, 500, 100000, 5000, 2000],
    'unit_cost': [1200, 8, 0.15, 0.30, 45, 0.10, 12, 8],
    'criticality': ['V', 'V', 'E', 'E', 'V', 'N', 'E', 'E']
})

classified = abc_ven_classification(hospital_items)
print(classified[['item_id', 'abc_class', 'ven_class', 'abc_ven', 'target_service_level', 'management_strategy']])
```

---

## Expiry Management & Waste Reduction

### FEFO (First-Expired, First-Out) Tracking

```python
from datetime import datetime, timedelta

def fefo_inventory_management(inventory_lots_df, current_date):
    """
    Manage inventory using FEFO logic and identify expiry risks

    inventory_lots_df: DataFrame with:
        - item_id: Product identifier
        - lot_number: Lot/batch number
        - quantity: Units on hand
        - expiry_date: Expiration date
        - unit_cost: Cost per unit
        - location: Storage location
    """

    inventory_lots_df = inventory_lots_df.copy()
    current_date = pd.to_datetime(current_date)
    inventory_lots_df['expiry_date'] = pd.to_datetime(inventory_lots_df['expiry_date'])

    # Calculate days to expiry
    inventory_lots_df['days_to_expiry'] = (inventory_lots_df['expiry_date'] - current_date).dt.days

    # Risk classification
    def expiry_risk(days):
        if days < 0:
            return 'EXPIRED'
        elif days <= 30:
            return 'CRITICAL'
        elif days <= 90:
            return 'WARNING'
        else:
            return 'NORMAL'

    inventory_lots_df['risk_level'] = inventory_lots_df['days_to_expiry'].apply(expiry_risk)

    # Calculate financial impact
    inventory_lots_df['inventory_value'] = inventory_lots_df['quantity'] * inventory_lots_df['unit_cost']

    # Sort by expiry date (FEFO)
    inventory_lots_df = inventory_lots_df.sort_values(['item_id', 'expiry_date'])

    # At-risk value summary
    risk_summary = inventory_lots_df.groupby('risk_level').agg({
        'inventory_value': 'sum',
        'quantity': 'sum',
        'item_id': 'count'
    }).round(2)

    # Action recommendations
    def action_recommendation(row):
        if row['risk_level'] == 'EXPIRED':
            return 'REMOVE - Quarantine and dispose per policy'
        elif row['risk_level'] == 'CRITICAL':
            return f'URGENT - Use within {row["days_to_expiry"]} days or transfer'
        elif row['risk_level'] == 'WARNING':
            return 'MONITOR - Prioritize usage, check demand forecast'
        else:
            return 'NORMAL - Routine management'

    inventory_lots_df['action'] = inventory_lots_df.apply(action_recommendation, axis=1)

    return inventory_lots_df, risk_summary

# Example inventory with expiry dates
inventory_lots = pd.DataFrame({
    'item_id': ['IV-Solution-001', 'IV-Solution-001', 'Surgical-Suture', 'Contrast-Dye', 'Saline-Flush'],
    'lot_number': ['LOT-2024-A', 'LOT-2024-B', 'LOT-2025-C', 'LOT-2024-X', 'LOT-2025-Y'],
    'quantity': [500, 300, 200, 50, 1000],
    'expiry_date': ['2024-02-15', '2024-06-30', '2025-12-31', '2024-02-01', '2025-08-15'],
    'unit_cost': [4.50, 4.50, 12.00, 85.00, 2.25],
    'location': ['Pharmacy', 'Pharmacy', 'Central Supply', 'Radiology', 'OR']
})

current_date = '2024-02-10'
fefo_results, risk_summary = fefo_inventory_management(inventory_lots, current_date)

print("Expiry Risk Summary:")
print(risk_summary)
print("\nCritical Items Requiring Action:")
print(fefo_results[fefo_results['risk_level'].isin(['EXPIRED', 'CRITICAL'])][
    ['item_id', 'lot_number', 'days_to_expiry', 'inventory_value', 'action']
])
```

---

## Emergency Supply Management

### Crash Cart & Emergency Supply Optimization

```python
def optimize_crash_cart_inventory(crash_cart_data_df):
    """
    Optimize crash cart and emergency supply placement

    crash_cart_data_df: DataFrame with:
        - cart_location: Where cart is located
        - item_id: Emergency medication or supply
        - par_level: Current PAR
        - usage_events: List of usage timestamps
        - expiry_months: Months until expiry
        - unit_cost: Cost per unit
    """

    results = []

    for idx, row in crash_cart_data_df.iterrows():
        usage_events = row['usage_events']
        num_events = len(usage_events) if usage_events else 0

        # Calculate usage frequency
        if num_events > 0:
            usage_per_year = num_events  # Assuming data is annual
            time_between_uses = 365 / num_events if num_events > 0 else 999
        else:
            usage_per_year = 0
            time_between_uses = 999

        # Calculate expiry risk
        expiry_risk_score = row['par_level'] / (row['expiry_months'] / usage_per_year) if usage_per_year > 0 else 0

        # Waste from expiry
        if time_between_uses > (row['expiry_months'] * 30):
            # Likely to expire before use
            annual_expiry_waste = row['par_level'] * (12 / row['expiry_months']) * row['unit_cost']
        else:
            annual_expiry_waste = 0

        # Recommendation
        if usage_per_year == 0 and row['expiry_months'] < 24:
            recommendation = "Remove from cart - no usage, short expiry"
        elif expiry_risk_score > 2:
            recommended_par = max(1, int(row['par_level'] / 2))
            recommendation = f"Reduce PAR to {recommended_par} - expiry risk"
        elif usage_per_year > 12:
            recommendation = "Maintain PAR - frequent usage"
        else:
            recommendation = "Current PAR appropriate"

        results.append({
            'cart_location': row['cart_location'],
            'item_id': row['item_id'],
            'current_par': row['par_level'],
            'annual_usage_events': usage_per_year,
            'days_between_uses': round(time_between_uses, 0),
            'expiry_months': row['expiry_months'],
            'annual_expiry_waste': round(annual_expiry_waste, 2),
            'recommendation': recommendation
        })

    results_df = pd.DataFrame(results)

    total_waste = results_df['annual_expiry_waste'].sum()

    return results_df, {'total_annual_expiry_waste': round(total_waste, 2)}

# Example crash cart data
crash_cart_data = pd.DataFrame({
    'cart_location': ['ICU-Floor-3', 'ICU-Floor-3', 'ER-Main', 'ER-Main', 'Med-Surg-2'],
    'item_id': ['Epinephrine-1mg', 'Atropine-1mg', 'Epinephrine-1mg', 'Narcan-2mg', 'Epinephrine-1mg'],
    'par_level': [10, 8, 10, 15, 8],
    'usage_events': [[1, 2], [], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [1]],
    'expiry_months': [18, 24, 18, 12, 18],
    'unit_cost': [8.50, 6.25, 8.50, 42.00, 8.50]
})

cart_results, cart_summary = optimize_crash_cart_inventory(crash_cart_data)
print("Crash Cart Optimization Results:")
print(cart_results)
print(f"\nTotal annual waste from expiry: ${cart_summary['total_annual_expiry_waste']:,.2f}")
```

---

## Stockout Prevention & Service Levels

### Stockout Analysis & Prevention

```python
def stockout_root_cause_analysis(stockout_data_df):
    """
    Analyze stockout events and identify root causes

    stockout_data_df: DataFrame with:
        - item_id: Product
        - stockout_date: When stockout occurred
        - location: Where it occurred
        - root_cause: Category (PAR_too_low, Delivery_delay, Demand_spike, etc.)
        - clinical_impact: High/Medium/Low
        - duration_hours: How long stockout lasted
    """

    # Root cause frequency
    root_cause_summary = stockout_data_df.groupby('root_cause').agg({
        'item_id': 'count',
        'duration_hours': 'mean'
    }).rename(columns={'item_id': 'occurrences'})

    root_cause_summary['avg_duration_hours'] = root_cause_summary['duration_hours'].round(1)

    # Clinical impact
    impact_summary = stockout_data_df.groupby('clinical_impact').size()

    # Most frequently stocked-out items
    frequent_stockouts = stockout_data_df.groupby('item_id').size().sort_values(ascending=False)

    # Corrective actions by root cause
    def corrective_action(cause):
        actions = {
            'PAR_too_low': 'Increase PAR level based on usage data',
            'Delivery_delay': 'Add safety stock buffer, evaluate supplier performance',
            'Demand_spike': 'Improve demand forecasting, add safety stock for variability',
            'Ordering_error': 'Implement automated replenishment, staff training',
            'Supplier_shortage': 'Identify alternative suppliers, increase lead time buffer',
            'Product_recall': 'Maintain recall reserve stock for critical items',
            'Inventory_error': 'Implement cycle counting, improve inventory accuracy'
        }
        return actions.get(cause, 'Investigate and implement preventive measures')

    root_cause_summary['corrective_action'] = root_cause_summary.index.map(corrective_action)

    return {
        'root_cause_summary': root_cause_summary,
        'impact_summary': impact_summary,
        'frequent_stockouts': frequent_stockouts.head(10),
        'total_stockout_events': len(stockout_data_df)
    }

# Example stockout data
stockout_events = pd.DataFrame({
    'item_id': ['IV-Catheter-22g', 'Surgical-Mask-N95', 'IV-Catheter-22g', 'Saline-1000ml', 'Gloves-L-Sterile'],
    'stockout_date': ['2024-01-15', '2024-01-18', '2024-01-22', '2024-01-25', '2024-02-01'],
    'location': ['ER', 'ICU', 'Med-Surg', 'OR', 'ER'],
    'root_cause': ['Demand_spike', 'Supplier_shortage', 'PAR_too_low', 'Ordering_error', 'Delivery_delay'],
    'clinical_impact': ['High', 'High', 'Medium', 'Low', 'Medium'],
    'duration_hours': [4, 24, 8, 2, 6]
})

stockout_analysis = stockout_root_cause_analysis(stockout_events)
print("Root Cause Summary:")
print(stockout_analysis['root_cause_summary'])
print(f"\nTotal stockout events: {stockout_analysis['total_stockout_events']}")
```

---

## Regulatory Compliance & Quality

### Joint Commission Compliance

**Key Requirements:**
1. **Medication Management (MM)**
   - Proper storage (temperature, security)
   - Expiry date monitoring
   - Accurate labeling
   - High-alert medication controls

2. **Infection Prevention (IC)**
   - Sterile supply management
   - Clean vs. sterile separation
   - Environmental controls
   - Single-use device policies

3. **Environment of Care (EC)**
   - Proper storage conditions
   - Temperature monitoring
   - Security of controlled substances
   - Emergency supply availability

4. **Performance Improvement (PI)**
   - Supply chain metrics tracking
   - Continuous improvement programs
   - Stockout reporting
   - Waste reduction initiatives

### Temperature Monitoring Compliance

```python
def temperature_monitoring_compliance(temp_log_df):
    """
    Monitor temperature logs for compliance with storage requirements

    temp_log_df: DataFrame with:
        - timestamp: Reading time
        - location: Storage area (pharmacy, refrigerator, etc.)
        - temperature_f: Temperature in Fahrenheit
        - required_range: Tuple (min_temp, max_temp)
    """

    temp_log_df = temp_log_df.copy()

    # Check if in range
    def check_compliance(row):
        temp = row['temperature_f']
        min_temp, max_temp = row['required_range']
        return min_temp <= temp <= max_temp

    temp_log_df['compliant'] = temp_log_df.apply(check_compliance, axis=1)
    temp_log_df['deviation'] = temp_log_df.apply(
        lambda row: abs(row['temperature_f'] - np.mean(row['required_range']))
        if not row['compliant'] else 0,
        axis=1
    )

    # Excursion detection (out of range events)
    excursions = temp_log_df[~temp_log_df['compliant']].copy()

    # Summary by location
    compliance_summary = temp_log_df.groupby('location').agg({
        'compliant': ['count', 'sum', 'mean'],
        'deviation': 'max'
    })

    compliance_summary.columns = ['total_readings', 'compliant_readings', 'compliance_rate', 'max_deviation']
    compliance_summary['compliance_rate'] = (compliance_summary['compliance_rate'] * 100).round(2)

    return {
        'compliance_summary': compliance_summary,
        'excursions': excursions,
        'total_excursions': len(excursions)
    }

# Example temperature monitoring data
temp_data = pd.DataFrame({
    'timestamp': pd.date_range('2024-01-01', periods=20, freq='6H'),
    'location': ['Pharmacy-Fridge', 'Pharmacy-Fridge'] * 10,
    'temperature_f': [38, 40, 39, 41, 45, 39, 38, 40, 39, 42, 38, 39, 40, 41, 39, 38, 40, 39, 38, 40],
    'required_range': [(36, 46)] * 20
})

temp_compliance = temperature_monitoring_compliance(temp_data)
print("Temperature Compliance Summary:")
print(temp_compliance['compliance_summary'])
if temp_compliance['total_excursions'] > 0:
    print(f"\n⚠ {temp_compliance['total_excursions']} temperature excursions detected")
    print(temp_compliance['excursions'][['timestamp', 'location', 'temperature_f']])
```

---

## Cost Reduction Strategies

### Supply Standardization Analysis

```python
def standardization_opportunity_analysis(product_usage_df):
    """
    Identify standardization opportunities to reduce SKU count and costs

    product_usage_df: DataFrame with:
        - category: Product category (e.g., 'IV Catheters')
        - item_id: Specific product
        - manufacturer: Product manufacturer
        - annual_usage: Units used per year
        - unit_cost: Cost per unit
        - user_dept: Department using product
    """

    # Group by category to find fragmentation
    category_analysis = []

    for category in product_usage_df['category'].unique():
        cat_data = product_usage_df[product_usage_df['category'] == category]

        num_skus = cat_data['item_id'].nunique()
        num_manufacturers = cat_data['manufacturer'].nunique()
        total_spend = (cat_data['annual_usage'] * cat_data['unit_cost']).sum()

        # Identify top 2 products by usage
        top_products = cat_data.groupby('item_id').agg({
            'annual_usage': 'sum',
            'unit_cost': 'mean'
        }).sort_values('annual_usage', ascending=False).head(2)

        # Calculate potential savings from standardization
        # Assume standardizing to top product with 10% volume discount
        top_product_cost = top_products['unit_cost'].iloc[0]
        standardized_cost = top_product_cost * 0.90  # 10% discount
        current_spend = total_spend
        standardized_spend = cat_data['annual_usage'].sum() * standardized_cost
        potential_savings = current_spend - standardized_spend

        category_analysis.append({
            'category': category,
            'num_skus': num_skus,
            'num_manufacturers': num_manufacturers,
            'total_annual_spend': round(total_spend, 2),
            'potential_savings': round(potential_savings, 2),
            'savings_pct': round((potential_savings / current_spend * 100), 1),
            'recommendation': f'Standardize to top 1-2 products' if num_skus > 3 else 'Appropriate'
        })

    category_df = pd.DataFrame(category_analysis)
    category_df = category_df.sort_values('potential_savings', ascending=False)

    return category_df

# Example product usage data
product_usage = pd.DataFrame({
    'category': ['IV Catheter'] * 6 + ['Surgical Gloves'] * 4,
    'item_id': ['IV-Cat-A', 'IV-Cat-B', 'IV-Cat-C', 'IV-Cat-D', 'IV-Cat-E', 'IV-Cat-F',
                'Glove-X', 'Glove-Y', 'Glove-Z', 'Glove-W'],
    'manufacturer': ['MfgA', 'MfgB', 'MfgA', 'MfgC', 'MfgB', 'MfgD',
                     'MfgX', 'MfgY', 'MfgX', 'MfgZ'],
    'annual_usage': [15000, 8000, 5000, 3000, 2000, 1000,
                     50000, 30000, 15000, 5000],
    'unit_cost': [8.50, 8.75, 8.25, 9.00, 8.50, 8.80,
                  0.35, 0.38, 0.34, 0.40],
    'user_dept': ['ER', 'ICU', 'Med-Surg', 'OR', 'Oncology', 'Peds',
                  'OR', 'ER', 'ICU', 'Clinic']
})

standardization_opps = standardization_opportunity_analysis(product_usage)
print("Standardization Opportunities:")
print(standardization_opps)
print(f"\nTotal potential savings: ${standardization_opps['potential_savings'].sum():,.2f}")
```

---

## Tools & Libraries

### Software Systems

**Materials Management Systems:**
- **GHX**: Supply chain management for healthcare
- **Infor CloudSuite Healthcare**: Materials management & supply chain
- **Oracle Healthcare**: Supply chain & inventory management
- **SAP for Healthcare**: Materials management module
- **Jump Technologies**: Healthcare supply chain platform
- **Tecsys Elite**: Healthcare distribution & logistics

**Inventory Optimization:**
- **OptiFlex**: PAR level optimization
- **R2D2 (Resilience)**: Healthcare inventory analytics
- **LeanTaaS**: OR and supply chain optimization
- **Bluesight**: Medication inventory management

**ERP Integration:**
- **Epic Supply Chain**: Integrated with Epic EHR
- **Cerner**: Supply chain module
- **Meditech**: Materials management

### Python Libraries

**Data Analysis:**
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computations
- `scipy`: Statistical functions
- `statsmodels`: Time series and statistics

**Optimization:**
- `pulp`: Linear programming
- `scipy.optimize`: Optimization algorithms
- `pyomo`: Optimization modeling

**Visualization:**
- `matplotlib`: Plotting and charts
- `seaborn`: Statistical visualization
- `plotly`: Interactive dashboards
- `dash`: Web-based dashboards

---

## Common Challenges & Solutions

### Challenge: High PAR Levels & Excess Inventory

**Problem:**
- Departments hoard supplies
- "Just in case" mentality
- Poor visibility to actual usage

**Solutions:**
- Implement usage-based PAR optimization
- Regular PAR level reviews (quarterly)
- Education on true costs of inventory
- Automated replenishment to reduce hoarding
- Make supplies easily available to reduce fear
- Metrics and accountability by department

### Challenge: OR Supply Waste

**Problem:**
- Overpicked case carts
- Physician preference variation
- Opened but unused items

**Solutions:**
- Track utilization by surgeon and procedure
- Standardize preference cards
- Clinical engagement and education
- Closed-loop supply chain (return unused to stock)
- Real-time tracking of opened items
- Value analysis committee review

### Challenge: Product Expiry & Waste

**Problem:**
- Short-dated products in slow-moving locations
- Poor rotation (FEFO not followed)
- Overstock of expiring items

**Solutions:**
- Automated expiry tracking system
- FEFO enforcement at pick/stock
- Transfer slow-moving stock to high-use areas
- Vendor return agreements
- Reduce PAR levels for slow movers
- Real-time alerts 60-90 days before expiry

### Challenge: Stockouts & Supply Availability

**Problem:**
- Unexpected demand spikes
- Supplier delivery issues
- Inaccurate inventory counts

**Solutions:**
- Safety stock based on variability
- Dual sourcing for critical items
- Vendor-managed inventory (VMI)
- Real-time inventory visibility
- Automated alerts at reorder point
- Cycle counting program
- Emergency supply agreements

### Challenge: Compliance & Regulatory Risk

**Problem:**
- Temperature excursions
- Expired products in use areas
- Controlled substance tracking
- Recall management

**Solutions:**
- Automated temperature monitoring with alerts
- Daily expiry checks required
- Automated controlled substance tracking
- Lot tracking for recall preparedness
- Regular compliance audits
- Staff training and competency assessment
- Electronic tracking systems

### Challenge: Staff Resistance to Change

**Problem:**
- "We've always done it this way"
- Fear of stockouts
- Additional workload concerns

**Solutions:**
- Clinical leadership engagement early
- Pilot programs to demonstrate success
- Address concerns through data
- Simplify processes (less work, not more)
- Quick wins to build trust
- Training and support
- Celebrate successes

---

## Output Format

### Hospital Logistics Optimization Report

**Executive Summary:**
- Current inventory investment by category
- Key performance metrics (turns, service level, waste)
- Recommended improvements and financial impact
- Implementation timeline

**PAR Level Optimization Results:**

| Department | Item | Current PAR | Recommended PAR | Change | Annual Savings |
|------------|------|-------------|-----------------|--------|----------------|
| OR-1 | IV Catheter 22g | 100 | 75 | -25 | $2,500 |
| ICU | Suture 3-0 | 50 | 65 | +15 | ($180) |
| ER | Gauze 4x4 | 500 | 400 | -100 | $60 |

**Inventory Classification:**

| Category | # Items | ABC-VEN Matrix | Target Service Level | Management Strategy |
|----------|---------|----------------|---------------------|---------------------|
| Cardiac Implants | 45 | AV | 99.9% | Consignment, tight control |
| IV Supplies | 120 | BV/BE | 98% | Weekly review, standard PAR |
| General Supplies | 850 | CE/CN | 95% | Monthly review, automated |

**Waste Reduction Opportunities:**

| Opportunity | Current Annual Waste | Improvement Action | Potential Savings |
|-------------|---------------------|-------------------|-------------------|
| OR Case Cart Over-picking | $125,000 | Standardize preference cards | $87,500 |
| Product Expiry | $68,000 | FEFO + expiry monitoring | $51,000 |
| Excess PAR Levels | $45,000 | Right-size PARs | $45,000 |
| SKU Proliferation | $92,000 | Standardization program | $64,400 |
| **Total** | **$330,000** | | **$247,900** |

**Implementation Roadmap:**

**Phase 1 (Months 1-3): Foundation**
- Implement PAR optimization for top 20% items (A items)
- Deploy expiry tracking system
- Begin OR utilization tracking

**Phase 2 (Months 4-6): Expansion**
- Roll out optimized PARs to all locations
- Launch standardization program
- Implement automated replenishment

**Phase 3 (Months 7-12): Optimization**
- Continuous improvement based on data
- Expand to all product categories
- Advanced analytics and forecasting

**Key Performance Indicators:**

| Metric | Baseline | Target | Timeline |
|--------|----------|--------|----------|
| Inventory Turns | 8.5 | 12.0 | 12 months |
| Stockout Rate | 2.3% | 0.5% | 6 months |
| Expiry Waste | $68K/year | $17K/year | 9 months |
| OR Utilization Rate | 67% | 85% | 12 months |
| Days on Hand | 43 | 30 | 12 months |

---

## Questions to Ask

If you need more context:

1. What type of healthcare facility? (acute care, specialty, ambulatory)
2. How many beds? Annual patient volume?
3. What materials management system is currently in use?
4. What's the current inventory investment and turnover rate?
5. What are the biggest pain points? (stockouts, expiry, cost, compliance)
6. What distribution model is used? (requisition, exchange cart, case cart)
7. Are there specific departments or product categories to focus on?
8. What compliance or regulatory requirements must be met?
9. What's the implementation timeline and budget?
10. Who are the key stakeholders? (materials management, nursing, physicians, finance)

---

## Related Skills

- **pharmacy-supply-chain**: Pharmacy-specific supply chain operations
- **medical-device-distribution**: Medical device logistics and distribution
- **clinical-trial-logistics**: Clinical trial supply management
- **value-analysis**: Healthcare value analysis and product evaluation
- **inventory-optimization**: General inventory optimization techniques
- **demand-forecasting**: Forecasting methods applicable to healthcare
- **compliance-management**: Regulatory compliance and quality management
- **warehouse-slotting-optimization**: Optimizing storage locations
- **track-and-trace**: Product traceability and serialization
