---
name: drafting-review-email
description: |
  Drafts a stakeholder review email and a meeting invite for a test plan and
  test cases, using reviewers identified from the Jira ticket. Use when a QA
  engineer wants to draft a review email, create a meeting invite, send a
  review request, or notify stakeholders about test artifacts.
disable-model-invocation: true
tools:
  - mcp-atlassian:jira_get_issue
---

# drafting-review-email

Drafts a stakeholder review email and meeting invite for test plan and test cases.

## Progress Checklist

Copy and track your progress:

```
- [ ] Step 1: Read project context
- [ ] Step 2: Extract reviewers from Jira ticket
- [ ] Step 3: Draft review email
- [ ] Step 4: Draft meeting invite
- [ ] Validate: Preview both drafts and confirm before saving
```

## Steps

### Step 1: Read Project Context

Read these files from the project folder:
- `README.md` — project overview and ticket ID
- `test_plan/README.md` — test plan type, scenario count
- `test_cases/README.md` — test case count
- `confluence/confluence_links.md` — Confluence page URLs

### Step 2: Extract Reviewers

Fetch the Jira ticket using `mcp-atlassian:jira_get_issue` to identify:
- Assignee (primary reviewer)
- Reporter (stakeholder)
- Watchers (additional reviewers)
- Any reviewer names mentioned in comments

### Step 3: Draft Review Email

Run `/pm-demo-email` to create the review email from project context and reviewer list.

### Step 4: Draft Meeting Invite

Run `/pm-meeting-invite` to create the meeting invite for the review session.

Use reference-style links (URLs at bottom) to keep the body scannable.

### Validate

Show both full drafts to the user. Ask: "Do these look good? Should I save them to files?"

**Do NOT save to disk until the user confirms.**

After confirmation, save:
- `demo/Demo_Showcase_Email.md` — email draft
- `Meeting_Invite_[Type]_Review.md` — meeting invite

## Expected Input

Path to project folder containing README.md, test_plan/, test_cases/, and confluence/ files.
