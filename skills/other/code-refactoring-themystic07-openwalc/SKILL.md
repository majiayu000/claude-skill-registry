---
name: code-refactoring
description: Simplify and refactor code while preserving behavior, improving clarity, and reducing complexity. Use when simplifying complex code, removing duplication, or applying design patterns. Handles Extract Method, DRY principle, SOLID principles, behavior validation, and refactoring patterns.
tags: [refactoring, code-quality, DRY, SOLID, design-patterns, clean-code, simplification, behavior-preservation]
platforms: [Claude, ChatGPT, Gemini, Codex]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Task
---

# Code Refactoring


## When to use this skill

- **코드 리뷰**: 복잡하거나 중복된 코드 발견
- **새 기능 추가 전**: 기존 코드 정리
- **버그 수정 후**: 근본 원인 제거
- **기술 부채 해소**: 정기적인 리팩토링

## Instructions

### Step 1: Extract Method (메서드 추출)

**Before (긴 함수)**:
```typescript
function processOrder(order: Order) {
  // 검증
  if (!order.items || order.items.length === 0) {
    throw new Error('Order must have items');
  }
  if (!order.customerId) {
    throw new Error('Order must have customer');
  }

  // 가격 계산
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
  }
  const tax = total * 0.1;
  const shipping = total > 100 ? 0 : 10;
  const finalTotal = total + tax + shipping;

  // 재고 확인
  for (const item of order.items) {
    const product = await db.product.findUnique({ where: { id: item.productId } });
    if (product.stock < item.quantity) {
      throw new Error(`Insufficient stock for ${product.name}`);
    }
  }

  // 주문 생성
  const newOrder = await db.order.create({
    data: {
      customerId: order.customerId,
      items: order.items,
      total: finalTotal,
      status: 'pending'
    }
  });

  return newOrder;
}
```

**After (메서드 추출)**:
```typescript
async function processOrder(order: Order) {
  validateOrder(order);
  const total = calculateTotal(order);
  await checkInventory(order);
  return await createOrder(order, total);
}

function validateOrder(order: Order) {
  if (!order.items || order.items.length === 0) {
    throw new Error('Order must have items');
  }
  if (!order.customerId) {
    throw new Error('Order must have customer');
  }
}

function calculateTotal(order: Order): number {
  const subtotal = order.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const tax = subtotal * 0.1;
  const shipping = subtotal > 100 ? 0 : 10;
  return subtotal + tax + shipping;
}

async function checkInventory(order: Order) {
  for (const item of order.items) {
    const product = await db.product.findUnique({ where: { id: item.productId } });
    if (product.stock < item.quantity) {
      throw new Error(`Insufficient stock for ${product.name}`);
    }
  }
}

async function createOrder(order: Order, total: number) {
  return await db.order.create({
    data: {
      customerId: order.customerId,
      items: order.items,
      total,
      status: 'pending'
    }
  });
}
```

### Step 2: Remove Duplication (중복 제거)

**Before (중복)**:
```typescript
async function getActiveUsers() {
  return await db.user.findMany({
    where: { status: 'active', deletedAt: null },
    select: { id: true, name: true, email: true }
  });
}

async function getActivePremiumUsers() {
  return await db.user.findMany({
    where: { status: 'active', deletedAt: null, plan: 'premium' },
    select: { id: true, name: true, email: true }
  });
}
```

**After (공통 로직 추출)**:
```typescript
type UserFilter = {
  plan?: string;
};

async function getActiveUsers(filter: UserFilter = {}) {
  return await db.user.findMany({
    where: {
      status: 'active',
      deletedAt: null,
      ...filter
    },
    select: { id: true, name: true, email: true }
  });
}

// 사용
const allActiveUsers = await getActiveUsers();
const premiumUsers = await getActiveUsers({ plan: 'premium' });
```

### Step 3: Replace Conditional with Polymorphism

**Before (긴 if-else)**:
```typescript
class PaymentProcessor {
  process(payment: Payment) {
    if (payment.method === 'credit_card') {
      // 신용카드 처리
      const cardToken = this.tokenizeCard(payment.card);
      const charge = this.chargeCreditCard(cardToken, payment.amount);
      return charge;
    } else if (payment.method === 'paypal') {
      // PayPal 처리
      const paypalOrder = this.createPayPalOrder(payment.amount);
      const approval = this.getPayPalApproval(paypalOrder);
      return approval;
    } else if (payment.method === 'bank_transfer') {
      // 은행 이체 처리
      const transfer = this.initiateBankTransfer(payment.account, payment.amount);
      return transfer;
    }
  }
}
```

**After (다형성)**:
```typescript
interface PaymentMethod {
  process(payment: Payment): Promise<PaymentResult>;
}

class CreditCardPayment implements PaymentMethod {
  async process(payment: Payment): Promise<PaymentResult> {
    const cardToken = await this.tokenizeCard(payment.card);
    return await this.chargeCreditCard(cardToken, payment.amount);
  }
}

class PayPalPayment implements PaymentMethod {
  async process(payment: Payment): Promise<PaymentResult> {
    const order = await this.createPayPalOrder(payment.amount);
    return await this.getPayPalApproval(order);
  }
}

class BankTransferPayment implements PaymentMethod {
  async process(payment: Payment): Promise<PaymentResult> {
    return await this.initiateBankTransfer(payment.account, payment.amount);
  }
}

class PaymentProcessor {
  private methods: Map<string, PaymentMethod> = new Map([
    ['credit_card', new CreditCardPayment()],
    ['paypal', new PayPalPayment()],
    ['bank_transfer', new BankTransferPayment()]
  ]);

  async process(payment: Payment): Promise<PaymentResult> {
    const method = this.methods.get(payment.method);
    if (!method) {
      throw new Error(`Unknown payment method: ${payment.method}`);
    }
    return await method.process(payment);
  }
}
```

### Step 4: Introduce Parameter Object

**Before (많은 파라미터)**:
```typescript
function createUser(
  name: string,
  email: string,
  password: string,
  age: number,
  country: string,
  city: string,
  postalCode: string,
  phoneNumber: string
) {
  // ...
}
```

**After (객체로 그룹화)**:
```typescript
interface UserProfile {
  name: string;
  email: string;
  password: string;
  age: number;
}

interface Address {
  country: string;
  city: string;
  postalCode: string;
}

interface CreateUserParams {
  profile: UserProfile;
  address: Address;
  phoneNumber: string;
}

function createUser(params: CreateUserParams) {
  const { profile, address, phoneNumber } = params;
  // ...
}

// 사용
createUser({
  profile: { name: 'John', email: 'john@example.com', password: 'xxx', age: 30 },
  address: { country: 'US', city: 'NYC', postalCode: '10001' },
  phoneNumber: '+1234567890'
});
```

### Step 5: SOLID 원칙 적용

**Single Responsibility (단일 책임)**:
```typescript
// ❌ 나쁜 예: 여러 책임
class User {
  constructor(public name: string, public email: string) {}

  save() {
    // DB 저장
  }

  sendEmail(subject: string, body: string) {
    // 이메일 발송
  }

  generateReport() {
    // 리포트 생성
  }
}

// ✅ 좋은 예: 책임 분리
class User {
  constructor(public name: string, public email: string) {}
}

class UserRepository {
  save(user: User) {
    // DB 저장
  }
}

class EmailService {
  send(to: string, subject: string, body: string) {
    // 이메일 발송
  }
}

class UserReportGenerator {
  generate(user: User) {
    // 리포트 생성
  }
}
```

## Output format

### 리팩토링 체크리스트

```markdown
- [ ] 함수는 한 가지 일만 한다 (SRP)
- [ ] 함수 이름이 하는 일을 명확히 설명한다
- [ ] 함수는 20줄 이하 (가이드라인)
- [ ] 매개변수는 3개 이하
- [ ] 중복 코드 없음 (DRY)
- [ ] if 중첩은 2단계 이하
- [ ] 매직 넘버 없음 (상수로 추출)
- [ ] 주석 없이도 이해 가능 (자기 문서화)
```

## Constraints

### 필수 규칙 (MUST)

1. **테스트 먼저**: 리팩토링 전 테스트 작성
2. **작은 단계**: 한 번에 하나씩 변경
3. **동작 보존**: 기능 변경 없음

### 금지 사항 (MUST NOT)

1. **동시에 여러 작업**: 리팩토링 + 기능 추가 동시 금지
2. **테스트 없이 리팩토링**: 회귀 위험

## Best practices

1. **Boy Scout Rule**: 코드를 발견했을 때보다 깨끗하게
2. **리팩토링 타이밍**: Red-Green-Refactor (TDD)
3. **점진적 개선**: 완벽보다 꾸준히
4. **행동 보존**: 리팩토링은 기능 변경 없음
5. **작은 커밋**: 포커스된 단위로 커밋

---

## Behavior Validation (Code Simplifier Integration)

### Step A: Understand Current Behavior

리팩토링 전 현재 동작 완전히 이해:

```markdown
## Behavior Analysis

### Inputs
- [입력 파라미터 목록]
- [타입 및 제약사항]

### Outputs
- [반환값]
- [부수 효과 (side effects)]

### Invariants
- [항상 참이어야 하는 조건들]
- [경계 조건 (edge cases)]

### Dependencies
- [외부 의존성]
- [상태 의존성]
```

### Step B: Validate After Refactoring

```bash
# 1. 테스트 실행
npm test -- --coverage

# 2. 타입 체크
npx tsc --noEmit

# 3. 린트 확인
npm run lint

# 4. 이전 동작과 비교 (스냅샷 테스트)
npm test -- --updateSnapshot
```

### Step C: Document Changes

```markdown
## Refactoring Summary

### Changes Made
1. [변경 1]: [이유]
2. [변경 2]: [이유]

### Behavior Preserved
- [x] 동일한 입력 → 동일한 출력
- [x] 부수 효과 동일
- [x] 에러 처리 동일

### Risks & Follow-ups
- [잠재적 위험]
- [후속 작업]

### Test Status
- [ ] Unit tests: passing
- [ ] Integration tests: passing
- [ ] E2E tests: passing
```

---

## Troubleshooting

### Issue: Tests fail after refactor
**Cause**: 동작 변경이 발생함
**Solution**: 되돌리고 변경을 격리하여 재시도

### Issue: Code still complex
**Cause**: 하나의 함수에 여러 책임 혼합
**Solution**: 명확한 경계로 더 작은 단위 추출

### Issue: Performance regression
**Cause**: 비효율적인 추상화 도입
**Solution**: 프로파일링 후 핫 패스 최적화

---

## Multi-Agent Workflow

### Validation & Retrospectives

- **Round 1 (Orchestrator)**: 행동 보존 체크리스트 검증
- **Round 2 (Analyst)**: 복잡도 및 중복 분석
- **Round 3 (Executor)**: 테스트 또는 정적 분석 검증

### Agent Roles

| Agent | Role |
|-------|------|
| Claude | 리팩토링 계획, 코드 변환 |
| Gemini | 대규모 코드베이스 분석, 패턴 탐지 |
| Codex | 테스트 실행, 빌드 검증 |

### Workflow Example

```bash
# 1. Gemini: 코드베이스 분석
ask-gemini "@src/ 복잡도 높은 함수 목록 추출"

# 2. Claude: 리팩토링 계획 및 실행
# IMPLEMENTATION_PLAN.md 기반 작업

# 3. Codex: 검증
codex-cli shell "npm test && npm run lint"
```

## References

- [Refactoring (Martin Fowler)](https://refactoring.com/)
- [Clean Code (Robert C. Martin)](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2025-01-01
- **호환 플랫폼**: Claude, ChatGPT, Gemini

### 관련 스킬
- [code-review](../code-review/SKILL.md)
- [backend-testing](../../backend/testing/SKILL.md)

### 태그
`#refactoring` `#code-quality` `#DRY` `#SOLID` `#design-patterns` `#clean-code`

## Examples

### Example 1: Basic usage
<!-- Add example content here -->

### Example 2: Advanced usage
<!-- Add advanced example content here -->
