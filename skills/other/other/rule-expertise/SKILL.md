---
name: rule-expertise
description: "Write effective instructions and prompts. Use when creating documentation, writing guidelines, establishing project rules, or crafting any directional communication. Keywords: instructions, guidelines, prompt engineering, documentation, rules. Not for code implementation, debugging, or non-instructional writing."
---

<mission_control>
<objective>Create clear, actionable instructions that guide recipients to successful outcomes with verifiable completion</objective>
<success_criteria>Instructions specify what to do, why it matters, how to verify success, and include concrete examples</success_criteria>
</mission_control>

# Effective Instruction Writing

Principles and practices for creating clear, actionable instructions that others can follow successfully.

## Quick Start

**If you need to write instructions:** Focus on what the recipient should do, why it matters, and how to verify success → Use positive language → Provide concrete examples.

**If you need to improve existing instructions:** Convert negative statements to positive guidance → Add specific success criteria → Remove unnecessary content.

**If you need to verify instruction quality:** Check for clarity, actionability, and verifiable outcomes.

## Core Principles

### Positive Direction

Tell recipients what TO do, not just what NOT to do.

| Less Effective | More Effective |
| :--- | :--- |
| "Never use inline styles" | "Use StyleSheet.create for better performance" |
| "Don't commit secrets" | "Keep sensitive data in environment variables" |
| "Avoid blocking operations" | "Use async patterns for responsiveness" |

**Why it works:** Positive guidance provides clear direction and reasoning, not just prohibitions.

### Specific Evidence

Define success with concrete, verifiable outcomes.

| Vague | Specific |
| :--- | :--- |
| "The code works" | "Tests pass (12/12, Exit Code 0)" |
| "Files updated" | "Modified 3 files: main.ts, config.ts, tests/" |
| "Configuration valid" | "Config validated: all required fields present" |

**Why it works:** Specific evidence leaves no ambiguity about completion.

### Essential Content

Include only what recipients need to know. Remove what's obvious or already understood.

| Remove | Keep |
| :--- | :--- |
| Generic explanations | Project-specific decisions |
| Obvious conventions | Non-obvious trade-offs |
| Detailed tutorials | Verification criteria |
| Historical context | Security constraints |

**Why it works:** Focus prevents overwhelming the recipient with noise.

### Clear Structure

Organize for scannability with logical flow.

| Approach | When to Use |
| :--- | :--- |
| Quick start guide | Complex processes with common entry points |
| Thematic sections | Multiple distinct topics |
| Step-by-step workflows | Linear procedures |
| Reference format | Lookup-oriented content |

**Why it works:** Structure helps recipients find what they need quickly.

---

## Communication Patterns

### Positive Framing Formula

Transform constraints into constructive guidance:

```
[Avoided behavior] → [Preferred action] + [Reason/benefit]
```

Examples:
- "Never use callbacks" → "Use async/await for more readable code"
- "Don't hardcode values" → "Use configuration files for environment-specific values"
- "Avoid monoliths" → "Structure code in modules for better maintainability"

### Evidence-Based Claims

Support assertions with verifiable information:

```markdown
## Success Criteria

| Claim | Evidence |
| :--- | :--- |
| Tests pass | Test output with exit code |
| Code reviewed | PR approved and merged |
| Build succeeds | Build artifact created |
| Documentation complete | All modules documented |
```

### Context-Specific Guidance

Tailor instructions to the recipient's situation:

| Audience | Adjust |
| :--- | :--- |
| **Beginners** | More explanations, examples, and context |
| **Experts** | Concise, assume prior knowledge |
| **Cross-team** | Explain your team's context clearly |
| **Public** | Self-contained, no internal references |

---

## Common Patterns

### Anti-Patterns to Avoid

| Mistake | Better Approach |
| :--- | :--- |
| **Negative-only** | "Don't do X" → "Use Y instead for benefit" |
| **Verbose** | Remove obvious explanations and justifications |
| **Vague** | Add specific evidence requirements |
| **Over-specified** | Provide outcomes, not step-by-step scripts |
| **Duplicated** | Define once, reference elsewhere |

### Effective Examples

**Writing Style:**

❌ Verbose: "In order to ensure that your code maintains high quality standards, you should run the linter before committing..."
✅ Concise: "Run linter before committing to catch issues early."

**Constraints:**

❌ Negative: "Important: Never use inline styles in production code."
✅ Positive: "Use StyleSheet.create for better performance and maintainability."

**Verification:**

❌ Vague: "Ensure all tests pass before continuing."
✅ Specific: "Run `npm test` and verify all tests pass (Exit Code 0)."

---

## Iterative Refinement

Instructions improve through cycles of observation and adjustment.

### Improvement Cycle

1. **Observe** - Note where instructions are unclear or ignored
2. **Analyze** - Determine root cause of confusion
3. **Revise** - Rewrite problematic sections with clarity
4. **Test** - Verify instructions are followed correctly
5. **Document** - Record successful patterns for future

### Feedback Signals

| Signal | Action |
| :--- | :--- |
| Recurring questions | Add clarification or examples |
| Common mistakes | Strengthen guidance or add warnings |
| Instructions ignored | Check relevance and clarity |
| Confusion reported | Simplify language or structure |

---

## Recognition Questions

Evaluate instruction quality by asking:

| Question | Purpose |
| :--- | :--- |
| Is the outcome clear? | Recipient knows what success looks like |
| Is the language positive? | Guidance directs toward preferred actions |
| Is verification possible? | Success can be objectively confirmed |
| Is the content essential? | Everything included serves a clear purpose |
| Is the structure logical? | Information is easy to navigate |
| Is the scope appropriate? | Content matches recipient's knowledge level |

---

## Examples: Good vs Bad

### Technical Instructions

**BAD:**
```markdown
## Code Style Guidelines

Please make sure to follow all the best practices for writing clean code. You should use meaningful variable names and write functions that do one thing. Also, add comments where the code is complex.
```

**GOOD:**
```markdown
## Code Style

- Use descriptive variable names that indicate purpose
- Write functions focused on single responsibility
- Add comments for complex logic only
- Run linter before committing: `npm run lint`
```

---

### Workflow Instructions

**BAD:**
```markdown
## Deployment Process

We need to deploy the application carefully. First build the Docker image, then push it to the registry, then update the Kubernetes configuration. Make sure to test after each step.
```

**GOOD:**
```markdown
## Deployment Process

1. Build: `docker build -t app:latest .`
2. Push: `docker push app:latest`
3. Update: `kubectl apply -f deployment.yaml`
4. Verify: `kubectl rollout status deployment/app`
```

---

### Requirements Definition

**BAD:**
```markdown
## Requirements

The system should be fast and secure. It needs to handle user data properly and scale well.
```

**GOOD:**
```markdown
## Requirements

- **Performance:** Respond to requests within 200ms (p95)
- **Security:** Encrypt data at rest and in transit; validate all inputs
- **Scalability:** Handle 10,000 concurrent users
- **Data:** Persist user data for 7 years; comply with GDPR
```

---

## Context-Specific Guidance

### For Different Recipients

| Context | Approach | Example |
| :--- | :--- | :--- |
| **Onboarding** | Include rationale and context | "Use modules for better code organization..." |
| **Reference** | Concise, assume familiarity | "Use module system: `import { X } from 'package'`" |
| **Emergency** | Direct, actionable steps | "To rollback: `kubectl rollout undo deployment/app`" |
| **Cross-team** | Explain your terms | "Use our shared logging library (see docs/logging/)" |

### For Different Project Types

| Project Type | Focus Areas |
| :--- | :--- |
| **Software** | Commands, workflows, verification |
| **Research** | Methodology, reproducibility, documentation |
| **Infrastructure** | Configuration, state, security |
| **Libraries** | API usage, versioning, contributions |

---

## Common Pitfalls

### Over-Specification

Don't prescribe exact steps when outcomes matter more:

❌ "First create directory X, then create file Y, then add content Z..."
✅ "Create component with X, Y, and Z in the components/ directory."

### Under-Specification

Don't assume knowledge when specificity matters:

❌ "Follow best practices for error handling."
✅ "Use Result types for operations that can fail: `Result<T, E>` pattern."

### Context Assumption

Don't assume recipient knows your context:

❌ "Use the shared library like we discussed."
✅ "Use the shared utility library: `import { utils } from '@shared/utils'`"

### Missing Verification

Don't leave success ambiguous:

❌ "Implement the feature and test it."
✅ "Implement feature; verify with tests; document API changes."

---

## Verification Methods

Different types of claims require different verification approaches.

### Code and Systems

| Claim | Verification |
| :--- | :--- |
| Functionality works | Test output, manual verification |
| Performance meets target | Benchmarks, profiling data |
| Security standards met | Security scan results, audit reports |
| Type safety maintained | Compiler output, linter results |

### Processes and Workflows

| Claim | Verification |
| :--- | :--- |
| Process followed | Checklist completed, steps documented |
| Compliance achieved | Audit results, certification obtained |
| Documentation complete | All modules documented, examples provided |

### Configuration

| Claim | Verification |
| :--- | :--- |
| Settings correct | Configuration validation, successful startup |
| Secrets managed | No secrets in code, env vars used |
| Permissions correct | Access tests, permission checks |

---

## Learning from Feedback

Instructions improve when you pay attention to how they're used.

### What Recurring Questions Tell You

| Question Pattern | Likely Issue | Fix |
| :--- | :--- | :--- |
| "Where do I start?" | Entry point unclear | Add quick start guide |
| "How do I verify X?" | Success criteria vague | Add specific verification |
| "Can I use Y instead?" | Constraint too rigid | Explain principles, allow flexibility |
| "What does this mean?" | Jargon or concept unclear | Simplify language or add examples |

### What Ignored Instructions Tell You

| Ignored Section | Likely Reason | Fix |
| :--- | :--- | :--- |
| Style guidelines | Not enforced | Add verification or linter |
| Workflow steps | Too complex | Simplify or automate |
| Background info | Not actionable | Remove or move to appendix |
| Examples | Not relatable | Use project-specific examples |

---

## Structure Best Practices

### Effective Organization

**Match structure to purpose:**

| Purpose | Structure |
| :--- | :--- |
| **Quick reference** | Bullet points, tables, concise |
| **Learning** | Explanations with examples |
| **Procedures** | Numbered steps, decision points |
| **Reference** | Searchable, cross-referenced |

**Signal important information:**

| Technique | Usage |
| :--- | :--- |
| **Placement** | Put critical information early |
| **Emphasis** | Use formatting for importance (bold, tables) |
| **Repetition** | State critical points in multiple ways |
| **Examples** | Illustrate abstract principles concretely |

### Navigation Aids

Help readers find what they need:

| Aid Type | When Useful |
| :--- | :--- |
| **Table of contents** | Long documents with multiple sections |
| **Section headers** | Scanning for specific topics |
| **Cross-references** | Related information in other sections |
| **Index/glossary** | Technical terms or acronyms |
| **Quick start** | Getting started quickly |

---

## Writing Techniques

### Clarity Techniques

| Technique | Example |
| :--- | :--- |
| **Imperative mood** | "Create file" not "You should create" |
| **Active voice** | "Run tests" not "Tests should be run" |
| **Present tense** | "The build creates artifacts" not "The build will create" |
| **Specific nouns** | "Users" not "end-users", "clients" not "client-side" |

### Precision Techniques

| Technique | Example |
| :--- | :--- |
| **Concrete verbs** | "Implement" not "handle", "process" |
| **Numbers over words** | "3 files" not "several files" |
| **Exact values** | "200ms limit" not "fast response" |
| **File paths** | "src/config.ts" not "the config file" |

### Brevity Techniques

| Technique | Example |
| :--- | :--- |
| **Remove filler** | Delete "in order to", "for the purpose of" |
| **Simplify explanations** | Keep one sentence per concept |
| **Use lists** | Replace paragraph with bullet points |
| **Trust knowledge** | Don't explain what recipient knows |

---

## Quality Indicators

### Signs of Effective Instructions

| Indicator | Example |
| :--- | :--- |
| **Questions decrease** | Recurring questions stop after clarification |
| **Compliance increases** | Instructions followed consistently |
| **Errors decrease** | Common mistakes become rare |
| **Onboarding faster** | New users become productive quickly |
| **Ambiguity rare** | Few requests for clarification |

### Signs of Problematic Instructions

| Indicator | Example |
| :--- | :--- |
| **Questions repeat** | Same questions asked repeatedly |
| **Workarounds emerge** | People create their own processes |
| **Sections skipped** | Parts of instructions consistently ignored |
| **Confusion common** | Frequent clarification requests |
| **Outdated info** | Instructions describe old processes |

---

## Recognition Questions

Use these questions to evaluate instruction quality:

| Question | Why It Matters |
| :--- | :--- |
| **Is the outcome clear?** | Recipient knows what success looks like |
| **Is the language positive?** | Guidance directs toward preferred actions |
| **Is verification possible?** | Success can be objectively confirmed |
| **Is the scope appropriate?** | Content matches recipient's needs and knowledge |
| **Is the structure logical?** | Information flows naturally |
| **Is the tone right?** | Language is appropriate for context |
| **Can it evolve?** | Format allows for updates and growth |
