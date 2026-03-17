---
name: delaware-franchise-tax
description: >-
  File your Delaware annual franchise tax and annual report. Guides you through
  tax calculation (Authorized Shares and Assumed Par Value Capital methods),
  the eCorp portal filing process, and payment. For Delaware C-Corps (March 1
  deadline) and LLCs/LPs/GPs (June 1 deadline).
license: MIT
metadata:
  author: open-agreements
  version: "0.1.0"
---

# Delaware Franchise Tax

File your Delaware annual franchise tax and annual report.

> **Interactivity note**: Always ask the user for missing inputs.
> If your agent has an `AskUserQuestion` tool (Claude Code, Cursor, etc.),
> prefer it — structured questions are easier for users to answer.
> Otherwise, ask in natural language.

## Security model

- This skill **does not** download or execute any code.
- All portal interactions are performed by the user, guided step-by-step by the agent.
- If the user opts in to browser automation (Playwright via CDP), the agent may assist with portal navigation — but credit card and banking details must **always** be entered by the user directly.

## When to Use

- Annually before **March 1** (C-Corps) or **June 1** (LLCs/LPs/GPs)
- When your registered agent sends a reminder
- When you receive a notice from the Delaware Division of Corporations
- **Portal hours**: 8:00am-11:45pm ET only
- **Scam warning**: Delaware warns about deceptive solicitations. Legitimate notices come from the state or your registered agent only. Discard anything that asks you to pay through a non-official channel.

## Phase 1: Gather Information

Ask the user for the following (use `AskUserQuestion` if available):

**All entity types:**
- Entity type: **C-Corp** or **LLC/LP/GP**
- Delaware Business Entity File Number (up to 9 digits)
- Registered agent name

**For C-Corps, also ask:**
- Total authorized shares by class and par value (e.g., 10,000,000 shares of Common Stock at $0.00001 par value)
- Total issued and outstanding shares as of December 31 of the tax year
- Total gross assets as of December 31 (from Form 1120 Schedule L, Line 15 — or estimated from bank balance + investments + receivables)
- Nature of business (brief description of how the company generates revenue)

**Officers and directors (C-Corps):**
- Officers: names, titles, addresses
- Directors: names, addresses

## Phase 2: Calculate Tax

### LLCs/LPs/GPs

Flat **$300** annual tax. No calculation needed. Skip to Phase 3.

### C-Corps — Calculate Both Methods

Always calculate both methods and recommend the lower one. Show all intermediate values so the user can verify.

#### Method 1: Authorized Shares Method

```
Shares <= 5,000:        $175 (minimum)
5,001 - 10,000:         $250
Each additional 10,000: +$85
Maximum:                $200,000
```

**Example**: 10,000,000 authorized shares
- First 10,000 shares: $250
- Remaining 9,990,000 shares = 999 increments of 10,000: 999 x $85 = $84,915
- Total: $250 + $84,915 = **$85,165**

#### Method 2: Assumed Par Value Capital (APVC) Method

Almost always cheaper for startups. Requires a gross assets figure.

```
Step 1: Assumed Par = Total Gross Assets / Total Issued Shares
Step 2: For each class of shares where assumed par >= stated par:
        use assumed par x number of authorized shares in that class
Step 3: For each class of shares where assumed par < stated par:
        use stated par x number of authorized shares in that class
Step 4: Sum all classes = Assumed Par Value Capital (APVC)
Step 5: Tax = (APVC rounded up to next $1,000,000 / $1,000,000) x $400
Step 6: Minimum tax: $400
Step 7: Maximum tax: $200,000
```

**Example**: 10,000,000 authorized shares at $0.00001 par, 1,000,000 issued, $50,000 gross assets
- Step 1: Assumed Par = $50,000 / 1,000,000 = $0.05
- Step 2: $0.05 >= $0.00001, so use assumed par: $0.05 x 10,000,000 = $500,000
- Step 4: APVC = $500,000
- Step 5: Round up to $1,000,000 -> 1 x $400 = **$400**

#### Filing Fee

- **$50** for non-exempt domestic corporations
- **$25** for 501(c)(3) exempt corporations

**Total due = franchise tax + filing fee**

Present both calculations to the user:
```
Method 1 (Authorized Shares): $XX,XXX
Method 2 (Assumed Par Value):  $XXX
Recommended method:            Method 2
Filing fee:                    $50
Total due:                     $XXX + $50 = $XXX
```

## Phase 3: File via Portal

The agent can automate the portal using Playwright if Chrome is running with remote debugging enabled. Otherwise, guide the user step-by-step.

### Automation Setup (Playwright via CDP)

If the user says "use playwright", "use the browser" or requests similar automation:

1. **Launch Chrome with remote debugging** (see `reference/ecorp-portal-playwright-notes.md` for commands)
2. **Connect via Playwright** (see reference for CDP connection snippet)
3. **Portal field reference**: See `reference/ecorp-portal-playwright-notes.md` for:
   - All field selector IDs
   - Date field workaround (must use JS `el.value =` not Playwright `.fill()`)
   - State dropdown abbreviations (use `value="NY"` not `label="New York"`)
   - Director name fields (separate first/middle/last fields, NOT one name field)
   - APVC activation sequence
   - Session/eId behavior

### Filing Steps

1. **Navigate**: Open https://icis.corp.delaware.gov/ecorp/logintax.aspx
2. **Login**: Enter Business Entity File Number. Solve CAPTCHA (if the user shares a screenshot, the agent can try to read it). Click **Continue**.
3. **Entity verification**: Confirm entity name, registered agent, and registered office match your records.
4. **Fill form fields** (all on one page):
   - **Stock info**: Issued shares (per-class field, NOT the readonly total), gross assets, asset date (must == fiscal year end)
   - **Address**: Principal business address with state abbreviation
   - **Nature of business**: Select from dropdown (e.g., "Technology/Software")
   - **Officer**: First/middle/last name, title, address
   - **Directors**: Set total count, click "Enter Directors Info", fill first/middle/last name + address for each
   - **Authorization**: First/middle/last name, title, address
   - **T&C checkbox**: Must check `chkCertify` before continuing
5. **Recalculate tax**: Click "Recalculate Tax" button. Verify the displayed tax matches your calculation from Phase 2. If it still shows the Authorized Shares method amount, the asset date is probably wrong — fix it via JavaScript.
6. **Review**: Click "Continue Filing" to see the Review Copy. Verify all data.
7. **Payment**: Click "Proceed to Payment". The agent **must stop here** — credit card and banking details must be entered by the user. If tax exceeds $5,000, ACH payment is required.
8. **Confirmation**: After payment:
   - Click **"Display Confirmation Copy"** (`onclick="downloadConfirmation();return false;"`) to save receipt PDF
   - Click **"Email Confirmation Copy"** to email the filed report (opens popup at `Email.aspx`, enter email address)
   - **CRITICAL**: "Once you leave this screen, you will no longer be able to obtain a confirmation copy" — save/email before navigating away
   - Record the Service Request Number from the URL: `srNo=XXXXX`

## Phase 4: Save Receipt and Remind

### Save the confirmation PDF

The downloaded confirmation PDF **is** the filing record — no need to create a separate one.

The portal downloads the receipt as `Ecorp_Confirmation_<ServiceRequestNumber>.pdf` to the default Downloads folder. Move it to a durable location:
- `~/Documents/Tax/Delaware/<EntityName>/` on local disk
- A "Tax" or "Corporate Records" folder in cloud storage if available
- Keep the original filename — it contains the Service Request Number for future reference

```bash
# Example
mkdir -p ~/Documents/Tax/Delaware/My-Corp-Name
mv ~/Downloads/Ecorp_Confirmation_*.pdf ~/Documents/Tax/Delaware/My-Corp-Name/
```

Ask the user where they keep tax records and move the file there.

### Set a reminder

Remind the user to set an annual reminder for approximately 2 weeks before the deadline:
- **Mid-February** for corporations (March 1 deadline)
- **Mid-May** for LLCs/LPs/GPs (June 1 deadline)

**Scheduling options:**
- **Claude Cowork**: `/schedule` for recurring tasks
- **Claude Code CLI**: external scheduler (cron, LaunchAgent)
- **Any calendar app**: set a recurring annual reminder
- If `~~calendar` MCP is available, create the reminder directly

## Reference

For detailed calculation formulas and official guidance, see the `reference/` directory:
- `reference/tax-calculation.md` — full formulas for both methods with examples
- `reference/filing-instructions.md` — fees, payment methods, deadlines
- `reference/faq.md` — frequently asked questions
- `reference/ecorp-portal-playwright-notes.md` — field selectors, gotchas, and automation tips for the eCorp portal

**Official source**: https://corp.delaware.gov/paytaxes/
**Help line**: 302-739-3073, Option 3

## Notes

- This skill does not provide tax advice — consult a tax professional for your specific situation.
- The Delaware Division of Corporations portal is the only official filing method.
- Late filing incurs a **$200 penalty + 1.5% monthly interest**.
- If franchise tax exceeds **$5,000**, ACH payment is required (credit cards not accepted above this threshold).
- **Large Corporate Filers** (listed on a national stock exchange with $750M+ in revenue or assets) pay a flat **$250,000**.
