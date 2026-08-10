---
name: privacy-policy-drafting
description: Draft privacy-policy language and a review checklist tailored to a business model, data practices, and relevant jurisdictions. Use when the user requests a privacy policy or needs to map disclosures for GDPR, CCPA, or similar frameworks; do not use it to guarantee legal compliance.
license: MIT
metadata:
  author: community
  version: "1.0"
---

# Privacy Policy Drafting

Draft legally informed privacy-policy language that addresses potentially applicable privacy frameworks and exposes unresolved business inputs. Treat the result as a working draft and review checklist, not proof of compliance. Verify current law, regulator guidance, product behavior, and jurisdiction with qualified counsel before publication.

## Workflow

1. **Gather Business Information** — Collect details about the business entity (name, jurisdiction, contact info), the product or service offered, target user demographics, and geographic reach. Determine which regulations apply based on where users are located, not just where the business is incorporated. A US-based SaaS serving EU customers must address GDPR.

2. **Identify Data Collection Practices** — Map every category of personal data collected: direct inputs (forms, account creation), automatic collection (cookies, analytics, device info, IP addresses), third-party sources (OAuth providers, data brokers), and derived data (usage patterns, preferences). For each category, document the collection method, storage location, retention period, and whether it includes sensitive/special category data.

3. **Map Legal Requirements** — Cross-reference collected data types against applicable frameworks. GDPR requires lawful basis for each processing activity, CCPA requires disclosure of sale/sharing practices and opt-out mechanisms, COPPA applies if users under 13 may access the service, and sector-specific rules (HIPAA, FERPA, GLBA) may layer additional requirements. Identify all required policy sections.

4. **Draft Policy Sections** — Generate each section with plain-language explanations alongside legally precise disclosures. Required sections include: data collected and purposes, legal basis for processing (GDPR), data sharing and third parties, cookies and tracking technologies, data retention, user rights and how to exercise them, international data transfers, children's privacy, security measures, and policy change notification procedures.

5. **Review for Compliance Gaps** — Audit the draft against a regulatory checklist. Verify that every data processing activity has a stated legal basis, all required rights are enumerated, contact information for DPO or privacy inquiries is included, cookie consent mechanisms are described, and data breach notification procedures are referenced. Flag any gaps or areas needing business input.

## Usage

Describe your business, what data you collect, and which jurisdictions your users are in. Include technical details about cookies, analytics tools, and third-party integrations.

**Example prompt:**
```
Draft a privacy policy for my SaaS app "TaskFlow" — a project management tool. We collect email, name, and usage analytics via Mixpanel. Users are in the US and EU. We use Stripe for payments and Google OAuth for login.
```

## Examples

### Example 1: SaaS App with Email and Usage Data

**Input:** TaskFlow, a project management SaaS. Collects email, name, profile photo, usage analytics (Mixpanel), payment info (Stripe), Google OAuth login. Users in US and EU.

**Output (key sections):**

**Information We Collect**

*Information you provide:* When you create an account, we collect your name, email address, and profile photo (if provided via Google OAuth). When you subscribe to a paid plan, our payment processor Stripe collects your payment card details — we do not store full card numbers on our servers.

*Information collected automatically:* We collect usage data including features accessed, session duration, and interaction patterns through Mixpanel. We collect device information (browser type, operating system, screen resolution), IP address, and approximate location derived from IP. We use cookies and similar technologies as described in our Cookie Policy section below.

*Information from third parties:* If you sign in via Google OAuth, we receive your name, email, and profile photo from Google per your Google account settings.

**Legal Basis for Processing (EEA/UK Users)**

| Processing Activity | Legal Basis |
|---------------------|-------------|
| Account creation and service delivery | Performance of contract |
| Payment processing | Performance of contract |
| Usage analytics for product improvement | Legitimate interest (improving service quality) |
| Email notifications about your account | Performance of contract |
| Marketing communications | Consent (opt-in) |

**Your Rights**

Under GDPR (EEA/UK users): access, rectification, erasure, restriction, portability, objection, and withdrawal of consent. Under CCPA (California residents): right to know, right to delete, right to opt-out of sale (we do not sell personal information), and right to non-discrimination.

### Example 2: Mobile App with Location Tracking

**Input:** FitRoute, a fitness tracking mobile app. Collects GPS location (continuous during workouts), health data (heart rate from wearables), email, age, weight. Users are global.

**Output (additional sections):**

**Location Data**

FitRoute collects precise GPS location data during active workout sessions to map your route and calculate distance. Location tracking begins only when you start a workout and stops when you end it. We do not track your location in the background. You can revoke location permissions at any time through your device settings, though this will prevent route mapping features from functioning.

**Health and Sensitive Data**

We collect health-related data including heart rate (synced from connected wearables), workout duration, calories burned, and body metrics you voluntarily provide (age, weight, height). Under GDPR, health data is a special category requiring explicit consent — we obtain this consent during onboarding. Under California law, this constitutes sensitive personal information subject to additional protections. This data is encrypted at rest using AES-256 and in transit using TLS 1.3.

**Consent Requirements**

Given the sensitive nature of location and health data, we implement layered consent: (1) initial consent during onboarding covering core data processing, (2) separate granular consent for location tracking activated at first workout, (3) separate consent for wearable data syncing, and (4) optional consent for anonymized data contribution to aggregate fitness research.

## Best Practices

- Use plain language alongside legal terms — define jargon on first use and write at an 8th-grade reading level where possible.
- Be specific about third-party services by name (Mixpanel, Stripe, Google Analytics) rather than vague references to "service providers."
- Include a "last updated" date and describe how users will be notified of material changes (email, in-app banner, etc.).
- Provide a data retention schedule with specific timeframes rather than "as long as necessary."
- Address cookie consent with granular categories (strictly necessary, functional, analytics, advertising) per ePrivacy Directive requirements.
- Include a direct contact method (email, form) for privacy inquiries with a stated response timeframe (e.g., 30 days for GDPR requests).

## Safety Boundaries

- Treat the output as informational drafting or issue spotting, not legal advice.
- Identify the governing jurisdiction and relevant effective date; verify changing requirements against current primary sources.
- Do not claim that language is compliant, enforceable, or complete. Flag uncertainty and recommend qualified counsel for material decisions.
- Do not file, publish, accept, sign, or send legal terms without the user reviewing and explicitly authorizing that action.

## Edge Cases

- **Apps targeting children or mixed-age audiences** — COPPA (under 13, US) and Age Appropriate Design Code (UK) impose strict requirements including verifiable parental consent and data minimization. If age-gating isn't enforced, assume the policy must address child users.
- **Businesses that share data with affiliates or ad networks** — CCPA considers this "selling" or "sharing" personal information even without monetary exchange. The policy must include a "Do Not Sell or Share" link and honor Global Privacy Control signals.
- **International data transfers post-Schrems II** — If transferring EU data to the US, reference the EU-US Data Privacy Framework or Standard Contractual Clauses. Vague statements about "appropriate safeguards" are insufficient.
- **AI/ML model training on user data** — If user data feeds into machine learning models, disclose this as a processing purpose with its own legal basis. Users may object under GDPR Article 22 to automated decision-making.
- **Acquisitions and data portability** — The policy should state what happens to user data if the business is sold, merged, or goes bankrupt, as this is a required CCPA disclosure.
