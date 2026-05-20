---
name: coverage
description: Generate Coverage and insurance resources with payer diversity including Medicare, Medicaid, commercial, Tricare, VA, and self-pay. Use when user mentions coverage, insurance, payer, Medicare, Medicaid, benefits, or coordination of benefits. For claims and EOB see the claims-eob skill.
keywords: [coverage, insurance, payer, Medicare, Medicaid, commercial, BCBS, Aetna, UHC, Cigna, Tricare, VA, self-pay, uninsured, workers comp, beneficiary, subscriber, coordination of benefits]
resource_types: [Coverage, Organization]
always: false
---

# Coverage and Insurance

Model payer diversity:
- Coverage resource: Include subscriber, beneficiary, payor references.
- Payer types: Medicare (Part A, B, C, D), Medicaid, Commercial (BCBS, Aetna, UHC, Cigna),
  Tricare, VA, Self-pay/uninsured, Workers' Comp.
- Class: group, plan, subplan, class, subclass, sequence.
- Include Coverage.type codes from http://terminology.hl7.org/CodeSystem/v3-ActCode:
  EHCPOL (employee healthcare), PUBLICPOL (public policy), SUBSIDIZ, MANDPOL.
- Period: coverage start/end dates, with some patients having gaps in coverage.
- Include patients with multiple coverages (primary/secondary coordination).

