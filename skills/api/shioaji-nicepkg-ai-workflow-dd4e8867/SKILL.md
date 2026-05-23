---
name: shioaji
description: |
  Shioaji Taiwan financial trading API guide. Use when trading stocks/futures/options on Taiwan markets, subscribing to real-time market data, querying account info, or building automated trading systems.
  Shioaji 台灣金融交易 API 指南。適用於：股票/期貨/選擇權交易、即時行情訂閱、帳務查詢、自動交易系統開發。
---

# Shioaji Trading API

Shioaji is SinoPac's Python API for trading Taiwan financial markets (stocks, futures, options).
Shioaji 是永豐金證券提供的 Python 交易 API，支援台灣股票、期貨、選擇權市場。

**Official Docs 官方文檔**: https://sinotrade.github.io/
**LLM Reference**: https://sinotrade.github.io/llms-full.txt

---

## Navigation 功能導覽

| Topic 主題 | File 檔案 | Description 說明 |
|------------|-----------|------------------|
| Preparation 準備 | [PREPARE.md](PREPARE.md) | Account setup, API keys, testing 開戶/金鑰申請/測試 |
| Contracts 合約 | [CONTRACTS.md](CONTRACTS.md) | Stocks, Futures, Options contracts 股票/期貨/選擇權合約 |
| Orders 下單 | [ORDERS.md](ORDERS.md) | Place, modify, cancel, combo orders 下單/改單/刪單/組合單 |
| Reserve 預收 | [RESERVE.md](RESERVE.md) | Reserve orders for disposition stocks 處置股預收券款 |
| Streaming 行情 | [STREAMING.md](STREAMING.md) | Real-time tick & bidask data 即時 Tick/BidAsk 資料 |
| Market Data 市場資料 | [MARKET_DATA.md](MARKET_DATA.md) | Historical, snapshot, credit, scanners 歷史資料/快照/資券/掃描器 |
| Accounting 帳務 | [ACCOUNTING.md](ACCOUNTING.md) | Balance, margin, P&L, trading limits 餘額/保證金/損益/額度 |
| Advanced 進階 | [ADVANCED.md](ADVANCED.md) | Quote binding, non-blocking, stop orders 報價綁定/非阻塞/觸價 |
| Troubleshooting 問題排解 | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues and solutions 常見問題與解決 |

---

## Quick Start 快速入門

### Installation 安裝

```bash
# pip
pip install shioaji

# uv (recommended 推薦)
uv add shioaji

# with speed optimization 速度優化版
uv add shioaji --extra speed

# Docker
docker run -it sinotrade/shioaji:latest
```

### Login & Activate CA 登入與憑證啟用

```python
import shioaji as sj

api = sj.Shioaji()

# Login with API Key 使用 API Key 登入
accounts = api.login(
    api_key="YOUR_API_KEY",
    secret_key="YOUR_SECRET_KEY"
)

# Activate CA certificate 啟用憑證 (required for placing orders 下單必須)
api.activate_ca(
    ca_path="/path/to/Sinopac.pfx",
    ca_passwd="YOUR_CA_PASSWORD",
)
```

### Simulation Mode 模擬模式

Test API without real money. 使用模擬環境測試 API。

```python
import shioaji as sj

api = sj.Shioaji(simulation=True)
api.login(api_key="YOUR_KEY", secret_key="YOUR_SECRET")
```

**Available in simulation 模擬模式可用功能:**
- Quote: subscribe, unsubscribe, ticks, kbars, snapshots
- Order: place_order, update_order, cancel_order, update_status, list_trades
- Account: list_positions, list_profit_loss
- Data: short_stock_sources, credit_enquires, scanners

### Simple Order Example 簡單下單範例

```python
# Get contract 取得合約
contract = api.Contracts.Stocks["2330"]  # TSMC 台積電

# Create order 建立訂單
order = api.Order(
    price=580,
    quantity=1,
    action=sj.constant.Action.Buy,
    price_type=sj.constant.StockPriceType.LMT,
    order_type=sj.constant.OrderType.ROD,
    account=api.stock_account,
)

# Place order 下單
trade = api.place_order(contract, order)
```

---

## Common Constants 常用常數

### Action 買賣方向
```python
sj.constant.Action.Buy   # 買進
sj.constant.Action.Sell  # 賣出
```

### Stock Price Type 股票價格類型
```python
sj.constant.StockPriceType.LMT  # Limit 限價
sj.constant.StockPriceType.MKT  # Market 市價
sj.constant.StockPriceType.MKP  # Range Market 範圍市價
```

### Futures Price Type 期貨價格類型
```python
sj.constant.FuturesPriceType.LMT  # Limit 限價
sj.constant.FuturesPriceType.MKT  # Market 市價
sj.constant.FuturesPriceType.MKP  # Range Market 範圍市價
```

### Order Type 委託條件
```python
sj.constant.OrderType.ROD  # Rest of Day 當日有效
sj.constant.OrderType.IOC  # Immediate or Cancel 立即成交否則取消
sj.constant.OrderType.FOK  # Fill or Kill 全部成交否則取消
```

### Stock Order Lot 股票交易單位
```python
sj.constant.StockOrderLot.Common      # Regular 整股 (1000 shares)
sj.constant.StockOrderLot.Odd         # After-hours odd lot 盤後零股
sj.constant.StockOrderLot.IntradayOdd # Intraday odd lot 盤中零股
sj.constant.StockOrderLot.Fixing      # Fixing 定盤
```

### Order Condition 信用交易條件
```python
sj.constant.StockOrderCond.Cash          # Cash 現股
sj.constant.StockOrderCond.MarginTrading # Margin 融資
sj.constant.StockOrderCond.ShortSelling  # Short 融券
```

### Quote Type 報價類型
```python
sj.constant.QuoteType.Tick    # Tick data 逐筆成交
sj.constant.QuoteType.BidAsk  # Bid/Ask data 五檔報價
```

---

## Account Objects 帳戶物件

```python
# Stock account 股票帳戶
api.stock_account

# Futures account 期貨帳戶
api.futopt_account

# List all accounts 列出所有帳戶
api.list_accounts()
```

---

## Rate Limits 流量限制

| Category 類別 | Limit 限制 |
|---------------|------------|
| Daily Traffic 每日流量 | 500MB - 10GB (based on trading volume 依交易量) |
| Quote Query 行情查詢 | 50 requests / 5 sec |
| Accounting Query 帳務查詢 | 25 requests / 5 sec |
| Connections 連線數 | 5 per person ID |
| Daily Logins 每日登入 | 1000 times |

---

## Common Patterns 常用模式

### Subscribe Market Data 訂閱行情

```python
# Subscribe tick data 訂閱逐筆成交
api.quote.subscribe(
    api.Contracts.Stocks["2330"],
    quote_type=sj.constant.QuoteType.Tick
)

# Subscribe bidask 訂閱五檔
api.quote.subscribe(
    api.Contracts.Stocks["2330"],
    quote_type=sj.constant.QuoteType.BidAsk
)

# Set callback 設定回調
@api.quote.on_quote
def quote_callback(topic, quote):
    print(f"Topic: {topic}, Quote: {quote}")
```

### Query Positions 查詢持倉

```python
# Stock positions 股票持倉
positions = api.list_positions(api.stock_account)

# Futures positions 期貨持倉
positions = api.list_positions(api.futopt_account)
```

### Cancel Order 刪單

```python
api.cancel_order(trade)
```

### Update Order 改單

```python
# Change price 改價
api.update_order(trade=trade, price=590)

# Reduce quantity 減量 (can only reduce 只能減少)
api.update_order(trade=trade, qty=1)
```

---

## Error Handling 錯誤處理

```python
try:
    trade = api.place_order(contract, order)
except Exception as e:
    print(f"Order failed: {e}")

# Check order status 檢查訂單狀態
api.update_status(api.stock_account)
for trade in api.list_trades():
    print(trade.status)
```

---

## Logout 登出

```python
api.logout()
```
