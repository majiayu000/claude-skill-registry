---
name: gettys-bufferbloat
description: Engineer low-latency networks in the style of Jim Gettys, discoverer of bufferbloat. Emphasizes understanding excessive buffering, queue management, latency under load, and the fq_codel solution. Use when diagnosing network latency issues, optimizing for real-time applications, or implementing queue management.
---

# Jim Gettys Bufferbloat Style Guide

## Overview

Jim Gettys, while working at Bell Labs and later on the One Laptop per Child project, discovered and named "bufferbloat"—the phenomenon where excessive buffering in network equipment causes massive latency spikes. Modern networks often have seconds of buffering, destroying interactive performance even when bandwidth is plentiful. Gettys' crusade to fix bufferbloat led to fq_codel and the understanding that network latency under load is the true measure of network quality.

## Core Philosophy

> "Latency is the new bandwidth. We have plenty of bandwidth; what we lack is low latency."

> "The buffer is full of lies. Every packet in that buffer is a broken promise about when it will arrive."

> "Good networks feel fast. Bufferbloated networks feel like wading through molasses."

Gettys realized that optimizing for throughput while ignoring latency creates terrible user experience. A network with 100ms idle RTT that spikes to 2000ms under load is fundamentally broken, even if it achieves high throughput. The solution is to keep queues short and managed.

## Design Principles

1. **Latency Under Load Matters**: Measure RTT while the network is busy, not idle.

2. **Buffers Lie About Bandwidth**: Large buffers mask congestion, delaying feedback.

3. **Queues Should Be Short**: Aim for milliseconds of buffering, not seconds.

4. **Flow Isolation**: One greedy flow shouldn't destroy latency for others.

5. **Active Queue Management**: Don't just drop when full—manage proactively.

## The Bufferbloat Problem

```
Without Bufferbloat (healthy network):
─────────────────────────────────────
Idle RTT:    20ms
Load RTT:    25ms  (slight increase)
Difference:   5ms  ✓ Good!

With Bufferbloat (broken network):
──────────────────────────────────
Idle RTT:    20ms
Load RTT:  2000ms  (100x increase!)
Difference: 1980ms ✗ Terrible!


Why does this happen?

┌─────────────────────────────────────────────────────────────┐
│                                                              │
│   Sender                    Router                Receiver   │
│   ──────                    ──────                ────────   │
│                                                              │
│   100 Mbps  ─────────►  ┌─────────┐  ─────────►  10 Mbps    │
│                         │ BUFFER  │                          │
│                         │█████████│ ← 2 seconds of packets! │
│                         │█████████│                          │
│                         │█████████│                          │
│                         └─────────┘                          │
│                                                              │
│   Packets queue up waiting for the slow link.               │
│   TCP doesn't know—it sees ACKs arriving (eventually).      │
│   User sees lag, even with "good bandwidth."                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## When Engineering Low-Latency Networks

### Always

- Measure latency UNDER LOAD, not just idle
- Use fq_codel or similar AQM on bottleneck queues
- Size buffers based on BDP, not maximum possible
- Test with realistic traffic patterns
- Monitor queue depth, not just throughput
- Prioritize latency for interactive traffic

### Never

- Assume more buffering is better
- Measure only idle RTT as "ping time"
- Optimize only for throughput benchmarks
- Use deep buffers "just in case"
- Ignore latency complaints with "bandwidth is fine"
- Conflate bandwidth with network quality

### Prefer

- Shallow queues over deep buffers
- Fair queuing over FIFO
- AQM over tail-drop
- Latency metrics over throughput
- Per-flow isolation
- Measuring under load

## Code Patterns

### Bufferbloat Detection

```python
class BufferbloatDetector:
    """
    Detect bufferbloat by comparing idle vs loaded RTT.
    Gettys' insight: the difference tells you everything.
    """
    
    def __init__(self, target_host: str):
        self.target = target_host
        self.idle_samples = []
        self.loaded_samples = []
    
    def measure_idle_rtt(self, samples: int = 20) -> float:
        """
        Measure RTT when network is idle.
        """
        rtts = []
        for _ in range(samples):
            rtt = self._ping(self.target)
            if rtt is not None:
                rtts.append(rtt)
            time.sleep(0.1)
        
        self.idle_samples = rtts
        return min(rtts) if rtts else None
    
    def measure_loaded_rtt(self, 
                            samples: int = 20,
                            load_generator: Callable = None) -> float:
        """
        Measure RTT while generating load.
        """
        # Start background load
        if load_generator:
            load_thread = threading.Thread(target=load_generator)
            load_thread.start()
        
        time.sleep(1)  # Let load stabilize
        
        rtts = []
        for _ in range(samples):
            rtt = self._ping(self.target)
            if rtt is not None:
                rtts.append(rtt)
            time.sleep(0.1)
        
        self.loaded_samples = rtts
        return sum(rtts) / len(rtts) if rtts else None
    
    def diagnose(self) -> BufferbloatDiagnosis:
        """
        Diagnose bufferbloat severity.
        """
        if not self.idle_samples or not self.loaded_samples:
            return BufferbloatDiagnosis(status='insufficient_data')
        
        baseline = min(self.idle_samples)
        loaded_avg = sum(self.loaded_samples) / len(self.loaded_samples)
        loaded_max = max(self.loaded_samples)
        
        bloat = loaded_avg - baseline
        bloat_ratio = loaded_avg / baseline if baseline > 0 else float('inf')
        
        # Gettys' thresholds
        if bloat < 5:
            grade = 'A'
            status = 'excellent'
            recommendation = 'Network is well-tuned'
        elif bloat < 30:
            grade = 'B'
            status = 'good'
            recommendation = 'Minor bufferbloat, acceptable for most uses'
        elif bloat < 100:
            grade = 'C'
            status = 'moderate'
            recommendation = 'Noticeable lag under load, enable fq_codel'
        elif bloat < 300:
            grade = 'D'
            status = 'poor'
            recommendation = 'Significant bufferbloat, enable AQM immediately'
        else:
            grade = 'F'
            status = 'severe'
            recommendation = 'Severe bufferbloat, network unusable for interactive use'
        
        return BufferbloatDiagnosis(
            grade=grade,
            status=status,
            baseline_rtt=baseline,
            loaded_rtt=loaded_avg,
            bloat_ms=bloat,
            bloat_ratio=bloat_ratio,
            recommendation=recommendation,
        )
    
    def _ping(self, host: str) -> Optional[float]:
        """Send ICMP ping and return RTT in ms."""
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '1', host],
                capture_output=True,
                text=True
            )
            # Parse RTT from ping output
            match = re.search(r'time=(\d+\.?\d*)', result.stdout)
            if match:
                return float(match.group(1))
        except Exception:
            pass
        return None


def run_bufferbloat_test(target: str = '8.8.8.8') -> BufferbloatDiagnosis:
    """
    Run a complete bufferbloat test.
    """
    detector = BufferbloatDetector(target)
    
    print("Measuring idle RTT...")
    detector.measure_idle_rtt()
    
    print("Measuring RTT under load...")
    
    def generate_load():
        # Download something large
        subprocess.run(
            ['curl', '-o', '/dev/null', '-s', 
             'http://speedtest.tele2.net/100MB.zip'],
            timeout=30
        )
    
    detector.measure_loaded_rtt(load_generator=generate_load)
    
    return detector.diagnose()
```

### fq_codel Implementation

```python
class FQCoDel:
    """
    Fair Queuing with Controlled Delay (fq_codel).
    The solution to bufferbloat: per-flow fair queuing + CoDel AQM.
    
    Key innovations:
    1. Flow isolation: one flow can't bloat another
    2. Per-flow AQM: CoDel applied to each flow
    3. Fair sharing: all flows get equal share of bandwidth
    """
    
    def __init__(self,
                 num_queues: int = 1024,
                 target_ms: float = 5.0,
                 interval_ms: float = 100.0,
                 quantum: int = 1514):
        self.num_queues = num_queues
        self.target = target_ms
        self.interval = interval_ms
        self.quantum = quantum  # Bytes per round
        
        self.queues = [FlowQueue(target_ms, interval_ms) 
                       for _ in range(num_queues)]
        self.active_list = []  # Flows with packets
        self.flow_states = {}  # Per-flow state
    
    def hash_flow(self, packet: Packet) -> int:
        """
        Hash packet to a queue based on flow (5-tuple).
        """
        flow_id = (
            packet.src_ip,
            packet.dst_ip,
            packet.src_port,
            packet.dst_port,
            packet.protocol
        )
        return hash(flow_id) % self.num_queues
    
    def enqueue(self, packet: Packet, now_ms: float) -> bool:
        """
        Enqueue a packet to its flow's queue.
        """
        queue_idx = self.hash_flow(packet)
        queue = self.queues[queue_idx]
        
        packet.enqueue_time = now_ms
        
        was_empty = queue.is_empty()
        success = queue.enqueue(packet)
        
        if success and was_empty:
            # Flow became active, add to round-robin
            self.active_list.append(queue_idx)
        
        return success
    
    def dequeue(self, now_ms: float) -> Optional[Packet]:
        """
        Dequeue using deficit round-robin with CoDel.
        """
        if not self.active_list:
            return None
        
        # Try each active queue in round-robin order
        for _ in range(len(self.active_list)):
            queue_idx = self.active_list[0]
            queue = self.queues[queue_idx]
            
            # Apply CoDel to this flow's queue
            packet = queue.codel_dequeue(now_ms)
            
            if packet is not None:
                # Got a packet, update deficit
                queue.deficit += self.quantum
                queue.deficit -= len(packet.data)
                
                if queue.deficit < 0:
                    # Exhausted quantum, move to back of active list
                    self.active_list.append(self.active_list.pop(0))
                    queue.deficit = 0
                
                return packet
            else:
                # Queue empty, remove from active list
                self.active_list.pop(0)
                queue.deficit = 0
        
        return None


class FlowQueue:
    """
    Per-flow queue with CoDel.
    """
    
    def __init__(self, target_ms: float, interval_ms: float, max_size: int = 10240):
        self.packets = deque()
        self.max_size = max_size
        self.deficit = 0
        
        # CoDel state
        self.target = target_ms
        self.interval = interval_ms
        self.first_above_time = None
        self.drop_next = 0
        self.count = 0
        self.dropping = False
    
    def is_empty(self) -> bool:
        return len(self.packets) == 0
    
    def enqueue(self, packet: Packet) -> bool:
        if len(self.packets) >= self.max_size:
            return False
        self.packets.append(packet)
        return True
    
    def codel_dequeue(self, now_ms: float) -> Optional[Packet]:
        """
        Dequeue with CoDel logic.
        """
        if not self.packets:
            self.dropping = False
            return None
        
        packet = self.packets[0]
        sojourn_time = now_ms - packet.enqueue_time
        
        if sojourn_time < self.target:
            # Good: below target
            self.first_above_time = None
        else:
            if self.first_above_time is None:
                self.first_above_time = now_ms + self.interval
            elif now_ms >= self.first_above_time:
                # Persistent delay: consider dropping
                pass
        
        if self.dropping:
            if sojourn_time < self.target:
                # Delay recovered, stop dropping
                self.dropping = False
            elif now_ms >= self.drop_next:
                # Time to drop
                self.packets.popleft()  # Drop
                self.count += 1
                self.drop_next = now_ms + self.interval / (self.count ** 0.5)
                return self.codel_dequeue(now_ms)  # Try next
        elif self.first_above_time and now_ms >= self.first_above_time:
            # Start dropping
            self.dropping = True
            self.count = 1
            self.drop_next = now_ms + self.interval
            self.packets.popleft()  # Drop
            return self.codel_dequeue(now_ms)  # Try next
        
        return self.packets.popleft()
```

### Network Quality Score

```python
class NetworkQualityScore:
    """
    Score network quality the Gettys way: latency under load.
    """
    
    @staticmethod
    def calculate_score(measurements: NetworkMeasurements) -> QualityScore:
        """
        Calculate a network quality score.
        
        Key insight: combine baseline latency, bloat, and jitter.
        """
        baseline = measurements.baseline_rtt
        loaded = measurements.loaded_rtt
        jitter = measurements.jitter
        loss = measurements.packet_loss
        
        # Bloat penalty
        bloat = loaded - baseline
        bloat_factor = 1.0 / (1.0 + bloat / 50.0)  # Penalize heavily
        
        # Baseline penalty (prefer low latency)
        baseline_factor = 1.0 / (1.0 + baseline / 100.0)
        
        # Jitter penalty
        jitter_factor = 1.0 / (1.0 + jitter / 20.0)
        
        # Loss penalty (severe)
        loss_factor = (1.0 - loss) ** 2
        
        # Combined score (0-100)
        raw_score = (bloat_factor * 0.5 + 
                     baseline_factor * 0.2 + 
                     jitter_factor * 0.2 + 
                     loss_factor * 0.1)
        
        score = int(raw_score * 100)
        
        # Grade
        if score >= 90:
            grade = 'A'
        elif score >= 75:
            grade = 'B'
        elif score >= 60:
            grade = 'C'
        elif score >= 40:
            grade = 'D'
        else:
            grade = 'F'
        
        return QualityScore(
            score=score,
            grade=grade,
            baseline_rtt=baseline,
            bloat=bloat,
            jitter=jitter,
            loss=loss,
            bottleneck=identify_bottleneck(measurements),
        )


def identify_bottleneck(measurements: NetworkMeasurements) -> str:
    """
    Identify what's hurting network quality most.
    """
    bloat = measurements.loaded_rtt - measurements.baseline_rtt
    
    if bloat > 100:
        return 'bufferbloat'
    elif measurements.baseline_rtt > 100:
        return 'high_base_latency'
    elif measurements.jitter > 30:
        return 'jitter'
    elif measurements.packet_loss > 0.01:
        return 'packet_loss'
    else:
        return 'none'
```

### Buffer Sizing

```python
class BufferSizing:
    """
    Size buffers correctly to avoid bloat while maintaining throughput.
    """
    
    @staticmethod
    def calculate_optimal_buffer(bandwidth_mbps: float,
                                  rtt_ms: float,
                                  num_flows: int = 1) -> BufferRecommendation:
        """
        Calculate optimal buffer size.
        
        Rule of thumb (for N flows):
            Buffer = BDP / sqrt(N)
        
        Where BDP = Bandwidth × RTT
        """
        # Bandwidth-Delay Product
        bandwidth_bytes_per_sec = bandwidth_mbps * 1_000_000 / 8
        rtt_sec = rtt_ms / 1000
        bdp_bytes = bandwidth_bytes_per_sec * rtt_sec
        
        # Buffer size
        if num_flows == 1:
            buffer_bytes = bdp_bytes
        else:
            # Appenzeller et al: BDP / sqrt(N)
            buffer_bytes = bdp_bytes / (num_flows ** 0.5)
        
        # Convert to practical units
        buffer_packets = int(buffer_bytes / 1500)  # MTU
        buffer_ms = rtt_ms / (num_flows ** 0.5) if num_flows > 1 else rtt_ms
        
        return BufferRecommendation(
            bdp_bytes=int(bdp_bytes),
            recommended_bytes=int(buffer_bytes),
            recommended_packets=buffer_packets,
            recommended_ms=buffer_ms,
            explanation=(
                f"For {bandwidth_mbps} Mbps link with {rtt_ms}ms RTT "
                f"and ~{num_flows} flows, buffer {buffer_packets} packets "
                f"(~{buffer_ms:.1f}ms of data)"
            )
        )
    
    @staticmethod
    def linux_buffer_settings(buffer_bytes: int) -> dict:
        """
        Generate Linux sysctl settings for buffer sizes.
        """
        return {
            'net.core.rmem_max': buffer_bytes,
            'net.core.wmem_max': buffer_bytes,
            'net.ipv4.tcp_rmem': f'4096 87380 {buffer_bytes}',
            'net.ipv4.tcp_wmem': f'4096 65536 {buffer_bytes}',
            'net.core.netdev_max_backlog': 1000,  # Reduce from default
        }
    
    @staticmethod
    def enable_fq_codel(interface: str) -> str:
        """
        Generate command to enable fq_codel on an interface.
        """
        return f"""
# Enable fq_codel on {interface}
tc qdisc del dev {interface} root 2>/dev/null
tc qdisc add dev {interface} root fq_codel

# Verify
tc -s qdisc show dev {interface}
"""
```

## Mental Model

Gettys approaches network performance by asking:

1. **What's the RTT under load?** That's the true latency
2. **How deep are the buffers?** Seconds of buffering = seconds of lag
3. **Is there flow isolation?** One flow shouldn't ruin others
4. **Is AQM enabled?** fq_codel should be everywhere
5. **Would I notice lag?** User experience is the metric

## The Bufferbloat Checklist

```
□ Measure RTT under load, not idle
□ Compare loaded RTT to baseline (>10x = severe bloat)
□ Enable fq_codel on all bottleneck queues
□ Size buffers based on BDP, not maximum
□ Test with interactive + bulk traffic together
□ Monitor queue depth, not just throughput
□ Grade with dslreports.com/speedtest or similar
□ Check router, modem, AND ISP equipment
```

## Signature Gettys Moves

- Bufferbloat diagnosis (idle vs loaded RTT)
- fq_codel as the universal solution
- "Latency is the new bandwidth"
- Flow isolation requirement
- Queue depth monitoring
- BDP-based buffer sizing
- User experience as the metric
- Crusading for AQM everywhere
