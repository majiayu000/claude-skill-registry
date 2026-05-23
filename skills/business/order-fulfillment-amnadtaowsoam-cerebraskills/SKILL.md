---
name: Order Fulfillment Workflow
description: Managing the complete order fulfillment process from picking and packing to shipping and returns processing, including warehouse management, 3PL integration, and fulfillment tracking.
---

# Order Fulfillment Workflow

> **Current Level:** Intermediate  
> **Domain:** E-commerce / Operations

---

## Overview

Order fulfillment manages the complete process from picking and packing to shipping and returns processing. Effective fulfillment systems include warehouse management, batch processing, quality control, shipping label generation, and integration with 3PL providers.

---

## Core Concepts

### Table of Contents

1. [Fulfillment Workflow](#fulfillment-workflow)
2. [Warehouse Management](#warehouse-management)
3. [Pick, Pack, Ship Process](#pick-pack-ship-process)
4. [Batch Processing](#batch-processing)
5. [Packing Slips](#packing-slips)
6. [Shipping Labels](#shipping-labels)
7. [Quality Control](#quality-control)
8. [Returns Processing](#returns-processing)
9. [3PL Integration](#3pl-integration)
10. [Fulfillment Tracking](#fulfillment-tracking)
11. [SLA Management](#sla-management)
12. [Analytics](#analytics)
13. [Best Practices](#best-practices)

---

## Fulfillment Workflow

### Fulfillment States

```typescript
enum FulfillmentStatus {
  PENDING = 'pending',
  PICKING = 'picking',
  PICKED = 'picked',
  PACKING = 'packing',
  PACKED = 'packed',
  SHIPPED = 'shipped',
  DELIVERED = 'delivered',
  FAILED = 'failed',
  CANCELLED = 'cancelled',
}

enum FulfillmentPriority {
  URGENT = 'urgent',      // < 24 hours
  HIGH = 'high',         // < 48 hours
  NORMAL = 'normal',      // < 72 hours
  LOW = 'low',           // < 5 days
}
```

### Fulfillment Workflow

```typescript
class FulfillmentWorkflow {
  constructor(private prisma: PrismaClient) {}

  /**
   * Start fulfillment
   */
  async startFulfillment(orderId: string): Promise<Fulfillment> {
    const order = await this.prisma.order.findUnique({
      where: { id: orderId },
      include: {
        items: {
          include: {
            product: true,
            variant: true,
          },
        },
        shippingAddress: true,
      },
    });

    if (!order) {
      throw new Error('Order not found');
    }

    if (order.status !== OrderStatus.PAID) {
      throw new Error('Order must be paid before fulfillment');
    }

    // Create fulfillment
    const fulfillment = await this.prisma.$transaction(async (tx) => {
      const fulfillment = await tx.fulfillment.create({
        data: {
          orderId,
          status: FulfillmentStatus.PENDING,
          priority: this.calculatePriority(order),
        },
      });

      // Create fulfillment items
      for (const item of order.items) {
        await tx.fulfillmentItem.create({
          data: {
            fulfillmentId: fulfillment.id,
            orderItemId: item.id,
            quantity: item.quantity,
            status: 'pending',
          },
        });
      }

      // Update order status
      await tx.order.update({
        where: { id: orderId },
        data: {
          status: OrderStatus.PROCESSING,
          fulfillmentStatus: FulfillmentStatus.PENDING,
        },
      });

      return fulfillment;
    });

    return fulfillment;
  }

  /**
   * Calculate priority
   */
  private calculatePriority(order: any): FulfillmentPriority {
    // Check for urgent items
    const hasUrgentItem = order.items.some((item: any) => {
      const product = item.product;
      return product?.isUrgent || false;
    });

    if (hasUrgentItem) {
      return FulfillmentPriority.URGENT;
    }

    // Check for expedited shipping
    if (order.shippingMethod === 'express') {
      return FulfillmentPriority.HIGH;
    }

    // Check order age
    const hoursSinceOrder = (Date.now() - order.createdAt.getTime()) / (1000 * 60 * 60);

    if (hoursSinceOrder > 48) {
      return FulfillmentPriority.URGENT;
    }

    if (hoursSinceOrder > 24) {
      return FulfillmentPriority.HIGH;
    }

    return FulfillmentPriority.NORMAL;
  }
}
```

---

## Warehouse Management

### Warehouse Manager

```typescript
class WarehouseManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get warehouse layout
   */
  async getWarehouseLayout(warehouseId: string): Promise<WarehouseLayout> {
    const warehouse = await this.prisma.warehouse.findUnique({
      where: { id: warehouseId },
      include: {
        zones: {
          include: {
            bins: {
              include: {
                inventory: {
                  include: {
                    product: true,
                    variant: true,
                  },
                },
              },
            },
          },
        },
      },
    });

    if (!warehouse) {
      throw new Error('Warehouse not found');
    }

    return {
      id: warehouse.id,
      name: warehouse.name,
      address: warehouse.address,
      zones: warehouse.zones.map(zone => ({
        id: zone.id,
        name: zone.name,
        type: zone.type,
        bins: zone.bins.map(bin => ({
          id: bin.id,
          name: bin.name,
          location: bin.location,
          capacity: bin.capacity,
          inventory: bin.inventory,
        })),
      })),
    };
  }

  /**
   * Find item location
   */
  async findItemLocation(params: {
    productId: string;
    variantId?: string;
    warehouseId: string;
  }): Promise<BinLocation | null> {
    const bin = await this.prisma.bin.findFirst({
      where: {
        warehouseId: params.warehouseId,
        inventory: {
          some: {
            productId: params.productId,
            variantId: params.variantId || null,
            quantity: { gt: 0 },
          },
        },
      },
      include: {
        inventory: {
          include: {
            product: true,
            variant: true,
          },
        },
      },
    });

    if (!bin) {
      return null;
    }

    return {
      id: bin.id,
      name: bin.name,
      location: bin.location,
      zoneId: bin.zoneId,
    };
  }

  /**
   * Optimize picking route
   */
  async optimizePickingRoute(fulfillmentId: string): Promise<PickingRoute> {
    const fulfillment = await this.prisma.fulfillment.findUnique({
      where: { id: fulfillmentId },
      include: {
        items: {
          include: {
            orderItem: {
              include: {
                product: true,
                variant: true,
              },
            },
          },
        },
      },
    });

    if (!fulfillment) {
      throw new Error('Fulfillment not found');
    }

    // Get locations for all items
    const locations: Array<{
      binId: string;
      binName: string;
      location: string;
      productId: string;
      variantId?: string;
      quantity: number;
    }> = [];

    for (const item of fulfillment.items) {
      const location = await this.findItemLocation({
        productId: item.orderItem.productId,
        variantId: item.orderItem.variantId,
        warehouseId: fulfillment.warehouseId,
      });

      if (location) {
        locations.push({
          binId: location.id,
          binName: location.name,
          location: location.location,
          productId: item.orderItem.productId,
          variantId: item.orderItem.variantId,
          quantity: item.quantity,
        });
      }
    }

    // Sort by location (simple nearest neighbor)
    const sorted = this.sortByLocation(locations);

    return {
      fulfillmentId,
      items: sorted,
      estimatedTime: this.estimatePickingTime(sorted),
    };
  }

  /**
   * Sort by location
   */
  private sortByLocation(locations: any[]): any[] {
    // Simple sorting by zone and bin name
    return locations.sort((a, b) => {
      if (a.location !== b.location) {
        return a.localeCompare(b.location);
      }
      return a.binName.localeCompare(b.binName);
    });
  }

  /**
   * Estimate picking time
   */
  private estimatePickingTime(locations: any[]): number {
    // Estimate 30 seconds per item + 1 minute per zone change
    let time = locations.length * 0.5; // 30 seconds per item

    for (let i = 1; i < locations.length; i++) {
      if (locations[i].location !== locations[i - 1].location) {
        time += 1; // 1 minute per zone change
      }
    }

    return time; // in minutes
  }
}
```

---

## Pick, Pack, Ship Process

### Pick Pack Ship Manager

```typescript
class PickPackShipManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Start picking
   */
  async startPicking(fulfillmentId: string): Promise<void> {
    await this.prisma.fulfillment.update({
      where: { id: fulfillmentId },
      data: {
        status: FulfillmentStatus.PICKING,
        pickingStartedAt: new Date(),
      },
    });
  }

  /**
   * Complete picking
   */
  async completePicking(params: {
    fulfillmentId: string;
    pickerId: string;
    notes?: string;
  }): Promise<void> {
    await this.prisma.$transaction(async (tx) => {
      // Update fulfillment
      await tx.fulfillment.update({
        where: { id: params.fulfillmentId },
        data: {
          status: FulfillmentStatus.PICKED,
          pickingCompletedAt: new Date(),
          pickerId: params.pickerId,
          pickingNotes: params.notes,
        },
      });

      // Update fulfillment items
      await tx.fulfillmentItem.updateMany({
        where: {
          fulfillmentId: params.fulfillmentId,
          status: 'pending',
        },
        data: {
          status: 'picked',
          pickedAt: new Date(),
          pickedBy: params.pickerId,
        },
      });
    });
  }

  /**
   * Start packing
   */
  async startPacking(fulfillmentId: string): Promise<void> {
    await this.prisma.fulfillment.update({
      where: { id: fulfillmentId },
      data: {
        status: FulfillmentStatus.PACKING,
        packingStartedAt: new Date(),
      },
    });
  }

  /**
   * Complete packing
   */
  async completePacking(params: {
    fulfillmentId: string;
    packerId: string;
    packageType: string;
    packageWeight: number;
    packageDimensions: {
      length: number;
      width: number;
      height: number;
    };
    trackingNumber?: string;
    carrier?: string;
    notes?: string;
  }): Promise<void> {
    await this.prisma.$transaction(async (tx) => {
      // Update fulfillment
      await tx.fulfillment.update({
        where: { id: params.fulfillmentId },
        data: {
          status: FulfillmentStatus.PACKED,
          packingCompletedAt: new Date(),
          packerId: params.packerId,
          packageType: params.packageType,
          packageWeight: params.packageWeight,
          packageDimensions: params.packageDimensions,
          trackingNumber: params.trackingNumber,
          carrier: params.carrier,
          packingNotes: params.notes,
        },
      });

      // Update order status
      await tx.order.updateMany({
        where: {
          fulfillments: {
            some: { id: params.fulfillmentId },
          },
        },
        data: {
          fulfillmentStatus: FulfillmentStatus.PACKED,
        },
      });
    });
  }

  /**
   * Ship fulfillment
   */
  async shipFulfillment(fulfillmentId: string): Promise<void> {
    const fulfillment = await this.prisma.fulfillment.findUnique({
      where: { id: fulfillmentId },
      include: { order: true },
    });

    if (!fulfillment) {
      throw new Error('Fulfillment not found');
    }

    if (!fulfillment.trackingNumber) {
      throw new Error('Tracking number required for shipping');
    }

    await this.prisma.$transaction(async (tx) => {
      // Update fulfillment
      await tx.fulfillment.update({
        where: { id: fulfillmentId },
        data: {
          status: FulfillmentStatus.SHIPPED,
          shippedAt: new Date(),
        },
      });

      // Update order status
      if (fulfillment.order) {
        await tx.order.update({
          where: { id: fulfillment.orderId },
          data: {
            status: OrderStatus.SHIPPED,
            fulfillmentStatus: FulfillmentStatus.SHIPPED,
            shippedAt: new Date(),
          },
        });
      }

      // Send shipping notification
      await this.sendShippingNotification(fulfillment);
    });
  }

  /**
   * Send shipping notification
   */
  private async sendShippingNotification(fulfillment: any): Promise<void> {
    const order = await this.prisma.order.findUnique({
      where: { id: fulfillment.orderId },
      include: { user: true },
    });

    if (!order) return;

    await emailService.send({
      to: order.customerEmail,
      subject: `Your order has been shipped!`,
      templateId: 'order-shipped',
      dynamicTemplateData: {
        orderNumber: order.orderNumber,
        trackingNumber: fulfillment.trackingNumber,
        carrier: fulfillment.carrier,
        trackingUrl: this.getTrackingUrl(fulfillment.trackingNumber, fulfillment.carrier),
      },
    });
  }

  /**
   * Get tracking URL
   */
  private getTrackingUrl(trackingNumber: string, carrier?: string): string {
    const trackingUrls: Record<string, string> = {
      'thailand_post': `https://track.thailandpost.co.th/?trackNumber=${trackingNumber}`,
      'kerry_express': `https://th.kerryexpress.com/track/v2/?track=${trackingNumber}`,
      'flash_express': `https://www.flashexpress.co.th/tracking/?id=${trackingNumber}`,
      'j_t_express': `https://www.jtexpress.co.th/track/trace?billcode=${trackingNumber}`,
      'dhl': `https://www.dhl.com/en-us/tracking.html?tracking-id=${trackingNumber}`,
      'fedex': `https://www.fedex.com/apps/fedextrack/?tracknumbers=${trackingNumber}`,
    };

    return trackingUrls[carrier || ''] || '#';
  }
}
```

---

## Batch Processing

### Batch Manager

```typescript
class BatchManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create fulfillment batch
   */
  async createBatch(params: {
    name: string;
    fulfillmentIds: string[];
    pickerId?: string;
  }): Promise<FulfillmentBatch> {
    return await this.prisma.$transaction(async (tx) => {
      const batch = await tx.fulfillmentBatch.create({
        data: {
          name: params.name,
          pickerId: params.pickerId,
          status: 'pending',
        },
      });

      // Add fulfillments to batch
      for (const fulfillmentId of params.fulfillmentIds) {
        await tx.fulfillment.update({
          where: { id: fulfillmentId },
          data: { batchId: batch.id },
        });
      }

      return batch;
    });
  }

  /**
   * Get optimal batch
   */
  async getOptimalBatch(params: {
    warehouseId: string;
    maxItems?: number;
  }): Promise<FulfillmentBatch> {
    // Get pending fulfillments
    const fulfillments = await this.prisma.fulfillment.findMany({
      where: {
        status: FulfillmentStatus.PENDING,
        warehouseId: params.warehouseId,
        batchId: null,
      },
      include: {
        items: {
          include: {
            orderItem: {
              include: {
                product: true,
                variant: true,
              },
            },
          },
        },
      },
      orderBy: { priority: 'desc' },
      take: params.maxItems || 50,
    });

    // Group by zone
    const zoneGroups = this.groupByZone(fulfillments);

    // Find optimal batch (most items in fewest zones)
    let optimalBatch: string[] = [];
    let minZones = Infinity;

    for (const [zone, items] of Object.entries(zoneGroups)) {
      if (items.length < minZones) {
        minZones = items.length;
        optimalBatch = items.map(f => f.id);
      }
    }

    // Create batch
    return await this.createBatch({
      name: `Batch ${Date.now()}`,
      fulfillmentIds: optimalBatch,
    });
  }

  /**
   * Group by zone
   */
  private groupByZone(fulfillments: any[]): Record<string, any[]> {
    const groups: Record<string, any[]> = {};

    for (const fulfillment of fulfillments) {
      for (const item of fulfillment.items) {
        const location = await this.findItemLocation({
          productId: item.orderItem.productId,
          variantId: item.orderItem.variantId,
          warehouseId: fulfillment.warehouseId,
        });

        if (location) {
          const zone = location.location.split('-')[0];
          if (!groups[zone]) {
            groups[zone] = [];
          }
          if (!groups[zone].find((f: any) => f.id === fulfillment.id)) {
            groups[zone].push(fulfillment);
          }
        }
      }
    }

    return groups;
  }

  /**
   * Start batch picking
   */
  async startBatchPicking(batchId: string, pickerId: string): Promise<void> {
    await this.prisma.fulfillmentBatch.update({
      where: { id: batchId },
      data: {
        status: 'picking',
        pickerId,
        startedAt: new Date(),
      },
    });

    // Start picking for all fulfillments in batch
    const fulfillments = await this.prisma.fulfillment.findMany({
      where: { batchId },
    });

    for (const fulfillment of fulfillments) {
      await this.prisma.fulfillment.update({
        where: { id: fulfillment.id },
        data: {
          status: FulfillmentStatus.PICKING,
          pickingStartedAt: new Date(),
        },
      });
    }
  }

  /**
   * Complete batch picking
   */
  async completeBatchPicking(batchId: string): Promise<void> {
    await this.prisma.$transaction(async (tx) => {
      // Update batch
      await tx.fulfillmentBatch.update({
        where: { id: batchId },
        data: {
          status: 'picked',
          completedAt: new Date(),
        },
      });

      // Update all fulfillments in batch
      await tx.fulfillment.updateMany({
        where: { batchId },
        data: {
          status: FulfillmentStatus.PICKED,
          pickingCompletedAt: new Date(),
        },
      });
    });
  }

  /**
   * Find item location
   */
  private async findItemLocation(params: {
    productId: string;
    variantId?: string;
    warehouseId: string;
  }): Promise<any> {
    const bin = await this.prisma.bin.findFirst({
      where: {
        warehouseId: params.warehouseId,
        inventory: {
          some: {
            productId: params.productId,
            variantId: params.variantId || null,
            quantity: { gt: 0 },
          },
        },
      },
    });

    return bin;
  }
}
```

---

## Packing Slips

### Packing Slip Generator

```typescript
class PackingSlipGenerator {
  /**
   * Generate packing slip
   */
  async generatePackingSlip(fulfillmentId: string): Promise<Buffer> {
    const fulfillment = await this.prisma.fulfillment.findUnique({
      where: { id: fulfillmentId },
      include: {
        items: {
          include: {
            orderItem: {
              include: {
                product: true,
                variant: true,
              },
            },
          },
        },
        order: {
          include: {
            user: true,
            shippingAddress: true,
            billingAddress: true,
          },
        },
      },
    });

    if (!fulfillment) {
      throw new Error('Fulfillment not found');
    }

    // Generate HTML
    const html = this.generateHTML(fulfillment);

    // Convert to PDF
    const pdf = await this.convertToPDF(html);

    return pdf;
  }

  /**
   * Generate HTML
   */
  private generateHTML(fulfillment: any): string {
    const order = fulfillment.order;

    return `
      <!DOCTYPE html>
      <html>
      <head>
        <title>Packing Slip - ${order.orderNumber}</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 20px; }
          .header { border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 20px; }
          .section { margin-bottom: 20px; }
          .item { padding: 10px 0; border-bottom: 1px solid #ccc; }
          .total { font-weight: bold; font-size: 18px; margin-top: 20px; }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>Packing Slip</h1>
          <p>Order Number: ${order.orderNumber}</p>
          <p>Date: ${new Date().toLocaleDateString()}</p>
        </div>

        <div class="section">
          <h2>Shipping Address</h2>
          <p>${order.shippingAddress.firstName} ${order.shippingAddress.lastName}</p>
          <p>${order.shippingAddress.address1}</p>
          ${order.shippingAddress.address2 ? `<p>${order.shippingAddress.address2}</p>` : ''}
          <p>${order.shippingAddress.city}, ${order.shippingAddress.state} ${order.shippingAddress.postalCode}</p>
          <p>${order.shippingAddress.country}</p>
          <p>Phone: ${order.shippingAddress.phone}</p>
        </div>

        <div class="section">
          <h2>Items</h2>
          ${fulfillment.items.map(item => `
            <div class="item">
              <p><strong>${item.orderItem.product.name}</strong></p>
              ${item.orderItem.variant ? `<p>Variant: ${item.orderItem.variant.name}</p>` : ''}
              <p>SKU: ${item.orderItem.product.sku}</p>
              <p>Quantity: ${item.quantity}</p>
            </div>
          `).join('')}
        </div>

        <div class="total">
          <p>Total Items: ${fulfillment.items.reduce((sum: number, i: any) => sum + i.quantity, 0)}</p>
        </div>
      </body>
      </html>
    `;
  }

  /**
   * Convert to PDF
   */
  private async convertToPDF(html: string): Promise<Buffer> {
    // Implement PDF generation using puppeteer or similar
    return Buffer.from(html);
  }
}
```

---

## Shipping Labels

### Label Generator

```typescript
class LabelGenerator {
  /**
   * Generate shipping label
   */
  async generateLabel(fulfillmentId: string): Promise<{
    labelUrl: string;
    trackingNumber: string;
  }> {
    const fulfillment = await this.prisma.fulfillment.findUnique({
      where: { id: fulfillmentId },
      include: {
        order: {
          include: {
            shippingAddress: true,
          },
        },
        items: {
          include: {
            orderItem: {
              include: {
                product: true,
                variant: true,
              },
            },
          },
        },
      },
    });

    if (!fulfillment) {
      throw new Error('Fulfillment not found');
    }

    // Calculate package details
    const { weight, dimensions } = this.calculatePackageDetails(fulfillment.items);

    // Get warehouse address
    const warehouse = await this.prisma.warehouse.findFirst({
      where: { isDefault: true },
    });

    if (!warehouse) {
      throw new Error('No default warehouse found');
    }

    // Generate label using carrier API
    const labelGenerator = new ShippingLabelGenerator();
    const label = await labelGenerator.generateLabel({
      from: warehouse.address,
      to: fulfillment.order.shippingAddress,
      weight,
      dimensions,
      serviceType: fulfillment.order.shippingMethod,
      referenceNumber: fulfillment.order.orderNumber,
    });

    // Update fulfillment
    await this.prisma.fulfillment.update({
      where: { id: fulfillmentId },
      data: {
        trackingNumber: label.trackingNumber,
        labelUrl: label.labelUrl,
        labelGeneratedAt: new Date(),
      },
    });

    return label;
  }

  /**
   * Calculate package details
   */
  private calculatePackageDetails(items: any[]): {
    weight: number;
    dimensions: {
      length: number;
      width: number;
      height: number;
    };
  } {
    let totalWeight = 0;
    let maxLength = 0;
    let maxWidth = 0;
    let maxHeight = 0;

    for (const item of items) {
      const product = item.orderItem.product;
      const variant = item.orderItem.variant;

      const itemWeight = (variant?.weight || product?.weight || 0) * item.quantity;
      const itemLength = variant?.length || product?.length || 0;
      const itemWidth = variant?.width || product?.width || 0;
      const itemHeight = variant?.height || product?.height || 0;

      totalWeight += itemWeight;
      maxLength = Math.max(maxLength, itemLength);
      maxWidth = Math.max(maxWidth, itemWidth);
      maxHeight = Math.max(maxHeight, itemHeight);
    }

    return {
      weight: totalWeight,
      dimensions: {
        length: maxLength,
        width: maxWidth,
        height: maxHeight,
      },
    };
  }
}
```

---

## Quality Control

### QC Manager

```typescript
class QualityControlManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create QC check
   */
  async createQCCheck(params: {
    fulfillmentId: string;
    inspectorId: string;
    items: Array<{
      fulfillmentItemId: string;
      passed: boolean;
      notes?: string;
    }>;
    overallPassed: boolean;
    notes?: string;
  }): Promise<QualityCheck> {
    return await this.prisma.$transaction(async (tx) => {
      const qc = await tx.qualityCheck.create({
        data: {
          fulfillmentId: params.fulfillmentId,
          inspectorId: params.inspectorId,
          overallPassed: params.overallPassed,
          notes: params.notes,
          checkedAt: new Date(),
        },
      });

      // Create QC items
      for (const item of params.items) {
        await tx.qualityCheckItem.create({
          data: {
            qualityCheckId: qc.id,
            fulfillmentItemId: item.fulfillmentItemId,
            passed: item.passed,
            notes: item.notes,
          },
        });
      }

      // Update fulfillment if failed
      if (!params.overallPassed) {
        await tx.fulfillment.update({
          where: { id: params.fulfillmentId },
          data: {
            status: FulfillmentStatus.FAILED,
            failedAt: new Date(),
            failureReason: 'Quality check failed',
          },
        });
      }

      return qc;
    });
  }

  /**
   * Get QC stats
   */
  async getQCStats(params: {
    startDate: Date;
    endDate: Date;
    inspectorId?: string;
  }): Promise<{
    totalChecks: number;
    passedChecks: number;
    failedChecks: number;
    passRate: number;
  }> {
    const where: any = {
      checkedAt: {
        gte: params.startDate,
        lte: params.endDate,
      },
    };

    if (params.inspectorId) {
      where.inspectorId = params.inspectorId;
    }

    const checks = await this.prisma.qualityCheck.findMany({
      where,
    });

    const passed = checks.filter(c => c.overallPassed).length;
    const failed = checks.length - passed;

    return {
      totalChecks: checks.length,
      passedChecks: passed,
      failedChecks: failed,
      passRate: checks.length > 0 ? (passed / checks.length) * 100 : 0,
    };
  }
}
```

---

## Returns Processing

### Returns Manager

```typescript
class ReturnsManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Process return
   */
  async processReturn(returnId: string): Promise<void> {
    const returnRecord = await this.prisma.return.findUnique({
      where: { id: returnId },
      include: {
        items: {
          include: {
            orderItem: {
              include: {
                product: true,
                variant: true,
              },
            },
          },
        },
      },
    });

    if (!returnRecord) {
      throw new Error('Return not found');
    }

    await this.prisma.$transaction(async (tx) => {
      // Update return status
      await tx.return.update({
        where: { id: returnId },
        data: {
          status: 'processing',
          processedAt: new Date(),
        },
      });

      // Process each item
      for (const item of returnRecord.items) {
        // Restock inventory
        await this.restockItem(tx, item);

        // Update return item status
        await tx.returnItem.update({
          where: { id: item.id },
          data: {
            status: 'processed',
          },
        });
      }

      // Update return status
      await tx.return.update({
        where: { id: returnId },
        data: {
          status: 'completed',
        },
      });
    });
  }

  /**
   * Restock item
   */
  private async restockItem(
    tx: Prisma.TransactionClient,
    returnItem: any
  ): Promise<void> {
    const inventory = await tx.inventory.findFirst({
      where: {
        productId: returnItem.orderItem.productId,
        variantId: returnItem.orderItem.variantId || null,
      },
    });

    if (inventory) {
      await tx.inventory.update({
        where: { id: inventory.id },
        data: {
          quantity: { increment: returnItem.quantity },
        },
      });
    }
  }
}
```

---

## 3PL Integration

### 3PL Manager

```typescript
class ThreePLManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Sync order to 3PL
   */
  async syncOrder(orderId: string): Promise<void> {
    const order = await this.prisma.order.findUnique({
      where: { id: orderId },
      include: {
        items: {
          include: {
            product: true,
            variant: true,
          },
        },
        shippingAddress: true,
      },
    });

    if (!order) {
      throw new Error('Order not found');
    }

    // Send to 3PL
    const threePLService = new ThreePLService();
    const response = await threePLService.createOrder({
      orderId: order.id,
      orderNumber: order.orderNumber,
      items: order.items.map(item => ({
        productId: item.productId,
        variantId: item.variantId,
        sku: item.product.sku,
        quantity: item.quantity,
      })),
      shippingAddress: order.shippingAddress,
      shippingMethod: order.shippingMethod,
    });

    // Save 3PL reference
    await this.prisma.order.update({
      where: { id: orderId },
      data: {
        threePLReference: response.orderId,
        threePLSyncedAt: new Date(),
      },
    });
  }

  /**
   * Sync tracking from 3PL
   */
  async syncTracking(): Promise<void> {
    const orders = await this.prisma.order.findMany({
      where: {
        threePLReference: { not: null },
        status: OrderStatus.PROCESSING,
      },
    });

    const threePLService = new ThreePLService();

    for (const order of orders) {
      const tracking = await threePLService.getTracking(order.threePLReference!);

      if (tracking.shipped) {
        await this.prisma.order.update({
          where: { id: order.id },
          data: {
            status: OrderStatus.SHIPPED,
            shippedAt: tracking.shippedAt,
          },
        });

        // Create fulfillment
        await this.prisma.fulfillment.create({
          data: {
            orderId: order.id,
            status: FulfillmentStatus.SHIPPED,
            trackingNumber: tracking.trackingNumber,
            carrier: tracking.carrier,
            shippedAt: tracking.shippedAt,
          },
        });
      }
    }
  }
}
```

---

## Fulfillment Tracking

### Tracking Manager

```typescript
class FulfillmentTrackingManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get fulfillment status
   */
  async getFulfillmentStatus(fulfillmentId: string): Promise<{
    fulfillment: Fulfillment;
    trackingEvents: TrackingEvent[];
  }> {
    const fulfillment = await this.prisma.fulfillment.findUnique({
      where: { id: fulfillmentId },
      include: {
        items: {
          include: {
            orderItem: {
              include: {
                product: true,
                variant: true,
              },
            },
          },
        },
        order: {
          include: {
            user: true,
            shippingAddress: true,
          },
        },
      },
    });

    if (!fulfillment) {
      throw new Error('Fulfillment not found');
    }

    // Get tracking events from carrier
    let trackingEvents: TrackingEvent[] = [];

    if (fulfillment.trackingNumber) {
      const trackingService = new TrackingService();
      trackingEvents = await trackingService.getTrackingEvents(fulfillment.trackingNumber);
    }

    return {
      fulfillment,
      trackingEvents,
    };
  }

  /**
   * Get fulfillment history
   */
  async getFulfillmentHistory(orderId: string): Promise<Fulfillment[]> {
    return await this.prisma.fulfillment.findMany({
      where: { orderId },
      include: {
        items: {
          include: {
            orderItem: {
              include: {
                product: true,
                variant: true,
              },
            },
          },
        },
      },
      orderBy: { createdAt: 'desc' },
    });
  }
}
```

---

## SLA Management

### SLA Manager

```typescript
class SLAManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Check SLA compliance
   */
  async checkSLACompliance(params: {
    startDate: Date;
    endDate: Date;
  }): Promise<{
    total: number;
    onTime: number;
    late: number;
    complianceRate: number;
    averageFulfillmentTime: number;
  }> {
    const fulfillments = await this.prisma.fulfillment.findMany({
      where: {
        createdAt: {
          gte: params.startDate,
          lte: params.endDate,
        },
        status: FulfillmentStatus.SHIPPED,
      },
    });

    let onTime = 0;
    let late = 0;
    let totalTime = 0;

    for (const fulfillment of fulfillments) {
      const slaHours = this.getSLAHours(fulfillment.priority);
      const fulfillmentHours = fulfillment.shippedAt
        ? (fulfillment.shippedAt.getTime() - fulfillment.createdAt.getTime()) / (1000 * 60 * 60)
        : 0;

      totalTime += fulfillmentHours;

      if (fulfillmentHours <= slaHours) {
        onTime++;
      } else {
        late++;
      }
    }

    return {
      total: fulfillments.length,
      onTime,
      late,
      complianceRate: fulfillments.length > 0 ? (onTime / fulfillments.length) * 100 : 0,
      averageFulfillmentTime: fulfillments.length > 0 ? totalTime / fulfillments.length : 0,
    };
  }

  /**
   * Get SLA hours
   */
  private getSLAHours(priority: FulfillmentPriority): number {
    switch (priority) {
      case FulfillmentPriority.URGENT:
        return 24;
      case FulfillmentPriority.HIGH:
        return 48;
      case FulfillmentPriority.NORMAL:
        return 72;
      case FulfillmentPriority.LOW:
        return 120;
      default:
        return 72;
    }
  }

  /**
   * Get SLA breaches
   */
  async getSLABreaches(params: {
    startDate: Date;
    endDate: Date;
  }): Promise<Fulfillment[]> {
    const fulfillments = await this.prisma.fulfillment.findMany({
      where: {
        createdAt: {
          gte: params.startDate,
          lte: params.endDate,
        },
        status: FulfillmentStatus.SHIPPED,
      },
    });

    const breaches: Fulfillment[] = [];

    for (const fulfillment of fulfillments) {
      const slaHours = this.getSLAHours(fulfillment.priority);
      const fulfillmentHours = fulfillment.shippedAt
        ? (fulfillment.shippedAt.getTime() - fulfillment.createdAt.getTime()) / (1000 * 60 * 60)
        : 0;

      if (fulfillmentHours > slaHours) {
        breaches.push(fulfillment);
      }
    }

    return breaches;
  }
}
```

---

## Analytics

### Fulfillment Analytics

```typescript
class FulfillmentAnalytics {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get fulfillment metrics
   */
  async getMetrics(params: {
    startDate: Date;
    endDate: Date;
  }): Promise<{
    totalFulfillments: number;
    shipped: number;
    pending: number;
    averageFulfillmentTime: number;
    averagePickingTime: number;
    averagePackingTime: number;
    topPickers: Array<{
      pickerId: string;
      pickerName: string;
      fulfillments: number;
      averageTime: number;
    }>;
  }> {
    const fulfillments = await this.prisma.fulfillment.findMany({
      where: {
        createdAt: {
          gte: params.startDate,
          lte: params.endDate,
        },
      },
      include: {
        picker: true,
      },
    });

    const shipped = fulfillments.filter(f => f.status === FulfillmentStatus.SHIPPED).length;
    const pending = fulfillments.filter(f => f.status === FulfillmentStatus.PENDING).length;

    // Calculate average times
    const shippedFulfillments = fulfillments.filter(f => f.status === FulfillmentStatus.SHIPPED);

    const averageFulfillmentTime = shippedFulfillments.length > 0
      ? shippedFulfillments.reduce((sum, f) => {
          return sum + (f.shippedAt!.getTime() - f.createdAt.getTime()) / (1000 * 60);
        }, 0) / shippedFulfillments.length
      : 0;

    const averagePickingTime = shippedFulfillments.length > 0
      ? shippedFulfillments.reduce((sum, f) => {
          return sum + (f.pickingCompletedAt!.getTime() - f.pickingStartedAt!.getTime()) / (1000 * 60);
        }, 0) / shippedFulfillments.length
      : 0;

    const averagePackingTime = shippedFulfillments.length > 0
      ? shippedFulfillments.reduce((sum, f) => {
          return sum + (f.packingCompletedAt!.getTime() - f.packingStartedAt!.getTime()) / (1000 * 60);
        }, 0) / shippedFulfillments.length
      : 0;

    // Top pickers
    const pickerStats = new Map<string, { count: number; totalTime: number }>();

    for (const fulfillment of shippedFulfillments) {
      if (fulfillment.pickerId) {
        const stats = pickerStats.get(fulfillment.pickerId) || { count: 0, totalTime: 0 };
        stats.count++;
        stats.totalTime += fulfillment.pickingCompletedAt!.getTime() - fulfillment.pickingStartedAt!.getTime();
        pickerStats.set(fulfillment.pickerId, stats);
      }
    }

    const topPickers = Array.from(pickerStats.entries())
      .map(([pickerId, stats]) => ({
        pickerId,
        pickerName: fulfillments.find(f => f.pickerId === pickerId)?.picker?.name || 'Unknown',
        fulfillments: stats.count,
        averageTime: stats.totalTime / stats.count / (1000 * 60),
      }))
      .sort((a, b) => b.fulfillments - a.fulfillments)
      .slice(0, 10);

    return {
      totalFulfillments: fulfillments.length,
      shipped,
      pending,
      averageFulfillmentTime,
      averagePickingTime,
      averagePackingTime,
      topPickers,
    };
  }
}
```

---

## Best Practices

### Fulfillment Best Practices

```typescript
// 1. Always validate before fulfillment
async function validateBeforeFulfillment(orderId: string): Promise<boolean> {
  const order = await prisma.order.findUnique({
    where: { id: orderId },
    include: { items: true },
  });

  if (!order) {
    throw new Error('Order not found');
  }

  // Check payment status
  if (order.status !== OrderStatus.PAID) {
    throw new Error('Order must be paid');
  }

  // Check inventory
  for (const item of order.items) {
    const stock = await getAvailableStock(item.productId, item.variantId);
    if (stock < item.quantity) {
      throw new Error('Insufficient stock');
    }
  }

  return true;
}

// 2. Use batch processing for efficiency
async function processBatch(fulfillmentIds: string[]): Promise<void> {
  const batchManager = new BatchManager(prisma);

  const batch = await batchManager.createBatch({
    name: `Batch ${Date.now()}`,
    fulfillmentIds,
  });

  await batchManager.startBatchPicking(batch.id, 'picker-id');
}

// 3. Implement proper QC checks
async function performQCCheck(fulfillmentId: string): Promise<void> {
  const qcManager = new QualityControlManager(prisma);

  const qc = await qcManager.createQCCheck({
    fulfillmentId,
    inspectorId: 'inspector-id',
    items: [],
    overallPassed: true,
  });

  if (!qc.overallPassed) {
    // Handle failed QC
    await handleFailedQC(fulfillmentId);
  }
}

// 4. Track fulfillment metrics
async function trackFulfillmentMetrics(fulfillmentId: string): Promise<void> {
  const fulfillment = await prisma.fulfillment.findUnique({
    where: { id: fulfillmentId },
  });

  if (!fulfillment) return;

  const metrics = {
    fulfillmentId,
    pickingTime: fulfillment.pickingCompletedAt && fulfillment.pickingStartedAt
      ? fulfillment.pickingCompletedAt.getTime() - fulfillment.pickingStartedAt.getTime()
      : null,
    packingTime: fulfillment.packingCompletedAt && fulfillment.packingStartedAt
      ? fulfillment.packingCompletedAt.getTime() - fulfillment.packingStartedAt.getTime()
      : null,
    totalFulfillmentTime: fulfillment.shippedAt && fulfillment.createdAt
      ? fulfillment.shippedAt.getTime() - fulfillment.createdAt.getTime()
      : null,
  };

  // Send to analytics
  await sendToAnalytics(metrics);
}

// 5. Implement proper error handling
async function handleFulfillmentError(
  fulfillmentId: string,
  error: Error
): Promise<void> {
  await prisma.fulfillment.update({
    where: { id: fulfillmentId },
    data: {
      status: FulfillmentStatus.FAILED,
      failureReason: error.message,
      failedAt: new Date(),
    },
  });

  // Notify team
  await notifyTeam({
    type: 'fulfillment_error',
    fulfillmentId,
    error: error.message,
  });
}
```

---

---

## Quick Start

### Fulfillment Workflow

```typescript
interface Fulfillment {
  id: string
  orderId: string
  status: 'pending' | 'picking' | 'packing' | 'shipped' | 'delivered'
  warehouseId: string
  trackingNumber?: string
  shippedAt?: Date
}

async function processFulfillment(orderId: string) {
  const order = await getOrder(orderId)
  
  // 1. Create fulfillment
  const fulfillment = await db.fulfillments.create({
    data: {
      orderId,
      status: 'pending',
      warehouseId: selectWarehouse(order)
    }
  })
  
  // 2. Generate pick list
  await generatePickList(fulfillment.id)
  
  // 3. Update status
  await updateFulfillmentStatus(fulfillment.id, 'picking')
}
```

---

## Production Checklist

- [ ] **Workflow**: Complete fulfillment workflow
- [ ] **Warehouse Management**: Multi-warehouse support
- [ ] **Pick List**: Generate pick lists
- [ ] **Packing**: Packing slip generation
- [ ] **Shipping Labels**: Shipping label generation
- [ ] **Quality Control**: QC checkpoints
- [ ] **Tracking**: Order tracking integration
- [ ] **3PL Integration**: Third-party logistics integration
- [ ] **SLA Management**: Fulfillment SLA tracking
- [ ] **Returns**: Returns processing
- [ ] **Analytics**: Fulfillment analytics
- [ ] **Documentation**: Document fulfillment process

---

## Anti-patterns

### ❌ Don't: No Status Tracking

```typescript
// ❌ Bad - No status tracking
await shipOrder(orderId)
// Status unknown!
```

```typescript
// ✅ Good - Status tracking
await updateFulfillmentStatus(fulfillmentId, 'shipped')
await updateOrderStatus(orderId, 'shipped')
await sendTrackingEmail(orderId)
```

### ❌ Don't: No Quality Control

```markdown
# ❌ Bad - Ship without QC
Pick → Pack → Ship
# No quality check!
```

```markdown
# ✅ Good - QC checkpoints
Pick → QC Check → Pack → QC Check → Ship
```

---

## Integration Points

- **Order Management** (`30-ecommerce/order-management/`) - Order processing
- **Inventory Management** (`30-ecommerce/inventory-management/`) - Stock management
- **Shipping Integration** (`30-ecommerce/shipping-integration/`) - Shipping providers

---

## Further Reading

- [Shopify Fulfillment](https://shopify.dev/api/admin-graphql/latest/objects/Fulfillment)
- [WooCommerce Orders](https://woocommerce.github.io/woocommerce-rest-api-docs/#orders)
- [Magento 2 Order Management](https://devdocs.magento.com/guides/v2.4/rest/bk-rest-api.html)

## Resources
- [BigCommerce Orders](https://developer.bigcommerce.com/api-reference/orders/orders-api)
