---
name: prd-create
description: Create documentation-first PRDs that guide development through user-facing content
category: project-management
---

# PRD Creation Slash Command

## Instructions

You are helping create a Product Requirements Document (PRD) for a new feature. This process involves two main components:

1. **GitHub Issue**: Short, immutable concept description that links to the detailed PRD
2. **PRD File**: Project management document with milestone tracking, progress logs, and implementation plan

## Process

### Step 1: Understand the Feature Concept
Ask the user to describe the feature idea to understand the core concept and scope.

### Step 2: Create GitHub Issue FIRST
Create the GitHub issue immediately to get the issue ID. This ID is required for proper PRD file naming.

**IMPORTANT: Add the "PRD" label to the issue for discoverability.**

### Step 3: Create PRD File with Correct Naming
Create the PRD file using the actual GitHub issue ID: `prds/[issue-id]-[feature-name].md`

### Step 4: Update GitHub Issue with PRD Link
Add the PRD file link to the GitHub issue description now that the filename is known.

### Step 5: Create PRD as a Project Management Document
Work through the PRD template focusing on project management, milestone tracking, and implementation planning. Documentation updates should be included as part of the implementation milestones.

**Key Principle**: Focus on 5-10 major milestones rather than exhaustive task lists. Each milestone should represent meaningful progress that can be clearly validated.

**Consider Including** (when applicable to the project/feature):
- **Tests** - If the project has tests, include a milestone for test coverage of new functionality
- **Documentation** - If the feature is user-facing, include a milestone for docs following existing project patterns

**Good Milestones Examples:**
- [ ] Core functionality implemented and working
- [ ] Tests passing for new functionality (if project has test suite)
- [ ] Documentation complete following existing patterns (if user-facing feature)
- [ ] Integration with existing systems working
- [ ] Feature ready for user testing

**Avoid Micro-Tasks:**
- ❌ Update README.md file
- ❌ Write test for function X
- ❌ Fix typo in documentation
- ❌ Individual file modifications

**Milestone Characteristics:**
- **Meaningful**: Represents significant progress toward completion
- **Testable**: Clear success criteria that can be validated
- **User-focused**: Relates to user value or feature capability
- **Manageable**: Can be completed in reasonable timeframe

## GitHub Issue Template (Keep Short & Stable)

**Initial Issue Creation (without PRD link):**
```markdown
## PRD: [Feature Name]

**Problem**: [1-2 sentence problem description]

**Solution**: [1-2 sentence solution overview]

**Detailed PRD**: Will be added after PRD file creation

**Priority**: [High/Medium/Low]
```

**Don't forget to add the "PRD" label to the issue after creation.**

**Issue Update (after PRD file created):**
```markdown
## PRD: [Feature Name]

**Problem**: [1-2 sentence problem description]

**Solution**: [1-2 sentence solution overview]

**Detailed PRD**: See [prds/[actual-issue-id]-[feature-name].md](https://github.com/vfarcic/dot-ai/blob/main/prds/[actual-issue-id]-[feature-name].md)

**Priority**: [High/Medium/Low]
```

## Discussion Guidelines

### PRD Planning Questions
1. **Problem Understanding**: "What specific problem does this feature solve for users?"
2. **User Impact**: "Walk me through the complete user journey — what will change for them?"
3. **Technical Scope**: "What are the core technical changes required?"
4. **Documentation Impact**: "Which existing docs need updates? What new docs are needed?"
5. **Integration Points**: "How does this feature integrate with existing systems?"
6. **Success Criteria**: "How will we know this feature is working well?"
7. **Implementation Phases**: "How can we deliver value incrementally?"
8. **Risk Assessment**: "What are the main risks and how do we mitigate them?"
9. **Dependencies**: "What other systems or features does this depend on?"
10. **Validation Strategy**: "How will we test and validate the implementation?"

### Discussion Tips:
- **Clarify ambiguity**: If something isn't clear, ask follow-up questions until you understand
- **Challenge assumptions**: Help the user think through edge cases, alternatives, and unintended consequences
- **Prioritize ruthlessly**: Help distinguish between must-have and nice-to-have based on user impact
- **Think about users**: Always bring the conversation back to user value, experience, and outcomes
- **Consider feasibility**: While not diving into implementation details, ensure scope is realistic
- **Focus on major milestones**: Create 5-10 meaningful milestones rather than exhaustive micro-tasks
- **Think cross-functionally**: Consider impact on different teams, systems, and stakeholders

**Note**: If any `gh` command fails with "command not found", inform the user that GitHub CLI is required and provide the installation link: https://cli.github.com/

## Workflow

1. **Concept Discussion**: Get the basic idea and validate the need
2. **Create GitHub Issue FIRST**: Short, stable concept description to get issue ID
3. **Create PRD File**: Detailed document using actual issue ID: `prds/[issue-id]-[feature-name].md`
4. **Update GitHub Issue**: Add link to PRD file now that filename is known
5. **Section-by-Section Discussion**: Work through each template section systematically
6. **Milestone Definition**: Define 5-10 major milestones that represent meaningful progress
7. **Review & Validation**: Ensure completeness and clarity

**CRITICAL**: Steps 2-4 must happen in this exact order to avoid the chicken-and-egg problem of needing the issue ID for the filename.

## Update ROADMAP.md (If It Exists)

After creating the PRD, check if `docs/ROADMAP.md` exists. If it does, add the new feature to the appropriate timeframe section based on PRD priority:
- **High Priority** → Short-term section
- **Medium Priority** → Medium-term section
- **Low Priority** → Long-term section

Format: `- [Brief feature description] (PRD #[issue-id])`

The ROADMAP.md update will be included in the commit at the end of the workflow (Option 2).

## Next Steps After PRD Creation

After completing the PRD, present the user with numbered options:

```
✅ PRD Created Successfully!

**PRD File**: prds/[issue-id]-[feature-name].md
**GitHub Issue**: #[issue-id]

What would you like to do next?

**1. Start working on this PRD now**
   Begin implementation immediately (recommended if you're ready to start)

**2. Commit and push PRD for later**
   Save the PRD and work on it later (will use [skip ci] flag)

Please enter 1 or 2:
```

### Option 1: Start Working Now

If user chooses option 1, first commit and push the PRD (same as Option 2), then instruct them:

---

**PRD committed and pushed.**

To start working on this PRD, run `/prd-start [issue-id]`

---

### Option 2: Commit and Push for Later

If user chooses option 2:

```bash
# Stage the PRD file (and ROADMAP.md if it was updated)
git add prds/[issue-id]-[feature-name].md
# If docs/ROADMAP.md exists and was updated, include it:
# git add docs/ROADMAP.md

# Commit with skip CI flag to avoid unnecessary CI runs
git commit -m "docs(prd-[issue-id]): create PRD #[issue-id] - [feature-name] [skip ci]

- Created PRD for [brief feature description]
- Defined [X] major milestones
- Documented problem, solution, and success criteria
- Added to ROADMAP.md ([timeframe] section)
- Ready for implementation"

# Pull latest and push to main
git pull --rebase origin main && git push origin main
```

**Confirmation Message:**
```
✅ PRD committed and pushed to main

The PRD is now available in the repository. To start working on it later, execute:
prd-start [issue-id]
```

## Important Notes

- **Option 1**: Best when you have time to begin implementation immediately
- **Option 2**: Best when creating multiple PRDs or planning future work
- **Skip CI flag**: Always use `[skip ci]` when committing PRD-only changes
- **Issue reference**: Include issue number in commit message for traceability