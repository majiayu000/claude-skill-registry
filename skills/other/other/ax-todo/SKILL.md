---
name: ax-todo
description: "ToDo 관리 + Confluence 동기화 — 진행현황 리포트 + 차이점 분석"
---

# AX ToDo Skill (ToDo 관리)

프로젝트 ToDo List 관리 및 Confluence 동기화를 수행합니다.
**원장**: project-todo.md (시스템 ToDo)
**미러**: Confluence ToDo 페이지 (읽기 전용)

## 트리거

- `/ax:todo` 명령
- "ToDo 점검해줘", "진행현황 알려줘" 프롬프트

## 사용법

```
/ax:todo                      # 기본: 점검 + 비교 + 업데이트 제안 (전체 실행)
/ax:todo --sync               # + Confluence 동기화 실행
/ax:todo --compare-only       # 비교만 실행 (리포트 없이)
/ax:todo --report-only        # 진행현황 리포트만 출력
/ax:todo --dry-run            # 변경 없이 미리보기
```

## 기본 동작 (옵션 없이 실행 시)

`/ax:todo` 명령은 **기본적으로 다음 3가지를 모두 실행**합니다:

1. **진행현황 리포트** 생성 (Phase별 통계, 완료율)
2. **Confluence 비교** (시스템 vs Confluence 차이점 분석)
3. **업데이트 제안** (상태 변경 필요 항목 안내)

## 실행 흐름

```
┌────────────────────────────────────────────────────────────┐
│ 1단계: project-todo.md 파싱                                 │
│     ↓                                                       │
│ 2단계: 진행현황 분석 (Phase별 통계, 완료율)                   │
│     ↓                                                       │
│ 3단계: Confluence ToDo 조회 (페이지 ID 설정 시)              │
│     ↓                                                       │
│ 4단계: 비교 및 차이점 분석 (SyncDiff 생성)                   │
│     ↓                                                       │
│ 5단계: 리포트 출력 (Markdown 형식)                           │
│     ↓                                                       │
│ 6단계: 업데이트 제안 (코드베이스 컨텍스트 기반)              │
│     ↓ (--sync 옵션 시)                                      │
│ 7단계: Confluence 동기화 실행                                │
└────────────────────────────────────────────────────────────┘
```

## 실행 단계

### 1단계: project-todo.md 파싱

```python
from backend.services import todo_sync_service

# 시스템 ToDo 로드
system_todo = await todo_sync_service.load_system_todo("project-todo.md")
print(f"총 {len(system_todo.items)}개 항목, 버전: {system_todo.version}")
```

**파싱 결과**:
- Phase별 항목 분류 (Phase 1~4)
- 상태별 분류 (completed, in_progress, pending)
- 버전 정보 추출 (v0.5.0 등)

### 2단계: 진행현황 분석

```python
# 진행현황 리포트 생성
report = await todo_sync_service.generate_progress_report(system_todo)

print(f"완료율: {report.completion_rate}%")
print(f"완료: {report.completed}, 진행중: {report.in_progress}, 대기: {report.pending}")
```

**리포트 내용**:

| 항목 | 설명 |
|------|------|
| `total_items` | 전체 ToDo 수 |
| `completed` | 완료 항목 수 |
| `in_progress` | 진행 중 항목 수 |
| `pending` | 대기 항목 수 |
| `completion_rate` | 완료율 (%) |
| `phase_stats` | Phase별 통계 |
| `stale_items` | 장기 미완료 항목 (Phase 1~2) |
| `recommendations` | 권장 사항 |

### 3단계: Confluence ToDo 조회

```python
# Confluence ToDo 로드 (CONFLUENCE_TODO_PAGE_ID 환경변수 필요)
confluence_todo = await todo_sync_service.load_confluence_todo()
```

**환경 변수 미설정 시**: 이 단계는 건너뜁니다.

### 4단계: 비교 및 차이점 분석

```python
# 시스템 vs Confluence 비교
diff = await todo_sync_service.compare(system_todo, confluence_todo)

if diff.has_diff:
    print(f"차이점 발견: {diff.summary}")
```

**SyncDiff 내용**:

| 필드 | 설명 |
|------|------|
| `only_in_system` | 시스템에만 있는 항목 |
| `only_in_confluence` | Confluence에만 있는 항목 (역방향 변경 경고) |
| `status_diff` | 상태가 다른 항목 |
| `content_diff` | 내용이 다른 항목 |

### 5단계: 리포트 출력

```python
# Markdown 형식 리포트
markdown_report = report.to_markdown()
print(markdown_report)
```

**출력 예시**:

```
# 📊 ToDo 진행현황 리포트

**생성일시**: 2026-01-17 10:30:00

---

## 📈 전체 현황

| 항목 | 건수 | 비율 |
|------|------|------|
| ✅ 완료 | 45 | 75% |
| 🚧 진행중 | 10 | 16.7% |
| 📋 대기 | 5 | 8.3% |
| **합계** | **60** | **100%** |

**완료율**: 75%

---

## 📁 Phase별 현황

| Phase | 완료 | 진행중 | 대기 | 완료율 |
|-------|------|--------|------|--------|
| Phase 1 | 15 | 0 | 0 | 100% |
| Phase 2 | 20 | 0 | 0 | 100% |
| Phase 3 | 8 | 7 | 5 | 40% |
| Phase 4 | 2 | 3 | 0 | 40% |

---

## 💡 권장 사항

- Phase 3에 미완료 항목이 5개 있습니다. 우선 처리하거나 스코프 조정을 검토하세요.
```

### 6단계: 업데이트 제안

```python
# 코드베이스 컨텍스트 기반 업데이트 제안
suggestions = await todo_sync_service.suggest_updates(
    system_todo,
    codebase_context="git diff output here..."
)

for suggestion in suggestions:
    print(f"- {suggestion}")
```

### 7단계: Confluence 동기화 (--sync 옵션)

```python
# Confluence에 동기화 (원장 → 미러)
result = await todo_sync_service.sync_to_confluence(system_todo)
print(f"동기화 결과: {result['status']}")
```

**동기화 방향** (단방향):

```
┌─────────────────────────────────────────────────┐
│  project-todo.md (원장)                          │
│         │                                        │
│         ├──→ /ax:todo --sync ──→ Confluence     │
│         │                        (읽기 전용 미러) │
│         │                                        │
│         └──← 수동 업데이트 (사용자/Claude)        │
└─────────────────────────────────────────────────┘
```

- **원장**: project-todo.md
- **Confluence**: 읽기 전용 미러 (팀 공유용)
- **역방향 동기화**: 지원하지 않음 (경고만 표시)

## 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--sync` | Confluence 동기화 실행 | false |
| `--compare-only` | 비교만 실행 (리포트 생략) | false |
| `--report-only` | 진행현황 리포트만 출력 | false |
| `--dry-run` | 실제 변경 없이 미리보기 | false |
| `--path <path>` | project-todo.md 경로 지정 | project-todo.md |

## Confluence 페이지 구조

```
Project TODO (720932) ─────────────── 스프린트 단위 진행현황
    │
    ├── EXT_Desk_D01 ToDo List (753719) ── Play별 세부 작업
    ├── EXT_Desk_D02 ToDo List (TBD)
    └── ...

Play DB (720899) ──────────────────── 세부 작업 페이지 링크만 포함
```

**역할 분리**:

| 페이지 | 용도 | 내용 |
|--------|------|------|
| Project TODO | 스프린트 진행현황 | 버전별 진행률, Phase별 요약 |
| Play ToDo (하위) | Play별 세부 작업 | 상세 체크리스트, 담당자, 목표일 |
| Play DB | Play 진행현황 DB | 통계 테이블 + 하위 페이지 링크 |

## 환경 변수

| 변수 | 용도 | 예시 |
|------|------|------|
| `CONFLUENCE_TODO_PAGE_ID` | Project TODO 페이지 ID | 720932 |
| `CONFLUENCE_PLAY_DB_PAGE_ID` | Play DB 페이지 ID | 720899 |

**설정 예시** (.env):

```env
CONFLUENCE_TODO_PAGE_ID=720932
CONFLUENCE_PLAY_DB_PAGE_ID=720899
```

## Play ToDo 하위 페이지 관리

새로운 Play ToDo 페이지 생성 시:

```python
# 1. Project TODO 하위에 페이지 생성
await confluence.create_page(
    title=f"{play_id} ToDo List",
    body_md=todo_content,
    parent_id="720932"  # Project TODO
)

# 2. Project TODO에 링크 추가
await confluence.append_to_page(
    page_id="720932",
    append_md=f"- [{play_id} ToDo List](page_url)"
)

# 3. Play DB에 링크 추가
await confluence.append_to_page(
    page_id="720899",
    append_md=f"- [{play_id} ToDo List](page_url)"
)
```

## 출력 예시

### 기본 실행 (`/ax:todo`)

```
🔄 ToDo 점검 시작...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 1. project-todo.md 파싱
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 파싱 완료
   버전: 0.5.0
   총 항목: 60개
   Phase 수: 4개

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 2. 진행현황 분석
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| 상태 | 건수 | 비율 |
|------|------|------|
| ✅ 완료 | 45 | 75% |
| 🚧 진행중 | 10 | 16.7% |
| 📋 대기 | 5 | 8.3% |

**완료율**: 75%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 3. Confluence 비교
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| 차이점 | 건수 |
|--------|------|
| 시스템에만 있음 | 3 |
| Confluence에만 있음 | 0 |
| 상태 차이 | 2 |
| 내용 차이 | 1 |

⚠️ 시스템과 Confluence 간 6개 차이점 발견

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 4. 업데이트 제안
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- [Phase3-5] 'WF-06 Confluence Sync...' - 관련 코드가 변경되었습니다. 완료 상태로 업데이트하세요.
- [Phase3-8] 'Teams 연동...' - 이전 Phase 항목이 아직 미완료입니다. 상태를 확인하세요.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 점검 완료
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Confluence에 동기화하려면: /ax:todo --sync
```

### 동기화 실행 (`/ax:todo --sync`)

```
... (위 출력에 이어서)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📤 5. Confluence 동기화
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 동기화 완료
   Page ID: 123456789
   동기화된 항목: 60개
```

## 에러 처리

| 에러 | 메시지 | 해결 방법 |
|------|--------|----------|
| 파일 없음 | "project-todo.md를 찾을 수 없습니다" | 파일 경로 확인 |
| Confluence 미설정 | "CONFLUENCE_TODO_PAGE_ID 미설정" | .env 파일에 환경변수 추가 |
| Confluence 연결 실패 | "Confluence 연결 실패" | API 토큰 및 네트워크 확인 |
| 역방향 변경 감지 | "⚠️ Confluence에만 있는 항목 발견" | 시스템 ToDo에 수동 반영 필요 |

## 연계 Skill/Agent

| Skill/Agent | 역할 | 연계 방식 |
|-------------|------|----------|
| `/ax:wrap-up` | 작업 정리 시 ToDo 업데이트 | project-todo.md 완료 체크 |
| `/ax:confluence` | Confluence 동기화 | ConfluenceMCP 호출 |
| `confluence_sync` | 페이지 업데이트 | update_page 호출 |

## 관련 파일

- [project-todo.md](../../../project-todo.md) - 시스템 ToDo (원장)
- [backend/services/todo_parser.py](../../../backend/services/todo_parser.py) - 파서
- [backend/services/todo_sync_service.py](../../../backend/services/todo_sync_service.py) - 동기화 서비스
