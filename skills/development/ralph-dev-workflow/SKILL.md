---
name: ralph-dev-workflow
description: Ralph Loop 기반 체계적인 앱 개발 워크플로우입니다. 기능 개발, 버그 수정, 리팩토링을 5단계 (탐색 -> 계획 -> 개발 -> 리뷰 -> 수정) 프로세스로 진행하며, 리뷰/수정 단계를 사용자 지정 횟수만큼 반복합니다. 모호한 요구사항은 명확히 하고, 아키텍처 결정 사항은 반드시 질문하며, 최종 완료 시 "complete"를 출력합니다. "/ralph-dev-workflow", "랄프 개발", "Ralph Loop로" 등의 명령으로 활성화됩니다.
---

# Ralph Dev Workflow - 체계적인 앱 개발 워크플로우

## 개요

**Ralph Dev Workflow**는 house-hold-account 프로젝트의 **Clean Architecture** 구조를 준수하는 체계적인 개발 프로세스입니다. 사용자의 요구사항을 받아 5단계 (탐색 → 계획 → 개발 → 리뷰 → 수정)로 진행하며, **리뷰/수정 단계를 사용자가 지정한 횟수만큼 반복**합니다.

이 스킬은 Ralph Loop (`/ralph-loop:ralph-loop`)를 기반으로 작동하며, 다음의 특징이 있습니다:

- **자동 완료 감지**: "complete" 출력으로 종료
- **반복 가능한 리뷰**: 사용자가 지정한 횟수까지 코드 리뷰 → 수정 반복
- **모호함 제거**: 불명확한 요구사항에 대해 추가 질문
- **아키텍처 확인**: 기존 패턴과 충돌 시 반드시 질문

---

## 사용 시작

### 스킬 활성화 명령어

```
/ralph-dev-workflow [요구사항] --max-iterations [반복횟수]
또는
랄프 개발 [요구사항]
```

### 필수 입력 정보

1. **요구사항 (requirement)**: 구현하려는 기능, 버그, 리팩토링 내용
2. **최대 반복 횟수 (--max-iterations)**: 리뷰/수정 단계 반복 횟수 (기본값: 1)

### 사용 예시

```
/ralph-dev-workflow 결제수단 자동저장 기능에서 중복 거래 검사 로직 추가 --max-iterations 2

/ralph-dev-workflow authStateProvider에서 Google 로그인 실패 시 재시도 로직 추가 --max-iterations 1

/ralph-dev-workflow payment_method feature 리팩토링하여 AutoSaveService 독립 분리
```

---

## 워크플로우 다이어그램

```
┌─────────────────────────────────────────┐
│  [1] 탐색 단계                          │
│  Explore Agent (Haiku)                  │
│  - 요구사항 분석 및 명확화              │
│  - 코드베이스 탐색                      │
│  - 관련 파일 및 패턴 식별              │
└──────────────┬──────────────────────────┘
               │
┌──────────────v──────────────────────────┐
│  [2] 계획 단계                          │
│  Plan Agent (Opus)                      │
│  - 아키텍처 설계                        │
│  - 파일 목록 및 변경 계획               │
│  - 아키텍처 결정사항 확인 (질문)       │
│  [사용자 승인]                          │
└──────────────┬──────────────────────────┘
               │
┌──────────────v──────────────────────────┐
│  [3] 개발 단계                          │
│  Dev Agent (Sonnet)                     │
│  - Clean Architecture 구조 준수          │
│  - SafeNotifier, rethrow 패턴 적용     │
│  - 테스트 코드 작성                     │
└──────────────┬──────────────────────────┘
               │
     ┌─────────────────────────────┐
     │ [리뷰 반복 루프 시작]         │
     │ (최대: 사용자 지정 횟수)      │
     └──────────────┬──────────────┘
                    │
┌───────────────────v──────────────────────┐
│  [4] 리뷰 단계                           │
│  Review Agent (Opus)                     │
│  - 성능, UI/UX, 보안, 코드 품질 분석    │
│  - 이슈 분류: 심각/중간/경미            │
└───────────────────┬──────────────────────┘
                    │
            [중간이상급 이슈?]
            /            \
          Yes            No
           │              │
      [5] v              v [반복 종료]
    수정 단계        (완료로 진행)
    Dev Agent           │
      │                 │
   [반복 카운터     [Ralph Loop 종료]
    감소]                │
      │                 v
   [반복 가능?]     /ralph-loop:ralph-loop
    /     \        —completion-promise
   Yes    No       "complete"
   │       │
   v       v
 [4단계]  [강제종료]
          + 보고서

```

---

## 5단계 상세 프로세스

### 1️⃣ 탐색 단계 (Explore Agent - Haiku)

**목적**: 요구사항을 정확히 이해하고 코드베이스를 빠르게 탐색

**수행 작업**:
- 요구사항 분석 및 명확화 (모호한 부분은 질문)
- 관련 파일 및 레이어 식별
- 기존 패턴 탐색 (유사 기능)
- 영향 범위 파악

**산출물**:
- 요구사항 요약
- 수정 대상 파일 목록
- 참고할 기존 코드 위치
- 예상 영향 범위

**Agent 역할**:
- 코드베이스 구조 빠르게 파악
- 프로젝트의 Clean Architecture 준수 확인
- SafeNotifier, Riverpod 패턴 기존 사용 예 찾기

---

### 2️⃣ 계획 단계 (Plan Agent - Opus)

**목적**: 탐색 결과를 바탕으로 상세한 구현 계획 수립

**수행 작업**:
- 아키텍처 설계 (Entity → Model → Repository → Provider → UI)
- 파일별 변경 내용 명시
- 구현 순서 제시
- 예상 위험 요소 식별

**필수 확인 사항** (아키텍처 결정사항):
- SafeNotifier 사용 여부 및 방식
- Provider 종류 선택 (FutureProvider vs StateNotifier)
- Realtime 구독 필요 여부
- 에러 처리 전략 (rethrow 적용)

**설계 충돌 시 반드시 사용자에게 질문**:
- "기존 `paymentMethodsProvider`를 변경하면 다른 페이지에 영향이 있습니다. 변경하시겠습니까?"
- "이 기능은 SafeNotifier를 상속한 새 Notifier가 필요합니다. 추가 파일 생성이 괜찮으신가요?"

**산출물**:
- 구현 계획서 (파일 목록, 순서, 각 파일의 역할)
- 아키텍처 다이어그램 (텍스트 형식)
- 구현 중 확인이 필요한 사항 정리

---

### 3️⃣ 개발 단계 (Dev Agent - Sonnet)

**목적**: 계획을 실현하여 실제 코드 작성

**수행 작업**:
- 계획에 따라 파일 생성/수정
- Clean Architecture 구조 준수
- 패턴 적용 (SafeNotifier, rethrow, Realtime 등)
- 테스트 코드 작성
- 코드 린트 실행

**핵심 패턴**:

```dart
// SafeNotifier 패턴 필수 사용
class MyNotifier extends SafeNotifier<List<Item>> {
  Future<void> loadItems() async {
    state = const AsyncValue.loading();
    try {
      final items = await safeAsync(() => repository.getItems());
      if (items == null) return; // disposed
      safeUpdateState(AsyncValue.data(items));
    } catch (e, st) {
      safeUpdateState(AsyncValue.error(e, st));
      rethrow; // 필수: UI까지 에러 전파
    }
  }
}

// 에러 처리 원칙: rethrow 필수
try {
  await repository.doSomething();
} catch (e, st) {
  state = AsyncValue.error(e, st);
  rethrow; // 절대 생략하지 말 것!
}
```

**코드 컨벤션**:
- 문자열: 작은따옴표 (`'`)
- 주석: 한글 사용, 이모티콘 금지
- 테스트: 한글로 상세하게 설명

**산출물**:
- 구현된 파일들 (Entity, Model, Repository, Provider, UI)
- 테스트 코드
- 린트 정상 통과 확인

---

### 4️⃣ 리뷰 단계 (Review Agent - Opus)

**목적**: 구현된 코드의 품질을 종합적으로 분석

**리뷰 항목** (4가지 영역):

| 영역 | 확인 사항 | 예시 |
|------|---------|------|
| **성능** | 불필요한 렌더링, 메모리 누수, N+1 쿼리 | `paymentMethodsProvider` 변경 시마다 UI 전체 리빌드? |
| **UI/UX** | 로딩/에러 상태 처리, 사용자 피드백 | 에러 발생 시 스낵바 표시? 로딩 상태 보여줌? |
| **보안** | 데이터 노출, 권한 검증, RLS 정책 | 다른 사용자의 거래 데이터 조회 가능? |
| **코드 품질** | 패턴 준수, 가독성, 중복, 주석 | SafeNotifier 사용? rethrow 있음? 의미 있는 주석? |

**이슈 분류 기준**:

| 심각 (Blocker) | 중간 (Should Fix) | 경미 (Nice to Have) |
|-------------|----------------|-----------------|
| 보안 취약점 | 성능 저하 | 스타일 이슈 |
| 데이터 손실 가능성 | 에러 처리 누락 | 주석 부족 |
| 빌드 실패 | 가독성 심각한 저하 | 불필요한 코드 |
| 기존 기능 손상 | SafeNotifier 미사용 | 들여쓰기 문제 |

**판정 기준**:
- **중간 이상급 이슈가 있으면** → 수정 단계로 진행
- **중간 이상급 이슈가 없으면** → 반복 종료, "complete" 출력

**산출물**:
- 이슈 목록 (분류별)
- 각 이슈의 상세 설명과 수정 권장사항
- 리뷰 결론 (진행/중단)

---

### 5️⃣ 수정 단계 (Dev Agent - Sonnet)

**목적**: 리뷰에서 지적한 중간 이상급 이슈 수정

**수행 작업**:
- 리뷰 피드백 적용
- 문제 부분 코드 수정
- 수정 후 재검증

**반복 로직**:
- 반복 카운터 감소
- 반복 가능 여부 확인 (카운터 > 0)
- 가능하면 4단계(리뷰)로 돌아감
- 불가능하면 강제 종료 + 최종 보고

**산출물**:
- 수정된 파일들
- 수정 내용 요약

---

## Ralph Loop 통합

이 스킬은 Ralph Loop를 사용하여 복잡한 워크플로우를 관리합니다.

### Ralph Loop 호출 방식

```bash
/ralph-loop:ralph-loop --completion-promise "complete" --max-iterations {반복횟수}
```

### 구성 요소

1. **Completion Promise**: `"complete"`
   - Ralph Loop는 "complete" 문자열 출력을 프로세스 종료 신호로 감지

2. **Max Iterations**: 사용자가 입력한 반복 횟수
   - 리뷰/수정 단계만 반복
   - 최대 횟수 도달 시 강제 종료

3. **Stage Management**:
   ```
   Iteration 1: 탐색 → 계획 → 개발 → 리뷰
   Iteration 2: (리뷰/수정 있으면) 수정 → 리뷰
   Iteration 3: (리뷰/수정 있으면) 수정 → 리뷰
   ...
   ```

---

## 완료 조건 및 최종 출력

### 완료 시 출력 형식

```
complete
```

이 한 줄을 출력하면 Ralph Loop가 자동으로 프로세스를 종료합니다.

### 최종 보고서 (선택사항)

워크플로우 종료 전에 최종 요약을 제시할 수 있습니다:

```
## 개발 완료 보고서

### 구현 내용
- [기능/버그/리팩토링 요약]

### 수정된 파일
- [파일 목록]

### 테스트 실행
- [테스트 결과]

### 주의사항
- [배포 시 확인 사항]

---

complete
```

---

## 컨벤션 및 패턴

스킬 사용 시 프로젝트의 모든 컨벤션과 패턴을 준수해야 합니다.

### 참고할 References 파일

다음 파일들은 개발 중에 참고해주세요:

- **clean_architecture_guide.md**: 레이어별 구조, 파일 생성 순서
- **riverpod_patterns.md**: SafeNotifier, Provider 패턴 모음
- **error_handling_patterns.md**: rethrow 원칙, 안전한 비동기 처리
- **testing_guide.md**: 테스트 코드 작성 가이드, Maestro E2E 테스트

### 핵심 패턴 요약

1. **SafeNotifier는 필수**
   - 모든 비동기 StateNotifier는 SafeNotifier를 상속해야 함
   - `safeAsync()`, `safeInvalidate()`, `safeUpdateState()` 사용

2. **에러 처리: rethrow 절대 생략 금지**
   ```dart
   try {
     // ...
   } catch (e, st) {
     state = AsyncValue.error(e, st);
     rethrow; // 이 줄 반드시 필요!
   }
   ```

3. **작은따옴표 사용**
   ```dart
   // ✅ 올바름
   final name = 'John';
   final message = 'Hello, world!';

   // ❌ 틀림
   final name = "John";
   final message = "Hello, world!";
   ```

4. **주석은 한글, 이모티콘 금지**
   ```dart
   // ✅ 올바름
   // 사용자가 dispose되었으므로 작업 중단
   if (result == null) return;

   // ❌ 틀림
   // 사용자가 dispose됨 🚫
   if (result == null) return;
   ```

---

## 주의사항

### 1. 모호한 요구사항 확인

사용자의 요구사항이 명확하지 않으면 탐색 단계에서 반드시 질문하세요.

**질문 예시**:
- "보류 중인 거래를 '자동 추가'하는 것인가요, 아니면 '사용자 확인 후 추가'하는 것인가요?"
- "이 기능은 모든 사용자에게 적용되나요, 아니면 특정 역할(owner/admin)만 가능해야 하나요?"

### 2. 아키텍처 결정사항은 반드시 질문

기존 패턴과 다르거나 새로운 구조가 필요하면 계획 단계에서 사용자에게 물어보세요.

**질문 예시**:
- "이 기능을 위해 새로운 StateNotifier가 필요한데, 기존 Provider와 통합하시겠습니까, 아니면 독립적으로 가져가시겠습니까?"
- "Realtime 구독이 필요한데, 기존 `paymentMethodNotifierProvider`를 확장하시겠습니까?"

### 3. 리뷰/수정 반복 한계 설정

`--max-iterations` 기본값은 1입니다. 복잡한 작업은 더 높은 값을 사용하세요.

```
/ralph-dev-workflow 복잡한 기능 --max-iterations 3  # 최대 3번 리뷰/수정
/ralph-dev-workflow 간단한 버그 --max-iterations 1  # 1번만 리뷰
```

### 4. 데이터베이스 에러는 절대 무시

CLAUDE.md의 원칙:
> "데이터베이스 에러는 절대 무시하지 않는다. Supabase에서 발생하는 모든 에러는 앱에서도 반드시 처리하고 사용자에게 표시해야 함"

리뷰 단계에서 에러 처리 누락을 발견하면 중간 이상급 이슈로 분류합니다.

---

## 사용 예시

### 예시 1: 새 기능 개발 (반복 1회)

```
/ralph-dev-workflow
결제수단 자동저장 설정에서 SMS 수신 권한 요청 화면 추가.
사용자가 권한을 거부하면 자동저장을 중단하고 안내 메시지 표시.
--max-iterations 1
```

**진행**:
1. Explore: SMS 권한 관련 코드 탐색
2. Plan: 권한 요청 UI, 상태 저장 방식 계획
3. Dev: 코드 작성 + 테스트
4. Review: 성능, 보안(권한 검증), 에러 처리 확인
5. 완료

---

### 예시 2: 버그 수정 + 리팩토링 (반복 2회)

```
/ralph-dev-workflow
autoSaveService에서 SMS 파싱 시 한글 금액 포맷 인식 안 되는 버그 수정.
SmsScannerService와 SmsParsing Service 코드 정리.
--max-iterations 2
```

**진행**:
1. Explore: SMS 파싱 코드 분석
2. Plan: 버그 원인, 리팩토링 방안 계획
3. Dev: 버그 수정 + 코드 정리
4. Review: 1차 리뷰 (이슈 지적)
5. Dev (수정): 피드백 적용
6. Review: 2차 리뷰 (최종 확인)
7. 완료

---

### 예시 3: 복잡한 기능 개발 (반복 3회)

```
/ralph-dev-workflow
PendingTransaction 워크플로우 개선.
중복 검사 로직을 더 정교하게 하고, 사용자 수락/거절 기능 추가.
학습된 SMS 포맷을 활용하여 자동 분류 기능도 함께.
--max-iterations 3
```

**진행**:
1. Explore: 현재 PendingTransaction 구조 파악
2. Plan: 새로운 WorkFlow, 데이터 모델 설계
3. Dev: 전체 구현
4. Review: 1차 리뷰 (이슈 지적)
5. Dev (수정): 1차 수정
6. Review: 2차 리뷰 (추가 이슈)
7. Dev (수정): 2차 수정
8. Review: 3차 리뷰 (최종)
9. 완료

---

## 주요 팀 구성

이 스킬은 다음과 같은 Specialist Agent들을 활용합니다:

| Agent | Model | 역할 |
|-------|-------|------|
| **Explore** | Haiku | 빠른 코드베이스 탐색 |
| **Plan** | Opus | 복잡한 아키텍처 설계 |
| **Dev** | Sonnet | 실제 코드 작성 |
| **Review** | Opus | 상세한 종합 분석 |

