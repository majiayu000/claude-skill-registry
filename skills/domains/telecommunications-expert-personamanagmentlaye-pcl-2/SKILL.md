---
name: telecommunications-expert
version: 1.0.0
description: Expert-level telecommunications systems, network management, billing, 5G, SDN, and telecom infrastructure
category: domains
tags: [telecom, networking, 5g, billing, oss, bss]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Telecommunications Expert

Expert guidance for telecommunications systems, network management, billing systems, 5G networks, SDN/NFV, and telecom infrastructure management.

## Core Concepts

### Telecommunications Systems
- Operations Support Systems (OSS)
- Business Support Systems (BSS)
- Network Management Systems (NMS)
- Service Assurance
- Inventory Management
- Provisioning systems
- Customer care platforms

### Network Technologies
- 5G/4G/LTE networks
- Fiber optic networks
- Software-Defined Networking (SDN)
- Network Functions Virtualization (NFV)
- Edge computing
- IoT connectivity
- Satellite communications

### Standards and Protocols
- 3GPP standards
- TM Forum Frameworx
- ETSI specifications
- ITU-T recommendations
- SIP (Session Initiation Protocol)
- Diameter protocol
- SNMP for network management

## Network Management System

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum
import numpy as np

class NetworkElementType(Enum):
    BASE_STATION = "base_station"
    ROUTER = "router"
    SWITCH = "switch"
    FIBER_NODE = "fiber_node"
    GATEWAY = "gateway"
    FIREWALL = "firewall"

class AlarmSeverity(Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    WARNING = "warning"
    CLEARED = "cleared"

@dataclass
class NetworkElement:
    """Network infrastructure element"""
    element_id: str
    element_type: NetworkElementType
    name: str
    location: dict
    ip_address: str
    status: str  # 'active', 'inactive', 'maintenance'
    vendor: str
    model: str
    software_version: str
    capacity: dict
    utilization: dict

@dataclass
class NetworkAlarm:
    """Network alarm/event"""
    alarm_id: str
    element_id: str
    severity: AlarmSeverity
    alarm_type: str
    description: str
    timestamp: datetime
    acknowledged: bool
    cleared: bool
    clear_timestamp: Optional[datetime]

@dataclass
class PerformanceMetric:
    """Network performance metric"""
    element_id: str
    metric_name: str
    value: float
    unit: str
    timestamp: datetime
    threshold_warning: float
    threshold_critical: float

class NetworkManagementSystem:
    """Telecom network management and monitoring"""

    def __init__(self):
        self.network_elements = {}
        self.alarms = []
        self.performance_data = []

    def monitor_network_element(self, element_id: str) -> dict:
        """Monitor network element health and performance"""
        element = self.network_elements.get(element_id)
        if not element:
            return {'error': 'Network element not found'}

        # Collect performance metrics via SNMP
        metrics = self._collect_snmp_metrics(element)

        # Check thresholds
        violations = []
        for metric in metrics:
            if metric.value >= metric.threshold_critical:
                violations.append({
                    'metric': metric.metric_name,
                    'value': metric.value,
                    'threshold': metric.threshold_critical,
                    'severity': 'critical'
                })
                self._raise_alarm(element_id, AlarmSeverity.CRITICAL,
                                f"{metric.metric_name} exceeded critical threshold")

            elif metric.value >= metric.threshold_warning:
                violations.append({
                    'metric': metric.metric_name,
                    'value': metric.value,
                    'threshold': metric.threshold_warning,
                    'severity': 'warning'
                })

        return {
            'element_id': element_id,
            'status': element.status,
            'metrics': [
                {
                    'name': m.metric_name,
                    'value': m.value,
                    'unit': m.unit
                }
                for m in metrics
            ],
            'violations': violations,
            'health_score': self._calculate_health_score(element, metrics)
        }

    def _collect_snmp_metrics(self, element: NetworkElement) -> List[PerformanceMetric]:
        """Collect metrics via SNMP"""
        metrics = []
        timestamp = datetime.now()

        # CPU utilization
        cpu_util = self._get_cpu_utilization(element)
        metrics.append(PerformanceMetric(
            element_id=element.element_id,
            metric_name='cpu_utilization',
            value=cpu_util,
            unit='percent',
            timestamp=timestamp,
            threshold_warning=70.0,
            threshold_critical=90.0
        ))

        # Memory utilization
        mem_util = self._get_memory_utilization(element)
        metrics.append(PerformanceMetric(
            element_id=element.element_id,
            metric_name='memory_utilization',
            value=mem_util,
            unit='percent',
            timestamp=timestamp,
            threshold_warning=80.0,
            threshold_critical=95.0
        ))

        # Interface traffic
        for interface in ['eth0', 'eth1']:
            traffic = self._get_interface_traffic(element, interface)
            metrics.append(PerformanceMetric(
                element_id=element.element_id,
                metric_name=f'{interface}_traffic',
                value=traffic,
                unit='mbps',
                timestamp=timestamp,
                threshold_warning=800.0,
                threshold_critical=950.0
            ))

        return metrics

    def _calculate_health_score(self,
                                element: NetworkElement,
                                metrics: List[PerformanceMetric]) -> float:
        """Calculate overall health score for network element"""
        if element.status != 'active':
            return 0.0

        score = 100.0

        for metric in metrics:
            if metric.value >= metric.threshold_critical:
                score -= 20
            elif metric.value >= metric.threshold_warning:
                score -= 10

        return max(0.0, score)

    def _raise_alarm(self, element_id: str, severity: AlarmSeverity, description: str):
        """Raise network alarm"""
        alarm = NetworkAlarm(
            alarm_id=self._generate_alarm_id(),
            element_id=element_id,
            severity=severity,
            alarm_type='performance',
            description=description,
            timestamp=datetime.now(),
            acknowledged=False,
            cleared=False,
            clear_timestamp=None
        )

        self.alarms.append(alarm)

        # Send notifications for critical alarms
        if severity == AlarmSeverity.CRITICAL:
            self._send_alarm_notification(alarm)

    def analyze_network_capacity(self, region: str) -> dict:
        """Analyze network capacity and utilization"""
        # Get all elements in region
        region_elements = [
            e for e in self.network_elements.values()
            if e.location.get('region') == region
        ]

        if not region_elements:
            return {'error': 'No network elements in region'}

        # Calculate aggregate capacity and utilization
        total_capacity = 0
        total_used = 0

        for element in region_elements:
            capacity = element.capacity.get('bandwidth_gbps', 0)
            utilization = element.utilization.get('bandwidth_percent', 0)

            total_capacity += capacity
            total_used += capacity * (utilization / 100)

        utilization_percent = (total_used / total_capacity * 100) if total_capacity > 0 else 0

        # Predict capacity needs
        growth_rate = 0.15  # 15% annual growth
        months_until_full = self._predict_capacity_exhaustion(
            total_capacity,
            total_used,
            growth_rate
        )

        return {
            'region': region,
            'total_capacity_gbps': total_capacity,
            'used_capacity_gbps': total_used,
            'available_capacity_gbps': total_capacity - total_used,
            'utilization_percent': utilization_percent,
            'predicted_full_in_months': months_until_full,
            'expansion_recommended': months_until_full < 12
        }

    def _predict_capacity_exhaustion(self,
                                    total_capacity: float,
                                    current_usage: float,
                                    growth_rate: float) -> float:
        """Predict when capacity will be exhausted"""
        if current_usage >= total_capacity:
            return 0.0

        available = total_capacity - current_usage
        monthly_growth_rate = growth_rate / 12

        # Calculate months until 90% capacity
        target_usage = total_capacity * 0.9
        usage_needed = target_usage - current_usage

        if usage_needed <= 0:
            return 0.0

        months = np.log(1 + (usage_needed / current_usage)) / np.log(1 + monthly_growth_rate)

        return months

    def _get_cpu_utilization(self, element: NetworkElement) -> float:
        """Get CPU utilization via SNMP"""
        # Implementation would use SNMP library
        return np.random.uniform(30, 70)  # Placeholder

    def _get_memory_utilization(self, element: NetworkElement) -> float:
        """Get memory utilization via SNMP"""
        return np.random.uniform(40, 80)  # Placeholder

    def _get_interface_traffic(self, element: NetworkElement, interface: str) -> float:
        """Get interface traffic via SNMP"""
        return np.random.uniform(100, 800)  # Placeholder

    def _send_alarm_notification(self, alarm: NetworkAlarm):
        """Send alarm notification"""
        # Implementation would send SMS/email/page
        pass

    def _generate_alarm_id(self) -> str:
        import uuid
        return f"ALM-{uuid.uuid4().hex[:10].upper()}"
```

## Billing System

```python
from decimal import Decimal

@dataclass
class Subscriber:
    """Telecom subscriber"""
    subscriber_id: str
    account_number: str
    name: str
    phone_number: str
    email: str
    address: dict
    plan_id: str
    status: str  # 'active', 'suspended', 'terminated'
    activation_date: datetime

@dataclass
class ServicePlan:
    """Service plan/package"""
    plan_id: str
    name: str
    description: str
    monthly_fee: Decimal
    data_allowance_gb: float
    voice_minutes: int
    sms_count: int
    overage_rates: dict

@dataclass
class UsageRecord:
    """Usage record for billing"""
    record_id: str
    subscriber_id: str
    usage_type: str  # 'voice', 'sms', 'data'
    timestamp: datetime
    quantity: float
    unit: str
    destination: Optional[str]
    charged: bool

class BillingSystem:
    """Telecom billing and charging system"""

    def __init__(self):
        self.subscribers = {}
        self.service_plans = {}
        self.usage_records = []
        self.invoices = []

    def process_usage(self, usage: UsageRecord) -> dict:
        """Process usage record for charging"""
        subscriber = self.subscribers.get(usage.subscriber_id)
        if not subscriber:
            return {'error': 'Subscriber not found'}

        if subscriber.status != 'active':
            return {'error': 'Subscriber not active'}

        plan = self.service_plans.get(subscriber.plan_id)
        if not plan:
            return {'error': 'Service plan not found'}

        # Check if usage is within plan allowance
        current_usage = self._get_current_month_usage(usage.subscriber_id, usage.usage_type)

        charge = Decimal('0')

        if usage.usage_type == 'data':
            if current_usage > plan.data_allowance_gb:
                # Overage charges
                overage_gb = usage.quantity
                charge = Decimal(str(overage_gb)) * plan.overage_rates['data_per_gb']

        elif usage.usage_type == 'voice':
            if current_usage > plan.voice_minutes:
                # Overage charges
                overage_minutes = usage.quantity
                charge = Decimal(str(overage_minutes)) * plan.overage_rates['voice_per_minute']

        elif usage.usage_type == 'sms':
            if current_usage > plan.sms_count:
                # Overage charges
                overage_sms = usage.quantity
                charge = Decimal(str(overage_sms)) * plan.overage_rates['sms_per_message']

        usage.charged = True
        self.usage_records.append(usage)

        return {
            'subscriber_id': usage.subscriber_id,
            'usage_type': usage.usage_type,
            'quantity': usage.quantity,
            'charge': float(charge),
            'within_allowance': charge == 0
        }

    def generate_invoice(self, subscriber_id: str, billing_period: tuple) -> dict:
        """Generate monthly invoice"""
        subscriber = self.subscribers.get(subscriber_id)
        if not subscriber:
            return {'error': 'Subscriber not found'}

        plan = self.service_plans.get(subscriber.plan_id)
        start_date, end_date = billing_period

        # Base charges
        monthly_fee = plan.monthly_fee

        # Usage charges
        period_usage = [
            u for u in self.usage_records
            if u.subscriber_id == subscriber_id and
            start_date <= u.timestamp <= end_date
        ]

        usage_charges = self._calculate_usage_charges(period_usage, plan)

        # Taxes (simplified)
        subtotal = monthly_fee + usage_charges['total']
        tax_rate = Decimal('0.10')  # 10%
        taxes = subtotal * tax_rate

        total = subtotal + taxes

        invoice = {
            'invoice_id': self._generate_invoice_id(),
            'subscriber_id': subscriber_id,
            'account_number': subscriber.account_number,
            'billing_period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'charges': {
                'monthly_fee': float(monthly_fee),
                'data_charges': float(usage_charges['data']),
                'voice_charges': float(usage_charges['voice']),
                'sms_charges': float(usage_charges['sms']),
                'other_charges': float(usage_charges['other'])
            },
            'subtotal': float(subtotal),
            'taxes': float(taxes),
            'total': float(total),
            'due_date': (end_date + timedelta(days=15)).isoformat()
        }

        self.invoices.append(invoice)

        return invoice

    def _get_current_month_usage(self, subscriber_id: str, usage_type: str) -> float:
        """Get current month usage for subscriber"""
        current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0)

        usage = [
            u for u in self.usage_records
            if u.subscriber_id == subscriber_id and
            u.usage_type == usage_type and
            u.timestamp >= current_month_start
        ]

        total = sum(u.quantity for u in usage)
        return total

    def _calculate_usage_charges(self,
                                usage_records: List[UsageRecord],
                                plan: ServicePlan) -> dict:
        """Calculate usage charges"""
        charges = {
            'data': Decimal('0'),
            'voice': Decimal('0'),
            'sms': Decimal('0'),
            'other': Decimal('0'),
            'total': Decimal('0')
        }

        # Group usage by type
        data_usage = sum(u.quantity for u in usage_records if u.usage_type == 'data')
        voice_usage = sum(u.quantity for u in usage_records if u.usage_type == 'voice')
        sms_usage = sum(u.quantity for u in usage_records if u.usage_type == 'sms')

        # Calculate overage charges
        if data_usage > plan.data_allowance_gb:
            overage = data_usage - plan.data_allowance_gb
            charges['data'] = Decimal(str(overage)) * plan.overage_rates['data_per_gb']

        if voice_usage > plan.voice_minutes:
            overage = voice_usage - plan.voice_minutes
            charges['voice'] = Decimal(str(overage)) * plan.overage_rates['voice_per_minute']

        if sms_usage > plan.sms_count:
            overage = sms_usage - plan.sms_count
            charges['sms'] = Decimal(str(overage)) * plan.overage_rates['sms_per_message']

        charges['total'] = sum([charges['data'], charges['voice'], charges['sms'], charges['other']])

        return charges

    def _generate_invoice_id(self) -> str:
        import uuid
        return f"INV-{uuid.uuid4().hex[:10].upper()}"
```

## 5G Network Management

```python
class FiveGNetworkManagement:
    """5G network management and optimization"""

    def __init__(self):
        self.base_stations = {}
        self.network_slices = {}

    def configure_network_slice(self, slice_config: dict) -> dict:
        """Configure 5G network slice"""
        slice_id = self._generate_slice_id()

        network_slice = {
            'slice_id': slice_id,
            'name': slice_config['name'],
            'slice_type': slice_config['slice_type'],  # 'eMBB', 'URLLC', 'mMTC'
            'resources': {
                'bandwidth_mhz': slice_config['bandwidth'],
                'latency_ms': slice_config['max_latency'],
                'reliability': slice_config['reliability']
            },
            'qos_profile': slice_config['qos_profile'],
            'status': 'active'
        }

        self.network_slices[slice_id] = network_slice

        # Allocate resources
        self._allocate_slice_resources(network_slice)

        return {
            'slice_id': slice_id,
            'status': 'configured',
            'resources_allocated': True
        }

    def optimize_beamforming(self, base_station_id: str, user_positions: List[tuple]) -> dict:
        """Optimize massive MIMO beamforming"""
        # Simplified beamforming optimization
        # In production, would use complex signal processing algorithms

        num_users = len(user_positions)
        num_antennas = 64  # Massive MIMO array

        # Calculate beam directions
        beam_directions = []
        for position in user_positions:
            angle = self._calculate_beam_angle(position)
            beam_directions.append(angle)

        # Calculate precoding matrix (simplified)
        # In production, would use ZF or MMSE precoding

        return {
            'base_station_id': base_station_id,
            'num_users': num_users,
            'num_antennas': num_antennas,
            'beam_directions': beam_directions,
            'expected_throughput_improvement': 2.5  # 2.5x improvement
        }

    def manage_handover(self, ue_id: str, source_cell: str, target_cell: str) -> dict:
        """Manage 5G handover"""
        # Measure signal quality
        source_rsrp = self._measure_rsrp(ue_id, source_cell)
        target_rsrp = self._measure_rsrp(ue_id, target_cell)

        # Decision criteria
        handover_threshold = 3  # dB
        if target_rsrp > source_rsrp + handover_threshold:
            # Initiate handover
            result = self._execute_handover(ue_id, source_cell, target_cell)

            return {
                'ue_id': ue_id,
                'handover': 'executed',
                'source_cell': source_cell,
                'target_cell': target_cell,
                'source_rsrp': source_rsrp,
                'target_rsrp': target_rsrp
            }
        else:
            return {
                'ue_id': ue_id,
                'handover': 'not_required',
                'source_rsrp': source_rsrp,
                'target_rsrp': target_rsrp
            }

    def _allocate_slice_resources(self, network_slice: dict):
        """Allocate network resources for slice"""
        # Implementation would configure SDN/NFV infrastructure
        pass

    def _calculate_beam_angle(self, position: tuple) -> float:
        """Calculate beam angle for position"""
        # Simplified calculation
        return 45.0  # degrees

    def _measure_rsrp(self, ue_id: str, cell_id: str) -> float:
        """Measure Reference Signal Received Power"""
        # Implementation would get actual RSRP from network
        return np.random.uniform(-110, -70)  # dBm

    def _execute_handover(self, ue_id: str, source: str, target: str) -> bool:
        """Execute handover procedure"""
        # Implementation would perform actual handover
        return True

    def _generate_slice_id(self) -> str:
        import uuid
        return f"SLICE-{uuid.uuid4().hex[:8].upper()}"
```

## Best Practices

### Network Management
- Implement proactive monitoring
- Use predictive analytics for fault detection
- Automate routine tasks
- Maintain network documentation
- Implement configuration management
- Use centralized logging
- Monitor key performance indicators (KPIs)

### Billing Systems
- Ensure real-time charging
- Implement usage mediation
- Support multiple rating models
- Provide transparent billing
- Enable self-service portal
- Automate invoice generation
- Implement payment processing

### 5G Networks
- Implement network slicing
- Optimize for low latency
- Use edge computing
- Enable dynamic resource allocation
- Support massive IoT connectivity
- Implement security measures
- Monitor QoS metrics

### Service Assurance
- Track service level agreements (SLAs)
- Implement automated testing
- Monitor customer experience
- Provide real-time diagnostics
- Enable root cause analysis
- Track mean time to repair (MTTR)
- Implement service quality metrics

## Anti-Patterns

❌ Reactive network management only
❌ Manual provisioning processes
❌ No capacity planning
❌ Inaccurate billing
❌ Poor alarm management (alarm storms)
❌ No network redundancy
❌ Ignoring customer experience metrics
❌ Manual configuration changes
❌ No disaster recovery plan

## Resources

- TM Forum: https://www.tmforum.org/
- 3GPP: https://www.3gpp.org/
- ETSI: https://www.etsi.org/
- ITU-T: https://www.itu.int/
- GSMA: https://www.gsma.com/
- ONF (Open Networking Foundation): https://opennetworking.org/
- O-RAN Alliance: https://www.o-ran.org/
