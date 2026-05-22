---
name: update-docs
description: Check if code changes require documentation updates and update the /docs knowledge base accordingly.
argument-hint: [file-or-directory]
disable-model-invocation: true
---

Review code changes and update the documentation knowledge base in `/docs` to keep it in sync.

## Scope

If `$ARGUMENTS` is provided, focus on that file or directory. Otherwise, use `git diff --name-only $(git merge-base HEAD main)...HEAD` to get the list of changed files on the current branch.

## Documentation Files

The knowledge base consists of:

| Doc File | Covers |
|----------|--------|
| `docs/ai-sdk.md` | AI SDK patterns, `createChatResponse`, `createTool`, built-in tools, `useChat` |
| `docs/ui-components.md` | shadcn/ui components, `cn()` utility, CVA variants, AI components |
| `docs/mcp-integration.md` | MCP servers, Smithery registry, `createMCPClient`, transport types |
| `docs/skills.md` | Skills system, SKILL.md format, manifest configuration |
| `docs/README.md` | Index and external links |

## Step 1: Identify Changed Files

Get the list of changed files:
```bash
git diff --name-only $(git merge-base HEAD main)...HEAD
```

## Step 2: Map Changes to Documentation

Check if any changed files affect documented areas:

### AI SDK (`docs/ai-sdk.md`)
Watch for changes in:
- `src/lib/chat/index.ts` - Core chat helpers
- `src/lib/chat/tools.ts` - Tool definitions
- `src/lib/chat/skills.ts` - Skill loading
- `src/app/api/chat/*/route.ts` - API routes
- `package.json` - AI SDK version changes

### UI Components (`docs/ui-components.md`)
Watch for changes in:
- `src/components/ui/*.tsx` - New or modified shadcn components
- `src/components/ai-elements/*.tsx` - AI-specific components
- `src/lib/utils.ts` - Utility functions like `cn()`

### MCP Integration (`docs/mcp-integration.md`)
Watch for changes in:
- `src/lib/mcp/index.ts` - Core MCP functions
- `src/lib/mcp/servers.ts` - Server definitions
- `src/lib/actions/integrations.ts` - Smithery integration
- `src/lib/hooks/use-server-search.ts` - Search hook
- `package.json` - MCP package version changes

### Skills System (`docs/skills.md`)
Watch for changes in:
- `src/lib/chat/skills.ts` - Skill loading logic
- `skills/*/SKILL.md` - Skill examples
- `.claude/skills/*/SKILL.md` - Claude Code skills

## Step 3: Analyze Impact

For each affected documentation file, determine:

1. **New additions**: New functions, components, or patterns that should be documented
2. **Changed signatures**: Function parameters, return types, or behavior changes
3. **Removed features**: Deprecated or removed functionality
4. **Version updates**: Package version changes in `package.json`
5. **New documentation needed**: Features that don't fit existing docs and need a new file

### When to Create New Documentation

Create a new doc file in `/docs` when:

- A major new system is added (e.g., authentication, notifications, caching)
- A new integration is added that's complex enough to warrant its own guide
- A new pattern emerges that spans multiple areas of the codebase
- The change would make an existing doc file too long or unfocused

New doc files should:
- Follow the naming pattern: `docs/<topic>.md`
- Be added to `docs/README.md` index
- Include sections: Overview, Package versions (if applicable), Key concepts, Code examples, Key files table

## Step 4: Generate Documentation Updates

For each documentation file that needs updating:

1. Read the current documentation
2. Read the changed source files
3. Identify specific sections that need updates
4. Draft the updated content

For new documentation files:

1. Determine the appropriate filename and scope
2. Create the file structure following the standard template
3. Add entry to `docs/README.md` index
4. Cross-reference from related existing docs

### Update Guidelines

- Keep the same structure and style as existing docs
- Include code examples from actual source files
- Update version numbers when packages change
- Add new sections for new features
- Mark deprecated features clearly
- Keep external links up to date

### New Documentation Template

```markdown
# [Feature Name]

Brief description of what this covers.

## Overview

What this feature/system does and why it exists.

## Package (if applicable)

\`\`\`json
{
  "package-name": "^x.y.z"
}
\`\`\`

## Key Concepts

### [Concept 1]

Explanation with code example.

### [Concept 2]

Explanation with code example.

## Key Files

| File | Purpose |
|------|---------|
| `/src/path/to/file.ts` | Description |

## Related Documentation

- [Related Doc](./related.md) - How it connects
```

## Step 5: Present Findings

Output a report in this format:

```
## Documentation Update Report

### Changed Source Files
- `path/to/file.ts` - [brief description of change]

### New Documentation Needed

#### docs/[new-feature].md (NEW)
- [ ] Create new doc for [feature name]
- [ ] Add to docs/README.md index
- [ ] Cross-reference from [related docs]

### Documentation Updates Needed

#### docs/ai-sdk.md
- [ ] Update `createChatResponse` section - new parameter added
- [ ] Add new tool helper function

#### docs/ui-components.md
- [ ] Add new `Dialog` component documentation
- [ ] Update `Button` variants

#### docs/mcp-integration.md
- [ ] No updates needed

### Package Version Changes
- `ai`: 6.0.48 → 6.1.0
- `@ai-sdk/mcp`: 1.0.13 → 1.0.15

### Recommended Actions
1. [First update to make]
2. [Second update to make]
```

## Step 6: Apply Updates

Ask the user if they want to:
1. Apply all documentation updates automatically
2. Apply specific updates (let them choose)
3. Just report without making changes

When applying updates:
- Edit existing documentation files
- Preserve formatting and structure
- Verify code examples match actual source
- Update version numbers

When creating new documentation:
- Create the new file in `/docs`
- Follow the standard template structure
- Add entry to `docs/README.md` guide table
- Add cross-references in related documentation files

## Integration with PR Workflow

This skill should be run before creating a PR to ensure documentation stays in sync with code changes. It's referenced in `CLAUDE.md` as part of the PR readiness workflow.
