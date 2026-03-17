---
name: okx-dex
description: OKX DEX aggregator (v6). Get swap quotes, swap/approve tx data, tokens, and chains.
homepage: https://web3.okx.com/build/dev-docs/wallet-api/dex-api-reference
metadata: {"clawdbot":{"emoji":"🧭","always":true,"requires":{"bins":["curl","jq","python3"]}}}
---

# OKX DEX Aggregator 🧭

OKX Wallet DEX API provides aggregated swap quotes and transaction data across multiple chains (EVM + non‑EVM).

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OKX_API_KEY` | OKX API key | Yes |
| `OKX_SECRET_KEY` | OKX API secret | Yes |
| `OKX_PASSPHRASE` | OKX API passphrase | Yes |

## API Base URL

```
https://web3.okx.com
```

## Authentication (Required Headers)

All requests must include the following headers:

- `OK-ACCESS-KEY`
- `OK-ACCESS-TIMESTAMP` (UTC ISO time)
- `OK-ACCESS-PASSPHRASE`
- `OK-ACCESS-SIGN` (Base64(HMAC_SHA256(prehash, secret)))

Prehash string:

```
TIMESTAMP + METHOD + REQUEST_PATH_WITH_QUERY + BODY
```

- For GET requests, `BODY` is empty and `REQUEST_PATH_WITH_QUERY` must include the query string.
- For POST requests, `BODY` is the raw JSON string.

## Get Supported Chains (Aggregator)

```bash
API_KEY="${OKX_API_KEY}"
SECRET_KEY="${OKX_SECRET_KEY}"
PASSPHRASE="${OKX_PASSPHRASE}"

TIMESTAMP=$(python3 - <<'PY'
from datetime import datetime, timezone
print(datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z'))
PY
)

METHOD="GET"
REQUEST_PATH="/api/v6/dex/aggregator/supported/chain"
QUERY="chainIndex=1"
PATH_WITH_QUERY="${REQUEST_PATH}?${QUERY}"

SIGN=$(python3 - <<PY
import hmac, hashlib, base64
import os
msg = f"${TIMESTAMP}${METHOD}${PATH_WITH_QUERY}"
secret = os.environ["SECRET_KEY"].encode()
print(base64.b64encode(hmac.new(secret, msg.encode(), hashlib.sha256).digest()).decode())
PY
)

curl -s "https://web3.okx.com${PATH_WITH_QUERY}" \
  -H "OK-ACCESS-KEY: ${API_KEY}" \
  -H "OK-ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "OK-ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "OK-ACCESS-SIGN: ${SIGN}" | jq '.'
```

## Get Tokens

```bash
API_KEY="${OKX_API_KEY}"
SECRET_KEY="${OKX_SECRET_KEY}"
PASSPHRASE="${OKX_PASSPHRASE}"
CHAIN_INDEX="1"  # Ethereum

TIMESTAMP=$(python3 - <<'PY'
from datetime import datetime, timezone
print(datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z'))
PY
)

METHOD="GET"
REQUEST_PATH="/api/v6/dex/aggregator/all-tokens"
QUERY="chainIndex=${CHAIN_INDEX}"
PATH_WITH_QUERY="${REQUEST_PATH}?${QUERY}"

SIGN=$(python3 - <<PY
import hmac, hashlib, base64
import os
msg = f"${TIMESTAMP}${METHOD}${PATH_WITH_QUERY}"
secret = os.environ["SECRET_KEY"].encode()
print(base64.b64encode(hmac.new(secret, msg.encode(), hashlib.sha256).digest()).decode())
PY
)

curl -s "https://web3.okx.com${PATH_WITH_QUERY}" \
  -H "OK-ACCESS-KEY: ${API_KEY}" \
  -H "OK-ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "OK-ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "OK-ACCESS-SIGN: ${SIGN}" | jq '.data[:5]'
```

## Get Swap Quote (Quote Only)

```bash
API_KEY="${OKX_API_KEY}"
SECRET_KEY="${OKX_SECRET_KEY}"
PASSPHRASE="${OKX_PASSPHRASE}"

CHAIN_INDEX="1"  # Ethereum
FROM_TOKEN="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"  # ETH (native)
TO_TOKEN="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"    # USDC
AMOUNT="1000000000000000000"  # 1 ETH in wei

TIMESTAMP=$(python3 - <<'PY'
from datetime import datetime, timezone
print(datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z'))
PY
)

METHOD="GET"
REQUEST_PATH="/api/v6/dex/aggregator/quote"
QUERY="chainIndex=${CHAIN_INDEX}&fromTokenAddress=${FROM_TOKEN}&toTokenAddress=${TO_TOKEN}&amount=${AMOUNT}&swapMode=exactIn"
PATH_WITH_QUERY="${REQUEST_PATH}?${QUERY}"

SIGN=$(python3 - <<PY
import hmac, hashlib, base64
import os
msg = f"${TIMESTAMP}${METHOD}${PATH_WITH_QUERY}"
secret = os.environ["SECRET_KEY"].encode()
print(base64.b64encode(hmac.new(secret, msg.encode(), hashlib.sha256).digest()).decode())
PY
)

curl -s "https://web3.okx.com${PATH_WITH_QUERY}" \
  -H "OK-ACCESS-KEY: ${API_KEY}" \
  -H "OK-ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "OK-ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "OK-ACCESS-SIGN: ${SIGN}" | jq '{
    fromTokenAmount: .data[0].fromTokenAmount,
    toTokenAmount: .data[0].toTokenAmount,
    tradeFee: .data[0].tradeFee,
    router: .data[0].router
  }'
```

## Get Swap Transaction (Router Call Data)

Note: `slippagePercent` is required by the swap endpoint and is expressed as a
decimal percentage (e.g., `0.01` = 1%).

```bash
API_KEY="${OKX_API_KEY}"
SECRET_KEY="${OKX_SECRET_KEY}"
PASSPHRASE="${OKX_PASSPHRASE}"

CHAIN_INDEX="1"  # Ethereum
FROM_TOKEN="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
TO_TOKEN="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
AMOUNT="1000000000000000000"  # 1 ETH in wei
slippagePercent="0.01"  # 1%
WALLET="<YOUR_WALLET_ADDRESS>"

TIMESTAMP=$(python3 - <<'PY'
from datetime import datetime, timezone
print(datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z'))
PY
)

METHOD="GET"
REQUEST_PATH="/api/v6/dex/aggregator/swap"
QUERY="chainIndex=${CHAIN_INDEX}&fromTokenAddress=${FROM_TOKEN}&toTokenAddress=${TO_TOKEN}&amount=${AMOUNT}&swapMode=exactIn&slippagePercent=${slippagePercent}&userWalletAddress=${WALLET}"
PATH_WITH_QUERY="${REQUEST_PATH}?${QUERY}"

SIGN=$(python3 - <<PY
import hmac, hashlib, base64
import os
msg = f"${TIMESTAMP}${METHOD}${PATH_WITH_QUERY}"
secret = os.environ["SECRET_KEY"].encode()
print(base64.b64encode(hmac.new(secret, msg.encode(), hashlib.sha256).digest()).decode())
PY
)

curl -s "https://web3.okx.com${PATH_WITH_QUERY}" \
  -H "OK-ACCESS-KEY: ${API_KEY}" \
  -H "OK-ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "OK-ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "OK-ACCESS-SIGN: ${SIGN}" | jq '{
    tx: .data[0].tx,
    router: .data[0].routerResult.router,
    priceImpactPercent: .data[0].routerResult.priceImpactPercent,
    dexRouterList: (.data[0].routerResult.dexRouterList // [])
  }'
```

## Get Approval Transaction (EVM)

Note: Some responses may omit `to`/`value`. If `to` is null, use the chain's
`dexTokenApproveAddress` from the Supported Chains response as the target.

```bash
API_KEY="${OKX_API_KEY}"
SECRET_KEY="${OKX_SECRET_KEY}"
PASSPHRASE="${OKX_PASSPHRASE}"

CHAIN_INDEX="1"  # Ethereum
TOKEN_ADDRESS="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC
AMOUNT="1000000000"  # 1,000,000 USDC (6 decimals)

TIMESTAMP=$(python3 - <<'PY'
from datetime import datetime, timezone
print(datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z'))
PY
)

METHOD="GET"
REQUEST_PATH="/api/v6/dex/aggregator/approve-transaction"
QUERY="chainIndex=${CHAIN_INDEX}&tokenContractAddress=${TOKEN_ADDRESS}&approveAmount=${AMOUNT}"
PATH_WITH_QUERY="${REQUEST_PATH}?${QUERY}"

SIGN=$(python3 - <<PY
import hmac, hashlib, base64
import os
msg = f"${TIMESTAMP}${METHOD}${PATH_WITH_QUERY}"
secret = os.environ["SECRET_KEY"].encode()
print(base64.b64encode(hmac.new(secret, msg.encode(), hashlib.sha256).digest()).decode())
PY
)

curl -s "https://web3.okx.com${PATH_WITH_QUERY}" \
  -H "OK-ACCESS-KEY: ${API_KEY}" \
  -H "OK-ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "OK-ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "OK-ACCESS-SIGN: ${SIGN}" | jq '{
    data: .data[0].data,
    dexContractAddress: .data[0].dexContractAddress,
    gasLimit: .data[0].gasLimit,
    gasPrice: .data[0].gasPrice
  }'
```

## Get Approval Transaction (EVM) with `to` from Supported Chains

```bash
API_KEY="${OKX_API_KEY}"
PASSPHRASE="${OKX_PASSPHRASE}"

CHAIN_INDEX="1"  # Ethereum
TOKEN_ADDRESS="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC
AMOUNT="1000000000"  # 1,000,000 USDC (6 decimals)

TIMESTAMP=$(python3 - <<'PY'
from datetime import datetime, timezone
print(datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z'))
PY
)

METHOD="GET"
REQUEST_PATH="/api/v6/dex/aggregator/supported/chain"
QUERY="chainIndex=${CHAIN_INDEX}"
PATH_WITH_QUERY="${REQUEST_PATH}?${QUERY}"

SIGN=$(python3 - <<PY
import hmac, hashlib, base64
import os
msg = f"${TIMESTAMP}${METHOD}${PATH_WITH_QUERY}"
secret = os.environ["OKX_SECRET_KEY"].encode()
print(base64.b64encode(hmac.new(secret, msg.encode(), hashlib.sha256).digest()).decode())
PY
)

APPROVE_TO=$(curl -s "https://web3.okx.com${PATH_WITH_QUERY}" \
  -H "OK-ACCESS-KEY: ${API_KEY}" \
  -H "OK-ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "OK-ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "OK-ACCESS-SIGN: ${SIGN}" | jq -r '.data[0].dexTokenApproveAddress')

TIMESTAMP=$(python3 - <<'PY'
from datetime import datetime, timezone
print(datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z'))
PY
)

METHOD="GET"
REQUEST_PATH="/api/v6/dex/aggregator/approve-transaction"
QUERY="chainIndex=${CHAIN_INDEX}&tokenContractAddress=${TOKEN_ADDRESS}&approveAmount=${AMOUNT}"
PATH_WITH_QUERY="${REQUEST_PATH}?${QUERY}"

SIGN=$(python3 - <<PY
import hmac, hashlib, base64
import os
msg = f"${TIMESTAMP}${METHOD}${PATH_WITH_QUERY}"
secret = os.environ["OKX_SECRET_KEY"].encode()
print(base64.b64encode(hmac.new(secret, msg.encode(), hashlib.sha256).digest()).decode())
PY
)

curl -s "https://web3.okx.com${PATH_WITH_QUERY}" \
  -H "OK-ACCESS-KEY: ${API_KEY}" \
  -H "OK-ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "OK-ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "OK-ACCESS-SIGN: ${SIGN}" | jq --arg to "${APPROVE_TO}" '{
    data: .data[0].data,
    dexContractAddress: (.data[0].dexContractAddress // $to),
    gasLimit: .data[0].gasLimit,
    gasPrice: .data[0].gasPrice
  }'
```

## Safety Rules

1. ALWAYS display swap details before execution.
2. WARN if price impact is high or priceImpactProtectionPercent is exceeded.
3. CHECK token allowance (EVM) before swap execution.
4. VERIFY slippage settings (`slippagePercent`).
5. For approve responses, if `to` is null, use `dexTokenApproveAddress` for the chain.
6. NEVER execute without explicit user confirmation.

## Links

- [OKX DEX API Reference (v6)](https://web3.okx.com/build/dev-docs/wallet-api/dex-api-reference)
