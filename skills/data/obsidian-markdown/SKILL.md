---
name: obsidian-markdown
description: Obsidian vault의 마크다운 문서 작업을 위한 Skill. markdown-oxide LSP를 활용하여 백링크 검색, 태그 탐색, 링크 관계 분석, Daily notes 관리를 수행. Obsidian vault, PKM, 마크다운 노트, 위키링크([[link]]), 태그(#tag), 백링크, 노트 검색, 문서 구조 분석 작업 시 사용.
allowed-tools: Read, Grep, Glob, LS, mcp__markdown-oxide
---

# Obsidian Markdown Skill

Obsidian vault에서 마크다운 문서 작업을 효율적으로 수행하기 위한 Skill.

## 핵심 기능

### 1. LSP 기반 검색 (markdown-oxide)

markdown-oxide MCP 서버가 연결되어 있으면 다음 기능 활용:

- **Find References**: 특정 노트를 참조하는 모든 백링크 찾기
- **Go to Definition**: `[[링크]]`에서 실제 파일로 이동
- **Tag Search**: `#tag` 사용 위치 모두 검색
- **Completion**: 링크, 태그, 헤딩 자동완성 정보 활용

### 2. Vault 구조 파악

작업 전 항상 vault 구조를 먼저 파악:

```bash
# 디렉토리 구조 확인
ls -la

# MOC(Map of Content) 노트 찾기
find . -name "*MOC*" -o -name "*Index*" -o -name "*목차*"

# 최근 수정된 노트 확인
find . -name "*.md" -mtime -7
```

### 3. 토큰 효율적 접근

대량 문서 작업 시 계층적 접근:

1. MOC/Index 노트 먼저 읽기
2. LSP로 관련 노트 식별
3. 필요한 노트만 선택적 로드
4. 작업 완료 후 `/compact` 권장

## 작업 지침

### 노트 검색 시

```
1. LSP find_references 우선 사용 (가능한 경우)
2. LSP 불가 시 Grep으로 [[노트명]] 패턴 검색
3. 태그 검색: grep -r "#태그명" --include="*.md"
```

### 링크 관계 분석 시

```
1. 대상 노트의 outgoing links 파악 (노트 내 [[링크]] 추출)
2. incoming links(백링크) 파악 (LSP 또는 grep)
3. 관계도 시각화 필요 시 Mermaid 다이어그램 생성
```

### 문서 수정 시

```
1. 수정 전 백링크 확인 (영향 범위 파악)
2. 파일명 변경 시 모든 참조 함께 업데이트
3. 헤딩 변경 시 앵커 링크([[노트#헤딩]]) 확인
```

### Daily Notes 작업 시

```
1. Daily note 형식 확인 (YYYY-MM-DD.md 등)
2. 날짜 기반 검색: find . -name "2025-01-*.md"
3. 특정 기간 노트 일괄 처리 가능
```

## Obsidian 특화 문법

### 지원하는 문법

| 문법             | 설명        | 예시                   |
| ---------------- | ----------- | ---------------------- |
| `[[링크]]`       | 내부 링크   | `[[노트 제목]]`        |
| `[[링크\|별칭]]` | 별칭 링크   | `[[긴제목\|짧은이름]]` |
| `[[링크#헤딩]]`  | 헤딩 링크   | `[[노트#섹션]]`        |
| `![[임베드]]`    | 노트 임베드 | `![[포함할노트]]`      |
| `#태그`          | 태그        | `#project/active`      |
| `#태그/하위`     | 중첩 태그   | `#status/in-progress`  |

### Frontmatter 처리

```yaml
---
title: 노트 제목
created: 2025-01-13
tags:
  - tag1
  - tag2
aliases:
  - 별칭1
  - 별칭2
---
```

- `aliases`: 다른 이름으로도 링크 가능
- `tags`: frontmatter 태그와 인라인 태그 모두 인식

## MCP 서버 설정

markdown-oxide MCP 서버 연결이 필요합니다.

### 설정 방법

```bash
# markdown-oxide 설치
brew install markdown-oxide
# 또는
cargo install --locked markdown-oxide

# MCP 서버 추가
claude mcp add-json "markdown-oxide" '{
  "type": "stdio",
  "command": "npx",
  "args": ["tritlo/lsp-mcp", "markdown", "markdown-oxide"]
}'
```

### 환경 변수

```bash
export ENABLE_LSP_TOOL=1
```

자세한 설정은 [REFERENCE.md](REFERENCE.md) 참조.

## 예시

### 백링크 검색

```
> "TDD" 노트를 참조하는 모든 노트를 찾아줘

1. LSP find_references로 [[TDD]] 검색
2. 결과: 15개 노트에서 참조
   - docs/development/테스트.md:23
   - daily/2025-01-10.md:45
   ...
```

### 태그 기반 분석

```
> #project/active 태그가 있는 노트들의 상태를 정리해줘

1. grep -r "#project/active" --include="*.md"
2. 각 노트의 frontmatter 확인
3. 상태 테이블 생성
```

### 링크 구조 분석

```
> "아키텍처" 노트의 링크 관계를 분석해줘

1. 아키텍처.md 읽기 (outgoing links 파악)
2. 백링크 검색 (incoming links)
3. Mermaid 다이어그램으로 시각화
```

## 주의사항

1. **대량 파일 로드 금지**: 한 번에 10개 이하 파일만 처리
2. **archive 폴더 주의**: 아카이브된 노트는 필요시에만 접근
3. **토큰 관리**: 작업 완료 후 `/compact` 실행 권장
4. **LSP 우선**: 텍스트 검색보다 LSP 기능 우선 사용

## 관련 파일

- [REFERENCE.md](REFERENCE.md): 상세 설정 및 고급 기능
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md): 문제 해결 가이드
