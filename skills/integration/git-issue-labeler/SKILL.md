---
name: git-issue-labeler
description: Assess GitHub issues and assign appropriate labels using GitHub default labels (bug, enhancement, documentation, duplicate, good first issue, help wanted, invalid, question, wontfix) with detailed descriptions
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers, maintainers
  workflow: issue-management
---

## What I do

I provide intelligent GitHub issue label assessment by:

- Analyzing issue content to determine appropriate GitHub default labels
- Using keyword and pattern matching to identify issue types
- Assigning single or multiple labels based on issue complexity
- Providing label descriptions for clarity and consistency
- Supporting the 9 GitHub default labels: bug, enhancement, documentation, duplicate, good first issue, help wanted, invalid, question, wontfix
- Using GitHub CLI (`gh`) to query available repository labels
- Generating label assignment reports for review

## When to use me

Use this when:
- You need to assess and label GitHub issues automatically
- You want consistent label assignment across your repository
- You need to categorize issues using GitHub's default label scheme
- You're setting up a new repository and need label guidelines
- You want to review unlabeled or mislabeled issues
- You need to train contributors on when to use specific labels

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Git repository with GitHub remote
- Write access to the GitHub repository
- Repository uses GitHub's default labels or custom labels
- Valid `GITHUB_TOKEN` or `gh` authentication setup

## GitHub Default Labels Reference

### bug
**Description**: Something isn't working as expected or is broken

**Keywords**: fix, error, broken, crash, fail, doesn't work, incorrect, wrong, problem, issue, bug, defect

**Examples**:
- "Login fails when user enters invalid credentials"
- "App crashes when uploading large files"
- "Button click doesn't trigger expected action"

### enhancement
**Description**: New feature or request to improve existing functionality

**Keywords**: add, implement, create, new, feature, support, introduce, build, develop, request, suggestion

**Examples**:
- "Add dark mode support to the dashboard"
- "Implement export to PDF functionality"
- "Add pagination to user list"

### documentation
**Description**: Improvements or additions to documentation

**Keywords**: document, readme, docs, guide, explain, tutorial, wiki, comment, manual, help

**Examples**:
- "Document the API endpoints for authentication"
- "Update README with installation instructions"
- "Add code comments to complex functions"

### duplicate
**Description**: This issue or pull request already exists

**Keywords**: duplicate, same as, already exists, similar, repeated, already reported

**Examples**:
- "This is the same as issue #123"
- "Already reported in #456"

### good first issue
**Description**: Good for newcomers or first-time contributors

**Keywords**: beginner, simple, easy, small, straightforward, first time, newcomer, junior

**Examples**:
- "Fix typo in header component"
- "Add unit test for utility function"
- "Update example in README"

### help wanted
**Description**: Extra attention or help is needed

**Keywords**: help wanted, need help, assistance, looking for help, collaboration, community

**Examples**:
- "Need help with performance optimization"
- "Looking for someone to review documentation"

### invalid
**Description**: This doesn't seem right or is not a valid issue

**Keywords**: invalid, not an issue, wrong repo, user error, configuration, misunderstanding

**Examples**:
- "This is a user configuration issue"
- "Wrong repository for this feature request"
- "Not a bug - working as designed"

### question
**Description**: Further information is requested or clarification needed

**Keywords**: question, how, what, why, clarification, explain, understand, ask, wondering

**Examples**:
- "How do I configure authentication?"
- "What is the purpose of this function?"
- "Question about API usage"

### wontfix
**Description**: This will not be worked on due to technical limitations, out of scope, or other reasons

**Keywords**: wontfix, out of scope, not feasible, declined, rejected, wont do, never

**Examples**:
- "Feature is out of scope for this project"
- "Technical limitations prevent implementation"
- "Not aligned with project goals"

## Steps

### Step 1: Query Available Labels
First, check what labels are available in the repository:

```bash
# Get all available labels in the repository
gh label list --json name,description,color

# Get default labels specifically
gh label list --search "bug|enhancement|documentation|duplicate|good first issue|help wanted|invalid|question|wontfix"
```

### Step 2: Analyze Issue Content
Read the issue title and body to identify keywords and patterns:

```bash
# Read issue content
gh issue view <issue-number> --json title,body,labels

# Extract title and body for analysis
issue_title=$(gh issue view <issue-number> --jq '.title')
issue_body=$(gh issue view <issue-number> --jq '.body')
```

### Step 3: Determine Appropriate Labels
Use keyword matching to assign labels:

#### Label Detection Logic

**Bug Detection**:
```bash
if [[ "$issue_content" =~ (fix|error|broken|crash|fail|doesn't work|incorrect|wrong|problem|bug|defect) ]]; then
  labels+=("bug")
fi
```

**Enhancement Detection**:
```bash
if [[ "$issue_content" =~ (add|implement|create|new|feature|support|introduce|build|develop|request|suggestion) ]]; then
  labels+=("enhancement")
fi
```

**Documentation Detection**:
```bash
if [[ "$issue_content" =~ (document|readme|docs|guide|explain|tutorial|wiki|comment|manual|help) ]]; then
  labels+=("documentation")
fi
```

**Duplicate Detection**:
```bash
if [[ "$issue_content" =~ (duplicate|same as|already exists|similar|repeated|already reported) ]]; then
  labels+=("duplicate")
fi
```

**Good First Issue Detection**:
```bash
if [[ "$issue_content" =~ (beginner|simple|easy|small|straightforward|first time|newcomer|junior) ]]; then
  labels+=("good first issue")
fi
```

**Help Wanted Detection**:
```bash
if [[ "$issue_content" =~ (help wanted|need help|assistance|looking for help|collaboration|community) ]]; then
  labels+=("help wanted")
fi
```

**Invalid Detection**:
```bash
if [[ "$issue_content" =~ (invalid|not an issue|wrong repo|user error|configuration|misunderstanding) ]]; then
  labels+=("invalid")
fi
```

**Question Detection**:
```bash
if [[ "$issue_content" =~ (question|how|what|why|clarification|explain|understand|ask|wondering) ]]; then
  labels+=("question")
fi
```

**Wontfix Detection**:
```bash
if [[ "$issue_content" =~ (wontfix|out of scope|not feasible|declined|rejected|wont do|never) ]]; then
  labels+=("wontfix")
fi
```

### Step 4: Assign Labels to Issue
Use GitHub CLI to assign the determined labels:

```bash
# Assign single label
gh issue edit <issue-number> --add-label "bug"

# Assign multiple labels
gh issue edit <issue-number> --add-label "bug,enhancement"

# Remove incorrect labels
gh issue edit <issue-number> --remove-label "documentation"
```

### Step 5: Generate Assessment Report
Create a summary of the label assignment:

```markdown
# Issue Label Assessment

**Issue**: #<issue-number> - <issue-title>

**Assigned Labels**:
- `<label1>`: <label description>
- `<label2>`: <label description>

**Detection Keywords**:
- `<keyword1>` → `<label1>`
- `<keyword2>` → `<label2>`

**Confidence**: High/Medium/Low

**Recommendations**:
- Additional labels to consider
- Labels to review
- Notes on ambiguous cases
```

## Best Practices

### Label Assignment

- **Start with primary label**: Assign the most appropriate label first
- **Use multiple labels sparingly**: Maximum 2-3 labels per issue is recommended
- **Prioritize by impact**: Bug > enhancement > documentation
- **Be consistent**: Use same labels for similar issues
- **Review existing labels**: Check issue history before assigning new labels

### Content Analysis

- **Analyze both title and body**: Keywords can appear in either
- **Consider context**: Same keyword may indicate different label based on context
- **Look for explicit requests**: "Please add" vs "How to add"
- **Check for negations**: "not a bug" should not be labeled as bug
- **Review issue comments**: Comments may provide additional context

### Quality Assurance

- **Verify label exists**: Check repository label list before assigning
- **Review custom labels**: Some repos use custom labels instead of defaults
- **Consider issue priority**: Critical bugs may need additional attention
- **Document decisions**: Add comments explaining label assignment rationale
- **Update as needed**: Labels can change as issue evolves

## Common Issues

### Label Doesn't Exist

**Issue**: Attempting to assign a label that doesn't exist in the repository

**Solution**:
```bash
# First, check available labels
gh label list

# If using custom labels, use those instead
gh issue edit <issue-number> --add-label "custom-label-name"

# Or create the missing label
gh label create "bug" --color "d73a4a" --description "Something isn't working"
```

### Conflicting Labels

**Issue**: Issue is assigned both "bug" and "enhancement" which may be conflicting

**Solution**:
- Review the issue content carefully
- Determine primary intent: fix vs new feature
- Remove the conflicting label
- Add a comment explaining the decision

### Multiple Labels Overlap

**Issue**: Issue qualifies for multiple similar labels (e.g., bug + invalid)

**Solution**:
- Assess which label is more appropriate
- "Invalid" takes precedence over "bug" if issue is not valid
- "Documentation" can be combined with other labels
- Use comment to explain the combination

### Low Confidence Assignment

**Issue**: Unable to confidently determine the appropriate label

**Solution**:
- Leave unlabeled or use generic label like "enhancement"
- Add comment requesting clarification from issue author
- Ask for team review: "needs: triage" label
- Manual review by maintainer

### Keyword Ambiguity

**Issue**: Same keyword indicates different labels based on context

**Examples**:
- "add" could be enhancement ("add feature") or bug ("add error handling")
- "fix" could be bug ("fix broken feature") or enhancement ("fix UI")
- "help" could be help wanted or question

**Solution**:
- Analyze surrounding context
- Check issue description for intent
- Look at code examples or screenshots
- When in doubt, ask for clarification

## Verification Commands

After assessing and labeling an issue:

```bash
# 1. Verify issue has labels
gh issue view <issue-number> --jq '.labels[].name'

# 2. Check label count
label_count=$(gh issue view <issue-number> --jq '.labels | length')
echo "Issue has $label_count label(s)"

# 3. Validate labels exist in repository
for label in $(gh issue view <issue-number> --jq '.labels[].name'); do
  if gh label list --search "$label" --jq 'any(.name == "'"$label"'")' | grep -q "true"; then
    echo "✓ Label '$label' exists"
  else
    echo "❌ Label '$label' does not exist"
  fi
done

# 4. Review issue timeline for label changes
gh issue view <issue-number> --json timeline --jq '.timeline[] | select(.event == "labeled")'

# 5. Generate assessment report
echo "Assessment for #<issue-number>"
echo "Title: $(gh issue view <issue-number> --jq '.title')"
echo "Labels: $(gh issue view <issue-number> --jq '.labels | map(.name) | join(\", \")')"
```

## Assessment Report Template

```markdown
# Issue Label Assessment Report

**Issue**: #<issue-number> - <issue-title>
**Author**: @<author>
**Created**: <date>
**Assessed By**: @<assessor>
**Assessment Date**: <date>

## Current Labels
- [x] `bug` - Something isn't working
- [ ] `enhancement` - New feature or request
- [ ] `documentation` - Documentation improvements
- [ ] `duplicate` - Already exists
- [ ] `good first issue` - Good for newcomers
- [ ] `help wanted` - Extra attention needed
- [ ] `invalid` - Not a valid issue
- [ ] `question` - Clarification needed
- [ ] `wontfix` - Will not be worked on

## Keyword Analysis
| Keyword Found | Detected Label | Confidence |
|---------------|----------------|------------|
| fix | bug | High |
| error | bug | High |
| add feature | enhancement | Medium |

## Recommended Labels
1. **Primary**: `bug` (High confidence)
2. **Secondary**: `enhancement` (Medium confidence)

## Notes
- Issue contains both bug report and feature request
- Clarification from author recommended
- Consider splitting into two separate issues

## Action Taken
- Assigned labels: `bug`, `enhancement`
- Added comment requesting clarification
- Scheduled for team review
```

## Related Skills

- **git-issue-creator**: For creating GitHub issues with intelligent tag detection
- **ticket-branch-workflow**: Framework for ticket-to-branch workflows
- **jira-git-integration**: For JIRA + GitHub workflows
- **pr-creation-workflow**: For creating pull requests after resolving issues

## Automation Example

Assess multiple issues at once:

```bash
#!/bin/bash
# Assess all open issues without labels

for issue_number in $(gh issue list --state open --limit 50 --jq '.[].number'); do
  labels=$(gh issue view "$issue_number" --jq '.labels | length')

  if [ "$labels" -eq 0 ]; then
    echo "Assessing issue #$issue_number..."

    # Get issue content
    title=$(gh issue view "$issue_number" --jq '.title')
    body=$(gh issue view "$issue_number" --jq '.body')
    content="${title} ${body}"

    # Determine labels
    assign_labels=()

    if [[ "$content" =~ (bug|fix|error|broken|crash) ]]; then
      assign_labels+=("bug")
    fi

    if [[ "$content" =~ (enhancement|add|implement|feature) ]]; then
      assign_labels+=("enhancement")
    fi

    if [[ "$content" =~ (documentation|docs|readme) ]]; then
      assign_labels+=("documentation")
    fi

    # Assign labels
    if [ ${#assign_labels[@]} -gt 0 ]; then
      label_string=$(IFS=,; echo "${assign_labels[*]}")
      gh issue edit "$issue_number" --add-label "$label_string"
      echo "✓ Assigned labels: $label_string"
    else
      echo "? Could not determine label for #$issue_number"
    fi
  fi
done
```
