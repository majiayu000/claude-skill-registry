---
name: dev-swarm-market-research
description: Conduct comprehensive market research and competitive analysis to validate the problem and understand the market landscape. Use when user asks to conduct market research, validate market, analyze competitors, or start Stage 1 after init-ideas.
---

# AI Builder - Market Research

This skill conducts comprehensive market research and competitive analysis to validate the problem defined in init-ideas and understand the market landscape.

## When to Use This Skill

- User asks to conduct "market research"
- User wants to "validate the market" or "analyze competitors"
- User requests to start Stage 1 or the next stage after init-ideas
- User wants to understand market landscape before building

## Prerequisites

This skill requires the **00-init-ideas** stage to be completed first. The market research will build upon the problem statement, target users, and value proposition defined in that stage.

## Your Roles in This Skill

- **Product Manager**: Conduct market research and competitive analysis (5-7 competitors). Create initial product vision and goals. Define key features and prioritization (P0/P1/P2).
- **Data Analyst**: Analyze market size and trends. Research competitor metrics and performance. Identify data requirements for success tracking. Define key metrics to measure.
- **Marketing Manager**: Conduct market opportunity assessment. Identify target audience segments. Estimate customer acquisition costs. Define initial positioning and messaging.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

Follow these steps in order:

### Step 0: Verify Prerequisites and Gather Context

1. **Check if `00-init-ideas/` folder exists (mandatory):**
   - If NOT found: Inform user they need to init ideas first, then STOP
   - If found: Read all files to understand.

1.5 **Verify previous stage completion (00-init-ideas is mandatory):**
   - Read `00-init-ideas/README.md` and list required docs
   - If README is missing or required docs are missing, ask the user to
     continue the 00 stage first, then STOP

2. Read and apply rules: `dev-swarm/docs/research-specs-rules.md`

3. **Check if this stage should be skipped:**
   - Check if `01-market-research/SKIP.md` exists
   - **If SKIP.md exists:**
     - Read SKIP.md to understand why this stage was skipped
     - Inform the user: "Stage 1 (market-research) is marked as SKIP because [reason from SKIP.md]"
     - Ask the user: "Would you like to proceed to the next stage (personas)?"
     - **If user says yes:**
       - Exit this skill and inform them to run the next stage skill
     - **If user says no:**
       - Ask if they want to proceed with market research anyway
       - If yes, delete SKIP.md and continue with this skill
       - If no, exit the skill

3. **Check if `01-market-research/` folder exists with README.md:**
   - **If README.md exists (update mode):**
     - Read README.md to understand what was planned
     - Read all existing files in the folder
     - Inform the user: "Market research stage has existing documentation. I will update it based on the latest information from 00-init-ideas."
     - Ask the user: "Should I update the existing market research documentation? (yes/no)"
     - **If user says no:**
       - Ask what they want to do instead
       - Exit if needed
     - **If user says yes:**
       - Proceed to Step 1 in UPDATE MODE (refine existing docs)

   - **If folder doesn't exist or only has .gitkeep (create mode):**
     - Proceed to Step 1 in CREATE MODE (create new docs)

   - **If README.md exists:** Check whether it requires diagrams. If it does,
     follow `dev-swarm/docs/mermaid-diagram-guide.md` and use the
     `dev-swarm-mermaid` skill to render outputs.

4. Proceed to Step 1 with gathered context

### Step 1: Create/Update README.md Based on init-ideas

**CRITICAL: Create/update README.md first without pre-approval. Then ask the user to review/update/approve it, re-read it after approval, and only then create other docs.**

1. **Analyze information from 00-init-ideas/:**
   - **First, check what files exist** in 00-init-ideas/ (use Glob or Read to list files)
   - **Read ALL existing files** to gather context:
     - Problem statement (understand the problem to research)
     - Target users (understand who has this problem)
     - Value proposition (understand the solution domain)
     - Owner requirements (understand specific requirements)
     - Cost budget (understand budget constraints for this stage)
     - Any other documentation files that exist
   - **Don't assume file names** - read whatever exists in the folder

2. **Create or update 01-market-research/README.md:**
   - Use the template in `references/README.md`
   - Follow the checkbox rules: checked items apply after README approval; create file items only after approval; propose default checks; allow user changes
   - Populate only the template sections; do not add new headings such as Documents or Deliverables
   - Follow `dev-swarm/docs/stage-readme-guidelines.md` before drafting
   - Refer to `references/deliverables.md` to select deliverables by project type
   - Present any choices as checkbox lists with a default selection
   - List deliverables explicitly in README (typical: market-overview.md, competitor-analysis.md, gap-analysis.md, pricing-research.md, validation-findings.md)
   - **Stage overview and objectives** (based on init-ideas context)
   - **Owners:** Product Manager, Data Analyst, Marketing Manager
   - **Diagrams (if required by project init):**
     - Reference `dev-swarm/docs/mermaid-diagram-guide.md`
     - Include `diagram/` deliverables when needed
   - **Research goal:**
     - What problem domain will be researched (NOT technology)
     - Why this research matters for the project
     - What specific aspects will be investigated
     - What documents will be created as research output
   - **Research scope and constraints:**
     - Time/depth trade-offs if applicable
     - What will NOT be researched (technology, frameworks, etc.)
   - **Status:** In Progress (update to "Completed" after research is done)

3. **Notify user after README is created:**
   - Say: "I have created README.md file, please check and update or approve the content."
   - Summarize the research goal and what will be researched
   - Summarize what documentation files will be created
   - Explain how it aligns with init-ideas

4. **Wait for user approval:**
   - **If user says yes:** Re-read README.md (user may have updated it), then proceed to Step 2
   - **If user says no:**
     - Ask what needs to be changed
     - Update README based on feedback
     - Ask for approval again, then re-read README.md before proceeding

### Step 2: Identify Research Focus - Core Project Value

**CRITICAL: Focus on WHAT the project does, NOT the technology used to build it.**

Before conducting any research, identify the **core value/purpose** of the project:

1. **Read and analyze the init-ideas documentation:**
   - What problem is being solved?
   - What value proposition is being delivered?
   - What does the end product do for users?

2. **Determine the research focus:**
   - **CORRECT Example:** If building a "Flutter mobile app for food delivery"
     - Research: food delivery market, competitors in food delivery, user needs for ordering food
     - **DO NOT** research: Flutter framework, mobile app development trends

   - **CORRECT Example:** If building a "Python CLI tool for database migrations"
     - Research: database migration solutions, existing migration tools, developer pain points with migrations
     - **DO NOT** research: Python language, CLI frameworks

   - **CORRECT Example:** If building a "React web app for project management"
     - Research: project management software market, PM tool competitors, team collaboration needs
     - **DO NOT** research: React ecosystem, web development trends

3. **The research must be narrow and focused:**
   - Research the **unique idea** the user wants to build
   - Research the **problem domain** and **solution space**
   - Research **competitors solving the same problem**
   - **NOT** the technology stack or frameworks

4. **Present the research focus to user for confirmation:**
   - Clearly state what problem domain will be researched
   - List the key research questions based on init-ideas
   - Explain what will NOT be researched (technology, frameworks, etc.)
   - Ask: "Does this research focus match your expectations? Should I proceed?"

5. **Wait for user approval before starting web searches (after re-reading README.md)**

### Step 3: Conduct/Update Market Research Using Web Search

**Only after user confirms the research focus:**

**If files already exist (UPDATE MODE):**
- Update them based on latest context from 00-init-ideas and user feedback
- Improve and refine existing content, add new research findings
- Ensure data is current and relevant to the core project value
- Ensure research focuses on the problem/solution domain, not technology

**If files don't exist (CREATE MODE):**
- Create new files with comprehensive research
- **Only create files as specified in the approved README**
- Focus all research on the core project value identified in Step 2

Use web search capabilities to gather information for each document:

**After completing all research:**
- Update README.md to change **Status** from "In Progress" to "Completed"
- Add a **Research Summary** section with key findings (2-3 paragraphs)
- Add a **Generated Files** section listing all created files with brief descriptions
- The README serves as the summary - detailed results are in the generated files

Use `references/deliverables.md` for file-by-file content guidance and example structures.

### Step 4: Research Execution Tips

When conducting research:

1. **ALWAYS start by identifying the core project value:**
   - What problem is being solved?
   - What is the unique idea?
   - What domain/industry does this belong to?

2. **Research the PROBLEM DOMAIN, not the technology:**
   - Focus searches on the problem being solved
   - Search for competitors in the same problem space
   - Avoid researching the tech stack, frameworks, or platforms

3. **Use Web Search Tool** extensively for:
   - Market size data and reports **in the problem domain**
   - Competitor information and reviews **solving the same problem**
   - Industry trends and analysis **in the solution space**
   - User feedback on forums and review sites **about the problem**
   - Pricing information **for similar solutions**

4. **Document Sources**: Include URLs and references for all data

5. **Be Specific**: Use concrete numbers, dates, and examples

6. **Stay Objective**: Present both positive and negative findings

7. **Focus on Recent Data**: Prioritize information from the last 1-2 years

8. **Cross-Reference**: Validate findings across multiple sources

9. **Validate Research Relevance:**
   - After gathering data, ask: "Does this research help understand the problem/solution domain?"
   - If researching technology instead of the problem, STOP and refocus

### Step 5: User Review of Completed Research

1. Inform the user that research is complete and README.md has been updated with summary
2. Ask the user to review the market research documentation in `01-market-research/`
3. Ask if they want to proceed to the next stage (personas and user stories)
4. Make any adjustments based on user feedback

### Step 6: Commit to Git (if user confirms)

1. **If user confirms the research is complete:**
   - Ask if they want to commit to git
2. **If user wants to commit:**
   - Stage all changes in `01-market-research/`
   - Use the dev-swarm-draft-commit-message skill to draft the commit message
   - Commit with the drafted message (should follow conventional commit format)
   - Example: "feat(market-research): complete market research and competitive analysis for [problem domain]"
