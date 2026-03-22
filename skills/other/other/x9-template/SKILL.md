---
name: x9-template
description: Generate payment request template JSON files for X9.150 testing
user-invocable: true
tools:
  - Bash
  - Read
  - Write
  - Glob
context: fork
inject:
  - !ls templates/*.json 2>/dev/null || echo "(no templates found)"
---

# X9.150 Template Creator

You generate payment request template JSON files for testing the X9.150 specification. Templates are partial PaymentRequest payloads — `qr_generator.py` adds runtime fields (`id`, `revision`, `createdAt`, timestamps, `status`, `qrCodeContent`, `paymentNotification`).

## Instructions

1. **Understand the scenario** the user wants:
   - Restaurant with tips
   - Deferred invoice (utility bill, B2B)
   - Marketplace with ultimateCreditor
   - Multi-currency with blockchain
   - Simple immediate payment
   - Custom scenario

2. **Read an existing template** for reference — `templates/01_coffee_shop.json` is the canonical example

3. **Generate the template** following the exact schema from `spec/openapi.yaml`

4. **Write the file** to `templates/` with the next available number prefix (e.g., `15_*.json`)

5. **Validate** the generated template's structure matches the spec

## Template Structure

A template contains only the fields that are known at design time:

```json
{
    "creditor": {
        "name": "Business Name",
        "phone": "+15551234567",
        "email": "contact@business.com",
        "address": {
            "line1": "123 Main St",
            "city": "City",
            "state": "ST",
            "postalCode": "12345",
            "country": "US"
        },
        "MCC": "5812"
    },
    "bill": {
        "paymentTiming": "immediate",
        "description": "Description of goods/services",
        "order": {
            "number": "ORD-2026-001",
            "date": "2026-01-15"
        },
        "amountDue": {
            "amount": 1500,
            "currency": "USD"
        },
        "tip": {
            "allowed": true,
            "range": { "min": 100, "max": 300 },
            "presets": [150, 200, 250]
        }
    },
    "additionalInformation": [
        { "key": "Item 1", "value": "10.00" },
        { "key": "Item 2", "value": "5.00" }
    ],
    "paymentMethods": [
        {
            "currency": "USD",
            "amount": 1500,
            "networks": {
                "FedNow": {
                    "routingNumber": "123456789",
                    "accountNumber": "9876543210",
                    "protectionType": "tokenized"
                }
            }
        }
    ]
}
```

## Scenario-Specific Fields

### Restaurant with Tips
```json
"tip": {
    "allowed": true,
    "range": { "min": 100, "max": 300 },
    "presets": [150, 180, 200, 250]
}
```
- Tip values are percentage × 10 (e.g., 150 = 15.0%)
- `range.min`/`max`: 0–999
- `presets`: 1–10 suggested percentages

### Deferred Invoice
```json
"bill": {
    "paymentTiming": "deferred",
    "invoice": {
        "number": "INV-2026-001",
        "date": "2026-01-15",
        "dueDate": "2026-02-15T23:59:59.000Z",
        "invoicee": {
            "name": "Customer Corp",
            "email": "ap@customer.com",
            "address": {
                "city": "New York",
                "country": "US"
            }
        }
    },
    "amountDue": { "amount": 500000, "currency": "USD" }
}
```
- `paymentTiming: "deferred"` REQUIRES `invoice.dueDate`
- `dueDate` uses full Timestamp format with milliseconds

### Marketplace with UltimateCreditor
```json
"creditor": {
    "name": "Marketplace Platform Inc",
    "MCC": "5999",
    "address": { "city": "Austin", "state": "TX", "country": "US" },
    "ultimateCreditor": {
        "name": "Sub-Merchant Store",
        "account": {
            "id": "seller_12345",
            "schemaName": "marketplace_id"
        },
        "address": { "city": "Portland", "state": "OR", "country": "US" }
    }
}
```

### Multi-Currency with Blockchain
```json
"paymentMethods": [
    {
        "currency": "USD",
        "amount": 5000,
        "networks": {
            "FedNow": {
                "routingNumber": "123456789",
                "accountNumber": "9876543210",
                "protectionType": "tokenized"
            }
        }
    },
    {
        "currency": "USDC",
        "amount": 50000000,
        "networks": {
            "Solana": {
                "address": "emjE6JshbysqU93MiTVFpjUQSo6GHjEhUNCLrSBjuiC"
            }
        }
    }
]
```
- USDC on Solana has 6 decimals: $50.00 = 50000000 base units
- USD in cents: $50.00 = 5000

### Adjustments (Discounts/Surcharges)
```json
"amountDue": {
    "amount": 10000,
    "currency": "USD",
    "adjustments": [
        {
            "explanation": "Early payment discount (2%)",
            "amount": -200,
            "validUntil": "2026-02-01T23:59:59.000Z"
        },
        {
            "explanation": "Late fee after due date",
            "amount": 500,
            "validUntil": "2026-03-01T23:59:59.000Z"
        }
    ]
}
```
- Negative amounts = discounts
- Positive amounts = surcharges
- Each adjustment has a `validUntil` expiration

## Common MCC Codes

| MCC | Business Type |
|-----|--------------|
| 5411 | Grocery Stores |
| 5812 | Restaurants |
| 5814 | Fast Food |
| 5912 | Drug Stores |
| 5999 | Miscellaneous Retail |
| 4900 | Utilities |
| 7011 | Hotels |
| 7230 | Barber/Beauty Shops |
| 8011 | Medical Services |
| 8299 | Schools/Education |

## Validation Checklist

Before writing the template, verify:
- [ ] `creditor.MCC` is exactly 4 digits
- [ ] `creditor.address` has `city` and `country`
- [ ] `country` is 2 uppercase letters
- [ ] `amount` values are integers in minor units
- [ ] Phone numbers start with `+` and digits only
- [ ] String fields match `^[ -~]*$` (printable ASCII)
- [ ] No field exceeds its `maxLength`
- [ ] If `paymentTiming: "deferred"`, `invoice.dueDate` exists
- [ ] If `tip.allowed: true`, `tip.range` has `min` and `max`
- [ ] `paymentMethods` has `validUntil` — use a placeholder that qr_generator.py will override
- [ ] File uses 4-space indentation, no trailing whitespace

## Naming Convention

Files: `templates/NN_descriptive_name.json`
- `NN` = 2-digit sequence number (next available)
- Use underscores, lowercase
- Descriptive of the scenario (e.g., `15_hardware_store.json`)
