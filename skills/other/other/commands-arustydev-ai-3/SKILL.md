---
description: Create a convert-X-Y skill for translating code between languages
argument-hint: <source-lang> <target-lang>
---

# Create Language Conversion Skill

Create a new one-way language conversion skill (`convert-<source>-<target>`) that extends `meta-convert-dev` with language-pair-specific patterns.

## Arguments

- `$1` - Source language (lowercase, e.g., `typescript`, `python`, `golang`)
- `$2` - Target language (lowercase, e.g., `rust`, `python`, `golang`)

## Quick Reference

| Step | Action              | Purpose                                              |
| ---- | ------------------- | ---------------------------------------------------- |
| 0    | Check existing      | Avoid duplicate skills                               |
| 0.5  | Check reverse skill | Reference `convert-$2-$1` for bidirectional insights |
| 1    | Validate args       | Ensure valid language names                          |
| 2    | Read foundations    | Understand meta-skill patterns                       |
| 2.5  | Validate 8 Pillars  | Ensure lang skills have coverage                     |
| 3    | Research pair       | Gather language-specific mappings                    |
| 3.5  | Assess difficulty   | Rate language pair complexity                        |
| 4    | Create directory    | Set up skill location                                |
| 5    | Generate SKILL.md   | Create from template                                 |
| 6    | Populate content    | Fill in language-specific details                    |
| 7    | Validate skill      | Run quality checklist                                |
| 8    | Cross-references    | Suggest related skill updates                        |
| 9    | Report              | Summary of what was created                          |
| 10   | Feedback            | Self-review and improvement suggestions              |

**Modes:**

- **Create** (default) - New skill from scratch
- **Update** - Improve existing skill (use `--update` or detect existing)
- **Quick Start** - For experienced users who know the patterns well

### Quick Start Mode (Experienced Users)

If you've created multiple conversion skills and are familiar with the 8-pillar validation, APTV workflow, and skill structure:

1. **Validate pillars quickly** (Step 2.5) - Check both lang skills for 8/8 coverage
2. **Check reverse skill** (Step 0.5) - Use Bidirectional Pattern Checklist if exists
3. **Assess difficulty** (Step 3.5) - Use difficulty matrix for expected effort
4. **Detect pattern families** (Step 3.10) - Find reusable patterns from similar pairs
5. **Skip deep research** - Use existing patterns from similar language pairs
6. **Focus on differentiators** - What makes THIS pair unique?
7. **Validate bidirectionally** (Step 7) - Run Bidirectional Consistency Validation

**Quick Start Checklist:**

- [ ] Steps 0, 0.5: Check existing & reverse skills
- [ ] Step 2.5: 8 Pillars validation (both skills ≥6/8)
- [ ] Step 3.5: Difficulty assessment (know expected size)
- [ ] Step 3.10: Pattern family identification
- [ ] Steps 4-6: Create and populate skill
- [ ] Step 7: Full validation including bidirectional consistency

**Similar language pair detection:**
| New Pair | Reference Pairs | Why Similar |
|----------|-----------------|-------------|
| clojure→X | python→X, elixir→X | Dynamic, functional |
| X→rust | X→go, typescript→rust | Static typing, ownership concepts |
| erlang→X | elixir→X | BEAM platform, same patterns |
| scala→X | kotlin→X, clojure→X | JVM, functional hybrid |

## Prerequisites

This command requires two meta-skills:

1. **`meta-convert-dev`** - Skill creation patterns (structure, template, workflow)
2. **`meta-convert-guide`** - Conversion methodology (APTV workflow, examples, reference guides)

---

## Workflow

### Step 0: Check for Existing Skill

Before creating a new skill, check if one already exists:

```bash
# Check if skill directory exists
ls components/skills/convert-$1-$2/

# Search for existing PRs
gh pr list --search "convert-$1-$2" --state all
```

**If the skill already exists:**

1. **Confirm with user**: "A `convert-$1-$2` skill already exists. Options:"
   - **Update mode**: Improve the existing skill (add missing sections, enhance examples)
   - **Skip**: Move on to next task
   - **Force create**: Replace existing (requires explicit confirmation)

2. **For update mode**, skip to [Step 6: Populate Content](#step-6-populate-content) and focus on:
   - Filling gaps identified in validation
   - Adding missing type mappings
   - Improving examples
   - Updating cross-references

3. **Report findings** even if skipping:

   ```markdown
   ## Existing Skill Found

   | Field    | Value                                      |
   | -------- | ------------------------------------------ |
   | Skill    | `convert-$1-$2`                            |
   | Status   | Already exists                             |
   | Location | `components/skills/convert-$1-$2/SKILL.md` |
   | PR       | #XXX (if known)                            |

   **Recommendation:** [Update / Skip / Review]
   ```

---

### Step 0.5: Check for Reverse Skill

Check if a skill for the reverse direction (`convert-$2-$1`) already exists:

```bash
# Check if reverse skill exists
ls components/skills/convert-$2-$1/

# Search for reverse skill PRs
gh pr list --search "convert-$2-$1" --state all
```

**Why check the reverse skill:**

- Bidirectional insights improve both skills
- Shared pitfalls and edge cases
- Consistent terminology and examples
- Cross-referencing opportunities

**If reverse skill EXISTS:**

1. **Read it for context** - Note patterns that apply in both directions
2. **Reference shared challenges** - Type mappings often have bidirectional insights
3. **Document cross-references** - Add "See Also" links in both skills
4. **Identify asymmetries** - Some patterns only matter in one direction
5. **Complete the Bidirectional Pattern Cross-Reference Checklist**

#### Bidirectional Pattern Cross-Reference Checklist

When a reverse skill exists, verify pattern consistency:

- [ ] Type mappings are inverse of reverse skill (where applicable)
- [ ] Shared error handling patterns documented in both
- [ ] Concurrency model translations are consistent
- [ ] Memory/ownership considerations mirror each other
- [ ] Platform ecosystem differences noted in both directions
- [ ] Idiom translations that work bidirectionally are documented in both
- [ ] One-way patterns are clearly marked (e.g., "No direct reverse translation")

```markdown
## Reverse Skill Found

| Field         | Value                                      |
| ------------- | ------------------------------------------ |
| Reverse Skill | `convert-$2-$1`                            |
| Location      | `components/skills/convert-$2-$1/SKILL.md` |
| Key Insights  | [List patterns that apply bidirectionally] |

**Action**: Reference in "See Also" section, share pitfalls documentation
```

**If reverse skill DOES NOT exist:**

1. **Note it as future work** - Add to "See Also" as `convert-$2-$1 (not yet available)`
2. **Consider creating an issue** - If the reverse direction is commonly needed
3. **Document one-way patterns** - Some translations are inherently one-directional

```markdown
## Reverse Skill Status

No `convert-$2-$1` skill exists. Consider:

- [ ] Create issue for reverse skill if commonly needed
- [ ] Document one-way patterns in this skill's pitfalls section
```

---

### Step 1: Validate Arguments

1. Confirm both source and target languages are provided
2. Validate language names are lowercase and recognized
3. Construct skill name: `convert-$1-$2`

If arguments are missing, ask the user:

```
Please provide source and target languages:
/create-lang-conversion-skill <source-lang> <target-lang>

Example: /create-lang-conversion-skill typescript rust
```

### Step 2: Read Foundation & Reference Skills

Read these skills to understand patterns and gather examples:

1. **Skill creation patterns** (required): `components/skills/meta-convert-dev/SKILL.md`
   - Skill naming convention
   - Required skill structure
   - 8 Pillars framework definition
   - Self-review checklist

2. **Conversion methodology** (required): `components/skills/meta-convert-guide/SKILL.md`
   - APTV workflow (Analyze → Plan → Transform → Validate)
   - Type mapping strategies (see `reference/type-system-mapping.md`)
   - Idiom translation approaches (see `examples/idiom-translation.md`)
   - Testing strategies (see `FORMS.md`)
   - Reference guides for each pillar (see `reference/` directory)

3. **Existing conversion skills** (required - read at least 1):
   - Search for `convert-*` skills in `components/skills/`
   - **Read one complete skill** (e.g., `convert-typescript-rust/SKILL.md` lines 1-300) to understand:
     - Expected depth for type mapping tables
     - "Why this translation" explanation style
     - Example complexity progression
   - Borrow patterns that apply to your language pair

4. **Language skills** (if available):
   - `lang-$1-dev` - Source language patterns
   - `lang-$2-dev` - Target language patterns

**Before proceeding**: Confirm you have read at least one complete conversion skill as a reference.

### Step 2.5: Validate 8 Pillars Coverage (Automated)

Before creating a conversion skill, validate that both source and target language skills have adequate coverage of the **8 Pillars** essential for code conversion.

#### Pillar Reference

| Pillar          | Search Terms                                             | Why Essential              |
| --------------- | -------------------------------------------------------- | -------------------------- |
| Module          | `## Module`, `import`, `export`, `visibility`            | Import/export translation  |
| Error           | `## Error`, `Result`, `Exception`, `try/catch`           | Error model translation    |
| Concurrency     | `## Concurrency`, `async`, `await`, `thread`             | Async pattern translation  |
| Metaprogramming | `## Metaprogramming`, `decorator`, `macro`, `annotation` | Attribute translation      |
| Zero/Default    | `## Zero`, `## Default`, `null`, `Option`, `None`        | Null-safety translation    |
| Serialization   | `## Serialization`, `JSON`, `serde`, `marshal`           | Data structure translation |
| Build           | `## Build`, `## Dependencies`, `Cargo`, `package.json`   | Project migration          |
| Testing         | `## Testing`, `#[test]`, `describe`, `unittest`          | Test suite conversion      |

**Optional 9th Pillar (for REPL-centric languages):**

| Pillar       | Search Terms                                          | Why Essential                 |
| ------------ | ----------------------------------------------------- | ----------------------------- |
| Dev Workflow | `## REPL`, `## Workflow`, `interactive`, `hot reload` | Development style translation |

Include this pillar when **either** source OR target language is REPL-centric:

| Language    | REPL Type                   | Include 9th Pillar? |
| ----------- | --------------------------- | ------------------- |
| Clojure     | Core development workflow   | **Always**          |
| Elixir      | IEx, LiveView hot reload    | **Always**          |
| Erlang      | Erl shell, hot code loading | **Always**          |
| Haskell     | GHCi for prototyping        | **Yes**             |
| Lisp/Scheme | REPL-first development      | **Always**          |
| Scala       | Ammonite, sbt console       | Yes (optional)      |
| Python      | IPython, Jupyter            | Yes (optional)      |
| F#          | FSI (F# Interactive)        | Yes (optional)      |

**Why this matters:** When converting FROM a REPL-centric language (e.g., Clojure→Rust), developers lose their REPL workflow. The skill should document how to achieve similar rapid feedback loops in the target (e.g., cargo watch, rust-analyzer). When converting TO a REPL-centric language, developers gain new workflows they should leverage.

#### Automated Validation

Run this validation automatically when reading the lang-\*-dev skills:

```bash
# Check for section headers (example for bash, but do this by reading the file)
for pillar in "Module" "Error" "Concurrency" "Metaprogramming" "Zero\|Default" "Serialization" "Build" "Testing"; do
  grep -c "## .*$pillar" components/skills/lang-$1-dev/SKILL.md
done
```

**While reading each skill file, check for these patterns:**

| Pillar          | ✓ Criteria                             | ~ Criteria                    | ✗ Criteria  |
| --------------- | -------------------------------------- | ----------------------------- | ----------- |
| Module          | Has `## Module` section with 50+ lines | Mentioned in another section  | No coverage |
| Error           | Has `## Error` section with examples   | Has Result/Exception mentions | No coverage |
| Concurrency     | Has `## Concurrency` section           | Has async/thread mentions     | No coverage |
| Metaprogramming | Has `## Metaprogramming` section       | Has decorator/macro mentions  | No coverage |
| Zero/Default    | Has dedicated section or table         | Mentioned in types section    | No coverage |
| Serialization   | Has `## Serialization` section         | Has JSON/serde mentions       | No coverage |
| Build           | Has `## Build` section                 | Has package manager mentions  | No coverage |
| Testing         | Has `## Testing` section               | Has test framework mentions   | No coverage |

#### Quick Score Calculation

Count section headers matching pillars:

- **8/8**: Excellent - proceed confidently
- **6-7/8**: Good - note gaps, proceed with pattern skill references
- **4-5/8**: Fair - strongly recommend improving lang skills first
- **0-3/8**: Poor - must improve lang skills before proceeding

#### Handling Gaps

| Score | Action                                                         |
| ----- | -------------------------------------------------------------- |
| 6-8/8 | Proceed. Reference pattern skills for missing pillars          |
| 4-5/8 | Ask user: Proceed with gaps documented OR improve skills first |
| 0-3/8 | Stop. Create issues to improve lang-\*-dev skills first        |

**Pattern skill supplements:**

- `patterns-concurrency-dev` → Concurrency gaps
- `patterns-serialization-dev` → Serialization gaps
- `patterns-metaprogramming-dev` → Metaprogramming gaps

**Pillar Gap Mitigation Examples:**

| Gap Scenario                     | Mitigation Strategy                        | Example                                                                     |
| -------------------------------- | ------------------------------------------ | --------------------------------------------------------------------------- |
| Source lacks Metaprogramming     | Research source language decorators/macros | Python→Rust: Research `@decorator` → `#[derive()]` mapping                  |
| Target lacks Concurrency docs    | Reference pattern skill + web search       | TypeScript→Go: Use `patterns-concurrency-dev` for goroutine patterns        |
| Both lack Serialization          | Create mappings from official docs         | Clojure→Elixir: Map `clojure.data.json` → `Jason` from library docs         |
| Source has partial Error section | Supplement with language reference         | Haskell→Rust: Expand `Maybe`/`Either` → `Option`/`Result` from Haskell wiki |

**Concrete mitigation workflow:**

1. Identify specific gap (e.g., "lang-clojure-dev has no Metaprogramming section")
2. Document what's missing ("macro hygiene, reader macros, syntax-quote")
3. Find authoritative source (Clojure.org docs, "Clojure for the Brave and True")
4. Create skill content with attribution in Limitations section
5. Track as improvement issue for lang-\*-dev skill

#### Report Format

```markdown
## 8 Pillars Validation

| Skill       | Mod | Err | Conc | Meta | Zero | Ser | Build | Test | Score |
| ----------- | --- | --- | ---- | ---- | ---- | --- | ----- | ---- | ----- |
| lang-$1-dev | ✓   | ✓   | ✓    | ~    | ✓    | ✓   | ✓     | ✓    | 7.5/8 |
| lang-$2-dev | ✓   | ✓   | ✓    | ✓    | ✓    | ✓   | ✓     | ✓    | 8/8   |

**Combined Score:** 15.5/16 (Excellent)
**Gaps:** lang-$1-dev metaprogramming is partial
**Mitigation:** Reference `patterns-metaprogramming-dev`
**Decision:** Proceed ✓
```

### Step 3: Research Language Pair

Before creating the skill, research the specific language pair using these structured checklists:

#### 3.1 Type System Differences

- [ ] Read primitive types sections in both lang skills
- [ ] Create draft mapping table for primitives
- [ ] Identify types without direct equivalents
- [ ] Note numeric precision differences (32-bit vs 64-bit, overflow behavior)

#### 3.2 Error Handling

- [ ] Identify error model in source (Exceptions? Result types? Error returns?)
- [ ] Identify error model in target
- [ ] Map error propagation patterns (try/catch → ?, throw → return Err)
- [ ] Note any "no runtime errors" guarantees (like Elm)

#### 3.3 Concurrency Models

- [ ] Identify async model in source (async/await, callbacks, actors?)
- [ ] Identify async model in target
- [ ] Map concurrency primitives (Promise → Future, Channel → mpsc)
- [ ] Note architectural differences (managed runtime vs explicit)

#### 3.4 Memory Models

- [ ] Source memory model: GC / ownership / manual / managed
- [ ] Target memory model
- [ ] If different, plan ownership translation strategy
- [ ] Note lifetime considerations if applicable

#### 3.5 Idiomatic Patterns

- [ ] What's considered "the way" in source language?
- [ ] What's considered "the way" in target language?
- [ ] Identify patterns that should NOT be directly translated
- [ ] Note paradigm shifts (OOP → FP, imperative → declarative)

#### 3.6 Ecosystem Equivalents

- [ ] Common HTTP libraries
- [ ] JSON/serialization libraries
- [ ] Testing frameworks
- [ ] Build tools

#### 3.7 Paradigm Shifts (if applicable)

- [ ] OOP → Functional: class hierarchies → data + functions, inheritance → composition
- [ ] Imperative → Declarative: loops → recursion/map/fold, mutation → immutability
- [ ] Dynamic → Static: duck typing → interfaces/traits, runtime checks → compile-time
- [ ] Script → Compiled: REPL workflow → build cycle, hot reload → recompile
- [ ] **Functional → Functional**: Different FP dialects have distinct idioms (see below)

**Functional→Functional Translation (e.g., Clojure→Elixir, Haskell→Scala):**

Even between functional languages, significant translation is needed:

| Aspect           | Variations                         | Example Pairs                                       |
| ---------------- | ---------------------------------- | --------------------------------------------------- |
| Type system      | Dynamic vs Static, HM vs dependent | Clojure (dynamic) → Haskell (static HM)             |
| Immutability     | Enforced vs Conventional           | Clojure (enforced) → Scala (conventional)           |
| Laziness         | Lazy vs Strict                     | Haskell (lazy) → Elixir (strict)                    |
| Concurrency      | Actor vs STM vs CSP                | Elixir (actors) → Clojure (STM + core.async)        |
| Macro system     | Hygienic vs Unhygienic             | Scheme (hygienic) → Clojure (limited hygiene)       |
| Pattern matching | Exhaustive vs Partial              | Haskell (exhaustive) → Elixir (partial ok)          |
| Effects          | Pure vs Practical                  | Haskell (IO monad) → Elixir (side effects anywhere) |

Don't assume functional→functional is simple—document the FP dialect differences.

#### 3.8 Transpilers & Interop Tools

- [ ] Check for existing transpilers between the languages (e.g., Fable.Python, GopherJS)
- [ ] Note FFI/interop capabilities (calling one language from the other)
- [ ] Document bidirectional insights from transpiler implementations

#### 3.9 Platform Ecosystem Differences

Different runtime platforms have distinct conventions and capabilities:

| Platform  | Languages                    | Key Characteristics                         |
| --------- | ---------------------------- | ------------------------------------------- |
| .NET/CLR  | C#, F#, VB.NET               | Rich stdlib, NuGet, strong async            |
| JVM       | Java, Kotlin, Scala, Clojure | Maven/Gradle, enterprise tooling            |
| BEAM/OTP  | Erlang, Elixir               | Actor model, hot reload, supervision        |
| Native    | Rust, C, C++, Go             | Direct memory, no GC (Rust/C), system-level |
| Scripting | Python, Ruby, JavaScript     | Dynamic, REPL-first, rapid prototyping      |

When converting across platforms:

- [ ] Note stdlib equivalents (collections, IO, networking)
- [ ] Consider runtime semantics (exceptions, threading, memory)
- [ ] Document dependency ecosystem differences (package managers)

#### When to Use WebSearch

Use WebSearch when:

- Lang skills lack coverage for a pillar
- Looking for real-world migration guides
- Finding common pitfalls others have encountered

**Example queries:**

- `"<Source> to <Target> migration patterns 2024"` - General migration guides
- `"<Source> <pattern> equivalent in <Target>"` - Specific pattern translations
- `"Common mistakes converting <Source> to <Target>"` - Pitfalls research
- `"<Source> vs <Target> error handling"` - Error model comparison

### Step 3.5: Assess Language Pair Difficulty

Rate the complexity of the language pair conversion to set expectations and guide depth of documentation.

> **See:** [meta-convert-guide/reference/difficulty-matrix.md](../skills/meta-convert-guide/reference/difficulty-matrix.md) for:
> - Complete rating framework (5 factors, 0-2 points each)
> - Pre-calculated difficulty for all 78 conversion pairs
> - Language characteristics table
> - Summary by difficulty level

#### Quick Reference

| Total Score | Difficulty | Expected Skill Size |
|-------------|------------|---------------------|
| 0-2 | Easy | 200-400 lines |
| 3-5 | Medium | 400-800 lines |
| 6-8 | Hard | 800-1200 lines |
| 9-10 | Expert | 1200+ lines |

#### Report Format

```markdown
## Difficulty Assessment

| Factor      | Score | Rationale                                                |
| ----------- | ----- | -------------------------------------------------------- |
| Type System | +X    | [e.g., "Dynamic → Static requires type annotation"]      |
| Paradigm    | +X    | [e.g., "OOP → FP requires mental model shift"]           |
| Memory      | +X    | [e.g., "GC → Ownership requires lifetime understanding"] |
| Concurrency | +X    | [e.g., "Promises → Actors"]                              |
| Platform    | +X    | [e.g., "Node → BEAM"]                                    |
| **Total**   | **X** | **[Easy/Medium/Hard/Expert]**                            |

**Implications:**

- Expected skill size: X lines
- Key focus areas: [List 2-3 main challenges]
- Recommended examples: [Number based on difficulty]
```

### Step 3.10: Cross-Language Pattern Detection

Identify patterns that share characteristics across language pairs. This helps reuse existing documentation and ensures consistency.

#### Pattern Families

| Pattern Family | Languages | Shared Characteristics |
|----------------|-----------|------------------------|
| **BEAM Family** | Erlang, Elixir | Actors, supervision, hot reload |
| **JVM Family** | Java, Kotlin, Scala, Clojure | Bytecode, classloaders, interop |
| **ML Family** | Haskell, OCaml, F#, Elm, Roc | ADTs, pattern matching, strong typing |
| **.NET Family** | C#, F#, VB.NET | CLR, async/await, LINQ patterns |
| **Lisp Family** | Clojure, Common Lisp, Scheme, Racket | S-expressions, macros, REPL |
| **Systems Family** | Rust, C, C++ | Manual memory, zero-cost abstractions |
| **Scripting Family** | Python, Ruby, JavaScript | Dynamic typing, duck typing, GC |

#### Cross-Reference Existing Skills

When creating a skill, check if related conversions already exist:

```bash
# Find skills involving source language
ls components/skills/convert-$1-*/
ls components/skills/convert-*-$1/

# Find skills involving target language
ls components/skills/convert-$2-*/
ls components/skills/convert-*-$2/
```

**Reuse patterns from:**

| New Skill | Reuse From | What to Borrow |
|-----------|------------|----------------|
| `convert-elixir-X` | `convert-erlang-X` | BEAM patterns, OTP supervision |
| `convert-X-rust` | `convert-go-rust` | GC→ownership, error handling |
| `convert-scala-X` | `convert-kotlin-X` | JVM idioms, null handling |
| `convert-haskell-X` | `convert-fsharp-X` | ML type patterns, ADTs |
| `convert-clojure-X` | `convert-elixir-X` | Functional patterns, immutability |

---

### Step 4: Create Skill Directory

```bash
mkdir -p components/skills/convert-$1-$2
```

### Step 5: Generate SKILL.md

Create the skill file using the template below.

**Important**: For code examples, reference existing `convert-X-Y` skills rather than creating examples from scratch. This ensures consistency and allows users to see real, tested patterns.

````markdown
---
name: convert-<source>-<target>
description: Convert <Source> code to idiomatic <Target>. Use when migrating <Source> projects to <Target>, translating <Source> patterns to idiomatic <Target>, or refactoring <Source> codebases. Extends meta-convert-dev with <Source>-to-<Target> specific patterns.
---

# Convert <Source> to <Target>

Convert <Source> code to idiomatic <Target>. This skill extends `meta-convert-dev` with <Source>-to-<Target> specific type mappings, idiom translations, and tooling.

## This Skill Extends

- `meta-convert-dev` - Skill creation patterns (structure, template)
- `meta-convert-guide` - Conversion methodology (APTV workflow, testing strategies)

For general concepts like the Analyze → Plan → Transform → Validate workflow, testing strategies, and common pitfalls, see `meta-convert-guide` first.

## This Skill Adds

- **Type mappings**: <Source> types → <Target> types
- **Idiom translations**: <Source> patterns → idiomatic <Target>
- **Error handling**: <Source> error model → <Target> error model
- **Async patterns**: <Source> concurrency → <Target> concurrency
- **[If applicable] Memory/Ownership**: <Source> memory model → <Target>

## This Skill Does NOT Cover

- General conversion methodology - see `meta-convert-dev`
- <Source> language fundamentals - see `lang-<source>-dev`
- <Target> language fundamentals - see `lang-<target>-dev`
- Reverse conversion (<Target> → <Source>) - see `convert-<target>-<source>`

---

## Quick Reference

| <Source> | <Target> | Notes |
| -------- | -------- | ----- |
| ...      | ...      | ...   |

## When Converting Code

1. **Analyze source thoroughly** before writing target
2. **Map types first** - create type equivalence table
3. **Preserve semantics** over syntax similarity
4. **Adopt target idioms** - don't write "<Source> code in <Target> syntax"
5. **Handle edge cases** - null/nil/None, error paths, resource cleanup
6. **Test equivalence** - same inputs → same outputs

---

## Type System Mapping

### Primitive Types

| <Source> | <Target> | Notes |
| -------- | -------- | ----- |
| ...      | ...      | ...   |

### Collection Types

| <Source> | <Target> | Notes |
| -------- | -------- | ----- |
| ...      | ...      | ...   |

### Composite Types

| <Source> | <Target> | Notes |
| -------- | -------- | ----- |
| ...      | ...      | ...   |

---

## Idiom Translation

### Pattern: <Common Pattern Name>

**<Source>:**

```<source-lang>
// Source code example
```
````

**<Target>:**

```<target-lang>
// Target code example - idiomatic, not transliterated
```

**Why this translation:**

- Explanation of why this is idiomatic in target language

[Repeat for major patterns...]

---

## Paradigm Translation (if applicable)

Include this section when converting between different paradigms (OOP→FP, imperative→declarative, etc.)

### Mental Model Shift: <Source Paradigm> → <Target Paradigm>

| <Source> Concept      | <Target> Approach            | Key Insight                       |
| --------------------- | ---------------------------- | --------------------------------- |
| Class with state      | Record + module functions    | Data and behavior separated       |
| Inheritance           | Composition / Protocols      | Favor interfaces over hierarchies |
| Mutable loops         | Recursion / fold / map       | Transformation over mutation      |
| Side effects anywhere | Pure functions + IO boundary | Effects pushed to edges           |

### Concurrency Mental Model

| <Source> Model  | <Target> Model     | Conceptual Translation           |
| --------------- | ------------------ | -------------------------------- |
| Threads + locks | Actors / CSP       | Shared state → message passing   |
| Callbacks       | Streams / Channels | Inversion of control → data flow |
| async/await     | Process mailboxes  | Promise → lightweight process    |

---

## Error Handling

### <Source> Error Model → <Target> Error Model

[Detailed section on error translation...]

---

## Concurrency Patterns

### <Source> Async → <Target> Async

[Detailed section on concurrency translation...]

---

## [If Applicable] Memory & Ownership

### <Source> Memory Model → <Target> Memory Model

[Detailed section for GC ↔ ownership conversions...]

---

## Common Pitfalls

1. **<Pitfall 1>**: Description and how to avoid
2. **<Pitfall 2>**: Description and how to avoid
   ...

---

## Limitations (if proceeding with Yellow/Red pillar coverage)

Include this section when creating a conversion skill despite incomplete lang-\*-dev coverage.

### Coverage Gaps

| Pillar   | Source Skill | Target Skill | Mitigation                                         |
| -------- | ------------ | ------------ | -------------------------------------------------- |
| <Pillar> | ✓/~/✗        | ✓/~/✗        | External research / pattern skill / documented gap |

### Known Limitations

1. **<Area>**: This skill has limited guidance on <topic> because lang-<x>-dev lacks coverage
2. **<Area>**: Conversion patterns for <feature> may be incomplete

### External Resources Used

| Resource        | What It Provided | Reliability |
| --------------- | ---------------- | ----------- |
| Official docs   | <topic> patterns | High        |
| Community guide | <topic> examples | Medium      |

---

## Tooling

| Tool | Purpose | Notes |
| ---- | ------- | ----- |
| ...  | ...     | ...   |

---

## Examples

Examples should progress in complexity:

### Example 1: Simple - <Single concept>

**Before (<Source>):**

```<source-lang>
// Simple, focused example demonstrating one concept
```

**After (<Target>):**

```<target-lang>
// Idiomatic translation of the single concept
```

### Example 2: Medium - <Multiple concepts>

**Before (<Source>):**

```<source-lang>
// Example combining 2-3 concepts (e.g., types + error handling)
```

**After (<Target>):**

```<target-lang>
// Shows how concepts interact in target language
```

### Example 3: Complex - <Real-world pattern>

**Before (<Source>):**

```<source-lang>
// Complete, realistic source code (~50-100 lines)
// Demonstrates a real-world use case
```

**After (<Target>):**

```<target-lang>
// Complete, idiomatic target code
// Shows full translation including edge cases
```

---

## See Also

For more examples and patterns, see:

- `meta-convert-dev` - Skill creation patterns
- `meta-convert-guide` - Conversion methodology, examples, and reference guides:
  - `examples/idiom-translation.md` - Null handling, collections, pattern matching
  - `examples/error-handling.md` - Exception→Result, error hierarchies
  - `examples/concurrency.md` - Promise/Future, parallel execution
  - `reference/gotchas/by-language.md` - Language-specific pitfalls
- `convert-X-Y` - Related conversion skills (list specific ones if applicable)
- `lang-<source>-dev` - <Source> development patterns
- `lang-<target>-dev` - <Target> development patterns

````

### Step 6: Populate Content

Fill in the template with specific content for this language pair:

#### Content Requirements

| Section | Minimum | Quality Bar |
|---------|---------|-------------|
| Quick Reference | 10 entries | Most common type mappings (see example below) |
| Primitive Types | All primitives | Include edge cases (infinity, NaN) |
| Collection Types | 5+ types | Array, Map, Set, Tuple equivalents |
| Composite Types | 3+ types | Struct, Class, Interface mappings |
| Idiom Translations | See priority list below | Common patterns with "why" explanations |
| Error Handling | Complete section | Full error model translation |
| Concurrency | Complete section | Async/threading translation |
| Memory/Ownership | If applicable | Include if languages differ (GC vs ownership) |
| Examples | 3+ (simple, medium, complex) | Progressive complexity |
| Pitfalls | 5+ pitfalls | Language-pair specific mistakes |

**Quick Reference Example (TypeScript → Rust):**

| TypeScript | Rust | Notes |
|------------|------|-------|
| `string` | `String` / `&str` | `String` for owned, `&str` for borrowed |
| `number` | `i32` / `f64` | Choose based on usage (integer vs float) |
| `boolean` | `bool` | Direct mapping |
| `null \| undefined` | `Option<T>` | Use `None` for absence |
| `T[]` | `Vec<T>` | Dynamic array equivalent |
| `Map<K,V>` | `HashMap<K,V>` | Import from `std::collections` |
| `interface` | `trait` / `struct` | Trait for behavior, struct for data |
| `class` | `struct` + `impl` | Separate data from methods |
| `Promise<T>` | `Future<Output=T>` | Requires async runtime |
| `try/catch` | `Result<T,E>` + `?` | Compile-time error handling |

This example shows 10 high-value mappings that cover the most common translation needs.

#### Organizing Large Type Mapping Tables

When type mappings exceed 20 entries, organize for scanability:

1. **Group by category**: Primitives → Collections → Composites → Special types
2. **Alphabetize within groups**: Easier to find specific types
3. **Use subsections**: Split into `### Primitive Types`, `### Collection Types`, etc.
4. **Highlight gotchas**: Bold or add ⚠️ for non-obvious translations

**Anti-pattern**: One giant table with 50+ rows sorted arbitrarily.

#### Idiom Translation Priority

**Required patterns (must include):**
1. Null/optional handling (null → Option, Maybe → nil, etc.)
2. Collection operations (map, filter, reduce equivalents)
3. Error propagation (try/catch → Result, throws → Either)
4. Async/await patterns (if either language has async)

**Language-specific patterns (include 2-6 based on relevance):**
- Type alias/newtype definitions
- Pattern matching
- Generics/type parameters
- Interface/trait implementations
- Resource cleanup (using/defer/Drop)
- Builder patterns
- Iteration patterns

#### Handling Features With No Equivalent

When source language has a feature with no direct target equivalent:

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **Explain the gap** | Feature is truly missing | Python decorators → Go (no equivalent; use code generation or manual wrapping) |
| **Suggest workaround** | Alternative achieves similar outcome | TypeScript `enum` → Go (use `const` + `iota` pattern) |
| **Recommend library** | Third-party fills the gap | Python list comprehensions → Java (use Streams or Guava) |
| **Document limitation** | No good solution exists | Ruby blocks → C (callbacks require explicit function pointers) |

**Template for no-equivalent patterns:**

```markdown
### Pattern: <Source Feature> (No Direct Equivalent)

**<Source>:**
\`\`\`<source-lang>
// Source code using the feature
\`\`\`

**<Target> - Closest Approximation:**
\`\`\`<target-lang>
// Best available approach
\`\`\`

**Why no direct equivalent:**
- [Explanation of language design differences]

**Workaround limitations:**
- [What the workaround doesn't provide]
```

#### Choosing Between Multiple Idiomatic Approaches

When the target language has multiple valid translations:

1. **Document all viable options** with trade-offs
2. **Recommend a default** for most cases
3. **Explain when to choose alternatives**

**Example (TypeScript `interface` → Rust):**

| Approach | When to Use |
|----------|-------------|
| `trait` | Defining shared behavior across types |
| `struct` | Defining data shape only |
| `struct` + `impl` | Data shape with associated methods |

**Template for multiple approaches:**

```markdown
### Pattern: <Source Pattern>

**Option A: <First Approach>** (Recommended for most cases)
\`\`\`<target-lang>
// Implementation
\`\`\`
When to use: [Criteria]

**Option B: <Alternative Approach>**
\`\`\`<target-lang>
// Implementation
\`\`\`
When to use: [Criteria]

**Decision guide:**
- Use A when: [condition]
- Use B when: [condition]
```

#### Common Pattern Template Snippets

Reusable templates for frequently needed patterns:

**Constructor/Factory Functions:**
```markdown
### Pattern: Constructor Function

**<Source>:**
\`\`\`<source-lang>
class User {
  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }
}
\`\`\`

**<Target>:**
\`\`\`<target-lang>
// Target equivalent (struct + new function, builder, etc.)
\`\`\`

**Why this translation:**
- [Reason for the pattern choice]
```

**Resource Cleanup:**
```markdown
### Pattern: Resource Management

**<Source>:** `try-finally` / `using` / `with`
**<Target>:** `Drop` trait / `defer` / context manager equivalent

[Include ownership/lifetime considerations if applicable]
```

**Singleton/Module Pattern:**
```markdown
### Pattern: Module-Level State

**<Source>:** Static class / module singleton
**<Target>:** `lazy_static!` / `once_cell` / module-level `const`

[Note thread-safety implications]
```

#### When to Use Code Comments vs Separate Explanation

| Situation | Use Comments | Use "Why" Section |
|-----------|--------------|-------------------|
| Non-obvious syntax | Yes - inline | No |
| Conceptual difference | Light comment | Yes - detailed |
| Performance implication | Brief note | Yes - with rationale |
| Gotcha/pitfall | Warning comment | Yes - with example |
| Standard idiom | No (self-evident) | Brief note if notable |

**Good comment pattern:**
```rust
// Note: Rust requires explicit Option unwrap; TS would allow direct access
let name = user.name.unwrap_or_default();
```

**When to move explanation out of code:**
- Explanation exceeds 2 lines
- Requires comparison to source language
- Documents a design decision, not just syntax

#### Quality Guidance: Good vs Great

| Aspect | Good | Great |
|--------|------|-------|
| Type mapping | `String → &str` | `String → &str for borrowed, String for owned; use Cow<str> when ownership varies` |
| Why explanation | "Use Result in Rust" | "Use Result because Rust has no exceptions; the ? operator propagates errors like try/catch but at compile time" |
| Example code | Syntactically correct | Syntactically correct + follows target language conventions (naming, formatting, idioms) |
| Pitfall | "Don't forget to handle errors" | "TypeScript's `undefined` vs Rust's `Option`: TS allows property access on undefined (runtime error), Rust requires explicit unwrap (compile error)" |

#### Example Complexity Guide

| Level | Lines | Concepts | Purpose |
|-------|-------|----------|---------|
| Simple | 5-15 | 1 | Demonstrate single type/idiom translation |
| Medium | 20-40 | 2-3 | Show concept interactions |
| Complex | 50-100 | 4+ | Real-world use case, production-ready |

#### Example Quality Checklist

Before finalizing examples, verify each one meets these criteria:

- [ ] **Syntactically valid** - Source code compiles/runs without errors
- [ ] **Target is idiomatic** - Not transliterated (avoid "Source code in Target syntax")
- [ ] **Demonstrates pattern clearly** - Single focus per example (Simple), combined focus (Medium/Complex)
- [ ] **Complexity matches level** - Don't overcomplicate Simple examples
- [ ] **Comments explain "why"** - Not just "what" the code does
- [ ] **Edge cases shown** - Null handling, error paths, empty collections where relevant

#### Example Organization (For Large Skills)

When skills grow beyond 800 lines or have 5+ examples:

**File Structure Options:**

```
convert-source-target/
├── SKILL.md              # Core content, inline simple/medium examples
├── examples/
│   ├── 01-simple.md      # Or inline if < 20 lines each
│   ├── 02-medium.md
│   └── 03-complex-api-client.md  # Named by use case
└── gotchas/
    └── common-mistakes.md  # Extract if > 10 pitfalls
```

**When to extract examples to separate files:**
- Example exceeds 50 lines (complex examples often do)
- Multiple variations of the same pattern
- Examples need their own context/setup code

**Naming conventions:**
- Number prefix for ordering: `01-`, `02-`, `03-`
- Descriptive suffix: `-api-client`, `-error-handling`, `-async-patterns`

**Keep inline when:**
- Simple/medium examples under 30 lines
- Pattern is central to understanding the skill
- Extraction would hurt discoverability

#### Balancing Comprehensiveness vs Maintainability

Skills should be complete enough to be useful but not so large they become unmaintainable.

**Size guidelines by difficulty:**

| Difficulty | Target Lines | Max Lines | When to Split |
|------------|--------------|-----------|---------------|
| Easy | 200-400 | 500 | Rarely needed |
| Medium | 400-800 | 1000 | Extract complex examples |
| Hard | 800-1200 | 1500 | Use progressive disclosure |
| Expert | 1200+ | 2000 | Split into focused sub-skills |

**Signs a skill is too comprehensive:**
- More than 80% of content is rarely used
- Examples cover edge cases that aren't practically common
- Type mappings include every possible type (not just common ones)

**Signs a skill is too sparse:**
- Users frequently need to search elsewhere for answers
- Common patterns are missing
- "See also" links are doing the heavy lifting

**Maintainability checklist:**
- [ ] Each section can be updated independently
- [ ] Examples can be validated without reading entire skill
- [ ] New patterns can be added without restructuring
- [ ] Outdated content can be identified and removed

#### Testing/Validation Guidance

To verify conversion examples are correct:

1. **Use language playgrounds** for quick validation:
   - TypeScript: [TS Playground](https://www.typescriptlang.org/play)
   - Python: [Python Tutor](https://pythontutor.com/) or REPL
   - Rust: [Rust Playground](https://play.rust-lang.org/)
   - Go: [Go Playground](https://go.dev/play/)
   - Elixir: [Elixir Playground](https://playground.elixir-lang.org/)

2. **For complex examples**, consider:
   - Create minimal test files to verify both source and target compile
   - Run equivalent inputs through both to verify same outputs
   - Check error cases behave equivalently

3. **Document behavioral differences**:
   - If source and target have different semantics (e.g., overflow behavior), note this
   - Include comments like `// Note: Python int is arbitrary precision, Rust i64 overflows`

### Step 7: Validate Skill

Run through this checklist before completing:

#### Structure Validation
- [ ] SKILL.md has valid YAML frontmatter
- [ ] `name` matches directory name (`convert-$1-$2`)
- [ ] `description` includes trigger phrases (convert, migrate, translate)
- [ ] All sections from template are present
- [ ] No placeholder text remains (`...`, `<Description>`, etc.)

#### Content Validation
- [ ] Type mapping tables are comprehensive
- [ ] Idiom translations include "why" explanations
- [ ] Error handling section covers full error model
- [ ] Concurrency section addresses async patterns
- [ ] Memory/Ownership included if languages differ
- [ ] Paradigm Translation included if paradigms differ (OOP→FP, etc.)

#### Type Mapping Validation Checklist
- [ ] **Primitives**: All basic types covered (int, float, string, bool, char)
- [ ] **Numerics**: Precision differences noted (i32 vs i64, overflow behavior)
- [ ] **Nullability**: null/nil/None → Option/Maybe mappings clear
- [ ] **Collections**: Array, List, Map, Set, Tuple equivalents
- [ ] **Composites**: Struct, Class, Interface, Enum, Union mappings
- [ ] **Generics**: Type parameter syntax and constraints
- [ ] **Special types**: Never/Bottom, Unit/Void, Any/Dynamic

#### Example Validation
- [ ] Examples progress in complexity (simple → complex)
- [ ] Source code examples are syntactically correct
- [ ] Target code examples are idiomatic (not transliterated)
- [ ] Examples cover different aspects (types, errors, async)
- [ ] Complex example is realistic and complete

#### Cross-Reference Validation
- [ ] References `meta-convert-dev` as foundation
- [ ] Links to `lang-$1-dev` if it exists
- [ ] Links to `lang-$2-dev` if it exists
- [ ] Mentions reverse skill `convert-$2-$1` in "Does NOT Cover"
- [ ] Lists related `convert-X-Y` skills in "See Also"

#### Bidirectional Consistency Validation

If a reverse skill (`convert-$2-$1`) exists, verify bidirectional consistency:

| Check | Status | Notes |
|-------|--------|-------|
| Type mappings are inverse | ☐ | e.g., `String→&str` ↔ `&str→String` |
| Shared pitfalls documented in both | ☐ | Common gotchas apply both ways |
| Platform considerations consistent | ☐ | Same platform diff noted in both |
| One-way patterns marked clearly | ☐ | Some patterns only work in one direction |
| Cross-references link to each other | ☐ | Both skills link to each other |

**One-Way Pattern Examples:**

| Pattern | Direction | Why One-Way |
|---------|-----------|-------------|
| GC→Ownership | Any→Rust | Must add lifetime annotations, no reverse automatic |
| Dynamic→Static | Python→TypeScript | Type inference possible but not automatic reverse |
| Macro→Function | Rust→Go | Macros have no Go equivalent |
| Actor→Thread | Erlang→Java | Actor patterns don't map back cleanly |

When documenting one-way patterns:
```markdown
<!-- In Pitfalls section -->
> **One-Way Pattern**: This translation from [source] to [target]
> does not have a clean reverse. See `convert-$2-$1` for the
> reverse approach, which uses [different strategy].
```

### Step 8: Suggest Cross-References

After creating the skill, suggest related skills that should reference it:

```markdown
## Cross-Reference Updates Suggested

Consider adding references to this skill in:

1. **`meta-convert-dev`** - Add to "Existing Conversion Skills" section
2. **`lang-$1-dev`** - Add to "Related Skills" section
3. **`lang-$2-dev`** - Add to "Related Skills" section
4. **`convert-$2-$1`** - Reference as reverse skill (if it exists)
````

### Step 9: Report Results

```
## Skill Created

| Field | Value |
|-------|-------|
| Skill Name | `convert-<source>-<target>` |
| Location | `components/skills/convert-<source>-<target>/SKILL.md` |
| Extends | `meta-convert-dev` |

**Validation Results:**
- [ ] Structure valid
- [ ] Content complete
- [ ] Examples validated
- [ ] Cross-references added

**Key Features:**
- [List main type mappings covered]
- [List main idiom translations covered]
- [Error handling approach]
- [Concurrency model translation]

**Next Steps:**
1. Review type mapping completeness
2. Test with real conversion scenarios
3. Update cross-referenced skills
```

### Step 10: Self-Review & Feedback

After completing the skill creation, provide feedback on the tools and skills used during the process. This helps improve the ecosystem.

#### 10.1 Identify Skills & Commands Used

List all skills and commands used during this task:

```markdown
## Skills & Commands Used

| Resource                        | Type    | How Used                              |
| ------------------------------- | ------- | ------------------------------------- |
| `meta-convert-dev`              | skill   | Foundation for structure and patterns |
| `lang-$1-dev`                   | skill   | Source language patterns (if used)    |
| `lang-$2-dev`                   | skill   | Target language patterns (if used)    |
| `convert-X-Y`                   | skill   | Reference for examples (if used)      |
| `/create-lang-conversion-skill` | command | This workflow                         |
```

#### 10.2 Gather Feedback

For each resource used, evaluate:

**What worked well:**

- Clear instructions that helped complete the task
- Patterns that translated well to this language pair
- Sections that saved time or prevented mistakes

**What could be improved:**

- Missing information that required external research
- Unclear instructions that caused confusion
- Patterns that didn't apply to this language pair
- Suggestions for new sections or examples

**Context to include:**

- Which language pair was being created
- Specific challenges encountered
- Workarounds used for missing guidance

#### 10.3 Create Feedback Issues

For each resource with actionable feedback:

1. **Search for existing parent issues:**

   ```bash
   gh issue list --repo aRustyDev/ai --search "<skill-or-command-name>" --state open
   ```

2. **If parent issue exists** (about the skill/command in question):
   - Create a child issue linked to the parent
   - Use `Relates to #<parent>` in the body

3. **If no relevant parent exists:**
   - Create a new issue

**Issue Template:**

```markdown
## Feedback: <skill-or-command-name>

### Context

- **Task**: Creating `convert-$1-$2` skill
- **Used for**: [e.g., "Understanding APTV workflow", "Type mapping patterns"]

### What Worked Well

- [Specific positive feedback with examples]

### Suggested Improvements

- [ ] [Actionable improvement 1]
- [ ] [Actionable improvement 2]

### Additional Notes

[Any other observations or suggestions]

---

Feedback from: `/create-lang-conversion-skill $1 $2`
```

**Example issue creation:**

```bash
# If parent issue #205 exists for meta-convert-dev
gh issue create --repo aRustyDev/ai \
  --title "feedback(meta-convert-dev): from convert-$1-$2 creation" \
  --body "$(cat <<'EOF'
## Feedback: meta-convert-dev

### Context
- **Task**: Creating `convert-typescript-rust` skill
- **Used for**: Foundation patterns, type mapping strategies

### What Worked Well
- APTV workflow provided clear structure
- Type mapping tables were excellent templates

### Suggested Improvements
- [ ] Add more examples for async cancellation patterns
- [ ] Include guidance on translating decorators/attributes

Relates to #205

---
Feedback from: `/create-lang-conversion-skill typescript rust`
EOF
)"
```

#### 10.4 Report Feedback Summary

```markdown
## Feedback Submitted

| Resource                        | Issue | Summary         |
| ------------------------------- | ----- | --------------- |
| `meta-convert-dev`              | #XXX  | [Brief summary] |
| `/create-lang-conversion-skill` | #YYY  | [Brief summary] |
```

## Examples

```
/create-lang-conversion-skill typescript rust
/create-lang-conversion-skill python golang
/create-lang-conversion-skill typescript python
```

## Notes

- Each conversion skill is ONE-WAY (e.g., `convert-ts-rust` is different from `convert-rust-ts`)
- Always read `meta-convert-dev` first for foundational patterns
- Reference existing `convert-X-Y` skills for structure and examples
- Focus on idiomatic translations, not syntax transliteration
- Include comprehensive type mapping tables
- Provide examples at multiple complexity levels (simple, medium, complex)
- Complete the validation checklist before marking skill as done
- **Always complete Step 10** - Feedback improves the ecosystem for future skill creation
