---
name: hunt-subdomain
description: Hunting skill for subdomain vulnerabilities. Built from 11 public bug bounty reports. Use when hunting subdomain on any target.
sources: github, hackerone_public
report_count: 11
---

## Crown Jewel Targets

Subdomain takeover is high-value because it allows an attacker to serve content from a **trusted, company-owned domain** — bypassing browser same-origin trust, phishing filters, and user skepticism simultaneously.

**Highest payout contexts:**
- Subdomains of major SaaS brands (Shopify, Snapchat, Mozilla, Yelp) where the trusted domain has user session context
- CDN-backed subdomains (Fastly, CloudFront) where CNAME points to unclaimed origins
- Third-party service integrations: UserVoice, WordPress.com, GitHub Pages, GitLab Pages, Heroku, Zendesk
- Preview/staging/dev subdomains (`new.`, `preview.`, `course.`, `delivery.`, `addons-preview.`) — abandoned after feature launches
- Subdomains used for OAuth redirect URIs or SSO endpoints — these pay highest

**Asset types that matter most:**
- CNAME records pointing to deprovisioned third-party services
- NS delegations to abandoned zones
- A records pointing to unallocated cloud IPs (less common)
- GitLab/GitHub Pages with unclaimed project namespaces

---

## Attack Surface Signals

**DNS signals:**
- `CNAME` pointing to `*.github.io`, `*.gitlab.io`, `*.fastly.net`, `*.herokudns.com`, `*.wordpress.com`, `*.uservoice.com`, `*.zendesk.com`, `*.s3.amazonaws.com`, `*.azurewebsites.net`, `*.netlify.app`
- NXDOMAIN or `SERVFAIL` on the CNAME target while the parent record still exists
- NS records delegating to registrars where the zone is no longer registered

**HTTP response signals:**
- `"There isn't a GitHub Pages site here"`
- `"NoSuchBucket"` (S3)
- `"The specified bucket does not exist"`
- `"No such app"` (Heroku)
- `"Sorry, this shop is currently unavailable"` (Shopify)
- `"This UserVoice subdomain is available"`
- `"Do you want to register"` (any domain parking page)
- HTTP 404 with provider-specific error templates
- Fastly: `"Fastly error: unknown domain"`

**Tech stack signals:**
- Response headers: `X-Served-By: cache-*` (Fastly), `X-GitHub-Request-Id`, `Server: Netlify`
- `CNAME` chain resolving to provider infrastructure but returning provider 404
- SSL cert issued to provider wildcard (`*.fastly.net`) rather than company domain

---

## Step-by-Step Hunting Methodology

1. **Enumerate all subdomains** for the target using passive + active sources:
   - `subfinder -d target.com -all`
   - `amass enum -passive -d target.com`
   - `assetfinder --subs-only target.com`
   - Certificate transparency: `crt.sh/?q=%.target.com`

2. **Resolve all subdomains** and flag those with:
   - NXDOMAIN responses
   - CNAME pointing to a third-party provider
   ```bash
   cat subdomains.txt | dnsx -a -cname -o resolved.txt
   ```

3. **Cross-reference CNAMEs** against known vulnerable provider fingerprints using `nuclei` or `subjack`:
   ```bash
   subjack -w subdomains.txt -t 100 -timeout 30 -ssl -c fingerprints.json
   nuclei -l subdomains.txt -t takeovers/
   ```

4. **Manual verification** for each flagged subdomain:
   - `dig CNAME subdomain.target.com` — confirm CNAME exists
   - `dig A <cname-target>` — confirm NXDOMAIN or no resolution
   - `curl -sk https://subdomain.target.com` — check for provider error string

5. **Confirm claimability** — attempt to register the resource:
   - GitHub Pages: check if `<username>.github.io/<repo>` or org page is unclaimed
   - GitLab Pages: check project namespace
   - S3: attempt `aws s3api create-bucket --bucket <bucketname>`
   - UserVoice/Zendesk/WordPress: visit registration URL
   - Fastly: check if origin hostname is unregistered

6. **Claim the resource** (only enough to prove control — do NOT serve malicious content):
   - Create a minimal index page with your HackerOne username and a timestamp
   - Take screenshot showing your content served on `subdomain.target.com`

7. **Document the chain**: CNAME record → provider target → unclaimed resource → your content

8. **Assess impact escalation**:
   - Does the subdomain appear in OAuth redirect allowlists?
   - Does it share cookies with parent domain (`domain=.target.com`)?
   - Is it referenced in the app's CSP?
   - Can it receive authenticated API calls?

9. **Write report** before releasing the claim (some programs want to verify first)

---

## Payload & Detection Patterns

**Bulk CNAME extraction and NXDOMAIN detection:**
```bash
# Extract CNAMEs and check if target resolves
while read sub; do
  cname=$(dig +short CNAME "$sub" | head -1)
  if [ -n "$cname" ]; then
    result=$(dig +short A "$cname")
    if [ -z "$result" ]; then
      echo "[POTENTIAL] $sub -> $cname (NXDOMAIN)"
    fi
  fi
done < subdomains.txt
```

**Nuclei takeover scan:**
```bash
nuclei -l subdomains.txt -t ~/nuclei-templates/http/takeovers/ -severity medium,high,critical
```

**subjack with SSL:**
```bash
subjack -w subdomains.txt -t 100 -timeout 30 -ssl -c $GOPATH/src/github.com/haccer/subjack/fingerprints.json -v
```

**Provider fingerprint grep patterns:**
```bash
curl -sk "https://$subdomain" | grep -iE \
  "there isn't a github pages|no such bucket|no such app|this uservoice|fastly error: unknown domain|do you want to register|sorry, this shop|project not found|404 not found|unclaimed"
```

**Check if subdomain is in scope for cookies (shared parent domain):**
```bash
curl -Isk "https://target.com" | grep -i "set-cookie" | grep "domain=.target.com"
```

**Fastly-specific detection:**
```bash
curl -sI "https://subdomain.target.com" -H "Host: subdomain.target.com" | grep -i "fastly\|x-served-by\|x-cache"
curl -sk "https://subdomain.target.com" | grep -i "fastly error"
```

**S3 unclaimed bucket check:**
```bash
aws s3api head-bucket --bucket <extracted-bucket-name> 2>&1 | grep -i "NoSuchBucket\|403\|404"
```

**GitLab Pages specific:**
```bash
dig CNAME sub.target.com
# If pointing to *.gitlab.io — visit the gitlab.io URL directly
# 404 from gitlab.io project = claimable
```

---

## Common Root Causes

1. **Service offboarding without DNS cleanup** — Developer removes a Heroku app, UserVoice account, or WordPress site but never deletes the CNAME record. DNS lives forever; service does not.

2. **Staging/preview infrastructure abandoned post-launch** — `course.`, `new.`, `preview.`, `beta.` subdomains provisioned for a product launch, pointed at a third-party, then forgotten when the campaign ends.

3. **Subdomain provisioned by a third-party team** — Marketing sets up a UserVoice or Zendesk subdomain via IT, product sunset kills it, but DNS is owned by engineering who doesn't know.

4. **CDN misconfiguration without origin validation** — Fastly and similar CDNs historically allowed any domain to "claim" a backend hostname by creating a service pointing to it. Unregistered origin hostnames become claimable.

5. **GitHub/GitLab Pages namespace not reserved** — Organization renames, user accounts deleted, or repos made private/deleted while the Pages CNAME still points to the old namespace.

6. **Wildcard DNS entries** — `*.target.com` pointing to a cloud provider means *any* unclaimed subdomain potentially resolves to claimable infrastructure.

7. **Acquired/divested company DNS not cleaned** — Post-acquisition, former brand subdomains (like `oberlo.com` under Shopify) retain CNAMEs to services that are no longer paid for.

---

## Bypass Techniques

**Defense: Manual fingerprint review before publishing**
- Bypass: Use alternative error strings — providers change their 404 pages. Maintain an up-to-date fingerprint list. Some providers show *different* errors on HTTP vs HTTPS. Test both.

**Defense: Scope restrictions (only main domain in scope)**
- Bypass: Check program's asset list carefully — `*.target.com` wildcards often include subdomains implicitly. Escalate impact to get it in scope.

**Defense: "Can't reproduce" responses due to timing**
- Bypass: Screenshot immediately after claiming. Record a video walkthrough. The window can be short for popular subdomains.

**Defense: HTTPS certificate mismatch blocking proof**
- Bypass: Some providers (GitHub Pages, Netlify) auto-provision TLS for claimed domains. Others don't — show HTTP takeover and note TLS would be resolved by provider on claim.

**Defense: Provider-side validation (Fastly verifying domain ownership)**
- Bypass: Some Fastly configurations don't validate origin hostnames. Check if the CNAME target is a generic Fastly backend hostname vs. a customer-verified one. Try claiming anyway and observe behavior.

**Defense: Rate limiting on subdomain enumeration**
- Bypass: Use passive-only sources (SecurityTrails, Shodan, crt.sh, VirusTotal) to avoid triggering WAF/IDS. DNS resolution doesn't touch the web server.

**Defense: Program claims "low severity / no impact"**
- Bypass: Demonstrate same-origin cookie theft, OAuth redirect abuse, or CSP bypass to escalate. Find if the subdomain is listed in any `postMessage` `targetOrigin` checks in JS.

---

## Gate 0 Validation

1. **What can the attacker DO right now?**
   Can you register the unclaimed resource (GitHub repo, S3 bucket, Heroku app, UserVoice account) and serve arbitrary content — including phishing pages, credential harvesters, or malicious scripts — under the target's trusted domain name?

2. **What does the victim LOSE?**
   Users lose trust and safety: they see a company-branded URL serving attacker content. The company loses brand integrity, potentially leaks session cookies if the subdomain is in `domain=.target.com` scope, and may have OAuth/SSO flows hijacked. Depending on CSP configuration, XSS against the main application may be possible.

3. **Can it be reproduced in 10 minutes from scratch?**
   - `dig CNAME subdomain.target.com` → confirms CNAME to provider
   - `curl -sk https://subdomain.target.com` → confirms provider error string
   - Visit provider registration page → confirms namespace is available
   - Screenshots of all three steps = reproducible in under 10 minutes

If you cannot show the provider resource is *currently unclaimed and claimable*, it is not a valid report.

---

## Real Impact Examples

**Scenario A — Trusted Brand Phishing via Abandoned SaaS (Snapchat/UserVoice)**
An attacker finds `feedback.snapchat.com` CNAME pointing to a UserVoice subdomain. The UserVoice account was cancelled but the DNS record remained. The attacker registers the matching UserVoice subdomain for free, gaining control of `feedback.snapchat.com`. Any user navigating to that URL — perhaps from old bookmarks or Google results — sees attacker-controlled content on a Snapchat-branded domain. Since the domain is trusted by browsers, phishing campaigns sent from this subdomain bypass email security filters that check domain reputation.

**Scenario B — CDN Origin Takeover Enabling Same-Origin Attacks (Mozilla/Fastly)**
`addons-preview-cdn.mozilla.net` had a CNAME pointing to a Fastly origin hostname that was no longer registered to Mozilla's Fastly account. An attacker could create a Fastly service claiming that origin hostname, causing all requests to `addons-preview-cdn.mozilla.net` to be routed to attacker-controlled Fastly infrastructure. Since the subdomain shares the `mozilla.net` domain, it could be leveraged to serve malicious CDN assets that appear to come from Mozilla's infrastructure, potentially bypassing CSP rules that allowlist `*.mozilla.net`.

**Scenario C — Staging Subdomain Abandoned Post-Product Migration (Rails/GitHub Pages)**
`new.rubyonrails.org` was pointed at a GitHub Pages deployment for a website redesign project. After the new site launched and the old GitHub repo was deleted or made private, the DNS CNAME remained. An attacker could fork or create a matching GitHub Pages repository and claim the namespace, serving content under `new.rubyonrails.org`. Because this is the official Ruby on Rails domain, any content served there — including fake download links or malicious gems — carries the full trust of the Rails brand.

---

## Related Skills & Chains

- **`hunt-cloud-misconfig`** — Most stale CNAMEs point at deleted cloud assets (S3, CloudFront, Heroku). Chain primitive: Cloud misconfig (S3 deleted) + `hunt-subdomain` → unclaimed CNAME points to bucket → claim bucket name → full subdomain control.
- **`hunt-oauth`** — A takeover on an OAuth `redirect_uri` host = persistent ATO across the entire SSO surface. Chain primitive: Subdomain takeover at `auth.target.com` + OAuth redirect_uri allowlist → auth code theft → ATO every user that re-authenticates.
- **`hunt-api-misconfig`** — CORS regexes routinely allowlist a takeoverable subdomain. Chain primitive: Subdomain takeover + CORS `*.target.com` with credentials → credentialed cross-origin API read → mass IDOR.
- **`hunt-xss`** — A claimed subdomain is same-origin to session-cookie-domain siblings. Chain primitive: Subdomain takeover at `feedback.target.com` + cookie scope `.target.com` → JS hosted on takeover host reads main-app cookies → session hijack.
- **`security-arsenal`** — Load the 27+ Subdomain Takeover Fingerprint Table (NoSuchBucket, "no such app", GitHub Pages 404 strings, Heroku, Shopify, Fastly) and the `subzy`/`subjack` automation patterns.
- **`triage-validation`** — Apply the Unique-Marker gate: takeover claim is informational on its own; submit only after publishing a unique HTML marker on the claimed host AND demonstrating a downstream impact (cookie read, OAuth chain, CSP bypass).