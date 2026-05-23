---
name: strategic-sourcing
description: When the user wants to develop category strategies, execute sourcing events, or implement strategic procurement initiatives. Also use when the user mentions "category management," "sourcing strategy," "value levers," "should-cost analysis," "RFx management," "e-sourcing," "strategic procurement," or "category sourcing." For supplier evaluation, see supplier-selection. For spend analysis, see spend-analysis.
---

# Strategic Sourcing

You are an expert in strategic sourcing and category management. Your goal is to help organizations develop and execute comprehensive category strategies that deliver sustainable value through supplier relationships, market insights, and analytical rigor.

## Initial Assessment

Before developing a sourcing strategy, understand:

1. **Category Context**
   - What category or commodity? (direct, indirect, services)
   - Annual spend volume?
   - Strategic importance? (critical, leverage, bottleneck, non-critical)
   - Current sourcing approach?

2. **Business Requirements**
   - Business objectives? (cost, innovation, risk, sustainability)
   - Stakeholder needs?
   - Technical specifications?
   - Volume projections?

3. **Market Dynamics**
   - Supply market characteristics?
   - Number of suppliers?
   - Competitive landscape?
   - Technology trends?
   - Price trends?

4. **Current State**
   - Incumbent suppliers?
   - Contract terms?
   - Known issues or opportunities?
   - Historical spend patterns?

---

## Strategic Sourcing Framework

### 7-Step Sourcing Process

**1. Profile the Category**
- Understand internal requirements
- Map current spend
- Identify stakeholders
- Define specifications

**2. Assess the Supply Market**
- Supplier landscape analysis
- Market trends and dynamics
- Technology innovations
- Risk factors

**3. Develop Sourcing Strategy**
- Kraljic positioning
- Value levers identification
- Supplier strategy (single/multi)
- Negotiation approach

**4. Generate Supplier Options**
- Incumbent evaluation
- New supplier identification
- Qualification criteria
- Long list creation

**5. Select Suppliers**
- RFx process execution
- Proposal evaluation
- Negotiation
- Final selection

**6. Negotiate & Contract**
- Terms finalization
- Legal review
- Contract execution
- Stakeholder alignment

**7. Integrate & Improve**
- Implementation planning
- Supplier onboarding
- Performance management
- Continuous improvement

---

## Category Management

### Kraljic Portfolio Analysis

**Classify categories based on:**
- **Supply Risk**: Availability, supplier concentration, substitution
- **Profit Impact**: Spend volume, impact on cost/quality

**Four Quadrants:**

```
High Supply Risk
       │
   2   │   1
Leverage│Strategic
       │
───────┼───────  High Profit Impact
       │
   3   │   4
Non-   │Bottleneck
Critical│
       │
Low Supply Risk
```

**1. Strategic (High Risk, High Impact)**
- Examples: Critical components, specialized services
- Strategy: Long-term partnerships, joint development, risk mitigation
- Approach: Relationship management, innovation focus

**2. Leverage (Low Risk, High Impact)**
- Examples: Standard materials with multiple suppliers
- Strategy: Competitive bidding, volume consolidation, aggressive negotiation
- Approach: Maximize buying power

**3. Non-Critical (Low Risk, Low Impact)**
- Examples: Office supplies, basic MRO
- Strategy: Simplify process, automate, consolidate
- Approach: Efficient transactions, e-catalogs

**4. Bottleneck (High Risk, Low Impact)**
- Examples: Specialty items, niche services
- Strategy: Ensure supply, reduce complexity, standardize
- Approach: Secure availability, long-term contracts

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class KraljicAnalysis:
    """Kraljic portfolio positioning for categories"""

    def __init__(self, categories_df):
        """
        categories_df: DataFrame with category, spend, supply_risk, profit_impact
        """
        self.categories = categories_df

    def classify_category(self, supply_risk, profit_impact):
        """Classify category into Kraljic quadrant"""

        if supply_risk >= 50 and profit_impact >= 50:
            return 'Strategic'
        elif supply_risk < 50 and profit_impact >= 50:
            return 'Leverage'
        elif supply_risk < 50 and profit_impact < 50:
            return 'Non-Critical'
        else:  # supply_risk >= 50 and profit_impact < 50
            return 'Bottleneck'

    def add_classifications(self):
        """Add Kraljic classification to categories"""

        self.categories['kraljic_quadrant'] = self.categories.apply(
            lambda row: self.classify_category(
                row['supply_risk'],
                row['profit_impact']
            ),
            axis=1
        )

        return self.categories

    def plot_portfolio(self):
        """Create Kraljic portfolio matrix visualization"""

        fig, ax = plt.subplots(figsize=(12, 8))

        # Color by quadrant
        colors = {
            'Strategic': 'red',
            'Leverage': 'green',
            'Bottleneck': 'orange',
            'Non-Critical': 'blue'
        }

        for quadrant in colors:
            data = self.categories[self.categories['kraljic_quadrant'] == quadrant]

            ax.scatter(
                data['profit_impact'],
                data['supply_risk'],
                s=data['spend'] / 10000,  # Bubble size by spend
                c=colors[quadrant],
                alpha=0.6,
                label=quadrant
            )

            # Add category labels
            for _, row in data.iterrows():
                ax.annotate(
                    row['category'],
                    (row['profit_impact'], row['supply_risk']),
                    fontsize=8,
                    ha='center'
                )

        # Quadrant lines
        ax.axvline(50, color='gray', linestyle='--', alpha=0.5)
        ax.axhline(50, color='gray', linestyle='--', alpha=0.5)

        # Labels
        ax.set_xlabel('Profit Impact (Spend, Cost Criticality)', fontsize=12)
        ax.set_ylabel('Supply Risk (Availability, Complexity)', fontsize=12)
        ax.set_title('Kraljic Portfolio Matrix', fontsize=14, weight='bold')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Quadrant labels
        ax.text(75, 75, 'Strategic', ha='center', fontsize=11, weight='bold')
        ax.text(25, 75, 'Bottleneck', ha='center', fontsize=11, weight='bold')
        ax.text(75, 25, 'Leverage', ha='center', fontsize=11, weight='bold')
        ax.text(25, 25, 'Non-Critical', ha='center', fontsize=11, weight='bold')

        plt.tight_layout()
        return fig


# Example usage
categories = pd.DataFrame({
    'category': ['IT Hardware', 'Office Supplies', 'Specialized Components',
                'Raw Materials', 'Consulting', 'MRO'],
    'spend': [2000000, 500000, 800000, 5000000, 1500000, 300000],
    'supply_risk': [30, 20, 80, 40, 60, 75],  # 0-100
    'profit_impact': [70, 40, 35, 90, 80, 25]  # 0-100
})

kraljic = KraljicAnalysis(categories)
classified = kraljic.add_classifications()

print("\nKraljic Classification:")
print(classified[['category', 'kraljic_quadrant', 'spend']])

# fig = kraljic.plot_portfolio()
# plt.show()
```

---

## Strategic Sourcing Value Levers

### Value Lever Framework

**1. Price/Rate Reduction**
- Competitive bidding
- Market pricing benchmarks
- Volume aggregation
- Global sourcing
- E-auctions

**2. Demand Management**
- Specification optimization
- Standardization
- Usage reduction
- Substitution
- Make vs. buy analysis

**3. Process Efficiency**
- Process automation (P2P)
- Supplier consolidation
- Transactional efficiency
- Self-service tools
- Payment optimization

**4. Total Cost Management**
- Total Cost of Ownership (TCO)
- Logistics optimization
- Quality improvement
- Working capital
- Lifecycle costs

**5. Supplier Value Creation**
- Innovation collaboration
- Continuous improvement
- Supplier development
- Value engineering
- Gain-sharing

```python
class ValueLevers:
    """Identify and quantify value levers for category"""

    def __init__(self, category, baseline_spend):
        self.category = category
        self.baseline_spend = baseline_spend
        self.levers = []

    def add_price_reduction(self, current_price, target_price, volume,
                           confidence=0.8, timeline_months=6):
        """Add price reduction lever"""

        savings_per_unit = current_price - target_price
        annual_savings = savings_per_unit * volume
        risk_adjusted = annual_savings * confidence

        self.levers.append({
            'lever_type': 'Price Reduction',
            'description': f'Negotiate price from ${current_price} to ${target_price}',
            'gross_savings': annual_savings,
            'confidence_%': confidence * 100,
            'risk_adjusted_savings': risk_adjusted,
            'implementation_timeline': timeline_months,
            'implementation_effort': 'Medium'
        })

    def add_demand_reduction(self, reduction_pct, rationale,
                            confidence=0.6, timeline_months=12):
        """Add demand management lever"""

        annual_savings = self.baseline_spend * reduction_pct
        risk_adjusted = annual_savings * confidence

        self.levers.append({
            'lever_type': 'Demand Management',
            'description': rationale,
            'gross_savings': annual_savings,
            'confidence_%': confidence * 100,
            'risk_adjusted_savings': risk_adjusted,
            'implementation_timeline': timeline_months,
            'implementation_effort': 'High'
        })

    def add_specification_change(self, savings_amount, description,
                                confidence=0.7, timeline_months=9):
        """Add specification optimization lever"""

        risk_adjusted = savings_amount * confidence

        self.levers.append({
            'lever_type': 'Specification Change',
            'description': description,
            'gross_savings': savings_amount,
            'confidence_%': confidence * 100,
            'risk_adjusted_savings': risk_adjusted,
            'implementation_timeline': timeline_months,
            'implementation_effort': 'High'
        })

    def add_process_improvement(self, savings_amount, description,
                               confidence=0.9, timeline_months=3):
        """Add process efficiency lever"""

        risk_adjusted = savings_amount * confidence

        self.levers.append({
            'lever_type': 'Process Improvement',
            'description': description,
            'gross_savings': savings_amount,
            'confidence_%': confidence * 100,
            'risk_adjusted_savings': risk_adjusted,
            'implementation_timeline': timeline_months,
            'implementation_effort': 'Medium'
        })

    def add_supplier_consolidation(self, expected_discount, description,
                                  confidence=0.75, timeline_months=6):
        """Add supplier consolidation lever"""

        annual_savings = self.baseline_spend * expected_discount
        risk_adjusted = annual_savings * confidence

        self.levers.append({
            'lever_type': 'Supplier Consolidation',
            'description': description,
            'gross_savings': annual_savings,
            'confidence_%': confidence * 100,
            'risk_adjusted_savings': risk_adjusted,
            'implementation_timeline': timeline_months,
            'implementation_effort': 'High'
        })

    def get_value_lever_summary(self):
        """Get prioritized value lever summary"""

        if not self.levers:
            return None

        df = pd.DataFrame(self.levers)
        df = df.sort_values('risk_adjusted_savings', ascending=False)

        # Add cumulative savings
        df['cumulative_savings'] = df['risk_adjusted_savings'].cumsum()

        total_gross = df['gross_savings'].sum()
        total_risk_adjusted = df['risk_adjusted_savings'].sum()

        return {
            'category': self.category,
            'baseline_spend': self.baseline_spend,
            'total_gross_savings': total_gross,
            'total_risk_adjusted_savings': total_risk_adjusted,
            'savings_pct': (total_risk_adjusted / self.baseline_spend * 100),
            'num_levers': len(df),
            'levers': df
        }


# Example: IT Hardware category
it_hardware = ValueLevers(category='IT Hardware', baseline_spend=2000000)

it_hardware.add_price_reduction(
    current_price=1200,
    target_price=1100,
    volume=1500,
    confidence=0.85,
    timeline_months=3
)

it_hardware.add_supplier_consolidation(
    expected_discount=0.05,
    description='Consolidate from 8 suppliers to 3',
    confidence=0.75,
    timeline_months=6
)

it_hardware.add_specification_change(
    savings_amount=80000,
    description='Standardize to fewer SKUs',
    confidence=0.70,
    timeline_months=9
)

it_hardware.add_process_improvement(
    savings_amount=40000,
    description='Implement e-procurement for efficiency',
    confidence=0.90,
    timeline_months=3
)

summary = it_hardware.get_value_lever_summary()

print(f"\nCategory: {summary['category']}")
print(f"Baseline Spend: ${summary['baseline_spend']:,.0f}")
print(f"Total Savings: ${summary['total_risk_adjusted_savings']:,.0f} ({summary['savings_pct']:.1f}%)")
print(f"\nValue Levers:")
print(summary['levers'][['lever_type', 'description', 'risk_adjusted_savings', 'implementation_timeline']])
```

---

## Should-Cost Analysis

### Cost Breakdown Modeling

**Understand Supplier's Cost Structure:**
- Raw materials
- Direct labor
- Manufacturing overhead
- SG&A (Selling, General, Administrative)
- Profit margin

```python
class ShouldCostModel:
    """Build should-cost model for products/services"""

    def __init__(self, product_name):
        self.product_name = product_name
        self.cost_components = {}

    def add_material_cost(self, material, quantity, unit_cost):
        """Add material cost component"""

        total_cost = quantity * unit_cost

        if 'materials' not in self.cost_components:
            self.cost_components['materials'] = []

        self.cost_components['materials'].append({
            'material': material,
            'quantity': quantity,
            'unit_cost': unit_cost,
            'total_cost': total_cost
        })

    def add_labor_cost(self, operation, hours, hourly_rate):
        """Add labor cost component"""

        total_cost = hours * hourly_rate

        if 'labor' not in self.cost_components:
            self.cost_components['labor'] = []

        self.cost_components['labor'].append({
            'operation': operation,
            'hours': hours,
            'hourly_rate': hourly_rate,
            'total_cost': total_cost
        })

    def add_overhead(self, overhead_rate):
        """Add overhead as % of labor"""

        if 'labor' not in self.cost_components:
            return

        labor_cost = sum(item['total_cost']
                        for item in self.cost_components['labor'])

        self.cost_components['overhead'] = labor_cost * overhead_rate

    def add_profit_margin(self, margin_rate):
        """Add profit margin"""

        self.margin_rate = margin_rate

    def calculate_should_cost(self):
        """Calculate total should-cost"""

        # Materials
        material_cost = sum(
            item['total_cost']
            for item in self.cost_components.get('materials', [])
        )

        # Labor
        labor_cost = sum(
            item['total_cost']
            for item in self.cost_components.get('labor', [])
        )

        # Overhead
        overhead_cost = self.cost_components.get('overhead', 0)

        # Manufacturing cost
        manufacturing_cost = material_cost + labor_cost + overhead_cost

        # SG&A (typically 10-15% of manufacturing)
        sga_cost = manufacturing_cost * 0.12

        # Total cost before profit
        total_cost = manufacturing_cost + sga_cost

        # Add profit margin
        margin_rate = getattr(self, 'margin_rate', 0.15)
        profit = total_cost * margin_rate

        # Should-cost price
        should_cost_price = total_cost + profit

        return {
            'product': self.product_name,
            'cost_breakdown': {
                'materials': round(material_cost, 2),
                'labor': round(labor_cost, 2),
                'overhead': round(overhead_cost, 2),
                'sga': round(sga_cost, 2),
                'subtotal': round(total_cost, 2),
                'profit_margin': round(profit, 2)
            },
            'should_cost_price': round(should_cost_price, 2),
            'cost_percentages': {
                'materials_%': round(material_cost / should_cost_price * 100, 1),
                'labor_%': round(labor_cost / should_cost_price * 100, 1),
                'overhead_%': round(overhead_cost / should_cost_price * 100, 1),
                'sga_%': round(sga_cost / should_cost_price * 100, 1),
                'profit_%': round(profit / should_cost_price * 100, 1)
            }
        }

    def compare_to_quoted_price(self, quoted_price):
        """Compare should-cost to quoted price"""

        should_cost = self.calculate_should_cost()
        should_cost_price = should_cost['should_cost_price']

        variance = quoted_price - should_cost_price
        variance_pct = (variance / should_cost_price) * 100

        return {
            **should_cost,
            'quoted_price': quoted_price,
            'variance': round(variance, 2),
            'variance_%': round(variance_pct, 1),
            'assessment': 'Over-priced' if variance > 0 else 'Fair' if abs(variance_pct) < 5 else 'Under-priced'
        }


# Example: Metal bracket manufacturing
bracket = ShouldCostModel('Metal Bracket Assembly')

# Materials
bracket.add_material_cost('Steel sheet', quantity=0.5, unit_cost=2.00)  # kg
bracket.add_material_cost('Bolts', quantity=4, unit_cost=0.15)
bracket.add_material_cost('Paint', quantity=0.1, unit_cost=5.00)  # liters

# Labor
bracket.add_labor_cost('Cutting', hours=0.2, hourly_rate=25.00)
bracket.add_labor_cost('Forming', hours=0.3, hourly_rate=28.00)
bracket.add_labor_cost('Assembly', hours=0.25, hourly_rate=22.00)

# Overhead (150% of labor)
bracket.add_overhead(overhead_rate=1.5)

# Profit margin (15%)
bracket.add_profit_margin(margin_rate=0.15)

# Calculate should-cost and compare to quote
result = bracket.compare_to_quoted_price(quoted_price=45.00)

print(f"\nShould-Cost Analysis: {result['product']}")
print(f"\nCost Breakdown:")
for component, cost in result['cost_breakdown'].items():
    print(f"  {component.capitalize()}: ${cost}")

print(f"\nShould-Cost Price: ${result['should_cost_price']}")
print(f"Quoted Price: ${result['quoted_price']}")
print(f"Variance: ${result['variance']} ({result['variance_%']}%)")
print(f"Assessment: {result['assessment']}")
```

---

## RFx Management & E-Sourcing

### E-Sourcing Event Types

**1. RFI (Request for Information)**
- Purpose: Market intelligence, supplier capabilities
- Use when: Exploring market, new category
- Outcome: Supplier shortlist

**2. RFP (Request for Proposal)**
- Purpose: Comprehensive evaluation (price, quality, service)
- Use when: Complex requirements, multiple factors
- Outcome: Detailed proposals, supplier selection

**3. RFQ (Request for Quotation)**
- Purpose: Price comparison for defined specifications
- Use when: Standard products, price-focused
- Outcome: Price quotes, cost comparison

**4. E-Auction (Reverse Auction)**
- Purpose: Dynamic price competition
- Use when: Standardized goods, multiple qualified suppliers
- Outcome: Lowest price commitment

```python
class EAuctionSimulator:
    """Simulate e-auction bidding dynamics"""

    def __init__(self, starting_price, reserve_price, num_suppliers):
        self.starting_price = starting_price
        self.reserve_price = reserve_price
        self.num_suppliers = num_suppliers
        self.current_price = starting_price
        self.bids = []
        self.round = 0

    def simulate_round(self):
        """Simulate one bidding round"""

        self.round += 1

        # Each supplier decides whether to bid
        for supplier_id in range(self.num_suppliers):

            # Probability of bidding decreases as price approaches reserve
            price_gap = self.current_price - self.reserve_price
            bid_probability = min(0.9, price_gap / self.starting_price)

            if np.random.random() < bid_probability:
                # Bid reduction (0.5% to 2% of current price)
                reduction_pct = np.random.uniform(0.005, 0.02)
                new_bid = self.current_price * (1 - reduction_pct)
                new_bid = max(new_bid, self.reserve_price)

                self.bids.append({
                    'round': self.round,
                    'supplier': f'Supplier_{supplier_id+1}',
                    'bid': round(new_bid, 2)
                })

                # Update current price to lowest bid
                if new_bid < self.current_price:
                    self.current_price = new_bid

    def run_auction(self, max_rounds=10):
        """Run complete auction"""

        for _ in range(max_rounds):
            self.simulate_round()

            # Stop if no bids in last two rounds
            recent_bids = [b for b in self.bids if b['round'] >= self.round - 1]
            if len(recent_bids) == 0:
                break

        return {
            'starting_price': self.starting_price,
            'final_price': self.current_price,
            'savings': self.starting_price - self.current_price,
            'savings_%': ((self.starting_price - self.current_price) /
                         self.starting_price * 100),
            'total_rounds': self.round,
            'total_bids': len(self.bids),
            'bid_history': pd.DataFrame(self.bids)
        }


# Example: E-auction for IT hardware
auction = EAuctionSimulator(
    starting_price=1200,
    reserve_price=1050,
    num_suppliers=5
)

results = auction.run_auction(max_rounds=15)

print(f"\nE-Auction Results:")
print(f"Starting Price: ${results['starting_price']}")
print(f"Final Price: ${results['final_price']}")
print(f"Savings: ${results['savings']} ({results['savings_%']:.1f}%)")
print(f"Total Rounds: {results['total_rounds']}")
print(f"Total Bids: {results['total_bids']}")

# print("\nBid History:")
# print(results['bid_history'].tail(10))
```

---

## Category Strategy Development

### Strategy Template

```python
class CategoryStrategy:
    """Comprehensive category strategy framework"""

    def __init__(self, category_name, annual_spend):
        self.category = category_name
        self.annual_spend = annual_spend
        self.strategy_elements = {}

    def set_positioning(self, kraljic_quadrant, rationale):
        """Set Kraljic positioning"""
        self.strategy_elements['positioning'] = {
            'quadrant': kraljic_quadrant,
            'rationale': rationale
        }

    def set_objectives(self, primary, secondary=None):
        """Set strategic objectives"""
        self.strategy_elements['objectives'] = {
            'primary': primary,
            'secondary': secondary or []
        }

    def set_sourcing_strategy(self, approach, num_suppliers, contract_term):
        """
        Define sourcing strategy

        approach: 'Single source', 'Dual source', 'Multiple suppliers'
        """
        self.strategy_elements['sourcing'] = {
            'approach': approach,
            'target_suppliers': num_suppliers,
            'contract_term_years': contract_term
        }

    def set_value_levers(self, levers):
        """
        Set prioritized value levers

        levers: list of dicts with lever details
        """
        self.strategy_elements['value_levers'] = levers

    def set_implementation_plan(self, milestones):
        """
        Set implementation milestones

        milestones: list of dicts with milestone, timeline, owner
        """
        self.strategy_elements['implementation'] = milestones

    def set_risks_mitigation(self, risks):
        """
        Set risks and mitigation plans

        risks: list of dicts with risk, impact, mitigation
        """
        self.strategy_elements['risks'] = risks

    def generate_strategy_document(self):
        """Generate comprehensive strategy document"""

        doc = []
        doc.append("=" * 80)
        doc.append(f"CATEGORY STRATEGY: {self.category.upper()}")
        doc.append("=" * 80)
        doc.append(f"Annual Spend: ${self.annual_spend:,.0f}")
        doc.append("")

        # Positioning
        if 'positioning' in self.strategy_elements:
            pos = self.strategy_elements['positioning']
            doc.append("STRATEGIC POSITIONING")
            doc.append("-" * 80)
            doc.append(f"Kraljic Quadrant: {pos['quadrant']}")
            doc.append(f"Rationale: {pos['rationale']}")
            doc.append("")

        # Objectives
        if 'objectives' in self.strategy_elements:
            obj = self.strategy_elements['objectives']
            doc.append("STRATEGIC OBJECTIVES")
            doc.append("-" * 80)
            doc.append(f"Primary: {obj['primary']}")
            if obj['secondary']:
                doc.append("Secondary:")
                for sec in obj['secondary']:
                    doc.append(f"  - {sec}")
            doc.append("")

        # Sourcing Strategy
        if 'sourcing' in self.strategy_elements:
            src = self.strategy_elements['sourcing']
            doc.append("SOURCING STRATEGY")
            doc.append("-" * 80)
            doc.append(f"Approach: {src['approach']}")
            doc.append(f"Target Number of Suppliers: {src['target_suppliers']}")
            doc.append(f"Contract Term: {src['contract_term_years']} years")
            doc.append("")

        # Value Levers
        if 'value_levers' in self.strategy_elements:
            doc.append("VALUE LEVERS & SAVINGS TARGETS")
            doc.append("-" * 80)
            total_savings = 0
            for i, lever in enumerate(self.strategy_elements['value_levers'], 1):
                doc.append(f"\n{i}. {lever['lever']}")
                doc.append(f"   Target Savings: ${lever['savings']:,.0f}")
                doc.append(f"   Timeline: {lever['timeline']}")
                total_savings += lever['savings']
            doc.append(f"\nTotal Target Savings: ${total_savings:,.0f} ({total_savings/self.annual_spend*100:.1f}%)")
            doc.append("")

        # Implementation Plan
        if 'implementation' in self.strategy_elements:
            doc.append("IMPLEMENTATION PLAN")
            doc.append("-" * 80)
            for milestone in self.strategy_elements['implementation']:
                doc.append(f"\n{milestone['milestone']}")
                doc.append(f"  Timeline: {milestone['timeline']}")
                doc.append(f"  Owner: {milestone['owner']}")
            doc.append("")

        # Risks
        if 'risks' in self.strategy_elements:
            doc.append("RISKS & MITIGATION")
            doc.append("-" * 80)
            for risk in self.strategy_elements['risks']:
                doc.append(f"\nRisk: {risk['risk']}")
                doc.append(f"  Impact: {risk['impact']}")
                doc.append(f"  Mitigation: {risk['mitigation']}")
            doc.append("")

        return "\n".join(doc)


# Example: IT Hardware category strategy
strategy = CategoryStrategy(category='IT Hardware', annual_spend=2000000)

strategy.set_positioning(
    kraljic_quadrant='Leverage',
    rationale='Multiple qualified suppliers, high spend volume'
)

strategy.set_objectives(
    primary='Reduce costs by 8-10% while maintaining quality',
    secondary=[
        'Consolidate supplier base from 8 to 3',
        'Standardize specifications',
        'Improve payment terms'
    ]
)

strategy.set_sourcing_strategy(
    approach='Dual source',
    num_suppliers=2,
    contract_term=2
)

strategy.set_value_levers([
    {'lever': 'Competitive bidding via RFP',
     'savings': 150000, 'timeline': 'Q1 2026'},
    {'lever': 'Supplier consolidation',
     'savings': 80000, 'timeline': 'Q2 2026'},
    {'lever': 'Specification standardization',
     'savings': 60000, 'timeline': 'Q3 2026'},
    {'lever': 'Payment terms optimization',
     'savings': 20000, 'timeline': 'Q1 2026'}
])

strategy.set_implementation_plan([
    {'milestone': 'Complete RFP and supplier selection',
     'timeline': 'Q1 2026', 'owner': 'Category Manager'},
    {'milestone': 'Negotiate contracts with selected suppliers',
     'timeline': 'Q2 2026', 'owner': 'Procurement Director'},
    {'milestone': 'Implement standardized specs across business units',
     'timeline': 'Q3 2026', 'owner': 'IT Director'},
    {'milestone': 'Monitor savings realization',
     'timeline': 'Ongoing', 'owner': 'Category Manager'}
])

strategy.set_risks_mitigation([
    {'risk': 'Supplier capacity constraints during transition',
     'impact': 'Medium',
     'mitigation': 'Phased transition, maintain backup supplier'},
    {'risk': 'Stakeholder resistance to standardization',
     'impact': 'High',
     'mitigation': 'Executive sponsorship, value communication'},
    {'risk': 'Market price increases',
     'impact': 'Low',
     'mitigation': 'Fixed pricing in contracts, 2-year term'}
])

print(strategy.generate_strategy_document())
```

---

## Tools & Libraries

### Python Libraries

**Analysis:**
- `pandas`: Data analysis
- `numpy`: Numerical computation
- `scipy`: Statistical analysis
- `scikit-learn`: Machine learning for analytics

**Optimization:**
- `pulp`: Supplier allocation optimization
- `cvxpy`: Convex optimization

**Visualization:**
- `matplotlib`, `seaborn`: Charts and analysis
- `plotly`: Interactive dashboards

### Commercial Software

**Strategic Sourcing Platforms:**
- **SAP Ariba**: Sourcing and procurement
- **Coupa**: Source-to-pay platform
- **Jaggaer**: Strategic sourcing suite
- **GEP SMART**: Unified procurement
- **Ivalua**: Source-to-pay
- **Zycus**: Sourcing and procurement
- **Keelvar**: Sourcing optimization

**E-Sourcing Tools:**
- **Ariba Sourcing**: RFx and auctions
- **Coupa Sourcing**: Event management
- **Scout RFP**: RFP management
- **BidNet**: Public sector sourcing

**Category Intelligence:**
- **SpendHQ**: Spend and market intelligence
- **Beroe**: Procurement intelligence
- **Market Dojo**: Sourcing and supplier management

---

## Common Challenges & Solutions

### Challenge: Stakeholder Resistance

**Problem:**
- Business units prefer incumbent suppliers
- "My requirements are unique"
- Fear of supply disruption
- Relationship concerns

**Solutions:**
- Early stakeholder engagement
- Demonstrate value (savings, quality, service)
- Pilot programs with willing business units
- Executive sponsorship
- Address concerns proactively
- Transparent communication

### Challenge: Insufficient Category Knowledge

**Problem:**
- Lack of technical expertise
- Don't understand supply market
- Can't assess supplier capabilities
- Difficulty writing specifications

**Solutions:**
- Engage subject matter experts (SMEs)
- Site visits and supplier meetings
- Industry association research
- Consultant or advisory support
- RFI process for market intelligence
- Cross-functional category teams

### Challenge: Limited Supplier Options

**Problem:**
- Sole source or limited suppliers
- Geographic constraints
- Specialized requirements
- Supplier oligopoly

**Solutions:**
- Global sourcing expansion
- Specification changes to enable alternatives
- Supplier development programs
- Make vs. buy analysis
- Long-term partnerships with risk-sharing
- Advance purchases or inventory buffers

### Challenge: Complex Requirements

**Problem:**
- Multiple stakeholders with different needs
- Conflicting requirements
- Difficulty defining specifications
- Hard to compare proposals

**Solutions:**
- Requirements rationalization workshops
- Prioritize must-have vs. nice-to-have
- Standardize where possible
- Modular specifications
- Weighted scoring for evaluation
- Proof-of-concept or trials

### Challenge: Savings Measurement & Tracking

**Problem:**
- Baseline debates
- Attribution questions
- Price vs. volume changes
- One-time vs. recurring

**Solutions:**
- Define baseline clearly (before sourcing)
- Track price changes separately from volume
- Third-party validation
- Savings governance process
- Regular savings audits
- Transparent reporting

---

## Output Format

### Category Strategy Document

**Executive Summary:**
- Category overview and strategic importance
- Key findings from analysis
- Recommended strategy and savings target
- Implementation approach

**Category Profile:**

| Attribute | Details |
|-----------|---------|
| Category | IT Hardware (Laptops, Desktops, Monitors) |
| Annual Spend | $2.0M |
| % of Total Spend | 3.5% |
| Kraljic Quadrant | Leverage |
| Current Suppliers | 8 active suppliers |
| Top 3 Concentration | 65% |
| Business Units Served | All (5 locations) |

**Supply Market Analysis:**

- Market Dynamics: Competitive, multiple Tier 1 suppliers
- Supply Risk: Low (abundant supply, multiple qualified sources)
- Price Trends: Flat to declining (commodity pressure)
- Technology Trends: Shift to cloud/thin clients, longer refresh cycles
- Key Suppliers: Dell, HP, Lenovo, Apple (OEMs), CDW, Insight (resellers)

**Current State Assessment:**

Strengths:
- Established relationships with major OEMs
- Good quality and reliability
- Adequate delivery performance

Weaknesses:
- Fragmented supplier base (8 suppliers, inconsistent terms)
- No standardized specifications (200+ SKU variations)
- Pricing 8-12% above market benchmarks
- Inconsistent payment terms and discounts

Opportunities:
- Consolidate to 2-3 strategic suppliers
- Standardize configurations (reduce to 20-30 SKUs)
- Leverage volume for better pricing
- Extend payment terms to Net 45

Threats:
- Component shortages (chips, displays)
- Technology obsolescence risk
- Business unit resistance to standardization

**Strategic Recommendation:**

Sourcing Strategy: Dual Source (70/30 split)
- Primary supplier (70%): Dell or HP via preferred reseller
- Secondary supplier (30%): Lenovo or alternate for competition
- Contract Term: 2 years with 1-year extension option

Value Proposition:
- Total savings target: $180K annually (9% of spend)
- Improved service levels and standardization
- Risk mitigation through dual sourcing

**Implementation Roadmap:**

```
Phase 1 (Months 1-3): RFP & Selection
  - Finalize requirements with stakeholders
  - Issue RFP to qualified suppliers
  - Evaluate proposals and select winners
  - Negotiate contracts

Phase 2 (Months 4-6): Transition & Onboarding
  - Establish catalogs and ordering process
  - Train stakeholders on new procedures
  - Transition volumes to new suppliers
  - Phase out non-strategic suppliers

Phase 3 (Months 7-12): Optimization
  - Monitor performance and compliance
  - Quarterly business reviews with suppliers
  - Track savings realization
  - Continuous improvement initiatives
```

**Expected Outcomes:**

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| Total Annual Spend | $2.0M | $1.82M | -9% |
| Number of Suppliers | 8 | 2 | -75% |
| Standardized SKUs | 200+ | 25 | -88% |
| Average Unit Price | $1,200 | $1,100 | -8.3% |
| Payment Terms | Net 30 | Net 45 | +15 days |
| On-Time Delivery | 92% | 98% | +6 pts |

---

## Questions to Ask

If you need more context:
1. What category or categories need strategy development?
2. What's the annual spend volume?
3. What's the current sourcing approach and pain points?
4. Who are the key stakeholders and what are their priorities?
5. What's known about the supply market?
6. Are there incumbent suppliers? What's the performance?
7. What constraints exist? (technical, regulatory, geographic)
8. What's the primary objective? (cost, innovation, risk, sustainability)
9. What's the timeline for implementing a new strategy?
10. What resources are available for the sourcing initiative?

---

## Related Skills

- **supplier-selection**: For executing supplier selection process
- **spend-analysis**: For category spend analysis
- **procurement-optimization**: For order allocation and lot sizing
- **contract-management**: For negotiating and managing contracts
- **supplier-risk-management**: For supplier risk assessment
- **supply-chain-analytics**: For performance tracking and KPIs
