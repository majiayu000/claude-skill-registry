---
name: adobe
description: Access Adobe Creative Cloud APIs - Photoshop, Lightroom, PDF Services, and Firefly AI. Automate creative workflows.
metadata: {"clawdbot":{"emoji":"🎨","requires":{"env":["ADOBE_CLIENT_ID","ADOBE_ACCESS_TOKEN"]}}}
---

# Adobe Creative Cloud

Creative and document APIs.

## Environment

```bash
export ADOBE_CLIENT_ID="xxxxxxxxxx"
export ADOBE_ACCESS_TOKEN="xxxxxxxxxx"
```

## Photoshop API - Remove Background

```bash
curl -X POST "https://image.adobe.io/sensei/cutout" \
  -H "Authorization: Bearer $ADOBE_ACCESS_TOKEN" \
  -H "x-api-key: $ADOBE_CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {"href": "https://example.com/image.jpg", "storage": "external"},
    "output": {"href": "https://your-bucket.s3.amazonaws.com/output.png", "storage": "external"}
  }'
```

## PDF Services - Create PDF

```bash
curl -X POST "https://pdf-services.adobe.io/operation/createpdf" \
  -H "Authorization: Bearer $ADOBE_ACCESS_TOKEN" \
  -H "x-api-key: $ADOBE_CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "assetID": "{asset_id}"
  }'
```

## PDF Services - Export PDF to Word

```bash
curl -X POST "https://pdf-services.adobe.io/operation/exportpdf" \
  -H "Authorization: Bearer $ADOBE_ACCESS_TOKEN" \
  -H "x-api-key: $ADOBE_CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "assetID": "{asset_id}",
    "targetFormat": "docx"
  }'
```

## Firefly - Generate Image (AI)

```bash
curl -X POST "https://firefly-api.adobe.io/v2/images/generate" \
  -H "Authorization: Bearer $ADOBE_ACCESS_TOKEN" \
  -H "x-api-key: $ADOBE_CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A futuristic cityscape at sunset",
    "n": 1,
    "size": {"width": 1024, "height": 1024}
  }'
```

## Lightroom - Get Catalog

```bash
curl "https://lr.adobe.io/v2/catalogs" \
  -H "Authorization: Bearer $ADOBE_ACCESS_TOKEN" \
  -H "x-api-key: $ADOBE_CLIENT_ID"
```

## Links
- Console: https://developer.adobe.com/console
- Docs: https://developer.adobe.com/apis
