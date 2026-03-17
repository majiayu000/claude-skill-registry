---
name: i18n-sync
description: |
  Bilingual content synchronization validator for young-personal-site.
  Ensures perfect zh-TW/en translation consistency.
activation-keywords: [translation, 翻譯, bilingual, 雙語, language, 語言, i18n, zh-TW, en]
priority: high
allowed-tools: [Read, Bash, Grep]
---

# i18n-sync - Bilingual Content Synchronization

## Purpose
Ensure perfect synchronization between Chinese (zh-TW) and English (en) translation files.

**Prevents**: Missing translations, inconsistent keys, type mismatches
**Ensures**: Structural consistency, complete translations, deployment safety

---

## Translation Files
```
messages/
  ├── zh-TW.json  (Chinese Traditional)
  └── en.json     (English)
```

---

## Validation Workflow

### 1. File Existence & JSON Validity
```bash
# Check both files exist and are valid JSON
ls -la messages/
python3 -m json.tool messages/zh-TW.json > /dev/null
python3 -m json.tool messages/en.json > /dev/null
```

### 2. Key Structure Comparison
```yaml
Checks:
  - All keys in zh-TW.json exist in en.json
  - All keys in en.json exist in zh-TW.json
  - Nested object keys match recursively

Reports:
  - Missing keys in either file
  - Path to each missing key (e.g., "projects.mediatek.media_coverage")
```

### 3. Value Type Validation
```yaml
Checks:
  - String in zh-TW → String in en
  - Array in zh-TW → Array in en
  - Object in zh-TW → Object in en

Reports:
  - Type mismatches (e.g., array vs. string)
  - Path to each mismatch
```

### 4. Empty Translation Detection
```yaml
Checks:
  - Empty strings ("")
  - Empty arrays ([])
  - Missing values

Reports:
  - Path to each empty translation
  - Which file (zh-TW or en)
```

---

## Validation Severity Levels

### ❌ Critical (MUST Fix - Blocks Deployment)
1. Missing translation files
2. Invalid JSON syntax
3. Missing top-level keys (navigation, projects, speaking, about)

### ⚠️ Warning (SHOULD Fix - Safe but Incomplete)
1. Missing nested keys
2. Empty translations
3. Type mismatches

### ℹ️ Info (NICE to Have)
1. Key order inconsistency
2. Translation length ratio differences
3. Unused keys

---

## Output Format

### Success
```
✅ i18n Synchronization: PASS

📊 Results:
  ✅ Both files exist and valid
  ✅ All keys synchronized (zh-TW ↔ en)
  ✅ Type consistency verified
  ✅ No empty translations

🎉 Bilingual content perfectly synchronized!
```

### Warnings
```
⚠️ i18n Synchronization: WARNINGS

📊 Results:
  ✅ Files valid
  ⚠️ 2 missing keys
  ⚠️ 1 empty translation

🔧 Issues:
  1. projects.newproject.media_coverage - Missing in en.json
  2. speaking.futuretalk.summary - Empty in zh-TW.json

💡 Fix before deployment
```

### Failure
```
❌ i18n Synchronization: FAILED

🚨 Critical Issues:
  1. en.json - Invalid JSON syntax (line 45: Unexpected token })

⛔ DEPLOYMENT BLOCKED
```

---

## Auto-Fix (Optional)

**User confirms auto-fix**:
```yaml
Process:
  1. Missing keys in en.json:
     - Add with placeholder: "[TRANSLATION NEEDED]"
     - Preserve structure from zh-TW.json

  2. Missing keys in zh-TW.json:
     - Add with placeholder: "[需要翻譯]"
     - Preserve structure from en.json

  3. Empty translations:
     - Keep empty (requires human input)
     - Flag for manual completion

  4. Save:
     - Backup original files
     - Write formatted JSON
     - Preserve key order
```

---

## Common Scenarios

### New Project Added
```
1. Detect new key in zh-TW.json
2. Check if exists in en.json
3. If missing → Warn: "Missing English translation"
4. User adds translation
5. Validate → PASS
```

### Content Update
```
1. Detect change in zh-TW.json
2. Remind: "Update English version too"
3. Validate after both updated
4. Report consistency
```

### Bulk Refactor
```
1. Full JSON structure comparison
2. Report all differences
3. Suggest auto-fix or manual updates
4. Re-validate after fixes
```

---

## Integration

**With content-update**:
```
content-update adds content → i18n-sync validates → Report issues → Fix → Re-validate
```

**With deploy-check**:
```
deploy-check → TypeScript check → i18n-sync → If PASS → Deploy, If FAIL → Block
```

---

## Edge Cases

### Nested Object Depth Mismatch
```json
// zh-TW: { "details": { "version": "2.0" } }
// en: { "details": "Version 2.0" }
→ Type mismatch: object vs. string
```

### Array Length Differences
```json
// zh-TW: ["AI", "教育", "創新"]
// en: ["AI", "Education"]
→ Warning: Array length mismatch (3 vs. 2)
```

### Special Character Encoding
```json
// zh-TW: "AI 專家 • iOS 開發者"
// en: "AI Expert \u2022 iOS Developer"
→ Both valid (JSON handles encoding)
```

---

## Troubleshooting

### JSON Parse Error
```bash
# Validate JSON syntax
python3 -m json.tool messages/zh-TW.json
# Fix syntax error on reported line
```

### Too Many Missing Keys
```
1. Use auto-fix for placeholders
2. Prioritize critical sections (navigation, projects)
3. Schedule time to complete all translations
```

### Cannot Read Files
```bash
# Check existence and permissions
ls -la messages/
chmod 644 messages/*.json
```

---

## Best Practices

1. Run before every content change
2. Fix issues immediately (avoid translation debt)
3. Mirror key hierarchy in both files
4. Keep same key order (easier review)
5. Version control all changes

---

**Version**: v1.1 | **Updated**: 2025-12-31
**Project**: young-personal-site
**Integration**: content-update, deploy-check
