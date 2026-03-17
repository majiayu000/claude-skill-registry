---
name: quic-channel-grading
description: |
  QUIC channel quality grading with BBRv3 congestion control analysis.
  Classifies network paths into GF(3) tiers based on RTT, bandwidth, loss,
  and pacing efficiency. Integrates with Iroh P2P and world-letter cross-predictions.
version: 1.0.0
tags:
  - quic
  - networking
  - congestion-control
  - bbr
  - channel-grading
  - p2p
  - iroh
color: "#00CED1"
hue: 181
trit: 0
role: ERGODIC
---

# QUIC Channel Grading

**GF(3)-classified network path quality assessment with BBRv3 congestion control.**

## Overview

QUIC Channel Grading assigns quality tiers to network channels using:
- **RTT measurements** (round-trip time)
- **Bandwidth estimation** (bottleneck bandwidth)
- **Loss rate** (packet loss percentage)
- **Pacing efficiency** (burst vs smooth delivery)
- **Jitter** (RTT variance)

## GF(3) Channel Tiers

| Tier | Trit | Quality | RTT | BW | Loss | Use Case |
|------|------|---------|-----|-----|------|----------|
| **PLUS** | +1 | Excellent | <20ms | >100Mbps | <0.1% | Real-time, video |
| **ERGODIC** | 0 | Standard | 20-100ms | 10-100Mbps | 0.1-1% | General, sync |
| **MINUS** | -1 | Degraded | >100ms | <10Mbps | >1% | Batch, async |

### Conservation Law

```
Channel assignments across triads: Σ trits ≡ 0 (mod 3)
```

When grading 3 channels simultaneously, ensure balance:
- 1 PLUS + 1 ERGODIC + 1 MINUS = 0 (balanced)
- 3 ERGODIC = 0 (all neutral)

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    QUIC CHANNEL GRADING SYSTEM                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐               │
│  │   PROBE     │   │   GRADE     │   │   ROUTE     │               │
│  │  (MINUS)    │──▶│  (ERGODIC)  │──▶│   (PLUS)    │               │
│  │  Measure    │   │  Classify   │   │  Optimize   │               │
│  └─────────────┘   └─────────────┘   └─────────────┘               │
│        │                 │                 │                        │
│        ▼                 ▼                 ▼                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    CHANNEL METRICS                          │   │
│  │  RTT: min/avg/max    BW: bottleneck    Loss: %              │   │
│  │  Jitter: σ(RTT)      Pacing: smooth?   ECN: marks           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│        │                                                            │
│        ▼                                                            │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    BBRv3 STATE MACHINE                       │   │
│  │  STARTUP → DRAIN → PROBE_BW → PROBE_RTT → (cycle)           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## BBRv3 Congestion Control

### State Machine

```
STARTUP ──────▶ DRAIN ──────▶ PROBE_BW ◀──────┐
   │              │              │             │
   │              │              ▼             │
   │              │         PROBE_RTT ─────────┘
   │              │              │
   ▼              ▼              ▼
[exponential]  [reduce]    [steady-state]
[growth]       [queue]     [oscillate]
```

### Key Improvements (v3 over v2)

| Feature | BBRv2 | BBRv3 | Impact |
|---------|-------|-------|--------|
| **Loss tolerance** | 2% | 1% | Better fairness with Cubic |
| **ECN support** | Basic | Full | Lower latency |
| **Inflight reduction** | Aggressive | Gradual | Smoother |
| **Startup exit** | Loss-based | BW plateau | Faster |

### Pacing Rate Calculation

```python
def bbr_pacing_rate(bw_estimate: float, gain: float = 1.0) -> float:
    """
    BBRv3 pacing rate = bottleneck_bandwidth * pacing_gain

    Gains by state:
    - STARTUP: 2.89 (fill pipe quickly)
    - DRAIN: 0.35 (reduce queue)
    - PROBE_BW: 1.0, 0.75, 1.25 (oscillate)
    - PROBE_RTT: 1.0 (maintain)
    """
    return bw_estimate * gain

def pacing_interval(packet_size: int, pacing_rate: float) -> float:
    """Time between packets in seconds."""
    return packet_size / pacing_rate
```

## Channel Grading Algorithm

### Metrics Collection

```python
from dataclasses import dataclass
from enum import IntEnum

class ChannelTrit(IntEnum):
    MINUS = -1   # Degraded
    ERGODIC = 0  # Standard
    PLUS = 1     # Excellent

@dataclass
class ChannelMetrics:
    rtt_min_ms: float      # Minimum RTT (base latency)
    rtt_avg_ms: float      # Average RTT
    rtt_max_ms: float      # Maximum RTT (tail latency)
    rtt_jitter_ms: float   # RTT standard deviation
    bandwidth_mbps: float  # Estimated bottleneck bandwidth
    loss_rate: float       # Packet loss rate (0.0 - 1.0)
    ecn_marks: int         # ECN congestion marks
    pacing_efficiency: float  # 0.0 (bursty) to 1.0 (smooth)

def grade_channel(m: ChannelMetrics) -> ChannelTrit:
    """Assign GF(3) trit based on channel quality."""
    score = 0

    # RTT scoring (-1 to +1)
    if m.rtt_avg_ms < 20:
        score += 1
    elif m.rtt_avg_ms > 100:
        score -= 1

    # Bandwidth scoring
    if m.bandwidth_mbps > 100:
        score += 1
    elif m.bandwidth_mbps < 10:
        score -= 1

    # Loss scoring
    if m.loss_rate < 0.001:
        score += 1
    elif m.loss_rate > 0.01:
        score -= 1

    # Jitter scoring
    if m.rtt_jitter_ms < 5:
        score += 1
    elif m.rtt_jitter_ms > 50:
        score -= 1

    # Map to GF(3)
    if score >= 2:
        return ChannelTrit.PLUS
    elif score <= -2:
        return ChannelTrit.MINUS
    else:
        return ChannelTrit.ERGODIC
```

### Hysteresis Decay

Channels exhibit **hysteresis** - quality changes lag behind metric changes:

```python
def apply_hysteresis(
    current_grade: ChannelTrit,
    new_metrics: ChannelMetrics,
    decay_rate: float = 0.1,
    threshold: float = 0.5
) -> ChannelTrit:
    """
    Prevent grade oscillation with exponential decay.

    Only change grade if confidence exceeds threshold after decay.
    """
    raw_grade = grade_channel(new_metrics)

    if raw_grade == current_grade:
        return current_grade

    # Calculate confidence with decay
    grade_diff = abs(raw_grade - current_grade)
    confidence = 1.0 - math.exp(-decay_rate * grade_diff)

    if confidence > threshold:
        return raw_grade
    else:
        return current_grade
```

## QUIC Implementation

### Quinn (Rust) Integration

```rust
use quinn::{Endpoint, Connection};
use std::time::{Duration, Instant};

#[derive(Debug, Clone, Copy)]
pub enum ChannelGrade {
    Plus,     // +1: Excellent
    Ergodic,  // 0: Standard
    Minus,    // -1: Degraded
}

pub struct ChannelGrader {
    rtt_samples: Vec<Duration>,
    bandwidth_estimate: f64,
    loss_count: u64,
    packet_count: u64,
}

impl ChannelGrader {
    pub fn record_rtt(&mut self, rtt: Duration) {
        self.rtt_samples.push(rtt);
        if self.rtt_samples.len() > 100 {
            self.rtt_samples.remove(0);
        }
    }

    pub fn grade(&self) -> ChannelGrade {
        let avg_rtt = self.avg_rtt_ms();
        let loss_rate = self.loss_rate();

        let mut score = 0i32;

        if avg_rtt < 20.0 { score += 1; }
        else if avg_rtt > 100.0 { score -= 1; }

        if self.bandwidth_estimate > 100.0 { score += 1; }
        else if self.bandwidth_estimate < 10.0 { score -= 1; }

        if loss_rate < 0.001 { score += 1; }
        else if loss_rate > 0.01 { score -= 1; }

        match score {
            s if s >= 2 => ChannelGrade::Plus,
            s if s <= -2 => ChannelGrade::Minus,
            _ => ChannelGrade::Ergodic,
        }
    }

    fn avg_rtt_ms(&self) -> f64 {
        if self.rtt_samples.is_empty() { return 50.0; }
        let sum: Duration = self.rtt_samples.iter().sum();
        sum.as_secs_f64() * 1000.0 / self.rtt_samples.len() as f64
    }

    fn loss_rate(&self) -> f64 {
        if self.packet_count == 0 { return 0.0; }
        self.loss_count as f64 / self.packet_count as f64
    }
}
```

### Iroh Integration

```rust
use iroh::net::Endpoint;

pub async fn grade_iroh_connection(
    endpoint: &Endpoint,
    peer_id: &str
) -> anyhow::Result<ChannelGrade> {
    // Probe RTT with ping
    let start = Instant::now();
    endpoint.ping(peer_id.parse()?).await?;
    let rtt = start.elapsed();

    // Get connection stats
    let stats = endpoint.connection_stats(peer_id.parse()?).await?;

    let mut grader = ChannelGrader::default();
    grader.record_rtt(rtt);
    grader.bandwidth_estimate = stats.send_rate_mbps;
    grader.loss_count = stats.lost_packets;
    grader.packet_count = stats.sent_packets;

    Ok(grader.grade())
}
```

## World-Letter Cross-Prediction Integration

### Channel Grades Across 26 Worlds

Each world-letter can predict channel quality to other worlds:

```sql
-- DuckDB schema for world-channel predictions
CREATE TABLE WorldChannelGrades (
    from_world CHAR(1),
    to_world CHAR(1),
    grade VARCHAR,  -- 'PLUS', 'ERGODIC', 'MINUS'
    trit INT,
    rtt_ms DOUBLE,
    bandwidth_mbps DOUBLE,
    loss_rate DOUBLE,
    measured_at TIMESTAMP,
    PRIMARY KEY (from_world, to_world)
);

-- Cross-prediction: what does world A predict about channel to B?
INSERT INTO WorldChannelGrades VALUES
    ('a', 'b', 'ERGODIC', 0, 45.2, 85.0, 0.002, NOW()),
    ('a', 'f', 'PLUS', 1, 12.3, 250.0, 0.0001, NOW()),
    ('a', 'z', 'MINUS', -1, 180.5, 5.2, 0.025, NOW());

-- Verify GF(3) conservation per source world
SELECT
    from_world,
    SUM(trit) as trit_sum,
    CASE WHEN SUM(trit) % 3 = 0 THEN 'BALANCED' ELSE 'UNBALANCED' END as status
FROM WorldChannelGrades
GROUP BY from_world;
```

### Bisimulation Channel Comparison

Two channels are **bisimilar** if they produce equivalent grades:

```python
def channels_bisimilar(
    ch1: ChannelMetrics,
    ch2: ChannelMetrics,
    tolerance: float = 0.1
) -> bool:
    """Check if two channels are operationally equivalent."""
    g1 = grade_channel(ch1)
    g2 = grade_channel(ch2)

    if g1 != g2:
        return False

    # Check metric similarity within tolerance
    rtt_similar = abs(ch1.rtt_avg_ms - ch2.rtt_avg_ms) / max(ch1.rtt_avg_ms, 1) < tolerance
    bw_similar = abs(ch1.bandwidth_mbps - ch2.bandwidth_mbps) / max(ch1.bandwidth_mbps, 1) < tolerance

    return rtt_similar and bw_similar
```

## Babashka Implementation

```clojure
#!/usr/bin/env bb
;; quic-channel-grade.clj - Channel grading with GF(3)

(defn grade-channel [{:keys [rtt-ms bandwidth-mbps loss-rate jitter-ms]}]
  (let [score (atom 0)]
    ;; RTT scoring
    (cond (< rtt-ms 20) (swap! score inc)
          (> rtt-ms 100) (swap! score dec))
    ;; Bandwidth scoring
    (cond (> bandwidth-mbps 100) (swap! score inc)
          (< bandwidth-mbps 10) (swap! score dec))
    ;; Loss scoring
    (cond (< loss-rate 0.001) (swap! score inc)
          (> loss-rate 0.01) (swap! score dec))
    ;; Jitter scoring
    (cond (< jitter-ms 5) (swap! score inc)
          (> jitter-ms 50) (swap! score dec))
    ;; Map to GF(3) trit
    (cond (>= @score 2) {:grade :PLUS :trit 1}
          (<= @score -2) {:grade :MINUS :trit -1}
          :else {:grade :ERGODIC :trit 0})))

(defn hysteresis-decay [current-grade new-metrics decay-rate]
  (let [raw (grade-channel new-metrics)
        diff (Math/abs (- (:trit raw) (:trit current-grade)))
        confidence (- 1.0 (Math/exp (- (* decay-rate diff))))]
    (if (> confidence 0.5) raw current-grade)))

;; Example: grade world-to-world channels
(def channels
  [{:from :a :to :b :rtt-ms 45 :bandwidth-mbps 85 :loss-rate 0.002 :jitter-ms 8}
   {:from :a :to :f :rtt-ms 12 :bandwidth-mbps 250 :loss-rate 0.0001 :jitter-ms 2}
   {:from :a :to :z :rtt-ms 180 :bandwidth-mbps 5 :loss-rate 0.025 :jitter-ms 60}])

(doseq [ch channels]
  (let [grade (grade-channel ch)]
    (println (format "%s→%s: %s (trit=%d)"
                     (name (:from ch)) (name (:to ch))
                     (name (:grade grade)) (:trit grade)))))

;; Verify GF(3) conservation
(let [trits (map #(:trit (grade-channel %)) channels)]
  (println (format "\nGF(3) sum: %d (mod 3 = %d) %s"
                   (reduce + trits)
                   (mod (reduce + trits) 3)
                   (if (zero? (mod (reduce + trits) 3)) "✓" "✗"))))
```

## Protocol ACSet Integration

```julia
# QUIC Channel as ACSet object
@present SchChannelACSet(FreeSchema) begin
    Channel::Ob
    Endpoint::Ob
    Metrics::Ob

    source::Hom(Channel, Endpoint)
    target::Hom(Channel, Endpoint)
    has_metrics::Hom(Channel, Metrics)

    # Attributes
    Grade::AttrType     # PLUS/ERGODIC/MINUS
    Trit::AttrType      # -1, 0, +1
    RTT::AttrType       # milliseconds
    Bandwidth::AttrType # Mbps
    Loss::AttrType      # percentage

    grade::Attr(Channel, Grade)
    trit::Attr(Channel, Trit)
    rtt::Attr(Metrics, RTT)
    bandwidth::Attr(Metrics, Bandwidth)
    loss::Attr(Metrics, Loss)
end

# Morphism: Channel upgrade (MINUS → ERGODIC → PLUS)
function upgrade_channel!(acset, channel_id)
    current_trit = acset[channel_id, :trit]
    if current_trit < 1
        acset[channel_id, :trit] = current_trit + 1
        acset[channel_id, :grade] = trit_to_grade(current_trit + 1)
    end
end
```

## Commands

```bash
# Grade a channel (probe and measure)
bb quic-channel-grade.clj probe <endpoint>

# Grade all world-to-world channels
bb quic-channel-grade.clj grade-worlds

# Check GF(3) conservation
bb quic-channel-grade.clj verify

# Export grades to DuckDB
bb quic-channel-grade.clj export --db channels.duckdb

# Visualize channel lattice
bb quic-channel-grade.clj visualize
```

## Kernel Configuration (BBRv3)

```bash
# Enable BBRv3 on Linux
sudo sysctl -w net.ipv4.tcp_congestion_control=bbr
sudo sysctl -w net.core.default_qdisc=fq

# Verify
sysctl net.ipv4.tcp_congestion_control
# Output: net.ipv4.tcp_congestion_control = bbr

# Check BBR version (v3 if kernel 6.x+)
cat /proc/sys/net/ipv4/tcp_available_congestion_control
```

## Visualization

```
═══════════════════════════════════════════════════════════════════
                    CHANNEL QUALITY LATTICE
═══════════════════════════════════════════════════════════════════

  PLUS (+1)     ████████████████████████████████  a→f (12ms, 250Mbps)
                ████████████████████████████      b→c (18ms, 150Mbps)

  ERGODIC (0)   ██████████████████████████        a→b (45ms, 85Mbps)
                █████████████████████████         d→e (52ms, 75Mbps)
                ████████████████████              f→g (68ms, 45Mbps)

  MINUS (-1)    ██████████████                    a→z (180ms, 5Mbps)
                ████████████                      o→p (220ms, 3Mbps)

═══════════════════════════════════════════════════════════════════
  Conservation: Σ trits = 0 (mod 3) ✓
═══════════════════════════════════════════════════════════════════
```

## Related Skills

- `iroh-p2p` - QUIC-based P2P networking with Iroh
- `protocol-acset` - Compositional protocol design
- `aptos-society` - World-letter cross-predictions
- `bisimulation-game` - Channel equivalence testing
- `localsend-analysis` - Local network discovery

## References

- [RFC 9000: QUIC Transport Protocol](https://datatracker.ietf.org/doc/html/rfc9000)
- [BBRv3 Paper: TUM Munich 2025](https://www.net.in.tum.de/fileadmin/TUM/NET/NET-2025-05-1/NET-2025-05-1_17.pdf)
- [QUIC Pacing Strategies (arXiv 2025)](https://arxiv.org/html/2505.09222v1)
- [Iroh Documentation](https://www.iroh.computer/)

## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Network Theory
- **networkx** via bicomodule for graph analysis
- **scipy** for statistical RTT analysis

### Bibliography References
- `networking`: BBR, QUIC, congestion control citations

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗ (parallel channel composition)
Kan Role: Adj (channel adaptation)
Color: #00CED1
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

Channel grades compose: `PLUS ⊗ ERGODIC ⊗ MINUS = balanced network`
