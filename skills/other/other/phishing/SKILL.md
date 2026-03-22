---
name: phishing
description: Email phishing analysis - headers, attachments, URLs
---

# Phishing Triage

Analyze suspicious emails:
- Header analysis (SPF/DKIM/DMARC)
- Sender reputation
- URL analysis
- Attachment analysis
- Social engineering indicators
- Verdict determination

## Required Context
1. **Email**: .eml file path or headers
2. **Attachments**: If separate analysis needed
3. **URLs**: If already extracted

## Output
- Verdict: PHISHING / SUSPICIOUS / SPAM / LEGITIMATE
- IOCs extracted
- Recommended actions

## Example
```
/phishing
Email: /samples/suspicious.eml
```
