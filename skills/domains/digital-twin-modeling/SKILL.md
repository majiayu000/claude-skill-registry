---
name: digital-twin-modeling
description: When the user wants to build digital twins, simulate supply chain operations, or create virtual replicas for testing. Also use when the user mentions "digital twin," "simulation modeling," "discrete event simulation," "system simulation," "virtual supply chain," "what-if analysis," "scenario simulation," or "operational testing." For network optimization, see network-design. For forecasting, see demand-forecasting.
---

# Digital Twin Modeling

You are an expert in digital twin modeling and supply chain simulation. Your goal is to help build virtual replicas of supply chain systems that enable testing, scenario analysis, optimization, and predictive insights without disrupting real operations.

## Initial Assessment

Before building a digital twin, understand:

1. **Business Context**
   - What supply chain system needs a digital twin? (warehouse, network, production line)
   - What decisions will the twin support? (capacity planning, layout design, policy testing)
   - Current pain points? (bottlenecks, unpredictable performance, risky changes)
   - Expected ROI or value from digital twin?

2. **System Scope**
   - Physical assets to model? (facilities, equipment, vehicles, inventory)
   - Processes to simulate? (order fulfillment, production, transportation)
   - System boundaries? (single facility, network, end-to-end supply chain)
   - Level of detail needed? (high-level vs. detailed operations)

3. **Data Availability**
   - Historical operational data? (transaction logs, sensor data, timestamps)
   - System parameters? (capacities, speeds, processing times)
   - Demand patterns and variability?
   - Real-time data feeds available? (IoT, ERP, WMS, TMS)

4. **Technical Environment**
   - Simulation expertise in team?
   - Preferred tools? (Python, Arena, AnyLogic, FlexSim)
   - Integration requirements? (ERP, real-time dashboards)
   - Computational resources available?

---

## Digital Twin Framework

### Digital Twin Maturity Levels

**Level 1: Descriptive Twin** (What happened?)
- Static 3D model or visualization
- Historical data replay
- Basic reporting
- No predictive capability

**Level 2: Informative Twin** (Why did it happen?)
- Real-time data integration
- Performance monitoring
- KPI dashboards
- Diagnostic analytics

**Level 3: Predictive Twin** (What will happen?)
- Simulation models
- Scenario analysis
- Forecasting capabilities
- What-if testing

**Level 4: Prescriptive Twin** (What should we do?)
- Optimization integration
- Automated recommendations
- Autonomous decision-making
- Continuous learning (ML integration)

**Level 5: Autonomous Twin** (Self-optimizing)
- Fully autonomous operations
- Self-healing capabilities
- Continuous adaptation
- Closed-loop control

### Digital Twin Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Digital Twin Layer                    │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Visualization│  │  Simulation  │  │ Optimization │ │
│  │    Layer     │  │    Engine    │  │    Engine    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────┤
│                    Analytics Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Real-Time  │  │  Predictive  │  │ Prescriptive │ │
│  │   Analytics  │  │    Models    │  │   Analytics  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────┤
│                 Data Integration Layer                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Historical  │  │  Real-Time   │  │   External   │ │
│  │     Data     │  │  Streaming   │  │  Data APIs   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────┤
│                   Physical Assets Layer                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Warehouses  │  │ Transportation│  │  Production  │ │
│  │   & DCs      │  │    Fleet     │  │  Facilities  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## Simulation Modeling Approaches

### Discrete Event Simulation (DES)

**Best For:**
- Order fulfillment processes
- Manufacturing operations
- Warehouse operations
- Transportation networks

**Key Concepts:**
- Events occur at discrete points in time
- Entities (orders, products, trucks) move through system
- Resources (workers, equipment) constrain flow
- Queues form when demand exceeds capacity

**Python Implementation with SimPy:**

```python
import simpy
import random
import pandas as pd
import numpy as np

class WarehouseDigitalTwin:
    """
    Digital twin of warehouse operations using discrete event simulation
    """

    def __init__(self, env, config):
        """
        Initialize warehouse digital twin

        config: dictionary with warehouse parameters
        - num_receiving_docks
        - num_pickers
        - num_packing_stations
        - num_shipping_docks
        """
        self.env = env
        self.config = config

        # Resources
        self.receiving_docks = simpy.Resource(env, config['num_receiving_docks'])
        self.pickers = simpy.Resource(env, config['num_pickers'])
        self.packing_stations = simpy.Resource(env, config['num_packing_stations'])
        self.shipping_docks = simpy.Resource(env, config['num_shipping_docks'])

        # Performance tracking
        self.metrics = {
            'orders_completed': 0,
            'total_cycle_time': 0,
            'receiving_queue_times': [],
            'picking_queue_times': [],
            'packing_queue_times': [],
            'shipping_queue_times': []
        }

    def receive_inventory(self, shipment_id):
        """Simulate receiving process"""

        arrival_time = self.env.now

        # Wait for receiving dock
        with self.receiving_docks.request() as request:
            yield request

            queue_time = self.env.now - arrival_time
            self.metrics['receiving_queue_times'].append(queue_time)

            # Unloading time (varies by shipment size)
            unload_time = random.uniform(30, 60)  # minutes
            yield self.env.timeout(unload_time)

            # Put-away time
            putaway_time = random.uniform(20, 40)
            yield self.env.timeout(putaway_time)

    def fulfill_order(self, order_id, num_items):
        """Simulate order fulfillment process"""

        order_start = self.env.now

        # Picking process
        pick_arrival = self.env.now
        with self.pickers.request() as request:
            yield request

            pick_queue_time = self.env.now - pick_arrival
            self.metrics['picking_queue_times'].append(pick_queue_time)

            # Picking time depends on number of items
            pick_time = num_items * random.uniform(2, 4)  # minutes per item
            yield self.env.timeout(pick_time)

        # Packing process
        pack_arrival = self.env.now
        with self.packing_stations.request() as request:
            yield request

            pack_queue_time = self.env.now - pack_arrival
            self.metrics['packing_queue_times'].append(pack_queue_time)

            # Packing time
            pack_time = random.uniform(5, 15)  # minutes
            yield self.env.timeout(pack_time)

        # Shipping process
        ship_arrival = self.env.now
        with self.shipping_docks.request() as request:
            yield request

            ship_queue_time = self.env.now - ship_arrival
            self.metrics['shipping_queue_times'].append(ship_queue_time)

            # Loading time
            load_time = random.uniform(5, 10)  # minutes
            yield self.env.timeout(load_time)

        # Record completion
        cycle_time = self.env.now - order_start
        self.metrics['orders_completed'] += 1
        self.metrics['total_cycle_time'] += cycle_time

    def generate_orders(self, arrival_rate=5):
        """
        Generate order arrivals (Poisson process)

        arrival_rate: average orders per hour
        """
        order_num = 0

        while True:
            # Inter-arrival time (exponential distribution)
            inter_arrival = random.expovariate(arrival_rate / 60)  # convert to minutes
            yield self.env.timeout(inter_arrival)

            # Create order
            order_num += 1
            num_items = random.randint(1, 10)

            # Start order fulfillment process
            self.env.process(self.fulfill_order(order_num, num_items))

    def run_simulation(self, duration_hours):
        """Run simulation for specified duration"""

        # Start order generation
        self.env.process(self.generate_orders(arrival_rate=5))

        # Run simulation
        self.env.run(until=duration_hours * 60)  # convert to minutes

        # Calculate summary metrics
        return self.get_performance_metrics()

    def get_performance_metrics(self):
        """Calculate and return performance metrics"""

        metrics = {
            'orders_completed': self.metrics['orders_completed'],
            'avg_cycle_time_min': (self.metrics['total_cycle_time'] /
                                   self.metrics['orders_completed']
                                   if self.metrics['orders_completed'] > 0 else 0),
            'avg_receiving_queue_min': (np.mean(self.metrics['receiving_queue_times'])
                                        if self.metrics['receiving_queue_times'] else 0),
            'avg_picking_queue_min': (np.mean(self.metrics['picking_queue_times'])
                                      if self.metrics['picking_queue_times'] else 0),
            'avg_packing_queue_min': (np.mean(self.metrics['packing_queue_times'])
                                      if self.metrics['packing_queue_times'] else 0),
            'avg_shipping_queue_min': (np.mean(self.metrics['shipping_queue_times'])
                                       if self.metrics['shipping_queue_times'] else 0),
            'throughput_orders_per_hour': (self.metrics['orders_completed'] /
                                          (self.env.now / 60))
        }

        return metrics

# Run simulation
env = simpy.Environment()

config = {
    'num_receiving_docks': 3,
    'num_pickers': 10,
    'num_packing_stations': 5,
    'num_shipping_docks': 4
}

warehouse_twin = WarehouseDigitalTwin(env, config)
results = warehouse_twin.run_simulation(duration_hours=8)

print("Warehouse Performance Metrics:")
print(f"Orders Completed: {results['orders_completed']}")
print(f"Average Cycle Time: {results['avg_cycle_time_min']:.1f} minutes")
print(f"Throughput: {results['throughput_orders_per_hour']:.1f} orders/hour")
print(f"Average Picking Queue Time: {results['avg_picking_queue_min']:.1f} minutes")
```

### Scenario Analysis with Digital Twin

```python
def scenario_analysis(base_config, scenarios, num_replications=10):
    """
    Run multiple scenarios to compare performance

    scenarios: dict of scenario configs to test
    num_replications: number of simulation runs per scenario
    """

    results = []

    for scenario_name, scenario_config in scenarios.items():
        print(f"\nRunning scenario: {scenario_name}")

        scenario_results = []

        for rep in range(num_replications):
            # Create new environment
            env = simpy.Environment()

            # Merge base config with scenario config
            config = {**base_config, **scenario_config}

            # Run simulation
            warehouse = WarehouseDigitalTwin(env, config)
            metrics = warehouse.run_simulation(duration_hours=8)

            metrics['scenario'] = scenario_name
            metrics['replication'] = rep
            scenario_results.append(metrics)

        results.extend(scenario_results)

    # Convert to DataFrame for analysis
    results_df = pd.DataFrame(results)

    # Calculate summary statistics by scenario
    summary = results_df.groupby('scenario').agg({
        'orders_completed': ['mean', 'std'],
        'avg_cycle_time_min': ['mean', 'std'],
        'throughput_orders_per_hour': ['mean', 'std']
    }).round(2)

    return results_df, summary

# Define scenarios
base_config = {
    'num_receiving_docks': 3,
    'num_pickers': 10,
    'num_packing_stations': 5,
    'num_shipping_docks': 4
}

scenarios = {
    'Baseline': {},
    'Add_Pickers': {'num_pickers': 15},
    'Add_Packing': {'num_packing_stations': 8},
    'Add_Both': {'num_pickers': 15, 'num_packing_stations': 8}
}

results_df, summary = scenario_analysis(base_config, scenarios, num_replications=20)

print("\nScenario Comparison:")
print(summary)

# Visualize results
import matplotlib.pyplot as plt
import seaborn as sns

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Cycle time comparison
sns.boxplot(data=results_df, x='scenario', y='avg_cycle_time_min', ax=axes[0])
axes[0].set_title('Cycle Time by Scenario')
axes[0].set_ylabel('Average Cycle Time (minutes)')
axes[0].set_xlabel('Scenario')

# Throughput comparison
sns.boxplot(data=results_df, x='scenario', y='throughput_orders_per_hour', ax=axes[1])
axes[1].set_title('Throughput by Scenario')
axes[1].set_ylabel('Orders per Hour')
axes[1].set_xlabel('Scenario')

plt.tight_layout()
plt.show()
```

---

## Advanced Digital Twin Components

### Agent-Based Modeling (ABM)

**Best For:**
- Complex adaptive systems
- Distributed decision-making
- Emergent behaviors
- Multi-actor supply chains

```python
import mesa
import numpy as np

class SupplierAgent(mesa.Agent):
    """Supplier agent in supply chain network"""

    def __init__(self, unique_id, model, capacity, lead_time, reliability):
        super().__init__(unique_id, model)
        self.capacity = capacity
        self.lead_time = lead_time
        self.reliability = reliability  # 0-1 probability of on-time delivery
        self.current_orders = []
        self.fulfilled_orders = 0
        self.revenue = 0

    def step(self):
        """Process orders each time step"""

        # Process pending orders
        orders_to_remove = []

        for order in self.current_orders:
            order['time_remaining'] -= 1

            if order['time_remaining'] <= 0:
                # Order ready
                if random.random() < self.reliability:
                    # Successfully deliver
                    order['customer'].receive_order(order)
                    self.fulfilled_orders += 1
                    self.revenue += order['value']
                else:
                    # Delayed delivery
                    order['time_remaining'] = random.randint(1, 3)

                if order['time_remaining'] <= 0:
                    orders_to_remove.append(order)

        for order in orders_to_remove:
            self.current_orders.remove(order)

    def accept_order(self, order):
        """Accept new order if capacity available"""

        if len(self.current_orders) < self.capacity:
            order['time_remaining'] = self.lead_time
            self.current_orders.append(order)
            return True
        return False


class ManufacturerAgent(mesa.Agent):
    """Manufacturer agent"""

    def __init__(self, unique_id, model, inventory_target, reorder_point):
        super().__init__(unique_id, model)
        self.inventory = inventory_target
        self.inventory_target = inventory_target
        self.reorder_point = reorder_point
        self.pending_orders = []
        self.demand_fulfilled = 0
        self.stockouts = 0

    def step(self):
        """Simulate manufacturer operations"""

        # Check inventory and place orders if needed
        if self.inventory < self.reorder_point:
            order_qty = self.inventory_target - self.inventory

            # Find best supplier
            suppliers = [agent for agent in self.model.schedule.agents
                        if isinstance(agent, SupplierAgent)]

            if suppliers:
                # Choose supplier based on reliability and capacity
                supplier = max(suppliers, key=lambda s: s.reliability)

                order = {
                    'quantity': order_qty,
                    'customer': self,
                    'value': order_qty * 100
                }

                if supplier.accept_order(order):
                    self.pending_orders.append(order)

        # Simulate customer demand
        demand = random.poisson(50)  # Daily demand

        if self.inventory >= demand:
            self.inventory -= demand
            self.demand_fulfilled += demand
        else:
            self.demand_fulfilled += self.inventory
            self.stockouts += (demand - self.inventory)
            self.inventory = 0

    def receive_order(self, order):
        """Receive order from supplier"""
        self.inventory += order['quantity']
        if order in self.pending_orders:
            self.pending_orders.remove(order)


class SupplyChainModel(mesa.Model):
    """Agent-based supply chain digital twin"""

    def __init__(self, num_suppliers, num_manufacturers):
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True

        # Create agents
        agent_id = 0

        # Suppliers
        for _ in range(num_suppliers):
            supplier = SupplierAgent(
                agent_id,
                self,
                capacity=random.randint(5, 10),
                lead_time=random.randint(3, 7),
                reliability=random.uniform(0.85, 0.98)
            )
            self.schedule.add(supplier)
            agent_id += 1

        # Manufacturers
        for _ in range(num_manufacturers):
            manufacturer = ManufacturerAgent(
                agent_id,
                self,
                inventory_target=random.randint(500, 1000),
                reorder_point=random.randint(200, 400)
            )
            self.schedule.add(manufacturer)
            agent_id += 1

        # Data collector
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Total_Inventory": lambda m: sum(
                    agent.inventory for agent in m.schedule.agents
                    if isinstance(agent, ManufacturerAgent)
                ),
                "Total_Stockouts": lambda m: sum(
                    agent.stockouts for agent in m.schedule.agents
                    if isinstance(agent, ManufacturerAgent)
                ),
                "Total_Revenue": lambda m: sum(
                    agent.revenue for agent in m.schedule.agents
                    if isinstance(agent, SupplierAgent)
                )
            }
        )

    def step(self):
        """Advance model by one step"""
        self.datacollector.collect(self)
        self.schedule.step()

# Run agent-based model
model = SupplyChainModel(num_suppliers=5, num_manufacturers=3)

for _ in range(365):  # Simulate 1 year
    model.step()

# Extract results
results = model.datacollector.get_model_vars_dataframe()

print(f"Average Inventory: {results['Total_Inventory'].mean():.0f}")
print(f"Total Stockouts: {results['Total_Stockouts'].sum():.0f}")
print(f"Total Revenue: {results['Total_Revenue'].sum():.0f}")

# Plot results
results.plot(subplots=True, figsize=(12, 8))
plt.tight_layout()
plt.show()
```

---

## Network Digital Twin

```python
import networkx as nx
import matplotlib.pyplot as plt

class SupplyChainNetworkTwin:
    """
    Digital twin of supply chain network
    """

    def __init__(self):
        self.network = nx.DiGraph()
        self.node_data = {}
        self.flow_data = {}

    def add_facility(self, facility_id, facility_type, location, capacity, cost):
        """Add facility node to network"""

        self.network.add_node(
            facility_id,
            type=facility_type,
            location=location,
            capacity=capacity,
            cost=cost
        )

        self.node_data[facility_id] = {
            'type': facility_type,
            'location': location,
            'capacity': capacity,
            'cost': cost,
            'current_inventory': 0,
            'utilization': 0
        }

    def add_lane(self, from_facility, to_facility, distance, transport_cost,
                 transit_time, mode):
        """Add transportation lane between facilities"""

        self.network.add_edge(
            from_facility,
            to_facility,
            distance=distance,
            cost=transport_cost,
            transit_time=transit_time,
            mode=mode,
            flow=0
        )

    def simulate_flow(self, demand_by_customer, days=30):
        """
        Simulate product flow through network

        demand_by_customer: dict {customer_id: daily_demand}
        """

        results = {
            'day': [],
            'total_cost': [],
            'avg_delivery_time': [],
            'fill_rate': []
        }

        for day in range(days):
            daily_cost = 0
            deliveries = []
            unmet_demand = 0

            # Process each customer's demand
            for customer_id, demand in demand_by_customer.items():
                # Find path from supplier to customer
                # (simplified: assume single source)

                source = [n for n, d in self.network.nodes(data=True)
                         if d['type'] == 'supplier'][0]

                try:
                    path = nx.shortest_path(
                        self.network,
                        source,
                        customer_id,
                        weight='cost'
                    )

                    # Calculate delivery time and cost
                    delivery_time = 0
                    transport_cost = 0

                    for i in range(len(path) - 1):
                        edge_data = self.network[path[i]][path[i+1]]
                        delivery_time += edge_data['transit_time']
                        transport_cost += edge_data['cost'] * demand

                        # Update flow
                        self.network[path[i]][path[i+1]]['flow'] += demand

                    daily_cost += transport_cost
                    deliveries.append(delivery_time)

                except nx.NetworkXNoPath:
                    unmet_demand += demand

            # Record metrics
            results['day'].append(day)
            results['total_cost'].append(daily_cost)
            results['avg_delivery_time'].append(
                np.mean(deliveries) if deliveries else 0
            )

            total_demand = sum(demand_by_customer.values())
            results['fill_rate'].append(
                (total_demand - unmet_demand) / total_demand * 100
            )

        return pd.DataFrame(results)

    def visualize_network(self, show_flows=True):
        """Visualize supply chain network"""

        pos = nx.spring_layout(self.network, k=2, iterations=50)

        plt.figure(figsize=(14, 10))

        # Color nodes by type
        node_colors = []
        for node in self.network.nodes():
            node_type = self.network.nodes[node]['type']
            if node_type == 'supplier':
                node_colors.append('lightgreen')
            elif node_type == 'dc':
                node_colors.append('lightblue')
            elif node_type == 'customer':
                node_colors.append('lightcoral')
            else:
                node_colors.append('lightgray')

        # Draw nodes
        nx.draw_networkx_nodes(
            self.network,
            pos,
            node_color=node_colors,
            node_size=1000,
            alpha=0.8
        )

        # Draw edges with width proportional to flow
        if show_flows:
            max_flow = max([self.network[u][v]['flow']
                           for u, v in self.network.edges()] or [1])

            for u, v in self.network.edges():
                flow = self.network[u][v]['flow']
                width = (flow / max_flow) * 5 if max_flow > 0 else 1

                nx.draw_networkx_edges(
                    self.network,
                    pos,
                    [(u, v)],
                    width=width,
                    alpha=0.6,
                    edge_color='gray',
                    arrows=True,
                    arrowsize=20
                )
        else:
            nx.draw_networkx_edges(
                self.network,
                pos,
                alpha=0.5,
                arrows=True
            )

        # Draw labels
        nx.draw_networkx_labels(
            self.network,
            pos,
            font_size=10,
            font_weight='bold'
        )

        plt.title("Supply Chain Network Digital Twin")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    def analyze_bottlenecks(self):
        """Identify network bottlenecks"""

        bottlenecks = []

        for node in self.network.nodes():
            node_data = self.node_data[node]

            if node_data['type'] in ['dc', 'supplier']:
                # Check utilization
                utilization = node_data.get('utilization', 0)

                if utilization > 0.85:  # 85% threshold
                    bottlenecks.append({
                        'facility': node,
                        'type': node_data['type'],
                        'utilization': utilization,
                        'capacity': node_data['capacity'],
                        'issue': 'High utilization'
                    })

        # Check for high-flow edges
        for u, v in self.network.edges():
            flow = self.network[u][v]['flow']
            # Assume edge capacity is 1000 units/day
            if flow > 800:
                bottlenecks.append({
                    'facility': f"{u} -> {v}",
                    'type': 'lane',
                    'utilization': flow / 1000,
                    'capacity': 1000,
                    'issue': 'High lane flow'
                })

        return pd.DataFrame(bottlenecks)

# Example usage
network_twin = SupplyChainNetworkTwin()

# Add facilities
network_twin.add_facility('Supplier_1', 'supplier', (0, 0), 10000, 1000000)
network_twin.add_facility('DC_East', 'dc', (5, 2), 5000, 500000)
network_twin.add_facility('DC_West', 'dc', (2, 5), 5000, 500000)
network_twin.add_facility('Customer_A', 'customer', (8, 3), None, 0)
network_twin.add_facility('Customer_B', 'customer', (3, 7), None, 0)

# Add lanes
network_twin.add_lane('Supplier_1', 'DC_East', 500, 2.5, 2, 'truck')
network_twin.add_lane('Supplier_1', 'DC_West', 400, 2.5, 2, 'truck')
network_twin.add_lane('DC_East', 'Customer_A', 150, 2.0, 1, 'truck')
network_twin.add_lane('DC_West', 'Customer_B', 200, 2.0, 1, 'truck')

# Simulate
demand = {
    'Customer_A': 100,
    'Customer_B': 150
}

results = network_twin.simulate_flow(demand, days=30)

print("Average Daily Cost:", results['total_cost'].mean())
print("Average Delivery Time:", results['avg_delivery_time'].mean())
print("Average Fill Rate:", results['fill_rate'].mean())

# Visualize
network_twin.visualize_network(show_flows=True)
```

---

## Real-Time Digital Twin with IoT Integration

```python
import time
from datetime import datetime
import threading

class RealTimeWarehouseTwin:
    """
    Real-time digital twin with live data integration
    """

    def __init__(self):
        self.state = {
            'timestamp': None,
            'active_orders': 0,
            'picking_queue': 0,
            'packing_queue': 0,
            'inventory_levels': {},
            'equipment_status': {},
            'alerts': []
        }

        self.historical_data = []
        self.is_running = False

    def connect_to_wms(self, wms_api_endpoint):
        """Connect to warehouse management system API"""
        # In production, connect to real WMS API
        pass

    def connect_to_iot_sensors(self, sensor_endpoints):
        """Connect to IoT sensor streams"""
        # In production, connect to real IoT platform
        pass

    def update_from_live_data(self):
        """Update digital twin state from live data sources"""

        while self.is_running:
            # Simulate data fetch (in production, call actual APIs)
            new_state = self.fetch_live_data()

            # Update state
            self.state = new_state
            self.state['timestamp'] = datetime.now()

            # Store historical data
            self.historical_data.append(self.state.copy())

            # Check for alerts
            self.check_alerts()

            # Sleep before next update
            time.sleep(5)  # Update every 5 seconds

    def fetch_live_data(self):
        """Fetch live data from various sources"""

        # Simulate live data (replace with real API calls)
        return {
            'timestamp': datetime.now(),
            'active_orders': random.randint(50, 150),
            'picking_queue': random.randint(10, 50),
            'packing_queue': random.randint(5, 30),
            'inventory_levels': {
                f'SKU_{i}': random.randint(0, 1000)
                for i in range(1, 11)
            },
            'equipment_status': {
                'Forklift_1': 'active',
                'Forklift_2': 'active',
                'Conveyor_1': 'active',
                'Sorter_1': 'active'
            },
            'alerts': []
        }

    def check_alerts(self):
        """Check for anomalies and generate alerts"""

        alerts = []

        # High queue alert
        if self.state['picking_queue'] > 40:
            alerts.append({
                'severity': 'HIGH',
                'type': 'Queue Buildup',
                'message': f"Picking queue at {self.state['picking_queue']} orders",
                'timestamp': datetime.now()
            })

        # Low inventory alert
        for sku, level in self.state['inventory_levels'].items():
            if level < 100:
                alerts.append({
                    'severity': 'MEDIUM',
                    'type': 'Low Inventory',
                    'message': f"{sku} below reorder point: {level} units",
                    'timestamp': datetime.now()
                })

        self.state['alerts'] = alerts

    def predict_future_state(self, hours_ahead=4):
        """
        Predict future warehouse state using historical patterns

        Uses simple time series forecasting
        """

        if len(self.historical_data) < 50:
            return None  # Need more historical data

        # Extract time series
        df = pd.DataFrame(self.historical_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp')

        # Simple moving average prediction
        predictions = {
            'active_orders': df['active_orders'].rolling(20).mean().iloc[-1],
            'picking_queue': df['picking_queue'].rolling(20).mean().iloc[-1],
            'packing_queue': df['packing_queue'].rolling(20).mean().iloc[-1]
        }

        return predictions

    def start(self):
        """Start real-time monitoring"""
        self.is_running = True

        # Start update thread
        update_thread = threading.Thread(target=self.update_from_live_data)
        update_thread.daemon = True
        update_thread.start()

    def stop(self):
        """Stop real-time monitoring"""
        self.is_running = False

    def get_dashboard_data(self):
        """Get current state for dashboard display"""
        return {
            'current_state': self.state,
            'predictions': self.predict_future_state(),
            'alerts': self.state['alerts']
        }

# Example usage
twin = RealTimeWarehouseTwin()
twin.start()

# Run for some time
time.sleep(60)

# Get dashboard data
dashboard_data = twin.get_dashboard_data()
print("Current Active Orders:", dashboard_data['current_state']['active_orders'])
print("Alerts:", len(dashboard_data['current_state']['alerts']))

twin.stop()
```

---

## Tools & Technologies

### Simulation Software

**Commercial:**
- **AnyLogic**: Multi-method simulation (DES, ABM, SD)
- **Arena (Rockwell)**: Discrete event simulation
- **FlexSim**: 3D simulation for manufacturing and logistics
- **Simul8**: Process simulation
- **ExtendSim**: Simulation for logistics and supply chain
- **Plant Simulation (Siemens)**: Manufacturing simulation
- **SIMIO**: Object-based simulation

**Open Source:**
- **SimPy (Python)**: Discrete event simulation
- **Mesa (Python)**: Agent-based modeling
- **Salabim (Python)**: Discrete event simulation
- **des.js (JavaScript)**: Browser-based DES
- **AnyLogic PLE**: Free personal learning edition

### Python Libraries

**Simulation:**
- `simpy`: Discrete event simulation
- `mesa`: Agent-based modeling
- `salabim`: Advanced DES with animation
- `ciw`: Queueing network simulation

**Network Modeling:**
- `networkx`: Graph and network analysis
- `pyvis`: Interactive network visualization
- `graph-tool`: Large-scale network analysis

**Visualization:**
- `matplotlib`: Basic plotting
- `plotly`: Interactive 3D visualization
- `mayavi`: Advanced 3D visualization
- `pygame`: Real-time animation

**Data Integration:**
- `pandas`: Data manipulation
- `numpy`: Numerical operations
- `sqlalchemy`: Database connections
- `requests`: API integration
- `mqtt`: IoT data streaming

### Digital Twin Platforms

**Enterprise:**
- **Azure Digital Twins (Microsoft)**: Cloud-based digital twin platform
- **AWS IoT TwinMaker**: Build digital twins with AWS
- **GE Digital Twin**: Industrial IoT platform
- **Siemens MindSphere**: IoT operating system
- **PTC ThingWorx**: IoT and AR platform
- **IBM Maximo**: Asset management and digital twin

**Supply Chain Specific:**
- **Blue Yonder Luminate**: Digital supply chain platform
- **o9 Solutions**: Digital brain platform with simulation
- **Kinaxis RapidResponse**: Concurrent planning with scenarios
- **LLamasoft (Coupa)**: Supply chain design and simulation

---

## Common Challenges & Solutions

### Challenge: Data Quality and Availability

**Problem:**
- Insufficient historical data
- Missing parameters (processing times, failure rates)
- Inconsistent data formats

**Solutions:**
- Use time studies to collect missing parameters
- Implement data collection systems (IoT sensors, automated logging)
- Start with simplified model, add detail iteratively
- Use industry benchmarks where data unavailable
- Validate model with subject matter experts

### Challenge: Model Complexity vs. Usability

**Problem:**
- Too detailed = slow, hard to maintain
- Too simple = inaccurate, limited value

**Solutions:**
- Start simple, add complexity only where needed
- Use appropriate level of detail for decisions being made
- Modular design (swap detailed/simplified components)
- Separate strategic (high-level) and operational (detailed) models
- Clear documentation of assumptions and limitations

### Challenge: Real-Time Integration

**Problem:**
- Legacy systems without APIs
- Data latency issues
- Integration complexity

**Solutions:**
- Use middleware or integration platforms
- Implement data buffering and caching
- Start with batch updates, evolve to real-time
- Use event-driven architecture
- Consider cloud-based integration services

### Challenge: Stakeholder Buy-In

**Problem:**
- Resistance to simulation results
- "Black box" perception
- Lack of trust in model

**Solutions:**
- Involve stakeholders in model development
- Validate model against known scenarios
- Transparent documentation of logic and assumptions
- Show sensitivity analysis to build confidence
- Start with pilot/proof-of-concept
- Visualize results effectively (3D animation helps)

### Challenge: Keeping Model Updated

**Problem:**
- Operations change, model becomes obsolete
- Maintenance overhead
- No clear owner

**Solutions:**
- Assign clear model ownership and governance
- Automate data updates where possible
- Regular validation against actual performance
- Version control for model changes
- Schedule periodic reviews and updates
- Design for maintainability from start

---

## Output Format

### Digital Twin Report Template

**Executive Summary:**
- Purpose of digital twin
- Key findings from simulation
- Recommended decisions
- Expected impact and ROI

**Model Overview:**
- Scope and boundaries
- Components modeled
- Level of detail
- Key assumptions

**Scenario Analysis Results:**

| Scenario | Throughput | Avg Cycle Time | Utilization | Cost | Recommendation |
|----------|-----------|----------------|-------------|------|----------------|
| Baseline | 500/day | 4.2 hrs | 78% | $125K/mo | Current state |
| Add Resources | 650/day | 3.1 hrs | 82% | $145K/mo | ⭐ Recommended |
| Optimize Layout | 580/day | 3.8 hrs | 85% | $130K/mo | Consider |
| Peak Demand | 720/day | 3.5 hrs | 91% | $155K/mo | Growth scenario |

**Sensitivity Analysis:**
- Impact of demand variability (+/-20%)
- Resource availability (equipment downtime)
- Process time variations
- Confidence intervals

**Bottleneck Analysis:**
- Identified constraints
- Impact on overall performance
- Mitigation options

**Implementation Plan:**
- Recommended changes
- Phasing and timeline
- Resource requirements
- Risk mitigation

**Model Validation:**
- Validation approach
- Comparison to actual performance
- Statistical tests
- Limitations and caveats

---

## Questions to Ask

If you need more context:
1. What system do you want to model? (warehouse, network, production, transportation)
2. What decisions will the digital twin support?
3. What level of detail is needed? (strategic vs. operational)
4. What data is available? (historical performance, parameters, real-time feeds)
5. What scenarios do you want to test?
6. Do you need real-time integration or batch simulation?
7. What tools/platforms are you using or prefer?
8. What's the expected timeline and budget for this initiative?

---

## Related Skills

- **supply-chain-automation**: For automated control systems
- **optimization-modeling**: For optimization within digital twin
- **prescriptive-analytics**: For decision recommendations
- **ml-supply-chain**: For predictive components
- **supply-chain-analytics**: For KPI tracking and dashboards
- **network-design**: For network modeling and optimization
- **warehouse-design**: For facility layout simulation
- **production-scheduling**: For manufacturing simulation
- **scenario-planning**: For strategic scenario analysis
