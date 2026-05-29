---
name: automotive-supply-chain
description: When the user wants to optimize automotive manufacturing supply chains, manage tier suppliers, implement JIT production, or handle automotive-specific logistics. Also use when the user mentions "automotive manufacturing," "OEM supply chain," "tier 1/2/3 suppliers," "sequenced parts delivery," "just-in-time automotive," "vehicle assembly," or "automotive aftermarket." For general manufacturing, see production-scheduling. For lean principles, see lean-manufacturing.
---

# Automotive Supply Chain

You are an expert in automotive supply chain management and manufacturing operations. Your goal is to help optimize complex multi-tier supply networks, implement just-in-time delivery, manage supplier relationships, and ensure efficient vehicle assembly operations.

## Initial Assessment

Before optimizing automotive supply chains, understand:

1. **Manufacturing Context**
   - OEM, Tier 1, Tier 2, or Tier 3 supplier?
   - Product types? (vehicles, engines, transmissions, components)
   - Production volume? (high-volume, low-volume, custom)
   - Manufacturing approach? (make-to-stock, make-to-order, configure-to-order)
   - Number of platforms/models?

2. **Supply Chain Structure**
   - How many tier suppliers?
   - Geographic footprint? (local, regional, global)
   - Sole source vs. multi-source strategy?
   - In-house vs. outsourced components?
   - Vertical integration level?

3. **Current State**
   - Inventory turns?
   - Supplier quality metrics (PPM defects)?
   - On-time delivery performance?
   - Line stoppage frequency?
   - Supply chain costs as % of revenue?

4. **Business Drivers**
   - Cost reduction targets?
   - New model launches?
   - Electrification strategy (EV transition)?
   - Reshoring or nearshoring plans?
   - Sustainability goals?

---

## Automotive Supply Chain Framework

### Tier Structure

**Multi-Tier Supplier Network:**

```
OEM (Vehicle Manufacturer)
  ↑
Tier 1 (System Integrators)
  ↑ ↑ ↑
Tier 2 (Component Suppliers)
  ↑ ↑ ↑ ↑
Tier 3 (Raw Materials, Basic Parts)
```

**Tier Definitions:**

- **OEM (Original Equipment Manufacturer)**: Ford, GM, Toyota, VW, Tesla
  - Final vehicle assembly
  - Design and engineering
  - Brand ownership
  - Dealer network management

- **Tier 1 Suppliers**: Bosch, Continental, Denso, Magna
  - Major systems and modules (seats, cockpit, powertrain)
  - Direct delivery to OEM assembly lines
  - Often sequenced or just-in-time
  - Design and engineering capability

- **Tier 2 Suppliers**: Component manufacturers
  - Individual parts and subassemblies
  - Supply to Tier 1
  - More standardized products
  - Limited design input

- **Tier 3 Suppliers**: Raw materials and commodities
  - Steel, aluminum, plastics, electronics
  - Supply to Tier 2 (sometimes Tier 1)
  - Highly commoditized

---

## Just-In-Time (JIT) and Sequencing

### JIT Delivery Model

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class AutomotiveJITScheduler:
    """
    Manage Just-In-Time delivery schedules for automotive assembly
    """

    def __init__(self, assembly_schedule, takt_time_minutes):
        """
        Initialize JIT scheduler

        Parameters:
        - assembly_schedule: vehicle build schedule
        - takt_time_minutes: time per vehicle (e.g., 60 seconds = 1 vehicle/min)
        """
        self.assembly_schedule = assembly_schedule
        self.takt_time = takt_time_minutes

    def calculate_part_requirements(self, bom_df):
        """
        Calculate part requirements based on assembly schedule

        Parameters:
        - bom_df: Bill of Materials with parts per vehicle

        Returns:
        - time-phased part requirements
        """

        requirements = []

        for idx, vehicle in self.assembly_schedule.iterrows():
            build_time = vehicle['scheduled_time']
            model = vehicle['model']
            vin = vehicle['vin']

            # Get BOM for this model
            model_bom = bom_df[bom_df['model'] == model]

            for _, part in model_bom.iterrows():
                requirements.append({
                    'vin': vin,
                    'model': model,
                    'part_number': part['part_number'],
                    'quantity': part['quantity_per_vehicle'],
                    'required_time': build_time,
                    'supplier': part['supplier'],
                    'delivery_lead_time_hours': part['delivery_lead_time_hours']
                })

        return pd.DataFrame(requirements)

    def generate_supplier_call_off(self, part_requirements, buffer_hours=2):
        """
        Generate supplier call-off schedule (when to deliver each part)

        Parameters:
        - part_requirements: parts needed with timing
        - buffer_hours: safety buffer before assembly need

        Returns:
        - supplier delivery schedule
        """

        call_offs = []

        # Group by supplier and part
        grouped = part_requirements.groupby(['supplier', 'part_number'])

        for (supplier, part_number), group in grouped:
            # Sort by required time
            group = group.sort_values('required_time')

            # Determine delivery frequency
            lead_time = group['delivery_lead_time_hours'].iloc[0]

            # Calculate delivery windows
            for idx, row in group.iterrows():
                required_time = row['required_time']
                delivery_time = required_time - timedelta(hours=lead_time + buffer_hours)

                call_offs.append({
                    'supplier': supplier,
                    'part_number': part_number,
                    'vin': row['vin'],
                    'quantity': row['quantity'],
                    'delivery_time': delivery_time,
                    'required_time': required_time,
                    'dock_door': self._assign_dock_door(supplier)
                })

        call_off_df = pd.DataFrame(call_offs)

        return call_off_df.sort_values('delivery_time')

    def _assign_dock_door(self, supplier):
        """Assign dock door based on supplier"""
        # Simplified: hash supplier name to dock door
        return (hash(supplier) % 20) + 1  # 20 dock doors

    def calculate_lineside_inventory(self, call_offs, consumption_rate):
        """
        Calculate lineside inventory levels

        Parameters:
        - call_offs: delivery schedule
        - consumption_rate: parts consumed per hour

        Returns:
        - inventory profile over time
        """

        # Simulate inventory over time
        inventory_profile = []

        current_inventory = 0
        time_periods = pd.date_range(
            start=call_offs['delivery_time'].min(),
            end=call_offs['required_time'].max(),
            freq='H'
        )

        for t in time_periods:
            # Add deliveries at this time
            deliveries = call_offs[call_offs['delivery_time'] == t]['quantity'].sum()
            current_inventory += deliveries

            # Subtract consumption
            current_inventory -= consumption_rate

            inventory_profile.append({
                'time': t,
                'inventory': max(0, current_inventory),
                'deliveries': deliveries
            })

        return pd.DataFrame(inventory_profile)


# Example usage
assembly_schedule = pd.DataFrame({
    'vin': ['VIN001', 'VIN002', 'VIN003'],
    'model': ['Model_A', 'Model_B', 'Model_A'],
    'scheduled_time': pd.to_datetime([
        '2025-01-20 08:00',
        '2025-01-20 09:00',
        '2025-01-20 10:00'
    ])
})

bom = pd.DataFrame({
    'model': ['Model_A', 'Model_A', 'Model_B'],
    'part_number': ['PART_001', 'PART_002', 'PART_001'],
    'quantity_per_vehicle': [4, 2, 4],
    'supplier': ['Supplier_A', 'Supplier_B', 'Supplier_A'],
    'delivery_lead_time_hours': [4, 2, 4]
})

scheduler = AutomotiveJITScheduler(assembly_schedule, takt_time_minutes=60)
requirements = scheduler.calculate_part_requirements(bom)
call_offs = scheduler.generate_supplier_call_off(requirements, buffer_hours=2)

print("Supplier Call-Off Schedule:")
print(call_offs[['supplier', 'part_number', 'delivery_time', 'quantity']])
```

### Sequenced Parts Delivery

**What is Sequencing?**
- Parts delivered in exact build sequence
- Example: Seats delivered in order 1-2-3 matching VINs
- Eliminates sorting at assembly line
- Requires tight coordination with supplier

```python
class SequencedPartsManager:
    """
    Manage sequenced parts delivery (e.g., seats, cockpits)
    """

    def __init__(self, build_sequence):
        self.build_sequence = build_sequence

    def generate_sequenced_order(self, part_specs):
        """
        Generate sequenced parts order matching build sequence

        Parameters:
        - part_specs: specifications for each vehicle (e.g., seat color/material)

        Returns:
        - sequenced order for supplier
        """

        sequenced_order = []

        for idx, vehicle in self.build_sequence.iterrows():
            vin = vehicle['vin']
            model = vehicle['model']

            # Get part spec for this VIN
            spec = part_specs[part_specs['vin'] == vin].iloc[0]

            sequenced_order.append({
                'sequence_number': idx + 1,
                'vin': vin,
                'model': model,
                'part_spec': spec['specification'],
                'color': spec['color'],
                'material': spec['material'],
                'delivery_time': vehicle['scheduled_time'] - timedelta(hours=2)
            })

        return pd.DataFrame(sequenced_order)

    def validate_sequence(self, delivered_sequence, expected_sequence):
        """
        Validate delivered parts match expected sequence

        Returns:
        - sequence accuracy and errors
        """

        errors = []

        for i, (delivered, expected) in enumerate(zip(delivered_sequence, expected_sequence)):
            if delivered['vin'] != expected['vin']:
                errors.append({
                    'position': i + 1,
                    'expected_vin': expected['vin'],
                    'delivered_vin': delivered['vin'],
                    'error_type': 'sequence_mismatch'
                })

            if delivered['spec'] != expected['spec']:
                errors.append({
                    'position': i + 1,
                    'vin': delivered['vin'],
                    'expected_spec': expected['spec'],
                    'delivered_spec': delivered['spec'],
                    'error_type': 'specification_mismatch'
                })

        accuracy = 1 - (len(errors) / len(expected_sequence))

        return {
            'accuracy_pct': accuracy * 100,
            'errors': errors,
            'error_count': len(errors)
        }
```

---

## Supplier Quality Management

### PPM (Parts Per Million) Defect Tracking

```python
class AutomotiveQualityManager:
    """
    Track supplier quality performance (PPM defects)
    """

    def __init__(self, target_ppm=50):
        """
        Initialize quality manager

        Parameters:
        - target_ppm: target defect rate (parts per million)
        """
        self.target_ppm = target_ppm
        self.quality_data = []

    def record_receipt(self, receipt_data):
        """Record parts receipt and inspection"""
        self.quality_data.append(receipt_data)

    def calculate_supplier_ppm(self, supplier=None, time_period_days=90):
        """
        Calculate PPM for supplier(s)

        Parameters:
        - supplier: specific supplier (None = all)
        - time_period_days: rolling time period

        Returns:
        - PPM metrics by supplier
        """

        df = pd.DataFrame(self.quality_data)

        # Filter time period
        cutoff_date = datetime.now() - timedelta(days=time_period_days)
        df = df[df['receipt_date'] >= cutoff_date]

        # Filter supplier if specified
        if supplier:
            df = df[df['supplier'] == supplier]

        # Calculate PPM by supplier
        supplier_ppm = df.groupby('supplier').agg({
            'quantity_received': 'sum',
            'quantity_defective': 'sum'
        })

        supplier_ppm['ppm'] = (
            supplier_ppm['quantity_defective'] /
            supplier_ppm['quantity_received'] * 1000000
        )

        supplier_ppm['meets_target'] = supplier_ppm['ppm'] <= self.target_ppm

        return supplier_ppm.sort_values('ppm', ascending=False)

    def identify_quality_issues(self):
        """Identify suppliers with quality problems"""

        ppm_data = self.calculate_supplier_ppm()

        critical_suppliers = ppm_data[ppm_data['ppm'] > self.target_ppm * 3]
        warning_suppliers = ppm_data[
            (ppm_data['ppm'] > self.target_ppm) &
            (ppm_data['ppm'] <= self.target_ppm * 3)
        ]

        return {
            'critical_suppliers': critical_suppliers,
            'warning_suppliers': warning_suppliers,
            'total_suppliers': len(ppm_data),
            'compliant_suppliers': len(ppm_data[ppm_data['meets_target']]),
            'compliance_rate': len(ppm_data[ppm_data['meets_target']]) / len(ppm_data) * 100
        }

    def generate_corrective_action(self, supplier, issue_description):
        """Generate corrective action request (CAR)"""

        car = {
            'car_id': f"CAR_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'supplier': supplier,
            'issue_date': datetime.now(),
            'issue_description': issue_description,
            'current_ppm': self.calculate_supplier_ppm(supplier)['ppm'].iloc[0],
            'target_ppm': self.target_ppm,
            'required_actions': [
                'Root cause analysis within 48 hours',
                'Containment plan immediate',
                'Corrective action plan within 1 week',
                'Effectiveness validation within 30 days'
            ],
            'status': 'open'
        }

        return car


# Example
qm = AutomotiveQualityManager(target_ppm=50)

# Record receipts
qm.record_receipt({
    'receipt_date': datetime.now() - timedelta(days=10),
    'supplier': 'Supplier_A',
    'part_number': 'PART_001',
    'quantity_received': 10000,
    'quantity_defective': 3
})

qm.record_receipt({
    'receipt_date': datetime.now() - timedelta(days=5),
    'supplier': 'Supplier_B',
    'part_number': 'PART_002',
    'quantity_received': 5000,
    'quantity_defective': 8
})

ppm = qm.calculate_supplier_ppm()
print("Supplier PPM:")
print(ppm)

issues = qm.identify_quality_issues()
print(f"\nCompliance Rate: {issues['compliance_rate']:.0f}%")
```

---

## EV Supply Chain Considerations

### Electric Vehicle Transition

**Supply Chain Differences:**

**Traditional ICE (Internal Combustion Engine) Vehicle:**
- ~30,000 parts
- Complex powertrain (engine, transmission, exhaust)
- Mature supplier base
- Established processes

**Electric Vehicle (EV):**
- ~20,000 parts (simpler)
- Battery pack (40-50% of vehicle cost)
- Electric motors and inverters
- New supplier base
- Battery supply chain critical

```python
class EVSupplyChainAnalyzer:
    """
    Analyze EV vs. ICE supply chain differences
    """

    def __init__(self):
        self.ice_bom_cost = 25000  # Average ICE vehicle BOM cost
        self.ev_bom_cost = 35000   # Average EV vehicle BOM cost

    def compare_cost_structures(self):
        """Compare ICE vs. EV cost structures"""

        ice_structure = {
            'powertrain': 0.25,  # 25% - engine, transmission
            'body_chassis': 0.30,
            'electronics': 0.15,
            'interior': 0.20,
            'other': 0.10
        }

        ev_structure = {
            'battery_pack': 0.40,  # 40% - massive cost driver
            'electric_motor': 0.05,
            'power_electronics': 0.10,
            'body_chassis': 0.25,
            'electronics': 0.10,
            'interior': 0.08,
            'other': 0.02
        }

        comparison = pd.DataFrame({
            'ICE_pct': ice_structure,
            'EV_pct': ev_structure,
            'ICE_cost': {k: v * self.ice_bom_cost for k, v in ice_structure.items()},
            'EV_cost': {k: v * self.ev_bom_cost for k, v in ev_structure.items()}
        })

        return comparison

    def analyze_battery_supply_chain(self, battery_capacity_kwh, cell_chemistry='NMC'):
        """
        Analyze battery supply chain requirements

        Parameters:
        - battery_capacity_kwh: battery pack size (kWh)
        - cell_chemistry: NMC (Nickel Manganese Cobalt) or LFP (Lithium Iron Phosphate)

        Returns:
        - material requirements
        """

        # Material requirements per kWh (kg)
        if cell_chemistry == 'NMC':
            materials = {
                'lithium': 0.8,
                'nickel': 1.2,
                'cobalt': 0.2,
                'manganese': 0.3,
                'graphite': 1.0,
                'copper': 1.5,
                'aluminum': 2.0
            }
        elif cell_chemistry == 'LFP':
            materials = {
                'lithium': 0.6,
                'iron': 1.0,
                'phosphate': 0.8,
                'graphite': 1.0,
                'copper': 1.2,
                'aluminum': 1.8
            }

        # Calculate total materials
        total_materials = {
            material: amount * battery_capacity_kwh
            for material, amount in materials.items()
        }

        # Estimate costs ($/kg)
        material_costs = {
            'lithium': 30,
            'nickel': 18,
            'cobalt': 35,
            'manganese': 2,
            'iron': 0.50,
            'phosphate': 1.50,
            'graphite': 8,
            'copper': 9,
            'aluminum': 2.5
        }

        total_material_cost = sum(
            total_materials.get(mat, 0) * cost
            for mat, cost in material_costs.items()
        )

        return {
            'battery_capacity_kwh': battery_capacity_kwh,
            'cell_chemistry': cell_chemistry,
            'materials_kg': total_materials,
            'material_cost': total_material_cost,
            'cost_per_kwh': total_material_cost / battery_capacity_kwh
        }


# Example
analyzer = EVSupplyChainAnalyzer()

cost_comparison = analyzer.compare_cost_structures()
print("Cost Structure Comparison:")
print(cost_comparison)

battery_analysis = analyzer.analyze_battery_supply_chain(
    battery_capacity_kwh=75,
    cell_chemistry='NMC'
)

print(f"\nBattery Materials for 75 kWh pack:")
print(f"Lithium: {battery_analysis['materials_kg']['lithium']:.1f} kg")
print(f"Total Material Cost: ${battery_analysis['material_cost']:,.0f}")
print(f"Cost per kWh: ${battery_analysis['cost_per_kwh']:.0f}")
```

---

## Automotive-Specific Performance Metrics

### Key Performance Indicators

```python
class AutomotiveKPITracker:
    """
    Track automotive supply chain KPIs
    """

    def __init__(self):
        self.kpis = {}

    def calculate_inventory_turns(self, annual_cogs, avg_inventory):
        """Inventory turnover (target: 15-20 for automotive)"""
        turns = annual_cogs / avg_inventory
        self.kpis['inventory_turns'] = turns
        return turns

    def calculate_dock_to_dock_time(self, total_cycle_time_hours):
        """Dock-to-dock time (supplier dock to customer dock)"""
        self.kpis['dock_to_dock_hours'] = total_cycle_time_hours
        return total_cycle_time_hours

    def calculate_otd(self, on_time_deliveries, total_deliveries):
        """On-Time Delivery (target: >99%)"""
        otd = on_time_deliveries / total_deliveries * 100
        self.kpis['otd_pct'] = otd
        return otd

    def calculate_line_stoppage_rate(self, stoppages, production_hours):
        """Line stoppages per 1000 production hours"""
        rate = (stoppages / production_hours) * 1000
        self.kpis['line_stoppage_per_1000hrs'] = rate
        return rate

    def generate_scorecard(self, benchmarks):
        """Generate KPI scorecard with benchmarks"""

        scorecard = []

        for kpi, value in self.kpis.items():
            benchmark = benchmarks.get(kpi, {})

            if 'target' in benchmark:
                if 'higher_better' in benchmark and benchmark['higher_better']:
                    status = 'green' if value >= benchmark['target'] else 'red'
                else:
                    status = 'green' if value <= benchmark['target'] else 'red'
            else:
                status = 'unknown'

            scorecard.append({
                'kpi': kpi,
                'actual': value,
                'target': benchmark.get('target', 'N/A'),
                'status': status
            })

        return pd.DataFrame(scorecard)


# Example
tracker = AutomotiveKPITracker()

tracker.calculate_inventory_turns(annual_cogs=50000000, avg_inventory=2500000)
tracker.calculate_otd(on_time_deliveries=9950, total_deliveries=10000)
tracker.calculate_line_stoppage_rate(stoppages=5, production_hours=2000)

benchmarks = {
    'inventory_turns': {'target': 15, 'higher_better': True},
    'otd_pct': {'target': 99, 'higher_better': True},
    'line_stoppage_per_1000hrs': {'target': 3, 'higher_better': False}
}

scorecard = tracker.generate_scorecard(benchmarks)
print("Automotive Supply Chain Scorecard:")
print(scorecard)
```

---

## Tools & Technologies

### Automotive Supply Chain Software

**Tier 1 Supplier Management:**
- **SAP Automotive**: Integrated supply chain for automotive
- **Oracle E-Business Suite**: Automotive-specific modules
- **Kinaxis RapidResponse**: S&OP for automotive
- **Blue Yonder**: Supply chain planning and execution
- **Coupa Supply Chain Design**: Network optimization

**Supplier Collaboration:**
- **SupplyOn**: Automotive supplier network (BMW, VW, Continental)
- **Elemica**: Supply chain collaboration
- **E2open**: Multi-tier visibility
- **Llamasoft**: Supply chain modeling

**Quality Management:**
- **IQMS**: Manufacturing ERP with quality
- **TrackWise**: Quality and compliance
- **MasterControl**: Supplier quality management
- **ETQ Reliance**: CAPA and quality

### Python Libraries

```python
# Supply chain optimization
from pulp import *
import pyomo.environ as pyo

# Data analysis
import pandas as pd
import numpy as np

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Machine learning for forecasting
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
```

---

## Common Challenges & Solutions

### Challenge: Single-Source Supply Risk

**Problem:**
- Critical part from single supplier
- Plant shutdown if supplier fails
- High negotiating leverage for supplier

**Solutions:**
- Dual-source strategy (at least 30/70 split)
- Safety stock for critical parts
- Supplier financial monitoring
- Contract manufacturing agreements
- Vertical integration for critical components

### Challenge: Long Lead Times for New Tools/Dies

**Problem:**
- Tooling lead times 6-12 months
- Delays new model launches
- High capital costs

**Solutions:**
- Early supplier involvement (ESI)
- Concurrent engineering
- Rapid prototyping and testing
- Modular tooling design
- Digital simulation before physical tooling

### Challenge: Managing 1,000+ Suppliers

**Problem:**
- Complexity managing multi-tier network
- Lack of visibility to Tier 2/3
- Quality issues from sub-tier

**Solutions:**
- Supplier tiering and segmentation
- Multi-tier visibility platforms
- Supplier scorecards and audits
- Supplier development programs
- Strategic supplier reductions (consolidation)

### Challenge: EV Battery Supply Constraints

**Problem:**
- Limited battery cell production capacity
- Competition for lithium, cobalt, nickel
- Price volatility
- Geographic concentration (China)

**Solutions:**
- Long-term supply agreements (offtake contracts)
- Vertical integration (own battery plants)
- Diversify cell suppliers and chemistries
- Recycling programs (circular economy)
- Alternative chemistries (LFP, solid-state)

---

## Output Format

### Automotive Supply Chain Report

**Executive Summary:**
- Plant: Detroit Assembly (Model A, Model B)
- Daily Production: 1,000 vehicles
- Tier 1 Suppliers: 120
- Inventory Turns: 18.5 (target: 15+)
- OTD Performance: 98.5% (target: 99%)
- Quality: 42 PPM (target: <50 PPM)
- Line Stoppages: 2.1 per 1000 hrs (target: <3)

**Supply Chain Performance:**

| Metric | Actual | Target | Status |
|--------|--------|--------|--------|
| Inventory Turns | 18.5 | 15+ | ✓ Green |
| OTD% | 98.5% | 99% | ⚠ Yellow |
| Quality (PPM) | 42 | <50 | ✓ Green |
| Line Stoppages | 2.1 | <3 | ✓ Green |
| Dock-to-Dock Time | 4.2 hrs | <6 hrs | ✓ Green |

**Supplier Quality (Top Issues):**

| Supplier | Part | PPM | Status | Action |
|----------|------|-----|--------|--------|
| Supplier_X | PART_123 | 285 | Critical | CAR issued |
| Supplier_Y | PART_456 | 110 | Warning | Under review |
| Supplier_Z | PART_789 | 45 | Good | Monitor |

**JIT Delivery Performance:**

| Supplier | Deliveries | On-Time | Early | Late | Performance |
|----------|------------|---------|-------|------|-------------|
| Supplier_A | 250 | 248 | 1 | 1 | 99.2% |
| Supplier_B | 180 | 175 | 3 | 2 | 97.2% |
| Supplier_C | 300 | 300 | 0 | 0 | 100% |

**Action Items:**
1. Address Supplier_X quality issue (285 PPM) - CAR in progress
2. Improve OTD from 98.5% to 99% - focus on 3 underperforming suppliers
3. Complete EV battery supplier qualification for Model C launch
4. Implement Tier 2 visibility platform for critical components

---

## Questions to Ask

If you need more context:
1. OEM or Tier 1/2/3 supplier?
2. What products/components are manufactured?
3. Production volume and model complexity?
4. Current supply chain structure and key metrics?
5. JIT delivery in place?
6. Supplier quality performance (PPM)?
7. Any EV products or transition plans?
8. Major supply chain challenges or pain points?

---

## Related Skills

- **production-scheduling**: For assembly line scheduling
- **lean-manufacturing**: For waste elimination and continuous improvement
- **capacity-planning**: For production capacity management
- **supplier-selection**: For supplier evaluation and qualification
- **supplier-risk-management**: For supply continuity
- **quality-management**: For quality systems and SPC
- **inventory-optimization**: For safety stock and inventory policies
- **master-production-scheduling**: For MPS development
- **demand-forecasting**: For production planning
