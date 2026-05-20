---
name: code-review-riscv
description: Review RISC-V assembly code for correctness, ABI compliance, and best practices. Use after modifying RISC-V assembly or inline asm code.
disable-model-invocation: true
context: fork
agent: riscv-review-agent
---

Review RISC-V assembly code for correctness, adherence to conventions, and best practices.

The review covers 8 analysis categories:
1. **Instruction correctness**: Valid syntax, proper operands, immediate ranges
2. **Register conventions**: ABI compliance, saved vs temporary registers, stack alignment
3. **Memory access**: Alignment requirements, sign extension, offset limits
4. **Control flow**: Branches, jumps, function calls, returns
5. **CSR operations**: Privilege level access, atomic semantics, field types
6. **Assembler directives**: Sections, alignment, symbol visibility, data placement
7. **Common issues**: Misalignment, stack corruption, clobbered registers, illegal immediates
8. **Platform-specific**: RV32I vs RV64I, extensions (M/A/F/D/C), ABI variants

Search for RISC-V assembly code in git changes (inline asm and .S files) and perform deep analysis.
