---
name: onboarding-playbook-creation
description: Design structured customer onboarding workflows with phased checklists, email templates, success milestones, and ownership assignments. Use when the user requests onboarding playbook creation or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: community
  version: "1.0"
---

# Onboarding Playbook Creation

Build comprehensive onboarding playbooks that guide new customers from signup to first value and sustained adoption. This skill produces phased workflows with explicit milestones, task checklists, communication templates, and clear ownership so that every customer follows a repeatable path to success regardless of which CSM is assigned.

## Workflow

1. **Define success milestones** — Identify the 3-5 concrete outcomes that signal a customer has been successfully onboarded. These should be measurable product actions, not vague goals. Examples: "first report generated," "3+ team members active," "integration with primary data source complete." Tie each milestone to a business outcome the customer cares about to maintain alignment with their goals throughout the process.

2. **Map onboarding phases** — Structure the journey into distinct phases, each with a clear entry criteria, exit criteria, and expected duration. A standard B2B framework uses four phases: **Welcome** (Day 0-3) — account setup and introductions. **Setup** (Day 4-10) — technical configuration and data import. **First Value** (Day 11-20) — achieving the initial "aha moment" with the product. **Adoption** (Day 21-30) — expanding usage across the team and embedding into workflows.

3. **Create task checklists per phase** — Break each phase into specific, actionable tasks with owners (CSM, customer, SE, product). Each task should have an estimated duration, dependencies on prior tasks, and a definition of done. Include both internal tasks (create customer Slack channel, schedule kickoff) and customer-facing tasks (invite team members, connect data source).

4. **Design communication templates** — Write email and in-app message templates for each phase transition and key touchpoint. Include: welcome email, kickoff meeting agenda, mid-onboarding check-in, milestone celebration, risk alert (if a milestone is missed), and graduation email. Each template should have personalization tokens and conditional blocks based on customer segment.

5. **Set timeline and ownership** — Assign every task to a specific role and set due dates relative to the onboarding start date (Day 0). Create escalation rules for overdue tasks: 2 days overdue triggers a CSM nudge, 5 days overdue triggers a manager alert, 10 days overdue triggers a playbook reassessment call. Build in buffer for enterprise accounts that require procurement and security reviews.

## Usage

Describe your product, customer segment, and onboarding goals. The agent will produce a complete playbook with phases, tasks, templates, and timelines.

```
Create a 30-day onboarding playbook for our B2B analytics platform. Target
segment is mid-market (50-500 employees). Key success milestones: connect a
data source, build first dashboard, share with 3+ team members.
```

## Examples

### Example 1: 30-day B2B SaaS onboarding playbook

**Input:** B2B analytics platform, mid-market segment, 30-day onboarding window.

**Output:**

#### Phase 1: Welcome (Day 0-3)
| Task | Owner | Duration | Done When |
|------|-------|----------|-----------|
| Send welcome email with login credentials and quickstart guide | CSM | 15 min | Email delivered, customer opens |
| Create internal customer channel (#cs-acme-corp) | CSM | 5 min | Channel exists with team added |
| Schedule kickoff call for Day 2-3 | CSM | 10 min | Calendar invite accepted |
| Conduct kickoff call: align on goals, introduce support channels, confirm timeline | CSM + Customer | 45 min | Meeting notes shared, milestones agreed |
| Customer completes account profile and invites admin user | Customer | 20 min | Admin user active in product |

#### Phase 2: Setup (Day 4-10)
| Task | Owner | Duration | Done When |
|------|-------|----------|-----------|
| Connect primary data source (guided walkthrough) | Customer + SE | 1-2 hours | Data source shows "connected" status, initial sync complete |
| Verify data integrity — spot-check 3 metrics against source | SE | 30 min | Metrics match within 2% tolerance |
| Configure SSO/SAML if enterprise | SE | 1 hour | Team can login via company identity provider |
| Send Day 7 check-in email: "How's setup going?" | CSM (automated) | — | Email sent, reply monitored |
| Troubleshoot any integration blockers | SE | Varies | All blockers resolved, customer unblocked |

#### Phase 3: First Value (Day 11-20)
| Task | Owner | Duration | Done When |
|------|-------|----------|-----------|
| Build first dashboard using template library | Customer + CSM | 45 min | Dashboard created with live data |
| CSM reviews dashboard and suggests improvements | CSM | 30 min | Customer confirms dashboard meets their needs |
| Customer shares dashboard with 3 team members | Customer | 10 min | 3+ users have viewed the shared dashboard |
| Send milestone email: "You built your first dashboard!" | CSM (automated) | — | Email delivered with next steps |
| 15-minute adoption check-in call | CSM + Customer | 15 min | Usage patterns reviewed, expansion opportunities identified |

#### Phase 4: Adoption (Day 21-30)
| Task | Owner | Duration | Done When |
|------|-------|----------|-----------|
| Customer creates 2 additional dashboards independently | Customer | Self-paced | 3+ total dashboards exist |
| Enable scheduled report delivery | Customer + CSM | 20 min | At least 1 scheduled report active |
| Conduct graduation call: review milestones, transition to ongoing CS | CSM + Customer | 30 min | Customer confirms self-sufficiency, success plan created |
| Internal handoff to ongoing CSM (if different from onboarding CSM) | CSM → CSM | 30 min | Handoff doc complete, new CSM introduced |
| Send graduation email with advanced resources and community invite | CSM (automated) | — | Email delivered |

### Example 2: Developer tool self-serve onboarding checklist

**Input:** Developer CLI tool, self-serve motion, no CSM involvement.

**Output:**

**In-App Onboarding Checklist (shown in dashboard sidebar)**

```
Welcome to DevTool! Complete these steps to get up and running.

□ Install the CLI
  Run: npm install -g @devtool/cli
  Verify: devtool --version shows v3.x

□ Authenticate your account
  Run: devtool auth login
  Opens browser → approve → token saved locally

□ Connect your first repository
  Run: devtool init in your project root
  Creates .devtool.yml config file

□ Run your first scan
  Run: devtool scan
  View results at app.devtool.com/results

□ Fix your first issue
  Click any finding → follow the suggested fix
  Re-run devtool scan to verify

□ Invite a teammate
  Go to Settings → Team → Invite
  Enter their email to share project access

□ Set up CI integration
  Add devtool scan to your CI pipeline
  See: docs.devtool.com/ci for GitHub Actions, GitLab CI, and Jenkins examples

✓ You're all set! Explore advanced features →
```

**Companion email sequence (automated):**
- **Signup +0h:** Welcome email with install instructions and link to interactive tutorial
- **Signup +24h:** "Did you run your first scan?" — re-engagement if install step incomplete
- **Signup +72h:** "Here's what teams like yours find most valuable" — use case inspiration
- **Signup +7d:** "Invite your team" — social proof of team adoption stats
- **Signup +14d:** "Ready for CI?" — guide to pipeline integration with ROI calculator

## Best Practices

- Optimize for time-to-first-value above all else — every task that doesn't directly contribute to the customer's first success moment should be deferred to post-onboarding.
- Build separate playbook variants per segment (SMB self-serve, mid-market guided, enterprise high-touch) rather than one generic playbook with conditional branches.
- Instrument every milestone as a product event so you can measure onboarding completion rates, identify drop-off points, and trigger automated interventions.
- Include "what good looks like" benchmarks for each phase — e.g., "80% of customers connect a data source by Day 7" — so CSMs know when an account is falling behind.
- Review and update the playbook quarterly based on completion rate data, customer feedback, and product changes.
- Assign a playbook owner (usually a CS Ops lead) who is accountable for maintaining the playbook, training new CSMs, and iterating on it.

## Edge Cases

- **Customer goes dark during onboarding** — If no response to 2 consecutive outreach attempts, trigger a "re-engagement" branch: peer CSM tries alternate contact, AE reaches out to economic buyer, final "we're here when you're ready" email at Day 25.
- **Customer wants to skip phases** — Technical customers who have already self-configured should be able to fast-track. Validate their setup meets the milestone criteria and advance them to the appropriate phase.
- **Multi-product onboarding** — When a customer purchases multiple products, stagger onboarding to avoid overwhelming them. Complete Product A onboarding before starting Product B, with a 1-week buffer.
- **Champion leaves mid-onboarding** — Immediately identify a new point of contact. Offer to restart the kickoff call with the replacement to rebuild context and alignment.
- **Onboarding takes longer than planned** — If Phase 2 (Setup) extends beyond its window due to technical complexity, do not compress Phase 3 and 4. Extend the total timeline and communicate the revised schedule to all stakeholders.
