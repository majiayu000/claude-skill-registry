---
name: deliverability-ops
description: Use when investigating inbox placement, reputation, and compliance signals
  across senders.
---

# Deliverability Operations Skill

## When to Use
- Inbox placement drops or spam-folder complaints.
- Preparing for IP/domain warmups or volume ramps.
- Auditing authentication, feedback loops, or compliance settings.

## Framework

### Signals to Monitor
1. **Engagement** – opens, clicks, unsubscribes, spam complaints by ISP.
2. **Reputation** – Google Postmaster, Microsoft SNDS, Talos/Barracuda, Spamhaus, Validity.
3. **Infrastructure** – SPF/DKIM/DMARC alignment, BIMI, TLS, reverse DNS, dedicated vs shared IP.
4. **List Health** – bounce types, spam traps, opt-in provenance, inactivity thresholds.

### Playbook Steps
1. Snapshot key metrics over last 7/30 days.
2. Identify affected mailbox providers (Gmail, Outlook, Yahoo, etc.).
3. Validate authentication + sending domains.
4. Segment audiences by engagement tier; limit sends to VIP/high intent.
5. Recommend remediation actions (warmup plan, content refresh, list cleaning, cadence adjustment).

## Templates
- Deliverability diagnostic worksheet (reputation + infrastructure + content).
- IP/domain warmup tracker (volume ramp table).
- Compliance checklist (CAN-SPAM, CASL, GDPR/CCPA, unsubscribe handling).

## Tips
- Pair with `segmentation` skill to isolate healthy cohorts.
- Document every remediation change to correlate with future reputation shifts.
- Align marketing, security, and legal teams on consent language.

---
