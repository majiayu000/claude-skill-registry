---
name: shelf-life-management
description: When the user wants to manage product shelf life, implement FEFO (First-Expired-First-Out), optimize freshness, or handle perishable products. Also use when the user mentions "expiration management," "date code tracking," "FEFO," "freshness optimization," "waste reduction," "markdown management," or "spoilage prevention." For food supply chain, see food-beverage-supply-chain. For pharmaceutical expiry, see pharmaceutical-supply-chain.
---

# Shelf Life Management

You are an expert in shelf life management and perishable product supply chain optimization. Your goal is to help minimize waste, maximize freshness, optimize inventory rotation, and ensure product quality through expiration date management.

## Initial Assessment

Before implementing shelf life management, understand:

1. **Product Characteristics**
   - What products have shelf life concerns? (food, pharma, cosmetics)
   - What are the shelf lives? (days, weeks, months)
   - Storage requirements? (ambient, refrigerated, frozen)
   - Regulatory requirements? (FDA, USDA, EU regulations)
   - Date code format? (use-by, sell-by, best-before, manufacturing date)

2. **Current State**
   - Current waste/spoilage rate? (% of inventory)
   - Inventory rotation method? (FIFO, FEFO, manual)
   - Date code tracking capability? (WMS, manual)
   - Markdown/clearance process?
   - Customer complaints about freshness?

3. **Supply Chain Characteristics**
   - Lead times from production to shelf?
   - Number of nodes (plants, DCs, stores)?
   - Replenishment frequency?
   - Promotional activity impact?

4. **Business Impact**
   - Annual waste cost (spoilage + markdown)?
   - Lost sales from stockouts?
   - Customer satisfaction issues?
   - Compliance penalties or recalls?

---

## Shelf Life Management Framework

### Shelf Life Definitions

**Key Date Types:**

1. **Manufacturing Date**
   - When product was produced
   - Starting point for shelf life calculation

2. **Expiration Date / Use-By Date**
   - Last date product should be used/consumed
   - Safety concern (especially food, pharma)
   - Regulatory requirement

3. **Best-Before Date**
   - Quality date (not safety)
   - Product may still be safe but quality degrades
   - Common in food products

4. **Sell-By Date**
   - Last date retailer should sell product
   - Provides buffer before expiration
   - Typical: expiration date minus X days

**Remaining Shelf Life (RSL):**
```
RSL = Expiration Date - Current Date
RSL % = (Expiration Date - Current Date) / (Expiration Date - Manufacturing Date) × 100
```

### Shelf Life Zones

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class ShelfLifeManager:
    """
    Manage shelf life and expiration dates
    """

    def __init__(self, shelf_life_days):
        self.shelf_life_days = shelf_life_days

        # Define shelf life zones
        self.zones = {
            'green': {'min_pct': 67, 'max_pct': 100, 'action': 'Normal sales'},
            'yellow': {'min_pct': 33, 'max_pct': 67, 'action': 'Priority sales'},
            'red': {'min_pct': 10, 'max_pct': 33, 'action': 'Markdown/clearance'},
            'expired': {'min_pct': 0, 'max_pct': 10, 'action': 'Pull from shelf'}
        }

    def calculate_rsl(self, manufacturing_date, current_date=None):
        """Calculate remaining shelf life"""

        if current_date is None:
            current_date = datetime.now()

        # Convert to datetime if strings
        if isinstance(manufacturing_date, str):
            manufacturing_date = pd.to_datetime(manufacturing_date)
        if isinstance(current_date, str):
            current_date = pd.to_datetime(current_date)

        expiration_date = manufacturing_date + timedelta(days=self.shelf_life_days)
        rsl_days = (expiration_date - current_date).days
        rsl_pct = (rsl_days / self.shelf_life_days) * 100

        return {
            'manufacturing_date': manufacturing_date,
            'expiration_date': expiration_date,
            'current_date': current_date,
            'rsl_days': max(0, rsl_days),
            'rsl_pct': max(0, rsl_pct),
            'expired': rsl_days <= 0
        }

    def classify_zone(self, rsl_pct):
        """Classify product into shelf life zone"""

        for zone_name, zone_info in self.zones.items():
            if zone_info['min_pct'] <= rsl_pct < zone_info['max_pct']:
                return {
                    'zone': zone_name,
                    'action': zone_info['action']
                }

        return {'zone': 'expired', 'action': 'Pull from shelf'}

    def generate_shelf_life_report(self, inventory_df):
        """
        Generate shelf life report for inventory

        Parameters:
        - inventory_df: DataFrame with columns ['sku', 'lot', 'manufacturing_date',
                       'quantity', 'location']

        Returns:
        - report with expiration analysis
        """

        current_date = datetime.now()

        # Calculate RSL for each lot
        inventory_df['rsl_info'] = inventory_df['manufacturing_date'].apply(
            lambda x: self.calculate_rsl(x, current_date)
        )

        # Extract RSL values
        inventory_df['rsl_days'] = inventory_df['rsl_info'].apply(lambda x: x['rsl_days'])
        inventory_df['rsl_pct'] = inventory_df['rsl_info'].apply(lambda x: x['rsl_pct'])
        inventory_df['expiration_date'] = inventory_df['rsl_info'].apply(
            lambda x: x['expiration_date']
        )
        inventory_df['expired'] = inventory_df['rsl_info'].apply(lambda x: x['expired'])

        # Classify zones
        inventory_df['zone_info'] = inventory_df['rsl_pct'].apply(self.classify_zone)
        inventory_df['zone'] = inventory_df['zone_info'].apply(lambda x: x['zone'])
        inventory_df['action'] = inventory_df['zone_info'].apply(lambda x: x['action'])

        # Summary by zone
        zone_summary = inventory_df.groupby('zone').agg({
            'quantity': 'sum',
            'lot': 'count'
        }).rename(columns={'lot': 'num_lots'})

        # Expiring soon (next 7 days)
        expiring_soon = inventory_df[
            (inventory_df['rsl_days'] <= 7) &
            (inventory_df['rsl_days'] > 0)
        ]

        # Expired inventory
        expired_inventory = inventory_df[inventory_df['expired'] == True]

        report = {
            'total_inventory': inventory_df['quantity'].sum(),
            'total_lots': len(inventory_df),
            'zone_summary': zone_summary,
            'expiring_soon_7days': {
                'quantity': expiring_soon['quantity'].sum(),
                'lots': len(expiring_soon),
                'details': expiring_soon[['sku', 'lot', 'quantity', 'rsl_days', 'location']]
            },
            'expired': {
                'quantity': expired_inventory['quantity'].sum(),
                'lots': len(expired_inventory),
                'details': expired_inventory[['sku', 'lot', 'quantity', 'expiration_date', 'location']]
            }
        }

        return report


# Example usage
manager = ShelfLifeManager(shelf_life_days=120)  # 120-day shelf life

inventory = pd.DataFrame({
    'sku': ['SKU_A', 'SKU_A', 'SKU_A', 'SKU_B', 'SKU_B'],
    'lot': ['LOT001', 'LOT002', 'LOT003', 'LOT004', 'LOT005'],
    'manufacturing_date': [
        datetime.now() - timedelta(days=100),  # Old
        datetime.now() - timedelta(days=60),   # Medium
        datetime.now() - timedelta(days=10),   # Fresh
        datetime.now() - timedelta(days=125),  # Expired
        datetime.now() - timedelta(days=80)    # Medium
    ],
    'quantity': [500, 1000, 1500, 200, 800],
    'location': ['DC1', 'DC1', 'DC2', 'DC1', 'DC2']
})

report = manager.generate_shelf_life_report(inventory)

print("Zone Summary:")
print(report['zone_summary'])
print(f"\nExpiring in 7 days: {report['expiring_soon_7days']['quantity']} units")
print(f"Expired: {report['expired']['quantity']} units")
```

---

## FEFO (First-Expired-First-Out) Implementation

### FEFO Allocation Logic

```python
class FEFOInventoryManager:
    """
    Implement FEFO (First-Expired-First-Out) inventory allocation
    """

    def __init__(self, inventory_df):
        """
        Initialize with inventory

        Parameters:
        - inventory_df: DataFrame with columns ['sku', 'lot', 'expiration_date',
                       'quantity', 'location']
        """
        self.inventory = inventory_df.copy()

    def allocate_order(self, sku, quantity_needed, location=None,
                        min_rsl_days=None):
        """
        Allocate inventory using FEFO logic

        Parameters:
        - sku: product SKU
        - quantity_needed: quantity to allocate
        - location: preferred location (None = any)
        - min_rsl_days: minimum remaining shelf life (customer requirement)

        Returns:
        - allocation list of lots
        """

        # Filter to SKU
        available = self.inventory[
            (self.inventory['sku'] == sku) &
            (self.inventory['quantity'] > 0)
        ].copy()

        # Filter by location if specified
        if location:
            available = available[available['location'] == location]

        # Filter by minimum RSL if specified
        if min_rsl_days:
            current_date = datetime.now()
            available = available[
                (available['expiration_date'] - current_date).dt.days >= min_rsl_days
            ]

        # Sort by expiration date (earliest first) - FEFO
        available = available.sort_values('expiration_date')

        # Allocate
        allocation = []
        remaining_need = quantity_needed

        for idx, row in available.iterrows():
            if remaining_need <= 0:
                break

            # Allocate from this lot
            allocate_qty = min(remaining_need, row['quantity'])

            allocation.append({
                'sku': sku,
                'lot': row['lot'],
                'location': row['location'],
                'expiration_date': row['expiration_date'],
                'quantity': allocate_qty,
                'rsl_days': (row['expiration_date'] - datetime.now()).days
            })

            # Update remaining need
            remaining_need -= allocate_qty

            # Update inventory
            self.inventory.loc[idx, 'quantity'] -= allocate_qty

        # Check if fully allocated
        allocated_qty = sum(a['quantity'] for a in allocation)
        shortage = quantity_needed - allocated_qty

        return {
            'allocated': allocation,
            'total_allocated': allocated_qty,
            'shortage': shortage,
            'fill_rate': allocated_qty / quantity_needed if quantity_needed > 0 else 0
        }

    def get_inventory_summary(self):
        """Get current inventory summary"""

        summary = self.inventory.groupby(['sku', 'location']).agg({
            'quantity': 'sum',
            'lot': 'count',
            'expiration_date': ['min', 'max']
        })

        return summary


# Example
inventory = pd.DataFrame({
    'sku': ['SKU_A', 'SKU_A', 'SKU_A', 'SKU_A'],
    'lot': ['LOT001', 'LOT002', 'LOT003', 'LOT004'],
    'expiration_date': pd.to_datetime([
        '2025-03-15',
        '2025-04-20',
        '2025-02-10',  # Oldest - should allocate first
        '2025-05-01'
    ]),
    'quantity': [500, 800, 300, 1000],
    'location': ['DC1', 'DC1', 'DC1', 'DC2']
})

fefo = FEFOInventoryManager(inventory)

# Allocate order
order = fefo.allocate_order(
    sku='SKU_A',
    quantity_needed=1000,
    location='DC1',
    min_rsl_days=30  # Customer requires 30 days min shelf life
)

print("Allocation:")
for alloc in order['allocated']:
    print(f"  Lot {alloc['lot']}: {alloc['quantity']} units, "
          f"RSL: {alloc['rsl_days']} days")

print(f"\nTotal Allocated: {order['total_allocated']}")
print(f"Shortage: {order['shortage']}")
```

---

## Waste Reduction Strategies

### Dynamic Markdown Optimization

```python
import numpy as np
from scipy.optimize import minimize_scalar

def optimize_markdown_timing(current_rsl_days, regular_price, cost,
                              demand_elasticity=-2.0):
    """
    Optimize when to markdown product to minimize waste

    Parameters:
    - current_rsl_days: remaining shelf life
    - regular_price: normal selling price
    - cost: product cost
    - demand_elasticity: price elasticity of demand

    Returns:
    - optimal markdown timing and price
    """

    def expected_profit(markdown_day):
        """Calculate expected profit if markdown starts on given day"""

        # Days at full price
        days_full_price = min(markdown_day, current_rsl_days)

        # Days at markdown price
        days_markdown = max(0, current_rsl_days - markdown_day)

        # Demand curves (simplified)
        daily_demand_full = 10  # Base demand at full price
        markdown_pct = min(0.5, days_markdown / current_rsl_days)  # Up to 50% off
        markdown_price = regular_price * (1 - markdown_pct)

        # Increased demand due to markdown
        demand_lift = (markdown_pct / 0.5) ** (-demand_elasticity)
        daily_demand_markdown = daily_demand_full * demand_lift

        # Total sales
        sales_full_price = days_full_price * daily_demand_full * regular_price
        sales_markdown = days_markdown * daily_demand_markdown * markdown_price

        # Costs
        units_sold = (days_full_price * daily_demand_full +
                     days_markdown * daily_demand_markdown)
        total_cost = units_sold * cost

        # Profit
        profit = sales_full_price + sales_markdown - total_cost

        # Penalty for waste (unsold inventory)
        # Assume some units don't sell even with markdown
        waste = max(0, 100 - units_sold)  # Assume started with 100 units
        waste_cost = waste * cost

        return profit - waste_cost

    # Optimize markdown day
    result = minimize_scalar(
        lambda x: -expected_profit(x),  # Negative for maximization
        bounds=(0, current_rsl_days),
        method='bounded'
    )

    optimal_day = int(result.x)
    optimal_profit = -result.fun

    # Calculate optimal markdown percentage
    markdown_pct = min(0.5, (current_rsl_days - optimal_day) / current_rsl_days)

    return {
        'optimal_markdown_day': optimal_day,
        'days_until_markdown': optimal_day,
        'markdown_pct': markdown_pct * 100,
        'markdown_price': regular_price * (1 - markdown_pct),
        'expected_profit': optimal_profit
    }


# Example
markdown_strategy = optimize_markdown_timing(
    current_rsl_days=30,
    regular_price=10.00,
    cost=6.00,
    demand_elasticity=-2.0
)

print(f"Start markdown in: {markdown_strategy['days_until_markdown']} days")
print(f"Markdown %: {markdown_strategy['markdown_pct']:.0f}%")
print(f"Markdown Price: ${markdown_strategy['markdown_price']:.2f}")
```

### Waste Tracking and Analysis

```python
class WasteAnalyzer:
    """
    Track and analyze waste from expiration
    """

    def __init__(self):
        self.waste_records = []

    def record_waste(self, waste_data):
        """Record waste event"""
        self.waste_records.append(waste_data)

    def analyze_waste(self):
        """Analyze waste patterns"""

        if not self.waste_records:
            return None

        df = pd.DataFrame(self.waste_records)

        analysis = {
            'total_waste_units': df['quantity'].sum(),
            'total_waste_value': (df['quantity'] * df['unit_cost']).sum(),
            'waste_by_sku': df.groupby('sku').agg({
                'quantity': 'sum',
                'unit_cost': lambda x: (df.loc[x.index, 'quantity'] * x).sum()
            }),
            'waste_by_location': df.groupby('location')['quantity'].sum(),
            'waste_by_reason': df.groupby('reason')['quantity'].sum(),
            'avg_rsl_at_waste': df['rsl_at_waste'].mean()
        }

        # Root cause analysis
        analysis['top_waste_skus'] = analysis['waste_by_sku'].nlargest(10, 'quantity')

        # Calculate waste rate
        if 'total_demand' in df.columns:
            analysis['waste_rate'] = (
                df['quantity'].sum() / df['total_demand'].sum() * 100
            )

        return analysis

    def identify_waste_drivers(self):
        """Identify key drivers of waste"""

        df = pd.DataFrame(self.waste_records)

        drivers = {}

        # 1. Overstocking
        overstock_waste = df[df['reason'] == 'overstock']
        drivers['overstock'] = {
            'waste_pct': len(overstock_waste) / len(df) * 100,
            'value': (overstock_waste['quantity'] * overstock_waste['unit_cost']).sum()
        }

        # 2. Long lead times
        long_lt_waste = df[df['lead_time_days'] > 14]
        drivers['long_lead_time'] = {
            'waste_pct': len(long_lt_waste) / len(df) * 100,
            'value': (long_lt_waste['quantity'] * long_lt_waste['unit_cost']).sum()
        }

        # 3. Poor forecasting
        forecast_error_waste = df[df['forecast_error_pct'].abs() > 20]
        drivers['forecast_error'] = {
            'waste_pct': len(forecast_error_waste) / len(df) * 100,
            'value': (forecast_error_waste['quantity'] *
                     forecast_error_waste['unit_cost']).sum()
        }

        # 4. Improper rotation (should be FEFO but wasn't)
        rotation_waste = df[df['reason'] == 'improper_rotation']
        drivers['improper_rotation'] = {
            'waste_pct': len(rotation_waste) / len(df) * 100,
            'value': (rotation_waste['quantity'] * rotation_waste['unit_cost']).sum()
        }

        return drivers


# Example
analyzer = WasteAnalyzer()

# Record waste events
analyzer.record_waste({
    'date': '2025-01-15',
    'sku': 'SKU_A',
    'location': 'DC1',
    'quantity': 100,
    'unit_cost': 5.00,
    'reason': 'overstock',
    'rsl_at_waste': 0,
    'lead_time_days': 21,
    'forecast_error_pct': 35,
    'total_demand': 500
})

analysis = analyzer.analyze_waste()
drivers = analyzer.identify_waste_drivers()

print(f"Total Waste Value: ${analysis['total_waste_value']:,.0f}")
print(f"Waste Rate: {analysis.get('waste_rate', 0):.1f}%")
print("\nWaste Drivers:")
for driver, data in drivers.items():
    print(f"  {driver}: {data['waste_pct']:.0f}% of waste, ${data['value']:,.0f}")
```

---

## Freshness Optimization

### Supplier Selection Based on Age

```python
def select_supplier_by_freshness(suppliers, demand, min_rsl_required):
    """
    Select suppliers to maximize freshness

    Parameters:
    - suppliers: list of suppliers with available product and RSL
    - demand: total demand to fulfill
    - min_rsl_required: minimum RSL acceptable

    Returns:
    - optimal supplier selection
    """

    from pulp import *

    # Create problem
    prob = LpProblem("Freshness_Optimization", LpMaximize)

    # Decision variables: quantity from each supplier
    x = LpVariable.dicts("Quantity",
                          [s['supplier_id'] for s in suppliers],
                          lowBound=0,
                          cat='Continuous')

    # Objective: Maximize weighted freshness
    # Higher RSL = better
    objective = lpSum([
        x[s['supplier_id']] * s['rsl_days']
        for s in suppliers
    ])

    prob += objective

    # Constraints

    # 1. Meet demand
    prob += lpSum([x[s['supplier_id']] for s in suppliers]) >= demand

    # 2. Supplier capacity
    for s in suppliers:
        prob += x[s['supplier_id']] <= s['available_quantity']

    # 3. Minimum RSL
    for s in suppliers:
        if s['rsl_days'] < min_rsl_required:
            prob += x[s['supplier_id']] == 0

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract results
    results = []
    for s in suppliers:
        qty = x[s['supplier_id']].varValue
        if qty > 0:
            results.append({
                'supplier': s['supplier_id'],
                'quantity': qty,
                'rsl_days': s['rsl_days'],
                'cost': qty * s['unit_cost']
            })

    total_qty = sum(r['quantity'] for r in results)
    weighted_rsl = sum(r['quantity'] * r['rsl_days'] for r in results) / total_qty

    return {
        'allocation': results,
        'total_quantity': total_qty,
        'weighted_avg_rsl': weighted_rsl,
        'total_cost': sum(r['cost'] for r in results)
    }


# Example
suppliers = [
    {
        'supplier_id': 'Supplier_A',
        'available_quantity': 500,
        'rsl_days': 90,
        'unit_cost': 5.00
    },
    {
        'supplier_id': 'Supplier_B',
        'available_quantity': 800,
        'rsl_days': 60,
        'unit_cost': 4.80
    },
    {
        'supplier_id': 'Supplier_C',
        'available_quantity': 400,
        'rsl_days': 120,  # Freshest
        'unit_cost': 5.20
    }
]

result = select_supplier_by_freshness(
    suppliers=suppliers,
    demand=1000,
    min_rsl_required=45
)

print("Supplier Allocation:")
for alloc in result['allocation']:
    print(f"  {alloc['supplier']}: {alloc['quantity']} units, "
          f"RSL: {alloc['rsl_days']} days")

print(f"\nWeighted Avg RSL: {result['weighted_avg_rsl']:.0f} days")
```

---

## Regulatory Compliance

### Date Code Management

```python
class DateCodeManager:
    """
    Manage date codes and regulatory compliance
    """

    def __init__(self, date_format='%Y%m%d'):
        self.date_format = date_format

    def parse_date_code(self, date_code, code_type='manufacturing'):
        """
        Parse date code to datetime

        Common formats:
        - YYYYMMDD: 20250115
        - YYMMDD: 250115
        - Julian: 25015 (year + day of year)
        """

        if len(date_code) == 8:  # YYYYMMDD
            return datetime.strptime(date_code, '%Y%m%d')
        elif len(date_code) == 6:  # YYMMDD
            return datetime.strptime(date_code, '%y%m%d')
        elif len(date_code) == 5:  # Julian YYDDD
            year = int('20' + date_code[:2])
            day_of_year = int(date_code[2:])
            return datetime(year, 1, 1) + timedelta(days=day_of_year - 1)
        else:
            raise ValueError(f"Unknown date code format: {date_code}")

    def validate_date_code(self, date_code, product_type='food'):
        """
        Validate date code meets regulatory requirements

        Requirements vary by region and product type
        """

        try:
            parsed_date = self.parse_date_code(date_code)
        except:
            return {'valid': False, 'reason': 'Invalid date code format'}

        current_date = datetime.now()

        # Check if manufacturing date is not in future
        if parsed_date > current_date:
            return {'valid': False, 'reason': 'Manufacturing date in future'}

        # Check if too old (product-specific)
        max_age_days = {
            'food_fresh': 30,
            'food_frozen': 365,
            'food_shelf_stable': 730,
            'pharma': 1825,  # 5 years typically
            'cosmetics': 730
        }

        age_days = (current_date - parsed_date).days
        max_age = max_age_days.get(product_type, 365)

        if age_days > max_age:
            return {
                'valid': False,
                'reason': f'Product too old: {age_days} days (max: {max_age})'
            }

        return {'valid': True, 'parsed_date': parsed_date, 'age_days': age_days}

    def calculate_expiration_date(self, manufacturing_date, shelf_life_days,
                                    sell_by_buffer_days=0):
        """
        Calculate expiration and sell-by dates

        Parameters:
        - manufacturing_date: when product was made
        - shelf_life_days: total shelf life
        - sell_by_buffer_days: days before expiration to stop selling

        Returns:
        - expiration_date, sell_by_date
        """

        if isinstance(manufacturing_date, str):
            manufacturing_date = self.parse_date_code(manufacturing_date)

        expiration_date = manufacturing_date + timedelta(days=shelf_life_days)
        sell_by_date = expiration_date - timedelta(days=sell_by_buffer_days)

        return {
            'manufacturing_date': manufacturing_date,
            'expiration_date': expiration_date,
            'sell_by_date': sell_by_date,
            'shelf_life_days': shelf_life_days
        }


# Example
manager = DateCodeManager()

# Parse date code
date_info = manager.parse_date_code('20250115')
print(f"Parsed Date: {date_info}")

# Validate
validation = manager.validate_date_code('20250115', product_type='food_shelf_stable')
print(f"Valid: {validation['valid']}")

# Calculate expiration
expiry = manager.calculate_expiration_date(
    manufacturing_date='20250115',
    shelf_life_days=180,
    sell_by_buffer_days=7
)

print(f"Expiration Date: {expiry['expiration_date']}")
print(f"Sell-By Date: {expiry['sell_by_date']}")
```

---

## Tools & Technologies

### Shelf Life Management Software

**Warehouse Management Systems (WMS) with FEFO:**
- **Manhattan Associates WMS**: Advanced FEFO and lot tracking
- **Blue Yonder WMS**: Shelf life management
- **SAP EWM**: Extended warehouse management with expiry
- **Oracle WMS**: Date code and FEFO support
- **HighJump WMS**: Perishables management

**Specialized Solutions:**
- **FoodLogiQ**: Food traceability and date code management
- **Trace Register**: Supply chain traceability
- **rfxcel**: Serialization and expiry tracking
- **FreshSurety**: Shelf life and temperature monitoring
- **ZestIOT**: Real-time freshness monitoring

**Markdown Optimization:**
- **Revionics**: Price and markdown optimization (Oracle)
- **Pricefx**: Dynamic pricing with expiry
- **PROS**: AI-driven markdown optimization

### Python Libraries

```python
# Date handling
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Optimization
from pulp import *
from scipy.optimize import minimize, minimize_scalar

# Machine learning for forecasting
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

# Data visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
```

---

## Common Challenges & Solutions

### Challenge: High Waste Rate

**Problem:**
- 5-10% of inventory expires
- Significant cost impact
- Lost revenue

**Solutions:**
- Implement FEFO rigorously
- Reduce order quantities (more frequent orders)
- Improve demand forecasting
- Dynamic safety stock (reduce as expiration approaches)
- Markdown earlier and more aggressively
- Donate near-expiry (tax benefit, goodwill)

### Challenge: Inconsistent Date Code Formats

**Problem:**
- Suppliers use different formats
- Manual tracking error-prone
- Compliance risk

**Solutions:**
- Standardize date code format across suppliers
- Automated date code parsing (OCR, barcode)
- Validation at receiving
- WMS integration
- Master data management

### Challenge: Customer Freshness Requirements

**Problem:**
- Retailers require 75% minimum RSL
- Limits usable inventory
- Increases waste at DC

**Solutions:**
- Negotiate RSL requirements
- Price incentives for lower RSL
- Fast replenishment to stores
- Allocate fresher stock to demanding customers
- Use older stock for promotions

### Challenge: Multi-Echelon Complexity

**Problem:**
- DCs hold aging inventory
- Stores also have freshness requirements
- Difficult to optimize across network

**Solutions:**
- Network-wide visibility of RSL
- Centralized allocation (freshest to furthest)
- Dynamic routing based on expiry
- Cross-docking for fast movers
- DC bypass for fresh products

---

## Output Format

### Shelf Life Performance Report

**Executive Summary:**
- Total Inventory: 500,000 units
- Waste Rate: 3.2% (down from 5.1% last year)
- Waste Value: $320,000 annually
- Average RSL at Sale: 68%
- Compliance: 100% (no expired products sold)

**Expiration Summary:**

| Zone | Units | % of Total | Action Required |
|------|-------|------------|-----------------|
| Green (>67% RSL) | 350,000 | 70% | Normal sales |
| Yellow (33-67% RSL) | 100,000 | 20% | Priority outbound |
| Red (10-33% RSL) | 45,000 | 9% | Markdown now |
| Expired (<10% RSL) | 5,000 | 1% | Pull immediately |

**Expiring in Next 30 Days:**

| SKU | Location | Quantity | Exp Date | RSL Days | Action |
|-----|----------|----------|----------|----------|--------|
| SKU_A | DC1 | 2,500 | 2025-02-15 | 15 | 30% markdown |
| SKU_B | DC2 | 1,200 | 2025-02-10 | 10 | 50% markdown |
| SKU_C | DC1 | 800 | 2025-02-05 | 5 | Pull/donate |

**Waste Analysis:**

| Category | Waste Units | Value | % of Total Waste |
|----------|-------------|-------|------------------|
| Overstock | 8,000 | $160,000 | 50% |
| Forecast Error | 4,000 | $80,000 | 25% |
| Long Lead Time | 3,000 | $60,000 | 18.75% |
| Improper Rotation | 1,000 | $20,000 | 6.25% |

**Recommendations:**
1. Implement automated FEFO allocation (reduce rotation errors)
2. Reduce order quantities for SKU_A, SKU_B (high waste items)
3. Earlier markdown trigger for slow movers (Red zone → markdown at 40% RSL)
4. Partner with food bank for donation program
5. Negotiate extended RSL requirements with retailers

---

## Questions to Ask

If you need more context:
1. What products have shelf life concerns? Shelf life duration?
2. Current waste/spoilage rate and cost?
3. Do you have FEFO capability in WMS?
4. What are customer RSL requirements?
5. Date code tracking and format?
6. Markdown process and timing?
7. Multi-echelon network or single location?
8. Regulatory requirements (FDA, USDA, etc.)?

---

## Related Skills

- **inventory-optimization**: For safety stock with expiration constraints
- **demand-forecasting**: To reduce overstock and waste
- **warehouse-slotting-optimization**: For FEFO-friendly slotting
- **food-beverage-supply-chain**: For perishable product supply chain
- **pharmaceutical-supply-chain**: For drug expiry management
- **markdown-optimization**: For price optimization of expiring products
- **quality-management**: For quality control and compliance
- **replenishment-strategy**: For optimal reorder policies with expiry
