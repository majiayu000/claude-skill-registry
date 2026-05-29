---
name: hospitality-procurement
description: When the user wants to optimize hospitality purchasing, manage hotel/restaurant suppliers, or improve procurement processes. Also use when the user mentions "hotel procurement," "restaurant purchasing," "hospitality sourcing," "F&B procurement," "hotel supplier management," "group purchasing organization," "contract negotiation," or "hospitality spend management." For hotel operations, see hotel-inventory-management. For cruise operations, see cruise-supply-chain.
---

# Hospitality Procurement

You are an expert in hospitality procurement and purchasing management. Your goal is to help optimize purchasing strategies, supplier relationships, and cost management for hotels, restaurants, and hospitality operations while maintaining quality standards and operational efficiency.

## Initial Assessment

Before optimizing hospitality procurement, understand:

1. **Property Profile**
   - Property type? (hotel, resort, restaurant, cruise, multi-unit)
   - Size and scale? (rooms, covers, locations)
   - Service level? (luxury, midscale, economy, QSR, fine dining)
   - Ownership structure? (independent, branded, franchise)

2. **Current Procurement Approach**
   - Procurement structure? (centralized, decentralized, hybrid)
   - Spend volume and categories?
   - Supplier base? (number of suppliers, concentration)
   - Contract structures? (fixed price, cost-plus, GPO)

3. **Category Breakdown**
   - F&B spend? (food, beverage, percentage of total)
   - Operating supplies? (cleaning, amenities, linens)
   - Capital purchases? (FF&E - furniture, fixtures, equipment)
   - Services? (maintenance, outsourced services)

4. **Objectives & Challenges**
   - Primary goals? (cost reduction, quality, sustainability)
   - Current pain points? (costs, supplier issues, processes)
   - Technology systems? (procurement platform, ERP)
   - Sustainability targets?

---

## Hospitality Procurement Framework

### Spend Categories

**Food & Beverage (35-45% of procurement spend):**
- Proteins (meat, poultry, seafood)
- Produce (fruits, vegetables)
- Dairy products
- Dry goods and staples
- Beverages (alcoholic, non-alcoholic)
- Specialty ingredients

**Operating Supplies (15-25%):**
- Guest amenities (toiletries, slippers, robes)
- Cleaning supplies and chemicals
- Paper products (toilet paper, napkins, etc.)
- Kitchen disposables
- Office supplies

**Linens & Uniforms (8-12%):**
- Bed linens and towels
- Table linens
- Staff uniforms
- Laundry supplies

**FF&E (Furniture, Fixtures, Equipment) (10-15%):**
- Furniture (beds, chairs, tables)
- Kitchen equipment
- Technology (TVs, phones, Wi-Fi)
- Fixtures and décor

**Services (10-15%):**
- Maintenance and repairs
- Waste management
- Pest control
- Landscaping

---

## Strategic Sourcing & Category Management

### Spend Analysis & Opportunity Identification

```python
import numpy as np
import pandas as pd

class HospitalitySpendAnalyzer:
    """
    Analyze procurement spend to identify savings opportunities
    """

    def __init__(self, spend_data):
        self.spend_data = spend_data  # DataFrame with transactions

    def perform_spend_analysis(self):
        """
        Comprehensive spend analysis

        Key outputs:
        - Spend by category
        - Supplier concentration
        - Maverick spend
        - Price variance analysis
        """

        # Spend by category
        category_spend = self.spend_data.groupby('category').agg({
            'amount': 'sum',
            'supplier': 'nunique',
            'transaction_id': 'count'
        }).reset_index()

        category_spend.columns = ['category', 'total_spend', 'num_suppliers',
                                  'num_transactions']
        category_spend['pct_of_total'] = (
            category_spend['total_spend'] / category_spend['total_spend'].sum() * 100
        )

        # Supplier concentration (80/20 rule)
        supplier_spend = self.spend_data.groupby('supplier')['amount'].sum().sort_values(
            ascending=False
        )

        cumulative_pct = supplier_spend.cumsum() / supplier_spend.sum() * 100
        top_suppliers = cumulative_pct[cumulative_pct <= 80].index

        # Pareto analysis
        pareto = {
            'top_20_suppliers': len(top_suppliers),
            'top_20_spend_pct': supplier_spend.loc[top_suppliers].sum() / supplier_spend.sum() * 100,
            'total_suppliers': len(supplier_spend),
            'concentration_ratio': len(top_suppliers) / len(supplier_spend)
        }

        # Price variance (for commodities)
        price_variance = self.calculate_price_variance()

        return {
            'category_spend': category_spend,
            'pareto_analysis': pareto,
            'price_variance': price_variance,
            'total_spend': self.spend_data['amount'].sum()
        }

    def calculate_price_variance(self):
        """
        Identify price discrepancies across suppliers and locations

        Opportunities for standardization and negotiation
        """

        # Calculate unit prices where applicable
        items_with_prices = self.spend_data[
            self.spend_data['quantity'].notna() & (self.spend_data['quantity'] > 0)
        ].copy()

        items_with_prices['unit_price'] = (
            items_with_prices['amount'] / items_with_prices['quantity']
        )

        # Variance by item
        variance_analysis = items_with_prices.groupby('item_description').agg({
            'unit_price': ['mean', 'std', 'min', 'max', 'count']
        }).reset_index()

        variance_analysis.columns = ['item', 'avg_price', 'std_price',
                                     'min_price', 'max_price', 'transactions']

        # Calculate coefficient of variation
        variance_analysis['cv'] = (
            variance_analysis['std_price'] / variance_analysis['avg_price']
        )

        # Price variance opportunity (difference between min and max)
        variance_analysis['variance_pct'] = (
            (variance_analysis['max_price'] - variance_analysis['min_price']) /
            variance_analysis['avg_price'] * 100
        )

        # High variance items = negotiation opportunities
        high_variance = variance_analysis[
            (variance_analysis['variance_pct'] > 20) &
            (variance_analysis['transactions'] >= 10)
        ].sort_values('variance_pct', ascending=False)

        return high_variance

    def identify_savings_opportunities(self):
        """
        Identify and quantify savings opportunities

        Levers:
        - Consolidation
        - Standardization
        - Negotiation
        - Specification changes
        """

        analysis = self.perform_spend_analysis()

        opportunities = []

        # Supplier consolidation
        category_spend = analysis['category_spend']

        for _, cat in category_spend.iterrows():
            if cat['num_suppliers'] > 5 and cat['total_spend'] > 50000:
                # Opportunity to consolidate
                potential_savings = cat['total_spend'] * 0.08  # 8% savings estimate

                opportunities.append({
                    'category': cat['category'],
                    'opportunity_type': 'Supplier Consolidation',
                    'current_suppliers': cat['num_suppliers'],
                    'target_suppliers': 2,
                    'potential_savings': potential_savings,
                    'confidence': 'Medium'
                })

        # Price standardization
        price_variance = analysis['price_variance']

        for _, item in price_variance.head(20).iterrows():
            if item['variance_pct'] > 30:
                # Calculate savings from standardization to average price
                # (Simplified - would need transaction volumes)
                estimated_savings = item['avg_price'] * 0.15 * item['transactions']

                opportunities.append({
                    'category': 'Price Standardization',
                    'opportunity_type': 'Price Harmonization',
                    'item': item['item'],
                    'current_variance': f"{item['variance_pct']:.1f}%",
                    'potential_savings': estimated_savings,
                    'confidence': 'High'
                })

        return pd.DataFrame(opportunities)

# Example usage
# spend_data would be a DataFrame with columns:
# ['transaction_id', 'date', 'category', 'supplier', 'item_description',
#  'quantity', 'amount', 'location']

spend_data = pd.DataFrame({
    'transaction_id': range(1000),
    'category': np.random.choice(['F&B-Proteins', 'F&B-Produce', 'Supplies',
                                 'Linens', 'Equipment'], 1000),
    'supplier': np.random.choice([f'Supplier_{i}' for i in range(50)], 1000),
    'amount': np.random.uniform(100, 5000, 1000)
})

analyzer = HospitalitySpendAnalyzer(spend_data)
analysis = analyzer.perform_spend_analysis()
opportunities = analyzer.identify_savings_opportunities()

print(f"Total annual spend: ${analysis['total_spend']:,.0f}")
print(f"\nTop opportunities:\n{opportunities.head()}")
```

---

## Supplier Management & Negotiation

### Supplier Scorecard & Performance Management

```python
class SupplierPerformanceManager:
    """
    Track and manage supplier performance across key metrics
    """

    def __init__(self, suppliers):
        self.suppliers = suppliers

    def calculate_supplier_scorecard(self, supplier_id, performance_data):
        """
        Calculate comprehensive supplier scorecard

        KPIs:
        - On-time delivery
        - Quality (acceptance rate)
        - Invoice accuracy
        - Responsiveness
        - Pricing competitiveness
        """

        metrics = {}

        # On-time delivery
        deliveries = performance_data['deliveries']
        on_time = sum([1 for d in deliveries if d['on_time']])
        metrics['on_time_delivery_pct'] = on_time / len(deliveries) * 100

        # Quality - acceptance rate
        receipts = performance_data['receipts']
        accepted = sum([r['quantity_accepted'] for r in receipts])
        delivered = sum([r['quantity_delivered'] for r in receipts])
        metrics['quality_acceptance_pct'] = accepted / delivered * 100 if delivered > 0 else 0

        # Invoice accuracy
        invoices = performance_data['invoices']
        accurate = sum([1 for i in invoices if i['accurate']])
        metrics['invoice_accuracy_pct'] = accurate / len(invoices) * 100 if len(invoices) > 0 else 100

        # Responsiveness (response time to inquiries)
        inquiries = performance_data.get('inquiries', [])
        if inquiries:
            avg_response_hours = np.mean([i['response_time_hours'] for i in inquiries])
            metrics['avg_response_hours'] = avg_response_hours
            # Score: < 4 hours = 100, 4-24 = 80, > 24 = 50
            if avg_response_hours < 4:
                metrics['responsiveness_score'] = 100
            elif avg_response_hours < 24:
                metrics['responsiveness_score'] = 80
            else:
                metrics['responsiveness_score'] = 50
        else:
            metrics['responsiveness_score'] = 100

        # Pricing competitiveness
        price_index = performance_data.get('price_vs_market', 1.0)
        # 1.0 = at market, < 1.0 = below market (better)
        metrics['price_index'] = price_index
        if price_index < 0.95:
            metrics['price_score'] = 100
        elif price_index < 1.05:
            metrics['price_score'] = 90
        else:
            metrics['price_score'] = 70

        # Overall score (weighted)
        weights = {
            'on_time_delivery_pct': 0.25,
            'quality_acceptance_pct': 0.30,
            'invoice_accuracy_pct': 0.15,
            'responsiveness_score': 0.10,
            'price_score': 0.20
        }

        overall_score = sum([
            metrics.get(key, 100) * weight
            for key, weight in weights.items()
        ])

        metrics['overall_score'] = overall_score

        # Performance tier
        if overall_score >= 90:
            tier = 'Preferred'
        elif overall_score >= 75:
            tier = 'Approved'
        elif overall_score >= 60:
            tier = 'Conditional'
        else:
            tier = 'Review Required'

        metrics['performance_tier'] = tier

        return metrics

    def supplier_segmentation(self, spend_data, performance_data):
        """
        Segment suppliers using Kraljic matrix

        Dimensions:
        - Spend/value (high/low)
        - Supply risk (high/low)

        Segments:
        - Strategic: High spend, high risk → Partnership
        - Leverage: High spend, low risk → Competitive bidding
        - Bottleneck: Low spend, high risk → Secure supply
        - Routine: Low spend, low risk → Simplify/automate
        """

        supplier_segments = {}

        for supplier_id, spend in spend_data.items():
            risk_score = performance_data.get(supplier_id, {}).get('supply_risk', 50)

            # Determine segment
            high_spend = spend > 100000
            high_risk = risk_score > 60

            if high_spend and high_risk:
                segment = 'Strategic'
                strategy = 'Develop partnership, long-term contracts'
            elif high_spend and not high_risk:
                segment = 'Leverage'
                strategy = 'Competitive bidding, volume discounts'
            elif not high_spend and high_risk:
                segment = 'Bottleneck'
                strategy = 'Secure supply, find alternatives'
            else:
                segment = 'Routine'
                strategy = 'Automate, consolidate, e-procurement'

            supplier_segments[supplier_id] = {
                'segment': segment,
                'spend': spend,
                'risk_score': risk_score,
                'strategy': strategy
            }

        return supplier_segments

# Example
manager = SupplierPerformanceManager([])

performance_data = {
    'deliveries': [
        {'on_time': True},
        {'on_time': True},
        {'on_time': False},
        {'on_time': True},
    ],
    'receipts': [
        {'quantity_delivered': 100, 'quantity_accepted': 98},
        {'quantity_delivered': 200, 'quantity_accepted': 200},
    ],
    'invoices': [
        {'accurate': True},
        {'accurate': True},
        {'accurate': False},
    ],
    'inquiries': [
        {'response_time_hours': 2},
        {'response_time_hours': 3},
    ],
    'price_vs_market': 0.98
}

scorecard = manager.calculate_supplier_scorecard('SUP001', performance_data)
print(f"Overall score: {scorecard['overall_score']:.1f}")
print(f"Performance tier: {scorecard['performance_tier']}")
```

---

## Group Purchasing & Consortia

### GPO (Group Purchasing Organization) Optimization

```python
def evaluate_gpo_membership(current_spend, gpo_contracts, admin_fee_pct=0.03):
    """
    Evaluate value of GPO membership vs. direct negotiation

    Parameters:
    - current_spend: current spending by category
    - gpo_contracts: available GPO contracts and pricing
    - admin_fee_pct: GPO administrative fee (typically 2-5%)
    """

    results = []

    for category, spend in current_spend.items():
        # Current situation
        current_price_index = 1.0  # baseline

        # GPO option
        if category in gpo_contracts:
            gpo_price_index = gpo_contracts[category]['price_index']
            gpo_spend = spend * gpo_price_index
            gpo_fee = gpo_spend * admin_fee_pct
            total_gpo_cost = gpo_spend + gpo_fee

            savings = spend - total_gpo_cost
            savings_pct = savings / spend * 100

            results.append({
                'category': category,
                'current_spend': spend,
                'gpo_spend': gpo_spend,
                'gpo_fee': gpo_fee,
                'total_gpo_cost': total_gpo_cost,
                'savings': savings,
                'savings_pct': savings_pct,
                'recommendation': 'Use GPO' if savings > 0 else 'Direct negotiation'
            })

    results_df = pd.DataFrame(results)

    return {
        'total_current_spend': sum(current_spend.values()),
        'total_gpo_spend': results_df['total_gpo_cost'].sum(),
        'total_savings': results_df['savings'].sum(),
        'savings_pct': results_df['savings'].sum() / sum(current_spend.values()) * 100,
        'category_analysis': results_df
    }

# Example
current_spend = {
    'F&B-Proteins': 500000,
    'F&B-Produce': 300000,
    'Supplies-Cleaning': 150000,
    'Linens': 100000
}

gpo_contracts = {
    'F&B-Proteins': {'price_index': 0.92},  # 8% discount
    'F&B-Produce': {'price_index': 0.95},   # 5% discount
    'Supplies-Cleaning': {'price_index': 0.88},  # 12% discount
    'Linens': {'price_index': 0.90}  # 10% discount
}

gpo_analysis = evaluate_gpo_membership(current_spend, gpo_contracts)
print(f"Total savings with GPO: ${gpo_analysis['total_savings']:,.0f} "
     f"({gpo_analysis['savings_pct']:.1f}%)")
```

---

## Sustainability & Responsible Sourcing

### Sustainable Procurement Scorecard

```python
class SustainableProcurementManager:
    """
    Manage sustainability in procurement decisions
    """

    def __init__(self, sustainability_goals):
        self.goals = sustainability_goals

    def evaluate_supplier_sustainability(self, supplier, certifications,
                                        environmental_data):
        """
        Score supplier on sustainability metrics

        Criteria:
        - Certifications (organic, Fair Trade, sustainable seafood, etc.)
        - Carbon footprint
        - Waste reduction
        - Local sourcing
        - Social responsibility
        """

        score = {}

        # Certifications
        cert_score = 0
        cert_weights = {
            'organic': 20,
            'fair_trade': 15,
            'msc_certified': 15,  # Marine Stewardship Council
            'rainforest_alliance': 10,
            'b_corp': 20,
            'iso_14001': 15
        }

        for cert, points in cert_weights.items():
            if cert in certifications:
                cert_score += points

        score['certification_score'] = min(cert_score, 100)

        # Carbon footprint
        carbon_emissions = environmental_data.get('carbon_kg_per_unit', 0)
        industry_avg = environmental_data.get('industry_avg_carbon', 10)

        if carbon_emissions < industry_avg * 0.7:
            score['carbon_score'] = 100
        elif carbon_emissions < industry_avg:
            score['carbon_score'] = 80
        elif carbon_emissions < industry_avg * 1.3:
            score['carbon_score'] = 60
        else:
            score['carbon_score'] = 40

        # Local sourcing (miles from property)
        distance = environmental_data.get('distance_miles', 1000)

        if distance < 50:
            score['local_score'] = 100
        elif distance < 150:
            score['local_score'] = 80
        elif distance < 500:
            score['local_score'] = 60
        else:
            score['local_score'] = 40

        # Social responsibility
        social_score = environmental_data.get('social_responsibility_score', 70)
        score['social_score'] = social_score

        # Waste reduction practices
        waste_diversion_pct = environmental_data.get('waste_diversion_pct', 50)
        score['waste_score'] = min(waste_diversion_pct, 100)

        # Overall sustainability score (weighted)
        overall = (
            score['certification_score'] * 0.25 +
            score['carbon_score'] * 0.25 +
            score['local_score'] * 0.15 +
            score['social_score'] * 0.20 +
            score['waste_score'] * 0.15
        )

        score['overall_sustainability_score'] = overall

        # Tier
        if overall >= 80:
            tier = 'Sustainability Leader'
        elif overall >= 65:
            tier = 'Sustainable'
        elif overall >= 50:
            tier = 'Developing'
        else:
            tier = 'Needs Improvement'

        score['sustainability_tier'] = tier

        return score

    def calculate_sustainable_procurement_pct(self, spend_by_supplier,
                                             supplier_sustainability):
        """
        Calculate percentage of spend with sustainable suppliers
        """

        total_spend = sum(spend_by_supplier.values())
        sustainable_spend = 0

        for supplier, spend in spend_by_supplier.items():
            sustainability_score = supplier_sustainability.get(supplier, {})

            if sustainability_score.get('overall_sustainability_score', 0) >= 65:
                sustainable_spend += spend

        sustainable_pct = sustainable_spend / total_spend * 100 if total_spend > 0 else 0

        return {
            'total_spend': total_spend,
            'sustainable_spend': sustainable_spend,
            'sustainable_pct': sustainable_pct,
            'target_pct': self.goals.get('sustainable_spend_target', 50),
            'gap_to_target': self.goals.get('sustainable_spend_target', 50) - sustainable_pct
        }
```

---

## Technology & Automation

### E-Procurement & P2P (Procure-to-Pay) Optimization

```python
def calculate_p2p_automation_roi(current_process_metrics, automation_costs,
                                transaction_volumes):
    """
    Calculate ROI of procurement automation

    Benefits:
    - Reduced manual processing
    - Fewer errors
    - Better compliance
    - Spend visibility
    - Faster cycle times
    """

    # Current state costs
    current_costs = {
        'manual_po_processing': (
            transaction_volumes['po_count'] *
            current_process_metrics['minutes_per_po'] / 60 *
            current_process_metrics['hourly_cost']
        ),
        'invoice_processing': (
            transaction_volumes['invoice_count'] *
            current_process_metrics['minutes_per_invoice'] / 60 *
            current_process_metrics['hourly_cost']
        ),
        'supplier_inquiries': (
            transaction_volumes['supplier_inquiries'] *
            current_process_metrics['minutes_per_inquiry'] / 60 *
            current_process_metrics['hourly_cost']
        ),
        'maverick_spend_cost': (
            current_process_metrics['maverick_spend_pct'] *
            transaction_volumes['total_spend'] *
            0.15  # 15% premium on maverick spend
        )
    }

    total_current_cost = sum(current_costs.values())

    # Future state with automation
    automation_efficiency = {
        'manual_po_processing': 0.70,  # 70% reduction
        'invoice_processing': 0.80,    # 80% reduction (3-way match)
        'supplier_inquiries': 0.60,    # 60% reduction (self-service)
        'maverick_spend_cost': 0.50    # 50% reduction (controlled procurement)
    }

    future_costs = {
        category: cost * (1 - automation_efficiency[category])
        for category, cost in current_costs.items()
    }

    total_future_cost = sum(future_costs.values())

    # Annual savings
    annual_savings = total_current_cost - total_future_cost

    # Implementation costs
    implementation_cost = automation_costs['software_license'] + \
                         automation_costs['implementation_fee'] + \
                         automation_costs['training']

    # Ongoing costs
    annual_ongoing_cost = automation_costs['annual_support'] + \
                         automation_costs['hosting']

    # Net annual benefit
    net_annual_benefit = annual_savings - annual_ongoing_cost

    # Payback period
    payback_months = implementation_cost / (net_annual_benefit / 12)

    # 3-year ROI
    three_year_benefit = net_annual_benefit * 3 - implementation_cost
    three_year_roi = three_year_benefit / implementation_cost * 100

    return {
        'current_annual_cost': total_current_cost,
        'future_annual_cost': total_future_cost,
        'annual_savings': annual_savings,
        'implementation_cost': implementation_cost,
        'annual_ongoing_cost': annual_ongoing_cost,
        'net_annual_benefit': net_annual_benefit,
        'payback_months': payback_months,
        'three_year_roi_pct': three_year_roi,
        'savings_breakdown': {
            category: current_costs[category] - future_costs[category]
            for category in current_costs
        }
    }

# Example
current_metrics = {
    'minutes_per_po': 20,
    'minutes_per_invoice': 15,
    'minutes_per_inquiry': 10,
    'hourly_cost': 35,
    'maverick_spend_pct': 0.25  # 25% of spend is maverick
}

transaction_volumes = {
    'po_count': 5000,
    'invoice_count': 6000,
    'supplier_inquiries': 2000,
    'total_spend': 10000000
}

automation_costs = {
    'software_license': 50000,
    'implementation_fee': 75000,
    'training': 15000,
    'annual_support': 15000,
    'hosting': 10000
}

roi = calculate_p2p_automation_roi(current_metrics, automation_costs,
                                  transaction_volumes)

print(f"Annual savings: ${roi['annual_savings']:,.0f}")
print(f"Payback period: {roi['payback_months']:.1f} months")
print(f"3-year ROI: {roi['three_year_roi_pct']:.0f}%")
```

---

## Tools & Libraries

### Python Libraries

**Data Analysis:**
- `pandas`, `numpy`: Data manipulation
- `matplotlib`, `seaborn`: Visualization
- `scikit-learn`: Analytics and clustering

**Optimization:**
- `PuLP`: Procurement optimization
- `scipy.optimize`: General optimization

### Commercial Software

**Procurement Platforms:**
- **Coupa**: Source-to-pay platform
- **Ariba (SAP)**: Procurement and invoicing
- **Oracle Procurement Cloud**: Enterprise procurement
- **Ivalua**: Spend management
- **GEP SMART**: Procurement software

**Hospitality-Specific:**
- **Birchstreet**: Hospitality procurement
- **MarketMan**: Restaurant purchasing
- **Apicbase**: F&B management
- **Restaurant365**: Restaurant operations

**Group Purchasing:**
- **Avendra (Aramark)**: Hospitality GPO
- **Entegra**: Foodservice GPO
- **Premier**: GPO for hospitality
- **Provista**: Broadline GPO

**Spend Analytics:**
- **SpendHQ**: Spend analysis
- **Insight Sourcing**: Procurement analytics
- **Zycus**: Spend analysis

---

## Common Challenges & Solutions

### Challenge: Maverick Spend

**Problem:**
- Off-contract purchasing
- Lack of spend visibility
- Compliance issues
- Lost savings opportunities

**Solutions:**
- E-procurement platform with catalogs
- Purchase approval workflows
- Preferred supplier programs
- Spend analytics and monitoring
- User training and communication

### Challenge: Supplier Proliferation

**Problem:**
- Too many suppliers (supplier sprawl)
- Administrative burden
- Lost volume leverage
- Difficult to manage

**Solutions:**
- Supplier rationalization programs
- Consolidation analysis
- Preferred supplier tiers
- Category management
- GPO participation

### Challenge: Price Volatility

**Problem:**
- Commodity price swings (beef, seafood, produce)
- Budget uncertainty
- Menu costing challenges

**Solutions:**
- Price hedging and contracts
- Menu engineering (substitutions)
- Alternative suppliers and products
- Seasonal menu planning
- Market intelligence and forecasting

### Challenge: Quality Consistency

**Problem:**
- Variable product quality
- Specification adherence
- Brand standards maintenance

**Solutions:**
- Detailed specifications
- Supplier quality audits
- Receiving inspection protocols
- Supplier performance scorecards
- Approved supplier lists

---

## Output Format

### Hospitality Procurement Report

**Executive Summary:**
- Total procurement spend
- Savings achieved vs. target
- Key initiatives and results
- Strategic priorities

**Spend Analysis:**

| Category | Annual Spend | % of Total | # Suppliers | Avg Price Variance |
|----------|--------------|------------|-------------|--------------------|
| F&B - Proteins | $1,250,000 | 25% | 8 | 12% |
| F&B - Produce | $875,000 | 17% | 12 | 18% |
| F&B - Dairy | $425,000 | 8% | 4 | 8% |
| Supplies - Cleaning | $320,000 | 6% | 6 | 15% |
| Supplies - Amenities | $285,000 | 6% | 10 | 10% |
| Linens | $450,000 | 9% | 3 | 5% |
| Equipment | $650,000 | 13% | 15 | 20% |
| Services | $745,000 | 15% | 25 | 25% |
| **Total** | **$5,000,000** | **100%** | **83** | **15%** |

**Supplier Performance:**

| Supplier | Category | Annual Spend | On-Time % | Quality % | Overall Score | Tier |
|----------|----------|--------------|-----------|-----------|---------------|------|
| ABC Foods | Proteins | $650,000 | 98% | 99% | 94 | Preferred |
| Fresh Produce Co | Produce | $520,000 | 92% | 95% | 88 | Approved |
| Clean Supply | Cleaning | $240,000 | 96% | 97% | 92 | Preferred |

**Savings Initiatives:**

| Initiative | Category | Target Savings | Achieved | % Complete | Status |
|------------|----------|----------------|----------|------------|--------|
| Protein consolidation | F&B | $125,000 | $108,000 | 86% | In Progress |
| GPO adoption | Supplies | $45,000 | $48,000 | 107% | Complete |
| Local produce program | F&B | $35,000 | $22,000 | 63% | In Progress |
| Linen standardization | Linens | $55,000 | $60,000 | 109% | Complete |
| **Total** | **All** | **$260,000** | **$238,000** | **92%** | - |

**Sustainability Metrics:**

| Metric | Current | Target | Progress |
|--------|---------|--------|----------|
| Sustainable Spend % | 42% | 50% | 84% |
| Local Sourcing % | 28% | 35% | 80% |
| Certified Organic % | 15% | 20% | 75% |
| Waste Diversion % | 38% | 45% | 84% |

**Recommendations:**
1. Complete protein supplier consolidation (save additional $17K)
2. Expand local produce program to 15 more items
3. Implement e-procurement platform (18-month ROI)
4. Renegotiate top 5 supplier contracts (8% savings opportunity)
5. Launch sustainability supplier certification program

---

## Questions to Ask

If you need more context:
1. What type of hospitality operation? (hotel, restaurant, multi-unit, cruise)
2. What's the scale of operations? (rooms, covers, locations)
3. What's the annual procurement spend?
4. How is procurement currently organized? (centralized, decentralized)
5. What are the key spend categories?
6. What systems are in place? (procurement platform, ERP)
7. What are the primary goals? (cost, quality, sustainability)

---

## Related Skills

- **hotel-inventory-management**: For hotel operations management
- **cruise-supply-chain**: For cruise procurement
- **tour-operations**: For tour operator purchasing
- **food-beverage-supply-chain**: For F&B specific operations
- **strategic-sourcing**: For sourcing strategies
- **contract-management**: For contract negotiation
- **supplier-selection**: For supplier evaluation
- **spend-analysis**: For spend analytics
- **sustainable-sourcing**: For sustainability programs
