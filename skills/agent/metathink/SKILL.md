---
name: metathink
description: Metathink - Optimize Claude Code usage through metacognitive strategies. Use extended thinking, context engineering, task decomposition, and chain-of-thought prompting. Use when planning complex tasks, debugging difficult issues, making architectural decisions, or improving AI collaboration effectiveness.
version: "1.0.0"
last_updated: "2026-01-18"
---

# Metathink: Metacognitive Reasoning with Claude Code

Strategic framework for optimizing Claude Code effectiveness through metacognitive awareness—thinking about how you and Claude think together.

> **Metathink** = Thinking about thinking while coding

## When to Use This Skill

- **Complex architectural decisions** - Need deep reasoning about trade-offs
- **Difficult debugging** - Issues requiring multi-step investigation
- **Large refactoring tasks** - Planning before implementation critical
- **Learning new patterns** - Understanding "why" not just "what"
- **Session optimization** - Improving collaboration effectiveness
- **Context management** - Maintaining clean, relevant context
- **Quality improvement** - Moving beyond "metacognitive laziness"

## Quick Reference

### Trigger Extended Thinking

```bash
# In your prompts, use trigger words for deeper reasoning:
"think"         # ~4,000 token thinking budget
"think hard"    # ~10,000 tokens
"think harder"  # ~31,999 tokens (maximum)
"ultrathink"    # Maximum reasoning budget

# View Claude's internal reasoning
Ctrl+O          # Toggle verbose mode (gray italic text)
```

### Essential Commands

```bash
/clear          # Reset context between distinct tasks
Ctrl+O          # Toggle thinking visibility
/help           # Get Claude Code help
```

### Quick Metacognitive Checklist

Before any task:
1. **REFLECT** → What's the complexity? What context is needed?
2. **PLAN** → Enter plan mode? Use agent? Which skills?
3. **PROMPT** → High-level instructions, trigger thinking if needed
4. **MONITOR** → Use Ctrl+O to observe reasoning
5. **EVALUATE** → Review solutions, ask "why"
6. **ITERATE** → Clear context, refine approach

## Core Workflow

### 1. Metacognitive Task Assessment

**Before prompting Claude, ask yourself:**

| Question | Action |
|----------|--------|
| **How complex is this task?** | Simple = direct prompt; Complex = plan mode or "think harder" |
| **What domain does this involve?** | Database → `database-specialist`; Sentry → `sentry-fixer-agent` |
| **Do I need to explore first?** | Unknown codebase areas → explore agent |
| **Will this touch multiple files?** | Yes → Enter plan mode for user approval |
| **Are there multiple approaches?** | Yes → Use AskUserQuestion or plan mode |

### 2. Strategic Prompt Construction

**Context Engineering Strategies:**

```markdown
❌ BAD - Direct jump to implementation:
"Add user authentication"

✅ GOOD - Metacognitive approach:
"I need to add user authentication. First, research our existing auth patterns
and explore how other features handle authentication. Then think hard about
the best approach before proposing an implementation plan."
```

**Trigger Deep Reasoning When:**
- Architectural decisions required
- Multiple valid approaches exist
- Edge cases need consideration
- Performance optimization needed
- Security implications present

**Example Prompts:**

```markdown
# Trigger extended thinking
"Think harder about the trade-offs between these database indexing strategies"

# Request explicit reasoning
"Explain your reasoning step-by-step before implementing the RLS policy"

# Encourage exploration
"Research how our codebase handles file uploads, then plan the best approach"

# Plan before implementation
"Let's enter plan mode - I want to review your approach before coding"
```

### 3. Context Management

**The 2026 Shift: Context Engineering > Prompt Engineering**

| Strategy | Implementation | Benefit |
|----------|----------------|---------|
| **Clear frequently** | `/clear` between distinct tasks | Removes irrelevant context |
| **Just-in-time loading** | Load files/skills only when needed | Reduces token usage |
| **Progressive disclosure** | Start broad, drill down as needed | Maintains focus |
| **Skill injection** | Use skills for domain knowledge | On-demand expertise |
| **Agent delegation** | Use specialized agents for domains | Optimized reasoning |

**Practical Context Commands:**

```bash
# Clear context between tasks
/clear

# Use skills for just-in-time knowledge
# (No need to load full docs into context)
"Use the database-migration-manager skill to create this migration"

# Delegate to specialized agents
"Use the database-specialist agent to design this schema"

# Load specific context files when needed
"Read the CLAUDE.md file in apps/web/"
```

### 4. Task Decomposition Strategy

**Think metacognitively about task structure:**

```markdown
# Step 1: Identify task type
├─ Research/Exploration → Use explore agent, don't code yet
├─ Implementation → Enter plan mode first
├─ Bug Fix → Use Sentry agent or step-by-step debugging
└─ Database Work → Use database-specialist agent

# Step 2: Break down complexity
├─ Simple (1-2 files) → Direct prompt
├─ Medium (3-5 files) → Use TodoWrite to track steps
└─ Complex (5+ files, architecture) → Plan mode required

# Step 3: Choose collaboration strategy
├─ Need thinking visibility → Ctrl+O (verbose mode)
├─ Need deeper reasoning → Add "think harder"
└─ Need user input on approach → AskUserQuestion or plan mode
```

**Example: Decomposing Complex Task**

```markdown
User: "Optimize the event listing page performance"

Metacognitive Approach:
1. REFLECT: This is complex - involves DB queries, React rendering, caching
2. PLAN: Use explore agent first, then db-performance-agent
3. PROMPT: "First, explore how the event listing page works. Then use the
   db-performance-agent to scan for N+1 queries and performance issues.
   Think hard about optimization strategies before proposing changes."
4. MONITOR: Enable Ctrl+O to see reasoning about trade-offs
5. EVALUATE: Review proposed optimizations, ask about edge cases
6. ITERATE: Implement approved changes, measure improvements
```

### 5. Chain-of-Thought Prompting

**Encourage explicit reasoning:**

```markdown
# Request step-by-step thinking
"Before implementing, explain:
1. What approaches you considered
2. Why you chose this approach
3. What edge cases exist
4. What could go wrong"

# Ask for trade-off analysis
"Compare the pros/cons of using Redis vs in-memory cache for this feature"

# Require justification
"Why is this the best pattern for our codebase?"

# Seek alternatives
"What are 3 different ways to solve this? Which do you recommend and why?"
```

### 6. Monitoring Claude's Reasoning

**Use Ctrl+O to observe:**
- How Claude approaches problems
- What it considers important
- Where it self-corrects
- How it handles edge cases
- When it's uncertain

**Look for:**
- ✅ Systematic exploration of options
- ✅ Consideration of edge cases
- ✅ Self-correction when wrong
- ❌ Jumping to conclusions
- ❌ Missing obvious alternatives
- ❌ Not checking assumptions

**Intervene when needed:**
```markdown
"I see you're considering approach A, but what about approach B?"
"You mentioned edge case X - how would the solution handle that?"
"I notice you didn't check if that file exists - let's verify first"
```

### 7. Avoiding Metacognitive Laziness

**Research Warning:** Over-reliance on AI can cause "metacognitive laziness"—letting AI do all thinking while you disengage.

**Stay Cognitively Engaged:**

| ❌ Passive AI Use | ✅ Active Collaboration |
|------------------|------------------------|
| "Just fix it" | "Explain the issue first, then propose solutions" |
| Accept code without review | "Walk me through what this code does" |
| Skip reading plans | "Why did you choose this approach?" |
| Don't question suggestions | "Are there alternative approaches?" |
| Copy-paste without understanding | "Explain this pattern so I can use it elsewhere" |

**Maintain Your Metacognition:**
1. **Understand, don't just accept** - Ask "why" and "how"
2. **Review before approving** - Read plans, check reasoning
3. **Challenge assumptions** - "Did you consider X?"
4. **Learn patterns** - Build your own understanding
5. **Practice independent thinking** - Try solving before asking
6. **Verify outputs** - Test, don't blindly trust

## Common Patterns

### Pattern 1: Research-First Workflow

```markdown
# Instead of: "Add feature X"
# Use metacognitive approach:

"I need to add feature X. First:
1. Explore how similar features are implemented in our codebase
2. Research best practices for this pattern
3. Think hard about edge cases and security implications
4. Enter plan mode so I can review your approach before coding"
```

### Pattern 2: Debugging with Metacognition

```markdown
# Instead of: "Fix this bug"
# Use systematic approach:

"I'm seeing error Y. Before fixing:
1. Use the explore agent to understand the relevant code paths
2. Explain what you think is causing the error
3. Think through potential solutions and their trade-offs
4. Propose the safest fix with minimal side effects"
```

### Pattern 3: Architecture Decisions

```markdown
# For complex architectural choices:

"We need to decide between approach A and B. Please:
1. Research how our codebase handles similar patterns
2. Think harder about the long-term implications of each approach
3. Consider: maintainability, performance, security, scalability
4. Present pros/cons with your recommendation and reasoning"
```

### Pattern 4: Context-Aware Sessions

```markdown
# Manage context deliberately:

# Start of session
"Let's work on the authentication system. First, explore the current
implementation so we have shared context."

# Between tasks
"/clear"  # Clean slate for next task

# Before complex work
"Let me give you context on our auth requirements..."
# (Provide specific, relevant context)

# Load knowledge just-in-time
"Use the flutter-development skill for this mobile feature"
```

### Pattern 5: Progressive Understanding

```markdown
# Build understanding incrementally:

# Level 1: Broad overview
"What's the overall architecture of the event system?"

# Level 2: Specific component
"How does event creation work specifically?"

# Level 3: Deep dive
"Read the event creation service and explain the validation logic"

# Level 4: Implementation
"Now that we understand the patterns, let's add feature X following
the same approach"
```

## Advanced Strategies

### Model-Specific Optimization

**Claude Code (Sonnet 4.5):**
- Prefers high-level instructions over prescriptive steps
- Excels at sustained reasoning for complex tasks
- Best for large files, complex refactors, architecture
- Use concise prompts, let Claude's creativity emerge

**Prompt Patterns:**
```markdown
✅ "Optimize the database queries in this service"
   (High-level, Claude determines approach)

❌ "First find all queries, then wrap each in transaction,
   then add error handling, then..."
   (Too prescriptive, limits Claude's reasoning)
```

### Extended Thinking Budget Management

**When to use different thinking levels:**

| Task Complexity | Trigger | Token Budget | Use Case |
|----------------|---------|--------------|----------|
| Simple | (none) | Default | Straightforward implementations |
| Medium | "think" | ~4k tokens | Multiple considerations |
| Complex | "think hard" | ~10k tokens | Architectural decisions |
| Critical | "think harder" | ~32k tokens | Security, performance, complexity |

**Example Usage:**

```markdown
# Simple task (no trigger needed)
"Add a console.log statement here"

# Medium complexity
"Think about the best way to structure this form validation"

# Complex problem
"Think hard about how to optimize this N+1 query while maintaining RLS"

# Critical decision
"Think harder about the security implications of this authentication flow"
```

### Agent Selection Framework

**Use agents for specialized reasoning:**

| Need | Agent | Rationale |
|------|-------|-----------|
| Database design | `database-specialist` | Domain expertise for schema/RLS |
| Performance issues | `db-performance-agent` | Specialized N+1 detection |
| Quality review | `quality-reviewer` | Pattern validation, auto-fixes |
| Production errors | `sentry-fixer-agent` | Error investigation workflow |
| Code exploration | `Explore` agent | Efficient codebase navigation |
| Flutter quality | `flutter-quality-agent` | Mobile-specific patterns |

**Metacognitive Agent Selection:**

```markdown
# Ask yourself: "What domain expertise is needed?"
├─ Database → database-specialist
├─ Performance → db-performance-agent
├─ Quality → quality-reviewer
├─ Errors → sentry-fixer-agent
├─ Exploration → Explore agent
└─ General → Claude handles natively

# Then prompt accordingly:
"Use the database-specialist agent to design this schema with proper RLS"
```

### Skills as Just-in-Time Knowledge

**Instead of loading full documentation:**

```markdown
# ❌ Don't do this:
"Read all the Flutter documentation files and then help me build a form"
(Loads thousands of tokens)

# ✅ Do this:
"Use the flutter-forms skill to build a multi-step form with validation"
(Loads only relevant skill content)
```

**Strategic Skill Usage:**

| Scenario | Skill | Benefit |
|----------|-------|---------|
| Database migrations | `database-migration-manager` | Migration patterns on-demand |
| RLS policies | `rls-policy-generator` | Security patterns without full docs |
| API patterns | `api-patterns` | Server action templates |
| i18n work | `i18n-translation-guide` | Translation patterns when needed |
| Performance | `web-performance-metrics` | Optimization strategies |

## Troubleshooting

| Issue | Cause | Metacognitive Solution |
|-------|-------|----------------------|
| Claude jumps to coding too fast | No planning phase | Use "First, explore..." or enter plan mode |
| Solutions feel generic | Missing context | Provide codebase-specific context, reference existing patterns |
| Repeated mistakes | Context pollution | Use `/clear` between tasks |
| Shallow reasoning | No thinking trigger | Add "think hard" or "think harder" |
| Missing edge cases | Not prompted for them | Ask "What edge cases exist?" |
| Wrong approach chosen | No comparison requested | "Compare approaches A, B, C - pros/cons" |
| Can't see Claude's reasoning | Verbose mode off | Press Ctrl+O to view thinking |
| Context limits hit | Too much loaded | Use skills/agents, progressive disclosure |

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Lazy Prompting
```markdown
"Fix it"
"Make it work"
"Do the thing"
```
**Problem:** No context, no guidance, poor results

**✅ Instead:**
```markdown
"The user authentication is failing with error X. First, explore the auth
code to understand the flow, then think about what could cause this error,
and propose a fix with explanation."
```

### ❌ Anti-Pattern 2: Blindly Accepting Output
```markdown
User: "Add feature X"
Claude: [Generates code]
User: "Great, ship it!"
```
**Problem:** Metacognitive laziness, no understanding

**✅ Instead:**
```markdown
User: "Add feature X"
Claude: [Generates code]
User: "Explain what this code does and why you chose this approach"
Claude: [Explains reasoning]
User: "What about edge case Y?"
Claude: [Addresses concern]
User: "Good, let's implement it"
```

### ❌ Anti-Pattern 3: Context Hoarding
```markdown
# Loading everything "just in case"
"Read all files in /app"
"Load all skills"
"Show me everything about feature X"
```
**Problem:** Token waste, context pollution

**✅ Instead:**
```markdown
# Just-in-time loading
"Explore the auth feature to find relevant files"
"Use the database-migration-manager skill for this migration"
"Read the specific file I need: apps/web/lib/auth.ts"
```

### ❌ Anti-Pattern 4: No Task Decomposition
```markdown
"Build the entire user management system"
```
**Problem:** Too complex, no tracking, likely incomplete

**✅ Instead:**
```markdown
"Let's build the user management system. First, enter plan mode so we can
break this into phases. I want to review the architecture before we start."
```

### ❌ Anti-Pattern 5: Ignoring Claude's Uncertainty
```markdown
Claude: "I think this might work, but I'm not certain about..."
User: "Just do it"
```
**Problem:** Proceeding despite uncertainty leads to bugs

**✅ Instead:**
```markdown
Claude: "I think this might work, but I'm not certain about..."
User: "Let's investigate that uncertainty. Research our codebase to see
how we handle similar cases."
```

## Quality Metrics

**Assess your metacognitive collaboration:**

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **Understanding** | Can explain all code changes | Ask yourself: "Why this approach?" |
| **Context efficiency** | < 5 `/clear` needs per complex task | Monitor context bloat |
| **Planning rate** | Use plan mode for 80%+ complex tasks | Track when you skip planning |
| **Thinking triggers** | Use extended thinking for critical decisions | Review transcripts |
| **Question frequency** | Ask "why" 3+ times per complex feature | Self-monitor engagement |
| **Error rate** | < 5% of implementations need rework | Track fixes/revisions |

## Session Optimization Checklist

Before starting work:
- [ ] Complexity assessed (simple/medium/complex)?
- [ ] Relevant skills identified?
- [ ] Need for plan mode evaluated?
- [ ] Context window clean (used `/clear` if needed)?
- [ ] Extended thinking triggers considered?

During work:
- [ ] Using Ctrl+O to monitor reasoning when appropriate?
- [ ] Asking "why" questions to understand approaches?
- [ ] Challenging assumptions and seeking alternatives?
- [ ] Using TodoWrite for multi-step tasks?
- [ ] Loading context just-in-time, not preemptively?

After work:
- [ ] Understanding all implemented code?
- [ ] Can explain design decisions to team?
- [ ] Learned patterns for future use?
- [ ] Context cleared for next task?
- [ ] Session insights captured?

## Related Resources

### Ballee-Specific Skills

Apply metacognitive strategies with domain skills:

**Web Development:**
- `database-migration-manager` - Migrations with planning
- `rls-policy-generator` - Security-first thinking
- `service-patterns` - Service layer patterns
- `api-patterns` - Server action patterns
- `web-performance-metrics` - Performance optimization

**Mobile Development:**
- `flutter-development` - Flutter patterns
- `flutter-query-testing` - Query validation
- `flutter-testing` - Testing strategies

**Operations:**
- `sentry-error-manager` - Error investigation
- `production-database-query` - Safe production queries
- `dev-environment-manager` - Environment management

### Official Documentation

- [Extended Thinking Tips - Claude Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/extended-thinking-tips)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [The "think" tool](https://www.anthropic.com/engineering/claude-think-tool)
- [Chain of Thought Prompting](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought)
- [Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

### Research Papers

- [Scaffolding Metacognition in Programming Education](https://arxiv.org/html/2511.04144v1)
- IBM 2026 Guide to Prompt Engineering
- K2View Prompt Engineering Techniques 2026

## Success Criteria

Effective metacognitive collaboration achieves:

✅ You understand WHY, not just WHAT was implemented
✅ Complex tasks planned before implementation
✅ Context stays relevant and clean
✅ Extended thinking used for critical decisions
✅ Claude's reasoning visible when needed
✅ Assumptions questioned, alternatives explored
✅ Implementations rarely need rework
✅ You're learning patterns, not just getting code
✅ Collaboration feels strategic, not reactive
✅ Quality improves over time

---

**Last Updated**: 2026-01-18
**Version**: 1.0.0
**Maintainer**: Ballee Engineering Team

## Key Takeaway

**Metacognition in Claude Code is not about using more features—it's about thinking strategically about:**
1. **What** you ask (task decomposition)
2. **How** you ask (prompting strategies)
3. **When** to use tools (context engineering)
4. **Why** approaches work (understanding, not just accepting)

Master these, and you transform Claude Code from a code generator into a reasoning partner.
