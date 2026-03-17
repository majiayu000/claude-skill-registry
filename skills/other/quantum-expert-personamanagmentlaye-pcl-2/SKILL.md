---
name: quantum-expert
version: 1.0.0
description: Expert-level quantum computing, Qiskit, quantum algorithms, and quantum information
category: scientific
tags: [quantum-computing, qiskit, quantum-algorithms, quantum-information]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(python:*)
---

# Quantum Computing Expert

Expert guidance for quantum computing, quantum algorithms, Qiskit programming, and quantum information theory.

## Core Concepts

### Quantum Mechanics Basics
- Qubits and superposition
- Quantum entanglement
- Quantum interference
- Measurement and collapse
- Quantum gates (Pauli, Hadamard, CNOT)
- Quantum circuits

### Quantum Algorithms
- Grover's search algorithm
- Shor's factoring algorithm
- Quantum Fourier Transform (QFT)
- Variational Quantum Eigensolver (VQE)
- Quantum Approximate Optimization Algorithm (QAOA)
- Quantum machine learning

### Quantum Hardware
- Superconducting qubits
- Ion trap quantum computers
- Quantum annealing
- Noise and error correction
- Quantum volume
- NISQ (Noisy Intermediate-Scale Quantum) devices

## Qiskit Programming

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute, transpile
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import numpy as np

# Basic Quantum Circuit
def create_bell_state():
    """Create Bell state (maximally entangled state)"""
    qc = QuantumCircuit(2, 2)

    # Create superposition on qubit 0
    qc.h(0)

    # Entangle qubits 0 and 1
    qc.cx(0, 1)

    # Measure both qubits
    qc.measure([0, 1], [0, 1])

    return qc

# Quantum Teleportation
def quantum_teleportation():
    """Implement quantum teleportation protocol"""
    qc = QuantumCircuit(3, 3)

    # Prepare state to teleport (qubit 0)
    qc.ry(np.pi/4, 0)

    # Create Bell pair between qubits 1 and 2
    qc.h(1)
    qc.cx(1, 2)

    # Bell measurement on qubits 0 and 1
    qc.cx(0, 1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])

    # Apply corrections on qubit 2 based on measurement
    qc.cx(1, 2)
    qc.cz(0, 2)

    # Measure final state
    qc.measure(2, 2)

    return qc

# Grover's Search Algorithm
class GroverSearch:
    def __init__(self, n_qubits: int, marked_state: str):
        self.n_qubits = n_qubits
        self.marked_state = marked_state
        self.circuit = None

    def create_oracle(self):
        """Create oracle that marks the target state"""
        oracle = QuantumCircuit(self.n_qubits)

        # Mark the target state by flipping phase
        for i, bit in enumerate(reversed(self.marked_state)):
            if bit == '0':
                oracle.x(i)

        # Multi-controlled Z gate
        oracle.h(self.n_qubits - 1)
        oracle.mcx(list(range(self.n_qubits - 1)), self.n_qubits - 1)
        oracle.h(self.n_qubits - 1)

        # Uncompute
        for i, bit in enumerate(reversed(self.marked_state)):
            if bit == '0':
                oracle.x(i)

        return oracle

    def create_diffuser(self):
        """Create diffusion operator"""
        diffuser = QuantumCircuit(self.n_qubits)

        # Apply H gates
        diffuser.h(range(self.n_qubits))

        # Apply X gates
        diffuser.x(range(self.n_qubits))

        # Multi-controlled Z
        diffuser.h(self.n_qubits - 1)
        diffuser.mcx(list(range(self.n_qubits - 1)), self.n_qubits - 1)
        diffuser.h(self.n_qubits - 1)

        # Apply X gates
        diffuser.x(range(self.n_qubits))

        # Apply H gates
        diffuser.h(range(self.n_qubits))

        return diffuser

    def build_circuit(self):
        """Build complete Grover's algorithm circuit"""
        self.circuit = QuantumCircuit(self.n_qubits, self.n_qubits)

        # Initialize in superposition
        self.circuit.h(range(self.n_qubits))

        # Calculate optimal number of iterations
        n_iterations = int(np.pi / 4 * np.sqrt(2**self.n_qubits))

        oracle = self.create_oracle()
        diffuser = self.create_diffuser()

        # Apply Grover iteration
        for _ in range(n_iterations):
            self.circuit.compose(oracle, inplace=True)
            self.circuit.compose(diffuser, inplace=True)

        # Measure
        self.circuit.measure(range(self.n_qubits), range(self.n_qubits))

        return self.circuit

    def run(self, shots: int = 1024):
        """Execute circuit"""
        backend = Aer.get_backend('qasm_simulator')
        job = execute(self.circuit, backend, shots=shots)
        result = job.result()
        counts = result.get_counts()

        return counts
```

## Variational Quantum Eigensolver (VQE)

```python
from qiskit.algorithms import VQE
from qiskit.algorithms.optimizers import SLSQP
from qiskit.circuit.library import TwoLocal
from qiskit.primitives import Estimator
from qiskit.quantum_info import SparsePauliOp

class VQESolver:
    """Variational Quantum Eigensolver for finding ground state energy"""

    def __init__(self, hamiltonian: SparsePauliOp, n_qubits: int):
        self.hamiltonian = hamiltonian
        self.n_qubits = n_qubits

    def create_ansatz(self, reps: int = 2):
        """Create parameterized quantum circuit (ansatz)"""
        ansatz = TwoLocal(
            self.n_qubits,
            'ry',
            'cz',
            reps=reps,
            entanglement='linear'
        )
        return ansatz

    def run_vqe(self):
        """Run VQE algorithm"""
        ansatz = self.create_ansatz()
        optimizer = SLSQP(maxiter=100)
        estimator = Estimator()

        vqe = VQE(estimator, ansatz, optimizer)
        result = vqe.compute_minimum_eigenvalue(self.hamiltonian)

        return {
            "eigenvalue": result.eigenvalue,
            "optimal_parameters": result.optimal_parameters,
            "optimal_point": result.optimal_point,
            "cost_function_evals": result.cost_function_evals
        }

# Example: H2 molecule
def create_h2_hamiltonian():
    """Create Hamiltonian for H2 molecule"""
    # Simplified Hamiltonian
    hamiltonian = SparsePauliOp.from_list([
        ("II", -1.0523732),
        ("IZ", 0.39793742),
        ("ZI", -0.39793742),
        ("ZZ", -0.01128010),
        ("XX", 0.18093119)
    ])
    return hamiltonian
```

## Quantum Machine Learning

```python
from qiskit_machine_learning.algorithms import VQC
from qiskit_machine_learning.neural_networks import CircuitQNN
from qiskit.circuit import Parameter
import numpy as np

class QuantumClassifier:
    """Variational Quantum Classifier"""

    def __init__(self, n_features: int, n_classes: int):
        self.n_features = n_features
        self.n_classes = n_classes
        self.vqc = None

    def create_feature_map(self):
        """Create feature map to encode classical data"""
        qc = QuantumCircuit(self.n_features)

        for i in range(self.n_features):
            param = Parameter(f'x[{i}]')
            qc.ry(param, i)

        return qc

    def create_ansatz(self):
        """Create parameterized circuit"""
        ansatz = TwoLocal(
            self.n_features,
            ['ry', 'rz'],
            'cz',
            reps=2,
            entanglement='full'
        )
        return ansatz

    def train(self, X_train, y_train):
        """Train quantum classifier"""
        feature_map = self.create_feature_map()
        ansatz = self.create_ansatz()

        self.vqc = VQC(
            num_qubits=self.n_features,
            feature_map=feature_map,
            ansatz=ansatz,
            optimizer=SLSQP(maxiter=100)
        )

        self.vqc.fit(X_train, y_train)

    def predict(self, X_test):
        """Predict using trained model"""
        return self.vqc.predict(X_test)
```

## Best Practices

### Circuit Design
- Minimize circuit depth for NISQ devices
- Use native gates when possible
- Consider qubit connectivity
- Implement error mitigation
- Optimize transpilation
- Use efficient state preparation

### Algorithm Implementation
- Start with small quantum circuits
- Validate with classical simulation
- Use noise models for realistic testing
- Implement proper error handling
- Monitor quantum volume metrics
- Document quantum advantage claims

### Production Usage
- Use quantum cloud services (IBM, AWS Braket)
- Implement hybrid classical-quantum algorithms
- Cache quantum results when possible
- Monitor job queue times
- Handle quantum hardware limitations
- Plan for error correction overhead

## Anti-Patterns

❌ Deep circuits on NISQ devices
❌ Ignoring hardware connectivity
❌ No error mitigation
❌ Claiming quantum advantage without proof
❌ Not validating with simulation first
❌ Ignoring decoherence times
❌ Inefficient state preparation

## Resources

- Qiskit: https://qiskit.org/
- IBM Quantum: https://quantum-computing.ibm.com/
- Quantum Computing Stack Exchange: https://quantumcomputing.stackexchange.com/
- AWS Braket: https://aws.amazon.com/braket/
