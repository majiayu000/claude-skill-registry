---
name: af-xdp
description: 'Use when creating AF_XDP sockets, configuring UMEM and XSK rings, writing an XDP redirect program, or choosing copy versus zero-copy mode. Not for full kernel bypass: use dpdk.'
---

# AF_XDP sockets

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Building a userspace packet path on AF_XDP: UMEM and ring setup, an XDP redirect program, the RX loop, copy versus zero-copy mode, or an AF_XDP versus DPDK decision. |
| Authority | Read-only. Writes nothing. Chat output only. No remote mutation. |
| Side effect | Returns setup code, ring lifecycle rules, and a mode recommendation. No source files are modified. |
| Done | The socket setup code, the fill-ring refill rule, the redirect program, and a mode choice tied to driver support are delivered. |

## Inputs

1. Interface and queue (required): the interface name and the RX queue the socket serves. One socket per queue.
2. Mode intent (optional): copy or zero-copy. Default to copy and confirm from the bind.
3. Build setup (optional): libbpf installed (`pkg-config --libs libbpf` returns `-lbpf`; `-lxdp` when libxdp is installed separately).

## Procedure

1. Lay out the object model before writing code. UMEM is the shared frame pool. The fill ring carries empty frame addresses from user space to the kernel. The completion ring returns transmitted frames. The RX ring delivers received packets. The TX ring carries outgoing packets. Done when: each ring and the UMEM has a named struct in the design.
2. Create the UMEM and the socket.

   ```c
   #include <bpf/xsk.h>

   #define NUM_FRAMES    4096
   #define FRAME_SIZE    XSK_UMEM__DEFAULT_FRAME_SIZE
   #define RX_BATCH_SIZE 64

   /* mmap one anonymous region; the UMEM describes it to the kernel */
   void *buffer = mmap(NULL, NUM_FRAMES * FRAME_SIZE,
                       PROT_READ | PROT_WRITE,
                       MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

   struct xsk_umem_config umem_cfg = {
       .fill_size = XSK_RING_PROD__DEFAULT_NUM_DESCS,
       .comp_size = XSK_RING_CONS__DEFAULT_NUM_DESCS,
       .frame_size = FRAME_SIZE,
       .frame_headroom = XSK_UMEM__DEFAULT_FRAME_HEADROOM,
       .flags = 0,
   };
   int ret = xsk_umem__create(&umem->umem, buffer, NUM_FRAMES * FRAME_SIZE,
                              &umem->fill, &umem->comp, &umem_cfg);

   struct xsk_socket_config xsk_cfg = {
       .rx_size = XSK_RING_CONS__DEFAULT_NUM_DESCS,
       .tx_size = XSK_RING_PROD__DEFAULT_NUM_DESCS,
       /* the skill loads its own program in step 4, so stop libbpf */
       .libbpf_flags = XSK_LIBBPF_FLAGS__INHIBIT_PROG_LOAD,
       .xdp_flags = XDP_FLAGS_UPDATE_IF_NOEXIST,
       .bind_flags = XDP_COPY, /* or XDP_ZEROCOPY, see step 6 */
   };
   ret = xsk_socket__create(&xsk->xsk, ifname, queue_id, umem->umem,
                            &xsk->rx, &xsk->tx, &xsk_cfg);
   ```

   Done when: the UMEM covers the whole mmap region and each ring struct is wired into its create call.
3. Keep the fill ring stocked. The kernel drops received packets when the fill ring holds no free frames. Reserve, fill frame offsets, submit.

   ```c
   uint32_t idx;
   uint32_t n = xsk_ring_prod__reserve(&umem->fill, RX_BATCH_SIZE, &idx);
   for (uint32_t i = 0; i < n; i++)
       *xsk_ring_prod__fill_addr(&umem->fill, idx + i) = i * FRAME_SIZE;
   xsk_ring_prod__submit(&umem->fill, n);
   ```

   Done when: the refill runs after every consumed RX batch, not only at startup.
4. Load an XDP program that redirects to the socket. A `BPF_MAP_TYPE_XSKMAP` maps queue index to socket fd.

   ```c
   #include <linux/bpf.h>
   #include <bpf/bpf_helpers.h>

   struct {
       __uint(type, BPF_MAP_TYPE_XSKMAP);
       __uint(max_entries, 64);
       __type(key, int);
       __type(value, int);
   } xsks_map SEC(".maps");

   SEC("xdp")
   int xdp_redirect_prog(struct xdp_md *ctx)
   {
       return bpf_redirect_map(&xsks_map, ctx->rx_queue_index, 0);
   }
   ```

   ```bash
   ip link set dev eth0 xdp obj xdp_redirect.o sec xdp
   # hand the socket fd to the map for this queue
   ```

   Done when: the program is attached and the map holds `xsk_socket__fd(xsk)` at this queue's index.
5. Run the RX loop. Peek a batch, resolve each descriptor to a packet pointer, release, refill.

   ```c
   uint32_t idx_rx, rcvd;
   rcvd = xsk_ring_cons__peek(&xsk->rx, RX_BATCH_SIZE, &idx_rx);
   for (uint32_t i = 0; i < rcvd; i++) {
       const struct xdp_desc *d = xsk_ring_cons__rx_desc(&xsk->rx, idx_rx + i);
       uint8_t *pkt = xsk_umem__get_data(buffer, d->addr);
       process_packet(pkt, d->len);
   }
   xsk_ring_cons__release(&xsk->rx, rcvd);
   refill_fill_ring(umem, rcvd);
   ```

   Done when: every peeked batch is released and refilled, and the loop drains the completion ring for TX frame reuse.
6. Choose copy versus zero-copy.

   | Mode | Bind flag | Driver requirement |
   |---|---|---|
   | Copy | `XDP_COPY` (default) | Any driver; the kernel copies into UMEM frames. |
   | Zero-copy | `XDP_ZEROCOPY` | Driver support: `i40e`, `ixgbe`, `mlx5`, `ice` and others. |

   Check support with `ethtool -i eth0` and read the bind result in `dmesg` (`dmesg | grep xsk`). The bind falls back to copy mode when the driver lacks support. Zero-copy lets the NIC DMA straight into UMEM frames, which is the low-latency path; copy mode works everywhere at a copy cost. Done when: the chosen mode matches confirmed driver support.
7. Decide AF_XDP versus DPDK for the workload.

   | Factor | AF_XDP | DPDK |
   |---|---|---|
   | Setup | Moderate | High (hugepages, EAL) |
   | Kernel integration | XDP filter stays in kernel | Full bypass |
   | Throughput | Close to DPDK in zero-copy mode, NIC and driver dependent | Highest |
   | NIC binding | Stays on the kernel driver | Bound to `vfio-pci` or `uio` |
   | Fit | Filter in kernel, selective traffic to user space | Full dataplane takeover |

   Throughput depends on NIC, driver, and CPU. No fixed number transfers between boards; measure with the real workload. Done when: the recommendation names the workload and the measured or expected traffic mix.
8. Apply production rules. Run one socket per RX queue, pinned with `taskset` to the CPU that handles that queue's interrupts. AF_XDP needs `CAP_NET_RAW`. Route deeper work: `ebpf` for XDP program development, `ebpf-rust` for XDP in Rust, `dpdk` for full bypass. Done when: queue pinning, capability, and routing are stated in the delivered guidance.

## Failure and recovery

| Symptom | Cause | Recovery |
|---|---|---|
| RX ring stays empty | Redirect program missing or map entry unset | Verify the map entry for this queue index and that the program is attached. |
| `EBUSY` on socket create | An XDP program is already attached | Detach with `ip link set dev eth0 xdp off`, then bind. |
| Zero-copy bind silently falls back | Driver lacks support | Read `dmesg`; use a supported driver or accept copy mode. |
| Packet drops under load | Fill ring empty at packet arrival | Refill after each batch; grow `NUM_FRAMES`. |
| TX stops | Completion ring never drained | Poll the completion ring to recycle transmitted frames. |
| Permission denied | `CAP_NET_RAW` missing | Run with the capability. |

## Output

Setup code for UMEM, socket, and rings; the refill rule with its drop hazard; the redirect program and attach commands; the mode choice with driver evidence; the AF_XDP versus DPDK recommendation; the production checklist.
