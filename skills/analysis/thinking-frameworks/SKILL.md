---
name: thinking-frameworks
description: Collection of mental models and decision-making frameworks (first principles, 5 whys, SWOT, Occam's razor, Pareto, inversion, second-order thinking). Use when analyzing problems, making decisions, evaluating trade-offs, or breaking down complex issues.
---

# Thinking Frameworks & Mental Models

A collection of proven mental models for problem-solving, decision-making, and analysis.

## Quick Reference

| Framework | Use For | Key Question |
|-----------|---------|--------------|
| **First Principles** | Breaking assumptions | What are the fundamental truths? |
| **5 Whys** | Root cause analysis | Why did this happen? (repeat 5x) |
| **SWOT** | Comparing options | Strengths/Weaknesses/Opportunities/Threats? |
| **Occam's Razor** | Simplifying solutions | What's the simplest explanation? |
| **Second-Order** | Long-term consequences | What are the consequences of consequences? |
| **Inversion** | Avoiding failure | How would this fail? |
| **Pareto (80/20)** | Prioritizing effort | Which 20% gives 80% of value? |
| **Opportunity Cost** | Choosing trade-offs | What am I giving up? |
| **One Thing** | Focus | What ONE thing makes everything else easier? |
| **10-10-10** | Time perspective | Impact in 10 min/months/years? |
| **Via Negativa** | Simplifying | What can I remove? |

## Detailed Frameworks

### First Principles Thinking
Strip away assumptions to fundamental truths, then rebuild.

**Process**:
1. State the problem
2. List ALL assumptions (even obvious ones)
3. Challenge each: "Is this actually true?"
4. Identify irreducible truths
5. Rebuild from fundamentals only

**Example**:
```
Problem: Need better pitch detection
Assumptions:
  - Must use time-domain autocorrelation (FALSE - frequency domain works)
  - Need complex algorithm (FALSE - HPS is simple and effective)
  - Accuracy requires YIN (FALSE - HPS achieves ±2 cents)
Fundamental truths:
  - Need to identify fundamental frequency
  - Must work in real-time (<50ms)
  - Target ±2 cent accuracy
Rebuilt solution: Use HPS - simple, fast, accurate enough
```

---

### 5 Whys
Drill to root cause by asking "why" repeatedly.

**Example**:
- **Problem**: Tests failing on CI
- Why? Sample rate mismatch
- Why? Test uses 44100, app uses 48000  
- Why? Test has hardcoded value
- Why? Copied from old codebase
- Why? Didn't check iOS defaults
- **Root**: Assumption about audio defaults

---

### SWOT Analysis
Systematic evaluation of internal/external factors.

```
Algorithm Choice: HPS vs YIN

HPS:
  Strengths: Simple (100 lines), proven, fast O(N log N)
  Weaknesses: Octave errors possible (±20% cases)
  Opportunities: Easy to optimize, well-understood
  Threats: Less effective below 50Hz

YIN:
  Strengths: Academic gold standard
  Weaknesses: Complex FFT (300+ lines), many gotchas
  Opportunities: Potentially higher accuracy
  Threats: Hard to implement correctly

Decision: HPS for v1, consider YIN if accuracy insufficient
```

---

### Occam's Razor
Simplest explanation is usually correct.

**Debugging Application**:
```
Bug: Constant 3-cent sharp error
Complex theory: FFT circular correlation bias, needs windowing correction
Simple theory: Sample rate is wrong
Occam says: Check sample rate first ✓

Result: Using 44100 instead of 48000 → Fix in 1 line
```

---

### Second-Order Thinking
Consider ripple effects beyond immediate consequences.

**Example - Caching Algorithm**:
- 1st order: Faster performance ✓
- 2nd order: Memory usage increases, stale data if settings change
- 3rd order: Need cache invalidation, increased code complexity
- **Decision**: Only cache if performance actually matters

---

### Inversion
Define how to fail, then avoid those paths.

**Pitch Detection Reliability**:
```
Goal: Accurate detection
Inversion: How to guarantee failure?
  1. Wrong sample rate ✗
  2. No window function ✗
  3. Skip interpolation ✗  
  4. Ignore amplitude ✗
  5. Don't test octaves ✗

Production Checklist:
  ✓ Capture sample rate from AVAudioSession
  ✓ Apply Hann window before FFT
  ✓ Use parabolic interpolation
  ✓ Check amplitude threshold
  ✓ Test A1-A6 (55Hz-1760Hz)
```

---

### Pareto Principle (80/20)
Focus on the vital few, not trivial many.

**Application**:
- 80% of bugs come from 20% of code → Focus testing there
- 80% of CPU time in 20% of functions → Optimize those first
- 80% of accuracy from 20% of implementation:
  - Correct sample rate
  - Proper windowing
  - Parabolic interpolation
  
**Anti-pattern**: Spending 80% time on features giving 20% value

---

### Opportunity Cost
Every choice means giving up alternatives.

**Example**:
```
Option A: Implement YIN (3 days)
Opportunity cost:
  - HPS (1 day) + UI polish (2 days)
  - Transposition feature (2 days) + tests (1 day)
  - Documentation (3 days)

Question: Is YIN worth more than alternatives?
Answer: Not unless HPS proves insufficient
```

---

### One Thing Focus
What ONE thing makes everything else easier or unnecessary?

**Questions**:
- Feature work: What's the ONE feature users actually need?
- Bug fixing: What's the ONE root cause of multiple symptoms?
- Optimization: What's the ONE bottleneck?

**Example**:
- Don't optimize 10 minor functions
- Find the ONE hotpath (FFT) and optimize that
- Result: 10x speedup from 1 optimization vs 2x from 10 optimizations

---

### 10-10-10 Rule
Evaluate decisions across time horizons.

**Example - Hardcode vs Config**:
```
Decision: A4 frequency (440 Hz default)

10 minutes: Hardcoding is faster
10 months: Users want customization → Refactor needed
10 years: Standard feature expectation

Decision: Make configurable now (saves 10-month refactor pain)
```

---

### Via Negativa
Improve by removing, not adding.

**Application**:
```
Problem: Complex, buggy YIN implementation

Addition approach:
  + Add more tests
  + Add error handling
  + Add comments
  + Add validation

Subtraction approach:
  - Remove YIN entirely
  - Use simpler HPS
  Result: Fewer bugs, less code, same accuracy

Question always: "What can I remove to make this simpler?"
```

---

## Usage Patterns

### Debugging Workflow
1. **5 Whys** → Root cause
2. **Occam's Razor** → Simplest explanation first
3. **Inversion** → How would this bug happen?

### Architecture Decisions
1. **First Principles** → What do we actually need?
2. **SWOT** → Compare options
3. **Second-Order** → Long-term consequences?
4. **10-10-10** → How will this age?

### Feature Prioritization
1. **Pareto** → Which features give 80% of value?
2. **One Thing** → What's the most important feature?
3. **Opportunity Cost** → What are we giving up?

### Code Review
1. **Via Negativa** → What can we remove?
2. **Occam's Razor** → Is this the simplest solution?
3. **Inversion** → How could this fail?

---

## Combining Frameworks

Complex decisions benefit from multiple frameworks:

**Example - Algorithm Choice**:
```
1. First Principles: Need frequency (Hz) from audio in <50ms
2. SWOT: Compare HPS vs YIN
3. Occam's Razor: HPS is simpler
4. Pareto: HPS gives 80% accuracy with 20% complexity
5. Opportunity Cost: YIN costs 2 extra days
6. 10-10-10: HPS sufficient for v1, can upgrade later

Decision: HPS
Confidence: High (multiple frameworks agree)
```

---

## Anti-Patterns

**Don't use frameworks to**:
- ❌ Justify pre-made decisions (confirmation bias)
- ❌ Avoid deciding (analysis paralysis)
- ❌ Sound smart (intellectual peacocking)
- ❌ Over-analyze simple choices

**Do use frameworks to**:
- ✓ Think clearly about complex problems
- ✓ Challenge your assumptions
- ✓ Communicate reasoning
- ✓ Make better decisions faster

---

## When to Use Which Framework

**Quick decisions** → Occam's Razor, One Thing
**Complex decisions** → First Principles, SWOT, Second-Order
**Prioritization** → Pareto, Opportunity Cost, Eisenhower Matrix
**Risk mitigation** → Inversion, Second-Order
**Simplification** → Via Negativa, Occam's Razor
**Root causes** → 5 Whys, First Principles
