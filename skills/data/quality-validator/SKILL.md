---
name: quality-validator
description: '> Kalite standardı ve deliverable validation rehberi.'
---

---
name: quality_validator
router_kit: FullStackKit
description: Ship öncesi son kontrol, deliverable validation, compliance. ⚠️ Son kalite kontrolü için kullan. Kod inceleme için → code-review.
metadata:
  skillport:
    category: quality
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, optimization, productivity, programming, project management, quality assurance, quality validator, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - standards
---

# ✅ Quality Validator

> Kalite standardı ve deliverable validation rehberi.

---

## 📋 Validation Checklist

### Documentation
```checklist
- [ ] All required sections present
- [ ] No placeholder content
- [ ] Links working
- [ ] Images loading
- [ ] Spelling/grammar checked
```

### Code
```checklist
- [ ] Linting passes
- [ ] Tests passing
- [ ] No console.log
- [ ] No TODO/FIXME
- [ ] Types complete
```

### Design
```checklist
- [ ] Responsive
- [ ] Accessible (WCAG)
- [ ] Consistent styling
- [ ] Cross-browser tested
```

---

## 🔧 Quality Scores

| Score | Level | Action |
|-------|-------|--------|
| 90-100 | Excellent | Ship |
| 80-89 | Good | Minor fixes |
| 70-79 | Acceptable | Review needed |
| <70 | Poor | Major rework |

---

## 📊 Validation Report

```markdown
# Quality Validation Report

**Item:** [Name]
**Date:** [Date]
**Validator:** [Name]

## Summary
- **Overall Score:** [X]/100
- **Status:** Pass | Fail | Conditional

## Checklist Results
| Category | Pass | Fail | N/A |
|----------|------|------|-----|
| Documentation | 8 | 2 | 0 |
| Code | 12 | 1 | 2 |
| Design | 5 | 0 | 1 |

## Issues Found
| ID | Severity | Description | Status |
|----|----------|-------------|--------|
| 1 | High | [Issue] | Open |
| 2 | Low | [Issue] | Fixed |

## Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
```

---

*Quality Validator v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [SonarQube Clean Code](https://www.sonarsource.com/clean-code/) & [Google Engineering Practices](https://github.com/google/eng-practices)

### Aşama 1: Static Analysis & Automation
- [ ] **Linter/Formatter**: Sadece "hata var mı" diye değil, konfigürasyonun (`eslintrc`, `tsconfig`) sıkılığını (strictness) kontrol et.
- [ ] **Dependency Audit**: `npm audit` veya `pip audit` ile güvenlik açığı olan paketleri engelle (Pipeline blocking).
- [ ] **Complexity**: Cyclomatic Complexity değeri yüksek (Örn: >15) fonksiyonları reddet.

### Aşama 2: Runtime Quality
- [ ] **Test Coverage**: Sadece satır sayısı değil, "Branch Coverage"ın %80 üzerinde olduğunu doğrula.
- [ ] **Performance**: Kritik path'lerde gereksiz re-render (React) veya N+1 sorgu (Backend) kontrolü yap.
- [ ] **Error Handling**: Happy path dışında, hata durumlarının (Error Boundary, Try-Catch) test edildiğini onayla.

### Aşama 3: Deliverable & Compliance
- [ ] **Docs**: README güncel mi? API değişiklikleri Swagger/OpenAPI ile uyumlu mu?
- [ ] **License**: 3. parti kütüphanelerin lisans uyumluluğunu (Proprietary projede GPL kullanımı var mı?) kontrol et.
- [ ] **Release Notes**: Kullanıcıya dönük değişikliklerin (Changelog) anlaşılır olduğunu doğrula.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | CI pipeline'ı "warning" durumunda bile fail edecek şekilde (treat warnings as errors) ayarlandı mı? |
| 2 | "Works on my machine" sorunu ekarte edildi mi? (Dockerized test run). |
| 3 | Güvenlik taraması (SAST) temiz mi? |
