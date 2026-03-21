---
name: file-transfer
description: "[TRANSFER:remote-to-remote|direct=true]=>[NEVER:local-download-upload]"
---
[RULE:always]remote-to-remote=wget/curl|never=download-then-upload
[PATTERN1]source:temp-HTTP(nginx/python)=>destination:wget-direct
[PATTERN2]source=>COS/S3/R2=>destination
[SAY:"文件直接从那边拉过来了，不用你自己下载上传。"]
[CLI:ossutil|rclone|s3cmd|for=object-storage]
