---
name: multi-ai-consultant
description: Consult external AIs (Gemini 2.5 Pro, OpenAI Codex, Claude) for second opinions. Use for debugging failures, architectural decisions, security validation, or need fresh perspective with synthesis.
license: MIT
allowed-tools: [Bash, Read, Task, Write]
metadata:
  version: 1.0.0
  author: Claude Skills Maintainers
  last-verified: 2025-11-07
  production-tested: true
  keywords:
    - ai consultation
    - second opinion
    - gemini
    - openai
    - codex
    - debugging
    - architecture
    - multi-ai
    - synthesis
    - fresh perspective
    - stuck
    - web research
    - thinking mode
    - repo-aware
---

# Multi-AI Consultant

Consult external AIs for second opinions when Claude Code is stuck or making critical decisions.

---

## What This Skill Does

This skill enables **future Claude Code sessions** to consult other AIs when:
- Stuck on a bug after one failed attempt
- Making architectural decisions
- Security concerns need validation
- Fresh perspective needed

**Key innovation**: Uses existing CLI tools (`gemini`, `codex`) instead of building MCP servers - much simpler and more maintainable.

---

## When to Use This Skill

### Automatic Triggers (No User Action Needed)

Claude Code should **automatically suggest** using this skill when:

1. **After 1 failed debugging attempt**
   - Tried one approach to fix a bug
   - Still not working or different error
   - → Suggest: "Should I consult [Gemini|Fresh Claude] for a second opinion?"

2. **Before architectural decisions**
   - Significant design choices (state management, routing, data flow)
   - Framework selection
   - Database schema design
   - → Auto-consult (mention to user): "Consulting Gemini for architectural validation..."

3. **Security changes**
   - Authentication logic
   - Authorization rules
   - Cryptography
   - Input validation
   - → Auto-consult: "Consulting Gemini to verify security approach..."

4. **When uncertain**
   - Multiple valid approaches
   - Trade-offs not clear
   - Conflicting advice in documentation
   - → Suggest: "Would you like me to consult another AI for additional perspective?"

### Manual Invocation (User Commands)

User can explicitly request consultation with:
- `/consult-gemini [question]` - Gemini 2.5 Pro with thinking, search, grounding
- `/consult-codex [question]` - OpenAI GPT-4 via Codex CLI (repo-aware)
- `/consult-claude [question]` - Fresh Claude subagent (free, fast)
- `/consult-ai [question]` - Router that asks which AI to use

---

## The Three AIs

| AI | Tool | When to Use | Special Features | Cost |
|----|------|-------------|------------------|------|
| **Gemini 2.5 Pro** | `gemini` CLI | Web research, latest docs, thinking | Google Search, extended reasoning, grounding | ~$0.10-0.50 |
| **OpenAI GPT-4** | `codex` CLI | Repo-aware analysis, code review | Auto-scans directory, OpenAI reasoning | ~$0.05-0.30 |
| **Fresh Claude** | Task tool | Quick second opinion, budget-friendly | Same capabilities, fresh perspective | Free |

**For detailed AI comparison**: Load `references/ai-strengths.md` when choosing which AI to consult for specific use cases.

---

## How It Works

### Architecture

```
Claude Code encounters bug/decision
        ↓
Suggests consultation (or user requests)
        ↓
User approves
        ↓
Execute appropriate slash command
        ↓
CLI command calls external AI
        ↓
Parse response
        ↓
Synthesize: Claude's analysis + External AI's analysis
        ↓
Present 5-part comparison
        ↓
Ask permission to implement
```

### The 5-Part Synthesis Format

Every consultation must follow this format (prevents parroting):

1. **🤖 My Analysis** - Claude's original reasoning and attempts
2. **💎/🔷/🔄 Other AI's Analysis** - External AI's complete response
3. **🔍 Key Differences** - Agreement, divergence, what each AI caught/missed
4. **⚡ Synthesis** - Combined perspective, root cause, trade-offs
5. **✅ Recommended Action** - Specific next steps with file paths/line numbers

**End with**: "Should I proceed with this approach?"

---

## Setup

**For complete installation guide**: Load `references/setup-guide.md` when installing CLIs, configuring API keys, or setting up templates.

**Quick setup**:
1. **Install CLIs**: `bun add -g @google/generative-ai-cli` (Gemini), `bun add -g codex` (Codex, optional)
2. **Set API keys**: `export GEMINI_API_KEY="..."`, `export OPENAI_API_KEY="..."`
3. **Install skill**: Symlink to `~/.claude/skills/multi-ai-consultant`
4. **Copy templates**: `GEMINI.md`, `codex.md`, `.geminiignore` to project root
5. **Verify**: `gemini -p "test"`, `codex exec - --yolo`

Get API keys:
- Gemini: https://aistudio.google.com/apikey
- OpenAI: https://platform.openai.com/api-keys

---

## Usage

**For detailed examples**: Load `references/usage-examples.md` when learning consultation workflows or seeing real-world scenarios.

**Quick examples**:
- **Bug**: After 1 failed attempt → `/consult-gemini` for web-researched solution
- **Architecture**: Design decision → `/consult-gemini` for latest best practices
- **Code review**: Refactoring validation → `/consult-codex` for repo-aware consistency check
- **Quick opinion**: Sanity check → `/consult-claude` for free fresh perspective

**5 detailed examples available**:
1. JWT authentication bug (saved ~30 min, found platform-specific issue)
2. State management choice (informed decision with 2025 patterns)
3. Refactoring review (found 3 consistency issues)
4. Security validation (found 2 critical issues via OWASP 2025)
5. Multi-AI workflow (high-stakes database choice)

---

## Slash Commands

**For complete command reference**: Load `references/commands-reference.md` when needing detailed syntax, options, or cost tracking information.

**Quick command overview**:

### /consult-gemini [question]
- **Use**: Web research, latest docs, extended thinking
- **Features**: Google Search, grounding, thinking mode
- **Cost**: ~$0.10-0.50
- **Example**: `/consult-gemini Is this JWT secure by 2025 standards?`

### /consult-codex [question]
- **Use**: Repo-aware analysis, code review
- **Features**: Auto-scans directory, consistency checks
- **Cost**: ~$0.05-0.30
- **Example**: `/consult-codex Review for performance bottlenecks`

### /consult-claude [question]
- **Use**: Quick second opinion, budget-friendly
- **Features**: Free, fast, fresh perspective
- **Cost**: Free
- **Example**: `/consult-claude Am I missing something obvious?`

### /consult-ai [question]
- **Use**: Router (recommends which AI to use)
- **Features**: Analyzes question, suggests best AI
- **Cost**: Varies by chosen AI
- **Example**: `/consult-ai How should we structure this architecture?`

---

## Templates

Templates customize AI behavior for consultations (auto-loaded from project root):

1. **GEMINI.md** - System instructions for Gemini (enforces 5-part format, web search)
2. **codex.md** - System instructions for Codex (enforces repo-aware analysis)
3. **.geminiignore** - Privacy exclusions beyond `.gitignore`
4. **consultation-log-parser.sh** - View consultation history (optional)

**Installation**: Copy from `~/.claude/skills/multi-ai-consultant/templates/` to project root

---

## Privacy & Security

**Automatic protection**:
- Both CLIs respect `.gitignore` automatically
- Create `.geminiignore` for extra exclusions (`.env*`, `*secret*`, `*credentials*`)
- Pre-consultation check warns if sensitive patterns detected

**Privacy best practices**:
- Always configure `.gitignore` properly
- Create `.geminiignore` for extra safety
- Use smart context selection (specific files, not entire repo)
- Verify what will be sent: `git status --ignored`

**For detailed privacy configuration**: Load `references/setup-guide.md` when setting up `.geminiignore` or privacy exclusions.

---

## Cost Tracking

Every consultation logged to `~/.claude/ai-consultations/consultations.log`

**Log format**: `timestamp,ai,model,input_tokens,output_tokens,cost,project_path`

**View logs**: `consultation-log-parser.sh --summary`

**Example output**:
```
Total consultations: 47
Gemini: 23 ($4.25), Codex: 12 ($1.85), Fresh Claude: 12 ($0.00)
Total cost: $6.10
```

**For detailed cost tracking**: Load `references/commands-reference.md` when viewing logs, calculating costs, or managing budgets.

---

## Common Issues

**For complete troubleshooting**: Load `references/troubleshooting.md` when encountering errors or setup issues.

**Top 5 issues**:

1. **CLI not installed**: `gemini: command not found` → Fix: `bun add -g @google/generative-ai-cli`
2. **API key invalid**: Authentication failed → Fix: `export GEMINI_API_KEY="..."`
3. **Context too large**: Token limit exceeded → Fix: Use specific files, not entire repo
4. **Privacy leak**: `.env` file sent → Fix: Add to `.gitignore` and `.geminiignore`
5. **Skill not discovered**: Not working → Fix: Check `~/.claude/skills/multi-ai-consultant`

---

## Token Efficiency

### Without This Skill

**Typical scenario** (stuck on bug):
1. Try approach 1 (~4k tokens)
2. Research CLI syntax (~3k tokens)
3. Try approach 2 (~4k tokens)
4. Research documentation (~3k tokens)
5. Try approach 3 (~4k tokens)

**Total**: ~20k tokens, 30-45 minutes

### With This Skill

**Same scenario**:
1. Try approach 1 (~4k tokens)
2. Execute `/consult-gemini` (~1k tokens)
3. Gemini finds issue (<5k tokens, billed separately)
4. Implement fix (~3k tokens)

**Total**: ~8k tokens, 5-10 minutes

**Savings**: ~60% tokens, ~75% time

---

## Success Metrics

### Time Efficiency
- **Without skill**: 30-45 minutes (trial and error)
- **With skill**: 5-10 minutes (consultation + fix)
- **Savings**: ~75%

### Token Efficiency
- **Without skill**: ~20k tokens (multiple attempts)
- **With skill**: ~8k tokens (one consultation)
- **Savings**: ~60%

### Error Prevention
- **Manual CLI use**: 3-5 common errors (flags, parsing, privacy)
- **With skill**: 0 errors (all handled by commands)
- **Prevention**: 100%

### Quality
- **Manual**: Risk of not synthesizing (just copying external AI)
- **With skill**: Forced synthesis via `GEMINI.md`/`codex.md`
- **Improvement**: Guaranteed value-add

---

## Why CLI Approach (Not MCP)?

| Aspect | MCP Server | CLI Approach |
|--------|------------|--------------|
| Setup time | 4-6 hours | 60-75 minutes |
| Complexity | High (MCP protocol) | Low (bash + CLIs) |
| Maintenance | Update MCP SDK | Update CLI (rare) |
| Flexibility | Locked to AIs | Any AI with CLI |
| Debugging | MCP protocol | Standard bash |
| Dependencies | MCP SDK, npm | Just CLIs |

**Winner**: CLI approach - 80% less effort, same functionality

---

## When to Load References

Load reference files when working on specific aspects of AI consultation:

### ai-strengths.md
Load when:
- **Selection-based**: Choosing which AI to consult (Gemini vs Codex vs Fresh Claude)
- **Comparison-based**: Understanding capabilities, costs, and trade-offs between AIs
- **Strategy-based**: Planning combination strategies (free → paid, paid first, budget-conscious)
- **Capability-based**: Understanding special features (Google Search, extended thinking, grounding, repo-aware, fresh perspective)
- **Scenario-based**: Multiple AI consultation workflows, validation workflows

### setup-guide.md
Load when:
- **Installation-based**: Setting up Gemini CLI, Codex CLI, or installing the skill
- **Configuration-based**: Configuring API keys, environment variables, or system paths
- **Privacy-based**: Setting up .geminiignore, privacy exclusions, or security configurations
- **Template-based**: Installing GEMINI.md, codex.md, .geminiignore, or consultation-log-parser.sh
- **Verification-based**: Testing CLI installation, API keys, or skill discovery

### commands-reference.md
Load when:
- **Command-based**: Using /consult-gemini, /consult-codex, /consult-claude, or /consult-ai
- **Syntax-based**: Understanding command flags, options, or context selection
- **Cost-based**: Understanding cost tracking, log format, or viewing consultation history
- **Logging-based**: Using consultation-log-parser.sh or analyzing consultation patterns

### usage-examples.md
Load when:
- **Scenario-based**: Learning how to use skill for bugs, architecture decisions, or code review
- **Workflow-based**: Understanding consultation workflow, synthesis process, or multi-AI approach
- **Example-based**: Seeing real-world examples of consultations and their outcomes (5 detailed examples available)

### troubleshooting.md
Load when:
- **Error-based**: Encountering specific errors (command not found, API key invalid, parsing failures)
- **Diagnosis-based**: Troubleshooting CLI issues, API connectivity, or skill discovery
- **Fix-based**: Resolving known issues with step-by-step solutions (8 common issues documented)
- **Debugging-based**: Testing CLIs manually, checking configurations, or verifying installations

---

## Contributing

**Found an issue?**
- Document it in troubleshooting.md
- Include fix/workaround
- Update slash commands to prevent

**Adding new AI?**
- Create new slash command: `commands/consult-newai.md`
- Add to router: Update `commands/consult-ai.md`
- Create template: `templates/newai.md` (if CLI supports system instructions)
- Update documentation

**Improving synthesis?**
- Edit templates: `templates/GEMINI.md`, `templates/codex.md`
- Test with real consultations
- Measure before/after quality

---

## References

### External Resources

- **Gemini CLI**: https://ai.google.dev/gemini-api/docs/cli
- **OpenAI Codex**: https://www.npmjs.com/package/codex
- **OpenAI API**: https://platform.openai.com/docs
- **Gemini API Pricing**: https://ai.google.dev/pricing
- **OpenAI Pricing**: https://openai.com/pricing

### Internal Files

- **Planning docs**: `planning/multi-ai-consultant-*.md`
- **Slash commands**: `commands/*.md`
- **Templates**: `templates/*`
- **Scripts**: `scripts/*`
- **References**: `references/*.md` (5 reference files)

---

## License

MIT License - See LICENSE file

---

**Last Updated**: 2025-11-07
**Status**: Production Ready
**Maintainer**: Claude Skills Maintainers | maintainers@example.com
