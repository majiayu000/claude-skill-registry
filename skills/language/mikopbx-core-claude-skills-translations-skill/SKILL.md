---
name: translations
description: Управление многоязычными переводами на 29 языков с приоритетом русского языка. Использовать при добавлении новых переводов, переводе на все языки, проверке консистентности или удалении устаревших ключей.
allowed-tools: Bash, Read, Grep, Glob
---

# MikoPBX Translation Managing

Translation management for the MikoPBX telephony system across 29 languages with Russian-first workflow.

## What This Skill Does

- Adds new translation keys to Russian (`ru/`) files
- Translates Russian keys to all 28 other languages using AI
- Validates translation consistency across all languages
- Removes obsolete translation keys from all languages
- Creates new translation module files

## When to Use

- Adding translations for new features or UI elements
- Translating Russian keys to all supported languages
- Checking translation consistency across languages
- Removing deprecated or unused translation keys
- Creating new translation modules for major features
- Fixing translation typos or errors
- Debugging missing translation issues

## Quick Start

### File Structure
```
src/Common/Messages/
├── ru/              ⭐ PRIMARY - Edit ONLY this
│   ├── ApiKeys.php
│   ├── Extensions.php
│   └── ... (all modules)
├── en/              🌐 Auto-translated
├── es/              🌐 Auto-translated
└── [27 more langs]  🌐 Auto-translated
```

### Golden Rule
**Developers ONLY modify Russian (`ru/*.php`) translations.**
All other languages are translated via:
- https://weblate.mikopbx.com (automatic sync)
- AI assistance (this skill)

## Critical Process Rules

### File-by-File Processing
**ONE FILE AT A TIME**: Never attempt to translate multiple files simultaneously. Complete one file fully (all languages) before moving to the next file.

### Sequential Language Processing
**PROCESS LANGUAGES SEQUENTIALLY**: Complete one language fully (analysis → translation → merge → validation → reset) before starting the next language.

### Validation After Each Step
**ALWAYS VERIFY KEY COUNT**: After processing each language, verify the key count matches Russian source EXACTLY. Stop if mismatch occurs.

### Preserve Existing Work
**NEVER OVERWRITE EXISTING TRANSLATIONS**: Only translate missing keys. Preserve all existing correct translations.

### Context Isolation
**RESET CONTEXT BETWEEN LANGUAGES**: Clear working variables and context after each language to prevent contamination or carry-over.

### Error Handling
- **Key count mismatch**: STOP, report issue, do not proceed
- **PHP syntax error**: STOP, fix error before continuing
- **Placeholder mismatch**: STOP, correct translation
- **Duplicate keys in source**: Report and await instructions

## Core Translation Rules

### 1. Placeholder Format
**ALWAYS** use `%variable%` format:

```php
// ✅ CORRECT
'gs_PasswordLength' => 'Пароль: %length% из %max% символов'

// ❌ WRONG
'gs_PasswordLength' => 'Пароль: {length} из {max} символов'
```

### 2. Technical Terms (Never Translate)
Keep these unchanged across ALL languages:
```
SIP, IAX, AMI, AJAM, PJSIP, NAT, STUN, TURN, RTP, CDR, IVR,
DID, CID, DTMF, codec, trunk, extension, IP, DNS, VPN
```

Example:
```php
// Russian
'pr_SipProviderSettings' => 'Настройки SIP провайдера'

// Thai - SIP stays the same
'pr_SipProviderSettings' => 'การตั้งค่าผู้ให้บริการ SIP'
```

### 3. Quote Escaping
Escape quotes properly for PHP:

```php
// ✅ CORRECT
'msg_Example' => 'He said: "Don\'t forget"'

// ❌ WRONG - breaks PHP
'msg_Example' => 'He said: "Don't forget"'
```

### 4. Consistency Requirement
All languages MUST have:
- ✅ Identical translation keys
- ✅ Identical file structure
- ✅ Same placeholder names
- ✅ Same array structure

**Example:** If Russian has 157 keys in `ApiKeys.php`, ALL 28 other languages must have exactly 157 keys in `ApiKeys.php`.

## Working with Large Files (Batch Processing)

### When to Use Batch Mode

Files are automatically processed in batch mode when they have:
- **> 300 translation keys** (missing in target language)
- **Average value length > 100 characters** (complex technical descriptions)
- **Files like:** RestApi.php (1962 keys), Common.php (700+ keys), GeneralSettings.php (500+ keys)

### Batch Processing Strategy

**Automatic Detection:**
```bash
# Check if file needs batching
php .claude/skills/translations/helpers/translation-batch-manager.php analyze src/Common/Messages/ru/Common.php en
```

**Key Thresholds:**
- Files < 150 keys → **Direct mode** (process all at once)
- Files 150-300 keys → **Optional batching** (based on complexity)
- Files > 300 keys → **Batch mode required** (100 keys per batch)

### Batch Processing Workflow

When translating large files, follow this **sequential batch workflow**:

**1. Analysis Phase:**
```bash
# Analyze target file to determine batching strategy
php translation-batch-manager.php analyze src/Common/Messages/ru/RestApi.php en
```

Output tells you:
- Total missing keys
- Whether batching is needed
- Number of batches required
- Average value length

**2. Split Phase:**
```bash
# Create batches (saved to .claude/temp/batches/)
php translation-batch-manager.php split src/Common/Messages/ru/RestApi.php en 100
```

Creates JSON files:
- `.claude/temp/batches/en_RestApi/batch_1.json` (keys 1-100)
- `.claude/temp/batches/en_RestApi/batch_2.json` (keys 101-200)
- ... etc

**3. Translation Phase (Repeat for each batch):**

For each batch file:
1. Read batch JSON file
2. Extract `keys` object (Russian key-value pairs)
3. Translate ONLY those keys using AI
4. Preserve technical terms (SIP, PBX, CDR, etc.)
5. Keep `%placeholder%` format identical
6. Escape quotes properly

**4. Merge Phase (After each batch translation):**
```bash
# Merge translated batch into target file
php translation-batch-manager.php merge src/Common/Messages/en/RestApi.php batch_1_translated.json
```

This command:
- Merges new translations with existing ones
- Maintains key order from Russian source
- Creates backup (.backup file)
- Validates PHP syntax

**5. Validation Phase (After each merge):**
```bash
# Validate merged result
php translation-batch-manager.php validate src/Common/Messages/en/RestApi.php src/Common/Messages/ru/RestApi.php
```

Checks:
- PHP syntax is valid
- Key count matches Russian source
- No missing keys
- No extra keys
- Placeholders match exactly

**6. Context Reset:**
After completing each batch:
- Clear working variables
- Log progress
- DO NOT carry over data to next batch

### Batch Translation Example

**Input batch JSON:**
```json
{
  "batch_num": 1,
  "total_batches": 20,
  "keys": {
    "rest_ApiKeys_ApiDescription": "Comprehensive API key management...",
    "rest_Extensions_CreateEndpoint": "Create a new PBX extension...",
    ...
  }
}
```

**Translate keys → Save as `batch_1_translated.json`:**
```json
{
  "batch_num": 1,
  "total_batches": 20,
  "keys": {
    "rest_ApiKeys_ApiDescription": "Comprehensive API key management...",
    "rest_Extensions_CreateEndpoint": "Create a new PBX extension...",
    ...
  }
}
```

**Merge into target file:**
```bash
php translation-batch-manager.php merge src/Common/Messages/en/RestApi.php batch_1_translated.json
```

### Progress Tracking with TodoWrite

When processing large files, create detailed task lists:

```
[1/28] English (en) - RestApi.php
  [1/20] ✓ Batch 1 (keys 1-100) - Translated & merged
  [2/20] ⏳ Batch 2 (keys 101-200) - In progress
  [3/20] ⏸ Batch 3 (keys 201-300) - Pending
  ...
  [20/20] ⏸ Batch 20 (keys 1901-1962) - Pending

[2/28] German (de) - RestApi.php
  [1/20] ⏸ Batch 1 (keys 1-100) - Pending
  ...
```

### Critical Batch Mode Rules

1. **One Batch at a Time:** Complete translation → merge → validate before next batch
2. **Incremental Progress:** Each batch is independently saved and validated
3. **Context Isolation:** Reset AI context between batches to prevent contamination
4. **Validation After Each Batch:** Never skip validation between batches
5. **Resume Capability:** If error occurs, can resume from last successful batch

### Error Handling in Batch Mode

**PHP Syntax Error in Merged File:**
- STOP immediately
- Restore from .backup file
- Fix translation in batch JSON
- Re-run merge command

**Key Count Mismatch After Merge:**
- STOP immediately
- Check batch JSON for duplicate keys
- Validate batch JSON format
- Re-run merge with corrected batch

**Placeholder Format Error:**
- Fix translation in batch JSON
- Re-run merge command
- Validate placeholders match

### Helper Script Reference

**Commands:**
```bash
# Analyze file
php translation-batch-manager.php analyze <ru_file> <target_lang>

# Split into batches
php translation-batch-manager.php split <ru_file> <target_lang> [batch_size]

# Merge batch
php translation-batch-manager.php merge <target_file> <batch_json>

# Validate result
php translation-batch-manager.php validate <target_file> <ru_file>

# Check status
php translation-batch-manager.php status <ru_file> <target_lang>
```

**All commands output JSON** for easy parsing by agents.

### Temporary Files Location

Batch files are stored in `.claude/temp/batches/` (gitignored):
```
.claude/temp/batches/
├── en_RestApi/
│   ├── batch_1.json
│   ├── batch_2.json
│   └── ...
├── de_Common/
│   ├── batch_1.json
│   └── ...
```

## Common Tasks

### Task 1: Add New Translations (Russian Only)

**Quick workflow:**

1. Determine module and prefix (see [prefixes.md](reference/prefixes.md))
2. Read existing Russian file
3. Add new keys with proper prefix
4. Maintain alphabetical order
5. Use Edit tool to save changes

**Example:**
```php
// ru/ApiKeys.php
return [
    // ... existing keys

    // API Key Permissions (new feature)
    'ak_PermissionsTitle' => 'Разрешения API ключа',
    'ak_PermissionRead' => 'Чтение',
    'ak_PermissionWrite' => 'Запись',
];
```

**After adding:**
- Report what was added
- Remind about cache clearing
- Ready for translation to other languages

### Task 2: Translate to All Languages (Incremental Process)

**IMPORTANT:** This workflow supports **incremental translation** - it translates ONLY missing keys and preserves existing translations.

**Quick workflow:**

1. **Initial Setup:**
   - Read Russian source file (e.g., `ru/ApiKeys.php`)
   - Count total keys in source
   - Check for duplicate keys in source
   - Scan `/src/Common/Messages/` to detect all language folders

2. **For EACH of 28 languages (process sequentially):**

   a) **Pre-Translation Analysis:**
      - Read existing target language file (if exists)
      - Compare with Russian source to identify:
        - Missing keys (in Russian but not in target)
        - Obsolete keys (in target but not in Russian)
      - Report findings

   b) **Incremental Translation:**
      - Translate ONLY the missing keys from Russian
      - **Preserve all existing translations** (do not retranslate)
      - Use AI translation with proper context
      - Batch process (max 50 keys per batch)
      - Apply localization rules (phone numbers, addresses, etc.)
      - Keep technical terms unchanged
      - Preserve `%placeholder%` format exactly

   c) **Merge & Update:**
      - Merge new translations with existing ones
      - Remove obsolete keys not in Russian source
      - Maintain key order from Russian file
      - Use proper PHP array syntax and indentation

   d) **Validation:**
      - Count keys in updated file
      - Verify count matches Russian source EXACTLY
      - Check all placeholders are preserved
      - Validate PHP syntax with `php -l`
      - Report validation results

   e) **Context Reset:**
      - Clear working variables before next language
      - Log completion status
      - DO NOT carry over data to next language

3. **Final Report:**
   - Summary of all languages processed
   - Total keys added/removed per language
   - Any errors or warnings
   - Confirmation all files have identical key counts

**Translation with AI:**
- Keep technical terms unchanged (SIP, IAX, PBX, CDR, etc.)
- Preserve `%placeholder%` format
- Adapt examples to local context (phone numbers, etc.)
- Use appropriate quotes for language
- Maintain informal but professional tone

### Task 3: Check Translation Consistency

**Quick workflow:**

1. Read Russian baseline
2. Compare each language with Russian
3. Report discrepancies:
   - Missing keys
   - Extra keys
   - Key count mismatches
4. Suggest fixes

**Example report:**
```
✅ en/ApiKeys.php: 157 keys (matches)
✅ es/ApiKeys.php: 157 keys (matches)
⚠️ th/ApiKeys.php: 145 keys (12 missing)
⚠️ ja/ApiKeys.php: 160 keys (3 extra)
```

### Task 4: Remove Obsolete Translations

**Quick workflow:**

1. Ask for keys to remove
2. Verify usage in codebase (optional)
3. Remove from Russian first
4. Remove from all 28 other languages
5. Report cleanup results

### Task 5: Create New Translation File

**Quick workflow:**

1. Gather info (module name, prefix, initial keys)
2. Create Russian template with header
3. Add to `ru/[ModuleName].php`
4. Replicate to all 28 other languages
5. Report completion

## Module Prefixes

Common prefixes (see [prefixes.md](reference/prefixes.md) for complete list):

| Prefix | Module | Example |
|--------|--------|---------|
| `ak_` | API Keys | `ak_AddNewApiKey` |
| `ex_` | Extensions | `ex_AddNewExtension` |
| `pr_` | Providers | `pr_SipProviderSettings` |
| `gs_` | General Settings | `gs_PasswordLength` |
| `api_` | REST API messages | `api_UnknownError` |

**Suffix patterns:**
- `_Validate` - Validation rules
- `_Error` - Error messages
- `_Tooltip` - UI tooltips
- `_header` / `_desc` - Structured content

## Supported Languages

MikoPBX supports **29 languages**. See [language-codes.md](reference/language-codes.md) for complete list.

**Primary language:** Russian (`ru`) ⭐
**Other languages:** 28 languages from Azerbaijani to Simplified Chinese

## File Format Example

```php
<?php
/**
 * API keys translations
 */

return [
    // AK - API Keys module prefix
    'ak_AddNewApiKey' => 'Добавить API ключ',
    'ak_ApiKeyWarning' => 'Сохраните этот ключ сейчас!',

    // With placeholders
    'ak_ConfirmDelete' => 'Удалить API ключ "{0}"?',
    'gs_PasswordLength' => 'Длина: %length% из %max%',

    // Tooltip example
    'ak_ApiKeyUsageTooltip_header' => 'Использование API ключей',
    'ak_ApiKeyUsageTooltip_curl_example' => 'curl -H "Authorization: Bearer KEY" ...',
];
```

## Cache Management

Translations are cached in Redis. After changes:

```bash
# Clear Redis cache
docker exec <container_id> redis-cli FLUSHDB

# Or restart container (clears all caches)
docker restart <container_id>

# Browser cache (hard refresh)
Ctrl+Shift+R (Windows/Linux)
Cmd+Shift+R (Mac)
```

## Validation Commands

```bash
# Count keys in Russian file
php -r "echo count(include 'src/Common/Messages/ru/ApiKeys.php');"

# Compare key counts across languages
for lang in en es fr de; do
  echo "$lang: $(php -r "echo count(include 'src/Common/Messages/$lang/ApiKeys.php');")"
done

# Find all translation files for a key
grep -r "ak_ApiKey" src/Common/Messages/

# Check PHP syntax
php -l src/Common/Messages/ru/ApiKeys.php
```

## Error Prevention

### Common Mistakes to Avoid

❌ **Breaking PHP syntax with quotes:**
```php
// WRONG
'msg' => 'He said: "Don't do this"'  // Breaks PHP

// CORRECT
'msg' => 'He said: "Don\'t do this"' // Escaped
```

❌ **Inconsistent placeholders:**
```php
// Russian: %username%
// WRONG translation: %user% (different name!)
// CORRECT: %username% (same name)
```

❌ **Translating technical terms:**
```php
// WRONG: 'pr_SipSettings' => 'Параметры СИП'
// CORRECT: 'pr_SipSettings' => 'Параметры SIP'
```

## Validation Checklist

Before finishing translation work:

- [ ] All 29 languages have identical file structure
- [ ] Each language has same number of keys per file
- [ ] Placeholders use `%variable%` format consistently
- [ ] Technical terms unchanged across languages
- [ ] Quotes properly escaped
- [ ] No PHP syntax errors (run `php -l`)
- [ ] Files have proper headers
- [ ] Keys follow naming conventions
- [ ] Translation cache cleared
- [ ] Tested in UI

## Reporting Format

Always provide clear, structured output:

```
🎯 Translation Task: [Task Name]

📁 Files Modified:
- ru/ApiKeys.php: +5 keys
- en/ApiKeys.php: +5 keys (translated)
- [... 27 more languages]

📊 Statistics:
- Keys added: 5
- Languages updated: 29
- Files modified: 29

✅ Validation:
- All languages consistent: YES
- Placeholder format correct: YES
- Technical terms preserved: YES
- PHP syntax valid: YES

⚠️ Next Steps:
1. Clear Redis cache
2. Clear browser cache
3. Test translations in UI
4. Commit changes if working

📝 Translation Keys Added:
1. ak_Feature - Feature description
2. ak_FeatureTooltip - Help tooltip
3. ak_ValidateFeature - Validation message
```

## Best Practices

1. **Batch Operations** - Process 50 keys at a time to avoid context overflow
2. **Incremental Validation** - Validate after each language
3. **Backup Before Changes** - Git commit before translating 100+ keys
4. **File-per-Module** - Create dedicated files for major features
5. **Consistent Naming** - Always use proper prefix
6. **Context-Aware** - Ask about feature purpose for better translations
7. **Test Early** - Test after small batches, not after everything
8. **Progress Tracking** - Report progress clearly for each language (see example below)

### Progress Tracking Example

When processing a file, report progress like this:

```
🎯 Processing: ApiKeys.php
📊 Source (ru): 47 keys found, 0 duplicates
🌐 Target languages: en, de, es, fr, it, nl, pt, th (8 languages)

[1/8] 🇬🇧 English (en)
  ✓ Pre-analysis: 5 missing keys, 2 obsolete keys
  ✓ Translation: 5 keys translated
  ✓ Merge: Updated with new keys, removed obsolete
  ✓ Validation: 47 keys (matches source)
  ✓ Context reset: Done

[2/8] 🇩🇪 German (de)
  ✓ Pre-analysis: 3 missing keys, 1 obsolete key
  ✓ Translation: 3 keys translated
  ✓ Merge: Updated with new keys, removed obsolete
  ✓ Validation: 47 keys (matches source)
  ✓ Context reset: Done

... continue for each language ...

✅ Final Summary:
  - Languages processed: 8/8
  - Total keys added: 28
  - Total keys removed: 10
  - All languages validated: YES
  - Cache cleared: Reminder sent
```

## Additional Resources

**Detailed References:**
- [Language Codes](reference/language-codes.md) - All 29 supported languages
- [Module Prefixes](reference/prefixes.md) - Complete prefix reference
- [AI Prompts](reference/ai-prompts.md) - AI translation templates
- [Workflow Examples](examples/workflow-examples.md) - Real-world scenarios

**External Links:**
- https://weblate.mikopbx.com - Weblate translation portal
- Phalcon Translation Docs

## Task Activation Patterns

This skill activates when you say:

- "Add translation for..."
- "Create new translation file..."
- "Translate [file] to all languages"
- "Check translation consistency"
- "Remove translation key..."
- "How do I add translations?"
- "Why is translation not showing?"
- "Translate my Russian keys"

---

**Remember:**
- 🇷🇺 Russian is PRIMARY - always edit Russian first
- 🌐 Other languages follow Russian structure exactly
- 🔧 Technical terms never translate
- 📝 Placeholders always use %format%
- 🎨 Localization adds creativity, not literal translation
- ✅ Consistency check before completing task

---

*Translation management for MikoPBX international development team* 🌍
