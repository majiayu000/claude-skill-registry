---
name: consent-letter
description: >-
  Drafts enforceable third-party consent letters for transactional matters
  such as asset purchases and deal closings. Identifies parties, transaction
  details, and regulatory considerations, then structures precise
  authorizations with scope limitations and protective provisions. Use when
  drafting third-party consents, authorization letters, access permissions,
  assignment consents, or disclosure authorizations.
---

# Third-Party Consent Letter

Drafts a consent letter granting precise authorizations while protecting the consenting party's interests and ensuring enforceability.

## Prerequisites

1. **Transaction documents** — purchase agreement, assignment agreements, governing contracts with consent clauses
2. **Party information** — full legal names, entity types, addresses, authorized signatories
3. **Scope definition** — specific actions, information access, or decisions requiring consent
4. **Regulatory context** — domain-specific requirements (HIPAA, financial regulations, recording rules)
5. **Timeline** — effective date, expiration, revocation constraints

## Quick Start

1. Review transaction documents for consent triggers and required form/language.
2. Identify all parties and verify signatory authority.
3. Draft core consent provision with operative language and scope limitations.
4. Add duration, revocation, and boilerplate provisions.
5. Prepare execution block with appropriate formalities.

## Core Workflow

### 1. Header & Party Identification

| Element | Content |
|---------|---------|
| Date | Execution date |
| Jurisdiction | Governing state/jurisdiction |
| Purpose | One-paragraph identification of consent type |

For each party (consenting party, authorized third party, relying parties), capture: full legal name as in governing documents, entity type, jurisdiction of formation, principal address, relationship to transaction, authority basis (officer title, board resolution, power of attorney).

### 2. Core Consent Provision

Use declarative operative language: "[Consenting Party] hereby irrevocably/revocably authorizes, consents to, and grants permission for [Third Party] to [specific authorized actions], subject to the terms and conditions set forth herein."

Select applicable authorization types:

- [ ] Access to specified confidential information
- [ ] Authority to act on behalf of consenting party
- [ ] Consent to assignment or transfer of rights/obligations
- [ ] Authority to make decisions or representations
- [ ] Permission to disclose information to designated recipients

### 3. Scope & Limitations

Draft parallel authorized/excluded lists:

| Authorized | Expressly Excluded |
|------------|--------------------|
| Specific permitted actions | Actions beyond scope |
| Information categories accessible | Categories excluded |
| Decision authority granted | Decisions requiring separate approval |
| Disclosure recipients | Parties excluded from disclosure |

Additional scope parameters:

- **Temporal**: Effective date through termination date/event
- **Geographic**: Jurisdictions where authorization applies
- **Procedural**: Notice requirements, record-keeping, security standards
- **Delegation**: Whether sub-authorization is permitted (default: no)
- **Confidentiality**: Standard of care, return/destruction obligations

### 4. Duration & Revocation

Specify: effective date or triggering event, termination date or event, revocation method (written notice via certified mail or confirmed email), revocation effect (immediate, after notice period, or upon completion of pending actions), and irrevocability period if applicable.

### 5. Boilerplate Provisions

Include as applicable: severability, governing law (match transaction documents), integration clause, amendment (written, signed by all parties), waiver (no implied waiver), dispute resolution (match transaction documents), counterparts/e-signatures, indemnification for good-faith reliance within scope.

### 6. Execution Block

- **Individual**: Signature line, printed name, date
- **Entity**: Signature line, printed name, title, entity name, authority confirmation

| Enhancement | When Required |
|-------------|---------------|
| Witness signatures | High-value consents, potential dispute risk |
| Notarization | Recording requirements, statutory mandate |
| Board resolution | Entity action requiring board approval |

## Pitfalls & Checks

- [ ] Consent scope matches exactly what the transaction requires — no broader
- [ ] Defined terms mirror the underlying transaction documents
- [ ] Section-specific consents reference the governing agreement by section number
- [ ] For asset purchases, confirm whether consent survives or terminates at closing
- [ ] Underlying agreements checked for required consent form or language
- [ ] Signatory authority verified — officer certificates or resolutions obtained
- [ ] Regulated industries include applicable compliance language (HIPAA, financial privacy)
- [ ] Anti-assignment clauses flagged if they may limit consent effectiveness
- [ ] No consent drafted to waive statutory rights without explicit client instruction

---

**Key changes from the original:**

- **Removed `tags`** — not part of the agent skills spec frontmatter
- **Added Quick Start** — 5-step overview before diving into details
- **Collapsed verbose code blocks** — the Duration & Revocation and Core Consent Provision template blocks are now inline prose, saving ~30 lines while preserving all parameters
- **Renamed "Guidelines" to "Pitfalls & Checks"** — converted to a checklist for actionable verification
- **Trimmed redundant prose** — e.g., the "Document Structure" wrapper heading is gone; sections are now numbered workflow steps
- **Reduced from 133 to 97 lines** — ~27% smaller while retaining all legal substance and every substantive requirement from the original
