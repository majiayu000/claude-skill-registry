---
name: multi-perspective-code-review
description: 다각도 코드 리뷰 스킬. UI/UX, 성능, 디자인, 코드 품질, 엣지케이스, 보안 등 6가지 관점에서 체계적인 코드 리뷰를 수행합니다. 코드 변경 후, PR 생성 전, 기능 구현 완료 후에 사용하세요. "/multi-perspective-code-review", "다각도 리뷰", "종합 코드 리뷰" 등의 명령으로 활성화됩니다.
---

# Multi-Perspective Code Review

## 개요

6가지 핵심 관점에서 코드를 종합적으로 분석하여 품질을 보장하는 코드 리뷰 스킬입니다.

**리뷰 관점**:
1. **UI/UX** - 사용자 경험, 접근성, 피드백
2. **성능** - 렌더링, 메모리, 네트워크
3. **디자인** - 아키텍처, 패턴, 확장성
4. **코드 품질** - 가독성, 유지보수성, 컨벤션
5. **엣지케이스** - 예외 상황, 경계값, 에러 처리
6. **보안** - 취약점, 권한, 데이터 보호

---

## 사용법

### 스킬 활성화

```
/multi-perspective-code-review [대상]

# 예시
/multi-perspective-code-review                    # git diff 기준 변경 내용 전체
/multi-perspective-code-review payment_method     # 특정 feature 리뷰
/multi-perspective-code-review lib/features/auth  # 특정 경로 리뷰
```

### 리뷰 대상 결정

1. **인자 없이 호출**: `git diff --staged` 또는 `git diff` 기준 변경 파일 리뷰
2. **feature 이름**: `lib/features/{feature}` 하위 전체 파일 리뷰
3. **경로 지정**: 해당 경로의 파일들 리뷰

---

## 리뷰 프로세스

### Step 1: 변경 내용 파악

```bash
# 변경 파일 목록 확인
git diff --name-only

# 변경 상세 내용 확인
git diff
```

### Step 2: 6가지 관점별 분석

각 관점에서 코드를 분석하고 이슈를 분류합니다.

**이슈 심각도**:
| 등급 | 설명 | 조치 |
|------|------|------|
| **Critical** | 보안 취약점, 데이터 손실, 빌드 실패 | 즉시 수정 필수 |
| **High** | 버그, 심각한 성능 문제, 기능 손상 | 수정 권장 |
| **Medium** | 코드 품질, 아키텍처 위반 | 개선 권장 |
| **Low** | 스타일, 문서화, 마이너 개선 | 선택적 수정 |

### Step 3: 리뷰 결과 출력

```markdown
## 코드 리뷰 결과

### 요약
- 리뷰 파일: {N}개
- 발견 이슈: Critical {N} / High {N} / Medium {N} / Low {N}

### Critical Issues
[이슈 목록]

### High Issues
[이슈 목록]

### 관점별 상세 분석

#### 1. UI/UX
[분석 결과]

#### 2. 성능
[분석 결과]

...

### 잘된 점
[긍정적 피드백]

### 권장 액션
1. [즉시 수정할 항목]
2. [개선할 항목]
```

---

## 6가지 리뷰 관점 상세

### 1. UI/UX 관점

**확인 항목**:
- 로딩 상태 표시 (스피너, 스켈레톤)
- 에러 상태 피드백 (스낵바, 다이얼로그)
- 빈 상태(Empty State) 처리
- 사용자 액션 피드백 (버튼 비활성화, 성공 메시지)
- 접근성 (Semantics, 최소 터치 영역 48x48)
- 반응형 레이아웃
- 다크모드 지원

**체크리스트**:
```dart
// 로딩 상태 처리 확인
state.when(
  loading: () => LoadingIndicator(),  // 있는지?
  error: (e, st) => ErrorWidget(e),    // 있는지?
  data: (data) => DataWidget(data),
);

// 빈 상태 처리
if (items.isEmpty) {
  return EmptyStateWidget();  // 있는지?
}
```

---

### 2. 성능 관점

**확인 항목**:
- 불필요한 위젯 리빌드 (const 활용)
- 무거운 연산의 build() 내 실행
- 이미지 캐싱 (CachedNetworkImage)
- 리스트 최적화 (ListView.builder)
- N+1 쿼리 문제
- 불필요한 API 호출
- 메모리 누수 (dispose, cancel)
- Realtime 구독 정리

**체크리스트**:
```dart
// const 위젯 활용
const SizedBox(height: 16),  // const 붙었는지?

// ListView 최적화
ListView.builder(  // .builder 사용하는지?
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(items[index]),
);

// dispose에서 리소스 정리
@override
void dispose() {
  _controller.dispose();  // 정리하는지?
  _subscription?.cancel();
  super.dispose();
}
```

---

### 3. 디자인 관점

**확인 항목**:
- Clean Architecture 레이어 준수
  - Domain: Entity (순수 비즈니스 로직)
  - Data: Model, Repository (데이터 접근)
  - Presentation: Provider, Page, Widget (UI)
- 의존성 방향 (Presentation -> Domain <- Data)
- 단일 책임 원칙 (SRP)
- Repository 패턴 준수
- Provider 분리 적절성
- 확장성 고려

**체크리스트**:
```dart
// Repository를 통한 데이터 접근
class TransactionNotifier {
  final TransactionRepository _repository;  // Repository 사용하는지?

  // 직접 Supabase 호출 금지
  // final supabase = Supabase.instance.client;
}

// Feature-first 구조
lib/features/{feature}/
  domain/entities/     # Entity 정의
  data/
    models/          # Model (JSON 변환)
    repositories/    # Repository 구현
  presentation/
    providers/       # 상태 관리
    pages/           # 화면
    widgets/         # 위젯
```

---

### 4. 코드 품질 관점

**확인 항목**:
- 코드 중복
- 함수/클래스 길이 (50줄 이하 권장)
- 명확한 네이밍
- 주석 품질 (한글, 이모티콘 금지)
- 문자열 따옴표 (작은따옴표 사용)
- import 정리
- 타입 명시
- 매직 넘버/스트링 제거

**체크리스트**:
```dart
// 올바른 문자열
final message = '저장되었습니다';

// 틀린 문자열
// final message = "저장되었습니다";

// 올바른 주석
// 사용자가 이미 로그인되어 있으면 홈으로 이동

// 틀린 주석 (이모티콘 금지)
// 사용자 로그인 체크

// 매직 넘버 제거
const maxRetryCount = 3;  // 올바름
// if (retry < 3) {}      // 틀림
```

---

### 5. 엣지케이스 관점

**확인 항목**:
- Null 처리
- 빈 리스트/맵 처리
- 경계값 (0, 음수, 최대값)
- 네트워크 오류 처리
- 타임아웃 처리
- 동시성 이슈 (Race Condition)
- 중복 요청 방지
- 취소/인터럽트 처리

**체크리스트**:
```dart
// Null 안전 처리
final amount = transaction.amount ?? 0;

// 빈 리스트 체크
if (transactions.isEmpty) {
  return EmptyState();
}

// 중복 요청 방지
if (_isLoading) return;
_isLoading = true;
try {
  await doSomething();
} finally {
  _isLoading = false;
}

// Race Condition 방지 (SafeNotifier 사용)
class MyNotifier extends SafeNotifier<Data> {
  Future<void> load() async {
    final result = await safeAsync(() => repository.fetch());
    if (result == null) return;  // disposed 체크
    safeUpdateState(AsyncValue.data(result));
  }
}
```

---

### 6. 보안 관점

**확인 항목**:
- SQL Injection (Supabase RPC 파라미터)
- XSS (사용자 입력 표시 시)
- 인증 검증
- 권한 검증 (RLS 정책)
- 민감 정보 노출 (API 키, 토큰)
- 로그에 민감 정보 출력
- HTTPS 사용
- 입력값 검증

**체크리스트**:
```dart
// RLS 정책 확인
// Supabase 마이그레이션에서 RLS 활성화 확인

// 민감 정보 로깅 금지
// debugPrint('Token: $accessToken');  // 금지
// debugPrint('Login successful');     // 허용

// 입력값 검증
if (amount <= 0) {
  throw ValidationException('금액은 0보다 커야 합니다');
}

// 권한 검증
if (member.role != 'owner' && member.role != 'admin') {
  throw UnauthorizedException('권한이 없습니다');
}
```

---

## 프로젝트 특화 규칙

이 프로젝트(house-hold-account)에서 추가로 확인해야 할 사항:

| 항목 | 규칙 |
|------|------|
| SafeNotifier | 모든 비동기 Notifier는 SafeNotifier 상속 필수 |
| rethrow | catch 블록에서 에러 전파 필수 |
| RLS | 모든 테이블에 Row Level Security 적용 |
| i18n | 하드코딩 텍스트 금지, ARB 파일 사용 |
| AutoSaveMode | manual/suggest/auto 3가지 모드 구분 |
| 결제수단 소유자 | owner_user_id 검증 필요 |

**필수 패턴**:
```dart
// SafeNotifier + rethrow 패턴
class MyNotifier extends SafeNotifier<Data> {
  Future<void> action() async {
    state = const AsyncValue.loading();
    try {
      final result = await safeAsync(() => repository.action());
      if (result == null) return;
      safeUpdateState(AsyncValue.data(result));
    } catch (e, st) {
      safeUpdateState(AsyncValue.error(e, st));
      rethrow;  // 필수!
    }
  }
}
```

---

## 출력 형식

리뷰 완료 시 다음 형식으로 결과를 출력합니다:

```markdown
## 다각도 코드 리뷰 결과

### 요약
| 관점 | Critical | High | Medium | Low |
|------|----------|------|--------|-----|
| UI/UX | 0 | 1 | 2 | 0 |
| 성능 | 0 | 0 | 1 | 1 |
| 디자인 | 0 | 0 | 0 | 0 |
| 코드 품질 | 0 | 1 | 0 | 2 |
| 엣지케이스 | 1 | 0 | 1 | 0 |
| 보안 | 0 | 0 | 0 | 0 |

### Critical Issues (즉시 수정)
1. **[엣지케이스]** `pending_transaction_card.dart:45`
   - 문제: 금액이 null일 때 크래시 발생
   - 해결: null 체크 추가 `amount ?? 0`

### High Issues (수정 권장)
1. **[UI/UX]** `auto_save_settings_page.dart:120`
   - 문제: 저장 버튼 클릭 시 로딩 표시 없음
   - 해결: 버튼에 CircularProgressIndicator 추가

2. **[코드 품질]** `sms_parsing_service.dart:78`
   - 문제: rethrow 누락으로 에러가 UI까지 전파 안 됨
   - 해결: catch 블록에 rethrow 추가

### 잘된 점
- SafeNotifier 패턴 일관되게 적용
- 한글 주석으로 가독성 좋음
- Repository 패턴 잘 준수

### 권장 액션
1. [ ] Critical 이슈 1건 즉시 수정
2. [ ] High 이슈 2건 수정 권장
3. [ ] Medium 이슈는 다음 스프린트에서 개선
```

---

## 리뷰 원칙

1. **건설적 피드백**: 문제점과 함께 구체적 해결책 제시
2. **우선순위 명확화**: Critical -> High -> Medium -> Low 순서
3. **컨텍스트 존중**: 프로젝트 컨벤션과 패턴 준수
4. **학습 기회 제공**: 왜 문제인지 설명
5. **긍정적 강화**: 잘된 부분도 언급

---

## References

상세 체크리스트는 `references/review-checklists.md` 참조
