---
name: pragmatic-guard
description: Enables and configures Pragmatic Guard Mode (YAGNI Enforcement) to prevent over-engineering. Use when the user requests "Enable pragmatic mode", "Turn on YAGNI enforcement", "Activate simplicity guard", "Challenge complexity", or similar phrases.
allowed-tools: Read,Edit
---

# Pragmatic Guard Mode

Enables and configures the Pragmatic Guard Mode to actively challenge over-engineering.

## Process

### 1. Check Current Configuration
- Read `.architecture/config.yml` to check current settings
- If config.yml doesn't exist, offer to create it from `.architecture/templates/config.yml`
- Check if `pragmatic_mode.enabled` is true
- Note the intensity level (strict/balanced/lenient)
- Review exemption categories and triggers

### 2. Enable Pragmatic Mode (if requested)
If user wants to enable:
- If config.yml doesn't exist:
  ```bash
  cp .architecture/templates/config.yml .architecture/config.yml
  ```
- Set `pragmatic_mode.enabled: true`
- Confirm intensity level with user or use default (balanced)
- Create `.architecture/deferrals.md` from template if it doesn't exist:
  ```bash
  cp .architecture/templates/deferrals.md .architecture/deferrals.md
  ```
- Inform user about mode activation and current settings

### 3. Configure Intensity Level
Ask user which intensity they prefer if not specified:

**Strict Mode**:
- Challenges aggressively, requires strong justification for any complexity
- Questions every "should" and "could"
- Pushes for absolute minimal implementation
- Best for: New projects, MVPs, startups with limited resources

**Balanced Mode** (RECOMMENDED):
- Challenges thoughtfully, accepts justified complexity
- Seeks middle ground between simplicity and best practices
- Questions "should" but accepts reasonable "must"
- Best for: Most projects, growing teams, moderate complexity

**Lenient Mode**:
- Raises concerns without blocking
- Suggests simpler alternatives as options
- Focuses on major complexity additions only
- Best for: Established projects, teams with strong architecture practices

### 4. Configure Triggers (optional)
Ask if user wants to customize which situations trigger pragmatic analysis:
- New abstraction layers (interfaces, base classes, DI containers)
- New external dependencies (libraries, frameworks, services)
- New architectural patterns (repository, strategy, observer)
- Scope expansion beyond initial requirements
- Performance optimizations without evidence
- Test infrastructure upfront
- Flexibility/configurability additions

### 5. Configure Exemptions (optional)
Confirm exemption categories where best practices should be maintained:
- Security-critical features (always exempt by default)
- Data integrity (always exempt by default)
- Compliance requirements (always exempt by default)
- Accessibility (always exempt by default)

### 6. Understanding the Pragmatic Enforcer
Explain how the Pragmatic Enforcer will participate:

**In Architecture Reviews**:
- Reviews each architect's recommendations
- Applies necessity assessment (0-10 scoring)
- Applies complexity assessment (0-10 scoring)
- Proposes simpler alternatives
- Calculates pragmatic score (complexity/necessity ratio, target <1.5)

**In ADR Creation**:
- Challenges proposed decisions
- Questions whether complexity is justified by current needs
- Suggests phased approaches or deferrals
- Documents trigger conditions for deferred decisions

**Question Framework**:
- **Necessity**: "Do we need this right now?" "What breaks without it?"
- **Simplicity**: "What's the simplest thing that could work?"
- **Cost**: "What's the cost of implementing now vs waiting?"
- **Alternatives**: "What if we just...?" "Could we use existing tools?"
- **Best Practices**: "Does this best practice apply to our context?"

### 7. Deferrals Tracking
If `behavior.track_deferrals` is true:
- Maintain `.architecture/deferrals.md` with deferred decisions
- Include trigger conditions for each deferral
- Track when deferrals are implemented or remain deferred

### 8. Report to User
```
Pragmatic Guard Mode: [Enabled | Disabled]

Configuration:
- Intensity: [strict | balanced | lenient]
- Apply to: [List of phases where it applies]
- Deferrals tracking: [enabled | disabled]

Exemptions:
- Security-critical: [enabled | disabled]
- Data integrity: [enabled | disabled]
- Compliance: [enabled | disabled]
- Accessibility: [enabled | disabled]

Triggers:
[List of active triggers]

The Pragmatic Enforcer will now:
- Challenge recommendations from other architects
- Question complexity and abstractions
- Propose simpler alternatives
- Calculate pragmatic scores (target ratio <1.5)
- [If enabled] Track deferred decisions in .architecture/deferrals.md

Next Steps:
- Create an ADR: "Create ADR for [topic]" (will include pragmatic analysis)
- Start a review: "Start architecture review for [target]" (will include pragmatic challenges)
- Adjust settings: Edit .architecture/config.yml
```

## When to Use Pragmatic Mode

**Enable for**:
- New projects or MVPs
- Teams prone to over-engineering
- Resource-constrained environments
- Learning environments (teaching YAGNI)
- Projects with tight deadlines

**Consider disabling for**:
- Mature systems with established patterns
- High-complexity domains requiring abstractions
- Teams already practicing strong YAGNI principles
- Projects with specific architectural requirements

## Notes
- Pragmatic mode is about finding balance, not blocking progress
- The Pragmatic Enforcer's role is to question and challenge, not to veto
- Intensity level should match team maturity and project complexity
- Exemptions ensure critical areas maintain appropriate rigor
- Deferrals can always be implemented when triggered by actual needs
