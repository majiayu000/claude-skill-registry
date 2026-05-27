---
name: showroom:create-lab
description: Guide you through creating a single Red Hat Showroom workshop module from reference materials (URLs, files, docs, or text) with business storytelling and proper AsciiDoc formatting.
---

---
context: main
model: sonnet
---

# Lab Module Generator

Guide you through creating a single Red Hat Showroom workshop module from reference materials (URLs, files, docs, or text) with business storytelling and proper AsciiDoc formatting.

## Workflow Diagram

![Workflow](workflow.svg)

## What You'll Need Before Starting

Have these ready before running this skill:

**Required:**
- 📁 **Target directory path** - Where to create modules (default: `content/modules/ROOT/pages/`)
- 📚 **Reference materials** - At least one of:
  - URLs to documentation, blogs, or guides
  - Local files with technical content
  - Text/notes describing what to build
- 🎯 **Learning objective** - What should learners accomplish?

**Helpful to have:**
- 🏢 **Company/scenario context** - Business story for the lab (e.g., "ACME Corp needs...")
- ⏱️ **Target duration** - How long should this module take? (e.g., 15 min, 30 min)
- 👥 **Audience level** - Beginner, Intermediate, or Advanced
- 📝 **Previous modules** - If continuing existing lab, know which module comes before this one

**Access needed:**
- ✅ Write permissions to the Showroom repository directory

## When to Use

**Use this skill when you want to**:
- Create a new workshop module from scratch
- Convert documentation into hands-on lab format
- Add a module to an existing workshop
- Transform technical content into engaging learning experience

**Don't use this for**:
- Creating demo content → use `/create-demo`
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

## Arguments (Optional)

This skill supports optional command-line arguments for faster workflows.

**Usage Examples**:
```bash
/create-lab                                    # Interactive mode (asks all questions)
/create-lab <directory>                        # Specify target directory
/create-lab <directory> --new                  # Create new lab in directory
/create-lab <directory> --continue <module>    # Continue from specific module
```

**Parameters**:
- `<directory>` - Target directory for module files
  - Example: `/create-lab content/modules/ROOT/pages/`
  - If not provided, defaults to `content/modules/ROOT/pages/`
- `--new` - Flag to create new lab (generates index + overview + details + module-01)
- `--continue <module-path>` - Continue from specified previous module
  - Example: `/create-lab content/modules/ROOT/pages/ --continue content/modules/ROOT/pages/03-module-01-intro.adoc`
  - Reads previous module to detect story continuity

**How Arguments Work**:
- Arguments skip certain questions (faster workflow)
- You can still use interactive mode by calling `/create-lab` with no arguments
- Arguments are validated before use

## Workflow

**CRITICAL RULES**

### 1. Ask Questions SEQUENTIALLY

- Ask ONE question or ONE group of related questions at a time
- WAIT for user's answer before proceeding
- Do NOT ask questions from multiple steps together
- Do NOT skip workflows based on incomplete answers

### 2. File Generation Order (First Module ONLY)

**If this is the FIRST module of a NEW lab, you MUST generate files in this EXACT order:**

1. **index.adoc** - Learner landing page (NOT facilitator guide)
2. **01-overview.adoc** - Business scenario and learning objectives
3. **02-details.adoc** - Technical requirements and setup
4. **03-module-01-*.adoc** - First hands-on module

**NEVER skip index/overview/details for first module!**

**File naming convention**:
- index.adoc (no number prefix)
- 01-overview.adoc
- 02-details.adoc
- 03-module-01-*.adoc
- 04-module-02-*.adoc
- 05-module-03-*.adoc
- etc.

**If continuing existing lab**:
- Detect next file number from existing modules
- Generate: 0X-module-YY-*.adoc (where X = next sequential file number)
- Example: If existing has 03-module-01, 04-module-02, next is 05-module-03
- Skip index/overview/details (already exist)

### 3. Manage Output Tokens

- **NEVER output full module content** - Use Write tool to create files
- **Show brief confirmations only** - "✅ Created: filename (X lines)"
- **Keep total output under 5000 tokens** - Summaries, not content
- **Files are written, not displayed** - User reviews with their editor
- **Token limit**: Claude Code has 32000 token output limit - stay well below it

**Example of WRONG approach**:
```
❌ Asking all at once:
1. Module file name?
2. UserInfo variables?
3. Learning objective?
4. Number of exercises?
```

**Example of CORRECT approach**:
```
✅ Ask sequentially:
Step 2: Complete overall lab story planning
[WAIT for completion]

Step 3.1: Module file name?
[WAIT for answer]

Step 3.2: Reference materials?
[WAIT for answer]

etc.
```

---

### Step 0: Reference Repository Setup (IMPORTANT)

**Before generating content, we need access to real Showroom examples for quality reference.**

**CRITICAL: This step MUST happen before any content generation to ensure quality matches real Showroom standards.**

**Ask the user:**

```
📚 Reference Repository Check

To generate high-quality content that matches Showroom standards, I need access to real Showroom examples.

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

Example: ~/work/showroom-content/my-workshop

Path:
```

**Validation:**
- Check if path exists using Read tool
- Verify it contains `content/modules/ROOT/pages/*.adoc` files
- If invalid, ask again or offer Option 2

**Once valid path provided:**
1. Read 2-3 example modules from `content/modules/ROOT/pages/*.adoc`
2. Analyze and learn from:
   - Section structure (= Title, == Heading, === Subheading)
   - Code block formatting and syntax highlighting
   - Admonition usage (TIP, NOTE, WARNING, IMPORTANT)
   - Image and diagram patterns (link=self,window=blank usage)
   - Navigation includes and xrefs
   - List formatting (blank lines before/after lists)
   - External link patterns (^ caret usage)
   - Business scenario integration
3. Use these patterns as templates for generating new content

**If Option 2 (NO - Clone template):**

```
I'll clone the Showroom template repository to /tmp/showroom-reference for you.

This provides standard Showroom examples to ensure quality output.

Proceed? [Yes/No]
```

**If Yes:**
```bash
git clone https://github.com/rhpds/showroom-template /tmp/showroom-reference
```

Then:
1. Read example modules from `/tmp/showroom-reference/content/modules/ROOT/pages/*.adoc`
2. Analyze patterns (same as Option 1)
3. Use for content generation

**If No or clone fails:**
- Warn user: "⚠️  Without reference examples, generated content quality may require significant manual rewrites"
- Ask: "Continue anyway? [Yes/No]"
- If Yes, proceed with generic templates (lower quality expected)
- If No, exit skill

**If Option 3 (Skip):**

```
⚠️  WARNING: Generating without reference repository

Without real Showroom examples, the generated content:
- May not match Showroom quality standards
- Will likely need manual rewrites
- May miss important formatting patterns
- Could take 5x longer to finalize

This is the issue reported: "Module 2 is crap, requires manual rewrite with actual showroom docs"

Are you sure you want to skip reference repository? [Yes/No]
```

**If Yes:** Proceed with generic templates, but add note in final output warning about potential quality issues
**If No:** Go back to Option 1 or 2

**Why This Step Matters:**

Before this fix:
- ❌ Module 2 was "crap"
- ❌ Required manual rewrite using actual Showroom docs
- ❌ 5 days of rework time
- ❌ WebFetch tried to get examples from GitHub URLs but got 404 errors

After this fix:
- ✅ Modules generated with quality matching real Showroom content from first iteration
- ✅ Reduces manual rewrites from days to hours
- ✅ AI learns from actual examples, not generic patterns
- ✅ Faster iteration, fewer back-and-forth edits

**Store reference path for later use:**
- Save reference repository path to use throughout content generation
- When generating modules, read reference examples to match quality
- Apply learned patterns to new content

---

### Step 1: Parse Arguments (If Provided)

**Check if user invoked skill with arguments**.

**Pattern 1: `/create-lab <directory> --new`**
```
Parsing arguments: "<directory> --new"

✓ Target directory: <directory>
✓ Mode: Create new lab
✓ Will generate: index.adoc → 01-overview → 02-details → 03-module-01

Validating directory...
[Check if directory exists, create if needed]

Skipping: Step 1 (mode already known: NEW lab)
Proceeding to: Step 2 (Plan Overall Lab Story)
```

**Pattern 2: `/create-lab <directory> --continue <module-path>`**
```
Parsing arguments: "<directory> --continue <module-path>"

✓ Target directory: <directory>
✓ Mode: Continue existing lab
✓ Previous module: <module-path>

Validating directory...
[Check if directory exists]

Reading previous module: <module-path>
[Extract story, company, progression]

Skipping: Step 1 (mode already known: CONTINUE)
Skipping: Step 2 (story detected from previous module)
Proceeding to: Step 3 (Module-Specific Details)
```

**Pattern 3: `/create-lab <directory>`**
```
Parsing arguments: "<directory>"

✓ Target directory: <directory>

Validating directory...
[Check if directory exists]

Skipping: Target directory question
Proceeding to: Step 1 (still need to ask: new vs continue)
```

**Pattern 4: `/create-lab` (no arguments)**
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

### Step 2: Determine Context (New Lab vs Existing Lab)

**SKIP THIS STEP IF**:
- User provided `--new` flag in arguments (already know: NEW lab)
- User provided `--continue <module>` in arguments (already know: EXISTING lab)

**CRITICAL: DO NOT read any files or make assumptions before asking this question!**

**First, ask the user**:

```
Welcome! Let's create your workshop together.

Are you starting a brand new lab or adding to an existing one?

1. 🆕 NEW lab (I'll create the whole thing: index → overview → details → first module)
2. ➕ EXISTING lab (I'll add the next module and continue your story)
3. 🤔 Something else (tell me what you need)

What's your situation? [1/2/3]
```

**ONLY AFTER user answers, proceed based on their response.**

### Step 2.5: Ask for Target Directory (if not provided as argument)

**SKIP THIS STEP IF**: User provided `<directory>` as argument

**Ask the user**:
```
Where should I create the lab files?

Default location: content/modules/ROOT/pages/

Press Enter to use default, or type a different path:
```

**Validation**:
- If directory doesn't exist, ask: "Directory not found. Create it? [Yes/No]"
- If Yes, create the directory
- If No, ask again for directory

**If option 1 (NEW lab)**:
- Generate ALL workshop files: index.adoc, 01-overview.adoc, 02-details.adoc, 03-module-01-*.adoc
- Proceed to Step 2 (Plan Overall Lab Story)

**If option 2 (EXISTING lab)**:
- Detect next file number from existing modules
- Generate ONLY next module: 0X-module-YY-*.adoc
- Skip Step 2 (already have overall story)
- Ask for previous module path or story recap

**If continuing existing lab**:
- Option 1: Provide path to previous module (I'll read and auto-detect story)
- Option 2: If previous module not available, I'll ask for story recap:
  - Company name and scenario
  - What was completed in previous modules
  - Current learning state
  - What comes next in progression

**Fallback behavior**:
- If user says "continuing" but cannot provide previous module content or workspace access:
  - Ask user to paste content of last module (or key sections)
  - OR ask short "Story Recap" questions:
    1. Company/scenario name?
    2. What topics were covered in previous modules?
    3. What skills have learners gained so far?
    4. What's the current state in the story?
  - This prevents broken continuity

### Step 3: Plan Overall Lab Story (if first module)

Awesome! Let's design your workshop together. I'll ask you some questions to build the perfect learning experience.

**IMPORTANT**: Ask these as **conversational, open-ended questions**. Do NOT provide multiple choice options.

**Question 1 - What Should We Call This?**:
```
What's the name of your workshop?

Example: "Building AI/ML Workloads on OpenShift AI"

I'll use this to set up your lab title and generate a clean URL-friendly slug.

Your lab name:

[After user provides title, I'll suggest a slug like "building-ai-ml-workloads-openshift-ai"]
```

**Question 2 - The Learning Goal**:
```
What's the main goal of this lab?

What should learners be able to do when they finish?

Example: "Learn to build and deploy AI/ML workloads on OpenShift AI"

Your lab goal:
```

**Question 3 - Who's Learning?**:
```
Who is this lab designed for?

Examples: Developers, Architects, SREs, Data Scientists, Platform Engineers

Your target audience:

What's their experience level?
- Beginner (new to the technology)
- Intermediate (some hands-on experience)
- Advanced (production experience)

Their level:
```

**Question 4 - The Learning Journey**:
```
By the end of this lab, what should learners understand and be able to do?

List the key skills they'll gain:

Your learning outcomes:
```

**Question 5 - Make It Real**:
```
What company or business scenario should we use to make this relatable?

Examples: "ACME Corp", "RetailCo", "FinTech Solutions"
Or create your own!

Company name:

What business challenge are they facing that drives this learning?

Their challenge:
```

**Question 6 - How Long?**:
```
How much time should learners budget for the complete lab?

Typical options: 30min, 1hr, 2hr

Your target duration:
```

**Question 7 - Technical Environment**:
```
Let's nail down the technical details:

OpenShift version? (e.g., "4.18", "4.20", or I can use {ocp_version} placeholder)

Product versions? (e.g., "OpenShift Pipelines 1.12, OpenShift AI 2.8")

Cluster type? (SNO or multinode)

Access level? (admin only, or multi-user with keycloak/htpasswd)

Your environment details:

Note: If you're not sure, I'll use placeholders that work across versions.
```

**Then I'll recommend**:
- Suggested module breakdown (how many modules, what each covers)
- Progressive learning flow (foundational → intermediate → advanced)
- Story arc across modules
- Key milestones and checkpoints

**You can**:
- Accept the recommended flow
- Adjust module count and topics
- Change the progression

### Step 3.1: Update Lab Configuration Files (REQUIRED for new labs)

**CRITICAL: Update these files with the lab name BEFORE generating any content files.**

Using the lab title and slug from Step 2, update:

1. **site.yml** (line 3):
   ```yaml
   site:
     title: {{ lab_title }}  # e.g., "Building AI/ML Workloads on OpenShift AI"
   ```

2. **content/antora.yml** (line 2):
   ```yaml
   name: modules
   title: {{ lab_title }}  # Same as site.yml
   ```

3. **content/antora.yml** (line 9):
   ```yaml
   asciidoc:
     attributes:
       lab_name: "{{ lab_slug }}"  # e.g., "building-ai-ml-workloads-openshift-ai"
   ```

**Example transformation**:
- User says: "Building AI/ML Workloads on OpenShift AI"
- Generated slug: `building-ai-ml-workloads-openshift-ai`
- site.yml title: "Building AI/ML Workloads on OpenShift AI"
- antora.yml title: "Building AI/ML Workloads on OpenShift AI"
- antora.yml lab_name: "building-ai-ml-workloads-openshift-ai"

**Note**: These files must be updated BEFORE Step 8 (Generate Files).

---

### Step 4: Gather Module-Specific Details

Now for this specific module:

1. **Module file name and numbering**:
   - **Naming convention**: `0X-module-YY-<slug>.adoc` (e.g., `03-module-01-pipelines-intro.adoc`)
   - **Title convention**: `= Module X: <Title>` (e.g., `= Module 1: Pipeline Fundamentals`)
   - Files go in `content/modules/ROOT/pages/`
   - **Number prefix**: 03 for first module, 04 for second, etc. (after 01-overview, 02-details)
   - **Conflict detection**: If file exists, suggest next available number
   - **Warning**: Don't overwrite existing modules without confirmation

2. **Reference materials** (optional but recommended):
   - URLs to Red Hat product documentation
   - Local file paths (Markdown, AsciiDoc, text, PDF)
   - Pasted content
   - **Better references = better content quality**
   - If not provided: Generate from templates and common patterns

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

4. **Main learning objective**:
   - Example: "Create and run a CI/CD pipeline with Tekton"

5. **Business scenario**:
   - Auto-detect from previous module (if exists)
   - Or ask for company name (default: ACME Corp)

6. **Technology/product focus**:
   - Example: "OpenShift Pipelines", "Podman"

7. **Number of exercises**:
   - Recommended: 2-3

8. **Diagrams, screenshots, or code blocks** (optional):
   - Do you have diagrams, screenshots, or code examples to include?
   - If yes: Provide file paths or paste content
   - I'll save them to `content/modules/ROOT/assets/images/`
   - And reference them properly in AsciiDoc

9. **Troubleshooting section** (optional):
   ```
   Q: Would you like to include a troubleshooting section in this module?

   A troubleshooting section helps learners solve common issues they may encounter.

   Options:
   1. Yes, include troubleshooting (Recommended for production workshops)
   2. No, skip it for now (I'll add it later if needed)

   Your choice? [1/2]
   ```

   **When to recommend "Yes"**:
   - Production-ready workshops
   - Complex technical modules with many potential failure points
   - Modules involving external dependencies (registries, APIs, networks)

   **When "No" is acceptable**:
   - Simple introductory modules
   - Proof-of-concept content
   - Modules with very straightforward steps

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
- `openshift_cluster_console_url`
- `openshift_api_server_url`
- `openshift_cluster_admin_username`
- `openshift_cluster_admin_password`
- `gitea_console_url`
- `gitea_admin_username`
- `gitea_admin_password`
- Custom workload-specific variables

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

**Map to Showroom attributes**:
```asciidoc
{openshift_cluster_console_url}
{openshift_api_server_url}
{openshift_cluster_admin_username}
{gitea_console_url}
{{ custom_variable }}
```

**CRITICAL: DO NOT Replace Variables with Actual Values**:
- ALWAYS keep variables as placeholders: `{openshift_console_url}`
- NEVER replace with actual values like `https://console-openshift-console.apps.cluster-abc123.abc123.example.opentlc.com`
- Showroom will replace these at runtime with actual deployment values
- Each deployment gets different URLs - variables MUST stay dynamic
- Example in module content:
  ```asciidoc
  . Navigate to the OpenShift Console at {openshift_cluster_console_url}
  . Login with username: {openshift_cluster_admin_username}
  . Password: {openshift_cluster_admin_password}
  ```

**What UserInfo variables are for**:
- Understanding WHICH variables are available
- Learning the correct variable names
- Seeing what endpoints/tools exist in the environment
- NOT for hardcoding actual values in content

### Step 6: Handle Diagrams, Screenshots, and Code Blocks (if provided)

If you provided visual assets or code:

**For images (diagrams, screenshots)**:

**Path convention**:
- All images go in: `content/modules/ROOT/assets/images/`

**Required for every image**:
1. **Meaningful alt text** (for accessibility)
2. **Clickable link** (`link=self,window=blank` - ALWAYS required)
3. **Width guidance** (500-800px typical)
4. **Descriptive filename** (no generic names like "image1.png")

**AsciiDoc syntax** (REQUIRED):
```asciidoc
image::pipeline-execution-1.png[Tekton pipeline showing three tasks executing in sequence,link=self,window=blank,width=700,title="Pipeline Execution in Progress"]
```

**CRITICAL**: **ALWAYS** include `link=self,window=blank` to make images clickable. This allows learners to see full resolution without losing their place in the workshop.

**Optional - Center alignment**:
```asciidoc
image::architecture-diagram.png[Architecture overview,link=self,window=blank,align="center",width=800,title="System Architecture"]
```

**Placeholders**:
- If real image doesn't exist yet: Insert placeholder and add to "Assets Needed" list
- Example placeholder:
  ```asciidoc
  // TODO: Add screenshot
  image::create-task-screenshot.png[OpenShift console showing task creation form,link=self,window=blank,width=600,title="Creating a Tekton Task"]
  ```

**Assets Needed list**:
At end of module, include:
```asciidoc
== Assets Needed

. `pipeline-execution-1.png` - Screenshot of pipeline running in OpenShift console
. `task-definition.png` - YAML editor showing task definition
```

**For code blocks**:
- If you provide code snippets: Format them in AsciiDoc
- Detect language (bash, yaml, python, etc.)
- Add proper syntax highlighting:
  ```asciidoc
  [source,bash]
  ----
  oc create deployment my-app --image=myimage:latest
  ----
  ```

**Recommended image naming**:
- Architecture diagrams: `architecture-overview.png`, `deployment-flow.png`
- UI screenshots: `console-project-view.png`, `dashboard-metrics.png`
- Command outputs: `oc-get-pods-output.png`, `build-logs.png`
- Step-by-step: `step-1-create-task.png`, `step-2-run-pipeline.png`

**Clickable Images (Links)**:
If an image should be clickable and link to external content, use `^` caret to open in new tab:

```asciidoc
// Using image macro with link attribute
image::architecture-diagram.png[Architecture,600,link=https://docs.redhat.com/architecture^]

// Using link macro around image
link:https://docs.redhat.com/architecture^[image:architecture-diagram.png[Architecture,600]]
```

**Critical**: Clickable images linking to external URLs MUST use `^` caret to open in new tab, just like text links.

### Step 7: Fetch and Analyze References

Based on your references, I'll:
- Fetch URLs with WebFetch
- Read local files (supports PDF)
- Extract procedures, commands, concepts
- Identify hands-on opportunities
- Combine with AgnosticV variables (if provided)
- Integrate provided code blocks and diagrams

**Reference Enforcement**:
- Every non-trivial claim must be backed by provided references
- If not backed by reference, mark clearly: `**Reference needed**: <claim>`
- Track which reference supports which section
- If references conflict:
  - Call out the conflict
  - Choose based on version relevance
  - Note the decision in module

**Reference Tracking** (for conclusion generation):
- Track all references used across all modules
- Store reference URLs, titles, and which modules used them
- References will be consolidated in the conclusion module, NOT in individual modules
- Each module can cite sources inline (e.g., "According to the Red Hat documentation...") but the formal References section will only appear in the conclusion

**IMPORTANT: External Link Format**:
- ALL external links MUST use `^` caret to open in new tab
- Format: `link:https://example.com[Link Text^]`
- The `^` ensures users don't lose their place in the workshop
- Internal xrefs (module navigation) should NOT use `^`
- Examples:
  - External: `link:https://docs.redhat.com/...[Red Hat Documentation^]`
  - Internal: `xref:03-module-02-next.adoc[Next Module]` (no caret)

### Step 8: Read Templates and Verification Criteria (BEFORE Generating)

**CRITICAL: I MUST read all these files BEFORE generating content to ensure output meets all standards.**

**Templates to read:**
- `.claude/templates/workshop/templates/00-index-learner.adoc` - Learner-facing index template
- `.claude/templates/workshop/templates/03-module-01.adoc` - Module template
- `.claude/templates/workshop/example/00-index.adoc` - Example index (but write for LEARNERS, not facilitators)
- `.claude/templates/workshop/example/01-overview.adoc` - Example overview
- `.claude/templates/workshop/example/02-details.adoc` - Example details
- `.claude/templates/workshop/example/03-module-01.adoc` - Example module

**Verification criteria to read and apply DURING generation:**
1. `.claude/prompts/enhanced_verification_workshop.txt` - Complete quality checklist
2. `.claude/prompts/redhat_style_guide_validation.txt` - Red Hat style rules
3. `.claude/prompts/verify_workshop_structure.txt` - Structure requirements
4. `.claude/prompts/verify_technical_accuracy_workshop.txt` - Technical accuracy standards
5. `.claude/prompts/verify_accessibility_compliance_workshop.txt` - Accessibility requirements
6. `.claude/prompts/verify_content_quality.txt` - Content quality standards

**How I use these:**
- Read ALL verification prompts BEFORE generating
- Apply criteria WHILE generating content
- Generate content that ALREADY passes all checks
- No separate validation step needed - content is validated during creation

### Step 9: Generate Files (Using Verification Criteria)

**IMPORTANT: Use Reference Repository from Step 0**

Before generating ANY content, refer back to the reference repository examples from Step 0:

1. **Read reference examples again** if needed to refresh patterns
2. **Match structure and style** from real Showroom modules
3. **Apply learned patterns** to new content:
   - Section structure matches reference examples
   - Code block formatting follows reference style
   - Image references use same patterns (link=self,window=blank)
   - List formatting matches reference (blank lines before/after)
   - External links follow reference pattern (^ caret for new tabs)
   - Business scenario integration follows reference approach

**This ensures generated content matches real Showroom quality instead of generic templates.**

**CRITICAL: If this is the FIRST module of a NEW lab, generate files in this order:**

#### Step 9.1: Generate index.adoc (First Module Only)

**Purpose**: Learner-facing landing page - NOT a facilitator guide

**Content**:
```asciidoc
= {{ Workshop Title }}

Welcome to the {{ workshop name }} workshop!

== What you'll learn

In this workshop, you will:

* {{ Learning objective 1 }}
* {{ Learning objective 2 }}
* {{ Learning objective 3 }}
* {{ Learning objective 4 }}

== Who this is for

This workshop is designed for {{ target audience }} who want to {{ main goal }}.

== Prerequisites

Before starting this workshop, you should have:

* {{ Prerequisite 1 }}
* {{ Prerequisite 2 }}
* Access to {{ environment/tools }}

== Workshop environment

{{ Brief description of the lab environment }}

* OpenShift cluster: {openshift_console_url}
* Login credentials will be provided

== Let's get started!

Click on the next section to begin the workshop.
```

**What NOT to do**:
- ❌ Don't copy facilitator guide template from workshop/templates/00-index.adoc
- ❌ Don't include facilitator instructions
- ❌ Don't write "This guide helps workshop facilitators..."

**What TO do**:
- ✅ Write for LEARNERS, not facilitators
- ✅ Simple welcome and what they'll learn
- ✅ Prerequisites and environment info
- ✅ Encouragement to get started

#### Step 9.2: Generate 01-overview.adoc (First Module Only)

**Purpose**: Business scenario and learning objectives

**Content**: See workshop/example/01-overview.adoc for pattern
- Business scenario/story
- Detailed learning objectives
- Expected outcomes
- Estimated time

#### Step 9.3: Generate 02-details.adoc (First Module Only)

**Purpose**: Technical requirements and setup

**Content**: See workshop/example/02-details.adoc for pattern
- Module timing breakdown
- Technical requirements
- Environment details
- Authors/contact

#### Step 9.4: Generate 03-module-01-*.adoc (Always)

I'll create a complete module with:

**CRITICAL: Image Syntax Enforcement**:
When generating ANY image reference in the module content, you MUST include `link=self,window=blank`:

✅ **CORRECT - Always use this format**:
```asciidoc
image::filename.png[Description,link=self,window=blank,width=700]
image::pipeline-view.png[Pipeline Execution,link=self,window=blank,width=700,title="Pipeline Running"]
```

❌ **WRONG - Never generate images without link parameter**:
```asciidoc
image::filename.png[Description,width=700]
image::pipeline-view.png[Pipeline Execution,width=700]
```

**Why**: This makes images clickable to open full-size in new tab, preventing learners from losing their place in the workshop.

**CRITICAL: AsciiDoc List Formatting Enforcement**:
When generating ANY list in the module content, you MUST include blank lines before and after the list:

✅ **CORRECT - Always use proper spacing**:
```asciidoc
**Learning objectives:**

* Understand how Tekton tasks work
* Create and execute pipelines
* Troubleshoot failed runs

By the end of this module...
```

❌ **WRONG - Text runs together when rendered**:
```asciidoc
**Learning objectives:**
* Understand how Tekton tasks work
* Create and execute pipelines
* Troubleshoot failed runs
By the end of this module...
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
All external links MUST use `^` caret to open in new tab, preventing learners from losing their place.

✅ **CORRECT - External links with caret**:
```asciidoc
According to link:https://docs.redhat.com/...[Red Hat Documentation^], OpenShift provides...
See the link:https://www.redhat.com/guides[Getting Started Guide^] for more details.
```

❌ **WRONG - Missing caret**:
```asciidoc
According to link:https://docs.redhat.com/...[Red Hat Documentation], OpenShift provides...
See the link:https://www.redhat.com/guides[Getting Started Guide] for more details.
```

**Internal links (NO caret)**:
```asciidoc
✅ CORRECT - Internal navigation without caret:
Navigate to xref:04-module-02.adoc[Next Module] to continue.
See xref:02-details.adoc#prerequisites[Prerequisites] section.
```

**Why**: External links without caret replace current tab, causing learners to lose their place in the workshop. Internal xrefs should NOT use caret to keep flow within the workshop.

**CRITICAL: Bullets vs Numbers - Knowledge vs Tasks**:
Knowledge/information sections use bullets (*). Task/step sections use numbers (.).

✅ **CORRECT - Bullets for knowledge, numbers for tasks**:
```asciidoc
== Learning Objectives

By the end of this module, you will understand:

* How Tekton tasks encapsulate CI/CD steps
* The relationship between tasks and pipelines
* Best practices for pipeline design

== Exercise 1: Create Your First Pipeline

Follow these steps:

. Open the OpenShift Console at {openshift_console_url}
. Navigate to Pipelines → Create Pipeline
. Enter the pipeline name: my-first-pipeline
. Add a task from the catalog
. Click Create

=== Verify

Check that your pipeline was created successfully:

* Pipeline appears in the list
* Status shows "Not started"
* All tasks are configured correctly
```

❌ **WRONG - Mixed up bullets and numbers**:
```asciidoc
== Exercise 1: Create Your First Pipeline

Follow these steps:

* Open the OpenShift Console  ← WRONG (should be numbers)
* Navigate to Pipelines
* Click Create

=== Verify

. Pipeline appears in the list  ← WRONG (should be bullets)
. Status shows "Not started"
```

**Rule**:
- Learning objectives → Use bullets (*) for concepts to understand
- Exercise steps → Use numbers (.) for sequential actions
- Verification → Use bullets (*) for success indicators
- Prerequisites → Use bullets (*) for requirements list
- Benefits/features → Use bullets (*) for information points

**Why**: Bullets indicate information to absorb; numbers indicate sequential actions to perform.

**Required Structure**:
- Learning objectives (3-4 items)
- Business introduction with scenario
- 2-3 progressive exercises
- Step-by-step instructions with commands
- **Verification checkpoints** (REQUIRED - see below)
- Image placeholders
- **Troubleshooting section** (OPTIONAL - if user requested in Step 3, see below)
- **Learning outcomes checkpoint** (REQUIRED - see below)
- Module summary

**Note**: References are NOT included in individual modules. All references will be consolidated in the mandatory conclusion module.

**Mandatory: Verification Checkpoints**:
Each major step must include:
```asciidoc
=== Verify

Run the following to confirm success:

[source,bash]
----
oc get pods
----

Expected output:
----
NAME                     READY   STATUS    RESTARTS   AGE
my-app-xxxxx-xxxxx      1/1     Running   0          2m
----

✓ Pod status is "Running"
✓ READY shows 1/1
```

**Optional: Troubleshooting Section (If Requested)**:
If the user requested troubleshooting in Step 3, include this section:
```asciidoc
== Troubleshooting

**Issue**: Pod stuck in "ImagePullBackOff"
**Solution**:
. Check image name: `oc describe pod <pod-name>`
. Verify registry credentials
. Common fix: `oc set image-lookup <deployment>`

**Issue**: Permission denied errors
**Solution**:
. Verify you're in correct project: `oc project`
. Check RBAC: `oc whoami` and `oc auth can-i create pods`

**Issue**: Command not found
**Solution**:
. Verify OpenShift CLI installed: `oc version`
. Expected version: {ocp_version}
```

**Guidelines for troubleshooting section**:
- Include 3-5 common issues specific to the module's technology
- Provide clear, actionable solutions
- Use real commands and expected outputs
- Tailor scenarios to the module's exercises
- If user declined troubleshooting, skip this section entirely

**Mandatory: Learning Outcomes Checkpoint**:
Every module must include a learning confirmation (not just technical validation):
```asciidoc
== Learning Outcomes

By completing this module, you should now understand:

* ✓ How Tekton tasks encapsulate reusable CI/CD steps
* ✓ The relationship between tasks, pipelines, and pipeline runs
* ✓ How to troubleshoot failed pipeline executions using logs and status
* ✓ When to use sequential vs parallel task execution patterns
```

**Guidelines**:
- 3-5 bullet outcomes tied to original learning objective
- Focus on understanding ("understand how X works") not just doing ("created X")
- Use outcomes later for blog transformation
- Helps reviewers, instructors, and people skimming modules

**Optional but Recommended: Cleanup**:
If module changes shared state:
```asciidoc
== Cleanup (Optional)

To reset your environment:

[source,bash]
----
oc delete project my-project
----
```

**Quality**:
- Valid AsciiDoc syntax
- Proper Red Hat product names
- Sentence case headlines
- Second-person narrative
- Code blocks with syntax highlighting

### Step 10: Final Quality Check

**Since verification criteria were applied during generation (Step 7-8), the module should already meet all standards.**

**Quick final checks:**

1. **AsciiDoc Syntax**:
   - ✓ All code blocks have proper syntax: `[source,bash]`
   - ✓ No broken includes
   - ✓ All attributes defined
   - ✓ External links use `^` caret to open in new tab

2. **Completeness**:
   - ✓ All required sections present (see Step 8)
   - ✓ Verification checkpoints after major steps
   - ✓ Troubleshooting section with 3+ scenarios (if user requested)
   - ✓ Learning outcomes section
   - ✓ No References section in module (references go in conclusion)

3. **Navigation**:
   - ✓ nav.adoc will be updated in Step 10

**Note:** Content was generated using verification prompts from Step 8 AND reference repository examples from Step 0, so it should already comply with:
- Red Hat style guide
- Workshop structure standards
- Technical accuracy requirements
- Accessibility standards
- Content quality standards

### Step 11: Update Navigation (REQUIRED)

I'll automatically update `content/modules/ROOT/nav.adoc` - this is REQUIRED for the module to appear in the Showroom sidebar.

**Navigation Rules**:
1. **Read existing nav.adoc first** - don't overwrite existing entries
2. **Keep index.adoc at top** if it exists
3. **Maintain sequential ordering** of modules
4. **Add new module in correct position** based on module number

**What I'll add**:
```asciidoc
* xref:index.adoc[Home]

* xref:03-module-01-intro.adoc[Module 1: Introduction]
** xref:03-module-01-intro.adoc#exercise-1[Exercise 1: Setup]
** xref:03-module-01-intro.adoc#exercise-2[Exercise 2: First Pipeline]

* xref:04-module-02-advanced.adoc[Module 2: Advanced Topics]  ← NEW MODULE
** xref:04-module-02-advanced.adoc#exercise-1[Exercise 1: Git Integration]
** xref:04-module-02-advanced.adoc#exercise-2[Exercise 2: Triggers]
```

**Conflict handling**:
- If module number conflicts with existing file, warn user
- Suggest next available number
- Do NOT overwrite without confirmation

**Note**: Without this nav.adoc entry, your module won't be accessible in Showroom!

### Step 12: Deliver

**CRITICAL: Manage Output Tokens to Prevent Overflow**

**Token Management Rules**:
1. **Write files using Write tool** - Don't output full file contents to user
2. **Show brief confirmations only** - "✅ Created: file.adoc (X lines)"
3. **Provide summary at end** - List what was created, not the full content
4. **Never output entire module content** - Files are already written
5. **Keep total output under 5000 tokens** - Brief summaries only

**Output Format for FIRST module**:

```
✅ Workshop Generation Complete

**Files Created**:
- content/modules/ROOT/pages/index.adoc (32 lines) - Learner landing page
- content/modules/ROOT/pages/01-overview.adoc (85 lines) - Business scenario
- content/modules/ROOT/pages/02-details.adoc (67 lines) - Technical details
- content/modules/ROOT/pages/03-module-01-intro.adoc (234 lines) - First hands-on module
- content/modules/ROOT/nav.adoc (updated)
```

**Output Format for CONTINUATION modules**:

```
✅ Module Generation Complete

**Files Created**:
- content/modules/ROOT/pages/04-module-02-advanced.adoc (198 lines)
- content/modules/ROOT/nav.adoc (updated)

**Module Structure**:
- Learning objectives: 4 items
- Exercises: 3
- Verification checkpoints: 3
- Troubleshooting scenarios: 5 (if included)
- Learning outcomes: 4 items

**Assets**:
- Images needed: 2 placeholders (see module for TODO comments)
- Dynamic attributes used: {openshift_console_url}, {user}, {password}

**Next Steps**:
1. Review module: content/modules/ROOT/pages/04-module-02-advanced.adoc
2. Capture screenshots for placeholder images
3. Test commands in your environment
4. Run: verify-content to check quality
5. Create next module: create-lab (continuing existing lab)

**Note**: All files have been written. Use your editor to review them.
```

**What NOT to do**:
- ❌ Don't show full module content in response
- ❌ Don't output the entire file you just created
- ❌ Don't paste hundreds of lines of generated AsciiDoc
- ❌ Don't include long example sections in output

**What TO do**:
- ✅ Write files using Write tool
- ✅ Show brief "Created: filename (X lines)" confirmations
- ✅ Provide structured summary
- ✅ Give clear next steps
- ✅ Keep output concise (under 5000 tokens)

### Step 13: Generate Conclusion Module (MANDATORY)

**After delivering the final module, ask if this is the last module:**

```
Q: Is this the last module of your workshop?

If YES, I will now generate the mandatory conclusion module that includes:
- Summary of what learners accomplished
- Key takeaways from all modules
- ALL REFERENCES used across the entire workshop
- Next steps and resources
- Related workshops and certification paths

If NO, you can continue creating more modules, and I'll generate the conclusion when you're done.

Is this your last module? [Yes/No]
```

**If user answers YES (this is the last module)**:

1. Read ALL previous modules to extract:
   - All learning outcomes from each module
   - All references cited in each module
   - Key concepts and skills taught
   - Technologies and products covered

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

   I found these references used across your modules:
   1. https://docs.openshift.com/container-platform/4.18/... [OpenShift Documentation] - Used in: Modules 1, 3
   2. https://tekton.dev/docs/pipelines/ [Tekton Pipelines] - Used in: Module 2
   3. https://developers.redhat.com/... [Developer Guide] - Used in: Module 1
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
   https://docs.redhat.com/... - OpenShift documentation
   https://developers.redhat.com/... - Developer guides

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

3. Detect highest module number (e.g., if last module is 07-module-05, conclusion will be 08-conclusion.adoc)

4. Generate conclusion module using the embedded template below

5. Customize the template by:
   - Extracting all learning outcomes from previous modules
   - Listing 3-5 key takeaways from the workshop
   - **Using the curated reference list from step 2** (REQUIRED)
   - Providing next steps (related workshops, docs, practice projects)

6. Update nav.adoc with conclusion entry at the end

7. Provide brief confirmation

**If user answers NO (more modules to come)**:
- Note that conclusion will be generated after the last module
- User can invoke /create-lab again to add more modules
- When adding the final module, this question will be asked again

**Embedded Conclusion Template**:
```asciidoc
= Conclusion and Next Steps

Congratulations! You've completed the {{ workshop_name }} workshop.

== What You've Learned

Throughout this workshop, you've gained hands-on experience with:

* ✅ {{ learning_outcome_1 }}
* ✅ {{ learning_outcome_2 }}
* ✅ {{ learning_outcome_3 }}
* ✅ {{ learning_outcome_4 }}

You now have the skills to {{ primary_capability }}.

== Key Takeaways

The most important concepts to remember:

. **{{ key_concept_1 }}**: {{ brief_explanation_1 }}
. **{{ key_concept_2 }}**: {{ brief_explanation_2 }}
. **{{ key_concept_3 }}**: {{ brief_explanation_3 }}

== Next Steps

Ready to continue your journey? Here are some recommended next steps:

=== Recommended Workshops

Explore related workshops to expand your skills:

* link:{{ related_workshop_1_url }}[{{ related_workshop_1_name }}^] - {{ related_workshop_1_description }}
* link:{{ related_workshop_2_url }}[{{ related_workshop_2_name }}^] - {{ related_workshop_2_description }}

=== Documentation and Resources

Deepen your knowledge with these resources:

* link:{{ docs_url_1 }}[{{ product_name }} Official Documentation^]
* link:{{ docs_url_2 }}[{{ feature_name }} Guide^]
* link:{{ community_url }}[{{ product_name }} Community^]

=== Practice Projects

Put your new skills to work:

. **{{ project_idea_1 }}**: {{ project_description_1 }}
. **{{ project_idea_2 }}**: {{ project_description_2 }}
. **{{ project_idea_3 }}**: {{ project_description_3 }}

== References

**CRITICAL**: This section consolidates ALL references used across the entire workshop.

Read all previous modules and extract every reference cited, then organize them by category:

=== Official Documentation

* link:{{ docs_url_1 }}[{{ product_name }} Documentation^] - Used in: Modules {{ modules_list }}
* link:{{ docs_url_2 }}[{{ feature_name }} Guide^] - Used in: Modules {{ modules_list }}

=== Red Hat Resources

* link:{{ redhat_resource_1 }}[{{ resource_title_1 }}^] - Used in: Module {{ module_number }}
* link:{{ redhat_resource_2 }}[{{ resource_title_2 }}^] - Used in: Module {{ module_number }}

=== Community and Open Source

* link:{{ community_url_1 }}[{{ community_resource_1 }}^] - Used in: Module {{ module_number }}
* link:{{ community_url_2 }}[{{ community_resource_2 }}^] - Used in: Module {{ module_number }}

=== Additional Reading

* link:{{ additional_url_1 }}[{{ additional_title_1 }}^] - Background information
* link:{{ additional_url_2 }}[{{ additional_title_2 }}^] - Advanced topics

**Guidelines for References section**:
- Group references by category (Official Docs, Red Hat Resources, Community, etc.)
- Include which module(s) used each reference
- ALL external links must use `^` caret to open in new tab
- Provide brief context for each reference (what it covers)
- Ensure ALL references from ALL modules are included

== Share Your Feedback

Help us improve this workshop:

* What did you find most valuable?
* What could be improved?
* What topics would you like to see covered in future workshops?

Contact us: {{ feedback_contact }}

== Thank You!

Thank you for participating in this workshop. We hope you found it valuable and informative.

Keep building, keep learning! 🚀

---

**Workshop**: {{ workshop_name }} +
**Completed**: {localdate} +
**Platform**: Red Hat Showroom
```

**Conclusion Module Naming**:
- File: `0X-conclusion.adoc` (sequential number, e.g., 08-conclusion.adoc)
- Title: `= Conclusion and Next Steps`
- Nav entry: `* xref:0X-conclusion.adoc[Conclusion and Next Steps]`

**Content to Include** (ALL REQUIRED):
- ✅ "What You've Learned" - Extract from all module learning outcomes
- ✅ "Key Takeaways" - 3-5 most important concepts
- ✅ "Next Steps" - Related workshops, documentation, practice projects
- ✅ **"References"** - Consolidate ALL references from ALL modules (MANDATORY)
- ✅ "Share Your Feedback" - Feedback prompts
- ✅ "Thank You" - Closing message

**CRITICAL**: The References section MUST include every reference used across all modules, organized by category.

## Example Usage

### Example 1: Create First Module with Overall Story Planning

```
User: Create a lab about OpenShift Pipelines for developers

Skill: Great! Since this is a new lab, let me gather the overall story first.

**Overall Lab Planning:**

Q: Is this the first module or continuing existing lab?
A: First module of a new lab

Q: What's the overall goal of this lab?
A: "Teach developers how to build and deploy cloud-native CI/CD pipelines using OpenShift Pipelines"

Q: Target audience?
A: Intermediate developers familiar with containers and Kubernetes

Q: What should learners know by the end?
A: - Create Tekton tasks and pipelines
   - Integrate with Git repositories
   - Deploy applications via automated pipelines
   - Troubleshoot pipeline failures

Q: Company/business scenario?
A: "DevOps Corp" - A company struggling with slow, manual deployment processes

Q: Estimated total duration?
A: 90 minutes

**Recommended Module Flow:**

Based on your goals, I recommend 3 modules:

Module 1: Pipeline Fundamentals (30 min)
- Introduce Tekton concepts
- Create first task
- Run simple pipeline
- Story: DevOps Corp's current manual deployment pain

Module 2: Git Integration & Automation (30 min)
- Connect pipelines to Git
- Trigger on commits
- Build from source
- Story: Enabling developer self-service

Module 3: Production Pipelines (30 min)
- Multi-stage pipelines (dev, test, prod)
- Pipeline parameters and workspaces
- Monitoring and troubleshooting
- Story: Full automation, reduced deployment time

Does this flow work for you, or would you like adjustments?

User: Perfect! Let's start with Module 1.

Skill: Excellent! Now let me gather details for Module 1...

Q1: Module file name? → "03-pipelines-intro.adoc"
Q2: Reference materials? → https://docs.openshift.com/pipelines/1.12/
Q3: Learning objective? → "Create and execute your first Tekton pipeline"
Q4: Business scenario? → "DevOps Corp" (using overall story)
Q5: Technology? → "OpenShift Pipelines / Tekton"
Q6: Exercise count? → 3
Q7: Diagrams/code? → No, not yet

[Generates Module 1 with DevOps Corp story]
[Sets up story arc for modules 2 and 3]

✓ Created: content/modules/ROOT/pages/03-pipelines-intro.adoc
✓ Story established: DevOps Corp's deployment transformation
✓ Module flow documented for next modules
✓ Ready for Module 2 (will auto-continue story)
```

### Example 2: Continue Existing Lab (Auto-Detect Story)

```
User: Create Module 2 for the OpenShift Pipelines lab

Skill: Let me check if this continues an existing lab...

Q: Is this first module or continuing?
A: Continuing existing lab

Q: Path to previous module?
A: content/modules/ROOT/pages/03-pipelines-intro.adoc

[Reads previous module]
→ Detected story: "DevOps Corp deployment transformation"
→ Detected company: "DevOps Corp"
→ Detected progression: Module 1 covered fundamentals
→ Next logical step: Git integration

I'll continue the DevOps Corp story. Now for Module 2 details...

Q1: Module file name? → "04-pipelines-git.adoc"
Q2: Reference materials? → https://docs.openshift.com/pipelines/.../triggers
Q4: Learning objective? → "Automate pipeline execution via Git webhooks"
Q5: Technology? → "OpenShift Pipelines / Tekton Triggers"
Q6: Exercise count? → 3
Q7: Diagrams/code? → No

[Generates Module 2]
- Continues DevOps Corp narrative
- References accomplishments from Module 1
- Builds toward Module 3's production pipeline

✓ Created: content/modules/ROOT/pages/04-pipelines-git.adoc
✓ Story continuity maintained from Module 1
✓ Ready for Module 3 (final module in recommended flow)
```

### Example 3: Create Module from Red Hat Docs

```
User: Create Module 1 for OpenShift Pipelines using:
      https://docs.openshift.com/pipelines/1.12/

Skill: I'll create that module. Let me ask a few questions...
       [asks if first module or continuing]
       [if first: asks overall story questions]
       [asks module-specific questions]
       [generates module with scenario]
       [validates with agents]

✓ Created: content/modules/ROOT/pages/03-pipelines-intro.adoc
✓ 3 exercises: Create task, Define pipeline, Run pipeline
✓ Screenshot guide provided
✓ Ready to add to nav.adoc
```

### Example 2: Create Module with Diagrams and Code Blocks

```
User: Create Module 1 for container security. I have an architecture diagram
      and some example Dockerfiles.

Skill: Great! Let me ask some questions...

Q1: Module file name? → "03-security-intro.adoc"
Q2: Reference materials? → https://docs.redhat.com/en/documentation/...
Q3: Learning objective? → "Implement container security best practices"
Q4: Business scenario? → ACME Corp
Q5: Technology? → "Container security, Podman, OpenShift"
Q6: Exercise count? → 3
Q7: Diagrams/screenshots/code? → Yes, I have:
    - Architecture diagram: ~/diagrams/security-architecture.png
    - Code: Secure Dockerfile examples (paste below)

User provides:
```dockerfile
FROM registry.redhat.io/ubi9/ubi-minimal:latest
USER 1001
WORKDIR /app
COPY --chown=1001:0 app.jar .
RUN chmod 440 app.jar
CMD ["java", "-jar", "app.jar"]
```

Skill: Perfect! Processing...

[Copies diagram to assets/images/]
→ Saved: content/modules/ROOT/assets/images/security-architecture.png

[Formats code blocks with syntax highlighting]
→ Integrated Dockerfile examples in exercises

[Generates module with:]
- Architecture diagram referenced:
  image::security-architecture.png[Container Security Architecture,link=self,window=blank,align="center",width=800,title="Container Security Architecture"]

- Code blocks formatted:
  [source,dockerfile]
  ----
  FROM registry.redhat.io/ubi9/ubi-minimal:latest
  USER 1001
  ...
  ----

- Exercise flow integrates the diagram and code naturally

✓ Created: content/modules/ROOT/pages/03-security-intro.adoc
✓ Diagram saved and referenced: security-architecture.png
✓ Code blocks integrated with syntax highlighting
✓ Screenshot guide for additional captures needed
```

## Tips for Best Results

- **Specific objectives**: "Build and deploy container with persistent storage" vs "Learn containers"
- **Multiple references**: More context = better content
- **Continue scenarios**: Reference previous module for narrative continuity
- **Test commands**: Always verify in real environment

## Quality Standards

Every module will have:
- ✓ Valid AsciiDoc syntax
- ✓ 3-4 clear learning objectives
- ✓ Business context introduction
- ✓ Progressive exercises (foundational → advanced)
- ✓ Verification steps
- ✓ Module summary
- ✓ Image placeholders
- ✓ External links with `^` to open in new tab
- ✓ Red Hat style compliance
