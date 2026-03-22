---
name: zkvm-evaluator
description: Trustless ERC-8183 job evaluation — run Client's verification program inside a zkVM with ZK proof.
metadata: { "cryptoclaw": { "emoji": "🔐", "always": true } }
---

# zkVM Evaluator

Trustless evaluation for ERC-8183 Agentic Commerce jobs. The Client provides a verification program, the Evaluator runs it on the Provider's deliverable inside a zkVM, and the zkVM generates a mathematical proof that the program actually executed and produced the claimed result.

**No trust in the evaluator needed.** The proof is verifiable on-chain by anyone.

## Tools

- `zkvm_evaluate_job` — Run verification program on deliverable, generate ZK proof, settle job on-chain
- `zkvm_status` — Check which zkVM backends are installed (SP1, RISC Zero, native)

## How It Works

```
Client creates Job:
  - description: "Write an ERC-20 contract"
  - verification program: test_suite.elf → IPFS (QmXyz...)
  - evaluator: zkVM evaluator contract

Provider submits:
  - deliverable: MyToken.sol → IPFS (QmAbc...)

Evaluator runs:
  zkvm_evaluate_job(
    jobId: "42",
    programRef: "QmXyz...",     ← Client's test suite
    deliverableRef: "QmAbc..."  ← Provider's code
  )

Inside zkVM:
  1. Load test_suite.elf (RISC-V binary)
  2. Feed MyToken.sol as stdin
  3. Execute: test_suite(MyToken.sol)
  4. Result: exit code 0 (all tests pass)
  5. Generate ZK proof of execution

On-chain:
  proof proves "program QmXyz on input QmAbc exited with code 0"
  → complete(jobId=42, reasonHash=proof_hash)
  → funds released to Provider
```

## Verification Program Requirements

The verification program is a compiled RISC-V ELF binary that:

- Reads the deliverable from **stdin**
- Reads optional context from env vars (`ZKVM_JOB_DESCRIPTION`, `ZKVM_DELIVERABLE_HASH`)
- Outputs evaluation details to **stdout**
- Exits with code **0** for pass, **non-zero** for fail

Example (Rust, compiled for RISC-V):

```rust
use std::io::Read;

fn main() {
    let mut deliverable = String::new();
    std::io::stdin().read_to_string(&mut deliverable).unwrap();

    // Check deliverable meets requirements
    if deliverable.contains("function transfer")
        && deliverable.contains("function approve")
        && deliverable.contains("event Transfer")
    {
        println!("PASS: ERC-20 interface complete");
        std::process::exit(0);
    } else {
        println!("FAIL: Missing required ERC-20 functions");
        std::process::exit(1);
    }
}
```

## Backends

| Backend            | ZK Proof            | Speed                                | Install                                                        |
| ------------------ | ------------------- | ------------------------------------ | -------------------------------------------------------------- |
| **SP1** (Succinct) | Yes (Groth16/PLONK) | Fastest                              | `curl -L https://sp1.succinct.xyz \| bash && sp1up`            |
| **RISC Zero**      | Yes (Groth16)       | Fast, Bonsai remote prover available | `curl -L https://risczero.com/install \| bash && rzup install` |
| **Native**         | No (dev only)       | Instant                              | Always available                                               |

Auto-detection: the tool picks the best available backend. Use `zkvm_status` to check.

## What the Proof Guarantees

```
Public inputs (anyone can see):
  - Program hash: SHA-256 of the verification program
  - Deliverable hash: SHA-256 of the deliverable
  - Exit code: 0 (pass) or non-zero (fail)

The proof mathematically guarantees:
  ✅ This specific program ran on this specific deliverable
  ✅ The exit code is what the program actually produced
  ✅ No one tampered with the execution

The proof does NOT reveal:
  ❌ The deliverable content (only its hash)
  ❌ Internal program state during execution
```

## On-Chain Cost

| Proof System | Verification Gas | Cost on Base L2 |
| ------------ | ---------------- | --------------- |
| Groth16      | ~200k gas        | ~$0.004         |
| PLONK        | ~300k gas        | ~$0.006         |

## Integration with TEE

For maximum security, run the zkVM evaluator inside a TEE enclave:

- TEE: proves the evaluator code wasn't tampered with
- ZK: proves the verification program produced the claimed result
- Combined: hardware + mathematical proof — strongest guarantee
