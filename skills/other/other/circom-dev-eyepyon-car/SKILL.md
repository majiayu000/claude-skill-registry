---
name: circom-dev
description: Zero-knowledge proof circuit development using circom. Use when implementing arithmetic circuits for zkSNARKs, including circuit design, constraint verification, witness generation, and testing. Triggers on tasks like "create a circom circuit", "implement ZK proof", "write Merkle tree circuit", "add range proof", or any zero-knowledge cryptography implementation requiring circom.
---

# Circom Development

Expert guidance for designing, implementing, and testing zero-knowledge proof circuits using circom.

## Overview

This skill provides comprehensive support for circom circuit development:

- **Circuit Implementation**: Design and write optimized arithmetic circuits
- **Constraint Verification**: Ensure circuits are properly constrained and secure
- **Witness Generation**: Create and test witness calculators
- **Testing**: Comprehensive testing patterns for circuits
- **Best Practices**: Security guidelines and optimization techniques

## Quick Start

### 1. Project Setup

Initialize a new circom project with required dependencies:

```bash
# Copy package.json template
cp assets/package.json ./package.json

# Install dependencies
npm install

# Create project structure
mkdir -p circuits build scripts
```

### 2. Create Circuit

Use the circuit template as a starting point:

```bash
cp assets/template_circuit.circom circuits/your_circuit.circom
```

Edit the circuit with your logic:

```circom
pragma circom 2.0.0;
include "node_modules/circomlib/circuits/poseidon.circom";

template YourCircuit() {
    signal input in;
    signal output out;

    component hasher = Poseidon(1);
    hasher.inputs[0] <== in;
    out <== hasher.out;
}

component main = YourCircuit();
```

### 3. Compile Circuit

Use the compilation script:

```bash
bash scripts/compile_circuit.sh circuits/your_circuit.circom
```

This generates:
- `build/your_circuit_js/your_circuit.wasm` - Witness calculator
- `build/your_circuit.r1cs` - Constraint system
- `build/your_circuit.sym` - Symbol mapping

### 4. Setup Proving Keys

Generate zkey and verification key:

```bash
bash scripts/setup_keys.sh build/your_circuit.r1cs
```

This generates:
- `build/zkey/your_circuit.zkey` - Proving key
- `build/zkey/verification_key.json` - Verification key
- `build/zkey/your_circuit_verifier.sol` - Solidity verifier

### 5. Create Test

Use the test template:

```bash
cp assets/template_test.js test.js
```

Update test inputs and run:

```bash
node test.js
```

## Workflow Decision Tree

```
┌─────────────────────────────────────┐
│ What do you need to do?             │
└──────────────┬──────────────────────┘
               │
       ┌───────┴────────┐
       │                │
   New Circuit    Modify Existing
       │                │
       ▼                ▼
  Start from      Read existing
   template        circuit first
       │                │
       ▼                ▼
  Implement       Understand
  constraints     constraints
       │                │
       ▼                ▼
   Compile         Make changes
       │                │
       ▼                ▼
  Setup keys      Recompile
       │                │
       ▼                ▼
  Write tests     Update tests
       │                │
       └────────┬───────┘
                ▼
          Run & verify
                │
        ┌───────┴────────┐
        │                │
    Success         Failure
        │                │
        ▼                ▼
    Complete      Debug & fix
                        │
                        └──> Repeat
```

## Circuit Design Guidelines

### 1. Define Requirements

Before writing code, clarify:

- **Private inputs**: What information must remain secret?
- **Public inputs**: What can be revealed to the verifier?
- **Outputs**: What statement are you proving?
- **Constraints**: What rules must be enforced?

**Example:** Password authentication
- Private: password
- Public: passwordHash
- Statement: "I know a password that hashes to passwordHash"

### 2. Choose Components

Consult [circomlib_components.md](references/circomlib_components.md) for standard components:

- **Hashing**: Poseidon, MiMC
- **Comparisons**: IsZero, LessThan, IsEqual
- **Merkle Trees**: SMTVerifier
- **Signatures**: EdDSA

### 3. Write Constraints

Follow these principles:

**Use `<==` for most operations** (assigns AND constrains):
```circom
output <== input1 * input2;
```

**Use `===` for explicit constraints**:
```circom
component.out === expectedValue;
```

**NEVER use `<--` alone** (no constraint):
```circom
// DANGEROUS - prover can cheat!
temp <-- unconstrained_value;
```

### 4. Validate Inputs

Always constrain input ranges:

```circom
// Ensure value is less than maximum
component check = LessThan(32);
check.in[0] <== value;
check.in[1] <== maxValue;
check.out === 1;
```

See [best_practices.md](references/best_practices.md) for security guidelines.

## Common Circuit Patterns

Consult [circuit_patterns.md](references/circuit_patterns.md) for complete implementations:

### Authentication
- **Password proof**: Prove knowledge of password without revealing it
- **Credential verification**: Prove possession of valid credentials

### Merkle Trees
- **Membership proof**: Prove element is in a set without revealing which
- **Tree update**: Prove correct update of Merkle tree

### Range Proofs
- **Value in range**: Prove value is within bounds (e.g., age > 18)
- **Balance sufficiency**: Prove sufficient balance without revealing amount

### Voting
- **Anonymous voting**: Vote without revealing identity
- **Weighted voting**: Vote with weight based on holdings

### Privacy
- **Private transfer**: Transfer funds without revealing sender/receiver/amount
- **Nullifier pattern**: Prevent double-spending

## Testing Workflow

### 1. Unit Test Components

Test individual templates in isolation:

```javascript
const circuit = await wasm_tester("circuits/component.circom");

// Test valid input
const input = { in: 10 };
const witness = await circuit.calculateWitness(input);
await circuit.checkConstraints(witness);

// Test expected output
await circuit.assertOut(witness, { out: 100 });
```

### 2. Test Edge Cases

Always test:
- **Zero values**: `{ in: 0 }`
- **Maximum values**: Near field prime
- **Boundary conditions**: Min/max range values
- **Invalid inputs**: Should fail constraint checks

### 3. Integration Testing

Test full proof generation and verification:

```javascript
const { proof, publicSignals } = await snarkjs.groth16.fullProve(
  input,
  wasmPath,
  zkeyPath
);

const vKey = JSON.parse(fs.readFileSync(vkeyPath));
const isValid = await snarkjs.groth16.verify(vKey, publicSignals, proof);
assert(isValid);
```

Use `scripts/verify_proof.js` for standalone verification:

```bash
node scripts/verify_proof.js -p proof.json -s public.json -v verification_key.json
```

## Optimization Techniques

### 1. Minimize Constraints

Fewer constraints = faster proving time.

**Check constraint count:**
```bash
npx snarkjs r1cs info build/circuit.r1cs
```

**Optimization tips:**
- Reuse components when possible
- Minimize hash operations (expensive)
- Use `assert` for compile-time checks (no runtime cost)
- Combine operations where possible

### 2. Choose Efficient Components

- **Poseidon > MiMC**: Poseidon is optimized for zkSNARKs
- **Bit operations**: Use Num2Bits/Bits2Num for bit manipulation
- **Range checks**: Use SafeLessThan for range-checked comparisons

### 3. Profile Circuit

Monitor statistics:
```bash
npx snarkjs r1cs info circuit.r1cs
```

Output shows:
- Number of constraints
- Number of public inputs/outputs
- Number of private inputs
- Number of wires

## Security Checklist

Before deploying, verify:

- [ ] All signals properly constrained (no `<--` without verification)
- [ ] Input ranges validated
- [ ] Division operations properly constrained (with remainder check)
- [ ] Public/private signals correctly specified
- [ ] Edge cases tested (0, max values, boundaries)
- [ ] No under-constrained circuits (verify constraint count)
- [ ] Code reviewed
- [ ] Static analysis tools run (Circomspect, PICUS if available)

See [best_practices.md](references/best_practices.md) for detailed security guidelines.

## Troubleshooting

### Common Issues

**"Constraint doesn't match"**
- Check all signals are properly constrained with `<==` or `===`
- Verify arithmetic is correct
- Look for signals using `<--` without corresponding constraints

**"Not enough values"**
- Ensure all inputs are provided in test
- Check array sizes match template parameters

**"Scalar size exceeds field size"**
- Input value is too large for the field
- Use range constraints to validate inputs

**High constraint count**
- Review circuit for optimization opportunities
- Consider refactoring complex logic
- Check for unnecessary component instantiations

### Debugging Tips

1. **Add debug signals**: Create intermediate signals to inspect values in witness
2. **Use circom logger**: Add `log()` statements in circuit
3. **Test incrementally**: Build circuit piece by piece, testing each addition
4. **Verify constraint count**: Monitor constraint growth as you add logic

## Scripts Reference

### compile_circuit.sh

Compile circom circuits to WASM and R1CS.

```bash
./scripts/compile_circuit.sh <circuit_file> [options]

Options:
  -o, --output DIR    Output directory (default: build)
  -h, --help         Show help
```

### setup_keys.sh

Generate proving and verification keys.

```bash
./scripts/setup_keys.sh <r1cs_file> [options]

Options:
  -s, --size N        Circuit size (default: 12)
  -o, --output DIR    Output directory (default: build/zkey)
  -p, --ptau DIR      ptau directory (default: ptau)
  -h, --help         Show help
```

### verify_proof.js

Verify a zero-knowledge proof.

```bash
node scripts/verify_proof.js [options]

Options:
  -p, --proof FILE     Proof JSON file
  -s, --signals FILE   Public signals JSON file
  -v, --vkey FILE      Verification key file
  -h, --help          Show help
```

## References

This skill includes detailed reference documentation:

### [circomlib_components.md](references/circomlib_components.md)

Standard library component reference:
- Hash functions (Poseidon, MiMC)
- Comparators (IsZero, LessThan, IsEqual)
- Multiplexers (Mux1, Mux3)
- Bitwise operations (Num2Bits, Bits2Num)
- Merkle trees (SMTVerifier)
- Signatures (EdDSA)

### [best_practices.md](references/best_practices.md)

Security and optimization guidelines:
- Constraint writing best practices
- Security considerations
- Optimization techniques
- Testing and debugging
- Common pitfalls and how to avoid them

### [circuit_patterns.md](references/circuit_patterns.md)

Implementation patterns for common use cases:
- Authentication patterns
- Merkle tree patterns
- Range proof patterns
- Voting patterns
- Privacy-preserving patterns

## Example: Complete Workflow

Here's a complete example of implementing a password authentication circuit:

```circom
// 1. Create circuit: circuits/password_auth.circom
pragma circom 2.0.0;
include "node_modules/circomlib/circuits/poseidon.circom";

template PasswordAuth() {
    signal input password;
    signal input passwordHash;

    component hasher = Poseidon(1);
    hasher.inputs[0] <== password;
    passwordHash === hasher.out;
}

component main {public [passwordHash]} = PasswordAuth();
```

```bash
# 2. Compile
bash scripts/compile_circuit.sh circuits/password_auth.circom

# 3. Setup keys
bash scripts/setup_keys.sh build/password_auth.r1cs
```

```javascript
// 4. Create test: test_password.js
const snarkjs = require("snarkjs");
const circomlibjs = require("circomlibjs");

async function test() {
  // Calculate expected hash
  const password = 12345;
  const poseidon = await circomlibjs.buildPoseidon();
  const passwordHash = poseidon.F.toString(poseidon([password]));

  // Generate proof
  const { proof, publicSignals } = await snarkjs.groth16.fullProve(
    { password, passwordHash },
    "build/password_auth_js/password_auth.wasm",
    "build/zkey/password_auth.zkey"
  );

  // Verify
  const vKey = require("./build/zkey/verification_key.json");
  const isValid = await snarkjs.groth16.verify(vKey, publicSignals, proof);
  console.log("Valid:", isValid);
}

test();
```

```bash
# 5. Run test
node test_password.js
```

## Additional Resources

- **Circom Documentation**: https://docs.circom.io/
- **circomlib Repository**: https://github.com/iden3/circomlib
- **snarkjs**: https://github.com/iden3/snarkjs
- **0xPARC Learning**: https://learn.0xparc.org/
- **ZK Whiteboard Sessions**: https://zkhack.dev/whiteboard/
