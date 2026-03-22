---
name: adr
description: "Documents architecture decisions with auto-numbering following the ADR pattern. Triggers on keywords: adr, architecture decision, decision record"
project-agnostic: false
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Architecture Decision Record (ADR) Command

Document architecture decisions following the ADR pattern. Auto-generates next ADR number and updates index.

## Arguments

- **Optional**: `<decision_context>` - If provided, document that specific decision
- **No argument**: Infer decision from recent conversation context

## Pre-Flight Checks

1. **Ensure ADR directory exists**:
   - Check for `adrs/` directory in current working directory
   - If missing: Create `adrs/` directory

2. **Ensure index exists**:
   - Check for `adrs/000-index.md`
   - If missing: Create default index template:
     ```markdown
     # Architecture Decision Records (ADR) Index

     > Critical decisions that govern development. **Read before implementing.**

     ## Index

     | # | Decision | Status | Date |
     |---|----------|--------|------|

     ## Usage

     ADRs document significant architectural and policy decisions. Each entry follows format:
     `NNN-<title>.md` where NNN is zero-padded sequence number.

     ### Creating New ADR
     Use `/adr` command or manually:
     1. Create file `adrs/NNN-title.md`
     2. Add entry to this index
     3. Commit: `adr(NNN): <title>`
     ```

3. **Read ADR index**: `adrs/000-index.md`
   - Extract highest existing ADR number
   - Generate next number (NNN format: zero-padded 3 digits)

4. **Validate decision context**:
   - If argument provided: Use that as decision context
   - If no argument: Infer from recent conversation (last 2-3 messages)
   - If unclear: STOP and ask user to clarify decision to document

## Execution

1. **Generate ADR metadata**:
   - Number: Next sequential (e.g., 001, 002, 003)
   - Title: Extract from decision context (kebab-case slug)
   - Date: Current date (YYYY-MM-DD format)
   - Status: "Accepted" (default)

2. **Create ADR file**: `adrs/NNN-<slug>.md`
   ```markdown
   # NNN - <Title>

   **Status**: Accepted
   **Date**: <YYYY-MM-DD>

   ## Context
   <Why this decision was needed - problem statement, constraints, requirements>

   ## Decision
   <What was decided - clear statement of the chosen approach>

   ## Consequences
   <Implications and trade-offs:>
   - **Positive**: <benefits>
   - **Negative**: <costs, limitations>
   - **Neutral**: <other impacts>

   ## References
   <Related docs, specs, links if any>
   ```

3. **Update index**: `adrs/000-index.md`
   - Add new row to table:
     ```
     | NNN | [<Title>](./NNN-<slug>.md) | Accepted | YYYY-MM-DD |
     ```

4. **Commit changes**:
   ```bash
   git add adrs/NNN-<slug>.md adrs/000-index.md && git commit -m "adr(NNN): <title>"
   ```

## Output

Report in markdown format:
- ADR number created
- File path (absolute)
- Title
- Commit status

## Example Usage

```
/adr Use pnpm for package management
```

Creates:
- File: `adrs/001-use-pnpm-for-package-management.md`
- Updates: `adrs/000-index.md`
- Commit: `adr(001): use pnpm for package management`
