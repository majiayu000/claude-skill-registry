---
name: mfe-unification
description: "Deep symmetries and unifying principles — gauge theory, Lie groups, Noether's theorem, and the Standard Model. Constructs field theories from symmetry requirements, derives conservation laws, and traces force unification. Use when working with gauge symmetry, Lie groups (U(1), SU(2), SU(3)), conservation laws via Noether's theorem, the Higgs mechanism, or Standard Model structure."
user-invocable: false
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-26"
      triggers:
        intents:
          - "symmetry"
          - "gauge"
          - "unify"
          - "standard model"
          - "force"
          - "coupling"
          - "conservation"
          - "invariance"
        contexts:
          - "mathematical problem solving"
          - "math reasoning"
---

# Unification

Part VIII: Converging — Chapters 26, 27 — Plane Position: (0, 0.6) radius 0.3 — 37 Primitives

## Workflow

1. **Identify the symmetry group** governing the problem — U(1) for electromagnetism, SU(2) for weak force, SU(3) for strong force, or combinations
2. **Apply the gauge principle** to derive required gauge fields from local invariance requirements
3. **Construct the Lagrangian** encoding field dynamics and interactions using gauge-invariant terms
4. **Apply Noether's theorem** to extract conserved quantities (charge, isospin, color charge) from continuous symmetries
5. **Check for spontaneous symmetry breaking** — apply the Higgs mechanism where gauge bosons acquire mass

## Key Concepts

**Gauge Principle** (technique): The gauge principle states that physics must be invariant under local (spacetime-dependent) symmetry transformations. Requiring local gauge invariance necessitates the introduction of gauge fields (connections) that transform as A_mu -> g A_mu g^{-1} + (i/e) g partial_mu g^{-1}.
  - Constructing quantum field theories from symmetry requirements
  - Deriving force-carrying particles from local invariance
  - Understanding why fundamental forces have the structure they do

**SU(2) Symmetry Group** (definition): SU(2) is the group of 2x2 unitary matrices with determinant 1. It is the gauge group of the weak nuclear force and is locally isomorphic to SO(3), the rotation group in 3D. Its Lie algebra su(2) has basis {sigma_1/2, sigma_2/2, sigma_3/2} (Pauli matrices).
  - Describing weak nuclear force gauge symmetry
  - Modeling isospin and weak interactions
  - Representing 3D rotations via double cover

**String Action** (definition): The Nambu-Goto action S_NG = -T integral d^2 sigma sqrt(-det(h_{alpha beta})) describes a relativistic string propagating through spacetime, where h_{alpha beta} = partial_alpha X^mu partial_beta X_mu is the induced metric on the worldsheet and T = 1/(2*pi*alpha') is the string tension.
  - Describing fundamental objects beyond point particles
  - Building quantum theories of gravity
  - Exploring the structure of spacetime at the Planck scale

**U(1) Symmetry Group** (definition): U(1) is the group of complex numbers of unit modulus under multiplication: U(1) = {e^{i*theta} : theta in [0, 2*pi)}. It is the gauge group of electromagnetism, with phase rotations psi -> e^{i*alpha} psi leaving the Lagrangian invariant.
  - Describing electromagnetic gauge invariance
  - Modeling phase symmetries in quantum mechanics
  - Classifying abelian gauge theories

**SU(3) Symmetry Group** (definition): SU(3) is the group of 3x3 unitary matrices with determinant 1. It is the gauge group of quantum chromodynamics (QCD), governing the strong nuclear force. Its 8 generators correspond to 8 gluons, the force carriers of the strong interaction.
  - Describing strong nuclear force interactions between quarks
  - Classifying hadrons using color charge representations
  - Modeling gluon self-interactions

**Lagrangian Formulation** (definition): The Lagrangian density L encodes the dynamics of a field theory. The action S = integral L d^4x is stationary under field variations (Hamilton's principle), yielding the Euler-Lagrange field equations. The Standard Model Lagrangian L_SM = L_gauge + L_fermion + L_Higgs + L_Yukawa.
  - Formulating physical theories from symmetry principles
  - Deriving equations of motion for fields and particles
  - Encoding all interactions in a single mathematical object

**Extra Dimensions and Compactification** (definition): String theory requires extra spatial dimensions (6 for superstrings, 22 for bosonic strings) beyond the 3+1 spacetime dimensions we observe. Compactification curls extra dimensions into small manifolds: M^{10} = M^{3,1} x K^6 where K^6 is a compact Calabi-Yau manifold.
  - Understanding why string theory predicts more than 4 spacetime dimensions
  - Connecting string theory to observable 4D physics
  - Exploring the landscape of possible low-energy effective theories

**Yang-Mills Theory** (definition): Yang-Mills theory is a gauge theory with a non-abelian gauge group G. The field strength tensor is F^a_{mu nu} = partial_mu A^a_nu - partial_nu A^a_mu + g f^{abc} A^b_mu A^c_nu, where f^{abc} are structure constants. The Lagrangian is L = -1/4 F^a_{mu nu} F^{a mu nu}.
  - Constructing non-abelian gauge theories for fundamental forces
  - Understanding self-interactions of gauge fields

**Noether's Theorem** (theorem): For every continuous symmetry of the action, there exists a corresponding conserved quantity. If the Lagrangian is invariant under a continuous transformation phi -> phi + epsilon * delta_phi, then the current j^mu = (partial L / partial(partial_mu phi)) delta_phi is conserved: partial_mu j^mu = 0.
  - Deriving conservation laws from symmetry principles
  - Understanding the deep connection between symmetry and physics
  - Finding conserved quantities for novel physical theories

**Higgs Mechanism** (technique): Spontaneous symmetry breaking via a scalar field phi with potential V(phi) = -mu^2 |phi|^2 + lambda |phi|^4 gives gauge bosons mass. The vacuum expectation value <phi> = v/sqrt(2) breaks SU(2) x U(1)_Y -> U(1)_EM, generating masses m_W = gv/2, m_Z = v*sqrt(g^2+g'^2)/2.
  - Explaining how gauge bosons acquire mass
  - Understanding mass generation without breaking gauge invariance at the Lagrangian level
  - Predicting particle masses from symmetry breaking patterns

## Composition Patterns

- U(1) Symmetry Group + unification-symmetry-group-su2 -> Electroweak gauge group SU(2) x U(1) (parallel)
- SU(2) Symmetry Group + unification-symmetry-group-su3 -> Non-abelian gauge group of the Standard Model: SU(3) x SU(2) x U(1) (parallel)
- SU(3) Symmetry Group + reality-schrodinger-time-independent -> QCD equations of motion for quark fields (nested)
- Gauge Principle + foundations-group-definition -> Construction of gauge theories from any Lie group (sequential)
- Lagrangian Formulation + unification-gauge-principle -> Gauge-invariant Lagrangian with gauge field kinetic terms (sequential)
- Noether's Theorem + unification-gauge-principle -> Gauge conservation laws: charge, color charge, weak isospin (sequential)
- Higgs Mechanism + unification-symmetry-group-su2 -> Massive W and Z bosons with predicted mass ratios (sequential)
- Spontaneous Symmetry Breaking + unification-gauge-principle -> Gauge boson mass generation (Higgs mechanism) (sequential)
- Electroweak Unification + unification-strong-force-qcd -> The complete Standard Model: SU(3) x SU(2) x U(1) (parallel)
- Quantum Chromodynamics (QCD) + unification-electroweak-unification -> The complete Standard Model of particle physics (parallel)

## Cross-Domain Links

- **foundations**: Compatible domain for composition and cross-referencing
- **mapping**: Compatible domain for composition and cross-referencing
- **emergence**: Compatible domain for composition and cross-referencing
- **synthesis**: Compatible domain for composition and cross-referencing

## Activation Patterns

- symmetry
- gauge
- unify
- standard model
- force
- coupling
- conservation
- invariance
