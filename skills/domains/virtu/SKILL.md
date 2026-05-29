---
name: virtu-market-microstructure
description: Build trading systems in the style of Virtu Financial, the leading electronic market maker and execution services firm. Emphasizes market microstructure, optimal execution, order routing, and minimizing market impact. Use when building execution algorithms, smart order routers, or analyzing market microstructure.
---

# Virtu Financial Style Guide

## Overview

Virtu Financial is one of the world's largest electronic market makers and execution services providers. They specialize in providing liquidity across asset classes and offer execution algorithms to institutional clients. Their edge comes from deep understanding of market microstructure—how orders interact with markets.

## Core Philosophy

> "Execution is not a cost center; it's an alpha opportunity."

> "Every basis point of slippage is money left on the table."

> "The market is not a monolith; it's a network of venues with different characteristics."

Virtu believes that how you execute is as important as what you execute. Understanding market microstructure—order queues, venue characteristics, information leakage—is essential to minimizing trading costs.

## Design Principles

1. **Microstructure Matters**: Order types, queue priority, and venue selection are critical.

2. **Minimize Information Leakage**: Your trading should not signal your intentions.

3. **Venue Diversity**: Different venues have different characteristics; use them wisely.

4. **Real-Time Adaptation**: Market conditions change; algorithms must adapt.

5. **Measure Everything**: If you can't measure execution quality, you can't improve it.

## When Building Execution Systems

### Always

- Model market impact before trading
- Consider queue position and priority
- Use multiple venues intelligently
- Measure execution quality (slippage, implementation shortfall)
- Adapt to real-time market conditions
- Randomize to avoid being predictable

### Never

- Execute large orders all at once
- Ignore the information content of your orders
- Use the same strategy regardless of market conditions
- Trade through wide spreads unnecessarily
- Reveal your full size
- Ignore venue-specific rules and characteristics

### Prefer

- Passive orders over aggressive (when possible)
- Lit venues for price discovery, dark for size
- TWAP/VWAP as baselines, not goals
- Adaptive algorithms over static schedules
- Order splitting over single large orders
- Anti-gaming logic to prevent exploitation

## Code Patterns

### Market Impact Model

```python
class MarketImpactModel:
    """
    Virtu's core competency: predicting and minimizing market impact.
    Based on academic models (Almgren-Chriss, etc.) with practical extensions.
    """
    
    def __init__(self, historical_data):
        self.data = historical_data
        self.fitted_params = {}
    
    def estimate_impact(self,
                        symbol: str,
                        side: Side,
                        size: int,
                        urgency: float,  # 0 = passive, 1 = aggressive
                        duration_minutes: float) -> ImpactEstimate:
        """
        Estimate market impact for a given order.
        
        Impact = temporary_impact + permanent_impact
        
        Temporary: price displacement during execution (mean-reverts)
        Permanent: information content of trade (doesn't revert)
        """
        params = self.get_params(symbol)
        adv = self.data.get_adv(symbol)  # Average daily volume
        volatility = self.data.get_volatility(symbol)
        spread = self.data.get_spread(symbol)
        
        # Participation rate
        participation = size / (adv * duration_minutes / 390)  # 390 minutes in trading day
        
        # Almgren-Chriss temporary impact
        # I_temp = η * σ * (Q/V)^0.5 * urgency_factor
        temp_impact_bps = (
            params['eta'] * 
            volatility * 
            np.sqrt(participation) * 
            (1 + urgency * params['urgency_sensitivity'])
        )
        
        # Permanent impact (information leakage)
        # I_perm = γ * σ * (Q/V)
        perm_impact_bps = params['gamma'] * volatility * participation
        
        # Spread cost (half spread for crossing)
        spread_cost_bps = spread / 2 * urgency  # More aggressive = more spread crossing
        
        return ImpactEstimate(
            temporary_bps=temp_impact_bps,
            permanent_bps=perm_impact_bps,
            spread_bps=spread_cost_bps,
            total_bps=temp_impact_bps + perm_impact_bps + spread_cost_bps,
            confidence_interval=self.bootstrap_confidence(symbol, size)
        )
    
    def optimal_execution_schedule(self,
                                    symbol: str,
                                    size: int,
                                    duration_minutes: float,
                                    risk_aversion: float) -> List[SchedulePoint]:
        """
        Almgren-Chriss optimal execution trajectory.
        Balance urgency risk (price drift) against impact cost.
        """
        params = self.get_params(symbol)
        volatility = self.data.get_volatility(symbol)
        
        # Almgren-Chriss kappa parameter
        # Higher kappa = more front-loaded (urgent)
        kappa = np.sqrt(risk_aversion * volatility**2 / params['eta'])
        
        schedule = []
        remaining = size
        
        for t in range(int(duration_minutes)):
            # Optimal trajectory is hyperbolic
            time_remaining = duration_minutes - t
            optimal_remaining = size * np.sinh(kappa * time_remaining) / np.sinh(kappa * duration_minutes)
            
            trade_size = remaining - optimal_remaining
            schedule.append(SchedulePoint(
                minute=t,
                size=trade_size,
                cumulative_pct=(size - optimal_remaining) / size
            ))
            remaining = optimal_remaining
        
        return schedule
```

### Smart Order Router

```python
class SmartOrderRouter:
    """
    Virtu's venue selection: route orders to minimize cost and information leakage.
    """
    
    def __init__(self, venue_models: Dict[str, VenueModel]):
        self.venues = venue_models
        self.order_flow_analyzer = OrderFlowAnalyzer()
    
    def route_order(self,
                    symbol: str,
                    side: Side,
                    size: int,
                    order_type: OrderType,
                    urgency: float) -> List[VenueAllocation]:
        """
        Determine optimal venue allocation for an order.
        """
        # Get current venue states
        venue_states = {
            name: venue.get_current_state(symbol)
            for name, venue in self.venues.items()
        }
        
        # Score each venue
        venue_scores = {}
        for name, state in venue_states.items():
            venue_scores[name] = self.score_venue(
                state, symbol, side, size, order_type, urgency
            )
        
        # Allocate based on scores
        allocations = self.allocate_across_venues(
            venue_scores, size, symbol, side
        )
        
        return allocations
    
    def score_venue(self,
                    state: VenueState,
                    symbol: str,
                    side: Side,
                    size: int,
                    order_type: OrderType,
                    urgency: float) -> float:
        """
        Score a venue based on multiple factors.
        """
        score = 0.0
        
        # 1. Spread (tighter is better)
        spread_score = 1.0 / (1.0 + state.spread_bps)
        score += spread_score * 0.2
        
        # 2. Depth at touch (more is better for large orders)
        depth_score = min(1.0, state.depth_at_touch / size)
        score += depth_score * 0.2
        
        # 3. Historical fill rate
        score += state.fill_rate * 0.15
        
        # 4. Queue position advantage (for passive orders)
        if order_type == OrderType.LIMIT:
            queue_score = self.estimate_queue_advantage(state, symbol, side)
            score += queue_score * 0.15
        
        # 5. Information leakage (lower is better)
        leakage = self.estimate_information_leakage(state, symbol, size)
        score += (1.0 - leakage) * 0.2
        
        # 6. Rebate/fee structure
        net_cost = state.take_fee if urgency > 0.5 else -state.make_rebate
        cost_score = 1.0 / (1.0 + net_cost * 100)  # Convert to reasonable scale
        score += cost_score * 0.1
        
        return score
    
    def allocate_across_venues(self,
                                scores: Dict[str, float],
                                total_size: int,
                                symbol: str,
                                side: Side) -> List[VenueAllocation]:
        """
        Allocate order across venues proportional to scores.
        """
        # Normalize scores
        total_score = sum(scores.values())
        normalized = {k: v / total_score for k, v in scores.items()}
        
        # Allocate, respecting venue depth limits
        allocations = []
        remaining = total_size
        
        for venue, score in sorted(normalized.items(), key=lambda x: -x[1]):
            venue_state = self.venues[venue].get_current_state(symbol)
            
            # Don't allocate more than venue can absorb
            max_venue_size = min(
                int(total_size * score * 1.5),  # Allow some concentration
                venue_state.depth_at_touch * 3   # Don't exhaust book
            )
            
            allocation = min(remaining, max_venue_size)
            if allocation > 0:
                allocations.append(VenueAllocation(
                    venue=venue,
                    size=allocation,
                    score=scores[venue]
                ))
                remaining -= allocation
            
            if remaining <= 0:
                break
        
        return allocations
```

### Execution Algorithm (TWAP/VWAP)

```python
class ExecutionAlgorithm:
    """
    Virtu execution algorithms: adaptive, anti-gaming, measured.
    """
    
    def __init__(self, 
                 impact_model: MarketImpactModel,
                 router: SmartOrderRouter):
        self.impact = impact_model
        self.router = router
    
    def execute_vwap(self,
                     symbol: str,
                     side: Side,
                     total_size: int,
                     start_time: datetime,
                     end_time: datetime,
                     max_participation: float = 0.15) -> ExecutionResult:
        """
        Volume-Weighted Average Price algorithm.
        Execute in proportion to expected volume.
        """
        # Get historical volume profile
        volume_profile = self.get_volume_profile(symbol)
        
        duration = (end_time - start_time).total_seconds() / 60
        schedule = self.build_vwap_schedule(volume_profile, start_time, end_time, total_size)
        
        executed = []
        remaining = total_size
        
        for slice_time, target_size in schedule:
            # Adjust for actual volume (adaptive)
            actual_volume = self.get_current_volume(symbol, slice_time)
            adjusted_size = min(
                target_size * (actual_volume / volume_profile[slice_time.minute]),
                remaining,
                actual_volume * max_participation
            )
            
            # Add randomization to avoid predictability
            adjusted_size = self.randomize_size(adjusted_size)
            
            # Route and execute
            fills = self.execute_slice(symbol, side, int(adjusted_size))
            executed.extend(fills)
            remaining -= sum(f.size for f in fills)
            
            if remaining <= 0:
                break
        
        return self.calculate_execution_quality(executed, symbol, start_time)
    
    def execute_slice(self,
                      symbol: str,
                      side: Side,
                      size: int) -> List[Fill]:
        """
        Execute a single slice with smart routing.
        """
        # Determine passive vs aggressive split
        spread = self.get_current_spread(symbol)
        urgency = self.calculate_urgency(symbol, size)
        
        passive_pct = max(0.3, 1.0 - urgency)
        aggressive_pct = 1.0 - passive_pct
        
        fills = []
        
        # Passive: post at near touch
        if passive_pct > 0:
            passive_size = int(size * passive_pct)
            passive_order = self.post_passive_order(symbol, side, passive_size)
            
            # Wait for fill or timeout
            passive_fills = self.wait_for_fills(passive_order, timeout_ms=500)
            fills.extend(passive_fills)
        
        # Aggressive: sweep available liquidity
        remaining = size - sum(f.size for f in fills)
        if remaining > 0 and aggressive_pct > 0:
            allocations = self.router.route_order(
                symbol, side, remaining, OrderType.IOC, urgency
            )
            
            for alloc in allocations:
                venue_fills = self.send_ioc(alloc.venue, symbol, side, alloc.size)
                fills.extend(venue_fills)
        
        return fills
    
    def randomize_size(self, size: int, variance: float = 0.1) -> int:
        """
        Add randomization to prevent pattern detection.
        """
        noise = np.random.uniform(1 - variance, 1 + variance)
        return int(size * noise)
    
    def calculate_execution_quality(self,
                                     fills: List[Fill],
                                     symbol: str,
                                     start_time: datetime) -> ExecutionResult:
        """
        Measure execution quality vs benchmarks.
        """
        if not fills:
            return ExecutionResult(filled=0)
        
        # Volume-weighted average fill price
        total_value = sum(f.price * f.size for f in fills)
        total_size = sum(f.size for f in fills)
        vwap_fill = total_value / total_size
        
        # Benchmark VWAP
        market_vwap = self.get_market_vwap(symbol, start_time, fills[-1].timestamp)
        
        # Arrival price
        arrival_price = self.get_price_at_time(symbol, start_time)
        
        # Implementation shortfall
        if fills[0].side == Side.BUY:
            is_bps = (vwap_fill - arrival_price) / arrival_price * 10000
            vwap_diff_bps = (vwap_fill - market_vwap) / market_vwap * 10000
        else:
            is_bps = (arrival_price - vwap_fill) / arrival_price * 10000
            vwap_diff_bps = (market_vwap - vwap_fill) / market_vwap * 10000
        
        return ExecutionResult(
            filled=total_size,
            vwap_fill=vwap_fill,
            market_vwap=market_vwap,
            arrival_price=arrival_price,
            implementation_shortfall_bps=is_bps,
            vwap_slippage_bps=vwap_diff_bps,
            num_fills=len(fills),
            venues_used=len(set(f.venue for f in fills))
        )
```

### Transaction Cost Analysis (TCA)

```python
class TransactionCostAnalysis:
    """
    Virtu's TCA: measure, analyze, and improve execution quality.
    """
    
    def __init__(self, execution_db):
        self.db = execution_db
    
    def analyze_execution(self, 
                          execution_id: str) -> TCAReport:
        """
        Comprehensive post-trade analysis.
        """
        execution = self.db.get_execution(execution_id)
        fills = self.db.get_fills(execution_id)
        market_data = self.db.get_market_data(
            execution.symbol,
            execution.start_time,
            execution.end_time
        )
        
        report = TCAReport()
        
        # Cost breakdown
        report.spread_cost = self.calculate_spread_cost(fills, market_data)
        report.timing_cost = self.calculate_timing_cost(fills, market_data)
        report.impact_cost = self.calculate_impact_cost(fills, market_data)
        report.opportunity_cost = self.calculate_opportunity_cost(execution, fills)
        
        # Benchmark comparisons
        report.vs_arrival = self.compare_to_arrival(fills, execution.start_time)
        report.vs_vwap = self.compare_to_vwap(fills, market_data)
        report.vs_twap = self.compare_to_twap(fills, market_data)
        report.vs_close = self.compare_to_close(fills, market_data)
        
        # Venue analysis
        report.venue_breakdown = self.analyze_venue_performance(fills)
        
        # Recommendations
        report.recommendations = self.generate_recommendations(report)
        
        return report
    
    def calculate_impact_cost(self, 
                               fills: List[Fill],
                               market_data: MarketData) -> float:
        """
        Estimate market impact from price trajectory.
        """
        # Pre-trade price
        pre_price = market_data.get_mid_price(fills[0].timestamp - timedelta(seconds=1))
        
        # Post-trade price (after last fill + some time)
        post_price = market_data.get_mid_price(fills[-1].timestamp + timedelta(minutes=5))
        
        # Average fill price
        avg_fill = sum(f.price * f.size for f in fills) / sum(f.size for f in fills)
        
        # Impact = how much price moved against us during execution
        if fills[0].side == Side.BUY:
            impact_bps = (avg_fill - pre_price) / pre_price * 10000
        else:
            impact_bps = (pre_price - avg_fill) / pre_price * 10000
        
        # Decompose into temporary (reverted) and permanent
        reversion = (post_price - avg_fill) / avg_fill * 10000
        
        return {
            'total_impact_bps': impact_bps,
            'permanent_impact_bps': impact_bps - reversion,
            'temporary_impact_bps': reversion
        }
    
    def generate_recommendations(self, report: TCAReport) -> List[str]:
        """
        Generate actionable recommendations from TCA.
        """
        recommendations = []
        
        if report.impact_cost['total_impact_bps'] > 10:
            recommendations.append(
                "High market impact detected. Consider slower execution or "
                "smaller participation rate."
            )
        
        if report.spread_cost > 5:
            recommendations.append(
                "High spread costs. Increase passive order usage or "
                "target tighter spread conditions."
            )
        
        best_venue = max(report.venue_breakdown.items(), 
                        key=lambda x: x[1]['performance'])
        worst_venue = min(report.venue_breakdown.items(),
                         key=lambda x: x[1]['performance'])
        
        if worst_venue[1]['performance'] < best_venue[1]['performance'] - 2:
            recommendations.append(
                f"Consider reducing allocation to {worst_venue[0]} "
                f"and increasing to {best_venue[0]}."
            )
        
        return recommendations
```

## Mental Model

Virtu approaches execution by asking:

1. **What's the true cost?** Spread, impact, timing, opportunity
2. **How much information am I leaking?** Signaling intentions
3. **Which venues are best?** For this order, at this time
4. **How do I measure success?** Benchmarks and attribution
5. **How can I improve?** Continuous measurement and adaptation

## Signature Virtu Moves

- Market impact modeling
- Smart order routing
- Adaptive execution algorithms
- Venue-specific optimization
- Anti-gaming logic
- Comprehensive TCA
- Real-time market microstructure analysis
- Continuous improvement through measurement
