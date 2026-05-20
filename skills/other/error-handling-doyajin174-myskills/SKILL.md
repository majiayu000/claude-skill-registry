---
name: error-handling
description: Enforce proper error handling patterns. Use when writing async code, API calls, or user-facing features. Covers try-catch, error boundaries, graceful degradation, and user feedback.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
license: MIT
metadata:
  author: antigravity-team
  version: "1.0"
---

# Error Handling Patterns

적절한 에러 처리 패턴을 강제하는 스킬입니다.

## Core Principle

> **"에러는 숨기지 않고, 적절히 처리하고, 사용자에게 알린다."**
> **"Fail gracefully, recover when possible."**

## Rules

| 규칙 | 상태 | 설명 |
|------|------|------|
| 빈 catch 블록 금지 | 🔴 필수 | 최소 로깅 필수 |
| 사용자 친화적 메시지 | 🔴 필수 | 기술적 에러 메시지 노출 금지 |
| Error Boundary 사용 | 🔴 필수 (React) | 컴포넌트 에러 격리 |
| Graceful Degradation | 🟡 권장 | 부분 실패 시 대안 제공 |

## 기본 패턴

### Try-Catch 올바른 사용

```typescript
// ❌ BAD: 빈 catch 블록
try {
  await fetchData();
} catch (e) {
  // 아무것도 안 함 - 에러 무시
}

// ❌ BAD: 모든 에러 동일 처리
try {
  await fetchData();
} catch (e) {
  console.log('에러 발생');  // 정보 부족
}

// ✅ GOOD: 적절한 에러 처리
try {
  await fetchData();
} catch (error) {
  // 1. 에러 로깅 (개발자용)
  console.error('fetchData failed:', error);

  // 2. 에러 추적 서비스 전송
  errorTracker.capture(error);

  // 3. 사용자에게 알림
  showToast('데이터를 불러오는데 실패했습니다. 다시 시도해주세요.');

  // 4. 필요시 재시도 또는 대안 제공
  return fallbackData;
}
```

### 에러 타입 구분

```typescript
// ✅ GOOD: 에러 타입별 처리
async function fetchUser(id: string) {
  try {
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    if (error instanceof NetworkError) {
      // 네트워크 에러: 재시도 제안
      showToast('네트워크 연결을 확인해주세요.');
      return null;
    }

    if (error instanceof NotFoundError) {
      // 404: 사용자 없음
      showToast('사용자를 찾을 수 없습니다.');
      return null;
    }

    if (error instanceof AuthError) {
      // 인증 에러: 로그인 페이지로
      router.push('/login');
      return null;
    }

    // 예상치 못한 에러
    console.error('Unexpected error:', error);
    errorTracker.capture(error);
    showToast('오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
    return null;
  }
}
```

## 커스텀 에러 클래스

```typescript
// errors.ts
export class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode?: number,
    public isOperational: boolean = true
  ) {
    super(message);
    this.name = 'AppError';
  }
}

export class ValidationError extends AppError {
  constructor(message: string, public field?: string) {
    super(message, 'VALIDATION_ERROR', 400);
    this.name = 'ValidationError';
  }
}

export class NetworkError extends AppError {
  constructor(message: string = '네트워크 연결을 확인해주세요') {
    super(message, 'NETWORK_ERROR', 0);
    this.name = 'NetworkError';
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource}을(를) 찾을 수 없습니다`, 'NOT_FOUND', 404);
    this.name = 'NotFoundError';
  }
}
```

## React Error Boundary

### 기본 Error Boundary

```tsx
// ErrorBoundary.tsx
import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    this.props.onError?.(error, errorInfo);

    // 에러 추적 서비스로 전송
    errorTracker.captureException(error, { extra: errorInfo });
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <DefaultErrorFallback error={this.state.error} />;
    }
    return this.props.children;
  }
}

// 기본 폴백 UI
function DefaultErrorFallback({ error }: { error?: Error }) {
  return (
    <div className="error-fallback">
      <h2>문제가 발생했습니다</h2>
      <p>페이지를 새로고침하거나 잠시 후 다시 시도해주세요.</p>
      <button onClick={() => window.location.reload()}>
        새로고침
      </button>
    </div>
  );
}
```

### Error Boundary 사용

```tsx
// 앱 전체 감싸기
function App() {
  return (
    <ErrorBoundary fallback={<FullPageError />}>
      <Router>
        <Routes />
      </Router>
    </ErrorBoundary>
  );
}

// 특정 섹션만 감싸기
function Dashboard() {
  return (
    <div>
      <Header />
      <ErrorBoundary fallback={<ChartError />}>
        <Chart data={data} />
      </ErrorBoundary>
      <ErrorBoundary fallback={<TableError />}>
        <DataTable data={data} />
      </ErrorBoundary>
    </div>
  );
}
```

## Async 에러 처리

### Promise 에러

```typescript
// ❌ BAD: unhandled rejection
fetchData().then(data => setData(data));

// ✅ GOOD: catch 처리
fetchData()
  .then(data => setData(data))
  .catch(error => {
    console.error('Failed to fetch:', error);
    setError(error);
  });

// ✅ BETTER: async/await
async function loadData() {
  try {
    const data = await fetchData();
    setData(data);
  } catch (error) {
    console.error('Failed to fetch:', error);
    setError(error);
  }
}
```

### 여러 Promise 처리

```typescript
// ❌ BAD: 하나라도 실패하면 전체 실패
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts(),
]);

// ✅ GOOD: 개별 결과 처리
const results = await Promise.allSettled([
  fetchUsers(),
  fetchPosts(),
]);

const users = results[0].status === 'fulfilled' ? results[0].value : [];
const posts = results[1].status === 'fulfilled' ? results[1].value : [];

// 실패한 것만 로깅
results
  .filter((r): r is PromiseRejectedResult => r.status === 'rejected')
  .forEach(r => console.error('Failed:', r.reason));
```

## Graceful Degradation

### 기능 저하 패턴

```typescript
// ✅ GOOD: 실패 시 대안 제공
async function getRecommendations(userId: string) {
  try {
    // 1차: 개인화된 추천
    return await fetchPersonalizedRecommendations(userId);
  } catch (error) {
    console.warn('Personalized recommendations failed:', error);

    try {
      // 2차: 인기 콘텐츠
      return await fetchPopularContent();
    } catch (error) {
      console.warn('Popular content failed:', error);

      // 3차: 캐시된 기본 추천
      return getCachedDefaultRecommendations();
    }
  }
}
```

### UI 대안 제공

```tsx
function UserAvatar({ userId }: { userId: string }) {
  const [imageError, setImageError] = useState(false);
  const user = useUser(userId);

  if (imageError || !user?.avatarUrl) {
    // 이미지 로드 실패 시 대안
    return (
      <div className="avatar-placeholder">
        {user?.name?.charAt(0) || '?'}
      </div>
    );
  }

  return (
    <img
      src={user.avatarUrl}
      alt={user.name}
      onError={() => setImageError(true)}
    />
  );
}
```

## 사용자 친화적 메시지

### 메시지 매핑

```typescript
const errorMessages: Record<string, string> = {
  NETWORK_ERROR: '네트워크 연결을 확인해주세요.',
  UNAUTHORIZED: '로그인이 필요합니다.',
  FORBIDDEN: '접근 권한이 없습니다.',
  NOT_FOUND: '요청한 정보를 찾을 수 없습니다.',
  VALIDATION_ERROR: '입력 정보를 확인해주세요.',
  RATE_LIMIT: '요청이 너무 많습니다. 잠시 후 다시 시도해주세요.',
  SERVER_ERROR: '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.',
  DEFAULT: '오류가 발생했습니다. 다시 시도해주세요.',
};

function getUserFriendlyMessage(error: unknown): string {
  if (error instanceof AppError) {
    return errorMessages[error.code] || errorMessages.DEFAULT;
  }
  return errorMessages.DEFAULT;
}
```

### 🔴 금지: 기술적 메시지 노출

```typescript
// ❌ BAD: 사용자에게 기술적 메시지 표시
showToast(error.message);  // "TypeError: Cannot read property 'id' of undefined"
showToast(error.stack);    // 스택 트레이스 노출

// ✅ GOOD: 친화적 메시지
showToast(getUserFriendlyMessage(error));
```

## 로깅 전략

```typescript
// logger.ts
export const logger = {
  error: (message: string, error: unknown, context?: object) => {
    // 개발 환경: 콘솔 출력
    if (process.env.NODE_ENV === 'development') {
      console.error(message, error, context);
    }

    // 프로덕션: 에러 추적 서비스
    errorTracker.captureException(error, {
      tags: { message },
      extra: context,
    });
  },

  warn: (message: string, context?: object) => {
    console.warn(message, context);
  },
};
```

## Checklist

### 코드 작성 시

- [ ] try-catch에 적절한 에러 처리 로직
- [ ] 빈 catch 블록 없음
- [ ] 에러 타입별 분기 처리
- [ ] 사용자 친화적 메시지 표시
- [ ] 에러 로깅/추적

### React 컴포넌트

- [ ] Error Boundary 적용
- [ ] 로딩/에러 상태 UI
- [ ] 재시도 기능 제공
- [ ] 폴백 UI 구현

### API 호출

- [ ] 네트워크 에러 처리
- [ ] 타임아웃 처리
- [ ] 재시도 로직 (필요시)
- [ ] 캐시 폴백 (필요시)

## References

- [React Error Boundaries](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary)
- [JavaScript Error Handling](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Control_flow_and_error_handling)
