---
name: track-and-trace
description: When the user wants to implement shipment tracking, product traceability, or supply chain visibility. Also use when the user mentions "tracking," "traceability," "visibility," "serialization," "lot tracking," "batch tracking," "chain of custody," "provenance," "track and trace," or "shipment monitoring." For control towers, see control-tower-design. For compliance, see compliance-management.
---

# Track and Trace

You are an expert in track-and-trace systems and supply chain visibility. Your goal is to help organizations implement end-to-end traceability, real-time tracking, and comprehensive visibility across their supply chains for operational efficiency, compliance, and customer service.

## Initial Assessment

Before implementing track-and-trace, understand:

1. **Business Drivers**
   - What's driving tracking needs? (customer service, compliance, efficiency, recalls)
   - Regulatory requirements? (FDA, EU MDR, FSMA, etc.)
   - Use cases? (shipment tracking, product traceability, asset tracking)
   - Current visibility gaps?

2. **Scope & Granularity**
   - What needs tracking? (shipments, products, assets, components)
   - Level of detail? (pallet, case, unit, serial number)
   - Geographic coverage? (domestic, international)
   - Supply chain depth? (supplier → manufacturer → customer)

3. **Technology Landscape**
   - Existing systems? (ERP, WMS, TMS)
   - Data capture capabilities? (barcodes, RFID, IoT)
   - Integration requirements?
   - Mobile and cloud readiness?

4. **Stakeholder Needs**
   - Internal users? (operations, quality, customer service)
   - External visibility? (customers, suppliers, regulators)
   - Real-time vs. periodic updates?
   - Alert and exception requirements?

---

## Track-and-Trace Framework

### Tracking vs. Tracing

**Tracking (Forward Looking)**
- Where is it now?
- Where is it going?
- When will it arrive?
- Real-time shipment monitoring
- Predictive ETAs
- Exception alerts

**Tracing (Backward Looking)**
- Where did it come from?
- Who handled it?
- What happened to it?
- Genealogy and pedigree
- Recall management
- Chain of custody

### Traceability Levels

**Level 1: Internal Traceability**
- Within single facility
- Batch/lot tracking
- Basic record keeping
- Limited integration

**Level 2: One-Up, One-Down**
- Track immediate supplier and customer
- Basic supply chain visibility
- Compliance minimum (FDA, EU)
- Limited end-to-end view

**Level 3: End-to-End Traceability**
- Full supply chain visibility
- Multi-tier tracking
- Integrated systems
- Comprehensive data

**Level 4: Real-Time Digital Twin**
- Live tracking and monitoring
- IoT and sensors
- Predictive analytics
- Autonomous decisions

**Level 5: Blockchain-Enabled**
- Immutable record
- Multi-party trust
- Smart contracts
- Full provenance

---

## Shipment Tracking System

### Real-Time Shipment Visibility

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class ShipmentTrackingSystem:
    """Real-time shipment tracking and monitoring system"""

    def __init__(self):
        self.shipments = {}
        self.tracking_events = []
        self.exceptions = []
        self.carriers = {}

    def create_shipment(self, shipment_id, origin, destination, carrier,
                       planned_ship_date, planned_delivery_date, contents):
        """
        Create new shipment for tracking

        contents: list of dicts with product and quantity info
        """

        self.shipments[shipment_id] = {
            'shipment_id': shipment_id,
            'origin': origin,
            'destination': destination,
            'carrier': carrier,
            'planned_ship_date': planned_ship_date,
            'planned_delivery_date': planned_delivery_date,
            'actual_ship_date': None,
            'actual_delivery_date': None,
            'current_location': origin,
            'status': 'Created',
            'contents': contents,
            'milestones': [],
            'exceptions': [],
            'created_timestamp': datetime.now()
        }

    def add_tracking_event(self, shipment_id, location, event_type,
                          event_timestamp, notes=''):
        """
        Add tracking event for shipment

        event_type: 'Picked Up', 'In Transit', 'At Hub', 'Out for Delivery',
                   'Delivered', 'Delayed', 'Exception', etc.
        """

        if shipment_id not in self.shipments:
            return None

        event = {
            'shipment_id': shipment_id,
            'location': location,
            'event_type': event_type,
            'event_timestamp': event_timestamp,
            'notes': notes,
            'recorded_timestamp': datetime.now()
        }

        self.tracking_events.append(event)

        # Update shipment
        shipment = self.shipments[shipment_id]
        shipment['current_location'] = location
        shipment['milestones'].append(event)

        # Update status based on event
        if event_type == 'Picked Up':
            shipment['status'] = 'In Transit'
            shipment['actual_ship_date'] = event_timestamp
        elif event_type == 'Delivered':
            shipment['status'] = 'Delivered'
            shipment['actual_delivery_date'] = event_timestamp
        elif event_type in ['Delayed', 'Exception']:
            shipment['status'] = 'Exception'
            self._create_exception(shipment_id, event_type, notes)

        return event

    def _create_exception(self, shipment_id, exception_type, description):
        """Create exception for shipment issue"""

        exception = {
            'shipment_id': shipment_id,
            'exception_type': exception_type,
            'description': description,
            'timestamp': datetime.now(),
            'status': 'Open',
            'resolution': None
        }

        self.exceptions.append(exception)
        self.shipments[shipment_id]['exceptions'].append(exception)

    def calculate_eta(self, shipment_id):
        """
        Calculate estimated time of arrival

        Uses historical performance and current status
        """

        if shipment_id not in self.shipments:
            return None

        shipment = self.shipments[shipment_id]

        if shipment['status'] == 'Delivered':
            return shipment['actual_delivery_date']

        # Use planned date as baseline
        planned_date = shipment['planned_delivery_date']

        # Adjust based on carrier performance (simplified)
        carrier_performance = self._get_carrier_performance(shipment['carrier'])
        avg_delay_days = carrier_performance.get('avg_delay_days', 0)

        # Adjust based on current location and distance
        # (In reality, would use sophisticated routing and timing algorithms)

        if isinstance(planned_date, str):
            planned_date = datetime.strptime(planned_date, '%Y-%m-%d')

        estimated_date = planned_date + timedelta(days=avg_delay_days)

        return {
            'shipment_id': shipment_id,
            'estimated_delivery_date': estimated_date,
            'confidence': 'Medium',  # Would calculate based on data quality
            'days_from_planned': avg_delay_days,
            'current_status': shipment['status']
        }

    def _get_carrier_performance(self, carrier):
        """Get historical carrier performance metrics"""

        # In reality, would query historical database
        # Simplified example

        default_performance = {
            'avg_delay_days': 0,
            'on_time_pct': 90
        }

        return self.carriers.get(carrier, default_performance)

    def get_shipment_status(self, shipment_id):
        """Get current shipment status with full details"""

        if shipment_id not in self.shipments:
            return None

        shipment = self.shipments[shipment_id]

        # Get latest milestone
        latest_milestone = shipment['milestones'][-1] if shipment['milestones'] else None

        # Calculate performance
        performance = self._calculate_performance(shipment)

        return {
            'shipment_id': shipment_id,
            'status': shipment['status'],
            'current_location': shipment['current_location'],
            'origin': shipment['origin'],
            'destination': shipment['destination'],
            'planned_delivery': shipment['planned_delivery_date'],
            'actual_delivery': shipment['actual_delivery_date'],
            'latest_milestone': latest_milestone,
            'total_milestones': len(shipment['milestones']),
            'exceptions_count': len(shipment['exceptions']),
            'performance': performance
        }

    def _calculate_performance(self, shipment):
        """Calculate shipment performance metrics"""

        if shipment['status'] != 'Delivered':
            return {'status': 'In Progress'}

        planned = shipment['planned_delivery_date']
        actual = shipment['actual_delivery_date']

        if isinstance(planned, str):
            planned = datetime.strptime(planned, '%Y-%m-%d')
        if isinstance(actual, str):
            actual = datetime.strptime(actual, '%Y-%m-%d')

        delay_days = (actual - planned).days

        return {
            'status': 'On Time' if delay_days <= 0 else 'Late',
            'delay_days': delay_days,
            'on_time': delay_days <= 0
        }

    def get_in_transit_shipments(self):
        """Get all shipments currently in transit"""

        in_transit = [
            s for s in self.shipments.values()
            if s['status'] in ['In Transit', 'Created']
        ]

        return pd.DataFrame(in_transit) if in_transit else pd.DataFrame()

    def get_exception_shipments(self):
        """Get all shipments with exceptions"""

        exception_shipments = [
            s for s in self.shipments.values()
            if len(s['exceptions']) > 0
        ]

        return pd.DataFrame(exception_shipments) if exception_shipments else pd.DataFrame()

    def generate_tracking_report(self):
        """Generate comprehensive tracking report"""

        total_shipments = len(self.shipments)
        delivered = len([s for s in self.shipments.values() if s['status'] == 'Delivered'])
        in_transit = len([s for s in self.shipments.values() if s['status'] == 'In Transit'])
        exceptions = len([s for s in self.shipments.values() if len(s['exceptions']) > 0])

        # Calculate on-time performance
        delivered_shipments = [s for s in self.shipments.values() if s['status'] == 'Delivered']
        on_time_count = sum(1 for s in delivered_shipments if self._calculate_performance(s).get('on_time', False))
        otd_pct = (on_time_count / delivered * 100) if delivered > 0 else 0

        return {
            'total_shipments': total_shipments,
            'delivered': delivered,
            'in_transit': in_transit,
            'with_exceptions': exceptions,
            'on_time_delivery_pct': round(otd_pct, 1),
            'exception_rate_pct': round(exceptions / total_shipments * 100, 1) if total_shipments > 0 else 0
        }


# Example shipment tracking
tracking_system = ShipmentTrackingSystem()

# Create shipments
tracking_system.create_shipment(
    'SHP001',
    origin='New York, NY',
    destination='Los Angeles, CA',
    carrier='FedEx',
    planned_ship_date='2025-12-10',
    planned_delivery_date='2025-12-15',
    contents=[{'product': 'Widget A', 'quantity': 100}]
)

tracking_system.create_shipment(
    'SHP002',
    origin='Chicago, IL',
    destination='Miami, FL',
    carrier='UPS',
    planned_ship_date='2025-12-11',
    planned_delivery_date='2025-12-14',
    contents=[{'product': 'Widget B', 'quantity': 50}]
)

# Add tracking events
tracking_system.add_tracking_event(
    'SHP001',
    'New York, NY',
    'Picked Up',
    datetime(2025, 12, 10, 8, 30),
    'Package picked up from origin'
)

tracking_system.add_tracking_event(
    'SHP001',
    'Memphis, TN',
    'At Hub',
    datetime(2025, 12, 12, 14, 20),
    'Package at FedEx hub'
)

tracking_system.add_tracking_event(
    'SHP001',
    'Los Angeles, CA',
    'Out for Delivery',
    datetime(2025, 12, 15, 6, 0),
    'Out for delivery'
)

tracking_system.add_tracking_event(
    'SHP001',
    'Los Angeles, CA',
    'Delivered',
    datetime(2025, 12, 15, 14, 30),
    'Delivered to recipient'
)

# Add exception
tracking_system.add_tracking_event(
    'SHP002',
    'Atlanta, GA',
    'Delayed',
    datetime(2025, 12, 13, 10, 0),
    'Weather delay'
)

# Get shipment status
status = tracking_system.get_shipment_status('SHP001')
print(f"Shipment {status['shipment_id']}:")
print(f"  Status: {status['status']}")
print(f"  Current Location: {status['current_location']}")
print(f"  Milestones: {status['total_milestones']}")
print(f"  Performance: {status['performance']['status']}")

# Generate report
report = tracking_system.generate_tracking_report()
print(f"\n\nTracking Report:")
print(f"  Total Shipments: {report['total_shipments']}")
print(f"  In Transit: {report['in_transit']}")
print(f"  With Exceptions: {report['with_exceptions']}")
print(f"  On-Time Delivery: {report['on_time_delivery_pct']}%")
```

---

## Product Traceability System

### Lot/Batch Tracking

```python
class ProductTraceabilitySystem:
    """Product traceability and genealogy tracking system"""

    def __init__(self):
        self.products = {}
        self.lots = {}
        self.movements = []
        self.transformations = []

    def create_lot(self, lot_id, product_id, quantity, manufacturing_date,
                  expiry_date, supplier_id=None, raw_material_lots=None):
        """
        Create lot/batch for traceability

        raw_material_lots: list of input lot IDs (for traceability chain)
        """

        self.lots[lot_id] = {
            'lot_id': lot_id,
            'product_id': product_id,
            'quantity': quantity,
            'manufacturing_date': manufacturing_date,
            'expiry_date': expiry_date,
            'supplier_id': supplier_id,
            'raw_material_lots': raw_material_lots or [],
            'current_location': 'Manufacturing',
            'status': 'Active',
            'movements': [],
            'consumed_in_lots': [],  # Downstream lots
            'created_timestamp': datetime.now()
        }

    def record_movement(self, lot_id, from_location, to_location, quantity,
                       movement_date, movement_type='Transfer'):
        """
        Record lot movement

        movement_type: 'Transfer', 'Sale', 'Return', 'Disposal', etc.
        """

        if lot_id not in self.lots:
            return None

        movement = {
            'lot_id': lot_id,
            'from_location': from_location,
            'to_location': to_location,
            'quantity': quantity,
            'movement_date': movement_date,
            'movement_type': movement_type,
            'recorded_timestamp': datetime.now()
        }

        self.movements.append(movement)
        self.lots[lot_id]['movements'].append(movement)
        self.lots[lot_id]['current_location'] = to_location

        return movement

    def record_transformation(self, input_lots, output_lot, transformation_type,
                            transformation_date, location):
        """
        Record manufacturing transformation (inputs → output)

        input_lots: list of dicts with lot_id and quantity
        output_lot: dict with lot_id, product_id, quantity
        transformation_type: 'Manufacturing', 'Repacking', 'Assembly', etc.
        """

        transformation = {
            'transformation_id': f"TRANS_{len(self.transformations) + 1:06d}",
            'input_lots': input_lots,
            'output_lot': output_lot,
            'transformation_type': transformation_type,
            'transformation_date': transformation_date,
            'location': location,
            'recorded_timestamp': datetime.now()
        }

        self.transformations.append(transformation)

        # Update lot genealogy
        for input_lot in input_lots:
            lot_id = input_lot['lot_id']
            if lot_id in self.lots:
                self.lots[lot_id]['consumed_in_lots'].append(output_lot['lot_id'])

        return transformation

    def trace_forward(self, lot_id):
        """
        Trace forward (where did this lot go?)

        Returns all downstream lots and movements
        """

        if lot_id not in self.lots:
            return None

        lot = self.lots[lot_id]

        forward_trace = {
            'lot_id': lot_id,
            'product_id': lot['product_id'],
            'movements': lot['movements'],
            'consumed_in_lots': lot['consumed_in_lots'],
            'downstream_chain': []
        }

        # Recursively trace downstream
        for downstream_lot_id in lot['consumed_in_lots']:
            if downstream_lot_id in self.lots:
                downstream_trace = self.trace_forward(downstream_lot_id)
                forward_trace['downstream_chain'].append(downstream_trace)

        return forward_trace

    def trace_backward(self, lot_id):
        """
        Trace backward (where did this lot come from?)

        Returns all upstream lots and suppliers
        """

        if lot_id not in self.lots:
            return None

        lot = self.lots[lot_id]

        backward_trace = {
            'lot_id': lot_id,
            'product_id': lot['product_id'],
            'manufacturing_date': lot['manufacturing_date'],
            'supplier_id': lot.get('supplier_id'),
            'raw_materials': [],
            'upstream_chain': []
        }

        # Recursively trace upstream
        for upstream_lot_id in lot.get('raw_material_lots', []):
            if upstream_lot_id in self.lots:
                upstream_trace = self.trace_backward(upstream_lot_id)
                backward_trace['upstream_chain'].append(upstream_trace)

        return backward_trace

    def simulate_recall(self, lot_id):
        """
        Simulate product recall - identify all affected lots and locations

        Critical for food safety, pharmaceuticals, etc.
        """

        # Trace forward to find all impacted lots
        forward_trace = self.trace_forward(lot_id)

        affected_lots = [lot_id]
        locations = set([self.lots[lot_id]['current_location']])

        def collect_downstream(trace):
            for downstream in trace.get('downstream_chain', []):
                affected_lots.append(downstream['lot_id'])
                if downstream['lot_id'] in self.lots:
                    locations.add(self.lots[downstream['lot_id']]['current_location'])
                collect_downstream(downstream)

        collect_downstream(forward_trace)

        # Calculate total quantity affected
        total_quantity = sum(
            self.lots[lid]['quantity'] for lid in affected_lots if lid in self.lots
        )

        return {
            'initiating_lot': lot_id,
            'affected_lots': affected_lots,
            'affected_locations': list(locations),
            'total_lots': len(affected_lots),
            'total_quantity': total_quantity,
            'forward_trace': forward_trace
        }


# Example traceability
traceability = ProductTraceabilitySystem()

# Create raw material lots
traceability.create_lot(
    'RM001',
    product_id='RAW_MATERIAL_A',
    quantity=1000,
    manufacturing_date='2025-11-01',
    expiry_date='2026-11-01',
    supplier_id='SUP001'
)

traceability.create_lot(
    'RM002',
    product_id='RAW_MATERIAL_B',
    quantity=500,
    manufacturing_date='2025-11-05',
    expiry_date='2026-11-05',
    supplier_id='SUP002'
)

# Create finished product lot (using raw materials)
traceability.create_lot(
    'FG001',
    product_id='FINISHED_PRODUCT_X',
    quantity=800,
    manufacturing_date='2025-12-01',
    expiry_date='2027-12-01',
    raw_material_lots=['RM001', 'RM002']
)

# Record transformation
traceability.record_transformation(
    input_lots=[
        {'lot_id': 'RM001', 'quantity': 600},
        {'lot_id': 'RM002', 'quantity': 300}
    ],
    output_lot={'lot_id': 'FG001', 'product_id': 'FINISHED_PRODUCT_X', 'quantity': 800},
    transformation_type='Manufacturing',
    transformation_date='2025-12-01',
    location='Plant A'
)

# Record movements
traceability.record_movement(
    'FG001',
    from_location='Plant A',
    to_location='DC East',
    quantity=800,
    movement_date='2025-12-05',
    movement_type='Transfer'
)

traceability.record_movement(
    'FG001',
    from_location='DC East',
    to_location='Customer XYZ',
    quantity=500,
    movement_date='2025-12-10',
    movement_type='Sale'
)

# Trace backward
backward = traceability.trace_backward('FG001')
print(f"Backward Trace for Lot FG001:")
print(f"  Manufacturing Date: {backward['manufacturing_date']}")
print(f"  Upstream Materials: {len(backward['upstream_chain'])}")

# Simulate recall
recall = traceability.simulate_recall('RM001')
print(f"\n\nRecall Simulation for Lot RM001:")
print(f"  Affected Lots: {recall['total_lots']}")
print(f"  Affected Locations: {recall['affected_locations']}")
print(f"  Total Quantity: {recall['total_quantity']} units")
```

---

## Tools & Libraries

### Python Libraries

**Data Processing:**
- `pandas`: Data manipulation
- `numpy`: Numerical computations
- `sqlalchemy`: Database connections

**APIs & Integration:**
- `requests`: HTTP requests for carrier APIs
- `ftplib`: FTP file transfer
- `paramiko`: SSH/SFTP

**Real-Time:**
- `kafka-python`: Apache Kafka
- `paho-mqtt`: MQTT messaging
- `redis`: Real-time data store

**Blockchain:**
- `web3.py`: Ethereum blockchain
- `hyperledger-fabric-sdk-py`: Hyperledger Fabric

**Visualization:**
- `matplotlib`, `plotly`: Tracking dashboards
- `folium`: Geographic mapping

### Commercial Software

**Shipment Tracking:**
- **project44**: Multi-carrier visibility
- **FourKites**: Real-time shipment tracking
- **Shippeo**: Supply chain visibility
- **ClearMetal**: Predictive logistics visibility
- **Descartes MacroPoint**: Load tracking

**Traceability Platforms:**
- **TraceLink**: Serialization and traceability
- **Optel**: Track and trace solutions
- **rfxcel**: Supply chain traceability
- **IBM Food Trust**: Blockchain traceability
- **SAP Information Collaboration Hub**: Track and trace

**IoT & Sensors:**
- **Tive**: Supply chain visibility sensors
- **Roambee**: Real-time tracking devices
- **Samsara**: IoT platform
- **Zest Labs**: Fresh food tracking

**Blockchain:**
- **IBM Blockchain**: Enterprise blockchain
- **VeChain**: Supply chain blockchain
- **OriginTrail**: Decentralized traceability
- **Morpheus.Network**: Supply chain platform

---

## Common Challenges & Solutions

### Challenge: Data Integration

**Problem:**
- Multiple disparate systems (ERP, WMS, TMS, carrier systems)
- Different data formats and standards
- Real-time vs. batch integration
- API limitations

**Solutions:**
- Middleware/integration platform (MuleSoft, Boomi)
- Standardized data models (GS1, EPCIS)
- API-first architecture
- Event-driven integration
- Master data management
- Phased integration approach

### Challenge: Data Quality & Accuracy

**Problem:**
- Incomplete tracking events
- Delayed updates
- Incorrect locations
- Missing scans

**Solutions:**
- Automated data validation
- Exception reporting and alerts
- Multiple data sources (triangulation)
- IoT sensors for automation
- Training and process discipline
- Data reconciliation processes

### Challenge: Real-Time Performance

**Problem:**
- High volume of tracking events
- Latency in updates
- System performance degradation
- Need for instant visibility

**Solutions:**
- Event-driven architecture (Kafka, MQTT)
- In-memory databases (Redis)
- Caching strategies
- Horizontal scaling
- Edge computing for IoT
- Asynchronous processing

### Challenge: Complexity at Scale

**Problem:**
- Millions of shipments/products
- Multi-tier supply chains
- Global operations
- Combinatorial explosion

**Solutions:**
- Hierarchical tracking (pallet → case → unit)
- Selective tracking (based on value/risk)
- Archive old data
- Distributed systems
- Cloud infrastructure
- Efficient data structures

### Challenge: Supplier/Partner Integration

**Problem:**
- Suppliers lack technology
- Reluctance to share data
- Different standards
- Small partners

**Solutions:**
- Tiered approach (EDI, APIs, portals, email)
- Standardized formats (GS1, EPCIS)
- Incentives for participation
- Technology provision
- Industry collaboration
- Gradual onboarding

### Challenge: Cost Justification

**Problem:**
- High implementation costs
- Ongoing operational costs
- Intangible benefits
- Long payback

**Solutions:**
- Start with pilot (high-value use case)
- Quantify benefits (efficiency, service, compliance)
- Phased investment
- Cloud-based SaaS models
- Shared industry infrastructure
- Compliance as driver

---

## Output Format

### Track-and-Trace Dashboard

**Executive Summary:**
- Total shipments/products tracked
- Tracking performance
- Exceptions and issues
- Key metrics

**Shipment Tracking:**

| Shipment ID | Origin | Destination | Status | Current Location | ETA | Delay | Exceptions |
|-------------|--------|-------------|--------|------------------|-----|-------|------------|
| SHP-10234 | NYC | LAX | In Transit | Memphis Hub | Jan 15 | On Time | None |
| SHP-10235 | CHI | MIA | Delayed | Atlanta | Jan 16 | +2 days | Weather |
| SHP-10236 | SEA | BOS | Exception | Portland | TBD | +5 days | Customs Hold |

**Traceability:**

| Lot/Batch ID | Product | Quantity | Manufacturing Date | Expiry | Current Location | Status |
|--------------|---------|----------|-------------------|--------|------------------|--------|
| LOT-A12345 | Product X | 1,000 | 2025-11-15 | 2027-11-15 | DC East | Active |
| LOT-A12346 | Product X | 800 | 2025-11-20 | 2027-11-20 | Customer ABC | Sold |
| LOT-A12347 | Product X | 500 | 2025-11-25 | 2027-11-25 | Recall | Quarantine |

**Performance Metrics:**

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Shipments Tracked | 15,234 | N/A | ✓ |
| Real-Time Visibility | 98.2% | 95.0% | ✓ Above |
| On-Time Delivery | 91.5% | 92.0% | ⚠ Slightly Below |
| Exception Rate | 4.3% | <5.0% | ✓ On Track |
| Traceability Coverage | 99.8% | 100% | ✓ Near Target |

**Exceptions Summary:**

| Exception Type | Count | Avg Resolution Time | Oldest Open |
|----------------|-------|---------------------|-------------|
| Delay | 127 | 18 hours | 3 days |
| Customs Hold | 23 | 4.2 days | 8 days |
| Damaged | 8 | 2 days | 1 day |
| Lost | 2 | Pending | 12 days |

---

## Questions to Ask

If you need more context:
1. What needs tracking? (shipments, products, assets, components)
2. What level of granularity? (pallet, case, unit, serial)
3. What are the regulatory requirements? (FDA, FSMA, EU MDR)
4. What systems need integration? (ERP, WMS, TMS, carrier systems)
5. Is real-time tracking required or periodic updates sufficient?
6. Who needs visibility? (internal teams, customers, suppliers, regulators)
7. What's the geographic scope? (domestic, international, multi-region)
8. What data capture methods exist? (barcodes, RFID, IoT, manual)
9. Are there recall or compliance scenarios to support?
10. What's the budget and timeline?

---

## Related Skills

- **control-tower-design**: For centralized monitoring and visibility
- **compliance-management**: For regulatory traceability requirements
- **circular-economy**: For reverse logistics tracking
- **supplier-collaboration**: For supplier visibility integration
- **risk-mitigation**: For tracking disruptions and risks
- **freight-optimization**: For transportation visibility
- **route-optimization**: For shipment tracking and optimization
- **quality-management**: For quality traceability
