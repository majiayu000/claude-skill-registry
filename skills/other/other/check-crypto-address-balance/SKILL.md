---
name: check-crypto-address-balance
description: Check cryptocurrency wallet balances across multiple blockchains using free public APIs.
---

# Check Crypto Address Balance Skill

Query cryptocurrency address balances across multiple blockchains using free public APIs. Supports Bitcoin, Ethereum, BSC, Solana, Litecoin, and other major chains without requiring API keys for basic queries.

## Supported chains & best free APIs

| Chain | API | Base URL | Rate limit | Notes |
|-------|-----|----------|------------|-------|
| **Bitcoin (BTC)** | Blockchain.info | `https://blockchain.info` | ~1 req/10s | Most reliable, no key needed |
| **Bitcoin (BTC)** | Blockstream | `https://blockstream.info/api` | Generous | Esplora API, open-source |
| **Ethereum (ETH)** | Etherscan | `https://api.etherscan.io/api` | 5 req/sec (free) | Optional key for higher limits |
| **Ethereum (ETH)** | Blockchair | `https://api.blockchair.com` | 30 req/min | Multi-chain support |
| **BSC (BNB)** | BscScan | `https://api.bscscan.com/api` | 5 req/sec (free) | Same API as Etherscan |
| **Solana (SOL)** | Public RPC | `https://api.mainnet-beta.solana.com` | Varies by node | Free public nodes |
| **Solana (SOL)** | Solscan API | `https://public-api.solscan.io` | 10 req/sec | No key for basic queries |
| **Litecoin (LTC)** | BlockCypher | `https://api.blockcypher.com/v1/ltc/main` | 200 req/hr | Multi-chain API |
| **Litecoin (LTC)** | Chain.so | `https://chain.so/api/v2` | Generous | Simple JSON responses |
| **Multi-chain** | Blockchair | `https://api.blockchair.com` | 30 req/min | BTC, ETH, LTC, DOGE, BCH |

## Skills

### Bitcoin (BTC) balance
```bash
# Using Blockchain.info (satoshis, convert to BTC by dividing by 100000000)
curl -s "https://blockchain.info/q/addressbalance/1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"

# Using Blockstream (satoshis)
curl -s "https://blockstream.info/api/address/1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa" | jq '.chain_stats.funded_txo_sum - .chain_stats.spent_txo_sum'
```

**Node.js:**
```javascript
async function getBTCBalance(address) {
  const res = await fetch(`https://blockchain.info/q/addressbalance/${address}`);
  const satoshis = await res.text();
  return parseFloat(satoshis) / 1e8; // convert satoshis to BTC
}
```

### Ethereum (ETH) balance
```bash
# Using Etherscan (no API key required for single queries, returns wei)
curl -s "https://api.etherscan.io/api?module=account&action=balance&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&tag=latest" | jq -r '.result'

# Using Blockchair (returns balance in wei with additional metadata)
curl -s "https://api.blockchair.com/ethereum/dashboards/address/0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae" | jq '.data[].address.balance'
```

**Node.js:**
```javascript
async function getETHBalance(address) {
  const url = `https://api.etherscan.io/api?module=account&action=balance&address=${address}&tag=latest`;
  const res = await fetch(url);
  const data = await res.json();
  return parseFloat(data.result) / 1e18; // convert wei to ETH
}
```

### BSC (BNB Smart Chain) balance
```bash
# Using BscScan (same API as Etherscan)
curl -s "https://api.bscscan.com/api?module=account&action=balance&address=0x8894E0a0c962CB723c1976a4421c95949bE2D4E3&tag=latest" | jq -r '.result'
```

**Node.js:**
```javascript
async function getBSCBalance(address) {
  const url = `https://api.bscscan.com/api?module=account&action=balance&address=${address}&tag=latest`;
  const res = await fetch(url);
  const data = await res.json();
  return parseFloat(data.result) / 1e18; // convert wei to BNB
}
```

### Solana (SOL) balance
```bash
# Using public RPC (balance in lamports, 1 SOL = 1e9 lamports)
curl -s https://api.mainnet-beta.solana.com -X POST -H "Content-Type: application/json" -d '
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "getBalance",
  "params": ["vines1vzrYbzLMRdu58ou5XTby4qAqVRLmqo36NKPTg"]
}' | jq '.result.value'

# Using Solscan API (returns SOL directly)
curl -s "https://public-api.solscan.io/account/vines1vzrYbzLMRdu58ou5XTby4qAqVRLmqo36NKPTg" | jq '.lamports'
```

**Node.js:**
```javascript
async function getSOLBalance(address) {
  const res = await fetch('https://api.mainnet-beta.solana.com', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 1,
      method: 'getBalance',
      params: [address]
    })
  });
  const data = await res.json();
  return data.result.value / 1e9; // convert lamports to SOL
}
```

### Litecoin (LTC) balance
```bash
# Using Chain.so (returns LTC directly)
curl -s "https://chain.so/api/v2/get_address_balance/LTC/LTC_ADDRESS/6" | jq -r '.data.confirmed_balance'

# Using BlockCypher (returns satoshis)
curl -s "https://api.blockcypher.com/v1/ltc/main/addrs/LTC_ADDRESS/balance" | jq '.balance'
```

**Node.js:**
```javascript
async function getLTCBalance(address) {
  const res = await fetch(`https://chain.so/api/v2/get_address_balance/LTC/${address}/6`);
  const data = await res.json();
  return parseFloat(data.data.confirmed_balance);
}
```

### Multi-chain helper (Node.js)
```javascript
const APIS = {
  BTC: (addr) => `https://blockchain.info/q/addressbalance/${addr}`,
  ETH: (addr) => `https://api.etherscan.io/api?module=account&action=balance&address=${addr}&tag=latest`,
  BSC: (addr) => `https://api.bscscan.com/api?module=account&action=balance&address=${addr}&tag=latest`,
  LTC: (addr) => `https://chain.so/api/v2/get_address_balance/LTC/${addr}/6`
};

const DIVISORS = { BTC: 1e8, ETH: 1e18, BSC: 1e18, LTC: 1 };

async function getBalance(chain, address) {
  if (chain === 'SOL') {
    const res = await fetch('https://api.mainnet-beta.solana.com', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0', id: 1, method: 'getBalance', params: [address]
      })
    });
    const data = await res.json();
    return data.result.value / 1e9;
  }
  
  const url = APIS[chain](address);
  const res = await fetch(url);
  
  if (chain === 'BTC') {
    const satoshis = await res.text();
    return parseFloat(satoshis) / DIVISORS[chain];
  } else if (chain === 'LTC') {
    const data = await res.json();
    return parseFloat(data.data.confirmed_balance);
  } else {
    const data = await res.json();
    return parseFloat(data.result) / DIVISORS[chain];
  }
}

// usage: getBalance('ETH', '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae').then(console.log);
```

## Agent prompt
```text
You have a cryptocurrency balance-checking skill. When a user provides a crypto address, detect the chain (BTC/ETH/BSC/SOL/LTC) from the address format:
- BTC: starts with 1, 3, or bc1
- ETH: starts with 0x (42 chars)
- BSC: starts with 0x (42 chars, context-dependent)
- SOL: base58 string (32-44 chars, no 0x)
- LTC: starts with L or M

Use the appropriate free public API from the table above, respecting rate limits. Return the balance in the native currency (BTC, ETH, BNB, SOL, LTC) with proper decimal conversion.
```

## Rate-limiting best practices
- Implement 1-2 second delays between requests to the same API.
- Cache results for at least 30 seconds to avoid redundant queries.
- Use exponential backoff on rate-limit errors (HTTP 429).
- For production, consider getting free API keys (Etherscan, BscScan) for higher limits.

## Additional chains (via Blockchair)
Blockchair supports: BTC, ETH, LTC, DOGE, BCH, Dash, Ripple, Groestlcoin, Stellar, Monero (view-key required), Cardano, and Zcash (t-addresses).

## See also
- [get-crypto-price.md](get-crypto-price.md) — Fetching current and historical crypto prices.
