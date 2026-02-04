---
name: package-review
description: Public package tester for GitHub repositories. Use when the user wants to review, test, or validate a public package, check documentation links, or verify composer.json quality.
---

# Package Review

**Role:** Tester of public packages published on GitHub or similar hubs. Validate documentation links and `composer.json` quality.

---

## 1. Documentation Links

**Do:**
- Find all links in the documentation.
- Verify that each link is functional.

---

## 2. Composer.json Quality

**Do:**
- Check the quality of the `composer.json` content.
- Determine whether all important keys are set.
- Validate that values are correct and complete.

---

## 3. Checklist

### 3.1 Required composer.json keys

**Check presence and correctness:**
- [ ] `name` — package name in `vendor/package` format
- [ ] `description` — clear, concise description
- [ ] `type` — package type (e.g. `library`, `project`)
- [ ] `license` — valid SPDX license identifier
- [ ] `authors` — author information
- [ ] `require` — dependencies with proper version constraints
- [ ] `autoload` — PSR-4 autoloading configuration

### 3.2 Recommended composer.json keys

**Check presence and usefulness:**
- [ ] `keywords` — searchable keywords
- [ ] `homepage` — project homepage URL
- [ ] `support` — support channels (issues, source, docs)
- [ ] `require-dev` — development dependencies
- [ ] `scripts` — useful composer scripts
