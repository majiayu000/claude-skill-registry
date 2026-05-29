---
name: ultrathink_templates
router_kit: FullStackKit
description: UltraThink analiz şablonları - hipotez, alternatif, karar ve risk matrisleri.
metadata:
  skillport:
    category: thinking
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, ultrathink templates, utilities, version control, workflow]      - ultrathink-core
---

# 📝 UltraThink Templates

> Analiz ve karar şablonları.

---

## 💡 Hipotez Template

```markdown
### H1: [Hipotez Adı]
- **Açıklama:** [Ne düşünüyoruz?]
- **Güven:** [%]
- **Varsayımlar:** [Neye dayanıyor?]
- **Test:** [Nasıl doğrularız?]
```

---

## ⚖️ Alternatif Karşılaştırma

| Kriter | Ağırlık | Yaklaşım 1 | Yaklaşım 2 |
|--------|---------|------------|------------|
| Performans | 30% | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Karmaşıklık | 20% | ⭐⭐⭐ | ⭐⭐ |
| Maliyet | 25% | $$ | $ |
| Risk | 25% | Düşük | Orta |

---

## 🎯 Final Karar Template

```markdown
## Seçilen Çözüm
**Yaklaşım:** [İsim]
**Güven:** [%]
**Gerekçe:** [Neden?]

## Risk Matrisi
| Risk | Olasılık | Etki | Önlem |
|------|----------|------|-------|
| [Risk] | [%] | [Seviye] | [Strateji] |

## Aksiyon Planı
1. [ ] Adım 1
2. [ ] Adım 2
```

---

## 🔴 Bias Kontrolü

| Bias | Kontrol Sorusu |
|------|----------------|
| Anchoring | İlk fikrim en iyisi mi? |
| Confirmation | Karşı kanıt aradım mı? |
| Overconfidence | Nasıl yanılabilirim? |

## 🔄 Workflow

> **Kaynak:** [McKinsey Problem Solving Framework](https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/the-seven-steps-of-becoming-a-powerhouse-problem-solver) & [Decision Matrix Best Practices](https://en.wikipedia.org/wiki/Decision_matrix)

### Aşama 1: Template Selection
- [ ] **Situation Analysis**: Mevcut durumun derinliğini belirle (Hafif/Derin).
- [ ] **Specific Template**: Hipotez, Karar veya Risk şablonlarından ihtiyaca uygun olanı seç.
- [ ] **Metric Definition**: Karşılaştırma için kullanılacak ağırlıklı kriterleri (Web/Performance/Cost) belirle.

### Aşama 2: Data Entry & Scoring
- [ ] **Evidence Gathering**: Şablonu doldururken varsayımlar yerine verilere (Log, Test, Doc) dayan.
- [ ] **Bias Mitigation**: Puanlama yaparken "Confirmation Bias" kontrolü yap.
- [ ] **Alternative Mapping**: En az iki gerçekçi alternatifi şablona ekle.

### Aşama 3: Result Summary & Archive
- [ ] **Final Verdict**: Karşılaştırma sonucunda çıkan "Winner" çözümü gerekçeleriyle özetle.
- [ ] **Risk Mitigation Plan**: Seçilen çözümün zayıf noktaları için önlem planını hazırla.
- [ ] **Artifact Update**: Sonucu `task_boundary` veya dökümante edilecek dosyaya yansıt.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Şablon tüm kritik soru işaretlerini (Unknowns) kapsıyor mu? |
| 2 | Puanlama toplamı %100 ağırlığa denk geliyor mu? |
| 3 | Çıktı, üçüncü bir kişi tarafından kolayca anlaşılabilir mi? |

---
*UltraThink Templates v1.5 - With Workflow*
