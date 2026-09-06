---
name: dpdk
description: 'Use when initializing EAL, configuring PMD drivers and huge pages, using mbuf pools and rte_ring, setting up RSS, or validating a port with testpmd. Not for AF_XDP sockets: use af-xdp.'
---

# DPDK

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Building a userspace DPDK dataplane: EAL init, port and PMD setup, `rte_eth_rx_burst`/`tx_burst`, mbuf pools, `rte_ring`, RSS, testpmd validation, or virtio-under-QEMU testing. |
| Authority | Read-only. Writes nothing. Chat output only. No remote mutation. |
| Side effect | Returns setup commands, driver code, and a validation plan. No source files are modified. |
| Done | The hugepage and EAL setup, the port init and burst loop, the RSS configuration, and a testpmd validation run are delivered. |

## Inputs

1. Target NIC and driver (required): the PCI address, the current kernel driver, and the PMD that will own it.
2. Core and memory layout (optional): lcore list, memory channels, hugepage size. Defaults to one lcore per RX queue.
3. Test plan (optional): testpmd forward mode and traffic generator, when the request includes validation.

## Procedure

1. Set up hugepages before EAL starts. EAL maps hugepages at startup and fails when pages are short.

   ```bash
   echo 1024 | sudo tee /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
   # 1 GiB pages help TLB reach on large-memory boxes
   echo 4 | sudo tee /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages
   sudo mkdir -p /mnt/huge
   sudo mount -t hugetlbfs nodev /mnt/huge
   grep Huge /proc/meminfo
   ```

   Done when: `/proc/meminfo` reports the requested hugepage count.
2. Initialize EAL. `rte_eal_init` consumes its arguments and returns how many it took; the rest belong to the application.

   ```c
   int ret = rte_eal_init(argc, argv);
   if (ret < 0)
       rte_exit(EXIT_FAILURE, "EAL init failed\n");
   return run_dataplane(argc - ret, argv + ret);
   ```

   ```bash
   ./dpdk_app -l 0-3 -n 4 --huge-dir=/mnt/huge -- -p 0x3
   # -l: lcore list   -n: memory channels
   # --proc-type=primary   --file-prefix=pfx for a second instance
   ```

   Done when: the app starts with its lcore list and the argument split is respected.
3. Bind the NIC to a PMD and configure the port. Physical NICs need `vfio-pci` (with IOMMU) or a `uio` driver.

   ```bash
   sudo dpdk-devbind.py --status
   sudo modprobe vfio-pci
   sudo dpdk-devbind.py --bind=vfio-pci 0000:03:00.0
   ```

   ```c
   #define RX_RING_SIZE 1024
   #define TX_RING_SIZE 1024
   #define NUM_MBUFS    8191
   #define MBUF_CACHE   250

   mbuf_pool = rte_pktmbuf_pool_create("MBUF_POOL", NUM_MBUFS, MBUF_CACHE,
                                       0, RTE_MBUF_DEFAULT_BUF_SIZE,
                                       rte_socket_id());
   struct rte_eth_dev_info dev_info;
   rte_eth_dev_info_get(port, &dev_info);
   struct rte_eth_rxconf rxq_conf = dev_info.default_rxconf;
   rte_eth_rx_queue_setup(port, 0, RX_RING_SIZE,
                          rte_eth_dev_socket_id(port), &rxq_conf, mbuf_pool);
   rte_eth_tx_queue_setup(port, 0, TX_RING_SIZE,
                          rte_eth_dev_socket_id(port), &dev_info.default_txconf, mbuf_pool);
   rte_eth_dev_start(port);
   rte_eth_promiscuous_enable(port);
   ```

   Done when: the port starts and `dpdk-devbind.py --status` shows the PMD bound.
4. Write the burst loop. Poll mode has no interrupts; cores spin. Assign one core per RX queue.

   ```c
   struct rte_mbuf *bufs[BURST_SIZE];
   uint16_t nb_rx = rte_eth_rx_burst(port, 0, bufs, BURST_SIZE);
   if (nb_rx == 0)
       return;
   uint16_t nb_tx = rte_eth_tx_burst(port, 0, bufs, nb_rx);
   /* return unsent mbufs to the pool or they leak */
   for (uint16_t i = nb_tx; i < nb_rx; i++)
       rte_pktmbuf_free(bufs[i]);
   ```

   Done when: every received mbuf is either transmitted or freed.
5. Use `rte_ring` for inter-core handoff. Single-producer/single-consumer flags buy lock-free speed when the topology allows them.

   ```c
   struct rte_ring *ring = rte_ring_create("RX_RING", 1024, rte_socket_id(),
                                           RING_F_SP_ENQ | RING_F_SC_DEQ);
   rte_ring_enqueue_bulk(ring, (void **)bufs, nb_rx, NULL);
   uint16_t nb = rte_ring_dequeue_bulk(ring, (void **)bufs, BURST_SIZE, NULL);
   ```

   Done when: each ring has one producer and one consumer matching the flags.
6. Configure RSS when flows must spread over queues. Map queues to cores for parallelism.

   ```c
   static const struct rte_eth_rss_conf rss_conf = {
       .rss_key = NULL, /* default hash key */
       .rss_hf = RTE_ETH_RSS_IP | RTE_ETH_RSS_TCP | RTE_ETH_RSS_UDP,
   };
   struct rte_eth_conf port_conf = {
       .rxmode = { .mq_mode = RTE_ETH_MQ_RX_RSS },
       .rx_adv_conf = { .rss_conf = rss_conf },
   };
   ```

   Done when: the receive-side table shows flows spread across the configured queues.
7. Validate with testpmd before custom code.

   ```bash
   ninja -C build dpdk-testpmd
   sudo ./build/app/dpdk-testpmd -l 0-3 -n 4 -- -i --forward-mode=io
   testpmd> show port stats all
   testpmd> start tx_first
   testpmd> show port stats all
   ```

   Forward modes `io`, `mac`, `macswap`, and `flowgen` serve throughput checks. Done when: both port counters advance at the expected rate.
8. For development under QEMU, present a multi-queue virtio device backed by hugepages.

   ```bash
   qemu-system-x86_64 -cpu host -m 4096 -smp 4 \
     -netdev user,id=net0 \
     -device virtio-net-pci,netdev=net0,mq=on,vectors=10 \
     -object memory-backend-file,id=mem,size=2G,mem-path=/dev/hugepages,share=on \
     -numa node,memdev=mem
   ```

   Inside the guest, bind the virtio PCI address to `vfio-pci`; `vhost-user` is the higher-throughput path. Route the host side: `qemu-kvm` for QEMU management. Done when: the guest sees the PMD and testpmd runs in it.
9. Pick the processing model from the per-packet work. Run-to-completion keeps RX, process, and TX on one core, which is the low-latency shape for simple logic. A pipeline (RX core, worker cores over rings, TX core) scales further for heavy per-packet work at the cost of ring hops. Done when: the recommendation names the per-packet work and the core budget.

## Failure and recovery

| Symptom | Cause | Recovery |
|---|---|---|
| EAL init fails on hugepages | Pages absent or hugetlbfs unmounted | Raise `nr_hugepages`; mount hugetlbfs. |
| `No probed ethernet devices` | NIC not bound to a PMD | `dpdk-devbind.py --bind=vfio-pci <addr>`. |
| RX drops climbing | Mbuf pool exhausted | Grow `NUM_MBUFS`; audit for unfreed mbufs. |
| 0 Mbps in testpmd | Port not started or link down | `start` in the testpmd shell; check link status. |
| VFIO permission error | No IOMMU group access | Enable IOMMU; fix group ownership. |
| Poor multi-core scaling | RSS off or too few queues | Enable RSS and add RX queues mapped to cores. |

## Output

Hugepage and EAL setup commands; port init code with the PMD binding; a burst loop that frees unsent mbufs; the ring and RSS configuration; a testpmd validation transcript; the QEMU development recipe; the processing-model choice.
