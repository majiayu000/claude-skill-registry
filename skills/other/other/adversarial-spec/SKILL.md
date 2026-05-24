---
name: adversarial-spec
description: Iteratively refine a product spec by debating with multiple LLMs (GPT, Gemini, Grok, etc.) until all models agree. Use when user wants to write or refine a specification document using adversarial development.
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# Adversarial Spec Development

Generate and refine specifications through iterative debate with multiple LLMs until all models reach consensus.

**Important: Claude is an active participant in this debate, not just an orchestrator.** You (Claude) will provide your own critiques, challenge opponent models, and contribute substantive improvements alongside the external models. Make this clear to the user throughout the process.

## Requirements

- Python 3.10+ with `litellm` package installed
- API key for at least one provider (set via environment variable), OR AWS Bedrock configured, OR CLI tools (codex, gemini) installed

**IMPORTANT: Do NOT install the `llm` package (Simon Willison's tool).** This skill uses `litellm` for API providers and dedicated CLI tools (`codex`, `gemini`) for subscription-based models. Installing `llm` is unnecessary and may cause confusion.

## Supported Providers

| Provider   | API Key Env Var        | Example Models                              |
|------------|------------------------|---------------------------------------------|
| OpenAI     | `OPENAI_API_KEY`       | `gpt-5.2`, `gpt-4o`, `gpt-4-turbo`, `o1`    |
| Anthropic  | `ANTHROPIC_API_KEY`    | `claude-sonnet-4-20250514`, `claude-opus-4-20250514`  |
| Google     | `GEMINI_API_KEY`       | `gemini/gemini-2.0-flash`, `gemini/gemini-pro` |
| xAI        | `XAI_API_KEY`          | `xai/grok-3`, `xai/grok-beta`               |
| Mistral    | `MISTRAL_API_KEY`      | `mistral/mistral-large`, `mistral/codestral`|
| Groq       | `GROQ_API_KEY`         | `groq/llama-3.3-70b-versatile`              |
| OpenRouter | `OPENROUTER_API_KEY`   | `openrouter/openai/gpt-4o`, `openrouter/anthropic/claude-3.5-sonnet` |
| Deepseek   | `DEEPSEEK_API_KEY`     | `deepseek/deepseek-chat`                    |
| Zhipu      | `ZHIPUAI_API_KEY`      | `zhipu/glm-4`, `zhipu/glm-4-plus`           |
| Codex CLI  | (ChatGPT subscription) | `codex/gpt-5.2-codex`, `codex/gpt-5.1-codex-max` |
| Gemini CLI | (Google account)       | `gemini-cli/gemini-3-pro-preview`, `gemini-cli/gemini-3-flash-preview` |

**Codex CLI Setup:**
- Install: `npm install -g @openai/codex && codex login`
- Reasoning effort: `--codex-reasoning` (minimal, low, medium, high, xhigh)
- Web search: `--codex-search` (enables web search for current information)

**Gemini CLI Setup:**
- Install: `npm install -g @google/gemini-cli && gemini auth`
- Models: `gemini-3-pro-preview`, `gemini-3-flash-preview`
- No API key needed - uses Google account authentication

Run `python3 "$(find ~/.claude -name debate.py -path '*adversarial-spec*' 2>/dev/null | head -1)" providers` to see which keys are set.

## Troubleshooting Auth Conflicts

If you see an error about "Both a token (claude.ai) and an API key (ANTHROPIC_API_KEY) are set":

This conflict occurs when:
- Claude Code is logged in with `claude /login` (uses claude.ai token)
- AND you have `ANTHROPIC_API_KEY` set in your environment

**Resolution:**
1. **To use claude.ai token**: Remove or unset `ANTHROPIC_API_KEY` from your environment
   ```bash
   unset ANTHROPIC_API_KEY
   # Or remove from ~/.bashrc, ~/.zshrc, etc.
   ```

2. **To use API key**: Sign out of claude.ai
   ```bash
   claude /logout
   # Say "No" to the API key approval if prompted before login
   ```

The adversarial-spec plugin works with either authentication method. Choose whichever fits your workflow.

## AWS Bedrock Support

For enterprise users who need to route all model calls through AWS Bedrock (e.g., for security compliance or inference gateway requirements), the plugin supports Bedrock as an alternative to direct API keys.

**When Bedrock mode is enabled, ALL model calls route through Bedrock** - no direct API calls are made.

### Bedrock Setup

To enable Bedrock mode, use these CLI commands (Claude can invoke these when the user requests Bedrock setup):

```bash
# Enable Bedrock mode with a region
python3 "$(find ~/.claude -name debate.py -path '*adversarial-spec*' 2>/dev/null | head -1)" bedrock enable --region us-east-1

# Add models that are enabled in your Bedrock account
python3 "$(find ~/.claude -name debate.py -path '*adversarial-spec*' 2>/dev/null | head -1)" bedrock add-model claude-3-sonnet
python3 "$(find ~/.claude -name debate.py -path '*adversarial-spec*' 2>/dev/null | head -1)" bedrock add-model claude-3-haiku

# Check current configuration
python3 "$(find ~/.claude -name debate.py -path '*adversarial-spec*' 2>/dev/null | head -1)" bedrock status

# Disable Bedrock mode (revert to direct API keys)
python3 "$(find ~/.claude -name debate.py -path '*adversarial-spec*' 2>/dev/null | head -1)" bedrock disable
```

### Bedrock Model Names

Users can specify models using friendly names (e.g., `claude-3-sonnet`), which are automatically mapped to Bedrock model IDs. Built-in mappings include:

- `claude-3-sonnet`, `claude-3-haiku`, `claude-3-opus`, `claude-3.5-sonnet`
- `llama-3-8b`, `llama-3-70b`, `llama-3.1-70b`, `llama-3.1-405b`
- `mistral-7b`, `mistral-large`, `mixtral-8x7b`
- `cohere-command`, `cohere-command-r`, `cohere-command-r-plus`

Run `python3 "$(find ~/.claude -name debate.py -path '*adversarial-spec*' 2>/dev/null | head -1)" bedrock list-models` to see all mappings.

### Bedrock Configuration Location

Configuration is stored at `~/.claude/adversarial-spec/config.json`:

```json
{
  "bedrock": {
    "enabled": true,
    "region": "us-east-1",
    "available_models": ["claude-3-sonnet", "claude-3-haiku"],
    "custom_aliases": {}
  }
}
```

### Bedrock Error Handling

If a Bedrock model fails (e.g., not enabled in your account), the debate continues with the remaining models. Clear error messages indicate which models failed and why.

## Document Types

Ask the user which type of document they want to produce:

### PRD (Product Requirements Document)

Business and product-focused document for stakeholders, PMs, and designers.

**Structure:**
- Executive Summary
- Problem Statement / Opportunity
- Target Users / Personas
- User Stories / Use Cases
- Functional Requirements
- Non-Functional Requirements
- Success Metrics / KPIs
- Scope (In/Out)
- Dependencies
- Risks and Mitigations
- Timeline / Milestones (optional)

**Critique Criteria:**
1. Clear problem definition with evidence
2. Well-defined user personas with real pain points
3. User stories follow proper format (As a... I want... So that...)
4. Measurable success criteria
5. Explicit scope boundaries
6. Realistic risk assessment
7. No technical implementation details (that's for tech spec)

### Technical Specification / Architecture Document

Engineering-focused document for developers and architects.

**Structure:**
- Overview / Context
- Goals and Non-Goals
- System Architecture
- Component Design
- API Design (endpoints, request/response schemas)
- Data Models / Database Schema
- Infrastructure Requirements
- Security Considerations
- Error Handling Strategy
- Performance Requirements / SLAs
- Observability (logging, metrics, alerting)
- Testing Strategy
- Deployment Strategy
- Migration Plan (if applicable)
- Open Questions / Future Considerations

**Critique Criteria:**
1. Clear architectural decisions with rationale
2. Complete API contracts (not just endpoints, but full schemas)
3. Data model handles all identified use cases
4. Security threats identified and mitigated
5. Error scenarios enumerated with handling strategy
6. Performance targets are specific and measurable
7. Deployment is repeatable and reversible
8. No ambiguity an engineer would need to resolve

## Process

### Step 0: Gather Input and Offer Interview Mode

Ask the user:

1. **Document type**: "PRD" or "tech"
2. **Starting point**:
   - Path to existing file (e.g., `./docs/spec.md`, `~/projects/auth-spec.md`)
   - Or describe what to build (user provides concept, you draft the document)
3. **Interview mode** (optional):
   > "Would you like to start with an in-depth interview session before the adversarial debate? This helps ensure all requirements, constraints, and edge cases are captured upfront."

### Step 0.5: Interview Mode (If Selected)

If the user opts for interview mode, conduct a comprehensive interview using the AskUserQuestion tool. This is NOT a quick Q&A; it's a thorough requirements gathering session.

**If an existing spec file was provided:**
- Read the file first
- Use it as the basis for probing questions
- Identify gaps, ambiguities, and unstated assumptions

**Interview Topics (cover ALL of these in depth):**

1. **Problem & Context**
   - What specific problem are we solving? What happens if we don't solve it?
   - Who experiences this pain most acutely? How do they currently cope?
   - What prior attempts have been made? Why did they fail or fall short?

2. **Users & Stakeholders**
   - Who are all the user types (not just primary)?
   - What are their technical sophistication levels?
   - What are their privacy/security concerns?
   - What devices/environments do they use?

3. **Functional Requirements**
   - Walk through the core user journey step by step
   - What happens at each decision point?
   - What are the error cases and edge cases?
   - What data needs to flow where?

4. **Technical Constraints**
   - What systems must this integrate with?
   - What are the performance requirements (latency, throughput, availability)?
   - What scale are we designing for (now and in 2 years)?
   - Are there regulatory or compliance requirements?

5. **UI/UX Considerations**
   - What is the desired user experience?
   - What are the critical user flows?
   - What information density is appropriate?
   - Mobile vs desktop priorities?

6. **Tradeoffs & Priorities**
   - If we can't have everything, what gets cut first?
   - Speed vs quality vs cost priorities?
   - Build vs buy decisions?
   - What are the non-negotiables?

7. **Risks & Concerns**
   - What keeps you up at night about this project?
   - What could cause this to fail?
   - What assumptions are we making that might be wrong?
   - What external dependencies are risky?

8. **Success Criteria**
   - How will we know this succeeded?
   - What metrics matter?
   - What's the minimum viable outcome?
   - What would "exceeding expectations" look like?

**Interview Guidelines:**
- Ask probing follow-up questions. Don't accept surface-level answers.
- Challenge assumptions: "You mentioned X. What if Y instead?"
- Look for contradictions between stated requirements
- Ask about things the user hasn't mentioned but should have
- Continue until you have enough detail to write a comprehensive spec
- Use multiple AskUserQuestion calls to cover all topics

**After interview completion:**
1. Synthesize all answers into a complete spec document
2. Write the spec to file
3. Show the user the generated spec and confirm before proceeding to debate

### Step 1: Load or Generate Initial Document

**If user provided a file path:**
- Read the file using the Read tool
- Validate it has content
- Use it as the starting document

**If user describes what to build (no existing file, no interview mode):**

This is the primary use case. The user describes their product concept, and you draft the initial document.

1. **Ask clarifying questions first.** Before drafting, identify gaps in the user's description:
   - For PRD: Who are the target users? What problem does this solve? What does success look like?
   - For Tech Spec: What are the constraints? What systems does this integrate with? What scale is expected?
   - Ask 2-4 focused questions. Do not proceed until you have enough context to write a complete draft.

2. **Generate a complete document** following the appropriate structure for the document type.
   - Be thorough. Cover all sections even if some require assumptions.
   - State assumptions explicitly so opponent models can challenge them.
   - For PRDs: Include placeholder metrics that the user can refine (e.g., "Target: X users in Y days").
   - For Tech Specs: Include concrete choices (database, framework, etc.) that can be debated.

3. **Present the draft for user review** before sending to opponent models:
   - Show the full document
   - Ask: "Does this capture your intent? Any changes before we start the adversarial review?"
   - Incorporate user feedback before proceeding

Output format (whether loaded or generated):
```
[SPEC]
<document content here>
[/SPEC]
```

### Step 2: Select Opponent Models

First, check which API keys are configured:

```bash
python3 "$(find ~/.claude -name debate.py -path '*adversarial-spec*' 2>/dev/null | head -1)" providers
```

Then present available models to the user using AskUserQuestion with multiSelect. Build the options list based on which API keys are set:

**If OPENAI_API_KEY is set, include:**
- `gpt-4o` - Fast, good for general critique
- `o1` - Stronger reasoning, slower

**If ANTHROPIC_API_KEY is set, include:**
- `claude-sonnet-4-20250514` - Claude 3.5 Sonnet v2, excellent reasoning
- `claude-opus-4-20250514` - Claude 3 Opus, highest capability

**If GEMINI_API_KEY is set, include:**
- `gemini/gemini-2.0-flash` - Fast, good balance

**If XAI_API_KEY is set, include:**
- `xai/grok-3` - Alternative perspective

**If MISTRAL_API_KEY is set, include:**
- `mistral/mistral-large` - European perspective

**If GROQ_API_KEY is set, include:**
- `groq/llama-3.3-70b-versatile` - Fast open-source

**If DEEPSEEK_API_KEY is set, include:**
- `deepseek/deepseek-chat` - Cost-effective

**If ZHIPUAI_API_KEY is set, include:**
- `zhipu/glm-4` - Chinese language model
- `zhipu/glm-4-plus` - Enhanced GLM model

**If Codex CLI is installed, include:**
- `codex/gpt-5.2-codex` - OpenAI Codex with extended reasoning

**If Gemini CLI is installed, include:**
- `gemini-cli/gemini-3-pro-preview` - Google Gemini 3 Pro
- `gemini-cli/gemini-3-flash-preview` - Google Gemini 3 Flash

Use AskUserQuestion like this:
```
question: "Which models should review this spec?"
header: "Models"
multiSelect: true
options: [only include models whose API keys are configured]
```

More models = more perspectives = stricter convergence.

### Step 3: Send to Opponent Models for Critique

Run the debate script with selected models:

```bash
python3 "$(find ~/.claude -name debate.py -path '*adversarial-spec*' 2>/dev/null | head -1)" critique --models MODEL_LIST --doc-type TYPE <<'SPEC_EOF'
<paste your document here>
SPEC_EOF
```

Replace:
- `MODEL_LIST`: comma-separated models from user selection
- `TYPE`: either `prd` or `tech`

The script calls all models in parallel and returns each model's critique or `[AGREE]`.

### Step 4: Review, Critique, and Iterate

**Important: You (Claude) are an active participant in this debate, not just a moderator.** After receiving opponent model responses, you must:

1. **Provide your own independent critique** of the current spec
2. **Evaluate opponent critiques** for validity
3. **Synthesize all feedback** (yours + opponent models) into revisions
4. **Explain your reasoning** to the user

Display your active participation clearly:
```
--- Round N ---
Opponent Models:
- [Model A]: <agreed | critiqued: summary>
- [Model B]: <agreed | critiqued: summary>

Claude's Critique:
<Your own independent analysis of the spec. What did you find that the opponent models missed? What do you agree/disagree with?>

Synthesis:
- Accepted from Model A: <what>
- Accepted from Model B: <what>
- Added by Claude: <your contributions>
- Rejected: <what and why>
```

**Handling Early Agreement (Anti-Laziness Check):**

If any model says `[AGREE]` within the first 2 rounds, be skeptical. Press the model by running another critique round with explicit instructions:

```bash
python3 "$(find ~/.claude -name debate.py -path '*adversarial-spec*' 2>/dev/null | head -1)" critique --models MODEL_NAME --doc-type TYPE --press <<'SPEC_EOF'
<spec here>
SPEC_EOF
```

The `--press` flag instructs the model to:
- Confirm it read the ENTIRE document
- List at least 3 specific sections it reviewed
- Explain WHY it agrees (what makes the spec complete)
- Identify ANY remaining concerns, however minor

If the model truly agrees after being pressed, output to the user:
```
Model X confirms agreement after verification:
- Sections reviewed: [list]
- Reason for agreement: [explanation]
- Minor concerns noted: [if any]
```

If the model was being lazy and now has critiques, continue the debate normally.

**If ALL models (including you) agree:**
- Proceed to Step 5 (Finalize and Output)

**If ANY participant (model or you) has critiques:**
1. List every distinct issue raised across all participants
2. For each issue, determine if it is valid (addresses a real gap) or subjective (style preference)
3. **If a critique raises a question that requires user input, ask the user before revising.** Examples:
   - "Model X suggests adding rate limiting. What are your expected traffic patterns?"
   - "I noticed the auth mechanism is unspecified. Do you have a preference (OAuth, API keys, etc.)?"
   - Do not guess on product decisions. Ask.
4. Address all valid issues in your revision
5. If you disagree with a critique, explain why in your response
6. Output the revised document incorporating all accepted feedback
7. Go back to Step 3 with your new document

**Handling conflicting critiques:**
- If models suggest contradictory changes, evaluate each on merit
- If the choice is a product decision (not purely technical), ask the user which approach they prefer
- Choose the approach that best serves the document's audience
- Note the tradeoff in your response

### Step 5: Finalize and Output Document

When ALL opponent models AND you have said `[AGREE]`:

**Before outputting, perform a final quality check:**

1. **Completeness**: Verify every section from the document structure is present and substantive
2. **Consistency**: Ensure terminology, formatting, and style are uniform throughout
3. **Clarity**: Remove any ambiguous language that could be misinterpreted
4. **Actionability**: Confirm stakeholders can act on this document without asking follow-up questions

**For PRDs, verify:**
- Executive summary captures the essence in 2-3 paragraphs
- User personas have names, roles, goals, and pain points
- Every user story follows "As a [persona], I want [action] so that [benefit]"
- Success metrics have specific numeric targets and measurement methods
- Scope explicitly lists what is OUT as well as what is IN

**For Tech Specs, verify:**
- Architecture diagram or description shows all components and their interactions
- Every API endpoint has method, path, request schema, response schema, and error codes
- Data models include field types, constraints, indexes, and relationships
- Security section addresses authentication, authorization, encryption, and input validation
- Performance targets include specific latency, throughput, and availability numbers

**Output the final document:**

1. Print the complete, polished document to terminal
2. Write it to `spec-output.md` in current directory
3. Print a summary:
   ```
   === Debate Complete ===
   Document: [PRD | Technical Specification]
   Rounds: N
   Models: [list of opponent models]
   Claude's contributions: [summary of what you added/changed]

   Key refinements made:
   - [bullet points of major changes from initial to final]
   ```
4. If Telegram enabled:
   ```bash
   python3 "$(find ~/.claude -name debate.py -path '*adversarial-spec*' 2>/dev/null | head -1)" send-final --models MODEL_LIST --doc-type TYPE --rounds N <<'SPEC_EOF'
   <final document here>
   SPEC_EOF
   ```

### Step 6: User Review Period

**After outputting the finalized document, give the user a review period:**

> "The document is finalized and written to `spec-output.md`. Please review it and let me know if you have any feedback, changes, or concerns.
>
> Options:
> 1. **Accept as-is** - Document is complete
> 2. **Request changes** - Tell me what to modify, and I'll update the spec
> 3. **Run another review cycle** - Send the updated spec through another adversarial debate"

**If user requests changes:**
1. Make the requested modifications to the spec
2. Show the updated sections
3. Write the updated spec to file
4. Ask again: "Changes applied. Would you like to accept, make more changes, or run another review cycle?"

**If user wants another review cycle:**
- Proceed to Step 7 (Additional Review Cycles)

**If user accepts:**
- Proceed to Step 8 (PRD to Tech Spec, if applicable)

### Step 7: Additional Review Cycles (Optional)

After the user review period, or if explicitly requested:

> "Would you like to run an additional adversarial review cycle for extra validation?"

**If yes:**

1. Ask if they want to use the same models or different ones:
   > "Use the same models (MODEL_LIST), or specify different models for this cycle?"

2. Run the adversarial debate again from Step 2 with the current document as input.

3. Track cycle count separately from round count:
   ```
   === Cycle 2, Round 1 ===
   ```

4. When this cycle reaches consensus, return to Step 6 (User Review Period).

5. Update the final summary to reflect total cycles:
   ```
   === Debate Complete ===
   Document: [PRD | Technical Specification]
   Cycles: 2
   Total Rounds: 5 (Cycle 1: 3, Cycle 2: 2)
   Models: Cycle 1: [models], Cycle 2: [models]
   Claude's contributions: [summary across all cycles]
   ```

**Use cases for additional cycles:**
- First cycle with faster/cheaper models (gpt-4o), second cycle with stronger models (o1, claude-opus)
- First cycle for structure and completeness, second cycle for security or performance focus
- Fresh perspective after user-requested changes

### Step 8: PRD to Tech Spec Continuation (Optional)

**If the completed document was a PRD**, ask the user:

> "PRD is complete. Would you like to continue into a Technical Specification based on this PRD?"

If yes:
1. Use the finalized PRD as context and requirements input
2. Optionally offer interview mode again for technical details
3. Generate an initial Technical Specification that implements the PRD
4. Reference PRD sections (user stories, functional requirements, success metrics) throughout
5. Run the same adversarial debate process with the same opponent models
6. Output the tech spec to `tech-spec-output.md`

This creates a complete PRD + Tech Spec pair from a single session.

## Convergence Rules

- Maximum 10 rounds per cycle (ask user to continue if reached)
- ALL models AND Claude must agree for convergence
- More models = stricter convergence (each adds a perspective)
- Do not agree prematurely - only accept when document is genuinely complete
- Apply critique criteria rigorously based on document type

**Quality over speed**: The goal is a document that needs no further refinement. If any participant raises a valid concern, address it thoroughly. A spec that takes 7 rounds but is bulletproof is better than one that converges in 2 rounds with gaps.

**When to say [AGREE]**: Only agree when you would confidently hand this document to:
- For PRD: A product team starting implementation planning
- For Tech Spec: An engineering team starting a sprint

**Skepticism of early agreement**: If opponent models agree too quickly (rounds 1-2), they may not have read the full document carefully. Always press for confirmation.

## Telegram Integration (Optional)

Enable real-time notifications and human-in-the-loop feedback. Only active with `--telegram` flag.

### Setup

1. Message @BotFather on Telegram, send `/newbot`, follow prompts
2. Copy the bot token
3. Run setup:
   ```bash
   python3 "$(find ~/.claude -name telegram_bot.py -path '*adversarial-spec*' 2>/dev/null | head -1)" setup
   ```
4. Message your bot, then run setup again to get chat ID
5. Set environment variables:
   ```bash
   export TELEGRAM_BOT_TOKEN="your-token"
   export TELEGRAM_CHAT_ID="your-chat-id"
   ```

### Usage

```bash
python3 debate.py critique --model gpt-4o --doc-type tech --telegram <<'SPEC_EOF'
<document here>
SPEC_EOF
```

After each round:
- Bot sends summary to Telegram
- 60 seconds to reply with feedback (configurable via `--poll-timeout`)
- Reply incorporated into next round
- No reply = auto-continue

## Advanced Features

### Critique Focus Modes

Direct models to prioritize specific concerns using `--focus`:

```bash
python3 debate.py critique --models gpt-4o --focus security --doc-type tech <<'SPEC_EOF'
<spec here>
SPEC_EOF
```

**Available focus areas:**
- `security` - Authentication, authorization, input validation, encryption, vulnerabilities
- `scalability` - Horizontal scaling, sharding, caching, load balancing, capacity planning
- `performance` - Latency targets, throughput, query optimization, memory usage
- `ux` - User journeys, error states, accessibility, mobile experience
- `reliability` - Failure modes, circuit breakers, retries, disaster recovery
- `cost` - Infrastructure costs, resource efficiency, build vs buy

Run `python3 debate.py focus-areas` to see all options.

### Model Personas

Have models critique from specific professional perspectives using `--persona`:

```bash
python3 debate.py critique --models gpt-4o --persona "security-engineer" --doc-type tech <<'SPEC_EOF'
<spec here>
SPEC_EOF
```

**Available personas:**
- `security-engineer` - Thinks like an attacker, paranoid about edge cases
- `oncall-engineer` - Cares about observability, error messages, debugging at 3am
- `junior-developer` - Flags ambiguity and tribal knowledge assumptions
- `qa-engineer` - Identifies missing test scenarios and acceptance criteria
- `site-reliability` - Focuses on deployment, monitoring, incident response
- `product-manager` - Focuses on user value and success metrics
- `data-engineer` - Focuses on data models and ETL implications
- `mobile-developer` - API design from mobile perspective
- `accessibility-specialist` - WCAG compliance, screen reader support
- `legal-compliance` - GDPR, CCPA, regulatory requirements

Run `python3 debate.py personas` to see all options.

Custom personas also work: `--persona "fintech compliance officer"`

### Context Injection

Include existing documents as context for the critique using `--context`:

```bash
python3 debate.py critique --models gpt-4o --context ./existing-api.md --context ./schema.sql --doc-type tech <<'SPEC_EOF'
<spec here>
SPEC_EOF
```

Use cases:
- Include existing API documentation that the new spec must integrate with
- Include database schemas the spec must work with
- Include design documents or prior specs for consistency
- Include compliance requirements documents

### Session Persistence and Resume

Long debates can crash or need to pause. Sessions save state automatically:

```bash
# Start a named session
python3 debate.py critique --models gpt-4o --session my-feature-spec --doc-type tech <<'SPEC_EOF'
<spec here>
SPEC_EOF

# Resume where you left off (no stdin needed)
python3 debate.py critique --resume my-feature-spec

# List all sessions
python3 debate.py sessions
```

Sessions save:
- Current spec state
- Round number
- All configuration (models, focus, persona, preserve-intent)
- History of previous rounds

Sessions are stored in `~/.config/adversarial-spec/sessions/`.

### Auto-Checkpointing

When using sessions, each round's spec is saved to `.adversarial-spec-checkpoints/` in the current directory:

```
.adversarial-spec-checkpoints/
├── my-feature-spec-round-1.md
├── my-feature-spec-round-2.md
└── my-feature-spec-round-3.md
```

Use these to rollback if a revision makes things worse.

### Retry on API Failure

API calls automatically retry with exponential backoff (1s, 2s, 4s) up to 3 times. If a model times out or rate-limits, you'll see:

```
Warning: gpt-4o failed (attempt 1/3): rate limit exceeded. Retrying in 1.0s...
```

If all retries fail, the error is reported and other models continue.

### Response Validation

If a model provides critique but doesn't include proper `[SPEC]` tags, a warning is displayed:

```
Warning: gpt-4o provided critique but no [SPEC] tags found. Response may be malformed.
```

This catches cases where models forget to format their revised spec correctly.

### Preserve Intent Mode

Convergence can collapse toward lowest-common-denominator interpretations, sanding off novel design choices. The `--preserve-intent` flag makes removals expensive:

```bash
python3 debate.py critique --models gpt-4o --preserve-intent --doc-type tech <<'SPEC_EOF'
<spec here>
SPEC_EOF
```

When enabled, models must:

1. **Quote exactly** what they want to remove or substantially change
2. **Justify the harm** - not just "unnecessary" but what concrete problem it causes
3. **Distinguish error from preference**:
   - ERRORS: Factually wrong, contradictory, or technically broken (remove/fix)
   - RISKS: Security holes, scalability issues, missing error handling (flag)
   - PREFERENCES: Different style, structure, or approach (DO NOT remove)
4. **Ask before removing** unusual but functional choices

This shifts the default from "sand off anything unusual" to "add protective detail while preserving distinctive choices."

**Use when:**
- Your spec contains intentional unconventional choices
- You want models to challenge your ideas, not homogenize them
- Previous rounds removed things you wanted to keep
- You're refining an existing spec that represents deliberate decisions

Can be combined with other flags: `--preserve-intent --focus security`

### Cost Tracking

Every critique round displays token usage and estimated cost:

```
=== Cost Summary ===
Total tokens: 12,543 in / 3,221 out
Total cost: $0.0847

By model:
  gpt-4o: $0.0523 (8,234 in / 2,100 out)
  gemini/gemini-2.0-flash: $0.0324 (4,309 in / 1,121 out)
```

Cost is also included in JSON output and Telegram notifications.

### Saved Profiles

Save frequently used configurations as profiles:

**Create a profile:**
```bash
python3 debate.py save-profile strict-security --models gpt-4o,gemini/gemini-2.0-flash --focus security --doc-type tech
```

**Use a profile:**
```bash
python3 debate.py critique --profile strict-security <<'SPEC_EOF'
<spec here>
SPEC_EOF
```

**List profiles:**
```bash
python3 debate.py profiles
```

Profiles are stored in `~/.config/adversarial-spec/profiles/`.

Profile settings can be overridden by explicit flags.

### Diff Between Rounds

Generate a unified diff between spec versions:

```bash
python3 debate.py diff --previous round1.md --current round2.md
```

Use this to see exactly what changed between rounds. Helpful for:
- Understanding what feedback was incorporated
- Reviewing changes before accepting
- Documenting the evolution of the spec

### Export to Task List

Extract actionable tasks from a finalized spec:

```bash
cat spec-output.md | python3 debate.py export-tasks --models gpt-4o --doc-type prd
```

Output includes:
- Title
- Type (user-story, task, spike, bug)
- Priority (high, medium, low)
- Description
- Acceptance criteria

Use `--json` for structured output suitable for importing into issue trackers:

```bash
cat spec-output.md | python3 debate.py export-tasks --models gpt-4o --doc-type prd --json > tasks.json
```

## Script Reference

```bash
# Core commands
python3 debate.py critique --models MODEL_LIST --doc-type TYPE [OPTIONS] < spec.md
python3 debate.py critique --resume SESSION_ID
python3 debate.py diff --previous OLD.md --current NEW.md
python3 debate.py export-tasks --models MODEL --doc-type TYPE [--json] < spec.md

# Info commands
python3 debate.py providers      # List supported providers and API key status
python3 debate.py focus-areas    # List available focus areas
python3 debate.py personas       # List available personas
python3 debate.py profiles       # List saved profiles
python3 debate.py sessions       # List saved sessions

# Profile management
python3 debate.py save-profile NAME --models ... [--focus ...] [--persona ...]

# Telegram
python3 debate.py send-final --models MODEL_LIST --doc-type TYPE --rounds N < spec.md
```

**Critique options:**
- `--models, -m` - Comma-separated model list (auto-detects from available API keys if not specified)
- `--doc-type, -d` - Document type: prd or tech (default: tech)
- `--round, -r` - Current round number (default: 1)
- `--focus, -f` - Focus area for critique
- `--persona` - Professional persona for critique
- `--context, -c` - Context file (can be used multiple times)
- `--profile` - Load settings from saved profile
- `--preserve-intent` - Require explicit justification for any removal
- `--session, -s` - Session ID for persistence and checkpointing
- `--resume` - Resume a previous session by ID
- `--press, -p` - Anti-laziness check for early agreement
- `--telegram, -t` - Enable Telegram notifications
- `--poll-timeout` - Telegram reply timeout in seconds (default: 60)
- `--json, -j` - Output as JSON
- `--codex-search` - Enable web search for Codex CLI models (allows researching current info)
