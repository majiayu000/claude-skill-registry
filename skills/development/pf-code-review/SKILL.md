---
name: pf-code-review
description: pf-frontend 프로젝트 컨벤션과 React 19 Best Practices 기반 코드 리뷰. "코드 리뷰", "리뷰해줘", "이 코드 괜찮아?" 요청 시 사용.
allowed-tools: Read, Glob, Grep
---

# PF 코드 리뷰

$ARGUMENTS 파일 또는 변경사항을 리뷰합니다.

---

## 리뷰 체크리스트

### 1. React 19 패턴

- [ ] **forwardRef 제거**: ref를 prop으로 직접 전달하는지
- [ ] **불필요한 메모이제이션**: useMemo/useCallback/memo가 정말 필요한지
- [ ] **새 Hooks 활용**: use(), useOptimistic, useActionState 적용 가능한지
- [ ] **Suspense 활용**: 로딩 상태를 Suspense로 처리할 수 있는지

```tsx
// ❌ 리뷰 포인트
const MemoizedComponent = memo(forwardRef((props, ref) => {
  const memoizedValue = useMemo(() => props.data, [props.data]);
  const handleClick = useCallback(() => onClick(), [onClick]);
  // ...
}));

// ✅ React 19 개선
function Component({ ref, data, onClick }) {
  // 메모이제이션 제거 (React Compiler가 처리)
  // ...
}
```

### 2. TypeScript

- [ ] **any 타입 금지**: unknown 또는 구체적 타입 사용
- [ ] **Props 인터페이스**: 컴포넌트마다 명시적 타입 정의
- [ ] **strict 모드 준수**: noUncheckedIndexedAccess 등
- [ ] **타입 추론 활용**: 불필요한 타입 명시 피함

```tsx
// ❌ 문제
function Component(props: any) {
  const item = items[0]; // undefined 가능성 무시
}

// ✅ 개선
interface ComponentProps {
  items: Item[];
}

function Component({ items }: ComponentProps) {
  const item = items[0]; // Item | undefined (strict 모드)
  if (!item) return null;
}
```

### 3. 상태관리 (Zustand)

- [ ] **Selector 사용**: 전체 store 대신 필요한 값만 구독
- [ ] **State/Actions 분리**: 인터페이스 분리
- [ ] **persist 설정**: partialize로 필요한 값만 저장

```tsx
// ❌ 불필요한 리렌더링
const { user, settings, theme } = useStore(); // user만 필요한데 전체 구독

// ✅ Selector로 최적화
const user = useStore(state => state.user);
// 또는
const user = useStore(selectUser);
```

### 4. API 호출

- [ ] **서비스 레이어**: apiClient 직접 호출 대신 service 함수 사용
- [ ] **에러 처리**: try-catch 또는 에러 바운더리
- [ ] **타입 안전성**: 응답 타입 명시

```tsx
// ❌ 컴포넌트에서 직접 호출
const data = await apiClient.get("/users");

// ✅ 서비스 레이어 활용
const data = await userService.getUsers();
```

### 5. 컴포넌트 구조

- [ ] **단일 책임**: 하나의 역할만 담당
- [ ] **적절한 분리**: 500줄 이상이면 분리 검토
- [ ] **Props 전달**: 3단계 이상 prop drilling 피함
- [ ] **조건부 렌더링**: 복잡하면 별도 컴포넌트로

```tsx
// ❌ 복잡한 조건부 렌더링
{isLoading ? <Loading /> : error ? <Error /> : data ? <List data={data} /> : null}

// ✅ 분리
if (isLoading) return <Loading />;
if (error) return <Error error={error} />;
if (!data) return null;
return <List data={data} />;
```

### 6. 스타일링

- [ ] **Tailwind 클래스 순서**: 일관성 유지
- [ ] **cn() 사용**: 동적 클래스 병합
- [ ] **CVA 활용**: variant가 많으면 CVA 패턴

```tsx
// ❌ 하드코딩된 조건부 스타일
className={`btn ${variant === 'primary' ? 'bg-blue-500' : 'bg-gray-500'}`}

// ✅ CVA + cn()
className={cn(buttonVariants({ variant, size }), className)}
```

### 7. 성능

- [ ] **불필요한 리렌더링**: React DevTools로 확인
- [ ] **큰 리스트**: 가상화 검토 (10,000+ 항목)
- [ ] **이미지 최적화**: lazy loading, 적절한 크기
- [ ] **번들 크기**: 동적 import 검토

### 8. 접근성

- [ ] **시맨틱 HTML**: 적절한 태그 사용
- [ ] **키보드 접근성**: Tab, Enter, Escape 처리
- [ ] **ARIA 속성**: 필요시 aria-label 등
- [ ] **색상 대비**: 충분한 대비율

```tsx
// ❌ 접근성 문제
<div onClick={handleClick}>클릭</div>

// ✅ 개선
<button onClick={handleClick} aria-label="작업 실행">
  클릭
</button>
```

### 9. 보안

- [ ] **XSS 방지**: dangerouslySetInnerHTML 사용 검토
- [ ] **환경변수**: 민감 정보 노출 여부
- [ ] **입력 검증**: Zod 스키마 사용

### 10. 코드 스타일

- [ ] **네이밍**: 명확하고 일관된 이름
- [ ] **주석**: 복잡한 로직에만 최소한으로
- [ ] **파일 구조**: 프로젝트 컨벤션 준수
- [ ] **export**: named export 사용

---

## 리뷰 출력 형식

```markdown
## 코드 리뷰 결과

### ✅ 잘된 점
- ...

### ⚠️ 개선 필요
1. **[카테고리]** 설명
   - 현재: `코드`
   - 개선: `코드`
   - 이유: 설명

### 💡 제안
- ...

### 📊 요약
| 항목 | 상태 |
|------|------|
| React 19 패턴 | ✅/⚠️/❌ |
| TypeScript | ✅/⚠️/❌ |
| 성능 | ✅/⚠️/❌ |
| 접근성 | ✅/⚠️/❌ |
```

---

## Context7 활용

최신 React 문서가 필요하면 Context7로 조회:

- React 19 공식 문서
- Zustand 최신 패턴
- Tailwind CSS 최신 기능
- TypeScript 최신 기능
