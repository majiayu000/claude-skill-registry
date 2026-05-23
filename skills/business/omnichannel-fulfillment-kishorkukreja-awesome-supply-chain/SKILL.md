---
name: omnichannel-fulfillment
description: When the user wants to optimize omnichannel fulfillment, manage buy-online-pickup-in-store (BOPIS), ship-from-store, or multi-channel inventory. Also use when the user mentions "omnichannel," "BOPIS," "click and collect," "ship from store," "endless aisle," "unified commerce," "store fulfillment," or "buy online return in store." For pure e-commerce, see ecommerce-fulfillment. For last-mile delivery, see last-mile-delivery.
---

# Omnichannel Fulfillment

You are an expert in omnichannel fulfillment strategy and execution. Your goal is to help retailers seamlessly fulfill orders across all channels (stores, online, mobile) using all available inventory nodes (stores, DCs, suppliers) to maximize sales, minimize costs, and deliver exceptional customer experiences.

## Initial Assessment

Before designing omnichannel fulfillment, understand:

1. **Channel Mix**
   - What sales channels exist? (stores, website, mobile app, marketplace)
   - Current split of sales by channel?
   - Which channels are growing vs. declining?
   - Cross-channel customer behavior? (research online, buy in store)

2. **Fulfillment Capabilities**
   - Can stores fulfill online orders? (ship-from-store capability)
   - BOPIS/curbside pickup available?
   - Store inventory visibility to online?
   - DC network size and locations?
   - Order management system (OMS) in place?

3. **Current Performance**
   - Online delivery time (2-day, 3-day, week+)?
   - BOPIS adoption rate?
   - Ship-from-store percentage of online orders?
   - Split shipment rate?
   - Fulfillment cost per order by channel?

4. **Business Goals**
   - Priority: Speed, cost, experience, or balance?
   - Target ship-from-store percentage?
   - Inventory turn goals?
   - Customer experience priorities?
   - Profitability by channel?

---

## Omnichannel Fulfillment Framework

### Core Fulfillment Models

**1. Buy Online, Pickup In Store (BOPIS)**
- Customer orders online, picks up at store
- Benefits: Fast (same-day), low cost, drives store traffic
- Challenges: Inventory accuracy, picking efficiency, customer wait time

**2. Ship from Store (SFS)**
- Stores act as mini-fulfillment centers
- Benefits: Faster delivery, reduces DC load, utilizes store inventory
- Challenges: Store labor, packaging supplies, competing with retail operations

**3. Ship from DC**
- Traditional centralized fulfillment
- Benefits: Efficient picking, lower unit costs, inventory concentration
- Challenges: Longer delivery times, higher transportation costs

**4. Marketplace/Dropship**
- Supplier ships directly to customer
- Benefits: No inventory investment, extended assortment
- Challenges: Quality control, delivery time variability, customer experience

**5. Endless Aisle**
- Store orders out-of-stock items for customer
- Benefits: Reduces lost sales, enhances customer experience
- Challenges: Margin pressure, complexity

**6. Reserve Online, Try In Store**
- Customer reserves items online, tries in store before buying
- Benefits: Reduces returns, drives traffic
- Challenges: Inventory holding, operational complexity

---

## Omnichannel Fulfillment Optimization

### Order Routing & Sourcing Logic

**Intelligent Order Routing:**

```python
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

class OmnichannelOrderRouter:
    """
    Intelligent order routing for omnichannel fulfillment

    Routes orders to optimal fulfillment location based on:
    - Inventory availability
    - Customer proximity
    - Delivery speed
    - Fulfillment cost
    - Store/DC capacity
    """

    def __init__(self, fulfillment_nodes, shipping_matrix, cost_matrix):
        """
        Parameters:
        - fulfillment_nodes: DataFrame with node info (stores, DCs)
          columns: ['node_id', 'type', 'lat', 'lon', 'capacity', 'inventory']
        - shipping_matrix: DataFrame with shipping times/costs
        - cost_matrix: Dict with cost per unit by fulfillment type
        """
        self.nodes = fulfillment_nodes
        self.shipping = shipping_matrix
        self.costs = cost_matrix

    def calculate_fulfillment_score(self, order, node):
        """
        Score a fulfillment node for an order

        Lower score = better option
        Balances speed, cost, and inventory health
        """

        # Check inventory availability
        if node['inventory'] < order['quantity']:
            return float('inf')  # Cannot fulfill

        # Calculate distance/delivery time
        distance = self._calculate_distance(
            order['customer_lat'], order['customer_lon'],
            node['lat'], node['lon']
        )

        # Delivery speed score (0-100)
        if node['type'] == 'store' and order['method'] == 'BOPIS':
            delivery_days = 0  # Same day pickup
        elif node['type'] == 'store':
            delivery_days = 1 if distance < 50 else 2
        else:  # DC
            delivery_days = 2 if distance < 500 else 3

        speed_score = delivery_days * 10

        # Cost score (0-100)
        if node['type'] == 'store' and order['method'] == 'BOPIS':
            fulfillment_cost = self.costs['bopis']
        elif node['type'] == 'store':
            fulfillment_cost = self.costs['ship_from_store'] + (distance * 0.5)
        else:
            fulfillment_cost = self.costs['ship_from_dc'] + (distance * 0.3)

        cost_score = fulfillment_cost

        # Inventory health score (0-100)
        # Prefer fulfilling from locations with excess inventory
        weeks_of_supply = node['inventory'] / (node['sales_per_week'] + 0.1)

        if weeks_of_supply > 8:
            inventory_score = -20  # Incentivize using excess inventory
        elif weeks_of_supply < 2:
            inventory_score = 50  # Penalize low inventory
        else:
            inventory_score = 0

        # Capacity score
        capacity_utilization = node['orders_today'] / node['capacity']
        if capacity_utilization > 0.9:
            capacity_score = 30  # Penalize overloaded nodes
        else:
            capacity_score = 0

        # Weighted total score
        total_score = (
            speed_score * 0.4 +
            cost_score * 0.3 +
            inventory_score * 0.2 +
            capacity_score * 0.1
        )

        return total_score

    def route_order(self, order):
        """
        Route order to optimal fulfillment location

        Returns: Best fulfillment node and score
        """

        # Score all eligible nodes
        scores = []
        for idx, node in self.nodes.iterrows():
            score = self.calculate_fulfillment_score(order, node)
            scores.append({
                'node_id': node['node_id'],
                'node_type': node['type'],
                'score': score,
                'delivery_cost': self._estimate_cost(order, node),
                'delivery_days': self._estimate_days(order, node)
            })

        # Select best option
        scores_df = pd.DataFrame(scores)
        best_option = scores_df.loc[scores_df['score'].idxmin()]

        return best_option

    def route_multi_item_order(self, order_items, allow_split=True):
        """
        Route multi-item order

        Decide whether to split shipment or fulfill from single location
        """

        # Try single location fulfillment first
        single_location_options = []

        for idx, node in self.nodes.iterrows():
            can_fulfill_all = all(
                node['inventory_by_sku'].get(item['sku'], 0) >= item['quantity']
                for item in order_items
            )

            if can_fulfill_all:
                total_score = sum(
                    self.calculate_fulfillment_score(
                        {'sku': item['sku'], 'quantity': item['quantity'],
                         'customer_lat': order_items[0]['customer_lat'],
                         'customer_lon': order_items[0]['customer_lon'],
                         'method': order_items[0]['method']},
                        node
                    )
                    for item in order_items
                )

                single_location_options.append({
                    'node_id': node['node_id'],
                    'total_score': total_score,
                    'split': False
                })

        # Try split shipment if allowed
        split_options = []
        if allow_split:
            item_routings = []
            for item in order_items:
                best_node = self.route_order(item)
                item_routings.append(best_node)

            # Calculate split shipment penalty
            unique_nodes = len(set(r['node_id'] for r in item_routings))
            split_penalty = (unique_nodes - 1) * 15  # Penalize splits

            total_split_score = sum(r['score'] for r in item_routings) + split_penalty

            split_options.append({
                'routings': item_routings,
                'total_score': total_split_score,
                'split': True,
                'num_shipments': unique_nodes
            })

        # Compare single vs. split
        all_options = single_location_options + split_options
        if not all_options:
            return {'error': 'Cannot fulfill order'}

        best_option = min(all_options, key=lambda x: x['total_score'])

        return best_option

    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points (miles)"""
        from math import radians, sin, cos, sqrt, atan2

        R = 3959  # Earth radius in miles

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        return R * c

    def _estimate_cost(self, order, node):
        """Estimate fulfillment cost"""
        if node['type'] == 'store' and order.get('method') == 'BOPIS':
            return self.costs['bopis']
        elif node['type'] == 'store':
            return self.costs['ship_from_store']
        else:
            return self.costs['ship_from_dc']

    def _estimate_days(self, order, node):
        """Estimate delivery days"""
        distance = self._calculate_distance(
            order['customer_lat'], order['customer_lon'],
            node['lat'], node['lon']
        )

        if node['type'] == 'store' and order.get('method') == 'BOPIS':
            return 0
        elif distance < 50:
            return 1
        elif distance < 200:
            return 2
        else:
            return 3

# Example usage
fulfillment_nodes = pd.DataFrame({
    'node_id': ['DC1', 'Store_101', 'Store_102', 'Store_103'],
    'type': ['dc', 'store', 'store', 'store'],
    'lat': [40.7128, 40.7580, 40.6782, 40.7489],
    'lon': [-74.0060, -73.9855, -73.9442, -73.9680],
    'capacity': [5000, 50, 50, 50],
    'inventory': [10000, 500, 300, 450],
    'sales_per_week': [2000, 100, 80, 90],
    'orders_today': [2500, 25, 30, 20]
})

cost_matrix = {
    'bopis': 2.50,
    'ship_from_store': 8.50,
    'ship_from_dc': 6.00
}

router = OmnichannelOrderRouter(fulfillment_nodes, None, cost_matrix)

# Route single order
order = {
    'sku': 'SKU123',
    'quantity': 2,
    'customer_lat': 40.7589,
    'customer_lon': -73.9851,
    'method': 'ship'
}

best_fulfillment = router.route_order(order)
print(f"Route order to: {best_fulfillment['node_id']}")
print(f"Estimated delivery: {best_fulfillment['delivery_days']} days")
print(f"Estimated cost: ${best_fulfillment['delivery_cost']:.2f}")
```

### BOPIS Optimization

**Store Pickup Operations:**

```python
class BOPISOptimizer:
    """
    Optimize Buy Online Pickup In Store (BOPIS) operations

    Focus on:
    - Inventory allocation (reserve for online vs. in-store)
    - Picking efficiency
    - Customer wait time reduction
    - Store capacity management
    """

    def __init__(self, store_config):
        self.store = store_config

    def allocate_inventory(self, sku, available_qty, online_demand_forecast,
                          instore_demand_forecast):
        """
        Allocate inventory between online and in-store channels

        Prevent online channel from selling out store inventory
        """

        total_demand = online_demand_forecast + instore_demand_forecast

        if available_qty >= total_demand:
            # Plenty of inventory - allocate all
            return {
                'online_allocation': online_demand_forecast,
                'instore_allocation': instore_demand_forecast,
                'allocation_strategy': 'Full allocation'
            }

        # Scarce inventory - prioritize based on margin and strategy
        online_margin_per_unit = self.store['online_margin']
        instore_margin_per_unit = self.store['instore_margin']

        # Also consider strategic value (online drives future loyalty)
        online_strategic_value = 1.2  # 20% premium for online
        instore_strategic_value = 1.0

        online_value = online_margin_per_unit * online_strategic_value
        instore_value = instore_margin_per_unit * instore_strategic_value

        # Allocate proportionally to value
        online_pct = online_value / (online_value + instore_value)

        online_allocation = min(
            int(available_qty * online_pct),
            online_demand_forecast
        )
        instore_allocation = available_qty - online_allocation

        return {
            'online_allocation': online_allocation,
            'instore_allocation': instore_allocation,
            'allocation_strategy': 'Value-based allocation',
            'online_pct': online_pct
        }

    def optimize_pickup_scheduling(self, orders, picker_capacity_per_hour=10):
        """
        Schedule BOPIS orders for picking

        Balance speed (customer satisfaction) with efficiency
        """

        orders_df = pd.DataFrame(orders)
        orders_df['order_time'] = pd.to_datetime(orders_df['order_time'])

        # Categorize by urgency
        orders_df['hours_until_pickup'] = (
            pd.to_datetime(orders_df['requested_pickup_time']) -
            orders_df['order_time']
        ).dt.total_seconds() / 3600

        # Priority scoring
        def calculate_priority(row):
            # High priority: short time until pickup, VIP customer, large order
            urgency_score = 100 / max(row['hours_until_pickup'], 0.5)
            vip_score = 20 if row.get('is_vip', False) else 0
            size_score = min(row['num_items'] * 2, 20)

            return urgency_score + vip_score + size_score

        orders_df['priority_score'] = orders_df.apply(calculate_priority, axis=1)

        # Sort by priority
        orders_df = orders_df.sort_values('priority_score', ascending=False)

        # Assign to time slots
        orders_df['assigned_pick_time'] = None
        current_time = datetime.now()
        orders_picked = 0
        slot_start = current_time

        for idx, order in orders_df.iterrows():
            # Estimate pick time for this order
            pick_time_minutes = order['num_items'] * 2  # 2 min per item

            # Assign to current slot
            orders_df.at[idx, 'assigned_pick_time'] = slot_start
            orders_df.at[idx, 'estimated_ready_time'] = (
                slot_start + timedelta(minutes=pick_time_minutes)
            )

            # Update slot
            orders_picked += 1
            if orders_picked >= picker_capacity_per_hour:
                slot_start += timedelta(hours=1)
                orders_picked = 0

        return orders_df[['order_id', 'priority_score', 'assigned_pick_time',
                         'estimated_ready_time', 'requested_pickup_time']]

    def calculate_bopis_roi(self, bopis_orders_per_month, avg_basket_size,
                           bopis_operating_cost_per_order=3.50):
        """
        Calculate ROI of BOPIS program

        Benefits:
        - Incremental sales from convenience
        - Additional impulse purchases in store
        - Reduced delivery costs vs. ship to home
        - Customer lifetime value increase
        """

        # Direct costs
        monthly_operating_cost = bopis_orders_per_month * bopis_operating_cost_per_order

        # Benefits
        # 1. Incremental purchases (customers buy more when picking up)
        impulse_purchase_rate = 0.35  # 35% buy additional items
        avg_impulse_purchase = 25
        impulse_revenue = (
            bopis_orders_per_month *
            impulse_purchase_rate *
            avg_impulse_purchase
        )

        # 2. Cost savings vs. home delivery
        home_delivery_cost = 8.50
        cost_savings = bopis_orders_per_month * (home_delivery_cost - bopis_operating_cost_per_order)

        # 3. Customer lifetime value increase (satisfaction)
        ltv_increase_per_customer = 50
        new_customers_per_month = bopis_orders_per_month * 0.3
        ltv_benefit = new_customers_per_month * ltv_increase_per_customer

        # 4. Inventory turns improvement (use store inventory)
        inventory_turn_benefit = bopis_orders_per_month * avg_basket_size * 0.05  # 5% carrying cost saved

        total_monthly_benefit = (
            impulse_revenue +
            cost_savings +
            ltv_benefit +
            inventory_turn_benefit
        )

        roi = (total_monthly_benefit - monthly_operating_cost) / monthly_operating_cost

        return {
            'monthly_cost': monthly_operating_cost,
            'monthly_benefit': total_monthly_benefit,
            'net_monthly_benefit': total_monthly_benefit - monthly_operating_cost,
            'roi': roi,
            'impulse_revenue': impulse_revenue,
            'cost_savings': cost_savings,
            'ltv_benefit': ltv_benefit
        }

# Example
bopis_optimizer = BOPISOptimizer({
    'online_margin': 15,
    'instore_margin': 18
})

# Inventory allocation
allocation = bopis_optimizer.allocate_inventory(
    sku='SKU456',
    available_qty=50,
    online_demand_forecast=30,
    instore_demand_forecast=35
)
print(f"Online allocation: {allocation['online_allocation']} units")
print(f"In-store allocation: {allocation['instore_allocation']} units")

# ROI calculation
roi_analysis = bopis_optimizer.calculate_bopis_roi(
    bopis_orders_per_month=2500,
    avg_basket_size=75
)
print(f"\nBOPIS ROI: {roi_analysis['roi']:.1%}")
print(f"Net monthly benefit: ${roi_analysis['net_monthly_benefit']:,.0f}")
```

### Ship-from-Store Optimization

**Store Fulfillment Capacity:**

```python
class ShipFromStoreOptimizer:
    """
    Optimize ship-from-store operations

    Balance store operations with fulfillment duties
    """

    def __init__(self, stores_config):
        self.stores = pd.DataFrame(stores_config)

    def calculate_store_fulfillment_capacity(self, store_id):
        """
        Determine optimal ship-from-store capacity for a store

        Based on:
        - Store traffic patterns
        - Staff availability
        - Physical space
        - Historical performance
        """

        store = self.stores[self.stores['store_id'] == store_id].iloc[0]

        # Available hours for fulfillment (avoid peak retail hours)
        if store['format'] == 'mall':
            fulfillment_hours_per_day = 4  # Morning before crowds
        elif store['format'] == 'strip':
            fulfillment_hours_per_day = 6
        else:
            fulfillment_hours_per_day = 8

        # Picking rate
        items_per_hour = 15

        # Staff allocation (% of staff that can be dedicated)
        staff_available = store['total_staff'] * 0.3  # 30% for online

        # Daily capacity
        daily_capacity = (
            fulfillment_hours_per_day *
            items_per_hour *
            staff_available
        )

        # Adjust for store size and layout
        if store['square_feet'] < 5000:
            space_factor = 0.7  # Cramped
        elif store['square_feet'] > 20000:
            space_factor = 1.2  # Ample space
        else:
            space_factor = 1.0

        daily_capacity *= space_factor

        return {
            'store_id': store_id,
            'daily_capacity_orders': int(daily_capacity / 3),  # 3 items per order avg
            'daily_capacity_units': int(daily_capacity),
            'fulfillment_hours': fulfillment_hours_per_day,
            'recommended_staff': staff_available
        }

    def allocate_online_orders_to_stores(self, orders, max_distance_miles=50):
        """
        Allocate online orders to stores for fulfillment

        Balances proximity, capacity, and inventory
        """

        allocations = []

        for order in orders:
            # Find eligible stores (within range, have inventory, have capacity)
            eligible_stores = []

            for idx, store in self.stores.iterrows():
                # Check distance
                distance = self._calculate_distance(
                    order['customer_lat'], order['customer_lon'],
                    store['lat'], store['lon']
                )

                if distance > max_distance_miles:
                    continue

                # Check inventory
                has_inventory = all(
                    store['inventory'].get(item['sku'], 0) >= item['quantity']
                    for item in order['items']
                )

                if not has_inventory:
                    continue

                # Check capacity
                capacity = self.calculate_store_fulfillment_capacity(store['store_id'])
                if store['orders_today'] >= capacity['daily_capacity_orders']:
                    continue

                # Calculate score
                score = distance  # Lower is better

                # Adjust for inventory health
                total_inventory_days = sum(
                    store['inventory'].get(item['sku'], 0) / store['sales_velocity'].get(item['sku'], 1)
                    for item in order['items']
                )

                if total_inventory_days > 60:
                    score *= 0.8  # Prefer stores with excess inventory

                eligible_stores.append({
                    'store_id': store['store_id'],
                    'distance': distance,
                    'score': score
                })

            if eligible_stores:
                # Select best store
                best_store = min(eligible_stores, key=lambda x: x['score'])
                allocations.append({
                    'order_id': order['order_id'],
                    'assigned_store': best_store['store_id'],
                    'distance': best_store['distance'],
                    'estimated_delivery_days': 1 if best_store['distance'] < 25 else 2
                })
            else:
                # No eligible store - route to DC
                allocations.append({
                    'order_id': order['order_id'],
                    'assigned_store': 'DC',
                    'distance': None,
                    'estimated_delivery_days': 3
                })

        return pd.DataFrame(allocations)

    def calculate_sfs_economics(self, annual_sfs_orders, avg_order_value=65):
        """
        Calculate economics of ship-from-store program

        Compare to DC fulfillment
        """

        # Ship-from-store costs
        sfs_labor_per_order = 4.50
        sfs_packaging_per_order = 1.20
        sfs_shipping_per_order = 7.00  # Lower than DC due to proximity
        sfs_overhead_per_order = 1.00
        sfs_total_cost_per_order = (
            sfs_labor_per_order +
            sfs_packaging_per_order +
            sfs_shipping_per_order +
            sfs_overhead_per_order
        )

        # DC fulfillment costs
        dc_labor_per_order = 3.00  # More efficient
        dc_packaging_per_order = 1.00
        dc_shipping_per_order = 9.50  # Farther from customer
        dc_overhead_per_order = 0.80
        dc_total_cost_per_order = (
            dc_labor_per_order +
            dc_packaging_per_order +
            dc_shipping_per_order +
            dc_overhead_per_order
        )

        # Annual comparison
        sfs_annual_cost = annual_sfs_orders * sfs_total_cost_per_order
        dc_annual_cost = annual_sfs_orders * dc_total_cost_per_order

        # Additional benefits of SFS
        # 1. Reduced inventory holding (use store stock)
        inventory_benefit = annual_sfs_orders * avg_order_value * 0.02  # 2% carrying cost

        # 2. Faster delivery (premium pricing potential)
        speed_benefit = annual_sfs_orders * 1.50  # $1.50 premium per order

        # 3. Reduced stockouts (more inventory nodes)
        stockout_reduction_benefit = annual_sfs_orders * avg_order_value * 0.01

        total_sfs_benefit = inventory_benefit + speed_benefit + stockout_reduction_benefit

        net_sfs_advantage = (dc_annual_cost - sfs_annual_cost) + total_sfs_benefit

        return {
            'annual_sfs_orders': annual_sfs_orders,
            'sfs_cost_per_order': sfs_total_cost_per_order,
            'dc_cost_per_order': dc_total_cost_per_order,
            'cost_difference_per_order': dc_total_cost_per_order - sfs_total_cost_per_order,
            'annual_cost_savings': dc_annual_cost - sfs_annual_cost,
            'additional_benefits': total_sfs_benefit,
            'net_annual_advantage': net_sfs_advantage,
            'roi_vs_dc': net_sfs_advantage / sfs_annual_cost if sfs_annual_cost > 0 else 0
        }

    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance in miles"""
        from math import radians, sin, cos, sqrt, atan2
        R = 3959
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return R * c

# Example
stores_config = [
    {'store_id': 'S001', 'format': 'mall', 'total_staff': 20, 'square_feet': 8000,
     'lat': 40.7589, 'lon': -73.9851, 'orders_today': 5},
    {'store_id': 'S002', 'format': 'strip', 'total_staff': 15, 'square_feet': 12000,
     'lat': 40.7128, 'lon': -74.0060, 'orders_today': 8},
]

sfs_optimizer = ShipFromStoreOptimizer(stores_config)

# Calculate capacity
capacity = sfs_optimizer.calculate_store_fulfillment_capacity('S001')
print(f"Store S001 daily capacity: {capacity['daily_capacity_orders']} orders")

# Economics
economics = sfs_optimizer.calculate_sfs_economics(annual_sfs_orders=50000)
print(f"Ship-from-store saves: ${economics['cost_difference_per_order']:.2f} per order")
print(f"Annual advantage: ${economics['net_annual_advantage']:,.0f}")
```

---

## Unified Inventory Visibility

**Real-Time Inventory Sync:**

```python
class UnifiedInventoryManager:
    """
    Manage unified inventory across all channels and nodes

    Challenges:
    - Real-time sync across systems
    - Inventory reservations
    - In-transit inventory
    - Accuracy issues
    """

    def __init__(self):
        self.inventory = {}  # SKU -> {node -> quantity}
        self.reservations = {}  # SKU -> {node -> reserved_qty}

    def get_available_to_promise(self, sku, node_id=None):
        """
        Calculate Available-to-Promise (ATP) inventory

        ATP = On-hand - Reserved - Safety stock
        """

        if node_id:
            nodes = [node_id]
        else:
            nodes = self.inventory.get(sku, {}).keys()

        atp_by_node = {}

        for node in nodes:
            on_hand = self.inventory.get(sku, {}).get(node, 0)
            reserved = self.reservations.get(sku, {}).get(node, 0)
            safety_stock = self._get_safety_stock(sku, node)

            atp = max(0, on_hand - reserved - safety_stock)
            atp_by_node[node] = atp

        return atp_by_node

    def reserve_inventory(self, order_id, sku, quantity, node_id,
                         reservation_duration_minutes=15):
        """
        Reserve inventory for an order

        Prevents overselling while customer completes purchase
        """

        atp = self.get_available_to_promise(sku, node_id)

        if atp.get(node_id, 0) < quantity:
            return {
                'success': False,
                'reason': 'Insufficient ATP',
                'available': atp.get(node_id, 0)
            }

        # Create reservation
        if sku not in self.reservations:
            self.reservations[sku] = {}
        if node_id not in self.reservations[sku]:
            self.reservations[sku][node_id] = 0

        self.reservations[sku][node_id] += quantity

        # Schedule expiration (would use job scheduler in production)
        expiration_time = datetime.now() + timedelta(minutes=reservation_duration_minutes)

        return {
            'success': True,
            'order_id': order_id,
            'sku': sku,
            'quantity': quantity,
            'node_id': node_id,
            'expires_at': expiration_time
        }

    def allocate_inventory_across_channels(self, sku, total_available,
                                          channel_forecasts):
        """
        Allocate inventory across channels (online, store, wholesale, etc.)

        Balance channel priorities and demand
        """

        # Calculate total demand
        total_demand = sum(channel_forecasts.values())

        if total_available >= total_demand:
            # Sufficient inventory - allocate all
            return channel_forecasts

        # Scarce inventory - prioritize by channel value
        channel_priority = {
            'online': 1.2,  # 20% premium (strategic)
            'store': 1.0,
            'wholesale': 0.8,
            'marketplace': 0.9
        }

        # Weight demands by priority
        weighted_demands = {
            channel: demand * channel_priority.get(channel, 1.0)
            for channel, demand in channel_forecasts.items()
        }

        total_weighted = sum(weighted_demands.values())

        # Allocate proportionally
        allocations = {
            channel: int(total_available * (weighted / total_weighted))
            for channel, weighted in weighted_demands.items()
        }

        # Handle rounding (allocate remainder to highest priority)
        allocated_sum = sum(allocations.values())
        if allocated_sum < total_available:
            # Give remainder to highest priority channel
            highest_priority_channel = max(
                channel_priority.items(),
                key=lambda x: x[1]
            )[0]
            if highest_priority_channel in allocations:
                allocations[highest_priority_channel] += (total_available - allocated_sum)

        return allocations

    def _get_safety_stock(self, sku, node):
        """Get safety stock for SKU at node"""
        # Simplified - would calculate based on demand variability
        return 10

# Example
inventory_manager = UnifiedInventoryManager()
inventory_manager.inventory = {
    'SKU789': {
        'DC1': 1000,
        'Store_101': 50,
        'Store_102': 30
    }
}

# Check ATP
atp = inventory_manager.get_available_to_promise('SKU789')
print(f"Available-to-Promise: {atp}")

# Reserve inventory
reservation = inventory_manager.reserve_inventory(
    order_id='ORD123',
    sku='SKU789',
    quantity=2,
    node_id='Store_101'
)
print(f"Reservation: {reservation['success']}")

# Allocate across channels
channel_forecasts = {
    'online': 500,
    'store': 400,
    'wholesale': 200
}

allocations = inventory_manager.allocate_inventory_across_channels(
    sku='SKU789',
    total_available=800,
    channel_forecasts=channel_forecasts
)
print(f"Channel allocations: {allocations}")
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `pulp`, `pyomo`: Mathematical optimization for order routing
- `scipy`: Optimization algorithms
- `ortools`: Google OR-Tools for vehicle routing

**Geospatial:**
- `geopy`: Distance calculations
- `folium`: Map visualization
- `geopandas`: Geospatial data analysis

**Data Processing:**
- `pandas`: Data manipulation
- `numpy`: Numerical computations
- `scikit-learn`: Clustering for zone optimization

### Commercial Software

**Order Management Systems (OMS):**
- **Manhattan Active Omni**: Enterprise OMS
- **Fluent Commerce**: Cloud-native OMS
- **IBM Sterling**: Order management
- **Blue Yonder Luminate**: Omnichannel fulfillment
- **Salesforce Order Management**: Cloud OMS

**Inventory Management:**
- **Radial**: Omnichannel inventory optimization
- **CommerceHub**: Distributed order management
- **Deposco**: Inventory & fulfillment platform
- **Brightpearl**: Retail operations platform

**Store Systems:**
- **Shopify POS**: Point of sale with online integration
- **Square**: POS and omnichannel
- **NCR**: Retail POS systems
- **Oracle Retail**: Enterprise retail management

---

## Common Challenges & Solutions

### Challenge: Inventory Accuracy

**Problem:**
- Store inventory often inaccurate (shrink, mis-scans)
- Online shows available but store doesn't have it
- Customer frustration, failed BOPIS orders

**Solutions:**
- RFID for real-time inventory tracking
- Perpetual inventory systems
- Regular cycle counts
- Safety stock buffers for online channel
- Probabilistic ATP (account for accuracy)
- Customer notification if item unavailable during pick

### Challenge: Split Shipment Decisions

**Problem:**
- Customer wants fast delivery
- Items available at different locations
- Split shipments increase cost but improve speed

**Solutions:**
- Cost-benefit analysis per order
- Customer preference (allow choice)
- Minimum split threshold (only split if saves 2+ days)
- Free shipping threshold incentives
- Show estimated delivery dates in cart
- Intelligent bundling algorithms

### Challenge: Store Capacity Constraints

**Problem:**
- Stores busy during peak hours
- Online fulfillment competes with retail operations
- Staff overwhelmed

**Solutions:**
- Dynamic capacity management
- Route orders to less busy stores
- Dedicated online fulfillment staff during peak
- Micro-fulfillment centers near stores
- After-hours picking programs
- BOPIS time slot management

### Challenge: Returns Complexity

**Problem:**
- Buy online, return in store (complexity)
- Buy in store, return by mail
- Inventory reallocation after returns
- Refund timing issues

**Solutions:**
- Unified return processing system
- Instant credit upon store return
- Return to any location policy
- Automated restocking workflows
- Return fraud detection
- Cross-channel return analytics

### Challenge: Profitability by Channel

**Problem:**
- Some fulfillment methods unprofitable
- Hard to measure true channel profitability
- Free shipping expectations

**Solutions:**
- Fully-loaded cost accounting by channel
- Minimum order values for free shipping
- BOPIS/pickup incentives (discounts)
- Shipping pass subscriptions
- Zone-based shipping fees
- Product-level profitability analysis

---

## Output Format

### Omnichannel Fulfillment Analysis Report

**Executive Summary:**
- Total orders by channel: Online 45%, Store 40%, BOPIS 15%
- Current fulfillment costs: $8.20 per order
- Ship-from-store percentage: 22%
- Target: Increase SFS to 40%, reduce cost to $7.00

**Channel Performance:**

| Channel | Orders/Month | Avg Basket | Fulfillment Cost | Net Margin | Growth YoY |
|---------|-------------|------------|------------------|------------|------------|
| E-commerce | 45,000 | $72 | $9.50 | 18% | +35% |
| BOPIS | 15,000 | $68 | $3.50 | 24% | +125% |
| Ship from Store | 22,000 | $65 | $8.00 | 19% | +80% |
| Store Retail | 40,000 | $58 | $2.00 | 22% | -5% |

**Fulfillment Network Utilization:**

| Node Type | # Locations | Capacity Util | Orders/Day | Avg Distance | Delivery Speed |
|-----------|-------------|---------------|------------|--------------|----------------|
| Distribution Centers | 3 | 68% | 1,200 | 450 mi | 3.2 days |
| Ship-from-Store | 45 | 42% | 800 | 35 mi | 1.8 days |
| BOPIS Pickup | 120 | 35% | 500 | 8 mi | Same day |

**Order Routing Analysis:**

- **Single-location fulfillment**: 78%
- **Split shipments**: 22%
- **Average splits per order**: 1.3 locations
- **Routing efficiency**: 82% (% routed to optimal location)

**Optimization Opportunities:**

1. **Expand ship-from-store (22% → 40%)**
   - Enable 50 additional stores for SFS
   - Investment: $250K (picking stations, training)
   - Expected impact: -$1.20 per order, -0.8 days delivery time
   - Annual savings: $650K

2. **Improve inventory accuracy (85% → 95%)**
   - RFID implementation in top 50 stores
   - Investment: $400K
   - Expected impact: -5% failed BOPIS, +8% BOPIS adoption
   - Annual savings: $320K + revenue lift

3. **Intelligent order routing optimization**
   - Implement ML-based routing engine
   - Investment: $150K
   - Expected impact: +15% routing efficiency, -$0.40 per order
   - Annual savings: $480K

4. **BOPIS expansion**
   - Add 30 BOPIS-capable stores
   - Investment: $180K
   - Expected impact: +10K orders/month, $25 impulse purchase lift
   - Annual benefit: $850K

**Implementation Roadmap:**

| Quarter | Initiative | Investment | Annual Benefit | Payback |
|---------|-----------|------------|----------------|---------|
| Q1 | Order routing optimization | $150K | $480K | 3.8 mo |
| Q2 | BOPIS expansion (30 stores) | $180K | $850K | 2.5 mo |
| Q3 | SFS expansion (50 stores) | $250K | $650K | 4.6 mo |
| Q4 | RFID inventory accuracy | $400K | $320K | 15 mo |

**Expected Results (Year 1):**

| Metric | Current | Year 1 Target | Improvement |
|--------|---------|---------------|-------------|
| Fulfillment cost per order | $8.20 | $7.00 | -15% |
| Ship-from-store % | 22% | 40% | +18 pts |
| Avg delivery speed | 2.8 days | 2.1 days | -0.7 days |
| BOPIS orders/month | 15,000 | 25,000 | +67% |
| Split shipment rate | 22% | 18% | -4 pts |
| Inventory accuracy | 85% | 95% | +10 pts |

---

## Questions to Ask

If you need more context:
1. What channels do you sell through? (stores, online, marketplace, mobile)
2. Do stores currently fulfill online orders? (BOPIS, ship-from-store)
3. How many stores and DCs in your network?
4. What's your current online order volume?
5. What percentage of online orders are BOPIS?
6. What's your average delivery time for online orders?
7. Do you have real-time inventory visibility across channels?
8. What systems do you use? (OMS, WMS, POS, e-commerce platform)
9. What are your main pain points? (cost, speed, experience, complexity)

---

## Related Skills

- **ecommerce-fulfillment**: Pure e-commerce fulfillment strategy
- **retail-allocation**: Initial allocation to stores
- **retail-replenishment**: Store replenishment optimization
- **last-mile-delivery**: Final delivery optimization
- **route-optimization**: Delivery route planning
- **warehouse-design**: DC and micro-fulfillment center design
- **network-design**: Fulfillment network strategy
- **inventory-optimization**: Safety stock and reorder points
- **demand-forecasting**: Channel demand forecasting
