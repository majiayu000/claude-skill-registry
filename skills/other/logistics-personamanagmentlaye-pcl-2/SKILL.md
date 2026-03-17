---
name: logistics-expert
version: 1.0.0
description: Expert-level supply chain management, logistics optimization, warehouse systems, and fleet management
category: domains
tags: [logistics, supply-chain, warehouse, fleet, optimization]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Logistics Expert

Expert guidance for supply chain management, logistics optimization, warehouse management systems, and transportation planning.

## Core Concepts

### Supply Chain Management
- Inventory management
- Demand forecasting
- Procurement and sourcing
- Warehouse management (WMS)
- Transportation management (TMS)
- Order fulfillment
- Last-mile delivery

### Optimization
- Route optimization
- Load planning
- Inventory optimization
- Network design
- Cost minimization
- Delivery scheduling

### Technologies
- RFID and barcode scanning
- GPS tracking
- IoT sensors
- Predictive analytics
- Automated warehouses
- Drone delivery

## Warehouse Management System

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from enum import Enum

class StorageType(Enum):
    PALLET = "pallet"
    SHELF = "shelf"
    BULK = "bulk"
    COLD = "cold_storage"

@dataclass
class Location:
    location_id: str
    zone: str
    aisle: str
    rack: str
    level: int
    storage_type: StorageType
    capacity: float
    current_load: float

@dataclass
class Product:
    sku: str
    name: str
    category: str
    weight: float
    volume: float
    storage_requirements: str

@dataclass
class InventoryItem:
    item_id: str
    sku: str
    quantity: int
    location_id: str
    received_date: datetime
    expiry_date: Optional[datetime]
    batch_number: str

class WMS:
    """Warehouse Management System"""

    def __init__(self, db):
        self.db = db

    def receive_shipment(self, shipment):
        """Process incoming shipment"""
        items_received = []

        for item in shipment.items:
            # Find optimal storage location
            location = self.find_optimal_location(item)

            # Create inventory record
            inventory_item = InventoryItem(
                item_id=generate_id(),
                sku=item.sku,
                quantity=item.quantity,
                location_id=location.location_id,
                received_date=datetime.now(),
                expiry_date=item.expiry_date,
                batch_number=item.batch_number
            )

            self.db.save_inventory(inventory_item)
            self.update_location_capacity(location, item)

            items_received.append(inventory_item)

        return {
            'shipment_id': shipment.shipment_id,
            'items_received': len(items_received),
            'status': 'completed'
        }

    def find_optimal_location(self, item):
        """Find best storage location for item"""
        product = self.db.get_product(item.sku)
        available_locations = self.db.get_available_locations(
            storage_type=product.storage_requirements,
            min_capacity=product.volume * item.quantity
        )

        # Prioritize locations
        # 1. Same SKU for efficient picking
        # 2. Closest to shipping area for fast-moving items
        # 3. Maximize space utilization

        same_sku_locations = [
            loc for loc in available_locations
            if self.has_same_sku(loc, item.sku)
        ]

        if same_sku_locations:
            return same_sku_locations[0]

        # Select closest to shipping for fast-moving items
        if product.category == 'fast-moving':
            return min(available_locations, key=lambda l: l.distance_to_shipping)

        # Otherwise, optimize space utilization
        return max(available_locations, key=lambda l: l.utilization_score)

    def pick_order(self, order_id):
        """Generate picking list and route"""
        order = self.db.get_order(order_id)
        picking_list = []

        for line_item in order.line_items:
            inventory = self.db.find_inventory(
                sku=line_item.sku,
                quantity=line_item.quantity
            )

            picking_list.append({
                'sku': line_item.sku,
                'quantity': line_item.quantity,
                'location': inventory.location_id,
                'batch': inventory.batch_number
            })

        # Optimize picking route
        optimized_route = self.optimize_picking_route(picking_list)

        return {
            'order_id': order_id,
            'picking_list': optimized_route,
            'estimated_time': self.estimate_picking_time(optimized_route)
        }

    def optimize_picking_route(self, picking_list):
        """Optimize warehouse picking route"""
        # Sort by zone, aisle, rack for efficient walking path
        sorted_picks = sorted(
            picking_list,
            key=lambda x: (
                self.get_location_zone(x['location']),
                self.get_location_aisle(x['location']),
                self.get_location_rack(x['location'])
            )
        )

        return sorted_picks

    def check_stock_level(self, sku):
        """Check current stock level"""
        total_quantity = self.db.sum_quantity_by_sku(sku)
        product = self.db.get_product(sku)

        status = 'normal'
        if total_quantity <= product.reorder_point:
            status = 'reorder'
        elif total_quantity <= product.safety_stock:
            status = 'critical'

        return {
            'sku': sku,
            'quantity': total_quantity,
            'status': status,
            'reorder_point': product.reorder_point
        }
```

## Route Optimization

```python
import numpy as np
from scipy.spatial.distance import cdist
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

class RouteOptimizer:
    """Vehicle routing optimization"""

    def optimize_delivery_routes(self, depot, deliveries, vehicles):
        """Optimize delivery routes using OR-Tools"""
        # Create distance matrix
        locations = [depot] + deliveries
        distance_matrix = self.create_distance_matrix(locations)

        # Create routing model
        manager = pywrapcp.RoutingIndexManager(
            len(distance_matrix),
            len(vehicles),
            0  # depot index
        )

        routing = pywrapcp.RoutingModel(manager)

        # Distance callback
        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Add capacity constraints
        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            return deliveries[from_node - 1].weight if from_node > 0 else 0

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            [v.capacity for v in vehicles],
            True,  # start cumul to zero
            'Capacity'
        )

        # Solve
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            return self.extract_routes(manager, routing, solution, locations)

        return None

    def create_distance_matrix(self, locations):
        """Create distance matrix from coordinates"""
        coords = np.array([(loc.lat, loc.lon) for loc in locations])
        return cdist(coords, coords, metric='euclidean')

    def extract_routes(self, manager, routing, solution, locations):
        """Extract optimized routes from solution"""
        routes = []

        for vehicle_id in range(routing.vehicles()):
            route = []
            index = routing.Start(vehicle_id)

            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)
                route.append(locations[node])
                index = solution.Value(routing.NextVar(index))

            routes.append({
                'vehicle_id': vehicle_id,
                'stops': route,
                'total_distance': solution.ObjectiveValue()
            })

        return routes
```

## Fleet Management

```python
@dataclass
class Vehicle:
    vehicle_id: str
    type: str
    capacity_weight: float
    capacity_volume: float
    fuel_efficiency: float
    status: str
    current_location: dict
    maintenance_due: datetime

class FleetManagement:
    """Fleet tracking and management"""

    def __init__(self, db):
        self.db = db

    def assign_vehicle(self, delivery):
        """Assign optimal vehicle for delivery"""
        available_vehicles = self.db.get_available_vehicles(
            location=delivery.origin,
            min_capacity=delivery.total_weight
        )

        # Score vehicles based on:
        # - Distance from origin
        # - Capacity utilization
        # - Fuel efficiency
        # - Maintenance status

        best_vehicle = min(
            available_vehicles,
            key=lambda v: self.calculate_vehicle_score(v, delivery)
        )

        return best_vehicle

    def track_vehicle(self, vehicle_id):
        """Real-time vehicle tracking"""
        vehicle = self.db.get_vehicle(vehicle_id)
        current_route = self.db.get_current_route(vehicle_id)

        return {
            'vehicle_id': vehicle_id,
            'location': vehicle.current_location,
            'status': vehicle.status,
            'current_delivery': current_route.delivery_id if current_route else None,
            'eta': self.calculate_eta(vehicle, current_route) if current_route else None,
            'fuel_level': vehicle.fuel_level,
            'distance_traveled_today': vehicle.daily_distance
        }

    def schedule_maintenance(self, vehicle_id):
        """Schedule vehicle maintenance"""
        vehicle = self.db.get_vehicle(vehicle_id)
        maintenance_history = self.db.get_maintenance_history(vehicle_id)

        # Predictive maintenance based on:
        # - Mileage
        # - Hours of operation
        # - Previous issues
        # - Manufacturer schedule

        next_maintenance = self.predict_maintenance_date(
            vehicle,
            maintenance_history
        )

        return {
            'vehicle_id': vehicle_id,
            'next_maintenance': next_maintenance,
            'type': 'preventive',
            'estimated_cost': self.estimate_maintenance_cost(vehicle)
        }
```

## Inventory Forecasting

```python
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

class DemandForecasting:
    """Demand forecasting and inventory optimization"""

    def forecast_demand(self, sku, forecast_period_days=30):
        """Forecast product demand"""
        # Get historical sales data
        historical_data = self.db.get_sales_history(sku, days=365)

        # Features: day of week, month, seasonality, promotions
        df = pd.DataFrame(historical_data)
        df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
        df['month'] = pd.to_datetime(df['date']).dt.month
        df['is_promotion'] = df['promotion_id'].notna().astype(int)

        X = df[['day_of_week', 'month', 'is_promotion']]
        y = df['quantity_sold']

        # Train model
        model = RandomForestRegressor(n_estimators=100)
        model.fit(X, y)

        # Generate forecast
        future_dates = pd.date_range(
            start=pd.Timestamp.now(),
            periods=forecast_period_days,
            freq='D'
        )

        forecast_features = pd.DataFrame({
            'day_of_week': future_dates.dayofweek,
            'month': future_dates.month,
            'is_promotion': 0  # Assume no promotions unless specified
        })

        predicted_demand = model.predict(forecast_features)

        return {
            'sku': sku,
            'forecast_period': forecast_period_days,
            'predicted_demand': predicted_demand.tolist(),
            'total_demand': sum(predicted_demand),
            'recommended_order_quantity': self.calculate_order_quantity(
                predicted_demand,
                sku
            )
        }

    def calculate_order_quantity(self, forecast, sku):
        """Calculate economic order quantity"""
        product = self.db.get_product(sku)
        total_demand = sum(forecast)

        # EOQ formula
        eoq = np.sqrt(
            (2 * total_demand * product.order_cost) /
            product.holding_cost
        )

        return int(eoq)
```

## Best Practices

- Implement real-time tracking
- Use predictive analytics
- Optimize inventory levels
- Automate warehouse operations
- Enable multi-modal transportation
- Implement quality control
- Track KPIs (on-time delivery, accuracy)
- Use lean principles
- Enable reverse logistics
- Implement safety protocols

## Anti-Patterns

❌ Manual inventory tracking
❌ No route optimization
❌ Overstocking or understocking
❌ Poor warehouse layout
❌ No real-time visibility
❌ Ignoring data analytics
❌ Inefficient picking processes

## Resources

- Council of Supply Chain Management Professionals: https://cscmp.org/
- OR-Tools: https://developers.google.com/optimization
- Warehouse Management: https://www.mhi.org/
- Transportation Management: https://www.inboundlogistics.com/
