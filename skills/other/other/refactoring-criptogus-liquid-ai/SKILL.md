---
name: refactoring
description: Refactoring - Padrões e técnicas de refatoração segura e OBJETIVA
version: 2.0.0
category: workflow
triggers:
  - refactoring
  - refatoração
  - refatorar
  - código legado
  - legacy code
  - code smell
  - clean code
  - technical debt
  - dívida técnica
  - melhorar código
tools: []
author: liquid-ai
---

# Refactoring - Melhorando Código Existente

Esta skill ajuda você a refatorar código de forma SEGURA e OBJETIVA.

## Regra Fundamental: OBJETIVIDADE

```
┌─────────────────────────────────────────────────────────────┐
│  🚨 REGRA MAIS IMPORTANTE: SEJA OBJETIVO E ÚTIL            │
│                                                              │
│  ❌ NUNCA RESPONDA ASSIM:                                   │
│  "Existem várias formas de melhorar esse código..."        │
│  "Depende do contexto..."                                  │
│  "Você poderia considerar..."                              │
│                                                              │
│  ✅ SEMPRE RESPONDA ASSIM:                                  │
│  "Extraia esse bloco para função: extractPaymentLogic()"   │
│  "Esse código tem 3 problemas: [lista específica]"         │
│  "Refatore assim: [código exato]"                          │
│                                                              │
│  DÊ O CÓDIGO REFATORADO, NÃO APENAS SUGESTÕES.             │
└─────────────────────────────────────────────────────────────┘
```

## Princípio Fundamental

```
┌─────────────────────────────────────────────────────────────┐
│  "Refactoring is the process of changing a software        │
│   system in such a way that it does not alter the          │
│   external behavior of the code yet improves its           │
│   internal structure." - Martin Fowler                     │
│                                                              │
│  COMPORTAMENTO IGUAL + ESTRUTURA MELHOR = REFACTORING      │
│                                                              │
│  Se muda comportamento → NÃO é refactoring                 │
│  Se não melhora estrutura → NÃO é refactoring              │
└─────────────────────────────────────────────────────────────┘
```

## Quando Usar Esta Skill

- Código difícil de entender ou modificar
- Code smells identificados
- Antes de adicionar nova feature
- Depois de testes passando
- Technical debt prioritizado

## O Ciclo de Refactoring

```
┌─────────────────────────────────────────────────────────────┐
│  1. GARANTA QUE TESTES EXISTEM E PASSAM                     │
│     → Se não tem testes, escreva primeiro                  │
│     → Testes são sua rede de segurança                     │
│                                                              │
│  2. FAÇA UMA PEQUENA MUDANÇA                                │
│     → Uma mudança por vez                                  │
│     → Se algo quebrar, você sabe o quê                     │
│                                                              │
│  3. RODE OS TESTES                                           │
│     → Todos devem passar                                   │
│     → Se falhar: desfaça e tente de novo                   │
│                                                              │
│  4. REPITA                                                   │
│     → Pequenos passos seguros                              │
│     → Commit frequente                                     │
│                                                              │
│  "Make the change easy, then make the easy change."        │
│  - Kent Beck                                                │
└─────────────────────────────────────────────────────────────┘
```

## Code Smells e Soluções

### 1. Função Muito Longa

```typescript
// ❌ ANTES: Função de 100+ linhas
async function processOrder(order: Order) {
  // validação (20 linhas)
  if (!order.items) throw new Error('No items');
  if (!order.customer) throw new Error('No customer');
  // ... mais validações ...

  // cálculo de preço (30 linhas)
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
    // ... descontos, impostos ...
  }

  // processamento de pagamento (30 linhas)
  const payment = await chargeCard(order.customer.card, total);
  // ... tratamento de erros ...

  // envio de notificações (20 linhas)
  await sendEmail(order.customer.email, 'Order confirmed');
  // ... mais notificações ...

  return { orderId: order.id, total, payment };
}

// ✅ DEPOIS: Funções pequenas e focadas
async function processOrder(order: Order) {
  validateOrder(order);
  const total = calculateTotal(order);
  const payment = await processPayment(order.customer, total);
  await sendNotifications(order, payment);
  return { orderId: order.id, total, payment };
}

function validateOrder(order: Order): void {
  if (!order.items?.length) throw new Error('No items');
  if (!order.customer) throw new Error('No customer');
}

function calculateTotal(order: Order): number {
  return order.items.reduce((total, item) =>
    total + item.price * item.quantity, 0);
}

async function processPayment(customer: Customer, total: number) {
  return await chargeCard(customer.card, total);
}

async function sendNotifications(order: Order, payment: Payment) {
  await sendEmail(order.customer.email, 'Order confirmed');
}
```

### 2. Código Duplicado

```typescript
// ❌ ANTES: Lógica duplicada
function getUserDisplayName(user: User): string {
  if (user.firstName && user.lastName) {
    return `${user.firstName} ${user.lastName}`;
  }
  return user.email.split('@')[0];
}

function getAdminDisplayName(admin: Admin): string {
  if (admin.firstName && admin.lastName) {
    return `${admin.firstName} ${admin.lastName}`;
  }
  return admin.email.split('@')[0];
}

// ✅ DEPOIS: Extraia para função genérica
interface HasName {
  firstName?: string;
  lastName?: string;
  email: string;
}

function getDisplayName(person: HasName): string {
  if (person.firstName && person.lastName) {
    return `${person.firstName} ${person.lastName}`;
  }
  return person.email.split('@')[0];
}

// Uso
getDisplayName(user);
getDisplayName(admin);
```

### 3. Muitos Parâmetros

```typescript
// ❌ ANTES: 7 parâmetros
function createUser(
  firstName: string,
  lastName: string,
  email: string,
  phone: string,
  address: string,
  city: string,
  country: string
) {
  // ...
}

// ✅ DEPOIS: Objeto de parâmetros
interface CreateUserParams {
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  address?: Address;
}

interface Address {
  street: string;
  city: string;
  country: string;
}

function createUser(params: CreateUserParams) {
  const { firstName, lastName, email, phone, address } = params;
  // ...
}

// Uso: mais legível, ordem não importa
createUser({
  firstName: 'João',
  lastName: 'Silva',
  email: 'joao@email.com',
  address: {
    street: 'Rua A',
    city: 'São Paulo',
    country: 'Brasil'
  }
});
```

### 4. Condicionais Complexos

```typescript
// ❌ ANTES: Nested ifs confusos
function getDiscount(user: User, order: Order): number {
  if (user.isPremium) {
    if (order.total > 1000) {
      if (order.items.length > 5) {
        return 0.25;
      } else {
        return 0.20;
      }
    } else {
      return 0.15;
    }
  } else {
    if (order.total > 1000) {
      return 0.10;
    } else {
      return 0;
    }
  }
}

// ✅ DEPOIS: Early returns + funções descritivas
function getDiscount(user: User, order: Order): number {
  if (!user.isPremium) {
    return order.total > 1000 ? 0.10 : 0;
  }

  if (order.total <= 1000) {
    return 0.15;
  }

  return order.items.length > 5 ? 0.25 : 0.20;
}

// OU: Ainda melhor com tabela de decisão
const DISCOUNT_RULES = [
  { premium: true,  minTotal: 1000, minItems: 5, discount: 0.25 },
  { premium: true,  minTotal: 1000, minItems: 0, discount: 0.20 },
  { premium: true,  minTotal: 0,    minItems: 0, discount: 0.15 },
  { premium: false, minTotal: 1000, minItems: 0, discount: 0.10 },
  { premium: false, minTotal: 0,    minItems: 0, discount: 0.00 },
];

function getDiscount(user: User, order: Order): number {
  const rule = DISCOUNT_RULES.find(r =>
    r.premium === user.isPremium &&
    order.total >= r.minTotal &&
    order.items.length >= r.minItems
  );
  return rule?.discount ?? 0;
}
```

### 5. Feature Envy

```typescript
// ❌ ANTES: Classe acessa demais dados de outra
class OrderService {
  calculateShipping(order: Order): number {
    // "Inveja" dos dados de Customer
    const address = order.customer.address;
    const city = address.city;
    const state = address.state;
    const isRemote = this.isRemoteArea(city, state);
    const weight = order.items.reduce((w, i) => w + i.weight, 0);

    if (isRemote) {
      return weight * 2.5;
    }
    return weight * 1.5;
  }
}

// ✅ DEPOIS: Mova lógica para onde estão os dados
class Address {
  city: string;
  state: string;

  isRemoteArea(): boolean {
    // Lógica com os próprios dados
    return REMOTE_AREAS.includes(`${this.city}-${this.state}`);
  }
}

class Order {
  items: Item[];
  customer: Customer;

  getTotalWeight(): number {
    return this.items.reduce((w, i) => w + i.weight, 0);
  }

  calculateShipping(): number {
    const baseRate = this.customer.address.isRemoteArea() ? 2.5 : 1.5;
    return this.getTotalWeight() * baseRate;
  }
}
```

## Refactorings Comuns

### Extract Function

```
QUANDO USAR:
→ Bloco de código faz uma coisa específica
→ Código se repete
→ Comentário explica o que o código faz

COMO:
1. Crie função com nome descritivo
2. Copie o código
3. Identifique variáveis necessárias → parâmetros
4. Identifique variáveis modificadas → retorno
5. Substitua código original por chamada
6. Rode testes
```

### Inline Function (oposto de Extract)

```
QUANDO USAR:
→ Função não adiciona clareza
→ Corpo é tão claro quanto o nome
→ Excesso de indireção

EXEMPLO:
// ❌ Indireção desnecessária
function isAdult(age: number): boolean {
  return age >= 18;
}

function canVote(person: Person): boolean {
  return isAdult(person.age);
}

// ✅ Inline quando óbvio
function canVote(person: Person): boolean {
  return person.age >= 18;
}
```

### Replace Temp with Query

```typescript
// ❌ ANTES: Variável temporária
function getPrice(order: Order): number {
  const basePrice = order.quantity * order.itemPrice;
  const discount = Math.max(0, order.quantity - 500) * order.itemPrice * 0.05;
  return basePrice - discount;
}

// ✅ DEPOIS: Métodos que expressam intenção
function getPrice(order: Order): number {
  return getBasePrice(order) - getDiscount(order);
}

function getBasePrice(order: Order): number {
  return order.quantity * order.itemPrice;
}

function getDiscount(order: Order): number {
  return Math.max(0, order.quantity - 500) * order.itemPrice * 0.05;
}
```

### Replace Conditional with Polymorphism

```typescript
// ❌ ANTES: Switch baseado em tipo
function calculatePay(employee: Employee): number {
  switch (employee.type) {
    case 'hourly':
      return employee.hoursWorked * employee.hourlyRate;
    case 'salaried':
      return employee.monthlySalary;
    case 'commissioned':
      return employee.baseSalary + employee.sales * employee.commissionRate;
  }
}

// ✅ DEPOIS: Polimorfismo
abstract class Employee {
  abstract calculatePay(): number;
}

class HourlyEmployee extends Employee {
  constructor(private hoursWorked: number, private hourlyRate: number) {
    super();
  }

  calculatePay(): number {
    return this.hoursWorked * this.hourlyRate;
  }
}

class SalariedEmployee extends Employee {
  constructor(private monthlySalary: number) {
    super();
  }

  calculatePay(): number {
    return this.monthlySalary;
  }
}

class CommissionedEmployee extends Employee {
  constructor(
    private baseSalary: number,
    private sales: number,
    private commissionRate: number
  ) {
    super();
  }

  calculatePay(): number {
    return this.baseSalary + this.sales * this.commissionRate;
  }
}
```

## Checklist de Refactoring

```
ANTES DE REFATORAR:
□ Testes existem e cobrem o código?
□ Todos os testes passam?
□ Você entende o que o código faz?
□ O refactoring vai melhorar algo mensurável?

DURANTE:
□ Uma mudança pequena por vez?
□ Rodando testes após cada mudança?
□ Commits frequentes?
□ Não mudando comportamento?

DEPOIS:
□ Todos os testes ainda passam?
□ Código está mais legível?
□ Menos duplicação?
□ Nomes são claros?
□ Funções são pequenas (<20 linhas)?
```

## Exemplo de Resposta OBJETIVA

**Usuário:** "Como refatoro este código?"
```javascript
function calc(items, user) {
  let t = 0;
  for (let i = 0; i < items.length; i++) {
    t += items[i].p * items[i].q;
    if (items[i].p * items[i].q > 100) {
      t = t - (items[i].p * items[i].q * 0.1);
    }
  }
  if (user.premium) {
    t = t * 0.9;
  }
  return t;
}
```

**Resposta:**
```
Este código tem 4 problemas:
1. Nomes ruins (t, p, q, calc)
2. Cálculo duplicado (items[i].p * items[i].q)
3. Lógica misturada (subtotal + desconto + premium)
4. Loop imperativo em vez de funcional

CÓDIGO REFATORADO:

interface CartItem {
  price: number;
  quantity: number;
}

interface User {
  isPremium: boolean;
}

function calculateCartTotal(items: CartItem[], user: User): number {
  const subtotal = calculateSubtotal(items);
  const itemDiscounts = calculateItemDiscounts(items);
  const premiumDiscount = calculatePremiumDiscount(subtotal, user);

  return subtotal - itemDiscounts - premiumDiscount;
}

function calculateSubtotal(items: CartItem[]): number {
  return items.reduce(
    (total, item) => total + getItemTotal(item),
    0
  );
}

function getItemTotal(item: CartItem): number {
  return item.price * item.quantity;
}

function calculateItemDiscounts(items: CartItem[]): number {
  const BULK_DISCOUNT_THRESHOLD = 100;
  const BULK_DISCOUNT_RATE = 0.10;

  return items.reduce((discount, item) => {
    const itemTotal = getItemTotal(item);
    if (itemTotal > BULK_DISCOUNT_THRESHOLD) {
      return discount + itemTotal * BULK_DISCOUNT_RATE;
    }
    return discount;
  }, 0);
}

function calculatePremiumDiscount(subtotal: number, user: User): number {
  const PREMIUM_DISCOUNT_RATE = 0.10;
  return user.isPremium ? subtotal * PREMIUM_DISCOUNT_RATE : 0;
}

MELHORIAS:
1. Nomes descritivos (calculateCartTotal, price, quantity)
2. Cálculo extraído (getItemTotal)
3. Responsabilidades separadas (3 funções de desconto)
4. Constantes nomeadas (BULK_DISCOUNT_THRESHOLD)
5. Funcional com reduce em vez de for loop
6. TypeScript para segurança de tipos

ORDEM DE REFACTORING:
1. Primeiro: renomeie variáveis (t→total, p→price, etc)
2. Rode testes
3. Extraia getItemTotal()
4. Rode testes
5. Extraia calculateSubtotal()
6. Rode testes
7. Continue passo a passo...
```

## Regras Imutáveis

```
1. SEJA OBJETIVO — dê o código refatorado, não apenas dicas
2. Testes primeiro, refactoring depois
3. Pequenos passos, sempre
4. Não mude comportamento durante refactoring
5. Nomes claros > comentários
6. Funções pequenas (<20 linhas)
7. Uma responsabilidade por função
8. DRY (Don't Repeat Yourself)
9. Commit frequente
10. "Make the change easy, then make the easy change"
```

---

**Esta skill ativa AUTOMATICAMENTE quando:**
- Código precisa ser melhorado
- Code smells identificados
- Technical debt sendo tratado
- Antes de adicionar features
- Revisão de código com problemas
