---
name: codex-peer-review
description: [CLAUDE CODE ONLY] Leverage Codex CLI for AI peer review, second opinions on architecture and design decisions, cross-validation of implementations, security analysis, and alternative approach generation. Requires terminal access to execute Codex CLI commands. Use when making high-stakes decisions, reviewing complex architecture, or when explicitly requested for a second AI perspective. Must be explicitly invoked using skill syntax.
license: Complete terms in LICENSE.txt
environment: claude-code
---

# Codex Peer Review Skill

🖥️ **Claude Code Only** - Requires terminal access to execute Codex CLI commands.

Enable Claude Code to leverage OpenAI's Codex CLI for collaborative AI reasoning, peer review, and multi-perspective analysis of code architecture, design decisions, and implementations.

## Core Philosophy

**Two AI perspectives are better than one for high-stakes decisions.**

This skill enables strategic collaboration between Claude Code (Anthropic) and Codex CLI (OpenAI) for:
- Architecture validation and critique
- Design decision cross-validation
- Alternative approach generation
- Security, performance, and testing analysis
- Learning from different AI reasoning patterns

**Not a replacement—a second opinion.**

---

## When to Use Codex Peer Review

### High-Value Scenarios

**DO use when:**
- Making high-stakes architecture decisions
- Choosing between significant design alternatives
- Reviewing security-critical code
- Validating complex refactoring plans
- Exploring unfamiliar domains or patterns
- User explicitly requests second opinion
- Significant disagreement about approach
- Performance-critical optimization decisions
- Testing strategy validation

**DON'T use when:**
- Simple, straightforward implementations
- Already confident in singular approach
- Time-sensitive quick fixes
- No significant trade-offs exist
- Low-impact tactical changes
- Codex CLI is not available/installed

### How to Invoke This Skill

**Important:** This skill requires explicit invocation. It is not automatically triggered by natural language.

**To use this skill, Claude must explicitly invoke it using:**

```
skill: "codex-peer-review"
```

**User phrases that indicate this skill would be valuable:**
- "Get a second opinion on..."
- "What would Codex think about..."
- "Review this architecture with Codex"
- "Use Codex to validate this approach"
- "Are there better alternatives to..."
- "Get Codex peer review for this"
- "Security review with Codex needed"
- "Ask Codex about this design"

When these phrases appear, Claude should suggest using this skill and invoke it explicitly if appropriate.

---

### Codex vs Gemini: Which Peer Review Skill?

Both Codex and Gemini peer review skills provide valuable second opinions, but excel in different scenarios.

**Use Codex Peer Review when:**
- Code size < 500 LOC (focused reviews)
- Need precise, line-level bug detection
- Want fast analysis with concise output
- Reviewing single modules or functions
- Need tactical implementation feedback
- Performance bottleneck identification (specific issues)
- Quick validation of design decisions

**Use Gemini Peer Review when:**
- Code size > 5k LOC (large codebase analysis)
- Need full codebase context (up to 1M tokens)
- Reviewing architecture across multiple modules
- Analyzing diagrams + code together (multimodal)
- Want research-grounded recommendations (current best practices)
- Cross-module security analysis (attack surface mapping)
- Systemic performance patterns
- Design consistency checking

**For mid-range codebases (500-5k LOC):**
- Use **Codex** if: Focused review, single module, speed priority, specific bugs
- Use **Gemini** if: Cross-module patterns, holistic view, diagram analysis, research grounding
- Consider **Both** for: Critical decisions requiring maximum confidence

**For maximum value on high-stakes decisions:** Use both skills sequentially and apply synthesis framework (see references/synthesis-framework.md).

---

## Core Workflow

### 1. Recognize Need for Peer Review

**Assess if peer review adds value:**

Questions to consider:
- Is this a high-stakes decision with significant impact?
- Are there multiple valid approaches to consider?
- Is the architecture complex or unfamiliar?
- Does this involve security, performance, or scalability concerns?
- Has the user explicitly requested a second opinion?
- Would different AI reasoning perspectives help?

**If yes to 2+ questions:** Proceed with peer review workflow

---

### 2. Prepare Context for Codex

**Extract and structure relevant information:**

Load `references/context-preparation.md` for detailed guidance on:
- What code/files to include
- How to frame questions effectively
- Context boundaries (what to include/exclude)
- Expectation setting for output format

**Key preparation steps:**

1. **Identify core question:** What specifically do we want Codex to review?
2. **Extract relevant code:** Include necessary files, not entire codebase
3. **Provide context:** Project type, constraints, requirements, concerns
4. **Frame clearly:** Specific questions, not vague requests
5. **Set expectations:** What kind of response we need

**Context structure template:**
```
[CONTEXT]
Project: [type, purpose]
Current situation: [what exists]
Constraints: [technical, business, time]

[CODE/ARCHITECTURE]
[relevant code or architecture description]

[QUESTION]
[specific question or review request]

[EXPECTED OUTPUT]
[format: analysis, alternatives, recommendations, etc.]
```

---

### 3. Invoke Codex CLI

**Execute appropriate Codex command:**

Load `references/codex-commands.md` for complete command reference.

**Common patterns:**

**Non-interactive review (recommended):**
```bash
cat <<'EOF' | codex exec
[prepared context and question here]
EOF
```

**Simple one-line review:**
```bash
codex exec "Review this code for security issues"
```

**Architecture review with diagram:**
```bash
codex --image architecture-diagram.png "Analyze this architecture"
```

**Key flags:**
- `exec`: Non-interactive execution streaming to stdout
- `--image` / `-i`: Attach architecture diagrams or screenshots
- `--full-auto`: Unattended mode (use with caution)

**Error handling:**
- If Codex CLI not installed, inform user and provide installation instructions
- If API limits reached, note limitation and proceed with Claude-only analysis
- If Codex returns unclear response, reformulate question and retry once

---

### 4. Synthesize Perspectives

**Compare and integrate both AI perspectives:**

Load `references/synthesis-framework.md` for detailed synthesis patterns.

**Analysis framework:**

1. **Agreement Analysis**
   - Where do both perspectives align?
   - What shared concerns exist?
   - What validates confidence in approach?

2. **Disagreement Analysis**
   - Where do perspectives diverge?
   - Why might approaches differ?
   - What assumptions differ?

3. **Complementary Insights**
   - What does Codex see that Claude missed?
   - What does Claude see that Codex missed?
   - How do perspectives complement each other?

4. **Trade-off Identification**
   - What trade-offs does each perspective reveal?
   - Which concerns are prioritized differently?
   - What constraints drive different conclusions?

5. **Insight Extraction**
   - What are the key actionable insights?
   - What alternatives emerge from both perspectives?
   - What risks are highlighted by either perspective?

**Synthesis output structure:**
```
## Perspective Comparison

**Claude's Analysis:**
[key points from Claude's initial analysis]

**Codex's Analysis:**
[key points from Codex's review]

**Points of Agreement:**
- [shared insights]

**Points of Divergence:**
- [different perspectives and why]

**Complementary Insights:**
- [unique value from each perspective]

## Synthesis & Recommendations

[integrated analysis incorporating both perspectives]

**Recommended Approach:**
[action plan based on both perspectives]

**Rationale:**
[why this approach balances both perspectives]

**Remaining Considerations:**
[open questions or concerns to address]
```

---

### 5. Present Balanced Analysis

**Deliver integrated insights to user:**

**Presentation principles:**
- Be transparent about which AI said what
- Acknowledge disagreements honestly
- Don't force false consensus
- Explain reasoning behind each perspective
- Give user enough context to make informed decision
- Present alternatives clearly
- Indicate confidence levels appropriately

**When perspectives align:**
"Both Claude and Codex agree that [approach] is preferable because [reasons]. This alignment increases confidence in the recommendation."

**When perspectives diverge:**
"Claude favors [approach A] prioritizing [factors], while Codex suggests [approach B] emphasizing [factors]. This divergence reveals an important trade-off: [explanation]. Consider [factors] to decide which approach better fits your context."

**When one finds issues the other missed:**
"Codex identified [concern] that wasn't initially apparent. This adds [insight] to our analysis..."

---

## Use Case Patterns

Load `references/use-case-patterns.md` for detailed examples of each scenario.

### 1. Architecture Review

**Scenario:** Reviewing system design before major implementation

**Process:**
1. Document current architecture or proposed design
2. Prepare context: system requirements, constraints, scale expectations
3. Ask Codex: "Review this architecture for scalability, maintainability, and potential issues"
4. Synthesize: Compare architectural concerns and recommendations
5. Present: Integrated architecture assessment with both perspectives

**Example question:** "Review this microservices architecture. Are there concerns with service boundaries, data consistency, or deployment complexity?"

---

### 2. Design Decision Validation

**Scenario:** Choosing between multiple implementation approaches

**Process:**
1. Document the decision point and alternatives
2. Prepare context: requirements, constraints, trade-offs known
3. Ask Codex: "Compare approaches A, B, and C for [criteria]"
4. Synthesize: Create trade-off matrix from both perspectives
5. Present: Clear comparison showing strengths/weaknesses

**Example question:** "Should we use event sourcing or traditional CRUD for this domain? Consider complexity, auditability, and team expertise."

---

### 3. Security Review

**Scenario:** Validating security-critical code before deployment

**Process:**
1. Extract security-relevant code sections
2. Prepare context: threat model, security requirements, compliance needs
3. Ask Codex: "Security review: identify vulnerabilities, attack vectors, and hardening opportunities"
4. Synthesize: Combine security concerns from both analyses
5. Present: Comprehensive security assessment with prioritized issues

**Example question:** "Review this authentication implementation. Are there vulnerabilities in session management, token handling, or access control?"

---

### 4. Performance Analysis

**Scenario:** Optimizing performance-critical code

**Process:**
1. Extract performance-critical sections
2. Prepare context: performance requirements, current bottlenecks, constraints
3. Ask Codex: "Analyze for performance bottlenecks and optimization opportunities"
4. Synthesize: Combine optimization suggestions from both perspectives
5. Present: Prioritized optimization recommendations with trade-offs

**Example question:** "This query endpoint is slow under load. Identify bottlenecks in the database access pattern, caching strategy, and N+1 issues."

---

### 5. Testing Strategy

**Scenario:** Improving test coverage and quality

**Process:**
1. Document current testing approach and coverage
2. Prepare context: critical paths, known gaps, testing constraints
3. Ask Codex: "Review testing strategy and suggest improvements"
4. Synthesize: Combine testing recommendations from both perspectives
5. Present: Comprehensive testing improvement plan

**Example question:** "Review our testing approach. Are there coverage gaps, missing edge cases, or better testing strategies for this complex state machine?"

---

### 6. Code Review & Learning

**Scenario:** Understanding unfamiliar code or patterns

**Process:**
1. Extract relevant code sections
2. Prepare context: what's unclear, specific questions, learning goals
3. Ask Codex: "Explain this code: patterns used, design decisions, potential concerns"
4. Synthesize: Combine explanations and identify patterns both AIs recognize
5. Present: Clear explanation with multiple perspectives on design

**Example question:** "Explain this recursive backtracking algorithm. What patterns are used, and are there clearer alternatives?"

---

### 7. Alternative Approach Generation

**Scenario:** Stuck on a problem or exploring better approaches

**Process:**
1. Document current approach and why it's unsatisfactory
2. Prepare context: problem constraints, what's been tried, goals
3. Ask Codex: "Generate alternative approaches to [problem]"
4. Synthesize: Combine creative alternatives from both perspectives
5. Present: Multiple vetted alternatives with trade-off analysis

**Example question:** "We're stuck on real-time conflict resolution for collaborative editing. What alternative CRDT or operational transform approaches could work better?"

---

## Command Reference

Load `references/codex-commands.md` for complete command documentation.

**Quick reference:**

| Use Case | Command Pattern |
|----------|----------------|
| Simple review | `codex exec "Review this code"` |
| Multi-line prompt | `cat <<'EOF' \| codex exec` ... `EOF` |
| Review with diagram | `codex --image diagram.png "Analyze this"` |
| Interactive mode | `codex "What do you think about..."` |
| Resume session | `codex resume --last` |

**Non-interactive review (recommended for automation):**
```bash
cat <<'EOF' | codex exec
[Your structured prompt here]
EOF
```

---

## Integration Points

### With Other Skills

**With `concept-forge` skill:**
- Forge architectural concepts → Validate with Codex peer review
- Use `@builder` and `@strategist` archetypes to prepare questions

**With `prose-polish` skill:**
- Ensure technical documentation is clear and professional
- Polish architecture decision records (ADRs)

**With `claimify` skill:**
- Map architectural arguments and assumptions
- Analyze decision rationale structure

### With Claude Code Workflows

**Pre-implementation:**
- Use peer review before starting major features
- Validate architecture before building

**Post-implementation:**
- Use peer review to validate completed work
- Cross-check refactoring results

**During implementation:**
- Use peer review when stuck or uncertain
- Validate critical decisions in real-time

---

## Quality Signals

### Peer Review is Valuable When:

- Both perspectives identify same concerns (high confidence)
- Perspectives reveal complementary insights
- Trade-offs become clearer through different lenses
- Alternative approaches emerge that weren't initially visible
- Security or performance concerns are validated independently
- User gains clarity on decision through multi-perspective analysis

### Peer Review Needs Refinement When:

- Responses are too vague or generic
- Question wasn't specific enough
- Context was insufficient
- Both perspectives say obvious things
- No new insights emerge
- Codex response misunderstands the question

**Action:** Reformulate question with better context and specificity

### Skip Peer Review When:

- Codex CLI unavailable and blocking progress
- Decision is time-sensitive and low-risk
- Approach is straightforward with no trade-offs
- User doesn't value second opinion for this decision
- Context is too large to prepare efficiently

---

## Best Practices

### Effective Peer Review

**DO:**
- Frame specific, answerable questions
- Provide sufficient context for informed analysis
- Use for high-stakes decisions where second opinion adds value
- Be transparent about which AI provided which insight
- Acknowledge disagreements and explain them
- Synthesize perspectives rather than just concatenating them
- Give user enough context to make informed decision

**DON'T:**
- Use for every trivial decision
- Ask vague questions without context
- Force false consensus when perspectives diverge
- Hide which AI said what
- Ignore one perspective in favor of the other
- Present peer review as authoritative truth
- Over-rely on peer review for basic decisions

### Context Preparation

**Effective context:**
- Focused on specific decision or area of code
- Includes relevant constraints and requirements
- Provides enough background without overwhelming
- Frames clear questions
- Sets expectations for output

**Ineffective context:**
- Dumps entire codebase
- No clear question or focus
- Missing critical constraints
- Vague or overly broad
- No guidance on what kind of response is useful

### Question Framing

**Good questions:**
- "Review this microservices architecture. Are service boundaries well-defined? Any concerns with data consistency or deployment complexity?"
- "Compare these three caching strategies for our use case. Consider memory overhead, invalidation complexity, and cold-start performance."
- "Security review this authentication flow. Focus on session management, token expiration, and refresh token handling."

**Poor questions:**
- "Is this code good?" (too vague)
- "Review everything" (too broad)
- "What do you think?" (no specific focus)

---

## Installation Requirements

**Codex CLI must be installed to use this skill.**

### Installation

```bash
# Via npm
npm i -g @openai/codex

# Via Homebrew
brew install openai/codex/codex
```

### Authentication

```bash
# Sign in with ChatGPT Plus/Pro/Business/Edu/Enterprise account
codex auth login

# Or provide API key
codex auth api-key [your-api-key]
```

### Verification

```bash
# Verify installation
codex --version

# Check authentication
codex login status
```

---

**If Codex CLI is not available:**
1. Inform user that peer review requires Codex CLI
2. Provide installation instructions
3. Continue with Claude-only analysis if user can't install
4. Note that second opinion isn't available

---

## Configuration

**Optional configuration in `~/.codex/config.toml`:**

```toml
# Approval mode (suggest|auto|on-failure)
ask_for_approval = "suggest"

# Sandbox mode (read-only|workspace-write|danger-full-access)
sandbox = "read-only"
```

**For peer review, recommended settings:**
- `sandbox = "read-only"` for read-only safety
- `ask_for_approval = "suggest"` for transparency

**Note:** Don't hardcode model names in config. Let Codex CLI use its default (latest) model.

---

## Limitations & Considerations

### Technical Limitations

- Requires Codex CLI installation and authentication
- Subject to OpenAI API rate limits
- May have different context windows than Claude
- Responses may vary in quality based on prompt
- No real-time communication between AIs (sequential only)

### Philosophical Considerations

- Different training data and approaches may lead to different perspectives
- Neither AI is objectively "correct"—both offer perspectives
- User judgment is ultimate arbiter
- Peer review adds time to workflow
- Over-reliance on peer review can slow decision-making

### When to Trust Which Perspective

**Trust convergence:**
- When both AIs agree, confidence increases

**Trust divergence:**
- Reveals important trade-offs and assumptions
- Neither is necessarily "right"—different priorities

**Trust specialized knowledge:**
- Codex may have different strengths in certain domains
- Claude may have different strengths in others
- Consider which AI's reasoning aligns better with your context

---

## Example Workflows

### Example: Architecture Decision

**User:** "I'm designing a multi-tenant SaaS architecture. Should I use separate databases per tenant or a shared database with row-level security?"

**Claude initial analysis:** [Provides analysis of trade-offs]

**Invoke peer review:**
```bash
cat <<'EOF' | codex exec
Review multi-tenant SaaS architecture decision:

CONTEXT:
- B2B SaaS with 100-500 tenants expected
- Varying data volumes per tenant (small to large)
- Strong data isolation requirements
- Team familiar with PostgreSQL
- Cloud deployment (AWS)

OPTIONS:
A) Separate database per tenant
B) Shared database with row-level security (RLS)

QUESTION:
Analyze trade-offs for scalability, operational complexity, data isolation, and cost. Which approach is recommended for this context?
EOF
```

**Synthesis:**
Compare Claude's and Codex's trade-off analysis, extract key insights, present balanced recommendation.

---

## Anti-Patterns

**Don't:**
- Use peer review for every trivial decision (wastes time)
- Blindly follow one AI's recommendation over the other
- Ask vague questions without context
- Expect perfect agreement between AIs
- Force implementation when both AIs raise concerns
- Use peer review as decision-avoidance mechanism
- Over-engineer simple problems by seeking too many opinions

**Do:**
- Use strategically for high-stakes decisions
- Synthesize both perspectives thoughtfully
- Frame clear, specific questions with context
- Embrace disagreement as revealing trade-offs
- Use peer review to inform, not replace, judgment
- Make timely decisions based on integrated analysis
- Balance peer review with velocity

---

## Success Metrics

**Peer review succeeds when:**
- User gains clarity on decision through multi-perspective analysis
- Important trade-offs are revealed that weren't initially apparent
- Alternative approaches emerge that are genuinely valuable
- Risks are identified by at least one AI perspective
- User makes more informed decision than without peer review
- Confidence increases (when perspectives align)
- Trade-offs become explicit (when perspectives diverge)

**Peer review fails when:**
- No new insights emerge (obvious analysis)
- Takes too long relative to decision impact
- Perspectives are confusing rather than clarifying
- User is more confused after peer review than before
- Blocks forward progress unnecessarily
- Becomes crutch for simple decisions

---

## Skill Improvement

**This skill improves through:**
- Better question framing patterns
- More effective context preparation
- Refined synthesis techniques
- Pattern recognition for when peer review adds value
- Learning which types of questions work best with Codex
- Understanding Codex's strengths and limitations
- Calibrating when peer review is worth the time investment

**Feedback loop:**
- Track which peer reviews provided valuable insights
- Note which question patterns work well
- Identify scenarios where peer review was or wasn't valuable
- Refine use case patterns based on experience

---

## Related Resources

- Codex CLI Documentation: https://developers.openai.com/codex/cli/
- Architecture Decision Records (ADR) patterns
- Design pattern catalogs
- Security review checklists
- Performance optimization frameworks
- Testing strategy guides
