---
name: skill-learning-patterns
description: Use when agents discover better patterns, find gaps or inaccuracies in existing skills, or need to contribute validated improvements to shared knowledge, or found unique experience that could be shared with others.
---

# Skill Learning Patterns

This meta-skill teaches agents to recognize valuable learnings during their work and contribute improvements back to the communal skill repository through pull requests.

## Core Philosophy

This repository is a **living knowledge base** that improves through collective learning. As agents work on tasks, they discover:
- Better approaches than documented
- Missing error handling cases
- Gaps in existing skills
- Clearer ways to explain patterns
- New patterns worth capturing

These discoveries should flow back into the repository so all agents benefit.

**Critical principle:** Skills must contain **general-purpose knowledge** that helps many agents across different contexts. This is not a place for project-specific configurations, personal preferences, or one-off solutions. Focus on patterns, principles, and practices that are broadly applicable.

## When to Use This Skill

Use this skill when:
- You discover something that took significant time to figure out
- Existing skill instructions led you astray or were incomplete
- You find yourself repeatedly solving the same undocumented problem
- You correct a mistake based on learning what actually works
- You notice a pattern emerging across multiple tasks
- You want to improve or clarify existing documentation

## Learning Recognition Process

### 1. Notice Patterns During Work

Pay attention to signals that indicate learnable moments:

**Time investment signals:**
- "I spent 20+ minutes debugging this"
- "I tried 3 approaches before finding what worked"
- "I wish I had known this at the start"

**Repetition signals:**
- "This is the third time I've solved this"
- "I remember encountering this before"
- "Other agents probably face this too"

**Correction signals:**
- "The skill said X, but Y actually works better"
- "I misunderstood the instruction and it caused problems"
- "This approach failed in ways not documented"

Consult `references/recognizing-learnings.md` for detailed patterns.

### 2. Validate the Learning

Before proposing changes, validate based on contribution type:

**For Tool/SDK Documentation:**
- ✅ Tool is widely-used (1000+ GitHub stars, top search result, or first-party product)
- ✅ Shares battle-tested insights beyond official docs (what you struggled with, not basic usage)
- ✅ Well-documented with working examples
- ✅ Accurate and up-to-date
- ❌ NOT just "getting started" guides (official docs already cover that)

**For Pattern Contributions:**
- ✅ **Is this generalizable beyond your specific context?** (Most critical)
- ✅ Have you seen this pattern multiple times? (2-3+ instances)
- ✅ Did you test that your approach works better?
- ✅ Does this address a real gap vs. personal preference?
- ✅ Are there edge cases or tradeoffs to consider?
- ✅ Framework-specific patterns require validation through real agent experience (not just "well-established practices")

See `references/validation-criteria.md` for detailed guidance.

### 3. Determine Contribution Type

**Update existing skill** when:
- Skill has incorrect or outdated information
- Skill is missing an important case or pattern
- Instructions are unclear and caused confusion
- Examples would help but are missing

**Create new skill** when:
- Tool/SDK: Widely-used tool (1000+ stars/top search result/first-party product) with battle-tested insights
- Pattern: Appears frequently (3+ times) across different contexts and isn't documented
- Knowledge would benefit many agents across different projects (not just your specific setup)

**Do NOT contribute** when:
- Learning is specific to your project/context (e.g., "Our API endpoint is X")
- Solution only works in your unique environment
- It's a personal preference without objective benefit
- It's a one-off workaround for unusual situation
- Knowledge is too narrow to help other agents

**Note in conversation only** when:
- Learning might be valuable but needs more validation
- Pattern needs more observation before documenting
- Temporary workaround that might become obsolete

### 4. Contribute via Pull Request

**Important:** All contributions go through pull requests, not direct commits to main.

**PR workflow:**
1. Create a feature branch for your changes
2. Make updates to skill(s)
3. Test that changes improve clarity/correctness
4. Write clear PR description with rationale
5. Submit PR for review
6. Respond to feedback and iterate

Consult `references/pr-workflow.md` for detailed process.

## Contribution Quality Standards

### Good Contributions Include

**Clear rationale:**
```
"I encountered rate limiting with multiple API providers 5 times. Added exponential 
backoff pattern with jitter which resolved all instances. This pattern 
isn't documented anywhere in the skills catalog."
```

**Before/after comparison:**
```
Before: "Use full rewrites for updates"
After: "Use append-only updates for concurrent writes (safer), use full rewrites 
only for single-agent exclusive access"
Why: Prevents data loss in multi-agent scenarios
```

**Evidence of validation:**
```
"Tested across 3 different projects, pattern held. Also confirmed in 
product docs. Previous approach caused data loss 2/3 times."
```

**Preserved existing knowledge:**
- Don't delete working information
- Build on rather than replace
- Add context, don't remove context

### Avoid These Anti-Patterns

❌ **Premature optimization** - Changing after single instance without validation

❌ **Over-generalization** - "This worked for me once" → "Always do this"

❌ **Opinion as fact** - Personal preference without objective improvement

❌ **Churn** - Changes that are different but not better

❌ **Deleting context** - Removing information that might help others

## Common Pitfalls

Even well-intentioned contributions can miss the mark. Here are patterns to watch for:

### Pitfall 1: The Specificity Trap

**Pattern:** Documenting your specific solution instead of extracting the general pattern.

**Example - TOO SPECIFIC:**
```
Skill: `<example-skill>` (git workflow conventions)
Content: "Always end commits with: Written by <name> ◯ <organization>"
Problem: This is a personal preference, not general knowledge
```

**Example - APPROPRIATELY GENERAL:**
```
Skill: `<example-skill>` (revised concept for discovering repo conventions)
Content: "Check repository for commit conventions in CONTRIBUTING.md or recent commits"
Better: Teaches pattern of discovering conventions, applies to any repository
```

**How to avoid:**
- Ask: "Would this help an agent on a completely different project?"
- Look for personal names, specific URLs, environment-specific configs
- Extract the pattern, not just your implementation

### Pitfall 2: Documentation vs. Specialized Knowledge

**Pattern:** Creating skills that just reformat well-known documentation.

**Example - JUST DOCUMENTATION:**
```
Skill: "How to use git"
Content: Explains git commands, branching, committing, PR creation
Problem: This is standard git knowledge available everywhere
```

**Example - SPECIALIZED KNOWLEDGE:**
```
Skill: `<example-skill>` (protocol server builder in this repository)
Content: Patterns for creating servers - not just "how to use the protocol" 
but specific guidance on tool design, error handling patterns, testing strategies
Better: Takes general protocol knowledge and adds specialized patterns for building quality servers
```

**How to avoid:**
- If official docs cover it well, link to docs instead of recreating
- Ask: "What specialized insight am I adding beyond standard documentation?"
- Focus on non-obvious patterns, edge cases, or agent-specific considerations

### Pitfall 3: Over-Generalizing From One Instance

**Pattern:** "I made one mistake" → "Let's create 3 new skills to prevent it"

**Real example from this repository (November 2025):**
```
Observation: One agent submitted overly-specific `<example-skill>` (git workflow conventions)
Initial reaction: "We need CULTURE.md + 3 new skills (knowledge-curation, 
agent-human-collaboration, pattern-recognition) + extended documentation"
Correction: Another agent called this out as the exact over-generalization we warn against
Right-sized solution: Add this "Common Pitfalls" section instead
Learning: The system worked - peer review caught premature abstraction
```

**How to avoid:**
- Count your data points: 1 occurrence = note it, 3+ = consider contributing
- Check if existing skill can be extended instead of creating new one
- Ask: "Am I solving a real recurring problem or reacting to one experience?"

### Pitfall 4: The Abstraction Ladder Confusion

Understanding where your learning sits on the abstraction ladder:

**Level 1 - Specific Solution (TOO LOW for skills):**
```
"I configured Firebase Auth with Google OAuth by setting these environment 
variables and calling these specific API endpoints"
→ Too specific, only helps others using Firebase + Google OAuth
```

**Level 2 - Pattern (GOOD for skills):**
```
"OAuth integration strategies: Provider discovery, token management, callback 
handling, session persistence. Applies to Google, GitHub, Microsoft, etc."
→ General enough to help with any OAuth integration
```

**Level 3 - Principle (ALSO GOOD for skills):**
```
"Delegating authentication to specialized providers: Trade-offs between 
managed auth services vs. self-hosted, security considerations, user experience"
→ Helps with authentication decisions broadly
```

**Where to contribute:**
- Level 1: Keep in project-specific docs or memory, not skills
- Level 2: Perfect for skills - concrete patterns that generalize
- Level 3: Great for skills - principles that apply across domains

**How to climb the ladder:**
- Start with: "What did I do?"
- Extract: "What pattern was I following?"
- Distill: "What principle guided this?"
- Contribute at Level 2 or 3

### Pitfall 5: Personal Preferences as Best Practices

**Pattern:** "I like doing it this way" → "Everyone should do it this way"

**Example:**
```
"Always use arrow functions in JavaScript"
"Always put API calls in src/api/ directory"  
"Always use the premium model over the balanced model"
→ These are preferences without objective evidence of superiority
```

**How to avoid:**
- Ask: "Can I measure why this is better?" (speed, reliability, cost, etc.)
- Consider: "Are there valid reasons someone would choose differently?"
- Test: "Does this improve outcomes or just match my style?"

### Pitfall 6: Fragmenting Information

**Pattern:** Creating new skills/docs when information should be added to existing ones.

**Signs you're fragmenting:**
- New skill significantly overlaps with existing skill's domain
- Information could be a section in existing skill
- Creates "which skill do I check?" confusion
- Duplicates concepts across multiple skills

**How to avoid:**
- Review existing skills in the domain first
- Ask: "Does this extend an existing skill or truly need separate space?"
- Bias toward extending existing skills unless clearly distinct domain

### Self-Check Before Contributing

Ask yourself:

1. ❓ Is this **general** enough? (Would it help agents on different projects?)
2. ❓ Is this **specialized** enough? (Does it add insight beyond standard docs?)
3. ❓ Is this **validated** enough? (Have I seen this pattern 2+ times?)
4. ❓ Is this **objective** enough? (Based on evidence, not preference?)
5. ❓ Is this **appropriately placed**? (New skill vs. extend existing vs. don't contribute?)

If you can confidently answer yes to all five → Contribute

If you're unsure on any → More validation needed or reconsider contribution type

## PR Description Template

Use this template for skill contributions:

```markdown
## What

[Brief description of what's changing]

## Why

[Problem you encountered / gap you found / improvement opportunity]

## Evidence

[How you validated this is better / how you tested / how often you saw this]

## Impact

[Who benefits / what situations this helps / what it prevents]

## Testing

[How you verified the change works / examples you tried]
```

See `references/contribution-examples.md` for real examples.

## Example Workflows

### Workflow 1: Correcting Existing Skill

```
During task: "Following `<example-skill>` (shared state updates), I used full-rewrite updates for 
concurrent writes. Result: data loss when two agents wrote simultaneously."

Validation: "Checked references/<example-reference>.md (concurrency guidance) - it says append-only updates are 
safer but warning wasn't prominent. Tested append-only updates with concurrent 
writes - no data loss."

Action: 
1. Create feature branch: fix/<example-skill>-concurrency-warning
2. Update SKILL.md to make warning more prominent
3. Add concrete example of data loss scenario
4. Create PR: "Emphasize append-only updates for concurrent writes"
5. Explain in PR: "Misread the guidance, led to data loss. Making warning 
   more visible to prevent this for other agents."
```

### Workflow 2: Adding Missing Pattern

```
During task: "Hit API rate limits 5 times across different projects. 
Spent 30min each time figuring out exponential backoff."

Validation: "Pattern works consistently. Checked the skills catalog - not documented. 
This is generalizable beyond my specific use case."

Action:
1. Create feature branch: add/<example-skill>-rate-limiting
2. Create new skill: .claude/skills/<example-skill>/ (API rate limiting patterns)
3. Document exponential backoff pattern with code examples
4. Create PR: "Add API rate limiting patterns"
5. Explain: "Common pattern that caused repeated debugging time. Validated 
   across 5 instances with different APIs."
```

### Workflow 3: Clarifying Ambiguity

```
During task: "Skill said 'use appropriate model' but didn't define criteria. 
Tried premium, balanced, and budget model tiers before finding best fit."

Validation: "Through testing, identified that task complexity + budget 
constraints should guide model choice. This clarification would have saved 
1 hour."

Action:
1. Create feature branch: clarify/<example-skill>-selection-criteria  
2. Add decision tree to skill
3. Include examples: "For X task → Y model because Z"
4. Create PR: "Add model selection decision tree"
5. Explain: "Ambiguous guidance led to trial-and-error. Adding decision 
   criteria to help agents choose upfront."
```

## Self-Correction Culture

**When you make mistakes:**
- Note what you learned
- Update relevant skill if gap exists
- Don't just fix the instance, prevent future instances

**When you discover better approaches:**
- Compare objectively with current documented approach
- Test to validate improvement
- Propose update with clear reasoning

**When skills lead you astray:**
- Don't assume skill is wrong without investigation
- Validate your alternative approach
- If truly better, propose improvement with evidence

## Validation Questions

Before submitting PR, ask:

1. Is this a genuine improvement or just different?
2. Have I validated this works better?
3. Is my evidence strong enough?
4. Am I preserving existing valid knowledge?
5. Will other agents benefit from this?
6. Is my PR description clear about what and why?

## Building on Others

**Attribution:**
- Reference existing skills you're building on
- Credit agents/humans whose insights helped
- Link to forum discussions or sources

**Collaboration:**
- Respond to PR feedback constructively
- Iterate based on reviewer insights
- Merge after approval, don't force through

**Continuous improvement:**
- Your contribution will be built upon by others
- This is expected and encouraged
- Living knowledge base means constant evolution

## Next Steps

After contributing:
1. Watch for PR feedback and respond
2. Note if your learning helps in future tasks
3. Continue pattern recognition in your work
4. Build on what you contributed as you learn more

The goal: **A knowledge base that gets smarter with every agent interaction.**
