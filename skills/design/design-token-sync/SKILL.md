---
name: Bidirectional Design Token Sync
description: Use this skill when users mention "sync design tokens", "Figma to code", "design system sync", "token drift", "keep tokens in sync", or want to synchronize design tokens between Figma and codebase bidirectionally with automatic drift detection and conflict resolution.
version: 1.0.0
---

# Bidirectional Design Token Sync

## Overview

Keep design tokens synchronized between Figma and your codebase automatically. Detect drift, resolve conflicts, and maintain a single source of truth for your design system.

**Key Innovation:** Bidirectional sync means changes in Figma OR code propagate automatically with conflict detection and intelligent merging.

## When to Use This Skill

Trigger this skill when the user:
- Mentions "sync tokens with Figma" or "Figma sync"
- Wants to "export tokens from Figma" or "import tokens to Figma"
- Asks about "design token drift" or "out of sync tokens"
- Wants to "update tokens from design" or vice versa
- Mentions Style Dictionary, design tokens, or token management
- Has conflicts between design and code token values

## Core Capabilities

### 1. Figma → Code Sync

**Problem:** Designers update colors/spacing in Figma, developers manually update code

**Solution:** Automatic extraction and sync:
```
Figma Variables/Styles → Parse → Transform → Code Tokens
```

Supports:
- Colors (all formats: hex, rgb, hsl)
- Typography (font-family, size, weight, line-height, letter-spacing)
- Spacing (padding, margin, gap)
- Border radius
- Shadows/elevation
- Gradients

### 2. Code → Figma Sync

**Problem:** Developers add tokens in code, design falls out of sync

**Solution:** Push code changes back to Figma:
```
Code Tokens → Transform → Figma API → Update Variables/Styles
```

### 3. Drift Detection

Automatically detect when design and code tokens diverge:

```bash
$ npm run tokens:check

🔍 Drift detected:

Figma → Code (5 changes):
  ✓ primary-500: #2196F3 → #1976D2 (theme update)
  ✓ spacing-lg: 20px → 24px (increased)
  ⚠️ New token: primary-gradient (add to code)
  ⚠️ New token: shadow-xl (add to code)
  ✓ Renamed: font-body → font-sans (update)

Code → Figma (2 changes):
  ⚠️ success-900 exists in code but not Figma (add)
  ⚠️ border-radius-2xl exists in code but not Figma (add)

Apply changes? [Figma→Code] [Code→Figma] [Both] [Review]
```

### 4. Conflict Resolution

When both sides changed the same token:

```
⚠️ Conflict detected for token: primary-500

Figma:  #1976D2 (updated 2 hours ago by Sarah Designer)
Code:   #2196F3 (updated 1 hour ago by you in commit abc123)

Which version should we keep?
[F]igma value  [C]ode value  [M]erge manually  [S]kip

Recommendation: Code value is newer, use Code (C)
```

## Technical Implementation

### Architecture

```
┌─────────┐         ┌──────────────┐         ┌──────┐
│  Figma  │ ←─────→ │ Style        │ ←─────→ │ Code │
│   API   │         │ Dictionary   │         │Tokens│
└─────────┘         └──────────────┘         └──────┘
     ↓                      ↓                     ↓
  Variables         tokens.json              CSS/JS/TS
   Styles                                  src/tokens/
```

### Components

1. **Figma Plugin** (Optional)
   - Runs inside Figma
   - Extracts variables and styles
   - Can update Figma from external source

2. **Sync CLI** (Core)
   - Command-line tool for sync
   - Connects to Figma API
   - Uses Style Dictionary for transformation

3. **Style Dictionary Config**
   - Transforms tokens to multiple formats
   - CSS variables, SCSS, JS, JSON, iOS, Android

4. **Drift Detector**
   - Compares Figma and code tokens
   - Identifies additions, deletions, changes
   - Tracks change history

### Setup

Use `/sync-design-tokens --setup` to configure:

```bash
Figma Design Token Sync Setup
==============================

1. Figma Configuration
   ? Figma file URL: https://figma.com/file/abc123...
   ? Figma access token: (input hidden)
   ? Token location in Figma: [Local Variables] [Shared Variables]

2. Sync Direction
   ? Sync direction: [Bidirectional] [Figma → Code only] [Code → Figma only]
   ? Auto-sync on file save: [Yes] [No]
   ? Sync on git commit: [Yes] [No]

3. Conflict Resolution
   ? On conflict: [Manual review] [Prefer Figma] [Prefer Code] [Use latest]

4. Output Formats
   ? Generate CSS variables: [Yes]
   ? Generate SCSS variables: [Yes]
   ? Generate TypeScript: [Yes]
   ? Generate JSON: [Yes]

Setting up...
✓ Installed: @figma/rest-api-client
✓ Installed: style-dictionary
✓ Created: tokens/figma-tokens.json (source of truth)
✓ Created: config/style-dictionary.config.js
✓ Created: scripts/sync-tokens.js
✓ Added NPM scripts

Setup complete! Run 'npm run tokens:sync' to sync for the first time.
```

### Workflow

#### Initial Sync (Figma → Code)

```bash
$ npm run tokens:sync

Fetching tokens from Figma...
  ✓ Connected to Figma file: Design System v2
  ✓ Found 127 color variables
  ✓ Found 43 typography styles
  ✓ Found 24 spacing tokens
  ✓ Found 12 shadow styles

Transforming tokens...
  ✓ Generated: src/tokens/colors.css
  ✓ Generated: src/tokens/colors.scss
  ✓ Generated: src/tokens/colors.ts
  ✓ Generated: src/tokens/typography.css
  ✓ Generated: src/tokens/spacing.css

Initial sync complete! 📦
Total tokens: 206
```

#### Regular Sync with Drift

```bash
$ npm run tokens:check

Checking for drift...

Changes detected:
  Figma → Code: 3 changes
  Code → Figma: 1 change

Would you like to review? [Yes] [Apply all] [Cancel]

User: Yes

---

Change 1 of 4: primary-600 color update

Source: Figma
Type: Color modification
Old value: #2196F3
New value: #1976D2
Last updated: 2 hours ago by Sarah Designer
Affected tokens in code: 12 references

Apply this change? [Yes] [No] [Skip all]

User: Yes

✓ Updated src/tokens/colors.css
✓ Updated src/tokens/colors.scss
✓ Updated src/tokens/colors.ts

---

Change 2 of 4: success-900 missing in Figma

Source: Code
Type: New token
Value: #1B5E20
Created: 3 days ago in commit def456
Usage: 5 components

Add to Figma? [Yes] [No] [Skip all]

User: Yes

✓ Created in Figma: success-900
✓ Added to collection: Colors/Success

---

Sync complete! Applied 4 changes.

Summary:
  ✓ Figma → Code: 3 changes applied
  ✓ Code → Figma: 1 change applied
  ✓ No conflicts

Run 'git status' to see updated files.
```

## Figma API Integration

### Authentication

```javascript
// scripts/sync-tokens.js
import { FigmaClient } from '@figma/rest-api-client';

const client = new FigmaClient({
  personalAccessToken: process.env.FIGMA_ACCESS_TOKEN
});

const fileKey = 'abc123...'; // From Figma URL

// Get file variables
const variables = await client.getFileVariables(fileKey);
```

### Extract Variables

```javascript
async function extractTokensFromFigma(fileKey) {
  const file = await client.getFile(fileKey);
  const variables = await client.getFileVariables(fileKey);

  const tokens = {
    color: {},
    typography: {},
    spacing: {},
    shadow: {}
  };

  // Extract color variables
  for (const [id, variable] of Object.entries(variables.variables)) {
    if (variable.resolvedType === 'COLOR') {
      const name = variable.name.toLowerCase().replace(/\s+/g, '-');
      const value = rgbaToHex(variable.valuesByMode.default);

      tokens.color[name] = {
        value,
        type: 'color',
        figmaId: id,
        description: variable.description || ''
      };
    }
  }

  // Extract typography styles
  const styles = await client.getFileStyles(fileKey);

  for (const style of styles.text) {
    const name = style.name.toLowerCase().replace(/\s+/g, '-');

    tokens.typography[name] = {
      fontFamily: style.fontFamily,
      fontSize: style.fontSize,
      fontWeight: style.fontWeight,
      lineHeight: style.lineHeight,
      letterSpacing: style.letterSpacing,
      type: 'typography',
      figmaId: style.id
    };
  }

  return tokens;
}
```

### Push Updates to Figma

```javascript
async function pushTokensToFigma(tokens, fileKey) {
  const updates = [];

  for (const [category, categoryTokens] of Object.entries(tokens)) {
    for (const [name, token] of Object.entries(categoryTokens)) {
      if (!token.figmaId) {
        // New token - create in Figma
        updates.push(createVariable(name, token));
      } else if (token.modified) {
        // Modified token - update in Figma
        updates.push(updateVariable(token.figmaId, token));
      }
    }
  }

  // Batch update
  await client.updateFileVariables(fileKey, { updates });
}

async function createVariable(name, token) {
  return {
    action: 'CREATE',
    name: name,
    resolvedType: token.type === 'color' ? 'COLOR' : 'FLOAT',
    valuesByMode: {
      default: parseTokenValue(token.value, token.type)
    }
  };
}
```

## Style Dictionary Configuration

```javascript
// config/style-dictionary.config.js
export default {
  source: ['tokens/figma-tokens.json'],

  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'src/tokens/',
      files: [{
        destination: 'colors.css',
        format: 'css/variables',
        filter: token => token.type === 'color'
      }]
    },

    scss: {
      transformGroup: 'scss',
      buildPath: 'src/tokens/',
      files: [{
        destination: '_colors.scss',
        format: 'scss/variables',
        filter: token => token.type === 'color'
      }]
    },

    js: {
      transformGroup: 'js',
      buildPath: 'src/tokens/',
      files: [{
        destination: 'colors.ts',
        format: 'javascript/es6',
        filter: token => token.type === 'color'
      }]
    },

    json: {
      buildPath: 'dist/tokens/',
      files: [{
        destination: 'tokens.json',
        format: 'json/flat'
      }]
    }
  }
};
```

## Drift Detection Algorithm

```python
# scripts/detect-drift.py

def detect_drift(figma_tokens, code_tokens):
    """Detect differences between Figma and code tokens"""

    drift = {
        'figma_to_code': [],  # Changes in Figma not in code
        'code_to_figma': [],  # Changes in code not in Figma
        'conflicts': []       # Both changed differently
    }

    all_token_names = set(figma_tokens.keys()) | set(code_tokens.keys())

    for name in all_token_names:
        figma_token = figma_tokens.get(name)
        code_token = code_tokens.get(name)

        if figma_token and not code_token:
            # Token exists in Figma but not code
            drift['figma_to_code'].append({
                'type': 'new',
                'name': name,
                'value': figma_token['value'],
                'action': 'add_to_code'
            })

        elif code_token and not figma_token:
            # Token exists in code but not Figma
            drift['code_to_figma'].append({
                'type': 'new',
                'name': name,
                'value': code_token['value'],
                'action': 'add_to_figma'
            })

        elif figma_token and code_token:
            # Token exists in both - check for changes
            if figma_token['value'] != code_token['value']:
                # Check timestamps to determine which is newer
                figma_time = figma_token.get('lastModified', 0)
                code_time = code_token.get('lastModified', 0)

                if figma_time > code_time:
                    drift['figma_to_code'].append({
                        'type': 'modified',
                        'name': name,
                        'old_value': code_token['value'],
                        'new_value': figma_token['value'],
                        'action': 'update_code'
                    })
                elif code_time > figma_time:
                    drift['code_to_figma'].append({
                        'type': 'modified',
                        'name': name,
                        'old_value': figma_token['value'],
                        'new_value': code_token['value'],
                        'action': 'update_figma'
                    })
                else:
                    # Modified at same time = conflict
                    drift['conflicts'].append({
                        'name': name,
                        'figma_value': figma_token['value'],
                        'code_value': code_token['value'],
                        'action': 'manual_resolution'
                    })

    return drift
```

## Example Usage

### Scenario 1: Designer Updates Color in Figma

```bash
# Designer changes primary-600 in Figma from #2196F3 to #1976D2

$ npm run tokens:sync

Syncing with Figma...

Changes detected:
  ✓ primary-600: #2196F3 → #1976D2 (Figma updated 5 mins ago)

Affected code:
  - src/components/Button.tsx (2 references)
  - src/components/Card.tsx (1 reference)
  - src/theme/colors.css (1 reference)

Apply change? [Yes] [No] [Review impact]

User: Yes

✓ Updated tokens/figma-tokens.json
✓ Regenerated src/tokens/colors.css
✓ Regenerated src/tokens/colors.scss
✓ Regenerated src/tokens/colors.ts

✓ Sync complete!

Next steps:
1. Review changes: git diff
2. Test visual regressions: npm run test:visual
3. Commit changes: git add . && git commit -m "chore: sync design tokens"
```

### Scenario 2: Developer Adds New Token in Code

```bash
# Developer adds success-900 in src/tokens/colors.ts

$ npm run tokens:sync

Syncing with Figma...

New tokens in code:
  ⚠️ success-900: #1B5E20 (not in Figma)

Add to Figma? [Yes] [No]

User: Yes

Creating in Figma...
  ✓ Created variable: success-900
  ✓ Added to collection: Colors/Success
  ✓ Value set to: #1B5E20

✓ Sync complete!

The token is now available in Figma for designers.
```

### Scenario 3: Conflict Resolution

```bash
$ npm run tokens:sync

⚠️ Conflict detected!

Token: spacing-lg
Figma:  24px (updated 2 hours ago by Sarah)
Code:   28px (updated 1 hour ago by you in commit abc123)

Both changed differently. Which should we keep?

[F]igma (24px)
[C]ode (28px)
[M]anual merge
[S]kip for now

Recommendation: Code value is newer (C)

User: C

✓ Keeping code value (28px)
✓ Updating Figma to match code

Conflict resolved!
```

## Best Practices

### 1. Single Source of Truth

Choose one source as primary:
- **Figma-first:** Designers own tokens, code syncs from Figma
- **Code-first:** Developers own tokens, Figma syncs from code
- **Bidirectional:** Both can update, conflicts resolved manually

### 2. Sync Frequency

- **Manual:** Run `npm run tokens:sync` when needed
- **On Save:** Auto-sync when Figma file saved (requires Figma plugin)
- **On Commit:** Pre-commit hook checks for drift
- **CI/CD:** Verify no drift in pull requests

### 3. Version Control

- Commit `tokens/figma-tokens.json` to git
- Commit generated CSS/SCSS/TS files
- Track token changes in changelog
- Tag releases with token versions

### 4. Team Workflow

- **Designers:** Update tokens in Figma, notify developers
- **Developers:** Run sync, review changes, commit
- **Both:** Use PR reviews to discuss token changes

## Troubleshooting

### Authentication Errors

```
❌ Error: Figma authentication failed

Cause: Invalid or expired access token

Fix:
1. Generate new token: https://figma.com/developers
2. Update .env: FIGMA_ACCESS_TOKEN=your_new_token
3. Try again: npm run tokens:sync
```

### Merge Conflicts

```
⚠️ Git merge conflict in tokens/figma-tokens.json

This means someone else updated tokens since your last sync.

Fix:
1. Pull latest changes: git pull origin main
2. Resolve conflicts in tokens/figma-tokens.json
3. Re-run sync: npm run tokens:sync
4. Commit resolved changes
```

### Too Many Changes

```
⚠️ Large number of changes detected (47 tokens modified)

This is unusual. Possible causes:
1. First time syncing
2. Major design system overhaul
3. Token format changed

Review carefully before applying.
```

## Integration with Other Skills

- **visual-regression-testing** - Test token changes visually
- **accessibility-remediation** - Verify color contrast after changes
- **dark-mode-generation** - Sync dark mode tokens
- **storybook-config** - Update Storybook theme tokens

## Files Reference

- `references/figma-api.md` - Figma API documentation
- `references/style-dictionary.md` - Style Dictionary guide
- `examples/sync-workflows.md` - Common sync scenarios
- `scripts/sync-tokens.js` - Main sync script
- `scripts/detect-drift.py` - Drift detection

## Summary

Design Token Sync keeps your design system consistent between Figma and code automatically. Bidirectional sync means changes in either location propagate with conflict detection and resolution.

**Key Benefits:**
- ✅ Automatic sync between Figma and code
- ✅ Drift detection and conflict resolution
- ✅ Multi-format output (CSS, SCSS, TS, JSON)
- ✅ Version controlled token history
- ✅ Team collaboration workflow

**Use this skill to** set up Figma sync, detect token drift, resolve conflicts, and maintain design-code consistency.
