---
name: defi-trading-systems
description: Designs DeFi trading systems for perpetual futures, liquidity provision, and automated strategies with risk management and MEV protection.
license: MIT
---

# DeFi Trading Systems

This skill provides guidance for building decentralized finance trading systems, with focus on perpetual futures, automated market makers, and risk management.

## Core Competencies

- **Perpetual Futures**: Funding rates, leverage, liquidation mechanics
- **Automated Market Makers**: Liquidity provision, impermanent loss
- **Risk Management**: Position sizing, stop losses, portfolio hedging
- **MEV Protection**: Sandwich attacks, frontrunning mitigation

## DeFi Trading Fundamentals

### Perpetual Futures Mechanics

```
Traditional Futures:              Perpetual Futures:
┌─────────────────┐              ┌─────────────────┐
│   Expiry Date   │              │   No Expiry     │
│   Settlement    │              │   Funding Rate  │
│   Roll Cost     │              │   Continuous    │
└─────────────────┘              └─────────────────┘

Funding Rate = (Mark Price - Index Price) / Index Price × Interval

If funding > 0: Longs pay Shorts
If funding < 0: Shorts pay Longs
```

### Key Concepts

| Term | Definition |
|------|------------|
| Mark Price | Fair value used for liquidation |
| Index Price | Spot price from exchanges |
| Funding Rate | Periodic payment between longs/shorts |
| Maintenance Margin | Minimum equity to avoid liquidation |
| Liquidation Price | Price at which position is forcibly closed |

## Position Management

### Position Sizing

```python
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Position:
    symbol: str
    side: str  # 'long' or 'short'
    size: Decimal
    entry_price: Decimal
    leverage: int
    margin: Decimal

    @property
    def notional_value(self) -> Decimal:
        return self.size * self.entry_price

    @property
    def liquidation_price(self) -> Decimal:
        """Calculate liquidation price"""
        maintenance_margin_rate = Decimal('0.005')  # 0.5%

        if self.side == 'long':
            # Liq price = Entry × (1 - Initial Margin + Maintenance Margin)
            return self.entry_price * (
                1 - (1 / self.leverage) + maintenance_margin_rate
            )
        else:
            return self.entry_price * (
                1 + (1 / self.leverage) - maintenance_margin_rate
            )

    def unrealized_pnl(self, current_price: Decimal) -> Decimal:
        """Calculate unrealized P&L"""
        if self.side == 'long':
            return self.size * (current_price - self.entry_price)
        else:
            return self.size * (self.entry_price - current_price)

    def roi_percent(self, current_price: Decimal) -> Decimal:
        """Return on investment percentage"""
        pnl = self.unrealized_pnl(current_price)
        return (pnl / self.margin) * 100


class PositionSizer:
    """Calculate position sizes based on risk parameters"""

    def __init__(self, account_balance: Decimal):
        self.balance = account_balance
        self.max_risk_per_trade = Decimal('0.02')  # 2% of account
        self.max_leverage = 10

    def calculate_size(
        self,
        entry_price: Decimal,
        stop_loss_price: Decimal,
        leverage: int
    ) -> dict:
        """Calculate position size for given risk parameters"""
        # Limit leverage
        leverage = min(leverage, self.max_leverage)

        # Risk amount
        risk_amount = self.balance * self.max_risk_per_trade

        # Price distance to stop
        price_distance = abs(entry_price - stop_loss_price)
        price_distance_pct = price_distance / entry_price

        # Position size based on risk
        # size × price_distance = risk_amount
        size = risk_amount / price_distance

        # Check margin requirements
        required_margin = (size * entry_price) / leverage

        if required_margin > self.balance:
            # Reduce size to fit available margin
            size = (self.balance * leverage) / entry_price

        return {
            'size': size,
            'leverage': leverage,
            'margin_required': (size * entry_price) / leverage,
            'risk_amount': size * price_distance,
            'risk_percent': (size * price_distance / self.balance) * 100
        }
```

### Liquidation Prevention

```python
class LiquidationMonitor:
    """Monitor positions for liquidation risk"""

    def __init__(self, warning_threshold: float = 0.8):
        self.warning_threshold = warning_threshold
        self.positions: dict[str, Position] = {}

    def check_health(self, position: Position, current_price: Decimal) -> dict:
        """Calculate position health metrics"""
        liq_price = position.liquidation_price

        if position.side == 'long':
            distance_to_liq = (current_price - liq_price) / current_price
        else:
            distance_to_liq = (liq_price - current_price) / current_price

        # Health ratio: 1.0 = max health, 0.0 = liquidation
        health_ratio = distance_to_liq / (1 / position.leverage)

        return {
            'liquidation_price': liq_price,
            'distance_percent': float(distance_to_liq) * 100,
            'health_ratio': float(health_ratio),
            'at_risk': health_ratio < self.warning_threshold,
            'margin_ratio': self._calculate_margin_ratio(position, current_price)
        }

    def _calculate_margin_ratio(
        self,
        position: Position,
        current_price: Decimal
    ) -> float:
        """Calculate current margin ratio"""
        pnl = position.unrealized_pnl(current_price)
        equity = position.margin + pnl
        return float(equity / position.notional_value)
```

## Funding Rate Strategies

### Funding Rate Arbitrage

```python
from typing import List
import asyncio

@dataclass
class FundingRateInfo:
    exchange: str
    symbol: str
    funding_rate: Decimal
    next_funding_time: int
    mark_price: Decimal
    index_price: Decimal

class FundingArbitrage:
    """Capture funding rate differentials"""

    def __init__(self, exchanges: List[str]):
        self.exchanges = exchanges
        self.min_rate_threshold = Decimal('0.0001')  # 0.01%

    async def find_opportunities(self, symbol: str) -> List[dict]:
        """Find funding rate arbitrage opportunities"""
        rates = await self._fetch_all_rates(symbol)

        opportunities = []

        # Sort by funding rate
        rates.sort(key=lambda x: x.funding_rate)

        # Find extremes
        lowest = rates[0]
        highest = rates[-1]

        spread = highest.funding_rate - lowest.funding_rate

        if spread > self.min_rate_threshold:
            opportunities.append({
                'type': 'cross_exchange',
                'long_exchange': lowest.exchange,
                'short_exchange': highest.exchange,
                'expected_return': spread,
                'annualized_return': spread * 3 * 365  # 8-hour funding
            })

        # Spot-perp basis trade
        for rate in rates:
            if abs(rate.funding_rate) > self.min_rate_threshold:
                opportunities.append({
                    'type': 'basis_trade',
                    'exchange': rate.exchange,
                    'direction': 'short_perp_long_spot' if rate.funding_rate > 0
                                 else 'long_perp_short_spot',
                    'expected_return': abs(rate.funding_rate),
                    'mark_index_spread': rate.mark_price - rate.index_price
                })

        return opportunities

    def calculate_basis_trade_pnl(
        self,
        funding_received: Decimal,
        entry_costs: Decimal,
        price_change_pnl: Decimal
    ) -> dict:
        """Calculate P&L for basis trade"""
        gross_pnl = funding_received + price_change_pnl
        net_pnl = gross_pnl - entry_costs

        return {
            'funding_pnl': funding_received,
            'price_pnl': price_change_pnl,  # Should be ~0 if hedged
            'costs': entry_costs,
            'net_pnl': net_pnl
        }
```

## AMM and Liquidity Provision

### Impermanent Loss Calculator

```python
import math

def calculate_impermanent_loss(price_ratio: float) -> float:
    """
    Calculate impermanent loss for a constant product AMM

    price_ratio: new_price / original_price

    Returns: IL as negative percentage (e.g., -0.05 for 5% loss)
    """
    # IL = 2 * sqrt(price_ratio) / (1 + price_ratio) - 1
    return 2 * math.sqrt(price_ratio) / (1 + price_ratio) - 1


def lp_value_vs_holding(
    initial_token_a: float,
    initial_token_b: float,
    initial_price: float,
    final_price: float
) -> dict:
    """Compare LP position value vs just holding"""
    # Initial value
    initial_value = initial_token_a * initial_price + initial_token_b

    # If just held
    hold_value = initial_token_a * final_price + initial_token_b

    # LP position (constant product: x * y = k)
    k = initial_token_a * initial_token_b
    # At new price: token_a_new * price = token_b_new (equal value)
    # token_a_new * token_b_new = k
    token_a_new = math.sqrt(k / final_price)
    token_b_new = math.sqrt(k * final_price)

    lp_value = token_a_new * final_price + token_b_new

    return {
        'initial_value': initial_value,
        'hold_value': hold_value,
        'lp_value': lp_value,
        'impermanent_loss': lp_value - hold_value,
        'il_percent': (lp_value - hold_value) / hold_value * 100,
        'new_token_a': token_a_new,
        'new_token_b': token_b_new
    }
```

### Concentrated Liquidity (Uniswap V3 Style)

```python
@dataclass
class LPPosition:
    """Concentrated liquidity position"""
    lower_tick: int
    upper_tick: int
    liquidity: Decimal
    token_a_deposited: Decimal
    token_b_deposited: Decimal

    @property
    def price_range(self) -> tuple[float, float]:
        """Convert ticks to prices"""
        return (
            1.0001 ** self.lower_tick,
            1.0001 ** self.upper_tick
        )

    def in_range(self, current_price: float) -> bool:
        """Check if current price is in position range"""
        lower, upper = self.price_range
        return lower <= current_price <= upper


class ConcentratedLPCalculator:
    """Calculate metrics for concentrated liquidity positions"""

    def calculate_liquidity(
        self,
        amount_a: Decimal,
        amount_b: Decimal,
        price_lower: float,
        price_upper: float,
        current_price: float
    ) -> Decimal:
        """Calculate liquidity value for given deposit"""
        sqrt_price = math.sqrt(current_price)
        sqrt_lower = math.sqrt(price_lower)
        sqrt_upper = math.sqrt(price_upper)

        if current_price <= price_lower:
            # All in token A
            liquidity = float(amount_a) * (sqrt_lower * sqrt_upper) / (sqrt_upper - sqrt_lower)
        elif current_price >= price_upper:
            # All in token B
            liquidity = float(amount_b) / (sqrt_upper - sqrt_lower)
        else:
            # Mixed
            liquidity_a = float(amount_a) * (sqrt_price * sqrt_upper) / (sqrt_upper - sqrt_price)
            liquidity_b = float(amount_b) / (sqrt_price - sqrt_lower)
            liquidity = min(liquidity_a, liquidity_b)

        return Decimal(str(liquidity))

    def calculate_position_value(
        self,
        position: LPPosition,
        current_price: float
    ) -> dict:
        """Calculate current value of LP position"""
        sqrt_price = math.sqrt(current_price)
        lower, upper = position.price_range
        sqrt_lower = math.sqrt(lower)
        sqrt_upper = math.sqrt(upper)

        liquidity = float(position.liquidity)

        if current_price <= lower:
            amount_a = liquidity * (sqrt_upper - sqrt_lower) / (sqrt_lower * sqrt_upper)
            amount_b = 0
        elif current_price >= upper:
            amount_a = 0
            amount_b = liquidity * (sqrt_upper - sqrt_lower)
        else:
            amount_a = liquidity * (sqrt_upper - sqrt_price) / (sqrt_price * sqrt_upper)
            amount_b = liquidity * (sqrt_price - sqrt_lower)

        return {
            'token_a': Decimal(str(amount_a)),
            'token_b': Decimal(str(amount_b)),
            'total_value_in_b': Decimal(str(amount_a * current_price + amount_b)),
            'in_range': position.in_range(current_price)
        }
```

## MEV Protection

### Understanding MEV Attacks

```
Sandwich Attack:

User wants to swap:     Attacker frontruns:    User's swap:         Attacker backruns:
Token A → Token B       Buy Token B            Worse price          Sell Token B
                        (raises price)          for user            (profit)

Timeline:
─────────────────────────────────────────────────────────────────────▶
         Attacker TX 1        User TX             Attacker TX 2
         (frontrun)           (victim)            (backrun)
```

### Protection Strategies

```python
from web3 import Web3

class MEVProtection:
    """Strategies to minimize MEV exposure"""

    def __init__(self, web3: Web3):
        self.w3 = web3

    def calculate_max_slippage(
        self,
        expected_output: Decimal,
        tolerance_percent: float = 0.5
    ) -> Decimal:
        """Calculate minimum output with slippage protection"""
        return expected_output * (1 - Decimal(str(tolerance_percent / 100)))

    def should_use_private_mempool(
        self,
        trade_size_usd: float,
        gas_price_gwei: float
    ) -> bool:
        """Determine if trade warrants private mempool"""
        # Larger trades are more attractive to MEV bots
        # Higher gas prices indicate competitive MEV environment

        mev_risk_score = (trade_size_usd / 10000) * (gas_price_gwei / 50)
        return mev_risk_score > 1.0

    def chunk_large_order(
        self,
        total_size: Decimal,
        max_chunk_size: Decimal,
        min_time_between_chunks: int = 30  # seconds
    ) -> List[dict]:
        """Split large order into smaller chunks"""
        chunks = []
        remaining = total_size

        while remaining > 0:
            chunk_size = min(remaining, max_chunk_size)
            chunks.append({
                'size': chunk_size,
                'delay': len(chunks) * min_time_between_chunks
            })
            remaining -= chunk_size

        return chunks

    def calculate_twap_schedule(
        self,
        total_size: Decimal,
        duration_minutes: int,
        num_orders: int
    ) -> List[dict]:
        """Create TWAP (Time-Weighted Average Price) schedule"""
        interval = duration_minutes / num_orders
        order_size = total_size / num_orders

        return [
            {
                'size': order_size,
                'execute_at_minute': i * interval
            }
            for i in range(num_orders)
        ]
```

### Flashbots Integration

```python
from eth_account import Account
import requests

class FlashbotsSubmitter:
    """Submit transactions via Flashbots to avoid public mempool"""

    def __init__(self, flashbots_url: str, signing_key: str):
        self.url = flashbots_url
        self.signer = Account.from_key(signing_key)

    def submit_bundle(
        self,
        signed_transactions: List[str],
        target_block: int
    ) -> dict:
        """Submit transaction bundle to Flashbots"""
        bundle = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_sendBundle",
            "params": [{
                "txs": signed_transactions,
                "blockNumber": hex(target_block)
            }]
        }

        # Sign the bundle
        message = Web3.keccak(text=str(bundle))
        signature = self.signer.sign_message(message)

        headers = {
            "X-Flashbots-Signature": f"{self.signer.address}:{signature.signature.hex()}"
        }

        response = requests.post(self.url, json=bundle, headers=headers)
        return response.json()
```

## Risk Management

### Portfolio Risk Metrics

```python
import numpy as np

class RiskMetrics:
    """Calculate portfolio risk metrics"""

    def calculate_var(
        self,
        returns: List[float],
        confidence_level: float = 0.95
    ) -> float:
        """Value at Risk - maximum expected loss at confidence level"""
        return np.percentile(returns, (1 - confidence_level) * 100)

    def calculate_cvar(
        self,
        returns: List[float],
        confidence_level: float = 0.95
    ) -> float:
        """Conditional VaR - expected loss beyond VaR"""
        var = self.calculate_var(returns, confidence_level)
        return np.mean([r for r in returns if r <= var])

    def calculate_sharpe_ratio(
        self,
        returns: List[float],
        risk_free_rate: float = 0.0
    ) -> float:
        """Risk-adjusted return metric"""
        excess_returns = np.array(returns) - risk_free_rate
        return np.mean(excess_returns) / np.std(excess_returns) if np.std(excess_returns) > 0 else 0

    def calculate_max_drawdown(self, equity_curve: List[float]) -> dict:
        """Maximum peak-to-trough decline"""
        peak = equity_curve[0]
        max_dd = 0
        max_dd_start = 0
        max_dd_end = 0

        current_dd_start = 0

        for i, value in enumerate(equity_curve):
            if value > peak:
                peak = value
                current_dd_start = i

            dd = (peak - value) / peak
            if dd > max_dd:
                max_dd = dd
                max_dd_start = current_dd_start
                max_dd_end = i

        return {
            'max_drawdown': max_dd,
            'start_index': max_dd_start,
            'end_index': max_dd_end
        }


class PortfolioRiskManager:
    """Manage overall portfolio risk"""

    def __init__(self, max_portfolio_risk: float = 0.1):
        self.max_risk = max_portfolio_risk  # 10% max portfolio risk
        self.positions: List[Position] = []

    def can_add_position(
        self,
        new_position: Position,
        current_price: Decimal
    ) -> tuple[bool, str]:
        """Check if new position fits risk limits"""
        # Calculate current portfolio risk
        current_risk = self._calculate_portfolio_risk(current_price)

        # Calculate risk of new position
        new_position_risk = self._calculate_position_risk(new_position)

        # Check correlation (simplified)
        total_risk = current_risk + new_position_risk  # Assumes correlation

        if total_risk > self.max_risk:
            return False, f"Would exceed max risk: {total_risk:.2%} > {self.max_risk:.2%}"

        return True, "Position within risk limits"

    def get_risk_summary(self, current_prices: dict) -> dict:
        """Get portfolio risk summary"""
        return {
            'total_exposure': sum(p.notional_value for p in self.positions),
            'net_exposure': self._calculate_net_exposure(),
            'var_95': self._calculate_portfolio_var(0.95),
            'positions_at_risk': [
                p.symbol for p in self.positions
                if self._is_position_at_risk(p, current_prices.get(p.symbol))
            ]
        }
```

## Best Practices

### Trading System Checklist

1. **Position Management**
   - [ ] Maximum position size limits
   - [ ] Leverage limits by asset volatility
   - [ ] Automatic stop-loss orders
   - [ ] Liquidation price monitoring

2. **Risk Management**
   - [ ] Portfolio-level risk limits
   - [ ] Correlation monitoring
   - [ ] Drawdown limits with automatic deleveraging
   - [ ] Regular VaR calculations

3. **Execution**
   - [ ] MEV protection (private mempool, chunking)
   - [ ] Slippage limits on all trades
   - [ ] Gas price limits
   - [ ] Failed transaction handling

4. **Operations**
   - [ ] Hot wallet limits
   - [ ] Multi-sig for large withdrawals
   - [ ] Regular reconciliation
   - [ ] Incident response plan

## References

- `references/perpetual-mechanics.md` - Deep dive into perp math
- `references/amm-formulas.md` - AMM constant product and concentrated liquidity
- `references/mev-protection.md` - Detailed MEV mitigation strategies
