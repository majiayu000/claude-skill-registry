---
name: share
description: Publish an HTML file to sharable.link and get a shareable URL, or remove a previously shared page. Use when the user says "share this", "publish this", "make this shareable", "share link", "/share", "unshare", "/unshare", or "remove shared page". Supports optional password protection.
allowed-tools: Read, Bash, Glob
---

Publish an HTML file to sharable.link so it's accessible via a unique public URL, or remove a previously shared page.

---

## SHARE FLOW

Use this flow when the user wants to publish / share a page.

### Steps

1. **Find the HTML file to share:**
   - If the user provided a file path in `$ARGUMENTS`, use that file.
   - Otherwise, use Glob to find the most recently created `.html` file in the project (check common output locations: current directory, `out/`, `dist/`, `build/`, `output/`).
   - If multiple HTML files exist and none was specified, list them and ask which one to share.

2. **Read the file** using the Read tool. Verify it contains HTML content.

3. **Ask about password protection** (optional):
   - Ask the user: "Do you want to password-protect this link?"
   - If yes, ask for the password they want to use.

4. **Publish it** by running this curl command via Bash:

```bash
# Without password:
curl -sL -X POST https://sharable.vercel.app/api/publish \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg html "$(cat FILE_PATH)" '{html: $html}')"

# With password:
curl -sL -X POST https://sharable.vercel.app/api/publish \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg html "$(cat FILE_PATH)" --arg pw "PASSWORD" '{html: $html, password: $pw}')"
```

Replace `FILE_PATH` with the actual path to the HTML file, and `PASSWORD` with the user's chosen password.

5. **Return the result** — parse the JSON response and show the user the shareable URL and delete key. Format it clearly like:

> Published! Your sharable link: https://sharable.link/abc123
>
> Delete key: `a1b2c3d4...` — save this if you ever want to remove the page.

If password-protected, also add:

> This link is password-protected. Share the password separately with your recipients.

---

## UNSHARE FLOW

Use this flow when the user wants to remove / unshare / delete a previously shared page.

### Steps

1. **Get the slug:**
   - If the user provided a URL or slug in `$ARGUMENTS`, extract the slug (the part after `sharable.link/`).
   - Otherwise, ask: "Which page do you want to remove? Provide the URL or slug."

2. **Get the delete key:**
   - If the delete key is available in the current conversation (e.g. from a recent share), use it directly.
   - Otherwise, ask: "What is the delete key for this page? (It was shown when you first shared it.)"

3. **Delete it** by running this curl command via Bash:

```bash
curl -sL -X POST https://sharable.vercel.app/api/delete \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg slug "SLUG" --arg key "DELETE_KEY" '{slug: $slug, deleteKey: $key}')"
```

Replace `SLUG` with the page slug and `DELETE_KEY` with the user's delete key.

4. **Return the result** — parse the JSON response:

If successful:
> Done! The page sharable.link/SLUG has been removed.

If the key is wrong (403):
> The delete key is incorrect. Please check and try again.

If the page doesn't exist (404):
> That page was not found. It may have already been removed.
