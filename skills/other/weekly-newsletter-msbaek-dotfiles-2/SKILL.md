---
name: weekly-newsletter
description: |
  Obsidian vault에서 이번 주(토~금) 작성/수정된 글들을 모아 뉴스레터 생성.
  서브 에이전트 기반 병렬 처리로 메인 컨텍스트 절약.
  기술적, 리더십적으로 외부에 공유할 만한 내용을 선별하여 정리.
  "뉴스레터 만들어줘", "이번 주 글 정리해줘", "weekly digest" 등의 요청 시 자동 적용.
---

# Weekly Newsletter Skill

## 개요

매주 토요일 오전 실행하여 **기술적, 리더십적으로 외부 공유할 만한 내용**을 뉴스레터로 작성하는 skill.

## 핵심 아키텍처

> **서브 에이전트 기반 병렬 처리**로 메인 에이전트의 컨텍스트를 최소화합니다.

```
┌─────────────────────────────────────────────────────────────┐
│                    Main Agent (Orchestrator)                 │
│  - 날짜 범위 계산 (Phase 1)                                    │
│  - 서브 에이전트 병렬 실행 (Phase 2)                            │
│  - 결과 통합 및 뉴스레터 작성 (Phase 3)                         │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │ SubAgent 1  │  │ SubAgent 2  │  │ SubAgent 3  │
    │ Daily Notes │  │ Coffee-time │  │ Weekly Docs │
    │ Analyzer    │  │ Analyzer    │  │ Analyzer    │
    └─────────────┘  └─────────────┘  └─────────────┘
         │               │               │
         └───────────────┼───────────────┘
                         ▼
              ┌─────────────────┐
              │ 뉴스레터 작성    │
              │ (Main Agent)    │
              └─────────────────┘
```

## 인수 (Arguments)

| 인수 | 설명 | 기본값 |
|------|------|--------|
| 주차 | 분석할 주차 (YYYY-WXX 형식) | 금주 |

**사용 예시**:
- `/weekly-newsletter` - 금주 뉴스레터 생성
- `/weekly-newsletter 2026-W03` - 2026년 3주차 뉴스레터 생성

## 주차 정의

> **중요**: 이 스킬에서 주(week)는 **토요일~금요일** 기준입니다.

| 주차 | 시작일 (토) | 종료일 (금) |
|------|------------|------------|
| 2026-W01 | 2025-12-27 | 2026-01-02 |
| 2026-W02 | 2026-01-03 | 2026-01-09 |
| 2026-W03 | 2026-01-10 | 2026-01-16 |

## 실행 시점

- **실행**: 매주 토요일 오전 (또는 필요 시)
- **대상 기간**: 해당 주 토요일 ~ 금요일 (7일간)
- **출력**: `newsletters/YYYY-WXX-newsletter.md`

## 경로 정보

| 항목 | 경로 |
|------|------|
| vault | `~/DocumentsLocal/msbaek_vault/` |
| coffee-time | `~/DocumentsLocal/msbaek_vault/coffee-time` |
| dailies | `~/DocumentsLocal/msbaek_vault/notes/dailies/` |
| newsletters | `~/DocumentsLocal/msbaek_vault/newsletters/` |
| 사용자 프로필 | `~/git/aboutme/AI-PROFILE.md` |

## 입력 소스

| 소스 | 경로 | 담당 서브 에이전트 |
|------|------|------------------|
| Daily Notes | `notes/dailies/` (토~금) | SubAgent 1 |
| coffee-time | `coffee-time/` (해당 주) | SubAgent 2 |
| 주간 작성 문서 | vault 전체 (해당 주 수정) | SubAgent 3 |

---

## 실행 절차

### Phase 1: 초기화 (메인 에이전트 - 순차)

1. **주차 결정 및 날짜 범위 계산**

```bash
# 인수로 주차가 주어진 경우
if [ -n "$1" ]; then
  WEEK_NUM="$1"  # 예: 2026-W03
else
  # 금주 계산 (ISO 주차 기준)
  WEEK_NUM=$(date +%G-W%V)
fi

# ISO 주차의 월요일 구하기
ISO_MONDAY=$(date -j -f "%G-W%V-%u" "${WEEK_NUM}-1" +%Y-%m-%d 2>/dev/null)

# 토요일 = ISO 월요일 - 2일 (주의 시작)
SATURDAY=$(date -j -v-2d -f "%Y-%m-%d" "$ISO_MONDAY" +%Y-%m-%d)

# 금요일 = 토요일 + 6일 (주의 끝)
FRIDAY=$(date -j -v+6d -f "%Y-%m-%d" "$SATURDAY" +%Y-%m-%d)

# 다음날 (검색 종료 경계)
NEXT_DAY=$(date -j -v+1d -f "%Y-%m-%d" "$FRIDAY" +%Y-%m-%d)

echo "주차: $WEEK_NUM"
echo "대상 기간: $SATURDAY (토) ~ $FRIDAY (금)"
```

**예시**:
- `2026-W03` → ISO 월요일: 2026-01-13 → 토요일: 2026-01-11 → 금요일: 2026-01-17
  - **수정**: 실제로는 2026-01-10 (토) ~ 2026-01-16 (금)

> **참고**: macOS `date` 명령어 사용. GNU date와 문법이 다름.

2. **출력 경로 확인**
```bash
OUTPUT_FILE="$HOME/DocumentsLocal/msbaek_vault/newsletters/${WEEK_NUM}-newsletter.md"
```

---

### Phase 2: 서브 에이전트 병렬 실행 ★

> **중요**: 아래 3개의 Task를 **단일 메시지에서 동시에 호출**하여 병렬 실행합니다.
> 각 서브 에이전트는 분석 결과를 **마크다운 형식의 텍스트**로 반환합니다.
> 비용/속도 최적화를 위해 **haiku 모델**을 사용합니다.

---

#### SubAgent 1: Daily Notes Analyzer

**Task 호출 파라미터:**
| 파라미터 | 값 |
|---------|-----|
| description | "Daily Notes 분석" |
| subagent_type | "general-purpose" |
| model | "haiku" |

**프롬프트 (SATURDAY, FRIDAY, NEXT_DAY 치환 필요):**

```
당신은 Daily Notes 분석 전문가입니다. 코드를 작성하지 말고 분석만 수행하세요.

## 작업
{SATURDAY} (토) ~ {FRIDAY} (금) 기간의 Daily Notes를 분석하여 주간 업무 하이라이트를 추출합니다.

## 경로
- Daily Notes: ~/DocumentsLocal/msbaek_vault/notes/dailies/

## 실행 단계
1. Bash로 해당 주 Daily Notes 찾기 (macOS 호환):
   find ~/DocumentsLocal/msbaek_vault/notes/dailies -name "*.md" -type f \
     -exec stat -f "%Sm %N" -t "%Y-%m-%d" {} \; 2>/dev/null | \
     awk -v start="{SATURDAY}" -v end="{FRIDAY}" '$1 >= start && $1 <= end {print $2}'

2. 각 Daily Note 읽기 (Read 도구 사용)

3. 추출할 내용:
   - 주요 업무 하이라이트
   - 기술 학습 내용
   - 해결한 문제들
   - 외부 공유에 적합한 인사이트

## 필터링 기준
**포함**: 기술 트렌드, 학습 방법론, 팀 운영 인사이트
**제외**: 내부 업무 세부사항, 개인 일정, 고객/파트너 정보

## 출력 형식 (마크다운으로 반환)
### 주간 업무 하이라이트
- **[날짜]**: 주요 작업 및 성과
- **[날짜]**: 주요 작업 및 성과

### 기술 학습
- 학습 내용 1
- 학습 내용 2

(Daily Notes가 없으면 "해당 주에 Daily Notes 없음" 반환)
```

---

#### SubAgent 2: Coffee-time Analyzer

**Task 호출 파라미터:**
| 파라미터 | 값 |
|---------|-----|
| description | "Coffee-time 분석" |
| subagent_type | "general-purpose" |
| model | "haiku" |

**프롬프트 (SATURDAY, FRIDAY, NEXT_DAY 치환 필요):**

```
당신은 Coffee-time 노트 분석 전문가입니다. 코드를 작성하지 말고 분석만 수행하세요.

## 작업
{SATURDAY} (토) ~ {FRIDAY} (금) 기간의 coffee-time 노트를 분석하여 핵심 인사이트를 추출합니다.

## 경로
- Coffee-time: ~/DocumentsLocal/msbaek_vault/coffee-time/

## 파일명 패턴
- `YYYY. M. DD. 커피타임.md`
- 예: `2026. 1. 14. 커피타임.md`

## 실행 단계
1. Bash로 해당 주 coffee-time 노트 찾기 (macOS 호환):
   find ~/DocumentsLocal/msbaek_vault/coffee-time -name "*.md" -type f \
     -exec stat -f "%Sm %N" -t "%Y-%m-%d" {} \; 2>/dev/null | \
     awk -v start="{SATURDAY}" -v end="{FRIDAY}" '$1 >= start && $1 <= end {print $2}'

2. 각 커피타임 노트 읽기 (Read 도구 사용)

3. 추출할 내용:
   - 기술 인사이트 (트렌드, 도구, 방법론)
   - 리더십/팀 운영 토론
   - 업계 동향 분석
   - 핵심 인용문/교훈

## 출력 형식 (마크다운으로 반환)
### 커피타임 하이라이트

#### [날짜] - [주제]
- 핵심 논의: ...
- 주요 인사이트: ...
- 교훈: ...

#### [날짜] - [주제] (있는 경우)
- 핵심 논의: ...

(커피타임 노트가 없으면 "해당 주에 커피타임 노트 없음" 반환)
```

---

#### SubAgent 3: Weekly Documents Analyzer

**Task 호출 파라미터:**
| 파라미터 | 값 |
|---------|-----|
| description | "주간 문서 분석" |
| subagent_type | "general-purpose" |
| model | "haiku" |

**프롬프트 (SATURDAY, FRIDAY, NEXT_DAY 치환 필요):**

```
당신은 Obsidian Vault 문서 분석 전문가입니다. 코드를 작성하지 말고 분석만 수행하세요.

## 작업
{SATURDAY} (토) ~ {FRIDAY} (금) 기간에 생성/수정된 기술 문서들을 분석하여 외부 공유 적합 내용을 추출합니다.

## 경로
- Vault: ~/DocumentsLocal/msbaek_vault/
- 분석 대상: 001-INBOX/, 003-RESOURCES/, 000-SLIPBOX/

## 실행 단계
1. Bash로 해당 주에 수정된 .md 파일 찾기 (macOS 호환):
   find ~/DocumentsLocal/msbaek_vault \( -path "*/001-INBOX/*" -o -path "*/003-RESOURCES/*" -o -path "*/000-SLIPBOX/*" \) \
     -name "*.md" -type f -exec stat -f "%Sm %N" -t "%Y-%m-%d" {} \; 2>/dev/null | \
     awk -v start="{SATURDAY}" -v end="{FRIDAY}" '$1 >= start && $1 <= end {print $2}'

2. 발견된 파일 중 중요 문서 읽기 (Read 도구 사용, 최대 10개)

3. 분류 기준:
   - 기술 트렌드 (AI, 아키텍처, 개발 방법론)
   - 리더십/조직 인사이트
   - 학습 방법론
   - 업계 동향

## 필터링 기준
**포함**: SDD, AI 코딩 도구, 새로운 아키텍처 패턴, 효과적인 매니저 특징, AI 활용 학습법
**제외**: 내부 업무 세부사항, 회사 고유 프로세스, 개인 일정, 고객/파트너 정보

## 출력 형식 (마크다운으로 반환)
### 기술 트렌드
- **[문서명]**: 핵심 내용 요약 (2-3줄)

### 리더십 & 조직 인사이트
- **[문서명]**: 핵심 내용 요약

### 학습 방법론
- **[문서명]**: 핵심 내용 요약

(수정된 문서가 없으면 "해당 주에 수정된 기술 문서 없음" 반환)
```

---

### Phase 3: 결과 통합 및 뉴스레터 작성 (메인 에이전트)

1. **3개 서브 에이전트 결과 수집**
   - 각 Task 도구의 반환값을 수집

2. **사용자 프로필 읽기**
   - Read 도구로 `~/git/aboutme/AI-PROFILE.md` 확인
   - 톤앤매너 조정에 활용

3. **뉴스레터 작성**

   Write 도구를 사용하여 `newsletters/{WEEK_NUM}-newsletter.md` 생성:

```markdown
---
id: {WEEK_NUM}-newsletter
aliases:
  - {YEAR}년 {WEEK}주차 뉴스레터
tags:
  - newsletter
  - weekly-digest
created_at: {TODAY}
period: {SATURDAY} ~ {FRIDAY}
---

# Weekly Digest - {YEAR}년 {WEEK}주차

> "핵심 인용문" - 출처

**기간**: {SATURDAY_DISPLAY} (토) ~ {FRIDAY_DISPLAY} (금)

---

## 이번 주 커피타임 하이라이트

{SubAgent 2 결과 - 커피타임 분석}

---

## 기술 트렌드

{SubAgent 3 결과 - 기술 트렌드 부분}

---

## 리더십 & 조직 인사이트

{SubAgent 3 결과 - 리더십 부분}
{SubAgent 2 결과 - 리더십 관련 내용}

---

## 주간 업무 하이라이트

{SubAgent 1 결과}

---

## 이번 주 핵심 교훈

1. 교훈 1 (위 내용에서 추출)
2. 교훈 2
3. 교훈 3

---

## 다음 주 포커스

- [ ] 포커스 영역 1
- [ ] 포커스 영역 2

---

## Related Notes

- [[관련 노트 1]]
- [[관련 노트 2]]
```

4. **완료 메시지 출력**
```
{WEEK_NUM} 뉴스레터가 생성되었습니다: newsletters/{WEEK_NUM}-newsletter.md
```

---

## 병렬 실행 핵심 원칙

1. **단일 응답에서 3개 Task 동시 호출**: 메인 에이전트는 Phase 2에서 하나의 응답에 3개의 Task 도구 호출을 포함해야 합니다.

2. **haiku 모델 사용**: 비용과 속도 최적화를 위해 서브 에이전트는 haiku 모델을 사용합니다.

3. **결과만 반환**: 각 서브 에이전트는 마크다운 형식의 분석 결과 텍스트만 반환합니다.

4. **메인 에이전트 역할 최소화**:
   - Phase 1: 날짜 계산만 수행
   - Phase 2: Task 호출만 수행 (분석 로직 없음)
   - Phase 3: 결과 조합 및 뉴스레터 작성만 수행

---

## 컨텍스트 절약 효과

| 구분 | 기존 방식 | 서브 에이전트 방식 |
|------|----------|-------------------|
| 메인 에이전트 컨텍스트 | 모든 파일 내용 로드 | 최종 결과만 수신 |
| 병렬 처리 | 불가 | 3개 작업 동시 실행 |
| 실패 격리 | 전체 실패 | 개별 서브 에이전트만 재시도 |

---

## 뉴스레터 톤앤매너

1. **CTO 관점의 Weekly Digest**
2. **점진적 개선(Incremental) 관점** 반영
3. **TDD/Clean Code 철학**과 연결
4. **실용적 인사이트** 중심
5. **핵심 인용문**으로 섹션 강조
6. **다음 주 포커스** 섹션으로 연속성 제공

---

## 외부 공유 적합성 필터링

**포함 (외부 공유 적합):**
| 분류 | 예시 |
|------|------|
| 기술 트렌드 | SDD, AI 코딩 도구, 새로운 아키텍처 패턴 |
| 리더십 인사이트 | 효과적인 매니저 특징, 팀 운영 노하우 |
| 학습 방법론 | 조각 지식 전략, AI 활용 학습법 |
| 업계 동향 분석 | 하이프 사이클, 재본스 역설 |

**제외:**
| 분류 | 이유 |
|------|------|
| 내부 업무 세부사항 | 민감한 비즈니스 정보 |
| 회사 고유 프로세스 | 내부 전용 |
| 개인 일정/TODO | 공유 부적합 |
| 고객/파트너 정보 | 기밀 사항 |

---

## 에러 처리

- 서브 에이전트 실패 시: 해당 섹션을 "분석 실패"로 표시하고 나머지 결과는 반영
- newsletters 폴더 없음: 자동 생성
- 파일 없음: "해당 주에 [항목] 없음"으로 표시

---

## 검증 체크리스트

- [ ] 해당 주(토~금) 날짜 범위 정확한지
- [ ] coffee-time 해당 주 노트 모두 포함 여부
- [ ] dailies 내용 반영 여부
- [ ] 외부 공유 부적합 내용 제외 여부
- [ ] 마크다운 포맷 정상 렌더링
- [ ] Related Notes 링크 정확성
- [ ] 주차 번호(Week Number) 정확한지

---

## 의존 관계

```
daily-work-logger (매일)
        ↓
    dailies/YYYY-MM-DD.md
        ↓
weekly-newsletter (토요일) ← 이 skill
        ↓
    newsletters/YYYY-WXX-newsletter.md
```

---

## 관련 Skill

- `daily-work-logger`: 매일 업무 내역 정리 (이 skill의 입력 소스)
- `obsidian-vault`: vault 작업 기본 가이드
