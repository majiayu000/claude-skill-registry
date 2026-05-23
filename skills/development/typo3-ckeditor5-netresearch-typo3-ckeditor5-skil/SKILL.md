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

## Migration Checklist

- [ ] Audit existing CKEditor 4 plugins
- [ ] Map features to CKEditor 5 equivalents
- [ ] Convert to class-based architecture
- [ ] Update YAML config from PageTSConfig
- [ ] Test content rendering

## Verification

```bash
./scripts/verify-ckeditor5.sh /path/to/extension
```

---

> **Contributing:** https://github.com/netresearch/typo3-ckeditor5-skill
