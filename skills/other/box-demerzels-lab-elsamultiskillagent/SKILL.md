---
name: box
description: Manage files and folders via Box API. Upload, download, and share content securely.
metadata: {"clawdbot":{"emoji":"📦","requires":{"env":["BOX_ACCESS_TOKEN"]}}}
---
# Box
Enterprise cloud storage.
## Environment
```bash
export BOX_ACCESS_TOKEN="xxxxxxxxxx"
```
## List Files in Folder
```bash
curl "https://api.box.com/2.0/folders/0/items" -H "Authorization: Bearer $BOX_ACCESS_TOKEN"
```
## Upload File
```bash
curl -X POST "https://upload.box.com/api/2.0/files/content" \
  -H "Authorization: Bearer $BOX_ACCESS_TOKEN" \
  -F "attributes={\"name\":\"file.txt\",\"parent\":{\"id\":\"0\"}}" \
  -F "file=@localfile.txt"
```
## Download File
```bash
curl "https://api.box.com/2.0/files/{fileId}/content" -H "Authorization: Bearer $BOX_ACCESS_TOKEN" -o file.txt
```
## Links
- Docs: https://developer.box.com
