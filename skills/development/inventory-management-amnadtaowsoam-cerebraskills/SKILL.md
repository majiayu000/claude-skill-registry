---
name: Inventory Management
description: Tracking stock levels, managing reservations, handling stock movements, and providing forecasting for e-commerce operations with real-time updates, multi-warehouse support, and low stock alerts.
---

# Inventory Management

> **Current Level:** Intermediate  
> **Domain:** E-commerce / Backend

---

## Overview

Inventory management tracks stock levels, manages reservations, handles stock movements, and provides forecasting for e-commerce operations. Effective inventory systems provide real-time stock updates, support multiple warehouses, handle reservations, and alert on low stock.

---

## Core Concepts

### Table of Contents

1. [Inventory Concepts](#inventory-concepts)
2. [Stock Tracking](#stock-tracking)
3. [Database Schema](#database-schema)
4. [Stock Updates](#stock-updates)
5. [Stock Reservation](#stock-reservation)
6. [Low Stock Alerts](#low-stock-alerts)
7. [Multi-Warehouse Support](#multi-warehouse-support)
8. [Stock Movements](#stock-movements)
9. [Inventory Adjustments](#inventory-adjustments)
10. [Stock Synchronization](#stock-synchronization)
11. [Inventory Reports](#inventory-reports)
12. [Forecasting](#forecasting)
13. [Optimistic Locking](#optimistic-locking)
14. [Best Practices](#best-practices)

---

## Inventory Concepts

### Inventory Types

```typescript
enum InventoryType {
  PHYSICAL = 'physical',      // Actual stock on hand
  AVAILABLE = 'available',    // Available for sale (physical - reserved)
  RESERVED = 'reserved',      // Reserved for orders
  IN_TRANSIT = 'in_transit',  // In transit to warehouse
  DAMAGED = 'damaged',        // Damaged items
  RETURNED = 'returned',      // Returned items
}

enum MovementType {
  PURCHASE = 'purchase',      // Stock in from supplier
  SALE = 'sale',              // Stock out from sale
  RETURN_IN = 'return_in',    // Returned from customer
  RETURN_OUT = 'return_out',  // Returned to supplier
  TRANSFER = 'transfer',      // Transfer between warehouses
  ADJUSTMENT = 'adjustment',  // Manual adjustment
  DAMAGE = 'damage',          // Damaged items
}

enum ReservationStatus {
  RESERVED = 'reserved',
  CONFIRMED = 'confirmed',
  RELEASED = 'released',
  CANCELLED = 'cancelled',
}
```

---

## Stock Tracking

### Inventory Tracker

```typescript
class InventoryTracker {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get stock level
   */
  async getStockLevel(params: {
    productId: string;
    variantId?: string;
    warehouseId?: string;
  }): Promise<{
    physical: number;
    available: number;
    reserved: number;
    inTransit: number;
    damaged: number;
  }> {
    const where: any = {
      productId: params.productId,
      variantId: params.variantId || null,
    };

    if (params.warehouseId) {
      where.warehouseId = params.warehouseId;
    }

    const inventory = await this.prisma.inventory.findFirst({
      where,
    });

    if (!inventory) {
      return {
        physical: 0,
        available: 0,
        reserved: 0,
        inTransit: 0,
        damaged: 0,
      };
    }

    return {
      physical: inventory.quantity,
      available: inventory.quantity - inventory.reserved,
      reserved: inventory.reserved,
      inTransit: inventory.inTransit || 0,
      damaged: inventory.damaged || 0,
    };
  }

  /**
   * Get stock levels for multiple products
   */
  async getStockLevels(params: {
    productIds: string[];
    warehouseId?: string;
  }): Promise<Map<string, StockLevel>> {
    const where: any = {
      productId: { in: params.productIds },
    };

    if (params.warehouseId) {
      where.warehouseId = params.warehouseId;
    }

    const inventories = await this.prisma.inventory.findMany({
      where,
    });

    const stockLevels = new Map<string, StockLevel>();

    for (const inventory of inventories) {
      const key = `${inventory.productId}:${inventory.variantId || ''}`;

      stockLevels.set(key, {
        productId: inventory.productId,
        variantId: inventory.variantId,
        physical: inventory.quantity,
        available: inventory.quantity - inventory.reserved,
        reserved: inventory.reserved,
        inTransit: inventory.inTransit || 0,
        damaged: inventory.damaged || 0,
      });
    }

    return stockLevels;
  }

  /**
   * Check availability
   */
  async checkAvailability(params: {
    productId: string;
    variantId?: string;
    quantity: number;
    warehouseId?: string;
  }): Promise<boolean> {
    const stockLevel = await this.getStockLevel(params);

    return stockLevel.available >= params.quantity;
  }
}

interface StockLevel {
  productId: string;
  variantId?: string;
  physical: number;
  available: number;
  reserved: number;
  inTransit: number;
  damaged: number;
}
```

---

## Database Schema

### Prisma Schema

```prisma
model Inventory {
  id          String   @id @default(uuid())
  productId   String
  product     Product  @relation(fields: [productId], references: [id])
  variantId   String?
  variant     Variant? @relation(fields: [variantId], references: [id])
  warehouseId String
  warehouse   Warehouse @relation(fields: [warehouseId], references: [id])
  quantity    Int      @default(0)
  reserved    Int      @default(0)
  inTransit   Int      @default(0)
  damaged     Int      @default(0)
  location    String?
  binLocation String?
  version     Int      @default(0) // For optimistic locking
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  movements   InventoryMovement[]
  reservations InventoryReservation[]

  @@unique([productId, variantId, warehouseId])
  @@index([productId])
  @@index([warehouseId])
}

model InventoryMovement {
  id          String       @id @default(uuid())
  inventoryId String
  inventory   Inventory    @relation(fields: [inventoryId], references: [id], onDelete: Cascade)
  type        MovementType
  quantity    Int
  referenceId String?      // Order ID, Purchase Order ID, etc.
  notes       String?
  createdAt   DateTime     @default(now())
  createdBy   String?

  @@index([inventoryId])
  @@index([createdAt])
  @@index([referenceId])
}

model InventoryReservation {
  id          String            @id @default(uuid())
  inventoryId String
  inventory   Inventory         @relation(fields: [inventoryId], references: [id], onDelete: Cascade)
  orderId     String
  order       Order             @relation(fields: [orderId], references: [id])
  quantity    Int
  status      ReservationStatus @default(RESERVED)
  expiresAt   DateTime?
  createdAt   DateTime          @default(now())
  updatedAt   DateTime          @updatedAt
  confirmedAt DateTime?
  releasedAt  DateTime?

  @@index([inventoryId])
  @@index([orderId])
  @@index([status])
  @@index([expiresAt])
}

model Warehouse {
  id          String      @id @default(uuid())
  name        String
  code        String      @unique
  address     Json
  isActive    Boolean     @default(true)
  isDefault   Boolean     @default(false)
  inventories Inventory[]
  transfers   StockTransfer[]
  createdAt   DateTime    @default(now())
  updatedAt   DateTime    @updatedAt

  @@index([code])
}

model StockTransfer {
  id              String   @id @default(uuid())
  fromWarehouseId  String
  fromWarehouse    Warehouse @relation("FromWarehouse", fields: [fromWarehouseId], references: [id])
  toWarehouseId   String
  toWarehouse      Warehouse @relation("ToWarehouse", fields: [toWarehouseId], references: [id])
  productId       String
  variantId       String?
  quantity        Int
  status          String   @default("pending") // pending, in_transit, completed, cancelled
  trackingNumber  String?
  notes           String?
  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt
  completedAt     DateTime?
  movements       InventoryMovement[]

  @@index([fromWarehouseId])
  @@index([toWarehouseId])
  @@index([status])
}

model LowStockAlert {
  id          String   @id @default(uuid())
  productId   String
  variantId   String?
  warehouseId String
  quantity    Int
  threshold   Int
  isResolved  Boolean  @default(false)
  resolvedAt  DateTime?
  createdAt   DateTime @default(now())

  @@index([productId])
  @@index([isResolved])
  @@index([createdAt])
}
```

---

## Stock Updates

### Stock Updater

```typescript
class StockUpdater {
  constructor(private prisma: PrismaClient) {}

  /**
   * Update stock with optimistic locking
   */
  async updateStock(params: {
    productId: string;
    variantId?: string;
    warehouseId: string;
    quantity: number;
    type: MovementType;
    referenceId?: string;
    notes?: string;
    createdBy?: string;
  }): Promise<Inventory> {
    return await this.prisma.$transaction(async (tx) => {
      // Find inventory
      const inventory = await tx.inventory.findFirst({
        where: {
          productId: params.productId,
          variantId: params.variantId || null,
          warehouseId: params.warehouseId,
        },
      });

      if (!inventory) {
        // Create inventory record
        const newInventory = await tx.inventory.create({
          data: {
            productId: params.productId,
            variantId: params.variantId || null,
            warehouseId: params.warehouseId,
            quantity: params.quantity,
          },
        });

        // Create movement
        await tx.inventoryMovement.create({
          data: {
            inventoryId: newInventory.id,
            type: params.type,
            quantity: params.quantity,
            referenceId: params.referenceId,
            notes: params.notes,
            createdBy: params.createdBy,
          },
        });

        return newInventory;
      }

      // Update with optimistic locking
      const newQuantity = inventory.quantity + params.quantity;

      if (newQuantity < 0) {
        throw new Error('Insufficient stock');
      }

      const updated = await tx.inventory.update({
        where: {
          id: inventory.id,
          version: inventory.version,
        },
        data: {
          quantity: newQuantity,
          version: { increment: 1 },
        },
      });

      // Create movement
      await tx.inventoryMovement.create({
        data: {
          inventoryId: inventory.id,
          type: params.type,
          quantity: params.quantity,
          referenceId: params.referenceId,
          notes: params.notes,
          createdBy: params.createdBy,
        },
      });

      // Check for low stock
      await this.checkLowStock(tx, updated);

      return updated;
    });
  }

  /**
   * Bulk update stock
   */
  async bulkUpdateStock(params: Array<{
    productId: string;
    variantId?: string;
    warehouseId: string;
    quantity: number;
    type: MovementType;
    referenceId?: string;
  }>): Promise<void> {
    await this.prisma.$transaction(async (tx) => {
      for (const item of params) {
        await this.updateStock({
          ...item,
          tx,
        });
      }
    });
  }

  /**
   * Check low stock
   */
  private async checkLowStock(
    tx: Prisma.TransactionClient,
    inventory: Inventory
  ): Promise<void> {
    // Get low stock threshold
    const threshold = await this.getLowStockThreshold(
      inventory.productId,
      inventory.variantId
    );

    const available = inventory.quantity - inventory.reserved;

    if (available <= threshold) {
      // Check if alert already exists
      const existingAlert = await tx.lowStockAlert.findFirst({
        where: {
          productId: inventory.productId,
          variantId: inventory.variantId,
          warehouseId: inventory.warehouseId,
          isResolved: false,
        },
      });

      if (!existingAlert) {
        await tx.lowStockAlert.create({
          data: {
            productId: inventory.productId,
            variantId: inventory.variantId,
            warehouseId: inventory.warehouseId,
            quantity: available,
            threshold,
          },
        });

        // Send notification
        await this.sendLowStockNotification(inventory, available, threshold);
      }
    }
  }

  /**
   * Get low stock threshold
   */
  private async getLowStockThreshold(
    productId: string,
    variantId?: string
  ): Promise<number> {
    const product = await this.prisma.product.findUnique({
      where: { id: productId },
    });

    return product?.lowStockThreshold || 10;
  }

  /**
   * Send low stock notification
   */
  private async sendLowStockNotification(
    inventory: Inventory,
    quantity: number,
    threshold: number
  ): Promise<void> {
    const product = await this.prisma.product.findUnique({
      where: { id: inventory.productId },
    });

    console.log(`Low stock alert: ${product?.name} - ${quantity} (threshold: ${threshold})`);
  }

  constructor(private prisma: PrismaClient) {}
}
```

---

## Stock Reservation

### Reservation Manager

```typescript
class ReservationManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Reserve stock
   */
  async reserveStock(params: {
    orderId: string;
    items: Array<{
      productId: string;
      variantId?: string;
      quantity: number;
      warehouseId?: string;
    }>;
  }): Promise<void> {
    await this.prisma.$transaction(async (tx) => {
      for (const item of params.items) {
        // Find inventory
        const warehouseId = item.warehouseId || await this.getDefaultWarehouse();

        const inventory = await tx.inventory.findFirst({
          where: {
            productId: item.productId,
            variantId: item.variantId || null,
            warehouseId,
          },
        });

        if (!inventory) {
          throw new Error(`Inventory not found for product ${item.productId}`);
        }

        const available = inventory.quantity - inventory.reserved;

        if (available < item.quantity) {
          throw new Error(`Insufficient stock for product ${item.productId}`);
        }

        // Update inventory
        await tx.inventory.update({
          where: { id: inventory.id },
          data: {
            reserved: { increment: item.quantity },
            version: { increment: 1 },
          },
        });

        // Create reservation
        await tx.inventoryReservation.create({
          data: {
            inventoryId: inventory.id,
            orderId: params.orderId,
            quantity: item.quantity,
            status: ReservationStatus.RESERVED,
            expiresAt: new Date(Date.now() + 30 * 60 * 1000), // 30 minutes
          },
        });
      }
    });
  }

  /**
   * Confirm reservation
   */
  async confirmReservation(orderId: string): Promise<void> {
    const reservations = await this.prisma.inventoryReservation.findMany({
      where: {
        orderId,
        status: ReservationStatus.RESERVED,
      },
      include: { inventory: true },
    });

    await this.prisma.$transaction(async (tx) => {
      for (const reservation of reservations) {
        await tx.inventoryReservation.update({
          where: { id: reservation.id },
          data: {
            status: ReservationStatus.CONFIRMED,
            confirmedAt: new Date(),
          },
        });

        // Deduct from physical stock
        await tx.inventory.update({
          where: { id: reservation.inventoryId },
          data: {
            quantity: { decrement: reservation.quantity },
            reserved: { decrement: reservation.quantity },
            version: { increment: 1 },
          },
        });
      }
    });
  }

  /**
   * Release reservation
   */
  async releaseReservation(orderId: string): Promise<void> {
    const reservations = await this.prisma.inventoryReservation.findMany({
      where: {
        orderId,
        status: ReservationStatus.RESERVED,
      },
      include: { inventory: true },
    });

    await this.prisma.$transaction(async (tx) => {
      for (const reservation of reservations) {
        await tx.inventoryReservation.update({
          where: { id: reservation.id },
          data: {
            status: ReservationStatus.RELEASED,
            releasedAt: new Date(),
          },
        });

        // Release reserved stock
        await tx.inventory.update({
          where: { id: reservation.inventoryId },
          data: {
            reserved: { decrement: reservation.quantity },
            version: { increment: 1 },
          },
        });
      }
    });
  }

  /**
   * Cancel expired reservations
   */
  async cancelExpiredReservations(): Promise<void> {
    const expiredReservations = await this.prisma.inventoryReservation.findMany({
      where: {
        status: ReservationStatus.RESERVED,
        expiresAt: { lt: new Date() },
      },
      include: { inventory: true },
    });

    await this.prisma.$transaction(async (tx) => {
      for (const reservation of expiredReservations) {
        await tx.inventoryReservation.update({
          where: { id: reservation.id },
          data: {
            status: ReservationStatus.CANCELLED,
            releasedAt: new Date(),
          },
        });

        // Release reserved stock
        await tx.inventory.update({
          where: { id: reservation.inventoryId },
          data: {
            reserved: { decrement: reservation.quantity },
            version: { increment: 1 },
          },
        });
      }
    });
  }

  /**
   * Get default warehouse
   */
  private async getDefaultWarehouse(): Promise<string> {
    const warehouse = await this.prisma.warehouse.findFirst({
      where: { isDefault: true },
    });

    if (!warehouse) {
      throw new Error('No default warehouse configured');
    }

    return warehouse.id;
  }

  constructor(private prisma: PrismaClient) {}
}
```

---

## Low Stock Alerts

### Alert Manager

```typescript
class LowStockAlertManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get active alerts
   */
  async getActiveAlerts(params?: {
    productId?: string;
    warehouseId?: string;
  }): Promise<LowStockAlert[]> {
    const where: any = {
      isResolved: false,
    };

    if (params?.productId) {
      where.productId = params.productId;
    }

    if (params?.warehouseId) {
      where.warehouseId = params.warehouseId;
    }

    return await this.prisma.lowStockAlert.findMany({
      where,
      include: {
        product: true,
      },
      orderBy: { createdAt: 'desc' },
    });
  }

  /**
   * Resolve alert
   */
  async resolveAlert(alertId: string): Promise<LowStockAlert> {
    return await this.prisma.lowStockAlert.update({
      where: { id: alertId },
      data: {
        isResolved: true,
        resolvedAt: new Date(),
      },
    });
  }

  /**
   * Auto-resolve alerts
   */
  async autoResolveAlerts(): Promise<void> {
    const alerts = await this.prisma.lowStockAlert.findMany({
      where: { isResolved: false },
      include: { product: true },
    });

    for (const alert of alerts) {
      // Check current stock level
      const inventory = await this.prisma.inventory.findFirst({
        where: {
          productId: alert.productId,
          variantId: alert.variantId,
          warehouseId: alert.warehouseId,
        },
      });

      if (!inventory) continue;

      const available = inventory.quantity - inventory.reserved;

      if (available > alert.threshold) {
        await this.resolveAlert(alert.id);
      }
    }
  }
}
```

---

## Multi-Warehouse Support

### Warehouse Manager

```typescript
class WarehouseManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create warehouse
   */
  async createWarehouse(params: {
    name: string;
    code: string;
    address: Address;
    isDefault?: boolean;
  }): Promise<Warehouse> {
    return await this.prisma.warehouse.create({
      data: {
        name: params.name,
        code: params.code,
        address: params.address,
        isDefault: params.isDefault || false,
      },
    });
  }

  /**
   * Get warehouses
   */
  async getWarehouses(): Promise<Warehouse[]> {
    return await this.prisma.warehouse.findMany({
      where: { isActive: true },
      orderBy: { name: 'asc' },
    });
  }

  /**
   * Transfer stock between warehouses
   */
  async transferStock(params: {
    fromWarehouseId: string;
    toWarehouseId: string;
    productId: string;
    variantId?: string;
    quantity: number;
    notes?: string;
  }): Promise<StockTransfer> {
    return await this.prisma.$transaction(async (tx) => {
      // Create transfer record
      const transfer = await tx.stockTransfer.create({
        data: {
          fromWarehouseId: params.fromWarehouseId,
          toWarehouseId: params.toWarehouseId,
          productId: params.productId,
          variantId: params.variantId,
          quantity: params.quantity,
          status: 'pending',
          notes: params.notes,
        },
      });

      // Deduct from source warehouse
      const sourceInventory = await tx.inventory.findFirst({
        where: {
          productId: params.productId,
          variantId: params.variantId || null,
          warehouseId: params.fromWarehouseId,
        },
      });

      if (!sourceInventory || sourceInventory.quantity < params.quantity) {
        throw new Error('Insufficient stock in source warehouse');
      }

      await tx.inventory.update({
        where: { id: sourceInventory.id },
        data: {
          quantity: { decrement: params.quantity },
          version: { increment: 1 },
        },
      });

      // Create movement
      await tx.inventoryMovement.create({
        data: {
          inventoryId: sourceInventory.id,
          type: MovementType.TRANSFER,
          quantity: -params.quantity,
          referenceId: transfer.id,
          notes: `Transfer to warehouse ${params.toWarehouseId}`,
        },
      });

      return transfer;
    });
  }

  /**
   * Complete transfer
   */
  async completeTransfer(transferId: string): Promise<StockTransfer> {
    return await this.prisma.$transaction(async (tx) => {
      const transfer = await tx.stockTransfer.findUnique({
        where: { id: transferId },
      });

      if (!transfer) {
        throw new Error('Transfer not found');
      }

      if (transfer.status !== 'in_transit') {
        throw new Error('Transfer is not in transit');
      }

      // Add to destination warehouse
      const destInventory = await tx.inventory.findFirst({
        where: {
          productId: transfer.productId,
          variantId: transfer.variantId || null,
          warehouseId: transfer.toWarehouseId,
        },
      });

      if (destInventory) {
        await tx.inventory.update({
          where: { id: destInventory.id },
          data: {
            quantity: { increment: transfer.quantity },
            version: { increment: 1 },
          },
        });

        await tx.inventoryMovement.create({
          data: {
            inventoryId: destInventory.id,
            type: MovementType.TRANSFER,
            quantity: transfer.quantity,
            referenceId: transfer.id,
            notes: `Transfer from warehouse ${transfer.fromWarehouseId}`,
          },
        });
      } else {
        await tx.inventory.create({
          data: {
            productId: transfer.productId,
            variantId: transfer.variantId || null,
            warehouseId: transfer.toWarehouseId,
            quantity: transfer.quantity,
          },
        });
      }

      // Update transfer status
      const updated = await tx.stockTransfer.update({
        where: { id: transferId },
        data: {
          status: 'completed',
          completedAt: new Date(),
        },
      });

      return updated;
    });
  }

  /**
   * Find nearest warehouse
   */
  async findNearestWarehouse(
    address: Address
  ): Promise<Warehouse | null> {
    const warehouses = await this.getWarehouses();

    // Implement geospatial search
    // For simplicity, return default warehouse
    return warehouses.find(w => w.isDefault) || warehouses[0] || null;
  }
}
```

---

## Stock Movements

### Movement Tracker

```typescript
class MovementTracker {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get movements
   */
  async getMovements(params: {
    productId?: string;
    variantId?: string;
    warehouseId?: string;
    type?: MovementType;
    startDate?: Date;
    endDate?: Date;
    page?: number;
    limit?: number;
  }): Promise<{
    movements: InventoryMovement[];
    total: number;
  }> {
    const where: any = {};

    if (params.productId) {
      where.inventory = {
        productId: params.productId,
      };
    }

    if (params.variantId) {
      where.inventory = {
        ...where.inventory,
        variantId: params.variantId,
      };
    }

    if (params.warehouseId) {
      where.inventory = {
        ...where.inventory,
        warehouseId: params.warehouseId,
      };
    }

    if (params.type) {
      where.type = params.type;
    }

    if (params.startDate || params.endDate) {
      where.createdAt = {};
      if (params.startDate) {
        where.createdAt.gte = params.startDate;
      }
      if (params.endDate) {
        where.createdAt.lte = params.endDate;
      }
    }

    const page = params.page || 1;
    const limit = params.limit || 50;
    const skip = (page - 1) * limit;

    const [movements, total] = await Promise.all([
      this.prisma.inventoryMovement.findMany({
        where,
        include: {
          inventory: {
            include: {
              product: true,
              variant: true,
              warehouse: true,
            },
          },
        },
        orderBy: { createdAt: 'desc' },
        skip,
        take: limit,
      }),
      this.prisma.inventoryMovement.count({ where }),
    ]);

    return { movements, total };
  }

  /**
   * Get movement summary
   */
  async getMovementSummary(params: {
    productId?: string;
    variantId?: string;
    warehouseId?: string;
    startDate: Date;
    endDate: Date;
  }): Promise<Record<MovementType, number>> {
    const where: any = {
      createdAt: {
        gte: params.startDate,
        lte: params.endDate,
      },
    };

    if (params.productId) {
      where.inventory = {
        productId: params.productId,
      };
    }

    if (params.variantId) {
      where.inventory = {
        ...where.inventory,
        variantId: params.variantId,
      };
    }

    if (params.warehouseId) {
      where.inventory = {
        ...where.inventory,
        warehouseId: params.warehouseId,
      };
    }

    const movements = await this.prisma.inventoryMovement.findMany({
      where,
    });

    const summary: Record<MovementType, number> = {
      [MovementType.PURCHASE]: 0,
      [MovementType.SALE]: 0,
      [MovementType.RETURN_IN]: 0,
      [MovementType.RETURN_OUT]: 0,
      [MovementType.TRANSFER]: 0,
      [MovementType.ADJUSTMENT]: 0,
      [MovementType.DAMAGE]: 0,
    };

    for (const movement of movements) {
      summary[movement.type] += movement.quantity;
    }

    return summary;
  }
}
```

---

## Inventory Adjustments

### Adjustment Manager

```typescript
class AdjustmentManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create adjustment
   */
  async createAdjustment(params: {
    productId: string;
    variantId?: string;
    warehouseId: string;
    quantity: number; // Can be positive or negative
    reason: string;
    createdBy: string;
  }): Promise<Inventory> {
    const stockUpdater = new StockUpdater(this.prisma);

    return await stockUpdater.updateStock({
      productId: params.productId,
      variantId: params.variantId,
      warehouseId: params.warehouseId,
      quantity: params.quantity,
      type: MovementType.ADJUSTMENT,
      notes: params.reason,
      createdBy: params.createdBy,
    });
  }

  /**
   * Bulk adjustment
   */
  async bulkAdjustment(params: {
    adjustments: Array<{
      productId: string;
      variantId?: string;
      warehouseId: string;
      quantity: number;
      reason: string;
    }>;
    createdBy: string;
  }): Promise<void> {
    const stockUpdater = new StockUpdater(this.prisma);

    for (const adjustment of params.adjustments) {
      await stockUpdater.updateStock({
        ...adjustment,
        type: MovementType.ADJUSTMENT,
        createdBy: params.createdBy,
      });
    }
  }

  /**
   * Cycle count
   */
  async cycleCount(params: {
    productId: string;
    variantId?: string;
    warehouseId: string;
    countedQuantity: number;
    countedBy: string;
  }): Promise<{
    inventory: Inventory;
    difference: number;
  }> {
    const inventory = await this.prisma.inventory.findFirst({
      where: {
        productId: params.productId,
        variantId: params.variantId || null,
        warehouseId: params.warehouseId,
      },
    });

    if (!inventory) {
      throw new Error('Inventory not found');
    }

    const difference = params.countedQuantity - inventory.quantity;

    if (difference !== 0) {
      await this.createAdjustment({
        productId: params.productId,
        variantId: params.variantId,
        warehouseId: params.warehouseId,
        quantity: difference,
        reason: `Cycle count: counted ${params.countedQuantity}, system ${inventory.quantity}`,
        createdBy: params.countedBy,
      });
    }

    return {
      inventory,
      difference,
    };
  }
}
```

---

## Stock Synchronization

### Sync Manager

```typescript
class SyncManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Sync with external system
   */
  async syncWithExternal(params: {
    externalStock: Array<{
      productId: string;
      variantId?: string;
      quantity: number;
      warehouseId: string;
    }>;
  }): Promise<{
    synced: number;
    errors: Array<{ item: any; error: string }>;
  }> {
    const stockUpdater = new StockUpdater(this.prisma);
    const errors: Array<{ item: any; error: string }> = [];
    let synced = 0;

    for (const item of params.externalStock) {
      try {
        // Get current inventory
        const inventory = await this.prisma.inventory.findFirst({
          where: {
            productId: item.productId,
            variantId: item.variantId || null,
            warehouseId: item.warehouseId,
          },
        });

        if (inventory) {
          const difference = item.quantity - inventory.quantity;

          if (difference !== 0) {
            await stockUpdater.updateStock({
              productId: item.productId,
              variantId: item.variantId,
              warehouseId: item.warehouseId,
              quantity: difference,
              type: MovementType.ADJUSTMENT,
              notes: 'Sync from external system',
            });
            synced++;
          }
        } else {
          await stockUpdater.updateStock({
            productId: item.productId,
            variantId: item.variantId,
            warehouseId: item.warehouseId,
            quantity: item.quantity,
            type: MovementType.PURCHASE,
            notes: 'Sync from external system',
          });
          synced++;
        }
      } catch (error) {
        errors.push({
          item,
          error: error.message,
        });
      }
    }

    return { synced, errors };
  }

  /**
   * Export inventory
   */
  async exportInventory(params?: {
    warehouseId?: string;
  }): Promise<Array<{
    productId: string;
    variantId?: string;
    warehouseId: string;
    quantity: number;
    reserved: number;
    available: number;
  }>> {
    const where: any = {};

    if (params?.warehouseId) {
      where.warehouseId = params.warehouseId;
    }

    const inventories = await this.prisma.inventory.findMany({
      where,
    });

    return inventories.map(inv => ({
      productId: inv.productId,
      variantId: inv.variantId || undefined,
      warehouseId: inv.warehouseId,
      quantity: inv.quantity,
      reserved: inv.reserved,
      available: inv.quantity - inv.reserved,
    }));
  }
}
```

---

## Inventory Reports

### Report Generator

```typescript
class InventoryReportGenerator {
  constructor(private prisma: PrismaClient) {}

  /**
   * Generate stock level report
   */
  async generateStockReport(params: {
    warehouseId?: string;
    lowStockOnly?: boolean;
  }): Promise<StockReport> {
    const where: any = {};

    if (params.warehouseId) {
      where.warehouseId = params.warehouseId;
    }

    if (params.lowStockOnly) {
      const lowStockProducts = await this.getLowStockProducts();
      where.productId = { in: lowStockProducts };
    }

    const inventories = await this.prisma.inventory.findMany({
      where,
      include: {
        product: true,
        variant: true,
        warehouse: true,
      },
    });

    const totalValue = inventories.reduce((sum, inv) => {
      const price = inv.variant?.price || inv.product?.price || 0;
      return sum + (price * inv.quantity);
    }, 0);

    return {
      totalItems: inventories.length,
      totalQuantity: inventories.reduce((sum, inv) => sum + inv.quantity, 0),
      totalValue,
      inventories,
    };
  }

  /**
   * Generate movement report
   */
  async generateMovementReport(params: {
    startDate: Date;
    endDate: Date;
    warehouseId?: string;
  }): Promise<MovementReport> {
    const where: any = {
      createdAt: {
        gte: params.startDate,
        lte: params.endDate,
      },
    };

    if (params.warehouseId) {
      where.inventory = {
        warehouseId: params.warehouseId,
      };
    }

    const movements = await this.prisma.inventoryMovement.findMany({
      where,
      include: {
        inventory: {
          include: {
            product: true,
            variant: true,
          },
        },
      },
    });

    const summary = this.summarizeMovements(movements);

    return {
      startDate: params.startDate,
      endDate: params.endDate,
      totalMovements: movements.length,
      summary,
      movements,
    };
  }

  /**
   * Generate valuation report
   */
  async generateValuationReport(params?: {
    warehouseId?: string;
  }): Promise<ValuationReport> {
    const where: any = {};

    if (params?.warehouseId) {
      where.warehouseId = params.warehouseId;
    }

    const inventories = await this.prisma.inventory.findMany({
      where,
      include: {
        product: true,
        variant: true,
      },
    });

    const items = inventories.map(inv => {
      const price = inv.variant?.price || inv.product?.price || 0;
      const cost = inv.variant?.cost || inv.product?.cost || 0;

      return {
        productId: inv.productId,
        variantId: inv.variantId,
        quantity: inv.quantity,
        unitPrice: price,
        unitCost: cost,
        totalValue: price * inv.quantity,
        totalCost: cost * inv.quantity,
        profit: (price - cost) * inv.quantity,
      };
    });

    const totalValue = items.reduce((sum, item) => sum + item.totalValue, 0);
    const totalCost = items.reduce((sum, item) => sum + item.totalCost, 0);
    const totalProfit = items.reduce((sum, item) => sum + item.profit, 0);

    return {
      items,
      totalValue,
      totalCost,
      totalProfit,
      profitMargin: totalValue > 0 ? (totalProfit / totalValue) * 100 : 0,
    };
  }

  private summarizeMovements(movements: any[]): Record<string, number> {
    const summary: Record<string, number> = {};

    for (const movement of movements) {
      const key = `${movement.type}`;
      summary[key] = (summary[key] || 0) + movement.quantity;
    }

    return summary;
  }

  private async getLowStockProducts(): Promise<string[]> {
    const alerts = await this.prisma.lowStockAlert.findMany({
      where: { isResolved: false },
      select: { productId: true },
    });

    return [...new Set(alerts.map(a => a.productId))];
  }

  constructor(private prisma: PrismaClient) {}
}

interface StockReport {
  totalItems: number;
  totalQuantity: number;
  totalValue: number;
  inventories: any[];
}

interface MovementReport {
  startDate: Date;
  endDate: Date;
  totalMovements: number;
  summary: Record<string, number>;
  movements: any[];
}

interface ValuationReport {
  items: any[];
  totalValue: number;
  totalCost: number;
  totalProfit: number;
  profitMargin: number;
}
```

---

## Forecasting

### Demand Forecaster

```typescript
class DemandForecaster {
  constructor(private prisma: PrismaClient) {}

  /**
   * Forecast demand
   */
  async forecastDemand(params: {
    productId: string;
    variantId?: string;
    days: number;
  }): Promise<{
    productId: string;
    variantId?: string;
    forecast: Array<{
      date: Date;
      predictedDemand: number;
      confidence: number;
    }>;
  }> {
    // Get historical sales data
    const historicalData = await this.getHistoricalSales(
      params.productId,
      params.variantId,
      90 // 90 days of history
    );

    // Simple moving average forecast
    const forecast: Array<{
      date: Date;
      predictedDemand: number;
      confidence: number;
    }> = [];

    for (let i = 1; i <= params.days; i++) {
      const date = new Date(Date.now() + i * 24 * 60 * 60 * 1000);
      const dayOfWeek = date.getDay();

      // Calculate average for this day of week
      const daySales = historicalData.filter(
        d => new Date(d.date).getDay() === dayOfWeek
      );

      const avgDemand = daySales.length > 0
        ? daySales.reduce((sum, d) => sum + d.quantity, 0) / daySales.length
        : 0;

      // Calculate confidence based on variance
      const variance = daySales.length > 0
        ? this.calculateVariance(daySales.map(d => d.quantity))
        : 0;

      const confidence = variance > 0
        ? Math.max(0, 1 - (variance / avgDemand))
        : 0.5;

      forecast.push({
        date,
        predictedDemand: Math.round(avgDemand),
        confidence,
      });
    }

    return {
      productId: params.productId,
      variantId: params.variantId,
      forecast,
    };
  }

  /**
   * Get historical sales
   */
  private async getHistoricalSales(
    productId: string,
    variantId: string | undefined,
    days: number
  ): Promise<Array<{ date: Date; quantity: number }>> {
    const startDate = new Date(Date.now() - days * 24 * 60 * 60 * 1000);

    const movements = await this.prisma.inventoryMovement.findMany({
      where: {
        type: MovementType.SALE,
        inventory: {
          productId,
          variantId: variantId || null,
        },
        createdAt: { gte: startDate },
      },
      orderBy: { createdAt: 'asc' },
    });

    // Group by day
    const grouped = new Map<string, number>();

    for (const movement of movements) {
      const dateKey = movement.createdAt.toISOString().split('T')[0];
      grouped.set(dateKey, (grouped.get(dateKey) || 0) + Math.abs(movement.quantity));
    }

    return Array.from(grouped.entries()).map(([date, quantity]) => ({
      date: new Date(date),
      quantity,
    }));
  }

  /**
   * Calculate variance
   */
  private calculateVariance(values: number[]): number {
    if (values.length === 0) return 0;

    const mean = values.reduce((sum, v) => sum + v, 0) / values.length;
    const squaredDiffs = values.map(v => Math.pow(v - mean, 2));

    return squaredDiffs.reduce((sum, v) => sum + v, 0) / values.length;
  }
}
```

---

## Optimistic Locking

### Optimistic Lock Manager

```typescript
class OptimisticLockManager {
  /**
   * Update with retry
   */
  async updateWithRetry<T>(
    updateFn: (version: number) => Promise<T>,
    maxRetries: number = 3
  ): Promise<T> {
    let version = 0;

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        return await updateFn(version);
      } catch (error: any) {
        if (error.code === 'P2034' && attempt < maxRetries) {
          // Optimistic lock conflict, retry
          console.log(`Optimistic lock conflict, retrying attempt ${attempt + 1}`);
          await new Promise(resolve => setTimeout(resolve, 100 * attempt));
          continue;
        }
        throw error;
      }
    }

    throw new Error('Max retries exceeded');
  }

  /**
   * Update inventory with optimistic locking
   */
  async updateInventoryWithLock(params: {
    inventoryId: string;
    quantityChange: number;
  }): Promise<Inventory> {
    return await this.updateWithRetry(async (version) => {
      const inventory = await prisma.inventory.findUnique({
        where: { id: params.inventoryId },
      });

      if (!inventory) {
        throw new Error('Inventory not found');
      }

      const newQuantity = inventory.quantity + params.quantityChange;

      if (newQuantity < 0) {
        throw new Error('Insufficient stock');
      }

      return await prisma.inventory.update({
        where: {
          id: params.inventoryId,
          version: inventory.version,
        },
        data: {
          quantity: newQuantity,
          version: { increment: 1 },
        },
      });
    });
  }
}
```

---

## Best Practices

### Inventory Best Practices

```typescript
// 1. Always use transactions for stock updates
async function updateStockWithTransaction(
  productId: string,
  quantity: number
): Promise<void> {
  await prisma.$transaction(async (tx) => {
    await tx.inventory.update({ ... });
    await tx.inventoryMovement.create({ ... });
  });
}

// 2. Implement proper reservation expiration
async function checkExpiredReservations(): Promise<void> {
  const expired = await prisma.inventoryReservation.findMany({
    where: {
      status: ReservationStatus.RESERVED,
      expiresAt: { lt: new Date() },
    },
  });

  for (const reservation of expired) {
    await releaseReservation(reservation.id);
  }
}

// 3. Use FIFO for stock allocation
async function allocateStock(orderItems: OrderItem[]): Promise<void> {
  for (const item of orderItems) {
    const inventory = await prisma.inventory.findFirst({
      where: {
        productId: item.productId,
        variantId: item.variantId,
        quantity: { gte: item.quantity },
      },
      orderBy: { createdAt: 'asc' },
    });

    if (!inventory) {
      throw new Error('Insufficient stock');
    }

    await reserveStock(inventory.id, item.quantity);
  }
}

// 4. Implement cycle counting
async function performCycleCount(
  productId: string,
  warehouseId: string
): Promise<void> {
  const inventory = await prisma.inventory.findFirst({
    where: { productId, warehouseId },
  });

  if (!inventory) return;

  const countedQuantity = await physicalCount(productId, warehouseId);
  const difference = countedQuantity - inventory.quantity;

  if (difference !== 0) {
    await createAdjustment({
      productId,
      warehouseId,
      quantity: difference,
      reason: 'Cycle count adjustment',
    });
  }
}

// 5. Set up proper low stock thresholds
async function setLowStockThreshold(
  productId: string,
  threshold: number
): Promise<void> {
  await prisma.product.update({
    where: { id: productId },
    data: { lowStockThreshold: threshold },
  });
}
```

---

---

## Quick Start

### Stock Management

```typescript
async function updateStock(productId: string, quantity: number) {
  await db.$transaction(async (tx) => {
    // Check current stock
    const product = await tx.products.findUnique({
      where: { id: productId }
    })
    
    if (product.stock + quantity < 0) {
      throw new Error('Insufficient stock')
    }
    
    // Update stock
    await tx.products.update({
      where: { id: productId },
      data: { stock: { increment: quantity } }
    })
    
    // Log movement
    await tx.stockMovements.create({
      data: {
        productId,
        quantity,
        type: quantity > 0 ? 'in' : 'out',
        reason: 'manual-adjustment'
      }
    })
  })
}
```

### Stock Reservation

```typescript
async function reserveStock(productId: string, quantity: number, orderId: string) {
  await db.$transaction(async (tx) => {
    const product = await tx.products.findUnique({
      where: { id: productId }
    })
    
    const available = product.stock - product.reserved
    
    if (available < quantity) {
      throw new Error('Insufficient available stock')
    }
    
    await tx.products.update({
      where: { id: productId },
      data: { reserved: { increment: quantity } }
    })
    
    await tx.stockReservations.create({
      data: { productId, quantity, orderId, expiresAt: addHours(new Date(), 24) }
    })
  })
}
```

---

## Production Checklist

- [ ] **Stock Tracking**: Real-time stock tracking
- [ ] **Reservations**: Stock reservation system
- [ ] **Multi-Warehouse**: Support multiple warehouses
- [ ] **Stock Movements**: Log all stock movements
- [ ] **Low Stock Alerts**: Alert on low stock
- [ ] **Forecasting**: Stock forecasting
- [ ] **Adjustments**: Manual stock adjustments
- [ ] **Synchronization**: Sync with external systems
- [ ] **Reports**: Inventory reports
- [ ] **Validation**: Validate stock operations
- [ ] **Audit Trail**: Complete audit trail
- [ ] **Performance**: Optimize for high volume

---

## Anti-patterns

### ❌ Don't: Race Conditions

```typescript
// ❌ Bad - Race condition
const product = await getProduct(productId)
if (product.stock >= quantity) {
  await updateStock(productId, -quantity)  // Another order might have taken stock!
}
```

```typescript
// ✅ Good - Transaction with lock
await db.$transaction(async (tx) => {
  const product = await tx.products.findUnique({
    where: { id: productId },
    lock: { mode: 'update' }  // Lock row
  })
  
  if (product.stock >= quantity) {
    await tx.products.update({
      where: { id: productId },
      data: { stock: { decrement: quantity } }
    })
  }
})
```

### ❌ Don't: No Reservations

```typescript
// ❌ Bad - No reservation
// Stock might be sold to multiple orders!
```

```typescript
// ✅ Good - Reserve stock
await reserveStock(productId, quantity, orderId)
// Stock reserved, safe to proceed with order
```

---

## Integration Points

- **Order Management** (`30-ecommerce/order-management/`) - Order processing
- **Shopping Cart** (`30-ecommerce/shopping-cart/`) - Cart validation
- **Database Transactions** (`04-database/database-transactions/`) - Transaction patterns

---

## Further Reading

- [Shopify Inventory API](https://shopify.dev/api/admin-graphql/latest/objects/InventoryLevel)
- [WooCommerce Inventory](https://woocommerce.github.io/woocommerce-rest-api-docs/#products)
- [Magento Inventory Management](https://devdocs.magento.com/guides/v2.4/inventory/)
- [BigCommerce Inventory API](https://developer.bigcommerce.com/api-reference/catalog/catalog-api/inventory)
