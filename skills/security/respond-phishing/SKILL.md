---
name: respond-phishing
description: "Respond to a reported phishing email following PICERL methodology. Use when a phishing email is reported or detected. Analyzes artifacts, identifies recipients who clicked, contains malicious IOCs, and removes emails from mailboxes."
required_roles:
  chronicle: roles/chronicle.editor
  soar: roles/chronicle.soarAdmin
  gti: GTI Enterprise
personas: [incident-responder]
---

# Phishing Incident Response Skill

Structured workflow for responding to reported phishing emails using the PICERL model.

## Inputs

- `CASE_ID` - SOAR case ID for the incident
- `ALERT_GROUP_IDENTIFIERS` - Alert group identifiers from SOAR
- `REPORTED_EMAIL_ARTIFACTS` - Information about the email:
  - Email headers
  - Email body
  - Attached files (hashes)
  - URLs in email
  - Recipient user ID(s)
  - Sender address/domain

## Required Outputs

**After completing each phase, you MUST report these outputs:**

### Identification Phase
| Output | Description |
|--------|-------------|
| `PHISHING_URLS` | URLs extracted from email body |
| `PHISHING_IOCS` | Confirmed malicious indicators (URLs, domains, hashes) |
| `AFFECTED_USERS` | All users who received the email |
| `CLICKED_USERS` | Users who clicked/interacted with malicious content |
| `PHISHING_CATEGORY` | Type: credential phish, spear phishing, BEC, malware delivery |

### Containment Phase
| Output | Description |
|--------|-------------|
| `BLOCKED_IOCS` | IOCs blocked at email gateway/proxy/firewall |
| `CONTAINED_USERS` | User accounts with restrictions applied |
| `ISOLATED_ENDPOINTS` | Endpoints isolated due to suspicious activity |

### Eradication Phase
| Output | Description |
|--------|-------------|
| `DELETED_EMAILS` | Count of malicious emails removed from mailboxes |
| `QUARANTINED_EMAILS` | Emails moved to quarantine |

### Recovery Phase
| Output | Description |
|--------|-------------|
| `RESTORED_ACCOUNTS` | User accounts restored to normal access |
| `USER_NOTIFICATIONS` | Users notified of incident and required actions |

## PICERL Phases

### Phase 2: Identification

**Step 2.1: Get Context & Check Duplicates**
```
secops-soar.get_case_full_details(case_id=CASE_ID)
```

Use `/check-duplicates`.

**Step 2.2: Analyze Email Artifacts**

Extract from email:
- All URLs → `EXTRACTED_URLS`
- Sender domain/IP
- Attachment hashes → `EXTRACTED_HASHES`
- Reply-to addresses
- Header anomalies (SPF/DKIM failures)

**Step 2.3: Enrich Extracted IOCs**

For each IOC (URLs, domains, IPs, hashes):

Use `/enrich-ioc`:
```
/enrich-ioc IOC_VALUE IOC_TYPE
```

Identify confirmed malicious IOCs → `MALICIOUS_IOCs`.

**Step 2.4: Categorize Phishing Type**

| Category | Indicators |
|----------|------------|
| **Generic Credential Phish** | Broad targeting, brand impersonation (Microsoft, Google) |
| **Spear Phishing** | Personalized, targets specific individuals |
| **Whaling** | Targets executives |
| **BEC** | Wire transfer requests, no malicious links |
| **Brand Impersonation** | Mimics known brands |
| **Malware Delivery** | Focus on attachments or download links |

Document: `PHISHING_CATEGORY`

**Step 2.5: Search for Related Activity (SIEM)**

```
secops-mcp.search_security_events(
    text="Network connections or DNS to MALICIOUS_IOCs",
    hours_back=72
)
```

Look for:
- Other emails with same subject/sender
- URL clicks to malicious URLs
- File executions of malicious hashes
- Suspicious activity from recipients

**Step 2.6: Identify Impact**

- `SIMILAR_EMAIL_RECIPIENTS` - Who else received it
- `POTENTIAL_COMPROMISED_USERS` - Who clicked/interacted
- `SUSPICIOUS_ENDPOINTS` - Endpoints with related activity

**Step 2.7: Document Identification**

Use `/document-in-case` with findings.

---

### Phase 3: Containment

**Step 3.1: Block Network IOCs**

For each IOC in `MALICIOUS_IOCs`:

Use `/confirm-action`:
> "Block domain/IP/URL [VALUE]?"

If confirmed, implement blocks at:
- Email gateway
- Web proxy
- Firewall
- DNS

**Step 3.2: Contain Potentially Compromised Users**

For each user in `POTENTIAL_COMPROMISED_USERS`:

Trigger `/respond-compromised-account`

**Step 3.3: Isolate Suspicious Endpoints**

For each endpoint in `SUSPICIOUS_ENDPOINTS`:

Use `/confirm-action`:
> "Isolate endpoint [HOSTNAME]?"

**Step 3.4: Verify Containment**

Monitor for continued activity to blocked IOCs.

Use `/document-in-case` with containment status.

---

### Phase 4: Eradication

**Step 4.1: Delete Malicious Emails**

*(Requires Email Gateway/Platform tools)*

Search all mailboxes for:
- Same subject line
- Same sender
- Contains malicious URLs/attachments

Delete/quarantine identified emails.
Document count of emails removed.

**Step 4.2: Address Malware (If Applicable)**

If phishing led to malware execution:
→ Trigger `/respond-malware`

**Step 4.3: Document Eradication**

Use `/document-in-case` with email deletion counts and actions.

---

### Phase 5: Recovery

**Step 5.1: User Account Recovery**

If accounts disabled during containment:
- Verify threat is removed
- Re-enable accounts
- Force password change if credentials potentially compromised

**Step 5.2: Endpoint Recovery**

If endpoints isolated:
- Verify clean before reconnecting
- Follow malware response recovery if infected

**Step 5.3: Validate Countermeasures**

After lifting blocks, verify legitimate traffic isn't blocked.

**Step 5.4: User Communication**

Notify affected users:
- What happened
- Actions taken
- What they should do (change passwords, be vigilant)

---

### Phase 6: Lessons Learned

Use `/generate-report` with:
- Phishing category
- Impact assessment
- Response timeline
- Emails deleted count
- Recommendations

Conduct review:
- How did it bypass email filters?
- Detection effectiveness
- User awareness gaps
- Recommended filter/rule updates

---

## Critical Warnings

- **DO check** who else received the email
- **DO NOT leave** malicious emails in mailboxes
- **DO NOT block** legitimate business domains (verify first)
- **VERIFY** extracted domains against company-owned domains list

## Phishing Response Checklist

- [ ] Email artifacts analyzed
- [ ] IOCs enriched and categorized
- [ ] All recipients identified
- [ ] Click/interaction assessed
- [ ] Malicious IOCs blocked
- [ ] Compromised users contained
- [ ] Malicious emails deleted from ALL mailboxes
- [ ] Users notified
- [ ] Report generated
