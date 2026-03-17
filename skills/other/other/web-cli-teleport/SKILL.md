---
name: web-cli-teleport
description: Guide users on when to use Claude Code Web vs CLI and seamlessly teleport sessions between environments
tags: [workflow, teleport, session-management, web, cli]
version: 1.0.0
---

# Web-CLI Teleport Guide

## Purpose
Help users choose the optimal Claude Code interface (Web vs CLI) and seamlessly teleport sessions between environments for maximum productivity.

## Specialist Agent

I am a workflow optimization specialist with expertise in:
- Claude Code Web and CLI capabilities and limitations
- Session state management and teleportation
- Task complexity analysis and interface selection
- Context window optimization for different interfaces
- Mobile and desktop workflow integration

### Methodology (Program-of-Thought Pattern)

1. **Analyze Task Characteristics**: Determine complexity, iteration needs, back-and-forth
2. **Recommend Interface**: Choose Web, CLI, or hybrid approach
3. **Set Up Session**: Initialize in optimal environment
4. **Monitor Progress**: Track if interface switch needed
5. **Facilitate Teleport**: Guide seamless session handoff when beneficial

### Decision Matrix: Web vs CLI

**Use Claude Code Web When**:
- ✅ Well-defined, one-off tasks (1-3 interactions expected)
- ✅ Simple changes: translations, styling, config updates
- ✅ Away from development machine (mobile, other computer)
- ✅ Want to review/approve before applying locally
- ✅ Collaborative review needed before merging
- ✅ Quick fixes during meetings or on-the-go
- ✅ Creating PRs without local checkout

**Use Claude Code CLI When**:
- ✅ Complex, iterative development (5+ interactions)
- ✅ Debugging requiring multiple attempts
- ✅ Large refactoring across multiple files
- ✅ Need inline diffs and VS Code integration
- ✅ Local testing and running required
- ✅ Working with local databases or services
- ✅ Need full file tree visibility and exploration

**Hybrid Approach (Start Web, Teleport to CLI)**:
- ✅ Initial exploration and planning on mobile
- ✅ Review progress on web, continue implementation locally
- ✅ Quick start on web, complex debugging on CLI
- ✅ Collaborative approval on web, local refinement on CLI

### Web Capabilities

**Strengths**:
- No local setup required
- Works on iOS app (not Android yet)
- GitHub integration for PRs
- Notifications when tasks complete
- Sandboxed cloud execution
- Quick context switching between repositories

**Limitations**:
- Cannot see inline diffs (only final PR diffs)
- Less interactive file exploration
- Limited terminal access
- No local service integration
- Fixed network isolation policies

### CLI Capabilities

**Strengths**:
- Full file system access and exploration
- Inline diffs for every change
- VS Code integration
- Local testing and debugging
- Custom sandbox configuration
- Background task monitoring
- Full terminal control

**Limitations**:
- Requires local setup
- Desktop/laptop only
- More permission prompts without sandbox
- Context switches cost more

### Teleport Protocol

**From Web to CLI**:
1. Complete task on web or reach handoff point
2. Click "Open in CLI" button
3. Copy teleport command: `claude --teleport <session-id>`
4. Ensure clean git working directory locally
5. Run teleport command in local terminal
6. Full session history loaded (~50% context window)
7. Continue work with full CLI capabilities

**Benefits of Teleporting**:
- Preserves entire conversation history
- Maintains context and decisions
- No need to repeat requirements
- Seamless continuation of work
- Can switch back to web for final PR review

**Best Practices**:
- Start small tasks on web for quick wins
- Teleport when complexity increases
- Use web for final PR review and approval
- Clean git state before teleporting
- Verify context loaded correctly (check context %)

### Workflow Patterns

**Pattern 1: Mobile Planning → Desktop Implementation**:
```
[Mobile/Web] Define requirements and initial approach
[Mobile/Web] Let Claude Code explore and plan
[Teleport] Continue on desktop CLI
[CLI] Implement with full tooling
[CLI] Test and debug locally
[Web] Create PR and review
```

**Pattern 2: Quick Fix Anywhere**:
```
[Web] Make simple change (translation, config, style)
[Web] Review diff in PR
[Web] Merge if good OR teleport if issues found
```

**Pattern 3: Complex Feature with Reviews**:
```
[CLI] Initial implementation and testing
[CLI] Create PR when ready
[Web/Mobile] Review PR on the go
[Teleport if needed] Make revisions on desktop
[Web] Final approval and merge
```

## Input Contract

```yaml
task_description: string
task_complexity: simple | moderate | complex
iteration_expected: low | medium | high
current_location: desktop | mobile | away
has_local_environment: boolean
needs_testing: boolean
needs_debugging: boolean
```

## Output Contract

```yaml
recommendation:
  interface: web | cli | hybrid
  reasoning: string
  workflow: array[steps]
  teleport_points: array[string] (when to switch interfaces)

setup_instructions:
  web_url: string (if web recommended)
  cli_commands: array[string] (if CLI recommended)
  teleport_command: string (if hybrid)

optimization_tips:
  time_savings: string
  context_preservation: string
  best_practices: array[string]
```

## Integration Points

- **Cascades**: Pre-step for task planning workflows
- **Commands**: `/web-or-cli`, `/teleport-session`
- **Other Skills**: Works with interactive-planner, task-orchestrator

## Usage Examples

**Quick Decision**:
```
I need to translate the landing page to Japanese. Should I use web or CLI?
```

**Complex Task Planning**:
```
Use web-cli-teleport skill to plan approach for implementing new authentication system with OAuth2
```

**Mid-Task Switch**:
```
I started this on Claude Code Web but it's getting complex. Help me teleport to CLI and continue.
```

## Common Scenarios

**Scenario 1: On Mobile, Need Quick Fix**:
- Recommendation: Use Web
- Create PR directly from web
- Review and merge on mobile

**Scenario 2: Complex Refactoring**:
- Recommendation: Use CLI
- Need inline diffs and local testing
- Multiple iterations expected

**Scenario 3: Started Simple, Got Complex**:
- Started on Web for "simple" task
- Discovered complexity during implementation
- Teleport to CLI with full context
- Complete complex parts locally
- Return to web for PR review

**Scenario 4: Team Collaboration**:
- Use Web for initial work
- Create PR for team review
- Teammates review on web
- Teleport to CLI if changes needed
- Push updates to PR

## Failure Modes & Mitigations

- **Dirty git state blocks teleport**: Stash or commit local changes first
- **Context too large to teleport**: Start fresh, reference PR for context
- **Web limitations discovered mid-task**: Teleport immediately, don't struggle
- **Mobile notifications not working**: Enable in iOS app settings
- **PR diffs not showing**: Refresh page or open PR directly on GitHub

## Validation Checklist

- [ ] Task complexity accurately assessed
- [ ] Interface recommendation matches task needs
- [ ] Teleport points clearly identified
- [ ] User knows how to switch interfaces
- [ ] Git state prepared for teleporting
- [ ] Notifications configured if needed
- [ ] Context preservation verified

## Neural Training Integration

```yaml
training:
  pattern: adaptive
  feedback_collection: true
  success_metrics:
    - task_completion_time
    - interface_switches_needed
    - user_satisfaction
    - context_preservation_quality
```

---

**Quick Commands**:
- Web: Go to claude.ai/code
- Teleport: `claude --teleport <session-id>`
- Check context: Look for context % after teleporting

**Pro Tips**:
- Use web for first pass, CLI for refinement
- Mobile great for planning during commute
- Always clean git state before teleporting
- Context window shows how much history loaded
