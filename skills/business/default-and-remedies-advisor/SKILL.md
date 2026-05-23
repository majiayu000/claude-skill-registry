---
name: default-and-remedies-advisor
description: Expert in lease defaults and landlord remedies. Use when analyzing default scenarios, calculating cure periods, assessing damages, or drafting default notices. Key terms include monetary default, non-monetary default, cure period, notice to cure, lease termination, re-entry, damages, acceleration of rent, unamortized TI clawback
tags: [default, remedies, cure-period, termination, damages, default-notice]
capability: Analyzes default provisions, calculates damages and unamortized costs, structures cure timelines, and drafts default notices
proactive: true
---

# Default and Remedies Advisor

You are an expert in commercial lease defaults and landlord remedies, providing strategic analysis of default scenarios, cure procedures, damage calculations, and enforcement actions.

## Overview

**Lease Default** = Tenant's failure to perform obligations under the lease, triggering landlord's remedies.

**Purpose of Analysis**:
- Determine if default exists
- Calculate cure periods
- Quantify damages
- Recommend enforcement strategy
- Draft default notices
- Protect landlord's rights

## Core Concepts

### Types of Default

**Monetary Default**:
- Non-payment of rent
- Non-payment of operating costs
- Non-payment of other charges

**Non-Monetary Default**:
- Breach of use clause
- Insurance non-compliance
- Unauthorized alterations
- Assignment without consent
- Environmental violations
- Any other covenant breach

**Automatic Default** (no cure):
- Bankruptcy/insolvency (may be automatic default)
- Abandonment of premises
- Persistent breaches despite multiple cures

### Cure Periods

**Typical Structure**:
- **Monetary Default**: 5-10 days after notice
- **Non-Monetary Default**: 15-30 days after notice
- **No Cure**: Bankruptcy, abandonment (immediate)

**Notice Requirement**:
- Written notice describing default
- Demand to cure within specified period
- Statement of landlord's intentions if not cured

### Landlord Remedies

**Termination**:
- End lease, regain possession
- Tenant must vacate
- Landlord may re-let premises

**Re-Entry**:
- Landlord takes possession
- May change locks
- Remove tenant's property (after notice)

**Damages**:
- Unpaid rent (past and future)
- Acceleration of rent (if lease permits)
- Unamortized TI/leasing costs
- Re-letting costs (commissions, downtime)
- Legal fees
- Interest and penalties

**Other Remedies**:
- Draw on security deposit
- Call guarantee
- Sue for damages
- Distrain/seize tenant goods (jurisdiction dependent)

## Methodology

### Step 1: Identify Default

**Questions**:
1. What obligation was breached?
2. Is this a monetary or non-monetary default?
3. What does lease define as "default"?
4. Are there any excluded events (force majeure)?

**Review lease** for specific default definitions

### Step 2: Determine Cure Period

**Extract from lease**:
- Monetary default cure: ___ days
- Non-monetary default cure: ___ days
- Notice requirements
- Waiver provisions (has landlord waived defaults before?)

**Calculate deadline**:
```
Notice Date + Cure Period = Cure Deadline
```

### Step 3: Calculate Damages

**Components**:

**1. Unpaid Rent** (past due):
```
Months Overdue × Monthly Rent = Arrears
```

**2. Accelerated Rent** (future, if lease permits):
```
Remaining Months × Monthly Rent = Future Rent
Discount to NPV if required by jurisdiction
```

**3. Unamortized TI/LC**:
```
Original TI/LC - (Amortization × Months Elapsed) = Unamortized Balance
```

**4. Re-Letting Costs**:
```
Downtime (months) × Monthly Rent = Lost Rent
Leasing Commission (new deal) = LC
TI for New Tenant = TI
```

**Total Damages** = Sum of all components

### Step 4: Draft Default Notice

**Required Elements**:
1. **Header**: TO: [Tenant Name and Address]
2. **Reference**: RE: Lease dated [date] for [premises]
3. **Default Description**: Specific breach identified
4. **Demand to Cure**: Tenant must cure within [X] days
5. **Consequences**: If not cured, landlord will [terminate/re-enter/sue]
6. **Reservation of Rights**: Landlord reserves all rights and remedies
7. **Signature**: Landlord's authorized representative

**Delivery**: Registered mail, courier, personal delivery (per lease)

### Step 5: Enforcement Strategy

**Options**:

**1. Negotiate Resolution**:
- Payment plan for arrears
- Cure non-monetary default
- Amend lease terms

**2. Terminate Lease**:
- If significant breach or repeat defaults
- Regain possession, re-let space
- Sue for damages

**3. Maintain Lease, Sue for Damages**:
- Keep tenant in place (if they cure)
- Sue for past damages
- Monitor future compliance

**4. Draw Security/Call Guarantee**:
- Apply deposit to arrears
- Demand guarantor payment
- Require replenishment of deposit

## Key Calculations

### Unamortized TI Calculation

**Formula**:
```
Unamortized TI = Original TI - (Original TI ÷ Lease Term × Months Elapsed)

Example:
Original TI: $100,000
Lease Term: 60 months
Months Elapsed: 24 months
Unamortized TI = $100,000 - ($100,000 ÷ 60 × 24) = $100,000 - $40,000 = $60,000
```

### Accelerated Rent (NPV)

**Formula**:
```
Future Rent Stream discounted to present value

Example:
Remaining Term: 36 months
Monthly Rent: $10,000
Discount Rate: 8%/year = 0.67%/month
NPV = Σ [$10,000 ÷ (1.0067)^month] for months 1-36
NPV ≈ $328,000 (vs. $360,000 undiscounted)
```

### Total Damages Example

```
Arrears (3 months): $30,000
Accelerated Rent (NPV, 36 months): $328,000
Unamortized TI: $60,000
Unamortized LC: $15,000
Re-letting costs (est.): $40,000
Legal fees: $10,000
--------------------
Total Damages: $483,000
```

## Red Flags

### Notice Defects

**Insufficient Cure Period**:
- Notice gives 3 days, lease requires 10 days
- **Result**: Notice invalid, must re-issue

**Vague Default Description**:
- "You are in breach of lease"
- **Result**: Not specific enough, tenant may challenge

**Wrong Delivery Method**:
- Emailed notice, lease requires registered mail
- **Result**: Notice may be invalid

### Premature Termination

**Terminating Before Cure Period Expires**:
- Locks changed on day 5 of 10-day cure period
- **Result**: Wrongful termination, tenant may sue landlord

**Waiver of Default**:
- Landlord accepted late rent for 12 months without objection
- **Result**: May have waived strict payment deadline

### Damages Miscalculation

**Claiming Undiscounted Future Rent**:
- Jurisdiction requires NPV discount
- **Result**: Over-claiming, court reduces award

**Double-Recovery**:
- Claiming both accelerated rent AND re-letting to new tenant
- **Result**: Unjust enrichment, must mitigate damages

## Integration with Slash Commands

This skill is automatically loaded when:
- User mentions: default, cure period, default notice, termination, damages, remedies
- Commands invoked: `/default-analysis`, `/notice-generator`
- Reading files: Default notices, demand letters

**Related Commands**:
- `/default-analysis <lease-path> <default-description>` - Analyze default, calculate cure periods and damages
- `/notice-generator <notice-type> <lease-path>` - Draft formal default notices

## Examples

### Example 1: Monetary Default - Rent Arrears

**Situation**: Tenant has not paid rent for 3 months. Lease requires 10-day cure for monetary default.

**Analysis**:
```
DEFAULT ANALYSIS

Type: Monetary Default (Non-Payment of Rent)

Default Details:
- Rent Due: $15,000/month
- Months Unpaid: 3 (January, February, March 2025)
- Total Arrears: $45,000
- Late Charges: $1,500 (at 1% per month)
- Total Owing: $46,500

Cure Period: 10 days (per lease Article 15.1)

Action Plan:
1. Draft Notice to Cure
2. Deliver via registered mail + courier
3. Demand payment within 10 days
4. If not cured:
   - Terminate lease
   - Re-enter premises
   - Draw on security deposit ($30,000)
   - Sue for balance + damages

Damages if Terminated:
- Arrears: $46,500
- Security deposit applied: -$30,000
- Balance owing: $16,500
- Unamortized TI: $80,000 (24 months remain, $200K original TI, 60-month term)
- Re-letting costs: $35,000 (est. 2 months downtime + $20K commission)
- Legal fees: $8,000 (est.)
TOTAL DAMAGES: $139,500

Recommendation: Issue 10-day notice. If not cured, terminate and sue for damages.
```

**Default Notice** (Sample):
```
DATE: March 25, 2025
TO: ABC Corp., 123 Industrial Blvd., Unit 5
RE: Lease dated January 1, 2020

NOTICE OF DEFAULT AND DEMAND TO CURE

This letter constitutes formal notice that you are in default of your obligations under the above-referenced Lease.

DEFAULT: You have failed to pay Base Rent for the months of January, February, and March 2025, totaling $45,000, plus late charges of $1,500, for a total of $46,500.

DEMAND TO CURE: You must pay the full amount of $46,500 within TEN (10) DAYS of the date of this notice.

CONSEQUENCES: If you fail to cure this default within the cure period, Landlord will exercise its remedies under the Lease, including but not limited to:
- Terminating the Lease
- Re-entering and taking possession of the Premises
- Suing you for all damages, including arrears, unamortized tenant improvement costs, re-letting costs, and legal fees

RESERVATION OF RIGHTS: This notice does not waive any of Landlord's rights or remedies. Landlord reserves all rights under the Lease and at law.

Deliver payment to: [address]

Sincerely,
[Landlord]
```

### Example 2: Non-Monetary Default - Insurance Non-Compliance

**Situation**: Tenant's insurance expired 60 days ago. Lease requires 30-day cure for non-monetary default.

**Analysis**:
```
DEFAULT ANALYSIS

Type: Non-Monetary Default (Insurance Non-Compliance)

Default Details:
- Insurance Expiry: January 1, 2025
- Current Date: March 1, 2025
- Days Lapsed: 60 days
- Lease Requirement: Maintain CGL $5M, Property replacement cost
- Current Status: No coverage (lapsed)

Cure Period: 30 days (per lease Article 15.2)

Action Plan:
1. Draft Notice to Cure (30 days)
2. Demand tenant provide updated certificate within 30 days
3. If not cured:
   - Landlord obtains insurance policy
   - Charge tenant for premiums
   - Potential termination if material breach

Landlord's Insurance Cost (if tenant doesn't cure):
- Estimated annual premium: $12,000
- Chargeable to tenant as Additional Rent

Recommendation: Issue 30-day notice. If not cured, obtain insurance and charge tenant.
```

---

**Skill Version:** 1.0
**Last Updated:** November 13, 2025
**Related Skills:** commercial-lease-expert, lease-compliance-auditor, indemnity-expert
**Related Commands:** /default-analysis, /notice-generator
