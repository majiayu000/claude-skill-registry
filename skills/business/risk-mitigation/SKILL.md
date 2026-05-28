---
name: risk-mitigation
description: When the user wants to identify and mitigate supply chain risks, build resilience, or develop business continuity plans. Also use when the user mentions "supply chain risk," "disruption management," "resilience," "risk assessment," "business continuity," "scenario planning," "supply chain vulnerability," "risk modeling," or "crisis management." For supplier-specific risks, see supplier-risk-management. For compliance risks, see compliance-management.
---

# Risk Mitigation

You are an expert in supply chain risk management and resilience. Your goal is to help organizations identify, assess, quantify, and mitigate risks across their supply chain while building adaptive capacity to respond to disruptions.

## Initial Assessment

Before developing risk mitigation strategies, understand:

1. **Risk Context**
   - What recent disruptions have occurred?
   - Industry-specific risk exposure?
   - Geographic risk concentration?
   - Current risk management maturity?

2. **Supply Chain Complexity**
   - Number of tiers in supply chain?
   - Global vs. regional footprint?
   - Single-source dependencies?
   - Lead time lengths and variability?

3. **Business Impact Tolerance**
   - Maximum acceptable downtime?
   - Revenue at risk from disruptions?
   - Customer SLA penalties?
   - Brand reputation concerns?

4. **Existing Capabilities**
   - Current risk monitoring processes?
   - Business continuity plans in place?
   - Inventory buffers maintained?
   - Flexibility in production/logistics?

---

## Risk Management Framework

### Risk Categories

**1. Supply Risks**
- Supplier failure or bankruptcy
- Quality issues and recalls
- Capacity constraints
- Raw material shortages
- Single-source dependencies
- Supplier concentration

**2. Demand Risks**
- Demand volatility
- Forecast inaccuracy
- New product uncertainty
- Market shifts
- Customer concentration
- Bullwhip effect

**3. Operational Risks**
- Production disruptions
- Equipment failures
- Quality defects
- IT system outages
- Labor strikes
- Process breakdowns

**4. Logistics Risks**
- Transportation delays
- Port congestion
- Carrier failures
- Customs issues
- Last-mile challenges
- Warehouse disruptions

**5. External Risks**
- Natural disasters (hurricanes, earthquakes, floods)
- Pandemics and health crises
- Geopolitical events (wars, sanctions)
- Cyberattacks
- Terrorism
- Climate change impacts

**6. Financial Risks**
- Currency fluctuations
- Commodity price volatility
- Credit risks
- Payment delays
- Economic recessions
- Inflation

**7. Regulatory & Compliance Risks**
- Regulatory changes
- Trade restrictions
- Tariffs and duties
- Environmental regulations
- Product safety standards
- Data privacy laws

---

## Risk Assessment Methodology

### Quantitative Risk Modeling

```python
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

class SupplyChainRiskAssessment:
    """Comprehensive supply chain risk assessment framework"""

    def __init__(self):
        self.risk_register = []

    def add_risk(self, risk_id, risk_name, category, probability,
                impact_revenue, impact_days, current_controls,
                residual_probability=None):
        """
        Add risk to risk register

        probability: likelihood (0-1)
        impact_revenue: financial impact ($)
        impact_days: operational impact (days of disruption)
        """

        # If residual probability not provided, assume controls reduce by 30%
        if residual_probability is None:
            residual_probability = probability * 0.7

        # Calculate risk scores
        inherent_risk_score = probability * impact_revenue
        residual_risk_score = residual_probability * impact_revenue

        # Risk level classification
        def classify_risk(score):
            if score > 1000000:
                return 'Critical'
            elif score > 500000:
                return 'High'
            elif score > 100000:
                return 'Medium'
            else:
                return 'Low'

        self.risk_register.append({
            'risk_id': risk_id,
            'risk_name': risk_name,
            'category': category,
            'inherent_probability': probability,
            'residual_probability': residual_probability,
            'impact_revenue': impact_revenue,
            'impact_days': impact_days,
            'inherent_risk_score': inherent_risk_score,
            'residual_risk_score': residual_risk_score,
            'inherent_risk_level': classify_risk(inherent_risk_score),
            'residual_risk_level': classify_risk(residual_risk_score),
            'current_controls': current_controls,
            'risk_reduction': inherent_risk_score - residual_risk_score
        })

    def calculate_value_at_risk(self, confidence_level=0.95):
        """
        Calculate Value at Risk (VaR) for supply chain

        VaR = maximum expected loss at given confidence level
        """

        df = pd.DataFrame(self.risk_register)

        if len(df) == 0:
            return None

        # Monte Carlo simulation of risk events
        n_simulations = 10000
        simulation_results = []

        for _ in range(n_simulations):
            total_loss = 0

            for _, risk in df.iterrows():
                # Simulate if risk occurs
                if np.random.random() < risk['residual_probability']:
                    # Loss if risk occurs (with some variability)
                    loss = np.random.normal(
                        risk['impact_revenue'],
                        risk['impact_revenue'] * 0.2  # 20% std dev
                    )
                    total_loss += abs(loss)

            simulation_results.append(total_loss)

        simulation_results = np.array(simulation_results)

        # Calculate VaR
        var = np.percentile(simulation_results, confidence_level * 100)

        # Calculate CVaR (Conditional VaR - expected loss beyond VaR)
        cvar = simulation_results[simulation_results >= var].mean()

        # Expected annual loss
        expected_loss = simulation_results.mean()

        return {
            'value_at_risk': round(var, 2),
            'conditional_var': round(cvar, 2),
            'expected_annual_loss': round(expected_loss, 2),
            'confidence_level': confidence_level,
            'max_simulated_loss': round(simulation_results.max(), 2),
            'simulations': n_simulations
        }

    def prioritize_risks(self):
        """Generate prioritized risk register"""

        df = pd.DataFrame(self.risk_register)

        if len(df) == 0:
            return df

        # Sort by residual risk score descending
        df = df.sort_values('residual_risk_score', ascending=False)

        # Add ranking
        df['priority_rank'] = range(1, len(df) + 1)

        return df

    def identify_mitigation_priorities(self, budget_limit=None):
        """
        Identify which risks to prioritize for mitigation investment

        Uses cost-benefit approach
        """

        df = self.prioritize_risks()

        # Calculate mitigation value (risk reduction potential)
        df['mitigation_value'] = df['inherent_risk_score'] - df['residual_risk_score']

        # Estimate mitigation cost (simplified: 10% of impact)
        df['estimated_mitigation_cost'] = df['impact_revenue'] * 0.10

        # ROI of mitigation
        df['mitigation_roi'] = df['mitigation_value'] / df['estimated_mitigation_cost']

        # Sort by ROI descending
        df = df.sort_values('mitigation_roi', ascending=False)

        if budget_limit:
            # Select risks within budget
            df['cumulative_cost'] = df['estimated_mitigation_cost'].cumsum()
            df['within_budget'] = df['cumulative_cost'] <= budget_limit
        else:
            df['within_budget'] = True

        return df

    def calculate_supply_chain_resilience_index(self, resilience_factors):
        """
        Calculate Supply Chain Resilience Index

        resilience_factors: dict with various resilience metrics
        """

        # Resilience dimensions (0-100 scale)
        flexibility = resilience_factors.get('flexibility', 50)
        redundancy = resilience_factors.get('redundancy', 50)
        visibility = resilience_factors.get('visibility', 50)
        collaboration = resilience_factors.get('collaboration', 50)
        agility = resilience_factors.get('agility', 50)
        robustness = resilience_factors.get('robustness', 50)

        # Weighted average
        weights = {
            'flexibility': 0.20,
            'redundancy': 0.20,
            'visibility': 0.15,
            'collaboration': 0.15,
            'agility': 0.15,
            'robustness': 0.15
        }

        resilience_index = (
            flexibility * weights['flexibility'] +
            redundancy * weights['redundancy'] +
            visibility * weights['visibility'] +
            collaboration * weights['collaboration'] +
            agility * weights['agility'] +
            robustness * weights['robustness']
        )

        # Classify resilience level
        if resilience_index >= 80:
            level = 'Highly Resilient'
        elif resilience_index >= 65:
            level = 'Resilient'
        elif resilience_index >= 50:
            level = 'Moderately Resilient'
        elif resilience_index >= 35:
            level = 'Vulnerable'
        else:
            level = 'Highly Vulnerable'

        return {
            'resilience_index': round(resilience_index, 1),
            'resilience_level': level,
            'dimension_scores': {
                'flexibility': flexibility,
                'redundancy': redundancy,
                'visibility': visibility,
                'collaboration': collaboration,
                'agility': agility,
                'robustness': robustness
            }
        }


# Example usage
risk_assessment = SupplyChainRiskAssessment()

# Add various risks
risk_assessment.add_risk(
    risk_id='R001',
    risk_name='Single-source supplier failure',
    category='Supply',
    probability=0.15,
    impact_revenue=2000000,
    impact_days=90,
    current_controls='Quarterly reviews, financial monitoring',
    residual_probability=0.10
)

risk_assessment.add_risk(
    risk_id='R002',
    risk_name='Port congestion (West Coast)',
    category='Logistics',
    probability=0.25,
    impact_revenue=500000,
    impact_days=30,
    current_controls='Dual port strategy, air freight backup',
    residual_probability=0.15
)

risk_assessment.add_risk(
    risk_id='R003',
    risk_name='Demand forecast error (new product)',
    category='Demand',
    probability=0.40,
    impact_revenue=800000,
    impact_days=60,
    current_controls='Market research, test markets',
    residual_probability=0.30
)

risk_assessment.add_risk(
    risk_id='R004',
    risk_name='Cyberattack on systems',
    category='External',
    probability=0.20,
    impact_revenue=3000000,
    impact_days=45,
    current_controls='Firewalls, backups, monitoring',
    residual_probability=0.12
)

risk_assessment.add_risk(
    risk_id='R005',
    risk_name='Natural disaster (supplier location)',
    category='External',
    probability=0.10,
    impact_revenue=1500000,
    impact_days=120,
    current_controls='Insurance, geographic diversification',
    residual_probability=0.08
)

# Prioritize risks
risk_register = risk_assessment.prioritize_risks()
print("Risk Register (Prioritized):")
print(risk_register[['risk_id', 'risk_name', 'residual_risk_level', 'residual_risk_score']])

# Calculate Value at Risk
var_result = risk_assessment.calculate_value_at_risk(confidence_level=0.95)
print(f"\n\nValue at Risk (95% confidence): ${var_result['value_at_risk']:,.2f}")
print(f"Expected Annual Loss: ${var_result['expected_annual_loss']:,.2f}")
print(f"Conditional VaR: ${var_result['conditional_var']:,.2f}")

# Mitigation priorities
mitigation_priorities = risk_assessment.identify_mitigation_priorities(budget_limit=500000)
print("\n\nMitigation Priorities:")
print(mitigation_priorities[['risk_id', 'risk_name', 'mitigation_roi', 'estimated_mitigation_cost', 'within_budget']])

# Calculate resilience index
resilience_factors = {
    'flexibility': 65,      # Supply/production flexibility
    'redundancy': 55,       # Backup suppliers, inventory
    'visibility': 70,       # End-to-end visibility
    'collaboration': 60,    # Partner collaboration
    'agility': 58,          # Speed of response
    'robustness': 62        # Ability to withstand shocks
}

resilience = risk_assessment.calculate_supply_chain_resilience_index(resilience_factors)
print(f"\n\nSupply Chain Resilience Index: {resilience['resilience_index']}/100")
print(f"Resilience Level: {resilience['resilience_level']}")
```

---

## Scenario Planning & Stress Testing

### Disruption Scenario Modeling

```python
class ScenarioPlanner:
    """Model and analyze supply chain disruption scenarios"""

    def __init__(self, baseline_data):
        self.baseline = baseline_data
        self.scenarios = []

    def add_scenario(self, scenario_name, probability, disruption_impacts):
        """
        Add disruption scenario

        disruption_impacts: dict with impact parameters
        """

        # Calculate scenario impact
        revenue_impact = disruption_impacts.get('revenue_loss', 0)
        cost_impact = disruption_impacts.get('additional_costs', 0)
        duration_days = disruption_impacts.get('duration_days', 0)

        total_impact = revenue_impact + cost_impact

        # Calculate expected value (probability-weighted)
        expected_impact = total_impact * probability

        # Recovery time
        recovery_days = disruption_impacts.get('recovery_days', duration_days * 1.5)

        self.scenarios.append({
            'scenario': scenario_name,
            'probability': probability,
            'revenue_loss': revenue_impact,
            'additional_costs': cost_impact,
            'total_impact': total_impact,
            'expected_impact': expected_impact,
            'duration_days': duration_days,
            'recovery_days': recovery_days,
            'affected_revenue_pct': (revenue_impact / self.baseline['annual_revenue'] * 100)
        })

    def stress_test(self, scenario_name):
        """
        Perform stress test for specific scenario

        Models cascade effects and secondary impacts
        """

        scenario = next((s for s in self.scenarios if s['scenario'] == scenario_name), None)

        if not scenario:
            return None

        # Calculate cascade effects
        primary_impact = scenario['total_impact']

        # Secondary impacts (simplified model)
        # 1. Customer penalties for late delivery
        late_delivery_penalty = primary_impact * 0.15

        # 2. Inventory carrying costs (if building buffer)
        additional_inventory_cost = primary_impact * 0.08

        # 3. Expediting costs (air freight, overtime)
        expediting_cost = primary_impact * 0.20

        # 4. Lost customer goodwill (long-term revenue impact)
        customer_attrition_impact = primary_impact * 0.25

        # Total impact with cascades
        total_with_cascade = (
            primary_impact +
            late_delivery_penalty +
            additional_inventory_cost +
            expediting_cost +
            customer_attrition_impact
        )

        return {
            'scenario': scenario_name,
            'primary_impact': round(primary_impact, 2),
            'secondary_impacts': {
                'late_delivery_penalties': round(late_delivery_penalty, 2),
                'inventory_costs': round(additional_inventory_cost, 2),
                'expediting_costs': round(expediting_cost, 2),
                'customer_attrition': round(customer_attrition_impact, 2)
            },
            'total_impact_with_cascade': round(total_with_cascade, 2),
            'cascade_multiplier': round(total_with_cascade / primary_impact, 2)
        }

    def compare_scenarios(self):
        """Compare all scenarios"""

        df = pd.DataFrame(self.scenarios)

        if len(df) == 0:
            return df

        # Sort by expected impact descending
        df = df.sort_values('expected_impact', ascending=False)

        return df

    def monte_carlo_portfolio_risk(self, n_simulations=10000):
        """
        Monte Carlo simulation of portfolio risk

        Simulates multiple disruptions occurring in same year
        """

        results = []

        for _ in range(n_simulations):
            annual_impact = 0

            for scenario in self.scenarios:
                # Check if this scenario occurs
                if np.random.random() < scenario['probability']:
                    # Add impact with variability
                    impact = np.random.normal(
                        scenario['total_impact'],
                        scenario['total_impact'] * 0.25  # 25% std dev
                    )
                    annual_impact += abs(impact)

            results.append(annual_impact)

        results = np.array(results)

        # Calculate statistics
        var_95 = np.percentile(results, 95)
        var_99 = np.percentile(results, 99)
        expected_loss = results.mean()
        max_loss = results.max()

        return {
            'expected_annual_loss': round(expected_loss, 2),
            'var_95': round(var_95, 2),
            'var_99': round(var_99, 2),
            'maximum_simulated_loss': round(max_loss, 2),
            'probability_zero_loss': round((results == 0).sum() / n_simulations * 100, 1),
            'probability_major_loss': round((results > self.baseline['annual_revenue'] * 0.05).sum() / n_simulations * 100, 1)
        }


# Example scenario planning
baseline = {
    'annual_revenue': 100000000,
    'operating_margin': 0.15,
    'inventory_value': 15000000
}

planner = ScenarioPlanner(baseline)

# Add scenarios
planner.add_scenario(
    'Major supplier failure',
    probability=0.10,
    disruption_impacts={
        'revenue_loss': 5000000,
        'additional_costs': 1000000,
        'duration_days': 90,
        'recovery_days': 120
    }
)

planner.add_scenario(
    'Pandemic (COVID-like)',
    probability=0.05,
    disruption_impacts={
        'revenue_loss': 15000000,
        'additional_costs': 3000000,
        'duration_days': 180,
        'recovery_days': 365
    }
)

planner.add_scenario(
    'Regional natural disaster',
    probability=0.15,
    disruption_impacts={
        'revenue_loss': 3000000,
        'additional_costs': 800000,
        'duration_days': 60,
        'recovery_days': 90
    }
)

planner.add_scenario(
    'Geopolitical crisis (trade restrictions)',
    probability=0.20,
    disruption_impacts={
        'revenue_loss': 8000000,
        'additional_costs': 2000000,
        'duration_days': 120,
        'recovery_days': 180
    }
)

planner.add_scenario(
    'Cyberattack (ransomware)',
    probability=0.12,
    disruption_impacts={
        'revenue_loss': 4000000,
        'additional_costs': 1500000,
        'duration_days': 30,
        'recovery_days': 45
    }
)

# Compare scenarios
comparison = planner.compare_scenarios()
print("Scenario Comparison:")
print(comparison[['scenario', 'probability', 'total_impact', 'expected_impact', 'duration_days']])

# Stress test specific scenario
stress_result = planner.stress_test('Pandemic (COVID-like)')
print(f"\n\nStress Test: Pandemic Scenario")
print(f"Primary Impact: ${stress_result['primary_impact']:,.2f}")
print(f"Total with Cascade: ${stress_result['total_impact_with_cascade']:,.2f}")
print(f"Cascade Multiplier: {stress_result['cascade_multiplier']}x")

# Monte Carlo simulation
mc_results = planner.monte_carlo_portfolio_risk(n_simulations=10000)
print(f"\n\nMonte Carlo Risk Analysis:")
print(f"Expected Annual Loss: ${mc_results['expected_annual_loss']:,.2f}")
print(f"Value at Risk (95%): ${mc_results['var_95']:,.2f}")
print(f"Value at Risk (99%): ${mc_results['var_99']:,.2f}")
print(f"Probability of Major Loss (>5% revenue): {mc_results['probability_major_loss']}%")
```

---

## Mitigation Strategies

### Risk Response Framework

**1. Avoidance**
- Eliminate the risk source
- Exit risky markets or suppliers
- Change product design to avoid dependencies

**2. Reduction**
- Implement controls to reduce likelihood or impact
- Dual sourcing, safety stock, process improvements
- Most common strategy

**3. Transfer**
- Shift risk to another party
- Insurance, contracts with penalties, outsourcing
- Cost of transfer must be justified

**4. Acceptance**
- Consciously accept the risk
- Low-probability, low-impact risks
- Have contingency plans ready

### Resilience Building Strategies

```python
class ResilienceBuilder:
    """Build supply chain resilience through strategic interventions"""

    def __init__(self, current_state):
        self.current_state = current_state
        self.interventions = []

    def evaluate_dual_sourcing(self, primary_supplier, backup_supplier, demand):
        """
        Evaluate dual sourcing strategy

        Compares cost vs. resilience benefit
        """

        # Single source scenario
        single_source_cost = demand * primary_supplier['unit_cost']

        # Risk of disruption
        disruption_probability = primary_supplier['disruption_probability']
        disruption_cost = primary_supplier['disruption_cost']

        single_source_expected_cost = single_source_cost + (disruption_probability * disruption_cost)

        # Dual source scenario (60/40 split)
        primary_volume = demand * 0.6
        backup_volume = demand * 0.4

        dual_source_cost = (
            primary_volume * primary_supplier['unit_cost'] +
            backup_volume * backup_supplier['unit_cost']
        )

        # Reduced disruption risk (assume 70% reduction)
        reduced_disruption_prob = disruption_probability * 0.3
        dual_source_expected_cost = dual_source_cost + (reduced_disruption_prob * disruption_cost)

        # Analysis
        additional_cost = dual_source_cost - single_source_cost
        risk_reduction = single_source_expected_cost - dual_source_expected_cost

        return {
            'single_source_cost': round(single_source_cost, 2),
            'single_source_expected_cost': round(single_source_expected_cost, 2),
            'dual_source_cost': round(dual_source_cost, 2),
            'dual_source_expected_cost': round(dual_source_expected_cost, 2),
            'additional_cost': round(additional_cost, 2),
            'risk_reduction': round(risk_reduction, 2),
            'net_benefit': round(risk_reduction - additional_cost, 2),
            'recommendation': 'Implement dual sourcing' if risk_reduction > additional_cost else 'Maintain single source'
        }

    def evaluate_safety_stock(self, demand_data, lead_time_data, target_service_level=0.95):
        """
        Evaluate optimal safety stock for risk mitigation

        Balances inventory cost vs. stockout risk
        """

        # Demand parameters
        avg_daily_demand = demand_data['avg_daily_demand']
        demand_std = demand_data['demand_std']

        # Lead time parameters
        avg_lead_time = lead_time_data['avg_lead_time_days']
        lead_time_std = lead_time_data['lead_time_std_days']

        # Safety stock calculation
        z_score = stats.norm.ppf(target_service_level)

        # Combined variability
        variance_during_lt = (
            avg_lead_time * demand_std**2 +
            avg_daily_demand**2 * lead_time_std**2
        )
        std_during_lt = np.sqrt(variance_during_lt)

        safety_stock = z_score * std_during_lt

        # Cost analysis
        unit_cost = demand_data['unit_cost']
        holding_cost_rate = 0.25  # 25% annual holding cost

        annual_holding_cost = safety_stock * unit_cost * holding_cost_rate

        # Stockout cost avoided
        stockout_probability_without_ss = 0.50  # 50% chance without safety stock
        stockout_probability_with_ss = 1 - target_service_level

        stockout_cost_per_event = demand_data['stockout_cost_per_event']
        stockouts_per_year = 365 / avg_lead_time  # Number of replenishment cycles

        stockout_cost_avoided = (
            (stockout_probability_without_ss - stockout_probability_with_ss) *
            stockouts_per_year *
            stockout_cost_per_event
        )

        net_benefit = stockout_cost_avoided - annual_holding_cost

        return {
            'safety_stock_units': round(safety_stock, 0),
            'safety_stock_value': round(safety_stock * unit_cost, 2),
            'annual_holding_cost': round(annual_holding_cost, 2),
            'stockout_cost_avoided': round(stockout_cost_avoided, 2),
            'net_annual_benefit': round(net_benefit, 2),
            'days_of_supply': round(safety_stock / avg_daily_demand, 1),
            'service_level_achieved': target_service_level
        }

    def evaluate_nearshoring(self, offshore_option, nearshore_option, demand):
        """
        Evaluate nearshoring to reduce supply chain risk

        Compare offshore vs. nearshore sourcing
        """

        # Offshore scenario
        offshore_cost = demand * offshore_option['unit_cost']
        offshore_lead_time = offshore_option['lead_time_days']
        offshore_disruption_risk = offshore_option['disruption_probability']
        offshore_disruption_cost = offshore_option['disruption_cost']

        offshore_total_cost = offshore_cost + (offshore_disruption_risk * offshore_disruption_cost)

        # Nearshore scenario
        nearshore_cost = demand * nearshore_option['unit_cost']
        nearshore_lead_time = nearshore_option['lead_time_days']
        nearshore_disruption_risk = nearshore_option['disruption_probability']
        nearshore_disruption_cost = nearshore_option['disruption_cost']

        nearshore_total_cost = nearshore_cost + (nearshore_disruption_risk * nearshore_disruption_cost)

        # Benefits
        lead_time_reduction = offshore_lead_time - nearshore_lead_time
        inventory_reduction = lead_time_reduction * (demand / 365) * nearshore_option['unit_cost'] * 0.25

        risk_reduction = (
            (offshore_disruption_risk * offshore_disruption_cost) -
            (nearshore_disruption_risk * nearshore_disruption_cost)
        )

        # Incremental cost
        incremental_cost = nearshore_cost - offshore_cost

        # Net benefit
        total_benefit = risk_reduction + inventory_reduction
        net_benefit = total_benefit - incremental_cost

        return {
            'offshore_total_cost': round(offshore_total_cost, 2),
            'nearshore_total_cost': round(nearshore_total_cost, 2),
            'incremental_cost': round(incremental_cost, 2),
            'lead_time_reduction_days': lead_time_reduction,
            'risk_reduction_value': round(risk_reduction, 2),
            'inventory_reduction_value': round(inventory_reduction, 2),
            'total_benefit': round(total_benefit, 2),
            'net_benefit': round(net_benefit, 2),
            'payback_period_years': round(abs(incremental_cost / total_benefit), 2) if total_benefit > 0 else float('inf'),
            'recommendation': 'Nearshore' if net_benefit > 0 else 'Remain offshore'
        }


# Example resilience building
current_state = {
    'annual_revenue': 50000000,
    'supply_chain_cost': 30000000
}

resilience_builder = ResilienceBuilder(current_state)

# Evaluate dual sourcing
primary = {
    'unit_cost': 10.00,
    'disruption_probability': 0.15,
    'disruption_cost': 2000000
}

backup = {
    'unit_cost': 10.80,  # 8% premium
    'disruption_probability': 0.05,
    'disruption_cost': 500000
}

dual_sourcing_result = resilience_builder.evaluate_dual_sourcing(
    primary, backup, demand=1000000
)

print("Dual Sourcing Analysis:")
print(f"  Additional Cost: ${dual_sourcing_result['additional_cost']:,.2f}")
print(f"  Risk Reduction: ${dual_sourcing_result['risk_reduction']:,.2f}")
print(f"  Net Benefit: ${dual_sourcing_result['net_benefit']:,.2f}")
print(f"  Recommendation: {dual_sourcing_result['recommendation']}")

# Evaluate safety stock
demand_data = {
    'avg_daily_demand': 100,
    'demand_std': 25,
    'unit_cost': 50,
    'stockout_cost_per_event': 10000
}

lead_time_data = {
    'avg_lead_time_days': 30,
    'lead_time_std_days': 7
}

safety_stock_result = resilience_builder.evaluate_safety_stock(
    demand_data, lead_time_data, target_service_level=0.95
)

print(f"\n\nSafety Stock Analysis:")
print(f"  Safety Stock: {safety_stock_result['safety_stock_units']} units ({safety_stock_result['days_of_supply']} days)")
print(f"  Annual Holding Cost: ${safety_stock_result['annual_holding_cost']:,.2f}")
print(f"  Stockout Cost Avoided: ${safety_stock_result['stockout_cost_avoided']:,.2f}")
print(f"  Net Annual Benefit: ${safety_stock_result['net_annual_benefit']:,.2f}")
```

---

## Tools & Libraries

### Python Libraries

**Risk Analysis:**
- `pandas`: Data manipulation
- `numpy`: Numerical computations
- `scipy`: Statistical analysis and distributions
- `scikit-learn`: Predictive risk modeling

**Simulation:**
- `simpy`: Discrete event simulation
- `mesa`: Agent-based modeling
- `pymc3`: Probabilistic programming

**Optimization:**
- `pulp`: Linear programming
- `pyomo`: Optimization modeling
- `scipy.optimize`: Numerical optimization

**Visualization:**
- `matplotlib`, `seaborn`: Risk charts
- `plotly`: Interactive dashboards
- `networkx`: Supply chain network analysis

### Commercial Software

**Risk Management Platforms:**
- **Resilinc**: Supply chain risk intelligence
- **Everstream Analytics**: AI-powered risk prediction
- **Interos**: Supply chain resilience
- **Exiger**: Third-party risk management
- **Riskpulse**: Weather and logistics risk

**Business Continuity:**
- **Fusion Framework**: Risk and resilience management
- **LogicManager**: Integrated risk management
- **Resolver**: Risk and incident management
- **Quantivate**: Risk and compliance

**Supply Chain Planning:**
- **Kinaxis RapidResponse**: Scenario planning and what-if analysis
- **o9 Solutions**: Digital planning with risk analytics
- **Blue Yonder**: Supply chain visibility and risk
- **SAP IBP**: Integrated business planning with risk

**Analytics & Simulation:**
- **LLamasoft (Coupa)**: Supply chain design and risk modeling
- **Anylogistix**: Supply chain simulation
- **Arena**: Discrete event simulation
- **@RISK**: Monte Carlo simulation add-in

---

## Common Challenges & Solutions

### Challenge: Risk Identification Blind Spots

**Problem:**
- Unknown or underestimated risks
- Lack of visibility beyond Tier 1
- Emerging risks not on radar

**Solutions:**
- Regular risk workshops with cross-functional teams
- External risk intelligence services
- Supplier audits and site visits
- Industry benchmarking and peer learning
- Horizon scanning for emerging threats
- N-tier supply chain mapping

### Challenge: Quantifying Low-Probability, High-Impact Events

**Problem:**
- Limited historical data
- Difficulty estimating probabilities
- Extreme events ("black swans")

**Solutions:**
- Use scenario planning instead of pure probability
- Stress testing and sensitivity analysis
- Expert judgment and Delphi method
- Consider worst-case scenarios
- Insurance for catastrophic risks
- Build adaptive capacity, not just planning

### Challenge: Balancing Cost and Resilience

**Problem:**
- Resilience investments hard to justify
- Pressure to minimize costs
- Benefits are uncertain and future

**Solutions:**
- Quantify expected value of risk reduction
- Use real-world disruption examples
- Calculate value-at-risk (VaR)
- Stress test financial impact
- Start with high-probability, high-impact risks
- Incremental investments, prove value

### Challenge: Organizational Silos

**Problem:**
- Risk owned by different functions
- Lack of coordination
- No enterprise view of risk

**Solutions:**
- Establish supply chain risk committee
- Cross-functional risk workshops
- Centralized risk register and monitoring
- Clear escalation and decision processes
- Risk KPIs in executive dashboards
- Shared incentives for risk management

### Challenge: Complacency After Stability

**Problem:**
- Risk management de-prioritized in good times
- Reduced investment in resilience
- Knowledge and preparedness decay

**Solutions:**
- Regular scenario planning exercises
- Maintain risk management as core process
- Annual risk assessments mandatory
- Leadership commitment and tone from top
- Link to compliance and audit requirements
- Regular testing of business continuity plans

### Challenge: Speed vs. Thoroughness

**Problem:**
- Disruptions require fast decisions
- Limited time for analysis
- Need to act with incomplete information

**Solutions:**
- Pre-approved response playbooks
- Clear decision authority and escalation
- War room protocols
- Real-time data and dashboards
- Simplified decision frameworks for crisis
- Post-disruption learning and improvement

---

## Output Format

### Risk Assessment Report

**Executive Summary:**
- Top risks and overall risk exposure
- Value at Risk (VaR) estimate
- Supply chain resilience score
- Priority actions required

**Risk Register:**

| Risk ID | Risk Description | Category | Probability | Impact | Risk Score | Current Controls | Priority |
|---------|------------------|----------|-------------|--------|------------|------------------|----------|
| R001 | Single-source supplier failure | Supply | 15% | $2.0M | High | Quarterly reviews | 1 |
| R002 | Port congestion | Logistics | 25% | $500K | Medium | Dual port strategy | 3 |
| R003 | Demand forecast error | Demand | 40% | $800K | High | Market research | 2 |
| R004 | Cyberattack | External | 20% | $3.0M | Critical | Security controls | 1 |

**Scenario Analysis:**

| Scenario | Probability | Revenue Impact | Duration | Recovery Time | Expected Loss |
|----------|-------------|----------------|----------|---------------|---------------|
| Major supplier failure | 10% | $5.0M | 90 days | 120 days | $600K |
| Pandemic | 5% | $15.0M | 180 days | 365 days | $900K |
| Natural disaster | 15% | $3.0M | 60 days | 90 days | $570K |
| Trade restrictions | 20% | $8.0M | 120 days | 180 days | $2.0M |

**Risk Metrics:**

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Value at Risk (95%) | $8.5M | <$5M | ⚠ Above target |
| Expected Annual Loss | $4.2M | <$3M | ⚠ Above target |
| Resilience Index | 62/100 | >70 | ⚠ Below target |
| Risks Mitigated (YTD) | 12 | 15 | ⚠ Behind plan |

**Mitigation Plan:**

| Initiative | Risk Addressed | Investment | Annual Benefit | Timeline | Owner |
|-----------|----------------|------------|----------------|----------|-------|
| Dual sourcing program | R001 | $500K | $300K | Q2 2026 | Procurement |
| Safety stock increase | R001, R002 | $2.0M | $800K | Q1 2026 | Supply Chain |
| Nearshoring evaluation | R002, R005 | $200K | TBD | Q3 2026 | Strategy |
| Cyber resilience | R004 | $800K | $600K | Q1-Q2 2026 | IT |

---

## Questions to Ask

If you need more context:
1. What disruptions have you experienced recently?
2. What are your critical dependencies? (single-source suppliers, key facilities)
3. What's the maximum acceptable downtime for operations?
4. How much revenue is at risk from supply chain disruptions?
5. What's your current resilience strategy? (inventory buffers, backup suppliers)
6. Are there geographic concentrations of risk?
7. How visible is your supply chain beyond Tier 1 suppliers?
8. What business continuity plans are in place?
9. What's the budget for risk mitigation?
10. What insurance coverage exists?

---

## Related Skills

- **supplier-risk-management**: For assessing and mitigating supplier-specific risks
- **scenario-planning**: For strategic scenario analysis
- **demand-forecasting**: For reducing demand uncertainty
- **inventory-optimization**: For safety stock and buffer strategies
- **network-design**: For designing resilient supply chain networks
- **supplier-selection**: For incorporating risk in sourcing decisions
- **compliance-management**: For regulatory and compliance risks
- **contract-management**: For risk transfer through contracts
- **supplier-collaboration**: For collaborative risk management
