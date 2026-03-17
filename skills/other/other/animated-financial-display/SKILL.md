---
name: animated-financial-display
model: standard
description: Patterns for animating financial numbers with spring physics, formatting, and visual feedback. Covers animated counters, price tickers, percentage changes, and value flash effects. Use when building financial dashboards or trading UIs. Triggers on animated number, price animation, financial display, number formatting, spring animation, value ticker.
---

# Animated Financial Display

Create engaging financial number displays with smooth animations, proper formatting, and visual feedback on value changes.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install animated-financial-display
```


---

## When to Use

- Building trading dashboards with live prices
- Showing portfolio values that update in real-time
- Displaying metrics that need attention on change
- Any financial UI that benefits from motion

---

## Pattern 1: Spring-Animated Number

Using framer-motion's spring physics:

```tsx
import { useSpring, animated } from '@react-spring/web';
import { useEffect, useRef } from 'react';

interface AnimatedNumberProps {
  value: number;
  prefix?: string;
  suffix?: string;
  decimals?: number;
  duration?: number;
}

export function AnimatedNumber({
  value,
  prefix = '',
  suffix = '',
  decimals = 2,
  duration = 500,
}: AnimatedNumberProps) {
  const prevValue = useRef(value);

  const { number } = useSpring({
    from: { number: prevValue.current },
    to: { number: value },
    config: { duration },
  });

  useEffect(() => {
    prevValue.current = value;
  }, [value]);

  return (
    <animated.span className="tabular-nums">
      {number.to((n) => `${prefix}${n.toFixed(decimals)}${suffix}`)}
    </animated.span>
  );
}
```

### Usage

```tsx
<AnimatedNumber value={price} prefix="$" decimals={2} />
<AnimatedNumber value={percentage} suffix="%" decimals={1} />
```

---

## Pattern 2: Value with Flash Effect

Flash color on value change:

```tsx
import { useEffect, useState, useRef } from 'react';
import { cn } from '@/lib/utils';

interface FlashingValueProps {
  value: number;
  formatter: (value: number) => string;
}

export function FlashingValue({ value, formatter }: FlashingValueProps) {
  const [flash, setFlash] = useState<'up' | 'down' | null>(null);
  const prevValue = useRef(value);

  useEffect(() => {
    if (value !== prevValue.current) {
      setFlash(value > prevValue.current ? 'up' : 'down');
      prevValue.current = value;
      
      const timer = setTimeout(() => setFlash(null), 600);
      return () => clearTimeout(timer);
    }
  }, [value]);

  return (
    <span
      className={cn(
        'transition-colors duration-600',
        flash === 'up' && 'text-success',
        flash === 'down' && 'text-destructive'
      )}
    >
      {formatter(value)}
    </span>
  );
}
```

---

## Pattern 3: Financial Number Formatting

```typescript
// lib/formatters.ts
export function formatCurrency(
  value: number,
  options: {
    currency?: string;
    compact?: boolean;
    decimals?: number;
  } = {}
): string {
  const { currency = 'USD', compact = false, decimals = 2 } = options;

  if (compact && Math.abs(value) >= 1_000_000_000) {
    return `$${(value / 1_000_000_000).toFixed(1)}B`;
  }
  if (compact && Math.abs(value) >= 1_000_000) {
    return `$${(value / 1_000_000).toFixed(1)}M`;
  }
  if (compact && Math.abs(value) >= 1_000) {
    return `$${(value / 1_000).toFixed(1)}K`;
  }

  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
}

export function formatPercentage(
  value: number,
  options: { showSign?: boolean; decimals?: number } = {}
): string {
  const { showSign = true, decimals = 2 } = options;
  const sign = showSign && value > 0 ? '+' : '';
  return `${sign}${value.toFixed(decimals)}%`;
}

export function formatNumber(
  value: number,
  options: { compact?: boolean; decimals?: number } = {}
): string {
  const { compact = false, decimals = 0 } = options;

  if (compact) {
    return Intl.NumberFormat('en-US', {
      notation: 'compact',
      maximumFractionDigits: 1,
    }).format(value);
  }

  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
}
```

---

## Pattern 4: Price Ticker Component

```tsx
interface PriceTickerProps {
  symbol: string;
  price: number;
  change24h: number;
  changePercent24h: number;
}

export function PriceTicker({
  symbol,
  price,
  change24h,
  changePercent24h,
}: PriceTickerProps) {
  const isPositive = changePercent24h >= 0;

  return (
    <div className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
      <div className="flex items-center gap-2">
        <span className="font-display font-medium">{symbol}</span>
      </div>
      
      <div className="flex items-center gap-3">
        <AnimatedNumber value={price} prefix="$" decimals={2} />
        
        <span
          className={cn(
            'text-sm font-mono tabular-nums',
            isPositive ? 'text-success' : 'text-destructive'
          )}
        >
          {formatPercentage(changePercent24h)}
        </span>
      </div>
    </div>
  );
}
```

---

## Pattern 5: Metric Card with Animation

```tsx
interface MetricCardProps {
  label: string;
  value: number;
  previousValue?: number;
  format: 'currency' | 'percent' | 'number';
}

export function MetricCard({
  label,
  value,
  previousValue,
  format,
}: MetricCardProps) {
  const formatValue = (v: number) => {
    switch (format) {
      case 'currency': return formatCurrency(v, { compact: true });
      case 'percent': return formatPercentage(v);
      case 'number': return formatNumber(v, { compact: true });
    }
  };

  const change = previousValue ? ((value - previousValue) / previousValue) * 100 : null;

  return (
    <Surface layer="metric" className="p-4">
      <div className="text-xs uppercase tracking-wider text-muted-foreground mb-1">
        {label}
      </div>
      
      <div className="text-2xl font-bold font-mono tabular-nums">
        <FlashingValue value={value} formatter={formatValue} />
      </div>
      
      {change !== null && (
        <div className={cn(
          'text-xs font-mono mt-1',
          change >= 0 ? 'text-success' : 'text-destructive'
        )}>
          {formatPercentage(change)} from previous
        </div>
      )}
    </Surface>
  );
}
```

---

## Pattern 6: CSS Value Flash Animation

```css
@keyframes value-flash-up {
  0% { 
    color: hsl(var(--success));
    text-shadow: 0 0 8px hsl(var(--success) / 0.5);
  }
  100% { 
    color: inherit;
    text-shadow: none;
  }
}

@keyframes value-flash-down {
  0% { 
    color: hsl(var(--destructive));
    text-shadow: 0 0 8px hsl(var(--destructive) / 0.5);
  }
  100% { 
    color: inherit;
    text-shadow: none;
  }
}

.animate-flash-up {
  animation: value-flash-up 0.6s ease-out;
}

.animate-flash-down {
  animation: value-flash-down 0.6s ease-out;
}
```

---

## Related Skills

- **Meta-skill:** [ai/skills/meta/design-system-creation/](../../meta/design-system-creation/) — Complete design system workflow
- [financial-data-visualization](../financial-data-visualization/) — Chart theming and data visualization
- [realtime-react-hooks](../../realtime/realtime-react-hooks/) — Real-time data hooks for live updates

---

## NEVER Do

- **Skip tabular-nums** — Numbers will jump as they change
- **Use linear animations** — Spring/ease-out feels more natural
- **Animate decimals rapidly** — Too much motion is distracting
- **Forget compact formatting** — Large numbers need abbreviation
- **Show raw floats** — Always format with appropriate precision
- **Flash on every render** — Only flash on actual value changes

---

## Typography for Numbers

```css
.metric {
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  font-weight: 600;
  letter-spacing: -0.02em;
}

.price-large {
  font-size: 2rem;
  font-weight: 800;
}

.percentage {
  font-size: 0.875rem;
  font-weight: 500;
}
```
