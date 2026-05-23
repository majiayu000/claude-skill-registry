---
name: Inventory Manager
slug: inventory-manager
description: Track inventory levels, manage stock, forecast demand, and optimize replenishment
category: business
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "inventory management"
  - "stock levels"
  - "inventory tracking"
  - "reorder point"
  - "stock replenishment"
  - "demand forecast"
tags:
  - inventory
  - operations
  - supply-chain
  - forecasting
  - business-operations
---

# Inventory Manager

Expert inventory management system that helps you track stock levels, forecast demand, optimize reorder points, and prevent stockouts while minimizing carrying costs. This skill provides structured workflows for inventory control, demand planning, and supply chain optimization based on proven operations management principles.

Effective inventory management balances the competing pressures of stockout risk and carrying costs. This skill helps you maintain optimal inventory levels, improve cash flow, reduce waste, and ensure product availability whether you're managing physical products, digital goods, or service capacity.

Built on best practices from supply chain leaders and operations research, this skill combines demand forecasting, safety stock calculations, and just-in-time principles to optimize your inventory investment.

## Core Workflows

### Workflow 1: Inventory Setup & Classification
**Establish your inventory system and categorize items strategically**

1. **Inventory Master Data**
   - **Item Basics**: SKU, description, category, supplier
   - **Costs**: Unit cost, carrying cost (% of value per year), ordering cost
   - **Physical**: Dimensions, weight, storage requirements
   - **Lead Times**: Supplier lead time, production lead time
   - **Constraints**: Minimum order quantity (MOQ), shelf life, storage capacity

2. **ABC Classification**
   - **A Items (20% of items, 80% of value)**
     - Tight control, daily monitoring
     - Accurate forecasting critical
     - Higher service levels (95-99%)
   - **B Items (30% of items, 15% of value)**
     - Moderate control, weekly monitoring
     - Standard forecasting methods
     - Medium service levels (90-95%)
   - **C Items (50% of items, 5% of value)**
     - Loose control, monthly monitoring
     - Simple replenishment rules
     - Lower service levels (85-90%)

3. **Tracking Methods**
   - Perpetual inventory (real-time updates with each transaction)
   - Periodic inventory (physical counts at intervals)
   - Cycle counting (continuous partial counts)
   - Barcode/RFID scanning for accuracy

### Workflow 2: Demand Forecasting
**Predict future demand to inform inventory decisions**

1. **Historical Analysis**
   - Gather historical sales data (minimum 12-24 months)
   - Identify patterns:
     - **Trend**: Overall increase or decrease over time
     - **Seasonality**: Repeating patterns (holiday spikes, quarterly cycles)
     - **Cyclical**: Longer-term economic cycles
     - **Random**: Unpredictable variation

2. **Forecasting Methods**
   - **Simple**: Moving average (stable demand), last period (very stable)
   - **Intermediate**: Weighted moving average, exponential smoothing
   - **Advanced**: Seasonal decomposition, regression analysis, machine learning

3. **Forecast Accuracy**
   - Calculate Mean Absolute Percentage Error (MAPE)
   - Compare forecast vs. actual monthly
   - Refine methods based on accuracy
   - Segment forecasting by product category/SKU

4. **Adjustments**
   - Factor in promotions, marketing campaigns
   - Account for market trends, competitive activity
   - Adjust for new product launches, discontinuations
   - Include known events (trade shows, holidays)

### Workflow 3: Reorder Point & Safety Stock
**Calculate optimal reorder triggers and buffer inventory**

1. **Reorder Point Calculation**
   ```
   Reorder Point = (Average Daily Demand × Lead Time Days) + Safety Stock
   ```
   - Example: Demand = 50 units/day, Lead Time = 10 days, Safety Stock = 100
   - Reorder Point = (50 × 10) + 100 = 600 units

2. **Safety Stock Calculation**
   ```
   Safety Stock = Z-Score × (Demand Std Dev) × √(Lead Time)
   ```
   - Z-Score based on desired service level:
     - 90% service level: Z = 1.28
     - 95% service level: Z = 1.65
     - 99% service level: Z = 2.33
   - Example: Std Dev = 15, Lead Time = 10 days, 95% service
   - Safety Stock = 1.65 × 15 × √10 = 78 units

3. **Economic Order Quantity (EOQ)**
   ```
   EOQ = √((2 × Annual Demand × Ordering Cost) / Carrying Cost per Unit)
   ```
   - Balances ordering costs vs. holding costs
   - Example: Demand = 10,000/year, Order Cost = $100, Holding Cost = $5/unit/year
   - EOQ = √((2 × 10,000 × 100) / 5) = 632 units per order

4. **Dynamic Adjustments**
   - Review reorder points quarterly
   - Adjust for seasonality (higher safety stock in peak seasons)
   - Consider supplier reliability (lower reliability = higher safety stock)
   - Balance service level vs. inventory investment

### Workflow 4: Stock Monitoring & Replenishment
**Track inventory levels and trigger replenishment actions**

1. **Daily Monitoring**
   - Check current stock levels vs. reorder points
   - Identify items at or below reorder point
   - Flag stockouts and backorders
   - Review slow-moving/dead stock

2. **Replenishment Triggers**
   - **Reorder Point System**: Order when stock hits reorder point
   - **Periodic Review**: Check and order on fixed schedule (weekly, monthly)
   - **Min-Max System**: Order up to max when below min
   - **Just-in-Time**: Order based on actual demand signals

3. **Purchase Order Generation**
   - Calculate order quantity (EOQ or adjusted for MOQ/promotions)
   - Select supplier based on lead time, cost, reliability
   - Generate PO with expected delivery date
   - Track open POs and follow up on delays

4. **Receiving & Updates**
   - Inspect incoming shipments for quality/quantity
   - Update inventory system immediately
   - Reconcile PO vs. actual received
   - Put away stock and update location data

### Workflow 5: Inventory Optimization
**Reduce costs, improve turns, and eliminate waste**

1. **Inventory Turns Analysis**
   ```
   Inventory Turnover = Cost of Goods Sold / Average Inventory Value
   ```
   - Target turns vary by industry (retail: 8-12, manufacturing: 4-8)
   - Calculate by SKU and category
   - Identify slow-moving items (low turns)

2. **Obsolescence Management**
   - Identify dead stock (no sales in 90+ days)
   - Aging analysis: 30/60/90+ days old
   - Disposition strategies:
     - Discounts/promotions to clear
     - Return to supplier if possible
     - Donate or dispose (write off)

3. **Carrying Cost Reduction**
   - Negotiate consignment or vendor-managed inventory
   - Reduce safety stock for reliable suppliers
   - Cross-dock fast-moving items
   - Optimize warehouse space utilization

4. **Stockout Prevention**
   - Analyze root causes of stockouts
   - Improve forecast accuracy
   - Reduce supplier lead time variability
   - Implement backup suppliers for critical items

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Check stock level | "Show inventory for [SKU]" |
| Items to reorder | "Show items at reorder point" |
| Calculate safety stock | "Calculate safety stock for [SKU]" |
| ABC classification | "Classify inventory by ABC" |
| Stockout report | "Show stockouts last 30 days" |
| Slow-moving items | "Find dead stock" |
| Inventory valuation | "Calculate total inventory value" |
| Forecast demand | "Forecast demand for [SKU]" |
| Generate PO | "Create purchase order for [SKU]" |
| Inventory turns | "Show inventory turnover by category" |

## Best Practices

### Data Accuracy
- Conduct regular cycle counts (daily for A items, weekly for B, monthly for C)
- Investigate and reconcile discrepancies immediately
- Use barcode/RFID scanning to eliminate manual errors
- Lock down inventory access to prevent unauthorized removals
- Train staff on proper transaction recording

### Forecasting Discipline
- Review and update forecasts monthly
- Track forecast accuracy and refine methods
- Collaborate with sales on upcoming promotions
- Account for lead time in forecast horizon
- Use statistical methods, not gut feel

### Safety Stock Calibration
- Set service levels by item importance (A items higher)
- Review safety stock quarterly or after major demand changes
- Don't over-invest in safety stock for slow movers
- Consider supplier reliability in calculations
- Balance stockout cost vs. carrying cost

### Supplier Management
- Track supplier on-time delivery rates
- Maintain relationships with backup suppliers
- Negotiate favorable lead times and MOQs
- Communicate forecast visibility to key suppliers
- Develop vendor scorecard (quality, delivery, cost)

### Technology & Automation
- Implement inventory management software
- Automate reorder point alerts
- Integrate with POS/ERP systems for real-time updates
- Use demand forecasting tools
- Generate automated reports and dashboards

## Key Metrics to Track

**Inventory Health:**
- Inventory turnover ratio (target: industry-dependent)
- Days inventory outstanding (DIO) = 365 / turnover
- Stock-to-sales ratio
- Dead stock value and percentage
- Inventory accuracy rate (target: 95%+)

**Service Level:**
- Fill rate (orders fulfilled completely)
- Stockout frequency
- Backorder rate
- Customer order cycle time

**Cost Metrics:**
- Total inventory value
- Carrying cost (% of inventory value)
- Stockout cost (lost sales + customer dissatisfaction)
- Shrinkage/waste rate
- Ordering cost per order

**Forecast Performance:**
- Forecast accuracy (MAPE target: <20%)
- Forecast bias (over-forecasting vs. under-forecasting)

## Common Pitfalls to Avoid

- **Over-ordering**: Tying up cash in excess inventory
- **Under-ordering**: Frequent stockouts and lost sales
- **Ignoring ABC**: Treating all items equally (wasteful)
- **Poor data hygiene**: Inaccurate counts lead to bad decisions
- **Static reorder points**: Not adjusting for seasonality or changes
- **Lack of visibility**: Not knowing what you have or where it is
- **Siloed systems**: Inventory data not integrated with sales/procurement
- **Emotional ordering**: Ordering based on fear of stockouts, not data

## Integration Points

- **Point of Sale (POS)**: Real-time sales deduction from inventory
- **E-commerce**: Sync online and physical store inventory
- **ERP/Accounting**: COGS, inventory valuation, financial reporting
- **Warehouse Management (WMS)**: Location tracking, pick/pack/ship
- **Supplier EDI**: Automated purchase orders and ASN (advance ship notice)
- **Demand Planning**: Import forecasts to inform replenishment
