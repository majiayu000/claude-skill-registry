---
name: prd-update-progress
description: Update PRD progress based on git commits and code changes, enhanced by conversation context
category: project-management
---

# PRD Update Progress Slash Command

## Instructions

You are helping update an existing Product Requirements Document (PRD) based on implementation work completed. This command analyzes git commits and code changes, enhanced by conversation context, to track PRD completion progress and propose evidence-based updates.

## Process Overview

1. **Identify Target PRD** - Determine which PRD to update
2. **Context-First Progress Analysis** - Use conversation context first, Git analysis as fallback
3. **Map Changes to PRD Items** - Intelligently connect work to requirements
4. **Propose Updates** - Suggest checkbox completions and requirement changes
5. **User Confirmation** - Verify proposals and handle edge cases
6. **Update PRD** - Apply changes to checkboxes and status
7. **Flag Divergences** - Alert when actual work differs from planned work
8. **Commit Progress Updates** - Preserve progress checkpoint
9. **Continue to Next Task** - Prompt user to run /prd-next

## Step 1: Smart PRD Identification

**Automatically detect target PRD using conversation context:**

1. **Current Work Context**: Look for recent conversation about specific PRD work, features, or issues
2. **Git Branch Analysis**: Check current git branch for PRD indicators (feature/prd-*, issue numbers)
3. **Recent File Activity**: Identify recently modified PRD files in `prds/` directory
4. **Todo List Context**: Check if TodoWrite tool shows PRD-specific tasks in progress

**Detection Priority Order:**
- If conversation explicitly mentions "PRD #X" or specific PRD file → Use that PRD
- If git branch contains PRD reference (e.g., "feature/prd-12-*") → Use PRD #12  
- If TodoWrite shows PRD-specific tasks → Use that PRD context
- If only one PRD file recently modified → Use that PRD
- If multiple PRDs possible → Ask user to clarify

## Step 2: Context-First Progress Analysis

**PRIORITY: Use conversation context first before Git analysis**

### Conversation Context Analysis (FAST - Use First)
**If recent conversation shows clear work completion:**
- **Recently discussed implementations**: "Just completed X", "Implemented Y", "Built Z"
- **Todo list context**: Check TodoWrite tool for completed/in-progress items
- **File creation mentions**: "Created file X", "Added Y functionality"
- **Test completion references**: "Tests passing", "All X tests complete"
- **User confirmations**: "That works", "Implementation complete", "Ready for next step"

**Use conversation context when available - it's faster and more accurate than Git parsing**

### Git Change Analysis (FALLBACK - Use Only If Context Unclear)

**Only use git tools when conversation context is insufficient:**

### Commit Analysis
```bash
# Get recent commits (last 10-20 commits)
git log --oneline -n 20

# Get detailed changes since last PRD update
git log --since="1 week ago" --pretty=format:"%h %an %ad %s" --date=short
```

### File Change Analysis
```bash
# See what files were modified recently
git diff --name-status HEAD~10..HEAD

# Get specific changes in key directories
git diff --stat HEAD~10..HEAD
```

### Change Categorization
Identify different types of changes:
- **New files**: Indicates new functionality or components
- **Modified files**: Shows updates to existing functionality
- **Test files**: Evidence of testing implementation
- **Documentation files**: Shows documentation updates
- **Configuration files**: Indicates setup or deployment changes

## Step 3: Comprehensive PRD Structure Analysis

### **CRITICAL**: Systematic Checkbox Scanning
**MUST perform this step to avoid missing requirements:**

1. **Scan ALL unchecked items** in the PRD using grep or search
2. **Categorize each unchecked requirement** by type:
   - **Implementation** (code, features, technical tasks)
   - **Documentation** (guides, examples, cross-references)
   - **Validation** (testing examples work, user journeys)
   - **User Acceptance** (real-world usage, cross-client testing)
   - **Launch Activities** (training, deployment, rollout)
   - **Success Metrics** (adoption, analytics, support impact)

3. **Map git changes to appropriate categories only**
4. **Be conservative** - only mark items complete with direct evidence

### Evidence-Based Completion Criteria

**Implementation Requirements** - Mark complete when:
- **Code files**: Show functionality is implemented
- **Test files**: Demonstrate comprehensive testing
- **Integration**: Components properly connected

**Documentation Requirements** - Mark complete when:
- **Files created**: Documentation files exist
- **Examples validated**: Commands/examples have been tested
- **Cross-references work**: Internal links verified

**Validation Requirements** - Mark complete when:
- **Manual testing done**: Workflows tested end-to-end
- **Examples verified**: All documented examples work
- **User journeys confirmed**: Complete workflows validated

**Launch Activities** - Mark complete when:
- **Training delivered**: Team has been trained
- **Deployment done**: Feature is live and accessible
- **Rollout complete**: Users are actively using the feature

### Conservative Completion Policy
**DO NOT mark complete unless there is direct evidence:**
- ❌ Don't assume documentation is "good enough" without validation
- ❌ Don't mark testing complete without evidence of actual testing
- ❌ Don't mark launch items complete without proof of rollout
- ❌ Don't mark success criteria complete without metrics

### Gap Analysis
Systematically identify:
- **Requirements without evidence** (what still needs work)
- **Evidence without requirements** (work done outside scope)
- **Missing validation** (implemented but not tested)
- **Missing rollout** (ready but not deployed/adopted)

## Step 4: Comprehensive Progress Report

### **REQUIRED**: Complete Status Analysis
Present a comprehensive breakdown:

```markdown
## PRD Progress Analysis: [PRD Name]

### ✅ COMPLETED (with evidence):
**Implementation** (X/Y items):
- [x] Item name - Evidence: specific files/changes
- [x] Item name - Evidence: specific files/changes

**Documentation** (X/Y items):
- [x] Item name - Evidence: docs created, examples tested
- [x] Item name - Evidence: cross-references verified

### ⏳ REMAINING WORK:
**Validation** (X items unchecked):
- [ ] Item name - Reason: needs manual testing/validation
- [ ] Item name - Reason: examples not tested

**User Acceptance** (X items unchecked):
- [ ] Item name - Reason: no cross-client testing done
- [ ] Item name - Reason: no user feedback collected

**Launch Activities** (X items unchecked):
- [ ] Item name - Reason: team not trained
- [ ] Item name - Reason: not deployed to production

**Success Metrics** (X items unchecked):
- [ ] Item name - Reason: no usage data available
- [ ] Item name - Reason: adoption not measured

### 🎯 COMPLETION STATUS:
- **Overall Progress**: X% complete (Y of Z total items)
- **Implementation Phase**: 100% complete ✅
- **Validation Phase**: X% complete (what's missing)
- **Launch Phase**: X% complete (what's missing)
```

### Conservative Recommendation Policy
**ONLY suggest marking items complete when you have direct evidence.**
**CLEARLY list what still needs to be done.**
**DO NOT claim "everything is done" unless ALL items are truly complete.**

## Step 5: Implementation vs Plan Analysis

### Divergence Detection
Flag when actual implementation differs from planned approach:
- **Architecture changes**: Different technical approach than originally planned
- **Scope changes**: Features added or removed during implementation
- **Requirement evolution**: User needs that became clearer during development
- **Technical discoveries**: Constraints or opportunities discovered during coding

### Update Recommendations
Suggest PRD updates when divergences are found:
- **Decision log updates**: Record why implementation approach changed
- **Requirement modifications**: Update requirements to match actual functionality
- **Architecture updates**: Revise technical approach documentation
- **Scope adjustments**: Move items between phases or update feature definitions

## Step 6: User Confirmation Process

Present proposed changes clearly with complete transparency:

1. **Evidence summary**: Show what work was detected
2. **Proposed completions**: List specific checkbox items to mark done with evidence
3. **Remaining work analysis**: Clearly show what's still unchecked and why
4. **Divergence alerts**: Highlight any plan vs reality differences
5. **Honest progress assessment**: Give realistic completion percentage

**Critical Requirements:**
- **Never claim "everything is done"** unless literally ALL checkboxes are complete
- **Be explicit about limitations** of git-based analysis
- **Acknowledge validation gaps** when you can't verify functionality works
- **Separate implementation from validation/rollout**

Wait for user confirmation before making changes, and handle:
- **Partial acceptance**: User agrees with some but not all suggestions
- **Additional context**: User provides information not visible in git history
- **Scope clarification**: User explains work that appears to be out of scope
- **Future planning**: User wants to adjust upcoming work based on current progress

## Step 7: Systematic Update Application

When applying updates:
1. **Update only confirmed items** - Don't make assumptions
2. **Update status sections** to reflect current phase
3. **Preserve unchecked items** that still need work
4. **Update completion percentages** realistically

## Step 7.5: Code Example Validation

When updating PRDs based on implementation progress:

**CRITICAL**: Always check if code examples in PRD match current implementation

### Example Impact Detection
1. **Interface Changes**: Function signatures, parameter types, return formats
2. **API Evolution**: Method names, class structures, data models
3. **Workflow Updates**: User interaction patterns, step sequences
4. **Integration Changes**: How components connect and communicate

### Code Example Update Process
1. **Scan PRD**: Identify all code snippets and examples
2. **Cross-reference Implementation**: Compare examples with actual code
3. **Mark Outdated**: Flag examples that no longer match
4. **Priority Assessment**: Determine which examples need immediate updates
5. **Update Examples**: Revise code snippets to match current implementation
6. **Validate Examples**: Test updated examples to ensure they work

### Example Categories to Check
- **Function calls**: Parameter order, types, names
- **Interface definitions**: TypeScript interfaces, class structures
- **API responses**: Data formats, field names, response structures  
- **Workflow steps**: User interaction sequences, tool usage patterns
- **Configuration**: Setup examples, environment variables, config files

### When to Update Examples
- **Immediately**: When interface changes break existing examples
- **Before completion**: When marking implementation milestones complete
- **During reviews**: When validating PRD accuracy
- **User feedback**: When someone reports examples don't work

## Step 8: Commit Progress Updates

After successfully updating the PRD, commit all changes to preserve the progress checkpoint:

### Commit Implementation Work
```bash
# MANDATORY: Stage ALL files - implementation work AND PRD updates together
# DO NOT selectively add only PRD files - commit everything as one atomic unit
git add .

# Verify what will be committed
git status

# Create comprehensive commit with PRD reference
git commit -m "feat(prd-X): implement [brief description of completed work]

- [Brief list of key implementation achievements]
- Updated PRD checkboxes for completed items

Progress: X% complete - [next major milestone]"
```

### Commit Message Guidelines
- **Reference PRD number**: Always include `prd-X` in commit message
- **Descriptive summary**: Brief but clear description of what was implemented
- **Progress indication**: Include completion status and next steps
- **Evidence-based**: Only commit when there's actual implementation progress

**Note**: Do NOT push commits unless explicitly requested by the user. Commits preserve local progress checkpoints without affecting remote branches.

## Step 9: Next Steps Based on PRD Status

After completing the PRD update and committing changes, guide the user based on completion status:

### If PRD has remaining tasks

---

**PRD progress updated and committed.**

To continue working on this PRD:
1. Clear/reset the conversation context
2. Run `/prd-next` to get the next task

---

### If PRD is 100% complete

---

**PRD #X is complete!**

To finalize:
1. Clear/reset the conversation context
2. Run `/prd-done` to move the PRD to the done folder and close the GitHub issue

---
