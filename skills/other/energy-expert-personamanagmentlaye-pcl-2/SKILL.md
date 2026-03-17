---
name: energy-expert
version: 1.0.0
description: Expert-level energy systems, smart grids, renewable energy, power management, and energy analytics
category: domains
tags: [energy, smart-grid, renewable, power, utilities, scada]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Energy Expert

Expert guidance for energy systems, smart grid technology, renewable energy integration, power management, and energy sector software development.

## Core Concepts

### Energy Systems
- Smart grid infrastructure
- Renewable energy systems (solar, wind, hydro)
- Power generation and distribution
- Energy storage systems (batteries, pumped hydro)
- Demand response management
- Energy trading and markets
- Grid stability and load balancing

### Smart Grid Technology
- Advanced Metering Infrastructure (AMI)
- Supervisory Control and Data Acquisition (SCADA)
- Distribution Management Systems (DMS)
- Energy Management Systems (EMS)
- Outage Management Systems (OMS)
- Geographic Information Systems (GIS)
- Real-time monitoring and control

### Standards and Protocols
- IEC 61850 (power utility automation)
- Modbus (industrial protocol)
- DNP3 (Distributed Network Protocol)
- IEEE 2030 (smart grid interoperability)
- OpenADR (automated demand response)
- CIM (Common Information Model)
- MQTT for IoT devices

## Smart Grid Monitoring System

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import numpy as np

@dataclass
class GridNode:
    """Represents a node in the power grid"""
    node_id: str
    node_type: str  # 'substation', 'transformer', 'meter'
    location: tuple  # (latitude, longitude)
    voltage_rating: float  # kV
    current_load: float  # MW
    capacity: float  # MW
    status: str  # 'online', 'offline', 'maintenance'
    last_updated: datetime

@dataclass
class PowerReading:
    """Real-time power measurement"""
    meter_id: str
    timestamp: datetime
    voltage: float  # Volts
    current: float  # Amperes
    power_factor: float
    active_power: float  # kW
    reactive_power: float  # kVAR
    frequency: float  # Hz

class SmartGridMonitor:
    """Smart grid monitoring and control system"""

    def __init__(self):
        self.nodes = {}
        self.alert_thresholds = {
            'voltage_deviation': 0.05,  # 5% deviation
            'overload': 0.95,  # 95% capacity
            'frequency_deviation': 0.5  # Hz
        }

    def process_meter_reading(self, reading: PowerReading) -> dict:
        """Process AMI meter reading"""
        alerts = []

        # Voltage quality check
        nominal_voltage = 240.0  # Volts
        voltage_deviation = abs(reading.voltage - nominal_voltage) / nominal_voltage

        if voltage_deviation > self.alert_thresholds['voltage_deviation']:
            alerts.append({
                'type': 'voltage_deviation',
                'severity': 'warning',
                'value': voltage_deviation,
                'message': f'Voltage deviation: {voltage_deviation:.2%}'
            })

        # Frequency check
        nominal_frequency = 60.0  # Hz (US) or 50.0 (Europe)
        freq_deviation = abs(reading.frequency - nominal_frequency)

        if freq_deviation > self.alert_thresholds['frequency_deviation']:
            alerts.append({
                'type': 'frequency_deviation',
                'severity': 'critical',
                'value': freq_deviation,
                'message': f'Frequency deviation: {freq_deviation:.2f} Hz'
            })

        # Power factor check
        if reading.power_factor < 0.9:
            alerts.append({
                'type': 'poor_power_factor',
                'severity': 'info',
                'value': reading.power_factor,
                'message': f'Low power factor: {reading.power_factor:.2f}'
            })

        return {
            'meter_id': reading.meter_id,
            'timestamp': reading.timestamp,
            'metrics': {
                'voltage': reading.voltage,
                'current': reading.current,
                'power': reading.active_power,
                'power_factor': reading.power_factor
            },
            'alerts': alerts
        }

    def calculate_grid_load(self, node_id: str) -> dict:
        """Calculate load metrics for grid node"""
        node = self.nodes.get(node_id)
        if not node:
            return {'error': 'Node not found'}

        load_percentage = (node.current_load / node.capacity) * 100
        available_capacity = node.capacity - node.current_load

        status = 'normal'
        if load_percentage > 95:
            status = 'critical'
        elif load_percentage > 80:
            status = 'warning'

        return {
            'node_id': node_id,
            'current_load_mw': node.current_load,
            'capacity_mw': node.capacity,
            'load_percentage': load_percentage,
            'available_capacity_mw': available_capacity,
            'status': status
        }

    def predict_demand(self, historical_data: List[float], hours_ahead: int = 24) -> np.ndarray:
        """Predict energy demand using time series analysis"""
        # Simple moving average prediction
        # In production, use LSTM or ARIMA models
        window_size = 168  # 1 week of hourly data

        if len(historical_data) < window_size:
            return np.array([np.mean(historical_data)] * hours_ahead)

        recent_data = np.array(historical_data[-window_size:])

        # Calculate seasonal pattern (24-hour cycle)
        hourly_pattern = np.zeros(24)
        for i in range(24):
            hourly_indices = list(range(i, len(recent_data), 24))
            hourly_pattern[i] = np.mean(recent_data[hourly_indices])

        # Generate predictions
        predictions = []
        for hour in range(hours_ahead):
            hour_of_day = hour % 24
            predictions.append(hourly_pattern[hour_of_day])

        return np.array(predictions)
```

## Renewable Energy Integration

```python
from datetime import datetime, timedelta
import math

class RenewableEnergyManager:
    """Manage renewable energy sources in the grid"""

    def __init__(self):
        self.solar_farms = {}
        self.wind_farms = {}
        self.energy_storage = {}

    def calculate_solar_output(self,
                              capacity_kw: float,
                              location: tuple,
                              timestamp: datetime,
                              cloud_cover: float = 0.0) -> float:
        """Calculate solar panel output based on conditions"""
        lat, lon = location

        # Calculate solar angle (simplified)
        day_of_year = timestamp.timetuple().tm_yday
        hour = timestamp.hour + timestamp.minute / 60.0

        # Solar declination
        declination = 23.45 * math.sin(math.radians((360/365) * (day_of_year - 81)))

        # Hour angle
        hour_angle = 15 * (hour - 12)

        # Solar elevation angle
        elevation = math.asin(
            math.sin(math.radians(lat)) * math.sin(math.radians(declination)) +
            math.cos(math.radians(lat)) * math.cos(math.radians(declination)) *
            math.cos(math.radians(hour_angle))
        )

        # Base output (0-1 scale)
        if elevation <= 0:
            return 0.0  # Night time

        base_output = math.sin(elevation)

        # Apply cloud cover factor
        cloud_factor = 1.0 - (cloud_cover * 0.75)

        # Calculate actual output
        output_kw = capacity_kw * base_output * cloud_factor

        return max(0.0, output_kw)

    def calculate_wind_output(self,
                            capacity_kw: float,
                            wind_speed_ms: float,
                            cut_in_speed: float = 3.0,
                            rated_speed: float = 12.0,
                            cut_out_speed: float = 25.0) -> float:
        """Calculate wind turbine output based on wind speed"""

        # Below cut-in speed
        if wind_speed_ms < cut_in_speed:
            return 0.0

        # Above cut-out speed (safety shutdown)
        if wind_speed_ms > cut_out_speed:
            return 0.0

        # Between cut-in and rated speed (cubic relationship)
        if wind_speed_ms < rated_speed:
            power_coefficient = ((wind_speed_ms - cut_in_speed) /
                               (rated_speed - cut_in_speed)) ** 3
            return capacity_kw * power_coefficient

        # At or above rated speed
        return capacity_kw

    def optimize_energy_storage(self,
                               current_demand: float,
                               renewable_output: float,
                               storage_capacity: float,
                               storage_level: float,
                               grid_price: float) -> dict:
        """Optimize battery storage charge/discharge"""

        surplus = renewable_output - current_demand

        action = 'hold'
        amount = 0.0

        # Surplus energy - charge battery
        if surplus > 0 and storage_level < storage_capacity:
            charge_amount = min(surplus, storage_capacity - storage_level)
            action = 'charge'
            amount = charge_amount

        # Deficit and high price - discharge battery
        elif surplus < 0 and storage_level > 0:
            discharge_amount = min(abs(surplus), storage_level)

            # Only discharge if grid price is high
            if grid_price > 0.15:  # $0.15/kWh threshold
                action = 'discharge'
                amount = discharge_amount

        new_storage_level = storage_level
        if action == 'charge':
            new_storage_level = storage_level + amount
        elif action == 'discharge':
            new_storage_level = storage_level - amount

        return {
            'action': action,
            'amount_kwh': amount,
            'storage_level_kwh': new_storage_level,
            'storage_percentage': (new_storage_level / storage_capacity) * 100
        }
```

## SCADA Integration

```python
import struct
from typing import Dict, Any

class ModbusClient:
    """Modbus protocol client for SCADA systems"""

    def __init__(self, host: str, port: int = 502):
        self.host = host
        self.port = port
        self.connected = False

    def read_holding_registers(self,
                               slave_id: int,
                               start_address: int,
                               count: int) -> List[int]:
        """Read holding registers (function code 0x03)"""
        # Build Modbus request
        request = struct.pack(
            '>BBHH',
            slave_id,
            0x03,  # Function code
            start_address,
            count
        )

        # Send request and receive response
        # In production, use pymodbus library
        response = self._send_request(request)

        # Parse response
        values = []
        for i in range(count):
            offset = 3 + (i * 2)  # Skip header
            value = struct.unpack('>H', response[offset:offset+2])[0]
            values.append(value)

        return values

    def write_single_register(self,
                            slave_id: int,
                            address: int,
                            value: int) -> bool:
        """Write single register (function code 0x06)"""
        request = struct.pack(
            '>BBHH',
            slave_id,
            0x06,  # Function code
            address,
            value
        )

        response = self._send_request(request)
        return response is not None

    def _send_request(self, request: bytes) -> bytes:
        """Send Modbus request and receive response"""
        # Implement actual TCP/RTU communication
        pass

class SCADASystem:
    """SCADA system for power grid control"""

    def __init__(self):
        self.devices = {}
        self.alarm_conditions = []

    def monitor_substation(self, substation_id: str) -> dict:
        """Monitor substation parameters via SCADA"""
        modbus = ModbusClient(f'substation-{substation_id}.local')

        try:
            # Read voltage (registers 0-2 for 3-phase)
            voltages = modbus.read_holding_registers(1, 0, 3)

            # Read current (registers 3-5)
            currents = modbus.read_holding_registers(1, 3, 3)

            # Read breaker status (registers 10-15)
            breaker_status = modbus.read_holding_registers(1, 10, 6)

            # Calculate power
            total_power = sum(
                v * c for v, c in zip(voltages, currents)
            ) / 1000.0  # Convert to kW

            return {
                'substation_id': substation_id,
                'voltages_v': voltages,
                'currents_a': currents,
                'power_kw': total_power,
                'breakers': {
                    f'breaker_{i+1}': 'closed' if status else 'open'
                    for i, status in enumerate(breaker_status)
                },
                'status': 'online'
            }

        except Exception as e:
            return {
                'substation_id': substation_id,
                'status': 'error',
                'error': str(e)
            }

    def control_breaker(self,
                       substation_id: str,
                       breaker_id: int,
                       action: str) -> bool:
        """Control circuit breaker (open/close)"""
        modbus = ModbusClient(f'substation-{substation_id}.local')

        value = 1 if action == 'close' else 0
        register = 10 + breaker_id - 1

        success = modbus.write_single_register(1, register, value)

        if success:
            self._log_control_action(substation_id, breaker_id, action)

        return success

    def _log_control_action(self, substation_id: str, breaker_id: int, action: str):
        """Log control actions for audit trail"""
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] Breaker control: {substation_id}/breaker_{breaker_id} -> {action}")
```

## Energy Trading and Markets

```python
from decimal import Decimal
from datetime import datetime, timedelta

class EnergyTradingSystem:
    """Energy trading and market operations"""

    def __init__(self):
        self.bids = []
        self.offers = []
        self.market_prices = {}

    def submit_bid(self,
                   participant_id: str,
                   quantity_mwh: Decimal,
                   price_per_mwh: Decimal,
                   delivery_hour: datetime) -> str:
        """Submit bid to purchase energy"""
        bid = {
            'bid_id': self._generate_id(),
            'participant_id': participant_id,
            'type': 'buy',
            'quantity_mwh': quantity_mwh,
            'price_per_mwh': price_per_mwh,
            'delivery_hour': delivery_hour,
            'timestamp': datetime.now(),
            'status': 'pending'
        }

        self.bids.append(bid)
        return bid['bid_id']

    def submit_offer(self,
                    participant_id: str,
                    quantity_mwh: Decimal,
                    price_per_mwh: Decimal,
                    delivery_hour: datetime) -> str:
        """Submit offer to sell energy"""
        offer = {
            'offer_id': self._generate_id(),
            'participant_id': participant_id,
            'type': 'sell',
            'quantity_mwh': quantity_mwh,
            'price_per_mwh': price_per_mwh,
            'delivery_hour': delivery_hour,
            'timestamp': datetime.now(),
            'status': 'pending'
        }

        self.offers.append(offer)
        return offer['offer_id']

    def clear_market(self, delivery_hour: datetime) -> dict:
        """Clear energy market using merit order"""
        # Filter bids and offers for delivery hour
        hour_bids = [b for b in self.bids
                    if b['delivery_hour'] == delivery_hour and b['status'] == 'pending']
        hour_offers = [o for o in self.offers
                      if o['delivery_hour'] == delivery_hour and o['status'] == 'pending']

        # Sort bids (descending price) and offers (ascending price)
        sorted_bids = sorted(hour_bids, key=lambda x: x['price_per_mwh'], reverse=True)
        sorted_offers = sorted(hour_offers, key=lambda x: x['price_per_mwh'])

        # Match bids and offers
        matches = []
        total_cleared_volume = Decimal('0')
        clearing_price = Decimal('0')

        bid_idx = 0
        offer_idx = 0

        while bid_idx < len(sorted_bids) and offer_idx < len(sorted_offers):
            bid = sorted_bids[bid_idx]
            offer = sorted_offers[offer_idx]

            # Check if bid price >= offer price
            if bid['price_per_mwh'] >= offer['price_per_mwh']:
                # Match found
                volume = min(bid['quantity_mwh'], offer['quantity_mwh'])
                clearing_price = (bid['price_per_mwh'] + offer['price_per_mwh']) / 2

                matches.append({
                    'bid_id': bid['bid_id'],
                    'offer_id': offer['offer_id'],
                    'volume_mwh': volume,
                    'price_per_mwh': clearing_price
                })

                total_cleared_volume += volume

                # Update quantities
                bid['quantity_mwh'] -= volume
                offer['quantity_mwh'] -= volume

                if bid['quantity_mwh'] == 0:
                    bid_idx += 1
                if offer['quantity_mwh'] == 0:
                    offer_idx += 1
            else:
                break

        return {
            'delivery_hour': delivery_hour,
            'clearing_price': clearing_price,
            'total_volume_mwh': total_cleared_volume,
            'matches': matches
        }

    def _generate_id(self) -> str:
        """Generate unique transaction ID"""
        import uuid
        return str(uuid.uuid4())
```

## Best Practices

### Smart Grid Operations
- Implement real-time monitoring with sub-second latency
- Use redundant communication paths for critical systems
- Deploy edge computing for local decision-making
- Maintain comprehensive audit logs for all control actions
- Implement cybersecurity measures (IEC 62351)
- Use time synchronization (IEEE 1588 PTP)

### Renewable Energy Integration
- Forecast renewable generation using ML models
- Implement dynamic curtailment strategies
- Use energy storage for grid stabilization
- Support virtual power plants (VPP)
- Enable peer-to-peer energy trading
- Monitor power quality metrics

### Data Management
- Use time-series databases (InfluxDB, TimescaleDB)
- Implement data compression for long-term storage
- Archive historical data with proper retention policies
- Ensure data integrity and traceability
- Support real-time analytics and visualization
- Implement anomaly detection algorithms

### System Design
- Design for 99.999% availability
- Implement graceful degradation
- Use microservices architecture
- Support multi-region deployments
- Enable automatic failover
- Implement load balancing

## Anti-Patterns

❌ Single point of failure in critical systems
❌ No backup power for control systems
❌ Ignoring cybersecurity requirements
❌ Insufficient data validation
❌ No disaster recovery plan
❌ Inadequate alarm management (alarm floods)
❌ Poor time synchronization
❌ No testing of protection schemes

## Resources

- IEC 61850 Standard: https://www.iec.ch/
- IEEE Smart Grid: https://smartgrid.ieee.org/
- OpenADR Alliance: https://www.openadr.org/
- Modbus Protocol: https://modbus.org/
- DNP3 Protocol: https://www.dnp.org/
- NIST Smart Grid Framework: https://www.nist.gov/smartgrid
- GridWise Architecture Council: https://www.gridwiseac.org/
