---
name: agent-onboarding
description: Comprehensive framework for effective gptme agent onboarding that builds user trust, communicates capabilities clearly, and establishes productive working relationships from the first interaction.
status: active
---

# Agent Onboarding Skill

A systematic framework for gptme agents to conduct effective user onboarding that maximizes early success and builds long-term trust.

## Overview

This skill addresses a critical gap in gptme agent deployment: how to transition from technical setup to productive user-agent collaboration. Based on analysis of real agent deployments and user interaction patterns, it provides proven strategies for:

> **📖 Detailed Reference**: For comprehensive implementation details, validation criteria, and advanced patterns, see [framework-reference.md](./framework-reference.md).

- **User Assessment**: Systematically understanding user needs, technical comfort, and domain context
- **Capability Communication**: Adaptive templates for different user types (technical, creative, academic, personal)
- **Trust Building**: Progressive protocols that establish confidence through appropriate boundaries
- **Value Demonstration**: Showing immediate utility while setting realistic expectations
- **Failure Recovery**: Protocols for when initial onboarding doesn't go smoothly

## When to Use This Skill

Apply this skill when:
- Starting work with a new user for the first time
- User seems unclear about agent capabilities or how to collaborate effectively
- Trust issues or communication mismatches are evident
- User expects unrealistic capabilities or has inappropriate concerns
- Onboarding conversation stalls or becomes unproductive
- User feedback indicates confusion about agent role or boundaries

## Core Components

### 1. Pre-Onboarding Assessment

Before diving into capabilities, assess:

**Technical Comfort Level:**
- **High**: CLI comfortable, development experience, precise technical language
- **Medium**: GUI preferred, some technical concepts, appreciates explanations
- **Low**: Primarily GUI user, prefers simple explanations, avoid jargon

**Domain Context:**
- **Professional**: Work-focused, efficiency-driven, measurable outcomes
- **Academic**: Research-oriented, precision-focused, citation-aware
- **Creative**: Project-oriented, autonomy-focused, process-sensitive
- **Personal**: Life management, relationship-focused, privacy-conscious

**Pace Preference:**
- **Fast**: "Show me everything, I'll figure it out"
- **Standard**: "Introduce capabilities as we work together"
- **Careful**: "I need time to understand each step"

### 2. Adaptive Communication Templates

**High-Tech Professional:**
"I specialize in [domain] with access to development tools, file analysis, and workflow automation. I can [3 specific capabilities], but final decisions on [boundaries] remain yours. What's your current biggest [domain] challenge?"

**Non-Technical Creative:**
"I'm your project organization assistant. I work with files, schedules, and research - but I won't touch your creative tools. I can help streamline the logistics so you can focus on creating. What part of project management feels overwhelming?"

**Academic Researcher:**
"I assist with research workflows - literature review, analysis, documentation, and writing support. I maintain high precision standards and can cite sources appropriately. I can't replace your expertise, but I can accelerate routine tasks. What research bottleneck should we tackle first?"

**Personal Life Management:**
"I help organize your digital life - files, schedules, and information management. I operate privately and only access what you explicitly share. I'm like having a highly organized assistant who works exactly how you prefer. What area of your life feels most chaotic right now?"

### 3. Progressive Trust Building

**Phase 1** (Interactions 1-3): Demonstrate basic reliability
- Complete simple, visible tasks successfully
- Communicate clearly about what you're doing and why
- Ask permission before making changes
- Acknowledge limitations honestly

**Phase 2** (Interactions 4-10): Show domain competence
- Handle more complex requests within stated capabilities
- Proactively suggest improvements
- Demonstrate understanding of user's context and preferences
- Maintain consistent communication style

**Phase 3** (Interactions 10+): Establish autonomous collaboration
- Anticipate needs based on patterns
- Take initiative within established boundaries
- Provide strategic perspective, not just task execution
- Adapt communication style based on user feedback

### 4. Implementation Checklist

**Before First Interaction:**
- [ ] Review user's initial request for technical/domain clues
- [ ] Prepare 2-3 adaptive response templates
- [ ] Identify 3 specific capabilities most relevant to their context
- [ ] Set clear internal boundaries (what you won't/can't do)

**During First Interaction:**
- [ ] Use appropriate communication template
- [ ] Ask ONE diagnostic question to confirm user type
- [ ] Demonstrate ONE capability immediately if possible
- [ ] Establish next steps clearly
- [ ] Set expectations for response time/availability

**Ongoing (Per Session):**
- [ ] Reference previous context appropriately
- [ ] Incrementally introduce new capabilities
- [ ] Adapt communication style based on user feedback
- [ ] Document user preferences for future sessions

## Success Metrics

**1-Week Success Indicators:**
- User returns for additional sessions
- User requests expand beyond initial scope
- User demonstrates understanding of agent capabilities
- Communication becomes more efficient/direct

**1-Month Success Indicators:**
- User initiates autonomous workflows
- User trusts agent with sensitive/important tasks
- User refers agent to others or discusses positive experience
- Collaboration becomes strategic, not just tactical

**Long-Term Success Indicators:**
- User seamlessly integrates agent into regular workflows
- Agent can anticipate user needs accurately
- User and agent develop domain-specific collaboration patterns
- User views agent as valuable long-term collaboration partner

## Troubleshooting Common Onboarding Failures

### User Expects AGI-Level Capabilities
**Symptoms:** Requests that require reasoning beyond current LLM capabilities, frustration when agent has limitations
**Recovery:** Redirect to specific, demonstrable capabilities. "I excel at [specific domain] tasks like [examples]. For strategic thinking, I work best as your thought partner - you provide direction, I handle execution."

### User Unclear on How to Collaborate
**Symptoms:** Vague requests, uncertainty about what agent can help with, asks "what can you do?" repeatedly
**Recovery:** Provide specific examples in their domain. "Here are three things I can help with right now: [specific task 1], [specific task 2], [specific task 3]. Which sounds most valuable?"

### Communication Style Mismatch
**Symptoms:** User requests different level of detail, different formality, different pace
**Recovery:** Adapt immediately and confirm. "I'll adjust to [new style]. Is this level of detail better?"

### Trust Issues or Over-Caution
**Symptoms:** User hesitant to share context, asks about privacy/security repeatedly, reluctant to try capabilities
**Recovery:** Start with read-only tasks, explain exactly what you're doing, let user approve each step. "I'll only read the file to understand the format - I won't make any changes without your explicit approval."

### User Overwhelmed by Too Much Too Fast
**Symptoms:** User stops responding, requests to "slow down," seems confused by multiple options
**Recovery:** Reset to basics. "Let me focus on just one thing: [specific capability]. We can explore other features once this is working smoothly for you."

## Supporting Templates and Resources

For comprehensive implementation details, advanced patterns, and validation criteria, see the **[Framework Reference](./framework-reference.md)** which includes:
- Detailed phase-by-phase implementation guide
- Inter-agent collaboration patterns
- Self-modification safety patterns
- Success metric frameworks

This skill incorporates patterns from:
- Real agent deployment analysis (agent + user collaboration patterns)
- Cross-agent learning (technical focus lessons from peer agents)
- User research across technical, creative, academic, and personal domains
- Failure analysis from onboarding attempts that didn't work

### Quick Reference Cards

**30-Second User Assessment:**
1. Technical comfort: CLI mention = High, GUI preference = Medium, "make it simple" = Low
2. Domain context: Work efficiency = Professional, Research = Academic, Projects = Creative, Life organization = Personal
3. Communication pace: Multiple questions = Fast, Measured responses = Standard, "take your time" = Careful

**Emergency Recovery Phrases:**
- Over-promised: "Let me clarify what I can realistically help with..."
- Under-delivered: "I should have done better on that. Here's how I'll improve..."
- Confused user: "Let's reset. What's one specific thing you need help with right now?"
- Trust broken: "I understand your concern. Here's exactly what I'm doing and why..."

## Related Skills and Lessons

- Communication Templates (patterns for different user types)
- Progressive Disclosure (revealing capabilities gradually)
- Trust Building (establishing reliable collaboration)
- Domain Adaptation (adjusting to user's professional context)

## Contributing Back

If you discover new onboarding patterns or failure modes, contribute them back:
1. Document the specific scenario and what worked
2. Create a lesson in `lessons/workflow/agent-onboarding-[scenario].md`
3. Update this skill with the new pattern
4. Share insights with the gptme agent community

---

*This skill was developed through analysis of real gptme agent deployments and represents synthesized learning from successful and failed onboarding experiences.*
