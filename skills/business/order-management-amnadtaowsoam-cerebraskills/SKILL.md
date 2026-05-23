---
name: Order Management System (OMS)
description: Handling the complete order lifecycle from creation to fulfillment, including order validation, status tracking, inventory reservation, payment processing, and returns.
---

# Order Management System (OMS)

> **Current Level:** Intermediate  
> **Domain:** E-commerce / Backend

---

## Overview

Order Management System handles the complete order lifecycle from creation to fulfillment, including order validation, status tracking, inventory reservation, and returns processing. Effective OMS systems ensure data consistency, handle edge cases, and provide real-time order status updates.

---

---

## Core Concepts

### Table of Contents

1. [Order Lifecycle](#order-lifecycle)
2. [Database Schema](#database-schema)
3. [Order Creation](#order-creation)
4. [Order Validation](#order-validation)
5. [Status Workflow](#status-workflow)
6. [Inventory Reservation](#inventory-reservation)
7. [Order Fulfillment](#order-fulfillment)
8. [Order Tracking](#order-tracking)
9. [Order Cancellation](#order-cancellation)
10. [Returns and Refunds](#returns-and-refunds)
11. [Order Search and Filtering](#order-search-and-filtering)
12. [Bulk Operations](#bulk-operations)
13. [API Design](#api-design)
14. [Best Practices](#best-practices)

---

## Order Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                        Order Lifecycle                          │
└─────────────────────────────────────────────────────────────────┘

Created → Pending → Paid → Processing → Shipped → Delivered
                                    ↓
                               Cancelled
                                    ↓
                               Returned
```

### Order States

```typescript
enum OrderStatus {
  CREATED = 'created',           // Order created, awaiting payment
  PENDING = 'pending',           // Payment initiated
  PAID = 'paid',                // Payment confirmed
  PROCESSING = 'processing',     // Being prepared for shipment
  SHIPPED = 'shipped',          // Shipped to customer
  DELIVERED = 'delivered',      // Delivered to customer
  CANCELLED = 'cancelled',       // Order cancelled
  RETURNED = 'returned',         // Returned by customer
  REFUNDED = 'refunded',        // Refunded
}

enum PaymentStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
  REFUNDED = 'refunded',
}

enum FulfillmentStatus {
  UNFULFILLED = 'unfulfilled',
  PARTIALLY_FULFILLED = 'partially_fulfilled',
  FULFILLED = 'fulfilled',
}
```

---

## Database Schema

### Prisma Schema

```prisma
model Order {
  id                String          @id @default(uuid())
  orderNumber       String         @unique
  userId            String?
  user              User?           @relation(fields: [userId], references: [id])
  status            OrderStatus     @default(CREATED)
  paymentStatus     PaymentStatus   @default(PENDING)
  fulfillmentStatus FulfillmentStatus @default(UNFULFILLED)
  currency          String          @default("USD")
  subtotal          Decimal         @default(0)
  tax               Decimal         @default(0)
  shipping          Decimal         @default(0)
  discount          Decimal         @default(0)
  total             Decimal         @default(0)
  notes             String?
  internalNotes     String?
  customerEmail     String
  customerPhone     String?
  shippingAddress   Json
  billingAddress    Json
  paymentIntentId   String?        @unique
  couponCode        String?
  source            String?         // web, mobile, admin
  createdAt         DateTime        @default(now())
  updatedAt         DateTime        @updatedAt
  paidAt            DateTime?
  shippedAt         DateTime?
  deliveredAt       DateTime?
  cancelledAt       DateTime?
  items             OrderItem[]
  payments          Payment[]
  fulfillments      Fulfillment[]
  returns           Return[]
  history           OrderHistory[]

  @@index([userId])
  @@index([status])
  @@index([createdAt])
  @@index([orderNumber])
}

model OrderItem {
  id          String   @id @default(uuid())
  orderId     String
  order       Order    @relation(fields: [orderId], references: [id], onDelete: Cascade)
  productId   String
  product     Product  @relation(fields: [productId], references: [id])
  variantId   String?
  variant     Variant? @relation(fields: [variantId], references: [id])
  name        String
  sku         String?
  quantity    Int
  price       Decimal
  salePrice   Decimal?
  total       Decimal
  createdAt   DateTime @default(now())

  @@index([orderId])
  @@index([productId])
}

model Payment {
  id               String        @id @default(uuid())
  orderId          String
  order            Order         @relation(fields: [orderId], references: [id], onDelete: Cascade)
  gateway          String        // stripe, paypal, 2c2p, omise
  paymentIntentId  String        @unique
  amount           Decimal
  currency         String
  status           PaymentStatus
  errorMessage     String?
  createdAt        DateTime      @default(now())
  paidAt           DateTime?
  refunds          Refund[]

  @@index([orderId])
  @@index([paymentIntentId])
}

model Refund {
  id                String   @id @default(uuid())
  paymentId         String
  payment           Payment  @relation(fields: [paymentId], references: [id], onDelete: Cascade)
  amount            Decimal
  reason            String?
  status            String    @default("pending")
  gatewayRefundId   String?  @unique
  createdAt         DateTime @default(now())
  processedAt       DateTime?

  @@index([paymentId])
}

model Fulfillment {
  id          String   @id @default(uuid())
  orderId     String
  order       Order    @relation(fields: [orderId], references: [id], onDelete: Cascade)
  trackingNumber String?
  carrier     String?
  status      String   @default("pending")
  items       FulfillmentItem[]
  createdAt   DateTime @default(now())
  shippedAt   DateTime?

  @@index([orderId])
}

model FulfillmentItem {
  id            String      @id @default(uuid())
  fulfillmentId String
  fulfillment   Fulfillment @relation(fields: [fulfillmentId], references: [id], onDelete: Cascade)
  orderItemId   String
  quantity      Int

  @@index([fulfillmentId])
}

model Return {
  id          String   @id @default(uuid())
  orderId     String
  order       Order    @relation(fields: [orderId], references: [id], onDelete: Cascade)
  status      String   @default("pending")
  reason      String?
  items       ReturnItem[]
  refundAmount Decimal
  createdAt   DateTime @default(now())
  processedAt DateTime?

  @@index([orderId])
}

model ReturnItem {
  id        String  @id @default(uuid())
  returnId  String
  return    Return  @relation(fields: [returnId], references: [id], onDelete: Cascade)
  orderItemId String
  quantity  Int
  reason    String?

  @@index([returnId])
}

model OrderHistory {
  id          String   @id @default(uuid())
  orderId     String
  order       Order    @relation(fields: [orderId], references: [id], onDelete: Cascade)
  status      OrderStatus
  changedBy   String?
  changedAt   DateTime @default(now())
  notes       String?

  @@index([orderId])
  @@index([changedAt])
}
```

---

## Order Creation

### Order Manager

```typescript
class OrderManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create order from cart
   */
  async createOrder(params: {
    userId?: string;
    cartId: string;
    shippingAddress: Address;
    billingAddress: Address;
    couponCode?: string;
    notes?: string;
    source?: string;
  }): Promise<Order> {
    // Get cart
    const cart = await this.prisma.cart.findUnique({
      where: { id: params.cartId },
      include: {
        items: {
          include: {
            product: true,
            variant: true,
          },
        },
      },
    });

    if (!cart) {
      throw new Error('Cart not found');
    }

    if (cart.items.length === 0) {
      throw new Error('Cart is empty');
    }

    // Validate cart
    const validation = await this.validateCart(cart);
    if (!validation.valid) {
      throw new Error(`Cart validation failed: ${validation.errors.join(', ')}`);
    }

    // Get user
    let user = null;
    if (params.userId) {
      user = await this.prisma.user.findUnique({
        where: { id: params.userId },
      });
    }

    // Calculate totals
    const totals = await this.calculateTotals(cart, params.couponCode);

    // Generate order number
    const orderNumber = await this.generateOrderNumber();

    // Create order
    const order = await this.prisma.$transaction(async (tx) => {
      // Create order
      const order = await tx.order.create({
        data: {
          orderNumber,
          userId: params.userId,
          customerEmail: user?.email || params.shippingAddress.email,
          customerPhone: params.shippingAddress.phone,
          shippingAddress: params.shippingAddress,
          billingAddress: params.billingAddress,
          currency: cart.currency,
          subtotal: totals.subtotal,
          tax: totals.tax,
          shipping: totals.shipping,
          discount: totals.discount,
          total: totals.total,
          notes: params.notes,
          couponCode: params.couponCode,
          source: params.source,
          status: OrderStatus.CREATED,
          paymentStatus: PaymentStatus.PENDING,
          fulfillmentStatus: FulfillmentStatus.UNFULFILLED,
        },
      });

      // Create order items
      for (const cartItem of cart.items) {
        const price = cartItem.salePrice || cartItem.price;
        const total = price * cartItem.quantity;

        await tx.orderItem.create({
          data: {
            orderId: order.id,
            productId: cartItem.productId,
            variantId: cartItem.variantId,
            name: cartItem.product.name,
            sku: cartItem.variant?.sku || cartItem.product.sku,
            quantity: cartItem.quantity,
            price,
            salePrice: cartItem.salePrice,
            total,
          },
        });
      }

      // Reserve inventory
      await this.reserveInventory(tx, order.id, cart.items);

      // Create history entry
      await tx.orderHistory.create({
        data: {
          orderId: order.id,
          status: OrderStatus.CREATED,
          changedBy: params.userId,
        },
      });

      // Clear cart
      await tx.cartItem.deleteMany({
        where: { cartId: params.cartId },
      });

      return order;
    });

    return order;
  }

  /**
   * Validate cart
   */
  private async validateCart(cart: any): Promise<{
    valid: boolean;
    errors: string[];
  }> {
    const errors: string[] = [];

    for (const item of cart.items) {
      // Check product exists and is active
      if (!item.product || !item.product.active) {
        errors.push(`Product ${item.productId} is not available`);
        continue;
      }

      // Check variant
      if (item.variantId && !item.variant) {
        errors.push(`Variant ${item.variantId} not found`);
        continue;
      }

      // Check stock
      const stock = await this.getAvailableStock(item.productId, item.variantId);
      if (item.quantity > stock) {
        errors.push(`Insufficient stock for ${item.product.name}`);
      }

      // Check price
      const currentPrice = item.variantId
        ? item.variant?.price
        : item.product?.price;

      const currentSalePrice = item.variantId
        ? item.variant?.salePrice
        : item.product?.salePrice;

      if (item.price !== currentPrice) {
        errors.push(`Price changed for ${item.product.name}`);
      }
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  /**
   * Calculate totals
   */
  private async calculateTotals(
    cart: any,
    couponCode?: string
  ): Promise<{
    subtotal: number;
    tax: number;
    shipping: number;
    discount: number;
    total: number;
  }> {
    let subtotal = 0;

    for (const item of cart.items) {
      const price = item.salePrice || item.price;
      subtotal += price * item.quantity;
    }

    // Calculate tax
    const tax = subtotal * 0.1; // 10% tax

    // Calculate shipping
    const shipping = await this.calculateShipping(cart);

    // Calculate discount
    let discount = 0;
    if (couponCode) {
      discount = await this.applyCoupon(couponCode, subtotal);
    }

    const total = subtotal + tax + shipping - discount;

    return {
      subtotal,
      tax,
      shipping,
      discount,
      total,
    };
  }

  /**
   * Generate order number
   */
  private async generateOrderNumber(): Promise<string> {
    const prefix = 'ORD';
    const date = new Date();
    const dateStr = date.getFullYear().toString().slice(-2) +
                   (date.getMonth() + 1).toString().padStart(2, '0') +
                   date.getDate().toString().padStart(2, '0');

    // Get last order number for today
    const lastOrder = await this.prisma.order.findFirst({
      where: {
        orderNumber: {
          startsWith: `${prefix}${dateStr}`,
        },
      },
      orderBy: { orderNumber: 'desc' },
    });

    let sequence = 1;
    if (lastOrder) {
      const lastSequence = parseInt(lastOrder.orderNumber.slice(-6));
      sequence = lastSequence + 1;
    }

    return `${prefix}${dateStr}${sequence.toString().padStart(6, '0')}`;
  }

  /**
   * Reserve inventory
   */
  private async reserveInventory(
    tx: Prisma.TransactionClient,
    orderId: string,
    items: any[]
  ): Promise<void> {
    for (const item of items) {
      await tx.inventoryReservation.create({
        data: {
          orderId,
          productId: item.productId,
          variantId: item.variantId,
          quantity: item.quantity,
          status: 'reserved',
        },
      });
    }
  }

  /**
   * Get available stock
   */
  private async getAvailableStock(productId: string, variantId?: string): Promise<number> {
    // Implement stock checking
    return 100;
  }

  /**
   * Calculate shipping
   */
  private async calculateShipping(cart: any): Promise<number> {
    // Implement shipping calculation
    return 0;
  }

  /**
   * Apply coupon
   */
  private async applyCoupon(couponCode: string, subtotal: number): Promise<number> {
    // Implement coupon application
    return 0;
  }

  constructor(private prisma: PrismaClient) {}
}
```

---

## Order Validation

### Order Validator

```typescript
class OrderValidator {
  /**
   * Validate order
   */
  async validateOrder(order: Order): Promise<{
    valid: boolean;
    errors: string[];
    warnings: string[];
  }> {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Validate items
    for (const item of order.items) {
      const itemValidation = await this.validateItem(item);
      errors.push(...itemValidation.errors);
      warnings.push(...itemValidation.warnings);
    }

    // Validate addresses
    const addressValidation = this.validateAddresses(order);
    errors.push(...addressValidation.errors);
    warnings.push(...addressValidation.warnings);

    // Validate totals
    const totalsValidation = this.validateTotals(order);
    errors.push(...totalsValidation.errors);

    return {
      valid: errors.length === 0,
      errors,
      warnings,
    };
  }

  /**
   * Validate item
   */
  private async validateItem(item: any): Promise<{
    errors: string[];
    warnings: string[];
  }> {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Check product exists
    const product = await this.prisma.product.findUnique({
      where: { id: item.productId },
    });

    if (!product) {
      errors.push(`Product ${item.productId} not found`);
      return { errors, warnings };
    }

    // Check variant
    if (item.variantId) {
      const variant = await this.prisma.variant.findUnique({
        where: { id: item.variantId },
      });

      if (!variant) {
        errors.push(`Variant ${item.variantId} not found`);
      }
    }

    // Check stock
    const stock = await this.getAvailableStock(item.productId, item.variantId);
    if (item.quantity > stock) {
      errors.push(`Insufficient stock for ${item.name}`);
    } else if (item.quantity > stock * 0.8) {
      warnings.push(`Low stock for ${item.name}`);
    }

    // Check price
    const currentPrice = item.variantId
      ? (await this.prisma.variant.findUnique({ where: { id: item.variantId } }))?.price
      : product.price;

    if (item.price !== currentPrice) {
      warnings.push(`Price changed for ${item.name}`);
    }

    return { errors, warnings };
  }

  /**
   * Validate addresses
   */
  private validateAddresses(order: any): {
    errors: string[];
    warnings: string[];
  } {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Check required fields
    const requiredFields = ['firstName', 'lastName', 'address1', 'city', 'country', 'postalCode'];

    for (const field of requiredFields) {
      if (!order.shippingAddress[field]) {
        errors.push(`Missing shipping address field: ${field}`);
      }
    }

    // Check email
    if (!order.customerEmail || !this.isValidEmail(order.customerEmail)) {
      errors.push('Invalid customer email');
    }

    return { errors, warnings };
  }

  /**
   * Validate totals
   */
  private validateTotals(order: any): {
    errors: string[];
  } {
    const errors: string[] = [];

    // Recalculate subtotal
    let calculatedSubtotal = 0;
    for (const item of order.items) {
      const price = item.salePrice || item.price;
      calculatedSubtotal += price * item.quantity;
    }

    if (Math.abs(order.subtotal - calculatedSubtotal) > 0.01) {
      errors.push(`Subtotal mismatch: expected ${calculatedSubtotal}, got ${order.subtotal}`);
    }

    return { errors };
  }

  private isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  private async getAvailableStock(productId: string, variantId?: string): Promise<number> {
    // Implement stock checking
    return 100;
  }

  constructor(private prisma: PrismaClient) {}
}
```

---

## Status Workflow

### Status Manager

```typescript
class StatusManager {
  private transitions: Record<OrderStatus, OrderStatus[]> = {
    [OrderStatus.CREATED]: [OrderStatus.PENDING, OrderStatus.CANCELLED],
    [OrderStatus.PENDING]: [OrderStatus.PAID, OrderStatus.CANCELLED],
    [OrderStatus.PAID]: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
    [OrderStatus.PROCESSING]: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
    [OrderStatus.SHIPPED]: [OrderStatus.DELIVERED],
    [OrderStatus.DELIVERED]: [OrderStatus.RETURNED],
    [OrderStatus.CANCELLED]: [],
    [OrderStatus.RETURNED]: [OrderStatus.REFUNDED],
    [OrderStatus.REFUNDED]: [],
  };

  /**
   * Transition status
   */
  async transitionStatus(params: {
    orderId: string;
    newStatus: OrderStatus;
    changedBy?: string;
    notes?: string;
  }): Promise<Order> {
    const order = await this.prisma.order.findUnique({
      where: { id: params.orderId },
    });

    if (!order) {
      throw new Error('Order not found');
    }

    // Check if transition is valid
    if (!this.canTransition(order.status, params.newStatus)) {
      throw new Error(`Cannot transition from ${order.status} to ${params.newStatus}`);
    }

    // Update order
    const updatedOrder = await this.prisma.$transaction(async (tx) => {
      const updated = await tx.order.update({
        where: { id: params.orderId },
        data: {
          status: params.newStatus,
          ...(params.newStatus === OrderStatus.SHIPPED && { shippedAt: new Date() }),
          ...(params.newStatus === OrderStatus.DELIVERED && { deliveredAt: new Date() }),
          ...(params.newStatus === OrderStatus.CANCELLED && { cancelledAt: new Date() }),
        },
      });

      // Create history entry
      await tx.orderHistory.create({
        data: {
          orderId: params.orderId,
          status: params.newStatus,
          changedBy: params.changedBy,
          notes: params.notes,
        },
      });

      return updated;
    });

    return updatedOrder;
  }

  /**
   * Check if transition is valid
   */
  canTransition(from: OrderStatus, to: OrderStatus): boolean {
    const allowed = this.transitions[from];
    return allowed.includes(to);
  }

  /**
   * Get available transitions
   */
  getAvailableTransitions(status: OrderStatus): OrderStatus[] {
    return this.transitions[status] || [];
  }

  constructor(private prisma: PrismaClient) {}
}
```

---

## Inventory Reservation

### Inventory Manager

```typescript
class InventoryManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Reserve inventory
   */
  async reserveInventory(params: {
    orderId: string;
    items: Array<{
      productId: string;
      variantId?: string;
      quantity: number;
    }>;
  }): Promise<void> {
    await this.prisma.$transaction(async (tx) => {
      for (const item of params.items) {
        // Check stock with optimistic locking
        const inventory = await tx.inventory.findFirst({
          where: {
            productId: item.productId,
            variantId: item.variantId,
          },
        });

        if (!inventory) {
          throw new Error(`Inventory not found for product ${item.productId}`);
        }

        if (inventory.quantity < item.quantity) {
          throw new Error(`Insufficient stock for product ${item.productId}`);
        }

        // Reserve stock
        await tx.inventory.update({
          where: { id: inventory.id },
          data: {
            quantity: { decrement: item.quantity },
            reserved: { increment: item.quantity },
          },
        });

        // Create reservation record
        await tx.inventoryReservation.create({
          data: {
            orderId: params.orderId,
            productId: item.productId,
            variantId: item.variantId,
            quantity: item.quantity,
            status: 'reserved',
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
      where: { orderId },
    });

    await this.prisma.$transaction(async (tx) => {
      for (const reservation of reservations) {
        // Find inventory
        const inventory = await tx.inventory.findFirst({
          where: {
            productId: reservation.productId,
            variantId: reservation.variantId,
          },
        });

        if (inventory) {
          // Release reserved stock
          await tx.inventory.update({
            where: { id: inventory.id },
            data: {
              reserved: { decrement: reservation.quantity },
            },
          });
        }

        // Update reservation status
        await tx.inventoryReservation.update({
          where: { id: reservation.id },
          data: { status: 'released' },
        });
      }
    });
  }

  /**
   * Confirm reservation (after successful payment)
   */
  async confirmReservation(orderId: string): Promise<void> {
    const reservations = await this.prisma.inventoryReservation.findMany({
      where: { orderId, status: 'reserved' },
    });

    await this.prisma.$transaction(async (tx) => {
      for (const reservation of reservations) {
        // Update reservation status
        await tx.inventoryReservation.update({
          where: { id: reservation.id },
          data: { status: 'confirmed' },
        });
      }
    });
  }

  constructor(private prisma: PrismaClient) {}
}
```

---

## Order Fulfillment

### Fulfillment Manager

```typescript
class FulfillmentManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create fulfillment
   */
  async createFulfillment(params: {
    orderId: string;
    items: Array<{
      orderItemId: string;
      quantity: number;
    }>;
    trackingNumber?: string;
    carrier?: string;
  }): Promise<Fulfillment> {
    const order = await this.prisma.order.findUnique({
      where: { id: params.orderId },
      include: { items: true },
    });

    if (!order) {
      throw new Error('Order not found');
    }

    const fulfillment = await this.prisma.$transaction(async (tx) => {
      // Create fulfillment
      const fulfillment = await tx.fulfillment.create({
        data: {
          orderId: params.orderId,
          trackingNumber: params.trackingNumber,
          carrier: params.carrier,
          status: 'pending',
        },
      });

      // Create fulfillment items
      for (const item of params.items) {
        await tx.fulfillmentItem.create({
          data: {
            fulfillmentId: fulfillment.id,
            orderItemId: item.orderItemId,
            quantity: item.quantity,
          },
        });
      }

      // Check if order is fully fulfilled
      const allFulfillments = await tx.fulfillment.findMany({
        where: { orderId: params.orderId },
        include: { items: true },
      });

      let totalFulfilled = 0;
      for (const f of allFulfillments) {
        for (const fi of f.items) {
          totalFulfilled += fi.quantity;
        }
      }

      const totalOrdered = order.items.reduce((sum, i) => sum + i.quantity, 0);

      if (totalFulfilled >= totalOrdered) {
        await tx.order.update({
          where: { id: params.orderId },
          data: {
            fulfillmentStatus: FulfillmentStatus.FULFILLED,
            status: OrderStatus.SHIPPED,
            shippedAt: new Date(),
          },
        });
      } else {
        await tx.order.update({
          where: { id: params.orderId },
          data: {
            fulfillmentStatus: FulfillmentStatus.PARTIALLY_FULFILLED,
            status: OrderStatus.PROCESSING,
          },
        });
      }

      return fulfillment;
    });

    return fulfillment;
  }

  /**
   * Update fulfillment tracking
   */
  async updateTracking(params: {
    fulfillmentId: string;
    trackingNumber: string;
    carrier: string;
  }): Promise<Fulfillment> {
    return await this.prisma.fulfillment.update({
      where: { id: params.fulfillmentId },
      data: {
        trackingNumber: params.trackingNumber,
        carrier: params.carrier,
      },
    });
  }
}
```

---

## Order Tracking

### Tracking Manager

```typescript
class TrackingManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get order tracking
   */
  async getOrderTracking(orderId: string): Promise<{
    order: Order;
    history: OrderHistory[];
    fulfillments: Fulfillment[];
    trackingEvents: TrackingEvent[];
  }> {
    const order = await this.prisma.order.findUnique({
      where: { id: orderId },
      include: {
        history: { orderBy: { changedAt: 'desc' } },
        fulfillments: {
          include: { items: true },
        },
      },
    });

    if (!order) {
      throw new Error('Order not found');
    }

    // Get tracking events from carriers
    const trackingEvents: TrackingEvent[] = [];

    for (const fulfillment of order.fulfillments) {
      if (fulfillment.trackingNumber && fulfillment.carrier) {
        const events = await this.getTrackingEvents(
          fulfillment.trackingNumber,
          fulfillment.carrier
        );
        trackingEvents.push(...events);
      }
    }

    return {
      order,
      history: order.history,
      fulfillments: order.fulfillments,
      trackingEvents,
    };
  }

  /**
   * Get tracking events from carrier
   */
  private async getTrackingEvents(
    trackingNumber: string,
    carrier: string
  ): Promise<TrackingEvent[]> {
    // Implement carrier API integration
    return [];
  }
}
```

---

## Order Cancellation

### Cancellation Manager

```typescript
class CancellationManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Cancel order
   */
  async cancelOrder(params: {
    orderId: string;
    reason?: string;
    refund?: boolean;
    changedBy?: string;
  }): Promise<Order> {
    const order = await this.prisma.order.findUnique({
      where: { id: params.orderId },
      include: { items: true, payments: true },
    });

    if (!order) {
      throw new Error('Order not found');
    }

    // Check if order can be cancelled
    if (order.status === OrderStatus.SHIPPED || order.status === OrderStatus.DELIVERED) {
      throw new Error('Order cannot be cancelled');
    }

    const statusManager = new StatusManager(this.prisma);

    // Transition to cancelled
    const cancelledOrder = await statusManager.transitionStatus({
      orderId: params.orderId,
      newStatus: OrderStatus.CANCELLED,
      changedBy: params.changedBy,
      notes: params.reason,
    });

    // Release inventory
    const inventoryManager = new InventoryManager(this.prisma);
    await inventoryManager.releaseReservation(params.orderId);

    // Process refund if requested
    if (params.refund && order.payments.length > 0) {
      const refundManager = new RefundManager(this.prisma);
      for (const payment of order.payments) {
        if (payment.status === PaymentStatus.COMPLETED) {
          await refundManager.createRefund({
            paymentId: payment.id,
            reason: params.reason || 'Order cancelled',
          });
        }
      }
    }

    return cancelledOrder;
  }
}
```

---

## Returns and Refunds

### Return Manager

```typescript
class ReturnManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create return request
   */
  async createReturn(params: {
    orderId: string;
    items: Array<{
      orderItemId: string;
      quantity: number;
      reason?: string;
    }>;
    reason?: string;
  }): Promise<Return> {
    const order = await this.prisma.order.findUnique({
      where: { id: params.orderId },
      include: { items: true },
    });

    if (!order) {
      throw new Error('Order not found');
    }

    // Validate items
    for (const item of params.items) {
      const orderItem = order.items.find(i => i.id === item.orderItemId);
      if (!orderItem) {
        throw new Error(`Order item ${item.orderItemId} not found`);
      }

      if (item.quantity > orderItem.quantity) {
        throw new Error(`Return quantity exceeds ordered quantity for ${orderItem.name}`);
      }
    }

    // Calculate refund amount
    let refundAmount = 0;
    for (const item of params.items) {
      const orderItem = order.items.find(i => i.id === item.orderItemId);
      if (orderItem) {
        const price = orderItem.salePrice || orderItem.price;
        refundAmount += price * item.quantity;
      }
    }

    // Create return
    const returnRecord = await this.prisma.$transaction(async (tx) => {
      const returnRecord = await tx.return.create({
        data: {
          orderId: params.orderId,
          status: 'pending',
          reason: params.reason,
          refundAmount,
        },
      });

      // Create return items
      for (const item of params.items) {
        await tx.returnItem.create({
          data: {
            returnId: returnRecord.id,
            orderItemId: item.orderItemId,
            quantity: item.quantity,
            reason: item.reason,
          },
        });
      }

      // Update order status
      await tx.order.update({
        where: { id: params.orderId },
        data: { status: OrderStatus.RETURNED },
      });

      return returnRecord;
    });

    return returnRecord;
  }

  /**
   * Process return
   */
  async processReturn(params: {
    returnId: string;
    approved: boolean;
    notes?: string;
  }): Promise<Return> {
    const returnRecord = await this.prisma.return.findUnique({
      where: { id: params.returnId },
      include: { order: { include: { payments: true } } },
    });

    if (!returnRecord) {
      throw new Error('Return not found');
    }

    if (returnRecord.status !== 'pending') {
      throw new Error('Return has already been processed');
    }

    const updatedReturn = await this.prisma.$transaction(async (tx) => {
      const updated = await tx.return.update({
        where: { id: params.returnId },
        data: {
          status: params.approved ? 'approved' : 'rejected',
          processedAt: new Date(),
        },
      });

      // If approved, process refund
      if (params.approved && returnRecord.order.payments.length > 0) {
        const refundManager = new RefundManager(tx);
        const payment = returnRecord.order.payments[0];

        await refundManager.createRefund({
          paymentId: payment.id,
          amount: returnRecord.refundAmount,
          reason: `Return ${params.returnId}`,
        });
      }

      return updated;
    });

    return updatedReturn;
  }
}
```

---

## Order Search and Filtering

### Search Manager

```typescript
class OrderSearchManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Search orders
   */
  async searchOrders(params: {
    query?: string;
    status?: OrderStatus;
    userId?: string;
    startDate?: Date;
    endDate?: Date;
    minAmount?: number;
    maxAmount?: number;
    page?: number;
    limit?: number;
    sortBy?: string;
    sortOrder?: 'asc' | 'desc';
  }): Promise<{
    orders: Order[];
    total: number;
    page: number;
    totalPages: number;
  }> {
    const where: any = {};

    // Build where clause
    if (params.query) {
      where.OR = [
        { orderNumber: { contains: params.query } },
        { customerEmail: { contains: params.query } },
        { customerPhone: { contains: params.query } },
      ];
    }

    if (params.status) {
      where.status = params.status;
    }

    if (params.userId) {
      where.userId = params.userId;
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

    if (params.minAmount || params.maxAmount) {
      where.total = {};
      if (params.minAmount) {
        where.total.gte = params.minAmount;
      }
      if (params.maxAmount) {
        where.total.lte = params.maxAmount;
      }
    }

    const page = params.page || 1;
    const limit = params.limit || 20;
    const skip = (page - 1) * limit;

    // Get total count
    const total = await this.prisma.order.count({ where });

    // Get orders
    const orders = await this.prisma.order.findMany({
      where,
      include: {
        items: true,
        user: true,
      },
      orderBy: {
        [params.sortBy || 'createdAt']: params.sortOrder || 'desc',
      },
      skip,
      take: limit,
    });

    return {
      orders,
      total,
      page,
      totalPages: Math.ceil(total / limit),
    };
  }
}
```

---

## Bulk Operations

### Bulk Operations Manager

```typescript
class BulkOperationsManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Bulk update status
   */
  async bulkUpdateStatus(params: {
    orderIds: string[];
    newStatus: OrderStatus;
    changedBy?: string;
  }): Promise<{ success: string[]; failed: Array<{ orderId: string; error: string }> }> {
    const success: string[] = [];
    const failed: Array<{ orderId: string; error: string }> = [];

    const statusManager = new StatusManager(this.prisma);

    for (const orderId of params.orderIds) {
      try {
        await statusManager.transitionStatus({
          orderId,
          newStatus: params.newStatus,
          changedBy: params.changedBy,
        });
        success.push(orderId);
      } catch (error) {
        failed.push({
          orderId,
          error: error.message,
        });
      }
    }

    return { success, failed };
  }

  /**
   * Bulk export
   */
  async bulkExport(params: {
    orderIds: string[];
    format: 'csv' | 'json' | 'xlsx';
  }): Promise<Buffer> {
    const orders = await this.prisma.order.findMany({
      where: {
        id: { in: params.orderIds },
      },
      include: {
        items: true,
        user: true,
        payments: true,
      },
    });

    switch (params.format) {
      case 'csv':
        return this.exportToCSV(orders);
      case 'json':
        return Buffer.from(JSON.stringify(orders, null, 2));
      case 'xlsx':
        return this.exportToExcel(orders);
      default:
        throw new Error('Unsupported format');
    }
  }

  private exportToCSV(orders: any[]): Buffer {
    const headers = [
      'Order Number',
      'Date',
      'Customer Email',
      'Status',
      'Total',
      'Currency',
    ];

    const rows = orders.map(order => [
      order.orderNumber,
      order.createdAt.toISOString(),
      order.customerEmail,
      order.status,
      order.total,
      order.currency,
    ]);

    const csv = [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
    return Buffer.from(csv);
  }

  private exportToExcel(orders: any[]): Buffer {
    // Implement Excel export
    return Buffer.from('');
  }
}
```

---

## API Design

### REST API

```typescript
import express from 'express';

const router = express.Router();

/**
 * GET /api/orders
 * List orders with filtering
 */
router.get('/', async (req, res) => {
  try {
    const searchManager = new OrderSearchManager(prisma);
    const result = await searchManager.searchOrders({
      query: req.query.q as string,
      status: req.query.status as OrderStatus,
      userId: req.user?.id,
      startDate: req.query.startDate ? new Date(req.query.startDate as string) : undefined,
      endDate: req.query.endDate ? new Date(req.query.endDate as string) : undefined,
      minAmount: req.query.minAmount ? parseFloat(req.query.minAmount as string) : undefined,
      maxAmount: req.query.maxAmount ? parseFloat(req.query.maxAmount as string) : undefined,
      page: req.query.page ? parseInt(req.query.page as string) : undefined,
      limit: req.query.limit ? parseInt(req.query.limit as string) : undefined,
      sortBy: req.query.sortBy as string,
      sortOrder: req.query.sortOrder as 'asc' | 'desc',
    });

    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * GET /api/orders/:id
 * Get order details
 */
router.get('/:id', async (req, res) => {
  try {
    const order = await prisma.order.findUnique({
      where: { id: req.params.id },
      include: {
        items: {
          include: {
            product: true,
            variant: true,
          },
        },
        user: true,
        payments: true,
        fulfillments: {
          include: { items: true },
        },
        history: {
          orderBy: { changedAt: 'desc' },
        },
      },
    });

    if (!order) {
      return res.status(404).json({ error: 'Order not found' });
    }

    res.json(order);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * POST /api/orders
 * Create order
 */
router.post('/', async (req, res) => {
  try {
    const orderManager = new OrderManager(prisma);
    const order = await orderManager.createOrder({
      userId: req.user?.id,
      ...req.body,
    });

    res.status(201).json(order);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

/**
 * PUT /api/orders/:id/status
 * Update order status
 */
router.put('/:id/status', async (req, res) => {
  try {
    const statusManager = new StatusManager(prisma);
    const order = await statusManager.transitionStatus({
      orderId: req.params.id,
      newStatus: req.body.status,
      changedBy: req.user?.id,
      notes: req.body.notes,
    });

    res.json(order);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

/**
 * POST /api/orders/:id/cancel
 * Cancel order
 */
router.post('/:id/cancel', async (req, res) => {
  try {
    const cancellationManager = new CancellationManager(prisma);
    const order = await cancellationManager.cancelOrder({
      orderId: req.params.id,
      reason: req.body.reason,
      refund: req.body.refund,
      changedBy: req.user?.id,
    });

    res.json(order);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

/**
 * POST /api/orders/:id/fulfill
 * Create fulfillment
 */
router.post('/:id/fulfill', async (req, res) => {
  try {
    const fulfillmentManager = new FulfillmentManager(prisma);
    const fulfillment = await fulfillmentManager.createFulfillment({
      orderId: req.params.id,
      ...req.body,
    });

    res.status(201).json(fulfillment);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

/**
 * GET /api/orders/:id/tracking
 * Get order tracking
 */
router.get('/:id/tracking', async (req, res) => {
  try {
    const trackingManager = new TrackingManager(prisma);
    const tracking = await trackingManager.getOrderTracking(req.params.id);

    res.json(tracking);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
```

---

## Best Practices

### Order Management Best Practices

```typescript
// 1. Always use transactions for order operations
async function createOrderWithTransaction(cartId: string): Promise<Order> {
  return await prisma.$transaction(async (tx) => {
    // Create order
    const order = await tx.order.create({ ... });

    // Create items
    await tx.orderItem.createMany({ ... });

    // Reserve inventory
    await tx.inventoryReservation.createMany({ ... });

    return order;
  });
}

// 2. Implement optimistic locking for inventory
async function reserveStockWithLock(productId: string, quantity: number): Promise<void> {
  await prisma.$transaction(async (tx) => {
    const inventory = await tx.inventory.findFirst({
      where: { productId },
    });

    if (inventory.quantity < quantity) {
      throw new Error('Insufficient stock');
    }

    await tx.inventory.update({
      where: { id: inventory.id },
      data: {
        quantity: { decrement: quantity },
        version: { increment: 1 }, // Optimistic locking
      },
    });
  });
}

// 3. Validate order before creation
async function validateOrderBeforeCreation(orderData: any): Promise<boolean> {
  const validator = new OrderValidator(prisma);
  const validation = await validator.validateOrder(orderData);

  if (!validation.valid) {
    throw new Error(`Validation failed: ${validation.errors.join(', ')}`);
  }

  return true;
}

// 4. Implement idempotency for order creation
async function createOrderIdempotent(idempotencyKey: string, cartId: string): Promise<Order> {
  // Check if order already exists
  const existing = await prisma.order.findFirst({
    where: { idempotencyKey },
  });

  if (existing) {
    return existing;
  }

  // Create new order
  return await prisma.order.create({
    data: {
      idempotencyKey,
      ...orderData,
    },
  });
}

// 5. Log all order state changes
async function logOrderStateChange(orderId: string, newStatus: OrderStatus): Promise<void> {
  await prisma.orderHistory.create({
    data: {
      orderId,
      status: newStatus,
      changedAt: new Date(),
    },
  });
}
```

---

---

## Quick Start

### Basic Order Creation

```typescript
interface OrderItem {
  productId: string
  quantity: number
  price: number
}

async function createOrder(
  userId: string,
  items: OrderItem[],
  shippingAddress: Address
) {
  // 1. Validate items
  for (const item of items) {
    const product = await getProduct(item.productId)
    if (!product.inStock || product.stock < item.quantity) {
      throw new Error(`Product ${item.productId} out of stock`)
    }
  }
  
  // 2. Calculate totals
  const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0)
  const tax = calculateTax(subtotal)
  const shipping = calculateShipping(shippingAddress)
  const total = subtotal + tax + shipping
  
  // 3. Create order
  const order = await db.orders.create({
    data: {
      userId,
      status: 'pending',
      subtotal,
      tax,
      shipping,
      total,
      items: {
        create: items.map(item => ({
          productId: item.productId,
          quantity: item.quantity,
          price: item.price
        }))
      }
    }
  })
  
  // 4. Reserve inventory
  await reserveInventory(items)
  
  return order
}
```

### Order Status Workflow

```typescript
const ORDER_STATUS_FLOW = {
  pending: ['processing', 'cancelled'],
  processing: ['shipped', 'cancelled'],
  shipped: ['delivered', 'returned'],
  delivered: ['returned'],
  cancelled: [],
  returned: ['refunded']
}

async function updateOrderStatus(orderId: string, newStatus: OrderStatus) {
  const order = await db.orders.findUnique({ where: { id: orderId } })
  
  if (!ORDER_STATUS_FLOW[order.status].includes(newStatus)) {
    throw new Error(`Invalid status transition: ${order.status} -> ${newStatus}`)
  }
  
  await db.orders.update({
    where: { id: orderId },
    data: { status: newStatus }
  })
  
  // Log status change
  await logOrderStateChange(orderId, newStatus)
}
```

---

## Production Checklist

- [ ] **Order Validation**: Validate all order data
- [ ] **Inventory Check**: Check inventory before order creation
- [ ] **Price Validation**: Validate prices server-side
- [ ] **Status Workflow**: Enforce valid status transitions
- [ ] **Idempotency**: Use idempotency keys for order creation
- [ ] **Inventory Reservation**: Reserve inventory on order creation
- [ ] **Payment Processing**: Integrate with payment gateway
- [ ] **Order Tracking**: Provide order tracking for customers
- [ ] **Notifications**: Send order status notifications
- [ ] **Cancellation**: Handle order cancellations
- [ ] **Returns**: Process returns and refunds
- [ ] **Audit Trail**: Log all order state changes

---

## Anti-patterns

### ❌ Don't: Trust Client Prices

```typescript
// ❌ Bad - Use client price
const order = await createOrder({
  items: [{ productId: '123', quantity: 1, price: clientPrice }]  // Can be manipulated!
})
```

```typescript
// ✅ Good - Get price from server
const items = await Promise.all(
  clientItems.map(async item => {
    const product = await getProduct(item.productId)
    return {
      productId: item.productId,
      quantity: item.quantity,
      price: product.price  // Server price
    }
  })
)
const order = await createOrder({ items })
```

### ❌ Don't: No Inventory Reservation

```typescript
// ❌ Bad - No reservation
const order = await createOrder(items)
// Inventory might be sold to another order!
```

```typescript
// ✅ Good - Reserve inventory
await reserveInventory(items)  // Lock inventory
const order = await createOrder(items)
// Inventory reserved, safe to proceed
```

### ❌ Don't: Invalid Status Transitions

```typescript
// ❌ Bad - Allow any status change
await updateOrderStatus(orderId, 'delivered')  // From 'pending'? Invalid!
```

```typescript
// ✅ Good - Validate transitions
const validTransitions = ORDER_STATUS_FLOW[currentStatus]
if (!validTransitions.includes(newStatus)) {
  throw new Error('Invalid status transition')
}
await updateOrderStatus(orderId, newStatus)
```

---

## Integration Points

- **Shopping Cart** (`30-ecommerce/shopping-cart/`) - Cart to order conversion
- **Payment Gateways** (`30-ecommerce/payment-gateways/`) - Payment processing
- **Inventory Management** (`30-ecommerce/inventory-management/`) - Stock management

---

## Further Reading

- [Order Management Best Practices](https://www.shopify.com/blog/order-management-system)
- [E-commerce Order Processing](https://www.bigcommerce.com/blog/order-management/)

- [Shopify Order API](https://shopify.dev/api/admin-graphql/latest/objects/Order)
- [WooCommerce Orders](https://woocommerce.github.io/woocommerce-rest-api-docs/#orders)
- [Magento 2 Order Management](https://devdocs.magento.com/guides/v2.4/rest/references/rest-orders.html)
- [BigCommerce Orders API](https://developer.bigcommerce.com/api-reference/orders/orders-api)
