---
name: deal-structuring
description: Deal structuring patterns for secured lending, intercreditor arrangements, and investment structuring. Covers UCC liens, collateral packages, and covenant structures.
---

# Deal Structuring Skill

Patterns and best practices for structuring investment and lending transactions.

## Security Package Design

### Collateral Types

| Type | Perfection | Priority | Considerations |
|------|------------|----------|----------------|
| Accounts Receivable | UCC-1 filing | First-to-file | Quality, concentration |
| Inventory | UCC-1 filing | First-to-file | Turnover, valuation |
| Equipment | UCC-1 filing | PMSI possible | Age, condition, FMV |
| Real Property | Mortgage/Deed of Trust | Recording date | Title, environmental |
| IP/Licenses | UCC-1 + specific | Varies | Transferability |
| Equity Interests | UCC-1 or control | Control preferred | Governance rights |
| Deposit Accounts | Control agreement | Control required | Bank cooperation |

### Advance Rates

Typical advance rates against collateral:

| Collateral | Standard Rate | Conservative Rate |
|------------|---------------|-------------------|
| Eligible A/R | 80-85% | 70-75% |
| Eligible Inventory | 50-60% | 40-50% |
| Equipment (OLV) | 70-80% | 60-70% |
| Real Estate | 65-75% | 55-65% |
| Cannabis Inventory | 40-50% | 30-40% |

### Eligibility Criteria

```markdown
Eligible Accounts Receivable:
- [ ] Less than 90 days past invoice date
- [ ] No concentration > 15% from single debtor
- [ ] Not contra or intercompany
- [ ] No government accounts (unless assigned)
- [ ] Debtor not bankrupt or insolvent
- [ ] No disputes or offsets claimed

Eligible Inventory:
- [ ] Located at approved locations
- [ ] Not consigned or on memo
- [ ] Saleable in ordinary course
- [ ] Covered by insurance
- [ ] Not obsolete or slow-moving
- [ ] Proper title documentation
```

## UCC Lien Perfection

### Filing Strategy

```
Priority of Perfection Methods:
1. Control (highest for deposit accounts, securities)
2. Possession (for certificated securities, negotiable instruments)
3. Filing (general collateral)
4. Automatic (certain purchase-money situations)
```

### Collateral Description Best Practices

```
GOOD (Specific):
"All equipment listed on Schedule A attached hereto, including
all attachments, accessories, and proceeds thereof."

GOOD (Blanket):
"All assets and personal property of every kind and nature,
whether now owned or hereafter acquired, including but not
limited to all accounts, inventory, equipment, general
intangibles, deposit accounts, investment property, and
all proceeds and products of the foregoing."

BAD (Too Vague):
"Business assets"
"Collateral as defined in loan agreement"
```

### Search and Filing Checklist

```markdown
Pre-Closing Search:
- [ ] UCC search in state of organization
- [ ] UCC search in states where assets located
- [ ] Tax lien search (federal and state)
- [ ] Judgment lien search
- [ ] Fixture filing search (if applicable)
- [ ] IP filings (USPTO, Copyright Office)

Filing Checklist:
- [ ] Debtor name matches exactly with Secretary of State
- [ ] Secured party name and address correct
- [ ] Collateral description comprehensive
- [ ] Authorization obtained (authenticated security agreement)
- [ ] Filing fee paid
- [ ] Acknowledgment copy received
- [ ] Follow-up search to confirm filing
```

## Intercreditor Agreements

### Standard Provisions

```markdown
1. DEFINITIONS
   - Senior Debt, Junior Debt
   - Collateral Pool
   - Enforcement Action
   - Standstill Period

2. LIEN PRIORITY
   - Clear statement of priority
   - Sharing or separate pools
   - Future advances treatment

3. PAYMENT PRIORITY
   - Waterfall structure
   - Blockage provisions
   - Permitted payments to junior

4. STANDSTILL
   - Trigger events
   - Duration (90-180 days typical)
   - Junior cure rights

5. ENFORCEMENT
   - Senior controls process
   - Junior right to participate
   - Sale free and clear provisions

6. RELEASE AND AMENDMENTS
   - Conditions for collateral release
   - Amendment requirements
   - Joinder provisions

7. PURCHASE OPTION
   - Junior right to buy senior debt
   - Exercise period and mechanics
   - Pricing (usually par + accrued)
```

### Key Negotiating Points

| Issue | Senior Position | Junior Position |
|-------|-----------------|-----------------|
| Standstill Period | 180 days minimum | 90 days maximum |
| Payment Blockage | Automatic on default | Only on payment default |
| Purchase Option | Par + premium | Par flat |
| Amendment Rights | Consent required | Reasonable consent |
| Cross-Default | Broad triggers | Narrow triggers |

## Covenant Structures

### Financial Covenants

```markdown
Maintenance Covenants (tested quarterly):
1. Minimum DSCR: 1.25x
2. Maximum Total Leverage: 4.0x
3. Minimum Liquidity: $X
4. Maximum CapEx: $X per year

Incurrence Covenants (tested at incurrence):
1. Pro forma leverage for new debt
2. Pro forma coverage for distributions
3. Asset sale reinvestment requirements
```

### Reporting Covenants

```markdown
Monthly Deliverables (within 30 days):
- Financial statements (unaudited)
- Covenant compliance certificate
- A/R and A/P aging
- Inventory report
- Bank statements

Quarterly Deliverables (within 45 days):
- Management discussion and analysis
- Updated projections
- Collateral value report

Annual Deliverables (within 120 days):
- Audited financial statements
- Tax returns
- Insurance certificates
- UCC search updates
```

### Negative Covenants

```markdown
Standard Restrictions:
- No debt without consent
- No liens without consent
- No sale of assets outside ordinary course
- No change of control
- No dividends/distributions (or limited basket)
- No capital expenditures above threshold
- No transactions with affiliates
- No changes to fiscal year or accounting methods
- Maintenance of existence and licenses
```

## Equity Investment Structures

### Preferred Equity Terms

```markdown
Liquidation Preference:
- 1.0x non-participating (standard)
- 1.0x participating (more investor-friendly)
- Multiple (2x, 3x for higher-risk deals)

Dividend Rights:
- Cumulative vs. non-cumulative
- PIK (payment-in-kind) vs. cash pay
- Typical rate: 8-12% annually

Conversion Rights:
- Optional conversion to common
- Mandatory conversion triggers
- Anti-dilution protection (weighted average vs. full ratchet)

Protective Provisions:
- Board seat(s)
- Consent rights on major decisions
- Information rights
- Pre-emptive rights
```

### Common Equity Terms

```markdown
Vesting Schedule:
- 4-year vesting with 1-year cliff (standard)
- Monthly vesting after cliff
- Acceleration on change of control

Tag-Along Rights:
- Right to participate in founder/majority sale
- Pro rata basis
- Same terms as selling shareholder

Drag-Along Rights:
- Majority can force sale
- Threshold typically 60-75%
- Fair value floor

ROFR/ROFO:
- Right of first refusal on transfers
- Right of first offer on new issuances
- Waiver mechanics
```

## Risk Mitigation Strategies

### Deal Structure Risk Mitigants

| Risk | Mitigant | Implementation |
|------|----------|----------------|
| Payment Default | Debt service reserve | 3-6 months PITI |
| Collateral Decline | Borrowing base limits | Monthly re-certification |
| Concentration | Limits on single exposure | 15-25% cap |
| Key Person | Life/disability insurance | Coverage = loan amount |
| Business Interruption | BI insurance | 12-month coverage |
| Environmental | Phase I/II, insurance | Remediation fund |
| Regulatory | License protection | Step-in rights |

### Documentation Risk Management

```markdown
Opinion Requirements:
- [ ] Corporate authority and due execution
- [ ] Enforceability of loan documents
- [ ] Perfection of security interests
- [ ] No conflicts with organizational documents
- [ ] Regulatory compliance (cannabis specific)

Title/Survey Requirements:
- [ ] ALTA policy with endorsements
- [ ] Survey dated within 90 days
- [ ] Zoning report
- [ ] Flood zone determination
```
