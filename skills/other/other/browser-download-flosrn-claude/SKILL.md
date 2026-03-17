---
name: browser-download
description: Download files from authenticated web sessions. Use when the browser tool cannot directly download files (attachments, exports) and you need to use cookies with curl.
---

# Browser Download Workaround

The `browser` tool doesn't support direct file downloads. Use this workaround to download files from authenticated sessions.

## Method

1. Extract cookies from the browser session
2. Use curl with those cookies to download

## Step 1: Extract Cookies

```javascript
// In browser act → evaluate
document.cookie
```

## Step 2: Download with curl

```bash
curl -L -b "cookie1=value1; cookie2=value2" -o /path/to/output.file "https://url/to/download"
```

## Gmail Attachment Example

```bash
# 1. Get cookies from Gmail session
# browser act → evaluate → document.cookie

# 2. Download attachment
curl -L \
  -b "GMAIL_AT=xxx; SID=yyy; HSID=zzz" \
  -o ~/Downloads/attachment.pdf \
  "https://mail.google.com/mail/u/0?ui=2&ik=xxx&attid=0.1&disp=safe&realattid=xxx&zw"
```

## Google Drive Example

```bash
curl -L \
  -b "SID=xxx; HSID=yyy" \
  -o ~/Downloads/file.pdf \
  "https://drive.google.com/uc?export=download&id=FILE_ID"
```

## Tips

- Use `-L` to follow redirects
- Use `-o` to specify output filename
- Some sites require additional headers: `-H "User-Agent: Mozilla/5.0..."`
- For large files, add `--progress-bar` to see download progress

## Alternative: Browser Screenshot/Print

For documents that can't be downloaded:
1. Navigate to the document in browser
2. Use `browser screenshot --fullPage` to capture
3. Or use `browser pdf` to save as PDF (if supported)
