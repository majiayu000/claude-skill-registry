---
name: x9-parse-qr
description: Parse EMVCo QR content strings — TLV breakdown, CRC validation, X9.150 URL extraction
user-invocable: true
tools:
  - Bash
  - Read
  - Glob
context: fork
inject:
  - !ls payer_db/qrs/*.txt 2>/dev/null || echo "(no QR files found — run qr_generator.py first)"
---

# X9.150 QR Code Parser

You parse EMVCo QR content strings into their TLV structure, validate the CRC-16 checksum, and extract the X9.150 payment URL.

## Instructions

1. **Accept input** — the user provides either:
   - A raw QR content string (starts with `000201`)
   - A file path to a `.txt` file in `payer_db/qrs/`
   - A request to "parse the latest QR" or "parse all QRs"

2. **Parse the TLV structure** — EMVCo QR codes use Tag-Length-Value encoding:
   - Each field: `[Tag:2 chars][Length:2 chars][Value:Length chars]`
   - Tags are 2-digit strings (not hex)
   - Length is decimal (not hex), zero-padded to 2 digits

3. **Validate CRC-16** — the last 8 characters should be `6304XXXX`:
   - `63` = CRC tag, `04` = length (4 hex chars)
   - CRC-16/CCITT-FALSE: polynomial 0x1021, initial 0xFFFF
   - Input to CRC: entire string including `6304`, excluding the 4-char CRC value

4. **Extract X9.150 data** from Tag 26 (Merchant Account Information):
   - Subtag 00: Global Unique Identifier — must be `org.x9`
   - Subtag 01: Payment URL — host/path only (no `https://`), e.g., `localhost:5005/fetch/abc123`
   - Reconstruct full URL: `https://<subtag01_value>`

5. **Display results** in a clear table format:

```
EMV QR PARSER — X9.150

CRC-16: VALID (calculated: ABCD, found: ABCD)

TAG | LEN | DESCRIPTION                              | VALUE
----|-----|------------------------------------------|------
00  | 02  | Payload Format Indicator                 | 01
01  | 02  | Point of Initiation Method               | 12
26  | XX  | Merchant Account Information (X9.150)    | (nested)
 .00| XX  | Global Unique Identifier                 | org.x9
 .01| XX  | Payment URL                              | localhost:5005/fetch/...
52  | 04  | Merchant Category Code (MCC)             | 5812
53  | 03  | Transaction Currency                     | 840
54  | XX  | Transaction Amount                       | 0.56
58  | 02  | Country Code                             | US
59  | XX  | Merchant Name                            | Brew & Bean Coffee
60  | XX  | Merchant City                            | San Francisco
63  | 04  | CRC                                      | ABCD

Fetch URL: https://localhost:5005/fetch/<id>
Payload ID: <extracted-uuid>
```

6. **Validate fields** against EMVCo rules:
   - Tag 00 must be `01`
   - Tag 01 must be `11` (static) or `12` (dynamic)
   - Tag 52 (MCC) must be 4 digits
   - Tag 53 must be 3 digits (ISO 4217 numeric currency code)
   - Tag 54 must match `^\d+\.\d{2}$`
   - Tag 58 must be 2 uppercase letters
   - Tag 59 max 25 chars
   - Tag 60 max 15 chars
   - Tag 26 subtag 00 must be `org.x9`

## Using qr_parser.py

You can also run the project's built-in parser for comparison:

```bash
# Parse a specific QR file non-interactively
python3.13 -c "
from qr_parser import process_qr_file
process_qr_file('payer_db/qrs/<filename>.txt')
"
```

## EMVCo Tag Reference

| Tag | Name | Required | Format |
|-----|------|----------|--------|
| 00 | Payload Format Indicator | Yes | `01` |
| 01 | Point of Initiation | Yes | `11` or `12` |
| 02-25 | Reserved | — | — |
| 26-51 | Merchant Account Info | Yes (26 for X9.150) | Nested TLV |
| 52 | MCC | Yes | 4 digits |
| 53 | Currency | Yes | 3 digits (ISO 4217 numeric) |
| 54 | Amount | Optional | Decimal with 2 places |
| 55-57 | Reserved | — | — |
| 58 | Country | Yes | ISO 3166-1 alpha-2 |
| 59 | Merchant Name | Yes | Up to 25 chars |
| 60 | Merchant City | Yes | Up to 15 chars |
| 61 | Postal Code | Optional | Variable |
| 62 | Additional Data | Optional | Nested TLV |
| 63 | CRC | Yes | 4 hex chars, must be LAST |

## Common Issues

- **CRC Mismatch**: QR was modified after generation, or CRC calculation includes wrong range
- **Missing `org.x9`**: Tag 26 subtag 00 is not set — not an X9.150 QR
- **URL without protocol**: Normal — Tag 26.01 omits `https://` to save space
- **Amount encoding**: Tag 54 is in major units with 2 decimals (e.g., `0.56`), but the JSON payload `amountDue.amount` is in minor units as integer (e.g., `56`)
