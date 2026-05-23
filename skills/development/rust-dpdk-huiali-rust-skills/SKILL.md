---
name: rust-dpdk
description: "用户态网络专家。处理 DPDK, 用户态驱动, 高性能网络, packet processing, 零拷贝, RSS 负载均衡"
globs: ["**/*.rs"]
---

# 用户态网络 (DPDK)

## 核心问题

**如何实现百万级 PPS 的高性能网络数据包处理？**

传统内核网络栈有太多上下文切换和内存拷贝开销。

---

## DPDK vs 内核网络栈

| 特性 | 内核网络栈 | DPDK |
|-----|----------|------|
| 上下文切换 | 每次包都切换 | 轮询模式，无切换 |
| 内存拷贝 | 多次拷贝 | 零拷贝 |
| 中断 | 频繁中断 | 轮询 (poll mode driver) |
| 延迟 | 较高 | 微秒级 |
| 吞吐量 | 万级 PPS | 百万级 PPS |
| CPU 利用率 | 较低但有开销 | 高但高效 |

---

## 核心组件

```rust
// DPDK 核心结构
struct DpdkContext {
    memory_pool: Mempool,        // 内存池
    ports: Vec<Port>,            // 网卡端口
    rx_queues: Vec<RxQueue>,     // 接收队列
    tx_queues: Vec<TxQueue>,     // 发送队列
    cpu_cores: Vec<Core>,        // CPU 核心分配
}

struct Port {
    port_id: u16,
    mac_addr: [u8; 6],
    link_speed: u32,
    max_queues: u16,
}

struct Mempool {
    name: String,
    buffer_size: usize,
    cache_size: usize,
    total_buffers: u32,
}
```

---

## 内存池管理

```rust
// 创建 DPDK 内存池
fn create_mempool() -> Result<Mempool, DpdkError> {
    let mempool = unsafe {
        rte_mempool_create(
            b"packet_pool\0".as_ptr() as *const c_char,
            NUM_BUFFERS as u32,        // 缓冲区数量
            BUFFER_SIZE as u16,        // 每个缓冲区大小
            CACHE_SIZE as u32,         // CPU 缓存大小
            0,                         // 私有数据大小
            Some(rte_pktmbuf_pool_init), // 初始化函数
            std::ptr::null(),          // 初始化参数
            Some(rte_pktmbuf_init),    // 对象初始化函数
            std::ptr::null(),          // 对象参数
            rte_socket_id() as i32,    // 内存所在 Socket
            0,                         // 标志位
        )
    };
    
    if mempool.is_null() {
        Err(DpdkError::MempoolCreateFailed)
    } else {
        Ok(Mempool { inner: mempool })
    }
}

// 分配缓冲区
fn alloc_mbuf(mempool: &Mempool) -> Option<*mut rte_mbuf> {
    unsafe {
        let mbuf = rte_pktmbuf_alloc(mempool.inner);
        if mbuf.is_null() {
            None
        } else {
            Some(mbuf)
        }
    }
}
```

---

## 零拷贝接收

```rust
// 零拷贝接收数据包
fn process_packets(
    port_id: u16,
    queue_id: u16,
    bufs: &mut [*mut rte_mbuf; MAX_BURST_SIZE],
) -> usize {
    let num_received = unsafe {
        rte_eth_rx_burst(
            port_id,
            queue_id,
            bufs.as_mut_ptr(),
            MAX_BURST_SIZE as u16,
        )
    };
    
    // 直接处理 mbuf，不需要拷贝
    for i in 0..num_received {
        let mbuf = bufs[i];
        
        // 访问数据（零拷贝）
        let data_ptr = unsafe {
            rte_pktmbuf_mtod(mbuf, *const u8)
        };
        let data_len = unsafe {
            rte_pktmbuf_pkt_len(mbuf)
        };
        
        // 处理数据包
        process_packet(data_ptr, data_len);
        
        // 释放 mbuf 回内存池
        unsafe {
            rte_pktmbuf_free(mbuf);
        }
    }
    
    num_received
}
```

---

## 批量发送

```rust
// 批量发送数据包
fn transmit_packets(
    port_id: u16,
    queue_id: u16,
    packets: &[Packet],
) -> usize {
    let mut mbufs: Vec<*mut rte_mbuf> = packets
        .iter()
        .map(|p| p.to_mbuf())
        .collect();
    
    let sent = unsafe {
        rte_eth_tx_burst(
            port_id,
            queue_id,
            mbufs.as_mut_ptr(),
            mbufs.len() as u16,
        )
    };
    
    // 释放未发送的 mbuf
    for i in sent..mbufs.len() {
        unsafe {
            rte_pktmbuf_free(mbufs[i]);
        }
    }
    
    sent
}
```

---

## RSS 负载均衡

```rust
// 配置 RSS (Receive Side Scaling)
fn configure_rss(port_id: u16) -> Result<(), DpdkError> {
    let mut port_info: rte_eth_dev_info = unsafe { std::mem::zeroed() };
    unsafe {
        rte_eth_dev_info_get(port_id, &mut port_info);
    }
    
    // 配置 RSS 哈希
    let mut rss_conf: rte_eth_rss_conf = unsafe { std::mem::zeroed() };
    rss_conf.rss_key_len = 40;
    rss_conf.rss_hf = RTE_ETH_RSS_TCP | RTE_ETH_RSS_UDP | RTE_ETH_RSS_IPV4;
    
    unsafe {
        let ret = rte_eth_dev_rss_hash_conf_update(
            port_id,
            &rss_conf,
        );
        if ret < 0 {
            return Err(DpdkError::RssConfigFailed);
        }
    }
    
    Ok(())
}

// 根据哈希值分配队列
fn get_queue_by_hash(hash: u32, num_queues: u16) -> u16 {
    // 使用简单的取模分发
    (hash % num_queues as u32) as u16
}
```

---

## 多队列配置

```rust
// 配置多队列
fn configure_multi_queue(port_id: u16, num_queues: u16) -> Result<(), DpdkError> {
    let mut port_conf: rte_eth_conf = unsafe { std::mem::zeroed() };
    port_conf.rxmode.split_hdr_size = 0;
    port_conf.rxmode.mq_mode = rte_eth_mq_mode::ETH_MQ_RX_RSS;
    port_conf.txmode.mq_mode = rte_eth_mq_mode::ETH_MQ_TX_NONE;
    
    // 配置 RX 队列
    let mut rx_conf: rte_eth_rxconf = unsafe { std::mem::zeroed() };
    rx_conf.rx_free_thresh = 32;
    rx_conf.rx_drop_en = 0;
    
    // 配置 TX 队列
    let mut tx_conf: rte_eth_txconf = unsafe { std::mem::zeroed() };
    tx_conf.tx_free_thresh = 32;
    
    // 分配 RX 队列
    for queue in 0..num_queues {
        unsafe {
            let ret = rte_eth_rx_queue_setup(
                port_id,
                queue,
                1024, // 队列深度
                rte_socket_id() as u32,
                &rx_conf,
                mempool.inner,
            );
            if ret < 0 {
                return Err(DpdkError::QueueSetupFailed);
            }
        }
    }
    
    // 分配 TX 队列
    for queue in 0..num_queues {
        unsafe {
            let ret = rte_eth_tx_queue_setup(
                port_id,
                queue,
                1024,
                rte_socket_id() as u32,
                &tx_conf,
            );
            if ret < 0 {
                return Err(DpdkError::QueueSetupFailed);
            }
        }
    }
    
    Ok(())
}
```

---

## CPU 亲和性

```rust
use std::os::raw::c_int;
use std::thread;

fn set_cpu_affinity(core_id: u32) -> Result<(), DpdkError> {
    let mut cpuset: cpu_set_t = unsafe { std::mem::zeroed() };
    
    unsafe {
        CPU_SET(core_id as usize, &mut cpuset);
        
        let ret = pthread_setaffinity_np(
            pthread_self(),
            std::mem::size_of::<cpu_set_t>(),
            &cpuset,
        );
        
        if ret != 0 {
            return Err(DpdkError::AffinitySetFailed);
        }
    }
    
    Ok(())
}

// 为每个 RX 队列分配专用核心
fn allocate_cores_for_queues(num_queues: u16) {
    for queue in 0..num_queues {
        thread::spawn(move || {
            set_cpu_affinity(queue as u32).unwrap();
            process_queue(queue);
        });
    }
}
```

---

## 性能优化

| 优化点 | 方法 |
|-------|------|
| 内存对齐 | 缓存行对齐 (64 字节) |
| 无锁队列 | 使用 SPSC 队列 |
| 批处理 | 批量收发减少系统调用 |
| CPU 亲和性 | 核心绑定减少上下文切换 |
| Hugepages | 2MB/1GB 大页减少 TLB miss |

---

## 与其他技能关联

```
rust-dpdk
    │
    ├─► rust-performance → 性能优化
    ├─► rust-embedded → no_std 环境
    └─► rust-concurrency → 并发模型
```

