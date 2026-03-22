---
name: x9-validate
description: Validate JSON payloads against the X9.150 OpenAPI schema
user-invocable: true
tools:
  - Bash
  - Read
  - Glob
context: fork
inject:
  - spec/openapi.yaml
  - !find spec/ -name "*.yaml" -maxdepth 1
---

# X9.150 Payload Validator

You validate JSON payloads against the X9.150 OpenAPI schema (`spec/openapi.yaml`). You auto-detect the schema type and report constraint violations with explanations.

## Instructions

1. **Accept input** — the user provides either:
   - A file path to a JSON file (template or generated payload)
   - Inline JSON pasted in the message
   - A template name (e.g., "01_coffee_shop") to validate from `templates/`

2. **Auto-detect the schema type** based on the payload structure:
   - Has `creditor` + `bill` + `paymentMethods` → **PaymentRequest**
   - Has `payment` + `id` (32-char hex) at root → **NotificationPayload**
   - Has only `qrCodeContent` → **FetchRequestPayload**
   - Has only `statusCode` → **SignedStatusCodePayload**
   - Has `creditor` + `bill` but no `id`/`status` → **Template** (pre-generation format, validate subset)

3. **Run validation** using the project's own validation infrastructure:

```bash
python3.13 -c "
import json, yaml, sys
from jsonschema import Draft7Validator
import referencing
from referencing.jsonschema import DRAFT7

with open('spec/openapi.yaml') as f:
    spec = yaml.safe_load(f)

payload = json.loads('''<PAYLOAD_JSON>''')

spec_uri = 'http://x9.150/openapi.yaml'
resource = referencing.Resource.from_contents(spec, default_specification=DRAFT7)
registry = referencing.Registry().with_resource(uri=spec_uri, resource=resource)
schema = {'\$ref': f'{spec_uri}#/components/schemas/<SCHEMA_NAME>'}

validator = Draft7Validator(schema, registry=registry)
errors = list(validator.iter_errors(payload))
if errors:
    for e in errors:
        path = '.'.join(str(p) for p in e.absolute_path) or '(root)'
        print(f'FAIL: {path} — {e.message}')
    sys.exit(1)
else:
    print('PASS: payload is valid')
"
```

4. **Report results** with:
   - Detected schema type
   - PASS/FAIL status
   - For each violation: field path, constraint violated, expected vs actual, explanation
   - Suggestions for fixing violations

## Common Validation Rules to Check

### Timestamps
- Must match `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$`
- Must include milliseconds (`.000`)
- Must end with `Z` (UTC)

### UUIDs
- `id`: 32 hex chars, no dashes (`^[0-9a-fA-F]{32}$`)
- `correlationId`: standard UUID with dashes

### Monetary Amounts
- Must be integers (minor units, e.g., cents)
- `amount: 56` = $0.56, not $56.00
- Adjustments use `SignedMonetaryAmount` (can be negative for discounts)

### Bill Rules
- `paymentTiming: "deferred"` requires `invoice.dueDate`
- `tip.allowed: true` requires `tip.range` with `min` and `max`

### PaymentMethod
- `validUntil` is required on each payment method
- `networks` must have at least one entry
- Traditional networks require `routingNumber` (9 digits), `accountNumber` (1-17 digits), `protectionType`

### Creditor
- `MCC` must be exactly 4 digits
- `address.country` must be 2 uppercase letters (ISO 3166-1)
- US postal codes: `^\d{5}(-\d{4})?$`

## Template vs Full PaymentRequest

Templates (in `templates/`) are partial — they lack runtime fields like `id`, `revision`, `createdAt`, `sentAt`, `validUntil`, `status`, `qrCodeContent`, `paymentNotification`. These are added by `qr_generator.py`. When validating a template, skip required-field checks for these runtime fields and focus on structural/format validation of the fields that ARE present.

## Error Explanation Style

For each error, explain:
1. What the constraint is (with the regex or rule)
2. What value was found
3. How to fix it
4. Why the spec requires this (brief context)
