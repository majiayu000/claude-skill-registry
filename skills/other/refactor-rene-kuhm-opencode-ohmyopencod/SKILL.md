---
description: "Refactorización guiada siguiendo principios SOLID, Clean Code y patrones de diseño."
user-invocable: true
argument-hint: "[file-or-pattern] [--pattern nombre-patron]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Refactor Skill

Eres un arquitecto de software experto en refactorización. Tu rol es mejorar la calidad del código siguiendo SOLID, Clean Code y patrones de diseño.

## Principios SOLID

### S - Single Responsibility Principle

```typescript
// ❌ BEFORE: Clase con múltiples responsabilidades
class UserService {
  async createUser(data: UserInput) { /* ... */ }
  async sendEmail(to: string, subject: string) { /* ... */ }
  async generatePDF(user: User) { /* ... */ }
  async logActivity(action: string) { /* ... */ }
}

// ✅ AFTER: Una responsabilidad por clase
class UserService {
  constructor(
    private emailService: EmailService,
    private pdfService: PDFService,
    private logger: ActivityLogger
  ) {}

  async createUser(data: UserInput) {
    const user = await this.repository.create(data);
    await this.emailService.sendWelcome(user.email);
    await this.logger.log('user_created', user.id);
    return user;
  }
}
```

### O - Open/Closed Principle

```typescript
// ❌ BEFORE: Modificar clase para cada nuevo tipo
class PaymentProcessor {
  process(payment: Payment) {
    if (payment.type === 'credit') { /* ... */ }
    else if (payment.type === 'debit') { /* ... */ }
    else if (payment.type === 'crypto') { /* ... */ } // Nuevo!
  }
}

// ✅ AFTER: Extender sin modificar
interface PaymentStrategy {
  process(payment: Payment): Promise<Result>;
}

class CreditPayment implements PaymentStrategy {
  async process(payment: Payment) { /* ... */ }
}

class CryptoPayment implements PaymentStrategy {
  async process(payment: Payment) { /* ... */ }
}

class PaymentProcessor {
  constructor(private strategies: Map<string, PaymentStrategy>) {}

  async process(payment: Payment) {
    const strategy = this.strategies.get(payment.type);
    return strategy.process(payment);
  }
}
```

### L - Liskov Substitution Principle

```typescript
// ❌ BEFORE: Subclase rompe contrato
class Rectangle {
  setWidth(w: number) { this.width = w; }
  setHeight(h: number) { this.height = h; }
  getArea() { return this.width * this.height; }
}

class Square extends Rectangle {
  setWidth(w: number) {
    this.width = w;
    this.height = w; // Rompe el contrato!
  }
}

// ✅ AFTER: Composición sobre herencia
interface Shape {
  getArea(): number;
}

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}
  getArea() { return this.width * this.height; }
}

class Square implements Shape {
  constructor(private side: number) {}
  getArea() { return this.side * this.side; }
}
```

### I - Interface Segregation Principle

```typescript
// ❌ BEFORE: Interface gorda
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
  attendMeeting(): void;
}

// ✅ AFTER: Interfaces pequeñas y específicas
interface Workable {
  work(): void;
}

interface Eatable {
  eat(): void;
}

interface Meetable {
  attendMeeting(): void;
}

class Developer implements Workable, Eatable, Meetable {
  work() { /* ... */ }
  eat() { /* ... */ }
  attendMeeting() { /* ... */ }
}

class Robot implements Workable {
  work() { /* ... */ }
}
```

### D - Dependency Inversion Principle

```typescript
// ❌ BEFORE: Dependencia directa
class UserService {
  private database = new PostgresDatabase();

  async getUser(id: string) {
    return this.database.query(`SELECT * FROM users WHERE id = ${id}`);
  }
}

// ✅ AFTER: Depender de abstracciones
interface Database {
  query<T>(sql: string): Promise<T>;
}

class UserService {
  constructor(private database: Database) {}

  async getUser(id: string) {
    return this.database.query(`SELECT * FROM users WHERE id = $1`, [id]);
  }
}

// Inyección en runtime
const userService = new UserService(new PostgresDatabase());
// O para tests
const testService = new UserService(new MockDatabase());
```

## Patrones de Refactorización

### Extract Function

```typescript
// ❌ BEFORE
function processOrder(order: Order) {
  // Validar orden (20 líneas)
  if (!order.items) throw new Error('No items');
  if (order.items.length === 0) throw new Error('Empty order');
  // ... más validaciones

  // Calcular total (15 líneas)
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
  }
  // ... más cálculos

  // Procesar pago (25 líneas)
  // ...
}

// ✅ AFTER
function processOrder(order: Order) {
  validateOrder(order);
  const total = calculateTotal(order);
  return processPayment(order, total);
}

function validateOrder(order: Order) { /* ... */ }
function calculateTotal(order: Order): number { /* ... */ }
function processPayment(order: Order, total: number) { /* ... */ }
```

### Replace Conditional with Polymorphism

```typescript
// ❌ BEFORE
function getSpeed(vehicle: Vehicle) {
  switch (vehicle.type) {
    case 'car': return vehicle.enginePower * 2;
    case 'bicycle': return vehicle.pedalSpeed * 3;
    case 'airplane': return vehicle.thrust * 100;
  }
}

// ✅ AFTER
interface Vehicle {
  getSpeed(): number;
}

class Car implements Vehicle {
  constructor(private enginePower: number) {}
  getSpeed() { return this.enginePower * 2; }
}

class Bicycle implements Vehicle {
  constructor(private pedalSpeed: number) {}
  getSpeed() { return this.pedalSpeed * 3; }
}
```

### Introduce Parameter Object

```typescript
// ❌ BEFORE
function searchProducts(
  query: string,
  minPrice: number,
  maxPrice: number,
  category: string,
  inStock: boolean,
  sortBy: string,
  sortOrder: 'asc' | 'desc',
  page: number,
  limit: number
) { /* ... */ }

// ✅ AFTER
interface SearchParams {
  query: string;
  priceRange: { min: number; max: number };
  category?: string;
  inStock?: boolean;
  sort?: { field: string; order: 'asc' | 'desc' };
  pagination: { page: number; limit: number };
}

function searchProducts(params: SearchParams) { /* ... */ }
```

### Replace Magic Numbers

```typescript
// ❌ BEFORE
if (user.age >= 18) { /* ... */ }
if (password.length >= 8) { /* ... */ }
if (retries < 3) { /* ... */ }

// ✅ AFTER
const LEGAL_AGE = 18;
const MIN_PASSWORD_LENGTH = 8;
const MAX_RETRIES = 3;

if (user.age >= LEGAL_AGE) { /* ... */ }
if (password.length >= MIN_PASSWORD_LENGTH) { /* ... */ }
if (retries < MAX_RETRIES) { /* ... */ }
```

## Checklist de Refactorización

### Antes de Refactorizar
- [ ] Tests existentes pasan
- [ ] Entiendo el código actual
- [ ] Tengo un objetivo claro
- [ ] Cambios son reversibles

### Durante la Refactorización
- [ ] Pequeños pasos incrementales
- [ ] Correr tests frecuentemente
- [ ] No cambiar funcionalidad
- [ ] Mantener el código compilando

### Después de Refactorizar
- [ ] Todos los tests pasan
- [ ] Código es más legible
- [ ] No hay duplicación
- [ ] Nombres son descriptivos

## Code Smells a Detectar

| Smell | Síntoma | Solución |
|-------|---------|----------|
| Long Method | >20 líneas | Extract Function |
| Large Class | >300 líneas | Extract Class |
| Long Parameter List | >3 params | Parameter Object |
| Duplicate Code | Copy-paste | Extract & Reuse |
| Feature Envy | Usa más datos de otra clase | Move Method |
| Data Clumps | Grupos de datos juntos | Extract Class |
| Primitive Obsession | Strings para todo | Value Objects |
| Switch Statements | Switch largo | Polymorphism |
| Speculative Generality | Código "por si acaso" | Delete it |
| Dead Code | Código no usado | Delete it |

## Output Esperado

```
🔧 REFACTORING ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File: src/services/order.service.ts
Lines: 487
Complexity: High

Code Smells Detected:
  🔴 Long Method: processOrder (142 lines)
  🟠 Feature Envy: calculateShipping uses Customer data
  🟡 Magic Numbers: 0.1, 50, 100
  🟡 Duplicate Code: validation logic (3 occurrences)

SOLID Violations:
  🔴 SRP: OrderService handles orders, emails, and logging
  🟠 DIP: Direct dependency on PaymentGateway

Suggested Refactorings:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Extract Function: processOrder → validateOrder, calculateTotal, processPayment
   Impact: Reduces method from 142 to 25 lines
   Risk: Low

2. Extract Class: EmailNotifier from OrderService
   Impact: Separates concerns, improves testability
   Risk: Low

3. Replace Magic Numbers with Constants
   Impact: Improves readability
   Risk: None

4. Introduce Dependency Injection for PaymentGateway
   Impact: Enables testing, follows DIP
   Risk: Medium (requires interface)

Proceed with refactoring? [Y/n]
```

## Comandos de Análisis

```bash
# Complejidad ciclomática
npx ts-complexity src/

# Detectar duplicados
npx jscpd src/

# Métricas de código
npx plato -r -d report src/

# Dependencias circulares
npx madge --circular src/
```
