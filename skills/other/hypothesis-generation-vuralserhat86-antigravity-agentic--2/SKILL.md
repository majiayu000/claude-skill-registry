---
name: hypothesis_generation
router_kit: FullStackKit
description: Bilimsel hipotez oluşturma, deney tasarımı ve test metodolojisi rehberi.
metadata:
  skillport:
    category: research
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, hypothesis generation, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]
---

# 🔬 Hypothesis Generation

> Bilimsel hipotez oluşturma ve test metodolojisi rehberi.

---

## 📋 Hipotez Yapısı

### Format
```
IF [independent variable/action]
THEN [dependent variable/outcome]
BECAUSE [mechanism/reasoning]
```

### Örnek
```
IF we reduce checkout steps from 5 to 3
THEN conversion rate will increase by 15%
BECAUSE fewer steps reduce friction and drop-off
```

---

## 🎯 Hipotez Kriterleri

| Kriter | Açıklama |
|--------|----------|
| **Specific** | Net ve belirsizlik yok |
| **Measurable** | Ölçülebilir outcome |
| **Testable** | Test edilebilir |
| **Falsifiable** | Yanlışlanabilir |
| **Relevant** | İş hedefine uygun |

---

## 🔧 Hipotez Türleri

### A/B Test Hipotezi
```markdown
**Hypothesis:** Changing CTA button from blue to green 
will increase click rate by 10%

**Metric:** CTA Click Rate
**Baseline:** 2.5%
**Target:** 2.75%
**Sample Size:** 10,000 users
**Duration:** 2 weeks
```

### Product Hipotezi
```markdown
**Problem:** Users abandon during onboarding
**Hypothesis:** Adding progress indicator will reduce 
abandonment by 20%
**Success Metric:** Onboarding completion rate
```

---

## 📊 Experiment Design

### Test Plan
```markdown
## Experiment: [Name]

### Hypothesis
[IF-THEN-BECAUSE statement]

### Variables
- Independent: [What we change]
- Dependent: [What we measure]
- Control: [What stays same]

### Metrics
- Primary: [Main KPI]
- Secondary: [Supporting metrics]
- Guardrail: [Safety metrics]

### Design
- Type: A/B / Multivariate
- Split: 50/50
- Duration: [X] weeks

### Analysis Plan
- Statistical test: [t-test, chi-square, etc.]
- Confidence level: 95%
- MDE: [Minimum detectable effect]
```

---

## 📝 Prioritization (ICE)

| Hypothesis | Impact | Confidence | Ease | Score |
|------------|--------|------------|------|-------|
| H1 | 8 | 7 | 6 | 7.0 |
| H2 | 9 | 5 | 4 | 6.0 |
| H3 | 6 | 8 | 9 | 7.7 |

```
ICE Score = (Impact + Confidence + Ease) / 3
```

---

*Hypothesis Generation v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Stanford d.school Design Thinking](https://dschool.stanford.edu/resources)

### Aşama 1: Observation
- [ ] **Data**: Analitik verisi veya kullanıcı görüşmesinden bir "Insight" yakala.
- [ ] **Problem**: Gözlemi net bir problem cümlesine dönüştür.

### Aşama 2: Construction
- [ ] **Formula**: IF [action] THEN [outcome] BECAUSE [reason] şablonunu kullan.
- [ ] **Variables**: Bağımsız (değişen) ve bağımlı (ölçülen) değişkenleri netleştir.

### Aşama 3: Prioritization
- [ ] **ICE Score**: Impact (Etki), Confidence (Güven), Ease (Kolaylık) 1-10 puanla.
- [ ] **Risk**: Test başarısız olursa ne kaybederiz?

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Hipotez yanlışlanabilir mi? (Her zaman doğruysa hipotez değildir) |
| 2 | Sonuç ölçülebilir bir metrik mi (Click rate, Retention)? |
| 3 | "Because" kısmı mantıklı bir kullanıcı davranışına dayanıyor mu? |
