---
name: io-uring
description: 'Use when building Linux servers with liburing, batching SQEs, multi-shot operations, provided buffer rings, registered files and buffers, or zero-copy send. Not for packet I/O: use af-xdp.'
---

# io_uring

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Building or tuning Linux async I/O with io_uring: the SQE/CQE model, liburing usage, multi-shot accept or recv, provided buffer rings, fixed files and buffers, zero-copy send, tokio-uring, or the io_uring versus epoll decision. |
| Authority | Read-only. Writes nothing. Chat output only. No remote mutation. |
| Side effect | Returns setup code, ring lifecycle rules, and a comparison verdict. No source files are modified. |
| Done | The liburing example, the multi-shot and buffer-ring patterns, the zero-copy rule, and the epoll comparison verdict are delivered. |

## Inputs

1. Workload shape (required): network or disk, operation mix, and connection count.
2. Kernel (required): the running version, because io_uring features vary by version; base support starts at 5.1.
3. Language (optional): C with liburing, or Rust with tokio-uring.

## Procedure

1. State the queue model. Each SQE describes one operation. Each CQE reports a result and the `user_data` cookie that identifies the operation. `io_uring_submit()` pushes SQEs to the kernel; `io_uring_wait_cqe()` blocks for a completion. Done when: the SQE-to-CQE flow with the cookie rule is stated in the delivered guidance.
2. Show the minimal liburing loop as the reference shape.

   ```c
   #include <liburing.h>

   struct io_uring ring;
   io_uring_queue_init(32, &ring, 0);

   struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);
   io_uring_prep_read(sqe, fd, buf, sizeof(buf), 0);
   io_uring_sqe_set_data(sqe, (void *)1);
   io_uring_submit(&ring);

   struct io_uring_cqe *cqe;
   io_uring_wait_cqe(&ring, &cqe);
   if (cqe->res >= 0)
       handle(cqe->res);
   io_uring_cqe_seen(&ring, cqe);
   io_uring_queue_exit(&ring);
   ```

   Build with `-luring`. Done when: the example compiles against liburing and each CQE is consumed with `cqe_seen`.
3. Map the request to its prep function: `io_uring_prep_read`, `prep_write`, `prep_recv`, `prep_send`, `prep_accept`, `prep_connect`, `prep_poll_add`, `prep_timeout`. Batch many SQEs between submits; one submit amortizes the syscall cost over the batch. Done when: every operation in the workload has a prep function and a batching point.
4. Use multi-shot operations for connection-heavy paths. One `io_uring_prep_multishot_accept` SQE keeps producing completions until it reports completion of its own life.

   ```c
   io_uring_prep_multishot_accept(sqe, listen_fd, NULL, NULL, 0);
   io_uring_sqe_set_data(sqe, (void *)ACCEPT_COOKIE);

   io_uring_wait_cqe(&ring, &cqe);
   if (cqe->user_data == ACCEPT_COOKIE && cqe->res >= 0)
       handle_client(cqe->res);
   int more = cqe->flags & IORING_CQE_F_MORE;
   io_uring_cqe_seen(&ring, cqe);
   if (!more)
       rearm_accept(); /* the multishot SQE ended; submit a new one */
   ```

   Done when: the loop re-arms exactly when `IORING_CQE_F_MORE` is clear.
5. Use provided buffer rings for recv paths. The kernel picks a buffer from the ring, which removes the per-recv allocation.

   ```c
   #define BUF_SIZE  4096
   #define BUF_COUNT 64

   int ret;
   struct io_uring_buf_ring *buf_ring =
       io_uring_setup_buf_ring(&ring, BUF_COUNT, BUF_GROUP, 0, &ret);
   for (int i = 0; i < BUF_COUNT; i++)
       /* mask is ring size - 1; offset walks the slots */
       io_uring_buf_ring_add(buf_ring, bufs[i], BUF_SIZE, i, BUF_COUNT - 1, i);
   io_uring_buf_ring_advance(buf_ring, BUF_COUNT);

   sqe = io_uring_get_sqe(&ring);
   io_uring_prep_recv_multishot(sqe, sock_fd, NULL, 0, 0);
   sqe->buf_group = BUF_GROUP;
   ```

   Return each consumed buffer with `io_uring_buf_ring_add` before the next advance. Done when: every consumed buffer is re-added, and the recv carries the buffer group.
6. Register files and buffers on hot paths. Registered files avoid the per-operation fd table lookup; registered buffers are pinned and suited to `*_fixed` operations.

   ```c
   io_uring_register_files(&ring, fds, 64);
   io_uring_prep_read(sqe, 0, buf, size, offset); /* index into the table, not the fd */
   struct iovec iov = { .iov_base = buf, .iov_len = size };
   io_uring_register_buffers(&ring, &iov, 1);
   io_uring_prep_read_fixed(sqe, fd, buf, size, offset, 0);
   ```

   Done when: hot-path operations use fixed variants and the registered tables are updated on fd churn.
7. Use zero-copy send where available. `io_uring_prep_send_zc` needs kernel 6.0 or later and falls back to a normal send when the protocol or device does not support it. A zero-copy send posts a second notification CQE; treat `IORING_CQE_F_MORE` on the first CQE as the signal to wait for it. Done when: the send path handles the notification CQE and the fallback.
8. For Rust, show the tokio-uring shape: the runtime owns the ring and returns buffer ownership with the result.

   ```rust
   use tokio_uring::fs::File;

   #[tokio_uring::main]
   async fn main() -> std::io::Result<()> {
       let file = File::open("test.txt").await?;
       let buf = vec![0u8; 4096];
       let (res, buf) = file.read_at(buf, 0).await;
       println!("read {} bytes", res?);
       Ok(())
   }
   ```

   Done when: the Rust example compiles with the `tokio-uring` crate and buffer ownership flow is stated.
9. Deliver the epoll comparison as a verdict, not a table of absolutes.

   | Aspect | epoll | io_uring |
   |---|---|---|
   | Syscalls | One per operation plus `epoll_wait` | Batched SQEs, one submit |
   | Buffers | Application allocates per op | Provided buffer rings |
   | Zero-copy send | Manual | `SEND_ZC` built in |
   | Portability | Everywhere | 5.1+, feature-dependent |

   Choose io_uring when syscall overhead is measured, not assumed, and the kernel has the needed operations. Stay on epoll for simple services and portability. Probe support at runtime with `io_uring_get_probe()`. Done when: the verdict cites a measured syscall or batching cost.
10. State the security posture. Some distributions restrict io_uring by default because it has been an attack surface.

   ```bash
   sysctl kernel.io_uring_disabled
   # 0: all processes may create instances
   # 1: CAP_SYS_ADMIN or members of kernel.io_uring_group only
   # 2: creation off for everyone
   sysctl kernel.io_uring_group   # the gid allowed at level 1
   ```

   Existing instances keep working after a policy change. Keep the kernel patched and sandbox untrusted code. Done when: the deployment documents its io_uring policy and kernel version.

## Failure and recovery

| Symptom | Cause | Recovery |
|---|---|---|
| `-EINVAL` on prep | Operation unsupported on this kernel | Check `io_uring_get_probe()`; gate the code path on it. |
| Hang on `wait_cqe` | SQEs never submitted | Call `io_uring_submit` after preparing. |
| Buffer never returned | Consumed buffer not re-added | Re-add with `buf_ring_add` after consuming. |
| `SEND_ZC` result unclear | Notification CQE pending | Wait for the second CQE; `IORING_CQE_F_MORE` marks the pair. |
| Slower than epoll | Tiny batches | Batch more SQEs per submit; consider SQPOLL. |
| `-EPERM` on setup | io_uring restricted by sysctl | Align with the `kernel.io_uring_disabled` policy. |

## Output

The queue-model statement; the minimal liburing example; the prep-function mapping and batching plan; the multi-shot and buffer-ring code; the registration rules; the zero-copy send rule; the tokio-uring example; the epoll verdict with its measured basis; the security posture.
