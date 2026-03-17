---
name: docs_code
router_kit: ManagementKit
description: Code comments, JSDoc/TSDoc ve changelog best practices.
metadata:
  skillport:
    category: operations
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, docs code, documentation, efficiency, git, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - docs-api
---

# 💻 Docs Code

> Code documentation ve changelog best practices.

---

## 📝 JSDoc/TSDoc

```typescript
/**
 * Calculates total price including tax.
 * 
 * @param amount - Base amount before tax
 * @param taxRate - Tax rate as decimal (0.18 = 18%)
 * @returns Total amount including tax
 * 
 * @example
 * const total = calculateTotal(100, 0.18); // 118
 */
function calculateTotal(amount: number, taxRate: number): number {
  return amount * (1 + taxRate);
}
```

---

## ✅ Comment Best Practices

```typescript
// ❌ What (kod zaten söylüyor)
// Increment counter by 1
counter++;

// ✅ Why (neden böyle yapıldığını açıklıyor)
// Using setTimeout to debounce API calls
setTimeout(() => saveChanges(), 500);

// ✅ Business logic
// Premium users get 20% discount (JIRA-1234)
if (user.isPremium) discount = 0.20;
```

---

## 📋 Changelog (Keep a Changelog)

```markdown
## [1.2.0] - 2025-01-15

### Added
- OAuth2 authentication

### Fixed
- Login button on mobile

### Security
- Patched XSS vulnerability
```

---

## 🔗 Conventional Commits

```
feat(auth): add Google OAuth
fix(api): handle null response
docs(readme): add installation
refactor(utils): simplify logic
```

---

*Docs Code v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [TSDoc Standard](https://tsdoc.org/) & [Keep a Changelog](https://keepachangelog.com/)

### Aşama 1: Inline Documentation
- [ ] **Public API**: Export edilen her fonksiyon/class için TSDoc (`/** ... */`) yaz.
- [ ] **Context**: "Neden" (Why) sorusunu cevaplayan yorumlar ekle (`// Optimize for ...`).
- [ ] **Examples**: Karmaşık fonksiyonlar için `@example` bloğu ekle.

### Aşama 2: Changelog Management
- [ ] **Unreleased**: Yapılan değişiklikleri anında `[Unreleased]` başlığı altına ekle.
- [ ] **Categories**: Added, Changed, Deprecated, Removed, Fixed, Security etiketlerini kullan.
- [ ] **Versioning**: SemVer (Maj.Min.Patch) kurallarına göre versiyonla.

### Aşama 3: Commit Standards
- [ ] **Format**: Conventional Commits (`feat:`, `fix:`, `docs:`) kullan.
- [ ] **Scope**: Değişikliğin kapsamını belirt (`feat(auth):`).

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | IDE'de fonksiyon üzerine gelince TSDoc çıkıyor mu? |
| 2 | Changelog'da tarih formatı ISO 8601 (YYYY-MM-DD) mi? |
| 3 | Commit mesajı "ne" ve "neden" sorularını cevaplıyor mu? |
