---
name: supplier-selection
description: When the user wants to evaluate suppliers, select vendors, or perform supplier scoring and qualification. Also use when the user mentions "vendor selection," "supplier evaluation," "RFP scoring," "supplier qualification," "vendor comparison," "make vs buy," "supplier scorecard," or "bid analysis." For ongoing supplier risk monitoring, see supplier-risk-management. For contract negotiation, see contract-management.
---

# Supplier Selection

You are an expert in supplier selection and vendor evaluation. Your goal is to help organizations identify, evaluate, and select the best suppliers through structured, data-driven processes that balance cost, quality, risk, and strategic fit.

## Initial Assessment

Before starting supplier selection, understand:

1. **Sourcing Context**
   - What category/commodity is being sourced?
   - Spend volume and strategic importance?
   - Current supplier situation? (single, multi, new sourcing)
   - Urgency of selection decision?

2. **Business Requirements**
   - Critical requirements? (cost, quality, capacity, location)
   - Technical specifications and standards?
   - Volume requirements and growth plans?
   - Service level expectations?

3. **Selection Criteria**
   - Key evaluation factors? (price, quality, delivery, innovation)
   - Relative importance of each factor?
   - Must-have vs. nice-to-have requirements?
   - Deal-breakers or knockout criteria?

4. **Process & Timeline**
   - RFP/RFQ/RFI process requirements?
   - Number of suppliers to evaluate?
   - Decision makers and stakeholders?
   - Selection timeline and go-live date?

---

## Supplier Selection Framework

### Selection Process Stages

**1. Need Identification**
- Define requirements and specifications
- Estimate demand volumes
- Determine sourcing strategy
- Build business case

**2. Market Research**
- Identify potential suppliers
- Conduct market analysis
- Assess supply market dynamics
- Benchmark pricing and terms

**3. Supplier Pre-Qualification**
- Screen for basic requirements
- Verify financial stability
- Check certifications and compliance
- Assess capacity and capability

**4. RFx Development & Issuance**
- Create RFP/RFQ/RFI documents
- Define evaluation criteria
- Issue to qualified suppliers
- Manage Q&A process

**5. Proposal Evaluation**
- Score supplier responses
- Conduct technical evaluations
- Perform cost analysis
- Site visits and audits

**6. Negotiation**
- Discuss terms and conditions
- Negotiate pricing and volumes
- Finalize service levels
- Address contingencies

**7. Final Selection**
- Make recommendation
- Obtain approvals
- Award contract
- Transition planning

---

## Supplier Evaluation Methods

### Weighted Scoring Model

**Most Common Approach:**
- Define evaluation criteria
- Assign weights based on importance
- Score each supplier on each criterion
- Calculate weighted total score

```python
import pandas as pd
import numpy as np

def weighted_scoring(suppliers, criteria, weights, scores):
    """
    Calculate weighted scores for supplier evaluation

    Parameters:
    - suppliers: list of supplier names
    - criteria: list of evaluation criteria
    - weights: dict {criterion: weight} (must sum to 1.0)
    - scores: dict {(supplier, criterion): score} (0-10 scale)

    Returns:
    - DataFrame with scores and rankings
    """

    # Validate weights sum to 1.0
    total_weight = sum(weights.values())
    if not np.isclose(total_weight, 1.0):
        print(f"Warning: Weights sum to {total_weight}, normalizing...")
        weights = {k: v/total_weight for k, v in weights.items()}

    results = []

    for supplier in suppliers:
        weighted_score = 0
        criterion_scores = {}

        for criterion in criteria:
            score = scores.get((supplier, criterion), 0)
            weight = weights.get(criterion, 0)
            weighted_value = score * weight

            criterion_scores[criterion] = score
            weighted_score += weighted_value

        results.append({
            'Supplier': supplier,
            **criterion_scores,
            'Weighted_Score': round(weighted_score, 2)
        })

    # Create DataFrame and rank
    df = pd.DataFrame(results)
    df['Rank'] = df['Weighted_Score'].rank(ascending=False, method='min')
    df = df.sort_values('Weighted_Score', ascending=False)

    return df


# Example usage
suppliers = ['Supplier_A', 'Supplier_B', 'Supplier_C']

criteria = ['Price', 'Quality', 'Delivery', 'Service', 'Innovation']

weights = {
    'Price': 0.30,
    'Quality': 0.25,
    'Delivery': 0.20,
    'Service': 0.15,
    'Innovation': 0.10
}

scores = {
    ('Supplier_A', 'Price'): 8,
    ('Supplier_A', 'Quality'): 9,
    ('Supplier_A', 'Delivery'): 7,
    ('Supplier_A', 'Service'): 8,
    ('Supplier_A', 'Innovation'): 9,

    ('Supplier_B', 'Price'): 9,
    ('Supplier_B', 'Quality'): 7,
    ('Supplier_B', 'Delivery'): 8,
    ('Supplier_B', 'Service'): 7,
    ('Supplier_B', 'Innovation'): 6,

    ('Supplier_C', 'Price'): 7,
    ('Supplier_C', 'Quality'): 9,
    ('Supplier_C', 'Delivery'): 9,
    ('Supplier_C', 'Service'): 9,
    ('Supplier_C', 'Innovation'): 8,
}

results = weighted_scoring(suppliers, criteria, weights, scores)
print(results)
```

### Total Cost of Ownership (TCO) Analysis

**Beyond Price:**
- Purchase price
- Transportation and logistics
- Quality costs (defects, returns)
- Inventory carrying costs
- Administrative costs
- Risk and disruption costs

```python
class TCOCalculator:
    """Total Cost of Ownership calculator for supplier comparison"""

    def __init__(self, supplier_name):
        self.supplier_name = supplier_name
        self.costs = {}

    def add_purchase_cost(self, unit_price, annual_volume):
        """Direct purchase cost"""
        self.costs['purchase'] = unit_price * annual_volume
        return self

    def add_logistics_cost(self, cost_per_unit, annual_volume):
        """Transportation, duties, handling"""
        self.costs['logistics'] = cost_per_unit * annual_volume
        return self

    def add_quality_cost(self, defect_rate, cost_per_defect, annual_volume):
        """Quality issues, returns, rework"""
        self.costs['quality'] = defect_rate * cost_per_defect * annual_volume
        return self

    def add_inventory_cost(self, lead_time_days, unit_cost,
                          annual_volume, carrying_rate=0.25):
        """Inventory carrying cost based on lead time"""
        avg_inventory = (lead_time_days / 365) * annual_volume
        inventory_value = avg_inventory * unit_cost
        self.costs['inventory'] = inventory_value * carrying_rate
        return self

    def add_admin_cost(self, annual_admin_cost):
        """Administrative overhead (POs, invoicing, etc.)"""
        self.costs['admin'] = annual_admin_cost
        return self

    def add_risk_cost(self, disruption_probability, disruption_cost):
        """Expected cost of supply disruptions"""
        self.costs['risk'] = disruption_probability * disruption_cost
        return self

    def calculate_tco(self):
        """Calculate total TCO and cost breakdown"""
        total_tco = sum(self.costs.values())

        return {
            'supplier': self.supplier_name,
            'total_tco': round(total_tco, 2),
            'breakdown': {k: round(v, 2) for k, v in self.costs.items()},
            'breakdown_pct': {
                k: round(v/total_tco*100, 1)
                for k, v in self.costs.items()
            }
        }


# Example: Compare two suppliers
annual_volume = 100000  # units

# Supplier A: Lower price, longer lead time, higher defect rate
supplier_a = TCOCalculator('Supplier_A')
supplier_a.add_purchase_cost(unit_price=10.00, annual_volume=annual_volume)
supplier_a.add_logistics_cost(cost_per_unit=1.50, annual_volume=annual_volume)
supplier_a.add_quality_cost(defect_rate=0.02, cost_per_defect=50, annual_volume=annual_volume)
supplier_a.add_inventory_cost(lead_time_days=45, unit_cost=10.00, annual_volume=annual_volume)
supplier_a.add_admin_cost(annual_admin_cost=25000)
supplier_a.add_risk_cost(disruption_probability=0.10, disruption_cost=200000)

tco_a = supplier_a.calculate_tco()

# Supplier B: Higher price, shorter lead time, lower defect rate
supplier_b = TCOCalculator('Supplier_B')
supplier_b.add_purchase_cost(unit_price=10.50, annual_volume=annual_volume)
supplier_b.add_logistics_cost(cost_per_unit=1.00, annual_volume=annual_volume)
supplier_b.add_quality_cost(defect_rate=0.005, cost_per_defect=50, annual_volume=annual_volume)
supplier_b.add_inventory_cost(lead_time_days=21, unit_cost=10.50, annual_volume=annual_volume)
supplier_b.add_admin_cost(annual_admin_cost=20000)
supplier_b.add_risk_cost(disruption_probability=0.03, disruption_cost=200000)

tco_b = supplier_b.calculate_tco()

# Compare
print(f"\n{tco_a['supplier']} TCO: ${tco_a['total_tco']:,.0f}")
print(f"{tco_b['supplier']} TCO: ${tco_b['total_tco']:,.0f}")
print(f"\nDifference: ${abs(tco_a['total_tco'] - tco_b['total_tco']):,.0f}")
```

### Analytical Hierarchy Process (AHP)

**For Complex Decisions:**
- Pairwise comparison of criteria
- Consistency checking
- Hierarchical decision structure
- Handles both quantitative and qualitative factors

```python
import numpy as np
from numpy.linalg import eig

def ahp_pairwise_matrix(comparisons):
    """
    Create pairwise comparison matrix for AHP

    comparisons: dict of tuples {(criterion_a, criterion_b): importance}
    importance scale: 1=equal, 3=moderate, 5=strong, 7=very strong, 9=extreme
    """

    # Extract unique criteria
    criteria = set()
    for (a, b) in comparisons.keys():
        criteria.add(a)
        criteria.add(b)
    criteria = sorted(list(criteria))
    n = len(criteria)

    # Build matrix
    matrix = np.ones((n, n))

    for i, crit_i in enumerate(criteria):
        for j, crit_j in enumerate(criteria):
            if i != j:
                if (crit_i, crit_j) in comparisons:
                    matrix[i, j] = comparisons[(crit_i, crit_j)]
                elif (crit_j, crit_i) in comparisons:
                    matrix[i, j] = 1.0 / comparisons[(crit_j, crit_i)]

    return matrix, criteria


def ahp_weights(matrix):
    """Calculate priority weights from pairwise comparison matrix"""

    # Calculate eigenvector of maximum eigenvalue
    eigenvalues, eigenvectors = eig(matrix)
    max_eigenvalue_idx = np.argmax(eigenvalues.real)
    principal_eigenvector = eigenvectors[:, max_eigenvalue_idx].real

    # Normalize to get weights
    weights = principal_eigenvector / principal_eigenvector.sum()

    # Calculate consistency ratio
    n = len(matrix)
    max_eigenvalue = eigenvalues[max_eigenvalue_idx].real
    ci = (max_eigenvalue - n) / (n - 1)

    # Random index values
    ri_values = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12,
                 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
    ri = ri_values.get(n, 1.49)

    cr = ci / ri if ri > 0 else 0

    return weights, cr


# Example: Compare evaluation criteria
comparisons = {
    ('Quality', 'Price'): 3,      # Quality is moderately more important than Price
    ('Quality', 'Delivery'): 5,   # Quality is strongly more important than Delivery
    ('Quality', 'Service'): 7,    # Quality is very strongly more important than Service
    ('Price', 'Delivery'): 3,     # Price is moderately more important than Delivery
    ('Price', 'Service'): 5,      # Price is strongly more important than Service
    ('Delivery', 'Service'): 3,   # Delivery is moderately more important than Service
}

matrix, criteria = ahp_pairwise_matrix(comparisons)
weights, consistency_ratio = ahp_weights(matrix)

print("AHP Criteria Weights:")
for criterion, weight in zip(criteria, weights):
    print(f"  {criterion}: {weight:.3f} ({weight*100:.1f}%)")

print(f"\nConsistency Ratio: {consistency_ratio:.3f}")
if consistency_ratio < 0.10:
    print("  ✓ Acceptable consistency (CR < 0.10)")
else:
    print("  ✗ Inconsistent judgments (CR >= 0.10), review needed")
```

---

## Supplier Qualification Criteria

### Financial Stability

**Key Metrics:**
- Credit rating (D&B, S&P)
- Years in business
- Annual revenue and growth
- Profit margins
- Debt-to-equity ratio
- Days sales outstanding (DSO)
- Working capital ratio

**Red Flags:**
- Recent bankruptcy or restructuring
- Declining revenues (>20% YoY)
- Negative cash flow
- High debt levels
- Frequent management turnover

```python
def assess_financial_health(financials):
    """
    Assess supplier financial health

    financials: dict with financial metrics
    Returns: risk score (0-10, higher is better)
    """

    score = 10.0
    flags = []

    # Years in business
    years = financials.get('years_in_business', 0)
    if years < 2:
        score -= 3
        flags.append("Limited operating history")
    elif years < 5:
        score -= 1

    # Revenue trend
    revenue_growth = financials.get('revenue_growth_yoy', 0)
    if revenue_growth < -0.20:
        score -= 2
        flags.append("Significant revenue decline")
    elif revenue_growth < 0:
        score -= 1

    # Profitability
    profit_margin = financials.get('profit_margin', 0)
    if profit_margin < 0:
        score -= 2
        flags.append("Unprofitable")
    elif profit_margin < 0.05:
        score -= 1

    # Liquidity
    current_ratio = financials.get('current_ratio', 0)
    if current_ratio < 1.0:
        score -= 2
        flags.append("Liquidity concerns")
    elif current_ratio < 1.5:
        score -= 0.5

    # Leverage
    debt_to_equity = financials.get('debt_to_equity', 0)
    if debt_to_equity > 2.0:
        score -= 1.5
        flags.append("High leverage")

    score = max(0, score)  # Floor at 0

    risk_level = 'Low' if score >= 7 else 'Medium' if score >= 4 else 'High'

    return {
        'score': round(score, 1),
        'risk_level': risk_level,
        'flags': flags
    }
```

### Operational Capability

**Assessment Areas:**
- Production capacity and utilization
- Technology and equipment
- Quality management systems (ISO 9001, etc.)
- Workforce skills and stability
- Process maturity
- Continuous improvement culture

**Evaluation Methods:**
- Site visits and audits
- Capability studies
- Reference checks
- Trial orders/samples

### Quality & Compliance

**Quality Indicators:**
- Certifications (ISO 9001, AS9100, IATF 16949, etc.)
- Defect rates (PPM)
- Process capability (Cpk)
- Quality management practices
- Testing and inspection procedures
- Corrective action processes

**Compliance Requirements:**
- Industry-specific regulations
- Safety standards (OSHA, etc.)
- Environmental (ISO 14001, RoHS, REACH)
- Social responsibility (SA8000)
- Conflict minerals (Dodd-Frank)
- Anti-bribery/corruption

### Delivery Performance

**Key Metrics:**
- On-time delivery rate (OTIF)
- Lead time consistency
- Order fill rate
- Flexibility and responsiveness
- Minimum order quantities
- Geographic coverage

### Innovation & Technology

**Evaluation Factors:**
- R&D investment
- Patent portfolio
- Technology roadmap
- Digital capabilities
- Collaboration on new products
- Industry leadership

---

## RFP/RFQ Process

### RFP Development Best Practices

**Document Structure:**

1. **Introduction & Overview**
   - Company background
   - Purpose and scope
   - Timeline and process
   - Contact information

2. **Requirements Specification**
   - Technical specifications
   - Volume requirements
   - Quality standards
   - Delivery requirements
   - Packaging and labeling

3. **Commercial Terms**
   - Pricing format (unit, volume tiers)
   - Payment terms
   - Incoterms
   - Contract duration
   - Price adjustment mechanisms

4. **Evaluation Criteria**
   - Weighted scoring factors
   - Must-have requirements
   - Preferred qualifications
   - Evaluation process

5. **Supplier Information Required**
   - Company profile
   - Financial statements
   - References
   - Certifications
   - Insurance coverage
   - Quality management

6. **Instructions to Bidders**
   - Submission format
   - Deadline
   - Q&A process
   - Confidentiality
   - Conditions and disclaimers

### RFP Response Scoring

```python
import pandas as pd

class RFPScorer:
    """Automated RFP response scoring system"""

    def __init__(self, criteria_weights):
        """
        Initialize with weighted criteria

        criteria_weights: dict {category: {criterion: weight}}
        """
        self.criteria_weights = criteria_weights
        self.supplier_scores = {}

    def add_supplier_response(self, supplier_name, responses):
        """
        Add supplier's scored responses

        responses: dict {category: {criterion: score}}
        scores on 0-10 scale
        """
        self.supplier_scores[supplier_name] = responses

    def calculate_scores(self):
        """Calculate weighted scores for all suppliers"""

        results = []

        for supplier, responses in self.supplier_scores.items():
            category_scores = {}
            total_weighted_score = 0
            total_weight = 0

            for category, criteria in self.criteria_weights.items():
                category_score = 0
                category_weight = sum(criteria.values())

                for criterion, weight in criteria.items():
                    score = responses.get(category, {}).get(criterion, 0)
                    category_score += score * weight
                    total_weighted_score += score * weight
                    total_weight += weight

                if category_weight > 0:
                    category_scores[category] = category_score / category_weight

            overall_score = total_weighted_score / total_weight if total_weight > 0 else 0

            results.append({
                'Supplier': supplier,
                **category_scores,
                'Overall_Score': round(overall_score, 2)
            })

        df = pd.DataFrame(results)
        df['Rank'] = df['Overall_Score'].rank(ascending=False, method='min')
        df = df.sort_values('Overall_Score', ascending=False)

        return df

    def generate_report(self):
        """Generate detailed scoring report"""
        df = self.calculate_scores()

        report = []
        report.append("=" * 80)
        report.append("RFP EVALUATION SUMMARY")
        report.append("=" * 80)
        report.append("")

        for _, row in df.iterrows():
            report.append(f"Rank #{int(row['Rank'])}: {row['Supplier']}")
            report.append(f"  Overall Score: {row['Overall_Score']:.2f}/10")
            report.append("")

        return "\n".join(report)


# Example usage
criteria = {
    'Technical': {
        'Specifications_Met': 0.15,
        'Quality_Certifications': 0.10,
        'Technical_Capability': 0.10
    },
    'Commercial': {
        'Price_Competitiveness': 0.20,
        'Payment_Terms': 0.05,
        'Volume_Flexibility': 0.05
    },
    'Operational': {
        'Lead_Time': 0.10,
        'Capacity': 0.08,
        'Geographic_Location': 0.07
    },
    'Strategic': {
        'Innovation': 0.05,
        'Sustainability': 0.03,
        'References': 0.02
    }
}

scorer = RFPScorer(criteria)

# Add supplier responses
scorer.add_supplier_response('Supplier_A', {
    'Technical': {'Specifications_Met': 9, 'Quality_Certifications': 8, 'Technical_Capability': 9},
    'Commercial': {'Price_Competitiveness': 7, 'Payment_Terms': 8, 'Volume_Flexibility': 7},
    'Operational': {'Lead_Time': 8, 'Capacity': 9, 'Geographic_Location': 7},
    'Strategic': {'Innovation': 9, 'Sustainability': 8, 'References': 9}
})

scorer.add_supplier_response('Supplier_B', {
    'Technical': {'Specifications_Met': 8, 'Quality_Certifications': 9, 'Technical_Capability': 8},
    'Commercial': {'Price_Competitiveness': 9, 'Payment_Terms': 7, 'Volume_Flexibility': 8},
    'Operational': {'Lead_Time': 7, 'Capacity': 8, 'Geographic_Location': 9},
    'Strategic': {'Innovation': 6, 'Sustainability': 7, 'References': 8}
})

results_df = scorer.calculate_scores()
print(results_df)
print("\n" + scorer.generate_report())
```

---

## Advanced Selection Techniques

### Multi-Attribute Utility Theory (MAUT)

**For Complex Trade-offs:**
- Convert attributes to common utility scale
- Handle non-linear preferences
- Risk attitudes incorporated

```python
def utility_function(value, min_val, max_val, risk_aversion=0.5):
    """
    Calculate utility for a value

    risk_aversion: 0 = risk neutral, <0 = risk seeking, >0 = risk averse
    """
    if max_val == min_val:
        return 1.0

    normalized = (value - min_val) / (max_val - min_val)

    # Power utility function
    if risk_aversion != 0:
        utility = normalized ** (1 - risk_aversion)
    else:
        utility = normalized

    return max(0, min(1, utility))
```

### Monte Carlo Simulation for Uncertainty

**When There's Uncertainty in Scores:**
- Model score distributions
- Run thousands of scenarios
- Calculate probability of best choice

```python
import numpy as np

def monte_carlo_supplier_selection(suppliers, criteria,
                                   score_distributions,
                                   n_simulations=10000):
    """
    Monte Carlo simulation for supplier selection under uncertainty

    score_distributions: dict {(supplier, criterion): (mean, std)}
    """

    results = {supplier: 0 for supplier in suppliers}

    for _ in range(n_simulations):
        scores = {}

        for supplier in suppliers:
            weighted_score = 0

            for criterion, weight in criteria.items():
                mean, std = score_distributions.get((supplier, criterion), (5, 1))
                score = np.random.normal(mean, std)
                score = max(0, min(10, score))  # Clip to 0-10
                weighted_score += score * weight

            scores[supplier] = weighted_score

        # Winner of this simulation
        winner = max(scores, key=scores.get)
        results[winner] += 1

    # Convert to probabilities
    probabilities = {
        supplier: count / n_simulations
        for supplier, count in results.items()
    }

    return probabilities


# Example with uncertainty
suppliers = ['Supplier_A', 'Supplier_B', 'Supplier_C']
criteria = {'Price': 0.4, 'Quality': 0.4, 'Delivery': 0.2}

# (mean, std) for each supplier-criterion pair
score_distributions = {
    ('Supplier_A', 'Price'): (8.0, 0.5),
    ('Supplier_A', 'Quality'): (9.0, 0.8),
    ('Supplier_A', 'Delivery'): (7.0, 1.0),

    ('Supplier_B', 'Price'): (9.0, 1.2),
    ('Supplier_B', 'Quality'): (7.0, 0.6),
    ('Supplier_B', 'Delivery'): (8.0, 0.8),

    ('Supplier_C', 'Price'): (7.0, 0.8),
    ('Supplier_C', 'Quality'): (9.0, 0.5),
    ('Supplier_C', 'Delivery'): (9.0, 0.7),
}

probabilities = monte_carlo_supplier_selection(
    suppliers, criteria, score_distributions
)

print("Probability of being best choice:")
for supplier, prob in sorted(probabilities.items(), key=lambda x: x[1], reverse=True):
    print(f"  {supplier}: {prob*100:.1f}%")
```

---

## Tools & Libraries

### Python Libraries

**Data Analysis & Scoring:**
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computations
- `scipy`: Scientific computing, optimization
- `scikit-learn`: Machine learning for predictive scoring

**Optimization:**
- `pulp`: Linear programming for multi-sourcing optimization
- `cvxpy`: Convex optimization
- `pyomo`: Mathematical optimization modeling

**Visualization:**
- `matplotlib`, `seaborn`: Statistical visualizations
- `plotly`: Interactive dashboards
- `networkx`: Supplier network visualization

### Commercial Software

**Sourcing Platforms:**
- **Coupa**: Source-to-pay platform
- **SAP Ariba**: Procurement and sourcing
- **Jaggaer**: Strategic sourcing suite
- **GEP SMART**: Unified procurement platform
- **Ivalua**: Source-to-pay solution
- **Zycus**: Source-to-pay suite

**Supplier Management:**
- **Dun & Bradstreet**: Supplier risk & financial data
- **RapidRatings**: Financial health ratings
- **EcoVadis**: Sustainability ratings
- **Resilinc**: Supply chain risk management

**Analytics:**
- **Tableau**, **Power BI**: Supplier analytics dashboards
- **Qlik**: Data visualization
- **ThoughtSpot**: Search & AI-driven analytics

---

## Common Challenges & Solutions

### Challenge: Lack of Objective Data

**Problem:**
- Limited supplier information
- Subjective evaluations
- Incomplete proposals

**Solutions:**
- Request verifiable data (certifications, test reports)
- Use industry benchmarks and standards
- Conduct site visits and audits
- Reference checks with existing customers
- Trial orders or pilot programs
- Third-party assessments (D&B, audits)

### Challenge: Price vs. Quality Trade-off

**Problem:**
- Lowest price often not the best value
- Difficult to quantify quality impact
- Stakeholder pressure on cost

**Solutions:**
- Use Total Cost of Ownership (TCO) analysis
- Quantify quality costs (defects, returns, downtime)
- Include risk and disruption costs
- Show long-term value vs. initial price
- Present multiple scenarios (low cost, balanced, premium)

### Challenge: Too Many Suppliers to Evaluate

**Problem:**
- RFP fatigue
- Resource constraints
- Time pressure

**Solutions:**
- Pre-qualification screening (knockout criteria)
- Two-stage process (RFI then RFP)
- Limit RFP to 3-5 qualified suppliers
- Use automated scoring for initial filtering
- Focus resources on top candidates

### Challenge: Single Source Dependency

**Problem:**
- Risk of supply disruption
- Limited negotiating power
- No backup option

**Solutions:**
- Dual sourcing strategy (70/30 split)
- Qualify backup suppliers
- Regional diversification
- Build inventory buffers
- Long-term agreements with protections
- Develop alternate specifications

### Challenge: Incumbent Advantage

**Problem:**
- Existing supplier has information advantage
- Switching costs and risks
- Relationship bias

**Solutions:**
- Level playing field in RFP (same info to all)
- Explicitly quantify switching costs
- Blind evaluation (anonymous proposals initially)
- Focus on future capabilities, not past
- Clear evaluation criteria upfront

### Challenge: Global Sourcing Complexity

**Problem:**
- Cultural and language barriers
- Time zones and communication
- Currency and payment terms
- Legal and compliance differences

**Solutions:**
- Use local representatives or agents
- Engage interpreters for technical discussions
- Standardize evaluation templates
- Legal review of international contracts
- Consider total landed cost (duties, freight)
- Factor in lead time and inventory impact

---

## Output Format

### Supplier Selection Report

**Executive Summary:**
- Recommended supplier(s) and rationale
- Key differentiators
- Total value and expected savings
- Implementation timeline and risks

**Evaluation Summary:**

| Rank | Supplier | Overall Score | Price | Quality | Delivery | Service | Total Cost (Annual) | Recommendation |
|------|----------|---------------|-------|---------|----------|---------|---------------------|----------------|
| 1 | Supplier B | 8.5 | 9 | 9 | 8 | 8 | $2.1M | Award 60% |
| 2 | Supplier C | 8.2 | 7 | 9 | 9 | 9 | $2.3M | Award 40% |
| 3 | Supplier A | 7.8 | 8 | 7 | 8 | 7 | $2.0M | Backup |

**Detailed Scoring:**

```
Supplier B: 8.5/10

Technical (35%): 8.8
  ✓ Specifications Met: 9/10
  ✓ Quality Certifications: 9/10 (ISO 9001, AS9100)
  ✓ Technical Capability: 8/10

Commercial (30%): 8.5
  ✓ Price Competitiveness: 9/10
  ✓ Payment Terms: 8/10 (Net 60)
  ✓ Volume Flexibility: 8/10

Operational (25%): 8.0
  ✓ Lead Time: 8/10 (21 days)
  ✓ Capacity: 8/10 (150% of requirement)
  ✓ Geographic Coverage: 8/10

Strategic (10%): 9.0
  ✓ Innovation: 9/10 (strong R&D)
  ✓ Sustainability: 9/10 (ISO 14001)
  ✓ References: 9/10 (excellent)

Strengths:
- Strong quality certifications and processes
- Competitive pricing with good payment terms
- Excellent references from industry leaders
- Commitment to sustainability and innovation

Weaknesses:
- Moderate lead time (21 days vs. 14 days for Supplier C)
- Geographic concentration (single plant location)

Risks:
- Capacity constraints if demand exceeds 150% of current forecast
- Currency exposure (EUR-based pricing)
```

**Total Cost of Ownership Comparison:**

| Cost Component | Supplier A | Supplier B | Supplier C |
|----------------|------------|------------|------------|
| Purchase Price | $1,800,000 | $2,000,000 | $2,150,000 |
| Logistics | $150,000 | $100,000 | $80,000 |
| Quality Costs | $100,000 | $50,000 | $40,000 |
| Inventory Carrying | $80,000 | $60,000 | $50,000 |
| Administrative | $30,000 | $25,000 | $25,000 |
| Risk Premium | $40,000 | $20,000 | $15,000 |
| **Total TCO** | **$2,200,000** | **$2,255,000** | **$2,360,000** |

**Recommendation:**
- Award 60% to Supplier B (best balance of cost, quality, and capability)
- Award 40% to Supplier C (dual sourcing, best delivery and service)
- Qualify Supplier A as backup
- Implement quarterly performance reviews
- Re-bid in 2 years or if performance issues arise

**Implementation Plan:**
1. Contract negotiation and finalization (Weeks 1-2)
2. Purchase orders and production planning (Weeks 3-4)
3. First shipments and quality validation (Weeks 5-8)
4. Full production ramp-up (Weeks 9-12)
5. Performance review (Month 3)

---

## Questions to Ask

If you need more context:
1. What product/service category are you sourcing?
2. What's the annual spend volume and strategic importance?
3. What are the must-have requirements and evaluation criteria?
4. How many suppliers should be evaluated?
5. What's the timeline for supplier selection and go-live?
6. Are there incumbent suppliers or is this new sourcing?
7. What's the current pain point (cost, quality, risk, capacity)?
8. Any regulatory or compliance requirements?
9. Single source or multi-source strategy preferred?
10. What's the RFP process and who are the decision makers?

---

## Related Skills

- **strategic-sourcing**: For overall category sourcing strategy
- **procurement-optimization**: For optimal order allocation across suppliers
- **supplier-risk-management**: For ongoing supplier monitoring and risk assessment
- **contract-management**: For negotiating and managing supplier contracts
- **spend-analysis**: For category spend analysis and savings opportunities
- **quality-management**: For supplier quality audits and improvement
