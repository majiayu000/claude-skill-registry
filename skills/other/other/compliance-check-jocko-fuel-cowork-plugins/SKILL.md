---
name: compliance-check
description: Check security compliance against standards and regulations
user-invocable: true
---

You are helping the team verify Jocko Fuel's compliance against security standards.

Follow these steps:

### Step 1: Select Compliance Framework

Ask the user which standard(s) to check:
- **PCI DSS**: Payment card data handling (relevant for Shopify payments)
- **SOC 2 Type II**: Service organization controls
- **GDPR**: EU data protection (if serving EU customers)
- **CCPA/CPRA**: California consumer privacy
- **General best practices**: CIS benchmarks, NIST CSF

If the user isn't sure, recommend starting with PCI DSS (e-commerce) and CCPA (California-based company).

### Step 2: Gather Evidence

Delegate to the `compliance-auditor` agent to collect:
- Current security policies and documentation
- Technical control implementations
- Access control configurations
- Data handling and retention practices
- Incident response procedures
- Employee training records

### Step 3: Assess Controls

For each control area in the selected framework, evaluate:
- **Implemented**: Control is in place and functioning
- **Partially implemented**: Control exists but has gaps
- **Not implemented**: Control is missing
- **Not applicable**: Control doesn't apply to the organization

### Step 4: Generate Gap Analysis

Present a compliance report with:
- **Overall compliance score** (% of controls met)
- **Gap analysis table**: Each control, status, and remediation needed
- **High-priority gaps**: Controls that pose the most risk if unmet
- **Remediation roadmap**: Prioritized plan to close gaps
- **Evidence inventory**: What documentation exists vs. what's needed

### Error Handling

- If the organization lacks formal security policies, recommend establishing baseline policies first
- If a framework is too extensive for current maturity, suggest starting with a subset of critical controls
- If compliance requires third-party attestation, note which items need external validation
