---
name: respond-compromised-account
description: "Respond to a potentially compromised user account. Use when impossible travel, credential stuffing, successful phishing, or suspicious activity indicates account compromise. Investigates activity, contains the account, removes persistence, and restores access."
required_roles:
  chronicle: roles/chronicle.editor
  soar: roles/chronicle.soarAdmin
  gti: GTI Standard
personas: [incident-responder]
---

# Compromised User Account Response Skill

Structured workflow for responding to potentially compromised user accounts using the PICERL model.

## Inputs

- `USER_ID` - Username or email of the potentially compromised user
- `CASE_ID` - SOAR case ID for documentation
- `ALERT_GROUP_IDENTIFIERS` - Alert group identifiers from SOAR
- *(Optional)* `INITIAL_ALERT_DETAILS` - Summary of triggering alert

## Required Outputs

**After completing each phase, you MUST report these outputs:**

### Identification Phase
| Output | Description |
|--------|-------------|
| `AFFECTED_ACCOUNTS` | User accounts confirmed or suspected compromised |
| `SUSPICIOUS_ACTIVITY` | Summary of anomalous activity detected |
| `ACCESS_SCOPE` | Systems/data the account had access to |
| `COMPROMISE_LIKELIHOOD` | Assessment level: `Low`, `Medium`, `High`, `Confirmed` |

### Containment Phase
| Output | Description |
|--------|-------------|
| `DISABLED_ACCOUNTS` | Accounts that were disabled |
| `RESET_PASSWORDS` | Accounts with passwords reset |
| `REVOKED_SESSIONS` | Sessions terminated |

### Eradication Phase
| Output | Description |
|--------|-------------|
| `REMOVED_PERSISTENCE` | Persistence mechanisms removed (forwarding rules, OAuth apps, etc.) |
| `CLEANED_ENDPOINTS` | Associated endpoints verified clean |

### Recovery Phase
| Output | Description |
|--------|-------------|
| `RESTORED_ACCOUNTS` | Accounts re-enabled with new security controls |
| `USER_NOTIFICATIONS` | Users notified of incident and required actions |

## PICERL Phases

### Phase 2: Identification

**Step 2.1: Get Context**

```
secops-soar.get_case_full_details(case_id=CASE_ID)
```

Use `/check-duplicates`.

**Step 2.2: Gather Initial Context**

SIEM entity lookup:
```
secops-mcp.lookup_entity(entity_value=USER_ID)
```

*(If IDP tools available)*:
- Account status
- Recent logins
- MFA configuration
- Password last changed

**Step 2.3: Analyze User Activity**

Search SIEM for last 96 hours:
```
secops-mcp.search_security_events(
    text="All activity for USER_ID",
    hours_back=96
)
```

Look for:
- **Anomalous logins**: Unusual locations, times, IPs, user agents
- **Suspicious commands**: On associated endpoints
- **Sensitive access**: Files, applications, databases
- **Lateral movement**: Logins to other systems
- **Data exfiltration**: Large transfers, unusual destinations
- **Account changes**: MFA, recovery email, forwarding rules
- **OAuth grants**: New application authorizations

**Step 2.4: Check Related Cases**

Use `/find-relevant-case` with `[USER_ID]`.

**Step 2.5: Assess Compromise Likelihood**

| Level | Indicators |
|-------|------------|
| **Low** | Single anomalous event, user confirms legitimate |
| **Medium** | Multiple anomalies, unverified |
| **High** | Clear malicious activity patterns |
| **Confirmed** | Known credential theft, attacker actions visible |

Document: `COMPROMISE_LIKELIHOOD`

**Step 2.6: Document Identification**

Use `/document-in-case` with findings and assessment.

---

### Phase 3: Containment

**Step 3.1: Confirm Containment Actions**

Based on `COMPROMISE_LIKELIHOOD`, use `/confirm-action`:

**High/Confirmed:**
> "Disable account [USER_ID] immediately?"

**Medium:**
> "Reset password and terminate sessions for [USER_ID]?"

**Low:**
> "Force MFA re-enrollment for [USER_ID]?"

**Step 3.2: Execute Containment**

*(Requires Identity Provider tools)*

Actions by severity:
- **Disable account**: Immediate lockout
- **Reset password**: Force change on next login
- **Terminate sessions**: Invalidate all active sessions
- **Revoke tokens**: OAuth and API tokens

**Step 3.3: Verify Containment**

Monitor for continued activity:
```
secops-mcp.search_security_events(
    text="Activity from USER_ID after containment",
    hours_back=1
)
```

Use `/document-in-case` with containment status.

---

### Phase 4: Eradication

**Step 4.1: Investigate Attacker Actions**

Thoroughly review what the attacker did while in the account:

```
secops-mcp.search_security_events(
    text="All actions by USER_ID during compromise window",
    hours_back=96
)
```

Focus on:
- **Emails**: Sent, received, forwarding rules created
- **Data access**: Files downloaded, shared externally
- **Configuration**: Account settings changed
- **OAuth apps**: New authorizations
- **Lateral movement**: Other systems accessed

**Step 4.2: Check for Persistence**

*(Requires email/cloud platform tools)*

Look for:
- Email forwarding rules to external addresses
- Delegate access grants
- Malicious OAuth applications
- Inbox rules that hide attacker activity
- Recovery email/phone changes

**Step 4.3: Remove Persistence**

Delete/revoke all identified persistence:
- Remove forwarding rules
- Revoke OAuth apps
- Remove delegate access
- Reset recovery options

**Step 4.4: Endpoint Investigation**

If account accessed specific endpoints:

Trigger endpoint triage to check for:
- Malware dropped
- Persistence mechanisms
- Credential caching

Use `/document-in-case` with eradication findings.

---

### Phase 5: Recovery

**Step 5.1: Ensure Threat Removed**

Verify:
- All persistence removed
- Associated endpoints clean
- No ongoing attacker access

**Step 5.2: Secure Account**

- Strong password set
- MFA properly configured (hardware key preferred)
- Recovery options secured
- Review account permissions

**Step 5.3: Re-enable Account**

*(If disabled during containment)*

Re-enable with:
- Password change required on first login
- MFA verification required

**Step 5.4: Communicate with User**

Inform the user:
- What happened (appropriate level of detail)
- Actions taken on their account
- Steps they need to take
- Warning signs to watch for
- How to report suspicious activity

**Step 5.5: Monitor Account**

Enhanced monitoring for 30 days:
- Watch for anomalous activity
- Alert on unusual logins
- Track sensitive data access

Use `/document-in-case` with recovery status.

---

### Phase 6: Lessons Learned

Use `/generate-report` with:
- Initial access vector (if determined)
- Attacker actions during compromise
- Data potentially exposed
- Response timeline
- Recommendations

Review:
- How was compromise detected?
- Was MFA bypassed? How?
- What data was at risk?
- What detections should be added/tuned?

---

## Critical Warnings

- **DO NOT execute containment** without analyst confirmation
- **DO NOT re-enable** without checking for persistence
- **MUST document** all findings in SOAR
- **ALWAYS check** for forwarding rules and OAuth apps

## Containment Decision Matrix

| Likelihood | Disable Account | Reset Password | Terminate Sessions |
|------------|-----------------|----------------|-------------------|
| Confirmed | ✅ Immediate | ✅ | ✅ |
| High | ✅ Recommended | ✅ | ✅ |
| Medium | Consider | ✅ | ✅ |
| Low | No | Consider | Consider |

## Common Persistence Mechanisms

| Mechanism | Where to Check |
|-----------|----------------|
| Email forwarding | Mail rules |
| Delegate access | Mailbox permissions |
| OAuth apps | Connected applications |
| Inbox rules | Mail filters |
| Recovery options | Account settings |
| API tokens | Developer settings |
