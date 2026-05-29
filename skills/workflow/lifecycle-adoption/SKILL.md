---
name: lifecycle-adoption
description: Use when starting new projects with CMMI, adding CMMI to active development, preparing for audits, migrating tools, or facing team resistance to process adoption
---

# Lifecycle Adoption

## Overview

This skill guides **incremental CMMI adoption** on existing projects without halting development. Whether you're starting a new project with CMMI from day one or retrofitting practices onto a 5-year-old codebase, this skill provides strategies for:

- **Parallel tracks adoption**: New work follows new process, legacy code exempt
- **Retrofitting existing systems**: Adding traceability, CM, testing, and metrics to running projects
- **Change management**: Overcoming team resistance and executive skepticism
- **Right-sizing practices**: Scaling from 2-person teams to large organizations
- **Managing transitions**: Tool migrations, process changes, audit preparation

**Reference**: See `docs/sdlc-prescription-cmmi-levels-2-4.md` Section 9 (Adoption Guide) for complete policy.

### When to Use This Skill

Use this skill when:

- **Starting new project**: Bootstrapping CMMI Level 2/3/4 from day one
- **Mid-project adoption**: Adding CMMI to active development without stopping
- **Audit preparation**: Retrofitting traceability/documentation for upcoming compliance review
- **Tool migration**: Changing platforms (GitHub ↔ Azure DevOps) while maintaining compliance
- **Team resistance**: Developers push back on "process overhead"
- **Executive skepticism**: Need to demonstrate ROI for CMMI investment

### What This Skill Covers

**High-Level Guidance:**
- The Parallel Tracks Strategy (don't stop development)
- Incremental vs. Big Bang Adoption
- Quick Wins vs. Foundational Practices
- Team Size Adaptations (2 developers to 50+)

**Reference Sheets (On-Demand):**
1. **Maturity Assessment** - Gap analysis, current state mapping, prioritization
2. **Incremental Adoption Roadmap** - Phased rollout, pilot projects, scaling strategies
3. **Retrofitting Requirements** - Adding traceability to existing features
4. **Retrofitting Configuration Management** - Adopting branching strategies mid-project
5. **Retrofitting Quality Practices** - Adding tests and reviews to legacy code
6. **Retrofitting Measurement** - Establishing baselines without historical data
7. **Managing the Transition** - Parallel operations, migration strategies, preserving compliance
8. **Change Management** - Team buy-in, executive sponsorship, demonstrating value

---

## High-Level Guidance

### The Parallel Tracks Strategy

**The Core Principle**: You don't need to stop development to adopt CMMI. Use parallel tracks:

```
┌─────────────────────────────────────────────────────────┐
│ NEW FEATURES (Follow New Process)                       │
│ - Requirements tracked in issues                        │
│ - ADRs for design decisions                            │
│ - PR reviews required                                   │
│ - Test coverage enforced                                │
│ - Full CMMI compliance                                  │
└─────────────────────────────────────────────────────────┘
                           │
                           │ Parallel Development
                           │
┌─────────────────────────────────────────────────────────┐
│ EXISTING CODE (Exempt from Retrofit)                    │
│ - Legacy code untouched unless modified                │
│ - Bug fixes follow minimal process                     │
│ - Critical paths retrofitted selectively               │
│ - No "rewrite everything" required                     │
└─────────────────────────────────────────────────────────┘
```

**Timeline**: 2-3 months to full adoption for typical team (5-10 developers)

**Benefits**:
- ✅ Development velocity maintained
- ✅ Team learns gradually (not overwhelmed)
- ✅ Quick wins demonstrate value
- ✅ Audit trail created going forward

**Anti-Pattern**: "Big Bang Adoption" - Trying to go from Level 1 to Level 3 overnight. Result: Development freeze, team revolt, incomplete implementation.

### Incremental vs. Big Bang Adoption

| Aspect | Big Bang (❌ Anti-Pattern) | Incremental (✅ Recommended) |
|--------|---------------------------|------------------------------|
| **Timeline** | "We're Level 3 starting Monday!" | 2-3 month phased rollout |
| **Development** | Freeze while implementing | Parallel tracks, continuous shipping |
| **Team reaction** | Overwhelm, resistance | Gradual learning, buy-in |
| **Risk** | High (all-or-nothing) | Low (course corrections possible) |
| **First milestone** | Full compliance | Quick wins (branch protection, PR reviews) |

**Why Big Bang Fails**:
1. **Cognitive overload**: 11 process areas, 100+ practices = team paralysis
2. **Business pressure**: "Why aren't we shipping?" within 2 weeks
3. **Incomplete implementation**: Rushing leads to cargo cult compliance (checklist theater)
4. **No feedback loop**: Can't learn what works for your team context

**Incremental Approach**:
1. **Week 1-2**: Quick wins (branch protection, PR templates, issue tracking)
2. **Week 3-4**: Foundation (CM workflow, basic traceability)
3. **Week 5-8**: Quality practices (test coverage, peer reviews, ADRs)
4. **Week 9-12**: Measurement (metrics collection, baselines)
5. **Month 4+**: Refinement (Level 3 enhancements, continuous improvement)

### Quick Wins vs. Foundational Practices

**Quick Wins** (implement first - immediate value):

| Practice | Time to Implement | Value |
|----------|------------------|-------|
| **Branch protection rules** | 30 minutes | Prevents force pushes, lost work |
| **PR review requirement** | 1 hour | Catches bugs before merge |
| **Issue templates** | 2 hours | Structured requirement capture |
| **CI/CD basic pipeline** | 1 day | Automated testing, faster feedback |
| **ADR template** | 1 hour | Decision documentation starts |

**Foundational Practices** (implement second - enables maturity):

| Practice | Time to Implement | Enables |
|----------|------------------|---------|
| **Requirements traceability** | 1-2 weeks | Audit trail, impact analysis |
| **Branching workflow (GitFlow/Trunk)** | 1 week + training | Release management, parallel dev |
| **Test coverage baseline** | 2-3 weeks | Quality metrics, regression prevention |
| **Metrics collection** | 2-4 weeks | Baselines, trend analysis, process improvement |
| **Risk register** | 1 week | Proactive risk management |

**Strategy**: Lead with quick wins to demonstrate value, then invest in foundations while team is bought in.

### Team Size Adaptations

**2-3 Person Team** (Minimal Viable CMMI):
- Target: Level 2 (Managed)
- **REQM**: GitHub Issues as requirements
- **CM**: Feature branches + PR review (both review each other)
- **VER**: Automated tests only, no formal test plan
- **Documentation**: Minimal (ADRs for major decisions, no formal specs)
- **Effort**: 5% of project time on process

**4-10 Person Team** (Sweet Spot):
- Target: Level 3 (Defined)
- **REQM**: Work items with acceptance criteria, RTM via tool
- **CM**: GitFlow or GitHub Flow, 2 reviewers required
- **VER**: Test coverage >80%, formal peer review checklist
- **Documentation**: Standard templates, comprehensive ADRs
- **Effort**: 10-15% of project time on process

**11-30 Person Team** (Organizational Standard):
- Target: Level 3 → Level 4
- **REQM**: Requirements templates, formal elicitation
- **CM**: Branching strategy document, release management
- **VER**: Test plans (IEEE 829), defect density tracking
- **Documentation**: Architecture review board, design reviews
- **Effort**: 15-20% of project time on process

**30+ Person Team** (Full CMMI):
- Target: Level 4 (Quantitatively Managed)
- **All Level 3 practices** +
- **Metrics**: Statistical process control, baselines, prediction models
- **Roles**: Dedicated process owner, metrics analyst
- **Effort**: 20-25% of project time on process

#### Small Team Enforcement (2-4 Person Teams)

**Problem**: Small teams lack independent oversight (no tech lead, no manager, no external review). Under deadline pressure, teams can exploit this to appear compliant while avoiding actual work.

**Solution**: See **Enforcement Mechanisms #16-20** (Small Team Enforcement section) for detailed enforcement strategies including:
- External review requirement
- Written requirements mandate
- ADR timing verification
- Solo emergency protocol
- Admin bypass audit

These mechanisms require external verification (advisor, consultant, or automation) since small teams cannot self-police.

### When NOT to Retrofit Everything

**Selective Retrofitting Principle**: Not all legacy code needs full CMMI compliance.

**DO retrofit**:
- ✅ Critical path features (security, payment processing, data integrity)
- ✅ High-change areas (frequent bugs, ongoing development)
- ✅ Audit-required components (regulated functionality)
- ✅ New features (all new work follows new process)

**DON'T retrofit**:
- ❌ Stable, low-risk code (hasn't changed in 6+ months)
- ❌ Deprecated features (scheduled for removal)
- ❌ Prototypes and throwaway code
- ❌ Well-tested legacy code with no known issues

**Risk-Based Decision Matrix**:

```
High Change Frequency │ RETROFIT    │ RETROFIT    │
                      │ (Full)      │ (Selective) │
─────────────────────┼─────────────┼─────────────┤
Low Change Frequency  │ RETROFIT    │ EXEMPT      │
                      │ (Critical)  │             │
                      └─────────────┴─────────────┘
                        High Risk     Low Risk
```

**Example**: 100 features shipped over 2 years
- **10 critical features** (payment, auth, data sync) → Full retrofit (requirements, tests, ADRs)
- **30 active features** (ongoing development) → Selective retrofit (traceability only)
- **60 stable features** (no changes in 6+ months) → Exempt (document as legacy)

**Time savings**: Retrofitting 40 features instead of 100 = 60% effort reduction

**CRITICAL: Exemption List Approval Gate**

**Enforcement**: CTO or security officer MUST approve exemption list before Week 4. This prevents managers from classifying everything as "low risk" to avoid retrofit work.

**Approval requirements**:
- [ ] Exemption list documented with rationale (feature name, why exempt, risk assessment)
- [ ] For each exempted feature: Must justify BOTH "low change frequency" AND "low risk"
- [ ] If feature handles ANY of these → Cannot be exempt without security officer approval:
  - Protected Health Information (PHI) / Personally Identifiable Information (PII)
  - Authentication or authorization
  - Payment processing
  - Audit logging
  - Encryption/decryption
- [ ] CTO sign-off required if >80% of features classified as "exempt"

**Red flags requiring escalation to executive sponsor**:
- >80% of features labeled "exempt" → Gaming detected
- All authentication features labeled "low risk" → Security misunderstanding
- Features with known vulnerabilities labeled "exempt" → Compliance violation

**Accountability**:
- Team lead must present exemption list with evidence to CTO in Week 4 review
- CTO spot-checks 10 random "exempt" features to verify classification accuracy
- If classification gaming detected → Restart with proper risk assessment

**Example compliant exemption**:
```
Feature: Legacy report generator (reports.py)
- Last changed: 18 months ago
- Risk: Low (read-only, no PII, no auth)
- Change frequency: Zero changes in 12+ months
- Status: EXEMPT (approved by CTO 2026-01-24)
```

**Example non-compliant exemption**:
```
Feature: User login endpoint (auth.py)
- Risk claimed: "Low"
- Reality: HIGH (authentication is always high risk)
- Status: CANNOT EXEMPT (handles auth → must retrofit)
```

### Common Objections and Responses

**Objection 1**: "CMMI will slow us down"

**Response**:
- Acknowledge: "Poorly implemented process DOES slow teams down. Let's avoid that."
- Show lightweight Level 2 approach (not bureaucracy)
- Quick wins demonstrate value: "Branch protection prevented 3 lost-work incidents this month"
- Data: Teams with code review find bugs 60% faster than those without (Microsoft Research)

**Objection 2**: "We're too small for CMMI"

**Response**:
- Level 2 works for 2-person teams (see Team Size Adaptations above)
- GitHub Issues + PR reviews + ADRs = minimal overhead, maximum audit trail
- Automation reduces burden (GitHub Actions, not manual checklists)
- Small teams benefit MORE from process (no redundancy to catch errors)

**Objection 3**: "We're agile, CMMI is waterfall"

**Response**:
- CMMI is methodology-agnostic (works with Scrum, Kanban, XP)
- Map CMMI to sprints: REQM in planning, VER in reviews, VAL in demos
- User stories = requirements, ADRs = design, sprint retro = process improvement
- See prescription Section 6.2 for Agile workflow mapping

**Objection 4**: "It's too late to change mid-project"

**Response**:
- Parallel tracks mean you don't change existing code
- New features follow new process starting TODAY
- Retrofitting is selective (critical paths only)
- 2-3 month transition is feasible even on 2-year-old projects

**Objection 5**: "We don't have time for this"

**Response**:
- Time pressure is exactly why you need process (reduce rework, catch bugs early)
- Quick wins (branch protection, PR reviews) take <1 day to implement
- ROI calculation: 1 hour of code review saves 5 hours of debugging (industry average)
- Audit failure costs MORE time than incremental adoption

### Red Flags: Thoughts That Mean "STOP"

If you or the user are thinking these thoughts, STOP and reconsider:

| Thought | Reality | What to Do Instead |
|---------|---------|-------------------|
| **"Let's do a big bang rollout"** | 95% failure rate for big bang CMMI adoption | Use parallel tracks: new work follows new process, old code exempt |
| **"We'll retrofit everything before starting new work"** | Analysis paralysis, development freeze | Selective retrofit (30% critical features), parallel new development |
| **"We're too small for CMMI"** | 2-person teams can do Level 2 in 1 week | Show team size adaptation table (Level 2 = minimal viable) |
| **"CMMI = waterfall, we're agile"** | CMMI is methodology-agnostic | Map CMMI to sprint ceremonies (RD in planning, VER in review) |
| **"Let's wait until the project is done"** | Post-hoc compliance is 10x harder | Start now with parallel tracks, minimal disruption |
| **"We need perfect compliance from day one"** | Perfectionism kills adoption | Incremental: 30% → 50% → 70% compliance over 3 months |
| **"Process first, then demonstrate value"** | Team will revolt before seeing benefits | Quick wins first (branch protection Day 1), then deeper practices |
| **"Everyone must follow the same process"** | One-size-fits-all fails | Tailoring by team size, risk, and domain |
| **"We'll add tests after the feature is done"** | "Later" = never | Require tests for all new code NOW, retrofit selectively |
| **"Management just needs to mandate it"** | Top-down mandates create cargo cult compliance | Involve team in process design, demonstrate value, then enforce |

### Rationalization Table

Common rationalizations that undermine adoption (and how to counter them):

| Rationalization | Pattern | Counter |
|----------------|---------|---------|
| **"Just this once we'll skip [practice]"** | Slippery slope | "Just this once" becomes "every time". Enforce consistently from Day 1. |
| **"We're in a hurry, no time for [practice]"** | Time pressure override | "Hurry is why we NEED process. Skipping reviews = 5x more debugging time later." |
| **"This feature is too small for [practice]"** | Scope minimization | "Small changes cause big bugs. All features follow process, no exceptions." |
| **"The process is slowing us down"** | Productivity panic | "Initial 10% slowdown, long-term 30% speedup. Measure before/after." |
| **"We already do code review informally"** | Informal = good enough | "Informal = inconsistent. 8 of last 10 PRs had no review (check GitHub)." |
| **"Our team is experienced, we don't make mistakes"** | Overconfidence | "Last month: 12 production bugs. Experience ≠ infallibility." |
| **"We'll fix the process later"** | Procrastination | "Process debt compounds like technical debt. Fix now or pay 10x later." |
| **"The audit is months away"** | Distant deadline | "Process takes 2-3 months to stabilize. Start now or fail audit." |
| **"Let's use our own process, not CMMI"** | Not invented here | "Your process likely duplicates CMMI. Map it, fill gaps, save time." |
| **"We need to finish this sprint first"** | Perpetual deferral | "Every sprint will have 'just one more thing'. Parallel tracks start TODAY." |
| **"This is too bureaucratic"** | Fear of overhead | "Level 2 = branch protection + PR template. That's not bureaucracy." |
| **"Our old process worked fine"** | Status quo bias | "13 bugs last quarter, 45% of time on rework. That's not 'fine'." |

**How to use this table:**
- When user or team member says a rationalization, identify the pattern
- Respond with the counter (data-driven, not defensive)
- Redirect to the appropriate reference sheet for concrete guidance

## Enforcement Mechanisms

**Purpose**: Prevent common loophole exploits discovered through TDD adversarial testing. These 19 mechanisms close rationalizations teams use under pressure.

**Organization**:
- **Adoption & Progression** (#1-5): Emergency bypass, progression gates, workshops, parallel tracks, early adopters
- **Requirements & Design** (#6-10): Depth, validation, coverage, traceability, discovery
- **Code Review** (#11-12): Risk assessment, quality standards
- **Small Teams** (#13-17): External review, written docs, timing, emergencies, admin access
- **Git Security** (#18-19): Fork attacks, branch protection

---

### Adoption & Progression

#### 1. Emergency Bypass Process

**Prevents**: "Just this once" excuse for skipping process

**Enforcement**:
- Emergency hotfixes STILL require 1 reviewer (4-hour async SLA)
- Tag commit `emergency-bypass`
- Post-hoc documentation within 24 hours
- Monthly review: >2/month = process problem

**Red flag**: >2 emergencies/month

#### 2. Progression Gates (Consolidated)

**Prevents**: Eternal quick-wins loop, permanent plateau

**Enforcement**:
- Week 2: Quick wins complete (branch protection, templates, 1+ bug caught)
- Week 4: Foundations started (50% traceability, 3+ ADRs, workflow documented)
- Week 8: Quality active (test coverage >60%, 100% PRs reviewed)
- Week 12: Measurement established (dashboard live, baselines calculated)
- Gate failure → CTO intervention required

**Red flag**: Still at quick wins in Month 3 → escalate

#### 3. Workshop Quality Standards

**Prevents**: Workshop theater (checkbox attendance without engagement)

**Enforcement**:
- 70% active participation (documented contributions)
- 2+ alternative approaches documented
- Post-workshop survey (70% comprehension, 50% buy-in)
- Artifacts: attendance, brainstorm notes, voting results
- CTO reviews artifacts Week 2

**Red flag**: <50% felt they could influence → repeat workshop

#### 4. Parallel Tracks Deadline

**Prevents**: Indefinite legacy exemption

**Enforcement**:
- Hard cutoff Month 2: ALL new work follows process
- Bug fix = <50 LOC change only
- Tech lead classifies work (not self-reported)
- Monthly audit: >50% "legacy" in Month 3 = gaming

**Red flag**: Work started Week 7 claimed as "legacy"

#### 5. Early Adopter Credibility

**Prevents**: Junior dev pilot theater

**Enforcement**:
- >1 year tenure required
- Team validates influence ("Who do you respect?")
- Scaling metrics: Week 4 (2-3 people), Week 8 (50%), Week 12 (80%)
- CTO reviews Month 2

**Red flag**: Pilot confined to 1-2 people Week 8

---

### Requirements & Design

#### 6. Requirement Depth Standards

**Prevents**: Shallow requirements speed run

**Enforcement**:
- 6-12 requirements per moderate feature minimum
- Tech lead reviews 20% sample
- Reject if average <5 requirements/feature
- Time calibration: 4-8 hours per feature (not negotiable)

**Red flag**: 5+ feature retrofits per day

#### 7. Stakeholder Validation Enforcement

**Prevents**: "Pending validation" indefinite deferral

**Enforcement**:
- 3 documented contact attempts required
- Escalation path to executive
- NO "pending" acceptable for audits
- Proxy validation allowed with documentation

**Red flag**: >10% "pending" at Week 4

#### 8. Level 2 vs 3 Coverage Clarification

**Prevents**: 30% escape hatch abuse

**Enforcement**:
- Determine audit level Week 0 (ask auditor)
- Level 2: 30-40% of CRITICAL features
- Level 3: 80-100% of ALL features
- Auditor decides scope, not PM

**Red flag**: PM unilaterally claims "Level 2"

#### 9. Tool-Based RTM Requirement

**Prevents**: Spreadsheet escape hatch at Level 3

**Enforcement**:
- Level 2: Spreadsheet acceptable
- Level 3: GitHub/ADO required (not spreadsheet)
- Migration timeline: Weeks 1-2 spreadsheet, Weeks 3-4 migrate, Week 5+ tool only

**Red flag**: Spreadsheet still used Month 2 for Level 3

#### 10. Dark Matter Feature Detection

**Prevents**: Hiding undocumented features from audit

**Enforcement**:
- 4-way verification: code analysis, routes, UI audit, stakeholder memory
- Cross-validate lists for discrepancies
- External reviewer spot-checks 10 random code sections

**Red flag**: Feature count suspiciously low for LOC

---

### Code Review

#### 11. Risk Assessment Authority

**Prevents**: Risk-labeling game (self-declaring "low risk")

**Enforcement**:
- Objective criteria: PII/Money/Auth = HIGH (non-negotiable)
- 2-person sign-off required for risk classification
- Security team approval to downgrade

**Red flag**: >80% features labeled "low risk"

#### 12. Review Quality Standards

**Prevents**: Rubber-stamp theater

**Enforcement**:
- Minimum 5 min per 100 LOC
- Substantive comment required (not just "LGTM")
- <2 min reviews flagged
- Monthly audit: 10% spot-check
- >20% rubber stamps → lose approval privileges 1 month

**Red flag**: 100% compliance, 0 bugs caught for 4+ weeks

---

### Small Team Enforcement (2-4 person teams)

#### 13. External Review Requirement

**Prevents**: Rubber-stamp between friends

**Enforcement**:
- Quarterly external review (10% of PRs)
- Automation BLOCKS <5 min/100 LOC reviews
- Monthly self-audit required

**Accountability**: External reviewer reports to executive

#### 14. Written Requirements Mandate

**Prevents**: Verbal-only work

**Enforcement**:
- Issue MUST exist BEFORE PR created
- Timestamp verification (Issue date < PR date)
- GitHub Action blocks PRs without linked issue

**Red flag**: >20% Issues created within 1 hour of PR

#### 15. ADR Timing Verification

**Prevents**: Backdating architectural decisions

**Enforcement**:
- ADR commit MUST precede implementation commits
- Git timestamp verification (automated check)
- Limit: 2 retroactive ADRs/quarter

**Verification**: `git log --format=%ai -- docs/adr/` vs implementation commits

#### 16. Solo Emergency Protocol

**Prevents**: Skipping review when partner unavailable

**Enforcement**:
- Preferred: 4-hour async review (phone acceptable)
- If truly solo: merge with `emergency-solo` tag, external review within 48 hours
- Limit: 1 solo emergency/quarter

**Red flag**: >4 solo emergencies/year

#### 17. Admin Bypass Audit

**Prevents**: GitHub admin bypass enabled

**Enforcement**:
- Weekly GitHub Action verifies "enforce_admins=true"
- Screenshot required for quarterly review
- Separation of duties: external admin OR weekly automation

**Verification**: `gh api repos/{owner}/{repo}/branches/main/protection | jq '.enforce_admins.enabled'`

---

### Git Workflow Security

#### 18. Fork Security Configuration

**Prevents**: Fork-based bypass attack

**Enforcement**:
- GitHub: "Restrict who can push to matching branches" enabled
- "Require linear history" enabled
- Weekly audit for force-push attempts
- Monthly manual audit of protection changes

**Red flag**: Multiple failed force-push attempts

#### 19. Emergency Hotfix Enforcement

**Prevents**: Disabling branch protection

**Enforcement**:
- Emergency does NOT mean disable protection
- 8-step process: hotfix branch → PR → 4-hour review → merge via protection
- Real-time webhook alerts if protection disabled
- Auto-remediation every 6 hours
- Mandatory post-mortem if disabled

**Red flag**: Protection disabled >1 hour

---



## Reference Sheets

The following reference sheets provide detailed, step-by-step guidance for specific adoption scenarios. Each reference is a separate file - load on-demand when needed.

### 1. Maturity Assessment (`maturity-assessment.md`)

**When to load:** Starting adoption, gap analysis, determining Level 2/3/4 fit, audit preparation

Assess current CMMI maturity level, identify gaps, prioritize improvements using:
- Process area scoring rubric (11 CMMI process areas)
- Evidence-based assessment templates
- Risk-based gap prioritization matrix (quick wins vs. foundational practices)

**Provides:** Scoring method, assessment templates, prioritization framework, tool integration patterns

**Load reference:** See `maturity-assessment.md` for complete assessment process.

---

### 2. Incremental Adoption Roadmap (`adoption-roadmap.md`)

**When to load:** Planning phased rollout, pilot project strategy, scaling practices organization-wide

12-week incremental adoption roadmap with:
- Week-by-week milestones for Level 2/3/4
- Pilot project approach (start small, scale success)
- Parallel tracks timeline (new work = new process)
- Team size adaptations (2-person to 50+ person teams)

**Provides:** Weekly implementation plans, pilot selection criteria, scaling strategies, rollout timelines

**Load reference:** See `adoption-roadmap.md` for complete phased rollout guidance.

---

### 3. Retrofitting Requirements (`retrofitting-requirements.md`)

**When to load:** Adding requirements traceability to existing features, documenting undocumented code

Add RD + REQM practices to existing codebase without rewriting:
- Dark matter feature detection (find undocumented features)
- Reverse-engineering requirements from code
- Progressive traceability (start with critical paths)
- Stakeholder validation for legacy features

**Provides:** Retrofitting workflow, traceability templates, GitHub/Azure DevOps implementation patterns

**Load reference:** See `retrofitting-requirements.md` for complete retrofitting process.

---

### 4. Retrofitting Configuration Management (`retrofitting-cm.md`)

**When to load:** Adopting branching strategies mid-project, adding version control discipline, migrating platforms

Add CM practices to existing project without disrupting active development:
- Branch strategy migration (trunk-based → GitFlow → release branches)
- Grandfathering existing violations (future-only enforcement)
- Tag/release strategy for untagged history
- Migration workflows (SVN → Git, Git → Monorepo)

**Provides:** Migration playbooks, branch protection rules, release process templates, rollback procedures

**Load reference:** See `retrofitting-cm.md` for complete CM retrofitting guidance.

---

### 5. Retrofitting Quality Practices (`retrofitting-quality.md`)

**When to load:** Adding tests and code reviews to legacy code, implementing VER + VAL practices

Add testing and review practices without "test everything first":
- Progressive test coverage (new code first, then critical paths)
- Characterization tests for legacy code
- Code review policy adoption (future PRs only)
- Validation criteria for existing features

**Provides:** Test retrofitting strategies, review policy templates, coverage targeting, validation workflows

**Load reference:** See `retrofitting-quality.md` for complete quality retrofitting process.

---

### 6. Retrofitting Measurement (`retrofitting-measurement.md`)

**When to load:** Establishing metrics without historical data, adding MA + QPM + OPP practices

Create baselines and measurement programs when starting from zero:
- Establishing baselines without history (use industry benchmarks)
- Metric selection for Level 2/3/4
- Automated data collection (GitHub API, Azure DevOps Analytics)
- Statistical baselines and control limits (Level 4)

**Provides:** Metric definitions, baseline establishment methods, dashboard templates, SPC implementation

**Load reference:** See `retrofitting-measurement.md` for complete measurement retrofitting guidance.

---

### 7. Managing the Transition (`managing-transition.md`)

**When to load:** Tool migrations, platform changes, maintaining compliance during parallel operations

Maintain CMMI compliance while changing tools/platforms:
- Parallel operations (old + new systems simultaneously)
- GitHub ↔ Azure DevOps migration patterns
- Preserving traceability during migration
- Compliance continuity strategies

**Provides:** Migration playbooks, parallel operation procedures, traceability preservation, rollback plans

**Load reference:** See `managing-transition.md` for complete transition management guidance.

---

### 8. Change Management (`change-management.md`)

**When to load:** Team resistance, executive skepticism, demonstrating ROI, building buy-in

Overcome organizational resistance and build support for CMMI adoption:
- Countering "process = overhead" objections (with data)
- Demonstrating quick wins (velocity improvement, bug reduction)
- Executive sponsorship strategies
- Team buy-in through incremental value delivery

**Provides:** Objection handling scripts, ROI calculations, stakeholder communication templates, success metrics

**Load reference:** See `change-management.md` for complete change management guidance.

---

## Loading Reference Sheets

**How to access:**
```
"I need detailed guidance on [topic]"
→ Load the appropriate reference sheet from the list above
```

**When you need a reference:**
- Be specific about which aspect you need ("gap analysis process" → maturity-assessment)
- References are comprehensive (250-550 lines each)
- Each reference is self-contained with templates and examples

**Cross-references:** Reference sheets link to each other when practices overlap (e.g., retrofitting requirements references maturity assessment for prioritization).
