---
name: vendix-frontend-component
description: Angular component structure rules.
metadata:
  scope: [root]
  auto_invoke: "Creating Angular components"
---
# Vendix Frontend Component Pattern

> **CRITICAL RULE** - **TODOS** los componentes Angular DEBEN estar en carpetas, sin importar si son standalone o modulares, por muy pequeños que sean.

## 🚨 THE GOLDEN RULE

**EVERY Angular component MUST be in a folder, ALWAYS, NO EXCEPTIONS**

```
❌ WRONG:
app-button.component.ts

✅ CORRECT:
button/
├── button.component.ts
├── button.component.html
└── button.component.scss
```

---
metadata:
  scope: [root]
  auto_invoke: "Creating Angular components"

## 📁 Component Folder Structure

### Standard Component Structure

```
{component-name}/
├── {component-name}.component.ts       # Component logic
├── {component-name}.component.html     # Template (optional if inline)
├── {component-name}.component.scss     # Styles (optional if using global)
└── {component-name}.component.spec.ts  # Tests (optional)
```

**Naming Rules:**
- Folder: **kebab-case** (ej: `product-list/`)
- Files: **kebab-case** with suffix (ej: `product-list.component.ts`)
- Class: **PascalCase** (ej: `export class ProductListComponent`)
- Selector: **kebab-case** with `app-` prefix (ej: `app-product-list`)

---

## 🔩 Standalone Component Pattern

### Standalone Component

**File:** `product-card/product-card.component.ts`

```typescript
import { Component, input, output, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Product } from '@/shared/interfaces/product.interface';

@Component({
  selector: 'app-product-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './product-card.component.html',
  styleUrls: ['./product-card.component.scss'],
})
export class ProductCardComponent {
  // Inputs (Angular 20 signals)
  readonly product = input.required<Product>();
  readonly isLoading = input<boolean>(false);

  // Outputs
  readonly addToCart = output<Product>();
  readonly viewDetails = output<Product>();

  // Computed properties
  readonly displayName = computed(() => this.product().name);
  readonly displayPrice = computed(() =>
    `$${this.product().base_price.toFixed(2)}`
  );

  // Actions
  onAddToCart() {
    this.addToCart.emit(this.product());
  }

  onViewDetails() {
    this.viewDetails.emit(this.product());
  }
}
```

### Template

**File:** `product-card/product-card.component.html`

```html
<div class="product-card" [class.loading]="isLoading()">
  <img [src]="product().images[0]" [alt]="displayName()" />
  <h3>{{ displayName() }}</h3>
  <p class="price">{{ displayPrice() }}</p>
  <button (click)="onAddToCart()">Add to Cart</button>
  <button (click)="onViewDetails()">View Details</button>
</div>
```

---

## 📦 Module-Based Component Pattern

### Component with Module

**File:** `user-profile/user-profile.component.ts`

```typescript
import { Component } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.scss'],
})
export class UserProfileComponent {
  // Component logic
}
```

**File:** `user-profile/user-profile.module.ts`

```typescript
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { UserProfileComponent } from './user-profile.component';

@NgModule({
  declarations: [UserProfileComponent],
  imports: [CommonModule, ReactiveFormsModule],
  exports: [UserProfileComponent],
})
export class UserProfileModule {}
```

**When to use modules:**
- Very complex components
- Components with many dependencies
- Components that need better modularity
- Legacy code being migrated

---

## 🎯 Component Size Examples

### Small Component (Still in folder!)

**Folder:** `icon/`

```
icon/
├── icon.component.ts
├── icon.component.html
└── icon.component.scss
```

**File:** `icon/icon.component.ts`

```typescript
import { Component, input } from '@angular/core';

@Component({
  selector: 'app-icon',
  standalone: true,
  templateUrl: './icon.component.html',
  styleUrls: ['./icon.component.scss'],
})
export class IconComponent {
  readonly name = input.required<string>();
  readonly size = input<number>(16);
}
```

---

### Medium Component

**Folder:** `product-list/`

```
product-list/
├── product-list.component.ts
├── product-list.component.html
├── product-list.component.scss
└── product-list.component.spec.ts
```

**File:** `product-list/product-list.component.ts`

```typescript
import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProductService } from '@/shared/services/product.service';
import { Product } from '@/shared/interfaces/product.interface';

@Component({
  selector: 'app-product-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.scss'],
})
export class ProductListComponent implements OnInit, OnDestroy {
  products: Product[] = [];
  isLoading = false;
  private destroy$ = new Subject<void>();

  constructor(private product_service: ProductService) {}

  ngOnInit() {
    this.loadProducts();
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }

  private loadProducts() {
    this.isLoading = true;
    this.product_service
      .getProducts()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (data) => {
          this.products = data;
          this.isLoading = false;
        },
        error: (error) => {
          console.error('Error loading products:', error);
          this.isLoading = false;
        },
      });
  }
}
```

---

### Large Component (with sub-components)

**Folder:** `checkout/`

```
checkout/
├── checkout.component.ts
├── checkout.component.html
├── checkout.component.scss
├── components/
│   ├── checkout-items/
│   │   ├── checkout-items.component.ts
│   │   ├── checkout-items.component.html
│   │   └── checkout-items.component.scss
│   ├── checkout-shipping/
│   │   ├── checkout-shipping.component.ts
│   │   ├── checkout-shipping.component.html
│   │   └── checkout-shipping.component.scss
│   └── checkout-payment/
│       ├── checkout-payment.component.ts
│       ├── checkout-payment.component.html
│       └── checkout-payment.component.scss
└── services/
    └── checkout.service.ts
```

---

## 🔗 Component Communication

### Parent to Child (Input)

```typescript
// Parent
@Component({
  template: `
    <app-product-card [product]="selectedProduct" />
  `,
})
export class ParentComponent {
  selectedProduct: Product = { ... };
}

// Child
export class ProductCardComponent {
  readonly product = input.required<Product>();
}
```

### Child to Parent (Output)

```typescript
// Child
export class ProductCardComponent {
  readonly addToCart = output<Product>();

  onAddToCart() {
    this.addToCart.emit(this.product());
  }
}

// Parent
@Component({
  template: `
    <app-product-card
      [product]="product"
      (addToCart)="handleAddToCart($event)"
    />
  `,
})
export class ParentComponent {
  handleAddToCart(product: Product) {
    console.log('Added to cart:', product);
  }
}
```

### Two-Way Binding

```typescript
// Child
export class InputComponent {
  readonly value = input<string>('');
  readonly valueChange = output<string>();

  updateValue(new_value: string) {
    this.valueChange.emit(new_value);
  }
}

// Parent
@Component({
  template: `
    <app-input [(value)]="searchQuery" />
  `,
})
export class ParentComponent {
  searchQuery = '';
}
```

---

## 🎨 Component Styles

### Component-Specific Styles

**File:** `product-card/product-card.component.scss`

```scss
:host {
  display: block;
}

.product-card {
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;

  &:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  img {
    width: 100%;
    height: 200px;
    object-fit: cover;
  }
}
```

### Global Styles Reference

```typescript
@Component({
  styleUrls: [
    './product-card.component.scss',
    '@/styles.scss',  // Global styles
  ],
})
```

---

## 📋 Best Practices

### 1. ALWAYS Use Folders

```typescript
// ❌ WRONG - Single file
app-button.component.ts

// ✅ CORRECT - Folder structure
button/
├── button.component.ts
├── button.component.html
└── button.component.scss
```

### 2. Use Angular 20 Signals

```typescript
// ✅ CORRECT - Angular 20 signals
readonly product = input.required<Product>();
readonly isLoading = input<boolean>(false);

// ❌ OUTDATED - Old decorators
@Input() product!: Product;
@Input() isLoading = false;
```

### 3. Proper Lifecycle Management

```typescript
export class ProductListComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  ngOnInit() {
    this.loadData()
      .pipe(takeUntil(this.destroy$))
      .subscribe();
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

### 4. Change Detection Strategy

```typescript
@Component({
  selector: 'app-product-card',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,  // Performance
  template: '...',
})
export class ProductCardComponent {}
```

---

## 🔍 Key Files Reference

| File | Purpose |
|------|---------|
| `shared/components/index.ts` | Centralized component exports |
| `app/shared/components/*/` | Reusable components |
| `app/private/modules/*/components/` | Module-specific components |

---

## Related Skills

- `vendix-frontend-module` - Module structure patterns
- `vendix-frontend-routing` - Routing patterns
- `vendix-naming-conventions` - Naming conventions (CRITICAL)
- `vendix-build-verification` - Build verification (CRITICAL)
