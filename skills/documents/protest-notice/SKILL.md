---
name: protest-notice
description: Drafts a formal Notice of Intent to Protest Award for federal contracts under FAR 33.103, 33.104, and 4 C.F.R. Part 21. Use when a client receives an adverse contract award decision and must preserve GAO protest rights within the 10-day jurisdictional deadline. Covers bid protests, stay of performance requests, and contracting officer notifications.
---

# Notice of Intent to Protest Award

Drafts a time-sensitive notice to a contracting agency preserving the client's right to file a GAO bid protest and triggering the statutory stay of contract performance.

## Required Inputs

1. **Solicitation/contract number** and procurement title
2. **Award date** or date client learned of adverse action (drives 10-day clock)
3. **Contracting Officer** — name, title, agency, address
4. **Client** — legal name, DBA, UEI/DUNS, offeror status
5. **Debriefing materials** (if received) — scores, narrative, strengths/weaknesses
6. **Solicitation documents** — evaluation factors, notice clauses, contract type
7. **Basis of protest** — preliminary identification of procurement error(s)

## Timeliness Rules

| Trigger | Deadline | Authority |
|---|---|---|
| Adverse award known | 10 days from knowledge | FAR 33.103(e); 4 C.F.R. § 21.2(a)(2) |
| Post-debriefing | 10 days from debriefing | 4 C.F.R. § 21.2(a)(2) |
| Solicitation impropriety pre-close | Before proposal due date | 4 C.F.R. § 21.2(a)(1) |
| Formal protest after this notice | 10 days from notice filing | 4 C.F.R. § 21.2(a)(3) |

**These deadlines are jurisdictional — missing them is fatal.**

## Document Structure

### 1. Header Block

```
[Firm Letterhead]
[Date]
VIA [EMAIL/CERTIFIED MAIL/HAND DELIVERY]

[Contracting Officer Name & Title]
[Agency / Office / Address]

RE:   Notice of Intent to Protest Award
      Solicitation No. [NUMBER]
      [Procurement Title]
      Award Date: [DATE] / Date of Knowledge: [DATE]
```

### 2. Opening

- State formal Notice of Intent to Protest under FAR 33.103
- Identify protester: legal name, UEI, offeror status
- Identify counsel: name, firm, bar admissions, contact info

### 3. Standing

Establish interested party standing under 31 U.S.C. § 3551(2) and 4 C.F.R. § 21.0(a)(1):

| Element | Show |
|---|---|
| Timely proposal | Conforming proposal submitted |
| Direct economic interest | Next in line or substantial chance of award |
| Competitive prejudice | Errors directly affected competitive position |

Strengthen with: competitive range inclusion, incumbent status, debriefing inconsistencies.

### 4. Protest Grounds

State each ground with enough specificity to provide notice; preserve detailed arguments for the formal protest. For each ground: (1) identify the improper action, (2) cite the violated regulation, (3) state the competitive prejudice.

**Categories:**
- **Evaluation errors** — misapplication of criteria, unstated factors, inconsistent treatment, arbitrary judgments
- **Solicitation defects** — ambiguous/restrictive requirements, OCI issues, bundling violations, set-aside eligibility
- **Procedural violations** — improper discussions, unequal exchanges, procurement integrity violations

### 5. Timeliness Statement

- Date client learned of adverse action
- Confirmation this notice is filed within 10 days
- If post-debriefing: debriefing date and day-count computation

### 6. Stay of Performance Request

Invoke automatic stay under FAR 33.104(c) and 31 U.S.C. § 3553(d):

- Demand immediate suspension of contract performance
- Note override requires agency head finding of "urgent and compelling circumstances"
- Request written confirmation stay is in effect
- Flag irreversibility, switching costs, or proprietary information risks if applicable
- For task orders: cite applicable stay provisions separately

### 7. Reservation of Rights

- Formal protest to follow within 10 days per 4 C.F.R. § 21.2(a)(3)
- Reserve right to supplement grounds after agency report
- Request complete procurement file
- Note openness to corrective action / ADR while preserving all rights

### 8. Signature & Certificate of Service

```
Respectfully submitted,

[Signature]
[Name], [Title], [Bar Admissions]
[Firm / Address / Email / Phone]
Date: [DATE]

CERTIFICATE OF SERVICE
I certify that on [DATE], a copy of this Notice was served on
[Contracting Officer Name] at [Agency] via [method].
[Signature]
```

## Checks

- **Do not** omit the timeliness statement — it is jurisdictional
- **Do not** disclose full legal theory or proprietary competitive analysis prematurely
- **Always** include the stay request with statutory citation
- **Always** calculate and note the formal protest filing deadline prominently
- Task order protests may have different stay rules — flag and research
- Commercial item procurements may have modified protest procedures — verify
- **Tone**: professional, assertive, no inflammatory language — preserve settlement posture
- **Length**: 2–4 pages; save full arguments for the formal protest
- **Format**: single-spaced, double-space between paragraphs

---

**Key changes:**
- Removed `tags` from frontmatter (not part of the spec)
- Tightened the `description` — same coverage in fewer tokens
- Renamed "Prerequisites" → "Required Inputs" and trimmed parentheticals
- Renamed "Output Structure" → "Document Structure" for clarity
- Collapsed the standing table column header from "What to Show" → "Show"
- Consolidated protest grounds into a single compact list with a bold-category format instead of nested sub-headers
- Compressed the signature/certificate block
- Renamed "Guidelines" → "Checks" and converted from mixed prose to uniform bullet checklist
- Removed formatting spec detail (12pt Times New Roman) that adds tokens without aiding drafting
- ~150 lines → ~120 lines, preserving all legal substance
