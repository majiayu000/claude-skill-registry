---
name: universal
description: '> Style/formatting: Follow ~/.claude/skills/word-doc-generator/SKILL.md'
---

# PEP STATUS SECTION

> **Style/formatting:** Follow `~/.claude/skills/word-doc-generator/SKILL.md`

## Purpose

Politically Exposed Person assessment. Determines PEP classification, level, and associated risks.

---

## TEMPLATE

```markdown
## Political Exposure

[IF NOT PEP:]
### PEP Screening

**[SUBJECT]** was screened against PEP databases and public records. No political exposure was identified. **[SUBJECT]** does not appear to hold or have held a prominent public function, nor to be a close family member or associate of a PEP.

[IF PEP:]
### PEP Classification

**[SUBJECT]** is classified as a Politically Exposed Person (PEP).

| Field | Details |
|-------|---------|
| **PEP Type** | [Domestic / Foreign / International Organization] |
| **PEP Level** | [PEP1 (direct) / PEP2 (family/associate)] |
| **Category** | [Head of State / Minister / Parliamentarian / etc.] |
| **Position** | [SPECIFIC ROLE] |
| **Jurisdiction** | [COUNTRY] |
| **Tenure** | [START DATE] - [END DATE / Present] |
| **Status** | [Current / Former] |

### Political Roles

| Period | Position | Institution | Jurisdiction |
|--------|----------|-------------|--------------|
| [DATES] | [ROLE] | [INSTITUTION] | [COUNTRY] |
| [DATES] | [ROLE] | [INSTITUTION] | [COUNTRY] |

### Political Affiliations

**[SUBJECT]** is affiliated with [PARTY NAME], [DESCRIPTION OF PARTY].[^X]

[IF FAMILY/ASSOCIATE PEP:]
### PEP Association

**[SUBJECT]** is classified as a PEP associate due to [his/her] relationship with **[PEP NAME]**, [PEP ROLE].[^X]

| Related PEP | Relationship | PEP Role |
|-------------|--------------|----------|
| **[NAME]** | [Spouse / Parent / Child / Business associate] | [ROLE] |

### Risk Considerations

[SELECT APPLICABLE:]

**Corruption Risk:**
> [COUNTRY] is ranked [RANK] out of [TOTAL] countries on Transparency International's Corruption Perceptions Index [YEAR], indicating [high / moderate / low] corruption risk.[^X]

**Sanctions Nexus:**
> [COUNTRY/REGIME] is subject to international sanctions. **[SUBJECT]**'s political role may expose [him/her] to sanctions risk.

**State-Owned Enterprises:**
> **[SUBJECT]**'s role at [STATE ENTITY] creates potential exposure to state-controlled enterprises.

**Defense/Security:**
> **[SUBJECT]** has held positions in [defense / security / intelligence], which may attract heightened scrutiny.
```

---

## RULES

### MUST Include
- Clear PEP/Non-PEP determination
- For PEPs: Category, level, role, dates
- For PEP associates: Relationship to PEP
- Risk context (TI ranking, sanctions status)

### MUST NOT
- Classify as PEP without clear evidence
- Omit tenure dates for political roles
- Fail to distinguish current vs former PEP
- Miss family/associate PEP status

---

## PEP CATEGORIES

### Tier 1 - Highest Risk

| Category | Examples |
|----------|----------|
| **Head of State/Government** | President, Prime Minister, Monarch |
| **Senior Government** | Cabinet Ministers, Deputy Ministers |
| **Senior Judiciary** | Supreme Court, Constitutional Court |
| **Senior Military** | General officers, Intelligence chiefs |
| **Central Bank** | Governor, Board members |
| **State Enterprise** | CEO/Chairman of major SOEs |
| **International Organizations** | UN, IMF, World Bank senior officials |

### Tier 2 - High Risk

| Category | Examples |
|----------|----------|
| **Parliamentarians** | MPs, Senators, Legislators |
| **Regional Government** | Governors, Mayors of major cities |
| **Senior Diplomats** | Ambassadors, Consul Generals |
| **Political Party** | Party leaders, senior officials |
| **Regulators** | Heads of regulatory agencies |

### Tier 3 - Moderate Risk

| Category | Examples |
|----------|----------|
| **Mid-level Officials** | Director-level, department heads |
| **Local Government** | Local council members |
| **Former PEPs** | Depending on time since leaving office |
| **PEP Associates** | Family members, close business associates |

---

## STANDARD PHRASES

**Current PEP:**
> **[SUBJECT]** is a current Politically Exposed Person, serving as [ROLE] of [INSTITUTION] since [DATE].

**Former PEP:**
> **[SUBJECT]** is a former PEP, having served as [ROLE] from [DATE] to [DATE]. [He/She] left office [X] years ago.

**Family member PEP:**
> **[SUBJECT]** is the [spouse / child / parent] of **[PEP NAME]**, [PEP ROLE], and is therefore classified as a PEP family member.

**Close associate PEP:**
> **[SUBJECT]** is classified as a PEP close associate due to [his/her] documented business relationship with **[PEP NAME]**.

**Not a PEP:**
> No political exposure was identified for **[SUBJECT]**. [He/She] does not appear to be a PEP or PEP associate.

**High-risk jurisdiction:**
> **[SUBJECT]**'s political role in [COUNTRY], combined with the jurisdiction's [high corruption risk / weak governance], warrants enhanced scrutiny.

---

## PEP TIMEFRAMES

| Jurisdiction | PEP Period After Leaving Office |
|--------------|--------------------------------|
| **FATF Guidance** | Minimum 12 months, risk-based beyond |
| **UK (FCA)** | Risk-based, no fixed period |
| **EU (4AMLD)** | 12 months minimum |
| **US (FinCEN)** | Risk-based, no fixed period |
| **Singapore (MAS)** | 12 months minimum |

---

## DISCLAIMER

> PEP status is determined based on available public information and screening databases. Classification may differ between institutions based on their risk appetite and regulatory requirements.

---

## FOOTNOTE FORMAT

**See `word-doc-generator/SKILL.md`** - URL-only footnotes.
