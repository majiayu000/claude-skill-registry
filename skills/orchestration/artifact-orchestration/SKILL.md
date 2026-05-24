---
name: artifact-orchestration
description: Orchestrate multi-agent artifact generation with the Primary Author → Parallel Reviewers → Synthesizer → Archive pattern. Use when relevant to the task.
---

# artifact-orchestration

Orchestrate multi-agent artifact generation with the Primary Author → Parallel Reviewers → Synthesizer → Archive pattern.

## Triggers

- "generate [artifact-type]"
- "create [SAD/test plan/deployment plan/requirements]"
- "draft [artifact]"
- "new [architecture/security/deployment] document"

## Purpose

This skill implements the core AIWG multi-agent documentation pattern that ensures high-quality artifacts through:
- Single primary author for consistency
- Parallel expert reviews for coverage
- Synthesis of feedback for conflict resolution
- Formal archival with metadata tracking

## Behavior

When triggered, this skill orchestrates:

1. **Artifact identification**:
   - Parse requested artifact type
   - Map to template and primary author
   - Identify required reviewers

2. **Workspace setup**:
   - Create `.aiwg/working/{type}/{name}/`
   - Initialize metadata via `artifact-metadata` skill
   - Load relevant template via `template-engine` skill

3. **Primary author dispatch**:
   - Launch primary author agent with template
   - Provide context (requirements, existing artifacts)
   - Receive draft v0.1

4. **Parallel review dispatch**:
   - Launch 3-5 reviewers via `parallel-dispatch` skill
   - Each reviewer analyzes from their perspective
   - Collect structured feedback

5. **Synthesis**:
   - Invoke Documentation Synthesizer agent
   - Merge feedback and resolve conflicts
   - Generate final artifact

6. **Archive**:
   - Move to `.aiwg/{category}/`
   - Update metadata to baselined
   - Update artifact index

## Artifact Configuration

### Software Architecture Document (SAD)

```yaml
artifact: software-architecture-document
template: analysis-design/software-architecture-doc-template
primary_author: architecture-designer
reviewers:
  - security-architect
  - test-architect
  - requirements-analyst
  - technical-writer
output: .aiwg/architecture/sad.md
```

### Test Plan

```yaml
artifact: test-plan
template: test/test-plan-template
primary_author: test-architect
reviewers:
  - security-auditor
  - requirements-analyst
  - devops-engineer
output: .aiwg/testing/test-plan.md
```

### Deployment Plan

```yaml
artifact: deployment-plan
template: deployment/deployment-plan-template
primary_author: deployment-manager
reviewers:
  - devops-engineer
  - security-architect
  - reliability-engineer
  - support-lead
output: .aiwg/deployment/deployment-plan.md
```

### Requirements Specification

```yaml
artifact: software-requirements-spec
template: requirements/srs-template
primary_author: requirements-analyst
reviewers:
  - domain-expert
  - system-analyst
  - test-architect
  - architecture-designer
output: .aiwg/requirements/srs.md
```

### Threat Model

```yaml
artifact: threat-model
template: security/threat-model-template
primary_author: security-architect
reviewers:
  - privacy-officer
  - architecture-designer
  - devops-engineer
output: .aiwg/security/threat-model.md
```

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────┐
│ 1. SETUP                                                │
│    • Create workspace: .aiwg/working/{type}/{name}/     │
│    • Initialize metadata.json                           │
│    • Load template                                      │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 2. PRIMARY AUTHOR                                       │
│    • Dispatch: architecture-designer (for SAD)          │
│    • Input: template, requirements, context             │
│    • Output: drafts/v0.1-primary.md                     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 3. PARALLEL REVIEW (single message, multiple agents)    │
│    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │
│    │ security-    │ │ test-        │ │ requirements-│  │
│    │ architect    │ │ architect    │ │ analyst      │  │
│    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘  │
│           │                │                │          │
│           ▼                ▼                ▼          │
│    reviews/security.md  reviews/test.md  reviews/req.md│
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 4. SYNTHESIS                                            │
│    • Dispatch: documentation-synthesizer                │
│    • Input: draft + all reviews                         │
│    • Output: synthesis/final.md                         │
│    • Conflicts: document with rationale                 │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 5. ARCHIVE                                              │
│    • Move to: .aiwg/{category}/{artifact}.md            │
│    • Update metadata: status=baselined, version=1.0.0   │
│    • Archive workspace to: .aiwg/archive/{date}/        │
└─────────────────────────────────────────────────────────┘
```

## Usage Examples

### Generate SAD

```
User: "Create the Software Architecture Document"

Skill orchestrates:
1. Setup workspace for SAD
2. Dispatch architecture-designer with SAD template
3. Launch parallel reviews (security, test, requirements, writer)
4. Synthesize feedback
5. Archive to .aiwg/architecture/sad.md

Output:
"SAD generation complete.
Version: 1.0.0
Status: Baselined
Location: .aiwg/architecture/sad.md

Reviews:
✓ Security Architect: Approved with suggestions
✓ Test Architect: Approved
✓ Requirements Analyst: Approved
✓ Technical Writer: Approved (minor edits)

Conflicts resolved: 2
- Auth approach: Chose JWT per security recommendation
- Caching strategy: Balanced performance vs complexity"
```

### Generate with Context

```
User: "Generate deployment plan for production release"

Skill uses project-awareness context:
- Phase: Construction
- Environment: AWS
- Compliance: SOC2

Tailors template and reviewer focus accordingly.
```

## Configuration

### Custom Artifact Types

Add custom artifact configurations in `.aiwg/config/artifacts.yaml`:

```yaml
artifacts:
  custom-api-doc:
    template: custom/api-documentation
    primary_author: api-documenter
    reviewers:
      - security-auditor
      - api-designer
      - technical-writer
    output: .aiwg/architecture/api-docs/
```

### Review Depth

```yaml
review_config:
  depth: standard  # minimal, standard, comprehensive
  timeout: 300     # seconds per reviewer
  require_unanimous: false  # or true for critical artifacts
```

## Integration

This skill uses:
- `parallel-dispatch`: For launching reviewer agents
- `artifact-metadata`: For tracking artifact lifecycle
- `template-engine`: For loading and instantiating templates
- `project-awareness`: For context about current phase and state

## Error Handling

### Reviewer Timeout

If a reviewer times out:
1. Mark review as "incomplete"
2. Continue with other reviews
3. Flag in final synthesis
4. User can re-run partial review

### Conflicting Reviews

When reviewers disagree:
1. Document both positions
2. Apply priority rules:
   - Security concerns take precedence
   - Compliance concerns take precedence
   - Domain expert breaks ties
3. Record decision rationale in synthesis

### Missing Template

If template not found:
1. List similar templates
2. Offer to proceed with generic structure
3. Or abort with guidance

## Output Locations

| Artifact | Output Path |
|----------|-------------|
| SAD | .aiwg/architecture/sad.md |
| ADR | .aiwg/architecture/adr-{number}.md |
| Test Plan | .aiwg/testing/test-plan.md |
| Deployment Plan | .aiwg/deployment/deployment-plan.md |
| SRS | .aiwg/requirements/srs.md |
| Threat Model | .aiwg/security/threat-model.md |

## References

- Multi-agent pattern: docs/multi-agent-documentation-pattern.md
- Templates: templates/
- Agent definitions: agents/
