---
name: harmonyos-app
description: HarmonyOS application development expert. Use when building HarmonyOS apps with ArkTS, ArkUI, Stage model, and distributed capabilities. Covers HarmonyOS NEXT (API 12+) best practices.
---
# HarmonyOS Application Development

## Core Principles

- **ArkTS First** — Use ArkTS with strict type safety, no `any` or dynamic types
- **Declarative UI** — Build UI with ArkUI's declarative components and state management
- **Stage Model** — Use modern Stage model (UIAbility), not legacy FA model
- **Distributed by Design** — Leverage cross-device capabilities from the start
- **Atomic Services** — Consider atomic services and cards for lightweight experiences
- **One-time Development** — Design for multi-device adaptation (phone, tablet, watch, TV)

---

## Hard Rules (Must Follow)

> These rules are mandatory. Violating them means the skill is not working correctly.

### No Dynamic Types

**ArkTS prohibits dynamic typing. Never use `any`, type assertions, or dynamic property access.**

```typescript
// ❌ FORBIDDEN: Dynamic types
let data: any = fetchData();
let obj: object = {};
obj['dynamicKey'] = value;  // Dynamic property access
(someVar as SomeType).method();  // Type assertion

// ✅ REQUIRED: Strict typing
interface UserData {
  id: string;
  name: string;
}
let data: UserData = fetchData();

// Use Record for dynamic keys
let obj: Record<string, string> = {};
obj['key'] = value;  // OK with Record type
```

### No Direct State Mutation

**Never mutate @State/@Prop variables directly in nested objects. Use immutable updates.**

```typescript
// ❌ FORBIDDEN: Direct mutation
@State user: User = { name: 'John', age: 25 };

updateAge() {
  this.user.age = 26;  // UI won't update!
}

// ✅ REQUIRED: Immutable update
updateAge() {
  this.user = { ...this.user, age: 26 };  // Creates new object, triggers UI update
}

// For arrays
@State items: string[] = ['a', 'b'];

// ❌ FORBIDDEN
this.items.push('c');  // UI won't update

// ✅ REQUIRED
this.items = [...this.items, 'c'];
```

### Stage Model Only

**Always use Stage model (UIAbility). Never use deprecated FA model (PageAbility).**

```typescript
// ❌ FORBIDDEN: FA Model (deprecated)
// config.json with "pages" array
export default {
  onCreate() { ... }  // PageAbility lifecycle
}

// ✅ REQUIRED: Stage Model
// module.json5 with abilities configuration
import { UIAbility } from '@kit.AbilityKit';

export default class EntryAbility extends UIAbility {
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    // Modern Stage model lifecycle
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    windowStage.loadContent('pages/Index');
  }
}
```

### Component Reusability

**Extract reusable UI into @Component. No inline complex UI in build() methods.**

```typescript
// ❌ FORBIDDEN: Monolithic build method
@Entry
@Component
struct MainPage {
  build() {
    Column() {
      // 200+ lines of inline UI...
      Row() {
        Image($r('app.media.avatar'))
        Column() {
          Text(this.user.name)
          Text(this.user.email)
        }
      }
      // More inline UI...
    }
  }
}

// ✅ REQUIRED: Extract components
@Component
struct UserCard {
  @Prop user: User;

  build() {
    Row() {
      Image($r('app.media.avatar'))
      Column() {
        Text(this.user.name)
        Text(this.user.email)
      }
    }
  }
}

@Entry
@Component
struct MainPage {
  @State user: User = { name: 'John', email: 'john@example.com' };

  build() {
    Column() {
      UserCard({ user: this.user })
    }
  }
}
```

---

## Quick Reference

### When to Use What

| Scenario | Pattern | Example |
|----------|---------|---------|
| Component-local state | @State | Counter, form inputs |
| Parent-to-child data | @Prop | Read-only child data |
| Two-way binding | @Link | Shared mutable state |
| Cross-component state | @Provide/@Consume | Theme, user context |
| Persistent state | PersistentStorage | User preferences |
| App-wide state | AppStorage | Global state |
| Complex state logic | @Observed/@ObjectLink | Nested object updates |

### State Decorator Selection

```
@State        → Component owns the state, triggers re-render on change
@Prop         → Parent passes value, child gets copy (one-way)
@Link         → Parent passes reference, child can modify (two-way)
@Provide      → Ancestor provides value to all descendants
@Consume      → Descendant consumes value from ancestor
@StorageLink  → Syncs with AppStorage, two-way binding
@StorageProp  → Syncs with AppStorage, one-way binding
@Observed     → Class decorator for observable objects
@ObjectLink   → Links to @Observed object in parent
```

---

## Project Structure

### Recommended Architecture

```
MyApp/
├── entry/                          # Main entry module
│   ├── src/main/
│   │   ├── ets/
│   │   │   ├── entryability/       # UIAbility definitions
│   │   │   │   └── EntryAbility.ets
│   │   │   ├── pages/              # Page components
│   │   │   │   ├── Index.ets
│   │   │   │   └── Detail.ets
│   │   │   ├── components/         # Reusable UI components
│   │   │   │   ├── common/         # Common components
│   │   │   │   └── business/       # Business-specific components
│   │   │   ├── viewmodel/          # ViewModels (MVVM)
│   │   │   ├── model/              # Data models
│   │   │   ├── service/            # Business logic services
│   │   │   ├── repository/         # Data access layer
│   │   │   ├── utils/              # Utility functions
│   │   │   └── constants/          # Constants and configs
│   │   ├── resources/              # Resources (strings, images)
│   │   └── module.json5            # Module configuration
│   └── build-profile.json5
├── common/                         # Shared library module
│   └── src/main/ets/
├── features/                       # Feature modules
│   ├── feature_home/
│   └── feature_profile/
└── build-profile.json5             # Project configuration
```

### Layer Separation

```
┌─────────────────────────────────────┐
│           UI Layer (Pages)          │  ArkUI Components
├─────────────────────────────────────┤
│         ViewModel Layer             │  State management, UI logic
├─────────────────────────────────────┤
│         Service Layer               │  Business logic
├─────────────────────────────────────┤
│        Repository Layer             │  Data access abstraction
├─────────────────────────────────────┤
│    Data Sources (Local/Remote)      │  Preferences, RDB, Network
└─────────────────────────────────────┘
```

---

## ArkUI Component Patterns

### Basic Component Structure

```typescript
import { router } from '@kit.ArkUI';

@Component
export struct ProductCard {
  // Props from parent
  @Prop product: Product;
  @Prop onAddToCart: (product: Product) => void;

  // Local state
  @State isExpanded: boolean = false;

  // Computed values (use getters)
  get formattedPrice(): string {
    return `¥${this.product.price.toFixed(2)}`;
  }

  // Lifecycle
  aboutToAppear(): void {
    console.info('ProductCard appearing');
  }

  aboutToDisappear(): void {
    console.info('ProductCard disappearing');
  }

  // Event handlers
  private handleTap(): void {
    router.pushUrl({ url: 'pages/ProductDetail', params: { id: this.product.id } });
  }

  private handleAddToCart(): void {
    this.onAddToCart(this.product);
  }

  // UI builder
  build() {
    Column() {
      Image(this.product.imageUrl)
        .width('100%')
        .aspectRatio(1)
        .objectFit(ImageFit.Cover)

      Text(this.product.name)
        .fontSize(16)
        .fontWeight(FontWeight.Medium)

      Text(this.formattedPrice)
        .fontSize(14)
        .fontColor('#FF6B00')

      Button('Add to Cart')
        .onClick(() => this.handleAddToCart())
    }
    .padding(12)
    .backgroundColor(Color.White)
    .borderRadius(8)
    .onClick(() => this.handleTap())
  }
}
```

### List with LazyForEach

```typescript
import { BasicDataSource } from '../utils/BasicDataSource';

class ProductDataSource extends BasicDataSource<Product> {
  private products: Product[] = [];

  totalCount(): number {
    return this.products.length;
  }

  getData(index: number): Product {
    return this.products[index];
  }

  addData(product: Product): void {
    this.products.push(product);
    this.notifyDataAdd(this.products.length - 1);
  }

  updateData(index: number, product: Product): void {
    this.products[index] = product;
    this.notifyDataChange(index);
  }
}

@Component
struct ProductList {
  private dataSource: ProductDataSource = new ProductDataSource();

  build() {
    List() {
      LazyForEach(this.dataSource, (product: Product, index: number) => {
        ListItem() {
          ProductCard({ product: product })
        }
      }, (product: Product) => product.id)  // Key generator
    }
    .lanes(2)  // Grid with 2 columns
    .cachedCount(4)  // Cache 4 items for smooth scrolling
  }
}
```

### Custom Dialog

```typescript
@CustomDialog
struct ConfirmDialog {
  controller: CustomDialogController;
  title: string = 'Confirm';
  message: string = '';
  onConfirm: () => void = () => {};

  build() {
    Column() {
      Text(this.title)
        .fontSize(20)
        .fontWeight(FontWeight.Bold)
        .margin({ bottom: 16 })

      Text(this.message)
        .fontSize(16)
        .margin({ bottom: 24 })

      Row() {
        Button('Cancel')
          .onClick(() => this.controller.close())
          .backgroundColor(Color.Gray)
          .margin({ right: 16 })

        Button('Confirm')
          .onClick(() => {
            this.onConfirm();
            this.controller.close();
          })
      }
    }
    .padding(24)
  }
}

// Usage
@Entry
@Component
struct MainPage {
  dialogController: CustomDialogController = new CustomDialogController({
    builder: ConfirmDialog({
      title: 'Delete Item',
      message: 'Are you sure you want to delete this item?',
      onConfirm: () => this.deleteItem()
    }),
    autoCancel: true
  });

  private deleteItem(): void {
    // Delete logic
  }

  build() {
    Button('Delete')
      .onClick(() => this.dialogController.open())
  }
}
```

---


## Extended Reference

Detailed material starting at `## State Management Patterns` has been moved to [`reference/extended.md`](reference/extended.md) to keep this skill concise. Load that reference when the task requires the moved examples, command catalogs, checklists, platform details, or implementation templates.
