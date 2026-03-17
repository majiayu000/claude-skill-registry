---
name: obsidian-vault
description: |
  Obsidian vault 및 마크다운 문서 작업 시 사용. markdown-oxide LSP를 통한 효율적인 검색,
  백링크 탐색, 태그 관리 지원. vault 경로, 태그 체계, vault-intelligence CLI, 토큰 최적화 전략 제공.
  Obsidian, vault, 마크다운, 태그, 노트 정리, zettelkasten, 백링크, wiki-link, PKM 관련 작업 시 자동 적용.
---

# Obsidian Vault 작업 가이드

## 경로 정보

| 항목 | 경로 |
|------|------|
| vault | `~/DocumentsLocal/msbaek_vault/` |
| vault-intelligence | `~/git/vault-intelligence/` |

## markdown-oxide LSP 활용

### 사용 가능한 LSP 기능

markdown-oxide MCP 서버가 연결되어 있으면 다음 기능을 활용할 수 있다:

1. **Go to Definition**: `[[링크]]` → 해당 파일로 이동
2. **Find References (백링크)**: 특정 노트를 참조하는 모든 노트 검색
3. **Tag Search**: `#태그`가 사용된 모든 위치 검색
4. **Completion**: 링크, 태그, 프로퍼티 자동완성
5. **Diagnostics**: 깨진 링크, 존재하지 않는 노트 감지

### LSP 기반 검색 예시

```
# 백링크 찾기
"TDD 노트를 참조하는 모든 노트 찾아줘"
→ LSP find_references 사용

# 태그 검색
"#project/active 태그가 있는 노트들 찾아줘"
→ LSP find_references 사용

# 깨진 링크 확인
"이 vault에서 깨진 링크가 있는 노트 확인해줘"
→ LSP diagnostics 사용
```

### LSP 우선 원칙

마크다운 파일 검색 시:
1. **우선**: markdown-oxide LSP 도구 사용 (빠르고 정확)
2. **차선**: vault-intelligence CLI (시맨틱 검색 필요 시)
3. **최후**: grep/ripgrep (단순 텍스트 매칭)

## 태그 체계

### Hierarchical Tags

- 형식: `#category/subcategory/detail`
- 5가지 카테고리: Topic, Document Type, Source, Status, Project

### Zettelkasten 폴더 구조

| 폴더 | 용도 | 작업 권한 |
|------|------|-----------|
| 000-SLIPBOX | 개인 인사이트 | 읽기/쓰기 |
| 001-INBOX | 수집함 | 읽기/쓰기 |
| 003-RESOURCES | 참고자료 | 주로 읽기 |
| archive | 보관 자료 | **접근 금지** |

### 상세 가이드

- 태그: `vault_root/vault-analysis/improved-hierarchical-tags-guide.md`

## vault-intelligence CLI

### 기본 사용법

```bash
cd ~/git/vault-intelligence
python -m src search --query "검색어" --search-method hybrid --top-k 10
```

### 주요 옵션

| 옵션 | 값 | 설명 |
|------|-----|------|
| `--search-method` | semantic, keyword, hybrid, colbert | hybrid 권장 |
| `--rerank` | (플래그) | 재순위화로 정확도 향상 |
| `--expand` | (플래그) | 쿼리 확장 (동의어 + HyDE) |
| `--top-k` | 숫자 | 반환 결과 수 |

### 자주 실수하는 옵션

| ❌ 잘못된 옵션 | ✅ 올바른 옵션 |
|---------------|---------------|
| `--method` | `--search-method` |
| `--k` | `--top-k` |
| `--output-file` | `--output` |
| `--reranking` | `--rerank` |

### 상세 가이드

- `~/git/vault-intelligence/CLAUDE.md`

## 토큰 최적화 전략

### 작업 원칙

1. **한 번에 10개 이하 파일 처리**
2. **archive, .obsidian 폴더 무시**
3. **MOC 노트 먼저 읽고 관련 노트만 선택적 로드**
4. **20회 반복 후 `/compact` 또는 `/clear`**

### 효율적인 요청 패턴

```
# ❌ 비효율적
"vault의 모든 파일을 분석해줘"

# ✅ 효율적
"003-RESOURCES에서 'kubernetes' 태그가 있는 노트 목록만 보여줘"
```

### 컨텍스트 관리

| 명령어 | 용도 | 시점 |
|--------|------|------|
| `/compact` | 히스토리 압축 | 70% 사용 시 |
| `/clear` | 초기화 | 새 작업 시작 |
| `/cost` | 토큰 확인 | 수시 |

## 파일 처리 시 주의사항

### 제외 대상

- `.obsidian/` 폴더
- `archive/` 폴더
- `.canvas` 파일
- 이미지 파일 (`.png`, `.jpg`, `.gif` 등)

### 오류 처리

- 읽기 오류 파일은 `UNPROCESSED-FILES.md`에 기록
- 인코딩 문제 시 UTF-8로 재시도

## 검색 도구 선택 가이드

| 검색 유형 | 권장 도구 |
|-----------|-----------|
| 백링크/참조 관계 | markdown-oxide LSP |
| 태그 기반 검색 | markdown-oxide LSP |
| 시맨틱 검색 (의미 기반) | vault-intelligence |
| 단순 키워드 매칭 | ripgrep |
| 파일명 검색 | glob/find |
