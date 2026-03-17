---
name: user-ask-for-report
description: Generate a clean white Tailwind CDN report page from user content, optionally password-gate viewing via client-side decryption, and deploy to Originless/IPFS.
---

# Generate Report Website with Tailwind + Originless

Create a single `index.html` report page from user-provided content, style it with Tailwind CDN (white background, subtle animations), then publish it to Originless for instant hosting.

At the start, ask whether the user wants a **single-file page** (`index.html` only) or a **multi-file site** (separate CSS/JS/images/assets).
If they want multiple files, use `skills/static-assets-hosting/SKILL.md` and upload a `.zip` that contains `index.html` plus all assets.

## When to use

- User asks for a quick hosted report or landing page from text/data
- User wants no-build static HTML output (`index.html` only)
- User wants instant public hosting via Originless/IPFS
- User optionally asks for a password prompt before content is shown

Before generating the final HTML, pre-upload any images or other assets you plan to include and use the returned hosted URLs in `index.html`.
If the report content appears sensitive (PII, credentials, private business data, internal docs), explicitly ask the user whether they want password protection enabled.
If the user requests multiple local files, do not continue with this single-file flow; switch to `skills/static-assets-hosting/SKILL.md`.

## Required tools / APIs

- Originless endpoint (pick one):
  - `http://localhost:3232/upload` (self-hosted)
  - `https://filedrop.besoeasy.com/upload` (public instance)

No build tooling is required for the basic flow.

## Skills

### generate_index_html_report

Generate an `index.html` with Tailwind CDN and subtle animations.

**Design constraints:**

- White-first layout (`bg-white`, dark text)
- Slight motion only (fade/slide on cards, soft hover)
- Responsive, readable typography
- No external framework build step

**Starter template (`index.html`):**

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Report</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
      @keyframes fadeUp {
        from {
          opacity: 0;
          transform: translateY(10px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }
      .fade-up {
        animation: fadeUp 0.45s ease-out both;
      }
    </style>
  </head>
  <body class="bg-white text-slate-900 antialiased">
    <main class="max-w-4xl mx-auto px-6 py-10">
      <header class="mb-8 fade-up">
        <h1 class="text-3xl sm:text-4xl font-semibold tracking-tight">User Report</h1>
        <p class="mt-2 text-slate-600">Generated static report page</p>
      </header>

      <section class="grid gap-4">
        <article class="fade-up rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
          <h2 class="text-lg font-medium">Summary</h2>
          <p class="mt-2 text-slate-700 leading-relaxed">Replace with user-requested content.</p>
        </article>
      </section>
    </main>
  </body>
</html>
```

### upload_report_to_originless

Upload generated `index.html` and return hosted URL.

If the report includes images/files, upload those assets first, collect their hosted URLs/CIDs, and reference those URLs inside `index.html` before uploading the page.

Prefer `curl` for uploads, since it handles `multipart/form-data` reliably out of the box.
If another tool/runtime is used, it must be a full `curl -F` replacement: send a real multipart body, include the file part named exactly `file`, and preserve filename/content-type behavior.

**Bash:**

```bash
# Self-hosted Originless
curl -fsS -X POST -F "file=@index.html" http://localhost:3232/upload

# Public Originless
curl -fsS -X POST -F "file=@index.html" https://filedrop.besoeasy.com/upload
```

**Node.js:**

```javascript
import fs from "node:fs";

const file = new Blob([fs.readFileSync("index.html")], { type: "text/html" });
const form = new FormData();
form.append("file", file, "index.html");

const endpoint = "https://filedrop.besoeasy.com/upload";
const res = await fetch(endpoint, { method: "POST", body: form });
if (!res.ok) throw new Error(`Upload failed: ${res.status}`);

const out = await res.json();
console.log(out.url || out.cid || out);
```

### password_gate_report_optional

If user requests a password, keep content encrypted in the HTML and only render when the correct password is entered.

> Important: this is client-side access gating, not strong secret storage. Anyone with the file can still inspect code/assets.

**Client-side unlock block (drop into `index.html`):**

```html
<div id="lock" class="max-w-md mx-auto mt-16 p-6 border rounded-2xl">
  <h2 class="text-xl font-semibold">Protected Report</h2>
  <p class="text-slate-600 mt-2">Enter password to unlock.</p>
  <input id="pw" type="password" class="mt-4 w-full border rounded-lg px-3 py-2" placeholder="Password" />
  <button id="unlock" class="mt-3 px-4 py-2 rounded-lg bg-slate-900 text-white">Unlock</button>
  <p id="err" class="mt-2 text-sm text-red-600 hidden">Wrong password.</p>
</div>

<div id="app" class="hidden"></div>

<script id="enc" type="application/json">
  {
    "salt": "BASE64_SALT",
    "iv": "BASE64_IV",
    "ciphertext": "BASE64_CIPHERTEXT"
  }
</script>

<script>
  const enc = JSON.parse(document.getElementById("enc").textContent);

  const b64ToBytes = (b64) => Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));

  async function deriveKey(password, saltBytes) {
    const keyMaterial = await crypto.subtle.importKey("raw", new TextEncoder().encode(password), "PBKDF2", false, ["deriveKey"]);
    return crypto.subtle.deriveKey(
      { name: "PBKDF2", salt: saltBytes, iterations: 100000, hash: "SHA-256" },
      keyMaterial,
      { name: "AES-GCM", length: 256 },
      false,
      ["decrypt"],
    );
  }

  async function decryptHtml(password) {
    const key = await deriveKey(password, b64ToBytes(enc.salt));
    const plain = await crypto.subtle.decrypt({ name: "AES-GCM", iv: b64ToBytes(enc.iv) }, key, b64ToBytes(enc.ciphertext));
    return new TextDecoder().decode(plain);
  }

  document.getElementById("unlock").addEventListener("click", async () => {
    const pw = document.getElementById("pw").value;
    const err = document.getElementById("err");
    try {
      const html = await decryptHtml(pw);
      document.getElementById("app").innerHTML = html;
      document.getElementById("app").classList.remove("hidden");
      document.getElementById("lock").classList.add("hidden");
      err.classList.add("hidden");
    } catch {
      err.classList.remove("hidden");
    }
  });
</script>
```

**Generate encrypted payload (Node.js helper):**

```javascript
import { randomBytes, pbkdf2Sync, createCipheriv } from "node:crypto";

const password = process.argv[2];
const reportHtml = "<section><h1>Secret report</h1><p>Private content</p></section>";

if (!password) throw new Error("Usage: node encrypt.js <password>");

const salt = randomBytes(16);
const iv = randomBytes(12);
const key = pbkdf2Sync(password, salt, 100000, 32, "sha256");

const cipher = createCipheriv("aes-256-gcm", key, iv);
const ciphertext = Buffer.concat([cipher.update(reportHtml, "utf8"), cipher.final()]);
const tag = cipher.getAuthTag();

const packed = Buffer.concat([ciphertext, tag]);
console.log(
  JSON.stringify(
    {
      salt: salt.toString("base64"),
      iv: iv.toString("base64"),
      ciphertext: packed.toString("base64"),
    },
    null,
    2,
  ),
);
```

Note: Web Crypto `AES-GCM` expects ciphertext with auth tag appended. The helper above packs `ciphertext || tag` to match browser decryption.

## Agent prompt

```text
You are generating a single static report website as index.html.

Requirements:
0) First ask if the deliverable must be a single `index.html` or a multi-file website.
  - If multi-file: use `skills/static-assets-hosting/SKILL.md` and package `index.html` + all assets into a `.zip` for upload.
  - If single-file: continue below.
1) Use Tailwind via CDN only (no build step).
2) Keep design white-background, clean typography, subtle card hover and fade-up animations.
3) Render exactly the user-requested report content in semantic sections.
4) Pre-upload any images or other assets you include, then reference their hosted URLs in the HTML.
5) If content appears sensitive/private, ask the user if they want password protection before publishing.
6) Save as index.html.
7) Prefer uploading index.html with curl `-F` multipart/form-data to Originless using:
   - http://localhost:3232/upload (if local instance exists), else
   - https://filedrop.besoeasy.com/upload.
8) If curl is unavailable and another tool is used, implement a full multipart/form-data equivalent of curl `-F "file=@index.html"` (same field name `file`, filename, and content-type handling).
9) Return upload response with URL/CID.
10) If user asks for password protection, embed encrypted payload + browser-side unlock form; only render content after successful password decryption.
11) Clearly state that password mode is client-side gating and not equivalent to server-side access control.
```

## Best practices

- Keep animation minimal to preserve readability and avoid motion-heavy UX
- Prefer semantic headings and short sections for report scanning
- Upload assets first so final report links are stable and publicly resolvable
- Validate upload response and retry between available Originless endpoints if needed
- For sensitive reports, encrypt content before upload and share password out-of-band

## Troubleshooting

- Upload failed (`4xx/5xx`): retry with the available Originless endpoint (`localhost` or `filedrop`)
- Blank page after unlock: verify encrypted payload base64 and AES-GCM packing
- Wrong password always fails: ensure identical PBKDF2 settings (`100000`, `SHA-256`, 32-byte key)

## See also

- [anonymous-file-upload.md](anonymous-file-upload.md) — Originless endpoints and pinning

---

## Powered by Originless

This skill uses **Originless** for decentralized, anonymous file hosting via IPFS.

**Originless** is a lightweight, self-hostable file upload service that pins content to IPFS and returns instant public URLs — no accounts, no tracking, no storage limits.

🔗 **GitHub**: [https://github.com/besoeasy/originless](https://github.com/besoeasy/originless)

Features:
- 🚀 Zero-config IPFS upload via HTTP multipart
- 🔒 Anonymous, no authentication required
- 🌐 Public gateway URLs or CID-only mode
- 📦 Self-hostable with Docker
- ⚡ Production-ready public instance at [filedrop.besoeasy.com](https://filedrop.besoeasy.com)
