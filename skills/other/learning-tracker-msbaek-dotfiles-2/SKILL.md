---
name: learning-tracker
description: |
  세션에서 새로운 기술/라이브러리/개념 학습 내용을 추출하여 TIL(Today I Learned) 문서로 정리.
  독립 실행 또는 daily-work-logger의 서브 에이전트로 호출 가능.
  "학습 정리", "TIL", "오늘 배운 것", "learning" 등의 요청 시 자동 적용.
---

# Learning Tracker Skill

## 개요

Claude Code 세션 로그에서 **새로운 기술, 라이브러리, 개념**에 대한 학습 내용을 추출하여 TIL(Today I Learned) 형식으로 정리하는 skill.

## 사용 방식

### 독립 실행
```bash
/learning-tracker           # 어제 날짜 학습 내용 추출
/learning-tracker 2026-01-15  # 특정 날짜 학습 내용 추출
```

### daily-work-logger 연동
- `daily-work-logger` 실행 시 SubAgent 4로 자동 호출됨
- 결과가 Daily Note의 "학습 기록" 섹션에 반영됨

## 경로 정보

| 항목 | 경로 |
|------|------|
| Claude 세션 | `~/.claude/projects/` |
| history.jsonl | `~/.claude/history.jsonl` |
| transcripts | `~/.claude/transcripts/` |
| TIL 출력 | `~/DocumentsLocal/msbaek_vault/notes/dailies/` (Daily Note 내) |

## 학습 감지 패턴

### 한국어 키워드
| 패턴 | 설명 |
|------|------|
| "배웠", "배워" | 학습 완료 표현 |
| "알게 됐", "알았" | 새로운 이해 |
| "처음", "처음으로" | 최초 경험 |
| "새로운", "새롭게" | 새로운 지식 |
| "이해했", "이해됐" | 개념 이해 |
| "몰랐던", "몰랐는데" | 기존 무지 인정 |

### 영어 키워드
| 패턴 | 설명 |
|------|------|
| "TIL", "Today I learned" | 명시적 학습 표현 |
| "learned", "discovered" | 학습/발견 |
| "didn't know", "now I know" | 새로운 지식 |
| "first time" | 최초 경험 |

### 질문 패턴 (사용자 질문 → 학습 기회)
| 패턴 | 설명 |
|------|------|
| "이게 뭐야?", "이게 뭔가요?" | 개념 질문 |
| "어떻게 해?", "어떻게 하나요?" | 방법 질문 |
| "왜?", "왜 그런가요?" | 이유 질문 |
| "차이가 뭐야?" | 비교 질문 |
| "What is", "How to", "Why" | 영어 질문 |

### 기술 학습 지표
| 지표 | 설명 |
|------|------|
| 새 라이브러리 import | 처음 사용하는 패키지 |
| 새 CLI 도구 사용 | 처음 사용하는 명령어 |
| API 문서 참조 | WebFetch로 공식 문서 조회 |
| 에러 해결 후 설명 | 문제 해결 과정에서 학습 |

---

## 실행 절차

### Step 1: 날짜 결정

```bash
TARGET_DATE="${1:-$(date -v-1d +%Y-%m-%d)}"
NEXT_DATE=$(date -j -f "%Y-%m-%d" -v+1d "$TARGET_DATE" +%Y-%m-%d)
echo "대상 날짜: $TARGET_DATE"
```

### Step 2: 해당 날짜 세션 로그 찾기

```bash
find ~/.claude/projects -name "*.jsonl" \
  -newermt "$TARGET_DATE 00:00:00" \
  ! -newermt "$NEXT_DATE 00:00:00" 2>/dev/null
```

### Step 3: 세션 로그에서 학습 내용 추출

각 세션 로그에서 다음을 분석:

```bash
# 사용자 질문 추출 (학습 기회)
cat session.jsonl | jq -r '
  select(.type == "user") |
  .message.content // "" |
  select(test("뭐야|어떻게|왜|차이|What|How|Why"; "i"))
' | head -20

# 학습 키워드 포함 대화 추출
cat session.jsonl | jq -r '
  select(.type == "user" or .type == "assistant") |
  .message.content // "" |
  select(test("배웠|알게|처음|TIL|learned|discovered"; "i"))
'
```

### Step 4: 학습 내용 분류

| 카테고리 | 설명 | 예시 |
|---------|------|------|
| 기술/도구 | 새 라이브러리, 프레임워크, CLI | "jq 사용법 배움" |
| 개념 | 프로그래밍 개념, 패턴 | "SOLID 원칙 이해" |
| 해결방법 | 에러 해결, 문제 해결 기법 | "TypeScript 타입 오류 해결" |
| 팁/트릭 | 효율적인 방법, 단축키 | "vim macro 사용법" |

### Step 5: 출력 형식

#### Daily Note 섹션용 (daily-work-logger 연동 시)

```markdown
### 학습 기록

#### 기술/도구
- **jq**: JSON 파싱 CLI 도구 사용법
  - `jq -r '.field'` 형식으로 필드 추출
  - `select()` 함수로 필터링

#### 개념
- **JSONL 형식**: 줄 단위 JSON 스트리밍 형식
  - 대용량 로그 처리에 적합
  - 각 줄이 독립적인 JSON 객체
```

#### 독립 실행 시 (TIL 요약)

```markdown
## TIL - {TARGET_DATE}

> {TARGET_DATE}에 새로 배운 내용들

### 오늘 배운 것

1. **jq CLI 도구**
   - JSON 파싱 및 필터링 도구
   - 세션 로그 분석에 활용

2. **JSONL 형식**
   - 줄 단위 JSON 스트리밍
   - 로그 처리에 적합한 형식
```

---

## daily-work-logger 서브 에이전트로 사용 시

### Task 호출 파라미터

| 파라미터 | 값 |
|---------|-----|
| description | "학습 내용 추출" |
| subagent_type | "general-purpose" |
| model | "haiku" |

### 프롬프트 템플릿 (TARGET_DATE, NEXT_DATE 치환)

```
당신은 학습 내용 추출 전문가입니다. 코드를 작성하지 말고 분석만 수행하세요.

## 작업
{TARGET_DATE} 날짜의 Claude Code 세션에서 학습 관련 내용을 추출합니다.

## 경로
- Claude 세션: ~/.claude/projects/

## 학습 감지 키워드
- 한국어: 배웠, 알게, 처음, 새로운, 이해, 몰랐
- 영어: TIL, learned, discovered, first time

## 실행 단계
1. Bash로 해당 날짜 세션 로그 찾기:
   find ~/.claude/projects -name "*.jsonl" -newermt "{TARGET_DATE} 00:00:00" ! -newermt "{NEXT_DATE} 00:00:00" 2>/dev/null

2. 각 세션에서 학습 관련 대화 추출:
   - 사용자 질문 (뭐야, 어떻게, 왜, What, How, Why)
   - 학습 표현 (배웠, 알게, TIL, learned)
   - Claude의 설명/교육 내용

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

## 에러 처리

- 세션 없음: "해당 날짜에 Claude Code 세션 없음" 반환
- 학습 내용 없음: "특별한 학습 기록 없음" 반환
- 파싱 오류: 해당 세션 건너뛰고 계속 진행

---

## 관련 Skill

- `daily-work-logger`: 일일 작업 로그 (이 skill의 호출자)
- `weekly-claude-analytics`: 주간 사용 분석
- `obsidian-vault`: vault 작업 기본 가이드
