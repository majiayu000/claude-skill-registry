---
name: co-packing-management
description: When the user wants to manage co-packing operations, select co-packers, optimize contract manufacturing, or coordinate outsourced production. Also use when the user mentions "contract manufacturing," "third-party manufacturing," "co-man," "toll manufacturing," "private label," "contract packaging," or "outsourced production." For capacity planning, see capacity-planning. For supplier selection, see supplier-selection.
---

# Co-Packing Management

You are an expert in co-packing (contract packaging/manufacturing) operations and supply chain management. Your goal is to help optimize co-packer selection, manage co-packer relationships, and ensure seamless integration of contract manufacturing into the supply chain.

## Initial Assessment

Before managing co-packing operations, understand:

1. **Business Context**
   - Why use co-packing? (capacity, seasonal surge, new products, geographic expansion)
   - What products for co-packing? (volume, SKU complexity)
   - Current manufacturing footprint? (own plants, co-packers)
   - What percentage outsourced vs. internal? (target mix)

2. **Product Characteristics**
   - Product types? (beverages, snacks, personal care, etc.)
   - Packaging complexity? (pouches, bottles, cans, multi-pack)
   - Shelf stability? (ambient, refrigerated, frozen)
   - Quality requirements and specifications?
   - Regulatory compliance? (FDA, USDA, organic, kosher, etc.)

3. **Volume and Capacity**
   - Annual volume requirements?
   - Seasonality patterns?
   - Minimum order quantities (MOQs)?
   - Lead times needed?
   - Growth projections?

4. **Current State**
   - Existing co-packer relationships?
   - Current performance issues?
   - Quality metrics and defect rates?
   - Cost structure and competitiveness?

---

## Co-Packing Strategy Framework

### Make vs. Buy Decision

**When to Use Co-Packers:**

1. **Capacity Constraints**
   - Own plants at capacity
   - Seasonal peaks exceed internal capacity
   - Faster time-to-market than building plant

2. **Geographic Expansion**
   - Enter new markets without capital investment
   - Reduce freight costs with regional production
   - Meet local content requirements

3. **Product Specialization**
   - Specialized equipment/processes (aseptic, HPP, freeze-dry)
   - Small volumes don't justify investment
   - Test market new products

4. **Cost Optimization**
   - Lower cost than internal production
   - Variable cost structure (vs. fixed plant costs)
   - Avoid capital expenditure

5. **Risk Mitigation**
   - Backup capacity for supply resilience
   - Diversify supplier base
   - Flexibility for demand uncertainty

**When to Keep Internal:**
- Core products with high volume
- Proprietary processes or trade secrets
- Quality-critical products
- High-margin products
- Strategic capabilities

---

## Co-Packer Selection Process

### Selection Criteria Matrix

```python
import pandas as pd
import numpy as np

def score_copacker_candidates(candidates_df, weights):
    """
    Score and rank co-packer candidates using weighted criteria

    Parameters:
    - candidates_df: DataFrame with candidate scores on each criterion
    - weights: dict with importance weights for each criterion

    Returns:
    - ranked candidates with total scores
    """

    criteria = [
        'quality_capability',
        'capacity_availability',
        'cost_competitiveness',
        'technical_expertise',
        'geographic_location',
        'financial_stability',
        'certifications',
        'equipment_technology',
        'flexibility',
        'customer_service',
        'lead_times',
        'track_record'
    ]

    # Calculate weighted scores
    candidates_df['total_score'] = 0

    for criterion in criteria:
        weight = weights.get(criterion, 1.0)
        candidates_df['total_score'] += (
            candidates_df[criterion] * weight
        )

    # Normalize to 100
    candidates_df['total_score'] = (
        candidates_df['total_score'] /
        candidates_df['total_score'].max() * 100
    )

    # Rank
    candidates_df['rank'] = candidates_df['total_score'].rank(
        ascending=False,
        method='dense'
    )

    return candidates_df.sort_values('rank')


# Example usage
candidates = pd.DataFrame({
    'copacker_name': ['CoPackA', 'CoPackB', 'CoPackC'],
    'quality_capability': [9, 8, 7],
    'capacity_availability': [7, 9, 8],
    'cost_competitiveness': [6, 8, 9],
    'technical_expertise': [9, 7, 6],
    'geographic_location': [8, 6, 9],
    'financial_stability': [9, 8, 7],
    'certifications': [9, 8, 8],
    'equipment_technology': [8, 9, 7],
    'flexibility': [7, 8, 9],
    'customer_service': [8, 7, 9],
    'lead_times': [7, 9, 8],
    'track_record': [9, 8, 8]
})

weights = {
    'quality_capability': 2.0,      # Double weight for quality
    'cost_competitiveness': 1.5,    # 1.5x for cost
    'capacity_availability': 1.5,   # 1.5x for capacity
    'certifications': 1.5,          # 1.5x for compliance
    # All others: 1.0 (default)
}

ranked = score_copacker_candidates(candidates, weights)
print(ranked[['copacker_name', 'rank', 'total_score']].head())
```

### Due Diligence Checklist

**Phase 1: Initial Qualification**
- [ ] Financial stability (D&B rating, financial statements)
- [ ] Certifications (SQF, BRC, GMP, organic, kosher, halal)
- [ ] Capacity and availability
- [ ] Equipment and technology match
- [ ] Geographic location
- [ ] References from current customers

**Phase 2: Detailed Assessment**
- [ ] Plant audit and quality assessment
- [ ] Production trials and sample approval
- [ ] Cost model and pricing structure
- [ ] Lead times and MOQs
- [ ] Service level agreements
- [ ] IT systems and integration capabilities

**Phase 3: Contract Negotiation**
- [ ] Pricing terms and escalation
- [ ] Volume commitments and flexibility
- [ ] Quality standards and specifications
- [ ] Liability and insurance
- [ ] IP protection and confidentiality
- [ ] Exit terms and transition plan

---

## Co-Packer Relationship Management

### Contract Structure

```python
class CoPackerContract:
    """
    Model co-packer contract terms and economics
    """

    def __init__(self, contract_terms):
        self.copacker = contract_terms['copacker_name']
        self.start_date = contract_terms['start_date']
        self.term_length = contract_terms['term_months']
        self.pricing = contract_terms['pricing']
        self.volumes = contract_terms['volume_commitments']
        self.quality_terms = contract_terms['quality_sla']

    def calculate_total_cost(self, actual_volume):
        """
        Calculate total cost including all fees

        Components:
        - Base manufacturing cost (per unit or per case)
        - Material cost (if co-packer sources)
        - Packaging cost
        - Storage fees
        - Setup/changeover fees
        - Quality testing fees
        - Other fees (expedite, special handling)
        """

        # Base cost (typically tiered by volume)
        base_cost = self._calculate_base_cost(actual_volume)

        # Materials (if applicable)
        material_cost = actual_volume * self.pricing.get('material_cost_per_unit', 0)

        # Packaging
        packaging_cost = actual_volume * self.pricing.get('packaging_cost_per_unit', 0)

        # Fixed fees
        setup_fees = self.pricing.get('setup_fee_per_run', 0) * \
                     self._calculate_production_runs(actual_volume)

        storage_fees = self.pricing.get('storage_fee_per_month', 0) * \
                      self._estimate_storage_months(actual_volume)

        testing_fees = self.pricing.get('testing_fee_per_lot', 0) * \
                      self._calculate_lots(actual_volume)

        total_cost = (
            base_cost +
            material_cost +
            packaging_cost +
            setup_fees +
            storage_fees +
            testing_fees
        )

        return {
            'total_cost': total_cost,
            'cost_per_unit': total_cost / actual_volume,
            'breakdown': {
                'base_cost': base_cost,
                'material_cost': material_cost,
                'packaging_cost': packaging_cost,
                'setup_fees': setup_fees,
                'storage_fees': storage_fees,
                'testing_fees': testing_fees
            }
        }

    def _calculate_base_cost(self, volume):
        """Calculate base manufacturing cost with volume tiers"""

        pricing_tiers = self.pricing['base_cost_tiers']

        for tier in sorted(pricing_tiers, key=lambda x: x['min_volume'], reverse=True):
            if volume >= tier['min_volume']:
                return volume * tier['cost_per_unit']

        # If below all tiers, use highest cost
        return volume * pricing_tiers[0]['cost_per_unit']

    def _calculate_production_runs(self, volume):
        """Estimate number of production runs"""
        lot_size = self.pricing.get('typical_lot_size', 10000)
        return int(np.ceil(volume / lot_size))

    def _calculate_lots(self, volume):
        """Calculate number of QC lots"""
        lot_size = self.pricing.get('qc_lot_size', 5000)
        return int(np.ceil(volume / lot_size))

    def _estimate_storage_months(self, volume):
        """Estimate storage duration"""
        # Simplified: assume storage for 1 month
        return 1

    def check_minimum_commitment(self, actual_volume):
        """Check if minimum volume commitment met"""

        min_annual = self.volumes.get('minimum_annual', 0)
        shortfall = max(0, min_annual - actual_volume)

        if shortfall > 0:
            penalty = shortfall * self.pricing.get('shortfall_penalty_per_unit', 0)
            return {
                'commitment_met': False,
                'shortfall': shortfall,
                'penalty': penalty
            }

        return {'commitment_met': True, 'shortfall': 0, 'penalty': 0}


# Example contract
contract_terms = {
    'copacker_name': 'ABC Co-Packing',
    'start_date': '2025-01-01',
    'term_months': 12,
    'pricing': {
        'base_cost_tiers': [
            {'min_volume': 100000, 'cost_per_unit': 2.50},
            {'min_volume': 50000, 'cost_per_unit': 2.75},
            {'min_volume': 0, 'cost_per_unit': 3.00}
        ],
        'material_cost_per_unit': 1.50,
        'packaging_cost_per_unit': 0.75,
        'setup_fee_per_run': 2500,
        'storage_fee_per_month': 1000,
        'testing_fee_per_lot': 500,
        'typical_lot_size': 10000,
        'qc_lot_size': 10000,
        'shortfall_penalty_per_unit': 0.50
    },
    'volume_commitments': {
        'minimum_annual': 75000
    },
    'quality_sla': {
        'max_defect_rate': 0.005,
        'on_time_delivery': 0.95
    }
}

contract = CoPackerContract(contract_terms)
cost_analysis = contract.calculate_total_cost(actual_volume=80000)

print(f"Total Cost: ${cost_analysis['total_cost']:,.0f}")
print(f"Cost per Unit: ${cost_analysis['cost_per_unit']:.2f}")
```

---

## Supply Chain Coordination

### Demand Planning and Forecasting

```python
def plan_copacker_orders(demand_forecast, lead_time_weeks, safety_stock_weeks,
                          moq, lot_size):
    """
    Plan co-packer orders based on demand forecast

    Parameters:
    - demand_forecast: weekly demand forecast
    - lead_time_weeks: co-packer lead time
    - safety_stock_weeks: weeks of safety stock
    - moq: minimum order quantity
    - lot_size: production lot size (for rounding)

    Returns:
    - order plan with timing and quantities
    """

    order_plan = []

    for week, demand in enumerate(demand_forecast):
        # Calculate order point
        lead_time_demand = sum(demand_forecast[week:week+lead_time_weeks])
        safety_stock = demand * safety_stock_weeks

        order_point = lead_time_demand + safety_stock

        # Current inventory
        current_inventory = calculate_current_inventory(week)

        # Order if below order point
        if current_inventory < order_point:
            order_qty = order_point - current_inventory

            # Round up to MOQ
            if order_qty < moq:
                order_qty = moq

            # Round up to lot size
            order_qty = int(np.ceil(order_qty / lot_size) * lot_size)

            order_plan.append({
                'order_week': week,
                'order_qty': order_qty,
                'delivery_week': week + lead_time_weeks,
                'demand': demand,
                'inventory_before': current_inventory,
                'inventory_after': current_inventory + order_qty
            })

    return order_plan
```

### Quality Management

```python
class CoPackerQualityManager:
    """
    Manage quality metrics and SLA compliance for co-packers
    """

    def __init__(self, quality_sla):
        self.sla = quality_sla
        self.quality_data = []

    def record_lot_inspection(self, lot_data):
        """Record quality inspection results for a production lot"""

        inspection = {
            'lot_number': lot_data['lot_number'],
            'date': lot_data['date'],
            'quantity': lot_data['quantity'],
            'defects_found': lot_data['defects'],
            'defect_rate': lot_data['defects'] / lot_data['quantity'],
            'accepted': lot_data['defects'] / lot_data['quantity'] <= self.sla['max_defect_rate']
        }

        self.quality_data.append(inspection)

        return inspection

    def calculate_performance_metrics(self):
        """Calculate quality performance metrics"""

        if not self.quality_data:
            return None

        df = pd.DataFrame(self.quality_data)

        metrics = {
            'total_lots': len(df),
            'accepted_lots': df['accepted'].sum(),
            'rejected_lots': (~df['accepted']).sum(),
            'acceptance_rate': df['accepted'].mean() * 100,
            'avg_defect_rate': df['defect_rate'].mean() * 100,
            'total_defects': df['defects_found'].sum(),
            'total_units_inspected': df['quantity'].sum()
        }

        # SLA compliance
        metrics['meets_quality_sla'] = (
            metrics['avg_defect_rate'] <= self.sla['max_defect_rate'] * 100
        )

        return metrics

    def generate_quality_report(self):
        """Generate quality scorecard"""

        metrics = self.calculate_performance_metrics()

        if metrics is None:
            return "No quality data available"

        report = f"""
Co-Packer Quality Performance Report

Total Lots Inspected: {metrics['total_lots']}
Accepted: {metrics['accepted_lots']} ({metrics['acceptance_rate']:.1f}%)
Rejected: {metrics['rejected_lots']}

Average Defect Rate: {metrics['avg_defect_rate']:.2f}%
SLA Target: {self.sla['max_defect_rate']*100:.2f}%
SLA Status: {'✓ PASS' if metrics['meets_quality_sla'] else '✗ FAIL'}

Total Units Inspected: {metrics['total_units_inspected']:,}
Total Defects: {metrics['total_defects']}
"""

        return report


# Example usage
quality_sla = {'max_defect_rate': 0.005}  # 0.5% max defects
qm = CoPackerQualityManager(quality_sla)

# Record inspections
qm.record_lot_inspection({
    'lot_number': 'LOT001',
    'date': '2025-01-15',
    'quantity': 10000,
    'defects': 45
})

qm.record_lot_inspection({
    'lot_number': 'LOT002',
    'date': '2025-01-22',
    'quantity': 10000,
    'defects': 52
})

print(qm.generate_quality_report())
```

---

## Cost Optimization

### Make vs. Buy Economic Analysis

```python
def make_vs_buy_analysis(internal_costs, copacker_costs, annual_volume):
    """
    Analyze economics of internal production vs. co-packing

    Parameters:
    - internal_costs: dict with internal cost structure
    - copacker_costs: dict with co-packer pricing
    - annual_volume: expected annual volume

    Returns:
    - cost comparison and recommendation
    """

    # Internal production costs
    internal_fixed = internal_costs.get('fixed_costs_annual', 0)
    internal_variable = internal_costs.get('variable_cost_per_unit', 0)
    internal_total = internal_fixed + (internal_variable * annual_volume)

    # Co-packer costs
    copacker_variable = copacker_costs.get('cost_per_unit', 0)
    copacker_fixed = copacker_costs.get('annual_fees', 0)
    copacker_total = copacker_fixed + (copacker_variable * annual_volume)

    # Comparison
    savings = internal_total - copacker_total
    savings_pct = savings / internal_total * 100 if internal_total > 0 else 0

    # Break-even volume
    if internal_variable < copacker_variable:
        # Internal has lower variable cost
        breakeven = internal_fixed / (copacker_variable - internal_variable)
    else:
        # Co-packer has lower variable cost
        breakeven = (copacker_fixed - internal_fixed) / (internal_variable - copacker_variable)

    recommendation = 'Make Internal' if internal_total < copacker_total else 'Use Co-Packer'

    return {
        'internal_cost': internal_total,
        'copacker_cost': copacker_total,
        'savings_with_copacker': savings,
        'savings_pct': savings_pct,
        'breakeven_volume': max(0, breakeven),
        'recommendation': recommendation,
        'cost_per_unit_internal': internal_total / annual_volume,
        'cost_per_unit_copacker': copacker_total / annual_volume
    }


# Example
analysis = make_vs_buy_analysis(
    internal_costs={
        'fixed_costs_annual': 500000,  # Plant overhead, equipment, staff
        'variable_cost_per_unit': 3.50  # Materials, labor, utilities
    },
    copacker_costs={
        'cost_per_unit': 4.25,
        'annual_fees': 50000  # Setup, tooling, etc.
    },
    annual_volume=100000
)

print(f"Internal Cost: ${analysis['internal_cost']:,.0f}")
print(f"Co-Packer Cost: ${analysis['copacker_cost']:,.0f}")
print(f"Savings: ${analysis['savings_with_copacker']:,.0f} ({analysis['savings_pct']:.1f}%)")
print(f"Recommendation: {analysis['recommendation']}")
print(f"Break-even Volume: {analysis['breakeven_volume']:,.0f} units")
```

### Multi-Sourcing Optimization

```python
from pulp import *

def optimize_copacker_allocation(demand, copackers, constraints):
    """
    Optimize allocation of production across multiple co-packers

    Parameters:
    - demand: total demand to fulfill
    - copackers: list of co-packers with costs and capacities
    - constraints: business rules

    Returns:
    - optimal allocation
    """

    # Create problem
    prob = LpProblem("CoPacker_Allocation", LpMinimize)

    # Decision variables: volume allocated to each co-packer
    allocation = LpVariable.dicts(
        "Allocation",
        [cp['name'] for cp in copackers],
        lowBound=0,
        cat='Continuous'
    )

    # Binary variables: is co-packer used?
    used = LpVariable.dicts(
        "Used",
        [cp['name'] for cp in copackers],
        cat='Binary'
    )

    # Objective: minimize total cost
    total_cost = 0

    for cp in copackers:
        name = cp['name']
        # Variable cost
        total_cost += allocation[name] * cp['cost_per_unit']
        # Fixed cost (if used)
        total_cost += used[name] * cp['fixed_cost']

    prob += total_cost

    # Constraints

    # 1. Meet demand
    prob += lpSum([allocation[cp['name']] for cp in copackers]) >= demand

    # 2. Capacity constraints
    for cp in copackers:
        name = cp['name']
        prob += allocation[name] <= cp['capacity']

    # 3. MOQ constraints
    for cp in copackers:
        name = cp['name']
        moq = cp.get('moq', 0)
        # If used, must meet MOQ
        prob += allocation[name] >= moq * used[name]
        # If not used, allocation = 0
        prob += allocation[name] <= cp['capacity'] * used[name]

    # 4. Single sourcing preference (optional)
    if constraints.get('prefer_single_source', False):
        prob += lpSum([used[cp['name']] for cp in copackers]) <= 2

    # 5. Minimum allocation for preferred suppliers
    preferred = constraints.get('preferred_suppliers', [])
    for pref in preferred:
        min_pct = pref.get('min_allocation_pct', 0)
        prob += allocation[pref['name']] >= demand * min_pct

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract results
    results = {
        'status': LpStatus[prob.status],
        'total_cost': value(prob.objective),
        'allocations': []
    }

    for cp in copackers:
        name = cp['name']
        if allocation[name].varValue > 0:
            results['allocations'].append({
                'copacker': name,
                'volume': allocation[name].varValue,
                'pct_of_demand': allocation[name].varValue / demand * 100,
                'cost': allocation[name].varValue * cp['cost_per_unit'] +
                        used[name].varValue * cp['fixed_cost']
            })

    return results


# Example
copackers = [
    {
        'name': 'CoPacker_A',
        'capacity': 50000,
        'cost_per_unit': 4.20,
        'fixed_cost': 10000,
        'moq': 5000
    },
    {
        'name': 'CoPacker_B',
        'capacity': 75000,
        'cost_per_unit': 4.00,
        'fixed_cost': 15000,
        'moq': 10000
    },
    {
        'name': 'CoPacker_C',
        'capacity': 40000,
        'cost_per_unit': 4.50,
        'fixed_cost': 5000,
        'moq': 2000
    }
]

result = optimize_copacker_allocation(
    demand=60000,
    copackers=copackers,
    constraints={'prefer_single_source': False}
)

print(f"Total Cost: ${result['total_cost']:,.0f}")
for alloc in result['allocations']:
    print(f"{alloc['copacker']}: {alloc['volume']:,.0f} units ({alloc['pct_of_demand']:.1f}%)")
```

---

## Performance Management

### Co-Packer Scorecard

```python
class CoPackerScorecard:
    """
    Comprehensive co-packer performance tracking
    """

    def __init__(self, copacker_name, sla_targets):
        self.copacker = copacker_name
        self.sla = sla_targets
        self.performance_data = []

    def record_performance(self, period_data):
        """Record performance for a period"""
        self.performance_data.append(period_data)

    def calculate_scorecard(self):
        """Calculate overall performance scorecard"""

        if not self.performance_data:
            return None

        df = pd.DataFrame(self.performance_data)

        scorecard = {}

        # Quality metrics
        scorecard['quality_score'] = self._score_quality(df)

        # Delivery metrics
        scorecard['delivery_score'] = self._score_delivery(df)

        # Cost metrics
        scorecard['cost_score'] = self._score_cost(df)

        # Service metrics
        scorecard['service_score'] = self._score_service(df)

        # Overall score (weighted average)
        weights = {
            'quality_score': 0.35,
            'delivery_score': 0.25,
            'cost_score': 0.25,
            'service_score': 0.15
        }

        scorecard['overall_score'] = sum(
            scorecard[metric] * weight
            for metric, weight in weights.items()
        )

        scorecard['grade'] = self._assign_grade(scorecard['overall_score'])

        return scorecard

    def _score_quality(self, df):
        """Score quality performance (0-100)"""
        avg_defect_rate = df['defect_rate'].mean()
        target_defect_rate = self.sla.get('max_defect_rate', 0.005)

        if avg_defect_rate <= target_defect_rate:
            return 100
        elif avg_defect_rate <= target_defect_rate * 2:
            return 80
        elif avg_defect_rate <= target_defect_rate * 3:
            return 60
        else:
            return 40

    def _score_delivery(self, df):
        """Score delivery performance (0-100)"""
        on_time_pct = df['on_time'].mean()
        target = self.sla.get('on_time_delivery', 0.95)

        if on_time_pct >= target:
            return 100
        elif on_time_pct >= target - 0.05:
            return 80
        elif on_time_pct >= target - 0.10:
            return 60
        else:
            return 40

    def _score_cost(self, df):
        """Score cost competitiveness (0-100)"""
        avg_cost = df['cost_per_unit'].mean()
        target_cost = self.sla.get('target_cost', avg_cost)

        variance = (avg_cost - target_cost) / target_cost

        if variance <= 0:  # Under target
            return 100
        elif variance <= 0.05:
            return 90
        elif variance <= 0.10:
            return 70
        else:
            return 50

    def _score_service(self, df):
        """Score service and responsiveness (0-100)"""
        # Composite of various service metrics
        service_score = (
            df.get('responsiveness', 80).mean() * 0.4 +
            df.get('flexibility', 80).mean() * 0.3 +
            df.get('communication', 80).mean() * 0.3
        )

        return min(100, service_score)

    def _assign_grade(self, score):
        """Assign letter grade"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
```

---

## Tools & Technologies

### Co-Packer Management Software

**Vendor Management:**
- **SAP Ariba**: Supplier management and collaboration
- **Coupa**: Supplier management and procurement
- **Jaggaer**: Supplier relationship management
- **Ivalua**: Procurement and supplier management

**Quality Management:**
- **TraceGains**: Supplier compliance and quality
- **MasterControl**: Quality management system
- **Sparta Systems**: Quality and compliance (TrackWise)
- **ETQ Reliance**: Quality management

**Contract Manufacturing Platforms:**
- **SQFI**: Safe Quality Food Institute certification
- **Selerant**: Recipe and formulation management
- **Blue Yonder**: Manufacturing planning and collaboration
- **E2open**: Supply chain collaboration platform

### Python Libraries

```python
# Contract and supplier management
import pandas as pd
import numpy as np

# Optimization
from pulp import *
import scipy.optimize as opt

# Data visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# Financial analysis
from scipy import stats
import statsmodels.api as sm
```

---

## Common Challenges & Solutions

### Challenge: Quality Inconsistency

**Problem:**
- Batch-to-batch variation
- Higher defect rates than internal
- Quality disputes

**Solutions:**
- Detailed specifications and approved samples
- First article inspection for new runs
- In-process quality checks
- Statistical process control (SPC)
- Regular audits and process reviews
- Invest in co-packer training

### Challenge: Long Lead Times

**Problem:**
- 8-12 week lead times
- Slow response to demand changes
- Inventory challenges

**Solutions:**
- Commit to longer-term forecasts
- Build safety stock
- Negotiate priority/expedite options
- Multi-source for flexibility
- Consider vendor-managed inventory (VMI)

### Challenge: High MOQs

**Problem:**
- MOQs larger than needed
- Excess inventory
- Cash flow impact

**Solutions:**
- Negotiate lower MOQs (pay premium)
- Combine SKUs in single run
- Find smaller/flexible co-packers
- Use tolling (bring your materials)
- Build to stock during off-peak

### Challenge: IP Protection

**Problem:**
- Risk of formula theft
- Proprietary process exposure
- Competing products

**Solutions:**
- Strong NDAs and contracts
- Separate ingredients/pre-mix
- Split production (multi co-packers)
- Regular audits
- Exclusive agreements
- Patent protection

### Challenge: Cost Creep

**Problem:**
- Prices increase over time
- Hidden fees and surcharges
- Less competitive

**Solutions:**
- Lock in multi-year pricing
- Index to commodities (transparent)
- Benchmark against alternatives
- RFQ every 2-3 years
- Volume commitments for discounts
- Monitor total landed cost

---

## Output Format

### Co-Packer Evaluation Report

**Executive Summary:**
- Co-Packer: ABC Co-Packing Inc.
- Location: Memphis, TN
- Products: Snack bars, granola
- Evaluation Date: January 2025
- Overall Score: 85/100 (Grade: B)
- Recommendation: Approved for partnership

**Scoring Detail:**

| Category | Score | Weight | Weighted | Target | Status |
|----------|-------|--------|----------|--------|--------|
| Quality | 90 | 35% | 31.5 | >85 | ✓ |
| Delivery | 85 | 25% | 21.25 | >90 | ⚠ |
| Cost | 80 | 25% | 20.0 | >80 | ✓ |
| Service | 82 | 15% | 12.3 | >80 | ✓ |
| **Total** | **85** | **100%** | **85** | **>80** | **✓** |

**Strengths:**
- Excellent quality track record (0.3% defect rate)
- SQF Level 3 certified
- Modern equipment and technology
- Competitive pricing
- Strong technical expertise

**Weaknesses:**
- Delivery performance below target (85% vs. 90%)
- Limited surge capacity
- Higher MOQs than desired

**Recommendations:**
1. Negotiate improved lead times and on-time delivery
2. Request MOQ reduction for initial SKUs
3. Establish expedite process for urgent orders
4. Proceed with pilot production (10,000 units)

---

## Questions to Ask

If you need more context:
1. What products do you want to co-pack? What volume?
2. Why co-packing vs. internal production?
3. Do you have existing co-packer relationships?
4. What are your quality requirements and certifications needed?
5. What lead times and MOQs can you accept?
6. What's your budget and target cost per unit?
7. Any geographic preferences?
8. IP protection concerns?

---

## Related Skills

- **capacity-planning**: For production capacity analysis
- **supplier-selection**: For vendor evaluation frameworks
- **supplier-risk-management**: For co-packer risk assessment
- **quality-management**: For quality systems and SPC
- **procurement-optimization**: For contract negotiation
- **inventory-optimization**: For co-packer inventory planning
- **master-production-scheduling**: For production scheduling
- **network-design**: For co-packer network strategy
- **compliance-management**: For regulatory compliance
