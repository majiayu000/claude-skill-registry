---
name: scope
description: Exploratory workflow for understanding problem spaces and drafting feature proposals, refactorings, or complex bug-fixes. Creates detailed tickets in your issue tracker without doing implementation work.
model: opus
---

# Scope - Problem Space Exploration & Ticket Creation

Helps you thoroughly understand a problem space through codebase exploration and iterative dialogue, then creates a well-specified ticket for future implementation.

**This skill does NOT write code.** It explores, questions, understands, and documents.

## Workflow

### 1. Initial Discovery

**Understand what the user wants to explore:**
- What feature are they considering?
- What refactoring are they contemplating?
- What bug needs detailed investigation?
- Is this greenfield or modifying existing code?

**Ask clarifying questions:**
- Scope and boundaries
- Problem statement
- Desired outcome (not implementation details yet)

Output: Clear understanding of what problem space to explore.

### 2. Codebase Exploration

**Use exploration tools to understand context:**
- Spawn `Explore` agent (set thoroughness based on scope: "quick", "medium", "very thorough")
- Use Grep to find relevant code patterns
- Use Read to examine key files identified
- Map out the current architecture/implementation

**For third-party dependencies:**
- Use WebFetch to read API documentation
- Clone relevant repositories to `/tmp` for examination if needed
- Understand integration points and constraints

**Exploration goals:**
- Where does this change fit in the architecture?
- What existing code will be affected?
- What patterns/conventions are already established?
- What are the integration points?
- What similar features exist that we can learn from?

Output: Comprehensive understanding of the relevant codebase areas.

### 3. Iterative Refinement

**Use AskUserQuestion to refine understanding:**
- Present what you've learned from exploration
- Ask about approaches (if multiple valid options exist)
- Clarify edge cases and requirements
- Discuss trade-offs between approaches
- Validate assumptions about existing code

**Loop until both Claude and user have:**
- Precise understanding of what to build
- Clear rationale for approach chosen
- Identified edge cases and constraints
- Agreed on acceptance criteria

**Important:** This is collaborative design, not just requirements gathering. Challenge assumptions, propose alternatives, discuss trade-offs.

Output: Shared, precise understanding of the work to be done.

### 4. Ticket Synthesis

**Draft ticket content adaptively based on type:**

**For feature proposals:**
- Problem statement (what problem does this solve?)
- Proposed solution (high-level approach)
- Acceptance criteria (specific, testable)
- Technical notes (implementation considerations, affected components)
- Security considerations (if the change introduces new attack surface, handles user input, touches auth/authz, or affects trust boundaries — note what controls will be needed. Consult the `sec-blue-teamer` agent if the implications are non-obvious.)
- Out of scope (what explicitly won't be done)
- Open questions (if any remain)

**For refactorings:**
- Current state (what's problematic about existing code)
- Desired state (what we want it to look like)
- Motivation (why is this worth doing)
- Approach (high-level refactoring strategy)
- Risk assessment (what could go wrong)
- Affected areas (files/modules that will change)

**For complex bug fixes:**
- Bug description (observed behavior)
- Root cause (from your exploration)
- Proposed fix (high-level approach)
- Why this happened (what allowed the bug)
- Verification plan (how to confirm fix works)
- Regression prevention (tests/checks to prevent recurrence)

**Format guidelines:**
- Use markdown
- Be specific, not vague
- Include code references (file paths, line numbers, function names)
- Link to relevant documentation or issues
- Make it actionable (someone else should be able to implement from this)

Output: Draft ticket content for user review.

### 5. Review & Refine Ticket

**Present draft to user:**
- Show complete ticket content
- Highlight any areas of uncertainty
- Ask if anything is missing or unclear

**Iterate if needed:**
- Adjust based on feedback
- Add missing details
- Clarify ambiguous sections

Output: Approved ticket content ready to create.

### 6. Create Ticket

**Detect issue tracker:**
- Check `CLAUDE.md` for tracker preference and integration method
- Auto-detect from git remote URL if not specified
- Use available integration (CLI, MCP server, or API)

**Create ticket using available integration:**
- Use platform integration to create issue
- Pass title and body
- Apply any default labels if specified in CLAUDE.md

**Capture ticket URL:**
- Present ticket URL to user
- Confirm successful creation

Output: Created ticket with URL.

## Issue Tracker Detection

**Check in this order:**
1. Look for explicit tracker specification in `CLAUDE.md` or `README.md`
2. Auto-detect from `git remote -v` URL
3. Use available integration method for the detected platform

**Note:** If no integration is available, output the ticket content and instructions for manual creation.

## Skill Boundaries

**This skill will:**
- Explore code extensively
- Ask lots of questions
- Synthesize understanding into tickets
- Challenge your assumptions
- Propose alternatives
- Create issues in your issue tracker

**This skill will NOT:**
- Write production code
- Make commits
- Run tests or linters
- Modify files (except ticket creation)
- Implement features

## Notes

**Exploration thoroughness:**
- Quick exploration: ~5 minutes, high-level understanding
- Medium exploration: ~15 minutes, detailed component analysis
- Very thorough: ~30 minutes, comprehensive system understanding

**Ticket quality over speed:**
- Take time to understand deeply
- Don't rush to ticket creation
- Better to ask more questions than create vague tickets

**Integration with /implement:**
- These skills are separate and complementary
- `/scope` creates the ticket, `/implement` implements it
- Ticket created by `/scope` can be handed to someone else or tackled later with `/implement`
