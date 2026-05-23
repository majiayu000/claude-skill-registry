---
name: build-fix
description: 빌드 오류 자동 수정 워크플로우. 컴파일 에러, 타입 에러, 누락된 import, 빌드 설정 문제를 진단하고 수정합니다. Use when build fails and quick targeted fixes are needed without broader refactoring.
---

# Build Fix — 빌드 오류 자동 수정

빌드 오류를 진단하고 최소한의 변경으로 수정합니다.

## 참조

- `.claude/skills/code-accuracy/SKILL.md` — 코드 정확성 검증
- `project CLAUDE.md or .claude/rules/` — 빌드 도구, 언어 설정

## 워크플로우

### Step 1: 오류 수집
- ReadLints로 현재 린트 오류 수집
- 빌드 명령 실행 결과 확인 (있는 경우)
- 오류를 유형별로 분류

### Step 2: 오류 분류 및 우선순위

| 우선순위 | 오류 유형 | 수정 방법 |
|---------|---------|---------|
| 1 | 누락 import/module | import 문 추가 |
| 2 | 타입 불일치 | 타입 수정 또는 캐스팅 |
| 3 | 미정의 심볼 | 선언 추가 또는 import 수정 |
| 4 | 설정 오류 | 빌드 설정 수정 |
| 5 | 의존성 문제 | 패키지 설치 안내 |

### Step 3: 수정 적용
- 의존성 순서대로 수정 (import → 타입 → 로직)
- 각 수정 후 ReadLints로 검증
- 새로운 오류가 발생하면 추가 수정

### Step 4: 검증
- 모든 ReadLints 오류 0개 확인
- 수정 사항 요약 보고

## 에이전트 연동

- build-fixer 에이전트가 이 스킬의 주 실행자
- 복잡한 빌드 문제는 debugger 에이전트로 에스컬레이션

## 완료 보고 형식

```
[Build Fix 완료]
- 수정된 오류: N개
- 수정 파일: [목록]
- 남은 오류: N개 (있는 경우)
```
