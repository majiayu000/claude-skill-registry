---
name: aerospace-supply-chain
description: When the user wants to optimize aerospace and defense supply chains, manage long lead-time components, handle MRO operations, or ensure AS9100 compliance. Also use when the user mentions "aerospace supply chain," "aviation manufacturing," "MRO supply chain," "AS9100," "aircraft parts," "defense procurement," "AOG support," "airworthiness," "ITAR compliance," "aerospace certification," or "aviation aftermarket." For general manufacturing, see production-scheduling. For quality, see quality-management.
---

# Aerospace Supply Chain

You are an expert in aerospace and defense supply chain management, aviation manufacturing operations, and MRO (Maintenance, Repair, Overhaul) logistics. Your goal is to help optimize complex multi-tier supply networks, manage long lead-time components, ensure regulatory compliance, and support both OEM production and aftermarket operations.

## Initial Assessment

Before optimizing aerospace supply chains, understand:

1. **Business Segment**
   - Industry sector? (commercial aviation, defense, space, business jets)
   - OEM or supplier tier? (Tier 1, 2, 3 supplier vs. OEM)
   - Product type? (airframes, engines, avionics, interiors, structures)
   - New production vs. aftermarket vs. MRO?
   - Government vs. commercial customers?

2. **Product & Program Complexity**
   - Aircraft platforms served? (737, A320, F-35, etc.)
   - Product lifecycle stage? (development, production, mature, legacy)
   - Production rate? (aircraft per month, engines per year)
   - Customization level? (standard, options, fully custom)
   - Part count and BOM depth? (assemblies, components, raw materials)

3. **Supply Chain Structure**
   - Number of suppliers by tier?
   - Geographic footprint? (domestic, global, strategic regions)
   - Sole source vs. multiple source?
   - Vertical integration level?
   - Outsourcing strategy? (make vs. buy)

4. **Regulatory & Quality**
   - Quality standards? (AS9100, AS9110, AS9120, Nadcap)
   - Certifications required? (FAA, EASA, military specs)
   - Export controls? (ITAR, EAR, defense articles)
   - Traceability requirements? (serialization, lot tracking)
   - Counterfeit part prevention?

---

## Aerospace Supply Chain Framework

### Value Chain Structure

**Aerospace Manufacturing Ecosystem:**

```
Raw Materials (Titanium, Composites, Aluminum, Special Alloys)
  ↓
Tier 3 Suppliers (Basic parts, fasteners, raw stock)
  ↓
Tier 2 Suppliers (Components, sub-assemblies)
  ↓
Tier 1 Suppliers (Major systems, integrated assemblies)
  ↓
OEMs (Aircraft Manufacturers)
  ├─ Boeing, Airbus, Lockheed Martin, Northrop Grumman
  ├─ Embraer, Bombardier, Gulfstream
  └─ Pratt & Whitney, GE Aviation, Rolls-Royce (engines)
  ↓
Airlines / Military / Operators
  ↓
MRO Providers
  ↓
Parts Distributors / Aftermarket
```

**Key Industry Players:**

- **OEMs**: Boeing, Airbus, Lockheed Martin, Northrop Grumman, BAE Systems
- **Tier 1**: Spirit AeroSystems, Collins Aerospace, Safran, Honeywell
- **Engines**: GE Aviation, Pratt & Whitney, Rolls-Royce, CFM International
- **MRO**: Lufthansa Technik, ST Engineering, AAR Corp, StandardAero

---

## Long Lead-Time Component Management

### Critical Path Analysis & Planning

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import networkx as nx

class AerospaceProgramPlanner:
    """
    Manage long lead-time aerospace program planning
    """

    def __init__(self, aircraft_program):
        """
        Initialize program planner

        Parameters:
        - aircraft_program: program details (platform, rate, start date)
        """
        self.program = aircraft_program

    def analyze_critical_path(self, bom_df, supplier_lead_times):
        """
        Analyze critical path for aircraft production

        Parameters:
        - bom_df: Bill of Materials with assembly tree
        - supplier_lead_times: lead times by part number

        Returns:
        - critical path analysis with longest lead time items
        """

        # Build assembly dependency graph
        G = nx.DiGraph()

        for idx, part in bom_df.iterrows():
            part_number = part['part_number']
            parent = part.get('parent_assembly', 'FINAL_ASSEMBLY')

            # Get lead time
            lead_time_weeks = supplier_lead_times.get(part_number, 52)

            G.add_node(part_number, lead_time=lead_time_weeks)
            G.add_edge(parent, part_number)

        # Calculate critical path
        critical_items = []

        for part in bom_df['part_number']:
            # Find longest path from this part to final assembly
            try:
                path_length = nx.shortest_path_length(
                    G, source=part, target='FINAL_ASSEMBLY'
                )

                # Cumulative lead time
                path = nx.shortest_path(G, source=part, target='FINAL_ASSEMBLY')
                cumulative_lt = sum(G.nodes[p].get('lead_time', 0) for p in path)

                critical_items.append({
                    'part_number': part,
                    'lead_time_weeks': G.nodes[part].get('lead_time', 0),
                    'levels_to_assembly': path_length,
                    'cumulative_lead_time_weeks': cumulative_lt,
                    'is_critical_path': cumulative_lt > 52  # >1 year
                })
            except:
                pass

        critical_analysis = pd.DataFrame(critical_items).sort_values(
            'cumulative_lead_time_weeks', ascending=False
        )

        return critical_analysis

    def calculate_procurement_schedule(self, production_schedule, critical_items):
        """
        Calculate when to order long lead-time components

        Parameters:
        - production_schedule: aircraft delivery schedule
        - critical_items: parts with cumulative lead times

        Returns:
        - procurement schedule by part
        """

        procurement_schedule = []

        for idx, aircraft in production_schedule.iterrows():
            delivery_date = aircraft['delivery_date']
            tail_number = aircraft['tail_number']
            quantity = aircraft.get('quantity', 1)

            for _, item in critical_items.iterrows():
                part_number = item['part_number']
                cumulative_lt_weeks = item['cumulative_lead_time_weeks']

                # Add safety buffer (typically 4-8 weeks)
                safety_buffer_weeks = 8

                total_lt_weeks = cumulative_lt_weeks + safety_buffer_weeks

                # Calculate order date
                order_date = delivery_date - timedelta(weeks=total_lt_weeks)

                procurement_schedule.append({
                    'tail_number': tail_number,
                    'part_number': part_number,
                    'delivery_date': delivery_date,
                    'order_date': order_date,
                    'lead_time_weeks': cumulative_lt_weeks,
                    'safety_buffer_weeks': safety_buffer_weeks,
                    'days_until_order': (order_date - datetime.now()).days,
                    'urgency': self._classify_urgency(
                        (order_date - datetime.now()).days
                    )
                })

        return pd.DataFrame(procurement_schedule).sort_values('order_date')

    def _classify_urgency(self, days_until_order):
        """Classify procurement urgency"""
        if days_until_order < 0:
            return 'overdue'
        elif days_until_order < 30:
            return 'urgent'
        elif days_until_order < 90:
            return 'normal'
        else:
            return 'future'

    def manage_production_rate_change(self, current_rate, target_rate,
                                     inventory_position, lead_times):
        """
        Manage supply chain through production rate changes

        Parameters:
        - current_rate: current aircraft per month
        - target_rate: target aircraft per month
        - inventory_position: current inventory levels
        - lead_times: component lead times

        Returns:
        - transition plan with inventory adjustments
        """

        rate_change_pct = (target_rate - current_rate) / current_rate

        transition_plan = {
            'current_rate_per_month': current_rate,
            'target_rate_per_month': target_rate,
            'rate_change_pct': rate_change_pct * 100,
            'transition_duration_months': abs(rate_change_pct) * 12,  # Longer for bigger changes
            'inventory_actions': []
        }

        # Determine inventory actions
        if rate_change_pct > 0:
            # Rate increase - need more inventory
            transition_plan['inventory_actions'] = [
                'increase_safety_stock_by_25pct',
                'advance_long_lead_orders_by_4_weeks',
                'negotiate_supplier_capacity_increases',
                'pre_build_inventory_for_critical_parts',
                'dual_source_bottleneck_components'
            ]

            # Calculate inventory investment needed
            avg_part_value = 50000  # Placeholder
            parts_per_aircraft = 500000
            months_of_buffer = 2

            additional_inventory_value = (
                (target_rate - current_rate) * months_of_buffer *
                parts_per_aircraft * avg_part_value / parts_per_aircraft
            )

            transition_plan['inventory_investment_usd'] = additional_inventory_value

        else:
            # Rate decrease - reduce inventory
            transition_plan['inventory_actions'] = [
                'reduce_safety_stock_gradually',
                'defer_non_critical_orders',
                'negotiate_supplier_volume_reductions',
                'assess_excess_and_obsolete_risk',
                'slow_down_receipts_timing'
            ]

            # Calculate potential excess
            months_of_excess = abs(rate_change_pct) * 6

            excess_inventory_risk = (
                (current_rate - target_rate) * months_of_excess * 100000
            )

            transition_plan['excess_inventory_risk_usd'] = excess_inventory_risk

        return transition_plan


# Example usage
program = {'name': 'Narrow_Body_Program', 'platform': 'A320', 'rate_per_month': 50}

bom = pd.DataFrame({
    'part_number': ['WING_ASSY', 'FUSELAGE', 'ENGINE_1', 'LANDING_GEAR'],
    'parent_assembly': ['FINAL_ASSEMBLY', 'FINAL_ASSEMBLY', 'FINAL_ASSEMBLY', 'FINAL_ASSEMBLY']
})

lead_times = {
    'WING_ASSY': 78,  # 18 months
    'FUSELAGE': 52,   # 12 months
    'ENGINE_1': 104,  # 24 months
    'LANDING_GEAR': 65  # 15 months
}

planner = AerospaceProgramPlanner(program)
critical_path = planner.analyze_critical_path(bom, lead_times)

print("Critical Path Analysis:")
print(critical_path[['part_number', 'lead_time_weeks', 'cumulative_lead_time_weeks', 'is_critical_path']])
```

---

## AS9100 Quality Management

### Quality & Certification Management

```python
class AerospaceQualityManager:
    """
    Manage AS9100 quality and aerospace certification requirements
    """

    def __init__(self):
        self.quality_standards = {
            'AS9100': 'Quality management for aviation/space/defense',
            'AS9110': 'Quality for MRO organizations',
            'AS9120': 'Quality for distributors/stockists',
            'Nadcap': 'Special process accreditation (heat treat, NDT, etc.)'
        }

    def assess_supplier_quality(self, supplier_details):
        """
        Assess supplier quality capabilities and certifications

        Parameters:
        - supplier_details: supplier info and certifications

        Returns:
        - quality assessment and approval status
        """

        required_certs = supplier_details.get('required_certifications', [])
        actual_certs = supplier_details.get('current_certifications', [])

        assessment = {
            'supplier': supplier_details['name'],
            'supplier_type': supplier_details.get('type', 'component'),
            'certifications_required': required_certs,
            'certifications_held': actual_certs,
            'gaps': list(set(required_certs) - set(actual_certs)),
            'quality_score': 0,
            'approved': False
        }

        # Check certifications
        if 'AS9100' in required_certs:
            if 'AS9100' in actual_certs:
                assessment['quality_score'] += 40
            else:
                assessment['gaps'].append('AS9100_required')

        # Check special process accreditations
        special_processes = supplier_details.get('special_processes', [])

        for process in special_processes:
            if process in ['heat_treat', 'welding', 'NDT', 'plating']:
                if 'Nadcap' in actual_certs:
                    assessment['quality_score'] += 20
                else:
                    assessment['gaps'].append(f'Nadcap_{process}')

        # Check performance history
        ppb_defects = supplier_details.get('ppb_defects', 0)  # Parts per billion

        if ppb_defects < 100:
            assessment['quality_score'] += 20
        elif ppb_defects < 500:
            assessment['quality_score'] += 10

        # On-time delivery
        otd_pct = supplier_details.get('otd_performance', 0)

        if otd_pct >= 95:
            assessment['quality_score'] += 20
        elif otd_pct >= 90:
            assessment['quality_score'] += 10

        # Approval decision
        if assessment['quality_score'] >= 70 and len(assessment['gaps']) == 0:
            assessment['approved'] = True
            assessment['status'] = 'approved'
        elif assessment['quality_score'] >= 50:
            assessment['approved'] = False
            assessment['status'] = 'conditional_pending_improvements'
        else:
            assessment['approved'] = False
            assessment['status'] = 'not_approved'

        return assessment

    def manage_first_article_inspection(self, part_details):
        """
        Manage First Article Inspection (FAI) process per AS9102

        Parameters:
        - part_details: part specifications and requirements

        Returns:
        - FAI checklist and requirements
        """

        fai_requirements = {
            'part_number': part_details['part_number'],
            'drawing_revision': part_details['drawing_revision'],
            'supplier': part_details['supplier'],
            'inspection_required': True,
            'as9102_forms': ['Form 1', 'Form 2', 'Form 3'],
            'inspection_plan': []
        }

        # Form 1: Part number accountability
        fai_requirements['inspection_plan'].append({
            'form': 'AS9102_Form_1',
            'description': 'Part number accountability and traceability',
            'items': [
                'Verify part number matches drawing',
                'Verify drawing revision',
                'Document material certifications',
                'Record manufacturing lot/batch'
            ]
        })

        # Form 2: Product accountability
        fai_requirements['inspection_plan'].append({
            'form': 'AS9102_Form_2',
            'description': 'Product accountability',
            'items': [
                'List all characteristics from drawing',
                'Identify critical and key characteristics',
                'Document measurement methods',
                'Record actual measurements'
            ]
        })

        # Form 3: Characteristic accountability
        characteristic_count = part_details.get('characteristic_count', 50)

        fai_requirements['inspection_plan'].append({
            'form': 'AS9102_Form_3',
            'description': f'Characteristic verification ({characteristic_count} characteristics)',
            'items': [
                'Measure all dimensional characteristics',
                'Verify material properties',
                'Confirm surface finish requirements',
                'Validate special processes (heat treat, plating, etc.)',
                'Photograph critical features'
            ]
        })

        # Additional requirements for critical parts
        if part_details.get('flight_critical', False):
            fai_requirements['additional_requirements'] = [
                'Witness inspection by customer',
                'Non-destructive testing (NDT)',
                'Material test reports from mill',
                'Certificate of Conformance',
                'Special packaging requirements'
            ]

        return fai_requirements

    def track_quality_metrics(self, supplier_performance_data):
        """
        Track aerospace supplier quality metrics

        Parameters:
        - supplier_performance_data: delivery and quality records

        Returns:
        - quality scorecard
        """

        metrics = {}

        for supplier_id, data in supplier_performance_data.items():
            # Calculate PPB (parts per billion defects)
            total_parts = data['parts_delivered']
            defective_parts = data['parts_rejected']

            ppb = (defective_parts / total_parts * 1_000_000_000
                  if total_parts > 0 else 0)

            # OTD (on-time delivery)
            otd_pct = (data['on_time_deliveries'] / data['total_deliveries'] * 100
                      if data['total_deliveries'] > 0 else 0)

            # Corrective actions
            open_cars = data.get('open_corrective_actions', 0)

            # Overall score
            quality_score = (
                (100 - min(ppb / 10, 50)) * 0.4 +  # PPB component (max 50 pts)
                otd_pct * 0.4 +  # OTD component (max 40 pts)
                (10 if open_cars == 0 else 0) * 0.2  # CAR component (max 20 pts)
            )

            metrics[supplier_id] = {
                'ppb_defects': ppb,
                'otd_performance_pct': otd_pct,
                'open_corrective_actions': open_cars,
                'quality_score': quality_score,
                'rating': self._classify_supplier_rating(quality_score)
            }

        return metrics

    def _classify_supplier_rating(self, score):
        """Classify supplier rating"""
        if score >= 90:
            return 'platinum'
        elif score >= 80:
            return 'gold'
        elif score >= 70:
            return 'silver'
        else:
            return 'needs_improvement'


# Example
qm = AerospaceQualityManager()

supplier = {
    'name': 'Precision_Machining_Inc',
    'type': 'machining',
    'required_certifications': ['AS9100', 'Nadcap'],
    'current_certifications': ['AS9100', 'Nadcap', 'ISO9001'],
    'special_processes': ['heat_treat'],
    'ppb_defects': 85,
    'otd_performance': 96
}

assessment = qm.assess_supplier_quality(supplier)
print(f"Supplier Assessment: {assessment['status']}")
print(f"Quality Score: {assessment['quality_score']}/100")
```

---

## MRO (Maintenance, Repair, Overhaul) Supply Chain

### AOG (Aircraft on Ground) Support

```python
class MROSupplyChain:
    """
    Manage MRO supply chain and AOG support
    """

    def __init__(self, parts_inventory, distribution_network):
        self.inventory = parts_inventory
        self.network = distribution_network

    def handle_aog_request(self, aog_request):
        """
        Handle Aircraft on Ground emergency request

        AOG = highest priority, aircraft cannot fly without part

        Parameters:
        - aog_request: urgent part request details

        Returns:
        - fulfillment plan with fastest option
        """

        part_number = aog_request['part_number']
        quantity = aog_request['quantity']
        aircraft_location = aog_request['aircraft_location']
        aircraft_type = aog_request['aircraft_type']
        tail_number = aog_request['tail_number']

        # Search inventory across network
        available_inventory = self.inventory[
            self.inventory['part_number'] == part_number
        ]

        fulfillment_options = []

        for idx, inv in available_inventory.iterrows():
            if inv['serviceable_quantity'] >= quantity:
                # Calculate delivery time
                distance_miles = self._calculate_distance(
                    inv['location'], aircraft_location
                )

                # Delivery options
                if distance_miles < 50:
                    delivery_method = 'ground_courier'
                    delivery_hours = 2
                    cost = 200
                elif distance_miles < 500:
                    delivery_method = 'regional_air_freight'
                    delivery_hours = 6
                    cost = 1500
                else:
                    delivery_method = 'dedicated_charter'
                    delivery_hours = 12
                    cost = 15000

                fulfillment_options.append({
                    'source_location': inv['location'],
                    'part_number': part_number,
                    'quantity_available': inv['serviceable_quantity'],
                    'delivery_method': delivery_method,
                    'estimated_delivery_hours': delivery_hours,
                    'cost_usd': cost,
                    'priority': 'AOG'
                })

        # Select fastest option
        if len(fulfillment_options) > 0:
            best_option = min(fulfillment_options,
                            key=lambda x: x['estimated_delivery_hours'])

            fulfillment_plan = {
                'aog_request_id': aog_request.get('request_id'),
                'tail_number': tail_number,
                'part_number': part_number,
                'status': 'confirmed',
                'fulfillment_option': best_option,
                'estimated_aircraft_downtime_hours': best_option['estimated_delivery_hours'] + 2,  # +2 for installation
                'total_cost_usd': best_option['cost_usd'],
                'dispatch_time': datetime.now(),
                'estimated_delivery_time': datetime.now() + timedelta(
                    hours=best_option['estimated_delivery_hours']
                )
            }
        else:
            # No inventory available - need to escalate
            fulfillment_plan = {
                'status': 'not_available',
                'escalation_actions': [
                    'search_alternative_sources',
                    'check_rotable_pool_at_other_bases',
                    'contact_OEM_for_priority_shipment',
                    'arrange_aircraft_ferry_to_maintenance_base',
                    'borrow_from_another_aircraft_if_MEL_allows'
                ],
                'priority': 'critical'
            }

        return fulfillment_plan

    def _calculate_distance(self, loc1, loc2):
        """Calculate distance between locations (simplified)"""
        # Simplified - would use geocoding in practice
        return np.random.randint(50, 2000)

    def optimize_rotable_pool(self, rotable_components, maintenance_schedule):
        """
        Optimize rotable component pool sizing

        Rotables = expensive parts that are repaired and reused
        Examples: landing gear, APUs, hydraulic pumps

        Parameters:
        - rotable_components: list of rotable parts
        - maintenance_schedule: when components need replacement

        Returns:
        - optimal pool size by component
        """

        pool_sizing = []

        for component in rotable_components:
            part_number = component['part_number']
            fleet_size = component['fleet_size']
            mtbr_hours = component['mean_time_between_removal']  # Flying hours
            repair_turnaround_days = component['repair_turnaround_days']
            avg_daily_utilization_hours = component.get('avg_daily_utilization', 8)

            # Calculate removal rate
            removals_per_year = (fleet_size * 365 * avg_daily_utilization_hours
                               / mtbr_hours)

            # Pipeline inventory
            # Parts in repair at any given time
            avg_repairs_in_progress = (removals_per_year / 365) * repair_turnaround_days

            # Safety stock for demand variability
            demand_std = removals_per_year * 0.2  # 20% variability
            service_level_z = 1.96  # 97.5% service level
            safety_stock = service_level_z * demand_std / np.sqrt(365 / repair_turnaround_days)

            # Total pool size
            recommended_pool_size = int(np.ceil(avg_repairs_in_progress + safety_stock))

            # Cost analysis
            unit_cost = component.get('unit_cost_usd', 100000)
            repair_cost = component.get('repair_cost_usd', 20000)

            total_investment = recommended_pool_size * unit_cost
            annual_repair_cost = removals_per_year * repair_cost

            pool_sizing.append({
                'part_number': part_number,
                'description': component.get('description'),
                'fleet_size': fleet_size,
                'removals_per_year': removals_per_year,
                'avg_repairs_in_progress': avg_repairs_in_progress,
                'safety_stock': safety_stock,
                'recommended_pool_size': recommended_pool_size,
                'total_investment_usd': total_investment,
                'annual_repair_cost_usd': annual_repair_cost,
                'cost_per_flying_hour': annual_repair_cost / (fleet_size * 365 * avg_daily_utilization_hours)
            })

        return pd.DataFrame(pool_sizing)

    def manage_shelf_life_limited_parts(self, inventory_df):
        """
        Manage shelf-life limited aerospace parts

        Many aerospace parts have shelf life limits (rubber, chemicals, etc.)

        Parameters:
        - inventory_df: inventory with shelf life dates

        Returns:
        - parts requiring action
        """

        current_date = datetime.now()

        shelf_life_analysis = []

        for idx, part in inventory_df.iterrows():
            if part.get('has_shelf_life', False):
                manufacture_date = part.get('manufacture_date')
                shelf_life_months = part.get('shelf_life_months', 60)

                expiry_date = manufacture_date + timedelta(
                    days=shelf_life_months * 30
                )

                remaining_days = (expiry_date - current_date).days

                # Classify action needed
                if remaining_days < 0:
                    action = 'expired_scrap_or_retest'
                    priority = 'immediate'
                elif remaining_days < 180:  # 6 months
                    action = 'use_immediately_or_extend_if_allowed'
                    priority = 'high'
                elif remaining_days < 365:  # 1 year
                    action = 'monitor_and_plan_usage'
                    priority = 'medium'
                else:
                    action = 'no_action_required'
                    priority = 'low'

                shelf_life_analysis.append({
                    'part_number': part['part_number'],
                    'lot_number': part['lot_number'],
                    'manufacture_date': manufacture_date,
                    'expiry_date': expiry_date,
                    'remaining_days': remaining_days,
                    'quantity': part['quantity'],
                    'value_usd': part['quantity'] * part.get('unit_cost', 0),
                    'action': action,
                    'priority': priority
                })

        return pd.DataFrame(shelf_life_analysis).sort_values('remaining_days')


# Example
inventory = pd.DataFrame({
    'part_number': ['GEAR_001', 'PUMP_002', 'SEAL_003'],
    'location': ['NYC', 'LAX', 'DFW'],
    'serviceable_quantity': [2, 1, 5]
})

network = {'locations': ['NYC', 'LAX', 'DFW', 'ORD', 'ATL']}

mro = MROSupplyChain(inventory, network)

aog = {
    'request_id': 'AOG_20250126_001',
    'part_number': 'GEAR_001',
    'quantity': 1,
    'aircraft_location': 'BOS',
    'aircraft_type': 'B737',
    'tail_number': 'N12345'
}

fulfillment = mro.handle_aog_request(aog)
print(f"AOG Status: {fulfillment['status']}")
if fulfillment['status'] == 'confirmed':
    print(f"Delivery Method: {fulfillment['fulfillment_option']['delivery_method']}")
    print(f"Estimated Delivery: {fulfillment['fulfillment_option']['estimated_delivery_hours']} hours")
```

---

## Export Control & Security

### ITAR & EAR Compliance

```python
class ExportControlManager:
    """
    Manage ITAR and export control compliance
    """

    def __init__(self):
        self.itar_categories = [
            'Category_I_Firearms',
            'Category_VIII_Aircraft',
            'Category_XI_Military_Electronics',
            # ... others
        ]

    def classify_part_export_control(self, part_details):
        """
        Classify part for export control

        Parameters:
        - part_details: part specifications and use

        Returns:
        - export classification
        """

        classification = {
            'part_number': part_details['part_number'],
            'description': part_details.get('description'),
            'export_classification': None,
            'license_required': False,
            'restricted_countries': [],
            'handling_requirements': []
        }

        # Determine if ITAR or EAR
        if part_details.get('defense_article', False):
            # ITAR - defense articles
            classification['export_classification'] = 'ITAR'
            classification['itar_category'] = part_details.get(
                'itar_category', 'Category_VIII_Aircraft'
            )
            classification['license_required'] = True
            classification['restricted_countries'] = 'all_except_exempted'
            classification['handling_requirements'] = [
                'marked_as_ITAR_controlled',
                'stored_in_secure_area',
                'access_restricted_to_US_persons',
                'export_requires_State_Dept_license',
                'technology_transfer_controlled'
            ]

        elif part_details.get('dual_use', False):
            # EAR - dual use (commercial + military application)
            classification['export_classification'] = 'EAR'
            classification['eccn'] = part_details.get('eccn', '9A991')  # ECCN code
            classification['license_required'] = self._requires_ear_license(
                part_details.get('eccn'), part_details.get('destination_country')
            )
            classification['restricted_countries'] = self._get_restricted_countries_ear()
            classification['handling_requirements'] = [
                'determine_ECCN_classification',
                'screen_denied_parties_list',
                'check_destination_country_restrictions',
                'maintain_export_records_5_years'
            ]

        else:
            # EAR99 - not specifically controlled
            classification['export_classification'] = 'EAR99'
            classification['license_required'] = False
            classification['restricted_countries'] = ['embargoed_countries']
            classification['handling_requirements'] = [
                'screen_denied_parties_list',
                'embargo_country_checks'
            ]

        return classification

    def _requires_ear_license(self, eccn, destination):
        """Determine if EAR license required (simplified)"""
        # Simplified logic - actual rules are complex
        restricted_eccns = ['9A610', '9A991', '9D610']

        return eccn in restricted_eccns

    def _get_restricted_countries_ear(self):
        """Get EAR restricted countries"""
        return ['Cuba', 'Iran', 'North Korea', 'Syria', 'Crimea']

    def screen_transaction(self, transaction_details):
        """
        Screen export transaction for compliance

        Parameters:
        - transaction_details: party, destination, items

        Returns:
        - screening result
        """

        screening_result = {
            'transaction_id': transaction_details.get('id'),
            'customer': transaction_details['customer'],
            'destination_country': transaction_details['destination'],
            'cleared': True,
            'screening_checks': []
        }

        # Check denied parties lists
        denied_lists = [
            'Denied_Persons_List',
            'Entity_List',
            'Specially_Designated_Nationals',
            'Unverified_List'
        ]

        customer_name = transaction_details['customer']

        # Simplified screening (would use actual databases)
        for denied_list in denied_lists:
            screening_result['screening_checks'].append({
                'list': denied_list,
                'result': 'no_match'  # Placeholder
            })

        # Check destination country
        destination = transaction_details['destination']

        if destination in self._get_restricted_countries_ear():
            screening_result['cleared'] = False
            screening_result['screening_checks'].append({
                'check': 'destination_country',
                'result': 'restricted_requires_license'
            })

        # Check end use
        end_use = transaction_details.get('end_use')

        prohibited_uses = ['military', 'nuclear', 'missile']

        if end_use in prohibited_uses and destination not in ['US', 'UK', 'Australia']:
            screening_result['cleared'] = False
            screening_result['screening_checks'].append({
                'check': 'end_use',
                'result': 'prohibited_end_use'
            })

        return screening_result


# Example
ecm = ExportControlManager()

part = {
    'part_number': 'AVIONICS_001',
    'description': 'Military avionics system',
    'defense_article': True,
    'itar_category': 'Category_XI_Military_Electronics'
}

classification = ecm.classify_part_export_control(part)
print(f"Export Classification: {classification['export_classification']}")
print(f"License Required: {classification['license_required']}")
print(f"Handling Requirements: {classification['handling_requirements']}")
```

---

## Tools & Libraries

### Python Libraries

**Supply Chain Optimization:**
- `pulp`: Linear programming for production planning
- `networkx`: Supply network and critical path analysis
- `scipy`: Statistical analysis

**Data Analysis:**
- `pandas`: Data manipulation and BOM management
- `numpy`: Numerical computations
- `matplotlib`: Visualization

**Project Management:**
- `python-gantt`: Gantt chart generation for programs
- `criticalpath`: Critical path method implementation

### Commercial Software

**ERP/MRP Systems:**
- **SAP S/4HANA Aerospace & Defense**: Industry-specific ERP
- **Oracle E-Business Suite Aerospace & Defense**: ERP with compliance
- **IFS Applications**: Aerospace and defense manufacturing
- **Infor CloudSuite Aerospace & Defense**: Industry cloud ERP

**PLM (Product Lifecycle Management):**
- **Siemens Teamcenter**: PLM for aerospace
- **Dassault ENOVIA**: PLM and collaboration
- **PTC Windchill**: PLM with configuration management
- **Aras Innovator**: PLM for complex products

**MRO Systems:**
- **IFS Maintenix**: Aviation MRO software
- **Ramco Aviation**: Comprehensive MRO suite
- **Swiss-AS AMOS**: Aircraft maintenance software
- **Quantum Control**: MRO and inventory management

**Supply Chain:**
- **Blue Yonder**: Demand and supply planning
- **Kinaxis RapidResponse**: S&OP for aerospace
- **E2open**: Multi-tier visibility
- **Exostar**: Aerospace supply chain collaboration

**Quality Management:**
- **ETQ Reliance**: AS9100 quality management
- **MasterControl**: Quality and compliance
- **Sparta Systems TrackWise**: CAPA and quality events

---

## Common Challenges & Solutions

### Challenge: Extremely Long Lead Times

**Problem:**
- Component lead times 12-36 months
-难以forecast demand 2-3 years out
- Production rate changes impact pipeline
- Cash tied up in WIP inventory

**Solutions:**
- **Advanced procurement**: Order components 24-36 months ahead
- **Supplier partnerships**: Long-term agreements with capacity commitments
- **Risk pooling**: Share components across programs where possible
- **Digital twins**: Model pipeline inventory dynamically
- **Flexible contracts**: Options for quantity adjustments
- **Safety stock strategies**: Strategic inventory for long-lead items
- **Supplier development**: Help suppliers reduce lead times

### Challenge: Sole Source Suppliers

**Problem:**
- Many parts have single qualified source
- High supplier leverage
- Supply disruption risk
- Limited negotiating power

**Solutions:**
- **Dual sourcing**: Qualify second source for critical parts
- **Vertical integration**: Bring critical capabilities in-house
- **Strategic inventory**: Higher safety stock for sole-source parts
- **Supplier monitoring**: Financial health tracking
- **Escrow arrangements**: Protect access to critical tooling/IP
- **Long-term agreements**: Lock in capacity and pricing
- **Alternative designs**: Design alternate parts where feasible

### Challenge: Counterfeit Parts

**Problem:**
- Counterfeit parts entering supply chain
- Safety and airworthiness risk
- Difficult to detect
- Liability exposure

**Solutions:**
- **Authorized sources only**: Purchase from OCM or authorized distributors
- **Supplier vetting**: Strict qualification and audits
- **Part inspection**: Incoming inspection with testing
- **Traceability**: Complete chain of custody documentation
- **Anti-counterfeit tech**: Use of blockchain, RFID, authentication chips
- **Training**: Educate procurement on red flags
- **Industry cooperation**: Share information through GIDEP, ERAI

### Challenge: AS9100 Compliance Complexity

**Problem:**
- Extensive quality documentation requirements
- First article inspections time-consuming
- Supplier non-compliance issues
- Audit findings and CARs

**Solutions:**
- **Digital quality systems**: Automate FAI and quality records
- **Supplier development**: Train suppliers on AS9100 requirements
- **Risk-based approach**: Focus resources on flight-critical parts
- **Pre-qualification**: Audit suppliers before award
- **Continuous improvement**: Regular internal audits
- **Lessons learned**: Database of quality issues and solutions
- **Certification support**: Help key suppliers achieve AS9100

### Challenge: Export Control Complexity

**Problem:**
- ITAR and EAR regulations complex
- Penalties for violations severe ($1M+ fines)
- Technology transfer restrictions
- Global supply chain conflicts with controls

**Solutions:**
- **Classification**: Properly classify all parts (ITAR, EAR, EAR99)
- **Compliance training**: Regular training for employees
- **Screening tools**: Automated denied party screening
- **Access controls**: Physical and system access restrictions
- **License management**: Track export licenses and approvals
- **Legal counsel**: Export control attorneys on staff
- **Segregation**: Separate ITAR from commercial operations
- **Documentation**: Maintain detailed export records

---

## Output Format

### Aerospace Supply Chain Report

**Executive Summary:**
- Program status (aircraft in production, backlog)
- Supply chain performance metrics
- Quality and compliance status
- Major risks and mitigation

**Program Production:**

| Program | Aircraft Type | Rate/Month | Backlog | Next Delivery | Critical Path Item |
|---------|---------------|------------|---------|---------------|--------------------|
| Program_A | B737 MAX | 31 | 450 | Feb 15 | Landing gear |
| Program_B | A320neo | 45 | 520 | Feb 10 | Engines |
| Program_C | F-35 | 12 | 185 | Mar 1 | Avionics |

**Long Lead-Time Components:**

| Part Number | Description | Lead Time | Order Date | Delivery | Status | Risk |
|-------------|-------------|-----------|------------|----------|--------|------|
| ENG_001 | Turbine engine | 104 wks | Ordered | Jun 2025 | On track | Low |
| GEAR_002 | Landing gear | 78 wks | Overdue | Apr 2025 | Late | High |
| WING_003 | Wing assembly | 65 wks | Ordered | May 2025 | On track | Medium |

**Quality Performance:**

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Supplier PPB Defects | 95 | <100 | ✓ Green |
| On-Time Delivery | 89% | 95% | ⚠ Yellow |
| AS9100 Compliance | 100% | 100% | ✓ Green |
| First Article Pass Rate | 87% | 90% | ⚠ Yellow |
| Open CARs | 12 | <10 | ⚠ Yellow |

**MRO Performance:**

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| AOG Response Time | 8 hrs | <12 hrs | ✓ Green |
| Parts Availability | 94% | 95% | ⚠ Yellow |
| Rotable Pool Adequacy | 97% | 95% | ✓ Green |
| Repair TAT | 35 days | 30 days | ⚠ Yellow |

**Export Control Status:**

| Category | Count | Notes |
|----------|-------|-------|
| ITAR Parts | 1,250 | All properly marked and controlled |
| EAR Parts | 3,400 | ECCN classification complete |
| Export Licenses Active | 45 | All current, monitored monthly |
| Denied Party Screens | 100% | Automated screening in place |

**Action Items:**
1. Escalate landing gear supplier (GEAR_002) - 2 weeks late, impacting Program A
2. Qualify second source for turbine blade forgings - reduce sole source risk
3. Complete AS9100 audit prep for Supplier_X - audit scheduled March 15
4. Implement AOG inventory at Asia Pacific hub - improve 12hr response in region
5. Close 12 open CARs - target completion by end of quarter

---

## Questions to Ask

If you need more context:
1. What aerospace segment? (commercial aviation, defense, space, business jets)
2. OEM or supplier tier level? (Tier 1, 2, 3, or OEM)
3. What products/assemblies are manufactured?
4. Production vs. aftermarket vs. MRO?
5. What quality standards apply? (AS9100, AS9110, AS9120, Nadcap)
6. Any export control requirements? (ITAR, EAR)
7. What are the current lead times for critical parts?
8. What are the main supply chain challenges?

---

## Related Skills

- **production-scheduling**: For manufacturing scheduling
- **capacity-planning**: For production capacity management
- **quality-management**: For AS9100 and quality systems
- **supplier-selection**: For supplier qualification
- **supplier-risk-management**: For supply continuity
- **inventory-optimization**: For safety stock and rotable pools
- **procurement-optimization**: For purchasing optimization
- **demand-forecasting**: For production planning
- **network-design**: For distribution network optimization
- **compliance-management**: For regulatory compliance
- **risk-mitigation**: For supply chain risk management
