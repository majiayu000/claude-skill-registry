---
name: mpi
description: 'Use when writing or debugging MPI programs: sends and receives, collectives, non-blocking requests, communicators, MPI-IO, hybrids with OpenMP, or mpirun launches. Not for threads alone: use openmp.'
---

# MPI

MPI is the message-passing standard for distributed-memory parallel programs: one process per rank, explicit sends, receives, and collectives over a communicator. The commands below are exercised against Open MPI 5.0.10, the implementation on the grounding host; MPICH and vendor MPIs accept the same API and a different `mpirun` option set.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user parallelizes across nodes or sockets, implements a distributed algorithm, combines ranks with OpenMP threads, runs under a scheduler, debugs a hang or a truncation error, or needs parallel file output. |
| Authority | Reversible local: writes only MPI source files, compiled binaries, hostfiles, and output data files in the working directory; rollback is deleting them. Scheduler submissions and remote launches are proposed to the user. No remote mutation. |
| Side effect | Source, binaries, and data files on disk. `mpirun` on the local host starts one process per rank. |
| Done | The program compiles with `mpicc`, runs under `mpirun -np N` with the expected output on every rank, every send has a matching receive, every non-blocking request is completed, and the scaling issue named in the request has a cause and a fix. |

## Inputs

- MPI implementation: `mpicc --version` and `mpirun --version` name it. `mpicc` wraps the C compiler with the include and link flags.
- Rank count and placement: cores per node, sockets, and whether OpenMP threads share a rank.
- For multi-node runs: a hostfile (`node0 slots=4`) or a scheduler allocation (`SLURM_NTASKS`).
- The failing symptom, when debugging: hang, wrong result, `MPI_ERR_TRUNCATE`, or poor scaling.

## Procedure

1. Start from the minimal program and prove the launch path:

   ```c
   #include <mpi.h>
   #include <stdio.h>

   int main(int argc, char **argv) {
       MPI_Init(&argc, &argv);
       int rank, size;
       MPI_Comm_rank(MPI_COMM_WORLD, &rank);
       MPI_Comm_size(MPI_COMM_WORLD, &size);
       printf("rank %d of %d\n", rank, size);
       MPI_Finalize();
       return 0;
   }
   ```

   `mpicc -O2 -o hello hello.c` then `mpirun -np 4 ./hello` (`mpiexec -n 4 ./hello` is the standard's spelling). On a laptop with fewer cores than ranks add `--oversubscribe`. Done when: every rank prints once.
2. Point-to-point. `MPI_Send(buf, count, MPI_INT, dest, tag, comm)` pairs with `MPI_Recv(buf, count, MPI_INT, source, tag, comm, MPI_STATUS_IGNORE)`; a receive matches on communicator, source, and tag, and `MPI_ANY_SOURCE` or `MPI_ANY_TAG` widen it. A receive count smaller than the incoming message raises `MPI_ERR_TRUNCATE`; larger is fine and `MPI_Get_count` on the status reports the real length. Done when: every send has a receive with the same communicator, tag, and datatype, and the receive buffer is at least as large.
3. Collectives instead of hand-rolled loops:

   | Call | Purpose |
   |---|---|
   | `MPI_Bcast` | One rank's buffer to all |
   | `MPI_Scatter`, `MPI_Gather` | Split a root buffer into chunks, or collect chunks |
   | `MPI_Allreduce(&local, &global, 1, MPI_INT, MPI_SUM, comm)` | Reduce and deliver the result to every rank |
   | `MPI_Reduce` | Reduce to the root only |
   | `MPI_Alltoall` | Every rank sends a chunk to every rank |
   | `MPI_Barrier` | Synchronize; use it for timing, not for correctness |

   Every rank in the communicator must call the collective with matching datatype and count. Done when: no collective is emulated with sends and receives, and the datatypes match on all ranks.
4. Overlap communication with computation using non-blocking requests. `MPI_Isend` and `MPI_Irecv` return an `MPI_Request`; do local work; then `MPI_Wait(&req, MPI_STATUS_IGNORE)` or `MPI_Waitall(n, reqs, MPI_STATUSES_IGNORE)`. The buffer belongs to MPI until the wait returns. Post receives before the matching sends where possible, so messages land in user buffers instead of internal ones. Done when: every request is completed by a wait or test before its buffer is reused or freed.
5. Split communicators for groups. `MPI_Comm_split(MPI_COMM_WORLD, color, key, &subcomm)` puts ranks with equal `color` in one communicator ordered by `key`; free it with `MPI_Comm_free`. Done when: group-local collectives run on the subcommunicator and it is freed.
6. Hybrid MPI and OpenMP. Initialize with `MPI_Init_thread(&argc, &argv, MPI_THREAD_FUNNELED, &provided)` when only the main thread calls MPI, or `MPI_THREAD_MULTIPLE` when any thread does, and check `provided`. Size the threads to the cores per rank: `OMP_NUM_THREADS = cores_per_node / ranks_per_node`. Place ranks with Open MPI's `--map-by ppr:2:package --bind-to core` (`socket` is the deprecated spelling of `package`); `--report-bindings` prints the result. `openmp` covers the thread side. Done when: ranks times threads equals the cores in use and `--report-bindings` shows no overlap.
7. Launch on several nodes. Hostfile lines are `node0 slots=4`; run `mpirun -np 8 --hostfile hosts.txt ./app`. Under Slurm, `srun -n 64 ./app` or `mpirun -np $SLURM_NTASKS ./app` inside the allocation. `--tag-output` prefixes each output line with its rank. Done when: ranks land on the intended nodes.
8. MPI-IO for parallel files:

   ```c
   MPI_File fh;
   MPI_File_open(MPI_COMM_WORLD, "output.dat", MPI_MODE_CREATE | MPI_MODE_WRONLY, MPI_INFO_NULL, &fh);
   MPI_Offset offset = (MPI_Offset)rank * chunk_bytes;
   MPI_File_write_at_all(fh, offset, buf, count, MPI_DOUBLE, MPI_STATUS_IGNORE);
   MPI_File_close(&fh);
   ```

   The `_all` collective form lets the library aggregate requests; `MPI_File_write_at` is the independent form. Done when: every rank writes its own offset range and the file size equals ranks times chunk.
9. Diagnose scaling. Load imbalance: measure per-rank time with `MPI_Wtime` around the work phase and redistribute chunks. Serialization at rank 0: replace gather-then-process with a reduction tree (`MPI_Reduce`, `MPI_Allreduce`) and parallel I/O. Excess synchronization: remove barriers that guard nothing. Many small messages: aggregate into larger buffers or derived datatypes. `MPI_Alltoall` at large rank counts: use neighborhood collectives (`MPI_Neighbor_alltoall`) on a topology communicator when each rank talks to few peers. Profile rank hotspots with `linux-perf` (`perf record` on one rank's PID). Done when: the bottleneck is named with a measurement and the fix is applied or proposed.

## Failure and recovery

| Failure | Cause | Fix |
|---|---|---|
| Hang in `MPI_Recv` | No matching send: tag, source, or communicator differs | Print the tuple on both sides; test with `MPI_ANY_TAG` to confirm a tag mismatch |
| Deadlock with blocking sends on both sides | Each rank waits for the other's receive | Order the exchange (even ranks send first), or use `MPI_Sendrecv` or non-blocking calls |
| Wrong reduction result | Datatype or count differs across ranks | Match `MPI_INT` versus `MPI_DOUBLE` and the count on every rank |
| `MPI_ERR_TRUNCATE` | Receive buffer smaller than the message | Match counts; use `MPI_Probe` and `MPI_Get_count` for variable sizes |
| Poor scaling past a few nodes | Rank 0 aggregates or writes everything | Distribute I/O with MPI-IO; use reductions |
| Hybrid run slower than pure MPI | Ranks times threads exceeds cores, or threads unbound | Set `OMP_NUM_THREADS`, bind with `--bind-to core`, check `--report-bindings` |
| Launch refused with a slots error (Open MPI `prte-rmaps-base:alloc-error`) | More ranks than detected slots | `--oversubscribe` for tests; a correct hostfile for real runs |
| Crash after `MPI_Finalize` or leaked communicators | Requests or communicators never completed or freed | Wait on every request; `MPI_Comm_free` every split communicator |

## Output

An MPI program that compiles with `mpicc`, runs under `mpirun` with correct output per rank, has matched sends and receives and completed requests, and, when performance was the question, a named bottleneck with its measurement and the applied fix; plus the launch command with its placement flags.
