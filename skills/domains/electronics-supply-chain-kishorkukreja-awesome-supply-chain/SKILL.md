---
name: electronics-supply-chain
description: When the user wants to optimize electronics manufacturing supply chains, manage semiconductor sourcing, handle PCB assembly, or navigate component allocation. Also use when the user mentions "electronics manufacturing," "semiconductor supply chain," "PCB assembly," "EMS/ODM," "component allocation," "lead time management," "electronics sourcing," "PCBA," "contract manufacturing," or "electronics lifecycle management." For general manufacturing, see production-scheduling. For quality, see quality-management.
---

# Electronics Supply Chain

You are an expert in electronics manufacturing supply chain management and semiconductor operations. Your goal is to help optimize complex global supply networks, manage component sourcing and allocation, implement efficient assembly operations, and navigate the unique challenges of electronics manufacturing.

## Initial Assessment

Before optimizing electronics supply chains, understand:

1. **Manufacturing Model**
   - OEM, ODM, EMS, or internal manufacturing?
   - Product types? (consumer electronics, industrial, automotive, medical)
   - Production volume? (high-volume, mid-volume, prototype)
   - Manufacturing approach? (make-to-stock, make-to-order, configure-to-order)
   - Where in value chain? (component, module, finished product)

2. **Component Profile**
   - Semiconductor dependency level? (ICs, processors, memory, analog)
   - Passive components volume? (resistors, capacitors, connectors)
   - Long lead-time components? (FPGAs, custom ASICs, displays)
   - Single-source vs. multi-source components?
   - Allocation status? (open market, allocated, allocated critical)

3. **Supply Chain Structure**
   - Geographic footprint? (Asia-heavy, diversified, nearshore)
   - Number of tier suppliers and CMs?
   - Direct vs. distributor sourcing?
   - Consignment vs. turnkey model?
   - VMI (Vendor Managed Inventory) programs?

4. **Current Challenges**
   - Component availability and allocation issues?
   - Lead time volatility?
   - Excess and obsolete (E&O) inventory?
   - Product lifecycle management?
   - Cost reduction targets?

---

## Electronics Supply Chain Framework

### Value Chain Structure

**Electronics Manufacturing Ecosystem:**

```
Raw Materials (Silicon, Metals, Plastics)
  ↓
Component Manufacturers (Semiconductors, Passives, Connectors)
  ↓
Distributors / Brokers
  ↓
EMS/ODM (Contract Manufacturers)
  ↓
OEM (Brand Owners)
  ↓
Distribution / Retail
  ↓
End Customers
```

**Key Players by Tier:**

- **Component Manufacturers**: Intel, Samsung, TSMC, TI, Analog Devices, Infineon
- **Distributors**: Arrow, Avnet, Digi-Key, Mouser, Future Electronics
- **EMS/ODM**: Foxconn, Flex, Jabil, Pegatron, Wistron, Quanta
- **OEMs**: Apple, Dell, HP, Cisco, Huawei, Lenovo

---

## Component Sourcing & Allocation Management

### Allocation Strategy

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class ComponentAllocationManager:
    """
    Manage component allocation in constrained supply environment
    """

    def __init__(self, components_df):
        """
        Initialize allocation manager

        Parameters:
        - components_df: component data with lead times, allocation status
        """
        self.components = components_df
        self.allocation_tiers = {
            'strategic': 1,
            'preferred': 2,
            'standard': 3,
            'new': 4
        }

    def assess_allocation_risk(self, bom_df, production_plan):
        """
        Assess component allocation risk for production plan

        Parameters:
        - bom_df: Bill of Materials
        - production_plan: planned production volumes by period

        Returns:
        - risk assessment by component
        """

        risk_assessment = []

        for idx, component in bom_df.iterrows():
            part_number = component['part_number']
            qty_per_unit = component['quantity_per_unit']

            # Get component details
            comp_info = self.components[
                self.components['part_number'] == part_number
            ].iloc[0] if len(self.components[
                self.components['part_number'] == part_number
            ]) > 0 else None

            if comp_info is None:
                continue

            # Calculate requirements
            total_requirement = production_plan['units'].sum() * qty_per_unit

            # Allocation status
            allocation_status = comp_info.get('allocation_status', 'open')
            lead_time_weeks = comp_info.get('lead_time_weeks', 12)
            available_inventory = comp_info.get('available_inventory', 0)
            allocated_qty = comp_info.get('allocated_qty', 0)

            # Calculate risk score
            risk_score = self._calculate_risk_score(
                allocation_status,
                lead_time_weeks,
                total_requirement,
                available_inventory + allocated_qty
            )

            risk_assessment.append({
                'part_number': part_number,
                'description': comp_info.get('description', ''),
                'manufacturer': comp_info.get('manufacturer', ''),
                'total_requirement': total_requirement,
                'available_inventory': available_inventory,
                'allocated_qty': allocated_qty,
                'shortfall': max(0, total_requirement - available_inventory - allocated_qty),
                'allocation_status': allocation_status,
                'lead_time_weeks': lead_time_weeks,
                'risk_score': risk_score,
                'risk_category': self._categorize_risk(risk_score)
            })

        return pd.DataFrame(risk_assessment).sort_values('risk_score', ascending=False)

    def _calculate_risk_score(self, allocation_status, lead_time, requirement, supply):
        """Calculate component risk score (0-100)"""

        # Allocation multiplier
        allocation_multiplier = {
            'open': 1.0,
            'watch': 2.0,
            'allocated': 4.0,
            'critical': 8.0,
            'unobtainable': 10.0
        }.get(allocation_status, 1.0)

        # Lead time factor (longer = higher risk)
        lt_factor = min(lead_time / 52, 2.0)  # Cap at 2x

        # Supply coverage (weeks)
        coverage = (supply / requirement) if requirement > 0 else 999
        coverage_factor = max(0, 2 - coverage)  # Higher if coverage < 2x

        risk_score = (allocation_multiplier * 20 +
                     lt_factor * 20 +
                     coverage_factor * 30)

        return min(100, risk_score)

    def _categorize_risk(self, risk_score):
        """Categorize risk level"""
        if risk_score >= 70:
            return 'critical'
        elif risk_score >= 50:
            return 'high'
        elif risk_score >= 30:
            return 'medium'
        else:
            return 'low'

    def optimize_allocation_strategy(self, risk_assessment, supplier_relationships):
        """
        Generate allocation strategy recommendations

        Parameters:
        - risk_assessment: output from assess_allocation_risk
        - supplier_relationships: customer tier with suppliers

        Returns:
        - recommended actions by component
        """

        recommendations = []

        critical_parts = risk_assessment[risk_assessment['risk_category'] == 'critical']

        for idx, part in critical_parts.iterrows():
            actions = []

            # Determine customer tier
            customer_tier = supplier_relationships.get(
                part['manufacturer'], 'standard'
            )

            # Strategy based on risk and relationship
            if part['allocation_status'] == 'critical':
                actions.append('escalate_to_executive_level')
                actions.append('request_emergency_allocation')
                actions.append('explore_authorized_distributors')

            if part['lead_time_weeks'] > 26:
                actions.append('increase_forecast_horizon')
                actions.append('commit_to_longer_term_contract')

            if part['shortfall'] > 0:
                actions.append('identify_alternative_components')
                actions.append('engage_design_engineering_for_redesign')
                actions.append('search_broker_market')

            if customer_tier == 'new':
                actions.append('establish_strategic_relationship')
                actions.append('increase_volumes_to_gain_priority')

            recommendations.append({
                'part_number': part['part_number'],
                'manufacturer': part['manufacturer'],
                'risk_category': part['risk_category'],
                'customer_tier': customer_tier,
                'recommended_actions': actions,
                'priority': 'immediate' if part['risk_score'] > 80 else 'urgent'
            })

        return pd.DataFrame(recommendations)


# Example usage
components_data = pd.DataFrame({
    'part_number': ['IC_001', 'IC_002', 'CAP_001', 'RES_001'],
    'description': ['MCU STM32', 'Power IC', 'MLCC 10uF', 'Resistor 10K'],
    'manufacturer': ['STMicro', 'TI', 'Murata', 'Yageo'],
    'allocation_status': ['allocated', 'critical', 'open', 'open'],
    'lead_time_weeks': [32, 52, 8, 4],
    'available_inventory': [5000, 0, 100000, 500000],
    'allocated_qty': [10000, 5000, 0, 0]
})

bom = pd.DataFrame({
    'part_number': ['IC_001', 'IC_002', 'CAP_001', 'RES_001'],
    'quantity_per_unit': [1, 1, 12, 45]
})

production_plan = pd.DataFrame({
    'month': ['2025-02', '2025-03', '2025-04'],
    'units': [10000, 12000, 15000]
})

manager = ComponentAllocationManager(components_data)
risk_assessment = manager.assess_allocation_risk(bom, production_plan)

print("Component Risk Assessment:")
print(risk_assessment[['part_number', 'allocation_status', 'shortfall',
                       'risk_score', 'risk_category']])
```

---

## PCB Assembly Optimization

### Line Balancing for SMT Lines

```python
class SMTLineOptimizer:
    """
    Optimize Surface Mount Technology (SMT) line operations
    """

    def __init__(self, line_config):
        """
        Initialize SMT line optimizer

        Parameters:
        - line_config: SMT line configuration (machines, feeders, speed)
        """
        self.line_config = line_config

    def calculate_line_capacity(self, board_config):
        """
        Calculate SMT line capacity for given board

        Parameters:
        - board_config: PCB specifications and component placement

        Returns:
        - theoretical capacity (boards/hour)
        """

        # Component placement time
        num_components = board_config['component_count']
        avg_placement_time_sec = board_config.get('avg_placement_time', 0.3)

        # Machine parameters
        num_placement_heads = self.line_config.get('placement_heads', 8)
        machine_efficiency = self.line_config.get('efficiency', 0.85)

        # Calculate placement time per board
        placement_time = (num_components * avg_placement_time_sec) / num_placement_heads

        # Add process times
        screen_print_time = 15  # seconds
        reflow_time = 180  # seconds
        inspection_time = 30  # seconds
        board_handling_time = 10  # seconds

        total_cycle_time = (placement_time + screen_print_time +
                           reflow_time + inspection_time + board_handling_time)

        # Apply efficiency factor
        effective_cycle_time = total_cycle_time / machine_efficiency

        # Capacity (boards per hour)
        capacity_per_hour = 3600 / effective_cycle_time

        return {
            'capacity_boards_per_hour': capacity_per_hour,
            'cycle_time_seconds': effective_cycle_time,
            'placement_time': placement_time,
            'bottleneck': self._identify_bottleneck(
                placement_time, screen_print_time, reflow_time
            )
        }

    def _identify_bottleneck(self, placement_time, print_time, reflow_time):
        """Identify process bottleneck"""
        times = {
            'placement': placement_time,
            'screen_print': print_time,
            'reflow': reflow_time
        }
        return max(times, key=times.get)

    def optimize_feeder_setup(self, bom_df, feeder_slots=120):
        """
        Optimize feeder setup for component loading

        Parameters:
        - bom_df: Bill of Materials with component usage
        - feeder_slots: available feeder slots on machine

        Returns:
        - feeder assignment plan
        """

        # Sort components by usage frequency
        bom_sorted = bom_df.sort_values('quantity_per_board', ascending=False)

        # Assign to feeders (most used components get priority positions)
        feeder_assignments = []

        for idx, component in bom_sorted.iterrows():
            if idx < feeder_slots:
                # Optimal position: center positions for high-usage parts
                if idx < 20:
                    position = 60 + (idx - 10)  # Center positions
                else:
                    position = idx

                feeder_assignments.append({
                    'part_number': component['part_number'],
                    'feeder_position': position,
                    'quantity_per_board': component['quantity_per_board'],
                    'priority': 'high' if idx < 20 else 'medium'
                })
            else:
                # Bulk feeders or manual loading required
                feeder_assignments.append({
                    'part_number': component['part_number'],
                    'feeder_position': None,
                    'quantity_per_board': component['quantity_per_board'],
                    'priority': 'low',
                    'loading_method': 'manual_or_bulk'
                })

        return pd.DataFrame(feeder_assignments)

    def calculate_changeover_time(self, current_bom, next_bom, feeder_change_time=60):
        """
        Calculate line changeover time between products

        Parameters:
        - current_bom: current product BOM
        - next_bom: next product BOM
        - feeder_change_time: seconds per feeder change

        Returns:
        - estimated changeover time
        """

        # Components unique to each product
        current_parts = set(current_bom['part_number'])
        next_parts = set(next_bom['part_number'])

        # Components to remove and add
        parts_to_remove = current_parts - next_parts
        parts_to_add = next_parts - current_parts

        total_changes = len(parts_to_remove) + len(parts_to_add)

        # Changeover time
        feeder_changeover = total_changes * feeder_change_time
        program_change = 300  # 5 minutes for program change
        first_article_inspection = 600  # 10 minutes

        total_changeover = feeder_changeover + program_change + first_article_inspection

        return {
            'total_changeover_minutes': total_changeover / 60,
            'feeder_changes': total_changes,
            'parts_to_remove': len(parts_to_remove),
            'parts_to_add': len(parts_to_add),
            'common_parts': len(current_parts & next_parts)
        }


# Example
line_config = {
    'placement_heads': 8,
    'efficiency': 0.85,
    'feeder_slots': 120
}

board_config = {
    'component_count': 450,
    'avg_placement_time': 0.3,
    'board_size': '300x200mm'
}

optimizer = SMTLineOptimizer(line_config)
capacity = optimizer.calculate_line_capacity(board_config)

print(f"Line Capacity: {capacity['capacity_boards_per_hour']:.1f} boards/hour")
print(f"Cycle Time: {capacity['cycle_time_seconds']:.1f} seconds")
print(f"Bottleneck: {capacity['bottleneck']}")
```

---

## Lead Time Management

### Dynamic Lead Time Planning

```python
class LeadTimeManager:
    """
    Manage component lead times and procurement planning
    """

    def __init__(self, components_df):
        self.components = components_df

    def calculate_procurement_dates(self, production_schedule, bom_df):
        """
        Calculate when to order components based on lead times

        Parameters:
        - production_schedule: planned production dates
        - bom_df: Bill of Materials with quantities

        Returns:
        - component order schedule
        """

        procurement_schedule = []

        for idx, production in production_schedule.iterrows():
            production_date = production['production_date']
            product_id = production['product_id']
            quantity = production['quantity']

            # Get BOM for this product
            product_bom = bom_df[bom_df['product_id'] == product_id]

            for _, component in product_bom.iterrows():
                part_number = component['part_number']
                qty_per_unit = component['quantity_per_unit']
                total_needed = quantity * qty_per_unit

                # Get component lead time
                comp_info = self.components[
                    self.components['part_number'] == part_number
                ].iloc[0]

                lead_time_weeks = comp_info['lead_time_weeks']
                safety_buffer_weeks = comp_info.get('safety_buffer_weeks', 2)

                # Calculate order date
                total_lead_time = timedelta(weeks=lead_time_weeks + safety_buffer_weeks)
                order_date = production_date - total_lead_time

                procurement_schedule.append({
                    'part_number': part_number,
                    'manufacturer': comp_info['manufacturer'],
                    'order_date': order_date,
                    'need_by_date': production_date,
                    'quantity': total_needed,
                    'lead_time_weeks': lead_time_weeks,
                    'production_order': product_id,
                    'days_until_order': (order_date - datetime.now()).days
                })

        return pd.DataFrame(procurement_schedule).sort_values('order_date')

    def simulate_lead_time_variability(self, component, order_quantity,
                                      num_simulations=1000):
        """
        Monte Carlo simulation of lead time variability

        Parameters:
        - component: component details with lead time distribution
        - order_quantity: quantity to order
        - num_simulations: number of Monte Carlo runs

        Returns:
        - lead time distribution and risk metrics
        """

        # Lead time distribution parameters
        lt_mean = component['lead_time_weeks']
        lt_std = component.get('lead_time_std', lt_mean * 0.2)

        # Simulate lead times
        simulated_lts = np.random.normal(lt_mean, lt_std, num_simulations)
        simulated_lts = np.maximum(simulated_lts, lt_mean * 0.5)  # Floor

        # Calculate percentiles
        p50 = np.percentile(simulated_lts, 50)
        p80 = np.percentile(simulated_lts, 80)
        p95 = np.percentile(simulated_lts, 95)

        return {
            'mean_lt_weeks': lt_mean,
            'p50_lt_weeks': p50,
            'p80_lt_weeks': p80,
            'p95_lt_weeks': p95,
            'recommended_buffer_weeks': p95 - lt_mean,
            'variability_coefficient': lt_std / lt_mean
        }


# Example
components_data = pd.DataFrame({
    'part_number': ['IC_001', 'IC_002'],
    'manufacturer': ['STMicro', 'TI'],
    'lead_time_weeks': [32, 52],
    'lead_time_std': [6, 12],
    'safety_buffer_weeks': [4, 8]
})

production_schedule = pd.DataFrame({
    'production_date': pd.to_datetime(['2025-06-01', '2025-07-01']),
    'product_id': ['PROD_A', 'PROD_A'],
    'quantity': [5000, 6000]
})

bom = pd.DataFrame({
    'product_id': ['PROD_A', 'PROD_A'],
    'part_number': ['IC_001', 'IC_002'],
    'quantity_per_unit': [1, 2]
})

lt_manager = LeadTimeManager(components_data)
procurement = lt_manager.calculate_procurement_dates(production_schedule, bom)

print("Procurement Schedule:")
print(procurement[['part_number', 'order_date', 'need_by_date',
                   'quantity', 'days_until_order']])
```

---

## Excess & Obsolete (E&O) Management

```python
class EOInventoryManager:
    """
    Manage excess and obsolete inventory in electronics
    """

    def __init__(self, inventory_df, bom_df, forecast_df):
        self.inventory = inventory_df
        self.bom = bom_df
        self.forecast = forecast_df

    def identify_excess_obsolete(self, time_horizon_months=12):
        """
        Identify excess and obsolete inventory

        Parameters:
        - time_horizon_months: planning horizon for demand

        Returns:
        - E&O classification by component
        """

        eo_analysis = []

        for idx, inv in self.inventory.iterrows():
            part_number = inv['part_number']
            on_hand_qty = inv['on_hand_quantity']
            unit_cost = inv['unit_cost']

            # Calculate future demand
            future_demand = self._calculate_future_demand(
                part_number, time_horizon_months
            )

            # Calculate excess
            excess_qty = max(0, on_hand_qty - future_demand)
            excess_value = excess_qty * unit_cost

            # Determine obsolescence risk
            lifecycle_status = inv.get('lifecycle_status', 'active')
            last_usage_date = inv.get('last_usage_date', datetime.now())
            months_since_use = (datetime.now() - last_usage_date).days / 30

            # Classification
            if lifecycle_status == 'discontinued' or months_since_use > 24:
                classification = 'obsolete'
            elif excess_qty > future_demand * 0.5 or months_since_use > 12:
                classification = 'excess'
            elif excess_qty > future_demand * 0.2:
                classification = 'watch'
            else:
                classification = 'normal'

            eo_analysis.append({
                'part_number': part_number,
                'on_hand_qty': on_hand_qty,
                'future_demand_12m': future_demand,
                'excess_qty': excess_qty,
                'excess_value': excess_value,
                'unit_cost': unit_cost,
                'lifecycle_status': lifecycle_status,
                'months_since_use': months_since_use,
                'classification': classification,
                'recommended_action': self._recommend_action(
                    classification, excess_qty, excess_value
                )
            })

        return pd.DataFrame(eo_analysis)

    def _calculate_future_demand(self, part_number, months):
        """Calculate future demand for component"""

        # Get products using this part
        products_using = self.bom[self.bom['part_number'] == part_number]

        total_demand = 0
        for _, product in products_using.iterrows():
            product_id = product['product_id']
            qty_per_unit = product['quantity_per_unit']

            # Get forecast for product
            product_forecast = self.forecast[
                self.forecast['product_id'] == product_id
            ]['forecast_units'].sum() if len(
                self.forecast[self.forecast['product_id'] == product_id]
            ) > 0 else 0

            total_demand += product_forecast * qty_per_unit

        return total_demand

    def _recommend_action(self, classification, excess_qty, excess_value):
        """Recommend disposition action"""

        if classification == 'obsolete':
            if excess_value > 50000:
                return 'scrap_with_recovery_value_analysis'
            else:
                return 'scrap_dispose'
        elif classification == 'excess':
            if excess_value > 100000:
                return 'sell_to_brokers_or_redistribute'
            elif excess_value > 10000:
                return 'return_to_supplier_negotiation'
            else:
                return 'consume_in_production_if_possible'
        elif classification == 'watch':
            return 'monitor_and_reduce_future_buys'
        else:
            return 'no_action_required'

    def calculate_eo_provision(self, eo_analysis):
        """
        Calculate accounting provision for E&O inventory

        Returns:
        - provision amount by category
        """

        provision_rates = {
            'normal': 0.0,
            'watch': 0.25,
            'excess': 0.50,
            'obsolete': 1.0
        }

        eo_analysis['provision_rate'] = eo_analysis['classification'].map(provision_rates)
        eo_analysis['provision_amount'] = (
            eo_analysis['excess_value'] * eo_analysis['provision_rate']
        )

        total_provision = eo_analysis['provision_amount'].sum()

        summary = eo_analysis.groupby('classification').agg({
            'excess_qty': 'sum',
            'excess_value': 'sum',
            'provision_amount': 'sum'
        })

        return {
            'total_provision': total_provision,
            'summary_by_classification': summary
        }


# Example would require full inventory, BOM, and forecast data
```

---

## Product Lifecycle Management

### New Product Introduction (NPI) Planning

```python
class NPIManager:
    """
    Manage New Product Introduction process for electronics
    """

    def __init__(self):
        self.npi_phases = [
            'concept',
            'design',
            'prototype',
            'pilot',
            'ramp',
            'mass_production'
        ]

    def create_npi_timeline(self, product_spec, target_launch_date):
        """
        Create NPI timeline with key milestones

        Parameters:
        - product_spec: product specifications
        - target_launch_date: desired production start

        Returns:
        - detailed timeline with activities
        """

        # Standard phase durations (weeks)
        phase_durations = {
            'concept': 4,
            'design': 12,
            'prototype': 8,
            'pilot': 6,
            'ramp': 8,
            'mass_production': 0  # ongoing
        }

        # Adjust for product complexity
        complexity_factor = product_spec.get('complexity_factor', 1.0)

        timeline = []
        current_date = target_launch_date

        # Work backwards from launch
        for phase in reversed(self.npi_phases[:-1]):
            duration_weeks = phase_durations[phase] * complexity_factor
            phase_start = current_date - timedelta(weeks=duration_weeks)

            timeline.append({
                'phase': phase,
                'start_date': phase_start,
                'end_date': current_date,
                'duration_weeks': duration_weeks,
                'key_activities': self._get_phase_activities(phase),
                'deliverables': self._get_phase_deliverables(phase)
            })

            current_date = phase_start

        # Reverse to chronological order
        timeline.reverse()

        return pd.DataFrame(timeline)

    def _get_phase_activities(self, phase):
        """Get key activities for NPI phase"""

        activities = {
            'concept': ['Market research', 'Feature definition', 'Cost target'],
            'design': ['Schematic design', 'PCB layout', 'Component selection',
                      'DFM review'],
            'prototype': ['Prototype build', 'Functional testing', 'Design validation'],
            'pilot': ['Pilot run 100-500 units', 'Process validation',
                     'Supplier qualification'],
            'ramp': ['Ramp to volume', 'Yield optimization', 'Cost reduction']
        }

        return activities.get(phase, [])

    def _get_phase_deliverables(self, phase):
        """Get deliverables for NPI phase"""

        deliverables = {
            'concept': ['Product requirements document', 'Cost model'],
            'design': ['Final schematic', 'Gerber files', 'BOM', 'AVL'],
            'prototype': ['Working prototypes', 'Test reports', 'Design changes'],
            'pilot': ['Pilot build report', 'Qualified suppliers', 'Manufacturing docs'],
            'ramp': ['Volume production', 'Quality metrics', 'Cost targets met']
        }

        return deliverables.get(phase, [])

    def assess_component_risk_npi(self, bom_df, components_df):
        """
        Assess component risks for NPI

        Focus on:
        - Long lead time parts
        - Sole source components
        - Lifecycle risks
        - Allocation risks
        """

        risks = []

        for idx, component in bom_df.iterrows():
            part_number = component['part_number']

            # Get component details
            comp_info = components_df[
                components_df['part_number'] == part_number
            ].iloc[0]

            # Risk factors
            risk_factors = []
            risk_score = 0

            # Lead time risk
            if comp_info['lead_time_weeks'] > 26:
                risk_factors.append('long_lead_time_>6months')
                risk_score += 30

            # Sole source risk
            if comp_info.get('alternate_sources', 0) == 0:
                risk_factors.append('sole_source')
                risk_score += 25

            # Lifecycle risk
            if comp_info.get('lifecycle_status') == 'nrnd':
                risk_factors.append('not_recommended_for_new_design')
                risk_score += 40

            # Allocation risk
            if comp_info.get('allocation_status') in ['allocated', 'critical']:
                risk_factors.append('allocated_part')
                risk_score += 35

            risks.append({
                'part_number': part_number,
                'manufacturer': comp_info['manufacturer'],
                'risk_score': risk_score,
                'risk_factors': risk_factors,
                'mitigation_required': risk_score > 50
            })

        return pd.DataFrame(risks).sort_values('risk_score', ascending=False)
```

---

## Tools & Libraries

### Python Libraries

**Supply Chain Optimization:**
- `pulp`: Linear programming for allocation optimization
- `pyomo`: Advanced optimization modeling
- `networkx`: Supply network analysis

**Data Analysis:**
- `pandas`: Data manipulation and BOM management
- `numpy`: Numerical computations
- `scipy`: Statistical analysis

**Visualization:**
- `matplotlib`, `seaborn`: Charts and graphs
- `plotly`: Interactive dashboards
- `networkx` + `matplotlib`: Supply network visualization

### Commercial Software

**ERP/MRP Systems:**
- **SAP S/4HANA**: Enterprise resource planning
- **Oracle ERP Cloud**: Cloud ERP for manufacturing
- **Microsoft Dynamics 365**: Supply chain management
- **IFS Applications**: Manufacturing and supply chain

**Component Management:**
- **Arena PLM**: Product lifecycle management
- **SiliconExpert**: Component lifecycle and compliance
- **Z2Data**: Supply chain intelligence
- **Supplyframe**: Component sourcing and intelligence

**Contract Manufacturing:**
- **Aligni**: Electronics inventory and BOM management
- **PLM systems**: PTC Windchill, Siemens Teamcenter, Dassault ENOVIA

**Supplier Collaboration:**
- **E2open**: Multi-tier supply chain visibility
- **Kinaxis RapidResponse**: Supply chain planning
- **Blue Yonder**: Supply chain suite

---

## Common Challenges & Solutions

### Challenge: Component Allocation & Shortages

**Problem:**
- Critical components on allocation (semiconductors, displays, connectors)
- Unable to secure required quantities
- Long lead times (26-52 weeks)
- Spot market prices 5-10x normal

**Solutions:**
- **Demand aggregation**: Consolidate forecasts to increase volumes
- **Strategic relationships**: Achieve preferred customer status with suppliers
- **Long-term agreements**: Commit to capacity with multi-year contracts
- **Design for availability**: Use readily available components in design phase
- **Authorized distributors**: Build relationships with franchise distributors
- **Alternate sourcing**: Qualify second sources during design
- **Buffer inventory**: Strategic stock of long lead-time parts
- **Allocation tracking**: Real-time monitoring of allocation status

### Challenge: Rapid Product Obsolescence

**Problem:**
- Component lifecycles shorter than product lifecycles
- Last-time-buy decisions difficult
- End-of-life (EOL) component management
- Redesign costs high

**Solutions:**
- **Lifecycle monitoring**: Track component lifecycle status continuously
- **Proactive obsolescence management**: 3-5 year lookout
- **Last-time-buy calculations**: Model remaining demand accurately
- **Design for longevity**: Select components with long lifecycles
- **Component standardization**: Reduce unique part count
- **Emulation/drop-in replacements**: Identify compatible alternatives
- **Escrow inventory**: Hold strategic stock for long-tail service demand

### Challenge: Managing Multiple EMS Providers

**Problem:**
- Coordinating 3-5 contract manufacturers globally
- Inconsistent quality and processes
- IP protection concerns
- Difficult to shift volumes

**Solutions:**
- **Standardized processes**: Implement common quality standards
- **Golden unit approach**: Reference builds for consistency
- **Regular audits**: Quarterly manufacturing site audits
- **Dual tooling**: Maintain tools at multiple sites for flexibility
- **IP controls**: NDA, controlled BOM access, design segmentation
- **Transparent costing**: Open-book pricing models
- **Volume balancing**: Strategic allocation based on capabilities

### Challenge: Counterfeit Component Risk

**Problem:**
- Counterfeit ICs in supply chain (especially gray market)
- Quality and reliability issues
- Brand and safety risks
- Difficult to detect

**Solutions:**
- **Authorized sources only**: Purchase from franchise distributors
- **Supplier qualification**: Strict vetting of sources
- **Testing protocols**: Incoming inspection and X-ray analysis
- **Traceability**: Full chain of custody documentation
- **Anti-counterfeit technologies**: Use of authentication chips/labels
- **Vendor audits**: Regular supplier facility inspections
- **Market monitoring**: Track gray market activity

### Challenge: Global Supply Chain Disruption

**Problem:**
- Geopolitical risks (China-Taiwan tensions)
- Natural disasters (earthquakes, tsunamis)
- Pandemic impacts
- Port congestion and logistics delays

**Solutions:**
- **Geographic diversification**: Multi-region manufacturing
- **Nearshoring**: Shift some production closer to demand
- **Safety stock strategies**: Higher inventory for critical parts
- **Dual sourcing**: Multiple suppliers and regions
- **Supply chain visibility**: Real-time tracking tools
- **Scenario planning**: Model disruption scenarios
- **Air freight capacity**: Reserved capacity for emergencies

---

## Output Format

### Electronics Supply Chain Report

**Executive Summary:**
- Product portfolio overview
- Critical component status
- Supply chain risk level
- Key initiatives and investments

**Component Risk Dashboard:**

| Part Number | Manufacturer | Allocation Status | Lead Time | Inventory | Shortfall | Risk Level |
|-------------|--------------|-------------------|-----------|-----------|-----------|------------|
| IC_STM32F4 | STMicro | Allocated | 32 wks | 10,000 | 15,000 | Critical |
| PMIC_TPS65 | TI | Critical | 52 wks | 0 | 25,000 | Critical |
| LCD_7inch | BOE | Watch | 16 wks | 8,000 | 0 | Medium |
| MLCC_10uF | Murata | Open | 8 wks | 50,000 | 0 | Low |

**Supply Chain Performance:**

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| On-Time Delivery | 87% | 95% | ⚠ Yellow |
| Component PPM | 120 | <100 | ⚠ Yellow |
| E&O Inventory | $2.8M | <$2M | ⚠ Yellow |
| Inventory Turns | 6.2 | 8.0 | ⚠ Yellow |
| Allocation Parts | 45 | <20 | ⚠ Yellow |

**NPI Status:**

| Product | Phase | Start Date | Launch Date | Status | Critical Risks |
|---------|-------|------------|-------------|--------|----------------|
| PROD_A | Pilot | 2025-01-15 | 2025-04-01 | On Track | IC allocation |
| PROD_B | Design | 2025-02-01 | 2025-08-01 | Delayed | Display EOL |
| PROD_C | Ramp | 2024-12-01 | 2025-03-01 | On Track | None |

**E&O Inventory:**

| Classification | Parts Count | Quantity | Value | Provision |
|----------------|-------------|----------|-------|-----------|
| Obsolete | 234 | 45,000 | $890K | $890K |
| Excess | 456 | 128,000 | $1.8M | $900K |
| Watch | 678 | 234,000 | $2.1M | $525K |
| **Total** | **1,368** | **407,000** | **$4.79M** | **$2.32M** |

**Action Items:**
1. Escalate STM32 allocation to executive level - engage VP Supply Chain
2. Complete last-time-buy for EOL display - approve $1.2M purchase
3. Qualify alternate PMIC supplier - complete by Q2 2025
4. Implement component lifecycle monitoring tool - evaluate SiliconExpert
5. Reduce E&O inventory to <$2M - broker sales and returns program

---

## Questions to Ask

If you need more context:
1. What type of electronics products? (consumer, industrial, automotive, medical)
2. Manufacturing model? (internal, EMS/ODM, hybrid)
3. What are the critical components causing issues?
4. What's the current allocation situation?
5. What are lead times for long lead-time parts?
6. How much E&O inventory currently?
7. What's the product lifecycle stage? (NPI, mature, end-of-life)
8. Geographic manufacturing footprint?

---

## Related Skills

- **production-scheduling**: For manufacturing scheduling
- **capacity-planning**: For production capacity management
- **inventory-optimization**: For component inventory policies
- **supplier-selection**: For EMS and component supplier selection
- **supplier-risk-management**: For supply continuity
- **quality-management**: For manufacturing quality and PPM tracking
- **demand-forecasting**: For component demand planning
- **procurement-optimization**: For component purchasing optimization
- **network-design**: For global supply network optimization
- **risk-mitigation**: For supply chain risk management
