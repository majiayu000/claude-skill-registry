---
name: naming-convention-guard
description: "**NAMING CONVENTION GUARD** - 코드 작성 시 자동 발동. 변수, 함수, 클래스, 파일명의 일관된 네이밍 규칙 적용. camelCase, PascalCase, snake_case 언어별 자동 적용. 나쁜 이름 탐지 및 개선 제안."
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Naming Convention Guard Skill v1.0

**네이밍 수호자** - 일관되고 의미 있는 이름으로 코드 가독성 향상

## 핵심 철학

```yaml
Core_Philosophy:
  원칙: "이름만 보고 역할을 알 수 있어야 한다"
  목표: "3개월 후에도 코드를 이해할 수 있는 네이밍"

  좋은_이름의_조건:
    - 의도를 드러낸다 (What, not How)
    - 검색 가능하다 (grep으로 찾기 쉬움)
    - 발음 가능하다 (팀원과 대화 가능)
    - 일관성이 있다 (프로젝트 전체)

  나쁜_이름_패턴:
    - 한 글자 (x, y, i 제외)
    - 의미 없는 줄임말 (usr, cnt, tmp)
    - 타입만 있는 이름 (data, info, list)
    - 헝가리안 표기법 (strName, intCount)
    - 부정 조건 (notFound, isNotValid)
```

## 자동 발동 조건

```yaml
Auto_Trigger_Conditions:
  Always_Active:
    - "Write tool로 코드 작성 시"
    - "Edit tool로 코드 수정 시"
    - "새 변수/함수/클래스 생성 시"

  File_Extensions:
    - ".ts, .tsx, .js, .jsx"
    - ".py"
    - ".go"
    - ".java, .kt"
```

## 언어별 컨벤션

### TypeScript/JavaScript

```yaml
TypeScript_Conventions:
  변수: "camelCase (userName, isLoggedIn)"
  상수: "SCREAMING_SNAKE_CASE (MAX_RETRY_COUNT)"
  함수: "camelCase + 동사 (getUserById, handleSubmit)"
  클래스: "PascalCase (UserService, OrderRepository)"
  인터페이스: "PascalCase, I 접두사 안씀 (User, CreateUserDto)"
  컴포넌트: "PascalCase (UserProfile, OrderList)"
  파일명: "kebab-case 또는 기능.타입.ts"

함수_동사_패턴:
  조회: "get*, find*, fetch*"
  생성: "create*, add*, insert*"
  수정: "update*, modify*, set*"
  삭제: "delete*, remove*, clear*"
  검증: "is*, has*, can*, should*"
  변환: "to*, from*, parse*, format*"
  핸들러: "handle*, on*"
```

### Python

```yaml
Python_Conventions:
  변수_함수: "snake_case (user_name, get_user)"
  상수: "SCREAMING_SNAKE_CASE (MAX_RETRY)"
  클래스: "PascalCase (UserService)"
  프라이빗: "_underscore (_internal)"
  모듈_파일: "snake_case (user_service.py)"
```

### Go

```yaml
Go_Conventions:
  Private: "camelCase (userName)"
  Public: "PascalCase (UserName)"
  인터페이스: "PascalCase + er (Reader, Writer)"
  파일명: "snake_case.go"
```

## 나쁜 이름 탐지

### 즉시 수정 필요

| 패턴 | 문제 | Bad | Good |
|------|------|-----|------|
| 한글자 | 의미 불명 | a, d, x | user, data, item |
| 숫자 접미사 | 구분 불명 | user1, user2 | primaryUser |
| 의미없음 | 역할 불명 | data, info | users, config |
| 타입만 | 내용 불명 | list, array | orders, items |

### 수정 권장

| 패턴 | 문제 | Bad | Good |
|------|------|-----|------|
| 줄임말 | 가독성 | usr, cnt | user, count |
| 부정조건 | 혼란 | isNotValid | isInvalid |
| 동사없음 | 동작불명 | user() | getUser() |
| 헝가리안 | 불필요 | strName | name |

## 명명 공식

### 변수

```yaml
규칙: "[형용사] + [명사]"
예시:
  - activeUser
  - totalOrderCount
  - lastLoginDate

Boolean: "is/has/can/should + [형용사/명사]"
예시:
  - isActive, isLoggedIn
  - hasPermission
  - canEdit, shouldUpdate

Array: "[명사]s (복수형)"
예시:
  - users, orders, selectedItems
```

### 함수

```yaml
규칙: "[동사] + [목적어] + [조건]"

CRUD:
  Create: "createUser, addItem"
  Read: "getUser, findUserById"
  Update: "updateUser, setStatus"
  Delete: "deleteUser, removeItem"

Query:
  단일: "getUser, findOrder"
  복수: "getUsers, listItems"
  조건: "getUsersByRole"

Handler:
  규칙: "handle* 또는 on*"
  예시: "handleClick, onSubmit"
```

### 파일

```yaml
Component: "PascalCase.tsx (UserProfile.tsx)"
Service: "[domain].[type].ts (user.service.ts)"
Types: "[domain].types.ts"
Test: "[file].test.ts"
Constants: "[category].constants.ts"
```

## 출력 형식

```markdown
## 네이밍 검토 결과

### 즉시 수정 필요
| 위치 | 현재 | 문제 | 제안 |
|------|------|------|------|
| L15 | d | 한글자 | data |
| L23 | user1 | 숫자 | primaryUser |

### 수정 권장
| 위치 | 현재 | 문제 | 제안 |
|------|------|------|------|
| L8 | usrCnt | 줄임말 | userCount |
```

## Quick Commands

| 명령 | 동작 |
|-----|------|
| naming check | 파일 네이밍 검사 |
| naming suggest | 이름 개선 제안 |

## 체크리스트

```markdown
### 변수명
[ ] 의미가 명확한가?
[ ] 검색 가능한가?
[ ] 적절한 길이인가? (2-30자)

### 함수명
[ ] 동사로 시작하는가?
[ ] 동작이 명확한가?

### 일관성
[ ] 프로젝트 전체 같은 규칙인가?
[ ] 같은 개념에 같은 단어인가?
```

---

**Version**: 1.0.0
**Auto-Active**: 코드 작성 시 항상
**Integration**: clean-code-mastery
