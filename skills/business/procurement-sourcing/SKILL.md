---
name: procurement-sourcing
description: "SAP Ariba alternative - PR, PO, RFQ, vendor management, three-way match"
---

# Procurement & Sourcing (Ariba Alternative)
Self-hosted procurement system saving $24,000/year.

## What This Does
- Purchase requisitions
- RFQ/RFP management
- Bid evaluation
- PO creation
- Three-way matching
- Contract management

## Quick Example
```python
procurement.send_rfq({
    'pr_id': 'PR-2025-001',
    'vendors': vendor_list,
    'deadline': '2025-11-15'
})
```

## Getting Started
"Create purchase requisition"
"Send RFQ to 3 vendors"
"Three-way match PO-001"
