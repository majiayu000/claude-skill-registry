---
name: x9-spec
description: X9.150 Secure Payment QR Code specification reference — OpenAPI schemas, field constraints, EMVCo TLV tags, JWS security, payment lifecycle
user-invocable: false
---

# X9.150 Specification Reference

You are an expert on the ANSI X9.150 Secure Payment QR Code standard. Use this knowledge when answering questions about X9.150, payment QR codes, JWS security in payments, or EMVCo QR structures.

## Three-Server Architecture

| Server | Port | Role |
|--------|------|------|
| `certserv.py` | 5001 | JWKS / public certificate hosting (optional with X9 PKI certs) |
| `qr_server.py` | 5005 | Payee backend — `/fetch/<id>` and `/notify/<id>` endpoints |
| `qr_appserver.py` | 5010 | App developer proxy — plain JSON gateway, handles JWS internally |

## Payment Lifecycle

1. **Template** → `qr_generator.py` reads `templates/*.json`, builds EMVCo QR string + JSON payload
2. **QR Scan** → Payer scans QR, extracts URL from Tag 26 Subtag 01
3. **Fetch** → `POST /fetch/<id>` with JWS-wrapped `FetchRequestPayload` → receives JWS-wrapped `PaymentRequest`
4. **Payment** → Payer executes payment on the selected network (e.g., Solana USDC)
5. **Notify** → `POST /notify/<id>` with JWS-wrapped `NotificationPayload` → receives JWS-wrapped `SignedStatusCodePayload`

## Payment Status Lifecycle

```
ACTIVE → PAYMENT_INITIATED → PAID
   ↓
CANCELLED
```

- `ACTIVE` — payload available for payment
- `PAYMENT_INITIATED` — payment started (pre-commit notification, no transactionId yet)
- `PAID` — payment confirmed (second notification includes transactionId)
- `CANCELLED` — payload cancelled

## OpenAPI Schemas

### PaymentRequest (root container)
Required fields: `id`, `revision`, `qrCodeContent`, `createdAt`, `revisedAt`, `sentAt`, `validUntil`, `status`, `creditor`, `bill`, `paymentMethods`

| Field | Type | Constraints |
|-------|------|-------------|
| `id` | UUIDNoDashes | `^[0-9a-fA-F]{32}$` |
| `revision` | integer | 0–99 |
| `qrCodeContent` | string | `^[a-zA-Z0-9_-]{0,1024}$` (base64url) |
| `createdAt` | Timestamp | `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$` |
| `revisedAt` | Timestamp | ≥ createdAt |
| `sentAt` | Timestamp | ≥ createdAt, updated each request |
| `validUntil` | Timestamp | expiration for QR acceptance |
| `status` | enum | `ACTIVE`, `PAYMENT_INITIATED`, `PAID`, `CANCELLED` |
| `paymentNotification` | URI | `^(?:https://(?:localhost\|(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})\|http://localhost)(?::\d+)?(?:/[^\s]*)?$` max 256 |
| `creditor` | Creditor | required: `MCC`, `name`, `address` |
| `bill` | Bill | required: `paymentTiming`, `amountDue` |
| `unstructured` | string | `^[ -~]*$` max 140 |
| `additionalInformation` | AdditionalInfo[] | key max 30, value max 218 |
| `paymentMethods` | PaymentMethod[] | min 1 item |

### Timestamp Format
- UTC RFC 3339 with **mandatory millisecond precision**: `2024-04-30T12:00:00.000Z`
- Pattern: `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$`
- Max length: 24

### Creditor
Required: `MCC`, `name`, `address`

| Field | Constraints |
|-------|-------------|
| `name` | `^[ -~]*$` max 50 |
| `phone` | `^\+[1-9]\d{1,20}$` (E.164) |
| `email` | RFC 5322, max 254 |
| `MCC` | `^\d{4}$` (ISO 18245) |
| `address` | required: `city`, `country` |
| `ultimateCreditor` | required: `name`, `account`, `address` |

### Address
Required: `city`, `country`

- US: `country: "US"`, `postalCode: ^\d{5}(-\d{4})?$`
- International: `country: ^[A-Z]{2}$`, `postalCode: ^[ -~]*$` max 20

### Bill
Required: `paymentTiming`, `amountDue`

- `paymentTiming`: `immediate` or `deferred`
- If `deferred` → `invoice` with `dueDate` is required
- `amountDue`: required `amount` (MonetaryAmount) + `currency` (CurrencyCode)
- `tip.allowed`: if `true` → `range` required (min/max 0–999, representing percentage × 10)
- `tip.presets`: array of 1–10 integers (suggested tip percentages × 10)
- `adjustments`: array of `{explanation, amount (SignedMonetaryAmount), validUntil}`

### MonetaryAmount Encoding
- **Integer in minor currency units** (e.g., cents for USD)
- `amount: 56` = $0.56 USD
- `amount: 560000` = 560,000 USDC base units (6 decimals)
- Positive values represent surcharges; negative values represent discounts (SignedMonetaryAmount)

### PaymentMethod
Required: `currency`, `amount`, `validUntil`, `networks`

| Field | Type |
|-------|------|
| `currency` | `^[a-zA-Z0-9._-]{1,32}$` (ISO 4217 or crypto ticker) |
| `amount` | MonetaryAmount |
| `validUntil` | Timestamp |
| `editable.range` | `{min, max}` MonetaryAmount |
| `networks` | object with `FedNow`, `RTP`, `ACH`, or custom keys |

### TraditionalNetworkDetails
Required: `routingNumber`, `accountNumber`, `protectionType`

- `routingNumber`: `^\d{9}$`
- `accountNumber`: `^\d{1,17}$`
- `protectionType`: `tokenized`, `encrypted`, or `plaintext`

### FetchRequestPayload
Required: `qrCodeContent`
- `qrCodeContent`: `^[a-zA-Z0-9_-]{0,1024}$`

### NotificationPayload
Required: `id`, `payment`
- `payment.amount` (MonetaryAmount), `payment.currency` (CurrencyCode), `payment.network` (string max 35) — all required
- `payment.transactionId` (string max 128) — absent on initiation, present on completion
- `payment.tipAmount` (MonetaryAmount) — optional
- `payer` — flexible object, `payer.info` optional
- `expectedDate` — optional Timestamp

### SignedStatusCodePayload
Required: `statusCode` (integer, mirrors HTTP status)

## JWS Security Layer

### Protected Header (JWSHeader)
Required: `iat`, `ttl`, `correlationId`, `crit`

| Field | Type | Description |
|-------|------|-------------|
| `alg` | string | `ES256` (ECC P-256) or `RS256` (RSA) — read from JWKS `alg` field |
| `typ` | string | `payreq+jws` (request) or `payresp+jws` (response) |
| `kid` | string | Key ID from JWKS |
| `iat` | int64 | Issued At — Unix seconds |
| `ttl` | int64 | Time To Live — Unix **milliseconds** (expiration) |
| `correlationId` | UUID | `^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-...` with dashes |
| `crit` | string[] | `["iat", "ttl", "correlationId"]` — mandatory-to-understand claims |
| `x5t#S256` | string | Base64url SHA-256 thumbprint of certificate |
| `x5c` | string[] | Base64 (not urlsafe) DER certificate chain |
| `jku` | URI | URL to fetch JWKS (used with self-signed certs) |

### Certificate Discovery Priority
1. **`x5t#S256`** — thumbprint lookup in local cache
2. **`x5c`** — certificate chain embedded in JWS header (X9 Financial PKI)
3. **`jku`** — fetch JWKS from URL (self-signed ECC certs)

### Freshness Validation
- `iat` must not be in future (60s clock skew allowed)
- `iat` must not be older than 8 minutes (480s)
- `ttl` (milliseconds) must not have passed
- `correlationId` in response must match request (non-repudiation)

### Content-Type
All JWS endpoints use `Content-Type: application/jose`

## EMVCo QR Code Structure (TLV)

| Tag | Length | Description | Validation |
|-----|--------|-------------|------------|
| 00 | 02 | Payload Format Indicator | Must be `01` |
| 01 | 02 | Point of Initiation Method | `11` (static) or `12` (dynamic) |
| 26 | var | Merchant Account Information (X9.150) | Contains subtags |
| 26.00 | var | Global Unique Identifier | Must be `org.x9` |
| 26.01 | var | Payment URL | Host/path only, no `https://` prefix |
| 52 | 04 | Merchant Category Code (MCC) | `^\d{4}$` |
| 53 | 03 | Transaction Currency | ISO 4217 numeric (e.g., `840` = USD) |
| 54 | var | Transaction Amount | `^\d+\.\d{2}$` (1–13 chars) |
| 58 | 02 | Country Code | `^[A-Z]{2}$` |
| 59 | var | Merchant Name | 1–25 chars |
| 60 | var | Merchant City | 1–15 chars |
| 63 | 04 | CRC-16/CCITT-FALSE | `^[0-9A-F]{4}$` |

### TLV Encoding
- Each field: `[Tag:2][Length:2][Value:Length]`
- Tag 63 (CRC) must be **last** — CRC covers everything before its value
- Tag 26 uses nested TLV for subtags
- URL in Tag 26.01 omits `https://` to save space

### CRC-16 Algorithm
- Polynomial: 0x1021 (CRC-16/CCITT-FALSE)
- Initial: 0xFFFF
- Input: entire QR string including `6304` prefix, excluding the 4-char CRC value

## Testing Flags

| Flag | Component | Effect |
|------|-----------|--------|
| `--failSignature` | Server & Payer | Corrupts JWS signature |
| `--failiat` | Server | Returns `iat` from 11 minutes ago |
| `--failttl` | Server | Returns expired JWS |
| `--failjwscustom` | Payer | Randomly omits mandatory JWS headers |
| `--failCorrelationId` | Server | Returns mismatched correlationId |
| `--sanctionedWallet` | Server | Blocks specified blockchain address (403) |

## Key Files

- `spec/openapi.yaml` — authoritative OpenAPI schema
- `qr_server.py` — canonical JWS sign/verify implementation
- `qr_payer.py` — full payer flow (scan → fetch → verify → pay → notify)
- `qr_parser.py` — EMVCo TLV parser
- `keygen.py` — ECC key pair + self-signed certificate generation
- `templates/*.json` — payment request templates
