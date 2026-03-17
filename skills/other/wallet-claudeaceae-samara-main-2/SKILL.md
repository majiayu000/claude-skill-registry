---
name: wallet
description: Check crypto wallet balances, transaction history, and addresses
user-invocable: true
---

# /wallet

Check your crypto wallet status across Solana, Ethereum, and Bitcoin.

## Usage

- `/wallet` or `/wallet status` — Show current balances across all chains
- `/wallet address` — Show wallet addresses for receiving funds
- `/wallet history` — Show recent transaction activity

## Implementation

### Status Check

Read the wallet state file and display current balances:

```bash
STATE_FILE="$HOME/.claude-mind/state/services/wallet-state.json"

if [ -f "$STATE_FILE" ]; then
    python3 -c "
import json
with open('$STATE_FILE') as f:
    state = json.load(f)

sol = state.get('solana', {}).get('balance', 0)
eth = state.get('ethereum', {}).get('balance', 0)
btc = state.get('bitcoin', {}).get('balance', 0)
last = state.get('last_check', 'never')

# Rough USD estimates
sol_usd = sol * 150
eth_usd = eth * 3100
btc_usd = btc * 92000
total = sol_usd + eth_usd + btc_usd

print(f'**Wallet Balances** (as of {last[:19] if last != \"never\" else \"never\"})')
print()
print(f'| Chain | Balance | ~USD |')
print(f'|-------|---------|------|')
print(f'| Solana | {sol:.4f} SOL | \${sol_usd:,.2f} |')
print(f'| Ethereum | {eth:.6f} ETH | \${eth_usd:,.2f} |')
print(f'| Bitcoin | {btc:.8f} BTC | \${btc_usd:,.2f} |')
print()
print(f'**Total estimated value: \${total:,.2f}**')
"
else
    echo "Wallet state not found. Run wallet-watcher first."
fi
```

### Address Display

Read wallet addresses from Keychain:

```bash
CREDENTIAL="$HOME/.claude-mind/system/bin/credential"
WALLET_JSON=$("$CREDENTIAL" get wallet-apis 2>/dev/null)

if [ -n "$WALLET_JSON" ]; then
    python3 -c "
import json, os
creds = json.loads(os.environ['WALLET_JSON'])

print('**Wallet Addresses**')
print()
print(f'**Solana:** \`{creds.get(\"solana\", {}).get(\"address\", \"not configured\")}\`')
print()
print(f'**Ethereum:** \`{creds.get(\"ethereum\", {}).get(\"address\", \"not configured\")}\`')
print()
print(f'**Bitcoin:** \`{creds.get(\"bitcoin\", {}).get(\"address\", \"not configured\")}\`')
"
else
    echo "Wallet credentials not found."
fi
```

### History Display

Show recent transaction signatures from state:

```bash
STATE_FILE="$HOME/.claude-mind/state/services/wallet-state.json"

python3 -c "
import json
with open('$STATE_FILE') as f:
    state = json.load(f)

print('**Recent Activity**')
print()

sol = state.get('solana', {})
if sol.get('recent_signatures'):
    print('**Solana:**')
    for sig in sol['recent_signatures'][:3]:
        print(f'  - [{sig[:16]}...](https://solscan.io/tx/{sig})')
else:
    print('Solana: No recent transactions')

print()
eth = state.get('ethereum', {})
if eth.get('last_tx_hash'):
    print(f'**Ethereum:** Last tx: [{eth[\"last_tx_hash\"][:16]}...](https://etherscan.io/tx/{eth[\"last_tx_hash\"]})')
else:
    print('Ethereum: No recent transactions')

print()
btc = state.get('bitcoin', {})
if btc.get('last_txid'):
    print(f'**Bitcoin:** Last tx: [{btc[\"last_txid\"][:16]}...](https://mempool.space/tx/{btc[\"last_txid\"]})')
else:
    print('Bitcoin: No recent transactions')
"
```

## Notes

- Balances are updated every 15 minutes by the wallet-watcher service
- USD estimates use approximate prices and may not reflect current market rates
- Transaction history is limited to recent activity tracked in state
