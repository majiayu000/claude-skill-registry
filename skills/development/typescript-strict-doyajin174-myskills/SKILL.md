---
name: typescript-strict
description: Enforce TypeScript strict mode and type safety. Use when setting up projects, reviewing code, or when type errors are ignored. Covers strict flags, no-any rules, and type inference best practices.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
license: MIT
metadata:
  author: antigravity-team
  version: "1.0"
---

# TypeScript Strict Mode

TypeScript 엄격 모드와 타입 안전성을 강제하는 스킬입니다.

## 2025 Context

> **TypeScript 5.x에서 strict 모드가 새 프로젝트의 기본값으로 권장됨**
> **"any 사용은 TypeScript를 쓰는 의미를 없앤다"**

## Core Rules

| 규칙 | 상태 | 설명 |
|------|------|------|
| `strict: true` | 🔴 필수 | 모든 엄격 검사 활성화 |
| `any` 금지 | 🔴 필수 | `unknown` 또는 제네릭 사용 |
| `// @ts-ignore` 금지 | 🔴 필수 | 타입 에러 해결 필수 |
| `as` 캐스팅 최소화 | 🟡 권장 | 타입 가드 우선 |

## tsconfig.json 권장 설정

```json
{
  "compilerOptions": {
    // 🔴 필수: strict 플래그
    "strict": true,

    // strict가 포함하는 옵션들 (개별 비활성화 금지)
    // "strictNullChecks": true,
    // "strictFunctionTypes": true,
    // "strictBindCallApply": true,
    // "strictPropertyInitialization": true,
    // "noImplicitAny": true,
    // "noImplicitThis": true,
    // "alwaysStrict": true,

    // 🔴 추가 필수 옵션
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,

    // 🟡 권장 옵션
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true
  }
}
```

## any 금지

### 문제: any 사용

```typescript
// ❌ BAD: any 사용
function processData(data: any) {
  return data.value;  // 런타임 에러 가능
}

const result: any = fetchData();
result.nonExistent();  // 컴파일 통과, 런타임 에러
```

### 해결: unknown 또는 타입 명시

```typescript
// ✅ GOOD: unknown + 타입 가드
function processData(data: unknown) {
  if (isValidData(data)) {
    return data.value;
  }
  throw new Error('Invalid data');
}

function isValidData(data: unknown): data is { value: string } {
  return typeof data === 'object'
    && data !== null
    && 'value' in data;
}

// ✅ GOOD: 제네릭 사용
function processData<T extends { value: string }>(data: T) {
  return data.value;
}
```

### any → unknown 마이그레이션

```typescript
// Before
function parse(json: string): any {
  return JSON.parse(json);
}

// After
function parse(json: string): unknown {
  return JSON.parse(json);
}

// 사용 시 타입 체크 필요
const result = parse('{"name": "test"}');
if (isUser(result)) {
  console.log(result.name);  // 안전
}
```

## 타입 단언(as) 최소화

### 문제: 과도한 타입 단언

```typescript
// ❌ BAD: 위험한 타입 단언
const user = response.data as User;
user.name.toUpperCase();  // null이면 에러

// ❌ BAD: 이중 단언 (매우 위험)
const value = data as unknown as TargetType;
```

### 해결: 타입 가드 사용

```typescript
// ✅ GOOD: 타입 가드
function isUser(data: unknown): data is User {
  return (
    typeof data === 'object' &&
    data !== null &&
    'name' in data &&
    typeof (data as { name: unknown }).name === 'string'
  );
}

if (isUser(response.data)) {
  response.data.name.toUpperCase();  // 안전
}

// ✅ GOOD: Zod 스키마 검증
import { z } from 'zod';

const UserSchema = z.object({
  name: z.string(),
  email: z.string().email(),
});

const user = UserSchema.parse(response.data);
```

## Null 안전성

### strictNullChecks 활용

```typescript
// ❌ BAD: null 체크 없음
function getLength(str: string | null) {
  return str.length;  // 에러: null일 수 있음
}

// ✅ GOOD: null 체크
function getLength(str: string | null) {
  if (str === null) return 0;
  return str.length;
}

// ✅ GOOD: 옵셔널 체이닝
function getLength(str: string | null) {
  return str?.length ?? 0;
}
```

### 배열 인덱스 접근

```typescript
// noUncheckedIndexedAccess: true 일 때

const arr = [1, 2, 3];
const first = arr[0];  // number | undefined

// ❌ BAD: undefined 체크 없음
console.log(first.toFixed(2));  // 에러

// ✅ GOOD: undefined 체크
if (first !== undefined) {
  console.log(first.toFixed(2));
}

// ✅ GOOD: 논리 연산자
console.log(arr[0]?.toFixed(2) ?? 'N/A');
```

## 함수 타입

### 반환 타입 명시 (권장)

```typescript
// ❌ BAD: 반환 타입 추론 의존
function fetchUser(id: string) {
  return api.get(`/users/${id}`);  // 반환 타입?
}

// ✅ GOOD: 명시적 반환 타입
async function fetchUser(id: string): Promise<User> {
  return api.get(`/users/${id}`);
}
```

### 함수 오버로드

```typescript
// ✅ GOOD: 오버로드로 정확한 타입
function process(input: string): string;
function process(input: number): number;
function process(input: string | number): string | number {
  if (typeof input === 'string') {
    return input.toUpperCase();
  }
  return input * 2;
}

const str = process('hello');  // string
const num = process(42);       // number
```

## 제네릭 활용

```typescript
// ❌ BAD: any 사용
function first(arr: any[]): any {
  return arr[0];
}

// ✅ GOOD: 제네릭
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

// ✅ GOOD: 제약 있는 제네릭
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

## ESLint 규칙

```json
{
  "extends": [
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking"
  ],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-unsafe-assignment": "error",
    "@typescript-eslint/no-unsafe-member-access": "error",
    "@typescript-eslint/no-unsafe-call": "error",
    "@typescript-eslint/no-unsafe-return": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-non-null-assertion": "warn",
    "@typescript-eslint/prefer-nullish-coalescing": "warn"
  }
}
```

## 금지 패턴

```typescript
// 🔴 절대 금지
// @ts-ignore
// @ts-nocheck
// @ts-expect-error (테스트 제외)
// eslint-disable @typescript-eslint/no-explicit-any

// 🔴 금지: any 캐스팅
data as any
(data as unknown) as TargetType

// 🟡 최소화
data!  // non-null assertion
data as Type  // 타입 가드 우선
```

## Workflow

### 1. 새 프로젝트 설정

```bash
# TypeScript 초기화
npx tsc --init

# strict 활성화 확인
grep -n "strict" tsconfig.json
```

### 2. 기존 프로젝트 마이그레이션

```bash
# 1. strict 활성화
# tsconfig.json: "strict": true

# 2. 에러 확인
npx tsc --noEmit

# 3. 점진적 수정
# - any → unknown
# - as → 타입 가드
# - null 체크 추가
```

### 3. 코드 리뷰 체크

```
타입 안전성 체크:
- [ ] any 사용하지 않음
- [ ] @ts-ignore 없음
- [ ] 타입 단언 최소화
- [ ] null 체크 적절함
```

## Checklist

- [ ] `strict: true` 설정
- [ ] `noUncheckedIndexedAccess: true` 설정
- [ ] ESLint @typescript-eslint 규칙 적용
- [ ] any 0개
- [ ] @ts-ignore 0개
- [ ] 타입 가드 함수 구현
- [ ] 명시적 반환 타입 (공개 API)

## References

- [TypeScript Handbook - Strict Mode](https://www.typescriptlang.org/tsconfig#strict)
- [typescript-eslint](https://typescript-eslint.io/)
- [Zod](https://zod.dev/)
