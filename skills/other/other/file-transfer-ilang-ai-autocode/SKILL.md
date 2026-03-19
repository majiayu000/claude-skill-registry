---
name: file-transfer
description: Help user move files between servers. Always use remote pull, never local download-upload.
---

# File Transfer

When user needs to move files:
1. ALWAYS use remote-to-remote transfer: wget/curl from source to destination
2. NEVER tell user to download to their computer then upload
3. If files need to go to object storage, use CLI tools (ossutil, rclone, s3cmd)

Pattern:
- Source server: make files accessible via HTTP (temporary nginx or python http.server)
- Destination: wget the files directly

Or use object storage as intermediary:
- Upload to COS/S3/R2 from source
- Download from COS/S3/R2 on destination

Tell user: "文件直接从那边拉过来了，不用你自己下载上传。"
