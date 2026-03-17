---
name: review-contract
description: Review Aztec smart contracts for correctness, security, and best practices. Use proactively after writing or modifying Aztec contracts.
allowed-tools: Read, Grep, Glob, Bash
---

# Aztec Contract Review Skill

Review Noir contracts written for the Aztec Network, focusing on correctness, security, and best practices.

## Usage

```
/review-contract [file-path]
```

**Examples:**

```
/review-contract                              # Review contract in current context
/review-contract contracts/token/src/main.nr  # Review specific file
/review-contract contracts/                   # Review all contracts in directory
```

## Workflow

### Step 1: Identify Contract(s) to Review

**If file path provided:**
- Use the provided path directly
- If directory, find all `main.nr` files within

**If no path (use context):**
- Check if a contract file was recently read or edited in conversation
- If not, search for contracts:

```bash
Glob: **/src/main.nr
```

### Step 2: Sync Aztec Version (if needed)

Ensure MCP server has the correct version for accurate pattern matching:

```
aztec_status()
```

If repos not synced or version mismatch with project's Nargo.toml, run:

```
aztec_sync_repos({ version: "<detected-version>" })
```

### Step 3: Read and Understand the Contract

1. Read the contract file(s)
2. Identify the contract's purpose from code and any comments
3. If purpose is unclear, **ask the user** what the contract is intended to do

### Step 4: Verify Patterns Against Current API

Before flagging issues, verify patterns using the MCP server:

```
aztec_search_code({ query: "<pattern-in-question>", filePattern: "*.nr" })
```

This prevents false positives from outdated knowledge.

### Step 5: Review Against Checklist

#### Contract Structure

- [ ] Proper use of `#[aztec]` attribute on contract module
- [ ] Storage struct defined with `#[storage]` attribute
- [ ] Correct state variable types (PublicMutable, Owned, Map, etc.)
- [ ] Constructor/initializer properly defined with `#[initializer]`
- [ ] Functions have appropriate visibility attributes

#### Function Visibility

| Attribute | Use Case |
|-----------|----------|
| `#[external("private")]` | Executes in PXE, reads/writes private state |
| `#[external("public")]` | Executes on sequencer, visible to everyone |
| `#[external("utility")]` + `unconstrained` | Off-chain reads without proofs |
| `#[view]` | Read-only, doesn't modify state |
| `#[only_self]` | Only callable by the contract itself |
| `#[internal("private")]` | Internal function callable only within the contract (private domain) |
| `#[internal("public")]` | Internal function callable only within the contract (public domain) |
| `#[authorize_once]` | Requires one-time authorization (authwit) to call |
| `#[allow_phase_change]` | Allows function to be called across phase boundaries |

#### Private State (Notes)

- [ ] Notes are properly created with correct owner
- [ ] Only note owners can nullify their notes (critical!)
- [ ] Nullifiers handled correctly to prevent double-spending
- [ ] No iteration over private state (impossible in Aztec)

#### Private <> Public Boundary

- [ ] Enqueued public calls used correctly from private functions
- [ ] No unintended information leakage between domains
- [ ] Understand that private-to-public is one-way in a transaction

#### Access Control

- [ ] Sensitive functions have proper access control
- [ ] `self.msg_sender()` used correctly (returns AztecAddress directly in v4, no `.unwrap()` needed)
- [ ] Admin functions protected appropriately

#### Cross-Contract Calls

- [ ] Interfaces are auto-generated in v4 (no manual `#[aztec(interface)]` needed)
- [ ] Correct handling of return values
- [ ] Privacy implications understood

### Step 6: Flag Issues by Severity

**Critical** - Could cause loss of funds or privacy breaches:
- Privacy leaks (private data exposed in public functions)
- Incorrect note ownership allowing unauthorized spending
- Missing nullifier checks enabling double-spend

**High** - Significant bugs or security concerns:
- Missing access control on sensitive functions
- Incorrect msg_sender handling
- State inconsistencies between private and public

**Medium** - Best practice violations:
- Inefficient patterns
- Missing view annotations
- Unclear function purposes

**Low** - Code style or minor improvements:
- Naming conventions
- Code organization
- Documentation gaps

### Step 7: Provide Recommendations

For each issue:
1. Explain **why** it's a problem
2. Show the **current code**
3. Provide **corrected code**
4. Reference similar patterns from `aztec_search_code` if helpful

## Output Format

```markdown
## Contract Review: [ContractName]

### Summary
Brief overview of the contract's purpose and overall quality.

### Issues Found

#### Critical
- **[Issue Title]**: Description
  - Location: `file:line`
  - Current: `code snippet`
  - Suggested: `fixed code`

#### High
...

#### Medium
...

#### Low
...

### Recommendations
Specific suggestions for improving the contract beyond fixing issues.

### What's Done Well
Highlight good practices observed in the contract.
```

## Interactive Review

During review, you may ask the user clarifying questions:

- "This function transfers notes but has no access control. Is this intentional?"
- "The `sender` field on this note cannot be used for authorization. Did you intend for the sender to be able to modify this note?"
- "This public function exposes the recipient address. Is this privacy tradeoff acceptable for your use case?"

## Common Aztec Pitfalls to Check

1. **Storing addresses on notes for "access control"** - Only the note owner can nullify. Fields are just data.

2. **Trying to iterate over private state** - Notes can't be enumerated. Use different patterns.

3. **Exposing private data in public function parameters** - Once public, always public.

4. **Race conditions between private and public state** - Private reads stale public state.

5. **Using `.unwrap()` on `msg_sender()` in v4** - In v4, `self.msg_sender()` returns `AztecAddress` directly; `.unwrap()` is no longer needed.
