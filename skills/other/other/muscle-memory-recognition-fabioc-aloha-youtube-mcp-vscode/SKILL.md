---
name: "Muscle Memory Recognition"
description: "Identify opportunities to build automation scripts (muscles) from repetitive or heavy-lifting tasks"
---

# Muscle Memory Recognition

Expert in identifying when manual work should become automated scripts.

## Capabilities

- Recognize repetitive task patterns
- Identify heavy-lifting operations suitable for scripting
- Evaluate automation ROI (time saved vs creation effort)
- Recommend muscle creation with language/framework
- Connect new muscles to trifecta files

## When to Use This Skill

- Same task performed manually 3+ times
- Multi-step operations with consistent patterns
- Error-prone manual processes
- Time-consuming operations during conversation
- Complex file manipulation or validation

## Muscle Identification Signals

| Signal | Strength | Example |
|--------|----------|---------|
| **Repetition** (3+ occurrences) | 🔴 Strong | "Run these 5 commands again" |
| **Multi-step sequence** (4+ steps) | 🔴 Strong | "Create folder, copy files, update config, validate" |
| **Error-prone operations** | 🟡 Medium | "Format all files, check for inconsistencies" |
| **Time sink in conversation** | 🟡 Medium | Operations taking >30 seconds |
| **Cross-session recurrence** | 🔴 Strong | "We did this last session too" |
| **Validation patterns** | 🟡 Medium | "Check all X for Y property" |
| **Batch operations** | 🟡 Medium | "Do X to all files matching pattern" |

## Anti-Signals (Don't Automate)

| Signal | Reason |
|--------|--------|
| One-time operation | ROI too low |
| Requires human judgment each time | Can't be scripted reliably |
| Simple single command | Already optimal |
| Rapidly changing requirements | Script would be constantly outdated |
| Security-sensitive operations | Manual review required |

## Muscle Creation Decision Matrix

```
IF (repetition >= 3) AND (steps >= 2):
    → CREATE MUSCLE (high value)

IF (repetition >= 2) AND (error_prone = true):
    → CREATE MUSCLE (reliability value)

IF (time_per_execution > 1min) AND (expected_uses >= 5):
    → CREATE MUSCLE (time value)

IF (steps >= 5) AND (pattern_consistent = true):
    → CREATE MUSCLE (complexity value)

ELSE:
    → DEFER (observe for more signals)
```

## Language Selection Guide

### Comparison Matrix

| Factor | PowerShell | Node.js (JS/TS) | Python |
|--------|------------|-----------------|--------|
| **Windows native** | ✅ No runtime needed | ❌ Requires Node | ❌ Requires Python |
| **Cross-platform** | ⚠️ Works but quirks | ✅ Excellent | ✅ Excellent |
| **File operations** | ✅ Native cmdlets | ✅ Good with fs | ✅ Good with pathlib |
| **JSON handling** | ⚠️ `ConvertFrom-Json` | ✅ Native | ✅ Native |
| **Pipeline syntax** | ✅ Excellent | ❌ Requires chaining | ❌ Requires chaining |
| **Async operations** | ⚠️ Jobs (awkward) | ✅ Native async/await | ✅ asyncio |
| **npm ecosystem** | ❌ No | ✅ Full access | ❌ No (pip instead) |
| **Type safety** | ❌ No | ✅ TypeScript | ⚠️ Type hints |
| **Startup speed** | ✅ Fast | ⚠️ ~200ms Node init | ⚠️ Similar |
| **VS Code integration** | ⚠️ Limited | ✅ Extension API | ❌ No |

### Task-to-Language Mapping

| Task Pattern | Recommended | Reason |
|--------------|-------------|--------|
| File validation / scanning | **PowerShell** | `Get-ChildItem`, pipeline, regex built-in |
| JSON config manipulation | **Node.js** | Native JSON, better object handling |
| CLI tools with nice UX | **TypeScript** | chalk, inquirer, spinners |
| npm library usage | **Node.js** | Direct access to ecosystem |
| Quick one-off scripts | **PowerShell** | No build step, immediate |
| Cross-platform / heir-critical | **Node.js** | Portable across systems |
| API calls with types | **TypeScript** | fetch, async/await, type safety |
| Text/Markdown transforms | **Node.js** | String methods, regex literals |
| Audits with reporting | **PowerShell** | Format-Table, pipeline filtering |

### Decision Algorithm

```
IF (validation OR audit OR file-scanning):
    → PowerShell (pipeline + cmdlets shine here)

IF (JSON manipulation OR npm libraries needed):
    → Node.js (native JSON + ecosystem access)

IF (CLI tool with user interaction):
    → TypeScript (type safety + UX libraries like chalk)

IF (quick prototype OR Windows-only):
    → PowerShell (no setup required)

IF (cross-platform required OR heir-critical):
    → Node.js (portable, same behavior everywhere)
```

## Muscle Naming Convention

```
{action}-{target}.{ext}

Examples:
- validate-skills.ps1
- sync-architecture.js
- normalize-paths.ps1
- gamma-generator.js
- brain-qa.ps1
```

## Integration Checklist

When creating a new muscle:

- [ ] Create script in `.github/muscles/`
- [ ] Add to `inheritance.json` (master-only or inheritable)
- [ ] Update referencing trifecta files (skills/instructions/prompts)
- [ ] Add to `TRIFECTA-CATALOG.md` if part of trifecta
- [ ] Document invocation in referencing files
- [ ] Test from heir context if inheritable

## Example Prompts

- "We've done this 3 times now, should we script it?"
- "This validation takes forever, can we automate it?"
- "I keep making mistakes with these steps"
- "What muscles exist for this type of task?"
- "Should this be a muscle or stay manual?"

## Output Format

When identifying a muscle opportunity:

```markdown
## 💪 Muscle Opportunity Detected

**Task**: [Description of repetitive/heavy task]
**Signal**: [Which signal triggered this]
**Estimated Value**: [Time saved × Expected uses]

### Recommendation
- **Action**: Create muscle / Defer / Keep manual
- **Language**: [Recommended language]
- **Name**: [Suggested muscle name]
- **Location**: `.github/muscles/{name}`
- **Inheritance**: master-only / inheritable

### Implementation Notes
[Any specific considerations for this muscle]
```

## Related Skills

- [Bootstrap Learning](.github/skills/bootstrap-learning/SKILL.md) - Parent skill for learning-to-automation flow
- [Research-First Development](.github/skills/research-first-development/SKILL.md) - Research before building muscles
- [Architecture Health](.github/skills/architecture-health/SKILL.md) - Validate muscle integration

## Synapses

- **Bootstrap Learning** → This skill (enables): Learning identifies automation opportunities
- **This skill** → Trifecta System (produces): Muscles become part of trifectas
- **Deep Thinking** → This skill (informs): Complex analysis reveals automation patterns
