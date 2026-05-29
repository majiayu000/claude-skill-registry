---
name: template-update
description: Updates template files in metasaver-marketplace as the source of truth before applying changes elsewhere. Use when standardizing configs across repos - updates template FIRST, then uses it for remediation. For config skills and domain skills with templates.
---

# Template Update Skill

> **AUDIT WORKFLOW SUPPORT** - Called by `/audit` command to ensure templates stay current before applying fixes.

**Purpose:** Update templates in metasaver-marketplace as the authoritative source, enabling downstream use in consumer repos

**Trigger:** After audit violations detected, before remediation options presented

**Input:**

- Template type (e.g., `eslint`, `prettier`, `vite-config`)
- New/updated content
- Reason for update
- Optional: affected repos list

**Output:**

- `updated_template_path` - Full path to updated template
- `template_content` - Content of template after update
- `affected_repos` - List of consumer repos that should re-audit

---

## Workflow Steps

1. **Identify template location:**
   - Config skills: `plugins/metasaver-core/skills/config/{category}/{name}/`
   - Domain skills: `plugins/metasaver-core/skills/domain/{name}/`
   - Look for SKILL.md with templates referenced

2. **Validate template readiness:**
   - Check if SKILL.md exists and is well-formed
   - Verify `templates/` subdirectory exists (or create it)
   - Confirm template file format is standard

3. **Update template content:**
   - Write new template to `templates/{name}.template.md` or appropriate format
   - Preserve template structure and comments
   - Document change with reason in SKILL.md if needed

4. **Validate template integrity:**
   - Parse YAML/JSON if applicable
   - Ensure no syntax errors introduced
   - Verify template still matches skill description

5. **Return results:**
   - Path to updated template
   - Content of updated template
   - List of affected consumer repos (for audit re-run)

---

## Template Locations

### Config Skills

```
plugins/metasaver-core/skills/config/{category}/{skill-name}/
├── SKILL.md
└── templates/
    ├── {config-type}.template.md
    ├── {config-type}.example.json
    └── ...
```

Example: `skills/config/code-quality/eslint-config/templates/eslintrc.template.js`

### Domain Skills

```
plugins/metasaver-core/skills/domain/{skill-name}/
├── SKILL.md
├── TEMPLATES.md
├── templates/
│   ├── {type}.template.ts
│   ├── {type}.template.md
│   └── ...
└── reference.md
```

Example: `skills/domain/react-app-structure/templates/component.template.tsx`

---

## Update Workflow

| Step | Action                                   | Output                                 |
| ---- | ---------------------------------------- | -------------------------------------- |
| 1    | Locate template in metasaver-marketplace | Template path                          |
| 2    | Read current template and SKILL.md       | Current content, skill structure       |
| 3    | Apply updates to template file           | Updated template content               |
| 4    | Validate syntax and structure            | Validation result (pass/fail)          |
| 5    | Document change reason (optional)        | Updated SKILL.md or changelog          |
| 6    | Return results for use in remediation    | Template path, content, affected repos |

---

## Standard Template Formats

### ESLint Config

```javascript
// templates/eslintrc.template.js
module.exports = {
  extends: ["@metasaver/eslint-config"],
  parserOptions: {
    ecmaVersion: 2021,
    sourceType: "module",
  },
  rules: {
    // Custom rules here
  },
};
```

### Prettier Config

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

### TypeScript Config

```json
{
  "extends": "@metasaver/tsconfig/base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

---

## Key Rules

**Template-First Updates**

- ALWAYS update source template in metasaver-marketplace first
- ALWAYS update template before applying config fixes to consumer repos
- Template is the single source of truth

**No Hardcoding**

- Keep templates abstract and reusable
- Use comments to explain customization points
- Reference SKILL.md for context

**Consumer Impact**

- Track which repos use this template
- Recommend re-audit after major template changes
- Document breaking changes clearly

---

## Integration

**Called by:** `/audit` command (remediation-options phase)

**Calls:** None (reads/writes to marketplace templates)

**Next step:** Remediation options workflow with updated template available

**Related skills:**

- `remediation-options` - Uses updated template for conform-to-template option
- `audit-workflow` - Orchestrates audit including template updates

---

## Example: ESLint Config Update

```
Input:
  template_type: "eslint"
  new_content: {extends: "@metasaver/eslint-config", rules: {...}}
  reason: "Add rules-of-hooks for React compliance"

Process:
  1. Locate: plugins/metasaver-core/skills/config/code-quality/eslint-config/
  2. Update: templates/eslintrc.template.js
  3. Validate: Parse syntax, check extends path exists
  4. Document: Add comment about rules-of-hooks in template
  5. Return:
     - template_path: ".../eslint-config/templates/eslintrc.template.js"
     - template_content: Updated ESLint config
     - affected_repos: ["repo1", "repo2", "repo3"]
     - recommendation: "Re-audit ESLint in 3 consumer repos"

Output:
  Updated template ready for use in remediation-options
  (Option 1: Conform to template will now use this updated version)
```

---

## Error Handling

**Template not found:**

- Check skill directory structure
- Verify skill name matches template type
- Create templates/ subdirectory if missing

**Validation fails:**

- Provide clear error message on what failed
- Return to user for manual review before applying
- ALWAYS validate templates before writing to marketplace

**Affected repos unclear:**

- Search marketplace.json for skills that reference this config type
- Check recent commits for related config changes
- Document uncertainty in output
