---
name: saas-legal-generator
description: Generate legal boilerplate documents for SaaS applications including Privacy Policy, Terms of Service, Cookie Policy, and GDPR/CCPA compliance. Use when launching new SaaS products or updating legal documents.
category: business
license: MIT
---

# SaaS Legal Boilerplate Generator

Generate legally compliant boilerplate documents for SaaS applications across
multiple jurisdictions (GDPR, CCPA, PIPEDA, LGPD).

**Important:** Templates are for informational purposes only. Always consult
with a qualified attorney for legal advice.

## Quick Start

### User Interactive Mode

Generate a complete legal package interactively:

```bash
cd skills/saas-legal-generator
npx -y bun scripts/index.ts
```

### Agent Mode

1. **Analyze**: Check user's source code/website to infer details (domain, tech
   stack, tracking).
2. **Prompt**: Ask user for key details (Company Name, Contact Email,
   Jurisdiction).
3. **Configure**: Create a config.json file with the details (see
   `example_config.json`).
4. **Generate**: Run `npx -y bun scripts/index.ts config.json`.

The generator prompts for:

1. Company details (name, domain, contact)
2. Service information (features, type)
3. Billing setup (plans, refund policy)
4. Data practices (collection, cookies)
5. Jurisdictions (GDPR, CCPA, PIPEDA, LGPD)
6. Third-party services (payment, hosting, analytics)

Output: Ready-to-use documents in `output/` directory.

## Context-Aware Adaptation

After generating the boilerplate, use the agent's capabilities to refine the
documents:

1. **Verify Tech Stack**:
   - Scan the project's package.json or source code for analytics tools (Google
     Analytics, Mixpanel), payment providers (Stripe), email services
     (SendGrid).
   - Update the _Third-Party Services_ section in the Privacy Policy
     accordingly.

2. **Check Tracking**:
   - Inspect website source or `index.html` for tracking scripts/pixels.
   - Update _Cookie Policy_ to reflect actual cookies used.

3. **Validate URLs**:
   - Ensure `[DOMAIN]` placeholders match the actual project URL.
   - Check if support/contact pages exist.

## Agent Usage Guidelines

- **Always prompt** the user for the "Company Name" and "Jurisdiction" if not
  explicitly stated.
- **Do not invent** legal contact emails; ask the user or default to
  `legal@[domain]`.
- **Review generated files**: After generation, do a quick read of the Markdown
  files to ensure no `[PLACEHOLDERS]` remain for critical fields.

## Document Types

### Privacy Policy

**When to use:** Any website/app collecting personal data

**Required sections:**

- Data collection practices
- Purpose of processing
- Legal basis (GDPR)
- Data subject rights
- International transfers
- Retention periods

**Jurisdictions:** Global + GDPR (EU) + CCPA (California) + PIPEDA (Canada)

### Terms of Service

**When to use:** Any web application or service

**Essential clauses:**

1. Service description and scope
2. User accounts and security
3. Payment terms and billing
4. Acceptable use policy
5. Intellectual property
6. **Limitation of liability** (crucial for SaaS)
7. Termination rights
8. Dispute resolution
9. Indemnification
10. Modification procedures

### Cookie Policy

**When to use:** Using cookies, tracking pixels, local storage

**Required by:** ePrivacy Directive (EU), CCPA (California)

**Categories:**

- Essential (authentication, security)
- Analytics (usage tracking)
- Functionality (preferences)
- Marketing (ad targeting)

### Data Processing Agreement (DPA)

**When to use:** Processing personal data on behalf of customers (GDPR
Article 28)

**Required clauses:**

- Processor acts on controller's instructions
- Confidentiality obligations
- Security measures
- Subprocessor approval
- Data subject rights assistance
- Breach notification (72 hours)

### CCPA "Do Not Sell" Opt-Out

**When to use:** California residents or targeting California market

**Required:**

- "Do Not Sell or Share My Personal Information" link in footer
- Consumer rights disclosure
- Opt-out mechanism
- Non-discrimination notice

## Core Workflows

### Workflow 1: Complete SaaS Launch Package

Generate all essential documents for a new SaaS product:

1. **Privacy Policy** - Global template with GDPR/CCPA addendums
2. **Terms of Service** - Service agreement with liability limitations
3. **Cookie Policy** - Tracking technology disclosure
4. **Acceptable Use Policy** - Usage guidelines
5. **Data Processing Agreement** - GDPR compliance (if processing user data)

**Run:** `npx -y bun scripts/index.ts`

### Workflow 2: GDPR Compliance Only

For European markets:

1. Privacy Policy (GDPR-compliant)
2. Cookie Policy (ePrivacy Directive)
3. Data Processing Agreement (Article 28)
4. Records of Processing Activities
5. Breach Notification Procedure

### Workflow 3: CCPA/CPRA Compliance

For California residents:

1. Privacy Policy (CCPA-compliant)
2. "Do Not Sell or Share" link
3. Consumer Rights Guide
4. Data Inventory Template

## Template Placeholders

All templates use placeholders replaced during generation:

| Placeholder        | Description           |
| ------------------ | --------------------- |
| `[COMPANY_NAME]`   | Legal business name   |
| `[DOMAIN]`         | Website domain        |
| `[CONTACT_EMAIL]`  | Privacy/legal contact |
| `[JURISDICTION]`   | Governing law         |
| `[EFFECTIVE_DATE]` | Document date         |
| `[CURRENCY]`       | Payment currency      |

## Jurisdiction Selection

Select based on target markets:

| Region         | Law       | Key Requirements                                    |
| -------------- | --------- | --------------------------------------------------- |
| European Union | GDPR      | Data subject rights, DPA, breach notification (72h) |
| California     | CCPA/CPRA | "Do Not Sell" link, consumer rights, opt-out        |
| Canada         | PIPEDA    | Consent, access, correction rights                  |
| Brazil         | LGPD      | Similar to GDPR, data subject rights                |
| United Kingdom | UK GDPR   | Post-Brexit, similar to EU GDPR                     |

## Deployment Requirements

### Website Footer (Required)

```html
<footer>
  <a href="/privacy">Privacy Policy</a>
  <a href="/terms">Terms of Service</a>
  <a href="/cookies">Cookie Policy</a>
  <a href="/do-not-sell">Do Not Sell or Share</a>
  <!-- CCPA required -->
</footer>
```

### Cookie Consent Banner (GDPR Required)

```html
<div id="cookie-banner">
  <p>
    We use cookies. By continuing, you agree to our
    <a href="/cookies">Cookie Policy</a>.
  </p>
  <button onclick="acceptEssential()">Accept Essential</button>
  <button onclick="acceptAll()">Accept All</button>
</div>
```

## Common Mistakes to Avoid

❌ **Copy-pasting without customization** - Adapt to your specific data
practices ❌ **One-size-fits-all** - Different jurisdictions need different
terms ❌ **Ignoring updates** - Laws change regularly ❌ **Buried clauses** -
Make key terms prominent ❌ **Overreaching disclaimers** - Unenforceable clauses
undermine credibility

## Best Practices

1. **Keep documents current** - Review at least annually
2. **Make accessible** - Link from footer, no login gate
3. **Track consent** - Record timestamps and IP addresses
4. **Maintain records** - Document processing activities
5. **Prepare for enforcement** - Designate DPO, establish breach response

## Maintenance Schedule

**Quarterly:**

- Review data collection changes
- Update vendor/subprocessor lists
- Check for law changes

**Annually:**

- Full document review
- Update effective dates
- Audit consent mechanisms

**As Needed:**

- Immediate update for major law changes
- Update when adding new data-intensive features
- Revise when expanding to new markets

## Validation Checklist

Before deploying legal documents, verify:

- [ ] All placeholder text replaced
- [ ] Jurisdictions match target markets
- [ ] Data collection accurately described
- [ ] User rights clearly explained
- [ ] Contact information current
- [ ] Links work from footer
- [ ] Document accessible (not login-gated)
- [ ] Reviewed by attorney (recommended)
- [ ] Translated for non-English markets

## Resources

- **templates/** - Complete document templates by jurisdiction
  - [privacy-policy-global.md](templates/privacy-policy-global.md)
  - [terms-of-service-saas.md](templates/terms-of-service-saas.md)
  - [cookie-policy.md](templates/cookie-policy.md)
  - [acceptable-use-policy.md](templates/acceptable-use-policy.md)
  - [data-processing-agreement.md](templates/data-processing-agreement.md)
  - [ccpa-opt-out-link.md](templates/ccpa-opt-out-link.md)
- **scripts/index.ts** - Interactive generation script
- **example_config.json** - Non-interactive generation input
- **output/** - Generated document examples

## Important Disclaimer

**These templates are for informational purposes only and do not constitute
legal advice.** Laws vary by jurisdiction and change frequently. Always consult
with a qualified attorney to review your legal documents before publication.

## Sources

- [GDPR Full Text and Recitals](https://gdpr-info.eu/)
- [CCPA/CPRA Overview | California DOJ](https://oag.ca.gov/privacy/ccpa)
- [UK GDPR Guidance | ICO](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/)
- [EDPB Guidelines](https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines_en)
