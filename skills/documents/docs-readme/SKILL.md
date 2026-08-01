---
name: docs-readme
description: '> README ve proje dokümantasyonu best practices.'
---

---
name: docs_readme
router_kit: ManagementKit
description: README best practices ve proje dokümantasyon şablonları.
metadata:
  skillport:
    category: operations
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, docs readme, documentation, efficiency, git, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - docs-code
---

# 📄 Docs README

> README ve proje dokümantasyonu best practices.

---

## 📋 README Template

```markdown
# Project Name

> Tek cümleyle projenin ne yaptığını açıkla.

## Features
- ✅ Feature 1
- ✅ Feature 2

## Quick Start

### Prerequisites
- Node.js 20+

### Installation
npm install && npm run dev

## Documentation
- [API Reference](./docs/api.md)
- [Contributing](./CONTRIBUTING.md)

## License
MIT
```

---

## 📝 README Kuralları

| Kural | Açıklama |
|-------|----------|
| Başlık açık | Ne olduğu hemen anlaşılmalı |
| Quick start kısa | 5 dakikada çalıştırabilmeli |
| Copy-paste ready | Kod blokları doğrudan çalışmalı |
| Görsel kullan | Badge, screenshot, diagram |

---

## 📊 Badges

```markdown
![Build](https://img.shields.io/badge/build-passing-green)
![Coverage](https://img.shields.io/badge/coverage-95%25-green)
```

---

*Docs README v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Awesome README](https://github.com/matiassingers/awesome-readme)

### Aşama 1: First Impression
- [ ] **Hero**: Proje ismi, kısa açıklama ve mümkünse logo/banner ekle.
- [ ] **Badges**: CI/CD durumu, lisans ve versiyon badge'lerini en üste koy.
- [ ] **Demo**: Canlı demo linki veya GIF/Screenshot ekle.

### Aşama 2: Content Structure
- [ ] **Installation**: Tek satırlık kurulum komutu (`npm install ...`).
- [ ] **Usage**: En yaygın kullanım senaryosu için kod örneği.
- [ ] **Contributing**: Katkı sağlama rehberine link (`CONTRIBUTING.md`).

### Aşama 3: Maintenance
- [ ] **Links**: Kırık link kontrolü yap (Link Checker).
- [ ] **License**: LICENSE dosyası ile README'deki lisans beyanı tutarlı mı?
- [ ] **Update**: Her major release sonrası README'yi güncelle.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Okuyucu projenin ne işe yaradığını 5 saniyede anlıyor mu? |
| 2 | Kurulum komutları "copy-paste" ile hatasız çalışıyor mu? |
| 3 | Görseller optimize edilmiş (hafif) ve yükleniyor mu? |
