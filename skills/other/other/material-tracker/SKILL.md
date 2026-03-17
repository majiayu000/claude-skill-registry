---
name: "material-tracker"
description: "Track material orders, deliveries, and inventory on construction sites. Monitor lead times, delivery status, and stock levels."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🛒", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Material Tracker

## Business Case

### Problem Statement
Material management challenges:
- Tracking multiple orders
- Coordinating deliveries
- Avoiding stockouts
- Managing lead times

### Solution
Comprehensive material tracking system to monitor orders, deliveries, inventory, and alert on potential issues.

## Technical Implementation

```python
import pandas as pd
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum


class OrderStatus(Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    CONFIRMED = "confirmed"
    IN_PRODUCTION = "in_production"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    PARTIAL = "partial"
    CANCELLED = "cancelled"


class PriorityLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"


@dataclass
class MaterialOrder:
    order_id: str
    material_code: str
    material_name: str
    supplier: str
    quantity: float
    unit: str
    unit_cost: float
    total_cost: float
    order_date: date
    required_date: date
    expected_delivery: date
    actual_delivery: Optional[date]
    status: OrderStatus
    priority: PriorityLevel
    delivered_qty: float = 0
    notes: str = ""


@dataclass
class InventoryItem:
    material_code: str
    material_name: str
    current_stock: float
    unit: str
    min_stock: float
    max_stock: float
    reorder_point: float
    location: str
    last_updated: date


@dataclass
class Delivery:
    delivery_id: str
    order_id: str
    delivery_date: date
    quantity: float
    received_by: str
    condition: str  # good, damaged, partial
    notes: str = ""


class MaterialTracker:
    """Track construction materials."""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.orders: Dict[str, MaterialOrder] = {}
        self.inventory: Dict[str, InventoryItem] = {}
        self.deliveries: List[Delivery] = []

    def create_order(self,
                     order_id: str,
                     material_code: str,
                     material_name: str,
                     supplier: str,
                     quantity: float,
                     unit: str,
                     unit_cost: float,
                     required_date: date,
                     lead_time_days: int = 14,
                     priority: PriorityLevel = PriorityLevel.NORMAL) -> MaterialOrder:
        """Create new material order."""

        order = MaterialOrder(
            order_id=order_id,
            material_code=material_code,
            material_name=material_name,
            supplier=supplier,
            quantity=quantity,
            unit=unit,
            unit_cost=unit_cost,
            total_cost=round(quantity * unit_cost, 2),
            order_date=date.today(),
            required_date=required_date,
            expected_delivery=date.today() + timedelta(days=lead_time_days),
            actual_delivery=None,
            status=OrderStatus.DRAFT,
            priority=priority
        )

        self.orders[order_id] = order
        return order

    def update_order_status(self, order_id: str, status: OrderStatus):
        """Update order status."""
        if order_id in self.orders:
            self.orders[order_id].status = status

    def record_delivery(self,
                        order_id: str,
                        quantity: float,
                        received_by: str,
                        condition: str = "good",
                        notes: str = "") -> Optional[Delivery]:
        """Record material delivery."""

        if order_id not in self.orders:
            return None

        order = self.orders[order_id]

        delivery = Delivery(
            delivery_id=f"DEL-{len(self.deliveries)+1:04d}",
            order_id=order_id,
            delivery_date=date.today(),
            quantity=quantity,
            received_by=received_by,
            condition=condition,
            notes=notes
        )

        self.deliveries.append(delivery)

        # Update order
        order.delivered_qty += quantity
        order.actual_delivery = date.today()

        if order.delivered_qty >= order.quantity:
            order.status = OrderStatus.DELIVERED
        else:
            order.status = OrderStatus.PARTIAL

        # Update inventory
        if order.material_code in self.inventory:
            self.inventory[order.material_code].current_stock += quantity
            self.inventory[order.material_code].last_updated = date.today()

        return delivery

    def add_inventory_item(self,
                           material_code: str,
                           material_name: str,
                           current_stock: float,
                           unit: str,
                           min_stock: float,
                           max_stock: float,
                           location: str):
        """Add item to inventory tracking."""

        reorder_point = min_stock + (max_stock - min_stock) * 0.3

        self.inventory[material_code] = InventoryItem(
            material_code=material_code,
            material_name=material_name,
            current_stock=current_stock,
            unit=unit,
            min_stock=min_stock,
            max_stock=max_stock,
            reorder_point=reorder_point,
            location=location,
            last_updated=date.today()
        )

    def consume_material(self,
                         material_code: str,
                         quantity: float,
                         activity: str = "") -> bool:
        """Record material consumption."""

        if material_code not in self.inventory:
            return False

        item = self.inventory[material_code]
        if item.current_stock < quantity:
            return False

        item.current_stock -= quantity
        item.last_updated = date.today()
        return True

    def get_pending_orders(self) -> List[MaterialOrder]:
        """Get all pending orders."""
        return [
            o for o in self.orders.values()
            if o.status not in [OrderStatus.DELIVERED, OrderStatus.CANCELLED]
        ]

    def get_late_orders(self) -> List[Dict[str, Any]]:
        """Get orders that are late or at risk."""

        late = []
        today = date.today()

        for order in self.orders.values():
            if order.status in [OrderStatus.DELIVERED, OrderStatus.CANCELLED]:
                continue

            days_late = (today - order.expected_delivery).days

            if days_late > 0 or (order.required_date - today).days < 3:
                late.append({
                    'order_id': order.order_id,
                    'material': order.material_name,
                    'supplier': order.supplier,
                    'required_date': order.required_date,
                    'expected_delivery': order.expected_delivery,
                    'days_late': max(0, days_late),
                    'days_until_required': (order.required_date - today).days,
                    'status': order.status.value,
                    'priority': order.priority.value
                })

        return sorted(late, key=lambda x: x['days_until_required'])

    def get_low_stock_items(self) -> List[Dict[str, Any]]:
        """Get items at or below reorder point."""

        low_stock = []

        for item in self.inventory.values():
            if item.current_stock <= item.reorder_point:
                low_stock.append({
                    'material_code': item.material_code,
                    'material_name': item.material_name,
                    'current_stock': item.current_stock,
                    'reorder_point': item.reorder_point,
                    'min_stock': item.min_stock,
                    'unit': item.unit,
                    'location': item.location,
                    'urgency': 'CRITICAL' if item.current_stock <= item.min_stock else 'REORDER'
                })

        return sorted(low_stock, key=lambda x: x['current_stock'])

    def get_delivery_schedule(self, days_ahead: int = 14) -> pd.DataFrame:
        """Get expected deliveries for coming days."""

        today = date.today()
        end_date = today + timedelta(days=days_ahead)

        scheduled = []

        for order in self.orders.values():
            if order.status in [OrderStatus.DELIVERED, OrderStatus.CANCELLED]:
                continue

            if today <= order.expected_delivery <= end_date:
                scheduled.append({
                    'Date': order.expected_delivery,
                    'Order ID': order.order_id,
                    'Material': order.material_name,
                    'Quantity': order.quantity,
                    'Unit': order.unit,
                    'Supplier': order.supplier,
                    'Priority': order.priority.value
                })

        return pd.DataFrame(scheduled).sort_values('Date') if scheduled else pd.DataFrame()

    def calculate_material_cost_summary(self) -> Dict[str, Any]:
        """Calculate material cost summary."""

        total_ordered = sum(o.total_cost for o in self.orders.values())
        total_delivered = sum(
            o.delivered_qty * o.unit_cost
            for o in self.orders.values()
        )
        total_pending = total_ordered - total_delivered

        by_supplier = {}
        for order in self.orders.values():
            if order.supplier not in by_supplier:
                by_supplier[order.supplier] = 0
            by_supplier[order.supplier] += order.total_cost

        return {
            'total_ordered': round(total_ordered, 2),
            'total_delivered': round(total_delivered, 2),
            'total_pending': round(total_pending, 2),
            'order_count': len(self.orders),
            'by_supplier': by_supplier
        }

    def export_to_excel(self, output_path: str) -> str:
        """Export material tracking to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Orders
            orders_df = pd.DataFrame([
                {
                    'Order ID': o.order_id,
                    'Material': o.material_name,
                    'Supplier': o.supplier,
                    'Quantity': o.quantity,
                    'Unit': o.unit,
                    'Unit Cost': o.unit_cost,
                    'Total Cost': o.total_cost,
                    'Order Date': o.order_date,
                    'Required': o.required_date,
                    'Expected': o.expected_delivery,
                    'Status': o.status.value,
                    'Delivered': o.delivered_qty
                }
                for o in self.orders.values()
            ])
            orders_df.to_excel(writer, sheet_name='Orders', index=False)

            # Inventory
            if self.inventory:
                inv_df = pd.DataFrame([
                    {
                        'Code': i.material_code,
                        'Name': i.material_name,
                        'Stock': i.current_stock,
                        'Unit': i.unit,
                        'Min': i.min_stock,
                        'Max': i.max_stock,
                        'Reorder Point': i.reorder_point,
                        'Location': i.location
                    }
                    for i in self.inventory.values()
                ])
                inv_df.to_excel(writer, sheet_name='Inventory', index=False)

            # Late orders
            late = self.get_late_orders()
            if late:
                late_df = pd.DataFrame(late)
                late_df.to_excel(writer, sheet_name='Late Orders', index=False)

            # Low stock
            low = self.get_low_stock_items()
            if low:
                low_df = pd.DataFrame(low)
                low_df.to_excel(writer, sheet_name='Low Stock', index=False)

        return output_path
```

## Quick Start

```python
from datetime import date, timedelta

# Initialize tracker
tracker = MaterialTracker("Office Building A")

# Create order
order = tracker.create_order(
    order_id="PO-001",
    material_code="CONC-C30",
    material_name="Concrete C30",
    supplier="ABC Ready Mix",
    quantity=200,
    unit="m3",
    unit_cost=150,
    required_date=date.today() + timedelta(days=10),
    lead_time_days=3,
    priority=PriorityLevel.HIGH
)

# Update status
tracker.update_order_status("PO-001", OrderStatus.CONFIRMED)

# Record delivery
tracker.record_delivery("PO-001", quantity=200, received_by="John Smith")
```

## Common Use Cases

### 1. Check Late Orders
```python
late = tracker.get_late_orders()
for order in late:
    print(f"{order['order_id']}: {order['days_late']} days late")
```

### 2. Low Stock Alert
```python
low_stock = tracker.get_low_stock_items()
for item in low_stock:
    print(f"{item['material_name']}: {item['current_stock']} {item['unit']} - {item['urgency']}")
```

### 3. Delivery Schedule
```python
schedule = tracker.get_delivery_schedule(days_ahead=7)
print(schedule)
```

## Resources
- **DDC Book**: Chapter 3.2 - Material Management
