---
name: control-tower-design
description: When the user wants to design supply chain control towers, implement visibility platforms, or establish centralized monitoring. Also use when the user mentions "control tower," "supply chain visibility," "command center," "control room," "real-time monitoring," "supply chain operations center," "visibility platform," "exception management," or "centralized control." For track-and-trace, see track-and-trace. For collaboration, see supplier-collaboration.
---

# Control Tower Design

You are an expert in supply chain control tower design and implementation. Your goal is to help organizations establish centralized visibility, monitoring, and coordination capabilities to proactively manage supply chain operations and respond rapidly to disruptions.

## Initial Assessment

Before designing a control tower, understand:

1. **Business Drivers**
   - What problems is the control tower solving? (visibility gaps, slow response, inefficiencies)
   - Target benefits? (cost reduction, service improvement, risk mitigation)
   - Triggering events? (disruptions, growth, complexity)
   - Executive sponsorship and budget?

2. **Scope & Coverage**
   - What processes to cover? (planning, execution, logistics, procurement)
   - Geographic coverage? (regional, global)
   - Internal vs. extended (suppliers, partners, customers)?
   - End-to-end or domain-specific?

3. **Current State**
   - Existing visibility capabilities?
   - Data sources and systems? (ERP, TMS, WMS, etc.)
   - Team structure and skills?
   - Performance monitoring processes?

4. **Organizational Readiness**
   - Cross-functional collaboration maturity?
   - Data quality and integration capability?
   - Change management resources?
   - Technology infrastructure?

---

## Control Tower Framework

### Control Tower Types

**1. Planning Control Tower**
- Demand-supply matching
- Production planning coordination
- S&OP process management
- Scenario planning and what-if analysis
- Forecast collaboration

**2. Logistics Control Tower**
- Transportation visibility
- Shipment tracking and monitoring
- Carrier performance management
- Freight spend optimization
- Last-mile delivery coordination

**3. Procurement Control Tower**
- Supplier performance monitoring
- Order tracking (PO to delivery)
- Supplier risk monitoring
- Contract compliance
- Spend analytics

**4. Manufacturing Control Tower**
- Production schedule monitoring
- Material availability tracking
- Quality monitoring
- Equipment performance
- Yield optimization

**5. End-to-End Control Tower**
- Comprehensive supply chain visibility
- Cross-functional coordination
- Integrated exception management
- Multi-tier visibility
- Strategic and operational integration

### Control Tower Maturity Model

**Level 1: Basic Visibility**
- Reactive monitoring
- Manual data collection
- Siloed dashboards
- Limited integration
- Email-based communication

**Level 2: Integrated Monitoring**
- Automated data feeds
- Consolidated dashboards
- Exception alerts
- Basic analytics
- Standard KPIs

**Level 3: Proactive Management**
- Predictive analytics
- Automated workflows
- Root cause analysis
- Performance optimization
- Collaboration tools

**Level 4: Cognitive Operations**
- AI/ML-driven insights
- Prescriptive recommendations
- Automated decision-making
- Self-healing processes
- Continuous optimization

**Level 5: Autonomous Supply Chain**
- Fully automated operations
- Real-time optimization
- Minimal human intervention
- Ecosystem orchestration
- Digital twin integration

---

## Control Tower Design Architecture

### Data Architecture

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class ControlTowerPlatform:
    """Supply Chain Control Tower platform for visibility and monitoring"""

    def __init__(self):
        self.data_sources = {}
        self.orders = []
        self.shipments = []
        self.exceptions = []
        self.kpis = {}
        self.alerts = []

    def register_data_source(self, source_name, source_type, update_frequency,
                           connection_params):
        """
        Register data source for control tower

        source_type: 'ERP', 'TMS', 'WMS', 'MES', 'API', 'EDI', etc.
        update_frequency: minutes between updates
        """

        self.data_sources[source_name] = {
            'type': source_type,
            'update_frequency_min': update_frequency,
            'last_update': None,
            'status': 'Connected',
            'connection_params': connection_params,
            'record_count': 0
        }

    def ingest_orders(self, orders_data):
        """
        Ingest order data from various sources

        orders_data: list of order dicts
        """

        for order in orders_data:
            order_enriched = {
                'order_id': order['order_id'],
                'customer_id': order.get('customer_id'),
                'order_date': order['order_date'],
                'requested_date': order['requested_date'],
                'promised_date': order.get('promised_date', order['requested_date']),
                'status': order.get('status', 'Open'),
                'value': order.get('value', 0),
                'priority': order.get('priority', 'Normal'),
                'items': order.get('items', []),
                'fulfillment_location': order.get('fulfillment_location'),
                'shipment_id': order.get('shipment_id'),
                'ingestion_timestamp': datetime.now()
            }

            # Calculate metrics
            order_enriched['days_to_requested'] = self._calculate_days_between(
                datetime.now(), order['requested_date']
            )

            # Flag exceptions
            if order_enriched['days_to_requested'] < 0:
                self._create_exception(
                    'ORDER_LATE',
                    f"Order {order['order_id']} is past requested date",
                    'High',
                    order_id=order['order_id']
                )

            self.orders.append(order_enriched)

    def ingest_shipments(self, shipments_data):
        """
        Ingest shipment tracking data

        shipments_data: list of shipment dicts with tracking info
        """

        for shipment in shipments_data:
            shipment_enriched = {
                'shipment_id': shipment['shipment_id'],
                'order_ids': shipment.get('order_ids', []),
                'carrier': shipment.get('carrier'),
                'tracking_number': shipment.get('tracking_number'),
                'origin': shipment.get('origin'),
                'destination': shipment.get('destination'),
                'ship_date': shipment.get('ship_date'),
                'planned_delivery_date': shipment.get('planned_delivery_date'),
                'actual_delivery_date': shipment.get('actual_delivery_date'),
                'current_location': shipment.get('current_location'),
                'status': shipment.get('status', 'In Transit'),
                'milestones': shipment.get('milestones', []),
                'ingestion_timestamp': datetime.now()
            }

            # Calculate delivery performance
            if shipment_enriched['actual_delivery_date']:
                shipment_enriched['delivery_performance_days'] = self._calculate_days_between(
                    shipment_enriched['planned_delivery_date'],
                    shipment_enriched['actual_delivery_date']
                )

                if shipment_enriched['delivery_performance_days'] < 0:
                    self._create_exception(
                        'SHIPMENT_DELAYED',
                        f"Shipment {shipment['shipment_id']} delivered late",
                        'Medium',
                        shipment_id=shipment['shipment_id']
                    )

            # Check for in-transit issues
            if shipment_enriched['status'] == 'Delayed':
                self._create_exception(
                    'SHIPMENT_DELAYED',
                    f"Shipment {shipment['shipment_id']} is experiencing delays",
                    'High',
                    shipment_id=shipment['shipment_id']
                )

            self.shipments.append(shipment_enriched)

    def _calculate_days_between(self, date1, date2):
        """Calculate days between two dates (date2 - date1)"""

        if isinstance(date1, str):
            date1 = datetime.strptime(date1, '%Y-%m-%d')
        if isinstance(date2, str):
            date2 = datetime.strptime(date2, '%Y-%m-%d')

        return (date2 - date1).days

    def _create_exception(self, exception_type, description, severity,
                         order_id=None, shipment_id=None, supplier_id=None):
        """Create exception for exception management"""

        exception = {
            'exception_id': f"EXC_{len(self.exceptions) + 1:06d}",
            'timestamp': datetime.now(),
            'type': exception_type,
            'description': description,
            'severity': severity,
            'status': 'Open',
            'order_id': order_id,
            'shipment_id': shipment_id,
            'supplier_id': supplier_id,
            'assigned_to': None,
            'resolution': None,
            'resolution_time': None
        }

        self.exceptions.append(exception)

        # Create alert if high severity
        if severity in ['High', 'Critical']:
            self._create_alert(exception)

    def _create_alert(self, exception):
        """Create alert for critical exceptions"""

        alert = {
            'alert_id': f"ALT_{len(self.alerts) + 1:06d}",
            'timestamp': datetime.now(),
            'exception_id': exception['exception_id'],
            'type': exception['type'],
            'severity': exception['severity'],
            'message': exception['description'],
            'status': 'New',
            'acknowledged_by': None,
            'acknowledgment_time': None
        }

        self.alerts.append(alert)

    def calculate_kpis(self):
        """Calculate key performance indicators"""

        # Order KPIs
        total_orders = len(self.orders)
        late_orders = len([o for o in self.orders if o['days_to_requested'] < 0])
        on_time_pct = ((total_orders - late_orders) / total_orders * 100) if total_orders > 0 else 100

        # Shipment KPIs
        total_shipments = len(self.shipments)
        delivered_shipments = [s for s in self.shipments if s.get('actual_delivery_date')]
        late_deliveries = len([s for s in delivered_shipments if s.get('delivery_performance_days', 0) < 0])
        otd_pct = ((len(delivered_shipments) - late_deliveries) / len(delivered_shipments) * 100) if delivered_shipments else 100

        # Exception KPIs
        open_exceptions = len([e for e in self.exceptions if e['status'] == 'Open'])
        high_severity_exceptions = len([e for e in self.exceptions if e['severity'] in ['High', 'Critical']])

        self.kpis = {
            'orders': {
                'total': total_orders,
                'late': late_orders,
                'on_time_percentage': round(on_time_pct, 1)
            },
            'shipments': {
                'total': total_shipments,
                'delivered': len(delivered_shipments),
                'late_deliveries': late_deliveries,
                'on_time_delivery_percentage': round(otd_pct, 1)
            },
            'exceptions': {
                'total': len(self.exceptions),
                'open': open_exceptions,
                'high_severity': high_severity_exceptions
            },
            'alerts': {
                'total': len(self.alerts),
                'new': len([a for a in self.alerts if a['status'] == 'New'])
            }
        }

        return self.kpis

    def get_exceptions_dashboard(self):
        """Generate exceptions dashboard"""

        if not self.exceptions:
            return pd.DataFrame()

        df = pd.DataFrame(self.exceptions)

        # Summary by type
        by_type = df.groupby(['type', 'severity']).size().reset_index(name='count')

        # Summary by status
        by_status = df.groupby('status').size().reset_index(name='count')

        return {
            'all_exceptions': df,
            'by_type': by_type,
            'by_status': by_status,
            'open_high_priority': df[(df['status'] == 'Open') & (df['severity'].isin(['High', 'Critical']))]
        }

    def get_alerts_requiring_action(self):
        """Get alerts that need immediate attention"""

        new_alerts = [a for a in self.alerts if a['status'] == 'New']

        return pd.DataFrame(new_alerts) if new_alerts else pd.DataFrame()

    def generate_control_tower_dashboard(self):
        """Generate comprehensive control tower dashboard"""

        kpis = self.calculate_kpis()

        dashboard = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'kpis': kpis,
            'data_sources': {
                'connected': len([s for s in self.data_sources.values() if s['status'] == 'Connected']),
                'total': len(self.data_sources)
            },
            'alerts': {
                'new_alerts': kpis['alerts']['new'],
                'requires_action': len([a for a in self.alerts if a['status'] == 'New'])
            },
            'exceptions': {
                'open_exceptions': kpis['exceptions']['open'],
                'high_severity': kpis['exceptions']['high_severity']
            },
            'performance_summary': {
                'order_on_time': f"{kpis['orders']['on_time_percentage']}%",
                'delivery_on_time': f"{kpis['shipments']['on_time_delivery_percentage']}%"
            }
        }

        return dashboard


# Example usage
control_tower = ControlTowerPlatform()

# Register data sources
control_tower.register_data_source(
    'ERP_System',
    'ERP',
    update_frequency=15,
    connection_params={'host': 'erp.company.com', 'api_key': 'xxx'}
)

control_tower.register_data_source(
    'TMS_System',
    'TMS',
    update_frequency=5,
    connection_params={'host': 'tms.company.com', 'api_key': 'yyy'}
)

# Ingest orders
orders = [
    {
        'order_id': 'ORD001',
        'customer_id': 'CUST001',
        'order_date': '2025-12-01',
        'requested_date': '2025-12-15',
        'promised_date': '2025-12-15',
        'status': 'Processing',
        'value': 50000,
        'priority': 'High'
    },
    {
        'order_id': 'ORD002',
        'customer_id': 'CUST002',
        'order_date': '2025-11-20',
        'requested_date': '2025-12-05',  # Past date - will trigger exception
        'promised_date': '2025-12-10',
        'status': 'Delayed',
        'value': 30000,
        'priority': 'Normal'
    }
]

control_tower.ingest_orders(orders)

# Ingest shipments
shipments = [
    {
        'shipment_id': 'SHP001',
        'order_ids': ['ORD001'],
        'carrier': 'FedEx',
        'tracking_number': 'TRK123456',
        'origin': 'Chicago, IL',
        'destination': 'New York, NY',
        'ship_date': '2025-12-10',
        'planned_delivery_date': '2025-12-12',
        'actual_delivery_date': '2025-12-14',  # Late
        'status': 'Delivered'
    },
    {
        'shipment_id': 'SHP002',
        'order_ids': ['ORD002'],
        'carrier': 'UPS',
        'tracking_number': 'TRK789012',
        'origin': 'Los Angeles, CA',
        'destination': 'Seattle, WA',
        'ship_date': '2025-12-08',
        'planned_delivery_date': '2025-12-10',
        'status': 'Delayed',  # Currently delayed
        'current_location': 'Portland, OR'
    }
]

control_tower.ingest_shipments(shipments)

# Generate dashboard
dashboard = control_tower.generate_control_tower_dashboard()

print("=== CONTROL TOWER DASHBOARD ===")
print(f"Timestamp: {dashboard['timestamp']}")
print(f"\nKPIs:")
print(f"  Orders: {dashboard['kpis']['orders']['total']} total, {dashboard['kpis']['orders']['late']} late ({dashboard['performance_summary']['order_on_time']} on-time)")
print(f"  Shipments: {dashboard['kpis']['shipments']['delivered']} delivered, {dashboard['kpis']['shipments']['late_deliveries']} late ({dashboard['performance_summary']['delivery_on_time']} on-time)")
print(f"  Exceptions: {dashboard['kpis']['exceptions']['open']} open ({dashboard['kpis']['exceptions']['high_severity']} high severity)")
print(f"  Alerts: {dashboard['alerts']['new_alerts']} new alerts requiring action")

# Get exceptions
exceptions_dashboard = control_tower.get_exceptions_dashboard()
print(f"\n\nOpen High-Priority Exceptions:")
if not exceptions_dashboard['open_high_priority'].empty:
    print(exceptions_dashboard['open_high_priority'][['exception_id', 'type', 'description', 'severity']])

# Get alerts
alerts = control_tower.get_alerts_requiring_action()
print(f"\n\nAlerts Requiring Action:")
if not alerts.empty:
    print(alerts[['alert_id', 'type', 'severity', 'message']])
```

---

## Tools & Libraries

### Python Libraries

**Data Processing:**
- `pandas`: Data manipulation
- `numpy`: Numerical computations
- `sqlalchemy`: Database connections

**Real-Time Processing:**
- `kafka-python`: Apache Kafka integration
- `paho-mqtt`: MQTT messaging
- `redis`: Real-time data store

**Visualization:**
- `dash`: Interactive dashboards
- `plotly`: Interactive charts
- `streamlit`: Dashboard apps
- `bokeh`: Real-time visualizations

**APIs & Integration:**
- `requests`: HTTP requests
- `fastapi`: API development
- `flask`: Web framework

### Commercial Software

**Control Tower Platforms:**
- **Blue Yonder (JDA)**: Luminate Control Tower
- **Kinaxis**: RapidResponse
- **o9 Solutions**: Digital brain platform
- **E2open**: Control tower platform
- **SAP**: Integrated Business Planning with Control Tower
- **Oracle**: Supply Chain Management Cloud

**Visibility Platforms:**
- **FourKites**: Real-time visibility
- **project44**: Transportation visibility
- **Shippeo**: Supply chain visibility
- **ClearMetal**: Predictive logistics
- **Descartes MacroPoint**: Load tracking

**Integration & IoT:**
- **MuleSoft**: API integration
- **Boomi**: Integration platform
- **PTC ThingWorx**: IoT platform
- **AWS IoT**: IoT services

---

## Common Challenges & Solutions

### Challenge: Data Integration Complexity

**Problem:**
- Multiple disparate systems
- Different data formats and standards
- Real-time vs. batch data
- Data quality issues

**Solutions:**
- Phased integration approach (start with critical systems)
- Master data management (MDM)
- API-first architecture
- Data quality rules and validation
- Middleware/integration platform
- Standardized data models

### Challenge: Organization Silos

**Problem:**
- Resistance to centralized control
- Competing priorities
- Lack of collaboration culture
- Unclear ownership

**Solutions:**
- Executive sponsorship and governance
- Cross-functional team structure
- Clear roles and responsibilities (RACI)
- Shared KPIs and incentives
- Change management program
- Quick wins to demonstrate value

### Challenge: Alert Fatigue

**Problem:**
- Too many alerts
- False positives
- Important signals missed
- Reduced responsiveness

**Solutions:**
- Intelligent alert thresholds
- Machine learning for anomaly detection
- Alert prioritization and routing
- Escalation rules
- Alert aggregation and suppression
- Continuous tuning

### Challenge: ROI Justification

**Problem:**
- High implementation costs
- Intangible benefits
- Long payback period
- Competing investments

**Solutions:**
- Start with pilot (limited scope)
- Quantify benefits (cost savings, revenue protection)
- Benchmark against manual processes
- Value case studies and references
- Phased investment approach
- Track and communicate wins

### Challenge: User Adoption

**Problem:**
- Resistance to new tools
- Workflow disruption
- Training requirements
- Habit change needed

**Solutions:**
- User-centric design
- Training and enablement
- Change champions
- Gradual rollout
- Continuous improvement based on feedback
- Gamification and incentives

### Challenge: Scalability

**Problem:**
- Growing data volumes
- More users and use cases
- Performance degradation
- Infrastructure costs

**Solutions:**
- Cloud-based architecture
- Microservices design
- Data archiving and retention policies
- Performance optimization
- Horizontal scaling
- Cost monitoring and optimization

---

## Output Format

### Control Tower Dashboard

**Executive Summary:**
- Overall supply chain health score
- Critical alerts requiring action
- Key performance trends
- Major disruptions or risks

**KPI Scoreboard:**

| KPI | Current | Target | Trend | Status |
|-----|---------|--------|-------|--------|
| Order Fill Rate | 94.2% | 96.0% | ↘ -1.2% | ⚠ Below |
| On-Time Delivery | 89.5% | 92.0% | ↗ +0.8% | ⚠ Below |
| Perfect Order % | 85.3% | 90.0% | → 0.0% | ⚠ Below |
| Order Cycle Time | 4.2 days | 4.0 days | ↗ +0.1 | ⚠ Above |
| Supply Chain Cost as % Revenue | 8.2% | 8.0% | ↘ -0.2% | ✓ On Track |

**Exception Summary:**

| Category | Open | Critical | High | Medium | Aging (>48h) |
|----------|------|----------|------|--------|--------------|
| Orders | 23 | 3 | 8 | 12 | 5 |
| Shipments | 18 | 2 | 6 | 10 | 3 |
| Inventory | 12 | 1 | 4 | 7 | 2 |
| Suppliers | 8 | 0 | 3 | 5 | 1 |
| **Total** | **61** | **6** | **21** | **34** | **11** |

**Critical Alerts:**

| Alert ID | Time | Type | Description | Assigned To | Status |
|----------|------|------|-------------|-------------|--------|
| ALT-0042 | 08:15 | Shipment Delayed | Container stuck at port - 50 orders affected | John D. | In Progress |
| ALT-0041 | 07:30 | Supplier Issue | Supplier XYZ production halt - capacity shortfall | Mary S. | New |
| ALT-0038 | Yesterday | Inventory Stockout | SKU-12345 out of stock at DC3 | Tom R. | Resolving |

**Shipment Tracking:**

| Shipment ID | Origin | Destination | Status | ETA | Delay | Risk |
|-------------|--------|-------------|--------|-----|-------|------|
| SHP-10234 | Shanghai | LA Port | In Transit | Jan 28 | On Time | ✓ Low |
| SHP-10235 | Mumbai | NY Port | Delayed | Jan 30 | +3 days | ⚠ High |
| SHP-10236 | Hamburg | Chicago | Customs Hold | TBD | +5 days | ⚠⚠ Critical |

**Supplier Performance:**

| Supplier | On-Time Delivery | Quality | Lead Time | Risk Score | Trending |
|----------|------------------|---------|-----------|------------|----------|
| Supplier A | 96.2% | 99.8% | 12 days | Low | ✓ Improving |
| Supplier B | 88.5% | 97.2% | 18 days | Medium | ⚠ Declining |
| Supplier C | 92.1% | 95.5% | 15 days | High | → Stable |

---

## Questions to Ask

If you need more context:
1. What business problem is the control tower solving?
2. What scope of operations to cover? (planning, execution, logistics, etc.)
3. What data sources need integration? (ERP, TMS, WMS, suppliers, etc.)
4. What are the critical KPIs to monitor?
5. Who are the users and stakeholders?
6. What's the current visibility and monitoring maturity?
7. What technology infrastructure exists?
8. What's the budget and timeline?
9. Is this internal or extended (suppliers, customers)?
10. What are the success criteria?

---

## Related Skills

- **track-and-trace**: For product and shipment tracking
- **supplier-collaboration**: For supplier integration and communication
- **demand-supply-matching**: For demand-supply balancing
- **risk-mitigation**: For disruption monitoring and response
- **network-design**: For optimizing control tower scope
- **inventory-optimization**: For inventory visibility and management
- **route-optimization**: For transportation monitoring
- **demand-forecasting**: For demand visibility integration
