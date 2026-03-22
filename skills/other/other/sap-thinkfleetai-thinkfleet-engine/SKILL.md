---
name: sap
description: "Query SAP systems — business partners, sales orders, materials, and financials via OData APIs."
metadata: {"thinkfleetbot":{"emoji":"🏢","requires":{"bins":["curl","jq"],"env":["SAP_BASE_URL","SAP_API_KEY"]}}}
---

# SAP

Query business partners, sales orders, and materials via SAP OData APIs.

## Environment Variables

- `SAP_BASE_URL` - SAP API base URL
- `SAP_API_KEY` - API key

## List business partners

```bash
curl -s -H "APIKey: $SAP_API_KEY" \
  "$SAP_BASE_URL/sap/opu/odata/sap/API_BUSINESS_PARTNER/A_BusinessPartner?\$top=10&\$select=BusinessPartner,BusinessPartnerFullName" | jq '.d.results[]'
```

## List sales orders

```bash
curl -s -H "APIKey: $SAP_API_KEY" \
  "$SAP_BASE_URL/sap/opu/odata/sap/API_SALES_ORDER_SRV/A_SalesOrder?\$top=10&\$select=SalesOrder,SoldToParty,TotalNetAmount" | jq '.d.results[]'
```

## Get material

```bash
curl -s -H "APIKey: $SAP_API_KEY" \
  "$SAP_BASE_URL/sap/opu/odata/sap/API_PRODUCT_SRV/A_Product?\$top=10&\$select=Product,ProductType" | jq '.d.results[]'
```

## Notes

- Always confirm before creating or modifying business data.
