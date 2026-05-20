---
name: ast-refactor
description: ast-grep를 활용한 구조적 코드 검색 및 리팩토링. 텍스트 매칭이 아닌 AST(추상 구문 트리) 기반으로 코드 패턴을 정밀하게 검색하고 치환합니다. Use when performing structural code transformations or finding patterns across the codebase.
---

# AST Refactor Skill

ast-grep를 활용한 구조적 코드 검색 및 리팩토링. 텍스트 매칭이 아닌 AST(추상 구문 트리) 기반으로 코드 패턴을 정밀하게 검색하고 치환합니다.

## ast-grep이란

- AST(Abstract Syntax Tree) 기반 코드 검색·치환 도구
- 텍스트 검색(grep)과 달리 문법 구조를 이해하여 정확한 매칭
- 정규식이나 퍼지 매칭으로 놓치기 쉬운 구조적 패턴을 안정적으로 찾음

## 사전 조건

- ast-grep 설치 확인: `which ast-grep`
- 미설치 시:
  - npm: `npm install -g @ast-grep/cli`
  - Homebrew: `brew install ast-grep`

## 워크플로우

### Step 1: 검색 패턴 정의

- 찾고자 하는 코드 구조를 AST 패턴으로 표현
- 메타 변수 활용: $VAR, $$$, $_

### Step 2: 검색 실행

```bash
ast-grep scan --pattern '$PATTERN' [--lang LANG] [PATH]
```

또는:

```bash
ast-grep --pattern '$PATTERN' [--lang LANG] [PATH]
```

### Step 3: 매칭 결과 검토

- 검색 결과의 파일·라인·매칭 내용 확인
- 의도한 패턴만 매칭되었는지 검증

### Step 4: 치환 (필요 시)

```bash
ast-grep scan --pattern '$OLD' --rewrite '$NEW' [--lang LANG] [PATH]
```

### Step 5: 검증

- ReadLints로 변경된 파일 검사
- 기존 기능 동작 확인

## 공통 패턴 예시

| 목적 | 패턴 | 설명 |
|------|------|------|
| 함수 호출 | `$FUNC($$$ARGS)` | 모든 함수 호출 |
| 메서드 체인 | `$OBJ.$METHOD($$$)` | 객체.메서드(인자) |
| 클래스 정의 | `class $NAME { $$$ }` | 클래스 선언 |
| 이름 변경 | `--pattern 'oldName($$$ARGS)' --rewrite 'newName($$$ARGS)'` | 함수명 변경 |

## 메타 변수

- $VAR: 단일 노드 (이름 자유)
- $$$: 여러 노드 (0개 이상)
- $_: 아무 단일 노드

## 지원 언어

JS, TS, Python, Go, Rust, Swift, Java, Kotlin, C, C++ 등 다수

## 안전 수칙

- 적용 전 반드시 search 결과로 미리보기
- 가능하면 `--interactive` 옵션 사용
- 소규모 범위부터 적용 후 점진적 확대

## autonomous-loop 연동

- 대규모 리팩토링 시 autonomous-loop 내부에서 ast-refactor 활용
- 패턴 검색 → 치환 → Verify 단계로 자동화
