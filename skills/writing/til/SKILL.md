---
name: til
description: Write TIL(Today I Learned) documents to ~/dev/TIL/{category}/. "Why" focused storytelling, conclusion first, mermaid diagrams, code examples. Auto-categorize (python, java, spring, nodejs, ai, etc). **Proactively use this skill** when user mentions "TIL", "TIL로 작성", "TIL 문서", "학습 노트 작성" without explicit /til command.
---

# TIL Writer

TIL 저장소에 "왜(Why)" 중심의 스토리텔링 기술 문서를 작성합니다.

## 사용법

```
/til "주제"     # 주제로 바로 문서 작성 시작
/til            # 대화형으로 주제/카테고리 선택
```

## Instructions

### Step 1: 주제 확인

**인자가 있는 경우** (`/til "주제"`):
- 주제를 파악하고 적절한 카테고리 제안
- 사용자 확인 후 작성 시작

**인자가 없는 경우** (`/til`):
- 어떤 주제로 TIL을 작성할지 질문
- 카테고리 선택 (python, java, spring, nodejs, security, computer-science, ai 등)

### Step 2: 문서 구조 작성

**필수 구조:**

```markdown
# 제목 (호기심 유발)

한 줄 설명

## 결론부터 말하면

[핵심 요약 2-3문장]
[다이어그램 또는 Before/After 코드 비교]

## 1. 왜 이런 개념이 필요한가? / 왜 이런 오해가 생겼나?

## 2. 핵심 개념 설명

## 3. 실제 사례 / 코드 예시

## 4. 정리

---

## 출처

- [출처 제목](URL)
```

### Step 3: 핵심 원칙 적용

#### "왜(Why)"를 반드시 설명

```markdown
❌ Bad: "DI는 의존성을 외부에서 주입하는 패턴입니다."
✅ Good: "만약 프레임워크 없이 웹 서버를 만든다면? 우리가 직접 해야 할 일들이 산더미처럼 쌓인다..."
```

#### 스토리텔링 패턴 사용

| 패턴 | 예시 |
|------|------|
| 문제 → 의문 → 해답 | "싱글스레드인데 어떻게 동시에? → libuv가 있기 때문" |
| 만약 ~라면? | "만약 Spring 없이 웹 서버를 만든다면?" |
| 이상한 점 발견 | "근데 이상하다. 싱글스레드라면서 왜 4개가 동시에?" |

#### 연결어로 흐름 만들기

```markdown
✅ Good:
"하지만 여기서 문제가 생겼다."
"왜일까?"
"그렇다면 이건 어떻게 설명할 수 있을까?"
"이제 답이 보인다."
```

#### 문단 단위로 설명 (한 줄씩 끊지 말 것)

```markdown
❌ Bad:
- libuv는 비동기 I/O 라이브러리다.
- Thread Pool을 가진다.

✅ Good:
libuv는 Node.js의 비동기 I/O를 담당하는 C 라이브러리다. Ryan Dahl이 Node.js를 만들 때
직접 개발했다. 왜 필요했을까? JavaScript 자체에는 파일을 읽거나 네트워크 통신을 하는
기능이 없다.
```

### Step 4: 시각화 규칙

#### ASCII 박스 금지 → 테이블 또는 mermaid 사용

```markdown
❌ Bad: ASCII 박스 (한글 정렬 깨짐)
┌─────────────────────────────────────────┐
│  Upstream: 데이터를 보내는 방향          │
└─────────────────────────────────────────┘

✅ Good: 테이블
| 용어 | 의미 |
|------|------|
| Upstream | 데이터를 보내는 방향 |
```

#### mermaid 스타일 규칙

**color를 반드시 명시:**
```markdown
❌ Bad: style Node fill:#e1f5ff          (color 생략)
✅ Good: style Node fill:#1565C0,color:#fff
✅ Good: style Node fill:#E3F2FD,color:#000
```

**줄바꿈은 `<br>` 사용:**
```markdown
❌ Bad: ["첫째 줄\n둘째 줄"]
✅ Good: ["첫째 줄<br>둘째 줄"]
```

### Step 5: 스타일 규칙

#### Bold 처리

**닫는 `**` 다음에 반드시 띄어쓰기:**
```markdown
❌ Bad: **정식 지원(Stable)**된다.
✅ Good: **정식 지원(Stable)** 된다.
```

#### 수식은 LaTeX

```markdown
❌ Bad: S = 1 / ((1 - P) + P/N)
✅ Good: $S = \frac{1}{(1-P) + \frac{P}{N}}$
```

### Step 6: 파일 저장

**파일명 = 제목과 동일:**

| 제목 | 파일명 |
|------|--------|
| `# Python의 f-string` | `Python의-f-string.md` |
| `# Node.js가 싱글스레드라는 미신` | `Node.js가-싱글스레드라는-미신.md` |

**저장 위치:** `/Users/sskim/dev/TIL/{category}/`

### Step 7: Self-Check 실행

문서 작성 완료 후 아래 항목 점검:

- [ ] **"왜"를 설명했는가?**
- [ ] **스토리텔링으로 풀어갔는가?**
- [ ] "결론부터 말하면" 섹션이 있는가?
- [ ] 파일명이 제목과 일치하는가?
- [ ] Bold 닫는 `**` 다음에 띄어쓰기가 있는가?
- [ ] mermaid에서 `\n` 대신 `<br>` 사용했는가?
- [ ] mermaid style에 color가 있는가?
- [ ] 출처를 명시했는가?

## 카테고리 목록

| 카테고리 | 설명 |
|----------|------|
| python | Python 학습 노트 (Java 비교 포함) |
| java | Java 학습 노트 |
| spring | Spring Framework |
| nodejs | Node.js, 비동기 I/O |
| security | 보안 관련 |
| computer-science | CS 기초 개념 |
| ai | AI/ML 관련 |

## 주의사항

- README.md는 GitHub Actions가 자동 생성하므로 **절대 수정하지 말 것**
- `git add`, `git commit`, `git push`는 **사용자가 명시적으로 요청할 때만** 실행
