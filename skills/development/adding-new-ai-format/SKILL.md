---
name: adding-new-ai-format
description: Step-by-step guide for adding support for a new AI editor format to PRPM - covers types, converters, schemas, CLI, webapp, and testing
---

# Adding a New AI Format to PRPM

Complete process for adding support for a new AI editor format (like OpenCode, Cursor, Claude, etc.) to PRPM.

## Overview

This skill documents the systematic process for adding a new AI format to PRPM, based on the OpenCode integration. Follow these steps in order to ensure complete integration across all packages.

## Prerequisites

- Format documentation (understand file structure, frontmatter, directory conventions)
- Example files from the format
- Understanding of format-specific features (tools, agents, commands, etc.)

## Step 1: Types Package (`packages/types/`)

**File**: `src/package.ts`

Add the format to the Format type and FORMATS array:

```typescript
export type Format =
  | 'cursor'
  | 'claude'
  | 'continue'
  | 'windsurf'
  | 'copilot'
  | 'kiro'
  | 'agents.md'
  | 'gemini.md'
  | 'claude.md'
  | 'gemini'
  | 'opencode'  // Add new format here
  | 'ruler'
  | 'generic'
  | 'mcp';

export const FORMATS: readonly Format[] = [
  'cursor',
  'claude',
  // ... other formats
  'opencode',  // Add here too
  'ruler',
  'generic',
  'mcp',
] as const;
```

**Build and verify**:
```bash
npm run build --workspace=@pr-pm/types
```

## Step 2: Converters Package - Schema (`packages/converters/schemas/`)

Create JSON schema file: `{format}.schema.json`

Example structure:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://registry.prpm.dev/api/v1/schemas/opencode.json",
  "title": "OpenCode Agent Format",
  "description": "JSON Schema for OpenCode Agents",
  "type": "object",
  "required": ["frontmatter", "content"],
  "properties": {
    "frontmatter": {
      "type": "object",
      "required": ["description"],
      "properties": {
        "description": { "type": "string" },
        // Format-specific fields
      },
      "additionalProperties": false
    },
    "content": {
      "type": "string",
      "description": "Body content as markdown"
    }
  }
}
```

**CRITICAL Schema Requirements:**
- `$id` must use new URL pattern: `https://registry.prpm.dev/api/v1/schemas/{format}.json` for base schemas
- For subtypes: `https://registry.prpm.dev/api/v1/schemas/{format}/{subtype}.json`
- Add `"additionalProperties": false` to frontmatter object to catch invalid fields
- String fields requiring slugs (like `name`) should use pattern: `"pattern": "^[a-z0-9-]+$"`

If the format has subtypes (like Claude with agents/skills/commands), create separate schema files:
- `{format}-agent.schema.json`
- `{format}-skill.schema.json`
- `{format}-slash-command.schema.json`
- etc.

**IMPORTANT**: When creating subtype schemas, you MUST update the validation logic to map them.

## Step 3: Converters Package - Format Documentation (`packages/converters/docs/`)

**CRITICAL**: Create comprehensive format documentation file: `{format}.md`

This documentation serves as the source of truth for:
- Package authors creating packages in this format
- PRPM contributors implementing converters
- Users understanding format capabilities and limitations

**Required sections**:

```markdown
# {Format Name} Format Specification

**File Locations:**
- {Type 1}: `{path}`
- {Type 2}: `{path}`

**Format:** {Markdown/JSON/etc.} with {YAML frontmatter/etc.}
**Official Docs:** {link to official documentation}

## Overview

Brief description of the format and its purpose.

## Frontmatter Fields

### Required Fields

- **`field-name`** (type): Description

### Optional Fields

- **`field-name`** (type): Description

## Content Format

Describe the body/content structure.

## Best Practices

1. Practice 1
2. Practice 2

## Conversion Notes

### From {Format} to Canonical

How the converter parses this format.

### From Canonical to {Format}

How the converter generates this format.

## Limitations

- Limitation 1
- Limitation 2

## Examples

### Example 1

```markdown
{example content}
```

## Related Documentation

- [Official Docs]({url})
- [PRPM Format Guide](../../docs/formats.mdx)

## Changelog

- **{Date}**: Initial format support
```

**Add to README.md**:

1. **Format Matrix table**: Add row(s) with subtypes, official docs, and OpenCode docs links
2. **Available Formats table**: Add row with link to your new `.md` file
3. **Schema Validation section**: Add schema filename(s) to appropriate list
4. **Frontmatter Support table**: Add row with frontmatter requirements
5. **File Organization table**: Add row with file paths and structure

See `packages/converters/docs/README.md` for examples of how other formats are documented.

## Step 4: Converters Package - Canonical Types

**File**: `packages/converters/src/types/canonical.ts`

### 3a. Add format to CanonicalPackage.format union:

```typescript
format: 'cursor' | 'claude' | ... | 'opencode' | 'ruler' | 'generic' | 'mcp';
```

### 3b. Add format-specific metadata (if needed):

```typescript
// In CanonicalPackage.metadata
metadata?: {
  // ... existing configs
  opencode?: {
    mode?: 'subagent' | 'primary' | 'all';
    model?: string;
    temperature?: number;
    permission?: Record<string, any>;
    disable?: boolean;
  };
};
```

### 3c. Add to MetadataSection.data (if storing format-specific data):

```typescript
export interface MetadataSection {
  type: 'metadata';
  data: {
    title: string;
    description: string;
    // ... existing fields
    opencode?: {
      // Same structure as above
    };
  };
}
```

### 3d. Add to formatScores and sourceFormat:

```typescript
formatScores?: {
  cursor?: number;
  // ... others
  opencode?: number;
};

sourceFormat?: 'cursor' | 'claude' | ... | 'opencode' | ... | 'generic';
```

## Step 5: Converters Package - From Converter

**File**: `packages/converters/src/from-{format}.ts`

Create converter that parses format → canonical:

```typescript
import type {
  CanonicalPackage,
  PackageMetadata,
  Section,
  MetadataSection,
  ToolsSection,
} from './types/canonical.js';
import { setTaxonomy } from './taxonomy-utils.js';
import yaml from 'js-yaml';  // If using YAML frontmatter

// Define format-specific interfaces
interface FormatFrontmatter {
  // Format-specific frontmatter structure
}

// Parse frontmatter if needed
function parseFrontmatter(content: string): {
  frontmatter: Record<string, any>;
  body: string
} {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) {
    return { frontmatter: {}, body: content };
  }

  const frontmatter = yaml.load(match[1]) as Record<string, any>;
  const body = match[2];

  return { frontmatter, body };
}

export function fromFormat(
  content: string,
  metadata: Partial<PackageMetadata> & Pick<PackageMetadata, 'id' | 'name' | 'version' | 'author'>
): CanonicalPackage {
  const { frontmatter, body } = parseFrontmatter(content);
  const fm = frontmatter as FormatFrontmatter;

  const sections: Section[] = [];

  // 1. Create metadata section
  const metadataSection: MetadataSection = {
    type: 'metadata',
    data: {
      title: metadata.name || metadata.id,
      description: fm.description || metadata.description || '',
      version: metadata.version || '1.0.0',
      author: metadata.author,
    },
  };

  // Store format-specific data for roundtrip
  if (/* has format-specific fields */) {
    metadataSection.data.formatName = {
      // Format-specific data
    };
  }

  sections.push(metadataSection);

  // 2. Extract tools (if applicable)
  if (fm.tools) {
    const enabledTools = Object.entries(fm.tools)
      .filter(([_, enabled]) => enabled === true)
      .map(([tool, _]) => {
        // Normalize tool names to canonical format
        return normalizeToolName(tool);
      });

    if (enabledTools.length > 0) {
      sections.push({
        type: 'tools',
        tools: enabledTools,
      });
    }
  }

  // 3. Add body as instructions
  if (body.trim()) {
    sections.push({
      type: 'instructions',
      title: 'Instructions',
      content: body.trim(),
    });
  }

  // 4. Build canonical package
  const canonicalContent: CanonicalPackage['content'] = {
    format: 'canonical',
    version: '1.0',
    sections
  };

  const pkg: CanonicalPackage = {
    ...metadata,
    id: metadata.id,
    name: metadata.name || metadata.id,
    version: metadata.version,
    author: metadata.author,
    description: metadata.description || fm.description || '',
    tags: metadata.tags || [],
    format: 'formatname',
    subtype: 'agent', // Or detect from content
    content: canonicalContent,
  };

  setTaxonomy(pkg, 'formatname', 'agent');
  return pkg;
}
```

**Key points**:
- Import yaml if format uses YAML frontmatter
- Extract all format-specific metadata for roundtrip conversion
- Normalize tool names to canonical format (Write, Edit, Bash, etc.)
- Always include `format: 'canonical'` and `version: '1.0'` in content
- InstructionsSection requires `title` field
- Call `setTaxonomy()` before returning

## Step 6: Converters Package - To Converter

**File**: `packages/converters/src/to-{format}.ts`

Create converter that converts canonical → format:

```typescript
import type {
  CanonicalPackage,
  ConversionResult,
} from './types/canonical.js';
import yaml from 'js-yaml';

export function toFormat(pkg: CanonicalPackage): ConversionResult {
  const warnings: string[] = [];
  let qualityScore = 100;

  try {
    const content = convertContent(pkg, warnings);

    const lossyConversion = warnings.some(w =>
      w.includes('not supported') || w.includes('skipped')
    );

    if (lossyConversion) {
      qualityScore -= 10;
    }

    return {
      content,
      format: 'formatname',
      warnings: warnings.length > 0 ? warnings : undefined,
      lossyConversion,
      qualityScore,
    };
  } catch (error) {
    warnings.push(`Conversion error: ${error instanceof Error ? error.message : String(error)}`);
    return {
      content: '',
      format: 'formatname',
      warnings,
      lossyConversion: true,
      qualityScore: 0,
    };
  }
}

function convertContent(pkg: CanonicalPackage, warnings: string[]): string {
  const lines: string[] = [];

  // Extract sections
  const metadata = pkg.content.sections.find(s => s.type === 'metadata');
  const tools = pkg.content.sections.find(s => s.type === 'tools');
  const instructions = pkg.content.sections.find(s => s.type === 'instructions');

  // Build frontmatter
  const frontmatter: Record<string, any> = {};

  if (metadata?.type === 'metadata') {
    frontmatter.description = metadata.data.description;
  }

  // Restore format-specific metadata (for roundtrip)
  const formatData = metadata?.type === 'metadata' ? metadata.data.formatName : undefined;
  if (formatData) {
    Object.assign(frontmatter, formatData);
  }

  // Convert tools
  if (tools?.type === 'tools' && tools.tools.length > 0) {
    frontmatter.tools = convertToolsToFormatStructure(tools.tools);
  }

  // Generate YAML frontmatter (if applicable)
  lines.push('---');
  lines.push(yaml.dump(frontmatter, { indent: 2, lineWidth: -1 }).trim());
  lines.push('---');
  lines.push('');

  // Add body content
  if (instructions?.type === 'instructions') {
    lines.push(instructions.content);
  }

  return lines.join('\n').trim() + '\n';
}
```

**Section type handling**:
- **PersonaSection**: `section.data.role` (NOT `section.content`)
- **RulesSection**: `section.items` (NOT `section.rules`), each item has `rule.content`
- **InstructionsSection**: `section.content` and `section.title`
- **ExamplesSection**: `section.examples` array with `description` and `code`

## Step 7: Converters Package - Exports and Validation

**File**: `packages/converters/src/index.ts`

Add to exports:
```typescript
// From converters
export { fromFormat } from './from-format.js';

// To converters
export { toFormat } from './to-format.js';
```

**File**: `packages/converters/src/validation.ts`

### 7a. Add to FormatType:
```typescript
export type FormatType =
  | 'cursor'
  | 'claude'
  // ... others
  | 'opencode'
  | 'canonical';
```

### 7b. Add to base schema map:
```typescript
const schemaMap: Record<FormatType, string> = {
  'cursor': 'cursor.schema.json',
  // ... others
  'opencode': 'opencode.schema.json',
  'canonical': 'canonical.schema.json',
};
```

### 7c. **CRITICAL**: Add subtype schemas to subtypeSchemaMap:
```typescript
const subtypeSchemaMap: Record<string, string> = {
  'claude:agent': 'claude-agent.schema.json',
  'claude:skill': 'claude-skill.schema.json',
  'claude:slash-command': 'claude-slash-command.schema.json',
  'claude:hook': 'claude-hook.schema.json',
  'cursor:slash-command': 'cursor-command.schema.json',
  'kiro:hook': 'kiro-hooks.schema.json',
  'kiro:agent': 'kiro-agent.schema.json',
  'droid:skill': 'droid-skill.schema.json',
  'droid:slash-command': 'droid-slash-command.schema.json',
  'droid:hook': 'droid-hook.schema.json',
  'opencode:slash-command': 'opencode-slash-command.schema.json',  // Add your subtypes here
};
```

**Why this matters**: Without adding subtypes to `subtypeSchemaMap`, validation will fall back to the base format schema and won't validate subtype-specific fields. This causes validation to fail or pass incorrectly.

**File**: `packages/converters/src/taxonomy-utils.ts`

Add to Format type:
```typescript
export type Format = 'cursor' | 'claude' | ... | 'opencode' | ... | 'mcp';
```

Add to normalizeFormat:
```typescript
export function normalizeFormat(sourceFormat: string): Format {
  const normalized = sourceFormat.toLowerCase();

  if (normalized.includes('cursor')) return 'cursor';
  // ... others
  if (normalized.includes('opencode')) return 'opencode';

  return 'generic';
}
```

**Build converters**:
```bash
npm run build --workspace=@pr-pm/converters
```

## Step 8: CLI Package - Filesystem

**File**: `packages/cli/src/core/filesystem.ts`

### 7a. Add to getDestinationDir:

```typescript
export function getDestinationDir(format: Format, subtype: Subtype, name?: string): string {
  const packageName = stripAuthorNamespace(name);

  switch (format) {
    // ... existing cases

    case 'opencode':
      // OpenCode supports agents, slash commands, and custom tools
      // Agents: .opencode/agent/*.md
      // Commands: .opencode/command/*.md
      // Tools: .opencode/tool/*.ts or *.js
      if (subtype === 'agent') return '.opencode/agent';
      if (subtype === 'slash-command') return '.opencode/command';
      if (subtype === 'tool') return '.opencode/tool';
      return '.opencode/agent';  // Default

    // ... rest
  }
}
```

### 7b. Add to autoDetectFormat:

```typescript
const formatDirs: Array<{ format: Format; dir: string }> = [
  { format: 'cursor', dir: '.cursor' },
  // ... others
  { format: 'opencode', dir: '.opencode' },
  { format: 'agents.md', dir: '.agents' },
];
```

## Step 9: CLI Package - Format Mappings

**Files**: `packages/cli/src/commands/search.ts` and `packages/cli/src/commands/install.ts`

Add to both files:

### 8a. formatIcons:

```typescript
const formatIcons: Record<Format, string> = {
  'claude': '🤖',
  'cursor': '📋',
  // ... others
  'opencode': '⚡',  // Choose appropriate emoji
  'gemini.md': '✨',  // Don't forget format aliases
  'claude.md': '🤖',
  'ruler': '📏',
  'generic': '📦',
};
```

### 8b. formatLabels:

```typescript
const formatLabels: Record<Format, string> = {
  'claude': 'Claude',
  'cursor': 'Cursor',
  // ... others
  'opencode': 'OpenCode',
  'gemini.md': 'Gemini',  // Format aliases
  'claude.md': 'Claude',
  'ruler': 'Ruler',
  'generic': '',
};
```

## Step 10: Webapp - Format Subtypes and Filter Dropdown

**File**: `packages/webapp/src/app/(app)/search/SearchClient.tsx`

### 9a. Add to FORMAT_SUBTYPES:

```typescript
const FORMAT_SUBTYPES: Record<Format, Subtype[]> = {
  'cursor': ['rule', 'agent', 'slash-command', 'tool'],
  'claude': ['skill', 'agent', 'slash-command', 'tool', 'hook'],
  'claude.md': ['agent'],  // Format aliases
  'gemini.md': ['slash-command'],
  // ... others
  'opencode': ['agent', 'slash-command', 'tool'],  // List all supported subtypes
  'ruler': ['rule', 'agent', 'tool'],
  'generic': ['rule', 'agent', 'skill', 'slash-command', 'tool', 'chatmode', 'hook'],
};
```

### 9b. Add to format filter dropdown (around line 1195):

```typescript
<select
  value={selectedFormat}
  onChange={(e) => setSelectedFormat(e.target.value as Format | '')}
  className="w-full px-3 py-2 bg-prpm-dark border border-prpm-border rounded text-white focus:outline-none focus:border-prpm-accent"
>
  <option value="">All Formats</option>
  <option value="cursor">Cursor</option>
  <option value="claude">Claude</option>
  <option value="continue">Continue</option>
  <option value="windsurf">Windsurf</option>
  <option value="copilot">GitHub Copilot</option>
  <option value="kiro">Kiro</option>
  <option value="gemini">Gemini CLI</option>
  <option value="droid">Droid</option>
  <option value="opencode">OpenCode</option>  {/* Add your format here */}
  <option value="mcp">MCP</option>
  <option value="agents.md">Agents.md</option>
  <option value="generic">Generic</option>
</select>
```

### 9c. Add compatibility info section (after the dropdown):

```typescript
{selectedFormat === 'opencode' && (
  <div className="mt-3 p-3 bg-gray-500/10 border border-gray-500/30 rounded-lg">
    <p className="text-xs text-gray-400">
      Tool-specific format for <strong>OpenCode AI</strong>
    </p>
  </div>
)}
```

## Step 11: Registry - Fastify Route Schemas

**CRITICAL**: Add the format to all Fastify route validation schemas to prevent 400 errors.

### 10a. **File**: `packages/registry/src/routes/download.ts`

Add to format enum in schema (2-3 places):

```typescript
// Download route schema (line ~46)
format: {
  type: 'string',
  enum: ['cursor', 'claude', 'continue', 'windsurf', 'copilot', 'kiro', 'ruler', 'agents.md', 'gemini', 'droid', 'opencode', 'generic'],
  description: 'Target format for conversion (optional)',
},

// Compatibility check route schema (lines ~201, 205)
from: {
  type: 'string',
  enum: ['cursor', 'claude', 'continue', 'windsurf', 'copilot', 'kiro', 'ruler', 'agents.md', 'gemini', 'droid', 'opencode', 'generic'],
},
to: {
  type: 'string',
  enum: ['cursor', 'claude', 'continue', 'windsurf', 'copilot', 'kiro', 'ruler', 'agents.md', 'gemini', 'droid', 'opencode', 'generic'],
},
```

### 10b. **File**: `packages/registry/src/routes/search.ts`

Add to FORMAT_ENUM constant (line ~12):

```typescript
const FORMAT_ENUM = ['cursor', 'claude', 'continue', 'windsurf', 'copilot', 'kiro', 'agents.md', 'gemini', 'ruler', 'droid', 'opencode', 'generic', 'mcp'] as const;
```

### 10c. **File**: `packages/registry/src/routes/analytics.ts`

Add to both Zod schema and Fastify schema:

```typescript
// Zod schema (line ~15)
const TrackDownloadSchema = z.object({
  packageId: z.string(),
  version: z.string().optional(),
  format: z.enum(['cursor', 'claude', 'continue', 'windsurf', 'copilot', 'kiro', 'agents.md', 'gemini', 'ruler', 'droid', 'opencode', 'generic', 'mcp']).optional(),
  client: z.enum(['cli', 'web', 'api']).optional(),
});

// Fastify schema (line ~45)
format: {
  type: 'string',
  enum: ['cursor', 'claude', 'continue', 'windsurf', 'copilot', 'kiro', 'agents.md', 'gemini', 'ruler', 'droid', 'opencode', 'generic', 'mcp'],
  description: 'Download format'
},
```

**Why this matters**: Without these additions, the registry will reject API requests with 400 validation errors when users try to download or filter by the new format.

## Step 12: Testing and Validation

### 11a. Build types package first:
```bash
npm run build --workspace=@pr-pm/types
```

This is critical because other packages depend on the updated Format type.

### 11b. Build registry and webapp:
```bash
npm run build --workspace=@pr-pm/registry
npm run build --workspace=@pr-pm/webapp
```

### 11c. Run typecheck:
```bash
npm run typecheck
```

Fix any TypeScript errors:
- Missing format in type unions
- Format aliases ('gemini.md', 'claude.md')
- Section structure (use correct field names)

### 11d. Build all packages:
```bash
npm run build
```

### 11e. Run converter tests:
```bash
npm test --workspace=@pr-pm/converters
```

### 11f. Create test fixtures (recommended):
```typescript
// packages/converters/src/__tests__/to-opencode.test.ts
import { describe, it, expect } from 'vitest';
import { toOpencode } from '../to-opencode.js';
import { validateMarkdown } from '../validation.js';
import type { CanonicalPackage } from '../types/canonical.js';

describe('OpenCode Format', () => {
  it('should convert from OpenCode to canonical', () => {
    const opencodeContent = `---
description: Test agent
mode: subagent
---
Test instructions`;

    const result = fromOpencode(opencodeContent, {
      id: 'test',
      name: 'test',
      version: '1.0.0',
      author: 'test',
    });

    expect(result.format).toBe('opencode');
    expect(result.subtype).toBe('agent');
  });

  it('should convert canonical to OpenCode', () => {
    const canonical: CanonicalPackage = {
      // ... build test package
    };

    const result = toOpencode(canonical);
    expect(result.format).toBe('opencode');
    expect(result.content).toContain('---');
  });

  // CRITICAL: Add schema validation tests!
  describe('JSON Schema Validation', () => {
    it('should generate schema-compliant agent output', () => {
      const agentPackage: CanonicalPackage = {
        // ... build agent test package with subtype: 'agent'
      };

      const result = toOpencode(agentPackage);
      const validation = validateMarkdown('opencode', result.content, 'agent');

      if (!validation.valid) {
        console.error('Validation errors:', validation.errors);
      }

      expect(validation.valid).toBe(true);
      expect(validation.errors).toHaveLength(0);
    });
  });
});
```

**Why Schema Validation Tests Matter:**
- Catch mismatches between converter implementation and schema
- Ensure converters generate compliant output
- Reveal missing required fields or incorrect field names
- Example: We discovered Claude agent schema was missing required `mode` field via validation tests

## Step 13: Additional Documentation

Beyond the format documentation created in Step 3:
- **User-facing**: Add to Mintlify docs if the format needs special installation instructions
- **Internal**: Add notes to `docs/development/` if there are special considerations
- **Decision logs**: Document any architectural decisions in `docs/decisions/`

## Common Pitfalls

### 1. Missing Format Aliases
Formats like 'gemini.md' and 'claude.md' are aliases that MUST be included in all format mappings.

### 2. Incorrect Section Structure
- PersonaSection uses `data.role`, not `content`
- RulesSection uses `items`, not `rules`
- InstructionsSection requires `title` field
- Each Rule has `content`, not `description`

### 3. CanonicalContent Requirements
Must always include:
```typescript
{
  format: 'canonical',
  version: '1.0',
  sections: [...]
}
```

### 4. setTaxonomy Signature
```typescript
setTaxonomy(pkg, 'formatname', 'subtype');  // Returns void
return pkg;  // Return the package separately
```

### 5. Tool Name Normalization
Map format-specific tool names to canonical:
- `write` → `Write`
- `edit` → `Edit`
- `bash` → `Bash`

### 6. YAML Import
If using YAML frontmatter:
```typescript
import yaml from 'js-yaml';  // Top-level import
// NOT: const yaml = await import('js-yaml');
```

## Checklist

Before submitting:

**Types Package:**
- [ ] Added format to types/src/package.ts (Format type and FORMATS array)
- [ ] Built types package

**Converters Package:**
- [ ] Created schema file(s) in converters/schemas/
- [ ] If format has subtypes, created separate schema files for each subtype (e.g., {format}-agent.schema.json, {format}-slash-command.schema.json)
- [ ] Created format documentation in converters/docs/{format}.md
- [ ] Updated converters/docs/README.md (Format Matrix, Available Formats, Schema Validation, Frontmatter Support, File Organization tables)
- [ ] Updated converters/src/types/canonical.ts (all 4 places: format union, metadata, MetadataSection.data, formatScores, sourceFormat)
- [ ] Created from-{format}.ts converter
- [ ] Created to-{format}.ts converter
- [ ] Updated converters/src/index.ts exports
- [ ] Updated converters/src/validation.ts (FormatType, schemaMap, and **CRITICAL**: subtypeSchemaMap for each subtype)
- [ ] Updated converters/src/taxonomy-utils.ts (Format type and normalizeFormat)
- [ ] Copied all schemas to packages/cli/dist/schemas/ for runtime use

**CLI Package:**
- [ ] Updated cli/src/core/filesystem.ts (getDestinationDir and autoDetectFormat)
- [ ] Updated cli/src/commands/search.ts (formatIcons and formatLabels, including aliases)
- [ ] Updated cli/src/commands/install.ts (formatIcons and formatLabels, including aliases)

**Webapp Package:**
- [ ] Updated webapp SearchClient.tsx (FORMAT_SUBTYPES, including aliases)
- [ ] Added to format filter dropdown
- [ ] Added compatibility info section

**Registry Package:**
- [ ] Updated registry/src/routes/download.ts (format enum in 2-3 places)
- [ ] Updated registry/src/routes/search.ts (FORMAT_ENUM constant)
- [ ] Updated registry/src/routes/analytics.ts (Zod schema and Fastify schema)
- [ ] Built registry package

**Testing:**
- [ ] Ran typecheck successfully
- [ ] Built all packages successfully
- [ ] Wrote tests for converters
- [ ] Documented the integration

## Example: OpenCode Integration

See the following files for reference:
- `packages/converters/src/from-opencode.ts`
- `packages/converters/src/to-opencode.ts`
- `packages/converters/schemas/opencode.schema.json`
- Git commit history for the OpenCode integration PR

## Summary

Adding a new format requires changes across 6 packages:
1. **types** - Add to Format type (build first!)
2. **converters** - Schema, from/to converters, canonical types, validation, taxonomy
3. **cli** - Filesystem and format mappings
4. **webapp** - Format subtypes, filter dropdown, compatibility info
5. **registry** - Fastify route schemas (download, search, analytics)
6. **tests** - Verify everything works

**Build order matters**: types → converters → cli → webapp → registry

Follow the steps systematically, use existing format implementations as reference, and always run typecheck and tests before submitting.
