---
name: sell
description: Transform a Vibes app into a multi-tenant SaaS with subdomain-based tenancy. Adds Clerk authentication, subscription gating, and generates a unified app with landing page, tenant routing, and admin dashboard.
license: MIT
allowed-tools: Read, Write, Bash, Glob, AskUserQuestion
---

**Display this ASCII art immediately when starting:**

```
░▒▓███████▓▒░▒▓████████▓▒░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░
 ░▒▓██████▓▒░░▒▓██████▓▒░ ░▒▓█▓▒░      ░▒▓█▓▒░
       ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░
       ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓███████▓▒░░▒▓████████▓▒░▒▓████████▓▒░▒▓████████▓▒░
```

## Quick Navigation

- [Critical Rules](#-critical-rules---read-first-) - Read this first
- [Step 1: Pre-Flight Checks](#step-1-pre-flight-checks) - Verify prerequisites
- [Step 2: Clerk Configuration](#step-2-clerk-configuration-required) - Set up authentication (REQUIRED)
- [Step 3: App Configuration](#step-3-app-configuration) - Collect app settings
- [Step 4: Assembly](#step-4-assembly) - Build the unified app
- [Step 5: Deployment](#step-5-deployment) - Go live with exe.dev
- [Step 6: Post-Deploy Verification](#step-6-post-deploy-verification) - Confirm everything works
- [Key Components](#key-components) - Routing, TenantContext, SubscriptionGate
- [Troubleshooting](#troubleshooting) - Common issues and fixes

---

## ⛔ CRITICAL RULES - READ FIRST ⛔

**DO NOT generate code manually.** This skill uses pre-built scripts:

| Step | Script | What it does |
|------|--------|--------------|
| Assembly | `assemble-sell.js` | Generates unified index.html |
| Deploy | `deploy-exe.js` | Deploys to exe.dev with registry |

**Script location:**
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/assemble-sell.js" ...
node "${CLAUDE_PLUGIN_ROOT}/scripts/deploy-exe.js" ...
```

**NEVER do these manually:**
- ❌ Write HTML/JSX for landing page, tenant app, or admin dashboard
- ❌ Generate routing logic or authentication code
- ❌ Deploy without `--clerk-key` and `--clerk-webhook-secret`

**ALWAYS do these:**
- ✅ Complete pre-flight checks before starting
- ✅ Collect ALL Clerk credentials BEFORE app configuration
- ✅ Run `assemble-sell.js` to generate the unified app
- ✅ Deploy with ALL required flags

---

# Sell - Transform Vibes to SaaS

This skill uses `assemble-sell.js` to inject the user's app into a pre-built template. The template contains security checks, proper Clerk integration, and Fireproof patterns.

Convert your Vibes app into a multi-tenant SaaS product with:
- Subdomain-based tenancy (alice.yourdomain.com)
- Clerk authentication with passkeys
- Subscription gating via Clerk Billing
- Per-tenant Fireproof database isolation
- Marketing landing page
- Admin dashboard

## Architecture

The sell skill generates a **single index.html** file that handles all routes via client-side subdomain detection:

```
yourdomain.com          → Landing page
*.yourdomain.com        → Tenant app with auth
admin.yourdomain.com    → Admin dashboard
```

This approach simplifies deployment - you upload one file and it handles everything.

---

## Step 1: Pre-Flight Checks

**Before starting, verify these prerequisites. STOP if any check fails.**

### 1.1 Check for Fireproof Connect

Run this command to check if Connect is configured:

```bash
cat .env 2>/dev/null | grep VITE_API_URL || echo "NOT_FOUND"
```

**If output shows `NOT_FOUND`:**
> "Fireproof Connect is not configured. Run `/vibes:connect` first to set up your sync backend, then return to `/vibes:sell`."

**STOP HERE** if Connect is not configured. The sell skill requires cloud sync for multi-tenant data isolation.

### 1.2 Detect Existing App

```bash
ls -la app.jsx 2>/dev/null || echo "NOT_FOUND"
```

**If output shows `NOT_FOUND`:**

Check for riff directories:
```bash
ls -d riff-* 2>/dev/null
```

**Decision tree:**
- Found `app.jsx` → Proceed to Step 2
- Found multiple `riff-*/app.jsx` → Ask user to select one, then copy to `app.jsx`
- Found nothing → Tell user to run `/vibes:vibes` first

**STOP HERE** if no app exists. The sell skill transforms existing apps.

### 1.3 Pre-Flight Summary

After both checks pass, confirm:
> "Pre-flight checks passed:
> - ✓ Fireproof Connect configured (.env found)
> - ✓ App found (app.jsx)
>
> Now let's configure Clerk authentication. This is required for multi-tenant SaaS."

---

## Step 2: Clerk Configuration (REQUIRED)

**These credentials are REQUIRED. Do not proceed without them.**

### 2.1 Clerk Dashboard Setup Instructions

Before collecting credentials, the user must set up Clerk. Present these instructions:

> **Clerk Setup Required**
>
> Before we continue, you need to configure Clerk authentication:
>
> 1. **Create a Clerk Application** at [clerk.com](https://clerk.com)
>    - Choose "Email + Passkey" authentication
>
> 2. **Configure Email Settings** (Dashboard → User & Authentication → Email):
>    | Setting | Value | Why |
>    |---------|-------|-----|
>    | Sign-up with email | ✅ ON | Users sign up via email |
>    | Require email address | ⬜ **OFF** | **CRITICAL** - signup fails if ON |
>    | Verify at sign-up | ✅ ON | Verify before session |
>    | Email verification code | ✅ Checked | Use code for verification |
>
> 3. **Configure Passkey Settings** (Dashboard → User & Authentication → Passkeys):
>    | Setting | Value |
>    |---------|-------|
>    | Sign-in with passkey | ✅ ON |
>    | Allow autofill | ✅ ON |
>    | Show passkey button | ✅ ON |
>    | Add passkey to account | ✅ ON |
>
> 4. **Create Webhook** (Dashboard → Configure → Webhooks):
>    - Click "Add Endpoint"
>    - Enter URL: `https://YOUR-APP.exe.xyz/webhook` (we'll confirm the name later)
>    - Select events: `user.created`, `user.deleted`, `subscription.*`
>    - Click "Create"
>    - Copy the **"Signing Secret"** (starts with `whsec_`)
>
> See [CLERK-SETUP.md](./CLERK-SETUP.md) for complete details.
>
> **When you're ready, I'll collect your Clerk credentials.**

### 2.2 Collect Clerk Credentials

Use AskUserQuestion with these 3 questions:

```
Question 1: "What's your Clerk Publishable Key?"
Header: "Clerk Key"
Options: User enters via "Other"
Description: "From Clerk Dashboard → API Keys. Starts with pk_test_ or pk_live_"

Question 2: "What's your Clerk JWKS Public Key?"
Header: "JWKS Key"
Options: User enters via "Other"
Description: "From Clerk Dashboard → API Keys → scroll to 'Show JWT Public Key'. Starts with -----BEGIN PUBLIC KEY-----"

Question 3: "What's your Clerk Webhook Secret?"
Header: "Webhook"
Options: User enters via "Other"
Description: "From the webhook you created. Starts with whsec_"
```

### 2.3 Validation Gate

**Before proceeding, validate ALL credentials:**

| Credential | Valid Format | If Invalid |
|------------|--------------|------------|
| Publishable Key | Starts with `pk_test_` or `pk_live_` | Stop, ask for correct key |
| JWKS Public Key | Starts with `-----BEGIN PUBLIC KEY-----` | Stop, guide to JWT Public Key location |
| Webhook Secret | Starts with `whsec_` | Stop, guide to webhook creation |

**If ANY validation fails:** Stop and help user get the correct credential. Do not proceed to Step 3.

### 2.4 Save JWKS Key to File

After receiving and validating the JWKS key, save it to a file for the deploy command:

```bash
cat > clerk-jwks-key.pem << 'EOF'
-----BEGIN PUBLIC KEY-----
[THE USER'S KEY CONTENT HERE]
-----END PUBLIC KEY-----
EOF
```

Verify the file was created:
```bash
head -1 clerk-jwks-key.pem
```

**Expected output:** `-----BEGIN PUBLIC KEY-----`

### 2.5 Clerk Configuration Complete

Confirm to the user:
> "Clerk credentials validated and saved:
> - ✓ Publishable Key: pk_test_... (saved for assembly)
> - ✓ JWKS Key: Saved to clerk-jwks-key.pem (for deployment)
> - ✓ Webhook Secret: whsec_... (saved for deployment)
>
> Now let's configure your app settings."

---

## Step 3: App Configuration

**Use AskUserQuestion to collect all config in 2 batches.**

### Batch 1: Core Identity

Use the AskUserQuestion tool with these 4 questions:

```
Question 1: "What should we call this app?"
Header: "App Name"
Options: Provide 2 suggestions based on context + user enters via "Other"
Description: "Used for database naming and deployment URL (e.g., 'wedding-photos')"

Question 2: "What domain will this deploy to?"
Header: "Domain"
Options: ["Use exe.xyz subdomain", "Custom domain"]
Description: "exe.xyz is instant. Custom domains require DNS setup."

Question 3: "Do you want to require paid subscriptions?"
Header: "Billing"
Options: ["No - free access for all", "Yes - subscription required"]
Description: "Billing is configured in Clerk Dashboard → Billing"

Question 4: "Display title for your app?"
Header: "Title"
Options: Suggest based on app name + user enters via "Other"
Description: "Shown in headers and landing page"
```

### Batch 2: Customization

Use the AskUserQuestion tool with these 3 questions:

```
Question 1: "Tagline for the landing page headline?"
Header: "Tagline"
Options: Generate 2 suggestions based on app context + user enters via "Other"
Description: "Bold headline text. Can include <br> for line breaks (e.g., 'SHARE YOUR DAY.<br>MAKE IT SPECIAL.')"

Question 2: "Subtitle text below the tagline?"
Header: "Subtitle"
Options: Generate 2 suggestions based on app context + user enters via "Other"
Description: "Explanatory text below the headline (e.g., 'The easiest way to share wedding photos with guests.')"

Question 3: "What features should we highlight on the landing page?"
Header: "Features"
Options: User enters via "Other"
Description: "Comma-separated list (e.g., 'Photo sharing, Guest uploads, Live gallery')"
```

### After Receiving Answers

1. If user selected "Custom domain", ask for the domain name
2. Admin User IDs default to empty (configured after first deploy - see Step 6)
3. **Proceed immediately to Step 4 (Assembly)**

### Config Values Reference

| Config | Script Flag | Example |
|--------|-------------|---------|
| App Name | `--app-name` | `wedding-photos` |
| Domain | `--domain` | `myapp.exe.xyz` |
| Billing | `--billing-mode` | `off` or `required` |
| Clerk Publishable Key | `--clerk-key` | `pk_test_xxx` |
| Title | `--app-title` | `Wedding Photos` |
| Tagline | `--tagline` | `SHARE YOUR DAY.<br>MAKE IT SPECIAL.` |
| Subtitle | `--subtitle` | `The easiest way to share wedding photos with guests.` |
| Features | `--features` | `'["Feature 1","Feature 2"]'` |
| Admin IDs | `--admin-ids` | `'["user_xxx"]'` (default: `'[]'`) |

---

## Step 4: Assembly

**CRITICAL**: You MUST use the assembly script. Do NOT generate your own HTML/JSX code.

### 4.1 Verify .env Exists

Before running assembly, verify the .env file exists:

```bash
test -f .env && echo "OK" || echo "MISSING"
```

**If MISSING:** Stop and run `/vibes:connect` first.

### 4.2 Update App for Tenant Context

The user's app needs to use `useTenant()` for database scoping. Check if their app has a hardcoded database name:

```jsx
// BEFORE: Hardcoded name
const { useLiveQuery } = useFireproofClerk("my-app");

// AFTER: Tenant-aware
const { dbName } = useTenant();
const { useLiveQuery } = useFireproofClerk(dbName);
```

If the app uses a hardcoded name, update it:
1. Find the `useFireproofClerk("...")` call
2. Add `const { dbName } = useTenant();` before it
3. Change to `useFireproofClerk(dbName)`

The template makes `useTenant` available globally via `window.useTenant`.

### 4.3 Run Assembly Script

Run the assembly script with all collected values:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/assemble-sell.js" app.jsx index.html \
  --clerk-key "pk_test_xxx" \
  --app-name "wedding-photos" \
  --app-title "Wedding Photos" \
  --domain "myapp.exe.xyz" \
  --tagline "SHARE YOUR DAY.<br>MAKE IT SPECIAL." \
  --subtitle "The easiest way to share wedding photos with guests." \
  --billing-mode "off" \
  --features '["Photo sharing","Guest uploads","Live gallery"]' \
  --admin-ids '[]'
```

### 4.4 Validation Gate: Check for Placeholders

After assembly, verify no config placeholders remain:

```bash
grep -o '__VITE_[A-Z_]*__' index.html | sort -u || echo "NO_PLACEHOLDERS"
```

**If any placeholders found:** The .env file is missing required values. Check:
- `VITE_CLERK_PUBLISHABLE_KEY` - must be set
- `VITE_API_URL` - must be set
- `VITE_CLOUD_URL` - optional but recommended

Fix the .env file and re-run assembly.

### 4.5 Customize Landing Page Theme (Optional)

The template uses neutral colors by default. To match the user's brand:

```css
:root {
  --landing-accent: #0f172a;        /* Primary button/text color */
  --landing-accent-hover: #1e293b;  /* Hover state */
}
```

**Examples based on prompt style:**
- Wedding app → `--landing-accent: #d4a574;` (warm gold)
- Tech startup → `--landing-accent: #6366f1;` (vibrant indigo)
- Health/wellness → `--landing-accent: #10b981;` (fresh green)

---

## Step 5: Deployment

**Registry server credentials are REQUIRED for SaaS apps.**

### 5.0 Pre-Deploy Check: Verify JWKS Key File

Before deploying, verify the JWKS key file exists:

```bash
test -f clerk-jwks-key.pem && echo "✓ JWKS key file exists" || echo "✗ MISSING: clerk-jwks-key.pem"
```

**If output shows `MISSING`:**
> Return to Step 2.4 and save the JWKS key to `clerk-jwks-key.pem`

### 5.1 Deploy with ALL Required Flags

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/deploy-exe.js" \
  --name wedding-photos \
  --file index.html \
  --clerk-key "$(cat clerk-jwks-key.pem)" \
  --clerk-webhook-secret "whsec_xxx"
```

**Required Flags for SaaS:**
| Flag | Source | Purpose |
|------|--------|---------|
| `--clerk-key` | clerk-jwks-key.pem file | Registry JWT verification |
| `--clerk-webhook-secret` | Clerk webhook | Subscription sync |

**Without these flags, the registry server will NOT be deployed and subdomain claiming will NOT work.**

### 5.2 DNS Configuration (For Custom Domains)

If using a custom domain (not just yourapp.exe.xyz), configure DNS:

| Type | Name | Value |
|------|------|-------|
| ALIAS | @ | exe.xyz |
| CNAME | * | yourapp.exe.xyz |

**Example for `cosmic-garden.exe.xyz` with custom domain `cosmicgarden.app`:**

| Type | Name | Value |
|------|------|-------|
| ALIAS | @ | exe.xyz |
| CNAME | * | cosmic-garden.exe.xyz |

This routes both the apex domain and all subdomains through exe.dev's proxy, which handles SSL automatically.

**Note:** If your DNS provider doesn't support ALIAS records, use the `?subdomain=` query parameter as a fallback.

### 5.3 Optional: AI Features

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/deploy-exe.js" \
  --name wedding-photos \
  --file index.html \
  --clerk-key "$(cat clerk-jwks-key.pem)" \
  --clerk-webhook-secret "whsec_xxx" \
  --ai-key "sk-or-v1-your-provisioning-key" \
  --multi-tenant \
  --tenant-limit 5
```

### 5.4 Validation Gate: Verify Registry

After deployment, verify the registry server is running:

```bash
curl -s https://wedding-photos.exe.xyz/registry.json | head -c 100
```

**Expected output:** `{"claims":{},"quotas":{},"reserved":["admin","api","www"]...`

**If you see HTML instead of JSON:**
- The registry server isn't running
- Check deployment logs
- Verify `--clerk-key` and `--clerk-webhook-secret` were provided

---

## Step 6: Post-Deploy Verification

### 6.1 Test Landing Page

```bash
curl -s -o /dev/null -w "%{http_code}" https://wedding-photos.exe.xyz
```

**Expected:** `200`

### 6.2 Test Tenant Routing

Open in browser: `https://wedding-photos.exe.xyz?subdomain=test`

Should show the tenant app (may require sign-in).

### 6.3 Clerk Dashboard Checklist

Present this checklist to the user:

> **Clerk Dashboard Settings Checklist**
>
> Verify these settings in your Clerk Dashboard:
>
> **Domains** (Dashboard → Domains):
> - [ ] Add your deployment domain (e.g., `wedding-photos.exe.xyz`)
> - [ ] If using custom domain, add that too
>
> **Webhook** (Dashboard → Configure → Webhooks):
> - [ ] Endpoint URL matches your deployment: `https://wedding-photos.exe.xyz/webhook`
> - [ ] Events selected: `user.created`, `user.deleted`, `subscription.*`
>
> **If using billing** (Dashboard → Billing):
> - [ ] Stripe connected
> - [ ] Plans created with matching names: `pro`, `basic`, `monthly`, `yearly`, `starter`, or `free`

### 6.4 Admin Setup (After First Signup)

Guide the user through admin setup:

> **Set Up Admin Access**
>
> 1. Visit your app and sign up: `https://wedding-photos.exe.xyz`
> 2. Complete the signup flow (email → verify → passkey)
> 3. Go to Clerk Dashboard → Users → click your user → copy User ID
> 4. Re-run assembly with admin access:
>
> ```bash
> node "${CLAUDE_PLUGIN_ROOT}/scripts/assemble-sell.js" app.jsx index.html \
>   --clerk-key "pk_test_xxx" \
>   --app-name "wedding-photos" \
>   --app-title "Wedding Photos" \
>   --domain "wedding-photos.exe.xyz" \
>   --admin-ids '["user_xxx"]' \
>   [... other options ...]
> ```
>
> 5. Re-deploy:
> ```bash
> node "${CLAUDE_PLUGIN_ROOT}/scripts/deploy-exe.js" \
>   --name wedding-photos \
>   --file index.html \
>   --clerk-key "$(cat clerk-jwks-key.pem)" \
>   --clerk-webhook-secret "whsec_xxx"
> ```

---

## Key Components

### Client-Side Routing

The unified template uses `getRouteInfo()` to detect subdomain and route:

```javascript
function getRouteInfo() {
  const hostname = window.location.hostname;
  const parts = hostname.split('.');
  const params = new URLSearchParams(window.location.search);
  const testSubdomain = params.get('subdomain');

  // Handle localhost testing with ?subdomain= param
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    if (testSubdomain === 'admin') return { route: 'admin', subdomain: null };
    if (testSubdomain) return { route: 'tenant', subdomain: testSubdomain };
    return { route: 'landing', subdomain: null };
  }

  // Handle exe.xyz testing (before custom domain is set up)
  if (hostname.endsWith('.exe.xyz')) {
    if (testSubdomain === 'admin') return { route: 'admin', subdomain: null };
    if (testSubdomain) return { route: 'tenant', subdomain: testSubdomain };
    return { route: 'landing', subdomain: null };
  }

  // Production: detect subdomain from hostname
  if (parts.length <= 2 || parts[0] === 'www') {
    return { route: 'landing', subdomain: null };
  }
  if (parts[0] === 'admin') {
    return { route: 'admin', subdomain: null };
  }
  return { route: 'tenant', subdomain: parts[0] };
}
```

### TenantContext

Provides database scoping for tenant apps:

```javascript
const TenantContext = createContext(null);

function TenantProvider({ children, subdomain }) {
  const dbName = `${APP_NAME}-${subdomain}`;
  return (
    <TenantContext.Provider value={{ subdomain, dbName, appName: APP_NAME, domain: APP_DOMAIN }}>
      {children}
    </TenantContext.Provider>
  );
}
```

### SubscriptionGate with Billing Mode

The subscription gate respects the billing mode setting:

- **`off`**: Everyone gets free access after signing in
- **`required`**: Users must subscribe via Clerk Billing

Admins always bypass the subscription check.

**SECURITY WARNING**: Do NOT add fallbacks like `|| ADMIN_USER_IDS.length === 0` to admin checks. An empty admin list means NO admin access, not "everyone is admin".

---

## Testing

Test different routes by adding `?subdomain=` parameter:

**Localhost:**
```
http://localhost:5500/index.html              → Landing page
http://localhost:5500/index.html?subdomain=test → Tenant app
http://localhost:5500/index.html?subdomain=admin → Admin dashboard
```

**exe.xyz (before custom domain):**
```
https://myapp.exe.xyz              → Landing page
https://myapp.exe.xyz?subdomain=test → Tenant app
https://myapp.exe.xyz?subdomain=admin → Admin dashboard
```

---

## Import Map

The unified template uses React 19 with `@necrodome/fireproof-clerk` for Clerk integration:

```json
{
  "imports": {
    "react": "https://esm.sh/stable/react@19.2.4",
    "react/jsx-runtime": "https://esm.sh/stable/react@19.2.4/jsx-runtime",
    "react/jsx-dev-runtime": "https://esm.sh/stable/react@19.2.4/jsx-dev-runtime",
    "react-dom": "https://esm.sh/stable/react-dom@19.2.4",
    "react-dom/client": "https://esm.sh/stable/react-dom@19.2.4/client",
    "use-fireproof": "https://esm.sh/stable/@necrodome/fireproof-clerk@0.0.3?external=react,react-dom",
    "@fireproof/clerk": "https://esm.sh/stable/@necrodome/fireproof-clerk@0.0.3?external=react,react-dom"
  }
}
```

---

## Troubleshooting

### "Unexpected token '<'" in console
- JSX not being transpiled by Babel
- Check that `<script type="text/babel" data-type="module">` is present

### "Cannot read properties of null (reading 'useEffect')"
- React version mismatch between packages
- Ensure fireproof-clerk imports have `?external=react,react-dom`

### "Subscription Required" loop
- Check that admin user ID is correct and in the `ADMIN_USER_IDS` array
- Verify Clerk Billing is set up with matching plan names

### Clerk not loading
- Add your domain to Clerk's authorized domains
- Check publishable key is correct (not secret key)

### Admin shows "Access Denied"
- User ID not in --admin-ids array
- Check Clerk Dashboard → Users → click user → copy User ID
- Re-run assembly with correct --admin-ids

### Database not isolated
- Verify `useTenant()` is used in the App component
- Check `useFireproofClerk(dbName)` uses the tenant database name

### Passkey creation fails
- Ensure HTTPS is configured (passkeys require secure context)
- For production: use `pk_live_*` key and add domain to allowed origins

### "Verification incomplete (missing_requirements)" error
1. Go to Clerk Dashboard → User & Authentication → Email
2. Set "Require email address" to **OFF** (critical fix!)
3. Ensure "Sign-up with email" is ON
4. Ensure "Verify at sign-up" is ON with "Email verification code" checked

### Registry returns HTML instead of JSON
- The registry server isn't running
- Deploy was run without `--clerk-key` and `--clerk-webhook-secret`
- Re-deploy with both flags:
  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/scripts/deploy-exe.js" \
    --name myapp \
    --file index.html \
    --clerk-key "$(cat clerk-jwks-key.pem)" \
    --clerk-webhook-secret "whsec_xxx"
  ```

### Assembly fails with ".env file not found"
- Fireproof Connect is not configured
- Run `/vibes:connect` first to set up your sync backend
- Then return to `/vibes:sell`

---

## What's Next?

After Step 6 verification completes, present options:

```
Question: "Your SaaS is deployed and verified! What would you like to do?"
Header: "Next"
Options:
- Label: "Set up admin access (Recommended)"
  Description: "Sign up on your app, get your user ID, and enable admin dashboard access."

- Label: "Customize landing page"
  Description: "Adjust colors, refine tagline, or update feature descriptions."

- Label: "I'm done for now"
  Description: "Your app is live at https://yourapp.exe.xyz"
```
