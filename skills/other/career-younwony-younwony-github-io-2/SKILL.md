---
name: write-career
description: 경력기술서(5페이지+) 작성이 필요할 때
---

# 경력기술서 작성

> **작성 원칙 및 STAR+I 가이드**: `/writing-guide` 참조
> **Professional Summary 명세**: `docs/career/PROFESSIONAL_SUMMARY_SPEC.md` 참조

---

## 기술 상세 상한선 규칙

> **원칙**: 모든 것을 쓰지 않는다. 면접에서 말할 여지를 남긴다.

| 항목 | 상한선 | 근거 |
|------|--------|------|
| **Troubleshooting** | 최대 1개 이슈만 상세 | 나머지는 면접에서 |
| **코드 스니펫** | 핵심 설계 판단이 드러나는 1곳만 | 코드는 보조 수단 |
| **Architecture Diagram** | 대표 프로젝트 2~3개만 허용 | 복잡도 제한 |
| **기술 스택 상세** | 버전 제외, 역할만 | `Spring Boot 3.2.1` ❌ → `Spring Boot` ✅ |

---

## 프로젝트 구성 전략 (Tier 1/Tier 2)

### Tier 1: 서사형 프로젝트 (3개, 각 1-2페이지)

> 면접에서 가장 많이 물어볼 대표 프로젝트

- STAR+I 상세 (모든 항목 포함)
- 아키텍처 다이어그램
- 트러블슈팅 상세 (시도-실패-성공)
- 기술 의사결정(WHY) 포함
- Lesson Learned 포함

### Tier 2: 요약형 프로젝트 (2-3개, 각 5-10줄)

> 임팩트는 있으나 깊이 설명할 필요 없는 프로젝트

- 한 줄 요약 + 핵심 성과 2-3개
- 기술 스택만 나열
- WHY 제외 (면접 질문 시 대답)

### 선정 기준

| Tier 1 조건 | Tier 2 조건 |
|-------------|-------------|
| 비즈니스 임팩트 명확 | 기술적 깊이는 있으나 임팩트 약함 |
| 기술 의사결정 복잡 | 단순 구현 위주 |
| 면접 확장 설명 가능 | 추가 질문 가능성 낮음 |
| 조직/팀에 영향 | 개인 업무 효율화 |

---

## Professional Summary 작성

경력기술서 상단의 Professional Summary 작성 시:

```
[문제] → [해결 방법] → [정량 성과] 패턴 적용

❌ "ChatOps 구축으로 운영 반복 업무 40% → 0% 완전 자동화"
✅ "운영팀 인터뷰로 발굴한 컨텍스트 스위칭 병목 → Slack ChatOps 구축으로 반복 업무 40% → 0% 자동화"
```

상세 작성 가이드는 `/writing-guide` 섹션 11 또는 `PROFESSIONAL_SUMMARY_SPEC.md` 참조

---

## 경력기술서 vs 이력서

| 구분 | 경력기술서 (이 스킬) | 이력서 |
|------|---------------------|--------|
| **분량** | 5페이지 이상 | 2-3페이지 |
| **목적** | 상세 역량 검증 | 빠른 스크리닝 |
| **내용** | STAR+I 상세 + 기술적 깊이 | 핵심 성과 요약 |
| **스킬** | `/write-career` | `/create-resume-document` |

---

## 경력기술서 특화 섹션

경력기술서는 이력서와 달리 **기술적 깊이**를 보여주는 섹션이 포함됩니다.

### 1. 아키텍처 다이어그램


> ### Architecture
> 
> ```markdown
> ┌─────────────────────────────────────────────────────────┐
> │                    Data Sources                         │
> ├─────────────┬─────────────┬─────────────┬──────────────┤
> │   TikTok    │  Ensemble   │   EchoTik   │ Web Scraper  │
> │    API      │    API      │    API      │  (Selenium)  │
> └──────┬──────┴──────┬──────┴──────┬──────┴───────┬──────┘
>        └─────────────┴─────────────┴──────────────┘
>                            │
>                            ▼
>              ┌───────────────────────┐
>              │    Collector Service   │
>              │    (Spring Batch)      │
>              └───────────┬───────────┘
>                          │
>       ┌──────────────────┼──────────────────┐
>       ▼                  ▼                  ▼
> ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
> │    MySQL    │───▶│Elasticsearch│    │    Redis    │
> │  (Master)   │    │  (Search)   │    │   (Lock)    │
> └─────────────┘    └─────────────┘    └─────────────┘
> ```

---

### 2. 데이터 플로우

> ### Data Flow
> 
> 1. 수집 (Collection)
>    Schedule Trigger → Lock Acquire → API Request → Response Parse
> 
> 2. 정제 (Processing)
>    Validation → Deduplication → Normalization → Image Download
> 
> 3. 적재 (Storage)
>    MySQL Insert → ES Index Sync → S3 Upload (Images)
> 
> 4. 서빙 (Serving)
>    Search Request → ES Query → Result Format → Response

---

### 3. 트러블슈팅 상세 ⭐

시니어 수준에서 가장 중요한 섹션입니다.

> ### Troubleshooting
> **문제**: 200만 건 검색 시 10초 이상 타임아웃
>
>**발견**:
>- 마케팅팀 피드백: "필터 적용하면 로딩이 안 끝나요"
>- Slow Query Log: `WHERE followers > 10000 AND country = 'US' AND ...` 12초
>
>**분석**:
>1. EXPLAIN 결과: type=ALL (Full Table Scan)
>2. 복합 인덱스 추가 시도 → 4초로 개선되었으나 부족
>3. 원인: 동적 필터 조합이 100가지 이상 → 인덱스 효율 저하
>
>**시도한 방법들**:
>- [실패] Covering Index → 5초로 개선되었으나 여전히 느림
>- [실패] Query Caching → 조건 조합이 많아 Hit율 5% 미만
>- [성공] Elasticsearch 도입 → 역색인 기반 1초 이내 달성
>
>**최종 해결**:
>- Elasticsearch 클러스터 구성 (3 nodes)
>- 실시간 동기화 파이프라인 구축 (MySQL → ES)
>- 검색 API 전환 및 Fallback 로직 구현
>
>**검증**:
>- Load Test: 1000 TPS에서 p99 < 200ms
>- 모니터링: 2주간 안정성 확인
>
>**Lesson Learned** (필수):
>- "초기 설계 시 검색 확장성 고려 부족 → 이후 프로젝트에서 데이터 규모 예측 기반 설계"

#### Lesson Learned 작성 규칙

> **필수**: 실패를 통해 얻은 인사이트 1줄 이상

| 좋은 예 | 나쁜 예 |
|---------|---------|
| "모니터링 없이 배포 → APM 필수 적용 원칙 수립" | "다음엔 잘 하겠다" |
| "초기 설계 시 확장성 고려 부족 → Scale-out 전제 설계" | "ES가 빠르다" |
| "장애 발생 후 Fallback 미비 인지 → Circuit Breaker 패턴 도입" | "테스트를 더 해야 한다" |

---

### 4. 기술 구현 상세 (코드 스니펫)

> **필수**: 코드가 해결한 핵심 문제를 "의도 주석"으로 포함

#### 코드 스니펫 규칙

| 항목 | 규칙 |
|------|------|
| 개수 | 프로젝트당 최대 1개 |
| 길이 | 10줄 이내 |
| 필수 포함 | 의도 주석 (이 코드가 해결한 문제) |
| 금지 | import문, getter/setter, 단순 CRUD |

#### 예시 (의도 주석 포함)

```markdown
### Implementation Details

**Redis Distributed Lock**:
```java
// 문제: 멀티 인스턴스 환경에서 동일 인플루언서 중복 수집
// 해결: TTL 기반 분산락으로 데드락 방지 + 멱등성 확보
String lockKey = "collector:" + platform + ":" + targetId;
long ttl = 60_000L; // 평균 작업시간 25초의 2.5배

RLock lock = redisson.getLock(lockKey);
boolean acquired = lock.tryLock(0, ttl, TimeUnit.MILLISECONDS);
```

**설계 근거**:
- Lock 단위: 인플루언서 ID → 최대 병렬성 확보
- TTL 60초: 작업 실패 시 자동 해제로 데드락 방지
- 재시도 없음: 다음 배치에서 처리 (멱등성)
```

---

### 5. Challenges & Solutions 테이블

```markdown
### Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| API Rate Limit | Token Bucket + Exponential Backoff |
| 멀티 인스턴스 중복 | Redis Distributed Lock |
| 이미지 CDN 만료 | S3 직접 업로드 |
| ES 동기화 지연 | Near Real-time Sync (< 1분) |
```

---

## 실행 단계

### Step 1: 프로젝트 선별

> `/writing-guide` 섹션 5. 파레토 원칙 참조

```
현재 프로젝트 목록 → 상위 20% (5-6개) 선별
```

### Step 2: STAR+I 작성

> `/writing-guide` 섹션 3. STAR+I 각 섹션별 가이드 참조

각 프로젝트마다:
1. 한 줄 요약 (비즈니스 임팩트)
2. Situation (조직 손실 명확히)
3. Task (AS-IS → TO-BE)
4. Action (기술 선택 근거 필수)
5. Result (Before/After 테이블)
6. Impact (조직 레벨 효과)

### Step 3: 기술적 깊이 추가

핵심 프로젝트 2-3개에 대해:
- 아키텍처 다이어그램
- 트러블슈팅 상세 (시도-실패-성공)
- Challenges & Solutions 테이블

### Step 4: 검증

```
프로젝트마다 자문:
"이게 없었다면 조직이 잃는 것은?"
→ 한 줄로 정리 못하면 제거 대상
```

### Step 5: 동기화

```bash
/update-resume
```

---

## 체크리스트

### 기본 품질 (필수)

> `/writing-guide` 섹션 10. 작성 체크리스트 참조

- [ ] 프로젝트 5-6개 선별 완료
- [ ] 각 프로젝트 STAR+I 작성 완료
- [ ] Before/After 테이블 성과 포함
- [ ] 시니어 톤 사용

### 기술적 깊이 (경력기술서 특화)

- [ ] 핵심 프로젝트 아키텍처 다이어그램 포함
- [ ] 트러블슈팅 상세 (시도-실패-성공) 포함
- [ ] Challenges & Solutions 테이블 포함
- [ ] 코드 스니펫 + 설계 근거 포함

---

## 데이터 정합성 (SSOT)

> **상세 가이드**: `/writing-guide` 섹션 18 참조

```
모든 수치와 성과는 my_career_data.md를 원본으로 사용
임의 변경/추정 금지, 변경 시 /update-resume 실행 필수
```

---

## 관련 스킬

- `/writing-guide`: STAR+I 작성 원칙, 시니어 톤, 파레토 기준, SSOT, 업데이트 원칙
- `/create-resume-document`: 이력서 작성 (2-3페이지, 세트 생성)
- `/write-portfolio`: 포트폴리오 작성 (10-15페이지, 기술 백서)
- `/svg-diagram`: SVG 아키텍처 다이어그램 (Before/After)
- `/mermaid-diagram`: Mermaid 다이어그램 (플로우, 시퀀스, ER)
- `/export`: PDF/PPT 내보내기

---

## 문서 세트 구조

> 이력서/경력기술서/포트폴리오는 동일한 원본 데이터(SSOT)를 기반으로 작성

| 문서 | 분량 | 목적 | 대상 |
|------|------|------|------|
| **이력서** | 2-3페이지 | 빠른 스크리닝 | 인사/채용담당 |
| **경력기술서** | 5페이지+ | 상세 역량 검증 | 실무 면접관 |
| **포트폴리오** | 10-15페이지 | 기술 의사결정/리더십 | Tech Lead/CTO |

### 중복 방지 원칙

| 항목 | 이력서 | 경력기술서 | 포트폴리오 |
|------|--------|-----------|-----------|
| 프로젝트 성과 | 1줄 요약 | STAR+I 상세 | Decision Log |
| 기술 선택 이유 | 제외 | 1-2줄 언급 | Why/Why NOT 상세 |
| 아키텍처 | 제외 | 다이어그램 포함 | Before/After 비교 |
| 실패 경험 | 제외 | Lesson Learned | Failure & Revisit |
