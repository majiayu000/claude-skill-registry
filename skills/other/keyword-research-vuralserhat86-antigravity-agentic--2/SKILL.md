---
name: keyword_research
router_kit: ManagementKit
description: SEO keyword araştırma, arama hacmi analizi ve içerik stratejisi rehberi.
metadata:
  skillport:
    category: research
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, keyword research, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - search
---

# 🔑 Keyword Research

> SEO keyword araştırma ve içerik stratejisi rehberi.

---

## 📋 Keyword Metrikleri

| Metrik | Açıklama | İdeal |
|--------|----------|-------|
| **Search Volume** | Aylık arama sayısı | >100 |
| **Keyword Difficulty** | Sıralama zorluğu | <50 |
| **CPC** | Tıklama başı maliyet | Domain'e göre |
| **Intent** | Arama niyeti | Match |

---

## 🎯 Search Intent

| Intent | Açıklama | Örnek |
|--------|----------|-------|
| **Informational** | Bilgi arama | "react nedir" |
| **Navigational** | Site arama | "github login" |
| **Commercial** | Karşılaştırma | "en iyi cms" |
| **Transactional** | Satın alma | "hosting satın al" |

---

## 🔧 Araştırma Süreci

### 1. Seed Keywords
```
[Ana konu]
    ├── Alt konu 1
    ├── Alt konu 2
    └── Alt konu 3
```

### 2. Keyword Expansion
- Google Autocomplete
- "People Also Ask"
- Related searches
- Competitor keywords

### 3. Filtreleme
```
Volume > 100
AND Difficulty < 50
AND Intent = Target
```

---

## 📊 Keyword Mapping

| Keyword | Volume | KD | Intent | Target Page |
|---------|--------|-----|--------|-------------|
| react tutorial | 10K | 45 | Info | /blog/react |
| react vs vue | 5K | 38 | Comm | /comparison |
| react developer | 3K | 52 | Trans | /hire |

---

## 📝 Content Brief Template

```markdown
## Target Keyword: [keyword]

### Metadata
- Volume: [X]
- Difficulty: [X]
- Intent: [Type]

### SERP Analysis
- Top 3 results: [...]
- Content type: [...]
- Avg word count: [...]

### Outline
1. H1: [Title]
2. H2: [Section 1]
3. H2: [Section 2]
4. ...

### LSI Keywords
- keyword1
- keyword2
```

---

*Keyword Research v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Semrush Keyword Strategy](https://www.semrush.com/blog/keyword-research-guide/) & [Ahrefs SEO Guide](https://ahrefs.com/blog/keyword-research/)

### Aşama 1: Topic Discovery (Seed)
- [ ] **Brainstorm**: İş hedeflerine uygun ana konuları (Topic Clusters) belirle.
- [ ] **Competitor**: Rakiplerin trafik aldığı kelimeleri analiz et (Gap Analysis).
- [ ] **Questions**: "People Also Ask" ve forumlardan (Reddit/Quora) soru kalıplarını topla.

### Aşama 2: Metric Analysis
- [ ] **Volume vs Difficulty**: Yüksek hacim + Düşük KD (Keyword Difficulty) fırsatlarını (Low Hanging Fruit) bul.
- [ ] **Intent Matching**: Kelimenin niyetini (Navigational, Informational, Transactional) belirle.
- [ ] **Long-tail**: Dönüşüm oranı yüksek 3+ kelimelik öbeklere odaklan.

### Aşama 3: Mapping & Clustering
- [ ] **Pillar Page**: Ana kelimeyi kapsayan kapsamlı rehber planla.
- [ ] **Cannibalization**: Aynı kelimeyi hedefleyen birden fazla sayfa olmamasını sağla.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Hedef kelimenin arama niyeti ile içeriğimiz uyuşuyor mu? |
| 2 | Bu kelimede sıralanmak için domain otoritemiz yeterli mi? |
| 3 | Rakip içeriklerden "daha iyi" (10x Content) bir şey sunuyor muyuz? |
