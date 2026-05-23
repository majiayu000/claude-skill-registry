---
name: context-master
description: "Universal context management and planning system. PROACTIVELY activate for: (1) ANY complex task requiring planning, (2) Multi-file projects/websites/apps, (3) Architecture decisions, (4) Research tasks, (5) Refactoring, (6) Long coding sessions, (7) Tasks with 3+ sequential steps. Provides: optimal file creation order, context-efficient workflows, extended thinking delegation (23x context efficiency), passive deep analysis architecture, progressive task decomposition, and prevents redundant work. Saves 62% context on average. Essential for maintaining session performance and analytical depth."
---

# Context Master

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems

### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation



---

Universal context management and planning system for complex tasks, long coding sessions, and efficient workflow optimization.

---

## ⚡ TL;DR QUICK START (Read This First)

**For ANY multi-file project, follow these 5 steps:**

```
1️⃣ STOP - Don't create files yet
2️⃣ PLAN - Use "think hard" OR create planning document
3️⃣ ANNOUNCE - Tell user your file creation order
4️⃣ CREATE - Make files in optimal order (dependencies first)
5️⃣ VERIFY - Check all references work
```

**Example:**
```
User: "Create a portfolio with home, about, projects pages"

✓ Step 1: STOP [Don't immediately create index.html]
✓ Step 2: PLAN [Think: Need styles.css + 3 HTML files, CSS first]
✓ Step 3: ANNOUNCE ["I'll create: 1. styles.css, 2. index.html, 3. about.html, 4. projects.html"]
✓ Step 4: CREATE [Make them in that order]
✓ Step 5: VERIFY [Check all HTML files link to styles.css correctly]

Result: Done efficiently, no refactoring needed!
```

**Token savings: ~5,000 tokens (62%) vs doing it wrong**

**Continue reading below for detailed guidance...**

---

## Overview

This skill provides comprehensive context management, planning strategies, and workflow optimization for ANY complex coding task, not just multi-file projects.

**MUST use this skill for:**
- ✅ ANY complex task requiring planning or strategy
- ✅ Multi-file projects (HTML, CSS, JS, APIs, apps, docs)
- ✅ Architecture or design decisions
- ✅ Research tasks requiring analysis
- ✅ Refactoring work
- ✅ Long coding sessions (context optimization)
- ✅ Tasks with 3+ sequential steps

**What this skill provides:**
- **Optimal file creation order** - Which files to create first, dependency management
- **Context-efficient workflows** - 62% average context savings
- **Extended thinking delegation** - 23x context efficiency for deep analysis
- **Passive deep thinking architecture** - Get analytical depth without context cost
- **Progressive task decomposition** - Break complex tasks into manageable phases
- **Planning frameworks** - Think before coding, prevent redundant work
- **Session optimization** - Maintain performance in long interactions

**This skill activates automatically for:**
- Complex tasks requiring planning ("build...", "create...", "implement...")
- Architecture decisions ("should we use...", "which approach...")
- Research requests ("research...", "analyze...", "compare...")
- Refactoring work ("refactor...", "improve...", "optimize...")
- Multi-step workflows (any task with 3+ steps)
- Long coding sessions (automatic context monitoring)

---

# ⚠️ MANDATORY FIRST STEP - READ THIS BEFORE DOING ANYTHING ⚠️

## 🛑 STOP - DO THIS FIRST 🛑

**IMMEDIATELY use extended thinking to plan. Do NOT create any files yet.**

**Your exact next output MUST be:**

```
"Think hard about the architecture for this [project type]:
- What files are needed and what is their purpose?
- What are the shared dependencies (CSS, config, base classes)?
- What is the optimal creation order and why?
- What are the cross-file references?
- What could go wrong if we create files in the wrong order?"
```

**After the extended thinking completes, THEN announce your plan to the user.**

**DO NOT create files until you:**
1. ✅ Complete extended thinking 
2. ✅ Announce the plan to the user
3. ✅ Get their acknowledgment (or proceed if plan is sound)

---

## 🎯 PLANNING METHOD OPTIONS

**You have TWO equally effective planning approaches:**

### Option A: Extended Thinking (Pure Mental Planning)
```
"Think hard about the architecture for this [project]:
- What files are needed?
- What is the optimal creation order?
- What dependencies exist?"
```

**Best for:** Quick projects, straightforward structures, when planning fits in thinking block

### Option B: Planning Document (Structured Written Plan)
```
Use bash_tool or create an artifact for the planning document:

ARCHITECTURE_PLAN.md:
- Files needed: [list]
- Creation order: [numbered list]
- Dependencies: [diagram/list]
- Potential issues: [list]
```

**Best for:** Complex projects, when you want a reference document, when planning is extensive

**Both work equally well!** Choose based on project complexity and your preference.

**Example using bash_tool for planning:**
```bash
cat > ARCHITECTURE_PLAN.md << 'EOF'
# Portfolio Website Architecture

## Files Needed
1. styles.css - Shared styling
2. index.html - Home page
3. about.html - About page
4. projects.html - Projects page
5. contact.html - Contact page

## Creation Order
1. styles.css (shared dependency, created first)
2. index.html (references styles.css)
3. about.html (references styles.css)
4. projects.html (references styles.css)
5. contact.html (references styles.css)

## Cross-References
- All HTML files link to styles.css via <link rel="stylesheet">
- All pages navigate to each other via <a href="...">
EOF
```

**Benefit of planning document:** You can reference it throughout the project, and it serves as documentation.

---## 💰 WHY THIS MATTERS: Token Savings

**Without planning:**
- Create files → Realize structure is wrong → Refactor → More explanations
- **Cost: ~8,000 tokens** (redundant work + explanations + fixes)

**With planning (this skill):**
- Think first → Create files in optimal order → Done correctly first time
- **Cost: ~3,000 tokens** (efficient creation only)

**💡 Savings: ~5,000 tokens (62% reduction) per multi-file project**

Over a long session with multiple projects, this compounds significantly.

### Real-World Token Savings by Project Size

**Small Project (3-4 files) - Portfolio Website**
```
Without planning: ~6,000 tokens
  - Create HTML → Add inline styles → Extract CSS → Update refs
With planning: ~2,500 tokens
  - Plan → Create CSS → Create HTML with refs
💰 Savings: ~3,500 tokens (58%)
```

**Medium Project (7-8 files) - Multi-page App**
```
Without planning: ~12,000 tokens
  - Create pages → Realize shared components → Refactor → Fix imports
With planning: ~4,500 tokens
  - Plan → Create shared → Create pages → No refactoring
💰 Savings: ~7,500 tokens (63%)
```

**Large Project (20+ files) - Full Application**
```
Without planning: ~35,000 tokens
  - Create files randomly → Multiple refactoring cycles → Fix dependencies
With planning: ~12,000 tokens
  - Plan architecture → Create in optimal order → Minimal fixes
💰 Savings: ~23,000 tokens (66%)
```

**Context window capacity:**
- Standard: 200K tokens
- With planning: Can complete 16-17 medium projects
- Without planning: Can complete only 7-8 medium projects
- **Effective capacity increase: 2.1x**

---## 🚨 ACTIVATION TRIGGERS (You are seeing one of these RIGHT NOW)

If the user's request includes ANY of these phrases, this skill activated for a reason:

- ✅ "create a website with..." ← **YOU ARE HERE**
- ✅ "build 3+ pages/files"
- ✅ "make a [type] application"
- ✅ "create [home/about/contact] pages"
- ✅ "build an API with..."
- ✅ "generate documentation for..."

**→ Your NEXT output should be extended thinking about architecture, NOT file creation**

---

## 📊 POST-PROJECT REFLECTION (Optional But Valuable)

**After completing a multi-file project, take a moment to assess the context savings:**

### Quick Self-Assessment Questions

```
1. Did you plan before creating files? [Yes/No]
   
2. How many files did you create? [Number]

3. Did you have to refactor or fix file references? [Yes/No]
   
4. If you planned first:
   - Estimated context used: ~[2,500-4,500] tokens for [3-8] files
   
5. If you created without planning:
   - You likely used: ~[6,000-12,000] tokens
   - Potential savings missed: ~[3,500-7,500] tokens
```

### Success Indicators

**✅ You used the skill effectively if:**
- Created foundation files (CSS, config) before dependent files
- No major refactoring needed after file creation
- All file references worked on first try
- Could describe file creation order before starting
- Spent more time planning than fixing

**⚠️ You could improve if:**
- Had to go back and add shared dependencies
- Needed to refactor file structure after creation
- Found broken references between files
- Created files in no particular order
- Spent more time fixing than planning

### Context Savings Calculator

**Estimate your actual savings:**
```
Files created: [N]
Did planning: [Yes/No]

If Yes:
  Tokens used: ~(N × 350) + 500 for planning
  Tokens saved: ~(N × 800)
  Efficiency: ~70%

If No:
  Tokens used: ~(N × 1,150) 
  Missed savings: ~(N × 800)
  Next time: Plan first!
```

**Example for 5-file project:**
- With planning: ~2,250 tokens
- Without planning: ~5,750 tokens  
- Actual savings: ~3,500 tokens (60%)

This reflection helps you recognize when the skill is working and when to apply it more strictly next time!

---

## ✓ REQUIRED WORKFLOW CHECKLIST

**For EVERY multi-file project, follow this exact sequence:**

```
☐ Step 1: THINK FIRST - Use "think hard" to plan architecture
         (List all files, determine optimal order, identify dependencies)
         
☐ Step 2: ANNOUNCE THE PLAN - Tell user the file creation order
         ("I'll create files in this order: 1. CSS, 2. index.html, 3...")
         
☐ Step 3: CREATE FOUNDATION FILES - Shared dependencies first
         (CSS files, config files, base classes)
         
☐ Step 4: CREATE DEPENDENT FILES - Files that use the foundations
         (HTML pages that reference CSS, components that use base classes)
         
☐ Step 5: VERIFY - Check all references/imports work
```

**DO NOT skip Step 1. ALWAYS think before creating files.**

---

## 🔴 COMMON MISTAKE TO AVOID

**WRONG APPROACH (what you might do without this skill):**
```
User: "Create a portfolio with home, about, and projects pages"
You: [Creates index.html]
You: [Creates about.html]
You: [Creates projects.html]
You: [Realizes CSS should be shared, has to refactor]
Result: Wasted effort, redundant work
```

**CORRECT APPROACH (what you MUST do with this skill):**
```
User: "Create a portfolio with home, about, and projects pages"
You: "Think hard about the architecture first..."
     [Plans: Need 1 CSS file + 3 HTML files, CSS should come first]
You: "I'll create files in this order: 1. styles.css, 2. index.html, 3. about.html, 4. projects.html"
You: [Creates files in that order]
Result: Efficient, no redundant work
```

---

## ❌ MORE ANTI-PATTERNS (What NOT to Do)

### Anti-Pattern 1: Creating JS Modules Before Main App File
**Wrong:**
```
1. Create utils.js
2. Create helpers.js
3. Create api.js
4. Create app.js (main file that imports all the above)
Problem: Had to keep going back to app.js to add imports
```

**Right:**
```
1. Think about module structure
2. Create app.js (with import statements planned)
3. Create utils.js (knowing what app.js needs)
4. Create helpers.js (knowing what app.js needs)
5. Create api.js (knowing what app.js needs)
Benefit: App.js structured correctly from the start
```

### Anti-Pattern 2: Writing Inline Styles Then Extracting Later
**Wrong:**
```
1. Create index.html with inline styles
2. Create about.html with inline styles
3. Realize styles are duplicated
4. Extract to styles.css
5. Update all HTML files to reference it
Problem: Redundant work, had to edit multiple files
```

**Right:**
```
1. Think: These pages will share styling
2. Create styles.css first
3. Create HTML files that reference styles.css
Benefit: No duplication, no refactoring needed
```

### Anti-Pattern 3: Building Components Before Data Structure
**Wrong:**
```
1. Create UserProfile.jsx component
2. Create UserList.jsx component
3. Realize data structure is unclear
4. Go back and modify components to match data
Problem: Components built on assumptions
```

**Right:**
```
1. Think about data structure first
2. Create types.js or schema.js
3. Create components that use defined data structure
Benefit: Components built correctly from the start
```

### Anti-Pattern 4: Creating Pages Before Shared Layout
**Wrong:**
```
1. Create home.html with full layout
2. Create about.html with full layout
3. Realize layout should be shared
4. Extract to layout component/template
5. Refactor all pages
Problem: Major refactoring required
```

**Right:**
```
1. Think: Pages will share layout
2. Create layout.html or Layout component
3. Create pages that use the layout
Benefit: DRY from the start
```

### Anti-Pattern 5: Creating Config Files Last
**Wrong:**
```
1. Create multiple files with hardcoded values
2. Realize config should be centralized
3. Create config.js
4. Update all files to use config
Problem: Config scattered, hard to change
```

**Right:**
```
1. Think: What values will be used across files?
2. Create config.js first
3. Create other files that import config
Benefit: Centralized configuration from start
```

---

# 📖 PART 1: UNIVERSAL GUIDANCE (All Users - Web, API, CLI)

**The sections below apply to ALL users. Read these first regardless of your environment.**

---

## Core Principles (All Environments)

### 1. Extended Thinking for Complex Tasks

Use extended thinking to keep reasoning separate from main context:

**Trigger phrases:**
- `"think about..."` - Standard extended thinking
- `"think hard about..."` - More thorough analysis  
- `"think harder about..."` - Deep analysis
- `"ultrathink..."` - Maximum thinking budget

**When to use:**
- Planning complex implementations
- Analyzing multiple approaches
- Design decisions with tradeoffs
- Any task requiring deep reasoning

**Benefit:** Reasoning happens in separate blocks that don't clutter your main context.

### 2. Artifacts for Content Offloading

Create artifacts for substantial content instead of inline responses:

**Use artifacts for:**
- Code files (>20 lines)
- Documents, reports, articles
- Data analysis results
- Complex visualizations
- Any reusable content

**Why it works:** Content lives in artifacts, not the conversation context.

### 3. Progressive Task Decomposition

Break complex requests into phases:

**Instead of:**
"Build me a complete app with authentication, database, and frontend"

**Do this:**
```
Phase 1: "think about the architecture for this app"
[Review architecture plan]

Phase 2: "Create the database schema"
[Review schema]

Phase 3: "Build the authentication system"
[Continue phase by phase]
```

**Benefit:** Each phase has fresh context, no accumulation of old decisions.

### 4. Explicit Context Boundaries

Signal when to start fresh:

- "Let's start fresh with a new approach"
- "Setting aside the previous discussion..."
- "Here's a new angle on this problem..."

**In Claude Code:** Use `/clear` command
**In web/API:** Explicitly state context reset

## Multi-File Project Planning (Critical Section)

**📌 QUICK REMINDER: Did you think first? If not, go back to "STOP - DO THIS FIRST" above.**

**When creating any project with 3+ related files, ALWAYS start with this planning workflow:**

### Step 1: Architecture Planning

**Choose your planning method (both equally effective):**

**Method A: Extended Thinking**
```
"Think hard about the architecture for this [project]:
- What files are needed and their purpose?
- What are shared dependencies?
- What is optimal creation order?
- What are cross-file references?
- What could go wrong?"
```

**Method B: Planning Document**
```
Create ARCHITECTURE_PLAN.md (via bash_tool or artifact):
- Files needed with purposes
- Shared dependencies
- Numbered creation order with reasoning
- Cross-file reference map
- Potential issues to avoid
```

**Before creating any files, use extended thinking OR create planning document with this template:**

```
ARCHITECTURE PLAN TEMPLATE:

□ FILES NEEDED:
  - [filename]: [purpose]
  - [filename]: [purpose]
  - [filename]: [purpose]

□ SHARED DEPENDENCIES (must be created first):
  - [dependency]: [what files need this]

□ CREATION ORDER (numbered with reasoning):
  1. [file] - Reason: [why this first]
  2. [file] - Reason: [why this second]
  3. [file] - Reason: [why this third]

□ CROSS-FILE REFERENCES:
  - [file A] references [file B] via [method]
  - [file C] imports [file D] via [method]

□ POTENTIAL ISSUES TO AVOID:
  - [what could go wrong]
  - [common mistake]
```

**Example filled template for portfolio website:**

```
ARCHITECTURE PLAN:

□ FILES NEEDED:
  - styles.css: Shared styling for all pages
  - index.html: Home page with navigation
  - about.html: About page
  - projects.html: Portfolio showcase
  - contact.html: Contact form

□ SHARED DEPENDENCIES:
  - styles.css: All HTML files need this for consistent styling

□ CREATION ORDER:
  1. styles.css - Reason: Shared dependency, all HTML files will reference it
  2. index.html - Reason: Main entry point, establishes structure
  3. about.html - Reason: References styles.css which now exists
  4. projects.html - Reason: References styles.css which now exists
  5. contact.html - Reason: References styles.css which now exists

□ CROSS-FILE REFERENCES:
  - All HTML files link to styles.css via <link rel="stylesheet">
  - All HTML pages link to each other via <a href="...">

□ POTENTIAL ISSUES TO AVOID:
  - Creating HTML before CSS → Would require going back to add links
  - Inline styles in HTML → Would require extraction later
  - Inconsistent navigation → Hard to maintain across files
```

**Use this template in your extended thinking output.**

### Step 2: Optimal File Creation Order

**General principles:**

1. **Foundations first** - Shared dependencies before dependents
   - CSS files before HTML files that use them
   - Configuration files before code that needs them
   - Base classes before derived classes

2. **Core before features** - Essential files before optional ones
   - index.html before other pages
   - main.js before feature modules
   - Core API before additional endpoints

3. **Structure before content** - Layout before details
   - HTML structure before detailed content
   - API structure before implementation details
   - Component scaffolds before full logic

**Common file creation orders:**

**Website project:**
```
1. styles.css (shared styling)
2. index.html (home page - references styles.css)
3. about.html (references styles.css)
4. projects.html (references styles.css)
5. contact.html (references styles.css)
6. script.js (if needed)
```

**React application:**
```
1. package.json (dependencies)
2. App.js (main component)
3. components/Header.js (layout components)
4. components/Footer.js
5. pages/Home.js (page components)
6. pages/About.js
7. styles/main.css
```

**Backend API:**
```
1. config.js (configuration)
2. database.js (DB connection)
3. models/User.js (data models)
4. routes/auth.js (route handlers)
5. routes/api.js
6. server.js (entry point)
```

### Step 3: Create Files with Awareness

**As you create each file:**
- Reference what's already been created
- Note what future files will depend on this one
- Keep consistent naming and structure
- Add comments about dependencies

### Step 4: Verify and Test

**After creating all files, perform these verification checks:**

#### ✓ File Path Verification
```
□ Check all file paths are correct
  - CSS links: <link href="styles.css"> (not "style.css" or "css/styles.css")
  - JS scripts: <script src="script.js"> 
  - Images: <img src="image.png">
  - Relative paths match actual file structure
```

#### ✓ Reference Loading Verification
```
□ Ensure CSS/JS references load properly
  - HTML files can find the CSS file
  - JavaScript imports resolve correctly
  - No 404 errors for missing files
  - Correct syntax in link/script tags
```

#### ✓ Navigation Verification (for websites)
```
□ Test navigation between pages
  - All navigation links point to correct files
  - Links use correct relative paths
  - No broken navigation (links to non-existent pages)
  - Back/forward navigation works logically
```

#### ✓ Cross-File Reference Verification
```
□ Validate cross-file dependencies work
  - Components import correctly
  - Modules can access exported functions
  - Shared utilities are accessible
  - API calls reference correct endpoints
```

#### ✓ Consistency Verification
```
□ Check consistency across files
  - Naming conventions are consistent
  - Styling is uniform (if using shared CSS)
  - Code structure follows same patterns
  - Documentation style matches across files
```

**Example verification for portfolio website:**
```
After creating styles.css, index.html, about.html, projects.html, contact.html:

✓ Verification checklist:
  [✓] All HTML files have <link rel="stylesheet" href="styles.css">
  [✓] styles.css exists and has content
  [✓] Navigation links: 
      - index.html links to about.html, projects.html, contact.html ✓
      - All other pages link back to index.html ✓
  [✓] All pages use consistent styling from styles.css ✓
  [✓] No broken links or missing file references ✓

Result: Project structure verified, ready to use!
```

**If verification fails, fix issues before considering the project complete.**

### When to Use This Planning Approach

**ALWAYS plan first for:**
- Websites with multiple pages (3+ HTML files)
- Applications with multiple components
- Projects with shared dependencies (CSS, config files)
- API implementations with multiple endpoints
- Documentation sets with multiple files
- Any project where files reference each other

**Don't need planning for:**
- Single file creations
- Truly independent files with no relationships
- Simple, obvious structures

## Passive Deep Thinking Architecture

**The key insight:** Extended thinking can happen in isolated contexts (subagents/artifacts), keeping the main session lean while still getting deep analysis.

### The Architectural Pattern

```
Main Session (Orchestrator)
├─ Stays high-level and focused
├─ Makes decisions based on summaries
└─ Delegates complex analysis

        ↓ delegates with thinking triggers ↓

Analysis Layer (Agents/Artifacts)
├─ Extended thinking happens HERE (5K+ tokens)
├─ Deep reasoning happens HERE
├─ Context-heavy work happens HERE
└─ Returns concise summaries UP (~200 tokens)

        ↑ returns actionable conclusions ↑

Main Session
└─ Receives well-reasoned recommendations
└─ Context stays clean for sustained work
```

### How This Achieves Passive Deep Thinking

**Without thinking delegation:**
- Extended thinking happens in main context
- Reasoning accumulates (~5K tokens per analysis)
- Context fills quickly over long sessions
- Eventually hits limits

**With thinking delegation:**
- Subagents/artifacts do extended thinking in isolation
- Main context only receives summaries (~200 tokens)
- Can sustain 25+ analyses before context issues
- Deep thinking happens passively through architecture

**Key benefit:** You get the depth of extended thinking without the context cost.

### Implementation by Environment

#### **Claude Code: Thinking Subagents**

Create subagents that automatically use extended thinking:

```bash
# Create a deep analyzer for complex decisions
python scripts/create_subagent.py architecture-advisor --type deep_analyzer

# Create thinking-enabled researcher
python scripts/create_subagent.py pattern-researcher --type researcher
```

**Usage:**
```
Main session: "I need to decide between microservices and monolith"
↓
/agent architecture-advisor "Analyze microservices vs monolith 
for an e-commerce platform with 10M users, considering team size 
of 8 developers"
↓
Subagent's isolated context:
  - Uses "ultrathink" automatically
  - 5K+ tokens of deep reasoning
  - Evaluates tradeoffs thoroughly
↓
Returns to main: "After deep analysis, I recommend starting with 
a modular monolith because [3 key reasons]. Microservices would 
add complexity your team size can't support yet."
↓
Main session: Receives actionable advice, context clean
```

**Context saved:** ~4,800 tokens per analysis

#### **Web/API: Thinking Artifacts**

Use artifacts as "thinking containers":

**Pattern:**
```
User: "Analyze the best database for this use case"

Claude: "I'll create a deep analysis artifact where I can think 
through this thoroughly."

[Creates artifact: "database-analysis.md"]
[Inside artifact:
  - Extended thinking block (collapsed in UI)
  - Detailed analysis
  - Comparison tables
  - Final recommendation
]

Main conversation: "Based on the analysis artifact, I recommend 
PostgreSQL because [2-sentence summary]. See artifact for complete 
reasoning including performance comparisons and scaling considerations."
```

**Why this works:**
- Thinking is visually separated (in artifact)
- Main conversation stays summary-focused
- User can reference artifact when needed
- Conversational context stays lean

### When to Use Thinking Delegation

**Delegate to thinking agents/artifacts for:**
- Architecture decisions
- Technology evaluations
- Complex tradeoff analysis
- Multi-factor comparisons
- Design pattern selection
- Performance optimization strategies
- Security assessment
- Refactoring approach planning

**Keep in main context for:**
- Simple implementation
- Quick queries
- Tactical decisions with obvious answers
- Tasks requiring full project context

### Example: Complex Decision with Thinking Delegation

**Scenario:** Choose state management for React app

**Traditional approach (main context):**
```
User: "What state management should I use?"
Claude: [5K tokens of thinking in main context]
Claude: [Another 2K tokens explaining recommendation]
Total: ~7K tokens consumed
```

**Thinking delegation approach:**
```
User: "What state management should I use for a large e-commerce app?"

Claude Code:
"This warrants deep analysis. Let me delegate to a deep analyzer."
/agent architecture-advisor "Think deeply about state management 
options (Redux, Zustand, Jotai, Context) for large-scale e-commerce 
with real-time inventory"

[Subagent uses ultrathink in isolated context - 5K tokens]
[Returns summary - 200 tokens]

Main context: "The advisor recommends Zustand for these reasons..."
Total in main: ~300 tokens
```

**Context efficiency:** 23x improvement while maintaining analytical depth

### Compound Effect Over Long Sessions

**Session without thinking delegation:**
- Analysis 1: 7K tokens
- Analysis 2: 7K tokens  
- Analysis 3: 7K tokens
- Analysis 4: 7K tokens
- Analysis 5: 7K tokens
- **Total: 35K tokens** (17% of 200K context)

**Session with thinking delegation:**
- Analysis 1: 300 tokens
- Analysis 2: 300 tokens
- Analysis 3: 300 tokens
- Analysis 4: 300 tokens
- Analysis 5: 300 tokens
- **Total: 1.5K tokens** (0.75% of 200K context)

**Result:** Can sustain 23x more analyses in same context window while maintaining analytical rigor.

## Universal Strategies

### Strategy 1: Research → Think → Implement

**Works in all environments:**

```
Step 1: Research phase
"Search for [topic] and gather key information"

Step 2: Analysis phase  
"think hard about the best approach based on those findings"

Step 3: Implementation phase
"Now implement [specific task] using the approach we decided"
```

**Why it works:** Each phase has clear purpose, prevents context sprawl.

### Strategy 2: Artifact-Driven Development

**For coding tasks:**

```
1. "Create a [file type] artifact with [functionality]"
2. Test/review the artifact
3. "Update the artifact to add [feature]"
4. Iterate within the artifact
```

**Why it works:** Code lives in artifact, conversation stays focused on decisions.

### Strategy 3: Document Plans Before Executing

**For complex projects:**

```
1. "think about the plan for this project"
2. "Create a markdown artifact with the plan"
3. Reference the plan artifact as you work
4. Update the plan artifact as decisions change
```

**Why it works:** Plan persists in artifact, you can reference it without re-explaining.

### Strategy 4: Chunked Research

**For large research tasks:**

```
1. "Research aspect A of [topic]"
2. "Create a summary artifact"
3. [New conversation or context reset]
4. "Research aspect B of [topic]" 
5. "Create a summary artifact"
6. "Synthesize findings from both research phases"
```

**Why it works:** Each research phase stays focused, final synthesis combines cleanly.

## Environment-Specific Techniques

### Web Interface & API

**Strategies:**
- Use extended thinking liberally for complex reasoning
- Create artifacts for code, documents, and substantial content
- Break long tasks into explicit phases
- Signal context resets when changing direction

**Example workflow:**
```
"I need to build a REST API. Let me break this into phases:

Phase 1: ultrathink about the API design and architecture
[Review thinking output]

Phase 2: Create an artifact with the OpenAPI specification
[Review spec]

Phase 3: Implement the authentication endpoints
[Continue implementation]
```

### Claude Code (CLI)

**Additional commands:**
- `/clear` - Reset context between tasks
- `/compact` - Compress context while keeping key decisions
- `/continue` - Resume previous session
- Subagents - Delegate research/testing to isolated contexts

**Generate project-specific CLAUDE.md:**
```bash
python scripts/generate_claude_md.py --type [TYPE] --output ./CLAUDE.md
```

**Create subagents for recurring tasks:**
```bash
python scripts/create_subagent.py [NAME] --type [TYPE]
```

See **Claude Code Tooling** section below for details.

## Common Workflows (All Environments)

### Workflow 0: Multi-File Website/Project Creation ⭐ MOST COMMON

**🚨 If user said: "create a website/app with multiple pages" → YOU ARE IN THIS WORKFLOW RIGHT NOW**

**MANDATORY WORKFLOW - FOLLOW THIS EXACT SEQUENCE:**

```
✓ STEP 1: STOP AND THINK (DO THIS FIRST, ALWAYS)
   Output: "Think hard about the architecture for this [project]..."
   [Extended thinking plans: files needed, creation order, dependencies]

✓ STEP 2: ANNOUNCE THE PLAN
   Output: "I'll create these files in this order:
            1. styles.css (shared styling)
            2. index.html (home page)
            3. about.html
            4. projects.html
            5. contact.html"

✓ STEP 3: CREATE FOUNDATION FILES FIRST
   Create: styles.css
   
✓ STEP 4: CREATE DEPENDENT FILES
   Create: index.html (references styles.css)
   Create: about.html (references styles.css)
   Create: projects.html (references styles.css)
   Create: contact.html (references styles.css)

✓ STEP 5: VERIFY
   Check: All HTML files reference styles.css correctly
```

**Example: Portfolio Website Request**

```
User: "Create a portfolio website with home, about, projects, and contact pages"

🛑 BEFORE YOU CREATE ANY FILES, YOU MUST OUTPUT:

"Let me think hard about the architecture first..."

[Extended thinking output should plan:
 - Files needed: index.html, about.html, projects.html, contact.html, styles.css
 - Optimal order: styles.css FIRST (it's a shared dependency), then HTML pages
 - Dependencies: All HTML files will reference styles.css
 - Structure: Simple multi-page site with shared stylesheet]

THEN announce the plan:

"I'll create the files in this order:

1. styles.css - Shared styling for all pages
2. index.html - Home page (will reference styles.css)
3. about.html - About page (will reference styles.css)
4. projects.html - Projects page (will reference styles.css)
5. contact.html - Contact page (will reference styles.css)

This order ensures all dependencies are in place before files that need them."

THEN create files in that exact order.
```

**❌ WRONG - What NOT to do:**
```
User: "Create a portfolio website with home, about, projects, and contact pages"

[Immediately creates index.html without thinking]
[Creates about.html]
[Creates projects.html]
[Realizes CSS should be shared, has to go back and add it]

This wastes effort and context!
```

**✅ RIGHT - What to do:**
```
User: "Create a portfolio website with home, about, projects, and contact pages"

"Think hard about architecture..." [Plans first]
"I'll create in this order: CSS first, then HTML pages" [Announces plan]
[Creates styles.css]
[Creates HTML pages that reference styles.css]

Efficient! No redundant work!
```

---

### Workflow 1: Complex Decision Making

**With Thinking Delegation:**

**Claude Code:**
```
User: "Should we use microservices or monolith?"

1. /agent deep-analyzer "Ultrathink about architecture choice 
   for 10M user e-commerce platform, 8 dev team"
2. [Receives well-reasoned recommendation in main context]
3. Make decision based on analysis
4. Proceed with implementation
```

**Web/API:**
```
User: "Should we use microservices or monolith?"

1. "Create a deep-analysis.md artifact and ultrathink about this"
2. [Artifact contains extended thinking + conclusion]
3. Main conversation: "Based on analysis, recommend monolith because..."
4. Proceed with implementation
```

**Context efficiency:** Deep thinking happens, main context stays clean.

---

### Workflow 2: Complex Feature Development

```
Phase 1: Architecture Analysis
Claude Code: /agent deep-analyzer "Think deeply about architecture for [feature]"
Web/API: "Create architecture-analysis artifact with deep thinking"
[Isolated thinking → summary to main]

Phase 2: Design Planning
"Based on that analysis, create implementation plan artifact"
[Main context references analysis conclusions]

Phase 3: Implementation
"Implement component A based on the plan"
[Create code artifact]

Phase 4: Testing
Claude Code: /agent test-runner "Run tests and analyze failures"
Web/API: "Run tests" [test output in separate space]

Phase 5: Integration
"Integrate based on architecture plan"
```

**Why it works:** Each phase has clear purpose, thinking isolated where needed.

---

### Workflow 3: Research & Technology Evaluation

```
Phase 1: Deep Research
Claude Code: /agent pattern-researcher "Research and think hard about 
  authentication approaches, analyze tradeoffs"
Web/API: "Create research-findings artifact and think through options"

Phase 2: Synthesis
[Receives summary of findings]
"Create comparison table artifact"

Phase 3: Recommendation
Claude Code: /agent deep-analyzer "Based on research, recommend approach"
Web/API: "Based on research artifact, ultrathink and recommend"

Phase 4: Implementation
"Implement recommended approach"
```

**Why it works:** Research and deep analysis isolated, implementation focused.

---

### Workflow 4: Code Generation & Iteration

```
1. "Create a [language] script that [functionality]"
   → Artifact created

2. "Add [feature] to the script"
   → Artifact updated

3. "Optimize the [specific part]"
   → Targeted update

4. "Add error handling"
   → Incremental improvement
```

**Why it works:** All code lives in the artifact, conversation stays focused on what to change.

---

### Workflow 5: Refactoring with Analysis

**Claude Code:**
```
1. /agent analyzer "Think hard about refactoring approach 
   for legacy auth system"
2. [Receives analysis in main: strategy, risks, order]
3. "Create REFACTOR.md plan based on analysis"
4. /clear
5. For each module:
   - Refactor according to plan
   - /agent test-runner "verify changes"
   - Commit
   - /clear before next
```

**Web/API:**
```
1. "Create refactoring-analysis artifact, think deeply about approach"
2. [Artifact has thinking + strategy]
3. "Create refactoring-plan artifact based on analysis"
4. Implement module by module
5. Reference plan artifact as you work
```

**Why it works:** Deep analysis happens once (isolated), execution follows clean plan.



## Best Practices (Universal)

### 1. Delegate Complex Analysis to Isolated Contexts

**The most powerful pattern for context efficiency:**

**Claude Code:**
```
✅ /agent deep-analyzer "Ultrathink about [complex decision]"
❌ "Think about [complex decision]" [happens in main context]
```

**Web/API:**
```
✅ "Create analysis artifact and ultrathink about [decision]"
❌ "Ultrathink about [decision]" [thinking stays in conversation]
```

**Benefit:** 5K+ tokens of reasoning happens in isolation, main context receives ~200 token summary. 23x context efficiency while maintaining analytical depth.

### 2. Use Extended Thinking for Planning
Before diving into implementation:
```
"think hard about the approach for [task]"
```

**Even better with delegation:**
- Claude Code: Delegate to deep_analyzer subagent
- Web/API: Use thinking artifact

**Benefit:** Reasoning stays out of main context, you get thoughtful plans.

### 3. Create Artifacts for Substantial Content
Don't inline long code or documents in conversation:
```
✅ "Create a Python script artifact that [functionality]"
❌ "Show me the Python code for [functionality]"
```

**Benefit:** Content lives in artifacts, not conversation history.

### 4. Break Complex Tasks Into Explicit Phases
State phase transitions clearly:
```
"Phase 1 complete. Moving to Phase 2: [description]"
```

**With thinking delegation:**
```
Phase 1: /agent deep-analyzer "analyze approaches"
Phase 2: Implement based on analysis
```

**Benefit:** Each phase has clear purpose and boundaries.

### 5. Document Decisions in Artifacts
Create persistent references:
```
"Create a decisions.md artifact tracking our key choices"
```

**Benefit:** Can reference decisions without re-explaining full context.

### 6. Progressive Disclosure
Don't request everything at once:
```
✅ "First, analyze the requirements"
    "Now, design the data model"
    "Now, implement the core logic"

❌ "Analyze requirements, design data model, and implement everything"
```

**Benefit:** Each step builds on the last without overwhelming context.

### 7. Use Thinking for Exploration
When uncertain about approach:
```
"ultrathink about multiple approaches and recommend the best one"
```

**Even better:** Delegate to deep_analyzer (Claude Code) or thinking artifact (Web/API)

**Benefit:** Deep analysis without context clutter.

### 8. Signal Context Resets
When changing direction:
```
"Setting aside the previous approach, let's try a different angle..."
```

**Benefit:** Clear boundaries prevent old context from interfering.

## Advanced Patterns (Universal)

### Pattern: Iterative Refinement
```
1. "Create initial version of [artifact]"
2. Review
3. "Improve [specific aspect]"
4. Review
5. "Add [feature]"
6. Continue iterating
```

**Benefit:** Focused improvements, not recreating everything each time.

### Pattern: Multi-Artifact Projects
```
1. "Create architecture.md artifact"
2. "Create database-schema.sql artifact"
3. "Create api-spec.yaml artifact"
4. "Now implement based on these artifacts"
```

**Benefit:** Each artifact is a stable reference, no context accumulation.

### Pattern: Thinking → Document → Execute
```
1. "ultrathink about [complex problem]"
2. "Document the decision in a plan artifact"
3. "Execute phase 1 of the plan"
4. Reference plan artifact as you continue
```

**Benefit:** Separation of reasoning, planning, and execution.

### Pattern: Chunked Content Generation
For long documents:
```
1. "Create outline artifact"
2. "Write introduction (add to artifact)"
3. "Write section 1 (add to artifact)"
4. Continue section by section
```

**Benefit:** Build progressively without loading entire document context each time.

---

# 🔧 PART 2: CLI-SPECIFIC FEATURES (Claude Code Users Only)

**The sections below are ONLY for users of Claude Code CLI. Web and API users can skip this part.**

---

## Claude Code Tooling (Bonus Features)

When using Claude Code CLI, additional optimization tools are available:

### Quick Start: Generate CLAUDE.md

Create a context-optimized CLAUDE.md file for your project:

```bash
python scripts/generate_claude_md.py --type [TYPE] --output ./CLAUDE.md
```

**Available types:**
- `general` - General-purpose projects
- `backend` - API/service projects  
- `frontend` - Web applications
- `fullstack` - Full-stack applications
- `data` - Data science/ML projects
- `library` - Library/package development

**What it does:** Generates a CLAUDE.md file that Claude Code reads automatically, providing persistent project guidance across sessions.

### Create Subagents

For recurring tasks, create dedicated subagents:

```bash
python scripts/create_subagent.py [NAME] --type [TYPE] --output [DIR]
```

**Available types:**
- `researcher` - Documentation searches with deep analysis
- `tester` - Test execution with failure analysis
- `analyzer` - Code analysis with architectural insights
- `builder` - Build and deployment tasks
- `deep_analyzer` - Complex decisions requiring extensive thinking (recommended for architecture, tech choices, design patterns)

**What it does:** Creates `.claude/agents/[NAME].md` configuration that can be invoked with:
```
/agent [NAME] [task description]
```

### Claude Code Commands

- `/clear` - Reset context between tasks
- `/compact` - Compress context while preserving key decisions
- `/continue` - Resume previous session
- `/agent [NAME]` - Delegate task to a subagent with isolated context

### Claude Code Patterns

**Pattern: Deep Analysis Delegation**
```
1. /clear (start fresh)
2. /agent deep-analyzer "Ultrathink about [complex decision]"
3. [Receives well-reasoned analysis in ~200 tokens]
4. Make decision and implement
5. Main context stayed clean throughout
```

**Pattern: Research with Thinking**
```
1. /agent pattern-researcher "Research [topic] and think hard about implications"
2. [Subagent searches + thinks in isolation]
3. Review findings in main context
4. Proceed with informed decision
```

**Pattern: Test-Driven Development with Analysis**
```
1. Write test in main context
2. /agent test-runner "Run test and think hard if it fails"
3. [Subagent analyzes root cause in isolation]
4. Implement fix based on analysis
5. /agent test-runner "verify"
6. If passing: commit and /clear
```

**Pattern: Architecture Evolution**
```
1. /agent analyzer "Think deeply about current architecture issues"
2. [Receives analysis: bottlenecks, technical debt, opportunities]
3. /agent deep-analyzer "Recommend evolution strategy"
4. Create EVOLUTION.md plan
5. /clear
6. Execute plan phase by phase
```

**Pattern: Large Refactoring with Thinking**
```
1. /agent analyzer "Think hard about refactoring scope and risks"
2. [Receives risk assessment + strategy]
3. Create REFACTOR.md plan
4. /clear
5. For each file:
   - Load and refactor
   - /agent test-runner "analyze test results"
   - /clear before next
```

For detailed Claude Code patterns, see [references/subagent_patterns.md](references/subagent_patterns.md) and [references/context_strategies.md](references/context_strategies.md).

## Troubleshooting (All Environments)

### "Responses are getting less focused"
**Symptoms:** Claude references old, irrelevant information or responses drift off topic.

**Solutions:**
- **Web/API:** Explicitly state "Setting aside previous discussion, let's focus on..."
- **Claude Code:** Use `/clear` or `/compact`
- **Universal:** Break task into new phases with clear boundaries

### "Complex task feels overwhelming"
**Symptoms:** Unsure where to start, too many moving parts.

**Solutions:**
1. "think harder about breaking this into phases"
2. Create a planning artifact
3. Execute one phase at a time
4. Reference plan artifact as you go

### "Conversation getting too long"
**Symptoms:** Long history, hard to track what's been decided.

**Solutions:**
- **Web/API:** Create a "decisions.md" artifact to summarize key points
- **Claude Code:** Use `/compact` to compress history
- **Universal:** Start a new conversation with "Previously we decided X, Y, Z. Now let's..."

### "Need to maintain context across sessions"
**Symptoms:** Have to re-explain everything each time.

**Solutions:**
- Create artifacts documenting key decisions and context
- **Claude Code:** Use CLAUDE.md for persistent project memory
- Start new sessions with: "Continuing from previous work where we [brief summary]"

### "Code keeps being regenerated instead of edited"
**Symptoms:** Small changes result in entire code rewrites.

**Solutions:**
1. Use artifacts for code
2. Request specific edits: "Update the handle_request function to add validation"
3. Don't say "show me the code again" - reference the existing artifact

### "Responses include too much explanation"
**Symptoms:** Getting lengthy explanations when you just want output.

**Solutions:**
- Be explicit: "Just create the artifact, minimal explanation"
- "Output only, no commentary"
- "Concise response please"

### "Extended thinking not being used"
**Symptoms:** Jumping straight to solutions without analysis.

**Solutions:**
- Explicitly request: "think hard about..."
- Use stronger triggers: "ultrathink about..."
- Ask for planning: "think about multiple approaches"

## Reference Documentation

For deeper understanding, consult the reference files:

- **[references/context_strategies.md](references/context_strategies.md)** - Comprehensive workflows and scenario-based strategies (includes Claude Code specific strategies)
- **[references/subagent_patterns.md](references/subagent_patterns.md)** - Detailed subagent usage patterns for Claude Code users

Load these when you need:
- Scenario-based workflow guidance
- Advanced context management techniques
- Claude Code-specific patterns
- Troubleshooting complex context issues

## Scripts Reference (Claude Code Users)

### generate_claude_md.py

Generate project-specific CLAUDE.md files:

```bash
python scripts/generate_claude_md.py --type TYPE --output PATH
```

**Options:**
- `--type`: Project type (general, backend, frontend, fullstack, data, library)
- `--output`: Output path (default: ./CLAUDE.md)

### create_subagent.py

Create subagent configurations:

```bash
python scripts/create_subagent.py NAME --type TYPE --output DIR
```

**Options:**
- `NAME`: Agent name (e.g., test-runner, doc-searcher)
- `--type`: Agent type (researcher, tester, analyzer, builder)
- `--output`: Output directory (default: current directory)

## Getting the Most from This Skill

### For All Claude Users:

1. **Delegate complex analysis** - Use thinking delegation architecture
   - Web/API: Create analysis artifacts for deep thinking
   - Claude Code: Use deep_analyzer subagent for decisions
2. **Use extended thinking liberally** - "think hard" for planning, but delegate when possible
3. **Create artifacts for substantial content** - Keep conversation focused
4. **Break tasks into explicit phases** - Clear boundaries prevent context sprawl
5. **Document decisions in artifacts** - Persistent references you can return to

### For Claude Code Users (Additional):

6. **Create thinking-enabled subagents immediately:**
   ```bash
   python scripts/create_subagent.py architecture-advisor --type deep_analyzer
   python scripts/create_subagent.py pattern-researcher --type researcher
   python scripts/create_subagent.py code-analyzer --type analyzer
   python scripts/create_subagent.py test-analyzer --type tester
   ```
7. **Generate CLAUDE.md for each project** - Persistent project memory
8. **Practice thinking delegation** - `/agent deep-analyzer` for complex decisions
9. **Use `/clear` between major tasks** - Start each task fresh
10. **Monitor context usage** - Claude reports remaining tokens

### Activation Tips:

This skill activates automatically for complex queries, but you can explicitly invoke it:
- "Help me manage context for this task"
- "What's the best approach to keep context efficient?"
- "Analyze this decision deeply but keep context clean"
- "Think deeply about this" (will suggest delegation)

### Measuring Success:

**Signs thinking delegation is working:**
- Complex decisions made with minimal main context usage
- Multiple analyses in single session without context bloat
- Clear, well-reasoned recommendations without verbose explanations
- Can sustain 10+ complex analyses in one session

**Context efficiency metrics:**
- Traditional: ~7K tokens per complex analysis
- With delegation: ~300 tokens per complex analysis
- **Target:** 20+ analyses per 200K context window

The goal is sustainable, high-quality Claude interactions that maintain performance and analytical depth regardless of task complexity or conversation length.
