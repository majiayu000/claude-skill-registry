---
name: project-time-tracker
description: |
  프로젝트별 Claude Code 세션 시간을 집계하여 리포트 생성.
  일별/주별/월별 시간 분포를 Obsidian 테이블로 시각화.
  "시간 추적", "프로젝트 시간", "time tracking" 등의 요청 시 자동 적용.
---

# Project Time Tracker Skill

## 개요

Claude Code 세션 로그의 타임스탬프를 분석하여 **프로젝트별 작업 시간**을 집계하고, 일별/주별/월별 리포트를 생성하는 skill.

## 사용 방식

```bash
/project-time-tracker              # 이번 주 시간 리포트
/project-time-tracker daily        # 오늘 시간 리포트
/project-time-tracker weekly       # 이번 주 시간 리포트 (기본값)
/project-time-tracker monthly      # 이번 달 시간 리포트
/project-time-tracker 2026-01-15   # 특정 날짜 시간 리포트
```

## 경로 정보

| 항목 | 경로 |
|------|------|
| 세션 로그 | `~/.claude/projects/[encoded-path]/*.jsonl` |
| 출력 | `~/DocumentsLocal/msbaek_vault/analytics/time-tracking/` |

---

## 데이터 구조

### 세션 로그 위치
```
~/.claude/projects/
├── -Users-msbaek-project-a/
│   ├── abc123.jsonl
│   └── def456.jsonl
├── -Users-msbaek-project-b/
│   └── ghi789.jsonl
└── ...
```

### JSONL 타임스탬프 추출

세션 시간 계산:
- **시작 시간**: 첫 번째 레코드의 `timestamp` 필드
- **종료 시간**: 마지막 레코드의 `timestamp` 필드
- **세션 시간**: 종료 - 시작

```bash
# 세션 시작/종료 시간 추출
jq -s '[.[0].timestamp, .[-1].timestamp] |
  {start: .[0], end: .[1],
   duration_min: ((.[1] | fromdateiso8601) - (.[0] | fromdateiso8601)) / 60}' \
  session.jsonl
```

---

## 실행 절차

### Step 1: 분석 기간 결정

```bash
# 모드에 따른 기간 설정
MODE="${1:-weekly}"

case "$MODE" in
  daily|today)
    START_DATE=$(date +%Y-%m-%d)
    END_DATE=$(date -v+1d +%Y-%m-%d)
    PERIOD_NAME="일일"
    ;;
  weekly)
    START_DATE=$(date -v-$(($(date +%u) - 1))d +%Y-%m-%d)  # 이번 주 월요일
    END_DATE=$(date -v+1d +%Y-%m-%d)
    PERIOD_NAME="주간"
    ;;
  monthly)
    START_DATE=$(date +%Y-%m-01)  # 이번 달 1일
    END_DATE=$(date -v+1d +%Y-%m-%d)
    PERIOD_NAME="월간"
    ;;
  *)
    # 특정 날짜
    START_DATE="$MODE"
    END_DATE=$(date -j -f "%Y-%m-%d" -v+1d "$MODE" +%Y-%m-%d)
    PERIOD_NAME="일일"
    ;;
esac

echo "분석 기간: $START_DATE ~ $END_DATE ($PERIOD_NAME)"
```

### Step 2: 해당 기간 세션 로그 수집

```bash
# 기간 내 수정된 세션 로그 찾기
find ~/.claude/projects -name "*.jsonl" \
  -newermt "$START_DATE 00:00:00" \
  ! -newermt "$END_DATE 00:00:00" 2>/dev/null
```

### Step 3: 프로젝트별 시간 집계

```bash
# 프로젝트 경로 디코딩 함수
decode_project_path() {
  echo "$1" | sed 's/-/\//g' | sed 's/^\/Users\/msbaek\///'
}

# 각 세션 시간 계산 및 프로젝트별 집계
for session in $(find ~/.claude/projects -name "*.jsonl" -newermt "$START_DATE"); do
  PROJECT_DIR=$(dirname "$session" | xargs basename)
  PROJECT_NAME=$(decode_project_path "$PROJECT_DIR")

  # 세션 시간 계산 (분 단위)
  DURATION=$(jq -s '
    if length > 1 then
      (((.[-1].timestamp | fromdateiso8601) - (.[0].timestamp | fromdateiso8601)) / 60) | floor
    else
      0
    end
  ' "$session" 2>/dev/null || echo "0")

  echo "$PROJECT_NAME: ${DURATION}분"
done | sort | uniq -c | sort -rn
```

### Step 4: 일별 분포 계산 (주간/월간 리포트용)

```bash
# 각 세션의 날짜별 시간 분포
for session in $(find ~/.claude/projects -name "*.jsonl" -newermt "$START_DATE"); do
  # 세션 시작 날짜 추출
  SESSION_DATE=$(jq -r '.[0].timestamp[:10]' "$session" 2>/dev/null)
  # ... 집계
done
```

### Step 5: 리포트 생성

#### 일일 리포트
```markdown
---
created: {DATE}
type: time-tracking
period: daily
date: {TARGET_DATE}
tags:
  - analytics/time
  - analytics/daily
---

# 시간 추적 - {TARGET_DATE}

## 오늘 작업 시간

| 프로젝트 | 세션 수 | 작업 시간 |
|---------|--------|----------|
| project-a | 3 | 2h 30m |
| project-b | 2 | 1h 15m |
| **합계** | **5** | **3h 45m** |

## 세션 상세

| 시작 | 종료 | 프로젝트 | 시간 |
|-----|-----|---------|-----|
| 09:30 | 11:00 | project-a | 1h 30m |
| 14:00 | 15:00 | project-b | 1h 00m |
| ... | ... | ... | ... |
```

#### 주간 리포트
```markdown
---
created: {DATE}
type: time-tracking
period: weekly
week: {WEEK_NUM}
tags:
  - analytics/time
  - analytics/weekly
---

# 주간 시간 추적 - {WEEK_NUM}

> 분석 기간: {START_DATE} (월) ~ {END_DATE} (금)

## 프로젝트별 총 시간

| 프로젝트 | 세션 수 | 총 시간 | 비율 |
|---------|--------|--------|-----|
| project-a | 12 | 8h 30m | 45% |
| project-b | 8 | 5h 20m | 28% |
| project-c | 5 | 3h 10m | 17% |
| 기타 | 3 | 1h 50m | 10% |
| **합계** | **28** | **18h 50m** | **100%** |

## 일별 시간 분포

| 프로젝트 | 월 | 화 | 수 | 목 | 금 | 합계 |
|---------|-----|-----|-----|-----|-----|------|
| project-a | 2h | 1h30m | 2h | 1h30m | 1h30m | 8h30m |
| project-b | 1h | 1h | 1h30m | 1h | 50m | 5h20m |
| ... | ... | ... | ... | ... | ... | ... |

## 일별 총 작업 시간

| 요일 | 세션 수 | 총 시간 |
|-----|--------|--------|
| 월 | 5 | 3h 30m |
| 화 | 6 | 4h 00m |
| 수 | 7 | 4h 15m |
| 목 | 5 | 3h 45m |
| 금 | 5 | 3h 20m |
```

#### 월간 리포트
```markdown
---
created: {DATE}
type: time-tracking
period: monthly
month: {MONTH}
tags:
  - analytics/time
  - analytics/monthly
---

# 월간 시간 추적 - {MONTH}

## 프로젝트별 총 시간

| 프로젝트 | 세션 수 | 총 시간 | 비율 |
|---------|--------|--------|-----|
| ... | ... | ... | ... |

## 주간별 분포

| 프로젝트 | W01 | W02 | W03 | W04 | 합계 |
|---------|-----|-----|-----|-----|------|
| project-a | 8h | 10h | 7h | 9h | 34h |
| ... | ... | ... | ... | ... | ... |

## 일별 추이 (그래프용 데이터)

| 날짜 | 시간(분) |
|-----|---------|
| 01 | 180 |
| 02 | 210 |
| ... | ... |
```

---

## 시간 계산 규칙

### 세션 시간 산정
- **기본 방식**: 첫 레코드 ~ 마지막 레코드 시간 차이
- **공백 처리**: 10분 이상 공백은 미활동으로 간주하여 제외 (선택적)
- **최소 단위**: 5분 이하 세션은 5분으로 올림

### 시간 형식
| 분 | 표시 형식 |
|----|----------|
| 30 | 30m |
| 60 | 1h |
| 90 | 1h 30m |
| 150 | 2h 30m |

```bash
# 분 → 시간:분 변환
format_duration() {
  local mins=$1
  local hours=$((mins / 60))
  local remaining=$((mins % 60))
  if [ $hours -gt 0 ]; then
    echo "${hours}h ${remaining}m"
  else
    echo "${remaining}m"
  fi
}
```

---

## 에러 처리

- 세션 없음: "해당 기간에 Claude Code 세션 없음" 반환
- 타임스탬프 없음: 해당 세션 건너뛰기
- 파싱 오류: 세션 건너뛰고 계속 진행

---

## 관련 Skill

- `weekly-claude-analytics`: 주간 종합 분석 (시간 외 다른 지표 포함)
- `daily-work-logger`: 일일 작업 로그
- `usage-pattern-analyzer`: 도구 사용 패턴 분석
