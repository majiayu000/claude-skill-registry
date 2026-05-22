---
name: tdd-flow
description: RED-GREEN-REFACTOR 워크플로우를 강제하는 TDD 개발 스킬
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# TDD Flow Skill

이 스킬은 ForkLore 프로젝트에서 TDD(Test-Driven Development) 워크플로우를 강제합니다.

## 워크플로우

### 1. RED 단계 - 실패하는 테스트 먼저 작성

```bash
# Backend (pytest)
poetry run pytest apps/{app}/tests/test_{feature}.py -v

# Frontend (vitest)
pnpm test -- {feature}.test.tsx
```

**반드시 테스트가 FAIL 상태임을 확인한 후 다음 단계로 진행합니다.**

### 2. GREEN 단계 - 최소한의 구현

테스트를 통과하기 위한 최소한의 코드만 작성합니다.
- 과도한 추상화 금지
- 불필요한 기능 추가 금지
- 테스트 통과만을 목표로 함

```bash
# 테스트 실행하여 PASS 확인
poetry run pytest apps/{app}/tests/test_{feature}.py -v
```

### 3. REFACTOR 단계 - 코드 개선

테스트가 통과한 상태에서 코드를 개선합니다.
- 중복 제거
- 가독성 향상
- 성능 최적화

```bash
# 리팩토링 후에도 테스트 PASS 유지 확인
poetry run pytest apps/{app}/tests/test_{feature}.py -v
```

## ForkLore 테스트 규칙

### Backend
- 테스트 위치: `apps/{app}/tests/`
- 픽스처: `@pytest.fixture`, `model_bakery`
- 커버리지: 95% 이상 유지
- 명령어: `poetry run pytest --cov=apps --cov-report=term-missing`

### Frontend
- 테스트 위치: `__tests__/` 또는 `*.test.tsx`
- 도구: vitest, React Testing Library
- 명령어: `pnpm test -- --run`

## 체크리스트

- [ ] 테스트 먼저 작성했는가?
- [ ] 테스트가 실패하는 것을 확인했는가?
- [ ] 최소한의 코드로 테스트를 통과시켰는가?
- [ ] 리팩토링 후에도 테스트가 통과하는가?
- [ ] 커버리지가 95% 이상인가?
