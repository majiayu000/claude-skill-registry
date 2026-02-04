---
name: obsidian-flashcard
description: |
  Obsidian Spaced Repetition 플러그인용 플래시카드 생성.
  세션 학습 내용 또는 특정 주제를 Q&A/Cloze 형식의 플래시카드로 변환.
  "플래시카드", "flashcard", "암기 카드", "복습 카드" 등의 요청 시 자동 적용.
---

# Obsidian Flashcard Writer

**Obsidian Spaced Repetition 플러그인용 플래시카드 생성 가이드**

---

## 기본 설정

| 항목 | 값 |
|------|-----|
| Vault 경로 | `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Note` |
| 저장 위치 | `10.Flashcards` |
| 파일명 규칙 | `FC-{주제}.md` (예: `FC-Spring-Security.md`) |
| 덱 태그 | `#flashcards/{category}` |

---

## 사용법

```bash
/obsidian-flashcard                       # 현재 세션에서 학습 내용 추출 → 플래시카드
/obsidian-flashcard "Spring Security"     # 특정 주제로 플래시카드 생성
/obsidian-flashcard --from-note "Spring"  # 기존 Obsidian 노트 검색 → 플래시카드 변환
```

---

## 기존 노트에서 변환 (--from-note)

Obsidian Vault에서 기존 노트를 검색하고 플래시카드로 변환합니다.

### 프로세스

```
Step 1: 노트 검색
  └─ Vault 경로에서 키워드로 노트 검색
  └─ 파일명 또는 내용에서 매칭

Step 2: 노트 선택
  └─ 검색 결과 목록 표시
  └─ 사용자가 변환할 노트 선택

Step 3: 내용 분석
  └─ 노트 구조 파악 (헤딩, 코드블록, 리스트)
  └─ 핵심 개념 추출

Step 4: 플래시카드 변환
  └─ 헤딩 → 섹션 구분
  └─ 정의/설명 → Q&A 카드
  └─ 순서/흐름 → Cloze 카드
  └─ 코드 예시 → 코드 카드

Step 5: 저장
  └─ FC-{원본노트명}.md 로 저장
  └─ 원본 노트 링크 추가
```

### 검색 경로

```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Note/
├── 00.Inbox/
├── 09.TIL/          ← TIL 노트
├── 01.Projects/
└── ...
```

### 변환 규칙

| 원본 노트 구조 | 플래시카드 변환 |
|---------------|----------------|
| `## 헤딩` | 섹션 구분자 |
| `**용어**: 정의` | `용어:::정의` |
| `- 항목1, 항목2` | Multi-line Q&A |
| 코드 블록 (전/후 비교) | `Before:::After` |
| 순서 설명 | Cloze `==키워드==` |
| `> 인용문` | 핵심 개념 추출 |

### 예시

**명령:**
```bash
/obsidian-flashcard --from-note "Spring Framework 7"
```

**검색 결과:**
```
🔍 "Spring Framework 7" 검색 결과:

1. 09.TIL/Spring-Framework-7.0.md
2. 09.TIL/Spring-Framework-7-API-Versioning.md
3. 09.TIL/Spring-Framework-7-HTTP-Service-Client.md

어떤 노트를 플래시카드로 변환할까요? (번호 또는 'all')
```

**변환 후:**
```markdown
---
title: "Spring Framework 7.0 플래시카드"
created: 2026-02-02
tags:
  - flashcard
source: "[[Spring-Framework-7.0]]"
---

#flashcards/spring

## 시스템 요구사항

Spring Framework 7.0의 최소 Java 버전은?::JDK 17 (권장: JDK 25 LTS)

...

---

> 생성: Claude Code /obsidian-flashcard --from-note
> 원본: [[Spring-Framework-7.0]]
```

### 변환 품질 향상 팁

1. **원본 노트가 잘 구조화되어 있을수록** 변환 품질이 높음
2. **결론부터/핵심 요약** 섹션이 있으면 좋은 카드 생성
3. **Before/After 코드 비교**가 있으면 양방향 카드로 변환
4. **Why 설명**이 있으면 Why 질문 카드 생성

---

## 카드 문법 (Spaced Repetition 플러그인)

### 1. Single-line Q&A

**기본 (단방향):**
```markdown
질문::답변
```

**양방향 (카드 2장 생성):**
```markdown
용어:::정의
```

### 2. Multi-line Q&A

**기본:**
```markdown
Spring의 IoC 컨테이너가 하는 일은?
?
- 객체 생성 및 관리
- 의존성 주입 (DI)
- 생명주기 관리
```

**양방향:**
```markdown
Authentication
??
인증 - 사용자가 누구인지 확인
```

### 3. Cloze (빈칸 채우기)

```markdown
Spring Security의 기본 필터 순서는 ==SecurityContextPersistenceFilter== → ==UsernamePasswordAuthenticationFilter== → ==ExceptionTranslationFilter==이다.
```

---

## 카드 작성 원칙

### 핵심 원칙: 시니어 개발자 & 면접 관점

```
⚠️ 카드 수 제한: 한 주제당 5-10개 (절대 20개 넘지 말 것)
⚠️ "왜?"를 설명할 수 있어야 진짜 아는 것
⚠️ 면접에서 "그래서 왜 그런가요?"에 답할 수 있는 깊이
```

### 카드로 만들어야 할 것

| 유형 | 기준 | 예시 |
|------|------|------|
| **Why 질문** | 원리/이유를 묻는 것 | `왜 @Transactional이 private에서 안 되나?::프록시 기반 AOP라서. Spring은 CGLIB/JDK 동적 프록시로 트랜잭션을 가로채는데, private은 상속/구현이 불가능` |
| **Trade-off** | 장단점, 선택의 이유 | `왜 Spring 7.0에서 Undertow를 버렸나?::Undertow가 Servlet 6.1을 지원 안 해서. Red Hat이 Jakarta EE 11 대응을 안 함` |
| **실무 판단** | 시니어가 알아야 할 것 | `언제 CompletableFuture 대신 Virtual Thread를 쓰나?::I/O 바운드 작업이 많고, 콜백 지옥을 피하고 싶을 때. CPU 바운드는 여전히 ForkJoinPool이 나음` |
| **아키텍처 결정** | 설계 시 고려사항 | `Jackson 3.x로 마이그레이션 시 주의점은?::tools.jackson 패키지지만 Annotation은 com.fasterxml.jackson 유지. 혼용 가능하나 Spring 7.1에서 2.x 완전 제거 예정` |

### 카드로 만들지 말 것

```markdown
❌ 단순 사실: "Spring 7.0의 Tomcat 버전은?" → 검색 1초
❌ 나열형: "Breaking Changes 5가지는?" → 문서 보면 됨
❌ What 질문: "RestTestClient란?" → 정의만 알면 의미 없음
❌ 코드 암기: "@Retryable 어노테이션 파라미터는?" → IDE가 해줌
```

### 면접 레벨 카드 예시

```markdown
❌ 주니어 레벨 (피하기):
Q: Spring 7.0에서 javax가 어떻게 바뀌었나?
A: jakarta로 변경

✅ 시니어 레벨 (지향):
Q: 왜 Spring이 javax를 완전히 버렸나?
A: Jakarta EE가 Eclipse 재단으로 이관되며 javax 상표권 문제 발생.
   Oracle이 javax 패키지명 사용을 허락 안 해서 jakarta로 전면 전환.
   Spring 6.x까지는 호환성 레이어 제공했으나, 7.0에서 완전 제거로
   의존성 충돌 방지 및 유지보수 비용 절감.

❌ 주니어 레벨 (피하기):
Q: @Retryable 어떻게 쓰나?
A: @EnableRetry + @Retryable 붙이면 됨

✅ 시니어 레벨 (지향):
Q: Spring 7.0에서 Retry가 core에 통합된 이유는?
A: Resilience4j, Spring Retry 등 외부 의존성 난립 문제 해결.
   MSA 환경에서 회복력이 필수가 되며 프레임워크 기본 기능으로 승격.
   @ConcurrencyLimit도 추가해 rate limiting까지 통합 제공.
```

### 답변 작성 가이드

```markdown
좋은 답변의 구조:
1. 핵심 답 (한 줄)
2. 이유/원리 (왜?)
3. 실무 맥락 (언제/어떻게 적용?)

예시:
Q: 왜 ListenableFuture가 제거됐나?
A: CompletableFuture가 표준이 되어서.
   Java 8에서 CompletableFuture가 도입되며 ListenableFuture의 존재 이유 상실.
   thenApply, thenCompose 등 함수형 체이닝이 더 강력하고,
   Virtual Thread와도 자연스럽게 통합됨.
```

---

## 카테고리 (덱 태그)

| 카테고리 | 태그 | 키워드 |
|----------|------|--------|
| Python | `#flashcards/python` | Python, pip, pytest, FastAPI |
| Java | `#flashcards/java` | Java, JVM, JUnit |
| Spring | `#flashcards/spring` | Spring Boot, Security, JPA |
| Database | `#flashcards/database` | SQL, Redis, PostgreSQL |
| DevOps | `#flashcards/devops` | Docker, K8s, CI/CD |
| CS | `#flashcards/cs` | 알고리즘, 자료구조, OS |
| AI | `#flashcards/ai` | LLM, RAG, LangChain |

---

## 출력 템플릿

```markdown
---
title: "{주제} 플래시카드"
created: {YYYY-MM-DD}
tags:
  - flashcard
---

#flashcards/{category}

## {섹션 1}

질문1::답변1

용어1:::정의1

여러 줄 질문?
?
여러 줄 답변

## {섹션 2}

Cloze 형식: ==핵심 키워드==를 가린다.

---

> 생성: Claude Code /obsidian-flashcard
```

---

## 작성 프로세스

### Step 1: 주제 파악

사용자가 제공한 주제 또는 세션 대화에서 학습 내용 추출:
- 새로 배운 개념
- 질문했던 내용
- 에러 해결 과정

### Step 2: 카드 유형 결정

| 내용 유형 | 권장 카드 형식 |
|-----------|---------------|
| 용어/정의 | `:::` (양방향) |
| 개념 설명 | `?` (multi-line) |
| 순서/흐름 | Cloze `==...==` |
| Why 질문 | `::` (단방향) |

### Step 3: 카드 작성

- **5-10개**로 제한 (핵심만!)
- 섹션별로 `## 헤딩` 사용 (컨텍스트 제공)
- 검색하면 바로 나오는 정보는 제외
- Why/How 질문 우선

### Step 4: 저장

- 파일명: `FC-{주제}.md`
- 위치: `10.Flashcards`
- 덱 태그 확인

---

## 예시: Spring Security 플래시카드

```markdown
---
title: "Spring Security 플래시카드"
created: 2024-01-15
tags:
  - flashcard
---

#flashcards/spring

## 기본 개념

Authentication:::인증 - 사용자가 누구인지 확인

Authorization:::인가 - 사용자가 무엇을 할 수 있는지 확인

Spring Security의 핵심 구성요소 3가지는?
?
- SecurityFilterChain
- AuthenticationManager
- UserDetailsService

## FilterChain

Spring Security 필터 체인에서 ==SecurityContextPersistenceFilter==가 가장 먼저 실행되어 ==SecurityContext==를 로드한다.

@Transactional이 private 메서드에서 작동하지 않는 이유는?::Spring AOP가 프록시 기반이라 private 메서드를 가로챌 수 없음

## CSRF

CSRF 공격이란?::사용자의 인증된 세션을 악용해 의도하지 않은 요청을 보내는 공격

CSRF 방어 방법은?
?
- CSRF 토큰 사용
- SameSite 쿠키 속성
- Referer 헤더 검증

---

> 생성: Claude Code /obsidian-flashcard
```

---

## learning-tracker 연동

`/learning-tracker` 실행 후 플래시카드 옵션 제공:

```
📚 학습 내용 추출 완료!

**감지된 학습 주제:**
1. Spring Security FilterChain
2. CSRF 방어 방법

**다음 작업:**
- [TIL 문서 작성] → /til
- [플래시카드 생성] → /obsidian-flashcard
```

---

## 체크리스트

### 일반 플래시카드
```markdown
□ 카드 수 5-10개 이내 (핵심만!)
□ 검색하면 나오는 정보는 제외했는가?
□ Why/How 질문 위주인가?
□ 덱 태그 (#flashcards/{category}) 포함
□ 파일명 FC-{주제}.md 형식
□ 10.Flashcards에 저장
```

### --from-note 변환
```markdown
□ 원본 노트에서 핵심 5-10개만 추출
□ 단순 버전/숫자 정보는 제외
□ source 필드에 원본 노트 링크 추가
□ 실무에서 바로 써먹을 지식만 포함
□ 푸터에 원본 노트 링크 명시
```
