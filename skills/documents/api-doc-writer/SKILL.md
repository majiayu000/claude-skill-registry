---
name: api-doc-writer
description: Creates comprehensive API reference documentation following Diátaxis Reference pattern. Reads source code to verify every method signature, creates structured API docs with zero fabrication tolerance. Use when documenting APIs, packages, or public interfaces.
version: 1.0.0
---

# API Documentation Writer Skill

## Purpose

Create comprehensive, accurate API reference documentation by reading source code and extracting exact method signatures. Follows the Diátaxis Reference pattern for information-oriented documentation with zero tolerance for fabricated methods or incorrect signatures.

## Diátaxis Framework: Reference Documentation

**Reference Type Characteristics:**

- **Information-oriented** - Describes the machinery, not how to use it
- **Technical descriptions** - Facts about APIs, parameters, return types
- **Complete coverage** - Every public method and type documented
- **Structured consistently** - Same format for all entries
- **Exact signatures** - Verified against source code
- **Minimal examples** - Usage demonstrations, not step-by-step tutorials

**What NOT to Include:**

- ❌ Tutorials (learning-oriented) - Use tutorial-writer skill
- ❌ How-To guides (problem-oriented) - Use migration-guide-writer skill
- ❌ Explanations (understanding-oriented) - Link to separate explanation docs
- ❌ Marketing language - Technical descriptions only

## Critical Rules (Zero Tolerance)

### P0 - CRITICAL Violations (Must Fix)

1. **Fabricated Methods** - Methods that don't exist in source code
2. **Wrong Signatures** - Parameter types, names, or order don't match source
3. **Invalid Examples** - Code that won't compile or uses fake imports
4. **Unverified Performance Claims** - Numbers without benchmark evidence

### P1 - HIGH Violations (Should Fix)

5. **Missing Source References** - Not citing which file/method documented
6. **Incomplete Coverage** - Missing public methods
7. **Marketing Language** - Buzzwords instead of technical descriptions

### P2 - MEDIUM Violations

8. **Structural Issues** - Not following template consistently
9. **Redundancy** - Repeating information unnecessarily

## Workflow (Quick Summary)

### Core Steps

1. **Discovery**: Identify language, locate public API surface using grep/glob patterns, create checklist
2. **Extraction**: Read source files, copy EXACT signatures (no paraphrasing), extract comments and error conditions
3. **Documentation**: Use standardized templates (types, functions, constants), follow Diátaxis Reference pattern
4. **Examples**: Write complete, runnable examples with imports and proper error handling
5. **Verification**: Verify signatures match source exactly, check completeness, eliminate marketing language
6. **Organization**: Structure logically (Overview → Types → Functions → Constants → Examples)

**For detailed step-by-step workflow with bash commands, templates, and verification checklists:**

```
Read `~/.claude/skills/api-doc-writer/references/WORKFLOW-STEPS.md`
```

**For API documentation templates (types, functions, constants):**

```
Read `~/.claude/skills/api-doc-writer/references/TEMPLATE-EXAMPLES.md`
```

Use when: Performing API documentation, need specific templates, or understanding each step

---

## Common Pitfalls (Quick Summary)

### Critical Issues to Avoid

1. **Paraphrasing Signatures**: Copy exact signature from source (include receiver types, pointer symbols)
2. **Fabricating Methods**: ONLY document methods that exist in source code (verify first)
3. **Wrong Parameter Types**: Match types exactly (string vs TaskId, pointer vs value)
4. **Missing Error Conditions**: Document specific error conditions from code logic
5. **Non-Runnable Examples**: Include all imports, use correct syntax and real APIs
6. **Line Number References**: Use method names, not line numbers (they change)
7. **Marketing Language**: Use technical descriptions ("provides CRUD operations" not "blazing-fast")

**For detailed pitfall examples with bad/good comparisons:**

```
Read `~/.claude/skills/api-doc-writer/references/PITFALLS.md`
```

Use when: Need concrete examples of common mistakes to avoid

---


## Integration with Other Skills

### Works With:

- **api-documentation-verify** - Verify reference docs for accuracy
- **migration-guide-writer** - Reference docs show new API signatures
- **tutorial-writer** - Tutorials link to reference for detailed API info

### Invokes:

- None (standalone skill, but uses Read tool extensively)

### Invoked By:

- User (manual invocation)
- As part of documentation workflow

## Output Format

**Primary Output**: Markdown file with structured API reference

**File Location**:

- `docs/api/[package-name].md` for package documentation
- `API.md` in project root for main API
- `docs/reference/[module-name].md` for module documentation

**Include at end of document:**

```markdown
---

## Documentation Metadata

**Last Updated**: [Date]
**Source Code Version**: [Commit SHA or version]
**Verification Status**: ✅ All APIs verified against source code
**Source Files**:

- `path/to/file1.go`
- `path/to/file2.go`

## Verification Checklist Completed:

- ✅ All methods verified against source
- ✅ All signatures exactly match
- ✅ All examples use real imports
- ✅ No fabricated methods
- ✅ No marketing language
- ✅ Source references included
```


## Time Estimates

**Small API** (< 10 public methods): 30-45 minutes
**Medium API** (10-30 public methods): 1-2 hours
**Large API** (30+ public methods): 2-4 hours
**Complex API with types** (many types and methods): 4-8 hours

## Example Usage

```bash
# Manual invocation
/skill api-doc-writer

# With specific package
/skill api-doc-writer pkg/services/task

# User request
User: "Document the TaskService API"
Assistant: "I'll use the api-doc-writer skill to create comprehensive API documentation"
```

## Success Criteria

Documentation is complete when:

- ✅ All public APIs discovered and documented
- ✅ All signatures verified against source code
- ✅ All examples use real imports and verified APIs
- ✅ No fabricated methods or wrong signatures
- ✅ Source references included for all entries
- ✅ Error conditions documented from code
- ✅ Verification checklist completed
- ✅ No marketing language or buzzwords
- ✅ Structured consistently using template

## References

- Diátaxis Framework: https://diataxis.fr/reference/
- Technical Documentation Expert Agent
- REFERENCE.md template in this skill directory

---

## Related Agent

For comprehensive documentation guidance that coordinates this and other documentation skills, use the **`documentation-coordinator`** agent.
