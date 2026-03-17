---
name: nda-generator
description: Create appropriate non-disclosure agreements for different business contexts with balanced terms and proper scope definitions
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# NDA Generator

> Generate appropriate non-disclosure agreements tailored to specific business contexts, with balanced terms that protect both parties.

## When to Use This Skill

- Starting vendor conversations
- Exploring partnerships
- Hiring contractors/consultants
- M&A due diligence
- Co-development discussions

## Methodology Foundation

Based on **standard NDA frameworks** combined with:
- Context-appropriate scope definition
- Balanced mutual obligations
- Clear exception handling
- Practical enforcement provisions

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Suggests NDA type | Signing authority |
| Drafts core terms | Jurisdiction |
| Identifies key provisions | Term length |
| Flags imbalanced terms | Business risk |
| Creates custom clauses | Final review |

## Instructions

### Step 1: Determine NDA Type

**NDA Types:**

| Type | When to Use | Protection |
|------|-------------|------------|
| **Mutual (Bilateral)** | Both parties share | Equal obligations |
| **One-Way** | Only one party shares | Receiving party bound |
| **Multilateral** | Multiple parties | All parties bound |

**Selection Matrix:**

| Scenario | Recommended Type |
|----------|------------------|
| Partnership exploration | Mutual |
| Vendor evaluation | One-way (you disclose) |
| Client proposal | One-way (client discloses) |
| M&A due diligence | Mutual |
| Employee/contractor | One-way (you disclose) |

### Step 2: Define Confidential Information

**Scope Options:**

| Scope | Definition | Risk Level |
|-------|------------|------------|
| **Broad** | All information shared | High (over-inclusive) |
| **Marked** | Only labeled "Confidential" | Medium (may miss verbal) |
| **Defined** | Specific categories listed | Low (clear boundaries) |
| **Combination** | Written must be marked, oral confirmed | Best practice |

**Common Categories:**
- Technical specifications
- Business plans and strategy
- Customer/prospect lists
- Financial information
- Product roadmaps
- Pricing and costs
- Trade secrets

### Step 3: Key Provisions

**Essential Elements:**

| Provision | Purpose | Standard Term |
|-----------|---------|---------------|
| Definition | What's protected | See scope above |
| Obligations | What recipient must do | Reasonable care standard |
| Permitted Use | Why they can access | Specific purpose stated |
| Exceptions | What's not confidential | Public, prior knowledge, etc. |
| Term | How long agreement lasts | 2-5 years typical |
| Survival | How long confidentiality lasts | 3-5 years after disclosure |
| Return/Destroy | What happens after | Certify destruction |

**Standard Exceptions:**
1. Publicly available (not through breach)
2. Already known by recipient
3. Independently developed
4. Received from third party (without breach)
5. Required by law (with notice)

### Step 4: Balance Assessment

**Balanced vs. Overreaching:**

| Balanced | Overreaching |
|----------|--------------|
| Mutual obligations | One-sided duties |
| Reasonable care standard | Strict liability |
| Defined scope | "Any information" |
| Specific purpose | Unlimited use |
| Reasonable term | Perpetual |
| Standard exceptions | No exceptions |

### Step 5: Generate Document

**Output Structure:**
1. Parties and date
2. Background/Recitals
3. Definitions
4. Obligations
5. Permitted use and purpose
6. Exceptions
7. Term and survival
8. Return/destruction
9. Remedies
10. General provisions
11. Signatures

## Examples

### Example 1: Mutual NDA for Partnership Discussion

**Input:**
```
Create a mutual NDA for:
- Exploring a potential integration partnership
- Both companies are SaaS providers
- We'll share technical specs and business plans
- 12-month discussion period expected
```

**Output:**
```
## MUTUAL NON-DISCLOSURE AGREEMENT

---

**This Mutual Non-Disclosure Agreement** ("Agreement") is entered into
as of [DATE] ("Effective Date") by and between:

**[YOUR COMPANY]**, a [State] corporation with its principal place
of business at [Address] ("Company A")

and

**[PARTNER COMPANY]**, a [State] corporation with its principal
place of business at [Address] ("Company B")

(each a "Party" and collectively the "Parties")

---

### RECITALS

The Parties wish to explore a potential business relationship
involving integration between their respective software platforms
(the "Purpose"). In connection with this evaluation, each Party
may disclose certain confidential and proprietary information to
the other Party.

---

### 1. DEFINITION OF CONFIDENTIAL INFORMATION

**1.1** "Confidential Information" means any non-public information
disclosed by one Party (the "Disclosing Party") to the other Party
(the "Receiving Party") in connection with the Purpose, including
but not limited to:

(a) Technical information: software architecture, APIs, source code,
    algorithms, product specifications, and development roadmaps

(b) Business information: business plans, strategies, customer lists,
    pricing, financial data, and partnership terms

(c) Any information marked "Confidential" or that would reasonably
    be understood to be confidential given its nature

**1.2** Confidential Information disclosed orally shall be confirmed
as confidential in writing within ten (10) business days of disclosure.

---

### 2. OBLIGATIONS

**2.1** The Receiving Party shall:

(a) Hold Confidential Information in strict confidence using at least
    the same degree of care used to protect its own confidential
    information, but no less than reasonable care

(b) Limit disclosure to employees and contractors with a need to know
    who are bound by confidentiality obligations at least as protective

(c) Use Confidential Information solely for the Purpose

(d) Not reverse engineer, disassemble, or decompile any software or
    technical information disclosed

**2.2** Each Party shall be responsible for any breach by its
employees, contractors, or agents.

---

### 3. EXCEPTIONS

**3.1** Confidential Information does not include information that:

(a) Is or becomes publicly available without breach of this Agreement

(b) Was rightfully known to the Receiving Party prior to disclosure,
    as documented by written records

(c) Is rightfully received from a third party without restriction
    and without breach of any obligation of confidentiality

(d) Is independently developed by the Receiving Party without
    reference to Confidential Information, as documented by
    written records

**3.2** Disclosure required by law: If legally compelled to disclose,
the Receiving Party shall provide prompt written notice (where
legally permitted) to allow the Disclosing Party to seek protective
measures.

---

### 4. TERM AND SURVIVAL

**4.1** This Agreement shall remain in effect for twelve (12) months
from the Effective Date unless earlier terminated by either Party
with thirty (30) days written notice.

**4.2** Confidentiality obligations shall survive for three (3) years
following disclosure of the specific Confidential Information,
regardless of Agreement termination.

---

### 5. RETURN OF INFORMATION

**5.1** Upon termination or request, the Receiving Party shall
promptly return or destroy all Confidential Information and certify
such destruction in writing.

**5.2** Notwithstanding the foregoing, the Receiving Party may retain:
(a) copies required by law or regulation, and (b) copies in automatic
backup systems, provided such retained copies remain subject to
confidentiality obligations.

---

### 6. NO LICENSE OR WARRANTY

**6.1** No license under any intellectual property rights is granted
or implied by this Agreement.

**6.2** Confidential Information is provided "AS IS" without warranty
of any kind.

---

### 7. REMEDIES

**7.1** Each Party acknowledges that breach may cause irreparable
harm for which monetary damages may be inadequate, and agrees that
the non-breaching Party may seek equitable relief without posting
bond.

**7.2** All remedies are cumulative and not exclusive.

---

### 8. GENERAL PROVISIONS

**8.1 Governing Law:** This Agreement shall be governed by the laws
of the State of [STATE] without regard to conflicts of law principles.

**8.2 Entire Agreement:** This Agreement constitutes the entire
understanding regarding its subject matter and supersedes all prior
discussions.

**8.3 Amendment:** Modifications must be in writing signed by
both Parties.

**8.4 Assignment:** Neither Party may assign without prior written
consent, except in connection with merger or acquisition.

**8.5 Severability:** If any provision is unenforceable, the
remainder shall continue in effect.

---

### SIGNATURES

**[YOUR COMPANY]**

By: _______________________
Name:
Title:
Date:

**[PARTNER COMPANY]**

By: _______________________
Name:
Title:
Date:
```

### Example 2: One-Way NDA for Consultant

**Input:**
```
Quick NDA for hiring a marketing consultant.
They'll see our customer data and growth metrics.
3-month engagement.
```

**Output:**
```
## ONE-WAY NON-DISCLOSURE AGREEMENT
## (Consultant/Contractor)

---

This Non-Disclosure Agreement ("Agreement") is made as of [DATE]
between:

**[COMPANY NAME]** ("Company")
and
**[CONSULTANT NAME]** ("Consultant")

---

### 1. PURPOSE

Company engages Consultant for marketing consulting services.
In performing these services, Consultant may access Company's
confidential business information.

---

### 2. CONFIDENTIAL INFORMATION

**Includes:**
- Customer lists and customer data
- Revenue, growth metrics, and financial information
- Marketing strategies and campaign data
- Business plans and projections
- Any information marked or identified as confidential

**Excludes:**
- Information publicly available (not through breach)
- Information Consultant already possessed
- Information independently developed
- Information received from third parties without restriction

---

### 3. CONSULTANT OBLIGATIONS

Consultant agrees to:
- Keep all Confidential Information strictly confidential
- Use information only for performing services for Company
- Not disclose to any third party without prior written consent
- Use reasonable care to prevent unauthorized disclosure
- Promptly notify Company of any suspected breach

---

### 4. TERM

- Agreement effective from date signed
- Engagement period: Three (3) months
- Confidentiality obligations survive for two (2) years
  after engagement ends

---

### 5. RETURN OF INFORMATION

Upon engagement completion or Company request, Consultant shall:
- Return or destroy all Confidential Information
- Delete from all personal devices and storage
- Certify compliance in writing if requested

---

### 6. ACKNOWLEDGMENTS

Consultant acknowledges that:
- Breach may cause irreparable harm
- Company may seek injunctive relief
- Consultant's obligations are independent of any compensation owed

---

### 7. GENERAL

- Governed by laws of [STATE]
- Entire agreement; supersedes prior discussions
- No assignment without consent
- Modifications require written agreement

---

**AGREED:**

Company: _______________________
Name:
Title:
Date:

Consultant: _______________________
Name:
Date:
```

## Skill Boundaries

### What This Skill Does Well
- Generating standard NDA language
- Adapting terms to context
- Identifying key provisions
- Flagging imbalanced terms

### What This Skill Cannot Do
- Provide legal advice
- Know jurisdiction-specific requirements
- Guarantee enforceability
- Replace legal review

### When to Escalate to Human
- High-value or high-risk situations
- Unusual or complex provisions
- Cross-border considerations
- Any modifications to generated templates

## Iteration Guide

**Follow-up Prompts:**
- "Add a non-compete provision"
- "Make this NDA more protective for us"
- "What if they want to share with their lawyers?"
- "Add a provision for joint development"

## References

- ACC Model NDAs
- ABA Business Law Section Guidelines
- Standard Commercial Contract Templates
- SEC EDGAR Filing Examples

## Related Skills

- `contract-review` - Reviewing received NDAs
- `gdpr-compliance` - Data protection overlay
- `terms-analyzer` - Terms of service

## Skill Metadata

- **Domain**: Legal
- **Complexity**: Beginner
- **Mode**: cyborg
- **Time to Value**: 15-30 min
- **Prerequisites**: Party information, context
