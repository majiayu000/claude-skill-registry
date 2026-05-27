---
name: showroom:create-demo
description: Guide you through creating a Red Hat Showroom demo module using the Know/Show structure for presenter-led demonstrations.
---

---
context: main
model: sonnet
---

# Demo Module Generator

Guide you through creating a Red Hat Showroom demo module using the Know/Show structure for presenter-led demonstrations.

## Workflow Diagram

![Workflow](workflow.svg)

## What You'll Need Before Starting

Have these ready before running this skill:

**Required:**
- 📁 **Target directory path** - Where to create modules (default: `content/modules/ROOT/pages/`)
- 📚 **Demo materials** - At least one of:
  - Product documentation or feature descriptions
  - URLs to technical guides or demos
  - Text describing what to demonstrate
- 🎯 **Demo objective** - What should the presenter show?

**Helpful to have:**
- 🏢 **Customer scenario** - Business context (e.g., "Financial services company needs...")
- 💼 **Value proposition** - Why does this matter to customers? What problem does it solve?
- ⏱️ **Target duration** - How long is the demo? (e.g., 10 min, 20 min)
- 👥 **Audience** - Who is watching? (Technical managers, developers, executives)
- 📝 **Previous modules** - If continuing existing demo, which module comes before this one

**Access needed:**
- ✅ Write permissions to the Showroom repository directory

## When to Use

**Use this skill when you want to**:
- Create presenter-led demo content
- Transform technical documentation into business-focused demos
- Add a module to an existing demo
- Create content for sales engineers or field demonstrations

**Don't use this for**:
- Hands-on workshop content → use `/create-lab`
- Converting to blog posts → use `/blog-generate`
- Reviewing existing content → use `/verify-content`

## Shared Rules

**IMPORTANT**: This skill follows shared contracts defined in `.claude/docs/SKILL-COMMON-RULES.md`:
- Version pinning or attribute placeholders (REQUIRED)
- Reference enforcement (REQUIRED)
- Attribute file location (REQUIRED)
- Image path conventions (REQUIRED)
- Navigation update expectations (REQUIRED)
- Failure-mode behavior (stop if cannot proceed safely)

See SKILL-COMMON-RULES.md for complete details.

## Know/Show Structure

Demos use a different format than workshops:

- **Know sections**: Business context, customer pain points, value propositions, why this matters
- **Show sections**: Step-by-step presenter instructions, what to demonstrate, expected outcomes

This separates what presenters need to **understand** (business value) from what they need to **do** (technical demonstration).

## Arguments (Optional)

This skill supports optional command-line arguments for faster workflows.

**Usage Examples**:
```bash
/create-demo                                   # Interactive mode (asks all questions)
/create-demo <directory>                       # Specify target directory
/create-demo <directory> --new                 # Create new demo in directory
/create-demo <directory> --continue <module>   # Continue from specific module
```

**Parameters**:
- `<directory>` - Target directory for demo files
  - Example: `/create-demo content/modules/ROOT/pages/`
  - If not provided, defaults to `content/modules/ROOT/pages/`
- `--new` - Flag to create new demo (generates index + overview + details + module-01)
- `--continue <module-path>` - Continue from specified previous demo module
  - Example: `/create-demo content/modules/ROOT/pages/ --continue content/modules/ROOT/pages/03-module-01-intro.adoc`
  - Reads previous module to detect story continuity

**How Arguments Work**:
- Arguments skip certain questions (faster workflow)
- You can still use interactive mode by calling `/create-demo` with no arguments
- Arguments are validated before use

## Workflow

**CRITICAL RULES**

### 1. Ask Questions SEQUENTIALLY

- Ask ONE question or ONE group of related questions at a time
- WAIT for user's answer before proceeding
- Do NOT ask questions from multiple steps together
- Do NOT skip workflows based on incomplete answers

### 2. Manage Output Tokens

- **NEVER output full demo content** - Use Write tool to create files
- **Show brief confirmations only** - "✅ Created: filename (X lines)"
- **Keep total output under 5000 tokens** - Summaries, not content
- **Files are written, not displayed** - User reviews with their editor
- **Token limit**: Claude Code has 32000 token output limit - stay well below it

**Example of WRONG approach**:
```
❌ Asking all at once:
1. Module file name?
2. UserInfo variables?
3. Presentation objective?
4. Number of demos?
```

**Example of CORRECT approach**:
```
✅ Ask sequentially:
Step 2: Complete overall demo story planning
[WAIT for completion]

Step 3.1: Module file name?
[WAIT for answer]

Step 3.2: Reference materials?
[WAIT for answer]

etc.
```

---

### Step 0: Reference Repository Setup (IMPORTANT)

**Before generating content, we need access to real Showroom demo examples for quality reference.**

**CRITICAL: This step MUST happen before any content generation to ensure quality matches real Showroom demo standards.**

**Ask the user:**

```
📚 Reference Repository Check

To generate high-quality demo content that matches Showroom standards, I need access to real Showroom demo examples.

Do you have a Showroom repository cloned locally that I can reference for patterns and examples?

Options:
1. Yes - I have a local Showroom repo (Recommended - best quality)
2. No - Clone template to /tmp/ for me
3. Skip - Generate without reference (Not recommended - may need manual rewrites)

Your choice: [1/2/3]
```

**If Option 1 (YES - Local repo):**

```
Great! Please provide the path to your Showroom repository:

Example: ~/work/showroom-content/my-demo

Path:
```

**Validation:**
- Check if path exists using Read tool
- Verify it contains demo content in `content/modules/ROOT/pages/*.adoc` files
- If invalid, ask again or offer Option 2

**Once valid path provided:**
1. Read 2-3 example demo modules from `content/modules/ROOT/pages/*.adoc`
2. Analyze and learn from:
   - Know/Show structure and separation
   - Business value messaging patterns
   - Presenter guidance formatting
   - Talk track examples ("What I say", "What I do", "What they should notice")
   - Code block formatting and syntax highlighting
   - Image and diagram patterns (link=self,window=blank usage)
   - Navigation includes and xrefs
   - List formatting (blank lines before/after lists)
   - External link patterns (^ caret usage)
   - Business metrics and ROI presentation
3. Use these patterns as templates for generating new demo content

**If Option 2 (NO - Clone template):**

```
I'll clone the Showroom template repository to /tmp/showroom-reference for you.

This provides standard Showroom demo examples to ensure quality output.

Proceed? [Yes/No]
```

**If Yes:**
```bash
git clone https://github.com/rhpds/showroom-template /tmp/showroom-reference
```

Then:
1. Read example demo modules from `/tmp/showroom-reference/content/modules/ROOT/pages/*.adoc`
2. Analyze demo patterns (same as Option 1)
3. Use for content generation

**If No or clone fails:**
- Warn user: "⚠️  Without reference examples, generated demo content quality may require significant manual rewrites"
- Ask: "Continue anyway? [Yes/No]"
- If Yes, proceed with generic templates (lower quality expected)
- If No, exit skill

**If Option 3 (Skip):**

```
⚠️  WARNING: Generating without reference repository

Without real Showroom demo examples, the generated content:
- May not match Showroom demo quality standards
- Will likely need manual rewrites
- May miss important Know/Show separation patterns
- Could lack effective business messaging
- May take 5x longer to finalize

This is the issue reported: "Module 2 is crap, requires manual rewrite with actual showroom docs"

Are you sure you want to skip reference repository? [Yes/No]
```

**If Yes:** Proceed with generic templates, but add note in final output warning about potential quality issues
**If No:** Go back to Option 1 or 2

**Why This Step Matters:**

Before this fix:
- ❌ Demo modules were "crap"
- ❌ Required manual rewrite using actual Showroom docs
- ❌ 5 days of rework time
- ❌ Business messaging didn't match Showroom quality
- ❌ Know/Show structure was inconsistent

After this fix:
- ✅ Demos generated with quality matching real Showroom content from first iteration
- ✅ Know/Show separation follows proven patterns
- ✅ Business messaging matches professional standards
- ✅ Reduces manual rewrites from days to hours
- ✅ AI learns from actual examples, not generic patterns

**Store reference path for later use:**
- Save reference repository path to use throughout demo generation
- When generating demo modules, read reference examples to match quality
- Apply learned Know/Show patterns to new content
- Follow business messaging style from references

---

### Step 1: Parse Arguments (If Provided)

**Check if user invoked skill with arguments**.

**Pattern 1: `/create-demo <directory> --new`**
```
Parsing arguments: "<directory> --new"

✓ Target directory: <directory>
✓ Mode: Create new demo
✓ Will generate: index.adoc → 01-overview → 02-details → 03-module-01

Validating directory...
[Check if directory exists, create if needed]

Skipping: Step 1 (mode already known: NEW demo)
Proceeding to: Step 2 (Plan Overall Demo Story)
```

**Pattern 2: `/create-demo <directory> --continue <module-path>`**
```
Parsing arguments: "<directory> --continue <module-path>"

✓ Target directory: <directory>
✓ Mode: Continue existing demo
✓ Previous module: <module-path>

Validating directory...
[Check if directory exists]

Reading previous module: <module-path>
[Extract story, business context, progression]

Skipping: Step 1 (mode already known: CONTINUE)
Skipping: Step 2 (story detected from previous module)
Proceeding to: Step 3 (Module-Specific Details)
```

**Pattern 3: `/create-demo <directory>`**
```
Parsing arguments: "<directory>"

✓ Target directory: <directory>

Validating directory...
[Check if directory exists]

Skipping: Target directory question
Proceeding to: Step 1 (still need to ask: new vs continue)
```

**Pattern 4: `/create-demo` (no arguments)**
```
No arguments provided.

Using interactive mode.
Target directory: Will use default (content/modules/ROOT/pages/)

Proceeding to: Step 1 (Determine Context)
```

**Argument Validation**:
- If directory doesn't exist, ask user: "Directory not found. Create it? [Yes/No]"
- If `--continue` but module path invalid, fall back to asking for story recap
- All arguments are optional - skill always works in interactive mode

---

### Step 2: Determine Context (New Demo vs Continuation)

**SKIP THIS STEP IF**:
- User provided `--new` flag in arguments (already know: NEW demo)
- User provided `--continue <module>` in arguments (already know: EXISTING demo)

**CRITICAL: DO NOT read any files or make assumptions before asking this question!**

**First, ask the user**:

```
Let's get started! I'll help you create amazing demo content.

Are you creating a new demo or continuing an existing one?

1. 🆕 Creating a NEW demo (I'll help you plan the whole story)
2. ➡️  Continuing an EXISTING demo (I'll pick up where you left off)
3. 🤔 Something else (tell me what you need)

What's your situation? [1/2/3]
```

**ONLY AFTER user answers, proceed based on their response.**

### Step 2.5: Ask for Target Directory (if not provided as argument)

**SKIP THIS STEP IF**: User provided `<directory>` as argument

**Ask the user**:
```
Where should I create the demo files?

Default location: content/modules/ROOT/pages/

Press Enter to use default, or type a different path:
```

**Validation**:
- If directory doesn't exist, ask: "Directory not found. Create it? [Yes/No]"
- If Yes, create the directory
- If No, ask again for directory

**If continuing existing demo**:
- Provide path to previous module (I'll read and auto-detect the story)

### Step 3: Plan Overall Demo Story (if new demo)

Great! Let's plan your demo together. I'll ask you a few questions to understand what you're trying to achieve.

**IMPORTANT**: Ask these as **conversational, open-ended questions**. Do NOT provide multiple choice options.

**Question 1 - The Big Picture**:
```
What's the main message you want to deliver in this demo?

Think about: What should your audience remember after seeing this?

Example: "Show how OpenShift accelerates application deployment for enterprises"

Your answer:
```

**Question 2 - Know Your Audience**:
```
Who will be watching this demo?

Examples: C-level executives, Sales engineers, Technical managers, Partners

Your audience:

And what matters most to them right now? (their business priorities)

Examples: Cost reduction, faster time-to-market, competitive advantage

Their priorities:
```

**Question 3 - The Transformation Story**:
```
Let's create the before-and-after narrative.

What's the customer challenge you're solving?

What's painful about their current state?

What does the ideal future state look like?

Your story:
```

**Question 4 - Customer Scenario**:
```
What company or industry should we feature in this demo?

Examples: "RetailCo" (retail), "FinanceCorp" (banking), "HealthTech" (healthcare)
Or create your own!

Company/industry:

What specific business challenge is driving urgency for them?

Their urgent challenge:
```

**Question 5 - Show the Impact**:
```
What quantifiable improvements will you highlight?

Examples:
- "6 weeks → 5 minutes deployment time"
- "80% reduction in infrastructure costs"
- "10x faster developer productivity"

Your key metrics:
```

**Question 6 - Timing**:
```
How long should the complete demo take?

Typical options: 15min, 30min, 45min

Your target duration:
```

**Then I'll recommend**:
- Suggested module/section breakdown
- Know/Show structure for each section
- Business narrative arc across modules
- Key proof points and "wow moments"
- Competitive differentiators to emphasize

**You can**:
- Accept the recommended flow
- Adjust sections and messaging
- Change business emphasis

---

### Step 4: Gather Module-Specific Details

Now for this specific module:

1. **Module file name**:
   - Module file name (e.g., "03-demo-intro.adoc", "04-platform-demo.adoc")
   - Files go directly in `content/modules/ROOT/pages/`
   - Pattern: `[number]-[topic-name].adoc`

2. **Reference materials** (optional but recommended):
   - URLs to Red Hat product documentation
   - Marketing materials, solution briefs
   - Local files (Markdown, AsciiDoc, PDF)
   - Pasted content
   - **Better references = better business value extraction**
   - If not provided: Generate from templates and common value propositions

3. **UserInfo variables** (optional, for accurate showroom content):
   - **I must ask the user:**

   ```
   Q: Do you have access to a deployed environment on demo.redhat.com or integration.demo.redhat.com?

   If YES (RECOMMENDED - easiest and most accurate):
   Please share the UserInfo variables from your deployed service:

   1. Login to https://demo.redhat.com (or integration.demo.redhat.com)
   2. Go to "My services" → Your service
   3. Click "Details" tab
   4. Expand "Advanced settings" section
   5. Copy and paste the output here

   This provides exact variable NAMES like:
   - openshift_cluster_console_url
   - openshift_cluster_admin_username
   - gitea_console_url
   - [custom workload variables]

   CRITICAL: I will use these to know WHICH variables exist, NOT to replace them with actual values!
   Variables will stay as placeholders: {openshift_cluster_console_url}
   Showroom replaces these at runtime with actual deployment values.

   If NO:
   Q: Would you like to use placeholder attributes for now?

   If YES:
   I'll use placeholders: {openshift_console_url}, {user}, {password}
   You can update these later when you get Advanced settings.

   If NO (RHDP internal team only):
   I can extract variables from AgnosticV repository if you have it cloned locally.
   This requires AgV path and catalog name.
   Note: Less reliable than Advanced settings.
   ```

4. **Target audience**:
   - Sales engineers, C-level executives, technical managers, developers

5. **Business scenario/challenge**:
   - Auto-detect from previous module (if exists)
   - Or ask for customer scenario (e.g., "RetailCo needs faster deployments")

6. **Technology/product focus**:
   - Example: "OpenShift", "Ansible Automation Platform"

7. **Number of demo parts**:
   - Recommended: 2-4 parts (each with Know/Show sections)

8. **Key metrics/business value**:
   - Example: "Reduce deployment time from 6 weeks to 5 minutes"

9. **Diagrams, screenshots, or demo scripts** (optional):
   - Do you have architecture diagrams, demo screenshots, or scripts?
   - If yes: Provide file paths or paste content
   - I'll save them to `content/modules/ROOT/assets/images/`
   - And reference them properly in Show sections

### Step 5: Get UserInfo Variables (if applicable)

If UserInfo variables weren't already provided in Step 3, I'll ask for them now.

**RECOMMENDED: Get from Deployed Environment (Primary Method)**

I'll ask: "Do you have access to a deployed environment on demo.redhat.com or integration.demo.redhat.com?"

**If YES** (recommended):
```
Please share the UserInfo variables from your deployed service:

1. Login to https://integration.demo.redhat.com (or demo.redhat.com)
2. Go to "My services" → Find your service
3. Click on "Details" tab
4. Expand "Advanced settings" section
5. Copy and paste the output here
```

This shows all available variables like:
- `openshift_cluster_console_url` → For showing presenter where to log in
- `openshift_api_server_url` → For API demonstrations
- `openshift_cluster_admin_username` → For admin access demos
- `openshift_cluster_admin_password` → For demo credentials
- `gitea_console_url` → For Git server demos
- `gitea_admin_username`, `gitea_admin_password` → For Gitea access
- Custom workload-specific variables → Product-specific endpoints

**If NO** (fallback):
I'll use common placeholder variables:
- `{openshift_console_url}`
- `{openshift_api_url}`
- `{user}`
- `{password}`
- `{bastion_public_hostname}`

**Alternative**: Clone collections from AgV catalog
- Read `common.yaml` from user-provided AgV path
- Clone collections from any repository (agnosticd, rhpds, etc.)
- Read workload roles to find `agnosticd_user_info` tasks
- Extract variables from `data:` sections
- Note: Less reliable than deployed environment output

**Result**: I'll use these in Show sections for precise presenter instructions with actual URLs and credentials.

### Step 6: Handle Diagrams, Screenshots, and Demo Scripts (if provided)

If you provided visual assets or scripts:

**For presenter screenshots**:
- Save to `content/modules/ROOT/assets/images/`
- Use descriptive names showing what presenters will see
- Reference in Show sections with proper context:
  ```asciidoc
  image::console-developer-view.png[Developer Perspective - What Presenters Will See,link=self,window=blank,align="center",width=700,title="Developer Perspective - What Presenters Will See"]
  ```
- **CRITICAL**: **ALWAYS** include `link=self,window=blank` to make images clickable

**For architecture diagrams**:
- Save to `content/modules/ROOT/assets/images/`
- Use business-context names: `retail-transformation-architecture.png`
- Reference in Know sections to show business value
- Use larger width (700-800px) for visibility during presentations
- **ALWAYS include `link=self,window=blank`** for clickable images

**For demo scripts or commands**:
- Format in code blocks with syntax highlighting
- Add presenter notes about what to emphasize:
  ```asciidoc
  [source,bash]
  ----
  oc new-app https://github.com/example/nodejs-ex
  ----

  [NOTE]
  ====
  **Presenter Tip:** Emphasize how this single command eliminates 3-5 days of manual setup.
  ====
  ```

**For before/after comparisons**:
- Save both images: `before-manual-deployment.png`, `after-automated-deployment.png`
- Use side-by-side or sequential placement
- Highlight business transformation visually

**Recommended image naming for demos**:
- Business context: `customer-challenge-overview.png`, `transformation-roadmap.png`
- UI walkthroughs: `step-1-login-console.png`, `step-2-create-project.png`
- Results: `deployment-success.png`, `metrics-dashboard.png`
- Comparisons: `before-state.png`, `after-state.png`

**Clickable Images (Links)**:
If an image should be clickable and link to external content, use `^` caret to open in new tab:

```asciidoc
// Using image macro with link attribute
image::customer-success-story.png[Case Study,600,link=https://www.redhat.com/case-study^]

// Using link macro around image
link:https://www.redhat.com/case-study^[image:customer-success-story.png[Case Study,600]]
```

**Critical**: Clickable images linking to external URLs MUST use `^` caret to open in new tab, preventing audience from losing demo context.

### Step 7: Fetch and Analyze References

Based on your references, I'll:
- Fetch URLs and extract technical capabilities
- Read local files
- Identify business value propositions
- Extract metrics and quantifiable benefits
- Map technical features to business outcomes
- Combine with AgnosticV variables (if provided)
- Integrate provided diagrams and screenshots strategically

**Reference Tracking** (for conclusion generation):
- Track all references used across all modules
- Store reference URLs, titles, and which modules used them
- References will be consolidated in the conclusion module, NOT in individual modules
- Each module can cite sources inline (e.g., "According to Red Hat's Total Economic Impact study...") but the formal References section will only appear in the conclusion

### Step 8: Read Templates and Verification Criteria (BEFORE Generating)

**CRITICAL: I MUST read all these files BEFORE generating content to ensure output meets all standards.**

**Templates to read:**
- `.claude/templates/demo/03-module-01.adoc`
- `.claude/templates/demo/01-overview.adoc`

**Verification criteria to read and apply DURING generation:**
1. `.claude/prompts/enhanced_verification_demo.txt` - Complete demo quality checklist
2. `.claude/prompts/redhat_style_guide_validation.txt` - Red Hat style rules
3. `.claude/prompts/verify_technical_accuracy_demo.txt` - Technical accuracy for demos
4. `.claude/prompts/verify_accessibility_compliance_demo.txt` - Accessibility requirements
5. `.claude/prompts/verify_content_quality.txt` - Content quality standards

**How I use these:**
- Read ALL verification prompts BEFORE generating
- Apply criteria WHILE generating content
- Generate content that ALREADY passes all checks
- No separate validation step needed - content is validated during creation

### Step 9: Generate Demo Module (Using Verification Criteria)

**IMPORTANT: Use Reference Repository from Step 0**

Before generating ANY demo content, refer back to the reference repository demo examples from Step 0:

1. **Read reference demo examples again** if needed to refresh patterns
2. **Match Know/Show structure** from real Showroom demos
3. **Apply learned patterns** to new demo content:
   - Know sections match reference business messaging style
   - Show sections follow reference presenter guidance patterns
   - Talk tracks ("What I say", "What I do") match reference format
   - Business metrics and ROI presentation follows reference examples
   - Code block formatting follows reference style
   - Image references use same patterns (link=self,window=blank)
   - List formatting matches reference (blank lines before/after)
   - External links follow reference pattern (^ caret for new tabs)

**This ensures generated demo content matches real Showroom demo quality instead of generic templates.**

I'll create a module with Know/Show structure:

**CRITICAL: Image Syntax Enforcement**:
When generating ANY image reference in the demo content, you MUST include `link=self,window=blank`:

✅ **CORRECT - Always use this format**:
```asciidoc
image::filename.png[Description,link=self,window=blank,width=700]
image::diagram.png[Architecture,link=self,window=blank,align="center",width=800,title="System Architecture"]
```

❌ **WRONG - Never generate images without link parameter**:
```asciidoc
image::filename.png[Description,width=700]
image::diagram.png[Architecture,align="center",width=800]
```

**Why**: This makes images clickable to open full-size in new tab, preventing presenters from losing their place.

**CRITICAL: AsciiDoc List Formatting Enforcement**:
When generating ANY list in the demo content, you MUST include blank lines before and after the list:

✅ **CORRECT - Always use proper spacing**:
```asciidoc
**Prerequisites:**

* OpenShift 4.18 or later
* Admin access to cluster
* Terminal with oc CLI

In this module, you will...
```

❌ **WRONG - Text runs together when rendered**:
```asciidoc
**Prerequisites:**
* OpenShift 4.18 or later
* Admin access to cluster
* Terminal with oc CLI
In this module, you will...
```

**Required blank lines**:
1. Blank line after bold heading (`**Text:**`) or colon (`:`)
2. Blank line before first list item
3. Blank line after last list item (before next content)

**Why**: Without blank lines, Showroom renders lists as plain text, causing content to run together and become unreadable.

**CRITICAL: Content Originality - No Plagiarism**:
All generated content MUST be original. Never copy from external sources without proper attribution.

✅ **CORRECT - Original with attribution**:
```asciidoc
According to link:https://kubernetes.io/docs/...[Kubernetes documentation^],
Kubernetes is "an open-source system for automating deployment." Red Hat OpenShift
extends Kubernetes with enterprise features including integrated CI/CD and security.
```

❌ **WRONG - Copied without attribution**:
```asciidoc
Kubernetes is an open-source system for automating deployment, scaling,
and management of containerized applications.
```

**Prohibited**:
- Copying documentation verbatim from external sources
- Slightly rewording existing tutorials
- Presenting others' examples as original work

**Required**:
- Write original explanations
- Add Red Hat-specific context
- Use proper attribution with quotes and links

**CRITICAL: No Em Dashes**:
Never use em dashes (—). Use commas, periods, or en dashes (–) instead.

✅ **CORRECT**:
```asciidoc
OpenShift, Red Hat's platform, simplifies deployments.
The process is simple. Just follow these steps.
2020–2025 (en dash for ranges)
```

❌ **WRONG - Em dash used**:
```asciidoc
OpenShift—Red Hat's platform—simplifies deployments.
The process is simple—just follow these steps.
```

**Why**: Follows Red Hat Corporate Style Guide and improves readability.

**CRITICAL: External Links Must Open in New Tab**:
All external links MUST use `^` caret to open in new tab, preventing loss of place.

✅ **CORRECT - External links with caret**:
```asciidoc
According to link:https://docs.redhat.com/...[Red Hat Documentation^], OpenShift provides...
See the link:https://www.redhat.com/case-study[RetailCo case study^] for details.
```

❌ **WRONG - Missing caret**:
```asciidoc
According to link:https://docs.redhat.com/...[Red Hat Documentation], OpenShift provides...
See the link:https://www.redhat.com/case-study[RetailCo case study] for details.
```

**Internal links (NO caret)**:
```asciidoc
✅ CORRECT - Internal navigation without caret:
Navigate to xref:03-next-module.adoc[Next Module] to continue.
See xref:02-overview.adoc#problem[Problem Statement] section.
```

**Why**: External links without caret replace current tab, causing presenters/learners to lose their place. Internal xrefs should NOT use caret to keep flow within the demo/workshop.

**CRITICAL: Bullets vs Numbers - Know vs Show**:
Knowledge sections use bullets (*). Task/step sections use numbers (.).

✅ **CORRECT - Bullets for knowledge, numbers for tasks**:
```asciidoc
=== Know

**Business Challenge:**

* Manual deployments take 8-10 weeks
* Security vulnerabilities discovered too late
* Infrastructure costs are too high

=== Show

**What I do:**

. Log into OpenShift Console at {openshift_console_url}
. Navigate to Developer perspective
. Click "+Add" → "Import from Git"
. Enter repository URL and click Create
```

❌ **WRONG - Mixed up bullets and numbers**:
```asciidoc
=== Know

**Business Challenge:**

. Manual deployments take 8-10 weeks  ← WRONG (should be bullets)
. Security vulnerabilities discovered too late
. Infrastructure costs are too high

=== Show

**What I do:**

* Log into OpenShift Console  ← WRONG (should be numbers)
* Navigate to Developer perspective
* Click "+Add" → "Import from Git"
```

**Rule**:
- Know sections → Use bullets (*) for business points, benefits, challenges
- Show sections → Use numbers (.) for sequential steps and tasks
- Verification → Use bullets (*) for success indicators

**Why**: Bullets indicate information to absorb; numbers indicate sequential actions to perform.

**CRITICAL: Demo Language - NO Learner Language**:
Demos are presenter-led, NOT learner-focused. Use the correct terminology.

**For index.adoc (Navigation Hub - if generating first demo)**:

✅ **CORRECT - Presenter-focused**:
```asciidoc
= OpenShift Platform Demo

**What This Demo Covers**

This demonstration shows how Red Hat OpenShift accelerates deployment cycles:

* Self-service developer platform capabilities
* Automated CI/CD pipeline integration
* Built-in security and compliance features
* Business ROI and cost reduction metrics
```

❌ **WRONG - Learner language**:
```asciidoc
= OpenShift Platform Demo

**What You'll Learn**

In this workshop, you will learn how to:
* Deploy applications to OpenShift
* Create CI/CD pipelines
* Configure security policies
```

**For 01-overview.adoc (Presenter Prep - if generating first demo)**:

✅ **CORRECT - Full business context for presenters**:
```asciidoc
= Demo Overview and Presenter Preparation

== Background

ACME inc is a retail company facing Black Friday deadlines with 10-week deployment cycles.
They need to accelerate feature delivery to remain competitive.

== Problem Breakdown

**Challenge 1: Slow deployment cycles** - Manual processes take 8-10 weeks
**Challenge 2: Security vulnerabilities** - 200+ CVEs discovered monthly
**Challenge 3: Infrastructure costs** - $2M annually on underutilized servers

== Solution Overview

Red Hat OpenShift provides self-service platform with automated security.

== Business Benefits

* 95% faster deployments (10 weeks → 30 minutes)
* 80% reduction in security vulnerabilities
* 60% lower infrastructure costs

== Common Customer Questions

**"How does this work with our existing tools?"**
→ Emphasize Jenkins integration path and existing tool enhancement
```

**Key Rules**:
1. index.adoc → Use "What This Demo Covers" (NOT "What You'll Learn")
2. index.adoc → Keep it brief (navigation hub)
3. index.adoc → No detailed problem statements
4. 01-overview.adoc → Complete business context for presenter preparation
5. 01-overview.adoc → Include all business benefits and customer Q&A
6. Never use "you will learn", "hands-on", "exercises" in demos

**CRITICAL: Demo Talk Track Separation**:
Demo modules MUST separate presenter guidance from technical steps:

**Required structure** for each Show section:
```asciidoc
=== Show

**What I say**:
"We're seeing companies like yours struggle with 6-8 week deployment cycles. Let me show you how OpenShift reduces that to minutes."

**What I do**:
. Log into OpenShift Console at {console_url}
. Navigate to Developer perspective
. Click "+Add" → "Import from Git"

**What they should notice**:
✓ No complex setup screens
✓ Self-service interface
✓ **Metric highlight**: "This used to take 6 weeks, watch what happens..."

**If asked**:
Q: "Does this work with our existing Git repos?"
A: "Yes, OpenShift supports GitHub, GitLab, Bitbucket, and private Git servers."

Q: "What about security scanning?"
A: "Built-in. I'll show that in part 2."
```

**Labs should NOT include talk tracks** - labs are for hands-on learners, not presenters.

**For each demo part**:

**Know Section**:
- Business challenge explanation
- Current state vs desired state
- Quantified pain points
- Stakeholder impact
- Value proposition

**Show Section**:
- **Optional visual cues** (recommended but not required)
- Step-by-step presenter instructions
- Specific commands and UI interactions
- Expected screens/outputs
- Image placeholders for key moments
- Business value callouts during demo
- Troubleshooting hints

**Example Structure**:
```asciidoc
== Part 1 — Accelerating Application Deployment

=== Know
_Customer challenge: Deployment cycles take 6-8 weeks, blocking critical business initiatives._

**Business Impact:**
* Development teams wait 6-8 weeks for platform provisioning
* Black Friday deadline in 4 weeks is at risk
* Manual processes cause errors and rework
* Competition is shipping features faster

**Value Proposition:**
OpenShift reduces deployment time from weeks to minutes through self-service developer platforms and automated CI/CD pipelines.

=== Show

**Optional visual**: Before/after deployment timeline diagram showing 6-8 weeks vs 2 minutes

* Log into OpenShift Console at {openshift_console_url}
  * Username: {user}
  * Password: {password}

* Navigate to Developer perspective → +Add

* Select "Import from Git" and enter:
  * Git Repo: `https://github.com/example/nodejs-ex`
  * Application name: `retail-checkout`
  * Deployment: Create automatically

* Click "Create" and observe:
  * Build starts automatically
  * Container image is built
  * Application deploys in ~2 minutes

image::deployment-progress.png[Deployment in Progress,link=self,window=blank,align="center",width=700,title="Deployment in Progress"]

* **Business Value Callout**: "What used to take your team 6-8 weeks just happened in 2 minutes. Developers can now deploy independently without waiting for infrastructure teams."

* Show the running application:
  * Click the route URL
  * Demonstrate the live application
  * Highlight the automatic scaling capability

* Connect to business outcome:
  "This self-service capability means your development team can meet the 4-week Black Friday deadline and ship updates daily instead of quarterly."
```

**Optional Visual Cues** (Recommended):

Add lightweight visual guidance without forcing asset creation:

```asciidoc
=== Show

**Optional visual**: Architecture diagram showing component relationships
**Optional slide**: Customer pain points - 6-8 week deployment cycles
**Optional visual**: Before/after comparison of manual vs automated workflow

[...presenter actions follow...]
```

**Cue Examples**:
- "Optional visual: Architecture diagram showing component relationships"
- "Optional slide: Customer pain points - 6-8 week deployment cycles"
- "Optional visual: Before/after comparison of manual vs automated workflow"
- "Optional diagram: Pipeline flow from commit to production"

**Guidelines**:
- Always mark as "Optional visual:" or "Optional slide:"
- Don't make demo depend on it
- Helps presenters prepare assets if they want
- Keeps demos tight without forcing asset creation

### Step 10: Validate

I'll automatically run:
- **workshop-reviewer** agent: Validates structure
- **style-enforcer** agent: Applies Red Hat style standards
- Verify Know/Show balance and business focus

### Step 11: Update Navigation (REQUIRED)

I'll automatically add the module to `content/modules/ROOT/nav.adoc` - this is REQUIRED for the module to appear in the Showroom sidebar.

**What I'll add**:
```asciidoc
* xref:<module-file>[<Module Number>. <Module Title>]
** xref:<module-file>#part-1[Part 1: <Title>]
** xref:<module-file>#part-2[Part 2: <Title>]
```

**Note**: Without this nav.adoc entry, your demo won't be accessible in Showroom!

### Step 12: Deliver

**CRITICAL: Manage Output Tokens to Prevent Overflow**

**Token Management Rules**:
1. **Write files using Write tool** - Don't output full file contents to user
2. **Show brief confirmations only** - "✅ Created: file.adoc (X lines)"
3. **Provide summary at end** - List what was created, not the full content
4. **Never output entire demo content** - Files are already written
5. **Keep total output under 5000 tokens** - Brief summaries only

**Output Format**:

```
✅ Demo Module Generation Complete

**Files Created**:
- content/modules/ROOT/pages/demo-01-platform-value.adoc (312 lines)
- content/modules/ROOT/nav.adoc (updated)

**Demo Structure**:
- Know sections: 4 (business context, pain points, value props, ROI)
- Show sections: 3 (technical demonstrations)
- Presenter tips: 8
- Business metrics: 5 quantified benefits
- Troubleshooting scenarios: 4

**Assets**:
- Diagrams needed: 3 placeholders (architecture, before/after, ROI chart)
- Screenshots needed: 2 placeholders (UI demonstrations)
- Dynamic attributes used: {openshift_console_url}, {demo_app_url}

**Presenter Notes**:
- Estimated presentation time: 25 minutes
- Business talking points included in each Know section
- Technical demo scripts in each Show section
- Pause points for questions marked

**Next Steps**:
1. Review demo: content/modules/ROOT/pages/demo-01-platform-value.adoc
2. Prepare diagrams for business context sections
3. Capture screenshots for technical demonstrations
4. Practice demo flow and timing
5. Run: verify-content to check quality
6. Create next module: create-demo (continuing existing demo)

**Note**: All files have been written. Use your editor to review them.
```

**What NOT to do**:
- ❌ Don't show full demo content in response
- ❌ Don't output the entire file you just created
- ❌ Don't paste hundreds of lines of generated AsciiDoc
- ❌ Don't include long example sections in output

**What TO do**:
- ✅ Write files using Write tool
- ✅ Show brief "Created: filename (X lines)" confirmations
- ✅ Provide structured summary
- ✅ Give clear next steps for presenters
- ✅ Keep output concise (under 5000 tokens)

### Step 13: Generate Conclusion Module (MANDATORY)

**After delivering the final module, ask if this is the last module:**

```
Q: Is this the last module of your demo?

If YES, I will now generate the mandatory conclusion module that includes:
- Business impact recap and ROI summary
- Competitive advantages demonstrated
- ALL REFERENCES used across the entire demo
- Next steps for evaluation, pilot, and production
- Call-to-action for technical teams and decision makers
- Q&A guidance

If NO, you can continue creating more modules, and I'll generate the conclusion when you're done.

Is this your last module? [Yes/No]
```

**If user answers YES (this is the last module)**:

1. Read ALL previous modules to extract:
   - All business value points and ROI metrics
   - All references cited in each module
   - Key technical capabilities demonstrated
   - Competitive differentiation points

2. Ask about references:

   **First, extract all references from previous modules:**
   - Read all module files (index.adoc, 01-overview.adoc, 02-details.adoc, 03-module-01-*.adoc, etc.)
   - Extract all external links found in the content
   - Identify reference materials provided during module creation (Step 3 question 2)
   - Compile a comprehensive list with:
     - URL
     - Link text/title
     - Which module(s) referenced it

   **Then ask the user:**
   ```
   Q: How would you like to handle references in the conclusion?

   I found these references used across your demo modules:
   1. https://www.redhat.com/... [Red Hat OpenShift Platform] - Used in: Modules 1, 3
   2. https://docs.redhat.com/... [Product Documentation] - Used in: Module 2
   3. https://customers.redhat.com/... [Customer Success Story] - Used in: Module 1
   {{ additional_references_if_found }}

   Options:
   1. Use these references as-is (I'll organize them by category)
   2. Let me provide additional references to include
   3. Let me curate the reference list (add/remove specific items)

   Your choice? [1/2/3]
   ```

   **If option 1**: Use extracted references, organize by category

   **If option 2**: Ask user to provide additional references:
   ```
   Q: Please provide additional references to include in the conclusion.

   Format: URL and description, one per line
   Example:
   https://www.redhat.com/... - Red Hat solution brief
   https://customers.redhat.com/... - Customer case study

   Your additional references:
   ```

   **If option 3**: Ask user which references to keep/remove/add:
   ```
   Q: Let's curate the reference list.

   Current references:
   {{ numbered_list_of_references }}

   Options:
   - Type numbers to REMOVE (e.g., "3, 5, 7")
   - Type "add" to add new references
   - Type "done" when finished

   Your action:
   ```

3. Detect highest module number (e.g., if last module is 05-module-03, conclusion will be 06-conclusion.adoc)

4. Generate conclusion module using the embedded template below

5. Customize the template with Know/Show structure:
   - File: `0X-conclusion.adoc` (where X = next sequential number)
   - **Know**: Business impact recap, ROI summary, competitive advantages
   - **Show**: Demo capabilities recap, technical highlights
   - Next steps: Workshops, POC, deep dives
   - **References**: Consolidated references from all modules (REQUIRED)
   - Call to action for decision makers and technical teams
   - Q&A guidance with common questions

6. Update nav.adoc with conclusion entry at the end

7. Provide brief confirmation

**If user answers NO (more modules to come)**:
- Note that conclusion will be generated after the last module
- User can invoke /create-demo again to add more modules
- When adding the final module, this question will be asked again

**Embedded Demo Conclusion Template**:
```asciidoc
= Demo Conclusion and Next Steps

*Presenter Note*: Use this concluding section to wrap up the demonstration, reinforce key messages, and provide clear next steps for the audience.

== Summary

=== Know

**Business Impact Recap**

You've just seen how {{ product_name }} addresses the critical business challenges we discussed:

* **{{ business_challenge_1 }}**: Solved with {{ solution_1 }}
* **{{ business_challenge_2 }}**: Solved with {{ solution_2 }}
* **{{ business_challenge_3 }}**: Solved with {{ solution_3 }}

**ROI and Value**

The solution demonstrated today delivers:

* {{ roi_metric_1 }} - {{ benefit_1 }}
* {{ roi_metric_2 }} - {{ benefit_2 }}
* {{ roi_metric_3 }} - {{ benefit_3 }}

**Competitive Advantages**

What sets this apart:

. {{ differentiator_1 }}
. {{ differentiator_2 }}
. {{ differentiator_3 }}

=== Show

**What We Demonstrated**

In this demo, you saw:

. ✅ {{ demo_capability_1 }}
. ✅ {{ demo_capability_2 }}
. ✅ {{ demo_capability_3 }}
. ✅ {{ demo_capability_4 }}

**Key Technical Highlights**

The most impressive technical capabilities:

* **{{ technical_highlight_1 }}**: {{ why_it_matters_1 }}
* **{{ technical_highlight_2 }}**: {{ why_it_matters_2 }}
* **{{ technical_highlight_3 }}**: {{ why_it_matters_3 }}

== Next Steps for Your Organization

=== Immediate Actions

Help your audience get started:

. **Try It Yourself**: {{ workshop_url }} - Hands-on workshop based on this demo
. **Request POC**: {{ poc_contact }} - Proof of concept in your environment
. **Schedule Deep Dive**: {{ schedule_url }} - Technical architecture session

=== Recommended Path

**Phase 1: Evaluate** (Weeks 1-2)::
* Attend hands-on workshop
* Review technical documentation
* Assess fit for your use cases

**Phase 2: Pilot** (Weeks 3-6)::
* Deploy proof of concept
* Test with representative workloads
* Measure performance and ROI

**Phase 3: Production** (Months 2-3)::
* Roll out to production environment
* Train teams
* Scale across organization

=== Resources

**Documentation**:

* link:{{ product_docs_url }}[{{ product_name }} Documentation^]
* link:{{ architecture_guide_url }}[Architecture Guide^]
* link:{{ best_practices_url }}[Best Practices^]

**Workshops and Training**:

* link:{{ workshop_url }}[Hands-on Workshop^] - Based on this demo
* link:{{ training_url }}[{{ product_name }} Training^]

**Support and Community**:

* link:{{ community_url }}[Community Forums^]
* link:{{ support_url }}[Enterprise Support^]
* link:{{ blog_url }}[Technical Blog^]

== Call to Action

*Presenter Guidance*: Tailor this section based on your audience (technical vs executive, evaluation vs purchase stage).

=== For Technical Teams

**Ready to build?**

. Access the hands-on workshop: {{ workshop_url }}
. Clone the demo repository: {{ demo_repo_url }}
. Join the community: {{ community_url }}

=== For Decision Makers

**Ready to transform your operations?**

. Schedule a custom demo: {{ custom_demo_url }}
. Request ROI analysis: {{ roi_analysis_contact }}
. Speak with an architect: {{ architect_contact }}

== Questions and Discussion

*Presenter Note*: Leave 5-10 minutes for Q&A. Common questions and answers:

**Q: How long does deployment take?**::
A: {{ deployment_time }} with our guided process. Proof of concept can be running in {{ poc_time }}.

**Q: What's the learning curve?**::
A: {{ learning_curve }}. Workshop participants are productive within {{ productivity_time }}.

**Q: Integration with existing tools?**::
A: {{ integration_summary }}. We support {{ integration_list }}.

**Q: Support and SLAs?**::
A: {{ support_summary }}. Enterprise support includes {{ sla_details }}.

== Presenter Action Items

*For Sales Engineers / Solution Architects*: Follow these steps after the demo:

=== Immediate Follow-up (Within 24 hours)

. **Send Demo Recording**: Email recording link with key timestamps
. **Share Resources**: Send links to documentation, workshop, and trial access
. **Schedule Next Meeting**: Book follow-up for deeper technical discussion or POC planning
. **Internal Notes**: Log demo feedback, questions asked, and objections in CRM

=== Within One Week

. **Proposal or ROI Analysis**: Send customized proposal based on their requirements
. **Technical Deep Dive**: Offer architecture review session with specialist
. **POC Proposal**: Outline proof-of-concept scope, timeline, and success criteria
. **Connect with Product Team**: Loop in product specialists if needed

=== Qualification Checkpoints

Based on this demo, assess:

* **Budget**: Do they have budget allocated or need justification?
* **Timeline**: When do they need to make a decision?
* **Authority**: Who else needs to be involved in the decision?
* **Need**: Is this a critical priority or nice-to-have?

== References

**CRITICAL**: This section consolidates ALL references used across the entire demo.

Read all previous modules and extract every reference cited, then organize them by category:

=== Product Documentation

* link:{{ product_docs_url }}[{{ product_name }} Documentation^] - Used in: Modules {{ modules_list }}
* link:{{ feature_docs_url }}[{{ feature_name }} Guide^] - Used in: Modules {{ modules_list }}

=== Red Hat Resources

* link:{{ redhat_resource_1 }}[{{ resource_title_1 }}^] - Used in: Module {{ module_number }}
* link:{{ solution_brief_url }}[{{ solution_brief_title }}^] - Used in: Module {{ module_number }}

=== Customer Success Stories

* link:{{ customer_story_1 }}[{{ customer_name_1 }} Case Study^] - Used in: Module {{ module_number }}
* link:{{ customer_story_2 }}[{{ customer_name_2 }} Success Story^] - Used in: Module {{ module_number }}

=== Industry Research and Analysis

* link:{{ analyst_report_url }}[{{ analyst_report_title }}^] - Market research
* link:{{ industry_study_url }}[{{ study_title }}^] - Industry benchmarks

**Guidelines for References section**:
- Group references by category (Product Docs, Red Hat Resources, Customer Stories, Research)
- Include which module(s) used each reference
- ALL external links must use `^` caret to open in new tab
- Provide brief context for each reference (what it covers)
- Ensure ALL references from ALL modules are included

== Thank You

Thank you for your time and attention. We're excited to help you {{ primary_value_proposition }}.

**Contact Information**:

* Sales: {{ sales_contact }}
* Technical: {{ technical_contact }}
* Support: {{ support_contact }}

---

**Demo**: {{ demo_name }} +
**Presented**: {localdate} +
**Platform**: Red Hat Showroom
```

**Conclusion Module Naming**:
- File: `0X-conclusion.adoc` (sequential number, e.g., 06-conclusion.adoc)
- Title: `= Demo Conclusion and Next Steps`
- Nav entry: `* xref:0X-conclusion.adoc[Conclusion and Next Steps]`

**Content to Include** (ALL REQUIRED):
- ✅ **Know**: Business impact recap, ROI metrics, competitive advantages
- ✅ **Show**: Demo capabilities summary, technical highlights
- ✅ "Next Steps for Your Organization" - Evaluation path, pilot, production
- ✅ "Resources" - Documentation, workshops, community
- ✅ "Call to Action" - Tailored for technical teams vs decision makers
- ✅ "Q&A Guidance" - Common questions with suggested answers
- ✅ **"References"** - Consolidate ALL references from ALL modules (MANDATORY)
- ✅ "Presenter Action Items" - Follow-up guidance for sales engineers
- ✅ "Thank You" - Contact information and closing

**CRITICAL**: The References section MUST include every reference used across all demo modules, organized by category (Product Docs, Red Hat Resources, Customer Stories, Research).

## Example Usage

### Example 1: Create First Demo Module with Overall Story Planning

```
User: Create a demo showing OpenShift value for C-level executives

Skill: Excellent! Since this is a new demo, let me gather the overall story first.

**Overall Demo Planning:**

Q: Are you creating a new demo or continuing an existing demo?
A: Creating a new demo

Q: What's the overall message?
A: "Show how OpenShift reduces time-to-market and operational costs for enterprises"

Q: Target audience?
A: C-level executives (CTO, CIO) evaluating platform modernization

Q: What are their business priorities?
A: - Reduce operational costs
   - Faster feature delivery to stay competitive
   - Risk mitigation (security, compliance)

Q: Business transformation story?
A: Current state: Manual deployments take 6-8 weeks, blocking business initiatives
   Desired state: Self-service platform enabling daily deployments

Q: Customer scenario?
A: "RetailCo" - Retail company facing Black Friday deadline with current 10-week deployment cycles

Q: Key metrics to showcase?
A: - 8 weeks → 10 minutes deployment time
   - 80% reduction in infrastructure costs
   - 95% reduction in security vulnerabilities

Q: Demo duration?
A: 30 minutes total

**Recommended Demo Flow:**

Based on your goals, I recommend 2 modules:

Module 1: Platform Value & Developer Experience (15 min)
- Know: RetailCo's deployment challenge, business impact
- Show: Self-service deployment demonstration
- Proof point: 8 weeks → 10 minutes
- Story: Developer empowerment, IT team efficiency

Module 2: Business Continuity & ROI (15 min)
- Know: Cost structure, security posture improvements
- Show: Auto-scaling, built-in security scanning
- Proof point: 80% cost reduction, 95% fewer vulnerabilities
- Story: Strategic platform investment ROI

Does this flow work for you, or adjustments needed?

User: Perfect! Create Module 1.

Skill: Great! Now let me gather details for Module 1...

Q1: Module file name? → "03-platform-value.adoc"
Q2: Reference materials? → https://www.redhat.com/en/technologies/cloud-computing/openshift
Q3: Target audience details? → C-level (using overall)
Q4: Business scenario? → "RetailCo" (using overall story)
Q5: Technology? → "OpenShift Container Platform"
Q6: Demo parts? → 3
Q7: Key metrics? → "8 weeks → 10 minutes" (using overall)
Q8: Diagrams? → Architecture diagram: ~/diagrams/retail-platform.png

[Generates Module 1 with RetailCo story]
[Sets up story arc for Module 2]

✓ Created: content/modules/ROOT/pages/03-platform-value.adoc
✓ Story established: RetailCo's platform modernization journey
✓ Business metrics integrated throughout
✓ Module flow documented for Module 2
✓ Ready for Module 2 (will auto-continue story)
```

### Example 2: Basic Demo Creation

```
User: Create demo Module 1 for OpenShift using:
      https://docs.openshift.com/container-platform/4.14/

Skill: I'll create that demo module. Let me ask questions...
       [asks if new demo or continuing]
       [if new demo: asks overall story questions]
       [asks module-specific questions]
       [generates module with business story]
       [validates with agents]

✓ Created: content/modules/ROOT/pages/03-platform-demo.adoc
✓ Presenter notes included
✓ Screenshot guide provided
✓ Navigation updated
```

### Example 3: Create Demo with Architecture Diagrams

```
User: Create demo for OpenShift AI value proposition. I have:
      - Architecture diagram: ~/diagrams/ai-platform-architecture.png
      - Before/after workflow diagrams

Skill: Excellent! Let me gather details...

Q1: Module file name? → "03-ai-platform-demo.adoc"
Q2: Reference materials? → https://www.redhat.com/en/technologies/cloud-computing/openshift/openshift-ai
Q3: Target audience? → C-level executives
Q4: Business scenario? → "TechCorp needs faster AI model deployment"
Q5: Technology? → "Red Hat OpenShift AI"
Q6: Demo parts? → 3
Q7: Key metrics? → "Weeks to hours for model deployment"
Q8: Diagrams/screenshots? → Yes:
    - Architecture: ~/diagrams/ai-platform-architecture.png
    - Before workflow: ~/diagrams/before-manual-ml.png
    - After workflow: ~/diagrams/after-automated-ml.png

Skill: Perfect! Processing diagrams and creating demo...

[Saves diagrams to assets/images/]
→ ai-platform-architecture.png
→ before-manual-ml.png
→ after-automated-ml.png

[Generates demo with:]
- Part 1 Know section includes architecture diagram
- Part 1 Show section references the architecture
- Part 2 Know section uses before/after comparison
- Each diagram has business-focused captions
- Presenter tips for discussing diagrams

Example output:
```asciidoc
== Part 1 — AI Platform Overview

=== Know
_TechCorp's data scientists wait weeks for infrastructure, delaying critical AI initiatives._

image::ai-platform-architecture.png[Red Hat OpenShift AI Platform Architecture,link=self,window=blank,align="center",width=800,title="Red Hat OpenShift AI Platform Architecture"]

**Current Challenge:**
* 2-3 weeks to provision ML infrastructure
* Manual environment setup prone to errors
* Inconsistent tooling across teams

=== Show
* Show the architecture diagram and explain:
  "This is how OpenShift AI eliminates infrastructure delays..."

* Log into OpenShift AI Dashboard at {rhods_dashboard_url}

[NOTE]
====
**Presenter Tip:** Point to the architecture diagram as you navigate the UI.
Show how the platform maps to the architectural components.
====
```

✓ Created: content/modules/ROOT/pages/03-ai-platform-demo.adoc
✓ 3 diagrams saved and referenced appropriately
✓ Before/after comparison integrated in Know section
✓ Presenter notes tied to visual elements
```

## Know Section Best Practices

Good Know sections include:

**Business Challenge**:
- Specific customer pain point
- Current state with metrics
- Why it matters now (urgency)

**Current vs Desired State**:
- "Now: 6-8 week deployment cycles"
- "Goal: Deploy multiple times per day"

**Stakeholder Impact**:
- Who cares: "VP Engineering, Product Managers"
- Why: "Missing market windows, losing to competitors"

**Value Proposition**:
- Clear benefit statement
- Quantified outcome
- Business language, not tech jargon

## Show Section Best Practices

Good Show sections include:

**Clear Instructions**:
- Numbered steps
- Specific UI elements ("Click Developer perspective")
- Exact field values to enter

**Expected Outcomes**:
- What presenters should see
- Screenshots of key moments
- Success indicators

**Business Callouts**:
- Connect each technical step to business value
- Use phrases like "This eliminates..." or "This reduces..."
- Quantify where possible

**Presenter Tips**:
- Common questions to expect
- Troubleshooting hints
- Pacing suggestions

## Tips for Best Results

- **Specific metrics**: "6 weeks → 5 minutes" not "faster deployments"
- **Real scenarios**: Base on actual customer challenges
- **Visual emphasis**: Demos need more screenshots than workshops
- **Business language**: Executives care about outcomes, not features
- **Story arc**: Build narrative across parts

## Quality Standards

Every demo module will have:
- ✓ Know/Show structure for each part
- ✓ Business context before technical steps
- ✓ Quantified metrics and value propositions
- ✓ Clear presenter instructions
- ✓ Image placeholders with descriptions
- ✓ Business value callouts during Show
- ✓ External links with `^` to open in new tab
- ✓ Dynamic variables as placeholders (not replaced with actual values)
- ✓ Target audience appropriate language
- ✓ Red Hat style compliance

## Common Demo Patterns

**Executive Audience**:
- More Know, less Show
- Focus on business outcomes
- High-level demonstrations
- Emphasize strategic value

**Technical Audience**:
- Balanced Know/Show
- Show depth and capabilities
- Include architecture discussions
- Technical credibility focus

**Sales Engineers**:
- Detailed Show sections
- Competitive differentiators
- Objection handling
- ROI calculations

## Integration Notes

**Templates used**:
- `.claude/templates/demo/03-module-01.adoc`
- `.claude/templates/demo/01-overview.adoc`

**Agents invoked**:
- `workshop-reviewer` - Validates structure
- `style-enforcer` - Applies Red Hat style

**Files created**:
- Demo module: `content/modules/ROOT/pages/<module-file>.adoc`
- Assets: `content/modules/ROOT/assets/images/`

**Files modified** (with permission):
- `content/modules/ROOT/nav.adoc` - Adds navigation entry
