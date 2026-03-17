---
name: daily-work-logger
description: |
  매일 아침 업무 시작 전 어제 작업 내역을 정리하여 Daily Note에 반영.
  서브 에이전트 기반 병렬 처리로 메인 컨텍스트 절약.
  "어제 작업 정리해줘", "daily log", "업무 내역 정리" 등의 요청 시 자동 적용.
---

# Daily Work Logger Skill

## 개요

매일 아침 업무 시작 전 실행하여 어제 작성/수정된 문서들에서 **업무 수행 관련 내용**을 추출하고 해당 날짜의 Daily Note에 **자동으로 반영**하는 skill.

## 핵심 아키텍처

> **서브 에이전트 기반 병렬 처리**로 메인 에이전트의 컨텍스트를 최소화합니다.

```
┌─────────────────────────────────────────────────────────────┐
│                    Main Agent (Orchestrator)                 │
│  - 날짜 결정 (Phase 1)                                        │
│  - 서브 에이전트 병렬 실행 (Phase 2)                            │
│  - 결과 수집 및 Daily Note 반영 (Phase 3)                      │
└─────────────────────────────────────────────────────────────┘
                              │
   ┌───────────┬───────┬──────┼──────┬───────────┐
   │           │       │      │      │           │
   ▼           ▼       ▼      ▼      ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ Sub 1  │ │ Sub 2  │ │ Sub 3  │ │ Sub 4  │ │ Sub 5  │
│ Vault  │ │ CC     │ │ Meetng │ │ Learn  │ │ Things │
│ Files  │ │ Sessns │ │ Notes  │ │ Extrcr │ │ Analzr │
└────────┘ └────────┘ └────────┘ └────────┘ └────────┘
   │           │       │      │      │           │
   └───────────┴───────┴──────┼──────┴───────────┘
                              ▼
                   ┌─────────────────┐
                   │ Daily Note 반영  │
                   │ (Main Agent)    │
                   └─────────────────┘
```

## 인수 (Arguments)

| 인수 | 설명 | 기본값 |
|------|------|--------|
| 날짜 | 분석할 날짜 (YYYY-MM-DD 형식) | 어제 날짜 |

**사용 예시**:
- `/daily-work-logger` - 어제 날짜 분석 및 반영
- `/daily-work-logger 2026-01-12` - 특정 날짜 분석 및 반영

## 경로 정보

| 항목 | 경로 |
|------|------|
| vault | `~/DocumentsLocal/msbaek_vault/` |
| dailies | `~/DocumentsLocal/msbaek_vault/notes/dailies/` |
| 미팅 노트 | `notes/dailies/YYYY-MM-DD-*.md` |
| 기술 문서 | `001-INBOX/`, `003-RESOURCES/` |
| Claude 세션 | `~/.claude/projects/` |

---

## 실행 절차

### Phase 1: 초기화 (메인 에이전트 - 순차)

1. **날짜 결정** - 인수가 없으면 어제 날짜 사용
```bash
TARGET_DATE="${1:-$(date -v-1d +%Y-%m-%d)}"
NEXT_DATE=$(date -j -f "%Y-%m-%d" -v+1d "$TARGET_DATE" +%Y-%m-%d)
echo "대상 날짜: $TARGET_DATE"
```

2. **Daily Note 경로 확인**
```bash
DAILY_NOTE="$HOME/DocumentsLocal/msbaek_vault/notes/dailies/${TARGET_DATE}.md"
```

---

### Phase 2: 서브 에이전트 병렬 실행 ★

> **중요**: 아래 5개의 Task를 **단일 메시지에서 동시에 호출**하여 병렬 실행합니다.
> 각 서브 에이전트는 분석 결과를 **마크다운 형식의 텍스트**로 반환합니다.
> 비용/속도 최적화를 위해 **haiku 모델**을 사용합니다.

---

#### SubAgent 1: Vault Files Analyzer

**Task 호출 파라미터:**
| 파라미터 | 값 |
|---------|-----|
| description | "Vault 파일 분석" |
| subagent_type | "general-purpose" |
| model | "haiku" |

**프롬프트 (TARGET_DATE, NEXT_DATE 치환 필요):**

```
당신은 Obsidian Vault 파일 분석 전문가입니다. 코드를 작성하지 말고 분석만 수행하세요.

## 작업
{TARGET_DATE} 날짜에 생성/수정된 파일들을 분석하여 업무 관련 내용을 추출합니다.

## 경로
- Vault: ~/DocumentsLocal/msbaek_vault/
- 분석 대상 디렉토리: 001-INBOX/, 003-RESOURCES/, 000-SLIPBOX/, work-log/

## 실행 단계
1. Bash로 해당 날짜에 수정된 .md 파일 찾기 (macOS 호환):
   find ~/DocumentsLocal/msbaek_vault -name "*.md" -type f -exec stat -f "%Sm %N" -t "%Y-%m-%d" {} \; 2>/dev/null | grep "{TARGET_DATE}" | awk '{print $2}' | grep -v "notes/dailies/"

   **주의**: macOS BSD find는 `-newermt` 옵션이 다르게 동작하므로 `stat` + `grep` 조합 사용

2. 발견된 각 파일의 내용 읽기 (Read 도구 사용)

3. 업무 관련 내용 추출:
   - 기술 학습 내용
   - 문서 작성/수정 내용
   - 프로젝트 관련 작업

## 출력 형식 (마크다운으로 반환)
### Vault 문서 작업
- **[파일명]**: 작업 내용 요약 (1-2줄)

(파일이 없으면 "해당 날짜에 수정된 vault 문서 없음" 반환)
```

---

#### SubAgent 2: Claude Sessions Analyzer

**Task 호출 파라미터:**
| 파라미터 | 값 |
|---------|-----|
| description | "Claude 세션 분석" |
| subagent_type | "general-purpose" |
| model | "haiku" |

**프롬프트 (TARGET_DATE, NEXT_DATE 치환 필요):**

```
당신은 Claude Code 세션 로그 분석 전문가입니다. 코드를 작성하지 말고 분석만 수행하세요.

## 작업
{TARGET_DATE} 날짜의 Claude Code 세션 로그를 분석하여 수행한 작업을 추출합니다.

## 경로
- Claude 프로젝트: ~/.claude/projects/

## 실행 단계
1. Bash로 해당 날짜 세션 로그 찾기 (macOS 호환):
   find ~/.claude/projects -name "*.jsonl" -type f -exec stat -f "%Sm %N" -t "%Y-%m-%d" {} \; 2>/dev/null | grep "{TARGET_DATE}" | awk '{print $2}'

   **주의**: macOS BSD find는 `-newermt` 옵션이 다르게 동작하므로 `stat` + `grep` 조합 사용

2. 각 세션 로그에서 추출할 정보 (Bash로 head -100 등으로 일부만 읽기):
   - 프로젝트 경로 (어떤 프로젝트에서 작업했는지) - 파일 경로에서 프로젝트명 추출
   - 주요 작업 내용 (코드 작성, 버그 수정, 리팩토링 등)
   - 사용자 요청 메시지 요약

3. JSONL 파일 분석 시 jq 사용:
   head -50 [파일] | jq -r 'select(.type=="user") | .message.content[:200]' 2>/dev/null

## 출력 형식 (마크다운으로 반환)
### Claude Code 작업
- **[프로젝트명]**: 수행 작업 요약
  - 세부 작업 1
  - 세부 작업 2

(세션이 없으면 "해당 날짜에 Claude Code 세션 없음" 반환)
```

---

#### SubAgent 3: Meeting Notes Analyzer

**Task 호출 파라미터:**
| 파라미터 | 값 |
|---------|-----|
| description | "미팅 노트 분석" |
| subagent_type | "general-purpose" |
| model | "haiku" |

**프롬프트 (TARGET_DATE 치환 필요):**

```
당신은 미팅 노트 분석 전문가입니다. 코드를 작성하지 말고 분석만 수행하세요.

## 작업
{TARGET_DATE} 날짜의 미팅 노트를 분석하여 주요 내용을 추출합니다.

## 경로
- 미팅 노트 패턴: ~/DocumentsLocal/msbaek_vault/notes/dailies/{TARGET_DATE}-*.md

## 실행 단계
1. Bash로 미팅 노트 파일 찾기:
   ls ~/DocumentsLocal/msbaek_vault/notes/dailies/{TARGET_DATE}-*.md 2>/dev/null

2. 발견된 각 미팅 노트 파일 읽기 (Read 도구 사용)

3. 각 미팅 노트에서 추출:
   - 미팅 주제/제목 (파일명에서 추출)
   - 참석자 (있는 경우)
   - 주요 논의 사항
   - 결정 사항 / Action Items

## 출력 형식 (마크다운으로 반환)
### 미팅
- **[미팅 제목]**
  - 주요 논의: ...
  - 결정 사항: ...
  - Action Items: ...

(미팅 노트가 없으면 "해당 날짜에 미팅 노트 없음" 반환)
```

---

#### SubAgent 4: Learning Extractor

**Task 호출 파라미터:**
| 파라미터 | 값 |
|---------|-----|
| description | "학습 내용 추출" |
| subagent_type | "general-purpose" |
| model | "haiku" |

**프롬프트 (TARGET_DATE, NEXT_DATE 치환 필요):**

```
당신은 학습 내용 추출 전문가입니다. 코드를 작성하지 말고 분석만 수행하세요.

## 작업
{TARGET_DATE} 날짜의 Claude Code 세션에서 학습 관련 내용을 추출합니다.

## 경로
- Claude 세션: ~/.claude/projects/

## 학습 감지 키워드
- 한국어: 배웠, 알게, 처음, 새로운, 이해, 몰랐
- 영어: TIL, learned, discovered, first time
- 질문 패턴: 뭐야, 어떻게, 왜, What, How, Why

## 실행 단계
1. Bash로 해당 날짜 세션 로그 찾기 (macOS 호환):
   find ~/.claude/projects -name "*.jsonl" -type f -exec stat -f "%Sm %N" -t "%Y-%m-%d" {} \; 2>/dev/null | grep "{TARGET_DATE}" | awk '{print $2}'

   **주의**: macOS BSD find는 `-newermt` 옵션이 다르게 동작하므로 `stat` + `grep` 조합 사용

2. 각 세션에서 학습 관련 대화 추출 (Bash로 일부만 읽기):
   head -100 [파일] | jq -r 'select(.type=="user") | .message.content // "" | select(test("뭐야|어떻게|왜|배웠|알게|TIL|learned"; "i"))' 2>/dev/null

3. 학습 내용 분류:
   - 기술/도구: 새 라이브러리, CLI, API
   - 개념: 프로그래밍 개념, 패턴, 원칙
   - 해결방법: 에러 해결, 문제 해결 기법

## 출력 형식 (마크다운으로 반환)
### 학습 기록

#### 기술/도구
- **[도구명]**: 설명 (1줄)

#### 개념
- **[개념명]**: 설명 (1줄)

#### 해결방법
- **[문제]**: 해결 방법 요약

(학습 내용 없으면 "해당 날짜에 특별한 학습 기록 없음" 반환)
```

---

#### SubAgent 5: Things Analyzer

**Task 호출 파라미터:**
| 파라미터 | 값 |
|---------|-----|
| description | "Things 활동 분석" |
| subagent_type | "general-purpose" |
| model | "haiku" |

**프롬프트 (TARGET_DATE 치환 필요):**

```
당신은 Things 3 작업 관리 분석 전문가입니다. 코드를 작성하지 말고 분석만 수행하세요.

## 작업
{TARGET_DATE} 날짜의 Things 활동 내역(완료된 작업, 새로 추가된 작업)을 분석합니다.

## 실행 단계
1. ToolSearch 도구로 "things" 검색하여 Things MCP 도구를 로드합니다.
   - 도구가 발견되지 않으면 "Things MCP 서버 미설정 - 건너뜀" 반환

2. 완료된 작업 수집:
   Things MCP의 get_logbook 도구를 호출합니다 (period="1d").
   반환된 결과에서 각 작업의 제목, 프로젝트명, 영역명을 추출합니다.

3. 새로 추가된 작업 수집:
   Things MCP의 get_recent 도구를 호출합니다 (period="1d").
   반환된 결과에서 각 작업의 제목, 할당된 리스트/프로젝트를 추출합니다.

4. 결과를 아래 형식으로 정리합니다.

## 에러 처리
- Things MCP 도구 로드 실패 → "Things MCP 서버 미설정 - 건너뜀" 반환
- Things 앱 접근 불가 → "Things 데이터 접근 불가" 반환
- 항목 없음 → 해당 섹션에 "없음" 표시

## 출력 형식 (마크다운으로 반환)
### Things 활동

#### 완료된 작업
- **[작업 제목]** (프로젝트명 | 영역명)
- **[작업 제목]** (프로젝트명)

#### 새로 추가된 작업
- **[작업 제목]** → [할당된 리스트/프로젝트]
- **[작업 제목]** → Inbox

(각각 해당 항목이 없으면 "없음" 표시)
(Things MCP 미설정 시 "Things MCP 서버 미설정 - 건너뜀" 반환)
```

---

### Phase 3: 결과 통합 및 Daily Note 반영 (메인 에이전트)

1. **5개 서브 에이전트 결과 수집**
   - 각 Task 도구의 반환값을 수집

2. **Daily Note 확인**
   - Read 도구로 기존 Daily Note 내용 확인
   - 파일이 없으면 기본 템플릿으로 생성

3. **결과 통합하여 Daily Note에 반영**

   Edit 또는 Write 도구를 사용하여 Daily Note에 다음 섹션 추가/업데이트:

```markdown
## 작업 내역

{SubAgent 1 결과 - Vault 문서 작업}

{SubAgent 2 결과 - Claude Code 작업}

{SubAgent 3 결과 - 미팅}

{SubAgent 5 결과 - Things 활동}

{SubAgent 4 결과 - 학습 기록}
```

4. **완료 메시지 출력**
```
{TARGET_DATE} 작업 내역이 Daily Note에 반영되었습니다.
```

---

## 병렬 실행 핵심 원칙

1. **단일 응답에서 5개 Task 동시 호출**: 메인 에이전트는 Phase 2에서 하나의 응답에 5개의 Task 도구 호출을 포함해야 합니다.

2. **haiku 모델 사용**: 비용과 속도 최적화를 위해 서브 에이전트는 haiku 모델을 사용합니다.

3. **결과만 반환**: 각 서브 에이전트는 마크다운 형식의 분석 결과 텍스트만 반환합니다.

4. **메인 에이전트 역할 최소화**:
   - Phase 1: 날짜 계산만 수행
   - Phase 2: Task 호출만 수행 (분석 로직 없음)
   - Phase 3: 결과 조합 및 파일 쓰기만 수행

---

## 컨텍스트 절약 효과

| 구분 | 기존 방식 | 서브 에이전트 방식 |
|------|----------|-------------------|
| 메인 에이전트 컨텍스트 | 모든 파일 내용 로드 | 최종 결과만 수신 |
| 병렬 처리 | 불가 | 5개 작업 동시 실행 |
| 실패 격리 | 전체 실패 | 개별 서브 에이전트만 재시도 |

---

## 에러 처리

- 서브 에이전트 실패 시: 해당 섹션을 "분석 실패"로 표시하고 나머지 결과는 반영
- Daily Note 없음: 기본 템플릿으로 새로 생성
- 파일 없음: "해당 날짜에 [항목] 없음"으로 표시
- Things MCP 미설정: SubAgent 5가 "Things MCP 서버 미설정 - 건너뜀" 반환, 나머지 서브 에이전트 정상 동작

---

## 관련 Skill

- `learning-tracker`: 학습 내용 추출 (SubAgent 4로 사용됨, 독립 실행도 가능)
- `weekly-claude-analytics`: 주간 종합 분석
- `project-time-tracker`: 프로젝트별 시간 추적
- `usage-pattern-analyzer`: 도구 사용 패턴 분석
- `obsidian-vault`: vault 작업 기본 가이드

## 필수 MCP 서버

| MCP 서버 | 용도 | 등록 명령 |
|----------|------|----------|
| Things MCP | SubAgent 5에서 Things 활동 분석 | `claude mcp add-json -s user things '{"command":"uvx","args":["things-mcp"]}'` |

> **참고**: Things MCP 서버가 등록되어 있지 않아도 스킬은 정상 동작합니다. SubAgent 5만 "건너뜀" 처리됩니다.
