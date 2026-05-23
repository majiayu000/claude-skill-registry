---
name: ctx
description: Load PRD, FRD, Tech Spec, or RFC into context
argument-hint: <doc-id|path>
---

# ctx (Context Hydration)

**Category**: Context Management

## Usage

```bash
/ctx <doc-reference>
```

## Arguments

- `<doc-reference>`: Required - Document identifier or path. Accepts:
  - Document IDs: `PRD-001`, `FRD-042`, `TS-0045`, `RFC-0042`
  - Partial names: `user-auth`, `payment-gateway`
  - File paths: `./product-docs/prds/active/user-auth-prd.md`

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

1. **Identify Document Type and Location**

   Search order by ID prefix:
   | Prefix | Type | Search Locations |
   |--------|------|------------------|
   | `PRD-` | Product PRD | `product-docs/prds/` |
   | `FRD-` | Feature PRD | `product-docs/prds/` |
   | `TS-` | Tech Spec | `tech-specs/` |
   | `RFC-` | RFC | `rfcs/` |

   If no prefix, search all locations for partial name match.

2. **Search for Document**

   ```
   # Search patterns by type
   PRD/FRD: product-docs/prds/**/*<query>*.md
   Tech Spec: tech-specs/**/*<query>*.md
   RFC: rfcs/**/*<query>*.md
   ```

3. **Handle Multiple Matches**

   If multiple documents match, display options:
   ```
   Multiple documents match "auth":

   1. PRD-001-user-authentication-prd.md (PRD)
   2. FRD-015-oauth-integration-frd.md (FRD)
   3. TS-0044-auth-implementation.md (Tech Spec)
   4. RFC-0043-auth-redesign.md (RFC)

   Which document to load? [1-4]
   ```

4. **Read and Present Document**

   Read the full document content and present with context header:

   ```
   ═══════════════════════════════════════════════════════════
   📄 CONTEXT LOADED: PRD-001 - User Authentication System
   ═══════════════════════════════════════════════════════════

   Type:     Product PRD
   Status:   ACTIVE
   Version:  1.2
   Location: product-docs/prds/active/PRD-001-user-authentication-prd.md

   Related Documents:
   - Tech Spec: TS-0044-auth-implementation.md
   - Tasks: tasks/PRD-001-tasks.md

   ───────────────────────────────────────────────────────────

   [Full document content here]

   ═══════════════════════════════════════════════════════════
   Context loaded. Ready to work on this document.
   ═══════════════════════════════════════════════════════════
   ```

5. **Extract Related Documents**

   Parse the loaded document for references to other documents:
   - Links to RFCs, Tech Specs, PRDs, FRDs
   - Task file references
   - Dependency references

   Offer to load related documents:
   ```
   💡 Related documents found:
      - RFC-0043 (linked)
      - TS-0044 (implementation spec)

   Load related? [y/N]
   ```

## Loading Multiple Documents

Support loading multiple documents at once:

```bash
# Load multiple by ID
/ctx PRD-001 RFC-0043

# Load all related to a PRD
/ctx PRD-001 --related

# Load PRD with its tech spec and tasks
/ctx PRD-001 --full
```

### Options

| Option | Description |
|--------|-------------|
| `--related` | Also load all related/linked documents |
| `--full` | Load document + tech spec + tasks |
| `--summary` | Show only metadata and overview, not full content |

## Output Modes

### Default (Full Content)
Loads complete document content into context.

### Summary Mode (`--summary`)
```
📄 PRD-001: User Authentication System
   Status: ACTIVE | Version: 1.2 | Progress: 67%

   Overview:
   Implement secure user authentication with OAuth 2.0 support,
   including social login providers and MFA capabilities.

   Key Sections:
   - User Stories (12 items)
   - Technical Requirements (8 items)
   - Success Metrics (5 KPIs)

   Use '/ctx PRD-001' for full content.
```

## Document Type Detection

Infer document type from:

1. **Filename patterns**
   - `*-prd.md` → Product PRD
   - `*-frd.md` → Feature PRD
   - `TS-*` → Tech Spec
   - `RFC-*` → RFC

2. **Directory location**
   - `product-docs/prds/` → PRD/FRD
   - `tech-specs/` → Tech Spec
   - `rfcs/` → RFC

3. **Frontmatter type field**
   ```yaml
   type: product-prd | feature-frd | tech-spec | rfc
   ```

## Error Handling

- **Document not found**: Show search suggestions
  ```
  Document "auth-prd" not found.

  Did you mean:
  - user-authentication-prd.md
  - oauth-auth-frd.md

  Or search all docs: /list-prds, /list-tech-specs, /list-rfcs
  ```

- **Invalid path**: Suggest correct format
- **Empty document**: Warn and show metadata only

## Examples

```bash
# Load by document ID
/ctx PRD-001
/ctx RFC-0043
/ctx TS-0044

# Load by partial name
/ctx user-auth
/ctx payment-gateway

# Load by path
/ctx ./product-docs/prds/active/user-auth-prd.md

# Load with related documents
/ctx PRD-001 --related

# Load full context (PRD + tech spec + tasks)
/ctx PRD-001 --full

# Quick overview only
/ctx PRD-001 --summary

# Load multiple documents
/ctx PRD-001 RFC-0043 TS-0044
```

## Integration Tips

1. **After loading context**: Ready to answer questions, implement tasks, or review the document
2. **Combine with task-focus**: Load context then focus on specific task
3. **Use summary mode**: Quick reference without full context load
4. **Chain with other commands**: `/ctx PRD-001 && /generate-tasks`

## Implementation Notes for Claude Code

1. **Efficient Search**: Use glob patterns, don't read files until match confirmed
2. **Cache Metadata**: Parse frontmatter first for quick filtering
3. **Fuzzy Matching**: Support partial names and common abbreviations
4. **Context Size**: Warn if document is very large (>2000 lines)
5. **Related Discovery**: Parse document content for cross-references
