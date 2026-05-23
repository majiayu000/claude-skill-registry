---
name: contract-management
description: When the user wants to manage supplier contracts, negotiate terms, track compliance, or optimize contract performance. Also use when the user mentions "contract lifecycle," "contract negotiation," "SLA management," "contract compliance," "renewal management," "terms and conditions," "pricing clauses," or "contract analytics." For supplier selection, see supplier-selection. For spend analysis, see spend-analysis.
---

# Contract Management

You are an expert in procurement contract management and negotiation. Your goal is to help organizations manage supplier contracts throughout their lifecycle, negotiate favorable terms, ensure compliance, and optimize contract value and performance.

## Initial Assessment

Before managing contracts, understand:

1. **Contract Portfolio Context**
   - How many active contracts?
   - Total contract value (TCV)?
   - Contract types? (MSA, SOW, purchase agreements)
   - Current pain points or issues?

2. **Management Maturity**
   - Existing contract management process?
   - CLM (Contract Lifecycle Management) system in place?
   - Contract compliance monitoring?
   - Renewal tracking process?

3. **Business Objectives**
   - Primary goal? (cost savings, risk mitigation, compliance)
   - Key performance indicators?
   - Contract standardization level?
   - Approval workflows?

4. **Resources & Systems**
   - Legal team involvement?
   - Procurement team structure?
   - Document management system?
   - Integration with ERP/P2P?

---

## Contract Lifecycle Management Framework

### Contract Lifecycle Stages

**1. Pre-Contract (Initiation)**
- Identify need
- Business case approval
- Supplier selection
- RFP/negotiation preparation

**2. Negotiation**
- Terms and conditions
- Pricing and payment terms
- SLAs and KPIs
- Risk allocation
- Legal review

**3. Execution**
- Contract signing
- Approvals and routing
- Contract repository storage
- Stakeholder notification

**4. Administration**
- Obligation tracking
- Performance monitoring
- Invoice and payment management
- Change requests
- Relationship management

**5. Renewal/Exit**
- Performance review
- Renewal decision
- Renegotiation
- Transition planning
- Contract closeout

---

## Contract Negotiation Strategies

### Negotiation Preparation

**Research & Analysis:**
- Market benchmarks and pricing
- Supplier financial health
- BATNA (Best Alternative To Negotiated Agreement)
- Walk-away point
- Stakeholder requirements

**Negotiation Leverage:**
- Volume/spend level
- Multi-year commitment
- Preferred supplier status
- Payment terms (early payment)
- Business growth potential
- Reference/testimonial

### Key Terms to Negotiate

**1. Pricing Terms**
```python
class PricingStructure:
    """Model different pricing structures for negotiation"""

    @staticmethod
    def fixed_price(unit_price, volume, discount_tiers=None):
        """
        Fixed price with volume discounts

        discount_tiers: list of (volume_threshold, discount_pct)
        """
        total_cost = unit_price * volume

        if discount_tiers:
            applicable_discount = 0
            for threshold, discount in sorted(discount_tiers, reverse=True):
                if volume >= threshold:
                    applicable_discount = discount
                    break

            total_cost = total_cost * (1 - applicable_discount)

        return {
            'pricing_model': 'Fixed Price',
            'base_unit_price': unit_price,
            'volume': volume,
            'discount': applicable_discount if discount_tiers else 0,
            'total_cost': round(total_cost, 2),
            'effective_unit_price': round(total_cost / volume, 2)
        }

    @staticmethod
    def cost_plus(cost, markup_pct, volume):
        """Cost-plus pricing model"""
        unit_price = cost * (1 + markup_pct)
        total_cost = unit_price * volume

        return {
            'pricing_model': 'Cost Plus',
            'base_cost': cost,
            'markup_pct': markup_pct * 100,
            'unit_price': round(unit_price, 2),
            'volume': volume,
            'total_cost': round(total_cost, 2)
        }

    @staticmethod
    def index_based(base_price, index_value, base_index, volume, cap=None):
        """
        Index-linked pricing (e.g., commodity, inflation)

        cap: maximum % increase/decrease
        """
        index_adjustment = (index_value - base_index) / base_index

        if cap and abs(index_adjustment) > cap:
            index_adjustment = cap if index_adjustment > 0 else -cap

        adjusted_price = base_price * (1 + index_adjustment)
        total_cost = adjusted_price * volume

        return {
            'pricing_model': 'Index Based',
            'base_price': base_price,
            'base_index': base_index,
            'current_index': index_value,
            'adjustment_pct': round(index_adjustment * 100, 2),
            'adjusted_unit_price': round(adjusted_price, 2),
            'volume': volume,
            'total_cost': round(total_cost, 2),
            'cap_applied': cap is not None and abs(index_adjustment) > cap
        }

    @staticmethod
    def gain_share(baseline_cost, actual_cost, sharing_ratio, volume):
        """
        Gain-share pricing (savings split between parties)

        sharing_ratio: % of savings to buyer (e.g., 0.6 = 60/40 split)
        """
        savings = baseline_cost - actual_cost
        buyer_savings = savings * sharing_ratio
        supplier_savings = savings * (1 - sharing_ratio)

        buyer_price = actual_cost + supplier_savings
        total_cost = buyer_price * volume

        return {
            'pricing_model': 'Gain Share',
            'baseline_cost': baseline_cost,
            'actual_cost': actual_cost,
            'total_savings': round(savings, 2),
            'buyer_share': round(buyer_savings, 2),
            'supplier_share': round(supplier_savings, 2),
            'buyer_unit_price': round(buyer_price, 2),
            'volume': volume,
            'total_cost': round(total_cost, 2)
        }


# Example: Compare pricing models
volume = 100000

fixed = PricingStructure.fixed_price(
    unit_price=10.00,
    volume=volume,
    discount_tiers=[(50000, 0.05), (100000, 0.08)]
)

cost_plus = PricingStructure.cost_plus(
    cost=8.50,
    markup_pct=0.15,
    volume=volume
)

index = PricingStructure.index_based(
    base_price=10.00,
    index_value=105,
    base_index=100,
    volume=volume,
    cap=0.10  # 10% cap
)

print("Fixed Price:", fixed)
print("Cost Plus:", cost_plus)
print("Index Based:", index)
```

**2. Payment Terms**
- Standard: Net 30, Net 60, Net 90
- Early payment discount: 2/10 Net 30
- Payment milestones (for services)
- Advance payment vs. arrears
- E-invoicing and auto-payment

```python
def evaluate_payment_terms(invoice_amount, terms_options):
    """
    Evaluate different payment terms

    terms_options: list of dicts with payment terms
    """

    results = []

    for option in terms_options:
        term_type = option['type']
        days = option.get('days', 30)
        discount = option.get('discount_pct', 0)

        if term_type == 'standard':
            effective_cost = invoice_amount
            cash_impact_days = days

        elif term_type == 'early_discount':
            discount_days = option.get('discount_days', 10)
            if option.get('take_discount', True):
                effective_cost = invoice_amount * (1 - discount)
                cash_impact_days = discount_days
            else:
                effective_cost = invoice_amount
                cash_impact_days = days

        # Annualized cost of capital
        cost_of_capital_annual = 0.08  # 8% annual
        holding_cost = effective_cost * (cash_impact_days / 365) * cost_of_capital_annual

        total_cost = effective_cost + holding_cost

        results.append({
            'terms': option['name'],
            'payment_days': cash_impact_days,
            'effective_amount': round(effective_cost, 2),
            'holding_cost': round(holding_cost, 2),
            'total_cost': round(total_cost, 2),
            'savings_vs_baseline': 0  # Will calculate below
        })

    # Calculate savings vs. baseline (first option)
    baseline_cost = results[0]['total_cost']
    for result in results:
        result['savings_vs_baseline'] = round(baseline_cost - result['total_cost'], 2)

    return results


# Example
terms = [
    {'name': 'Net 30', 'type': 'standard', 'days': 30},
    {'name': 'Net 60', 'type': 'standard', 'days': 60},
    {'name': '2/10 Net 30 (take discount)', 'type': 'early_discount',
     'days': 30, 'discount_days': 10, 'discount_pct': 0.02, 'take_discount': True},
    {'name': '2/10 Net 30 (no discount)', 'type': 'early_discount',
     'days': 30, 'discount_days': 10, 'discount_pct': 0.02, 'take_discount': False},
]

payment_analysis = evaluate_payment_terms(invoice_amount=100000, terms_options=terms)

for result in payment_analysis:
    print(f"\n{result['terms']}")
    print(f"  Effective Amount: ${result['effective_amount']:,.2f}")
    print(f"  Total Cost: ${result['total_cost']:,.2f}")
    print(f"  Savings: ${result['savings_vs_baseline']:,.2f}")
```

**3. Service Level Agreements (SLAs)**

```python
class SLAManager:
    """Manage and track Service Level Agreements"""

    def __init__(self, contract_id):
        self.contract_id = contract_id
        self.slas = []

    def add_sla(self, metric, target, measurement_period,
               penalty_structure=None):
        """
        Add SLA metric

        penalty_structure: list of (threshold, penalty_pct)
        """
        sla = {
            'metric': metric,
            'target': target,
            'measurement_period': measurement_period,
            'penalty_structure': penalty_structure or []
        }
        self.slas.append(sla)

    def calculate_performance(self, metric, actual_value):
        """Calculate performance vs. SLA target"""

        sla = next((s for s in self.slas if s['metric'] == metric), None)
        if not sla:
            return None

        target = sla['target']

        # Determine if higher or lower is better based on metric name
        higher_better = any(word in metric.lower()
                          for word in ['uptime', 'delivery', 'fill', 'accuracy'])

        if higher_better:
            performance_pct = (actual_value / target) * 100
            meets_target = actual_value >= target
        else:  # Lower is better (e.g., defect rate, lead time)
            performance_pct = (target / actual_value) * 100
            meets_target = actual_value <= target

        # Calculate penalty if applicable
        penalty_pct = 0
        if not meets_target and sla['penalty_structure']:
            variance = abs(actual_value - target) / target

            for threshold, penalty in sorted(sla['penalty_structure'], reverse=True):
                if variance >= threshold:
                    penalty_pct = penalty
                    break

        return {
            'metric': metric,
            'target': target,
            'actual': actual_value,
            'performance_%': round(performance_pct, 1),
            'meets_target': meets_target,
            'penalty_%': penalty_pct,
            'status': 'Met' if meets_target else 'Missed'
        }

    def generate_scorecard(self, actual_values):
        """
        Generate SLA performance scorecard

        actual_values: dict {metric: actual_value}
        """
        scorecard = []

        for metric, actual in actual_values.items():
            result = self.calculate_performance(metric, actual)
            if result:
                scorecard.append(result)

        # Calculate overall compliance
        total_slas = len(scorecard)
        met_slas = sum(1 for s in scorecard if s['meets_target'])
        compliance_rate = (met_slas / total_slas * 100) if total_slas > 0 else 0

        return {
            'contract_id': self.contract_id,
            'sla_details': scorecard,
            'total_slas': total_slas,
            'met_slas': met_slas,
            'compliance_rate_%': round(compliance_rate, 1)
        }


# Example usage
sla_manager = SLAManager(contract_id='CNT-12345')

# Add SLAs with penalty structures
sla_manager.add_sla(
    metric='On-Time Delivery %',
    target=95.0,
    measurement_period='monthly',
    penalty_structure=[
        (0.05, 0.02),  # 5% miss = 2% penalty
        (0.10, 0.05),  # 10% miss = 5% penalty
        (0.15, 0.10),  # 15% miss = 10% penalty
    ]
)

sla_manager.add_sla(
    metric='Defect Rate (PPM)',
    target=1000,
    measurement_period='monthly',
    penalty_structure=[
        (0.20, 0.03),  # 20% over = 3% penalty
        (0.50, 0.05),  # 50% over = 5% penalty
    ]
)

sla_manager.add_sla(
    metric='Lead Time (days)',
    target=21,
    measurement_period='monthly',
    penalty_structure=[
        (0.10, 0.01),  # 10% over = 1% penalty
        (0.25, 0.03),  # 25% over = 3% penalty
    ]
)

# Evaluate actual performance
actual_performance = {
    'On-Time Delivery %': 92.5,  # Below target
    'Defect Rate (PPM)': 1200,   # Above target
    'Lead Time (days)': 23       # Above target
}

scorecard = sla_manager.generate_scorecard(actual_performance)

print(f"\nSLA Scorecard for {scorecard['contract_id']}")
print(f"Compliance Rate: {scorecard['compliance_rate_%']}%")
print(f"Met {scorecard['met_slas']} of {scorecard['total_slas']} SLAs\n")

for sla in scorecard['sla_details']:
    print(f"{sla['metric']}:")
    print(f"  Target: {sla['target']}")
    print(f"  Actual: {sla['actual']}")
    print(f"  Status: {sla['status']}")
    if sla['penalty_%'] > 0:
        print(f"  Penalty: {sla['penalty_%']}%")
```

**4. Risk Allocation & Indemnification**
- Liability caps
- Insurance requirements
- Warranty terms
- Force majeure
- IP indemnification
- Data security and privacy

**5. Change Management**
- Change request process
- Pricing for scope changes
- Timeline adjustments
- Approval requirements

**6. Termination Clauses**
- Termination for convenience
- Termination for cause
- Notice periods
- Exit obligations
- Transition assistance

---

## Contract Compliance Monitoring

### Obligation Tracking

```python
import pandas as pd
from datetime import datetime, timedelta

class ContractObligationTracker:
    """Track contract obligations and deadlines"""

    def __init__(self):
        self.obligations = []

    def add_obligation(self, contract_id, obligation_type, description,
                      responsible_party, due_date, status='Pending'):
        """Add contract obligation"""

        self.obligations.append({
            'contract_id': contract_id,
            'type': obligation_type,
            'description': description,
            'responsible_party': responsible_party,
            'due_date': pd.to_datetime(due_date),
            'status': status,
            'added_date': datetime.now()
        })

    def get_upcoming_obligations(self, days_ahead=30):
        """Get obligations due in next N days"""

        df = pd.DataFrame(self.obligations)

        if df.empty:
            return df

        # Filter pending obligations
        df = df[df['status'] == 'Pending']

        # Filter by date range
        today = pd.Timestamp.now()
        future_date = today + timedelta(days=days_ahead)

        df = df[(df['due_date'] >= today) & (df['due_date'] <= future_date)]

        # Sort by due date
        df = df.sort_values('due_date')

        # Add days until due
        df['days_until_due'] = (df['due_date'] - today).dt.days

        return df

    def get_overdue_obligations(self):
        """Get overdue obligations"""

        df = pd.DataFrame(self.obligations)

        if df.empty:
            return df

        # Filter pending and overdue
        df = df[df['status'] == 'Pending']
        today = pd.Timestamp.now()
        df = df[df['due_date'] < today]

        # Sort by due date (oldest first)
        df = df.sort_values('due_date')

        # Add days overdue
        df['days_overdue'] = (today - df['due_date']).dt.days

        return df

    def update_status(self, contract_id, description, new_status):
        """Update obligation status"""

        for obligation in self.obligations:
            if (obligation['contract_id'] == contract_id and
                obligation['description'] == description):
                obligation['status'] = new_status
                obligation['completed_date'] = datetime.now()
                break


# Example usage
tracker = ContractObligationTracker()

# Add various obligations
tracker.add_obligation(
    contract_id='CNT-001',
    obligation_type='Deliverable',
    description='Submit quarterly business review',
    responsible_party='Supplier',
    due_date='2026-04-01'
)

tracker.add_obligation(
    contract_id='CNT-001',
    obligation_type='Payment',
    description='Monthly payment due',
    responsible_party='Buyer',
    due_date='2026-02-15'
)

tracker.add_obligation(
    contract_id='CNT-002',
    obligation_type='Audit',
    description='Annual security audit',
    responsible_party='Supplier',
    due_date='2026-03-15'
)

tracker.add_obligation(
    contract_id='CNT-003',
    obligation_type='Renewal Decision',
    description='Notify renewal or termination',
    responsible_party='Buyer',
    due_date='2026-01-30'  # Overdue
)

# Check upcoming obligations
upcoming = tracker.get_upcoming_obligations(days_ahead=60)
print("Upcoming Obligations:")
print(upcoming[['contract_id', 'description', 'due_date', 'days_until_due']])

# Check overdue
overdue = tracker.get_overdue_obligations()
print("\nOverdue Obligations:")
print(overdue[['contract_id', 'description', 'days_overdue']])
```

### Spend Compliance Monitoring

```python
def analyze_contract_compliance(actual_spend_df, contracts_df):
    """
    Analyze spend compliance with contracts

    actual_spend_df: DataFrame with actual purchases
    contracts_df: DataFrame with contract details
    """

    # Merge actual spend with contracts
    spend_with_contract = actual_spend_df.merge(
        contracts_df[['supplier_name', 'category', 'contract_id',
                     'contracted_price', 'volume_commitment']],
        on=['supplier_name', 'category'],
        how='left'
    )

    # Calculate compliance metrics
    compliance_summary = []

    for contract_id in contracts_df['contract_id'].unique():
        contract_data = spend_with_contract[
            spend_with_contract['contract_id'] == contract_id
        ]

        if len(contract_data) == 0:
            continue

        contract = contracts_df[contracts_df['contract_id'] == contract_id].iloc[0]

        total_spend = contract_data['spend_amount'].sum()
        total_volume = contract_data['volume'].sum()
        volume_commitment = contract['volume_commitment']

        # Volume compliance
        volume_achievement = total_volume / volume_commitment * 100

        # Price compliance
        contract_data['price_variance'] = (
            contract_data['unit_price'] - contract_data['contracted_price']
        ) / contract_data['contracted_price']

        avg_price_variance = contract_data['price_variance'].mean() * 100
        price_compliant = (contract_data['price_variance'].abs() < 0.02).mean() * 100

        compliance_summary.append({
            'contract_id': contract_id,
            'supplier': contract['supplier_name'],
            'category': contract['category'],
            'total_spend': total_spend,
            'volume_commitment': volume_commitment,
            'actual_volume': total_volume,
            'volume_achievement_%': round(volume_achievement, 1),
            'avg_price_variance_%': round(avg_price_variance, 1),
            'price_compliance_%': round(price_compliant, 1),
            'status': 'Compliant' if (volume_achievement >= 80 and
                                     abs(avg_price_variance) < 5) else 'Non-Compliant'
        })

    return pd.DataFrame(compliance_summary)
```

---

## Contract Renewal Management

### Renewal Decision Framework

```python
class ContractRenewalAnalysis:
    """Analyze contract for renewal decision"""

    def __init__(self, contract_id, current_terms):
        self.contract_id = contract_id
        self.current_terms = current_terms
        self.performance_data = {}
        self.market_data = {}

    def add_performance_data(self, sla_compliance, quality_score,
                            delivery_score, relationship_score):
        """Add supplier performance data"""
        self.performance_data = {
            'sla_compliance_%': sla_compliance,
            'quality_score': quality_score,  # 0-10
            'delivery_score': delivery_score,  # 0-10
            'relationship_score': relationship_score  # 0-10
        }

    def add_market_data(self, market_price, inflation_rate,
                       competitive_alternatives):
        """Add market intelligence"""
        self.market_data = {
            'market_price': market_price,
            'current_price': self.current_terms['price'],
            'inflation_rate': inflation_rate,
            'competitive_alternatives': competitive_alternatives
        }

    def calculate_renewal_score(self):
        """Calculate overall renewal recommendation score"""

        score = 0
        max_score = 100
        factors = []

        # Performance scoring (40 points)
        if self.performance_data:
            perf = self.performance_data

            # SLA compliance (15 points)
            sla_points = (perf['sla_compliance_%'] / 100) * 15
            score += sla_points

            if perf['sla_compliance_%'] >= 95:
                factors.append("✓ Excellent SLA compliance")
            elif perf['sla_compliance_%'] < 90:
                factors.append("✗ Poor SLA compliance")

            # Quality (10 points)
            quality_points = (perf['quality_score'] / 10) * 10
            score += quality_points

            # Delivery (10 points)
            delivery_points = (perf['delivery_score'] / 10) * 10
            score += delivery_points

            # Relationship (5 points)
            relationship_points = (perf['relationship_score'] / 10) * 5
            score += relationship_points

        # Price competitiveness (30 points)
        if self.market_data:
            market = self.market_data

            price_variance = (market['current_price'] - market['market_price']) / market['market_price']

            if price_variance <= -0.05:  # 5% below market
                price_points = 30
                factors.append("✓ Very competitive pricing")
            elif price_variance <= 0:
                price_points = 25
                factors.append("✓ Competitive pricing")
            elif price_variance <= 0.05:
                price_points = 20
                factors.append("~ At market price")
            elif price_variance <= 0.10:
                price_points = 10
                factors.append("✗ Above market price")
            else:
                price_points = 0
                factors.append("✗✗ Significantly above market")

            score += price_points

            # Competitive alternatives (10 points)
            if market['competitive_alternatives'] == 0:
                score += 0
                factors.append("✗ No alternatives (locked in)")
            elif market['competitive_alternatives'] <= 2:
                score += 5
                factors.append("~ Limited alternatives")
            else:
                score += 10
                factors.append("✓ Multiple alternatives available")

        # Switching cost consideration (20 points)
        switching_cost = self.current_terms.get('switching_cost', 'medium')
        if switching_cost == 'low':
            score += 20
        elif switching_cost == 'medium':
            score += 12
        else:  # high
            score += 5
            factors.append("⚠ High switching cost")

        # Normalize to 100
        score = min(score, max_score)

        # Recommendation
        if score >= 80:
            recommendation = "Renew - Strong Performance"
        elif score >= 60:
            recommendation = "Renew with Renegotiation"
        elif score >= 40:
            recommendation = "Competitive Bid"
        else:
            recommendation = "Replace - Poor Value"

        return {
            'contract_id': self.contract_id,
            'renewal_score': round(score, 1),
            'recommendation': recommendation,
            'key_factors': factors,
            'performance_data': self.performance_data,
            'market_data': self.market_data
        }


# Example usage
renewal = ContractRenewalAnalysis(
    contract_id='CNT-12345',
    current_terms={
        'price': 105,
        'volume': 10000,
        'switching_cost': 'medium'
    }
)

renewal.add_performance_data(
    sla_compliance=94.5,
    quality_score=8.5,
    delivery_score=9.0,
    relationship_score=8.0
)

renewal.add_market_data(
    market_price=100,
    inflation_rate=0.03,
    competitive_alternatives=3
)

result = renewal.calculate_renewal_score()

print(f"\nRenewal Analysis: {result['contract_id']}")
print(f"Renewal Score: {result['renewal_score']}/100")
print(f"Recommendation: {result['recommendation']}")
print("\nKey Factors:")
for factor in result['key_factors']:
    print(f"  {factor}")
```

---

## Contract Analytics

### Portfolio Analytics

```python
def contract_portfolio_analytics(contracts_df):
    """
    Analyze contract portfolio

    contracts_df: DataFrame with contract details
    """

    analytics = {}

    # Total contract value
    analytics['total_contract_value'] = contracts_df['annual_value'].sum()

    # Number of contracts
    analytics['total_contracts'] = len(contracts_df)

    # Contracts by status
    analytics['by_status'] = contracts_df.groupby('status')['annual_value'].agg([
        ('count', 'count'),
        ('value', 'sum')
    ]).to_dict('index')

    # Contracts expiring in next 90 days
    today = pd.Timestamp.now()
    expiry_threshold = today + timedelta(days=90)

    expiring_soon = contracts_df[
        (contracts_df['end_date'] >= today) &
        (contracts_df['end_date'] <= expiry_threshold)
    ]

    analytics['expiring_90_days'] = {
        'count': len(expiring_soon),
        'value': expiring_soon['annual_value'].sum(),
        'contracts': expiring_soon['contract_id'].tolist()
    }

    # Average contract value
    analytics['avg_contract_value'] = contracts_df['annual_value'].mean()

    # Contract concentration (top 10 by value)
    top_10_value = contracts_df.nlargest(10, 'annual_value')['annual_value'].sum()
    analytics['top_10_concentration_%'] = (
        top_10_value / analytics['total_contract_value'] * 100
    )

    # By category
    analytics['by_category'] = contracts_df.groupby('category')['annual_value'].agg([
        ('count', 'count'),
        ('value', 'sum')
    ]).to_dict('index')

    return analytics
```

---

## Tools & Libraries

### Python Libraries

**Document Management:**
- `python-docx`: Microsoft Word documents
- `PyPDF2`, `pdfplumber`: PDF parsing
- `spacy`, `nltk`: Natural language processing
- `pandas`: Data analysis

**Contract Analytics:**
- `numpy`: Numerical analysis
- `matplotlib`, `seaborn`: Visualization
- `sklearn`: Machine learning for contract analysis

### Commercial Software

**Contract Lifecycle Management (CLM):**
- **Coupa CLM**: Contract management platform
- **SAP Ariba Contracts**: Contract lifecycle
- **Icertis**: Enterprise contract management
- **Agiloft**: CLM with AI
- **DocuSign CLM (SpringCM)**: Digital contracting
- **Ironclad**: Digital contracting platform
- **Concord**: Contract management

**Legal Tech:**
- **Kira Systems**: AI contract review
- **LawGeex**: AI contract review
- **eBrevia**: Contract analytics

**Document Management:**
- **SharePoint**: Collaboration and storage
- **Box**, **Dropbox**: Cloud storage
- **M-Files**: Intelligent information management

---

## Common Challenges & Solutions

### Challenge: Contract Fragmentation

**Problem:**
- Contracts stored in multiple locations
- No central repository
- Version control issues
- Hard to find specific contracts

**Solutions:**
- Implement CLM system
- Centralized contract repository
- Metadata tagging and indexing
- Search functionality
- Access controls and permissions
- Regular audits and cleanup

### Challenge: Renewal Tracking

**Problem:**
- Missed renewal deadlines
- Auto-renewals unnoticed
- Last-minute scrambling
- Lost negotiation leverage

**Solutions:**
- Automated renewal reminders (90/60/30 days)
- Contract calendar/dashboard
- Renewal workflow process
- Performance review requirement before renewal
- Standard renewal timelines
- Executive visibility on expirations

### Challenge: Compliance Monitoring

**Problem:**
- Can't track contract terms
- Maverick spending
- Price leakage
- SLA non-compliance unnoticed

**Solutions:**
- Obligation tracking system
- Automated compliance alerts
- Integration with P2P system
- Regular compliance audits
- Supplier scorecards
- Penalty enforcement process

### Challenge: Contract Negotiation Expertise

**Problem:**
- Procurement lacks legal expertise
- One-sided terms accepted
- Inconsistent contract terms
- Risk exposure

**Solutions:**
- Standard contract templates
- Legal team collaboration
- Negotiation training
- Playbooks for common terms
- External legal counsel (complex deals)
- Pre-approved terms matrix

### Challenge: Value Realization

**Problem:**
- Negotiated savings not realized
- Price increases unmonitored
- Volume commitments not tracked
- No post-contract management

**Solutions:**
- Contract vs. actual spend tracking
- Regular business reviews
- Performance dashboards
- Value realization process
- Stakeholder accountability
- Contract compliance team

---

## Output Format

### Contract Summary Report

**Executive Summary:**
- Total contract portfolio value
- Number of active contracts
- Key risks and opportunities
- Action items

**Portfolio Overview:**

| Metric | Value |
|--------|-------|
| Total Contract Value | $45.2M |
| Number of Contracts | 127 |
| Average Contract Value | $356K |
| Expiring in 90 Days | 15 contracts ($8.3M) |
| Compliance Rate | 87% |
| Top 10 Concentration | 62% |

**Contracts Requiring Action:**

| Contract ID | Supplier | Category | Value | Expiry | Action Required |
|-------------|----------|----------|-------|--------|-----------------|
| CNT-001 | Supplier A | IT Services | $3.2M | 2026-03-15 | Renewal decision |
| CNT-045 | Supplier B | Raw Materials | $2.8M | 2026-04-01 | Price renegotiation |
| CNT-078 | Supplier C | Logistics | $1.5M | Ongoing | SLA non-compliance |
| CNT-092 | Supplier D | MRO | $0.8M | 2026-02-28 | Volume shortfall |

**Renewal Pipeline (Next 12 Months):**

```
Q1 2026: 15 contracts, $8.3M
  - 8 recommend renew
  - 4 renegotiate
  - 3 competitive bid

Q2 2026: 23 contracts, $12.1M
  - 15 recommend renew
  - 6 renegotiate
  - 2 competitive bid

Q3 2026: 18 contracts, $6.8M
Q4 2026: 12 contracts, $4.5M
```

**Compliance Issues:**

- **Price Variance**: 12 contracts with >5% price variance
  - Estimated leakage: $450K annually
  - Action: Enforce contracted pricing

- **Volume Commitments**: 8 contracts below 80% of commitment
  - Risk: Price increase or penalty
  - Action: Consolidate demand or renegotiate

- **SLA Misses**: 5 suppliers consistently missing SLAs
  - Action: Enforce penalties, develop improvement plans

**Key Recommendations:**

1. Prioritize renewal of 15 contracts expiring in Q1
2. Renegotiate pricing for 4 contracts above market
3. Address SLA non-compliance with 5 suppliers
4. Implement automated compliance monitoring
5. Consolidate spend with top-performing suppliers

---

## Questions to Ask

If you need more context:
1. How many active contracts and what's the total value?
2. Is there a CLM system in place?
3. What contract types? (MSA, SOW, purchase orders)
4. Primary concerns? (savings, compliance, risk, renewal management)
5. How are contracts currently stored and tracked?
6. Any upcoming renewals or expirations?
7. Are there compliance or performance issues?
8. Who are the key stakeholders? (procurement, legal, finance)
9. What metrics or KPIs are tracked?
10. Any specific contracts that need attention?

---

## Related Skills

- **supplier-selection**: For selecting suppliers before contracting
- **strategic-sourcing**: For category sourcing strategies
- **procurement-optimization**: For optimal contract terms
- **spend-analysis**: For contract spend compliance
- **supplier-risk-management**: For contract risk assessment
- **quality-management**: For SLA monitoring and performance
