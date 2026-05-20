---
name: ax-confluence
description: "Confluence 동기화 규칙 — DB/Live doc 업데이트"
---

# /ax:confluence Command

Confluence 페이지를 동기화하고 업데이트합니다.

## 트리거

- `/ax:confluence` 명령
- "Confluence 동기화" 프롬프트
- "Confluence 업데이트" 프롬프트

## 사용법

```
/ax:confluence [--action <sync|update|import|status>] [--target <page|db|all>]
```

## 인자

| 인자 | 필수 | 설명 | 예시 |
|------|------|------|------|
| `--action` | | 실행할 작업 | sync (기본), update, import, status |
| `--target` | | 동기화 대상 | page, db, all |
| `--page-id` | | 특정 페이지 ID | 123456789 |
| `--dry-run` | | 실제 실행 없이 미리보기 | |

## 실행 단계

### 1단계: 동기화 대상 확인

```bash
# API 호출
GET /api/workflows/confluence-sync/status
```

- 동기화 대상 식별 (Signal, Scorecard, Brief, Activity)
- DB vs Confluence 데이터 비교

### 2단계: 데이터 수집

```python
# DB에서 최신 데이터 조회
signals = await signal_repo.list_all()
briefs = await brief_repo.list_all()
activities = await activity_repo.list_all()
```

### 3단계: Confluence 업데이트

```python
# WF-06 Confluence Sync 실행
POST /api/workflows/confluence-sync
{
  "targets": [
    {"target_type": "page", "action": "update"},
    {"target_type": "db", "action": "sync"}
  ]
}
```

## 출력 예시

```
🔄 Confluence 동기화 시작...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 1. 동기화 대상 확인
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

동기화 대상:
  📄 프로젝트 현황 페이지
  📊 Play DB 테이블
  📝 Action Log

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 2. 데이터 수집
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Signal: 35건 (신규 3건)
✅ Scorecard: 28건 (신규 2건)
✅ Brief: 12건 (신규 1건)
✅ Activity: 45건 (신규 5건)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 3. Confluence 업데이트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 프로젝트 현황 업데이트 완료
✅ Play DB 동기화 완료 (5 rows updated)
✅ Action Log 기록 완료 (11 entries)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 동기화 완료
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📎 https://confluence.../ax-discovery-portal
```

## Confluence 페이지 구조

```
AX-BD Space
├── Project TODO (720932) ─────────── 스프린트 단위 진행현황
│   ├── EXT_Desk_D01 ToDo (753719)   ── Play별 세부 작업
│   ├── EXT_Desk_D02 ToDo (TBD)
│   └── ...
├── Play 진행현황 DB (720899) ─────── 43개 Play 통계 테이블 + 하위 페이지 링크
├── Action Log (786433) ────────────── 작업 이력 기록
├── 프로젝트 현황 (753665) ─────────── 개요 페이지
├── Plays/
│   ├── EXT_Desk_D01_Seminar/
│   │   └── Live doc              ← 이벤트별 append
│   ├── KT_Sales_S01_Interview/
│   │   └── Live doc
│   └── ...
└── Briefs/
    ├── BRF-2025-001/
    └── ...
```

**페이지 역할**:

| 페이지 | ID | 용도 |
|--------|-----|------|
| Project TODO | 720932 | 스프린트 진행현황, Play ToDo 하위 페이지 부모 |
| Play DB | 720899 | 43개 Play 통계 테이블, 하위 페이지 링크 |
| Action Log | 786433 | 작업 이력 append |
| 프로젝트 현황 | 753665 | 프로젝트 개요 |
| EXT_Desk_D01 ToDo | 753719 | 세미나파이프라인 세부 작업 |

## Play DB 필드

| 필드 | 타입 | 설명 | 업데이트 주기 |
|------|------|------|-------------|
| play_id | text | Play 고유 ID | 고정 |
| status | select | G/Y/R | 주간 |
| activity_qtd | number | 분기 Activity 수 | 실시간 |
| signal_qtd | number | 분기 Signal 수 | 실시간 |
| brief_qtd | number | 분기 Brief 수 | 실시간 |
| s2_qtd | number | 분기 S2 수 | 실시간 |
| last_updated | date | 최종 수정일 | 자동 |

## Action Log 필드

| 필드 | 타입 | 설명 |
|------|------|------|
| log_id | text | 로그 ID |
| play_id | text | Play ID |
| action_type | select | Activity/Signal/Brief/S2/S3 |
| title | text | 제목 |
| actor | user | 수행자 |
| created_at | date | 생성일시 |

## API 엔드포인트

| 엔드포인트 | 용도 |
|-----------|------|
| `POST /api/workflows/confluence-sync` | 동기화 실행 |
| `POST /api/workflows/confluence-sync/preview` | 미리보기 |
| `POST /api/workflows/confluence-sync/import` | 역방향 동기화 |
| `GET /api/workflows/confluence-sync/status` | 상태 조회 |

## 에러 처리

| 에러 | 메시지 | 해결 방법 |
|------|--------|----------|
| 인증 실패 | "Confluence 인증 실패" | CONFLUENCE_API_TOKEN 확인 |
| 페이지 없음 | "페이지를 찾을 수 없습니다" | page_id 확인 |
| 버전 충돌 | "페이지가 수정되었습니다" | 재시도 |

## 환경 변수

```env
# Confluence 연결
CONFLUENCE_BASE_URL=https://your-domain.atlassian.net/wiki
CONFLUENCE_API_TOKEN=your-api-token
CONFLUENCE_USER_EMAIL=your-email@example.com
CONFLUENCE_SPACE_KEY=AB

# 페이지 ID
CONFLUENCE_TODO_PAGE_ID=720932       # Project TODO (스프린트 진행현황)
CONFLUENCE_PLAY_DB_PAGE_ID=720899    # Play DB (통계 테이블)
CONFLUENCE_ACTION_LOG_PAGE_ID=786433 # Action Log
CONFLUENCE_PROJECT_STATUS_PAGE_ID=753665  # 프로젝트 현황
```

## 관련 커맨드

- `/ax:kpi-digest` - KPI 리포트 생성 후 Confluence 공유
- `/ax:brief` - Brief 생성 후 자동 동기화
- `/ax:wrap-up` - 작업 완료 후 문서 업데이트
