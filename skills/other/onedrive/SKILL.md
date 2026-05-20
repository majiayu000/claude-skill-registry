---
name: onedrive
description: Manage OneDrive files and folders via Microsoft Graph. Upload, download, and share files.
metadata: {"thinkfleet":{"emoji":"☁️","requires":{"env":["MICROSOFT_ACCESS_TOKEN"]}}}
---
# OneDrive
Microsoft cloud storage.
## Environment
```bash
export MICROSOFT_ACCESS_TOKEN="xxxxxxxxxx"
```
## List Root Files
```bash
curl "https://graph.microsoft.com/v1.0/me/drive/root/children" -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN"
```
## Upload File
```bash
curl -X PUT "https://graph.microsoft.com/v1.0/me/drive/root:/filename.txt:/content" \
  -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary @localfile.txt
```
## Download File
```bash
curl "https://graph.microsoft.com/v1.0/me/drive/items/{itemId}/content" \
  -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN" -o downloaded.txt
```
## Links
- Docs: https://docs.microsoft.com/en-us/graph/api/resources/onedrive
