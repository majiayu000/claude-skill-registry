---
name: SapEcc
description: |
  SAP ECC expert for automotive manufacturing operations. Covers Materials Management (MM), Production Planning (PP),
  Sales & Distribution (SD), Quality Management (QM), Plant Maintenance (PM), and Finance/Controlling (FI/CO).

  USE WHEN user says 'SAP', 'ECC', 'transaction code', 't-code', 'MRP', 'purchase order', 'production order',
  'goods receipt', 'goods issue', 'material master', 'BOM', 'routing', 'work center', or needs help with SAP processes.

  Integrates with AutomotiveManufacturing and SupplyChain skills.
---

# SAP ECC Expert - Automotive Manufacturing

## When to Activate This Skill

- "How do I [action] in SAP?"
- "What t-code for [function]?"
- "Create purchase order for [material]"
- "Check MRP results"
- "Production order status"
- "Goods receipt process"
- "Material master setup"
- "SAP integration issue"

---

## Core Modules Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        SAP ECC LANDSCAPE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    │
│   │   MM    │    │   PP    │    │   SD    │    │   QM    │    │
│   │Materials│───▶│Production│───▶│  Sales  │    │ Quality │    │
│   │ Mgmt    │    │Planning │    │  Dist   │    │  Mgmt   │    │
│   └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘    │
│        │              │              │              │          │
│        └──────────────┼──────────────┼──────────────┘          │
│                       │              │                          │
│   ┌─────────┐    ┌────▼────┐    ┌────▼────┐                    │
│   │   PM    │    │  FI/CO  │    │   WM    │                    │
│   │  Plant  │    │Finance/ │    │Warehouse│                    │
│   │  Maint  │    │Control  │    │  Mgmt   │                    │
│   └─────────┘    └─────────┘    └─────────┘                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Materials Management (MM)

### Key Processes

| Process | T-Codes | Description |
|---------|---------|-------------|
| Purchase Requisition | ME51N, ME52N, ME53N | Create, change, display PR |
| Purchase Order | ME21N, ME22N, ME23N | Create, change, display PO |
| Goods Receipt | MIGO, MB01 | Receive goods against PO |
| Invoice Verification | MIRO | Enter vendor invoice |
| Material Master | MM01, MM02, MM03 | Create, change, display material |
| Vendor Master | XK01, XK02, XK03 | Create, change, display vendor |
| Stock Overview | MMBE, MB52 | View stock levels |
| MRP | MD01, MD02, MD04 | Run MRP, display results |

### Purchase Order Process Flow

```
Purchase Requisition (ME51N)
         │
         ▼
    ┌─────────┐
    │ Approval │ (if required)
    └────┬────┘
         │
         ▼
Purchase Order (ME21N)
         │
         ▼
    ┌─────────┐
    │  Vendor  │ Confirmation
    └────┬────┘
         │
         ▼
Goods Receipt (MIGO)
         │
         ▼
Invoice Verification (MIRO)
         │
         ▼
Payment (FI)
```

### Material Master Views

| View | Purpose | Key Fields |
|------|---------|------------|
| Basic Data 1 | General info | Description, UoM, material group |
| Basic Data 2 | Extended info | Dimensions, weights |
| Purchasing | Procurement | Purchasing group, order unit |
| MRP 1 | Planning | MRP type, reorder point |
| MRP 2 | Lot sizing | Lot size, safety stock |
| MRP 3 | Forecast | Strategy group |
| MRP 4 | Scheduling | In-house time, GR processing |
| Accounting 1 | Valuation | Price control, standard price |
| Accounting 2 | Cost info | Profit center |
| Costing 1 | Cost estimate | Cost elements |
| Costing 2 | Extended | Costing data |
| Plant Data/Stor 1 | Storage | Storage location, bin |
| Plant Data/Stor 2 | Weights | Unit weight |
| Quality Mgmt | QM settings | Inspection type, certificate |
| Sales: General | SD info | Sales org, distribution |
| Sales: Plant | Delivery | Loading group, availability |

### Stock Types

| Stock Type | Description | Movement |
|------------|-------------|----------|
| Unrestricted | Available for use | 101, 561 |
| Quality Inspection | Pending QC | 103 |
| Blocked | Not available | 105, 344 |
| In Transit | Between plants | 351 |
| Consignment | Vendor-owned | 501 |

---

## Production Planning (PP)

### Key Processes

| Process | T-Codes | Description |
|---------|---------|-------------|
| BOM | CS01, CS02, CS03 | Create, change, display BOM |
| Routing | CA01, CA02, CA03 | Create, change, display routing |
| Work Center | CR01, CR02, CR03 | Create, change, display work center |
| Production Order | CO01, CO02, CO03 | Create, change, display prod order |
| Order Confirmation | CO11N, CO15 | Confirm operations |
| Goods Issue | MIGO, MB1A | Issue components to order |
| Goods Receipt | MIGO, MB31 | Receive finished goods |
| Capacity Planning | CM01, CM21 | Capacity evaluation |

### Production Order Lifecycle

```
Planned Order (from MRP)
         │
         ▼
Production Order Created (CO01)
    Status: CRTD (Created)
         │
         ▼
Order Released (CO02)
    Status: REL (Released)
         │
         ▼
Components Issued (MIGO - 261)
    Status: REL + GMPS (Goods Mvmt Posted)
         │
         ▼
Operations Confirmed (CO11N)
    Status: REL + CNF (Confirmed)
         │
         ▼
Goods Receipt (MIGO - 101)
    Status: DLV (Delivered)
         │
         ▼
Order Settlement (CO88)
    Status: TECO (Technically Complete)
         │
         ▼
Order Closed
    Status: CLSD (Closed)
```

### MRP Types

| MRP Type | Description | Use Case |
|----------|-------------|----------|
| PD | MRP | Standard planning |
| VB | Reorder Point | Simple replenishment |
| VM | Manual Reorder | Exception items |
| ND | No Planning | Non-stock items |
| VV | Forecast-based | Seasonal demand |

### Lot Sizing Procedures

| Procedure | Description |
|-----------|-------------|
| EX | Exact lot size |
| FX | Fixed lot size |
| HB | Replenish to max |
| TB | Daily lot size |
| WB | Weekly lot size |
| MB | Monthly lot size |

---

## Sales & Distribution (SD)

### Key Processes

| Process | T-Codes | Description |
|---------|---------|-------------|
| Sales Order | VA01, VA02, VA03 | Create, change, display SO |
| Delivery | VL01N, VL02N, VL03N | Create, change, display delivery |
| Goods Issue | VL02N | Post goods issue |
| Billing | VF01, VF02, VF03 | Create, change, display invoice |
| Customer Master | XD01, XD02, XD03 | Create, change, display customer |
| Pricing | VK11, VK12, VK13 | Maintain condition records |
| Availability | CO09, MD04 | Check ATP |

### Order-to-Cash Flow

```
Customer Inquiry (VA11)
         │
         ▼
Quotation (VA21)
         │
         ▼
Sales Order (VA01)
         │
         ▼
Delivery (VL01N)
         │
         ▼
Goods Issue (VL02N)
         │
         ▼
Billing (VF01)
         │
         ▼
Payment Receipt (FI)
```

---

## Quality Management (QM)

### Key Processes

| Process | T-Codes | Description |
|---------|---------|-------------|
| Inspection Lot | QA01, QA02, QA03 | Create, change, display |
| Results Recording | QE51N | Enter inspection results |
| Usage Decision | QA11, QA12 | Accept/reject lot |
| Quality Notification | QM01, QM02 | Create, change notification |
| Quality Certificate | QC21, QC22 | Create, display certificate |
| Inspection Plan | QP01, QP02 | Create, change plan |
| Master Inspection Char | QS21, QS22 | Create, change MIC |

### Inspection Types

| Type | Description | Trigger |
|------|-------------|---------|
| 01 | Goods Receipt | PO receipt |
| 02 | Goods Receipt (Prod) | Production GR |
| 03 | In-process | During production |
| 04 | Final Inspection | Before delivery |
| 05 | Audit | Periodic audit |
| 08/09 | Recurring | Time-based |
| 10 | Source Inspection | At vendor |

### Usage Decision Codes

| Code | Description | Stock Posting |
|------|-------------|---------------|
| A | Accept | Unrestricted |
| R | Reject | Blocked/Scrap |
| P | Partial | Split stock |

---

## Plant Maintenance (PM)

### Key Processes

| Process | T-Codes | Description |
|---------|---------|-------------|
| Equipment Master | IE01, IE02, IE03 | Create, change, display |
| Functional Location | IL01, IL02, IL03 | Create, change, display |
| Maintenance Order | IW31, IW32, IW33 | Create, change, display |
| Notification | IW21, IW22, IW23 | Create, change, display |
| Work Order Confirm | IW41, IW42 | Time confirmation |
| Preventive Maint | IP10, IP30 | Schedule, deadline monitoring |
| Task List | IA01, IA02 | Create, change task list |

### Maintenance Order Types

| Type | Description |
|------|-------------|
| PM01 | Corrective Maintenance |
| PM02 | Preventive Maintenance |
| PM03 | Refurbishment |
| PM04 | Calibration |

---

## Finance & Controlling (FI/CO)

### Key T-Codes

| Process | T-Codes | Description |
|---------|---------|-------------|
| G/L Posting | FB50, FB01 | Document entry |
| Vendor Invoice | FB60 | A/P invoice |
| Customer Invoice | FB70 | A/R invoice |
| Payment | F110 | Automatic payment |
| Cost Center | KS01, KS02 | Create, change CC |
| Internal Order | KO01, KO02 | Create, change order |
| Cost Analysis | KSB1, KOB1 | Line item reports |

### Document Types

| Type | Description |
|------|-------------|
| SA | G/L Account Document |
| RE | Invoice - Gross |
| KR | Vendor Invoice |
| KG | Vendor Credit Memo |
| DR | Customer Invoice |
| DG | Customer Credit Memo |

---

## Common Integration Scenarios

### Procure-to-Pay

```
MM (PR → PO) → MM (GR) → QM (Inspection) → MM (Stock) → FI (Invoice → Payment)
```

### Plan-to-Produce

```
SD (SO) → PP (MRP) → PP (Prod Order) → MM (GI) → PP (Confirm) → MM (GR) → CO (Settlement)
```

### Order-to-Cash

```
SD (SO) → MM (ATP) → SD (Delivery) → MM (GI) → SD (Billing) → FI (A/R)
```

---

## Troubleshooting Quick Reference

### Common Issues

| Issue | Check | Resolution |
|-------|-------|------------|
| PO won't release | Release strategy | Check approval workflow |
| GR blocked | QM inspection | Complete usage decision |
| MRP not running | Planning file | MDAB/MD21 to reset |
| Invoice mismatch | 3-way match | Check PO/GR quantities |
| Stock negative | Movement type | Correct posting/reversal |
| Order not settling | Status | Check TECO status |

### Useful Reports

| Report | T-Code | Purpose |
|--------|--------|---------|
| Stock Overview | MB52 | Warehouse stock |
| Purchase Orders | ME2M | PO by material |
| Open Orders | COOIS | Production order status |
| MRP List | MD05 | Planning results |
| Delivery Due | VL10 | Deliveries to create |
| Open Items | FBL1N/FBL5N | A/P, A/R aging |

---

## Best Practices for Automotive

### Master Data Quality

1. **Material Master**
   - Complete all required views
   - Accurate lead times
   - Correct UoM and conversion
   - Updated safety stock

2. **BOM Accuracy**
   - Current revision level
   - Correct quantities
   - Valid date ranges
   - Phantom assemblies where appropriate

3. **Routing Accuracy**
   - Realistic operation times
   - Correct work centers
   - Setup and run time split
   - Scrap factors

### IATF 16949 Alignment

| SAP Process | IATF Requirement |
|-------------|------------------|
| QM Inspection | Product verification |
| Batch Traceability | Identification and traceability |
| Document Control | Documented information |
| Calibration (PM) | Monitoring and measuring resources |
| Change Management | Design and development changes |

---

## Quick Reference Cards

### Movement Types

| Type | Description | Process |
|------|-------------|---------|
| 101 | GR from purchase order | MIGO |
| 102 | Reversal of 101 | MIGO |
| 103 | GR to quality inspection | MIGO |
| 104 | Reversal of 103 | MIGO |
| 105 | GR to blocked stock | MIGO |
| 201 | GI for cost center | MIGO |
| 261 | GI for production order | MIGO |
| 262 | Reversal of 261 | MIGO |
| 301 | Transfer posting plant to plant | MIGO |
| 311 | Transfer to another storage location | MIGO |
| 501 | GR without PO | MIGO |
| 561 | Initial entry of stock | MIGO |
| 601 | GI for delivery | VL02N |

### Order Status Codes

| Status | Description |
|--------|-------------|
| CRTD | Created |
| REL | Released |
| PCNF | Partially confirmed |
| CNF | Confirmed |
| PDLV | Partially delivered |
| DLV | Delivered |
| TECO | Technically complete |
| CLSD | Closed |
| DLFL | Deletion flag |

---

## Integration with PAI Skills

### AutomotiveManufacturing
- Work instructions reference SAP transactions
- Document control aligned with SAP DMS
- Quality procedures link to QM inspection

### SupplyChain
- Purchasing processes in MM
- Supplier scorecards from QM data
- Inventory management strategies

### A3CriticalThinking
- Root cause analysis for SAP process issues
- Priority hierarchy for system changes

---

## Extended Context

For detailed transaction guides and configuration:
`read ~/.claude/skills/SapEcc/CLAUDE.md`

For transaction code reference:
`read ~/.claude/skills/SapEcc/reference/tcodes.md`
