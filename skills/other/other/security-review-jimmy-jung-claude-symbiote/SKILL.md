---
name: security-review
description: 보안 취약점 검토 워크플로우. 입력 검증, 인증/인가, 시크릿 노출, 인젝션, XSS, 의존성 취약점을 체계적으로 검사합니다. Use when reviewing code for security vulnerabilities or when security review is explicitly requested.
---

# Security Review — 보안 취약점 검토

코드의 보안 취약점을 체계적으로 검사하고 수정 방안을 제시합니다.

## 참조

- `project CLAUDE.md or .claude/rules/` — 프로젝트 보안 요구사항

## 검사 항목

### 입력 검증
- 사용자 입력의 유효성 검증 여부
- SQL Injection 방어 (파라미터화된 쿼리)
- XSS 방어 (출력 이스케이핑)
- Command Injection 방어
- Path Traversal 방어

### 인증/인가
- 인증 바이패스 가능 경로
- 권한 검사 누락
- 세션 관리 취약점
- JWT/토큰 검증

### 시크릿 관리
- 하드코딩된 비밀번호/API 키
- .env 파일 커밋 여부
- 로그에 민감 데이터 출력

### 의존성
- 알려진 취약점이 있는 라이브러리
- 최소 권한 원칙 준수

### 데이터 보호
- 민감 데이터 암호화
- 안전한 통신 (HTTPS)
- 적절한 데이터 삭제

## 워크플로우

### Step 1: 코드 스캔
- Grep으로 위험 패턴 검색 (password, secret, api_key, eval, exec 등)
- 입력 처리 로직 추적
- 인증/인가 경로 분석

### Step 2: 취약점 분류

| 심각도 | 설명 |
|-------|-----|
| Critical | 즉시 악용 가능한 취약점 |
| High | 조건부 악용 가능 |
| Medium | 보안 모범 사례 위반 |
| Low | 개선 권장 |

### Step 3: 보고

```
[Security Review 결과]

Critical:
- [파일:라인] [취약점] → [수정 방안] [참조: CWE-XXX]

High:
- [파일:라인] [취약점] → [수정 방안]

Medium/Low:
- [파일:라인] [취약점] → [수정 방안]

종합: [통과 / 수정 필요 / 즉시 대응 필요]
```

## 에이전트 연동

- security-reviewer 에이전트가 이 스킬의 주 실행자
