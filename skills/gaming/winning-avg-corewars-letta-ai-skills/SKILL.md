---
name: winning-avg-corewars
description: This skill provides guidance for creating CoreWars warriors that achieve target win rates against multiple opponents. Use this skill when tasked with writing Redcode warriors, optimizing CoreWars strategies, or achieving specific win rate thresholds against a set of opponents. The skill covers systematic opponent analysis, parameter tuning methodologies, and common pitfalls in warrior design.
---

# Winning Avg CoreWars

## Overview

This skill enables systematic development of CoreWars warriors that must achieve specific win rate thresholds against multiple diverse opponents. It provides a structured methodology for analyzing opponents, designing effective warriors, and iteratively improving performance through hypothesis-driven testing.

## Key Concepts

CoreWars is a programming game where warriors (programs written in Redcode) compete in a shared memory space called the core. Common warrior archetypes include:

- **Scanners**: Search for opponents and attack when found
- **Bombers**: Systematically drop DAT bombs across the core
- **Replicators (Paper)**: Copy themselves throughout memory
- **Vampires**: Convert opponent processes to work for them
- **Imps**: Simple MOV 0,1 programs that spread through memory
- **Stones**: Bombing patterns with specific step sizes

## Workflow

### Phase 1: Opponent Analysis

Before writing any code, thoroughly analyze each opponent warrior:

1. **Read each opponent file completely** - understand every instruction
2. **Identify the archetype** - what strategy does it use?
3. **Extract key parameters**:
   - Step sizes (affects coverage patterns and vulnerabilities)
   - Memory access patterns
   - Process count and management
   - Defensive mechanisms
4. **Document vulnerabilities** - what attacks would disrupt this warrior?
5. **Calculate mathematical properties**:
   - For bombers: coverage rate = core_size / step_size
   - For replicators: replication speed and spread pattern
   - For scanners: scan density and blind spots

Reference `references/corewars_fundamentals.md` for mathematical relationships between step sizes, coprime values, and coverage patterns.

### Phase 2: Strategy Design

Design strategy based on opponent analysis, not trial and error:

1. **Categorize opponents by weakness**:
   - Fast bombers vulnerable to: quick replicators, distributed processes
   - Replicators vulnerable to: precise scanners, widespread bombing
   - Scanners vulnerable to: decoys, position-independent code
   - Imps vulnerable to: imp gates, specific bombing patterns

2. **Choose primary strategy** based on which approach counters the most opponents

3. **Design countermeasures** for each opponent type:
   - Document expected mechanism of winning
   - Identify which component defeats which opponent

4. **Consider hybrid approaches** when single strategies cannot meet all thresholds

### Phase 3: Parameter Selection

Select parameters based on mathematical analysis, not arbitrary values:

1. **Step sizes**: Choose coprime values relative to core size for optimal coverage
2. **Gate positions**: Calculate based on opponent scanning patterns
3. **Bombing intervals**: Match or counter opponent timing
4. **SPL count**: Understand trade-offs:
   - More processes = better survival against bombing
   - More processes = slower individual execution
   - Document which opponents benefit from each configuration

### Phase 4: Systematic Testing

Establish a rigorous testing methodology:

1. **Create a test script** that runs all opponents automatically (see `scripts/test_warrior.sh`)
2. **Test each component in isolation** before combining
3. **Record results systematically**:
   ```
   Version | Opponent | Wins | Losses | Ties | Notes
   ```
4. **Form hypotheses before changes**: "Increasing step to X should improve stone performance because..."
5. **Test one variable at a time** to understand causation

### Phase 5: Iterative Improvement

Follow a hypothesis-driven improvement cycle:

1. **Identify the weakest matchup** - focus on the opponent with the worst performance
2. **Hypothesize the cause** - why is this matchup failing?
3. **Design a targeted fix** - what specific change addresses the hypothesis?
4. **Predict the outcome** - what should improve? What might regress?
5. **Test and measure** - did results match predictions?
6. **If predictions were wrong**, revise understanding before trying another change

## Verification Strategies

### Win Rate Verification

- Run sufficient matches (100+ per opponent) for statistical significance
- Track variance across runs - inconsistent results indicate non-deterministic factors
- Verify with the exact testing harness that will be used for final evaluation

### Component Verification

- Test scanner component: Does it find targets at various positions?
- Test bomber component: What is actual coverage over N cycles?
- Test replicator component: How many copies survive after N cycles?
- Test imp backup: Does it activate when main warrior is killed?

### Regression Testing

- After any change, test ALL opponents, not just the target
- Document which changes help which opponents and why
- Maintain a "best known version" for each opponent matchup

## Common Pitfalls

### Trial-and-Error Without Understanding

**Problem**: Making random parameter changes hoping something works.
**Solution**: Every change should have a hypothesis explaining why it should help.

### Neglecting Difficult Opponents

**Problem**: Focusing only on opponents close to threshold while ignoring others.
**Solution**: Address each opponent systematically; a warrior that fails against one opponent type may need fundamental redesign.

### Conflating Correlation with Causation

**Problem**: "3 SPLs helped paper, so 3 SPLs is better."
**Solution**: Understand WHY 3 SPLs helps paper (more surviving processes) and whether that trades off against other opponents.

### Abandoning Promising Approaches

**Problem**: When V12 gets 70/75 wins, moving to completely different V13.
**Solution**: When close to threshold, explore variations of the successful version.

### File Format Issues

**Problem**: Redcode has strict formatting requirements; extra spaces or tabs cause syntax errors.
**Solution**: Test warrior loads correctly before testing against opponents. Use pmars -b to check for assembly errors.

### Ignoring Defensive Design

**Problem**: Pure offense with no consideration for surviving attacks.
**Solution**: Include defensive elements:
- Position-independent code when possible
- Imp backup as last resort
- Process distribution to survive partial kills

### Single Imp Backup

**Problem**: Adding `mov 0, imp` provides minimal backup - single imp easily caught.
**Solution**: Use imp rings or multiple distributed imps for effective backup.

## Resources

### scripts/test_warrior.sh

A template script for systematic warrior testing. Modify the opponent list and paths for the specific task environment.

### references/corewars_fundamentals.md

Mathematical foundations including:
- Step size selection and coprime relationships
- Core coverage calculations
- Process timing and execution order
- Classic warrior archetype characteristics
