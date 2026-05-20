---
name: comment-checker
description: 코드 주석 품질 관리 및 불필요한 주석 감지. 좋은/나쁜 주석의 원칙과 AI 생성 주석 감지 워크플로우를 제공합니다. Use when reviewing code comments, removing redundant comments, or writing meaningful inline documentation.
---

# Comment Checker — 주석 품질 관리

AI가 생성한 코드에서 불필요한 주석을 감지하고, 좋은 주석 원칙에 따라 제거 또는 개선을 제안합니다.

## 나쁜 주석 카테고리 (상세)

| 카테고리 | 설명 | 예시 |
|----------|------|------|
| 중복 주석 | 코드가 이미 설명하는 내용을 반복 | i++; // i를 1 증가시킨다 |
| 잘못된 주석 | 코드와 다른 내용, 오래된 정보 | 함수 설명과 구현이 다른 경우 |
| 형식적 주석 | 규칙 때문에 강제로 작성, 가치 없음 | 의미 없는 DocComment, 파라미터 반복 설명 |
| 저널 주석 | 코드 내 changelog, 버전 이력 | // 2024-01-15 수정됨 |
| 노이즈 주석 | 자명한 내용만 기술 | // 변수 선언 |
| 위치 마커 | 섹션 구분용 주석 (Extract Method 대상) | // === Section ===, // 1. 데이터 로드 |
| 주석 처리된 코드 | 삭제하고 버전 관리에 맡기기 | // oldFunction(); |
| HTML/포맷팅 | 주석 내 마크업 남용 | <!-- HTML 주석 형태 --> |

## 좋은 주석 카테고리 (상세)

| 카테고리 | 설명 | 예시 |
|----------|------|------|
| 법적/저작권 | 라이선스, 저작권 | Copyright, License 헤더 |
| 의도 설명 | WHY를 설명 (WHAT 금지) | 결제 실패 시 3회까지 재시도 (비즈니스 정책) |
| 복잡한 로직 설명 | 정규식, 비트 연산 등 난해한 부분 | |
| 경고 | 특별한 주의사항, 부작용 | 이 함수는 메인 스레드에서만 호출 |
| TODO | 티켓 번호와 함께 | TODO(JIRA-1234): 서버 API 수정 후 제거 |
| Public API 문서화 | DocComment, 공개 인터페이스 문서 | 매개변수, 반환값, 예외 설명 |

## Extract Method over Comment 패턴

주석이 코드 블록을 설명할 때: 해당 블록을 잘 이름 붙인 함수로 추출하고 주석을 제거한다.

예시:
```
Before:
// 사용자 인증 확인
if user != nil && user.isActive { ... }

After:
if isUserAuthenticated(user) { ... }

private func isUserAuthenticated(_ user: User?) -> Bool {
    return user != nil && user.isActive
}
```

판단 기준: 주석이 "무엇을 하는지" 설명한다면 → Extract Method 후보. 함수명이 주석을 대체한다.

## 4단계 리뷰 워크플로우

1. 스캔: 대상 파일 확인, 주석 개수 파악, 언어 식별
2. 패턴 감지: Grep으로 주석 패턴 검색 (언어별 주석 구문 대응)
3. 분류: 발견된 주석을 제거/개선/유지 카테고리로 분류
4. 제안: 제거 권장, 개선 권장, 유지 사유를 포함한 리포트 출력

## AI 생성 주석 감지 패턴

- 코드를 자연어로 그대로 번역한 주석 (// 변수 초기화, // 반환)
- 함수명/타입명과 동일한 내용의 DocComment
- 모든 파라미터를 나열하는 형식적 문서화
- // Gets the user, // Saves the data 등 get/set 반복
- 의미 없는 섹션 구분 (// Data loading, // Processing)

## 주석 품질 판정 테이블

| 타입 | 판정 | 조치 |
|------|------|------|
| Redundant | 제거 | 코드로 표현 가능 |
| Mandatory | 제거/개선 | 규칙 재검토, 가치 있는 경우만 유지 |
| What 설명 | 제거 | Extract Method 또는 이름 개선 |
| Why 설명 | 유지 | 비즈니스 맥락, 정책 |
| Rule/정책 | 유지 | 비즈니스 규칙 |
| Perf/최적화 | 유지 | 성능 관련 설명 |
| Algo/알고리즘 | 유지 | 복잡한 로직 설명 |
| Doc/API문서 | 유지 | Public API에 한함 |
| Stale/오래됨 | 제거 | 코드와 불일치 |
| Section | 개선 | Extract Method로 전환 |

## 리뷰 리포트 형식

```
## Comment Check Report

제거 권장:
- [파일:라인] 주석 — 사유

개선 권장:
- [파일:라인] 현재 → 개선안 (Extract Method 또는 이름 개선)

유지:
- [유지 사유가 있는 주석]

요약: 제거 N개, 개선 N개, 유지 N개
```

## 핵심 원칙

1. 코드는 자기 설명적이어야 한다: 주석 없이도 의도가 명확해야 함
2. 주석은 최후의 수단: 코드로 표현할 수 없을 때만 사용
3. 감사받는 주석만 작성: Why를 설명, What은 금지
4. 주석보다 리네이밍 우선: 변수/함수 이름으로 의도 표현

## 주석 작성 판단 기준

주석 작성 전 확인:
1. 이 주석이 없으면 코드를 이해할 수 없는가? → No면 불필요
2. 이 내용을 함수/변수 이름으로 표현할 수 있는가? → Yes면 이름 개선
3. Extract Method로 해결할 수 있는가? → Yes면 Extract 적용
4. Why(왜)를 설명하는가? → No면 재검토
5. 읽는 사람이 감사할 만한 정보인가? → No면 삭제

## 자동 수정 모드

명확한 위반 사항은 자동 제거를 제안합니다. 사용자 확인 후 적용 가능.

## 예시

나쁜 예:
```
// Bad: redundant
i++; // i를 1 증가시킨다

// Bad: What 설명
// 데이터베이스에 사용자 저장
database.save(user)
```

좋은 예:
```
// Good: intent
// 결제 실패 시 3회까지 재시도 (비즈니스 정책)
retryPayment(maxAttempts: 3);
```
