---
name: security-check
description: Assess token and address security via the GoPlus Security API.
metadata: { "cryptoclaw": { "emoji": "🛡️", "always": true } }
---

# GoPlus Security API

## Quick Access

The `check_address_security` tool provides instant address risk assessment. All transfers are also auto-checked before execution.

Assess token contracts, wallet addresses, and approvals for security risks using the free GoPlus API.

## Base URL

```
https://api.gopluslabs.io/api/v1
```

No API key required. Free tier is sufficient for normal usage.

## Security Checks

### 1. Token Security

```
GET /token_security/{chain_id}?contract_addresses={address}
```

Chain IDs: `1` (Ethereum), `56` (BSC), `137` (Polygon), `42161` (Arbitrum), `10` (Optimism), `8453` (Base)

Key response fields:

- `is_honeypot` — token cannot be sold (CRITICAL)
- `buy_tax` / `sell_tax` — percentage tax on trades (HIGH if > 10%)
- `is_mintable` — owner can mint unlimited tokens
- `hidden_owner` — ownership is concealed
- `can_take_back_ownership` — owner can reclaim after renouncing
- `selfdestruct` — contract can self-destruct
- `is_proxy` — upgradeable proxy contract
- `is_open_source` — source code is verified
- `holder_count` — number of holders
- `lp_holder_count` — number of LP holders
- `is_anti_whale` — anti-whale mechanism present
- `owner_percent` — percentage held by owner
- `creator_percent` — percentage held by creator

### 2. Address Security

```
GET /address_security/{address}?chain_id={chain_id}
```

Checks if an address is associated with: phishing, stealing, malicious contracts, or blacklists.

### 3. Approval Security

```
GET /approval_security/{chain_id}?contract_addresses={address}
```

Checks token approval risks: whether the approved contract is malicious or has known exploits.

### 4. NFT Security

```
GET /nft_security/{chain_id}?contract_addresses={address}
```

Checks NFT contract for: privileged operations, restricted transfer, self-destruct, and trading risks.

### 5. Phishing Site Detection

```
GET /phishing_site?url={url}
```

Checks if a URL is a known phishing site. Use this before directing users to any DeFi frontend.

## Risk Scoring Workflow

Evaluate the response fields and classify risk:

**CRITICAL** (do not proceed):

- `is_honeypot: 1`
- `selfdestruct: 1`
- `hidden_owner: 1` AND `is_mintable: 1`

**HIGH** (strong warning):

- `buy_tax > 10%` or `sell_tax > 10%`
- `can_take_back_ownership: 1`
- `is_open_source: 0` (unverified source)
- `owner_percent > 50%`

**MEDIUM** (note to user):

- `is_proxy: 1` (upgradeable)
- `is_mintable: 1` (alone)
- `holder_count < 100`

**LOW** (informational):

- `is_anti_whale: 1`
- Minor tax (< 5%)

## Risk Report Template

```
🛡️ Security Report: {token_name} ({symbol})
Chain: {chain_name} | Contract: {address}

Risk Level: {CRITICAL|HIGH|MEDIUM|LOW}

✅ Passed:
- Open source: Yes
- Not a honeypot
- No self-destruct

⚠️ Warnings:
- Sell tax: 5%
- Mintable: Yes
- Holder count: 87

❌ Critical:
- (none)

Recommendation: {proceed with caution / avoid / safe to interact}
```

## Cross-references

Other skills should invoke security checks:

- **token-swap**: Check token before executing swaps
- **nft-manager**: Check NFT contract before purchases
- **etherscan**: Complement ABI analysis with security data

## Example Interactions

User: "Is this token safe? 0x..."
→ Call `/token_security/56?contract_addresses=0x...`, generate risk report

User: "Check this address for me: 0x..."
→ Call `/address_security/0x...?chain_id=56`, report any flags

User: "Are my token approvals safe?"
→ Call `/approval_security/56?contract_addresses=0x...` for each approved contract

User: "Is this DeFi site legit? https://..."
→ Call `/phishing_site?url=https://...`, report result
