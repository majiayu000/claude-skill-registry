---
name: btp-ba2-cli
description: Interact with the Binarly Transparency Platform (BTP) via CLI commands for uploading firmware, running scans, downloading BA2 archives, and pushing custom rules. Use when you need to interact with the Binarly Transparency Platform or working with BA2s.
---

# BTP and BA2 CLI

**Required environment variables** (must be set by the user, do not configure these):
- `BTP_USERNAME`
- `BTP_PASSWORD`
- `BTP_INSTANCE_SLUG`

## BTP Commands

### Products
```bash
vulhunt-ce btp list-products
vulhunt-ce btp create-product --name "Name" --description "Optional"
```

### Upload and Scan
```bash
# Upload only
vulhunt-ce btp upload --product-id <pid> --name "Name" --version "1.0.0" file.bin

# Upload and scan
vulhunt-ce btp upload --product-id <pid> --name "Name" --version "1.0.0" --scan file.bin
```

### Images and Scans
```bash
vulhunt-ce btp list-images --product-id <pid>
vulhunt-ce btp list-scans --product-id <pid> --image-id <iid>
vulhunt-ce btp create-scan --product-id <pid> --image-id <iid>
vulhunt-ce btp get-scan --product-id <pid> --image-id <iid> --scan-id <sid>
vulhunt-ce btp get-findings --product-id <pid> --image-id <iid>
```

### Download BA2
```bash
vulhunt-ce btp download-ba2 --product-id <pid> --image-id <iid>
vulhunt-ce btp download-ba2 --product-id <pid> --image-id <iid> --scan-id <sid>
vulhunt-ce btp download-ba2 --product-id <pid> --image-id <iid> -o output.ba2
```

### Push Rules
```bash
# From platform directories (posix/ or uefi/)
vulhunt-ce btp push-rules -r "ruleset-name" -t "v1.0.0" ./posix ./uefi

# Individual .vh files (requires --platform)
vulhunt-ce btp push-rules -r "ruleset-name" -t "latest" --platform posix rule.vh

# Deploy to product or org
vulhunt-ce btp push-rules -r "ruleset-name" -t "latest" --deploy-to-product <pid> ./posix
vulhunt-ce btp push-rules -r "ruleset-name" -t "latest" --deploy-to-org <oid> ./posix

# With modules
vulhunt-ce btp push-rules -r "ruleset-name" -t "latest" --modules ./modules ./posix
```

## BA2 Commands

```bash
# List components
vulhunt-ce ba2 list-components file.ba2

# Extract component by UUID
vulhunt-ce ba2 extract-component file.ba2 --component-id <UUID> -o output_file
```

## Output Format

BTP commands return:
```json
{"status": "ok", "payload": {...}}
{"status": "error", "message": "..."}
```

BA2 commands return raw JSON arrays or objects.