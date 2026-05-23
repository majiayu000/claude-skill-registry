---
name: operations
description: Operations excellence expertise for supply chain optimization, process improvement (Lean, Six Sigma), capacity planning, vendor management, quality assurance, and operational efficiency. Use when optimizing processes, managing supply chains, or improving operational performance.
---

# Operations Expert

Comprehensive operations frameworks for process improvement, supply chain management, and operational excellence.

## Operational Excellence Frameworks

### Lean Manufacturing Principles

```
THE 5 PRINCIPLES OF LEAN:
1. Value - Define from customer perspective
2. Value Stream - Map all steps, eliminate waste
3. Flow - Make value-creating steps flow smoothly
4. Pull - Let customer demand drive production
5. Perfection - Continuously improve toward perfection
```

### 8 Wastes (DOWNTIME)

| Waste                   | Definition                        | Examples                           | Countermeasures                   |
| ----------------------- | --------------------------------- | ---------------------------------- | --------------------------------- |
| **D**efects             | Work requiring rework/scrap       | Quality issues, errors             | Poka-yoke, quality at source      |
| **O**verproduction      | Making more than needed           | Excess inventory, WIP              | Pull systems, kanban              |
| **W**aiting             | Idle time between processes       | Queue time, approvals              | Flow optimization, cross-training |
| **N**on-utilized talent | Underusing employee skills        | Manual data entry, routine tasks   | Empowerment, automation           |
| **T**ransportation      | Unnecessary movement of materials | Multiple handling, poor layout     | Facility layout optimization      |
| **I**nventory           | Excess stock/materials            | Safety stock, WIP                  | JIT, demand planning              |
| **M**otion              | Unnecessary worker movement       | Poor workstation design            | 5S, ergonomics                    |
| **E**xtra processing    | More work than required           | Over-engineering, redundant checks | Value stream mapping              |

### Six Sigma DMAIC

```
DEFINE
- Problem statement
- Project charter
- Voice of customer (VOC)
- SIPOC diagram
- CTQ (Critical to Quality) tree

MEASURE
- Data collection plan
- Process capability (Cp, Cpk)
- Measurement system analysis
- Baseline metrics

ANALYZE
- Root cause analysis (5 Whys, Fishbone)
- Statistical analysis
- Process mapping
- Hypothesis testing

IMPROVE
- Solution generation
- Pilot testing
- Implementation plan
- Risk assessment (FMEA)

CONTROL
- Control plan
- Statistical process control (SPC)
- Standard operating procedures
- Training and handoff
```

### Six Sigma Metrics

| Sigma Level | DPMO    | Yield    |
| ----------- | ------- | -------- |
| 1           | 691,462 | 30.9%    |
| 2           | 308,538 | 69.1%    |
| 3           | 66,807  | 93.3%    |
| 4           | 6,210   | 99.4%    |
| 5           | 233     | 99.98%   |
| 6           | 3.4     | 99.9997% |

## Supply Chain Management

### Supply Chain Strategy

| Strategy         | When to Use                               | Key Characteristics                           |
| ---------------- | ----------------------------------------- | --------------------------------------------- |
| **Efficient**    | Stable demand, commodity products         | Low cost, high utilization, minimal inventory |
| **Responsive**   | Unpredictable demand, innovative products | Speed, flexibility, buffer inventory          |
| **Risk-Hedging** | Supply uncertainty                        | Multiple suppliers, pooled inventory          |
| **Agile**        | Demand and supply uncertainty             | All above combined, modular design            |

### SCOR Model (Supply Chain Operations Reference)

```
PLAN
- Demand planning
- Supply planning
- S&OP process
- Inventory planning

SOURCE
- Supplier selection
- Contract negotiation
- Procurement
- Supplier performance

MAKE
- Production scheduling
- Manufacturing execution
- Quality management
- Capacity management

DELIVER
- Order management
- Warehousing
- Transportation
- Last-mile delivery

RETURN
- Reverse logistics
- Returns processing
- Warranty management
- Disposal/recycling

ENABLE
- Business rules
- Performance management
- Data management
- Risk management
```

### Supply Chain KPIs

| Category             | Metric                    | Formula                                                 | Target            |
| -------------------- | ------------------------- | ------------------------------------------------------- | ----------------- |
| **Reliability**      | Perfect Order             | (Complete, On-time, Damage-free, Accurate docs) / Total | 95%+              |
|                      | OTIF                      | Orders On-Time In-Full / Total Orders                   | 98%+              |
| **Responsiveness**   | Order Cycle Time          | Order receipt to delivery                               | Industry specific |
|                      | Lead Time                 | Request to fulfillment                                  | Minimize          |
| **Agility**          | Upside Flexibility        | % increase possible in 30 days                          | 20%+              |
|                      | Supply Chain Adaptability | Time to adjust to market change                         | Minimize          |
| **Cost**             | Supply Chain Cost         | Total SC cost / Revenue                                 | 5-10%             |
|                      | COGS                      | Cost of Goods Sold / Revenue                            | Industry specific |
| **Asset Management** | Cash-to-Cash              | DIO + DSO - DPO                                         | Industry specific |
|                      | Inventory Turns           | COGS / Average Inventory                                | Higher is better  |

## Demand Planning & Forecasting

### Forecasting Methods

| Method                    | Use Case                       | Accuracy    |
| ------------------------- | ------------------------------ | ----------- |
| **Moving Average**        | Stable demand                  | Low-Medium  |
| **Exponential Smoothing** | Trend data                     | Medium      |
| **Regression**            | Causal relationships           | Medium-High |
| **ARIMA**                 | Complex patterns               | High        |
| **Machine Learning**      | Large datasets, many variables | High        |
| **Collaborative**         | Retail, promotions             | Medium-High |

### S&OP (Sales & Operations Planning)

```
MONTHLY S&OP CYCLE:

Week 1: Data Gathering
- Update sales forecast
- Review actual vs. plan
- Identify issues

Week 2: Demand Planning
- Demand review meeting
- Consensus forecast
- New product planning

Week 3: Supply Planning
- Capacity analysis
- Inventory planning
- Resource requirements

Week 4: Pre-S&OP
- Gap analysis
- Scenario planning
- Financial reconciliation

Week 5: Executive S&OP
- Final decisions
- Resource allocation
- Performance review
```

### Inventory Management

| Model             | Formula       | Use Case              |
| ----------------- | ------------- | --------------------- |
| **EOQ**           | √(2DS/H)      | Constant demand       |
| **Safety Stock**  | z × σ × √LT   | Buffer uncertainty    |
| **Reorder Point** | (D × LT) + SS | Trigger replenishment |

```
ABC CLASSIFICATION:
A Items: 20% of SKUs, 80% of value → Tight control
B Items: 30% of SKUs, 15% of value → Moderate control
C Items: 50% of SKUs, 5% of value → Minimal control

XYZ CLASSIFICATION (Variability):
X: Low variability (CV < 0.5) → Predictable
Y: Medium variability (0.5 < CV < 1.0) → Some variation
Z: High variability (CV > 1.0) → Sporadic
```

## Quality Management

### Total Quality Management (TQM)

```
TQM PRINCIPLES:
1. Customer focus
2. Total employee involvement
3. Process-centered
4. Integrated system
5. Strategic and systematic approach
6. Continuous improvement
7. Fact-based decision making
8. Communications
```

### Quality Tools

| Tool                 | Purpose                   | When to Use             |
| -------------------- | ------------------------- | ----------------------- |
| **Pareto Chart**     | Identify vital few        | Prioritizing problems   |
| **Fishbone Diagram** | Root cause analysis       | Problem investigation   |
| **Control Charts**   | Monitor process stability | Ongoing monitoring      |
| **Histogram**        | Show distribution         | Understanding variation |
| **Scatter Diagram**  | Show correlation          | Relationship analysis   |
| **Check Sheet**      | Data collection           | Systematic recording    |
| **Flowchart**        | Visualize process         | Process understanding   |

### Statistical Process Control (SPC)

```
CONTROL CHART RULES (Western Electric):
Rule 1: One point beyond 3σ
Rule 2: 2 of 3 points beyond 2σ (same side)
Rule 3: 4 of 5 points beyond 1σ (same side)
Rule 4: 8 points in a row on one side of center
Rule 5: 6 points trending up or down
Rule 6: 14 points alternating up and down
Rule 7: 15 points within 1σ (reduced variation)
Rule 8: 8 points beyond 1σ (both sides)
```

## Capacity Planning

### Capacity Analysis

```
CAPACITY METRICS:
Design Capacity: Maximum theoretical output
Effective Capacity: Expected output given constraints
Actual Output: Real production achieved

Utilization = Actual Output / Design Capacity
Efficiency = Actual Output / Effective Capacity

CAPACITY STRATEGIES:
Lead: Build capacity ahead of demand
Lag: Build capacity after demand materializes
Match: Incrementally match demand
```

### Production Planning

| Planning Level  | Horizon     | Decisions                   |
| --------------- | ----------- | --------------------------- |
| **Strategic**   | 1-5 years   | Facilities, major equipment |
| **Tactical**    | 3-18 months | Workforce, inventory levels |
| **Operational** | Days-weeks  | Scheduling, sequencing      |

## Vendor Management

### Supplier Evaluation Criteria

```
QCDDM FRAMEWORK:
Q - Quality (PPM, certification, capability)
C - Cost (Price, TCO, cost reduction)
D - Delivery (OTIF, lead time, flexibility)
D - Development (Innovation, collaboration)
M - Management (Financial stability, risk)

SCORECARD WEIGHTS (example):
Quality: 30%
Delivery: 25%
Cost: 25%
Service: 10%
Innovation: 10%
```

### Supplier Relationship Tiers

| Tier          | Relationship  | Characteristics                           |
| ------------- | ------------- | ----------------------------------------- |
| **Strategic** | Partnership   | Joint development, long-term, shared risk |
| **Preferred** | Collaboration | Volume commitment, improvement programs   |
| **Approved**  | Transactional | Competitive bidding, standard terms       |
| **Spot**      | One-time      | Emergency purchases, minimal vetting      |

### Contract Management

```
KEY CONTRACT ELEMENTS:
- Scope of work / specifications
- Pricing structure (fixed, cost-plus, tiered)
- Volume commitments
- Quality requirements and remedies
- Delivery terms (Incoterms)
- IP ownership
- Liability and indemnification
- Force majeure
- Termination rights
- Performance metrics / SLAs
- Dispute resolution
```

## Process Improvement Methodology

### Value Stream Mapping

```
CURRENT STATE MAP:
1. Identify product family
2. Map customer requirements
3. Walk the process
4. Collect data (cycle time, changeover, uptime)
5. Calculate lead time vs. process time
6. Identify waste

FUTURE STATE MAP:
1. Calculate takt time
2. Implement continuous flow where possible
3. Use pull systems
4. Level production
5. Identify kaizen bursts
6. Calculate new lead time
```

### Kaizen Events

| Phase           | Duration   | Activities                                |
| --------------- | ---------- | ----------------------------------------- |
| **Preparation** | 2-4 weeks  | Scope, team, data gathering               |
| **Event**       | 3-5 days   | Analysis, solution design, implementation |
| **Follow-up**   | 30-60 days | Sustain, measure, adjust                  |

### 5S Methodology

| Step | Japanese | English      | Actions                  |
| ---- | -------- | ------------ | ------------------------ |
| 1    | Seiri    | Sort         | Remove unnecessary items |
| 2    | Seiton   | Set in Order | Organize remaining items |
| 3    | Seiso    | Shine        | Clean work area          |
| 4    | Seiketsu | Standardize  | Create standards         |
| 5    | Shitsuke | Sustain      | Maintain discipline      |

## Operational Metrics Dashboard

### Key Operating Metrics

| Category      | Metric                        | Frequency |
| ------------- | ----------------------------- | --------- |
| **Safety**    | TRIR, Lost Time               | Daily     |
| **Quality**   | First Pass Yield, Defect Rate | Daily     |
| **Delivery**  | OTIF, Lead Time               | Daily     |
| **Cost**      | Unit Cost, Productivity       | Weekly    |
| **Inventory** | Turns, DOS                    | Weekly    |
| **Equipment** | OEE, Downtime                 | Daily     |

### OEE (Overall Equipment Effectiveness)

```
OEE = Availability × Performance × Quality

Availability = Run Time / Planned Production Time
Performance = (Total Count × Ideal Cycle Time) / Run Time
Quality = Good Count / Total Count

WORLD-CLASS OEE: 85%+
- Availability: 90%
- Performance: 95%
- Quality: 99%
```

## See Also

- [Fortune 50 Business Strategy](../fortune50-business-strategy/SKILL.md)
- [Fortune 50 Finance](../fortune50-finance/SKILL.md)
- [Fortune 50 Risk Management](../fortune50-risk-management/SKILL.md)
