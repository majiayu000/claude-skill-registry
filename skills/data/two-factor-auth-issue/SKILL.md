---
name: two-factor-auth-issue
description: Help with two-factor authentication problems. Use when a customer cannot get a 2FA code or device verification.
metadata:
  trigger_phrases:
      - "two factor"
      - "factor authentication"
      - "authentication problems"
  related_skills: ["password-reset-issue", "access-locked-out", "login-link", "payment-method-issue", "email-delivery-failure"]
  sample_size: "4"
  validation: |
    required_phrases:
      - "to your kit account"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 4\navg_thread_length: 2.75\ntop_phrases:\n  - phrase: \"to your kit account\"\n    count: 2\n    percent: 50\n  - phrase: \"to log in to\"\n    count: 2\n    percent: 50\n  - phrase: \"thank you creeland forwarded\"\n    count: 1\n    percent: 25\n  - phrase: \"you creeland forwarded message\"\n    count: 1\n    percent: 25\n  - phrase: \"creeland forwarded message from\"\n    count: 1\n    percent: 25\n  - phrase: \"forwarded message from email\"\n    count: 1\n    percent: 25\n  - phrase: \"message from email date\"\n    count: 1\n    percent: 25\n  - phrase: \"from email date december\"\n    count: 1\n    percent: 25\n  - phrase: \"email date december 5\"\n    count: 1\n    percent: 25\n  - phrase: \"date december 5 2024\"\n    count: 1\n    percent: 25"
---
# Two-Factor Authentication Issue

## Response Patterns (from samples)

Common openings:
- "Thank you, [NAME] ----------- Forwarded message ----------- From: [EMAIL] Date: December 5, 2024 at 3:44 PM CST Subject: New login to your Kit account To: [EMAIL] You recently attempted to log in to your Kit account from an unrecognized device. Device: Chrome on Mac OS X Location: Boise, Idaho, United States (approximate) Time: 4:44 PM EST, December 05, 2024 If this was you, you can complete your login by clicking one of the buttons below. If you're logging in from a shared or public device, we recommend allowing access just once. Trust this device Trust this device once If you didn't recently attempt to log in to Kit, we recommend that you change your password immediately to secure your account. You can request a password change by clicking here , or by visiting app.kit.com and clicking the \"Forgot your password?\" link. Need help? Get in touch by emailing Customer Success at [EMAIL] [ADDRESS] #761, Boise, Idaho 83701"
- "I have been able to reset the password but now when accessing the admin"
- "Hey Kiran,"

Common core lines:
- ">"
- "Thank you, [NAME] ----------- Forwarded message ----------- From: [EMAIL] Date: December 5, 2024 at 3:44 PM CST Subject: New login to your Kit account To: [EMAIL] You recently attempted to log in to your Kit account from an unrecognized device. Device: Chrome on Mac OS X Location: Boise, Idaho, United States (approximate) Time: 4:44 PM EST, December 05, 2024 If this was you, you can complete your login by clicking one of the buttons below. If you're logging in from a shared or public device, we recommend allowing access just once. Trust this device Trust this device once If you didn't recently attempt to log in to Kit, we recommend that you change your password immediately to secure your account. You can request a password change by clicking here , or by visiting app.kit.com and clicking the \"Forgot your password?\" link. Need help? Get in touch by emailing Customer Success at [EMAIL] [ADDRESS] #761, Boise, Idaho 83701"
- "I have been able to reset the password but now when accessing the admin"

Common closings:
- "Thank you, [NAME] ----------- Forwarded message ----------- From: [EMAIL] Date: December 5, 2024 at 3:44 PM CST Subject: New login to your Kit account To: [EMAIL] You recently attempted to log in to your Kit account from an unrecognized device. Device: Chrome on Mac OS X Location: Boise, Idaho, United States (approximate) Time: 4:44 PM EST, December 05, 2024 If this was you, you can complete your login by clicking one of the buttons below. If you're logging in from a shared or public device, we recommend allowing access just once. Trust this device Trust this device once If you didn't recently attempt to log in to Kit, we recommend that you change your password immediately to secure your account. You can request a password change by clicking here , or by visiting app.kit.com and clicking the \"Forgot your password?\" link. Need help? Get in touch by emailing Customer Success at [EMAIL] [ADDRESS] #761, Boise, Idaho 83701"
- ">"
- "Let me know if you have any issues requesting login links using that email address."

## Phrases That Work (4-gram frequency)

- "to your kit account" — 2 (50%)
- "to log in to" — 2 (50%)
- "thank you creeland forwarded" — 1 (25%)
- "you creeland forwarded message" — 1 (25%)
- "creeland forwarded message from" — 1 (25%)
- "forwarded message from email" — 1 (25%)
- "message from email date" — 1 (25%)
- "from email date december" — 1 (25%)
- "email date december 5" — 1 (25%)
- "date december 5 2024" — 1 (25%)

## Tone Guidance (observed)

- Openings trend toward: "Thank you, [NAME] ----------- Forwarded message ----------- From: [EMAIL] Date: December 5, 2024 at 3:44 PM CST Subject: New login to your Kit account To: [EMAIL] You recently attempted to log in to your Kit account from an unrecognized device. Device: Chrome on Mac OS X Location: Boise, Idaho, United States (approximate) Time: 4:44 PM EST, December 05, 2024 If this was you, you can complete your login by clicking one of the buttons below. If you're logging in from a shared or public device, we recommend allowing access just once. Trust this device Trust this device once If you didn't recently attempt to log in to Kit, we recommend that you change your password immediately to secure your account. You can request a password change by clicking here , or by visiting app.kit.com and clicking the \"Forgot your password?\" link. Need help? Get in touch by emailing Customer Success at [EMAIL] [ADDRESS] #761, Boise, Idaho 83701"
- Closings often include: "Thank you, [NAME] ----------- Forwarded message ----------- From: [EMAIL] Date: December 5, 2024 at 3:44 PM CST Subject: New login to your Kit account To: [EMAIL] You recently attempted to log in to your Kit account from an unrecognized device. Device: Chrome on Mac OS X Location: Boise, Idaho, United States (approximate) Time: 4:44 PM EST, December 05, 2024 If this was you, you can complete your login by clicking one of the buttons below. If you're logging in from a shared or public device, we recommend allowing access just once. Trust this device Trust this device once If you didn't recently attempt to log in to Kit, we recommend that you change your password immediately to secure your account. You can request a password change by clicking here , or by visiting app.kit.com and clicking the \"Forgot your password?\" link. Need help? Get in touch by emailing Customer Success at [EMAIL] [ADDRESS] #761, Boise, Idaho 83701"

## What NOT To Do

- Don't introduce policy details that are not present in the verified response lines above.
- Don't paraphrase or reframe the customer's question in a way that changes meaning.
- Don't add refund/discount promises unless they appear in the extracted responses for this topic.

## Validation

Draft must:
- [ ] Include at least one of the required phrases from the validation block
- [ ] Stay consistent with the observed response patterns above
- [ ] NOT introduce policy details that are not present in the verified response lines above.