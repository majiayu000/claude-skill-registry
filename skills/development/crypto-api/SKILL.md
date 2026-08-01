---
name: crypto-api
description: 'Access: Access keys using .env file. Do not view the keys. They may
  be accessed for the API by accessing COINBASEAPIKEY and COINBASESECRETKEY. Do not
  modify the keys.'
---

# skills/crypto-api/coinbase-advanced-skill.md
---
name: "Coinbase Advanced Trade API"
description: "Source for granular L2 Orderbook data."
---

## Keys
* **Access**: Access keys using `.env` file. Do not view the keys. They may be accessed for the API by accessing `COINBASE_API_KEY` and `COINBASE_SECRET_KEY`. Do not modify the keys.

## Websocket Feed
* **Endpoint**: `wss://advanced-trade-ws.coinbase.com`
* **Channels**:
    * `level2`: Full orderbook updates.
    * `market_trades`: Real-time Time & Sales.

## L2 Book Construction
1.  **Snapshot**: Receive initial state.
2.  **Updates**: Apply `l2update` messages (quantity changes at specific price levels).
3.  **Pruning**: Backend should maintain the *full* book for analysis, but slice `top_20` for the Frontend to minimize bandwidth.