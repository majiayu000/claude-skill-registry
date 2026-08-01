---
name: opportunity-scorer
description: '> Fırsat puanlama ve karar verme rehberi.'
---

---
name: opportunity_scorer
router_kit: FullStackKit
description: Fırsat puanlama, scoring rubric ve go/no-go karar verme rehberi.
metadata:
  skillport:
    category: business
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, opportunity scorer, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - prioritization
---

# 📊 Opportunity Scorer

> Fırsat puanlama ve karar verme rehberi.

---

## 📋 Scoring Framework

### Kriterler (0-10)
| Kriter | Ağırlık | Açıklama |
|--------|---------|----------|
| Market Size | 20% | TAM/SAM büyüklüğü |
| Fit | 25% | Yetenek/strateji uyumu |
| Competition | 15% | Rekabet yoğunluğu |
| Effort | 20% | Uygulama zorluğu |
| Timeline | 10% | Zaman çerçevesi |
| Risk | 10% | Risk seviyesi |

---

## 🔧 Scoring Template

```markdown
## Opportunity: [Name]

| Kriter | Score (0-10) | Weight | Weighted |
|--------|--------------|--------|----------|
| Market Size | 8 | 20% | 1.6 |
| Fit | 9 | 25% | 2.25 |
| Competition | 6 | 15% | 0.9 |
| Effort | 7 | 20% | 1.4 |
| Timeline | 8 | 10% | 0.8 |
| Risk | 7 | 10% | 0.7 |
| **TOTAL** | | | **7.65** |
```

---

## 🎯 Decision Thresholds

| Score | Recommendation | Action |
|-------|----------------|--------|
| 8.0+ | STRONG GO | Prioritize |
| 6.5-7.9 | GO | Proceed |
| 5.0-6.4 | CONDITIONAL | More research |
| <5.0 | NO GO | Pass |

---

## 📊 Comparison Matrix

| Opportunity | Score | Rank | Decision |
|-------------|-------|------|----------|
| Opp A | 8.2 | 1 | STRONG GO |
| Opp B | 7.1 | 2 | GO |
| Opp C | 5.8 | 3 | CONDITIONAL |
| Opp D | 4.2 | 4 | NO GO |

---

*Opportunity Scorer v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [RICE Scoring Model](https://www.productplan.com/glossary/rice-scoring-model/) & [Weighted Decision Matrix](https://www.atlassian.com/team-playbook/plays/decision-matrix)

### Aşama 1: Criteria Definition
- [ ] **Factors**: Değerlendirme kriterlerini (Market, Effort, Risk) projeye özel revize et.
- [ ] **Weighting**: Her kriterin ağırlığını (Toplam 100% olacak şekilde) belirle. Stratejik hedefe göre ayarla.
- [ ] **Scale**: 1-10 veya 1-5 arası net bir puanlama ölçeği tanımla (Örn: 10 = Hemen şimdi, 1 = Asla).

### Aşama 2: Scoring Process
- [ ] **Data Gathering**: Puanlamayı "tahmin" ile değil "veri" ile yap (Market raporu, teknik fizibilite).
- [ ] **Consensus**: Puanlamayı tek kişi değil, farklı disiplinlerden (Tech, Biz, Design) oluşan bir ekip ile yap.
- [ ] **Normalization**: Total skoru hesapla ve anormallikleri (Outliers) tartış.

### Aşama 3: Decision
- [ ] **Threshold Check**: Skoru eşik değerlerle (Go/No-Go) karşılaştır.
- [ ] **Sensitivity Analysis**: "Effort %10 artarsa karar değişir mi?" analizini yap.
- [ ] **Document**: Kararı ve gerekçeyi kaydet (Architectural Decision Record gibi).

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Tüm paydaşlar kriter ağırlıkları konusunda hemfikir mi? |
| 2 | En yüksek puan alan fırsat, şirketin şu anki stratejisiyle uyumlu mu? |
| 3 | Veto hakkı olan bir kısıt (Showstopper) gözden kaçtı mı? |
