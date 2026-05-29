---
name: sustainable-sourcing
description: When the user wants to implement sustainable procurement practices, evaluate supplier sustainability, or develop responsible sourcing programs. Also use when the user mentions "sustainable procurement," "responsible sourcing," "ESG sourcing," "ethical sourcing," "green procurement," "supplier sustainability," "sustainable suppliers," "social responsibility," or "environmental sourcing." For carbon tracking, see carbon-footprint-tracking. For circular economy, see circular-economy.
---

# Sustainable Sourcing

You are an expert in sustainable and responsible sourcing practices. Your goal is to help organizations integrate environmental, social, and governance (ESG) criteria into procurement decisions, evaluate supplier sustainability performance, and build responsible supply chains.

## Initial Assessment

Before implementing sustainable sourcing, understand:

1. **Sustainability Objectives**
   - What's driving sustainable sourcing? (stakeholder pressure, compliance, values)
   - Specific sustainability goals? (carbon reduction, human rights, circularity)
   - Industry sustainability benchmarks?
   - Customer or investor ESG requirements?

2. **Current State**
   - Existing supplier assessment processes?
   - Sustainability criteria in sourcing decisions?
   - Supplier sustainability data available?
   - Baseline sustainability performance?

3. **Scope & Priority**
   - Which categories to prioritize? (high spend, high risk, high impact)
   - Geographic focus areas?
   - Tier 1 vs. multi-tier approach?
   - Resource availability for implementation?

4. **Stakeholder Engagement**
   - Internal sustainability champions?
   - Supplier readiness and willingness?
   - Budget for sustainable sourcing programs?
   - Cross-functional support?

---

## Sustainable Sourcing Framework

### ESG Criteria for Sourcing

**Environmental Criteria:**
- Carbon emissions and climate impact
- Energy efficiency and renewable energy use
- Water consumption and water management
- Waste generation and circular practices
- Pollution prevention and control
- Biodiversity and land use
- Hazardous materials management
- Environmental certifications (ISO 14001, etc.)

**Social Criteria:**
- Labor rights and working conditions
- Health and safety
- Fair wages and benefits
- Child labor and forced labor prevention
- Diversity and inclusion
- Community impact
- Human rights due diligence
- Social certifications (SA 8000, Fair Trade, etc.)

**Governance Criteria:**
- Business ethics and anti-corruption
- Transparency and reporting
- Board diversity and independence
- Compliance management
- Risk management practices
- Supply chain traceability
- Whistleblower protections
- Data privacy and security

### Sustainable Sourcing Maturity Model

**Level 1: Compliance-Driven**
- Basic regulatory compliance
- Reactive to issues
- Limited supplier screening
- No systematic approach

**Level 2: Risk Management**
- Supplier risk assessments
- Code of conduct requirements
- Basic audits for high-risk suppliers
- Corrective action processes

**Level 3: Strategic Integration**
- Sustainability criteria in sourcing decisions
- Supplier development programs
- Performance scorecards
- Collaboration on improvements

**Level 4: Value Creation**
- Innovation partnerships
- Circular economy initiatives
- Life cycle optimization
- Shared value creation

**Level 5: Industry Leadership**
- Systemic change initiatives
- Multi-stakeholder collaborations
- Transparency and advocacy
- Transformative impact

---

## Supplier Sustainability Assessment

### Comprehensive ESG Scoring

```python
import pandas as pd
import numpy as np

class SustainableSourcingManager:
    """Manage sustainable sourcing assessments and decisions"""

    def __init__(self):
        self.suppliers = {}
        self.assessment_criteria = self._define_criteria()
        self.assessments = []

    def _define_criteria(self):
        """Define ESG assessment criteria with weightings"""

        return {
            'environmental': {
                'weight': 0.35,
                'subcriteria': {
                    'carbon_emissions': {'weight': 0.30, 'metric': 'emissions_intensity'},
                    'energy_management': {'weight': 0.20, 'metric': 'renewable_energy_pct'},
                    'water_management': {'weight': 0.15, 'metric': 'water_efficiency'},
                    'waste_management': {'weight': 0.15, 'metric': 'waste_recycling_rate'},
                    'certifications': {'weight': 0.20, 'metric': 'env_certifications'}
                }
            },
            'social': {
                'weight': 0.35,
                'subcriteria': {
                    'labor_rights': {'weight': 0.30, 'metric': 'labor_audit_score'},
                    'health_safety': {'weight': 0.25, 'metric': 'safety_performance'},
                    'fair_compensation': {'weight': 0.20, 'metric': 'wage_fairness'},
                    'diversity_inclusion': {'weight': 0.15, 'metric': 'diversity_metrics'},
                    'community_impact': {'weight': 0.10, 'metric': 'community_engagement'}
                }
            },
            'governance': {
                'weight': 0.30,
                'subcriteria': {
                    'ethics_compliance': {'weight': 0.30, 'metric': 'compliance_record'},
                    'transparency': {'weight': 0.25, 'metric': 'disclosure_score'},
                    'risk_management': {'weight': 0.20, 'metric': 'risk_processes'},
                    'business_continuity': {'weight': 0.15, 'metric': 'bcp_readiness'},
                    'data_security': {'weight': 0.10, 'metric': 'cybersecurity_score'}
                }
            }
        }

    def assess_supplier_esg(self, supplier_id, supplier_name, esg_data):
        """
        Conduct comprehensive ESG assessment of supplier

        esg_data: dict with environmental, social, governance metrics
        """

        assessment = {
            'supplier_id': supplier_id,
            'supplier_name': supplier_name,
            'dimension_scores': {},
            'overall_score': 0,
            'rating': '',
            'strengths': [],
            'improvement_areas': [],
            'red_flags': []
        }

        total_weighted_score = 0

        # Assess each dimension
        for dimension, dimension_config in self.assessment_criteria.items():
            dimension_score = 0

            for criterion, criterion_config in dimension_config['subcriteria'].items():
                metric_value = esg_data.get(dimension, {}).get(criterion, 50)  # Default to 50/100

                # Score the metric (0-100 scale)
                criterion_score = self._score_metric(metric_value, criterion)

                # Weight the criterion
                weighted_criterion = criterion_score * criterion_config['weight']
                dimension_score += weighted_criterion

                # Identify strengths (>80) and weaknesses (<40)
                if criterion_score >= 80:
                    assessment['strengths'].append(f"{dimension.capitalize()}: {criterion} ({criterion_score}/100)")
                elif criterion_score < 40:
                    assessment['improvement_areas'].append(f"{dimension.capitalize()}: {criterion} ({criterion_score}/100)")

                # Check for red flags (critical issues)
                if criterion_score < 20:
                    assessment['red_flags'].append(f"Critical: {dimension} - {criterion} (score: {criterion_score})")

            assessment['dimension_scores'][dimension] = round(dimension_score, 1)
            total_weighted_score += dimension_score * dimension_config['weight']

        assessment['overall_score'] = round(total_weighted_score, 1)
        assessment['rating'] = self._get_rating(total_weighted_score)

        self.assessments.append(assessment)

        return assessment

    def _score_metric(self, metric_value, criterion):
        """
        Convert metric value to 0-100 score

        Simplified - in reality would have criterion-specific scoring logic
        """

        # Assume metric_value is already on 0-100 scale
        # In reality, would normalize different metric types

        return min(100, max(0, metric_value))

    def _get_rating(self, score):
        """Convert score to rating"""
        if score >= 80:
            return 'A - Leader'
        elif score >= 65:
            return 'B - Advanced'
        elif score >= 50:
            return 'C - Adequate'
        elif score >= 35:
            return 'D - Needs Improvement'
        else:
            return 'F - Critical Gaps'

    def compare_suppliers(self, supplier_ids=None):
        """Compare ESG performance across suppliers"""

        if supplier_ids:
            assessments = [a for a in self.assessments if a['supplier_id'] in supplier_ids]
        else:
            assessments = self.assessments

        if not assessments:
            return None

        df = pd.DataFrame([{
            'supplier_id': a['supplier_id'],
            'supplier_name': a['supplier_name'],
            'overall_score': a['overall_score'],
            'rating': a['rating'],
            'environmental': a['dimension_scores'].get('environmental', 0),
            'social': a['dimension_scores'].get('social', 0),
            'governance': a['dimension_scores'].get('governance', 0),
            'red_flags': len(a['red_flags'])
        } for a in assessments])

        df = df.sort_values('overall_score', ascending=False)

        return df

    def calculate_sustainable_sourcing_score(self, spend_data):
        """
        Calculate sustainable sourcing score for portfolio

        spend_data: list of dicts with supplier_id and annual_spend
        """

        total_spend = sum(item['annual_spend'] for item in spend_data)
        weighted_score = 0

        for item in spend_data:
            supplier_id = item['supplier_id']
            spend = item['annual_spend']
            spend_weight = spend / total_spend if total_spend > 0 else 0

            # Find supplier assessment
            assessment = next((a for a in self.assessments if a['supplier_id'] == supplier_id), None)

            if assessment:
                supplier_score = assessment['overall_score']
            else:
                supplier_score = 50  # Default for not assessed

            weighted_score += supplier_score * spend_weight

        return {
            'sustainable_sourcing_score': round(weighted_score, 1),
            'total_spend': total_spend,
            'suppliers_assessed': len([a for a in self.assessments]),
            'rating': self._get_rating(weighted_score)
        }

    def identify_sourcing_priorities(self, spend_data, sustainability_goals):
        """
        Identify priority categories/suppliers for sustainable sourcing

        Using spend and impact analysis
        """

        priorities = []

        for item in spend_data:
            supplier_id = item['supplier_id']
            spend = item['annual_spend']
            category = item.get('category', 'Unknown')
            environmental_impact = item.get('environmental_impact_score', 50)  # 0-100
            social_risk = item.get('social_risk_score', 50)  # 0-100

            # Find current assessment
            assessment = next((a for a in self.assessments if a['supplier_id'] == supplier_id), None)
            current_score = assessment['overall_score'] if assessment else 50

            # Calculate priority score
            # High spend + High impact + Low current performance = High priority
            spend_factor = min(100, (spend / 1000000) * 20)  # $1M = 20 points, cap at 100
            impact_factor = (environmental_impact + social_risk) / 2
            gap_factor = 100 - current_score

            priority_score = (spend_factor * 0.4 + impact_factor * 0.35 + gap_factor * 0.25)

            priorities.append({
                'supplier_id': supplier_id,
                'category': category,
                'annual_spend': spend,
                'current_esg_score': current_score,
                'environmental_impact': environmental_impact,
                'social_risk': social_risk,
                'priority_score': round(priority_score, 1),
                'priority_level': 'High' if priority_score >= 70 else 'Medium' if priority_score >= 50 else 'Low'
            })

        df = pd.DataFrame(priorities)
        df = df.sort_values('priority_score', ascending=False)

        return df


# Example usage
sourcing_mgr = SustainableSourcingManager()

# Assess suppliers
supplier1_data = {
    'environmental': {
        'carbon_emissions': 65,      # Moderate emissions intensity
        'energy_management': 80,     # Good renewable energy use
        'water_management': 70,
        'waste_management': 75,
        'certifications': 90         # ISO 14001 certified
    },
    'social': {
        'labor_rights': 85,
        'health_safety': 88,
        'fair_compensation': 72,
        'diversity_inclusion': 68,
        'community_impact': 75
    },
    'governance': {
        'ethics_compliance': 82,
        'transparency': 78,
        'risk_management': 80,
        'business_continuity': 75,
        'data_security': 85
    }
}

assessment1 = sourcing_mgr.assess_supplier_esg('SUP001', 'GreenTech Manufacturing', supplier1_data)

print(f"Supplier: {assessment1['supplier_name']}")
print(f"Overall ESG Score: {assessment1['overall_score']}/100")
print(f"Rating: {assessment1['rating']}")
print(f"Environmental: {assessment1['dimension_scores']['environmental']}/100")
print(f"Social: {assessment1['dimension_scores']['social']}/100")
print(f"Governance: {assessment1['dimension_scores']['governance']}/100")
print(f"Strengths: {len(assessment1['strengths'])}")
print(f"Improvement Areas: {len(assessment1['improvement_areas'])}")
print(f"Red Flags: {len(assessment1['red_flags'])}")

# Assess another supplier with issues
supplier2_data = {
    'environmental': {
        'carbon_emissions': 35,      # High emissions
        'energy_management': 40,
        'water_management': 45,
        'waste_management': 38,
        'certifications': 20         # No certifications
    },
    'social': {
        'labor_rights': 52,
        'health_safety': 48,
        'fair_compensation': 55,
        'diversity_inclusion': 45,
        'community_impact': 40
    },
    'governance': {
        'ethics_compliance': 60,
        'transparency': 35,          # Poor transparency
        'risk_management': 50,
        'business_continuity': 45,
        'data_security': 55
    }
}

assessment2 = sourcing_mgr.assess_supplier_esg('SUP002', 'LowCost Industries', supplier2_data)

# Compare suppliers
comparison = sourcing_mgr.compare_suppliers()
print("\n\nSupplier ESG Comparison:")
print(comparison[['supplier_name', 'overall_score', 'rating', 'environmental', 'social', 'governance']])

# Calculate portfolio score
spend_data = [
    {'supplier_id': 'SUP001', 'annual_spend': 5000000},
    {'supplier_id': 'SUP002', 'annual_spend': 3000000}
]

portfolio_score = sourcing_mgr.calculate_sustainable_sourcing_score(spend_data)
print(f"\n\nSustainable Sourcing Portfolio Score: {portfolio_score['sustainable_sourcing_score']}/100")
print(f"Rating: {portfolio_score['rating']}")

# Identify priorities
spend_with_impact = [
    {'supplier_id': 'SUP001', 'annual_spend': 5000000, 'category': 'Electronics',
     'environmental_impact_score': 75, 'social_risk_score': 60},
    {'supplier_id': 'SUP002', 'annual_spend': 3000000, 'category': 'Plastics',
     'environmental_impact_score': 85, 'social_risk_score': 70}
]

priorities = sourcing_mgr.identify_sourcing_priorities(spend_with_impact, {})
print("\n\nSourcing Priorities:")
print(priorities[['supplier_id', 'category', 'annual_spend', 'current_esg_score', 'priority_level']])
```

---

## Sustainable Sourcing Decision Framework

### Total Cost of Ownership (TCO) with Sustainability

```python
class SustainableTCO:
    """Calculate Total Cost of Ownership including sustainability factors"""

    def calculate_tco(self, supplier_options):
        """
        Calculate TCO for supplier options including sustainability costs/benefits

        supplier_options: list of dicts with pricing and ESG data
        """

        tco_results = []

        for option in supplier_options:
            supplier_name = option['supplier_name']

            # Traditional cost components
            unit_price = option['unit_price']
            annual_volume = option['annual_volume']
            purchase_cost = unit_price * annual_volume

            quality_cost = option.get('quality_cost', 0)  # Defects, returns, rework
            logistics_cost = option.get('logistics_cost', 0)
            inventory_holding_cost = option.get('inventory_cost', 0)
            transaction_cost = option.get('transaction_cost', 0)

            traditional_tco = (purchase_cost + quality_cost + logistics_cost +
                             inventory_holding_cost + transaction_cost)

            # Sustainability-related costs/benefits
            carbon_cost = self._calculate_carbon_cost(option)
            compliance_risk_cost = self._calculate_compliance_risk(option)
            reputation_risk_cost = self._calculate_reputation_risk(option)
            innovation_benefit = self._calculate_innovation_benefit(option)

            sustainability_adjusted_cost = (carbon_cost + compliance_risk_cost +
                                           reputation_risk_cost - innovation_benefit)

            # Total TCO
            total_tco = traditional_tco + sustainability_adjusted_cost

            # Calculate per-unit TCO
            per_unit_tco = total_tco / annual_volume if annual_volume > 0 else 0

            tco_results.append({
                'supplier_name': supplier_name,
                'unit_price': unit_price,
                'traditional_tco': traditional_tco,
                'carbon_cost': carbon_cost,
                'compliance_risk_cost': compliance_risk_cost,
                'reputation_risk_cost': reputation_risk_cost,
                'innovation_benefit': innovation_benefit,
                'sustainability_adjustment': sustainability_adjusted_cost,
                'total_tco': total_tco,
                'per_unit_tco': round(per_unit_tco, 2),
                'esg_score': option.get('esg_score', 50)
            })

        df = pd.DataFrame(tco_results)
        df = df.sort_values('total_tco', ascending=True)

        return df

    def _calculate_carbon_cost(self, option):
        """Calculate cost of carbon emissions"""

        # Carbon intensity (kg CO2e per unit)
        carbon_intensity = option.get('carbon_intensity_kg_co2e', 10)
        annual_volume = option['annual_volume']

        total_emissions = carbon_intensity * annual_volume  # kg CO2e

        # Carbon price ($/tonne CO2e)
        # Use internal carbon price or regulatory price
        carbon_price = option.get('carbon_price_per_tonne', 50)

        carbon_cost = (total_emissions / 1000) * carbon_price  # Convert kg to tonnes

        return round(carbon_cost, 2)

    def _calculate_compliance_risk(self, option):
        """Calculate expected cost of compliance violations"""

        esg_score = option.get('esg_score', 50)

        # Lower ESG score = higher compliance risk
        # Estimate probability of violation
        violation_probability = (100 - esg_score) / 200  # 0-0.5 range

        # Average cost of compliance violation (fines, remediation, delays)
        avg_violation_cost = option.get('avg_violation_cost', 500000)

        expected_compliance_cost = violation_probability * avg_violation_cost

        return round(expected_compliance_cost, 2)

    def _calculate_reputation_risk(self, option):
        """Calculate cost of potential reputation damage"""

        esg_score = option.get('esg_score', 50)
        annual_volume = option['annual_volume']

        # Poor ESG performance increases reputation risk
        if esg_score < 40:  # High risk
            risk_probability = 0.15
            potential_revenue_loss = option.get('revenue_at_risk', 10000000)
        elif esg_score < 60:  # Medium risk
            risk_probability = 0.05
            potential_revenue_loss = option.get('revenue_at_risk', 5000000)
        else:  # Low risk
            risk_probability = 0.01
            potential_revenue_loss = option.get('revenue_at_risk', 1000000)

        expected_reputation_cost = risk_probability * potential_revenue_loss

        return round(expected_reputation_cost, 2)

    def _calculate_innovation_benefit(self, option):
        """Calculate benefit from supplier sustainability innovation"""

        esg_score = option.get('esg_score', 50)

        # High ESG performers tend to be more innovative
        if esg_score >= 80:
            # Innovation potential (cost savings, new products, efficiency)
            innovation_value = option.get('innovation_value', 200000)
        elif esg_score >= 65:
            innovation_value = option.get('innovation_value', 100000)
        else:
            innovation_value = 0

        return round(innovation_value, 2)


# Example TCO calculation
tco_calculator = SustainableTCO()

supplier_options = [
    {
        'supplier_name': 'GreenTech Manufacturing',
        'unit_price': 10.50,
        'annual_volume': 1000000,
        'quality_cost': 50000,
        'logistics_cost': 300000,
        'inventory_cost': 150000,
        'transaction_cost': 100000,
        'carbon_intensity_kg_co2e': 5.0,  # Low carbon
        'carbon_price_per_tonne': 50,
        'esg_score': 78,
        'avg_violation_cost': 500000,
        'revenue_at_risk': 10000000,
        'innovation_value': 150000
    },
    {
        'supplier_name': 'LowCost Industries',
        'unit_price': 9.80,  # Lower price
        'annual_volume': 1000000,
        'quality_cost': 120000,  # Higher quality issues
        'logistics_cost': 350000,
        'inventory_cost': 180000,
        'transaction_cost': 120000,
        'carbon_intensity_kg_co2e': 15.0,  # High carbon
        'carbon_price_per_tonne': 50,
        'esg_score': 42,  # Poor ESG
        'avg_violation_cost': 500000,
        'revenue_at_risk': 10000000,
        'innovation_value': 0
    },
    {
        'supplier_name': 'MidRange Solutions',
        'unit_price': 10.20,
        'annual_volume': 1000000,
        'quality_cost': 75000,
        'logistics_cost': 320000,
        'inventory_cost': 160000,
        'transaction_cost': 105000,
        'carbon_intensity_kg_co2e': 8.0,
        'carbon_price_per_tonne': 50,
        'esg_score': 62,
        'avg_violation_cost': 500000,
        'revenue_at_risk': 10000000,
        'innovation_value': 50000
    }
]

tco_results = tco_calculator.calculate_tco(supplier_options)

print("Sustainable TCO Analysis:")
print(tco_results[['supplier_name', 'unit_price', 'traditional_tco', 'sustainability_adjustment', 'total_tco', 'esg_score']])
print(f"\n\nLowest TCO: {tco_results.iloc[0]['supplier_name']}")
print(f"Total TCO: ${tco_results.iloc[0]['total_tco']:,.2f}")
```

---

## Tools & Libraries

### Python Libraries

**Sustainability Assessment:**
- `pandas`: Data analysis
- `numpy`: Numerical computations
- `scikit-learn`: Predictive modeling

**Life Cycle Assessment:**
- `brightway2`: LCA framework
- `openLCA`: Open-source LCA

**Data Collection:**
- `requests`: API integration
- `beautifulsoup4`: Web scraping
- `selenium`: Automated data collection

**Visualization:**
- `matplotlib`, `seaborn`: Charts
- `plotly`: Interactive dashboards

### Commercial Software

**Supplier Sustainability:**
- **EcoVadis**: Supplier sustainability ratings
- **Sedex**: Supply chain ethics platform
- **IntegrityNext**: Supplier sustainability management
- **Assent Compliance**: Supply chain ESG data
- **Sourcemap**: Supply chain transparency

**ESG Platforms:**
- **Sustainalytics**: ESG research and ratings
- **MSCI ESG Research**: ESG ratings
- **Refinitiv**: ESG data
- **Bloomberg ESG**: ESG data and analytics

**Procurement Platforms:**
- **SAP Ariba**: Sustainable procurement
- **Coupa**: Supplier sustainability
- **Ivalua**: Responsible sourcing
- **Jaggaer**: Sustainable procurement

**Carbon & LCA:**
- **Watershed**: Carbon management
- **Persefoni**: Carbon accounting
- **SimaPro**: LCA software
- **GaBi**: Life cycle assessment

---

## Common Challenges & Solutions

### Challenge: Supplier Data Collection

**Problem:**
- Suppliers reluctant to share ESG data
- Inconsistent data quality
- Small suppliers lack resources

**Solutions:**
- Tiered approach (simple questionnaire to detailed audit)
- Industry collaboration (shared assessments)
- Third-party platforms (EcoVadis, Sedex)
- Incentives for participation
- Supplier capacity building programs
- Technology solutions (automated data collection)

### Challenge: Balancing Cost and Sustainability

**Problem:**
- Sustainable options often more expensive
- Short-term cost pressure
- Difficult to quantify benefits

**Solutions:**
- Total Cost of Ownership (TCO) analysis
- Quantify risk costs (compliance, reputation)
- Long-term value vs. short-term cost
- Innovation partnerships for cost reduction
- Volume commitments for better pricing
- Executive commitment to sustainability

### Challenge: Measuring Impact

**Problem:**
- Hard to attribute improvements to sourcing
- Scope 3 emissions estimation challenges
- Multiple variables affecting outcomes

**Solutions:**
- Baseline measurement before initiatives
- Supplier-specific metrics and targets
- Regular progress tracking
- Use primary data where possible
- Industry benchmarks for comparison
- Third-party verification

### Challenge: Supplier Capability Gaps

**Problem:**
- Suppliers lack ESG expertise
- Limited resources for improvement
- Resistance to change

**Solutions:**
- Supplier development programs
- Training and capacity building
- Collaborative improvement projects
- Longer-term contracts for investment security
- Shared investment in improvements
- Recognition and rewards for leaders

### Challenge: Greenwashing

**Problem:**
- Suppliers exaggerate sustainability claims
- Lack of verification
- Misleading certifications

**Solutions:**
- Third-party verification and audits
- Site visits and inspections
- Multiple data sources and validation
- Credible certification schemes
- Supplier transparency requirements
- Consequences for false claims

### Challenge: Complexity and Resources

**Problem:**
- Overwhelming scope (many suppliers, criteria)
- Limited resources for assessment
- Competing priorities

**Solutions:**
- Risk-based prioritization (high spend, high impact)
- Phased implementation by category
- Leverage existing assessments and platforms
- Cross-functional teams
- Technology and automation
- Industry collaboration

---

## Output Format

### Sustainable Sourcing Report

**Executive Summary:**
- Sustainable sourcing score
- Progress toward goals
- Key achievements and challenges
- Investment and ROI

**Supplier ESG Performance:**

| Supplier | Spend | ESG Score | E | S | G | Rating | Change | Red Flags |
|----------|-------|-----------|---|---|---|--------|--------|-----------|
| GreenTech | $5.0M | 78 | 82 | 76 | 75 | B+ | ↗ +5 | None |
| MidRange | $3.5M | 62 | 65 | 58 | 64 | C+ | → 0 | None |
| LowCost | $2.8M | 42 | 38 | 45 | 44 | D | ↘ -3 | 2 |

**Category Performance:**

| Category | Spend | Avg ESG Score | Suppliers Assessed | Target | Status |
|----------|-------|---------------|-------------------|--------|--------|
| Electronics | $15M | 68 | 12/15 | 70 | ⚠ Below |
| Plastics | $8M | 58 | 8/10 | 65 | ⚠ Below |
| Metals | $12M | 72 | 10/10 | 70 | ✓ On Track |

**Sustainable Sourcing KPIs:**

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Sustainable Sourcing Score | 64/100 | 70/100 | 86% to goal |
| % Spend with A/B Rated Suppliers | 58% | 75% | Behind |
| Supplier ESG Assessment Coverage | 75% | 90% | On Track |
| Suppliers with Improvement Plans | 18 | 25 | Behind |
| Carbon Intensity Reduction | -12% | -20% | On Track |

**Improvement Initiatives:**

| Initiative | Suppliers | Investment | Expected Impact | Timeline | Status |
|-----------|-----------|------------|-----------------|----------|--------|
| Renewable Energy Program | 8 | $500K | -5,000 tCO2e | 2026 | In Progress |
| Waste Reduction Partnership | 5 | $200K | 30% waste reduction | 2026 | Planning |
| Fair Wage Assessment | 12 | $150K | Wage gaps identified | Q1 2026 | Starting |
| Supplier Training Program | 20 | $300K | Knowledge building | Ongoing | Active |

---

## Questions to Ask

If you need more context:
1. What are your organization's sustainability goals?
2. What categories or suppliers should be prioritized?
3. Is there existing supplier sustainability data?
4. What sustainability criteria are most important? (carbon, labor, water, etc.)
5. Are there customer or investor ESG requirements?
6. What's the budget for sustainable sourcing programs?
7. How is sustainability currently factored into sourcing decisions?
8. Are there industry sustainability benchmarks to follow?
9. What supplier engagement and development resources exist?
10. How will success be measured?

---

## Related Skills

- **carbon-footprint-tracking**: For measuring Scope 3 supplier emissions
- **circular-economy**: For circular sourcing and material recovery
- **compliance-management**: For regulatory sustainability requirements
- **supplier-selection**: For integrating ESG in supplier evaluation
- **supplier-risk-management**: For ESG-related supplier risks
- **procurement-optimization**: For balancing cost and sustainability
- **contract-management**: For sustainability terms in contracts
- **spend-analysis**: For sustainability spend analytics
