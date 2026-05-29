---
name: typo3-ckeditor5
description: "Agent Skill: CKEditor 5 development for TYPO3 v12+. Use when developing custom plugins, configuring RTE presets, or migrating from CKEditor 4. By Netresearch."
---

# TYPO3 CKEditor 5 Skill

CKEditor 5 integration patterns for TYPO3: custom plugins, configuration, and migration.

## Expertise Areas

- **Architecture**: Plugin system, schema/conversion, commands, UI components
- **TYPO3 Integration**: YAML configuration, plugin registration, content elements
- **Migration**: CKEditor 4→5, plugin conversion, data migration

## Reference Files

- `references/ckeditor5-architecture.md` - Core concepts
- `references/typo3-integration.md` - TYPO3-specific patterns
- `references/plugin-development.md` - Custom plugin guide
- `references/migration-guide.md` - CKEditor 4→5 migration

## Quick Reference

### Plugin Registration (ext_localconf.php)

```php
$GLOBALS['TYPO3_CONF_VARS']['RTE']['Presets']['my_preset'] = 'EXT:my_ext/Configuration/RTE/MyPreset.yaml';
$GLOBALS['TYPO3_CONF_VARS']['SYS']['ckeditor5']['plugins']['my-plugin'] = [
    'entryPoint' => 'EXT:my_ext/Resources/Public/JavaScript/Ckeditor/my-plugin.js',
];
```

### Plugin Structure

```
packages/my-plugin/src/
├── myplugin.js           # Main plugin (requires Editing + UI)
├── mypluginediting.js    # Schema, converters, commands
├── mypluginui.js         # Toolbar buttons, dropdowns
└── myplugincommand.js    # Command implementation
```

## Backend Integration (nr-llm)

When integrating CKEditor plugins with TYPO3 backend services (like nr-llm for AI features):

### Response Property Names

**CRITICAL:** Frontend JavaScript must use the exact property names returned by the backend.

```javascript
// Backend returns: { content: "...", model: "...", usage: {...} }

// WRONG - will be undefined
const text = result.completion;  // Backend doesn't return 'completion'

// CORRECT - matches backend response
const text = result.content;
```

**Real-world bug from t3x-cowriter:**
- Backend `CompleteResponse::success()` returned `content` property
- Frontend used `result.completion` (wrong property name)
- Fix: Changed to `result.content`

### Verification Pattern

```javascript
// Log response structure during development
console.log('Backend response:', JSON.stringify(result, null, 2));

// Then use correct property
const content = result.content || '';
```

## Migration Checklist

- [ ] Audit existing CKEditor 4 plugins
- [ ] Map features to CKEditor 5 equivalents
- [ ] Convert to class-based architecture
- [ ] Update YAML config from PageTSConfig
- [ ] Test content rendering
- [ ] **Verify JS property names match backend response** (if using AJAX)

## Verification

```bash
./scripts/verify-ckeditor5.sh /path/to/extension
```

---

> **Contributing:** https://github.com/netresearch/typo3-ckeditor5-skill
