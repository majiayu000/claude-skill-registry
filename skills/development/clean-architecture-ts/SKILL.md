---
name: clean-architecture-ts
description: Best practices for implementing Clean Architecture in Remix/TypeScript apps. Covers Service Layer, Repository Pattern, and Dependency Injection.
---

# Clean Architecture for Remix/TypeScript Apps

As Remix apps grow, `loader` and `action` functions can become bloated "God Functions". This skill emphasizes separation of concerns.

## 1. The Layers

### A. The Web Layer (Loaders/Actions)
**Responsibility**: Parsing requests, input validation (Zod), and returning Responses (JSON/Redirect).
**Rule**: NO business logic here. Only orchestration.

```typescript
// app/routes/app.products.update.ts
export const action = async ({ request }: ActionFunctionArgs) => {
  const { shop } = await authenticate.admin(request);
  const formData = await request.formData();
  
  // 1. Validate Input
  const input = validateProductUpdate(formData);

  // 2. Call Service
  const updatedProduct = await ProductService.updateProduct(shop, input);

  // 3. Return Response
  return json({ product: updatedProduct });
};
```

### B. The Service Layer (Business Logic)
**Responsibility**: The "What". Rules, calculations, error handling, complex flows.
**Rule**: Framework agnostic. Should not know about "Request" or "Response" objects.

```typescript
// app/services/product.service.ts
export class ProductService {
  static async updateProduct(shop: string, input: ProductUpdateInput) {
    // Business Rule: Can't update archived products
    const existing = await ProductRepository.findByShopAndId(shop, input.id);
    if (existing.status === 'ARCHIVED') {
      throw new BusinessError("Cannot update archived product");
    }

    // Business Logic
    const result = await ProductRepository.save({
      ...existing,
      ...input,
      updatedAt: new Date()
    });

    return result;
  }
}
```

### C. The Repository Layer (Data Access)
**Responsibility**: The "How". interaction with Database (Prisma), APIs (Shopify Admin), or File System.
**Rule**: Only this layer touches the DB/API.

```typescript
// app/repositories/product.repository.ts
export class ProductRepository {
  static async findByShopAndId(shop: string, id: string) {
    return prisma.product.findFirstOrThrow({
      where: { shop, id: BigInt(id) }
    });
  }
}
```

## 2. Directory Structure

```
app/
  routes/         # Web Layer
  services/       # Business Logic
  repositories/   # Data Access (DB/API)
  models/         # Domain Types / Interfaces
  utils/          # Pure functions (math, string manipulation)
```

## 3. Dependency Injection (Optional but Recommended)
For complex apps, use a container like `tsyringe` to manage dependencies, especially for testing (mocking Repositories).

```typescript
// app/services/order.service.ts
@injectable()
export class OrderService {
  constructor(
    @inject(OrderRepository) private orderRepo: OrderRepository,
    @inject(ShopifyClient) private shopify: ShopifyClient
  ) {}
}
```

## 4. Error Handling
Create custom Error classes to differentiate between "Bad Request" (User error) and "Server Error" (System error).

```typescript
// app/errors/index.ts
export class BusinessError extends Error {
  public code = 422;
}

export class NotFoundError extends Error {
  public code = 404;
}
```
Refactor your `loader`/`action` to catch these errors and return appropriate HTTP status codes.
