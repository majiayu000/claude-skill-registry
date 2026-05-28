---
name: Enterprise ERP Consultant
description: Expert guidance for enterprise resource planning systems, business logic, domain modeling, and ERP integration patterns. Use when building ERP systems, implementing business workflows, or integrating with ERP platforms.
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
---

# Enterprise ERP Consultant

Enterprise resource planning architecture and business domain patterns.

## Core ERP Modules

### 1. Financial Management

```typescript
// Chart of Accounts
interface Account {
  code: string;
  name: string;
  type: 'asset' | 'liability' | 'equity' | 'revenue' | 'expense';
  parentCode?: string;
  balance: number;
}

// General Ledger Entry
interface JournalEntry {
  id: string;
  date: Date;
  description: string;
  lines: JournalLine[];
  posted: boolean;
}

interface JournalLine {
  accountCode: string;
  debit: number;
  credit: number;
  description: string;
}

// Double-entry bookkeeping validation
function validateJournalEntry(entry: JournalEntry): boolean {
  const totalDebit = entry.lines.reduce((sum, line) => sum + line.debit, 0);
  const totalCredit = entry.lines.reduce((sum, line) => sum + line.credit, 0);
  return Math.abs(totalDebit - totalCredit) < 0.01; // Allow for rounding
}
```

### 2. Inventory Management

```python
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field

class InventoryMethod(str, Enum):
    FIFO = "fifo"  # First In, First Out
    LIFO = "lifo"  # Last In, First Out
    AVERAGE = "average"  # Weighted Average

class StockMovement(BaseModel):
    product_id: str
    quantity: int
    movement_type: str  # 'in', 'out', 'adjustment'
    reference: str
    timestamp: datetime
    cost_per_unit: float = 0

class InventoryService:
    def __init__(self, method: InventoryMethod = InventoryMethod.FIFO):
        self.method = method
        self.stock_layers: dict[str, list[StockMovement]] = {}

    def receive_stock(self, product_id: str, quantity: int, cost: float):
        """Record stock receipt."""
        if product_id not in self.stock_layers:
            self.stock_layers[product_id] = []

        movement = StockMovement(
            product_id=product_id,
            quantity=quantity,
            movement_type='in',
            reference=f"PO-{datetime.now().timestamp()}",
            timestamp=datetime.now(),
            cost_per_unit=cost
        )
        self.stock_layers[product_id].append(movement)

    def issue_stock(self, product_id: str, quantity: int) -> float:
        """Issue stock and return COGS."""
        if product_id not in self.stock_layers:
            raise ValueError(f"Product {product_id} not found")

        layers = self.stock_layers[product_id]
        remaining = quantity
        cogs = 0.0

        if self.method == InventoryMethod.FIFO:
            for layer in layers:
                if remaining <= 0:
                    break
                issued = min(layer.quantity, remaining)
                cogs += issued * layer.cost_per_unit
                layer.quantity -= issued
                remaining -= issued

        return cogs

    def get_inventory_value(self, product_id: str) -> float:
        """Calculate current inventory value."""
        layers = self.stock_layers.get(product_id, [])
        return sum(layer.quantity * layer.cost_per_unit for layer in layers)
```

### 3. Order Management

```typescript
// Order-to-Cash Process
interface SalesOrder {
  orderId: string;
  customerId: string;
  orderDate: Date;
  status: OrderStatus;
  lines: OrderLine[];
  totalAmount: number;
  paymentTerms: string;
}

enum OrderStatus {
  Draft = 'draft',
  Confirmed = 'confirmed',
  Shipped = 'shipped',
  Invoiced = 'invoiced',
  Paid = 'paid',
  Cancelled = 'cancelled',
}

interface OrderLine {
  productId: string;
  quantity: number;
  unitPrice: number;
  discount: number;
  taxRate: number;
  lineTotal: number;
}

class OrderWorkflow {
  async confirmOrder(orderId: string): Promise<void> {
    const order = await this.getOrder(orderId);

    // Check inventory availability
    for (const line of order.lines) {
      const available = await this.checkInventory(line.productId);
      if (available < line.quantity) {
        throw new Error(`Insufficient inventory for ${line.productId}`);
      }
    }

    // Reserve inventory
    for (const line of order.lines) {
      await this.reserveInventory(line.productId, line.quantity);
    }

    // Update order status
    await this.updateOrderStatus(orderId, OrderStatus.Confirmed);

    // Create shipment
    await this.createShipment(orderId);
  }

  async invoiceOrder(orderId: string): Promise<string> {
    const order = await this.getOrder(orderId);

    if (order.status !== OrderStatus.Shipped) {
      throw new Error('Order must be shipped before invoicing');
    }

    // Create invoice
    const invoice = await this.createInvoice(order);

    // Create accounting entries
    await this.createJournalEntry({
      date: new Date(),
      description: `Invoice ${invoice.id}`,
      lines: [
        { accountCode: '1200', debit: order.totalAmount, credit: 0 }, // AR
        { accountCode: '4000', debit: 0, credit: order.totalAmount }, // Revenue
      ],
    });

    // Update order status
    await this.updateOrderStatus(orderId, OrderStatus.Invoiced);

    return invoice.id;
  }
}
```

### 4. Manufacturing (MRP)

```python
from datetime import datetime, timedelta
from typing import List

class BillOfMaterials(BaseModel):
    """Product structure definition."""
    product_id: str
    components: List['BOMComponent']

class BOMComponent(BaseModel):
    component_id: str
    quantity: float
    unit: str
    scrap_factor: float = 0.05  # 5% default scrap

class ManufacturingOrder(BaseModel):
    mo_id: str
    product_id: str
    quantity: float
    scheduled_start: datetime
    scheduled_end: datetime
    status: str  # 'draft', 'confirmed', 'in_progress', 'done'

class MRPEngine:
    """Material Requirements Planning."""

    def calculate_requirements(
        self,
        product_id: str,
        quantity: float,
        required_date: datetime
    ) -> List[dict]:
        """Calculate material requirements."""
        bom = self.get_bom(product_id)
        requirements = []

        for component in bom.components:
            net_quantity = quantity * component.quantity * (1 + component.scrap_factor)
            on_hand = self.get_on_hand(component.component_id)
            on_order = self.get_on_order(component.component_id)

            net_requirement = max(0, net_quantity - on_hand - on_order)

            if net_requirement > 0:
                # Calculate lead time
                lead_time = self.get_lead_time(component.component_id)
                order_date = required_date - timedelta(days=lead_time)

                requirements.append({
                    'component_id': component.component_id,
                    'quantity': net_requirement,
                    'required_date': required_date,
                    'order_date': order_date,
                    'action': 'purchase' if self.is_purchased(component.component_id) else 'manufacture'
                })

                # Recursively calculate for sub-assemblies
                if self.has_bom(component.component_id):
                    sub_requirements = self.calculate_requirements(
                        component.component_id,
                        net_requirement,
                        order_date
                    )
                    requirements.extend(sub_requirements)

        return requirements
```

### 5. Multi-Tenancy & Data Isolation

```typescript
// Row-Level Security Pattern
interface TenantContext {
  tenantId: string;
  userId: string;
  permissions: string[];
}

class TenantAwareRepository<T> {
  constructor(
    private tenantContext: TenantContext,
    private db: Database
  ) {}

  async find(filters: any): Promise<T[]> {
    // Automatically add tenant filter
    return this.db.query({
      ...filters,
      tenant_id: this.tenantContext.tenantId,
    });
  }

  async create(data: Partial<T>): Promise<T> {
    // Automatically add tenant ID
    return this.db.insert({
      ...data,
      tenant_id: this.tenantContext.tenantId,
      created_by: this.tenantContext.userId,
    });
  }
}

// PostgreSQL RLS policy
const RLS_POLICY = `
CREATE POLICY tenant_isolation ON invoices
  FOR ALL
  USING (tenant_id = current_setting('app.current_tenant')::uuid);

ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
`;
```

### 6. Approval Workflows

```python
from enum import Enum

class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class ApprovalRule(BaseModel):
    document_type: str
    amount_threshold: float
    approver_role: str
    sequence: int

class ApprovalWorkflow:
    def __init__(self):
        self.rules: List[ApprovalRule] = []

    def add_rule(self, rule: ApprovalRule):
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.sequence)

    async def submit_for_approval(
        self,
        document_type: str,
        document_id: str,
        amount: float
    ) -> str:
        """Submit document for approval."""
        applicable_rules = [
            rule for rule in self.rules
            if rule.document_type == document_type and amount >= rule.amount_threshold
        ]

        if not applicable_rules:
            # Auto-approve if no rules apply
            return await self.auto_approve(document_id)

        # Create approval requests
        for rule in applicable_rules:
            await self.create_approval_request(
                document_id=document_id,
                approver_role=rule.approver_role,
                sequence=rule.sequence
            )

        return "pending_approval"

    async def approve(self, approval_id: str, approver_id: str):
        """Process approval."""
        approval = await self.get_approval(approval_id)
        approval.status = ApprovalStatus.APPROVED
        approval.approved_by = approver_id
        approval.approved_at = datetime.now()

        # Check if all approvals complete
        all_approvals = await self.get_document_approvals(approval.document_id)
        if all(a.status == ApprovalStatus.APPROVED for a in all_approvals):
            await self.finalize_document(approval.document_id)
```

### 7. Audit Trail

```typescript
interface AuditLog {
  id: string;
  tenantId: string;
  userId: string;
  action: 'create' | 'update' | 'delete';
  entityType: string;
  entityId: string;
  changes: Record<string, { old: any; new: any }>;
  timestamp: Date;
  ipAddress: string;
}

class AuditService {
  async logChange(
    entity: any,
    oldValues: any,
    action: string
  ): Promise<void> {
    const changes: Record<string, any> = {};

    for (const key in entity) {
      if (entity[key] !== oldValues?.[key]) {
        changes[key] = {
          old: oldValues?.[key],
          new: entity[key],
        };
      }
    }

    await this.createAuditLog({
      action,
      entityType: entity.constructor.name,
      entityId: entity.id,
      changes,
      timestamp: new Date(),
    });
  }
}
```

## Integration Patterns

### SAP Integration
```python
from pyrfc import Connection

class SAPConnector:
    def __init__(self, config: dict):
        self.conn = Connection(**config)

    def create_sales_order(self, order_data: dict) -> str:
        """Create sales order in SAP."""
        result = self.conn.call(
            'BAPI_SALESORDER_CREATEFROMDAT2',
            ORDER_HEADER_IN=order_data['header'],
            ORDER_ITEMS_IN=order_data['items']
        )
        return result['SALESDOCUMENT']
```

---

**When to Use:** ERP development, business logic implementation, financial systems, inventory management, order processing.
