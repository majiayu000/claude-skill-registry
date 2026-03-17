---
name: testing-strategy
description: Comprehensive testing workflow combining TDD, real implementations (no mocking), and E2E testing. Use when implementing features, writing tests, or setting up test infrastructure.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
license: MIT
metadata:
  author: obra/superpowers
  version: "2.0"
---

# Testing Strategy

TDD와 실제 구현 기반 테스트를 결합한 통합 테스트 스킬입니다.

## Iron Law

> **"NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"**

## RED-GREEN-REFACTOR Cycle

### 1. RED - 실패하는 테스트 작성
```
- 원하는 동작을 보여주는 최소한의 테스트 작성
- 테스트가 실패하는지 반드시 확인
```

### 2. GREEN - 테스트 통과시키기
```
- 테스트를 통과시키는 가장 단순한 코드 작성
- 완벽한 코드 X, 동작하는 코드 O
```

### 3. REFACTOR - 리팩토링
```
- 코드 정리 (중복 제거, 명명 개선)
- 테스트가 계속 통과하는지 확인
```

---

## No Mocking Policy

> **실제 구현을 테스트하라**

### ❌ 금지
```typescript
jest.mock('./database');
jest.mock('./api');
```

### ✅ 허용
```typescript
// 실제 테스트 DB 또는 인메모리 DB 사용
const db = await createTestDatabase();

// MSW로 실제 HTTP 계층 테스트
const server = setupServer(
  rest.get('/api/users', (req, res, ctx) => {
    return res(ctx.json([{ id: 1, name: 'Test' }]));
  })
);
```

---

## E2E Testing (Playwright)

```typescript
test('user can complete checkout', async ({ page }) => {
  await page.goto('/products');
  await page.click('[data-testid="add-to-cart"]');
  await page.click('[data-testid="checkout"]');
  await expect(page.locator('.confirmation')).toBeVisible();
});
```

---

## Test Categories

| 유형 | 범위 | 도구 |
|------|------|------|
| Unit | 함수/클래스 | Vitest, Jest |
| Integration | 모듈 간 연동 | 실제 DB, MSW |
| E2E | 전체 사용자 흐름 | Playwright |

## Checklist

- [ ] 모든 함수가 테스트됨
- [ ] 테스트가 먼저 실패하는 것을 확인
- [ ] Mock 사용 없음 (MSW 허용)
- [ ] E2E로 핵심 흐름 검증
