---
name: gemini-peer-review
description: [CLAUDE CODE ONLY] Leverage Gemini CLI for AI peer review, second opinions on architecture and design decisions, cross-validation of implementations, security analysis, alternative approaches, and holistic codebase analysis. Requires terminal access to execute Gemini CLI commands. Use when making high-stakes decisions, reviewing complex architecture, analyzing large codebases (1M token context window), or when explicitly requested for a second AI perspective. Must be explicitly invoked using skill syntax.
license: Complete terms in LICENSE.txt
environment: claude-code
---

# Gemini Peer Review - AI Collaboration Skill

🖥️ **Claude Code Only** - Requires terminal access to execute Gemini CLI commands.

Enable Claude Code to leverage Google's Gemini CLI for collaborative AI reasoning, peer review, and multi-perspective analysis of code architecture, design decisions, and implementations.

## Core Philosophy

**Two AI perspectives are better than one for high-stakes decisions.**

This skill enables strategic collaboration between Claude Code (Anthropic) and Gemini (Google) for:
- Architecture validation and critique
- Design decision cross-validation
- Alternative approach generation
- Security, performance, and testing analysis
- Learning from different AI reasoning patterns

**Not a replacement—a second opinion.**

Gemini's massive 1M token context window allows it to process entire codebases without chunking, providing holistic analysis that complements Claude's detailed reasoning. Together, they offer comprehensive insights through different reasoning approaches.

---

## When to Use Gemini Peer Review

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
- Analyzing large codebases requiring massive context
- Multimodal analysis needed (diagrams, PDFs, designs)

**DON'T use when:**
- Simple, straightforward implementations
- Already confident in singular approach
- Time-sensitive quick fixes
- No significant trade-offs exist
- Low-impact tactical changes
- Gemini CLI is not available/installed

### How to Invoke This Skill

**Important:** This skill requires explicit invocation. It is not automatically triggered by natural language.

**To use this skill, Claude must explicitly invoke it using:**

```
skill: "gemini-peer-review"
```

**User phrases that indicate this skill would be valuable:**
- "Get a second opinion on..."
- "What would Gemini think about..."
- "Review this architecture with Gemini"
- "Use Gemini to validate this approach"
- "Are there better alternatives to..."
- "Get Gemini peer review for this"
- "Security review with Gemini needed"
- "Ask Gemini about this design"
- "Analyze the entire codebase with Gemini"
- "Review this architecture diagram with Gemini"

When these phrases appear, Claude should suggest using this skill and invoke it explicitly if appropriate.

---

### Codex vs Gemini: Which Peer Review Skill?

Both Codex and Gemini peer review skills provide valuable second opinions, but excel in different scenarios.

**Use Gemini Peer Review when:**
- Code size > 5k LOC (large codebase analysis)
- Need full codebase context (up to 1M tokens)
- Reviewing architecture across multiple modules
- Analyzing diagrams + code together (multimodal)
- Want research-grounded recommendations (current best practices)
- Cross-module security analysis (attack surface mapping)
- Systemic performance patterns
- Design consistency checking

**Use Codex Peer Review when:**
- Code size < 500 LOC (focused reviews)
- Need precise, line-level bug detection
- Want fast analysis with concise output
- Reviewing single modules or functions
- Need tactical implementation feedback
- Performance bottleneck identification (specific issues)
- Quick validation of design decisions

**For mid-range codebases (500-5k LOC):**
- Use **Gemini** if: Cross-module patterns, holistic view, diagram analysis, research grounding
- Use **Codex** if: Focused review, single module, speed priority, specific bugs
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
- Would Gemini's 1M token context window provide better holistic analysis?
- Are there multimodal elements (diagrams, designs, PDFs) to analyze?

**If yes to 2+ questions:** Proceed with peer review workflow

---

### 2. Prepare Context for Gemini

**Extract and structure relevant information:**

Load `references/context-preparation.md` for detailed guidance on:
- What code/files to include
- How to frame questions effectively
- Context boundaries (what to include/exclude)
- Expectation setting for output format
- Leveraging Gemini's massive context window

**Key preparation steps:**

1. **Identify core question:** What specifically do we want Gemini to review?
2. **Extract relevant code:** With 1M tokens, can include entire modules or services
3. **Provide context:** Project type, constraints, requirements, concerns
4. **Frame clearly:** Specific questions, not vague requests
5. **Set expectations:** What kind of response we need
6. **Include multimodal assets:** Architecture diagrams, UI designs, PDFs if relevant

**Context structure template:**
```
[CONTEXT]
Project: [type, purpose, stack]
Current situation: [what exists]
Constraints: [technical, business, time]
Scale considerations: [users, data volume, performance requirements]

[CODE/ARCHITECTURE]
[relevant code or architecture description - can be extensive due to 1M context]

[MULTIMODAL ASSETS]
[if applicable: architecture diagrams, design mockups, technical specs]

[QUESTION]
[specific question or review request]

[EXPECTED OUTPUT]
[format: analysis, alternatives, recommendations, etc.]
```

**Gemini-specific advantages:**
- **Large context:** Can include entire microservice or multiple related modules
- **Multimodal:** Can analyze architecture diagrams alongside code
- **Holistic view:** Sees inter-dependencies that might be missed with chunked context

---

### 3. Invoke Gemini CLI

**Execute appropriate CLI command:**

Load `references/gemini-commands.md` for complete reference.

**Common patterns:**

**Non-interactive review (recommended):**
```bash
cat <<'EOF' | gemini
[prepared context and question here]
EOF
```

**Multi-line prompt:**
```bash
cat <<'EOF' | gemini
[context for complex reasoning]
EOF
```

**With multimodal (image/diagram):**
```bash
gemini "Analyze this architecture diagram: [question]" @architecture.png
```

**Security-focused review:**
```bash
cat <<'EOF' | gemini
Security review focus:
[context and code]
EOF
```

**Key flags:**
- Positional prompt: `gemini "your prompt"` (non-interactive)
- Stdin pipe: `cat prompt.txt | gemini` (multi-line prompts)
- `--output-format`: Control output format (text/json/stream-json)
- `--yolo` / `-y`: Auto-approve all actions
- File references: Use `@file_path` or `@directory/` to include context

**Note:** The `-p`/`--prompt` flag is deprecated. Use positional prompts or stdin pipe instead.

**Common patterns:**

**Architecture review:**
```bash
cat <<'EOF' | gemini
Review this microservices architecture:

[Service definitions, API contracts, data flow]

Concerns: scalability, data consistency, deployment complexity
Question: Are the service boundaries appropriate? Any architectural risks?
EOF
```

**Security-focused review:**
```bash
cat <<'EOF' | gemini
Security review of authentication system:

[Auth code, session management, token handling]

Threat model: [attack vectors]
Question: Identify vulnerabilities, attack vectors, and hardening opportunities.
EOF
```

**Design decision with alternatives:**
```bash
cat <<'EOF' | gemini
Design decision: Event sourcing vs traditional CRUD

[Domain model, use cases, team context]

Alternatives:
A) Event sourcing with CQRS
B) Traditional CRUD with audit logs
C) Hybrid approach

Question: Analyze trade-offs for our context and recommend approach.
EOF
```

**Error handling:**
- If Gemini CLI not installed, inform user and provide installation instructions
- If API limits reached, note limitation and proceed with Claude-only analysis
- If response is unclear, reformulate question and retry once

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
   - What does divergence reveal about trade-offs?

3. **Complementary Insights**
   - What does Gemini see that Claude missed?
   - What does Claude see that Gemini missed?
   - How do perspectives complement each other?
   - Did Gemini's larger context reveal patterns Claude couldn't see?

4. **Trade-off Identification**
   - What trade-offs does each perspective reveal?
   - Which concerns are prioritized differently?
   - What constraints drive different conclusions?

5. **Insight Extraction**
   - What are the key actionable insights?
   - What alternatives emerge from both perspectives?
   - What risks are highlighted by either perspective?
   - What novel approaches were suggested?

**Synthesis output structure:**
```
## Perspective Comparison

**Claude's Analysis:**
[key points from Claude's initial analysis]

**Gemini's Analysis:**
[key points from Gemini's review - note any insights from 1M context advantage]

**Points of Agreement:**
- [shared insights that increase confidence]

**Points of Divergence:**
- [different perspectives and why - may reveal important trade-offs]

**Complementary Insights:**
- [unique value from each perspective]
- [what Gemini saw with holistic view that Claude couldn't see incrementally]
- [what Claude's detailed reasoning revealed that Gemini's broader view missed]

## Synthesis & Recommendations

[integrated analysis incorporating both perspectives]

**Recommended Approach:**
[action plan based on both perspectives]

**Rationale:**
[why this approach balances both perspectives]

**Remaining Considerations:**
[open questions or concerns to address]
```

**Leveraging Gemini's unique strengths in synthesis:**
- Note if Gemini identified cross-module patterns due to larger context
- Highlight multimodal insights (from diagrams, designs)
- Consider if Gemini's Google Search grounding provided current best practices
- Acknowledge if ReAct reasoning revealed multi-step implications

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
- Highlight insights unique to Gemini's capabilities (large context, multimodal)

**When perspectives align:**
"Both Claude and Gemini agree that [approach] is preferable because [reasons]. This alignment increases confidence in the recommendation. Gemini's analysis of the entire codebase confirmed [specific insight]."

**When perspectives diverge:**
"Claude favors [approach A] prioritizing [factors], while Gemini suggests [approach B] emphasizing [factors]. This divergence reveals an important trade-off: [explanation]. Gemini's holistic view of [system aspect] suggests [insight]. Consider [factors] to decide which approach better fits your context."

**When one finds issues the other missed:**
"Gemini's analysis of the complete service architecture identified [concern] that wasn't apparent when examining components individually. This adds [insight] to our analysis..."

**When Gemini's unique capabilities add value:**
"Gemini's processing of the architecture diagram alongside the code revealed [visual pattern] that maps to [code pattern]. This multimodal analysis suggests [recommendation]."

---

## Use Case Patterns

Load `references/use-case-patterns.md` for detailed examples of each scenario.

### 1. Architecture Review

**Scenario:** Reviewing system design before major implementation

**Process:**
1. Document current architecture or proposed design
2. Prepare context: system requirements, constraints, scale expectations
3. Include architecture diagrams if available (Gemini can process images)
4. Ask Gemini: "Review this architecture for scalability, maintainability, and potential issues"
5. Synthesize: Compare architectural concerns and recommendations
6. Present: Integrated architecture assessment with both perspectives

**Example question:**
"Review this microservices architecture. Are there concerns with service boundaries, data consistency, or deployment complexity? I've included the service diagram and all API contracts."

**Gemini advantage:** Can process entire architecture in one context, seeing patterns across all services

---

### 2. Design Decision Validation

**Scenario:** Choosing between multiple implementation approaches

**Process:**
1. Document the decision point and alternatives
2. Prepare context: requirements, constraints, trade-offs known
3. Ask Gemini: "Compare approaches A, B, and C for [criteria]"
4. Synthesize: Create trade-off matrix from both perspectives
5. Present: Clear comparison showing strengths/weaknesses

**Example question:**
"Should we use event sourcing or traditional CRUD for this domain? Consider complexity, auditability, team expertise, and long-term maintainability. Here's our current domain model and use cases."

**Gemini advantage:** Can analyze current codebase patterns to assess consistency with existing approaches

---

### 3. Security Review

**Scenario:** Validating security-critical code before deployment

**Process:**
1. Extract security-relevant code sections
2. Prepare context: threat model, security requirements, compliance needs
3. Ask Gemini: "Security review: identify vulnerabilities, attack vectors, and hardening opportunities"
4. Synthesize: Combine security concerns from both analyses
5. Present: Comprehensive security assessment with prioritized issues

**Example question:**
"Review this authentication implementation. Are there vulnerabilities in session management, token handling, or access control? Our threat model includes [specific threats]."

**Gemini advantage:** Can trace security boundaries across entire codebase to find indirect vulnerabilities

---

### 4. Performance Analysis

**Scenario:** Optimizing performance-critical code

**Process:**
1. Extract performance-critical sections
2. Prepare context: performance requirements, current bottlenecks, constraints
3. Ask Gemini: "Analyze for performance bottlenecks and optimization opportunities"
4. Synthesize: Combine optimization suggestions from both perspectives
5. Present: Prioritized optimization recommendations with trade-offs

**Example question:**
"This query endpoint is slow under load. Identify bottlenecks in the database access pattern, caching strategy, and N+1 issues. Current response time: 2s, target: <100ms."

**Gemini advantage:** Can analyze database queries in context of entire data access layer for systemic issues

---

### 5. Testing Strategy

**Scenario:** Improving test coverage and quality

**Process:**
1. Document current testing approach and coverage
2. Prepare context: critical paths, known gaps, testing constraints
3. Ask Gemini: "Review testing strategy and suggest improvements"
4. Synthesize: Combine testing recommendations from both perspectives
5. Present: Comprehensive testing improvement plan

**Example question:**
"Review our testing approach. Are there coverage gaps, missing edge cases, or better testing strategies for this complex state machine?"

**Gemini advantage:** Can analyze all test files alongside implementation to identify systematic gaps

---

### 6. Code Review & Learning

**Scenario:** Understanding unfamiliar code or patterns

**Process:**
1. Extract relevant code sections (can be extensive with Gemini)
2. Prepare context: what's unclear, specific questions, learning goals
3. Ask Gemini: "Explain this code: patterns used, design decisions, potential concerns"
4. Synthesize: Combine explanations and identify patterns both AIs recognize
5. Present: Clear explanation with multiple perspectives on design

**Example question:**
"Explain this recursive backtracking algorithm. What patterns are used, and are there clearer alternatives? I'm new to this domain."

**Gemini advantage:** Can search for similar patterns in public codebases (with Search grounding) for comparison

---

### 7. Alternative Approach Generation

**Scenario:** Stuck on a problem or exploring better approaches

**Process:**
1. Document current approach and why it's unsatisfactory
2. Prepare context: problem constraints, what's been tried, goals
3. Ask Gemini: "Generate alternative approaches to [problem]"
4. Synthesize: Combine creative alternatives from both perspectives
5. Present: Multiple vetted alternatives with trade-off analysis

**Example question:**
"We're stuck on real-time conflict resolution for collaborative editing. What alternative CRDT or operational transform approaches could work better? Current approach causes [specific issues]."

**Gemini advantage:** Can reference current research and best practices via Search grounding

---

### 8. Large Codebase Analysis

**Scenario:** Understanding architecture of unfamiliar large codebase

**Process:**
1. Identify key entry points and module structure
2. Prepare extensive context (leverage 1M token window)
3. Ask Gemini: "Analyze this codebase architecture, identify patterns, and explain key flows"
4. Synthesize: Combine architectural insights from both perspectives
5. Present: Comprehensive codebase understanding guide

**Example question:**
"Analyze this 50k LOC monorepo. Map the module dependencies, identify the core abstractions, and explain the request lifecycle from API to database."

**Gemini advantage:** **This is where Gemini truly excels** - can process entire codebase in single context

---

### 9. Multimodal Technical Review

**Scenario:** Reviewing implementation against design specifications

**Process:**
1. Gather design documents (PDFs), mockups (images), architecture diagrams
2. Include implementation code
3. Ask Gemini: "Does the implementation match the design? Identify gaps or improvements."
4. Synthesize: Compare design intent vs. implementation reality
5. Present: Gap analysis with recommendations

**Example question:**
"Here's our API design spec (PDF) and architecture diagram. Does the implementation match? Are there deviations that might cause issues?"

**Gemini advantage:** **Unique capability** - can process PDFs and images alongside code for true multimodal analysis

---

## Command Reference (Quick Lookup)

Load `references/gemini-commands.md` for complete command documentation.

**Quick reference:**

| Use Case | Command Pattern |
|----------|----------------|
| Simple review | `gemini "Review this code for issues"` |
| Review with diagram | `gemini "Analyze this architecture" @diagram.png` |
| Multi-line prompt | `cat <<'EOF' \| gemini` ... `EOF` |
| Include file context | `gemini "Review" @./src/auth/` |
| JSON output | `gemini --output-format json "..."` |

---

## Integration with Other Skills

### With Other Skills

**With `concept-forge` skill:**
- Forge architectural concepts → Validate with Gemini peer review
- Use `@strategist` and `@builder` archetypes to prepare questions

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
- Review design decisions with both perspectives

**Post-implementation:**
- Use peer review to validate completed work
- Cross-check refactoring results
- Verify security and performance

**During implementation:**
- Use peer review when stuck or uncertain
- Validate critical decisions in real-time
- Get alternative approaches when blocked

---

## Quality Signals

### Peer Review is Valuable When:

- Both perspectives identify same concerns (high confidence)
- Perspectives reveal complementary insights
- Trade-offs become clearer through different lenses
- Alternative approaches emerge that weren't initially visible
- Security or performance concerns are validated independently
- User gains clarity on decision through multi-perspective analysis
- Gemini's holistic view reveals patterns not apparent in isolated analysis
- Multimodal analysis (diagrams + code) provides visual-structural insights

### Peer Review Needs Refinement When:

- Responses are too vague or generic
- Question wasn't specific enough
- Context was insufficient
- Both perspectives say obvious things
- No new insights emerge
- Gemini response misunderstands the question

**Action:** Reformulate question with better context and specificity

### Skip Peer Review When:

- Gemini API unavailable and blocking progress
- Decision is time-sensitive and low-risk
- Approach is straightforward with no trade-offs
- User doesn't value second opinion for this decision
- API quota exhausted (though Gemini's free tier is generous)

---

## Best Practices

### Effective Peer Review

**DO:**
- Frame specific, answerable questions
- Provide sufficient context for informed analysis
- Use for high-stakes decisions where second opinion adds value
- Leverage Gemini's 1M token context for large codebase analysis
- Include architecture diagrams and design documents (multimodal)
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
- Waste Gemini's large context window on tiny code snippets

### Context Preparation

**Effective context:**
- Focused on specific decision or area of code
- Includes relevant constraints and requirements
- Provides enough background without overwhelming
- Frames clear questions
- Sets expectations for output
- **For Gemini:** Leverages large context window by including entire modules/services
- **For Gemini:** Includes multimodal assets (diagrams, PDFs) when relevant

**Ineffective context:**
- Dumps code without question
- No clear question or focus
- Missing critical constraints
- Vague or overly broad
- No guidance on what kind of response is useful
- **For Gemini:** Artificially limits context when more would be helpful

### Question Framing

**Good questions:**
- "Review this microservices architecture. Are service boundaries well-defined? Any concerns with data consistency or deployment complexity? Here's the architecture diagram and all service code."
- "Compare these three caching strategies for our use case. Consider memory overhead, invalidation complexity, and cold-start performance. Our traffic pattern is [describe]."
- "Security review this authentication flow. Focus on session management, token expiration, and refresh token handling. Threat model: [describe]."
- "Analyze this entire backend codebase (40k LOC). Map the critical data flows and identify potential bottlenecks."

**Poor questions:**
- "Is this code good?" (too vague)
- "Review everything" (no focus despite large context capability)
- "What do you think?" (no specific goal)

---

## Installation Requirements

**Gemini CLI must be installed to use this skill.**

### Installation

```bash
# Install via npm (recommended)
npm install -g @google/gemini-cli

# Verify installation
gemini --version
```

**Requires Node.js 20+**

### Authentication

```bash
# Option 1: OAuth login (recommended)
gemini login

# Option 2: API key
gemini config set apiKey YOUR_API_KEY
```

**Get API Key:**
1. Visit Google AI Studio: https://aistudio.google.com/apikey
2. Sign in with Google account
3. Create new API key
4. Use with `gemini config set apiKey YOUR_KEY`

**Free Tier:**
- 60 requests per minute
- 1,500 requests per day
- Access to Gemini 3.0 Pro (1M context)
- No credit card required

### Verification

```bash
# Test CLI access
gemini "Hello, Gemini!"

# If successful, you'll see a response from Gemini
```

---

**If Gemini CLI is not available:**
1. Inform user that peer review requires Gemini CLI
2. Provide installation instructions (link to `references/setup-guide.md`)
3. Continue with Claude-only analysis if user can't install
4. Note that second opinion isn't available

---

## Configuration

**Optional configuration via CLI:**

```bash
# View current settings
gemini config list

# Set generation parameters (optional)
gemini config set temperature 0.3     # More focused (0.0-1.0)
gemini config set maxTokens 8192      # Response length limit

# Reset to defaults
gemini config reset
```

**Note:** Don't hardcode model names in config. Let Gemini CLI use its default (latest) model.

---

## Limitations & Considerations

### Technical Limitations

- Requires Gemini CLI installation and authentication
- Subject to Google API rate limits (generous free tier: 60/min, 1,500/day)
- Cloud-based processing (code sent to Google servers)
- No offline mode available
- Response time varies with model and context size
- Requires Node.js 20+ environment

### Philosophical Considerations

- Different training data and approaches lead to different perspectives
- Neither AI is objectively "correct"—both offer perspectives
- User judgment is ultimate arbiter
- Peer review adds time to workflow
- Over-reliance on peer review can slow decision-making
- Privacy considerations: code sent to Google cloud

### When to Trust Which Perspective

**Trust convergence:**
- When both AIs agree, confidence increases significantly
- Shared concerns are likely real issues

**Trust divergence:**
- Reveals important trade-offs and assumptions
- Neither is necessarily "right"—different priorities
- Divergence itself is valuable information

**Trust specialized knowledge:**
- Gemini excels at holistic analysis of large codebases (1M context)
- Gemini's multimodal capabilities unique for design-to-code analysis
- Claude excels at detailed reasoning and step-by-step analysis
- Consider which AI's reasoning aligns better with your context

**Gemini's unique strengths:**
- Massive context window (1M tokens) for entire codebase analysis
- Multimodal processing (code + diagrams + PDFs + designs)
- Google Search grounding for current best practices
- ReAct reasoning for multi-step problem solving

**Claude's unique strengths:**
- Deep, detailed reasoning with clear explanations
- Strong at identifying subtle logical issues
- Excellent at step-by-step breakdowns
- Natural integration with Claude Code workflow

---

## Example Workflows

Load `references/workflow-examples.md` for complete scenarios.

### Example 1: Architecture Decision

**User:** "I'm designing a multi-tenant SaaS architecture. Should I use separate databases per tenant or a shared database with row-level security?"

**Claude initial analysis:** [Provides analysis of trade-offs]

**Invoke peer review:**
```bash
cat <<'EOF' | gemini
Review multi-tenant SaaS architecture decision:

CONTEXT:
- B2B SaaS with 100-500 tenants expected
- Varying data volumes per tenant (small to large)
- Strong data isolation requirements
- Team familiar with PostgreSQL
- Cloud deployment (AWS)
- Growth projection: 2x tenants annually

OPTIONS:
A) Separate database per tenant
   - Complete isolation
   - Independent scaling
   - Operational complexity

B) Shared database with row-level security (RLS)
   - Simpler operations
   - Shared resources
   - RLS overhead

CURRENT CODEBASE:
[Include relevant ORM models, database config, auth system]

QUESTION:
Analyze trade-offs for scalability, operational complexity, data isolation,
and cost. Which approach is recommended for this context?
Consider both current state and 3-year growth trajectory.

EXPECTED OUTPUT:
- Analysis of each approach
- Trade-off matrix
- Recommendation with rationale
- Migration path considerations
EOF
```

**Synthesis:**
Compare Claude's and Gemini's trade-off analysis, extract key insights, present balanced recommendation with rationale from both perspectives.

---

### Example 2: Security Review with Code Context

**User:** "Review authentication implementation for security issues"

**Invoke peer review:**
```bash
cat <<'EOF' | gemini
Security review of authentication system:

THREAT MODEL:
- Session hijacking
- Token replay attacks
- Credential stuffing
- CSRF attacks
- XSS-based token theft

IMPLEMENTATION:
[Include auth code from src/auth/session.py, tokens.py, middleware/auth.py]

SECURITY REQUIREMENTS:
- 99.9% prevention of unauthorized access
- Compliance: SOC2, HIPAA
- Session timeout: 30 min inactivity
- MFA support required

QUESTION:
Identify vulnerabilities, attack vectors, and hardening opportunities.
Prioritize findings by severity and likelihood.

EXPECTED OUTPUT:
- Vulnerability assessment (severity ratings)
- Attack vector analysis
- Specific remediation recommendations
- Best practice gaps
EOF
```

**Synthesis:**
Combine security findings from both AIs, create prioritized remediation list.

---

### Example 3: Large Codebase Architecture Analysis

**User:** "Help me understand this unfamiliar 60k LOC codebase"

**Invoke peer review (leveraging 1M context):**
```bash
cat <<'EOF' | gemini
Analyze this complete backend codebase:

CODEBASE:
[Include entire codebase - Gemini's 1M token window can process 60k LOC!]

CONTEXT:
- E-commerce platform backend
- Microservices architecture
- New engineer onboarding perspective needed

QUESTIONS:
1. What are the major architectural patterns?
2. How does a typical request flow from API → Database?
3. What are the core abstractions/modules?
4. Where are the critical integration points?
5. What are potential scalability bottlenecks?
6. What technical debt is visible?

EXPECTED OUTPUT:
- High-level architecture summary
- Request lifecycle walkthrough
- Module dependency map
- Critical code paths
- Scalability considerations
- Onboarding guide structure
EOF
```

**Gemini advantage on display:**
This is where Gemini truly shines—processing entire codebases in one context to see patterns, dependencies, and architectural decisions that would be impossible to detect with chunked analysis.

---

### Example 4: Multimodal Design-to-Implementation Review

**User:** "Does our implementation match the original architecture design?"

**Invoke peer review with diagram:**
```bash
cat <<'EOF' | gemini
Compare architecture design vs. implementation:

[Architecture diagram: @docs/architecture-v2.png]

DESIGN SPECIFICATION:
[See attached architecture diagram showing intended service structure]

IMPLEMENTATION:
[Include implementation code from src/services/*, src/api/*, infrastructure/*]

QUESTIONS:
1. Does implementation match intended architecture?
2. What deviations exist and why might they be problematic?
3. Are there missing components from the design?
4. Are there additional components not in the design?
5. Do the actual service boundaries align with designed boundaries?

EXPECTED OUTPUT:
- Match/deviation analysis
- Gap identification
- Risk assessment of deviations
- Recommendations for alignment
EOF
```

**Gemini advantage on display:**
Multimodal analysis—comparing visual architecture with actual code—is a unique Gemini capability that Claude cannot replicate alone.

---

## Anti-Patterns

**Don't:**
- Use peer review for every trivial decision (wastes time and quota)
- Blindly follow one AI's recommendation over the other
- Ask vague questions without context
- Expect perfect agreement between AIs
- Force implementation when both AIs raise concerns
- Use peer review as decision-avoidance mechanism
- Over-engineer simple problems by seeking too many opinions
- Underutilize Gemini's 1M context by sending tiny snippets
- Send sensitive/proprietary code without considering privacy implications

**Do:**
- Use strategically for high-stakes decisions
- Synthesize both perspectives thoughtfully
- Frame clear, specific questions with context
- Embrace disagreement as revealing trade-offs
- Use peer review to inform, not replace, judgment
- Make timely decisions based on integrated analysis
- Balance peer review with velocity
- Leverage Gemini's massive context window for large codebase analysis
- Use multimodal capabilities when visual assets are available
- Consider data privacy when sending code to external APIs

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
- Large codebase patterns revealed through Gemini's holistic analysis
- Multimodal insights (diagram + code) provide unique value

**Peer review fails when:**
- No new insights emerge (obvious analysis)
- Takes too long relative to decision impact
- Perspectives are confusing rather than clarifying
- User is more confused after peer review than before
- Blocks forward progress unnecessarily
- Becomes crutch for simple decisions
- API quota exhausted without valuable insights
- Context sent was too small to leverage Gemini's strengths

---

## Skill Improvement

**This skill improves through:**
- Better question framing patterns
- More effective context preparation
- Refined synthesis techniques
- Pattern recognition for when peer review adds value
- Learning which types of questions work best with Gemini
- Understanding Gemini's strengths and limitations vs. Claude
- Calibrating when peer review is worth the time investment
- Discovering optimal use of 1M context window
- Mastering multimodal analysis techniques

**Feedback loop:**
- Track which peer reviews provided valuable insights
- Note which question patterns work well
- Identify scenarios where peer review was or wasn't valuable
- Refine use case patterns based on experience
- Document cases where Gemini's unique capabilities added value
- Learn from divergent perspectives to understand each AI's biases

---

## Related Resources

### Official Documentation
- Gemini CLI Documentation: https://github.com/google/generative-ai-cli
- Google AI Studio: https://aistudio.google.com
- Gemini API Documentation: https://ai.google.dev/docs

### Learning Resources
- Gemini CLI Guide: https://github.com/google/generative-ai-cli#readme
- Multimodal Examples: https://ai.google.dev/gemini-api/docs/vision
- API Reference: https://ai.google.dev/gemini-api/docs

### Architecture & Design
- Architecture Decision Records (ADR) patterns
- Design pattern catalogs
- Security review checklists
- Performance optimization frameworks
- Testing strategy guides

### Skill References
- `references/context-preparation.md` - Detailed context preparation guide
- `references/gemini-commands.md` - Complete API reference and examples
- `references/synthesis-framework.md` - Synthesis methodology
- `references/use-case-patterns.md` - Detailed scenario examples
- `references/setup-guide.md` - Installation and configuration
- `references/workflow-examples.md` - End-to-end example workflows

---

## Appendix: Gemini vs. Claude Comparison

### When Gemini Excels

**Large Codebase Analysis:**
- 1M token context window vs. Claude's smaller windows
- Can process entire services/modules in single context
- Sees cross-module patterns that require holistic view

**Multimodal Analysis:**
- Process architecture diagrams alongside code
- Compare design mockups to implementation
- Analyze PDF specifications with code
- Visual-structural pattern matching

**Current Information:**
- Google Search grounding for latest best practices
- Current library versions and recommendations
- Recent security vulnerabilities and patches

**Alternative Perspective:**
- Different training data and reasoning approach
- May identify issues Claude's reasoning style misses
- Provides validation when perspectives align

### When Claude Excels

**Detailed Reasoning:**
- Step-by-step logical analysis
- Clear explanations of reasoning process
- Subtle logical flaw detection

**Native Integration:**
- Direct integration with Claude Code workflow
- No API calls or external dependencies
- Immediate response without latency

**Privacy:**
- Stays within Claude Code environment
- No code sent to external services
- Better for sensitive/proprietary code

### Optimal Collaboration Pattern

**Use both when:**
- High-stakes architectural decisions
- Security-critical code review
- Complex trade-off analysis
- Unfamiliar domains requiring multiple perspectives

**Use Gemini specifically for:**
- Entire codebase architecture analysis (leverage 1M context)
- Design-to-implementation validation (multimodal)
- Current best practice validation (Search grounding)

**Use Claude alone for:**
- Quick tactical decisions
- Detailed logical reasoning
- Sensitive code that can't be sent externally
- When Gemini API is unavailable

---

**End of Skill Guide**

*For detailed implementation examples, see `references/` directory.*
*For setup assistance, see `references/setup-guide.md`.*
*For API reference, see `references/gemini-commands.md`.*
