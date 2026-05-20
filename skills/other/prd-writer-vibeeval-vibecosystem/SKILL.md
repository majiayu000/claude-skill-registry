---
name: prd-writer
description: Product Requirements Document writing - PRD templates, MoSCoW prioritization, user personas, competitive analysis, feature specs, acceptance criteria, risk assessment
---

# PRD Writer

## PRD Template

```markdown
# Product Requirements Document

## Meta
| Field | Value |
|-------|-------|
| Product | [urun adi] |
| Author | [yazar] |
| Version | [v1.0] |
| Status | [Draft / In Review / Approved] |
| Last Updated | [tarih] |
| Stakeholders | [paydas listesi] |

---

## 1. Problem Statement

### The Problem
[Kullanicilarin yasadigi sorunu 2-3 cumle ile acikla]

### Who is Affected
[Etkilenen kullanici segmenti ve buyuklugu]

### Current Solutions
[Mevcut cozumler ve neden yetersiz oldugu]

### Evidence
- [Veri noktasi 1: kullanici arastirmasi, anket, metrik]
- [Veri noktasi 2]
- [Veri noktasi 3]

---

## 2. Goals & Success Metrics

### Goals
| Goal | Description | Metric | Target |
|------|-------------|--------|--------|
| G1 | [birincil hedef] | [olcum] | [hedef deger] |
| G2 | [ikincil hedef] | [olcum] | [hedef deger] |

### Non-Goals (Out of Scope)
- [Bu PRD kapsaminda OLMAYAN seyler]
- [Gelecek iterasyona birakilanlar]

### Success Metrics
| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| [KPI 1] | [mevcut] | [hedef] | [nasil olculecek] |
| [KPI 2] | [mevcut] | [hedef] | [nasil olculecek] |

---

## 3. User Personas

[Asagidaki Persona Template'i kullan]

---

## 4. User Stories

[Epic → Story → Acceptance Criteria hiyerarsisi]

---

## 5. Requirements

### Functional Requirements

| ID | Requirement | Priority | Notes |
|----|------------|----------|-------|
| FR-1 | [gereksinim] | Must | [detay] |
| FR-2 | [gereksinim] | Should | [detay] |

### Non-Functional Requirements

| ID | Category | Requirement | Target |
|----|----------|------------|--------|
| NFR-1 | Performance | Page load time | < 2s |
| NFR-2 | Scalability | Concurrent users | 10,000 |
| NFR-3 | Availability | Uptime SLA | 99.9% |
| NFR-4 | Security | Data encryption | AES-256 |

---

## 6. Design & UX

### User Flows
[Temel kullanici akislari - diyagram veya adim listesi]

### Wireframes
[Link veya embed]

### Edge Cases
| Scenario | Expected Behavior |
|----------|-------------------|
| [durum 1] | [beklenen davranis] |
| [durum 2] | [beklenen davranis] |

---

## 7. Technical Considerations

### Architecture
[Mimari yaklasim ve entegrasyonlar]

### Dependencies
| Dependency | Type | Risk | Mitigation |
|-----------|------|------|------------|
| [dep 1] | External API | Medium | Fallback mechanism |
| [dep 2] | Internal service | Low | Already available |

### Migration / Backward Compatibility
[Mevcut sistemle uyumluluk plani]

---

## 8. Timeline & Milestones

| Phase | Milestone | Duration | Target Date |
|-------|-----------|----------|-------------|
| Phase 1 | MVP | [sure] | [tarih] |
| Phase 2 | Beta | [sure] | [tarih] |
| Phase 3 | GA | [sure] | [tarih] |

---

## 9. Risks & Mitigations

[Asagidaki Risk Assessment framework'unu kullan]

---

## 10. Open Questions

| # | Question | Owner | Status |
|---|----------|-------|--------|
| 1 | [soru] | [kisi] | Open |
| 2 | [soru] | [kisi] | Resolved: [cevap] |
```

## MoSCoW Prioritization

### Framework

| Category | Definition | Guideline |
|----------|-----------|-----------|
| **Must** | Critical, non-negotiable | Launch blocker - no release without it |
| **Should** | Important but not critical | Expected by users, can workaround temporarily |
| **Could** | Nice to have | Enhances experience, not core |
| **Won't** | Out of scope (this iteration) | Documented for future consideration |

### Prioritization Matrix

```markdown
## Feature Prioritization

| Feature | Impact (1-5) | Effort (1-5) | Risk (1-5) | Priority |
|---------|-------------|-------------|-----------|----------|
| [F1] | 5 | 2 | 1 | Must |
| [F2] | 4 | 3 | 2 | Should |
| [F3] | 3 | 4 | 3 | Could |
| [F4] | 2 | 5 | 4 | Won't |

### Scoring Rules
- Impact: Business/user value (5 = critical)
- Effort: Dev time and complexity (5 = very hard)
- Risk: Technical/business uncertainty (5 = very risky)
- Priority = High Impact + Low Effort + Low Risk = Must
```

## User Persona Template

```markdown
## Persona: [Isim]

**Photo:** [placeholder]
**Role:** [is unvani / kullanici tipi]
**Age:** [yas araligi]
**Tech Savvy:** [Low / Medium / High]

### Background
[2-3 cumle: kim, ne yapiyor, nerede calisiyor]

### Goals
1. [birincil hedef - isini kolaylastiran]
2. [ikincil hedef - uzun vadeli]
3. [ucuncul hedef - kisilsel]

### Pain Points
1. [en buyuk sorun - gunluk frustration]
2. [ikinci sorun]
3. [ucuncu sorun]

### Behaviors
- [nasil bilgi arar]
- [hangi araclari kullanir]
- [ne siklikta etkilesin]

### Motivations
- [ne motive eder]
- [ne icin para oder]

### Quote
> "[Persona'nin tipik bir sozu - empati kurmak icin]"

### Scenario
[Tipik bir gun: urunu ne zaman, nasil, neden kullanir]
```

### Persona Anti-Patterns

| Anti-Pattern | Neden Yanlis | Dogru Yol |
|-------------|-------------|-----------|
| Too many personas (5+) | Odak kaybeder | 2-3 primary persona |
| Vague demographics only | Actionable degil | Behavior + motivation ekle |
| No pain points | Cozum odakli olamaz | Gercek kullanici arastirmasindan cikar |
| Fictional without data | Yaniltici | Interview/survey veriyle destekle |

## Competitive Analysis Framework

```markdown
## Competitive Analysis

### Market Landscape

| Competitor | Market Share | Target Segment | Pricing |
|-----------|-------------|---------------|---------|
| [rakip 1] | [%] | [segment] | [fiyat modeli] |
| [rakip 2] | [%] | [segment] | [fiyat modeli] |

### Feature Comparison Matrix

| Feature | Us | Competitor A | Competitor B | Competitor C |
|---------|-----|-------------|-------------|-------------|
| [F1] | [planned] | [var/yok] | [var/yok] | [var/yok] |
| [F2] | [planned] | [var/yok] | [var/yok] | [var/yok] |
| [F3] | [planned] | [var/yok] | [var/yok] | [var/yok] |

### Differentiators
1. [Bizi farkli kilan 1]
2. [Bizi farkli kilan 2]
3. [Bizi farkli kilan 3]

### Competitive Moat
[Neden kopyalanamaz / zorlasilir]

### Gaps & Opportunities
- [Rakiplerin zayif noktasi 1]
- [Rakiplerin zayif noktasi 2]
```

## Feature Specification Format

```markdown
## Feature: [Ozellik Adi]

**ID:** FEAT-001
**Priority:** Must / Should / Could
**Epic:** [bagli epic]
**Owner:** [sorumluluk]

### Description
[1-2 paragraf: ne yapiyor, neden onemli]

### User Stories
- As a [role], I want [feature], so that [benefit]

### Acceptance Criteria
- [ ] Given [precondition], when [action], then [result]
- [ ] Given [precondition], when [action], then [result]

### UI/UX
[Wireframe link veya description]

### Edge Cases
| Case | Behavior |
|------|----------|
| [durum] | [davranis] |

### Technical Notes
[API endpoint, data model, entegrasyon notlari]

### Dependencies
- [Bagimlilik 1]
- [Bagimlilik 2]

### Out of Scope
- [Bu iterasyonda yapilmayacak]
```

## Acceptance Criteria Yazimi

### Given-When-Then (BDD) Format

```gherkin
Feature: User Registration

  Scenario: Successful registration with valid data
    Given the user is on the registration page
    And the user has not previously registered
    When the user enters valid email "user@example.com"
    And the user enters a password meeting complexity requirements
    And the user clicks "Register"
    Then a new account should be created
    And a verification email should be sent
    And the user should see a success message

  Scenario: Registration with existing email
    Given the user is on the registration page
    And an account with "user@example.com" already exists
    When the user enters email "user@example.com"
    And the user clicks "Register"
    Then the user should see "Email already in use" error
    And no duplicate account should be created
```

### Acceptance Criteria Checklist

- [ ] Happy path covered
- [ ] Error states defined
- [ ] Edge cases documented
- [ ] Performance requirements specified
- [ ] Security requirements included
- [ ] Accessibility requirements noted
- [ ] Testable (can be verified objectively)

### Anti-Patterns

| Anti-Pattern | Neden Yanlis | Dogru Yol |
|-------------|-------------|-----------|
| "System should be fast" | Olculemez | "Page loads in < 2 seconds" |
| "Should work correctly" | Belirsiz | Specific expected behavior |
| No error scenarios | Incomplete | Define every failure mode |
| Implementation details | Cozumu kisitlar | Focus on behavior, not how |

## Risk Assessment

### Risk Matrix

```markdown
## Risk Register

| ID | Risk | Likelihood (1-5) | Impact (1-5) | Score | Mitigation | Owner |
|----|------|-------------------|--------------|-------|------------|-------|
| R1 | [risk] | [L] | [I] | [LxI] | [plan] | [kisi] |
| R2 | [risk] | [L] | [I] | [LxI] | [plan] | [kisi] |

### Risk Categories
- **Technical:** Architecture, integration, performance
- **Resource:** Staffing, skills, availability
- **Schedule:** Dependencies, estimation accuracy
- **Business:** Market changes, stakeholder alignment
- **External:** Third-party, regulatory, competitive

### Risk Response Strategies
- **Avoid:** Change plan to eliminate risk
- **Mitigate:** Reduce likelihood or impact
- **Transfer:** Insurance, outsource, vendor SLA
- **Accept:** Monitor and contingency plan
```

## Timeline & Milestone Planning

### Phase Planning Template

```markdown
## Implementation Phases

### Phase 1: Foundation (Week 1-2)
- [ ] Data model design
- [ ] API scaffolding
- [ ] Auth integration
**Deliverable:** Backend API functional
**Exit Criteria:** API tests passing, deployed to staging

### Phase 2: Core Features (Week 3-5)
- [ ] Feature A implementation
- [ ] Feature B implementation
- [ ] Integration testing
**Deliverable:** Core functionality complete
**Exit Criteria:** All Must requirements met, QA passed

### Phase 3: Polish (Week 6-7)
- [ ] UI/UX refinement
- [ ] Performance optimization
- [ ] Should requirements
**Deliverable:** Beta-ready product
**Exit Criteria:** Beta user feedback positive

### Phase 4: Launch (Week 8)
- [ ] Production deployment
- [ ] Monitoring setup
- [ ] Documentation
**Deliverable:** GA release
**Exit Criteria:** All launch criteria met
```

### PRD Review Checklist

- [ ] Problem statement is clear and evidence-based
- [ ] Success metrics are measurable and time-bound
- [ ] User personas based on real research
- [ ] Requirements use MoSCoW prioritization
- [ ] Acceptance criteria are testable
- [ ] Risks identified with mitigation plans
- [ ] Timeline is realistic with buffer
- [ ] Open questions have owners and deadlines
- [ ] All stakeholders have reviewed and agreed
- [ ] Non-goals explicitly stated
