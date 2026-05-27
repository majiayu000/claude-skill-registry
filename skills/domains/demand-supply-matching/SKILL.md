---
name: demand-supply-matching
description: When the user wants to balance demand and supply, resolve supply-demand mismatches, or optimize fulfillment allocation. Also use when the user mentions "demand-supply balancing," "ATP," "available-to-promise," "allocation," "supply rationing," "fulfillment optimization," "demand prioritization," or "supply allocation." For forecasting, see demand-forecasting. For S&OP, see sales-operations-planning.
---

# Demand-Supply Matching

You are an expert in demand-supply matching and fulfillment optimization. Your goal is to help organizations effectively balance demand and supply, optimize allocation decisions, and maximize customer service while minimizing costs and inefficiencies.

## Initial Assessment

Before implementing demand-supply matching, understand:

1. **Business Context**
   - What's driving matching needs? (supply constraints, demand volatility, growth)
   - Current matching process and pain points?
   - Service level objectives by customer/channel?
   - Cost of mismatches (shortages vs. excess)?

2. **Demand Characteristics**
   - Demand predictability and variability?
   - Customer/channel segmentation?
   - Priority rules and commitments?
   - Seasonality and promotions?

3. **Supply Constraints**
   - Production capacity limitations?
   - Supplier capacity and lead times?
   - Inventory availability across network?
   - Transportation and logistics constraints?

4. **Complexity Factors**
   - Multi-plant, multi-DC network?
   - Global vs. regional operations?
   - Product complexity (BOM depth, variants)?
   - Perishability or shelf-life issues?

---

## Demand-Supply Matching Framework

### Matching Scenarios

**1. Unconstrained (Supply > Demand)**
- Fulfill all demand
- Optimize fulfillment source
- Minimize costs
- Manage excess inventory

**2. Constrained (Demand > Supply)**
- Allocate limited supply
- Prioritize customers/orders
- Balance service and revenue
- Communicate shortfalls

**3. Balanced (Supply ≈ Demand)**
- Optimize matching
- Buffer for uncertainty
- Monitor closely
- Prepare for swings

### Allocation Strategies

**1. First-Come, First-Served (FCFS)**
- Simple, fair
- No prioritization
- May not optimize value
- Risk of strategic orders

**2. Pro-Rata Allocation**
- Proportional to demand
- Fair across customers
- Doesn't consider customer value
- Simple to implement

**3. Priority-Based Allocation**
- Strategic customer priority
- Contract commitments first
- Revenue or margin optimization
- May strain low-priority customers

**4. Optimization-Based Allocation**
- Maximize objective (revenue, margin, service)
- Consider constraints
- Most complex
- Best financial outcome

---

## Available-to-Promise (ATP) Logic

### ATP Calculation

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class ATPEngine:
    """Available-to-Promise calculation engine"""

    def __init__(self):
        self.inventory_positions = {}
        self.supply_schedule = []
        self.demand_schedule = []
        self.allocations = []

    def add_inventory_position(self, location, product_id, on_hand, in_transit=0):
        """
        Add current inventory position

        on_hand: Physical inventory
        in_transit: Confirmed receipts en route
        """

        key = (location, product_id)
        self.inventory_positions[key] = {
            'location': location,
            'product_id': product_id,
            'on_hand': on_hand,
            'in_transit': in_transit,
            'available': on_hand,  # Available = on_hand - allocated
            'allocated': 0
        }

    def add_supply(self, location, product_id, quantity, receipt_date):
        """Add future supply (production, purchases, transfers)"""

        self.supply_schedule.append({
            'location': location,
            'product_id': product_id,
            'quantity': quantity,
            'receipt_date': receipt_date,
            'type': 'supply'
        })

    def add_demand(self, location, product_id, quantity, required_date, priority=5):
        """
        Add demand requirement

        priority: 1 (highest) to 10 (lowest)
        """

        self.demand_schedule.append({
            'location': location,
            'product_id': product_id,
            'quantity': quantity,
            'required_date': required_date,
            'priority': priority,
            'type': 'demand',
            'allocated_quantity': 0,
            'status': 'Pending'
        })

    def calculate_atp(self, location, product_id, horizon_days=30):
        """
        Calculate Available-to-Promise for a product-location

        Returns ATP by time period
        """

        key = (location, product_id)

        if key not in self.inventory_positions:
            return None

        # Starting position
        current_available = self.inventory_positions[key]['on_hand']

        # Get relevant supply and demand
        supplies = [s for s in self.supply_schedule
                   if s['location'] == location and s['product_id'] == product_id]

        demands = [d for d in self.demand_schedule
                  if d['location'] == location and d['product_id'] == product_id]

        # Sort by date
        supplies.sort(key=lambda x: x['receipt_date'])
        demands.sort(key=lambda x: x['required_date'])

        # Calculate ATP by period
        today = datetime.now().date()
        atp_schedule = []

        for day_offset in range(horizon_days + 1):
            target_date = today + timedelta(days=day_offset)

            # Add supplies arriving on or before this date
            supplies_today = sum(s['quantity'] for s in supplies
                               if s['receipt_date'] <= target_date)

            # Subtract demands required on or before this date
            demands_today = sum(d['quantity'] for d in demands
                              if d['required_date'] <= target_date)

            atp = current_available + supplies_today - demands_today

            atp_schedule.append({
                'date': target_date,
                'day_offset': day_offset,
                'atp': max(0, atp),  # ATP cannot be negative
                'cumulative_supply': supplies_today,
                'cumulative_demand': demands_today
            })

        return pd.DataFrame(atp_schedule)

    def allocate_supply(self, allocation_method='priority'):
        """
        Allocate available supply to demands

        allocation_method: 'priority', 'fcfs', 'pro_rata'
        """

        if allocation_method == 'priority':
            return self._allocate_by_priority()
        elif allocation_method == 'fcfs':
            return self._allocate_fcfs()
        elif allocation_method == 'pro_rata':
            return self._allocate_pro_rata()
        else:
            raise ValueError(f"Unknown allocation method: {allocation_method}")

    def _allocate_by_priority(self):
        """Allocate supply based on demand priority"""

        # Sort demands by priority (1 = highest) then by date
        sorted_demands = sorted(self.demand_schedule,
                               key=lambda x: (x['priority'], x['required_date']))

        allocations = []

        for demand in sorted_demands:
            location = demand['location']
            product_id = demand['product_id']
            quantity_needed = demand['quantity']

            key = (location, product_id)

            if key not in self.inventory_positions:
                continue

            available = self.inventory_positions[key]['available']

            if available > 0:
                # Allocate as much as possible
                allocated = min(quantity_needed, available)

                # Update available inventory
                self.inventory_positions[key]['available'] -= allocated
                self.inventory_positions[key]['allocated'] += allocated

                # Update demand
                demand['allocated_quantity'] = allocated
                demand['status'] = 'Fulfilled' if allocated == quantity_needed else 'Partial'

                allocations.append({
                    'location': location,
                    'product_id': product_id,
                    'required_date': demand['required_date'],
                    'priority': demand['priority'],
                    'requested_quantity': quantity_needed,
                    'allocated_quantity': allocated,
                    'shortfall': quantity_needed - allocated
                })

        return pd.DataFrame(allocations)

    def _allocate_fcfs(self):
        """Allocate supply first-come, first-served (by date)"""

        # Sort by required date
        sorted_demands = sorted(self.demand_schedule, key=lambda x: x['required_date'])

        allocations = []

        for demand in sorted_demands:
            location = demand['location']
            product_id = demand['product_id']
            quantity_needed = demand['quantity']

            key = (location, product_id)

            if key not in self.inventory_positions:
                continue

            available = self.inventory_positions[key]['available']

            if available > 0:
                allocated = min(quantity_needed, available)

                self.inventory_positions[key]['available'] -= allocated
                self.inventory_positions[key]['allocated'] += allocated

                demand['allocated_quantity'] = allocated
                demand['status'] = 'Fulfilled' if allocated == quantity_needed else 'Partial'

                allocations.append({
                    'location': location,
                    'product_id': product_id,
                    'required_date': demand['required_date'],
                    'requested_quantity': quantity_needed,
                    'allocated_quantity': allocated,
                    'shortfall': quantity_needed - allocated
                })

        return pd.DataFrame(allocations)

    def _allocate_pro_rata(self):
        """Allocate supply proportionally across all demands"""

        # Group demands by location and product
        demand_groups = {}

        for demand in self.demand_schedule:
            key = (demand['location'], demand['product_id'])
            if key not in demand_groups:
                demand_groups[key] = []
            demand_groups[key].append(demand)

        allocations = []

        for key, demands in demand_groups.items():
            location, product_id = key

            if key not in self.inventory_positions:
                continue

            available = self.inventory_positions[key]['available']
            total_demand = sum(d['quantity'] for d in demands)

            if total_demand == 0:
                continue

            # Calculate allocation ratio
            allocation_ratio = min(1.0, available / total_demand)

            for demand in demands:
                allocated = int(demand['quantity'] * allocation_ratio)

                demand['allocated_quantity'] = allocated
                demand['status'] = 'Fulfilled' if allocated == demand['quantity'] else 'Partial'

                allocations.append({
                    'location': location,
                    'product_id': product_id,
                    'required_date': demand['required_date'],
                    'priority': demand.get('priority', 5),
                    'requested_quantity': demand['quantity'],
                    'allocated_quantity': allocated,
                    'allocation_ratio': allocation_ratio,
                    'shortfall': demand['quantity'] - allocated
                })

            self.inventory_positions[key]['allocated'] = sum(a['allocated_quantity'] for a in allocations if a['location'] == location and a['product_id'] == product_id)
            self.inventory_positions[key]['available'] = available - self.inventory_positions[key]['allocated']

        return pd.DataFrame(allocations)

    def generate_shortage_report(self):
        """Generate report of unfulfilled demands"""

        shortages = []

        for demand in self.demand_schedule:
            if demand['status'] in ['Pending', 'Partial']:
                shortfall = demand['quantity'] - demand['allocated_quantity']

                shortages.append({
                    'location': demand['location'],
                    'product_id': demand['product_id'],
                    'required_date': demand['required_date'],
                    'priority': demand['priority'],
                    'requested_quantity': demand['quantity'],
                    'allocated_quantity': demand['allocated_quantity'],
                    'shortfall': shortfall,
                    'status': demand['status']
                })

        return pd.DataFrame(shortages) if shortages else pd.DataFrame()


# Example ATP and allocation
atp_engine = ATPEngine()

# Add inventory positions
atp_engine.add_inventory_position('DC1', 'PROD001', on_hand=1000, in_transit=500)
atp_engine.add_inventory_position('DC2', 'PROD001', on_hand=800, in_transit=300)

# Add future supply
atp_engine.add_supply('DC1', 'PROD001', 500, datetime.now().date() + timedelta(days=10))
atp_engine.add_supply('DC1', 'PROD001', 700, datetime.now().date() + timedelta(days=20))

# Add demands with priorities
atp_engine.add_demand('DC1', 'PROD001', 600, datetime.now().date() + timedelta(days=5), priority=1)  # High priority
atp_engine.add_demand('DC1', 'PROD001', 400, datetime.now().date() + timedelta(days=7), priority=3)
atp_engine.add_demand('DC1', 'PROD001', 500, datetime.now().date() + timedelta(days=12), priority=2)
atp_engine.add_demand('DC1', 'PROD001', 300, datetime.now().date() + timedelta(days=15), priority=5)  # Low priority

# Calculate ATP
atp = atp_engine.calculate_atp('DC1', 'PROD001', horizon_days=30)
print("Available-to-Promise Schedule:")
print(atp[atp['day_offset'] % 5 == 0][['day_offset', 'atp', 'cumulative_supply', 'cumulative_demand']])  # Show every 5 days

# Allocate supply (priority-based)
print("\n\nPriority-Based Allocation:")
allocations = atp_engine.allocate_supply(allocation_method='priority')
print(allocations[['product_id', 'required_date', 'priority', 'requested_quantity', 'allocated_quantity', 'shortfall']])

# Generate shortage report
shortages = atp_engine.generate_shortage_report()
print("\n\nShortage Report:")
if not shortages.empty:
    print(shortages[['product_id', 'required_date', 'priority', 'shortfall', 'status']])
else:
    print("No shortages - all demands fulfilled")
```

---

## Optimization-Based Allocation

### Multi-Objective Allocation Optimization

```python
from scipy.optimize import linprog
import numpy as np

class OptimizedAllocation:
    """Optimization-based demand-supply matching"""

    def optimize_allocation(self, supply_data, demand_data, customer_priorities):
        """
        Optimize allocation to maximize weighted service level

        supply_data: dict {location: {product: quantity}}
        demand_data: list of dicts with customer, product, quantity, location
        customer_priorities: dict {customer: weight} (1-10, higher = more important)
        """

        # Build optimization problem
        # Decision variables: allocation[i] for each demand i

        n_demands = len(demand_data)

        # Objective: Maximize weighted fulfillment
        # Higher priority customers get more weight
        c = []  # Coefficients for objective (negative because linprog minimizes)
        for demand in demand_data:
            customer = demand['customer']
            weight = customer_priorities.get(customer, 5)  # Default weight 5
            c.append(-weight * demand['quantity'])  # Negative for maximization

        c = np.array(c)

        # Constraints: Supply constraints
        # Sum of allocations for each product-location <= available supply

        A_ub = []  # Inequality constraint matrix
        b_ub = []  # Inequality constraint bounds

        # Group demands by product-location
        product_location_demands = {}
        for i, demand in enumerate(demand_data):
            key = (demand['product'], demand['location'])
            if key not in product_location_demands:
                product_location_demands[key] = []
            product_location_demands[key].append(i)

        # Create constraint for each product-location
        for (product, location), demand_indices in product_location_demands.items():
            constraint_row = np.zeros(n_demands)
            for idx in demand_indices:
                constraint_row[idx] = 1  # Sum allocations for this product-location

            A_ub.append(constraint_row)

            # Available supply for this product-location
            available_supply = supply_data.get(location, {}).get(product, 0)
            b_ub.append(available_supply)

        A_ub = np.array(A_ub)
        b_ub = np.array(b_ub)

        # Bounds: 0 <= allocation[i] <= demand[i]
        bounds = [(0, demand['quantity']) for demand in demand_data]

        # Solve
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

        if result.success:
            allocations = result.x

            # Create allocation results
            allocation_results = []
            for i, demand in enumerate(demand_data):
                allocated = round(allocations[i], 2)
                fulfillment_rate = (allocated / demand['quantity'] * 100) if demand['quantity'] > 0 else 100

                allocation_results.append({
                    'customer': demand['customer'],
                    'product': demand['product'],
                    'location': demand['location'],
                    'requested': demand['quantity'],
                    'allocated': allocated,
                    'fulfillment_rate': round(fulfillment_rate, 1),
                    'priority_weight': customer_priorities.get(demand['customer'], 5)
                })

            return {
                'success': True,
                'allocations': pd.DataFrame(allocation_results),
                'objective_value': -result.fun,  # Negative because we minimized negative
                'solver_status': result.message
            }
        else:
            return {
                'success': False,
                'message': result.message
            }


# Example optimization
optimizer = OptimizedAllocation()

# Supply availability
supply = {
    'DC1': {'PROD001': 1000, 'PROD002': 800},
    'DC2': {'PROD001': 600, 'PROD002': 500}
}

# Demands
demands = [
    {'customer': 'CUST_A', 'product': 'PROD001', 'location': 'DC1', 'quantity': 600},
    {'customer': 'CUST_B', 'product': 'PROD001', 'location': 'DC1', 'quantity': 500},
    {'customer': 'CUST_C', 'product': 'PROD001', 'location': 'DC1', 'quantity': 400},
    {'customer': 'CUST_A', 'product': 'PROD002', 'location': 'DC1', 'quantity': 300},
    {'customer': 'CUST_D', 'product': 'PROD002', 'location': 'DC1', 'quantity': 700},
]

# Customer priorities (1-10, 10 = highest)
priorities = {
    'CUST_A': 10,  # Strategic customer
    'CUST_B': 7,
    'CUST_C': 5,
    'CUST_D': 3
}

# Optimize
result = optimizer.optimize_allocation(supply, demands, priorities)

if result['success']:
    print("Optimized Allocation:")
    print(result['allocations'])
    print(f"\nObjective Value (Weighted Fulfillment): {result['objective_value']:.2f}")
else:
    print(f"Optimization failed: {result['message']}")
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `scipy.optimize`: Linear and non-linear optimization
- `pulp`: Linear programming
- `pyomo`: Optimization modeling
- `ortools`: Google OR-Tools

**Data Processing:**
- `pandas`: Data manipulation
- `numpy`: Numerical computations

**Forecasting Integration:**
- `statsmodels`: Statistical models
- `prophet`: Forecasting

### Commercial Software

**Planning & Allocation:**
- **Blue Yonder**: Allocation and fulfillment
- **Kinaxis RapidResponse**: S&OP and allocation
- **o9 Solutions**: Demand-supply matching
- **SAP IBP**: Integrated business planning
- **Oracle Demantra**: Demand and supply planning

**Order Management:**
- **Manhattan OMS**: Order management and allocation
- **Blue Yonder Order Management**: Fulfillment optimization
- **Fluent Commerce**: Order orchestration
- **Salesforce Order Management**: Commerce cloud

**ATP/CTP Engines:**
- **SAP ATP**: Available-to-promise
- **Oracle ATP**: Global order promising
- **Kinaxis ATP**: Real-time promising

---

## Common Challenges & Solutions

### Challenge: Conflicting Objectives

**Problem:**
- Maximize revenue vs. customer fairness
- Short-term profit vs. long-term relationships
- Service level vs. cost
- Competing stakeholder interests

**Solutions:**
- Multi-objective optimization with weights
- Clear prioritization framework
- Scenario analysis to show trade-offs
- Executive governance for conflicts
- Customer tier classification
- Balanced scorecards

### Challenge: Dynamic Conditions

**Problem:**
- Demand and supply constantly changing
- Need for frequent re-optimization
- Orders arriving continuously
- Real-time updates required

**Solutions:**
- Event-driven matching (trigger on changes)
- Periodic re-optimization cycles
- Rolling horizon approach
- Reservation and release logic
- Buffer for uncertainty
- Near-real-time systems

### Challenge: Data Quality

**Problem:**
- Inaccurate inventory positions
- Outdated supply schedules
- Forecast errors
- System delays

**Solutions:**
- Real-time inventory visibility
- Automated data feeds
- Data validation and reconciliation
- Buffer for data uncertainty
- Regular cycle counting
- Safety margins in ATP

### Challenge: Customer Communication

**Problem:**
- Managing expectations on allocation
- Explaining shortfalls
- Transparency vs. competitive information
- Fairness perception

**Solutions:**
- Clear allocation policies communicated upfront
- Proactive shortage notifications
- Alternative options offered
- Historical allocation transparency
- Customer portal with visibility
- Regular business reviews

### Challenge: Complexity at Scale

**Problem:**
- Large number of SKUs, locations, customers
- Computational time for optimization
- Combinatorial explosion
- Network constraints

**Solutions:**
- Hierarchical optimization (aggregate then detail)
- Heuristic approaches for large problems
- Parallel processing
- Incremental updates vs. full re-optimization
- Simplification where possible
- High-performance computing

### Challenge: Cross-Functional Alignment

**Problem:**
- Sales wants maximum fulfillment
- Finance wants inventory reduction
- Operations wants stability
- Misaligned incentives

**Solutions:**
- Shared KPIs and goals
- Integrated S&OP process
- Cross-functional governance
- Transparent decision rules
- Regular alignment meetings
- Executive sponsorship

---

## Output Format

### Demand-Supply Matching Report

**Executive Summary:**
- Overall demand-supply balance
- Allocation decisions made
- Shortfalls and impacts
- Actions required

**Supply-Demand Balance:**

| Product | Total Demand | Total Supply | Balance | Status |
|---------|--------------|--------------|---------|--------|
| PROD001 | 2,500 | 2,800 | +300 | ✓ Surplus |
| PROD002 | 1,800 | 1,500 | -300 | ⚠ Shortage |
| PROD003 | 1,200 | 1,200 | 0 | ✓ Balanced |
| PROD004 | 950 | 600 | -350 | ⚠⚠ Critical Shortage |

**Allocation Results:**

| Customer | Product | Requested | Allocated | Fulfillment % | Priority | Status |
|----------|---------|-----------|-----------|---------------|----------|--------|
| CUST_A | PROD001 | 600 | 600 | 100% | 1 | Fulfilled |
| CUST_B | PROD001 | 500 | 500 | 100% | 3 | Fulfilled |
| CUST_C | PROD002 | 800 | 600 | 75% | 2 | Partial |
| CUST_D | PROD002 | 500 | 0 | 0% | 5 | Unfulfilled |

**Shortage Impact:**

| Product | Shortage Qty | Affected Customers | Revenue at Risk | Mitigation Actions |
|---------|-------------|-------------------|-----------------|-------------------|
| PROD002 | 300 | 2 | $45K | Expedite production, substitute PROD003 |
| PROD004 | 350 | 3 | $28K | Allocate to strategic customers only |

**ATP Horizon:**

| Product | Location | Today | Week 1 | Week 2 | Week 3 | Week 4 |
|---------|----------|-------|--------|--------|--------|--------|
| PROD001 | DC1 | 400 | 650 | 1,100 | 1,300 | 1,200 |
| PROD002 | DC1 | 0 | 200 | 600 | 800 | 750 |

**Action Items:**

| Priority | Action | Owner | Due Date | Status |
|----------|--------|-------|----------|--------|
| Critical | Expedite PROD002 production | Operations | Tomorrow | In Progress |
| High | Communicate shortfalls to affected customers | Sales | Today | Pending |
| Medium | Evaluate substitute products for PROD004 | Product Mgmt | This week | Planning |

---

## Questions to Ask

If you need more context:
1. What's the current demand-supply balance situation?
2. What allocation method is preferred? (priority, pro-rata, optimization)
3. What customer segmentation or prioritization exists?
4. What are the service level objectives?
5. What supply constraints exist? (capacity, inventory, logistics)
6. How frequently does matching need to occur?
7. What systems provide demand and supply data?
8. What's the cost of shortages vs. excess?
9. Are there substitutable products?
10. What decision authority exists for allocation?

---

## Related Skills

- **demand-forecasting**: For accurate demand inputs
- **sales-operations-planning**: For integrated demand-supply planning
- **inventory-optimization**: For safety stock and buffer decisions
- **capacity-planning**: For supply capacity constraints
- **supplier-collaboration**: For collaborative supply planning
- **control-tower-design**: For real-time visibility and monitoring
- **network-design**: For optimizing fulfillment network
- **route-optimization**: For logistics constraints in matching
