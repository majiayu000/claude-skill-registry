---
name: jacobson-network-performance
description: Engineer network systems in the style of Van Jacobson, the architect of TCP congestion control who saved the internet from collapse. Emphasizes congestion avoidance, RTT-based adaptation, queue management, and understanding network dynamics. Use when optimizing network performance, implementing congestion control, or diagnosing latency issues.
---

# Van Jacobson Network Performance Style Guide

## Overview

Van Jacobson is the most influential network performance engineer in history. In 1988, when the internet was experiencing "congestion collapse" (throughput dropping to 0.1% of capacity), Jacobson developed the congestion control algorithms that saved it. His slow start, congestion avoidance, fast retransmit, and fast recovery algorithms are still the foundation of TCP today. He also created traceroute, tcpdump, and later CoDel—tools and algorithms that define how we understand and manage networks.

## Core Philosophy

> "The network is a shared resource. Every packet you send affects everyone else."

> "Congestion is not a problem to be avoided—it's information to be used."

> "Measure, don't guess. The network will tell you what's happening if you listen."

Jacobson's insight was that the network itself provides feedback about congestion through packet loss and delay. By responding to this feedback correctly, endpoints can cooperatively share bandwidth without central coordination. The key is measuring Round-Trip Time (RTT) accurately and responding to congestion signals promptly.

## Design Principles

1. **Conservation of Packets**: In equilibrium, inject a new packet only when one leaves.

2. **Additive Increase, Multiplicative Decrease (AIMD)**: Probe for bandwidth slowly, back off quickly.

3. **RTT is Truth**: Round-trip time tells you the network's state.

4. **Self-Clocking**: Use ACKs to pace transmission, not timers.

5. **Respond to Congestion, Don't Cause It**: Detect early, react appropriately.

## The Congestion Control Algorithms

### Slow Start

```
On connection start or after timeout:
    cwnd = 1 MSS (or IW = 10 in modern TCP)
    
On each ACK received:
    cwnd = cwnd + MSS  (exponential growth)
    
Until:
    cwnd >= ssthresh  →  enter Congestion Avoidance
    OR packet loss    →  enter Fast Recovery
```

```
Slow Start Visualization:

RTT 1:  [1]                           cwnd = 1
RTT 2:  [2][3]                        cwnd = 2
RTT 3:  [4][5][6][7]                  cwnd = 4
RTT 4:  [8][9][10][11][12][13][14][15] cwnd = 8
        ↑
        Exponential growth: doubles each RTT
```

### Congestion Avoidance

```
When cwnd >= ssthresh:
    
On each ACK received:
    cwnd = cwnd + MSS * (MSS / cwnd)  (linear growth)
    
    Equivalently: cwnd increases by 1 MSS per RTT
    
On packet loss (3 duplicate ACKs):
    ssthresh = cwnd / 2
    cwnd = ssthresh + 3 MSS
    Enter Fast Recovery
    
On timeout:
    ssthresh = cwnd / 2
    cwnd = 1 MSS
    Enter Slow Start
```

```
Congestion Avoidance Visualization:

cwnd
  ^
  |         /\
  |        /  \        /\
  |       /    \      /  \
  |      /      \    /    \
  |     /        \  /      \
  |    /          \/        \
  |   /                      ↓ loss: cwnd = cwnd/2
  |  / ← slow start
  | /
  +---------------------------------> time
     ssthresh
```

### Fast Retransmit and Fast Recovery

```
On receiving 3 duplicate ACKs (same ACK number):
    # Packet was likely lost, not delayed
    
    ssthresh = cwnd / 2
    cwnd = ssthresh + 3 MSS  (inflate for packets in flight)
    Retransmit the missing segment
    
On each additional duplicate ACK:
    cwnd = cwnd + MSS  (keep inflating)
    
On new ACK (acknowledges new data):
    cwnd = ssthresh  (deflate to new window)
    Enter Congestion Avoidance
```

## RTT Estimation

### Jacobson's Algorithm

```python
# Jacobson's RTT estimator (RFC 6298)

class RTTEstimator:
    """
    Jacobson's algorithm for RTT estimation.
    The foundation of all TCP timing.
    """
    
    def __init__(self):
        self.srtt = None      # Smoothed RTT
        self.rttvar = None    # RTT variance
        self.rto = 1.0        # Retransmission timeout
        
        # Constants (from RFC 6298)
        self.alpha = 1/8      # SRTT smoothing factor
        self.beta = 1/4       # RTTVAR smoothing factor
        self.K = 4            # RTO variance multiplier
        self.G = 0.001        # Clock granularity (1ms)
    
    def update(self, measured_rtt: float):
        """
        Update RTT estimate with new measurement.
        """
        if self.srtt is None:
            # First measurement
            self.srtt = measured_rtt
            self.rttvar = measured_rtt / 2
        else:
            # Jacobson's algorithm
            # RTTVAR = (1 - beta) * RTTVAR + beta * |SRTT - R'|
            self.rttvar = (1 - self.beta) * self.rttvar + \
                          self.beta * abs(self.srtt - measured_rtt)
            
            # SRTT = (1 - alpha) * SRTT + alpha * R'
            self.srtt = (1 - self.alpha) * self.srtt + \
                        self.alpha * measured_rtt
        
        # RTO = SRTT + max(G, K * RTTVAR)
        self.rto = self.srtt + max(self.G, self.K * self.rttvar)
        
        # Clamp RTO to reasonable bounds
        self.rto = max(1.0, min(60.0, self.rto))
        
        return self.rto
    
    def timeout_occurred(self):
        """
        Double RTO on timeout (exponential backoff).
        """
        self.rto = min(60.0, self.rto * 2)
```

### Karn's Algorithm

```python
# Karn's algorithm: Don't update RTT from retransmitted segments

class KarnRTTEstimator(RTTEstimator):
    """
    Karn's algorithm: only measure RTT from non-retransmitted segments.
    Avoids ambiguity about which transmission the ACK is for.
    """
    
    def __init__(self):
        super().__init__()
        self.retransmitted = set()
    
    def send_segment(self, seq_num: int, is_retransmit: bool):
        """Track which segments are retransmits."""
        if is_retransmit:
            self.retransmitted.add(seq_num)
        else:
            self.retransmitted.discard(seq_num)
    
    def receive_ack(self, ack_num: int, measured_rtt: float):
        """
        Only update RTT if segment wasn't retransmitted.
        """
        if ack_num in self.retransmitted:
            # Ambiguous: was this ACK for original or retransmit?
            # Don't update RTT, but do clear the retransmit flag
            self.retransmitted.discard(ack_num)
            return None
        else:
            # Safe to update RTT
            return self.update(measured_rtt)
```

## When Engineering Networks

### Always

- Measure RTT continuously—it's your primary signal
- Respond to packet loss by reducing rate
- Use AIMD for stable convergence
- Implement exponential backoff on timeouts
- Consider the network as a shared resource
- Test under realistic congestion conditions

### Never

- Send faster than ACKs arrive (violates self-clocking)
- Ignore packet loss (the network is telling you something)
- Use fixed timeouts (RTT varies enormously)
- Assume the network is empty (others share it)
- Measure RTT from retransmits (Karn's algorithm)
- React to single events (smooth your signals)

### Prefer

- RTT-based signals over loss-based (less destructive)
- Gradual probing over aggressive sending
- Self-clocking over timer-based pacing
- Smooth estimates over instantaneous values
- Multiplicative decrease over additive (stability)
- End-to-end measurement over assumptions

## Code Patterns

### TCP Congestion Control Implementation

```python
class JacobsonCongestionControl:
    """
    Jacobson's TCP congestion control.
    The algorithm that saved the internet.
    """
    
    def __init__(self, mss: int = 1460):
        self.mss = mss
        self.cwnd = mss  # Congestion window
        self.ssthresh = 65535  # Slow start threshold
        self.state = 'SLOW_START'
        self.dup_ack_count = 0
        self.rtt_estimator = RTTEstimator()
    
    def on_ack(self, bytes_acked: int, is_duplicate: bool, rtt: float = None):
        """
        Process an ACK.
        """
        if rtt is not None:
            self.rtt_estimator.update(rtt)
        
        if is_duplicate:
            return self._on_duplicate_ack()
        else:
            self.dup_ack_count = 0
            return self._on_new_ack(bytes_acked)
    
    def _on_new_ack(self, bytes_acked: int):
        """Handle new ACK (acknowledges new data)."""
        
        if self.state == 'SLOW_START':
            # Exponential growth
            self.cwnd += self.mss
            
            if self.cwnd >= self.ssthresh:
                self.state = 'CONGESTION_AVOIDANCE'
                
        elif self.state == 'CONGESTION_AVOIDANCE':
            # Linear growth: +1 MSS per RTT
            # Approximated as: cwnd += MSS * (MSS / cwnd) per ACK
            self.cwnd += self.mss * self.mss // self.cwnd
            
        elif self.state == 'FAST_RECOVERY':
            # Exit fast recovery
            self.cwnd = self.ssthresh
            self.state = 'CONGESTION_AVOIDANCE'
        
        return {'cwnd': self.cwnd, 'state': self.state}
    
    def _on_duplicate_ack(self):
        """Handle duplicate ACK."""
        self.dup_ack_count += 1
        
        if self.state == 'FAST_RECOVERY':
            # Inflate cwnd for each dup ACK
            self.cwnd += self.mss
            
        elif self.dup_ack_count == 3:
            # Enter fast recovery
            self.ssthresh = max(self.cwnd // 2, 2 * self.mss)
            self.cwnd = self.ssthresh + 3 * self.mss
            self.state = 'FAST_RECOVERY'
            return {'retransmit': True, 'cwnd': self.cwnd}
        
        return {'cwnd': self.cwnd, 'state': self.state}
    
    def on_timeout(self):
        """Handle retransmission timeout."""
        # Timeout is severe: go back to slow start
        self.ssthresh = max(self.cwnd // 2, 2 * self.mss)
        self.cwnd = self.mss
        self.state = 'SLOW_START'
        self.dup_ack_count = 0
        self.rtt_estimator.timeout_occurred()
        
        return {'retransmit': True, 'cwnd': self.cwnd, 'rto': self.rtt_estimator.rto}
    
    def bytes_in_flight_limit(self) -> int:
        """Maximum bytes allowed in flight."""
        return self.cwnd
```

### Traceroute Implementation

```python
class Traceroute:
    """
    Jacobson's traceroute: discover the path packets take.
    Uses TTL expiration to elicit ICMP responses from routers.
    """
    
    def __init__(self, 
                 target: str,
                 max_hops: int = 30,
                 probes_per_hop: int = 3,
                 timeout: float = 5.0):
        self.target = target
        self.max_hops = max_hops
        self.probes = probes_per_hop
        self.timeout = timeout
    
    def trace(self) -> List[Hop]:
        """
        Trace the route to target.
        """
        hops = []
        target_reached = False
        
        for ttl in range(1, self.max_hops + 1):
            hop_results = []
            
            for probe in range(self.probes):
                result = self._send_probe(ttl)
                hop_results.append(result)
                
                if result.reached_target:
                    target_reached = True
            
            hops.append(Hop(
                ttl=ttl,
                probes=hop_results,
                addr=self._most_common_addr(hop_results),
            ))
            
            if target_reached:
                break
        
        return hops
    
    def _send_probe(self, ttl: int) -> ProbeResult:
        """
        Send a single probe with given TTL.
        """
        # Create UDP or ICMP packet with specified TTL
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
        sock.settimeout(self.timeout)
        
        # Use high port unlikely to be in use
        dest_port = 33434 + ttl
        
        start_time = time.time()
        
        try:
            sock.sendto(b'', (self.target, dest_port))
            
            # Wait for ICMP response
            icmp_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, 
                                      socket.IPPROTO_ICMP)
            icmp_sock.settimeout(self.timeout)
            
            data, addr = icmp_sock.recvfrom(1024)
            rtt = (time.time() - start_time) * 1000  # ms
            
            icmp_type = data[20]  # ICMP type in IP payload
            
            if icmp_type == 11:  # Time Exceeded
                return ProbeResult(addr=addr[0], rtt=rtt, reached_target=False)
            elif icmp_type == 3:  # Destination Unreachable (we reached it!)
                return ProbeResult(addr=addr[0], rtt=rtt, reached_target=True)
            
        except socket.timeout:
            return ProbeResult(addr=None, rtt=None, reached_target=False)
        
        finally:
            sock.close()
```

### Network Diagnostic Tools

```python
class NetworkDiagnostics:
    """
    Jacobson-style network diagnostics.
    Measure, don't guess.
    """
    
    def measure_bandwidth_delay_product(self, 
                                         rtt_ms: float, 
                                         bandwidth_mbps: float) -> int:
        """
        Calculate BDP: the amount of data "in flight" for full utilization.
        
        BDP = RTT × Bandwidth
        
        This determines optimal buffer and window sizes.
        """
        rtt_seconds = rtt_ms / 1000
        bandwidth_bytes_per_sec = bandwidth_mbps * 1_000_000 / 8
        
        bdp_bytes = int(rtt_seconds * bandwidth_bytes_per_sec)
        
        return bdp_bytes
    
    def diagnose_congestion(self, 
                             samples: List[RTTSample]) -> CongestionDiagnosis:
        """
        Diagnose network congestion from RTT samples.
        """
        if len(samples) < 10:
            return CongestionDiagnosis(status='insufficient_data')
        
        rtts = [s.rtt for s in samples]
        min_rtt = min(rtts)
        avg_rtt = sum(rtts) / len(rtts)
        max_rtt = max(rtts)
        
        # Buffering = avg_rtt - min_rtt
        buffering_delay = avg_rtt - min_rtt
        
        # Jitter = variance in RTT
        variance = sum((r - avg_rtt) ** 2 for r in rtts) / len(rtts)
        jitter = variance ** 0.5
        
        # Diagnose
        if buffering_delay > min_rtt:
            status = 'severe_buffering'
            recommendation = 'Reduce buffer sizes or apply AQM'
        elif buffering_delay > min_rtt * 0.5:
            status = 'moderate_buffering'
            recommendation = 'Consider AQM (CoDel/fq_codel)'
        elif jitter > min_rtt * 0.3:
            status = 'high_jitter'
            recommendation = 'Check for competing traffic or poor link'
        else:
            status = 'healthy'
            recommendation = 'Network performing well'
        
        return CongestionDiagnosis(
            status=status,
            min_rtt=min_rtt,
            avg_rtt=avg_rtt,
            buffering_delay=buffering_delay,
            jitter=jitter,
            recommendation=recommendation,
        )
    
    def estimate_available_bandwidth(self,
                                      packet_pairs: List[PacketPair]) -> float:
        """
        Estimate available bandwidth using packet pair technique.
        """
        # Dispersion = time between arrivals of back-to-back packets
        # Bandwidth = packet_size / dispersion
        
        bandwidths = []
        for pair in packet_pairs:
            if pair.dispersion > 0:
                bw = pair.packet_size / pair.dispersion
                bandwidths.append(bw)
        
        if not bandwidths:
            return 0.0
        
        # Use median to filter outliers
        bandwidths.sort()
        median_idx = len(bandwidths) // 2
        return bandwidths[median_idx]
```

### CoDel (Controlled Delay)

```python
class CoDel:
    """
    CoDel: Controlled Delay AQM.
    Jacobson & Nichols' solution to bufferbloat.
    
    Key insight: control delay, not queue length.
    """
    
    def __init__(self,
                 target_delay_ms: float = 5.0,
                 interval_ms: float = 100.0):
        self.target = target_delay_ms
        self.interval = interval_ms
        
        self.first_above_time = None
        self.drop_next = 0
        self.count = 0
        self.dropping = False
    
    def should_drop(self, packet: Packet, now_ms: float) -> bool:
        """
        Decide whether to drop a packet.
        
        CoDel only drops when queue delay persistently exceeds target.
        """
        sojourn_time = now_ms - packet.enqueue_time
        
        if sojourn_time < self.target:
            # Good: delay below target
            self.first_above_time = None
            return False
        
        # Delay exceeds target
        if self.first_above_time is None:
            # First time above target
            self.first_above_time = now_ms
            return False
        
        if now_ms - self.first_above_time < self.interval:
            # Haven't been above target long enough
            return False
        
        # Persistent high delay: start/continue dropping
        if not self.dropping:
            self.dropping = True
            self.count = 1
            self.drop_next = now_ms + self.interval
            return True
        
        if now_ms >= self.drop_next:
            self.count += 1
            # Decrease interval: drop more aggressively
            self.drop_next = now_ms + self.interval / (self.count ** 0.5)
            return True
        
        return False
    
    def dequeue(self, queue: Queue, now_ms: float) -> Optional[Packet]:
        """
        Dequeue with CoDel logic.
        """
        packet = queue.peek()
        if packet is None:
            self.dropping = False
            return None
        
        if self.should_drop(packet, now_ms):
            queue.pop()  # Drop this packet
            # Try next packet
            return self.dequeue(queue, now_ms)
        
        return queue.pop()
```

## Mental Model

Jacobson approaches network performance by asking:

1. **What does the RTT tell me?** It's the network's heartbeat
2. **Is there packet loss?** The network signaling congestion
3. **Am I being fair?** Others share this resource
4. **Am I measuring or guessing?** Always measure
5. **What's the delay vs. throughput tradeoff?** Optimize for the use case

## The Network Performance Checklist

```
□ Measure RTT continuously and accurately
□ Respond to congestion signals (loss, delay)
□ Use AIMD for stable convergence
□ Implement proper timeout calculation (Jacobson's algorithm)
□ Follow Karn's algorithm for retransmit RTT
□ Understand your bandwidth-delay product
□ Check for bufferbloat (RTT under load vs idle)
□ Use appropriate queue management (CoDel/fq_codel)
```

## Signature Jacobson Moves

- Slow start and congestion avoidance
- Fast retransmit and fast recovery
- RTT estimation with variance (Jacobson's algorithm)
- Self-clocking via ACK pacing
- AIMD (Additive Increase, Multiplicative Decrease)
- CoDel active queue management
- traceroute and tcpdump
- Conservation of packets principle
