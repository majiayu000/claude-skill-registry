---
name: documentation-explanation
description: Efficient documentation discovery, interpretation, and explanation methodology for technical projects. Use when explaining system architecture, design rationale, implementation patterns, or integrating multiple documentation sources (text docs, code comments, diagrams, test descriptions). Provides strategies for navigating large documentation sets, extracting design intent, cross-referencing multiple sources, and synthesizing comprehensive explanations.
---

# Documentation Explanation Methodology

Universal framework for efficiently discovering, interpreting, and explaining technical documentation across text files, code comments, diagrams, and test descriptions.

## When to Use This Skill

- Explaining system architecture from multiple documentation sources
- Extracting design rationale and decisions from specifications
- Understanding how components integrate by cross-referencing docs and code
- Navigating large documentation sets to answer specific questions
- Synthesizing information from text docs + code + diagrams + tests
- Identifying documentation gaps or inconsistencies
- Teaching users how a system works based on available documentation

## Documentation Discovery Framework

### Document Type Taxonomy

Technical projects contain multiple documentation types serving different purposes:

| Type | Purpose | Common Locations | Triggering Questions |
|------|---------|------------------|---------------------|
| **Architecture Specs** | System design, component hierarchy | `docs/architecture/`, `docs/design/` | "How does X work?", "What's the overall structure?" |
| **Implementation Guides** | Coding patterns, best practices | `docs/implementation/`, module headers | "How to implement Y?", "What pattern to use?" |
| **API References** | Interface definitions, contracts | `docs/api/`, interface files, header comments | "What parameters does X take?", "What does Y return?" |
| **Test Plans** | Verification strategy, coverage | `docs/testing/`, test files, assertion comments | "What tests exist?", "Is X verified?" |
| **Debugging Guides** | Known issues, troubleshooting | `docs/debugging/`, `docs/known_issues/` | "Why is X failing?", "Known problems with Y?" |
| **Integration Guides** | Cross-module interfaces | `docs/integration/`, glue logic | "How do X and Y connect?", "What's the data flow?" |
| **Design Rationale** | Why decisions were made | Embedded in specs, commit messages | "Why was X designed this way?", "What tradeoffs?" |
| **Reference Docs** | Standards, protocols, ISA | `docs/reference/`, external links | "What does instruction X do?", "Protocol requirements?" |

### Discovery Strategies

#### Text Documentation Search

**Filename patterns reveal content**:
- `*_spec.md`, `*_architecture.md` → High-level design
- `*_implementation.md`, `*_guide.md` → How-to information
- `*_test_plan.md`, `*_verification.md` → Testing strategy
- `*_api.md`, `*_reference.md` → Interface definitions
- `*_debug.md`, `*_issues.md`, `*_troubleshooting.md` → Problem-solving
- `README.md` → Entry point, overview
- `CHANGELOG.md`, `*_status.md` → Implementation progress

**Directory structure indicates organization**:
- `docs/` → Primary documentation
- `docs/cpu/`, `docs/modules/` → Component-specific docs
- `reference/` → External or upstream documentation
- Root-level `.md` files → Project-wide information

**Content signatures identify purpose**:
- "Design Intent", "Rationale", "Why this approach" → Design decisions
- "Mandatory", "Must", "Shall" → Requirements
- "Known Issue", "Workaround", "Bug" → Debugging information
- "Example", "Usage", "How to" → Implementation guidance
- Tables with addresses/opcodes → Reference material
- "Status: Complete", "TODO", "Pending" → Implementation progress
- "❌ Wrong / ✅ Correct" → Anti-patterns and best practices

#### Code-as-Documentation Search

**Module/Class headers** contain architectural information:
```systemverilog
// Module: vexriscv_decoder
// Purpose: Instruction decode stage with hazard detection
// Inputs: 32-bit instruction, pipeline control signals
// Outputs: ALU control, register addresses, immediate values
// Design rationale: Single-cycle decode with bypass forwarding
```

**Interface definitions** document contracts:
```systemverilog
interface axi4_lite_if(input logic clk);
    // Address Write Channel
    logic [31:0] awaddr;   // Write address
    logic        awvalid;  // Write address valid
    logic        awready;  // Write address ready (response from slave)
    // ...
endinterface
```

**Function/Task signatures** with docstrings:
```python
def analyze_pipeline_stall(trace_data: list, cycle: int) -> StallReason:
    """Determine why pipeline stalled at specific cycle.
    
    Args:
        trace_data: List of cycle-by-cycle execution trace
        cycle: Cycle number to analyze
        
    Returns:
        StallReason enum indicating hazard type (DATA/CONTROL/MEMORY)
        
    Algorithm:
        1. Check for RAW hazards (read-after-write)
        2. Check for control flow changes (branch/jump)
        3. Check for memory access conflicts
    """
```

**Inline comments** explain non-obvious logic:
```verilog
// Multi-cycle shift operation causes 8-cycle stall
// Must hold decode stage until shifter completes
assign decode_stall = shifter_busy && rs2_is_shift_count;
```

**Assertion messages** document expected behavior:
```systemverilog
property p_axi_wdata_stable;
    @(posedge clk) (awvalid && !awready) |=> $stable(awaddr);
endproperty

assert property (p_axi_wdata_stable) else
    $error("AXI Protocol Violation: awaddr changed while awvalid held and awready=0");
```

**Test descriptions** explain verification intent:
```systemverilog
// Test: Load-Use Hazard with Forwarding
// Scenario: LW x5, 0(x1)  followed by  ADD x6, x5, x7
// Expected: Pipeline stalls 1 cycle, then forwards MEM→EX
// Verification: Check stall signal asserted for exactly 1 cycle
```

**Naming conventions** as implicit documentation:
- `fetch_pc_valid` → PC output from fetch stage is valid
- `decode_rs1_hazard` → Register source 1 has data hazard
- `mem_stage_stall_req` → Memory stage requesting pipeline stall
- `csr_mtvec_base` → Machine trap vector base address (CSR)

### Progressive Disclosure Approach

**Don't read everything at once.** Use progressive refinement:

1. **Overview first**: Read high-level architecture docs, README files
2. **Narrow down**: Identify which subsystem/module is relevant
3. **Read specifics**: Load detailed module documentation
4. **Cross-reference**: Validate understanding against code/tests
5. **Synthesize**: Combine multiple sources into coherent explanation

**Example flow for "How does hazard detection work?"**:
1. Overview: `docs/architecture.md` → Identifies hazard unit module
2. Narrow: `docs/cpu/hazard_unit.md` → Detailed hazard logic
3. Code: Read `hazard_unit.sv` module header and key logic
4. Tests: Check `tests/*_hazard_test.sv` for test scenarios
5. Synthesize: Explain based on spec + implementation + verification

## Multi-Source Synthesis Patterns

### Combining Documentation Sources

**Architecture question: "How does component X work?"**

Sources to combine:
1. **Text spec** (design intent, requirements)
2. **Module header** (interface, I/O signals)
3. **Implementation** (actual logic, algorithms)
4. **Diagrams** (visual structure - see [references/diagram-interpretation.md](references/diagram-interpretation.md))
5. **Tests** (expected behavior, edge cases)
6. **Known issues** (limitations, gotchas)

**Synthesis pattern**:
```
[Component X] {purpose from spec}

Architecture:
- {Structure from spec + diagrams}
- {Key interfaces from code headers}

Implementation:
- {Algorithm/logic from spec + inline comments}
- {Data flow from code analysis}

Verification:
- {Test scenarios from test descriptions}
- {Edge cases from assertions}

Known limitations:
- {Issues from debugging docs}
```

### Cross-Validation Techniques

**Does code match specification?**

Check for mismatches:
- Spec says "single-cycle operation" but code shows multi-cycle FSM
- Spec defines 5 pipeline stages but code implements 4
- Interface diagram shows signal `ready` but code uses `rdy`
- Test plan says "fully verified" but no tests exist in test directory

**Identifying documentation gaps**:
- Module implemented but no specification document
- Complex algorithm in code without explanation comments
- Test exists but no test plan documentation
- Interface signals without timing diagrams

**Resolving inconsistencies**:
1. Code is typically source of truth for "what exists"
2. Specs reveal "what was intended"
3. Tests show "what was verified"
4. Comments explain "why it works this way"

If conflict exists:
- Note the discrepancy in explanation
- Verify which source is more recent (git history, timestamps)
- Check if issue is documented in known_issues
- Recommend updating documentation

## Explanation Templates

### "How does X work?" Pattern

**Question structure**: User wants to understand a component's operation

**Response template**:
```
[Component X] performs {high-level purpose from spec}.

Architecture:
{Structure description from spec/diagrams}
Key components: {From architecture doc or block diagram}

Interface:
{Input/output signals from code header or interface definition}

Operation:
{Algorithm/behavior from spec + code + inline comments}
{Timing/sequence from timing diagrams or sequence diagrams}

Example:
{Concrete example from test descriptions or code comments}

Related components:
{Cross-references to interacting modules}
```

### "Why was X designed this way?" Pattern

**Question structure**: User wants design rationale

**Response template**:
```
[Design decision X] was chosen because {extract from design rationale sections}.

Alternatives considered:
{From "Design Alternatives" sections or commit messages}

Tradeoffs:
Advantages: {Performance, simplicity, compatibility, etc.}
Disadvantages: {Limitations, complexity, resource cost}

Constraints:
{Requirements that drove the decision - from specs}

Implementation status:
{Current state from status docs - complete/partial/planned}
```

### "How to integrate X with Y?" Pattern

**Question structure**: User wants to connect two components

**Response template**:
```
[Component X] connects to [Component Y] through {interface description}.

Interface signals:
{Signal list from interface definitions or glue logic}

Data flow:
{Sequence from X to Y, from sequence diagrams or code}

Configuration required:
{Setup steps from integration guides or test setup code}

Example integration:
{From existing integration code or test harnesses}

Common issues:
{From debugging docs or known issues}
```

### "What tests exist for X?" Pattern

**Question structure**: User wants verification status

**Response template**:
```
[Component X] verification coverage:

Test inventory:
{List from test plan docs and actual test files}

Scenarios covered:
{Test descriptions from test plan and test file headers}

Coverage gaps:
{Unimplemented tests from test plan, or features without tests}

Assertions:
{Assertion descriptions from assertion modules}

Known issues:
{Bugs/limitations from debugging docs}

Test execution:
{How to run tests - from test infrastructure docs}
```

### "Known issues with X?" Pattern

**Question structure**: User debugging or planning work

**Response template**:
```
[Component X] known issues:

Issue inventory:
{List from known_issues.md, bug_fixes_*.md, or issue tracking}

Symptoms:
{Observable behavior from debugging docs}

Root causes:
{Analysis from debugging docs or bug fix descriptions}

Workarounds:
{Temporary solutions from debugging guides}

Status:
{Fixed/open/wontfix from status docs or changelogs}

Related tests:
{Tests that catch or demonstrate the issue}
```

## Documentation Quality Assessment

When explaining from documentation, note quality indicators:

**High-quality documentation signs**:
- ✅ Design rationale explained
- ✅ Diagrams match code structure
- ✅ Interface contracts clearly defined
- ✅ Code has explanatory comments
- ✅ Tests document expected behavior
- ✅ Known limitations documented
- ✅ Examples provided

**Documentation gaps to flag**:
- ❌ Complex logic without comments
- ❌ Inconsistency between spec and code
- ❌ Modules without specifications
- ❌ Interfaces without timing diagrams
- ❌ Features without test coverage
- ❌ Bugs without troubleshooting guides
- ❌ No design rationale for unusual choices

## Best Practices

### Efficient Navigation

1. **Start broad, narrow down**: Overview → subsystem → component → details
2. **Use file structure**: Directory hierarchy reveals organization
3. **Follow cross-references**: Docs link related information
4. **Check timestamps**: Recent docs more likely accurate
5. **Validate with code**: Code is source of truth for implementation
6. **Look for patterns**: Similar modules have similar documentation

### Interpretation Strategies

1. **Read abstracts first**: Frontmatter, summaries, introductions
2. **Skim for structure**: Headings, bullet lists, diagrams
3. **Focus on relevant sections**: Don't read everything
4. **Extract key concepts**: Design decisions, interfaces, algorithms
5. **Note assumptions**: Requirements, constraints, dependencies
6. **Identify status**: Complete, partial, planned, deprecated

### Explanation Construction

1. **Match user's level**: Adjust detail to question specificity
2. **Structure clearly**: Headings, lists, logical flow
3. **Concrete examples**: From tests, code, or diagrams
4. **Cite sources**: Reference specific docs/files/lines
5. **Note gaps**: Be honest about missing information
6. **Cross-reference**: Link related components/concepts
7. **Visual aids**: Reference diagrams (see [references/diagram-interpretation.md](references/diagram-interpretation.md))

### Bilingual Content Handling

When documentation uses multiple languages:

1. **Identify primary language**: Usually code/comments are English, design rationale may be native language
2. **Preserve technical terms**: Keep signal names, module names as-is
3. **Translate for clarity**: Convert design rationale to user's preferred language
4. **Note language mixing**: Flag when critical info is in non-English sections
5. **Respect author intent**: Some terms better left in original language

Example (Japanese design doc with English code):
```
Design Intent (設計意図): Pipeline hazard detection must complete in single cycle
to avoid degrading clock frequency.

Implementation: 
logic decode_hazard = (ex_rd == decode_rs1) && ex_regwrite_valid;
```

Output explanation: "The hazard unit performs single-cycle detection to maintain clock frequency. It checks if the decode stage's source register matches the execute stage's destination register while that destination is being written."

### Auto-Generated Content Recognition

Some documentation is machine-generated:

**Indicators**:
- "AUTO-GENERATED - DO NOT EDIT" headers
- Consistent formatting (tables, lists)
- Timestamps in headers
- Scripts referenced (`generate_docs.py`)

**Handling**:
- Treat as reference (opcodes, register maps, API lists)
- Don't suggest edits to these files
- Point users to source data (JSON, schemas) for changes
- Note that manual docs may override auto-generated content

## Advanced Techniques

### Documentation Mining

For large documentation sets, mine for specific information:

**Keyword search patterns**:
- Design decisions: `(rationale|why|because|chose|decision|tradeoff)`
- Requirements: `(must|shall|mandatory|required|critical)`
- Issues: `(bug|issue|problem|workaround|limitation)`
- Status: `(complete|implemented|pending|todo|wip)`
- Examples: `(example|usage|scenario|sample)`

**Cross-referencing**:
- Find all mentions of component X across docs
- Build connection map (which components interact)
- Identify documentation clusters (related topics)

### Version/Status Indicators

Track implementation progress from docs:

- ✅ / `[Done]` / `Status: Complete` → Implemented and verified
- ⏳ / `[WIP]` / `Status: In Progress` → Partial implementation
- ❌ / `[TODO]` / `Status: Planned` → Not yet implemented
- ⚠️ / `[Known Issue]` / `Status: Buggy` → Implemented but problematic
- 🔧 / `[Refactoring]` / `Status: Redesign` → Being reworked

### Diagram Integration

Diagrams provide visual documentation - see detailed interpretation guide: [references/diagram-interpretation.md](references/diagram-interpretation.md)

Quick diagram types:
- **Block diagrams** → Component structure and connectivity
- **Sequence diagrams** → Temporal behavior and message flow
- **State machines** → Control flow and state transitions
- **Timing diagrams** → Cycle-accurate signal behavior
- **Flowcharts** → Algorithmic logic and decision trees

## Common Pitfalls

❌ **Reading everything before answering**: Too slow, wastes tokens
✅ **Progressive disclosure**: Start broad, narrow down as needed

❌ **Treating specs as absolute truth**: May be outdated or incorrect
✅ **Cross-validate**: Check spec against code and tests

❌ **Ignoring code comments**: Often contain critical context
✅ **Mine code-as-documentation**: Headers, comments, assertions, tests

❌ **Missing diagram information**: Diagrams often clearest explanation
✅ **Interpret visuals**: Extract structure and flow from diagrams

❌ **Not noting documentation gaps**: User needs complete picture
✅ **Flag inconsistencies**: Note missing docs, conflicts, uncertainties

❌ **Over-explaining obvious concepts**: Wastes time and tokens
✅ **Match detail to question**: Answer what was asked

❌ **Single-source answers**: Incomplete understanding
✅ **Synthesize sources**: Text + code + diagrams + tests = complete picture

## Summary

Effective documentation explanation requires:

1. **Smart discovery**: Use taxonomy and search patterns to find relevant docs quickly
2. **Multi-source synthesis**: Combine text, code, diagrams, and tests
3. **Progressive disclosure**: Start broad, narrow down as needed
4. **Cross-validation**: Check consistency across sources
5. **Clear explanation**: Structure responses with templates
6. **Quality assessment**: Note gaps and inconsistencies
7. **Efficient navigation**: Don't read everything, focus on relevance

For diagram interpretation strategies, see [references/diagram-interpretation.md](references/diagram-interpretation.md).
