---
name: emerging-tech
description: Emerging and transformative technologies -- artificial intelligence, biotechnology, quantum computing, blockchain, robotics, IoT, augmented/virtual reality, and nanotechnology. Covers how each technology works at a conceptual level, current capabilities vs hype, societal implications, and risk assessment frameworks. Use when evaluating new technologies, assessing technological claims, understanding technology trends, or reasoning about the future impact of technology. Pairs with responsible-innovation for ethical analysis.
type: skill
category: technology
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/technology/emerging-tech/SKILL.md
superseded_by: null
---
# Emerging Technologies

Emerging technologies are those in the process of transitioning from laboratory research to widespread deployment. They promise transformative change, but that promise is often mixed with hype, uncertainty, and risk. This skill equips the learner to understand what emerging technologies actually do, distinguish demonstrated capabilities from marketing claims, and reason about societal implications before adoption decisions are made.

**Agent affinity:** joy (technology risk assessment, existential risk), gates-m (technology for social impact, global development), hicks (social construction of technology, labor implications)

**Concept IDs:** tech-transformative-technologies, tech-responsible-innovation

## Evaluating Emerging Technologies

### The Gartner Hype Cycle (as a critical tool, not gospel)

The Gartner Hype Cycle describes how new technologies move through phases of inflated expectations, disillusionment, and eventual productive use. While the model is imperfect and commercially motivated, its phases provide useful vocabulary:

1. **Technology trigger:** A breakthrough or proof of concept generates interest.
2. **Peak of inflated expectations:** Media coverage and vendor marketing create unrealistic expectations.
3. **Trough of disillusionment:** Reality falls short of hype; early adopters encounter limitations.
4. **Slope of enlightenment:** Practical applications emerge; understanding matures.
5. **Plateau of productivity:** Mainstream adoption with realistic expectations.

**Critical note:** The Hype Cycle is descriptive, not predictive. It does not tell you when a technology will mature or whether it will mature at all. Some technologies die in the trough. Use the vocabulary; do not use it as a forecasting tool.

### The Amara-Kranzberg Framework

Two principles guide technology assessment:

- **Amara's Law:** We tend to overestimate the effect of a technology in the short run and underestimate the effect in the long run.
- **Kranzberg's First Law:** Technology is neither good nor bad; nor is it neutral. Every technology reshapes social arrangements, economic structures, and power dynamics in ways that benefit some and harm others.

Together: be skeptical of short-term promises, attentive to long-term consequences, and always ask who benefits and who bears the cost.

## Technology Profiles

### Artificial Intelligence

**What it is:** Systems that perform tasks normally requiring human intelligence -- pattern recognition, language processing, decision-making, planning. Current AI is narrow (excels at specific tasks) rather than general (capable across all domains).

**How it works (conceptual):** Machine learning systems learn patterns from data rather than following explicit rules. A neural network adjusts millions of numerical weights during training so that its outputs match desired results. Deep learning uses many layers of such networks to learn hierarchical features.

**Current capabilities:** Image recognition, language generation, translation, code completion, game playing, scientific modeling, medical imaging analysis. These are genuine and useful.

**Limitations and risks:** Hallucination (confident generation of false information), bias amplification (reflecting and reinforcing patterns in training data), energy consumption, job displacement in specific sectors, concentration of power in organizations with training resources.

### Quantum Computing

**What it is:** Computation using quantum mechanical phenomena (superposition, entanglement) to process information in ways classical computers cannot efficiently replicate.

**How it works (conceptual):** A quantum bit (qubit) can exist in a superposition of 0 and 1 simultaneously. Entangled qubits exhibit correlated behavior regardless of distance. Quantum algorithms exploit these properties to explore solution spaces exponentially faster for specific problem types.

**Current capabilities:** Proof-of-concept demonstrations on small problems. Quantum advantage has been demonstrated for specific, artificial benchmarks. No commercial quantum computer yet outperforms classical computers on practical problems.

**Limitations and risks:** Decoherence (qubits lose quantum properties rapidly), error rates orders of magnitude higher than classical computing, cryogenic cooling requirements, limited practical applications in the near term. The primary risk is misallocation of resources based on overpromising.

### Biotechnology

**What it is:** Technology that uses biological systems, living organisms, or derivatives to make products and processes.

**Key developments:** CRISPR gene editing, synthetic biology, personalized medicine, mRNA vaccine platforms, bioinformatics, agricultural biotech.

**Current capabilities:** CRISPR enables precise gene editing; mRNA platforms enabled rapid COVID-19 vaccine development; synthetic biology can produce biofuels and materials.

**Limitations and risks:** Off-target effects in gene editing, dual-use potential (bioweapons), regulatory lag behind capability, access inequality between wealthy and poor nations, ecological risks of engineered organisms.

### Internet of Things (IoT)

**What it is:** Networks of physical objects embedded with sensors, software, and connectivity that collect and exchange data.

**Current capabilities:** Smart home devices, industrial monitoring, precision agriculture, fleet tracking, environmental sensing, wearable health monitors.

**Limitations and risks:** Security vulnerabilities (many IoT devices have minimal security), privacy concerns (continuous data collection), e-waste (short device lifecycles), network congestion, vendor lock-in, and the assumption that "connected" always means "better."

### Blockchain and Distributed Ledgers

**What it is:** A distributed database that maintains a continuously growing list of records (blocks) linked using cryptography. Designed to be tamper-resistant and operate without a central authority.

**Current capabilities:** Cryptocurrency transactions, supply chain transparency, digital identity verification, smart contracts.

**Limitations and risks:** Extreme energy consumption (proof-of-work), scalability limitations, regulatory uncertainty, speculative volatility, and a gap between the technology's capabilities and its marketing claims.

### Robotics and Automation

**What it is:** Machines that can sense their environment, make decisions, and take physical action with varying degrees of autonomy.

**Current capabilities:** Industrial manufacturing, warehouse logistics, surgical assistance, autonomous vehicles (limited conditions), service robots, agricultural automation.

**Limitations and risks:** Job displacement in specific sectors, safety in shared human-robot spaces, algorithmic decision-making in high-stakes situations (autonomous weapons, self-driving cars), maintenance and obsolescence costs.

## Risk Assessment Framework

Bill Joy's 2000 essay "Why the Future Doesn't Need Us" posed the question: how do we evaluate technologies whose risks may be existential? The following framework adapts Joy's concerns into an actionable assessment tool.

### Five Risk Dimensions

| Dimension | Question | Scale |
|---|---|---|
| **Reversibility** | If this technology causes harm, can the harm be undone? | Fully reversible -- Partially reversible -- Irreversible |
| **Controllability** | Can deployment be stopped or contained once started? | Easily contained -- Difficult to contain -- Self-propagating |
| **Scope** | How many people are affected? | Individual -- Community -- Global |
| **Velocity** | How fast do consequences manifest? | Gradual (decades) -- Rapid (years) -- Immediate (days) |
| **Equity** | Who bears the risk vs who receives the benefit? | Equally distributed -- Moderately skewed -- Highly concentrated |

### Using the Framework

For each emerging technology, evaluate all five dimensions. Technologies that score "irreversible," "self-propagating," "global," "immediate," and "highly concentrated" demand the most caution. Technologies that score well on all dimensions may still carry risk, but the risk is more manageable.

**Example assessment: Gene drives (engineered genes that spread through wild populations)**
- Reversibility: Irreversible (gene drives self-propagate; recall is extremely difficult)
- Controllability: Self-propagating (designed to spread without human intervention)
- Scope: Global (a released gene drive can cross national boundaries)
- Velocity: Rapid (generations of the target organism, which may be weeks)
- Equity: Highly concentrated (decision-makers in one country affect ecosystems worldwide)

This assessment does not say "never use gene drives." It says "proceed with extreme caution, broad international consent, and containment research."

## Cross-References

- **joy agent:** Technology risk assessment, existential risk reasoning. Primary agent for evaluating transformative risk.
- **gates-m agent:** Technology for social impact and global development. Evaluates whether technologies serve or exclude marginalized populations.
- **hicks agent:** Social construction of technology, labor implications. Analyzes how technologies reshape work and power.
- **responsible-innovation skill:** Ethical frameworks for responsible technology development.
- **cybersecurity-basics skill:** Security implications of emerging technologies.
- **digital-systems skill:** Foundational knowledge underlying all digital emerging technologies.

## References

- Joy, B. (2000). "Why the Future Doesn't Need Us." *Wired*, April 2000.
- Brynjolfsson, E. & McAfee, A. (2014). *The Second Machine Age*. W. W. Norton.
- Crawford, K. (2021). *Atlas of AI*. Yale University Press.
- O'Neil, C. (2016). *Weapons of Math Destruction*. Crown.
- Jasanoff, S. (2016). *The Ethics of Invention*. W. W. Norton.
- Susskind, R. & Susskind, D. (2015). *The Future of the Professions*. Oxford University Press.
