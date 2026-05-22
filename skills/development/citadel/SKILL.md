---
name: citadel-low-latency-systems
description: Build trading systems in the style of Citadel Securities, the world's largest market maker. Emphasizes ultra-low latency, deterministic execution, kernel bypass networking, and high-frequency trading infrastructure. Use when building latency-critical systems, market making engines, or high-performance trading platforms.
---

# Citadel Securities Style Guide

## Overview

Citadel Securities is the world's largest market maker, handling ~25% of all U.S. equity volume and ~40% of retail order flow. They execute millions of trades daily with sub-microsecond latency requirements. Their infrastructure represents the pinnacle of low-latency systems engineering.

## Core Philosophy

> "Every microsecond is a competitive advantage."

> "Determinism is more important than average performance."

> "The fastest system is the one that doesn't do unnecessary work."

Citadel believes that in market making, consistent low latency beats occasionally fast. Jitter is the enemy. Every component must be predictable and measurable.

## Design Principles

1. **Latency is King**: Measure in microseconds, optimize in nanoseconds.

2. **Determinism Over Speed**: Predictable performance beats variable performance.

3. **Kernel Bypass**: The OS is too slow; go around it.

4. **Lock-Free Everything**: Locks are latency landmines.

5. **Mechanical Sympathy**: Know your hardware intimately.

## When Building Low-Latency Systems

### Always

- Measure latency at every component boundary
- Use kernel bypass networking (DPDK, Solarflare OpenOnload)
- Pin threads to cores, isolate from OS scheduler
- Pre-allocate all memory, no runtime allocation
- Use lock-free data structures
- Disable all non-essential OS features (hyperthreading, C-states, etc.)

### Never

- Allocate memory on the critical path
- Use locks in the hot path
- Let the OS schedule your critical threads
- Use exceptions for control flow
- Trust the compiler—verify generated assembly
- Log synchronously on the critical path

### Prefer

- Busy-waiting over blocking
- Batch processing over item-by-item
- Inline functions over virtual dispatch
- Fixed-size structures over dynamic allocation
- Struct-of-arrays over array-of-structs (for cache efficiency)
- Direct hardware access over OS abstractions

## Code Patterns

### Kernel Bypass Networking with DPDK

```cpp
// DPDK-based ultra-low-latency packet processing

class DPDKMarketDataReceiver {
private:
    struct rte_mempool* mbuf_pool_;
    uint16_t port_id_;
    alignas(64) Stats stats_;  // Cache-line aligned
    
public:
    void init(uint16_t port_id) {
        port_id_ = port_id;
        
        // Pre-allocate packet buffers
        mbuf_pool_ = rte_pktmbuf_pool_create(
            "MBUF_POOL",
            8192,           // Number of buffers
            256,            // Cache size
            0,              // Private data size
            RTE_MBUF2_BUF_SIZE,
            rte_socket_id()
        );
        
        // Configure port for low latency
        struct rte_eth_conf port_conf = {};
        port_conf.rxmode.mq_mode = ETH_MQ_RX_NONE;
        port_conf.txmode.mq_mode = ETH_MQ_TX_NONE;
        
        // Disable all offloads for minimum latency
        port_conf.rxmode.offloads = 0;
        port_conf.txmode.offloads = 0;
        
        rte_eth_dev_configure(port_id_, 1, 0, &port_conf);
    }
    
    // Hot path: called millions of times per second
    __attribute__((always_inline, hot))
    void poll_packets(PacketHandler& handler) {
        struct rte_mbuf* bufs[32];
        
        // Busy-poll: no syscalls, no context switches
        uint16_t nb_rx = rte_eth_rx_burst(port_id_, 0, bufs, 32);
        
        // Prefetch next batch while processing current
        if (likely(nb_rx > 0)) {
            rte_prefetch0(rte_pktmbuf_mtod(bufs[0], void*));
        }
        
        for (uint16_t i = 0; i < nb_rx; i++) {
            // Prefetch next packet
            if (i + 1 < nb_rx) {
                rte_prefetch0(rte_pktmbuf_mtod(bufs[i + 1], void*));
            }
            
            // Process packet inline
            char* data = rte_pktmbuf_mtod(bufs[i], char*);
            uint16_t len = rte_pktmbuf_data_len(bufs[i]);
            
            handler.process(data, len);
            
            rte_pktmbuf_free(bufs[i]);
        }
        
        stats_.packets_received += nb_rx;
    }
};
```

### Lock-Free Order Book

```cpp
// Lock-free order book for maximum throughput

template<size_t MAX_LEVELS = 256>
class alignas(64) LockFreeOrderBook {
private:
    struct PriceLevel {
        std::atomic<int64_t> price;
        std::atomic<int64_t> quantity;
    };
    
    // Separate cache lines for bids and asks
    alignas(64) std::array<PriceLevel, MAX_LEVELS> bids_;
    alignas(64) std::array<PriceLevel, MAX_LEVELS> asks_;
    alignas(64) std::atomic<uint64_t> sequence_;
    
public:
    // Update from market data (single writer)
    __attribute__((always_inline))
    void update_bid(size_t level, int64_t price, int64_t qty) {
        // Relaxed store is fine for single writer
        bids_[level].price.store(price, std::memory_order_relaxed);
        bids_[level].quantity.store(qty, std::memory_order_relaxed);
        
        // Release fence ensures all updates visible before sequence bump
        std::atomic_thread_fence(std::memory_order_release);
        sequence_.fetch_add(1, std::memory_order_relaxed);
    }
    
    // Read snapshot (multiple readers)
    __attribute__((always_inline))
    bool read_bbo(int64_t& bid, int64_t& ask, int64_t& bid_qty, int64_t& ask_qty) {
        uint64_t seq1, seq2;
        
        // Seqlock pattern: retry if writer was active
        do {
            seq1 = sequence_.load(std::memory_order_acquire);
            
            // Read all values
            bid = bids_[0].price.load(std::memory_order_relaxed);
            bid_qty = bids_[0].quantity.load(std::memory_order_relaxed);
            ask = asks_[0].price.load(std::memory_order_relaxed);
            ask_qty = asks_[0].quantity.load(std::memory_order_relaxed);
            
            std::atomic_thread_fence(std::memory_order_acquire);
            seq2 = sequence_.load(std::memory_order_relaxed);
            
        } while (seq1 != seq2 || (seq1 & 1));  // Retry if sequence changed or odd (write in progress)
        
        return true;
    }
};
```

### CPU Pinning and Isolation

```cpp
// Thread pinning for deterministic latency

class LatencyCriticalThread {
public:
    void configure_for_low_latency(int cpu_core) {
        // Pin to specific CPU core
        cpu_set_t cpuset;
        CPU_ZERO(&cpuset);
        CPU_SET(cpu_core, &cpuset);
        pthread_setaffinity_np(pthread_self(), sizeof(cpu_set_t), &cpuset);
        
        // Set real-time priority
        struct sched_param param;
        param.sched_priority = sched_get_priority_max(SCHED_FIFO);
        pthread_setschedparam(pthread_self(), SCHED_FIFO, &param);
        
        // Lock memory to prevent page faults
        mlockall(MCL_CURRENT | MCL_FUTURE);
        
        // Disable transparent huge pages for this process
        prctl(PR_SET_THP_DISABLE, 1, 0, 0, 0);
    }
};

// System configuration (run at boot)
/*
# Isolate CPUs from kernel scheduler
GRUB_CMDLINE_LINUX="isolcpus=2,3,4,5 nohz_full=2,3,4,5 rcu_nocbs=2,3,4,5"

# Disable hyperthreading
echo off > /sys/devices/system/cpu/smt/control

# Disable C-states (CPU power saving)
for cpu in /sys/devices/system/cpu/cpu*/cpuidle/state*/disable; do
    echo 1 > $cpu
done

# Set CPU frequency to maximum
for cpu in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
    echo performance > $cpu
done
*/
```

### Memory Pool with Zero Allocation

```cpp
// Pre-allocated object pool for zero-allocation hot path

template<typename T, size_t POOL_SIZE = 65536>
class alignas(64) ObjectPool {
private:
    struct alignas(64) Slot {
        std::aligned_storage_t<sizeof(T), alignof(T)> storage;
        std::atomic<Slot*> next;
    };
    
    std::array<Slot, POOL_SIZE> slots_;
    alignas(64) std::atomic<Slot*> free_list_;
    
public:
    ObjectPool() {
        // Pre-construct free list
        for (size_t i = 0; i < POOL_SIZE - 1; i++) {
            slots_[i].next.store(&slots_[i + 1], std::memory_order_relaxed);
        }
        slots_[POOL_SIZE - 1].next.store(nullptr, std::memory_order_relaxed);
        free_list_.store(&slots_[0], std::memory_order_release);
        
        // Pre-fault all pages
        volatile char* ptr = reinterpret_cast<volatile char*>(slots_.data());
        for (size_t i = 0; i < sizeof(slots_); i += 4096) {
            ptr[i] = 0;
        }
    }
    
    __attribute__((always_inline))
    T* allocate() {
        Slot* slot;
        do {
            slot = free_list_.load(std::memory_order_acquire);
            if (!slot) return nullptr;  // Pool exhausted
        } while (!free_list_.compare_exchange_weak(
            slot, slot->next.load(std::memory_order_relaxed),
            std::memory_order_release, std::memory_order_relaxed));
        
        return reinterpret_cast<T*>(&slot->storage);
    }
    
    __attribute__((always_inline))
    void deallocate(T* ptr) {
        Slot* slot = reinterpret_cast<Slot*>(ptr);
        Slot* head;
        do {
            head = free_list_.load(std::memory_order_relaxed);
            slot->next.store(head, std::memory_order_relaxed);
        } while (!free_list_.compare_exchange_weak(
            head, slot,
            std::memory_order_release, std::memory_order_relaxed));
    }
};
```

### Latency Measurement

```cpp
// Nanosecond-precision latency measurement

class LatencyHistogram {
private:
    static constexpr size_t BUCKETS = 1000;  // 0-999 microseconds
    alignas(64) std::array<std::atomic<uint64_t>, BUCKETS> histogram_;
    std::atomic<uint64_t> overflow_;
    
public:
    __attribute__((always_inline))
    void record(uint64_t latency_ns) {
        uint64_t bucket = latency_ns / 1000;  // Convert to microseconds
        if (bucket < BUCKETS) {
            histogram_[bucket].fetch_add(1, std::memory_order_relaxed);
        } else {
            overflow_.fetch_add(1, std::memory_order_relaxed);
        }
    }
    
    LatencyStats get_stats() const {
        uint64_t total = 0;
        uint64_t count = 0;
        uint64_t p50_bucket = 0, p99_bucket = 0, p999_bucket = 0;
        
        // Calculate percentiles
        for (size_t i = 0; i < BUCKETS; i++) {
            uint64_t bucket_count = histogram_[i].load(std::memory_order_relaxed);
            count += bucket_count;
            total += bucket_count * i;
        }
        
        uint64_t running = 0;
        for (size_t i = 0; i < BUCKETS; i++) {
            running += histogram_[i].load(std::memory_order_relaxed);
            if (p50_bucket == 0 && running >= count * 0.50) p50_bucket = i;
            if (p99_bucket == 0 && running >= count * 0.99) p99_bucket = i;
            if (p999_bucket == 0 && running >= count * 0.999) p999_bucket = i;
        }
        
        return {
            .mean_us = static_cast<double>(total) / count,
            .p50_us = p50_bucket,
            .p99_us = p99_bucket,
            .p999_us = p999_bucket,
            .count = count
        };
    }
};

// RDTSC for sub-nanosecond timing
__attribute__((always_inline))
inline uint64_t rdtsc() {
    uint32_t lo, hi;
    asm volatile("rdtsc" : "=a"(lo), "=d"(hi));
    return ((uint64_t)hi << 32) | lo;
}
```

## Mental Model

Citadel approaches low-latency systems by asking:

1. **What's the latency budget?** Allocate nanoseconds to each component
2. **Where are the syscalls?** Eliminate them from the hot path
3. **Where are the locks?** Replace with lock-free alternatives
4. **Where are the allocations?** Pre-allocate everything
5. **What's the worst case?** Optimize for tail latency, not average

## Signature Citadel Moves

- Kernel bypass with DPDK/OpenOnload
- Lock-free data structures everywhere
- CPU pinning and isolation
- Pre-allocated memory pools
- Busy-polling over blocking
- RDTSC for timing
- Cache-line alignment
- Disabled OS features (HT, C-states, THP)
- Assembly-level verification
- Nanosecond-precision measurement
