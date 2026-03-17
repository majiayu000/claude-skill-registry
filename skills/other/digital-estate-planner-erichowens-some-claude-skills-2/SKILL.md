---
name: digital-estate-planner
description: Organizing digital life for legacy, emergency access, and death preparedness. Specializes in password management, account documentation, digital asset preservation, and ensuring loved ones can access what they need.
allowed-tools: Read, Edit, Write, Bash, Glob, Grep, WebFetch, WebSearch, Task
category: Lifestyle & Personal
tags:
  - legacy
  - passwords
  - estate
  - death-preparedness
  - digital-assets
pairs-with:
  - skill: grief-companion
    reason: Support for end-of-life planning
  - skill: security-auditor
    reason: Ensure secure estate documentation
---

# Digital Estate Planner

A comprehensive guide for organizing your digital life so that in the event of death, incapacity, or emergency, your loved ones can access what they need without guessing passwords, hunting for accounts, or losing irreplaceable data.

## Core Philosophy

We plan for physical death but ignore digital death. This skill helps you:
- Document accounts and access methods systematically
- Designate what should happen to digital assets
- Preserve important data and memories
- Create clear instructions for digital executors
- Do this in a way that maintains security while enabling access

## The Digital Estate Problem

```
What happens when someone dies:

PHYSICAL WORLD:
- Safe deposit box → Bank knows location, key exists
- House → Deed on file, keys can be made
- Car → Title exists, spare key somewhere

DIGITAL WORLD:
- Email → Password unknown, 2FA on dead phone
- Photos → Which cloud? iCloud? Google? Both? Neither?
- Crypto → Private keys? Seed phrase? Hardware wallet location?
- Subscriptions → Which cards? Auto-renewing forever?
- Social media → How to memorialize? Who has access?
```

## Decision Tree

```
What is the user trying to accomplish?
├── FULL ESTATE PLANNING → Complete digital inventory + instructions
├── EMERGENCY ACCESS SETUP → Minimal viable access for trusted person
├── SPECIFIC ACCOUNT QUESTIONS → Single account legacy settings
├── CRYPTO/FINANCIAL ASSETS → High-security asset documentation
├── SOCIAL MEDIA LEGACY → Memorialization and content decisions
└── PHOTO/DATA PRESERVATION → Ensuring memories survive

Is there a trusted person designated?
├── NO → Help identify digital executor first
└── YES → Proceed with documentation

What is the security comfort level?
├── HIGH (tech-savvy) → Can use password manager inheritance, encrypted docs
├── MEDIUM → Password manager + written backup in secure location
├── LOW → Written documentation in secure physical location
```

## The Digital Inventory

### Tier 1: Critical Access (Must have for estate management)

| Account Type | Examples | Priority |
|-------------|----------|----------|
| Primary email | Gmail, Outlook, iCloud | CRITICAL |
| Phone/carrier | Verizon, AT&T, T-Mobile | CRITICAL |
| Password manager | 1Password, Bitwarden, LastPass | CRITICAL |
| Banking | Primary bank, credit cards | CRITICAL |
| Government | SSA, IRS, DMV accounts | HIGH |
| Insurance | Life, health, auto, home | HIGH |

### Tier 2: Financial Assets

| Asset Type | Documentation Needed |
|------------|---------------------|
| Bank accounts | Account numbers, online access, location of cards |
| Investment accounts | Brokerage, 401k, IRA access info |
| Cryptocurrency | Wallet addresses, seed phrases, hardware wallet location |
| PayPal/Venmo | Account access for balance recovery |
| Property deeds | Digital copies location, original locations |

### Tier 3: Digital Memories

| Type | Preservation Action |
|------|-------------------|
| Photos | Identify ALL locations (phone, cloud, social), consolidate |
| Videos | Same as photos—often more scattered |
| Documents | Identify family archives, important files |
| Social media | Download archives, decide preservation wishes |
| Creative work | Writing, art, projects—where stored? |

### Tier 4: Ongoing Services

| Service | Death Action |
|---------|--------------|
| Subscriptions | List all, note which to cancel |
| Domains | Renewal info, transfer instructions |
| Hosting | Websites, what should happen to them |
| Cloud storage | Paid plans that need canceling or transferring |

## The Digital Executor

### Who Should This Be?

**Good candidates:**
- Tech-comfortable (can navigate password managers, 2FA)
- Trustworthy (obvious, but critical)
- Likely to outlive you
- Emotionally capable of handling your digital life

**Consider:**
- Same person as physical executor? (Often yes, but not required)
- Backup digital executor?
- Specific person for specific assets? (Crypto expert for crypto)

### What They Need

Create a "Digital Executor Letter" containing:

```markdown
# Digital Executor Instructions for [Name]

## If I Die or Become Incapacitated

### Immediate Access

1. My password manager is: [1Password/Bitwarden/etc]
   - Master password location: [safe deposit box/with attorney/sealed envelope location]
   - Emergency access feature: [if applicable, how to trigger it]

2. My phone passcode: [stored with master password OR specific location]

3. My primary email: [address]
   - Access through password manager
   - This email is recovery email for most other accounts

### Critical First Steps

1. Access email and phone to receive 2FA codes
2. Notify these accounts of death: [list priority accounts]
3. Download/preserve: [list what matters]
4. Cancel: [list subscriptions to stop]

### Specific Account Instructions

[Bank Name]: Contact branch at [location], reference account #[number]
[Crypto]: Hardware wallet in [location], seed phrase in [separate location]
[Social Media]: Please memorialize / delete / [specific instructions]

### What I Want Preserved

- Photos in [Google Photos/iCloud/etc] - please download and keep
- Writing in [location] - please share with [person]
- [Specific items with specific instructions]

### What Can Be Deleted

- Browser history (please don't look, just delete)
- [Other items you don't care about preserving]
```

## Password Manager Inheritance Features

### 1Password
- **Emergency Kit**: PDF with account info, Secret Key, printed password
- **Family/Team sharing**: Add trusted person to vault
- **Tip**: Store Emergency Kit with attorney or in safe deposit box

### Bitwarden
- **Emergency Access**: Trusted contact can request access, waiting period you set
- **Organizations**: Shared vaults for family
- **Export**: Can create encrypted backup

### LastPass
- **Emergency Access**: Similar to Bitwarden—trusted contact, waiting period
- **Family plan**: Shared folders

### Apple Keychain
- **Legacy Contact**: iOS 15.2+, designate someone who can request access
- **Recovery Key**: Store securely if used

### Google
- **Inactive Account Manager**: Designate contacts, set inactivity period
- **Data download**: Contacts get access to specified data after inactivity

## Cryptocurrency Special Handling

Crypto is the highest-risk digital asset for inheritance. Private keys = ownership.

### Documentation Required

```
CRYPTO ESTATE DOCUMENTATION
───────────────────────────

Exchange Accounts: [Coinbase, Kraken, etc]
- Login credentials in password manager
- 2FA backup codes stored with master password

Hardware Wallets: [Ledger, Trezor]
- Physical location: [where]
- PIN: [stored with seed phrase OR separate location]

Seed Phrases: [CRITICAL - this is the money]
- Location: [safe deposit box, fireproof safe, split storage]
- NEVER store digitally unless encrypted
- Consider: stamped metal backup (fireproof)

Software Wallets: [MetaMask, etc]
- Seed phrase location: [same security as hardware]

Instructions:
- How to access: [step by step for non-crypto person]
- What to do: [hold, sell, transfer to specific wallet]
- Who can help: [crypto-savvy friend/advisor name and contact]
```

### Seed Phrase Security

Options for seed phrase storage:
1. **Safe deposit box** - Bank access, but bank can access too
2. **Home fireproof safe** - You control, fire risk lower
3. **Split storage** - Half with attorney, half in safe (requires both)
4. **Metal backup** - Stamped steel survives fire/flood
5. **Shamir's Secret Sharing** - Technical but very secure

## Social Media Legacy Settings

### Facebook
- **Legacy Contact**: Designate someone to manage memorialized account
- **Options**: Memorialize (frozen tribute) or Delete after death
- **Location**: Settings > Memorialization Settings

### Instagram
- **Memorialization**: Request form available, requires proof of death
- **Removal**: Can request account removal with proof

### Twitter/X
- **Deactivation**: Family can request with death certificate
- **No memorialization**: Account either stays or goes

### LinkedIn
- **Memorialization**: Family can request, becomes memorial page
- **Removal**: Also available upon request

### Google/YouTube
- **Inactive Account Manager**: Best option, proactive setup
- **Posthumous**: Family can request access/deletion with documentation

## Photo Preservation Strategy

Photos are often the most emotionally important digital assets:

### Consolidation Checklist

- [ ] iPhone photos → where backed up? (iCloud, Google, both?)
- [ ] Android photos → Google Photos? Local?
- [ ] Old phones → transferred or sitting in drawer?
- [ ] Camera SD cards → backed up?
- [ ] Facebook/Instagram → downloaded?
- [ ] Cloud services → which ones have photos?
- [ ] External drives → where located?
- [ ] Computer folders → documented?

### Preservation Actions

1. **Consolidate** to one primary location
2. **Backup** to secondary location (3-2-1 rule: 3 copies, 2 media types, 1 offsite)
3. **Document** where everything is
4. **Share access** with trusted person now
5. **Label** important folders ("Wedding 2019", "Kids Baby Photos")

## Annual Review Checklist

Digital estates change. Review annually:

- [ ] New accounts added? Document them.
- [ ] Passwords changed? Password manager updated?
- [ ] New devices? Access documented?
- [ ] Trusted contacts still appropriate?
- [ ] Cryptocurrency holdings changed?
- [ ] New subscriptions to add to cancel list?
- [ ] Digital executor still appropriate and informed?

## Anti-Patterns

❌ **Storing master password digitally unencrypted**
❌ **Telling no one about the plan**
❌ **Assuming family can "figure it out"**
❌ **Putting seed phrases in cloud storage**
❌ **Not testing the access methods**
❌ **Forgetting about old accounts**

## Integration with Other Skills

- **grief-companion**: Emotional support alongside practical planning
- **pet-memorial-creator**: Digital memorials for pets
- **career-biographer**: Preserving professional legacy
- **panic-room-finder**: Finding secure physical storage locations

## The Gift

Digital estate planning isn't morbid—it's a gift to those who love you. When they're grieving, they won't have to guess passwords, hunt for accounts, or lose precious photos. You've made the hardest time a little bit easier.

That's love in practical form.
