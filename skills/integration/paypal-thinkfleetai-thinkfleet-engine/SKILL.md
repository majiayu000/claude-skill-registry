---
name: paypal
description: "Manage PayPal — orders, payments, refunds, and payouts via the REST API."
metadata: {"thinkfleetbot":{"emoji":"💵","requires":{"bins":["curl","jq"],"env":["PAYPAL_CLIENT_ID","PAYPAL_CLIENT_SECRET"]}}}
---

# PayPal

Manage orders, payments, refunds, and payouts.

## Environment Variables

- `PAYPAL_CLIENT_ID` - Client ID
- `PAYPAL_CLIENT_SECRET` - Client secret

## Get access token

```bash
curl -s -X POST "https://api-m.paypal.com/v1/oauth2/token" \
  -u "$PAYPAL_CLIENT_ID:$PAYPAL_CLIENT_SECRET" \
  -d "grant_type=client_credentials" | jq '{access_token, expires_in}'
```

## Create order

```bash
TOKEN=$(curl -s -X POST "https://api-m.paypal.com/v1/oauth2/token" -u "$PAYPAL_CLIENT_ID:$PAYPAL_CLIENT_SECRET" -d "grant_type=client_credentials" | jq -r '.access_token')
curl -s -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://api-m.paypal.com/v2/checkout/orders" \
  -d '{"intent":"CAPTURE","purchase_units":[{"amount":{"currency_code":"USD","value":"10.00"}}]}' | jq '{id, status}'
```

## List transactions

```bash
TOKEN=$(curl -s -X POST "https://api-m.paypal.com/v1/oauth2/token" -u "$PAYPAL_CLIENT_ID:$PAYPAL_CLIENT_SECRET" -d "grant_type=client_credentials" | jq -r '.access_token')
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api-m.paypal.com/v1/reporting/transactions?start_date=2024-01-01T00:00:00Z&end_date=2024-12-31T23:59:59Z&fields=all&page_size=10" | jq '.transaction_details[] | {transaction_id: .transaction_info.transaction_id, amount: .transaction_info.transaction_amount}'
```

## Notes

- Use `api-m.sandbox.paypal.com` for testing.
- Always confirm before creating orders or issuing refunds.
