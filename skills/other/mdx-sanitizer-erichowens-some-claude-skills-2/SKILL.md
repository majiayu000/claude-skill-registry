---
name: mdx-sanitizer
description: Comprehensive MDX content sanitizer that escapes angle brackets, generics, and other JSX-conflicting patterns to prevent build failures
version: "1.0.0"
category: DevOps & Automation
tags:
  - mdx
  - docusaurus
  - markdown
  - build-tools
  - sanitization
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
triggers:
  - "mdx error"
  - "angle bracket"
  - "jsx parsing"
  - "build failure mdx"
  - "escape angle brackets"
  - "sanitize markdown"
---

# MDX Sanitizer

Comprehensive MDX content sanitizer that prevents JSX parsing errors caused by angle brackets, generics, and other conflicting patterns.

## The Problem

MDX 2.x treats unescaped `<` and `{` as JSX syntax. This causes build failures when content contains:

- **TypeScript generics**: `Promise&lt;T&gt;`, `Array&lt;string&gt;`, `Map&lt;K, V&gt;`
- **Comparisons**: `&lt;100ms`, `&lt;=`, `&gt;=`
- **Arrows**: `--&gt;`, `&lt;--`, `-&gt;`
- **Invalid tags**: `&lt;link&gt;` in prose, `&lt;tag&gt;` placeholders
- **Empty brackets**: `&lt;&gt;`

## Solution Architecture

This skill implements a three-layer defense:

### 1. Sync-Time Sanitization (Proactive)
Content is sanitized when syncing from `.claude/skills/` to `website/docs/`:
- `syncSkillDocs.ts` - Main skill files
- `syncSkillSubpages.ts` - Reference files
- `doc-generator.ts` - Generated docs

### 2. Pre-Commit Validation (Reactive)
The git pre-commit hook validates files before commit using `validate-brackets.js`.

### 3. Build-Time Validation (Final Check)
`npm run validate:all` runs as part of `prebuild` to catch any issues.

## Usage

### Check for Issues (Dry Run)
```bash
cd website
npm run sanitize:mdx
# or with verbose output
npm run sanitize:mdx -- --verbose
```

### Fix All Issues
```bash
cd website
npm run sanitize:mdx -- --fix
# or shorthand
npm run fix:mdx
```

### Programmatic API
```typescript
import { sanitizeForMdx, validateMdxSafety, isMdxSafe } from './lib/mdx-sanitizer';

// Sanitize content
const result = sanitizeForMdx(content, { useHtmlEntities: true });
if (result.modified) {
  console.log(`Fixed ${result.issues.length} issues`);
  fs.writeFileSync(path, result.content);
}

// Validate without modifying
const issues = validateMdxSafety(content, 'path/to/file.md');

// Quick check
if (!isMdxSafe(content)) {
  // Handle issues
}
```

## Escaping Strategies

The sanitizer uses HTML entities for maximum compatibility:

| Pattern | Original | Escaped |
|---------|----------|---------|
| Less-than | `<` | `&lt;` |
| Greater-than | `>` | `&gt;` |
| Generics | `&lt;T&gt;` | `&amp;lt;T&amp;gt;` |
| Comparison | `&lt;=` | `&amp;lt;=` |

Content inside code blocks (`` ``` `` or `` ` ``) is automatically protected and never escaped.

## Files Modified

- `website/scripts/lib/mdx-sanitizer.ts` - Core sanitizer module
- `website/scripts/sanitize-mdx.ts` - CLI wrapper
- `website/scripts/syncSkillDocs.ts` - Integration
- `website/scripts/syncSkillSubpages.ts` - Integration
- `website/scripts/lib/doc-generator.ts` - Integration
- `website/package.json` - npm scripts

## Patterns Detected

1. **Less-than before digit**: `&lt;100`, `&lt;0.5ms`
2. **Comparison operators**: `&lt;=`, `&gt;=`
3. **Empty brackets**: `&lt;&gt;`
4. **Arrows**: `&lt;--`, `--&gt;`
5. **Generic types**: `Promise&lt;T&gt;`, `Array&lt;string&gt;`
6. **Space after less-than**: `&lt; value`
7. **Invalid pseudo-tags**: `&lt;link&gt;`, `&lt;tag&gt;` (not valid HTML)

## Troubleshooting

### Build Still Fails After Running Sanitizer

1. Clear Docusaurus cache: `npm run clear`
2. Re-run sanitizer: `npm run sanitize:mdx -- --fix`
3. Rebuild: `npm run build`

### False Positives

If valid JSX components are being escaped:
- Ensure they use PascalCase (e.g., `&lt;MyComponent&gt;`)
- Check they're valid HTML5 elements

### Manual Escaping

For edge cases, manually escape in source:
- Use backticks for inline code: `` `&lt;T&gt;` ``
- Use fenced code blocks for multi-line
- Use HTML entities: `&lt;` and `&gt;`

## Sources

- [MDX Troubleshooting](https://mdxjs.com/docs/troubleshooting-mdx/)
- [TypeDoc MDX Issues](https://github.com/tgreyuk/typedoc-plugin-markdown/issues/167)
