---
name: experimental-methods
description: Experimental methods for physics including measurement, uncertainty analysis, and experimental design. Covers the scientific method applied to physics, the SI unit system, significant figures, uncertainty and error analysis (systematic vs. random, propagation of uncertainty), dimensional analysis (Buckingham Pi theorem), experimental design (controls, variables, reproducibility), data analysis (linear regression, chi-squared, curve fitting), lab safety, landmark physics experiments (Millikan, Cavendish, photoelectric effect, Michelson-Morley), graphical analysis, and order-of-magnitude estimation (Fermi problems). Use when designing experiments, analyzing data, reporting measurements, or making back-of-the-envelope estimates.
type: skill
category: physics
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/physics/experimental-methods/SKILL.md
superseded_by: null
---
# Experimental Methods

Physics is an empirical science. Every theory must survive confrontation with experiment, and every experiment must be designed, conducted, and analyzed with rigorous methodology. This skill covers the practical foundations of experimental physics: measurement, uncertainty, dimensional analysis, experimental design, data analysis, and the landmark experiments that shaped our understanding. It also covers Fermi estimation — the physicist's art of getting useful answers from minimal information.

**Agent affinity:** faraday (pedagogy, Sonnet), curie (department chair, Opus)

**Concept IDs:** phys-motion-kinematics, phys-wave-properties (measurement context)

## Experimental Methods at a Glance

| # | Topic | Key idea |
|---|---|---|
| 1 | Scientific method | Hypothesis -> prediction -> experiment -> analysis -> revision |
| 2 | SI units | Seven base units; all physics quantities derived from them |
| 3 | Significant figures | Report precision honestly |
| 4 | Uncertainty & error analysis | Quantify how much you trust your result |
| 5 | Dimensional analysis | Units constrain possible equations |
| 6 | Experimental design | Controls, variables, reproducibility |
| 7 | Data analysis | Regression, chi-squared, curve fitting |
| 8 | Graphical analysis | Linearize to extract parameters |
| 9 | Landmark experiments | The experiments that built physics |
| 10 | Fermi estimation | Order-of-magnitude reasoning |
| 11 | Lab safety | Practical hazard awareness |

## Topic 1 — The Scientific Method in Physics

**The cycle:**
1. **Observe** a phenomenon.
2. **Hypothesize** a mechanism or relationship.
3. **Predict** quantitative consequences.
4. **Experiment** to test the predictions.
5. **Analyze** data; compare with predictions.
6. **Revise** the hypothesis if predictions fail; confirm (tentatively) if they succeed.

**Key discipline.** A theory is not proved by experiment — it is merely not yet disproved. A single reproducible disagreement between theory and experiment can overthrow a theory that has survived millions of confirmations. This asymmetry between confirmation and falsification (Popper, 1934) is the logical structure of empirical science.

**Reproducibility.** An experiment that cannot be independently reproduced is not evidence. The design, procedure, and raw data must be documented in sufficient detail for others to replicate the result.

## Topic 2 — The SI Unit System

**Seven base units:**

| Quantity | Unit | Symbol |
|---|---|---|
| Length | meter | m |
| Mass | kilogram | kg |
| Time | second | s |
| Electric current | ampere | A |
| Temperature | kelvin | K |
| Amount of substance | mole | mol |
| Luminous intensity | candela | cd |

**All other physical quantities** are derived from these. Examples: force (N = kg m/s^2), energy (J = kg m^2/s^2), pressure (Pa = kg/(m s^2)), voltage (V = kg m^2/(A s^3)).

**SI prefixes:** From yocto (10^-24) to yotta (10^24). Common in physics: nano (10^-9), micro (10^-6), milli (10^-3), kilo (10^3), mega (10^6), giga (10^9).

**Unit consistency.** Every term in a physics equation must have the same dimensions. If your answer comes out in "meters per kilogram," something is wrong. Always check units before and after calculation.

## Topic 3 — Significant Figures

**Rules:**
1. All nonzero digits are significant. (4.53 has 3 sig figs.)
2. Zeros between nonzero digits are significant. (1.003 has 4 sig figs.)
3. Leading zeros are not significant. (0.0045 has 2 sig figs.)
4. Trailing zeros after a decimal point are significant. (2.300 has 4 sig figs.)
5. Trailing zeros with no decimal point are ambiguous. (1500 could be 2, 3, or 4 sig figs — use scientific notation to be clear: 1.50 * 10^3 has 3 sig figs.)

**Arithmetic rules:**
- **Multiplication/division:** Result has the same number of sig figs as the input with the fewest.
- **Addition/subtraction:** Result has the same number of decimal places as the input with the fewest.

**Important caveat.** Significant figures are a rough method for tracking precision. For serious experimental work, use explicit uncertainty analysis (Topic 4) instead.

## Topic 4 — Uncertainty and Error Analysis

### Types of Error

**Systematic errors** shift all measurements in the same direction. Examples: a miscalibrated instrument, a consistently misread scale, air resistance neglected in a free-fall experiment. Systematic errors are not reduced by repeating measurements — they must be identified and corrected.

**Random errors** cause measurements to scatter unpredictably around the true value. Examples: timing variations in manual stopwatch use, electronic noise. Random errors are reduced by averaging multiple measurements.

**Accuracy vs. precision.** Accuracy is how close the measurement is to the true value (affected by systematic errors). Precision is how reproducible the measurement is (affected by random errors). A measurement can be precise but inaccurate (tight cluster far from center), accurate but imprecise (scattered around center), or both or neither.

### Reporting Uncertainty

**Standard form:** x = x_best +/- delta_x (units). Example: L = 1.53 +/- 0.02 m.

**The uncertainty delta_x** is typically the standard deviation of the mean (for repeated measurements) or the instrument resolution (for single measurements): delta_x = sigma / sqrt(N) for N repeated measurements.

### Propagation of Uncertainty

When a result depends on several measured quantities, how does the uncertainty propagate?

**For f = f(x, y, z):**

delta_f = sqrt((df/dx)^2 (delta_x)^2 + (df/dy)^2 (delta_y)^2 + (df/dz)^2 (delta_z)^2)

**Common special cases:**
- **Addition/subtraction:** f = x + y. delta_f = sqrt(delta_x^2 + delta_y^2).
- **Multiplication/division:** f = xy. delta_f/f = sqrt((delta_x/x)^2 + (delta_y/y)^2).
- **Power:** f = x^n. delta_f/f = |n| delta_x/x.

**Worked example.** *You measure the period of a pendulum as T = 2.05 +/- 0.03 s and the length as L = 1.04 +/- 0.01 m. Calculate g from T = 2 pi sqrt(L/g) and its uncertainty.*

**Solution.** g = 4 pi^2 L / T^2 = 4 * 9.87 * 1.04 / 4.2025 = 9.77 m/s^2.

Fractional uncertainties: delta_L/L = 0.01/1.04 = 0.0096. delta_T/T = 0.03/2.05 = 0.0146. Since g proportional to L / T^2: delta_g/g = sqrt((delta_L/L)^2 + (2 delta_T/T)^2) = sqrt(0.0096^2 + 0.0293^2) = sqrt(0.000092 + 0.000858) = sqrt(0.000950) = 0.0308.

delta_g = 0.0308 * 9.77 = 0.30 m/s^2. Result: g = 9.8 +/- 0.3 m/s^2.

## Topic 5 — Dimensional Analysis

**Principle.** Every valid physics equation must be dimensionally consistent. This provides a powerful constraint on possible relationships between variables.

**Uses:**
1. **Checking equations.** If the dimensions do not match, the equation is wrong.
2. **Deriving functional forms.** If you know which variables a quantity depends on, dimensional analysis can determine the functional form up to a dimensionless constant.

**Buckingham Pi theorem.** If a physical quantity depends on n variables involving k independent dimensions, then the relationship can be expressed in terms of (n - k) independent dimensionless groups (Pi groups).

**Worked example.** *Find the period of a simple pendulum using dimensional analysis. The period T might depend on length L, mass m, and gravitational acceleration g.*

**Solution.** Assume T = C L^a m^b g^c, where C is dimensionless.

Dimensions: [T] = [L]^a [M]^b [L/T^2]^c = L^(a+c) M^b T^(-2c).

Matching: For T: 1 = -2c, so c = -1/2. For L: 0 = a + c = a - 1/2, so a = 1/2. For M: 0 = b.

Therefore T = C sqrt(L/g). The mass does not appear. Dimensional analysis cannot determine C, but the full derivation gives C = 2 pi.

**When dimensional analysis fails.** It cannot determine dimensionless constants, and it cannot discover relationships between quantities with the same dimensions (e.g., distinguishing kinetic and potential energy).

## Topic 6 — Experimental Design

**Independent variable:** The quantity you deliberately vary.
**Dependent variable:** The quantity you measure in response.
**Controlled variables:** Everything else, held constant.

**Control group.** A baseline experiment with no treatment, used for comparison. Essential for isolating the effect of the independent variable.

**Randomization and blinding.** Reduce bias by randomizing the order of measurements and, where possible, blinding the experimenter to which condition is being tested.

**Reproducibility checklist:**
1. Document all equipment (model, serial number, calibration date).
2. Record all environmental conditions (temperature, pressure, humidity).
3. Describe the procedure in enough detail for a stranger to replicate it.
4. Report raw data, not just processed results.
5. Archive data in a durable format.

## Topic 7 — Data Analysis

### Linear Regression (Least Squares)

**Purpose.** Fit a straight line y = mx + b to data points (x_i, y_i) by minimizing the sum of squared residuals.

**Formulas:**
m = (N sum(x_i y_i) - sum(x_i) sum(y_i)) / (N sum(x_i^2) - (sum(x_i))^2)
b = (sum(y_i) - m sum(x_i)) / N

**Uncertainty in slope:** delta_m = sigma_y sqrt(N / (N sum(x_i^2) - (sum(x_i))^2)), where sigma_y is the standard deviation of residuals.

### Chi-Squared Test

**Purpose.** Quantify how well a model fits the data, accounting for measurement uncertainties.

chi^2 = sum over i of ((y_i - f(x_i))^2 / sigma_i^2)

**Interpretation:** chi^2 / (degrees of freedom) approximately equal to 1 indicates a good fit. Much greater than 1 indicates a poor fit or underestimated uncertainties. Much less than 1 suggests overestimated uncertainties.

### Curve Fitting

**Strategy for nonlinear models.** Whenever possible, transform the data to make the relationship linear.

| Physical relationship | Transformation | Linear form |
|---|---|---|
| y = ax^n | Plot ln(y) vs ln(x) | ln(y) = n ln(x) + ln(a) |
| y = ae^(bx) | Plot ln(y) vs x | ln(y) = bx + ln(a) |
| y = a/(x + b) | Plot 1/y vs x | 1/y = x/a + b/a |

**Worked example.** *You suspect that the period T of a mass-spring system depends on mass m as T = C m^n. You measure T for five masses and plot ln(T) vs ln(m). The slope is 0.498 +/- 0.012. What is n?*

**Solution.** n = 0.498 +/- 0.012. Within uncertainty, n = 1/2, confirming T proportional to sqrt(m), consistent with T = 2 pi sqrt(m/k).

## Topic 8 — Graphical Analysis

**Principles:**
1. **Plot the data.** Before any numerical analysis, look at the graph. Human pattern recognition catches outliers, nonlinearity, and systematic trends that statistics alone may miss.
2. **Include error bars.** Every data point should show its uncertainty as an error bar.
3. **Label axes.** Include the quantity name, symbol, and units. Example: "Period T (s)".
4. **Draw the best-fit line through the error bars**, not through the points. A good fit passes through most error bars.
5. **Extract physical parameters from the graph.** Slope and intercept correspond to physical constants.

**Residual plots.** After fitting, plot the residuals (data minus fit). Random scatter indicates a good fit. Systematic patterns (curvature, trends) indicate that the model is wrong or that systematic errors are present.

## Topic 9 — Landmark Physics Experiments

### Millikan Oil Drop Experiment (1909)

**Purpose:** Measure the charge of the electron.
**Method:** Suspend charged oil droplets between parallel plates by balancing gravitational and electric forces. Vary the voltage until a droplet hovers.
**Result:** Charges are always integer multiples of e = 1.602 * 10^-19 C. Charge is quantized.
**Lesson:** Elegant experimental design extracts fundamental constants from macroscopic observations.

### Cavendish Experiment (1798)

**Purpose:** Measure the gravitational constant G and "weigh the Earth."
**Method:** A torsion balance measures the tiny gravitational attraction between lead spheres.
**Result:** G = 6.674 * 10^-11 N m^2/kg^2 (modern value). Combined with g and R_Earth, this gives M_Earth = 5.97 * 10^24 kg.
**Lesson:** Extraordinary sensitivity (detecting forces of ~10^-7 N) achieved through careful mechanical design.

### Photoelectric Effect Experiments (Lenard, 1902; Millikan, 1916)

**Purpose:** Test Einstein's photon hypothesis.
**Method:** Illuminate a metal surface with light of varying frequency and intensity; measure the ejected electron energies via stopping voltage.
**Result:** KE_max = hf - phi. Confirmed the quantum nature of light.
**Lesson:** Sometimes the data forces a paradigm shift (classical wave theory predicted wrong dependences).

### Michelson-Morley Experiment (1887)

**Purpose:** Detect the Earth's motion through the luminiferous ether.
**Method:** Split a light beam, send halves along perpendicular paths, recombine, and look for interference fringe shifts as the apparatus rotates.
**Result:** Null result — no fringe shift detected. The speed of light is the same in all directions.
**Lesson:** The most important null result in physics history. Led directly to special relativity.

### Rutherford Scattering (1911)

**Purpose:** Determine the structure of the atom.
**Method:** Fire alpha particles at gold foil and measure scattering angles.
**Result:** Most alpha particles pass through; a few scatter at large angles. The atom has a tiny, dense, positive nucleus.
**Lesson:** Unexpected results are the most valuable — Rutherford called the large-angle scattering "as if you fired a cannon shell at tissue paper and it came back and hit you."

## Topic 10 — Fermi Estimation (Order-of-Magnitude Problems)

**The Fermi method.** Break a complex question into smaller pieces, estimate each piece, and combine. The goal is not a precise answer but the correct order of magnitude (power of 10).

**Why it works.** Individual estimates may be off by a factor of 2-3 in either direction, but errors tend to partially cancel when multiplied together. The final answer is typically within a factor of 10 of the true value.

**Worked example.** *How many piano tuners are there in Chicago?*

**Solution (Fermi's original example).**
- Chicago population: ~3 million
- Average household size: ~2.5, so ~1.2 million households
- Fraction with pianos: ~1 in 10, so ~120,000 pianos
- Each piano tuned once per year
- A tuner does ~4 tunings per day, ~250 days per year = ~1000 tunings/year
- Piano tuners needed: 120,000 / 1000 = ~120

The actual number is approximately 100-200. The estimate is correct to within a factor of 2.

**Worked example.** *Estimate the total energy output of the Sun.*

**Solution.**
- Solar constant at Earth: ~1400 W/m^2 (measured)
- Earth-Sun distance: ~1.5 * 10^11 m
- The Sun radiates isotropically over a sphere: A = 4 pi r^2 = 4 pi (1.5e11)^2 = 2.83e23 m^2
- Total power: L = 1400 * 2.83e23 = 3.96e26 W

The accepted value is 3.846 * 10^26 W. The estimate is within 3%.

**Fermi estimation strategy:**
1. Identify the quantity to estimate.
2. Break it into factors you can estimate individually.
3. Estimate each factor, rounding to one significant figure.
4. Multiply (or add/subtract as appropriate).
5. State the answer as an order of magnitude.
6. Sanity-check against known facts.

## Topic 11 — Lab Safety

**General principles:**
- Know the location of emergency shutoffs, fire extinguishers, and first aid kits before starting any experiment.
- Wear appropriate PPE: safety glasses for optics/projectile labs, closed-toe shoes always, lab coats for chemistry-adjacent experiments.
- Never look directly into a laser beam or its reflections.
- High voltage equipment: always work with one hand behind your back (prevents current path across the heart). Use a buddy system.
- Radioactive sources: maintain distance, minimize exposure time, use shielding. Follow ALARA (As Low As Reasonably Achievable).
- Cryogenics (liquid nitrogen, liquid helium): frostbite risk; ensure adequate ventilation (displaces oxygen); use insulated gloves and face shield.
- Report all incidents, including near-misses.

## When to Use This Skill

- Designing a physics experiment from scratch
- Analyzing experimental data (regression, uncertainty, chi-squared)
- Reporting measurements with proper uncertainty
- Checking equations using dimensional analysis
- Making quick estimates of physical quantities (Fermi problems)
- Understanding how landmark experiments established fundamental physics

## When NOT to Use This Skill

- **Solving theoretical physics problems without experimental context:** Use the relevant domain skill (classical-mechanics, electromagnetism, etc.).
- **Statistical methods beyond physics (social science, biology):** The core techniques transfer, but field-specific conventions differ.
- **Engineering tolerances and manufacturing precision:** This skill covers scientific measurement; engineering standards involve additional considerations.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Reporting more sig figs than the data supports | Implies false precision | Round the final answer to match the least precise input |
| Ignoring systematic errors | Averaging does not reduce systematic bias | Identify and correct systematic errors before analyzing random ones |
| Adding uncertainties instead of adding in quadrature | Overestimates total uncertainty | Use delta_f = sqrt(sum of (partial derivative * delta)^2) |
| Forcing a line through the origin | The intercept may have physical meaning | Let the fit determine the intercept unless theory demands zero |
| Discarding outliers without justification | May discard valid data | Only discard outliers with a documented physical reason |
| Conflating correlation with causation | Two correlated quantities may share a common cause | Establish a causal mechanism; use controlled experiments |

## Cross-References

- **faraday agent:** Primary pedagogy agent. Excels at making experimental methods accessible and concrete. Sonnet-class.
- **curie agent:** Department chair, Opus-class. Coordinates experimental methods across all physics sub-disciplines.
- **newton agent:** For mechanics experiments (pendulum, inclined plane, collisions).
- **maxwell agent:** For electromagnetic experiments (circuits, Faraday's law, optics labs).
- **boltzmann agent:** For thermal experiments (calorimetry, gas laws, heat conduction).
- **all domain skills:** Experimental methods apply across all physics domains. Every skill benefits from proper uncertainty analysis, dimensional checking, and experimental design.

## References

- Taylor, J. R. (1997). *An Introduction to Error Analysis*. 2nd edition. University Science Books.
- Bevington, P. R., & Robinson, D. K. (2003). *Data Reduction and Error Analysis for the Physical Sciences*. 3rd edition. McGraw-Hill.
- Baird, D. C. (1995). *Experimentation: An Introduction to Measurement Theory and Experiment Design*. 3rd edition. Prentice Hall.
- Hughes, I., & Hase, T. (2010). *Measurements and their Uncertainties*. Oxford University Press.
- Weinberg, S. (2015). *To Explain the World: The Discovery of Modern Science*. Harper.
- Buckingham, E. (1914). "On physically similar systems; illustrations of the use of dimensional equations." *Physical Review*, 4(4), 345-376.
- Millikan, R. A. (1913). "On the elementary electrical charge and the Avogadro constant." *Physical Review*, 2(2), 109-143.
- Michelson, A. A., & Morley, E. W. (1887). "On the relative motion of the Earth and the luminiferous ether." *American Journal of Science*, 34, 333-345.
