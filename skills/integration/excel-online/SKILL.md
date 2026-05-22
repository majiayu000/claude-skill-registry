---
name: excel-online
description: Read and write Excel files via Microsoft Graph API. Manage workbooks, worksheets, and cells in OneDrive/SharePoint.
metadata: {"clawdbot":{"emoji":"📗","requires":{"env":["MICROSOFT_ACCESS_TOKEN"]}}}
---

# Excel Online (Microsoft Graph)

Excel automation via Microsoft 365.

## Environment

```bash
export MICROSOFT_ACCESS_TOKEN="xxxxxxxxxx"
```

## List Workbooks in OneDrive

```bash
curl "https://graph.microsoft.com/v1.0/me/drive/root/search(q='.xlsx')" \
  -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN"
```

## Get Worksheets

```bash
curl "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/workbook/worksheets" \
  -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN"
```

## Read Range

```bash
curl "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/workbook/worksheets/{sheet-name}/range(address='A1:D10')" \
  -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN"
```

## Write to Range

```bash
curl -X PATCH "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/workbook/worksheets/{sheet-name}/range(address='A1:B2')" \
  -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"values": [["Name", "Value"], ["Test", 123]]}'
```

## Add Worksheet

```bash
curl -X POST "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/workbook/worksheets" \
  -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "NewSheet"}'
```

## Create Table

```bash
curl -X POST "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/workbook/worksheets/{sheet-name}/tables/add" \
  -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"address": "A1:C5", "hasHeaders": true}'
```

## Run Formula

```bash
curl -X POST "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/workbook/functions/sum" \
  -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"values": [[1, 2, 3, 4, 5]]}'
```

## Links
- OneDrive: https://onedrive.live.com
- Docs: https://docs.microsoft.com/en-us/graph/api/resources/excel
