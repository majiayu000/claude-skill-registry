---
name: jetbrains-workflow
description: JetBrains MCP 도구를 활용한 빠른 개발 워크플로우. IDE 검사, Run Configuration 실행, 리팩토링, 파일 검색 등을 통해 Gradle 의존도를 줄이고 개발 속도를 10배 향상시킵니다. Kotlin/Spring 개발 시 필수로 사용하세요.
---

# JetBrains MCP Workflow

> **JetBrains IDE의 MCP 도구를 최대한 활용하여 개발 속도를 극대화합니다.**

## 핵심 원칙

```
IDE 먼저, Gradle 나중에
- 코드 검사 → jetbrains.get_file_problems() (0-2초)
- 테스트 실행 → jetbrains.execute_run_configuration() (IDE 캐시 활용)
- 포맷팅 → jetbrains.reformat_file() (즉시)
- 검색 → jetbrains.find_files_by_name_keyword() (인덱스 활용)
```

---

## 1. 코드 검증 워크플로우

### Step 1: 즉시 에러 확인 (0-2초)

```python
# 코드 수정 후 항상 먼저 실행
jetbrains.get_file_problems(
    filePath="module-core-domain/src/main/kotlin/.../Service.kt",
    errorsOnly=True,
    timeout=5000,
    projectPath="/path/to/project-basecamp-server"
)
```

**반환 정보:**
- 문법 에러, 타입 에러
- 미해결 참조
- 컴파일 에러
- 라인/컬럼 위치

### Step 2: 단일 테스트 실행

**옵션 A: Run Configuration 사용 (권장)**

```python
# 먼저 사용 가능한 Run Configuration 확인
jetbrains.get_run_configurations(
    projectPath="/path/to/project-basecamp-server"
)

# Run Configuration으로 테스트 실행 (IDE 캐시 활용으로 더 빠름)
jetbrains.execute_run_configuration(
    configurationName="PipelineServiceTest",
    timeout=60000,
    maxLinesCount=200,
    projectPath="/path/to/project-basecamp-server"
)
```

**옵션 B: Terminal 명령어 사용**

```python
# Gradle 단일 테스트 실행
jetbrains.execute_terminal_command(
    command="./gradlew :module-core-domain:test --tests '*PipelineServiceTest'",
    timeout=60000,
    maxLinesCount=200,
    reuseExistingTerminalWindow=True,
    projectPath="/path/to/project-basecamp-server"
)
```

### Step 3: 최종 빌드 (기능 완료 후 1회만)

```python
jetbrains.execute_terminal_command(
    command="./gradlew build",
    timeout=300000,
    reuseExistingTerminalWindow=True,
    projectPath="/path/to/project-basecamp-server"
)
```

---

## 2. 리팩토링 워크플로우

### 심볼 이름 변경 (프로젝트 전체 자동 업데이트)

```python
# IDE의 리팩토링 기능 활용 - 모든 참조 자동 업데이트
jetbrains.rename_refactoring(
    pathInProject="module-core-domain/src/main/kotlin/.../PipelineService.kt",
    symbolName="createPipeline",
    newName="createNewPipeline",
    projectPath="/path/to/project-basecamp-server"
)
```

**장점:**
- 프로젝트 전체에서 모든 참조 자동 업데이트
- 문자열 치환보다 안전
- import 문도 자동 수정

### 코드 포맷팅

```python
# IDE 포맷터로 즉시 포맷팅 (ktlintFormat보다 빠름)
jetbrains.reformat_file(
    path="module-core-domain/src/main/kotlin/.../Service.kt",
    projectPath="/path/to/project-basecamp-server"
)
```

---

## 3. 파일 검색 워크플로우

### 파일명으로 빠른 검색 (인덱스 활용)

```python
# grep보다 훨씬 빠름 - IDE 인덱스 활용
jetbrains.find_files_by_name_keyword(
    nameKeyword="Service",
    fileCountLimit=20,
    timeout=5000,
    projectPath="/path/to/project-basecamp-server"
)
```

### Glob 패턴으로 검색

```python
jetbrains.find_files_by_glob(
    globPattern="**/test/**/*Test.kt",
    fileCountLimit=50,
    timeout=10000,
    projectPath="/path/to/project-basecamp-server"
)
```

### 텍스트 검색 (내용 기반)

```python
# 코드 내용에서 텍스트 검색
jetbrains.search_in_files_by_text(
    searchText="@Transactional",
    directoryToSearch="module-core-domain/src",
    fileMask="*.kt",
    maxUsageCount=50,
    timeout=10000,
    projectPath="/path/to/project-basecamp-server"
)
```

### 정규식 검색

```python
jetbrains.search_in_files_by_regex(
    regexPattern="@Service\\s+class\\s+\\w+",
    directoryToSearch="module-core-domain/src",
    fileMask="*.kt",
    maxUsageCount=30,
    timeout=10000,
    projectPath="/path/to/project-basecamp-server"
)
```

---

## 4. 코드 이해 워크플로우

### Quick Documentation 조회

```python
# 심볼에 대한 문서/타입 정보 조회
jetbrains.get_symbol_info(
    filePath="module-core-domain/src/main/kotlin/.../Service.kt",
    line=45,
    column=20,
    projectPath="/path/to/project-basecamp-server"
)
```

**반환 정보:**
- 심볼 이름, 시그니처, 타입
- 문서 (KDoc/JavaDoc)
- 선언 위치

### 프로젝트 구조 파악

```python
# 디렉토리 트리 조회
jetbrains.list_directory_tree(
    directoryPath="module-core-domain/src/main/kotlin",
    maxDepth=3,
    timeout=5000,
    projectPath="/path/to/project-basecamp-server"
)

# 프로젝트 모듈 목록
jetbrains.get_project_modules(
    projectPath="/path/to/project-basecamp-server"
)

# 의존성 목록
jetbrains.get_project_dependencies(
    projectPath="/path/to/project-basecamp-server"
)
```

### 열린 파일 확인

```python
jetbrains.get_all_open_file_paths(
    projectPath="/path/to/project-basecamp-server"
)
```

---

## 5. 파일 조작 워크플로우

### 파일 생성

```python
jetbrains.create_new_file(
    pathInProject="module-core-domain/src/main/kotlin/.../NewService.kt",
    text="package com.dataops.basecamp.domain.service\n\n@Service\nclass NewService {\n}",
    overwrite=False,
    projectPath="/path/to/project-basecamp-server"
)
```

### 파일 읽기

```python
jetbrains.get_file_text_by_path(
    pathInProject="module-core-domain/src/main/kotlin/.../Service.kt",
    maxLinesCount=500,
    truncateMode="MIDDLE",
    projectPath="/path/to/project-basecamp-server"
)
```

### 텍스트 치환

```python
jetbrains.replace_text_in_file(
    pathInProject="module-core-domain/src/main/kotlin/.../Service.kt",
    oldText="oldMethodName",
    newText="newMethodName",
    replaceAll=True,
    caseSensitive=True,
    projectPath="/path/to/project-basecamp-server"
)
```

### 파일 열기

```python
jetbrains.open_file_in_editor(
    filePath="module-core-domain/src/main/kotlin/.../Service.kt",
    projectPath="/path/to/project-basecamp-server"
)
```

---

## 6. Gradle 명령어 전략 (최소 → 최대)

> **항상 최소 단위 명령어부터 실행하세요. 실패 시 빠르게 피드백을 받을 수 있습니다.**

### 점진적 검증 순서

```bash
# Step 1: 컴파일만 (가장 빠름, 3-5초)
./gradlew :module-core-domain:compileKotlin

# Step 2: QueryDSL Q-Class 생성 (Entity 변경 시, 5-10초)
./gradlew :module-core-domain:kaptKotlin

# Step 3: 테스트 코드 컴파일 (5-10초)
./gradlew :module-core-domain:compileTestKotlin

# Step 4: ktlint 단일 파일 체크 (수정된 파일만)
./gradlew :module-core-domain:ktlintCheck -PktlintFilter="**/ServiceName.kt"

# Step 5: 단일 테스트 실행 (5-10초)
./gradlew :module-core-domain:test --tests "*ServiceTest"

# Step 6: 모듈 전체 테스트 (15-30초)
./gradlew :module-core-domain:test

# Step 7: ktlint 전체 체크 (기능 완료 시)
./gradlew ktlintCheck

# Step 8: 전체 빌드 (기능 완료 후 1회만, 60초+)
./gradlew build
```

### Entity 변경 시 워크플로우

Entity 파일을 수정했다면 Q-Class 재생성이 필요합니다:

```bash
# Entity 수정 후 순서
./gradlew :module-core-domain:compileKotlin           # 컴파일 체크
./gradlew :module-core-domain:kaptKotlin              # Q-Class 재생성
./gradlew :module-core-domain:compileTestKotlin       # 테스트 컴파일
./gradlew :module-core-domain:test --tests "*Test"    # 테스트 실행
```

### ktlint 단계별 실행

```bash
# 단일 파일 체크 (수정한 파일만)
./gradlew :module-core-domain:ktlintCheck -PktlintFilter="**/MyService.kt"

# 모듈 체크
./gradlew :module-core-domain:ktlintCheck

# 전체 체크 (최종 검증)
./gradlew ktlintCheck

# 자동 포맷팅 (필요시)
./gradlew :module-core-domain:ktlintFormat
```

### 명령어 조합 패턴

```bash
# 패턴 1: 빠른 컴파일 체크
./gradlew :module-core-domain:compileKotlin :module-core-domain:compileTestKotlin

# 패턴 2: 컴파일 + 단일 테스트
./gradlew :module-core-domain:compileKotlin :module-core-domain:test --tests "*ServiceTest"

# 패턴 3: Entity 변경 + 테스트
./gradlew :module-core-domain:compileKotlin :module-core-domain:kaptKotlin :module-core-domain:test --tests "*Test"

# 패턴 4: 여러 모듈 컴파일 체크
./gradlew :module-core-domain:compileKotlin :module-core-infra:compileKotlin :module-server-api:compileKotlin

# 패턴 5: 특정 모듈 빌드 (clean 없이)
./gradlew :module-core-domain:build

# 패턴 6: 컴파일 + ktlint + 테스트 (최종 모듈 검증)
./gradlew :module-core-domain:compileKotlin :module-core-domain:ktlintCheck :module-core-domain:test
```

### 모듈별 명령어 참조

| 모듈 | 컴파일 | 테스트 컴파일 | 테스트 |
|------|--------|--------------|--------|
| core-common | `:module-core-common:compileKotlin` | `:module-core-common:compileTestKotlin` | `:module-core-common:test` |
| core-domain | `:module-core-domain:compileKotlin` | `:module-core-domain:compileTestKotlin` | `:module-core-domain:test` |
| core-infra | `:module-core-infra:compileKotlin` | `:module-core-infra:compileTestKotlin` | `:module-core-infra:test` |
| server-api | `:module-server-api:compileKotlin` | `:module-server-api:compileTestKotlin` | `:module-server-api:test` |

### 개발 중 금지 패턴

```bash
# ❌ 개발 반복 중 사용 금지 (매번 실행하면 느려짐)
./gradlew clean build           # 개발 중 금지 → 60-120초 낭비!
./gradlew test                  # 개발 중 금지 → --tests 사용!
./gradlew clean                 # 개발 중 금지 → 캐시 문제 시에만!

# ✅ 개발 중 올바른 사용
./gradlew :module-core-domain:compileKotlin                    # 컴파일만 (3-5초)
./gradlew :module-core-domain:kaptKotlin                       # Q-Class 생성 (Entity 변경 시)
./gradlew :module-core-domain:ktlintCheck -PktlintFilter="**/*.kt"  # 단일 파일 린트
./gradlew :module-core-domain:test --tests "*ServiceTest"       # 단일 테스트 (5-10초)

# ✅ 최종 검증 (기능 완료 후 1회만 허용)
./gradlew ktlintCheck           # 전체 린트 체크
./gradlew build                 # 전체 빌드
./gradlew clean build           # 캐시 문제 시에만
```

### JetBrains MCP와 Gradle 조합

```python
# 1. IDE 검사로 빠른 에러 확인 (0-2초)
jetbrains.get_file_problems(filePath="...", errorsOnly=True)

# 2. 에러 없으면 컴파일 체크 (3-5초)
jetbrains.execute_terminal_command(
    command="./gradlew :module-core-domain:compileKotlin :module-core-domain:compileTestKotlin",
    timeout=30000
)

# 3. 컴파일 성공하면 단일 테스트 (5-10초)
jetbrains.execute_terminal_command(
    command="./gradlew :module-core-domain:test --tests '*ServiceTest'",
    timeout=60000
)

# 4. 기능 완료 후 최종 빌드 (1회만)
jetbrains.execute_terminal_command(
    command="./gradlew build",
    timeout=300000
)
```

---

## 도구 선택 가이드

| 작업 | JetBrains MCP 도구 | 대안 (느림) |
|------|-------------------|-------------|
| **에러 확인** | `get_file_problems` (0-2초) | `compileKotlin` (3-5초) |
| **단일 테스트** | `execute_run_configuration` | `gradlew test --tests` |
| **포맷팅** | `reformat_file` (즉시) | `ktlintFormat` (5초+) |
| **리네임** | `rename_refactoring` (안전) | sed/수동 (위험) |
| **파일 검색** | `find_files_by_name_keyword` | grep/find |
| **텍스트 검색** | `search_in_files_by_text` | grep -r |
| **문서 조회** | `get_symbol_info` | 파일 읽기 |

---

## 워크플로우 요약

### TDD 사이클 (권장)

```
1. 테스트 작성
2. get_file_problems() → 문법 에러 확인
3. execute_run_configuration() 또는 execute_terminal_command() → 테스트 실행
4. 구현
5. get_file_problems() → 에러 확인
6. 테스트 실행 → 통과 확인
7. reformat_file() → 포맷팅
8. 반복
9. 기능 완료 후 → ./gradlew build (1회)
```

### 리팩토링 사이클

```
1. get_file_problems() → 현재 상태 확인
2. rename_refactoring() → 심볼 이름 변경
3. get_file_problems() → 변경 후 에러 확인
4. execute_run_configuration() → 테스트로 검증
```

---

## 주의사항

1. **projectPath 필수**: 모든 도구에 `projectPath` 파라미터 전달 필요
2. **timeout 설정**: 복잡한 작업은 충분한 timeout 설정 (기본 30초)
3. **IDE 실행 필요**: JetBrains IDE가 실행 중이어야 MCP 도구 작동
4. **Run Configuration 사전 설정**: `execute_run_configuration` 사용 시 IDE에서 미리 설정 필요

---

## Sources

- [IntelliJ IDEA MCP Server Documentation](https://www.jetbrains.com/help/idea/mcp-server.html)
- [JetBrains AI Assistant MCP](https://www.jetbrains.com/help/ai-assistant/mcp.html)
- [JetBrains MCP GitHub Repository](https://github.com/JetBrains/mcp-jetbrains)
