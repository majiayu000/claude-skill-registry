---
name: jump-trading-fpga-hft
description: Build trading systems in the style of Jump Trading, the high-frequency trading firm pioneering FPGA-based trading. Emphasizes hardware acceleration, network optimization, and nanosecond-level execution. Use when building FPGA trading systems, network-optimized infrastructure, or ultra-low-latency order execution.
---

# Jump Trading Style Guide

## Overview

Jump Trading is a proprietary trading firm known for pushing the boundaries of trading technology. They pioneered FPGA-based trading, invested in microwave networks for faster-than-fiber connectivity, and operate at the absolute frontier of latency optimization.

## Core Philosophy

> "The speed of light is the only limit we accept."

> "Software is too slow. Put it in hardware."

> "Network latency is just physics. Compute latency is engineering failure."

Jump believes that when software is too slow, you put the logic in hardware. FPGAs can process market data and generate orders in hundreds of nanoseconds—faster than a CPU can even wake up.

## Design Principles

1. **Hardware > Software**: When latency matters, use FPGAs.

2. **Network is Critical**: Microwave beats fiber. Co-location beats remote.

3. **Picoseconds Matter**: At the frontier, every nanosecond is fought for.

4. **Deterministic Wins**: Jitter is the enemy of consistent performance.

5. **Full Stack Ownership**: Own everything from NIC to exchange.

## When Building Ultra-Low-Latency Systems

### Always

- Measure wire-to-wire latency, not component latency
- Use FPGAs for time-critical decisions
- Optimize network path (co-location, cross-connects, switches)
- Process data in the NIC when possible (smart NICs)
- Eliminate all unnecessary hops
- Use hardware timestamps for accurate measurement

### Never

- Trust software timestamps
- Use general-purpose switches in the critical path
- Assume network latency is fixed
- Ignore the physical layer (cables, optics, switches)
- Process sequentially when you can pipeline
- Wait for full message when you can cut-through

### Prefer

- FPGAs over CPUs for fixed logic
- Cut-through switching over store-and-forward
- Microwave/millimeter-wave over fiber for long distances
- Dedicated lines over shared infrastructure
- Hardware timestamping over software
- Parallel processing over sequential

## Code Patterns

### FPGA Market Data Parser (Pseudo-Verilog)

```verilog
// FPGA-based market data parsing and order generation
// Processes UDP multicast market data, generates orders in ~200ns

module market_data_parser (
    input wire clk_312_5mhz,      // 312.5 MHz clock (3.2ns period)
    input wire [63:0] eth_data,   // 64-bit data from MAC
    input wire eth_valid,
    input wire eth_sof,           // Start of frame
    input wire eth_eof,           // End of frame
    
    output reg [63:0] order_data,
    output reg order_valid,
    output reg [15:0] symbol_id,
    output reg [31:0] bid_price,
    output reg [31:0] ask_price,
    output reg [31:0] bid_size,
    output reg [31:0] ask_size
);

    // Pipeline stages for parallel processing
    reg [2:0] state;
    localparam IDLE = 0, PARSE_HEADER = 1, PARSE_SYMBOL = 2,
               PARSE_BID = 3, PARSE_ASK = 4, GENERATE_ORDER = 5;
    
    // Pre-computed strategy parameters (loaded at startup)
    reg [31:0] fair_value [0:4095];      // Per-symbol fair value
    reg [31:0] edge_threshold [0:4095];  // Min edge to trade
    reg [31:0] max_position [0:4095];    // Position limits
    
    // Current positions (updated by fill handler)
    reg [31:0] positions [0:4095];
    
    always @(posedge clk_312_5mhz) begin
        case (state)
            IDLE: begin
                order_valid <= 0;
                if (eth_valid && eth_sof) begin
                    state <= PARSE_HEADER;
                end
            end
            
            PARSE_HEADER: begin
                // Parse UDP header, extract message type
                // Skip IP/UDP headers (known fixed offsets)
                if (is_quote_message(eth_data)) begin
                    state <= PARSE_SYMBOL;
                end else begin
                    state <= IDLE;
                end
            end
            
            PARSE_SYMBOL: begin
                symbol_id <= eth_data[15:0];
                state <= PARSE_BID;
            end
            
            PARSE_BID: begin
                bid_price <= eth_data[31:0];
                bid_size <= eth_data[63:32];
                state <= PARSE_ASK;
            end
            
            PARSE_ASK: begin
                ask_price <= eth_data[31:0];
                ask_size <= eth_data[63:32];
                state <= GENERATE_ORDER;
            end
            
            GENERATE_ORDER: begin
                // All logic executes in single clock cycle
                wire [31:0] fv = fair_value[symbol_id];
                wire [31:0] edge = edge_threshold[symbol_id];
                wire [31:0] pos = positions[symbol_id];
                wire [31:0] max_pos = max_position[symbol_id];
                
                // Buy if bid is below fair value minus edge
                wire should_buy = (bid_price < fv - edge) && (pos < max_pos);
                
                // Sell if ask is above fair value plus edge  
                wire should_sell = (ask_price > fv + edge) && (pos > -max_pos);
                
                if (should_buy) begin
                    order_data <= build_buy_order(symbol_id, bid_price, bid_size);
                    order_valid <= 1;
                end else if (should_sell) begin
                    order_data <= build_sell_order(symbol_id, ask_price, ask_size);
                    order_valid <= 1;
                end
                
                state <= IDLE;
            end
        endcase
    end

endmodule
```

### Network Topology Optimization

```python
class NetworkOptimizer:
    """
    Jump's network optimization: every nanosecond counts.
    Model and optimize the full network path.
    """
    
    def __init__(self):
        self.topology = {}
        self.latency_measurements = {}
    
    def model_path_latency(self, 
                           source: str, 
                           destination: str) -> LatencyBreakdown:
        """
        Break down latency into components.
        """
        path = self.find_path(source, destination)
        
        breakdown = LatencyBreakdown()
        
        for i, (node_a, node_b) in enumerate(zip(path[:-1], path[1:])):
            link = self.topology[(node_a, node_b)]
            
            # Propagation delay (speed of light in medium)
            # Fiber: ~5 ns/meter, Microwave: ~3.3 ns/meter
            prop_delay = link.distance_meters * link.propagation_factor
            breakdown.propagation_ns += prop_delay
            
            # Serialization delay (time to put bits on wire)
            # 10GbE: 67.2ns for 64-byte frame
            serial_delay = (link.frame_size_bytes * 8) / link.bandwidth_gbps
            breakdown.serialization_ns += serial_delay
            
            # Switch/router delay
            if link.device_type == 'cut_through_switch':
                # Cut-through: forward after seeing destination MAC (~300ns)
                breakdown.switching_ns += 300
            elif link.device_type == 'store_forward_switch':
                # Store-and-forward: wait for full frame (~5000ns for 64B)
                breakdown.switching_ns += 5000
            
            # NIC delay (if applicable)
            if i == 0:  # Source NIC
                breakdown.nic_tx_ns += link.nic_tx_latency_ns
            if i == len(path) - 2:  # Destination NIC
                breakdown.nic_rx_ns += link.nic_rx_latency_ns
        
        return breakdown
    
    def compare_microwave_vs_fiber(self, 
                                    point_a: Location, 
                                    point_b: Location) -> dict:
        """
        Microwave travels at ~c (speed of light in vacuum).
        Fiber travels at ~0.67c (speed of light in glass).
        For long distances, microwave wins despite being line-of-sight.
        """
        distance_km = self.calculate_distance(point_a, point_b)
        
        # Speed of light
        c = 299792.458  # km/s
        
        # Fiber: ~0.67c due to refractive index, plus routing overhead
        fiber_speed = c * 0.67
        fiber_distance = distance_km * 1.3  # Routing adds ~30%
        fiber_latency_ms = (fiber_distance / fiber_speed) * 1000
        
        # Microwave: ~0.99c, nearly straight line
        microwave_speed = c * 0.99
        microwave_distance = distance_km * 1.02  # Slight deviation for terrain
        microwave_latency_ms = (microwave_distance / microwave_speed) * 1000
        
        return {
            'fiber_latency_ms': fiber_latency_ms,
            'microwave_latency_ms': microwave_latency_ms,
            'savings_ms': fiber_latency_ms - microwave_latency_ms,
            'savings_percent': (fiber_latency_ms - microwave_latency_ms) / fiber_latency_ms * 100
        }
```

### Smart NIC Processing

```cpp
// Smart NIC (Bluefield/Netronome) for in-NIC processing
// Process market data before it hits CPU

class SmartNICProcessor {
public:
    // Run on NIC's ARM cores / P4 engine
    struct PacketContext {
        uint64_t timestamp_hw;    // Hardware timestamp from PHY
        uint8_t* packet_data;
        uint16_t length;
    };
    
    // This runs on the NIC, not the host CPU
    __attribute__((section(".nic_code")))
    Action process_packet(PacketContext* ctx) {
        // Parse at line rate
        auto* eth = reinterpret_cast<EthernetHeader*>(ctx->packet_data);
        
        if (eth->ethertype != ETHERTYPE_IP) {
            return Action::PASS_TO_HOST;
        }
        
        auto* ip = reinterpret_cast<IPHeader*>(eth + 1);
        auto* udp = reinterpret_cast<UDPHeader*>(ip + 1);
        
        // Filter: only process market data multicast
        if (!is_market_data_multicast(ip->dst_addr, udp->dst_port)) {
            return Action::PASS_TO_HOST;
        }
        
        auto* msg = reinterpret_cast<MarketDataMessage*>(udp + 1);
        
        // Simple filtering: drop if not in our symbol universe
        if (!is_in_universe(msg->symbol_id)) {
            return Action::DROP;
        }
        
        // Add hardware timestamp and pass to host
        ctx->packet_data = prepend_timestamp(ctx->packet_data, ctx->timestamp_hw);
        
        return Action::PASS_TO_HOST;
    }
};
```

### Precision Time Protocol (PTP)

```cpp
// Hardware-based time synchronization

class PTPTimeSync {
    /*
     * Jump uses PTP (IEEE 1588) for nanosecond-accurate time sync.
     * Critical for correlating events across systems and fair latency measurement.
     */
    
public:
    void configure_ptp_hardware(int nic_fd) {
        // Enable hardware timestamping
        struct hwtstamp_config config = {};
        config.tx_type = HWTSTAMP_TX_ON;
        config.rx_filter = HWTSTAMP_FILTER_ALL;
        
        struct ifreq ifr = {};
        ifr.ifr_data = (char*)&config;
        ioctl(nic_fd, SIOCSHWTSTAMP, &ifr);
        
        // Get PHC (PTP Hardware Clock) device
        struct ethtool_ts_info info = {};
        info.cmd = ETHTOOL_GET_TS_INFO;
        ifr.ifr_data = (char*)&info;
        ioctl(nic_fd, SIOCETHTOOL, &ifr);
        
        // Open PHC device
        char phc_device[32];
        snprintf(phc_device, sizeof(phc_device), "/dev/ptp%d", info.phc_index);
        phc_fd_ = open(phc_device, O_RDWR);
    }
    
    uint64_t get_hardware_time_ns() {
        struct ptp_clock_time ptc;
        ioctl(phc_fd_, PTP_CLOCK_GETTIME, &ptc);
        return ptc.sec * 1000000000ULL + ptc.nsec;
    }
    
    // Extract hardware timestamp from received packet
    uint64_t extract_rx_timestamp(struct msghdr* msg) {
        for (struct cmsghdr* cmsg = CMSG_FIRSTHDR(msg); 
             cmsg; 
             cmsg = CMSG_NXTHDR(msg, cmsg)) {
            
            if (cmsg->cmsg_level == SOL_SOCKET &&
                cmsg->cmsg_type == SCM_TIMESTAMPING) {
                
                struct scm_timestamping* ts = 
                    (struct scm_timestamping*)CMSG_DATA(cmsg);
                
                // Use hardware timestamp (ts[2]) not software (ts[0])
                return ts->ts[2].tv_sec * 1000000000ULL + 
                       ts->ts[2].tv_nsec;
            }
        }
        return 0;
    }

private:
    int phc_fd_;
};
```

### Wire-to-Wire Latency Measurement

```cpp
class WireToWireLatency {
    /*
     * Measure true latency: from photons arriving at RX NIC
     * to photons leaving TX NIC.
     * Software timestamps are useless at these scales.
     */
    
public:
    struct Measurement {
        uint64_t rx_hw_timestamp;    // When packet hit our NIC (hardware)
        uint64_t tx_hw_timestamp;    // When response left our NIC (hardware)
        uint64_t wire_to_wire_ns;    // Total latency
        
        // Component breakdown (if instrumented)
        uint64_t parse_ns;
        uint64_t strategy_ns;
        uint64_t order_build_ns;
        uint64_t tx_queue_ns;
    };
    
    void record_tick_to_trade(
        uint64_t market_data_rx_hw_ts,
        uint64_t order_tx_hw_ts) {
        
        uint64_t latency_ns = order_tx_hw_ts - market_data_rx_hw_ts;
        
        histogram_.record(latency_ns);
        
        // Alert if we exceed target
        if (latency_ns > target_latency_ns_) {
            log_slow_path(latency_ns);
        }
    }
    
    void print_histogram() {
        // Typical Jump-style output:
        // p50: 180ns, p99: 320ns, p999: 890ns, max: 1.2us
        auto stats = histogram_.get_stats();
        printf("Wire-to-wire latency:\n");
        printf("  p50:  %luns\n", stats.p50);
        printf("  p99:  %luns\n", stats.p99);
        printf("  p999: %luns\n", stats.p999);
        printf("  max:  %luns\n", stats.max);
    }
};
```

## Mental Model

Jump approaches ultra-low-latency by asking:

1. **What's the physics limit?** Speed of light × distance
2. **Where's the compute?** Move it to hardware (FPGA/SmartNIC)
3. **What's the network path?** Optimize every hop
4. **What's the jitter?** Worst case matters more than average
5. **Can we pipeline?** Process in parallel, not sequentially

## Signature Jump Moves

- FPGA-based trading logic
- Microwave networks for long-haul
- Smart NIC pre-processing
- Hardware PTP time synchronization
- Cut-through switching
- Wire-to-wire latency measurement
- Nanosecond-level optimization
- Co-location at every major exchange
- Full-stack hardware/software ownership
