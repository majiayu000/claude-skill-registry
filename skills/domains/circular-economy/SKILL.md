---
name: circular-economy
description: When the user wants to implement circular economy principles, design closed-loop supply chains, or optimize reverse logistics. Also use when the user mentions "circular supply chain," "product lifecycle," "recycling," "remanufacturing," "refurbishment," "product returns," "waste reduction," "cradle-to-cradle," "regenerative design," or "resource recovery." For carbon tracking, see carbon-footprint-tracking. For sustainable sourcing, see sustainable-sourcing.
---

# Circular Economy

You are an expert in circular economy design and implementation for supply chains. Your goal is to help organizations transition from linear "take-make-dispose" models to circular systems that eliminate waste, keep materials in use, and regenerate natural systems.

## Initial Assessment

Before implementing circular economy strategies, understand:

1. **Current Business Model**
   - What products or services are offered?
   - Current product lifecycle (design, use, end-of-life)?
   - Existing waste streams and disposal methods?
   - Material flows and resource consumption?

2. **Circularity Goals**
   - What's driving circular economy interest? (sustainability, cost, regulation)
   - Target circularity rate or KPIs?
   - Customer demand for circular products?
   - Regulatory requirements (EPR, recycled content mandates)?

3. **Product Characteristics**
   - Product longevity and durability?
   - Material composition and recyclability?
   - Modularity and repairability?
   - Value retention over time?

4. **Reverse Logistics Capabilities**
   - Existing returns infrastructure?
   - Collection and sorting capabilities?
   - Refurbishment or remanufacturing facilities?
   - Secondary markets for used products?

---

## Circular Economy Framework

### Ellen MacArthur Foundation Principles

**1. Design Out Waste and Pollution**
- Eliminate waste at the design stage
- Choose safe, recyclable materials
- Design for disassembly
- Avoid hazardous substances

**2. Keep Products and Materials in Use**
- Maximize product lifespan
- Enable repair and maintenance
- Facilitate refurbishment and remanufacturing
- Ensure high-quality recycling

**3. Regenerate Natural Systems**
- Use renewable resources
- Return biological nutrients to earth
- Restore and enhance ecosystems
- Build soil health

### Circular Business Models

**1. Circular Supplies**
- Replace virgin materials with renewable or recycled inputs
- Biomaterials, renewable energy
- Example: Patagonia using recycled materials

**2. Product as a Service (PaaS)**
- Retain ownership, sell usage/performance
- Incentivizes durability and upgradability
- Example: Philips "Lighting as a Service"

**3. Product Life Extension**
- Repair, upgrade, refurbishment, remanufacturing
- Maintain product value longer
- Example: Caterpillar remanufacturing programs

**4. Sharing Platforms**
- Enable shared use of underutilized products
- Increase utilization rates
- Example: Zipcar, tool libraries

**5. Resource Recovery**
- Collect products at end-of-life
- Extract and reuse materials
- Example: Apple's recycling robots

---

## Circularity Metrics

### Material Circularity Indicator (MCI)

```python
import numpy as np
import pandas as pd

class CircularityCalculator:
    """Calculate circularity metrics for products and systems"""

    def calculate_mci(self, virgin_input, recycled_input, product_mass,
                     waste_generated, product_lifespan_actual,
                     product_lifespan_industry_avg):
        """
        Calculate Material Circularity Indicator (Ellen MacArthur Foundation)

        MCI ranges from 0 (linear) to 1 (fully circular)

        Parameters:
        - virgin_input: kg of virgin material input
        - recycled_input: kg of recycled material input
        - product_mass: kg of final product
        - waste_generated: kg of waste in production + end-of-life
        - product_lifespan_actual: years product is used
        - product_lifespan_industry_avg: years average for product category
        """

        total_input = virgin_input + recycled_input

        # Linear Flow Index (LFI) - measures material losses
        # LFI = (Virgin input + Waste) / (2 × Product mass)
        lfi = (virgin_input + waste_generated) / (2 * product_mass) if product_mass > 0 else 1

        # Utility factor - accounts for product lifespan
        # Longer life = better circularity
        utility_factor = product_lifespan_actual / product_lifespan_industry_avg
        utility_factor = min(utility_factor, 5)  # Cap at 5x industry average

        # MCI calculation
        mci = (1 - lfi) * utility_factor

        # Ensure MCI is between 0 and 1
        mci = max(0, min(1, mci))

        return {
            'mci': round(mci, 3),
            'lfi': round(lfi, 3),
            'utility_factor': round(utility_factor, 2),
            'virgin_content_pct': round(virgin_input / total_input * 100, 1) if total_input > 0 else 0,
            'recycled_content_pct': round(recycled_input / total_input * 100, 1) if total_input > 0 else 0,
            'circularity_level': self._classify_mci(mci)
        }

    def _classify_mci(self, mci):
        """Classify circularity level"""
        if mci >= 0.9:
            return 'Highly Circular'
        elif mci >= 0.7:
            return 'Circular'
        elif mci >= 0.5:
            return 'Moderately Circular'
        elif mci >= 0.3:
            return 'Somewhat Circular'
        else:
            return 'Linear'

    def calculate_circularity_rate(self, cycled_materials, total_material_flow):
        """
        Calculate Circularity Rate

        Percentage of materials that are cycled back into the economy
        """

        circularity_rate = (cycled_materials / total_material_flow * 100) if total_material_flow > 0 else 0

        return {
            'circularity_rate_pct': round(circularity_rate, 1),
            'cycled_materials': cycled_materials,
            'total_material_flow': total_material_flow,
            'linear_materials': total_material_flow - cycled_materials
        }

    def calculate_r_strategies_impact(self, product_value, r_strategy,
                                     value_retention_rate):
        """
        Calculate value retention for different R-strategies

        R-strategies (9R framework):
        R0: Refuse, R1: Rethink, R2: Reduce
        R3: Reuse, R4: Repair, R5: Refurbish
        R6: Remanufacture, R7: Repurpose, R8: Recycle, R9: Recover
        """

        # Value retention rates by strategy (typical)
        retention_rates = {
            'refuse': 1.0,       # Prevent need
            'rethink': 1.0,      # Product-as-service
            'reduce': 1.0,       # More efficient use
            'reuse': 0.95,       # Direct reuse
            'repair': 0.90,      # Fix for same use
            'refurbish': 0.85,   # Restore to good condition
            'remanufacture': 0.80,  # Disassemble and rebuild
            'repurpose': 0.60,   # Different application
            'recycle': 0.40,     # Material recovery
            'recover': 0.20      # Energy recovery
        }

        default_retention = retention_rates.get(r_strategy, 0.5)
        actual_retention = value_retention_rate if value_retention_rate else default_retention

        retained_value = product_value * actual_retention

        return {
            'r_strategy': r_strategy,
            'original_value': product_value,
            'retention_rate': actual_retention,
            'retained_value': round(retained_value, 2),
            'value_lost': round(product_value - retained_value, 2)
        }


# Example usage
calculator = CircularityCalculator()

# Example 1: Calculate MCI for a product
mci_result = calculator.calculate_mci(
    virgin_input=8.0,       # kg virgin materials
    recycled_input=2.0,     # kg recycled materials
    product_mass=10.0,      # kg final product
    waste_generated=1.5,    # kg waste (production + end-of-life)
    product_lifespan_actual=8,  # years
    product_lifespan_industry_avg=5  # years
)

print("Material Circularity Indicator (MCI):")
print(f"  MCI Score: {mci_result['mci']}")
print(f"  Circularity Level: {mci_result['circularity_level']}")
print(f"  Virgin Content: {mci_result['virgin_content_pct']}%")
print(f"  Recycled Content: {mci_result['recycled_content_pct']}%")
print(f"  Utility Factor: {mci_result['utility_factor']}")

# Example 2: Circularity rate
circ_rate = calculator.calculate_circularity_rate(
    cycled_materials=3000,      # tonnes recycled/reused
    total_material_flow=10000   # tonnes total materials used
)

print(f"\nCircularity Rate: {circ_rate['circularity_rate_pct']}%")

# Example 3: R-strategy value retention
repair_value = calculator.calculate_r_strategies_impact(
    product_value=500,
    r_strategy='repair',
    value_retention_rate=0.90
)

print(f"\nRepair Strategy:")
print(f"  Original Value: ${repair_value['original_value']}")
print(f"  Retained Value: ${repair_value['retained_value']}")
print(f"  Value Retention Rate: {repair_value['retention_rate']*100}%")
```

---

## Design for Circularity

### Design Principles

```python
class CircularDesignAssessment:
    """Assess product design for circularity"""

    def __init__(self, product_name):
        self.product_name = product_name
        self.assessment_criteria = {}

    def assess_design_for_disassembly(self, design_data):
        """
        Assess how easy product is to disassemble

        design_data: dict with design characteristics
        """
        score = 0
        max_score = 100
        feedback = []

        # Fastener type (0-20 points)
        fasteners = design_data.get('fasteners', 'permanent')
        if fasteners == 'snap_fit_reversible':
            score += 20
            feedback.append("✓ Reversible snap-fit fasteners")
        elif fasteners == 'screws_standard':
            score += 15
            feedback.append("✓ Standard screws used")
        elif fasteners == 'screws_proprietary':
            score += 10
            feedback.append("⚠ Proprietary fasteners (use standard)")
        else:
            score += 0
            feedback.append("✗ Permanent fasteners (welding, glue)")

        # Material variety (0-20 points)
        num_materials = design_data.get('num_material_types', 5)
        if num_materials <= 2:
            score += 20
            feedback.append("✓ Limited material types (≤2)")
        elif num_materials <= 4:
            score += 15
            feedback.append("⚠ Moderate material variety (3-4 types)")
        else:
            score += 5
            feedback.append("✗ High material variety (simplify)")

        # Material compatibility (0-20 points)
        incompatible_materials = design_data.get('incompatible_material_combos', 0)
        if incompatible_materials == 0:
            score += 20
            feedback.append("✓ No incompatible material combinations")
        elif incompatible_materials <= 2:
            score += 10
            feedback.append("⚠ Some incompatible combinations")
        else:
            score += 0
            feedback.append("✗ Many incompatible combinations")

        # Component labeling (0-15 points)
        if design_data.get('components_labeled', False):
            score += 15
            feedback.append("✓ Components labeled for recycling")
        else:
            score += 0
            feedback.append("✗ Components not labeled")

        # Modular design (0-25 points)
        modularity = design_data.get('modularity_level', 'none')
        if modularity == 'high':
            score += 25
            feedback.append("✓ Highly modular design")
        elif modularity == 'medium':
            score += 15
            feedback.append("⚠ Partially modular")
        else:
            score += 0
            feedback.append("✗ Not modular")

        return {
            'score': score,
            'max_score': max_score,
            'percentage': round(score / max_score * 100, 1),
            'rating': self._get_rating(score / max_score),
            'feedback': feedback
        }

    def assess_material_selection(self, material_data):
        """Assess material choices for circularity"""
        score = 0
        max_score = 100
        feedback = []

        # Recycled content (0-30 points)
        recycled_pct = material_data.get('recycled_content_pct', 0)
        if recycled_pct >= 50:
            score += 30
            feedback.append(f"✓ High recycled content ({recycled_pct}%)")
        elif recycled_pct >= 25:
            score += 20
            feedback.append(f"⚠ Moderate recycled content ({recycled_pct}%)")
        elif recycled_pct > 0:
            score += 10
            feedback.append(f"⚠ Low recycled content ({recycled_pct}%)")
        else:
            score += 0
            feedback.append("✗ No recycled content")

        # Recyclability (0-30 points)
        recyclability = material_data.get('recyclability', 'difficult')
        if recyclability == 'easily_recyclable':
            score += 30
            feedback.append("✓ Materials easily recyclable")
        elif recyclability == 'recyclable_with_effort':
            score += 20
            feedback.append("⚠ Materials recyclable with effort")
        else:
            score += 5
            feedback.append("✗ Materials difficult to recycle")

        # Renewable materials (0-20 points)
        renewable_pct = material_data.get('renewable_content_pct', 0)
        if renewable_pct >= 50:
            score += 20
            feedback.append(f"✓ High renewable content ({renewable_pct}%)")
        elif renewable_pct >= 25:
            score += 12
            feedback.append(f"⚠ Moderate renewable content ({renewable_pct}%)")
        elif renewable_pct > 0:
            score += 5
            feedback.append(f"⚠ Low renewable content ({renewable_pct}%)")

        # Hazardous substances (0-20 points)
        if material_data.get('hazardous_free', True):
            score += 20
            feedback.append("✓ No hazardous substances")
        else:
            score += 0
            feedback.append("✗ Contains hazardous substances")
            if material_data.get('hazardous_list'):
                feedback.append(f"  Substances: {', '.join(material_data['hazardous_list'])}")

        return {
            'score': score,
            'max_score': max_score,
            'percentage': round(score / max_score * 100, 1),
            'rating': self._get_rating(score / max_score),
            'feedback': feedback
        }

    def assess_durability_repairability(self, durability_data):
        """Assess product durability and ease of repair"""
        score = 0
        max_score = 100
        feedback = []

        # Expected lifespan (0-25 points)
        expected_years = durability_data.get('expected_lifespan_years', 0)
        industry_avg = durability_data.get('industry_avg_lifespan_years', 5)

        if expected_years >= industry_avg * 1.5:
            score += 25
            feedback.append(f"✓ Long lifespan ({expected_years} yrs, 1.5x industry avg)")
        elif expected_years >= industry_avg:
            score += 18
            feedback.append(f"✓ Good lifespan ({expected_years} yrs, meets industry avg)")
        else:
            score += 10
            feedback.append(f"⚠ Below average lifespan ({expected_years} yrs)")

        # Repairability (0-25 points)
        repair_score = durability_data.get('repair_score_out_of_10', 5)
        score += repair_score * 2.5
        if repair_score >= 8:
            feedback.append(f"✓ Highly repairable (score: {repair_score}/10)")
        elif repair_score >= 5:
            feedback.append(f"⚠ Moderately repairable (score: {repair_score}/10)")
        else:
            feedback.append(f"✗ Difficult to repair (score: {repair_score}/10)")

        # Spare parts availability (0-25 points)
        if durability_data.get('spare_parts_available', False):
            score += 25
            commitment_years = durability_data.get('spare_parts_commitment_years', 0)
            feedback.append(f"✓ Spare parts available ({commitment_years} years)")
        else:
            score += 0
            feedback.append("✗ Spare parts not available")

        # Repair documentation (0-25 points)
        if durability_data.get('repair_manual_available', False):
            score += 15
            feedback.append("✓ Repair manual available")
        else:
            feedback.append("✗ No repair manual")

        if durability_data.get('repair_videos_available', False):
            score += 10
            feedback.append("✓ Repair videos available")

        return {
            'score': score,
            'max_score': max_score,
            'percentage': round(score / max_score * 100, 1),
            'rating': self._get_rating(score / max_score),
            'feedback': feedback
        }

    def _get_rating(self, score_ratio):
        """Convert score to rating"""
        if score_ratio >= 0.9:
            return 'Excellent'
        elif score_ratio >= 0.75:
            return 'Good'
        elif score_ratio >= 0.60:
            return 'Fair'
        elif score_ratio >= 0.40:
            return 'Poor'
        else:
            return 'Very Poor'

    def generate_comprehensive_assessment(self, design_data, material_data,
                                          durability_data):
        """Generate full circularity assessment"""

        disassembly = self.assess_design_for_disassembly(design_data)
        materials = self.assess_material_selection(material_data)
        durability = self.assess_durability_repairability(durability_data)

        # Overall score (weighted average)
        overall_score = (
            disassembly['percentage'] * 0.35 +
            materials['percentage'] * 0.35 +
            durability['percentage'] * 0.30
        )

        return {
            'product': self.product_name,
            'overall_score': round(overall_score, 1),
            'overall_rating': self._get_rating(overall_score / 100),
            'design_for_disassembly': disassembly,
            'material_selection': materials,
            'durability_repairability': durability
        }


# Example assessment
product = CircularDesignAssessment('Acme Widget Pro')

design_data = {
    'fasteners': 'screws_standard',
    'num_material_types': 3,
    'incompatible_material_combos': 0,
    'components_labeled': True,
    'modularity_level': 'high'
}

material_data = {
    'recycled_content_pct': 60,
    'recyclability': 'easily_recyclable',
    'renewable_content_pct': 20,
    'hazardous_free': True
}

durability_data = {
    'expected_lifespan_years': 10,
    'industry_avg_lifespan_years': 6,
    'repair_score_out_of_10': 8,
    'spare_parts_available': True,
    'spare_parts_commitment_years': 10,
    'repair_manual_available': True,
    'repair_videos_available': True
}

assessment = product.generate_comprehensive_assessment(
    design_data, material_data, durability_data
)

print(f"Circular Design Assessment: {assessment['product']}")
print(f"Overall Score: {assessment['overall_score']}/100 ({assessment['overall_rating']})")
print(f"\nDesign for Disassembly: {assessment['design_for_disassembly']['percentage']}%")
print(f"Material Selection: {assessment['material_selection']['percentage']}%")
print(f"Durability & Repairability: {assessment['durability_repairability']['percentage']}%")
```

---

## Reverse Logistics Optimization

### Product Take-Back Program

```python
class ReverseLogisticsOptimizer:
    """Optimize reverse logistics and product take-back operations"""

    def __init__(self):
        self.collection_sites = []
        self.processing_facilities = []

    def calculate_collection_coverage(self, collection_sites, customer_locations,
                                     max_distance_km=50):
        """
        Calculate coverage of collection network

        collection_sites: list of dicts with lat/lon
        customer_locations: list of dicts with lat/lon
        """

        def haversine_distance(lat1, lon1, lat2, lon2):
            """Calculate distance between two points on Earth"""
            from math import radians, sin, cos, sqrt, atan2

            R = 6371  # Earth radius in km

            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
            dlat = lat2 - lat1
            dlon = lon2 - lon1

            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))

            return R * c

        covered_customers = 0

        for customer in customer_locations:
            cust_lat = customer['lat']
            cust_lon = customer['lon']

            # Check if any collection site is within max distance
            for site in collection_sites:
                distance = haversine_distance(
                    cust_lat, cust_lon,
                    site['lat'], site['lon']
                )

                if distance <= max_distance_km:
                    covered_customers += 1
                    break  # Customer is covered

        coverage_pct = (covered_customers / len(customer_locations) * 100) if customer_locations else 0

        return {
            'total_customers': len(customer_locations),
            'covered_customers': covered_customers,
            'coverage_percentage': round(coverage_pct, 1),
            'uncovered_customers': len(customer_locations) - covered_customers,
            'max_distance_km': max_distance_km
        }

    def calculate_return_rate_economics(self, product_data):
        """
        Calculate economics of product returns and refurbishment

        product_data: dict with product and return info
        """

        original_price = product_data['original_price']
        units_sold = product_data['units_sold']
        return_rate = product_data['return_rate']  # fraction (e.g., 0.15 for 15%)

        # Returns
        units_returned = units_sold * return_rate

        # Collection costs
        collection_cost_per_unit = product_data.get('collection_cost_per_unit', 5)
        collection_cost_total = units_returned * collection_cost_per_unit

        # Sorting and grading
        sorting_cost_per_unit = product_data.get('sorting_cost_per_unit', 2)
        sorting_cost_total = units_returned * sorting_cost_per_unit

        # Categorize returns
        grade_a_rate = product_data.get('grade_a_rate', 0.30)  # Resell as-is
        grade_b_rate = product_data.get('grade_b_rate', 0.40)  # Refurbish
        grade_c_rate = product_data.get('grade_c_rate', 0.20)  # Parts recovery
        grade_d_rate = product_data.get('grade_d_rate', 0.10)  # Recycle/dispose

        units_grade_a = units_returned * grade_a_rate
        units_grade_b = units_returned * grade_b_rate
        units_grade_c = units_returned * grade_c_rate
        units_grade_d = units_returned * grade_d_rate

        # Grade A: Resell as-is
        resale_price_a = original_price * 0.70  # 70% of original
        cleaning_cost_a = 3
        revenue_a = units_grade_a * (resale_price_a - cleaning_cost_a)

        # Grade B: Refurbish
        refurb_cost_b = original_price * 0.20  # 20% of original to refurbish
        resale_price_b = original_price * 0.60  # 60% of original
        revenue_b = units_grade_b * (resale_price_b - refurb_cost_b)

        # Grade C: Parts recovery
        parts_value_c = original_price * 0.30  # 30% parts value
        disassembly_cost_c = original_price * 0.10
        revenue_c = units_grade_c * (parts_value_c - disassembly_cost_c)

        # Grade D: Material recycling
        material_value_d = original_price * 0.05  # 5% material value
        processing_cost_d = original_price * 0.03
        revenue_d = units_grade_d * (material_value_d - processing_cost_d)

        # Total
        total_revenue = revenue_a + revenue_b + revenue_c + revenue_d
        total_cost = collection_cost_total + sorting_cost_total
        net_value = total_revenue - total_cost

        return {
            'units_returned': round(units_returned, 0),
            'return_rate_pct': round(return_rate * 100, 1),
            'distribution': {
                'grade_a_resell': round(units_grade_a, 0),
                'grade_b_refurbish': round(units_grade_b, 0),
                'grade_c_parts': round(units_grade_c, 0),
                'grade_d_recycle': round(units_grade_d, 0)
            },
            'revenue_by_grade': {
                'grade_a': round(revenue_a, 2),
                'grade_b': round(revenue_b, 2),
                'grade_c': round(revenue_c, 2),
                'grade_d': round(revenue_d, 2),
                'total': round(total_revenue, 2)
            },
            'costs': {
                'collection': round(collection_cost_total, 2),
                'sorting': round(sorting_cost_total, 2),
                'total': round(total_cost, 2)
            },
            'net_value': round(net_value, 2),
            'value_per_returned_unit': round(net_value / units_returned, 2) if units_returned > 0 else 0
        }

    def optimize_refurbishment_capacity(self, demand_data):
        """
        Optimize refurbishment facility capacity

        demand_data: dict with demand forecasts and cost info
        """

        # Demand parameters
        avg_monthly_returns = demand_data['avg_monthly_returns']
        returns_std_dev = demand_data['returns_std_dev']
        refurb_rate = demand_data.get('refurb_rate', 0.40)  # 40% need refurbishment

        refurb_demand_avg = avg_monthly_returns * refurb_rate
        refurb_demand_std = returns_std_dev * refurb_rate

        # Capacity options
        capacity_options = []

        for capacity_level in [0.8, 1.0, 1.2, 1.5, 2.0]:
            capacity = refurb_demand_avg * capacity_level

            # Fixed costs (facility, equipment, base staffing)
            fixed_cost_monthly = demand_data.get('fixed_cost_base', 50000) * capacity_level

            # Variable costs (per unit processed)
            variable_cost_per_unit = demand_data.get('variable_cost_per_unit', 20)

            # Calculate expected utilization
            # Assumes normal distribution of demand
            from scipy import stats
            prob_exceed = 1 - stats.norm.cdf(capacity, refurb_demand_avg, refurb_demand_std)
            utilization = min(1.0, refurb_demand_avg / capacity)

            # Units processed
            units_processed = min(capacity, refurb_demand_avg)

            # Backlog cost (if demand exceeds capacity)
            backlog_units = max(0, refurb_demand_avg - capacity)
            backlog_cost_per_unit = demand_data.get('backlog_cost_per_unit', 50)
            backlog_cost = backlog_units * backlog_cost_per_unit

            # Total cost
            total_cost = fixed_cost_monthly + (units_processed * variable_cost_per_unit) + backlog_cost
            cost_per_unit = total_cost / units_processed if units_processed > 0 else float('inf')

            capacity_options.append({
                'capacity_level': capacity_level,
                'capacity_units': round(capacity, 0),
                'expected_utilization': round(utilization * 100, 1),
                'units_processed': round(units_processed, 0),
                'backlog_units': round(backlog_units, 0),
                'fixed_cost': round(fixed_cost_monthly, 2),
                'variable_cost': round(units_processed * variable_cost_per_unit, 2),
                'backlog_cost': round(backlog_cost, 2),
                'total_cost': round(total_cost, 2),
                'cost_per_unit': round(cost_per_unit, 2)
            })

        # Find optimal (lowest cost per unit)
        optimal = min(capacity_options, key=lambda x: x['cost_per_unit'])

        return {
            'capacity_options': pd.DataFrame(capacity_options),
            'optimal_capacity': optimal,
            'recommendation': f"Build capacity for {optimal['capacity_level']}x average demand"
        }


# Example usage
rl_optimizer = ReverseLogisticsOptimizer()

# Example 1: Calculate return economics
product_data = {
    'original_price': 500,
    'units_sold': 10000,
    'return_rate': 0.12,  # 12% return rate
    'collection_cost_per_unit': 10,
    'sorting_cost_per_unit': 3,
    'grade_a_rate': 0.25,  # 25% can resell as-is
    'grade_b_rate': 0.45,  # 45% need refurbishment
    'grade_c_rate': 0.20,  # 20% for parts
    'grade_d_rate': 0.10   # 10% recycle
}

economics = rl_optimizer.calculate_return_rate_economics(product_data)

print("Return Economics:")
print(f"  Units Returned: {economics['units_returned']}")
print(f"  Total Revenue: ${economics['revenue_by_grade']['total']:,.2f}")
print(f"  Total Costs: ${economics['costs']['total']:,.2f}")
print(f"  Net Value: ${economics['net_value']:,.2f}")
print(f"  Value per Unit: ${economics['value_per_returned_unit']:.2f}")

# Example 2: Optimize refurbishment capacity
demand_data = {
    'avg_monthly_returns': 500,
    'returns_std_dev': 100,
    'refurb_rate': 0.45,
    'fixed_cost_base': 40000,
    'variable_cost_per_unit': 25,
    'backlog_cost_per_unit': 60
}

capacity_analysis = rl_optimizer.optimize_refurbishment_capacity(demand_data)

print("\n\nRefurbishment Capacity Options:")
print(capacity_analysis['capacity_options'][['capacity_level', 'capacity_units', 'expected_utilization', 'cost_per_unit']])
print(f"\n{capacity_analysis['recommendation']}")
```

---

## Tools & Libraries

### Python Libraries

**Circularity Analysis:**
- `pandas`: Data manipulation
- `numpy`: Numerical computations
- `scipy`: Statistical analysis

**Life Cycle Assessment:**
- `brightway2`: LCA framework
- `openLCA`: Open-source LCA
- `lca_algebraic`: Algebraic LCA

**Optimization:**
- `pulp`: Linear programming
- `scipy.optimize`: Optimization algorithms
- `pyomo`: Optimization modeling

**Visualization:**
- `matplotlib`, `seaborn`: Charts and plots
- `plotly`: Interactive visualizations
- `sankey`: Material flow diagrams

### Commercial Software

**Circular Economy Platforms:**
- **Circularity Metrics**: Ellen MacArthur Foundation tool
- **Circularise**: Supply chain traceability
- **Rheaply**: Asset management and reuse
- **Reconomy**: Resource recovery platform
- **Excess Materials Exchange**: Material marketplace

**Product Design:**
- **Autodesk Fusion 360**: Design for circularity
- **Solidworks Sustainability**: Environmental impact analysis
- **SimaPro**: LCA software
- **GaBi**: Life cycle assessment

**Reverse Logistics:**
- **Optoro**: Returns optimization
- **ReverseLogix**: Returns management
- **Inmar**: Product returns and recycling
- **B-Stock**: Liquidation marketplace

**Material Passports:**
- **Madaster**: Material passport platform
- **Concular**: Building material marketplace
- **Opalis**: Circular material management

---

## Common Challenges & Solutions

### Challenge: Economic Viability

**Problem:**
- Circular models may have higher upfront costs
- Uncertain ROI on take-back programs
- Competition with cheap linear alternatives

**Solutions:**
- Start with high-value products (electronics, machinery)
- Design for multiple lifecycles from start
- Extended Producer Responsibility (EPR) can offset costs
- Market refurbished products to value-conscious segments
- Partner with specialists for reverse logistics
- Calculate full lifecycle costs (including disposal)

### Challenge: Consumer Behavior

**Problem:**
- Customers prefer new over refurbished
- Low participation in take-back programs
- Resistance to product-as-service models

**Solutions:**
- Offer incentives (trade-in credit, discounts)
- Certification and warranties for refurbished products
- Educate on quality and environmental benefits
- Make returns convenient (free shipping, drop-off points)
- Build circular features into brand identity
- Start with B2B where circularity is valued

### Challenge: Product Design Legacy

**Problem:**
- Existing products not designed for circularity
- Long product development cycles
- Cost pressures favor cheap, disposable designs

**Solutions:**
- Implement design guidelines for new products
- Retrofit take-back for current products
- Pilot circular design with new product lines
- Calculate business case including end-of-life value
- Regulatory pressure (right-to-repair, EPR)
- Executive commitment to sustainability

### Challenge: Reverse Logistics Complexity

**Problem:**
- Collection network expensive to build
- Variable product conditions
- Unpredictable return volumes
- Need for inspection, sorting, testing

**Solutions:**
- Partner with existing logistics providers
- Use retail locations as collection points
- Implement grading standards and automation
- Build data analytics for return prediction
- Start in concentrated geographies
- Third-party refurbishment specialists

### Challenge: Material Traceability

**Problem:**
- Unknown material composition of products
- Mixed materials difficult to separate
- Lack of information on product history

**Solutions:**
- Implement material passports (digital records)
- Label components with material information
- Use blockchain for supply chain traceability
- Design for easy material identification
- Material libraries and databases
- Industry standardization efforts

### Challenge: Scale and Infrastructure

**Problem:**
- Lack of recycling/refurbishment infrastructure
- Limited markets for secondary materials
- Technology for separation not available

**Solutions:**
- Collaborate with industry players
- Government support for circular infrastructure
- Design for existing recycling systems
- Build material marketplaces
- Invest in separation technologies
- Regional circular economy hubs

---

## Output Format

### Circular Economy Assessment Report

**Executive Summary:**
- Current circularity rate
- Material flows and waste streams
- Circular economy opportunities identified
- Recommended initiatives and ROI

**Material Flow Analysis:**

| Material | Input (tonnes) | Virgin (%) | Recycled (%) | Output (tonnes) | Waste (%) | Circulated (%) |
|----------|----------------|------------|--------------|-----------------|-----------|----------------|
| Steel | 1,000 | 65% | 35% | 950 | 10% | 40% |
| Plastic | 500 | 80% | 20% | 480 | 15% | 25% |
| Aluminum | 300 | 40% | 60% | 290 | 5% | 65% |
| **Total** | **1,800** | **65%** | **35%** | **1,720** | **11%** | **42%** |

**Product Circularity Assessment:**

| Product | MCI Score | Recycled Content | Lifespan vs Avg | Repairability | Priority |
|---------|-----------|------------------|-----------------|---------------|----------|
| Product A | 0.72 | 45% | 1.5x | 8/10 | High |
| Product B | 0.45 | 20% | 1.0x | 5/10 | Medium |
| Product C | 0.28 | 10% | 0.8x | 3/10 | Redesign |

**Circular Initiatives:**

| Initiative | Strategy | Investment | Annual Savings | Payback | Impact (tCO2e) | Priority |
|-----------|----------|------------|----------------|---------|----------------|----------|
| Product Take-Back | Recovery | $500K | $180K | 2.8 yrs | -1,200 | High |
| Design for Disassembly | Design | $200K | $90K | 2.2 yrs | -400 | High |
| Remanufacturing Program | Extend | $800K | $350K | 2.3 yrs | -2,000 | High |
| Material Substitution | Inputs | $300K | $120K | 2.5 yrs | -600 | Medium |

**Financial Impact:**

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| Circularity Rate | 35% | 60% | +25 pts |
| Waste to Landfill | 200 tonnes | 50 tonnes | -75% |
| Material Cost | $2.5M | $2.0M | -$500K |
| Revenue from Returns | $100K | $650K | +$550K |
| Net Benefit | | | **$1.05M/year** |

---

## Questions to Ask

If you need more context:
1. What products or materials are in scope?
2. What's the current end-of-life fate of products? (landfill, recycle, reuse)
3. Are products designed for disassembly and repair?
4. What's the return/take-back rate?
5. Are there regulatory drivers? (EPR, right-to-repair, recycled content mandates)
6. What circular business models are being considered? (PaaS, refurbishment, recycling)
7. Is there infrastructure for collection and processing?
8. What are material costs and availability of recycled alternatives?
9. What's the customer attitude toward refurbished products?
10. Are there existing circular economy partnerships or programs?

---

## Related Skills

- **carbon-footprint-tracking**: For emissions impact of circular strategies
- **sustainable-sourcing**: For procurement of recycled and renewable materials
- **compliance-management**: For EPR and circular economy regulations
- **network-design**: For designing reverse logistics networks
- **route-optimization**: For optimizing collection logistics
- **warehouse-design**: For refurbishment and sorting facilities
- **demand-forecasting**: For predicting product returns
- **inventory-optimization**: For managing refurbished product inventory
- **quality-management**: For grading and testing returned products
