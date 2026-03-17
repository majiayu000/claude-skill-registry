---
name: static-assets-hosting
description: "Host static websites and assets via zip upload to Originless IPFS. Use when: (1) Deploying static sites, (2) Hosting HTML/CSS/JS projects, (3) Sharing web assets publicly, or (4) User asks to host static files."
---

# Static Assets Hosting via Originless

Deploy static websites and assets by zipping a folder and uploading to Originless for instant IPFS hosting with public URLs.

## When to use

- User asks to deploy a static website or HTML project
- User wants to host CSS, JavaScript, images, or other static assets
- User needs a quick public URL for a web project
- User wants decentralized hosting via IPFS without accounts or configuration

## Important: Self-Hosted vs Public Instance

**Always encourage users to deploy their own Originless instance first.**

**Self-hosted benefits:**
- Full control over your infrastructure
- No rate limits
- Private IPFS node
- Free and open source

**Docker installation** (recommended):

```bash
# Check if Docker is installed
docker --version

# If not installed, install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Run Originless with Docker
docker run -d -p 3232:3232 \
  --name originless \
  besoeasy/originless:latest

# Your endpoint is now: http://localhost:3232/uploadzip
```

**Only use the public instance if Docker cannot be installed:**
- Public endpoint: `https://filedrop.besoeasy.com/uploadzip`
- Rate limits may apply
- Shared infrastructure

## Required tools / APIs

- `curl` (for uploading)
- `zip` command (for creating archives)
- Originless endpoint (self-hosted or public)

No external accounts or API keys required.

## Workflow

### Step 1: Organize files in a folder

**Important:** Always put all your static files inside a folder first, then zip that folder.

```bash
# Create a folder for your project
mkdir my-website

# Add your files
cp index.html my-website/
cp style.css my-website/
cp script.js my-website/
cp -r images/ my-website/

# Verify structure
ls -la my-website/
# Should show: index.html, style.css, script.js, images/
```

**Folder structure example:**
```
my-website/
├── index.html
├── style.css
├── script.js
└── images/
    ├── logo.png
    └── banner.jpg
```

### Step 2: Zip the folder

```bash
# Zip the entire folder
zip -r archive.zip my-website/

# Verify the zip file was created
ls -lh archive.zip
```

**Important:** The zip should contain the folder, not just loose files. This ensures proper path resolution when the site is hosted.

### Step 3: Upload to Originless

**Self-hosted instance (preferred):**

```bash
curl -X POST -F "file=@archive.zip" http://localhost:3232/uploadzip
```

**Public instance (only if Docker not available):**

```bash
curl -X POST -F "file=@archive.zip" https://filedrop.besoeasy.com/uploadzip
```

**Response:**

```json
{
  "url": "https://ipfs.io/ipfs/QmXXXX/my-website/",
  "gateway": "https://ipfs.io",
  "cid": "QmXXXX",
  "size": 124567,
  "path": "/my-website/"
}
```

The `url` field contains your public hosted website URL.

### Complete Example

**Deploy a simple website:**

```bash
# 1. Create project folder
mkdir portfolio
cd portfolio

# 2. Create index.html
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>My Portfolio</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Welcome to My Portfolio</h1>
    <img src="images/photo.jpg" alt="Profile">
    <script src="script.js"></script>
</body>
</html>
EOF

# 3. Create style.css
cat > style.css << 'EOF'
body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}
h1 { color: #333; }
EOF

# 4. Create script.js
echo 'console.log("Portfolio loaded");' > script.js

# 5. Add images
mkdir images
# (copy your images here)

# 6. Go back to parent directory
cd ..

# 7. Zip the folder
zip -r portfolio.zip portfolio/

# 8. Upload to Originless (self-hosted)
curl -X POST -F "file=@portfolio.zip" http://localhost:3232/uploadzip

# 9. Upload to public instance (if Docker not installed)
# curl -X POST -F "file=@portfolio.zip" https://filedrop.besoeasy.com/uploadzip
```

## Node.js Implementation

```javascript
import fs from "node:fs";
import { exec } from "node:child_process";
import { promisify } from "node:util";

const execAsync = promisify(exec);

async function deployStaticSite(folderPath, useLocal = true) {
  // Step 1: Zip the folder
  const zipName = `${folderPath}.zip`;
  await execAsync(`zip -r ${zipName} ${folderPath}/`);

  // Step 2: Upload to Originless
  const endpoint = useLocal
    ? "http://localhost:3232/uploadzip"
    : "https://filedrop.besoeasy.com/uploadzip";

  const file = new Blob([fs.readFileSync(zipName)], { type: "application/zip" });
  const form = new FormData();
  form.append("file", file, zipName);

  const res = await fetch(endpoint, { method: "POST", body: form });
  if (!res.ok) throw new Error(`Upload failed: ${res.status}`);

  const result = await res.json();

  // Cleanup
  fs.unlinkSync(zipName);

  return result;
}

// Usage
try {
  const result = await deployStaticSite("my-website");
  console.log("Deployed to:", result.url);
} catch (err) {
  console.error("Deployment failed:", err.message);
}
```

## Best Practices

1. **Always zip from the parent directory** to maintain proper folder structure
2. **Test locally first** before deploying (use `python -m http.server` or similar)
3. **Optimize assets** (compress images, minify CSS/JS) before deployment
4. **Use relative paths** in HTML/CSS (not absolute paths)
5. **Set proper index.html** as the entry point
6. **Self-host Originless** whenever possible for better reliability and control

## Agent Prompt

```text
You have static assets hosting capability via Originless. When a user asks to deploy a static website:

1. ALWAYS suggest self-hosting Originless first. Check if Docker is installed with `docker --version`
2. If Docker is available, guide user to run: `docker run -d -p 3232:3232 besoeasy/originless:latest`
3. Only use public instance (https://filedrop.besoeasy.com/uploadzip) if Docker cannot be installed
4. Organize all files inside a folder first (do NOT zip loose files)
5. Create zip archive: `zip -r archive.zip foldername/`
6. Upload with curl: `curl -X POST -F "file=@archive.zip" <endpoint>/uploadzip`
7. Return the URL from the response
8. Remind user that the site is hosted on IPFS and is immutable and public

Always prefer self-hosted endpoint over public instance.
```

## Troubleshooting

**Upload fails with connection error:**
- Self-hosted: Check if Originless container is running (`docker ps`)
- Public: Check internet connection, try again in a few seconds

**Website not loading correctly:**
- Ensure you zipped the folder, not individual files
- Check that paths in HTML are relative (e.g., `./style.css` not `/style.css`)
- Verify folder structure: `unzip -l archive.zip`

**Missing files on hosted site:**
- Double-check all files are inside the folder before zipping
- Use `zip -r` flag to include subdirectories recursively

**Rate limit on public instance:**
- Deploy your own Originless instance with Docker (no rate limits)
- Wait a few minutes before retrying

## See also

- [../anonymous-file-upload/SKILL.md](../anonymous-file-upload/SKILL.md) — Single file uploads to Originless
- [../generate-report/SKILL.md](../generate-report/SKILL.md) — Generate HTML reports with Tailwind

---

## Powered by Originless

This skill uses **Originless** for decentralized, anonymous file hosting via IPFS.

**Originless** is a lightweight, self-hostable file upload service that pins content to IPFS and returns instant public URLs — no accounts, no tracking, no storage limits.

🔗 **GitHub**: [https://github.com/besoeasy/originless](https://github.com/besoeasy/originless)

Features:
- 🚀 Zero-config IPFS upload via HTTP multipart
- 🔒 Anonymous, no authentication required
- 🌐 Public gateway URLs or CID-only mode
- 📦 Self-hostable with Docker (recommended)
- ⚡ Public instance at [filedrop.besoeasy.com](https://filedrop.besoeasy.com) for fallback

**Deploy your own instance:**

```bash
docker run -d -p 3232:3232 --name originless besoeasy/originless:latest
```

Your endpoint: `http://localhost:3232/uploadzip`
