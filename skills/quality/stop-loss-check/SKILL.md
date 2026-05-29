---
name: stop-loss-check
description: |
  Validate stop-loss placement to ensure it's on the correct side of entry price. 验证止损设置是否正确。

  Use this skill when:
  - Validating stop-loss configuration (验证止损配置)
  - Checking SL placement before live trading (实盘前检查止损位置)
  - Debugging stop-loss trigger issues (调试止损触发问题)
  - Verifying the stop-loss bug fix (验证止损修复)

  Keywords: stop-loss, SL, entry price, validation, trading, 止损, 入场价, 验证
disable-model-invocation: true
---

# Stop-Loss Validation

## Core Rules

| Direction | Stop-Loss Position | Validation |
|-----------|-------------------|------------|
| **LONG** | SL must be < entry price | `stop_loss_price < entry_price - PRICE_EPSILON` |
| **SHORT** | SL must be > entry price | `stop_loss_price > entry_price + PRICE_EPSILON` |

> Note: Use `PRICE_EPSILON = entry_price * 1e-8` for floating-point comparison.

## Fixed Bug

**Commit**: `7f940fb`
**Problem**: When market moves fast, support/resistance levels may be on wrong side of entry price, causing immediate SL trigger.

**Example**:
```
Entry: $91,626 (LONG)
Support: $91,808 (above entry!)
Original: SL = $91,808 × 0.999 = $91,808.10
Result: SL triggered immediately, loss -$0.18 in 820ms
```

**Fix**:
```python
# strategy/deepseek_strategy.py lines 1502-1543
PRICE_EPSILON = max(entry_price * 1e-8, 1e-8)  # Relative tolerance

if side == OrderSide.BUY:
    default_sl = entry_price * 0.98  # Default 2% SL
    if self.sl_use_support_resistance and support > 0:
        potential_sl = support * (1 - self.sl_buffer_pct)
        # Validate: SL must be below entry (with epsilon tolerance)
        if potential_sl < entry_price - PRICE_EPSILON:
            stop_loss_price = potential_sl
        else:
            stop_loss_price = default_sl  # Fallback to default 2%
            self.log.warning(f"⚠️ Support above entry, using default SL")
```

## Test Command

```bash
cd /home/linuxuser/nautilus_AItrader
source venv/bin/activate
python3 test_sl_fix.py
```

## Expected Output

```
============================================================
  Stop-Loss Fix Validation Test
============================================================
Test 1: Bug scenario: Support above entry ✅ Passed
Test 2: Normal scenario: Support below entry ✅ Passed
...
🎉 All tests passed! Stop-loss fix is correct!
```

## Key Files

| File | Purpose | Key Lines |
|------|---------|-----------|
| `strategy/deepseek_strategy.py` | Main strategy | 1502-1602 |
| `test_sl_fix.py` | Test script | - |

## Verification Steps

1. Read `strategy/deepseek_strategy.py` lines 1502-1602
2. Confirm stop-loss validation logic exists (with `PRICE_EPSILON` tolerance)
3. Run `python3 test_sl_fix.py`
4. All tests pass = fix is correct
