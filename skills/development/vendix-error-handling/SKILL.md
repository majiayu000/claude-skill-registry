---
name: vendix-error-handling
description: Error handling patterns.
metadata:
  scope: [root]
  auto_invoke: "Handling Errors"
---
# Vendix Error Handling Pattern

> **Consistent Error Handling** - Try-catch patterns, respuestas de error y logging estandarizado.

## 🎯 Error Handling Principles

**Siempre manejar errores en todas las capas:**
- Service layer: Lógica de negocio
- Controller layer: Respuestas HTTP
- Frontend services: Notificaciones al usuario
- Componentes: Estados de error

---

## 🔧 Backend Error Handling

### Service Layer Pattern

```typescript
async createOrder(create_order_dto: CreateOrderDto): Promise<Order> {
  try {
    // Validate business rules
    if (!create_order_dto.items || create_order_dto.items.length === 0) {
      throw new BadRequestException('Order must have at least one item');
    }

    // Check product availability
    for (const item of create_order_dto.items) {
      const product = await this.prisma.products.findUnique({
        where: { id: item.product_id },
      });

      if (!product) {
        throw new NotFoundException(`Product ${item.product_id} not found`);
      }

      if (product.stock_quantity < item.quantity) {
        throw new BadRequestException(
          `Insufficient stock for product: ${product.name}`
        );
      }
    }

    // Create order with transaction
    const order = await this.prisma.$transaction(async (tx) => {
      const new_order = await tx.sales_orders.create({
        data: {
          customer_id: create_order_dto.customer_id,
          total_amount: create_order_dto.total_amount,
          organization_id: this.context.organization_id,
          store_id: this.context.store_id,
        },
      });

      // Create order items
      await Promise.all(
        create_order_dto.items.map(item =>
          tx.sales_order_items.create({
            data: {
              order_id: new_order.id,
              product_id: item.product_id,
              quantity: item.quantity,
              unit_price: item.unit_price,
              subtotal: item.quantity * item.unit_price,
            },
          })
        )
      );

      // Update stock
      await Promise.all(
        create_order_dto.items.map(item =>
          tx.products.update({
            where: { id: item.product_id },
            data: {
              stock_quantity: {
                decrement: item.quantity,
              },
            },
          })
        )
      );

      return new_order;
    });

    return order;

  } catch (error) {
    // Handle Prisma-specific errors
    if (error.code === 'P2002') {
      throw new ConflictException('Duplicate entry');
    }

    if (error.code === 'P2025') {
      throw new NotFoundException('Record not found');
    }

    // Re-throw HTTP exceptions
    if (error instanceof HttpException) {
      throw error;
    }

    // Log unexpected errors
    console.error('Unexpected error creating order:', error);

    // Throw generic error
    throw new InternalServerErrorException(
      'An error occurred while creating the order'
    );
  }
}
```

---

### Controller Layer Pattern

```typescript
@Post()
async createOrder(@Body() create_order_dto: CreateOrderDto) {
  try {
    const order = await this.order_service.createOrder(create_order_dto);
    return this.response_service.success(order, 'Order created successfully');
  } catch (error) {
    // ResponseService handles error formatting
    if (error instanceof HttpException) {
      throw error;  // Let exception filter handle it
    }

    return this.response_service.error(
      'Failed to create order',
      'ORDER_CREATION_FAILED',
      error.message
    );
  }
}
```

---

### Prisma Error Codes

| Code | Description | Handling |
|------|-------------|----------|
| P2002 | Unique constraint violation | `ConflictException` |
| P2025 | Record not found | `NotFoundException` |
| P2003 | Foreign key constraint violation | `BadRequestException` |
| P2014 | Changing required relation would violate constraint | `BadRequestException` |
| P2006 | Invalid value for field type | `BadRequestException` |

---

## 🌐 Frontend Error Handling

### Service Layer Pattern

```typescript
getOrders(filters?: OrderFilters): Observable<Order[]> {
  const params = new HttpParams({ fromObject: filters });

  return this.http.get<Order[]>(this.api_url, { params }).pipe(
    catchError((error: HttpErrorResponse) => {
      // Handle specific error codes
      if (error.status === 401) {
        this.toast_service.error('Session expired. Please login again.');
        this.router.navigate(['/auth/login']);
      } else if (error.status === 403) {
        this.toast_service.error('You do not have permission to view orders.');
      } else if (error.status === 404) {
        this.toast_service.error('Orders not found.');
      } else if (error.status >= 500) {
        this.toast_service.error('Server error. Please try again later.');
      } else {
        this.toast_service.error(
          error.error?.message || 'An error occurred while loading orders'
        );
      }

      // Return empty array or rethrow
      return of([]);
    })
  );
}
```

---

### Component Error Handling

```typescript
@Component({
  selector: 'app-order-list',
  template: `
    @if (isLoading()) {
      <div class="loading">Loading...</div>
    } @else if (error()) {
      <div class="error">
        <p>{{ error() }}</p>
        <button (click)="retry()">Retry</button>
      </div>
    } @else if (orders().length === 0) {
      <app-empty-state message="No orders found" />
    } @else {
      <div *ngFor="let order of orders()">
        {{ order.id }}
      </div>
    }
  `,
})
export class OrderListComponent implements OnInit {
  private order_service = inject(OrderService);

  orders = signal<Order[]>([]);
  isLoading = signal<boolean>(false);
  error = signal<string | null>(null);

  ngOnInit() {
    this.loadOrders();
  }

  loadOrders() {
    this.isLoading.set(true);
    this.error.set(null);

    this.order_service.getOrders().subscribe({
      next: (data) => {
        this.orders.set(data);
        this.isLoading.set(false);
      },
      error: (err) => {
        this.error.set(err.message);
        this.isLoading.set(false);
      },
    });
  }

  retry() {
    this.loadOrders();
  }
}
```

---

## 🔔 Toast Notifications

### Using ToastService

```typescript
// Success
this.toast_service.success('Order created successfully');

// Error
this.toast_service.error('Failed to create order');

// Warning
this.toast_service.warning('Stock is low for some products');

// Info
this.toast_service.info('Order is being processed');

// Custom duration
this.toast_service.show({
  variant: 'success',
  message: 'Order completed',
  duration: 5000,
});
```

---

## 📝 Error Logging

### Backend Logging

```typescript
import { Logger } from '@nestjs/common';

export class OrderService {
  private logger = new Logger(OrderService.name);

  createOrder(dto: CreateOrderDto) {
    try {
      this.logger.log(`Creating order for customer ${dto.customer_id}`);

      const order = await this.executeOrderCreation(dto);

      this.logger.log(`Order ${order.id} created successfully`);

      return order;
    } catch (error) {
      this.logger.error(
        `Failed to create order: ${error.message}`,
        error.stack
      );
      throw error;
    }
  }
}
```

### Frontend Logging

```typescript
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class LoggingService {
  private is_production = environment.production;

  log(message: string, data?: any) {
    if (!this.is_production) {
      console.log(`[LOG] ${message}`, data);
    }
  }

  warn(message: string, data?: any) {
    console.warn(`[WARN] ${message}`, data);
  }

  error(message: string, error?: any) {
    console.error(`[ERROR] ${message}`, error);

    // Send to error tracking service in production
    if (this.is_production) {
      this.sendToErrorTracking(message, error);
    }
  }

  private sendToErrorTracking(message: string, error: any) {
    // Send to Sentry, LogRocket, etc.
  }
}
```

---

## 🎯 Error Response Format

### Standard Error Response

```typescript
interface ErrorResponse {
  success: false;
  error: {
    message: string;
    code?: string;
    details?: any;
    stack?: string;  // Only in development
  };
}

// Example
{
  "success": false,
  "error": {
    "message": "Product not found",
    "code": "PRODUCT_NOT_FOUND",
    "details": {
      "product_id": 123
    }
  }
}
```

---

## 🔍 Key Files Reference

| File | Purpose |
|------|---------|
| `common/responses/response.service.ts` | Error formatting |
| `common/filters/http-exception.filter.ts` | Global error filter |
| `core/interceptors/error.interceptor.ts` | Frontend error handling |
| `shared/components/toast/toast.service.ts` | User notifications |

---

## Related Skills

- `vendix-validation` - Validation patterns
- `vendix-backend-api` - API response patterns
- `vendix-frontend-state` - Frontend service patterns
