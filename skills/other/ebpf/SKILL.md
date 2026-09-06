---
name: ebpf
description: 'Use when writing eBPF programs with libbpf or bpftrace, attaching kprobes, tracepoints, or XDP hooks, triaging verifier errors, choosing maps, or porting with CO-RE. Not for Rust: use ebpf-rust.'
---

# eBPF

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A kernel event needs tracing, a libbpf program needs writing or loading, the verifier rejects a program, kernel and user space need to share data, or an XDP filter needs attaching. |
| Authority | Reversible local. The write set is the user's source and object files, programs and maps loaded into the running kernel, pins under `/sys/fs/bpf`, and XDP attachments on a named interface. Rollback is detaching the program, unpinning, and `ip link set dev <if> xdp off`. Loading needs `CAP_BPF` or root. No remote mutation. |
| Side effect | Kernel state changes while a program is loaded. Every load in this skill is paired with its detach. |
| Done | The program loads, attaches, and produces output for the traced event, or the verifier error is mapped to its cause and the fix is applied. |

## Inputs

- Goal (required): a one-off trace, a production program with a user-space side, an inspection of loaded objects, or packet processing.
- Kernel (required): the running kernel must expose BTF at `/sys/kernel/btf/vmlinux` for CO-RE. The grounded floor is Linux 7.2 mainline or the 6.18 LTS line; every kernel feature named below exists in both.
- Toolchain (required for libbpf work): `clang` with the `bpf` target, `bpftool`, and libbpf 1.x with its headers.

## Procedure

1. Pick the tool by goal. A one-line trace or a script is `bpftrace`. A production program with a loader is libbpf in C (or aya in Rust, see `ebpf-rust`). Inspecting loaded programs and maps is `bpftool`. High-rate packet processing is XDP with libbpf. Done when: one tool is chosen.
2. For a quick trace, write the `bpftrace` one-liner and confirm the probe exists. Done when: the probe prints for a live event.

```bash
bpftrace -l 'tracepoint:syscalls:*'                 # list probes
bpftrace -l 'kprobe:tcp_*'
bpftrace -e 'tracepoint:syscalls:sys_enter_execve { printf("%s %s\n", comm, str(args->filename)); }'
bpftrace -e 'tracepoint:raw_syscalls:sys_enter { @[comm] = count(); }'
bpftrace -e '
  tracepoint:syscalls:sys_enter_read { @start[tid] = nsecs; }
  tracepoint:syscalls:sys_exit_read  { @us = hist((nsecs - @start[tid]) / 1000); delete(@start[tid]); }'
```

3. For a libbpf program, write the kernel side, generate the skeleton, and write the loader. Done when: the loader attaches and the map fills.

```c
/* counter.bpf.c: count read() calls per process. */
#include <vmlinux.h>
#include <bpf/bpf_helpers.h>

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __type(key, u32);
    __type(value, u64);
    __uint(max_entries, 1024);
} call_count SEC(".maps");

SEC("tracepoint/syscalls/sys_enter_read")
int trace_read(struct trace_event_raw_sys_enter *ctx)
{
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    u64 *cnt = bpf_map_lookup_elem(&call_count, &pid);
    if (cnt) {
        __sync_fetch_and_add(cnt, 1);
    } else {
        u64 one = 1;
        bpf_map_update_elem(&call_count, &pid, &one, BPF_ANY);
    }
    return 0;
}

char LICENSE[] SEC("license") = "GPL";
```

```c
/* counter.c: open, load, attach, read, destroy. */
#include "counter.skel.h"

int main(void)
{
    struct counter_bpf *skel = counter_bpf__open();
    if (!skel || counter_bpf__load(skel))
        return 1;
    if (counter_bpf__attach(skel))
        return 1;
    /* read call_count through bpf_map__fd(skel->maps.call_count) */
    counter_bpf__destroy(skel);
    return 0;
}
```

```bash
bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h
clang -g -O2 -target bpf -D__TARGET_ARCH_x86 -c counter.bpf.c -o counter.bpf.o
bpftool gen skeleton counter.bpf.o > counter.skel.h
gcc -o counter counter.c -lbpf -lelf -lz
```

The skeleton's `open`, `load`, `attach`, and `destroy` functions replace the older `bpf_object__open_file` and `bpf_object__load` split, which still exist for loading an object by path.

4. Choose the map. Use a hash map for per-key state, an array for fixed-index config, a per-CPU map for a hot counter that must not lock, an LRU hash for bounded connection tracking, a program array for tail calls, and a ring buffer for kernel-to-user events. Prefer `BPF_MAP_TYPE_RINGBUF` over `BPF_MAP_TYPE_PERF_EVENT_ARRAY` for new code: one shared buffer, ordering across CPUs, variable-size records, and a reserve that fails instead of dropping. The full type table, operations, and pinning live in `references/ebpf-map-types.md`. Done when: the map type and its `max_entries` are chosen.

```c
struct {
    __uint(type, BPF_MAP_TYPE_RINGBUF);
    __uint(max_entries, 256 * 1024);
} rb SEC(".maps");

SEC("kprobe/do_sys_openat2")
int handle_open(struct pt_regs *ctx)
{
    struct event *e = bpf_ringbuf_reserve(&rb, sizeof(*e), 0);
    if (!e)
        return 0;
    e->pid = bpf_get_current_pid_tgid() >> 32;
    bpf_ringbuf_submit(e, 0);   /* bpf_ringbuf_discard(e, 0) on an error path */
    return 0;
}
```

User space consumes with `ring_buffer__poll`; the perf buffer equivalent is `perf_buffer__poll` over `bpf_perf_event_output`.

5. Triage a verifier rejection. Load with `bpftool` to see the full log, then map the message. Done when: the message has a cause and the program passes.

```bash
bpftool prog load prog.bpf.o /sys/fs/bpf/prog type kprobe 2>&1 | head -100
bpftool prog list
bpftool prog dump xlated id 42
```

| Verifier message | Cause | Fix |
|---|---|---|
| `invalid mem access 'scalar'` | Dereference of a pointer the verifier could not bound | Null-check the pointer before use |
| `R0 !read_ok` | A path returns without setting `R0` | Return a value on every path |
| `jump out of range` | Branch target beyond the program | Restructure the conditional |
| `back-edge detected` | A loop the verifier cannot bound | Bound the loop with a constant, or use `bpf_loop()` (kernel 5.17 and later; present on the grounded floor) |
| `unreachable insn` | Dead code after a return | Remove the dead branch |
| `invalid indirect read` | Stack bytes read before being written | Zero-initialize the struct: `struct foo x = {};` |
| `misaligned stack access` | Pointer arithmetic off alignment | Align reads to `__u64` |

6. For packet filtering, write an XDP program and attach it in driver mode where the NIC supports it. Done when: the program is attached and the interface shows it, and the detach command is recorded.

```c
#include <vmlinux.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>

SEC("xdp")
int xdp_filter(struct xdp_md *ctx)
{
    void *data_end = (void *)(long)ctx->data_end;
    void *data = (void *)(long)ctx->data;
    struct ethhdr *eth = data;

    if ((void *)(eth + 1) > data_end)
        return XDP_PASS;
    if (bpf_ntohs(eth->h_proto) != ETH_P_IP)
        return XDP_PASS;

    struct iphdr *ip = (void *)(eth + 1);
    if ((void *)(ip + 1) > data_end)
        return XDP_PASS;
    if (ip->protocol == IPPROTO_ICMP)
        return XDP_DROP;
    return XDP_PASS;
}
char LICENSE[] SEC("license") = "GPL";
```

```bash
ip link set dev eth0 xdpdrv object xdp_drop_icmp.bpf.o section xdp   # driver mode
ip link set dev eth0 xdpgeneric object prog.bpf.o section xdp        # fallback when the driver lacks XDP
ip link set dev eth0 xdp off                                          # detach
```

Return codes are `XDP_PASS`, `XDP_DROP`, `XDP_TX` (send back out the same port), and `XDP_REDIRECT`. For redirecting into AF_XDP sockets, use `af-xdp`; for a full kernel bypass, use `dpdk`.

7. Make the program portable with CO-RE. Include `vmlinux.h` generated from the build host's BTF and read kernel struct fields through `BPF_CORE_READ`, which libbpf relocates to the running kernel's field offsets at load time. Done when: the same object loads on a second kernel version.

```c
#include <vmlinux.h>
#include <bpf/bpf_core_read.h>

SEC("kprobe/tcp_connect")
int trace_connect(struct pt_regs *ctx)
{
    struct sock *sk = (struct sock *)PT_REGS_PARM1(ctx);
    u16 dport = BPF_CORE_READ(sk, __sk_common.skc_dport);
    bpf_printk("connect to port %d\n", bpf_ntohs(dport));
    return 0;
}
```

8. Reach for iterators and atomics when the simple form is too slow. An `SEC("iter/task")` program walks every task once through `bpf_seq_printf` without a probe firing per element; read its output with `bpftool prog tracelog` or the seq file the loader creates. For a counter updated by concurrent probes, use a per-CPU array and sum in user space; when a single shared value is required, increment it with `__sync_fetch_and_add`. The full BPF atomic set (fetch-and-add with a returned value, and, or, xor, exchange, compare-exchange) is available from kernel 5.12; plain add-without-return predates it. Both are on the grounded floor. Done when: the hot path uses per-CPU storage or an atomic, not a plain read-modify-write.

For seccomp filtering, use `kernel-security`. For module development that a probe targets, use `linux-kernel-modules`.

## Failure and recovery

| Failure class | Behavior |
|---|---|
| `/sys/kernel/btf/vmlinux` missing | The kernel lacks `CONFIG_DEBUG_INFO_BTF`. CO-RE cannot work; report it and fall back to a kernel with BTF. |
| `Permission denied` on load | The process lacks `CAP_BPF` (or `CAP_SYS_ADMIN` for some program types). Run as root or grant the capability; do not weaken `kernel.unprivileged_bpf_disabled`. |
| Verifier rejects the program | Map the message with the table in step 5. Fix the program; do not shrink `max_entries` or remove checks to make it pass. |
| XDP attach fails in driver mode | The driver lacks native XDP. Attach with `xdpgeneric` and note the throughput cost. |
| Ring buffer reserve returns null | The buffer is full. Enlarge `max_entries` or drain faster in user space; count the drops. |
| Map already pinned | A previous run left a pin under `/sys/fs/bpf`. Reuse it or unpin it before reloading. |

## Output

The program source, the build and load commands, the attach and detach pair, and either the traced output or the verifier message mapped to its fix. Every kernel-side object the run leaves behind is listed with its removal command.
