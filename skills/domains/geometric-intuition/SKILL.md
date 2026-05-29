---
name: geometric-intuition
description: Spatial reasoning, coordinate geometry, transformations, and trigonometry for geometric problem solving. Covers Euclidean geometry (points, lines, angles, congruence, similarity), triangle geometry (Pythagorean theorem, laws of sines and cosines), circle geometry (tangent lines, inscribed angles, power of a point), coordinate geometry (distance, midpoint, slope, conic sections), transformations as functions (rotation, reflection, translation, dilation), trigonometry (unit circle, identities, inverse functions), and geometric proof techniques. Use when reasoning about shapes, angles, spatial relationships, coordinate problems, or trigonometric computations.
type: skill
category: math
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/math/geometric-intuition/SKILL.md
superseded_by: null
---
# Geometric Intuition

Geometry is the study of shape, size, position, and the properties of space. It grounds abstract mathematics in spatial reasoning and provides the visual intuition that guides discovery across all mathematical domains. This skill covers Euclidean geometry, coordinate methods, transformations, trigonometry, and geometric proof techniques.

**Agent affinity:** euclid (axiomatic geometry, geometric proofs), euler (coordinate methods, analytic geometry)

**Concept IDs:** math-shape-properties, math-transformations, math-measurement-area, math-coordinate-geometry, math-trigonometry

## Part I — Euclidean Geometry

### Foundational Objects

Euclid's *Elements* (c. 300 BCE) builds geometry from five postulates. The first four are uncontroversial; the fifth (the parallel postulate) generated two millennia of investigation and eventually the discovery of non-Euclidean geometries.

**Points** have no dimension — they represent position only. **Lines** extend infinitely in both directions and are determined by any two distinct points. **Planes** are flat, two-dimensional surfaces extending infinitely.

### Angles

An angle measures the rotation between two rays sharing a common endpoint (vertex).

| Type | Measure | Example |
|---|---|---|
| Acute | 0 < theta < 90 degrees | Interior angles of an equilateral triangle (60 degrees each) |
| Right | theta = 90 degrees | Corner of a rectangle |
| Obtuse | 90 < theta < 180 degrees | Obtuse angle in a 30-30-120 triangle |
| Straight | theta = 180 degrees | A line viewed as an angle |
| Reflex | 180 < theta < 360 degrees | The "outside" of an acute angle |

**Key angle relationships:**
- **Vertical angles** are equal: when two lines cross, opposite angles are congruent.
- **Supplementary angles** sum to 180 degrees.
- **Complementary angles** sum to 90 degrees.
- **Parallel line transversal:** Corresponding angles are equal; alternate interior angles are equal; co-interior (same-side) angles are supplementary.

### Triangle Fundamentals

**The angle sum theorem.** The interior angles of any triangle sum to 180 degrees. (This is equivalent to the parallel postulate in Euclidean geometry; in hyperbolic geometry the sum is less, in spherical geometry it is greater.)

**Triangle classification by sides:** Equilateral (all sides equal), isosceles (at least two equal), scalene (all different). **By angles:** Acute (all angles < 90), right (one angle = 90), obtuse (one angle > 90).

**Triangle inequality.** For any triangle with sides a, b, c: a + b > c, a + c > b, b + c > a. Three positive numbers form a triangle if and only if each is less than the sum of the other two.

### Congruence

Two figures are congruent if one can be transformed into the other by rigid motions (translations, rotations, reflections) — they have the same shape and size.

**Triangle congruence criteria:**
- **SSS (Side-Side-Side):** Three pairs of equal sides.
- **SAS (Side-Angle-Side):** Two pairs of equal sides with the included angle equal.
- **ASA (Angle-Side-Angle):** Two pairs of equal angles with the included side equal.
- **AAS (Angle-Angle-Side):** Two pairs of equal angles with a non-included side equal.
- **HL (Hypotenuse-Leg):** For right triangles, equal hypotenuse and one equal leg.
- **SSA does NOT work in general** (the ambiguous case — can produce 0, 1, or 2 triangles).

### Similarity

Two figures are similar if one can be transformed into the other by a combination of rigid motions and dilation — they have the same shape but possibly different size. The ratio of corresponding sides is the **scale factor** k.

**Triangle similarity criteria:**
- **AA (Angle-Angle):** Two pairs of equal angles (the third is forced by the angle sum theorem).
- **SAS similarity:** One pair of equal angles with the adjacent sides in proportion.
- **SSS similarity:** All three pairs of sides in the same ratio.

**Worked example.** *In triangle ABC, DE is parallel to BC with D on AB and E on AC. Prove triangle ADE is similar to triangle ABC.*

**Proof.** Since DE is parallel to BC, angle ADE = angle ABC (corresponding angles with transversal AB) and angle AED = angle ACB (corresponding angles with transversal AC). By AA similarity, triangle ADE ~ triangle ABC.

## Part II — Triangle Geometry

### The Pythagorean Theorem

In a right triangle with legs a, b and hypotenuse c: a^2 + b^2 = c^2.

**Proof (Euclid, Elements I.47).** Construct squares on each side of the right triangle. The square on the hypotenuse can be dissected into two rectangles, each equal in area to one of the leg squares, established by the congruence of triangles formed by dropping an altitude from the right angle to the hypotenuse.

**Converse.** If a^2 + b^2 = c^2 for a triangle with sides a, b, c, then the angle opposite c is a right angle.

**Generalization.** If the angle C opposite side c satisfies c^2 = a^2 + b^2 - 2ab*cos(C) (law of cosines), then the Pythagorean theorem is the special case C = 90 degrees (where cos(90) = 0).

### The Law of Sines

For any triangle with sides a, b, c opposite angles A, B, C:

a/sin(A) = b/sin(B) = c/sin(C) = 2R

where R is the circumradius (radius of the circumscribed circle).

**When to use.** When you know an angle and its opposite side, plus one other piece (AAS or ASA configurations).

**The ambiguous case (SSA).** Given angle A, side a, and side b: if a < b*sin(A), no triangle exists; if a = b*sin(A), exactly one (right) triangle; if b*sin(A) < a < b, two triangles; if a >= b, one triangle.

### The Law of Cosines

c^2 = a^2 + b^2 - 2ab*cos(C)

**When to use.** When you know SAS (two sides and the included angle) or SSS (all three sides, solving for an angle).

**Worked example.** *In a triangle with a = 5, b = 7, C = 60 degrees, find c.*

c^2 = 25 + 49 - 2(5)(7)cos(60) = 74 - 70(0.5) = 74 - 35 = 39. So c = sqrt(39) approximately 6.245.

## Part III — Circle Geometry

### Fundamental Properties

A circle is the set of all points at distance r (the radius) from a center point O. The diameter d = 2r. Circumference = 2*pi*r. Area = pi*r^2.

### Tangent Lines

A tangent to a circle at point P is perpendicular to the radius OP. Two tangent segments from an external point to a circle are equal in length.

### Inscribed Angles

**Inscribed angle theorem.** An inscribed angle (vertex on the circle, sides are chords) is half the central angle subtending the same arc. Consequence: all inscribed angles subtending the same arc are equal.

**Thales' theorem (special case).** An inscribed angle subtending a diameter is a right angle.

### Power of a Point

For a point P and a circle, the **power** of P is d^2 - r^2, where d is the distance from P to the center.

- If two chords through P intersect the circle at A, B and C, D respectively: PA * PB = PC * PD.
- If a secant through P meets the circle at A, B and a tangent from P touches at T: PA * PB = PT^2.

This invariant simplifies many circle geometry problems.

### Cyclic Quadrilaterals

A quadrilateral is cyclic (inscribable in a circle) if and only if opposite angles sum to 180 degrees. **Ptolemy's theorem** for cyclic quadrilaterals ABCD: AC * BD = AB * CD + AD * BC.

## Part IV — Coordinate Geometry

### The Coordinate Plane

Descartes' coordinate system (Cartesian plane) maps geometric objects to algebraic equations and vice versa, bridging geometry and algebra.

### Core Formulas

**Distance.** Between (x_1, y_1) and (x_2, y_2): d = sqrt((x_2 - x_1)^2 + (y_2 - y_1)^2).

**Midpoint.** ((x_1 + x_2)/2, (y_1 + y_2)/2).

**Slope.** m = (y_2 - y_1)/(x_2 - x_1). Undefined for vertical lines.

**Parallel lines** have equal slopes. **Perpendicular lines** have slopes whose product is -1 (m_1 * m_2 = -1), provided neither is vertical.

### Line Equations

- **Slope-intercept:** y = mx + b
- **Point-slope:** y - y_1 = m(x - x_1)
- **General form:** ax + by + c = 0
- **Distance from point (x_0, y_0) to line ax + by + c = 0:** |ax_0 + by_0 + c| / sqrt(a^2 + b^2)

### Conic Sections

The conic sections — circle, ellipse, parabola, hyperbola — arise from slicing a cone with a plane (Apollonius, c. 200 BCE).

| Conic | Standard form (centered at origin) | Eccentricity |
|---|---|---|
| Circle | x^2 + y^2 = r^2 | e = 0 |
| Ellipse | x^2/a^2 + y^2/b^2 = 1 (a > b > 0) | 0 < e < 1, e = c/a where c^2 = a^2 - b^2 |
| Parabola | y = (1/(4p))x^2 or x = (1/(4p))y^2 | e = 1 |
| Hyperbola | x^2/a^2 - y^2/b^2 = 1 | e > 1, e = c/a where c^2 = a^2 + b^2 |

**Worked example.** *Find the foci of the ellipse x^2/25 + y^2/9 = 1.*

Here a^2 = 25, b^2 = 9, so c^2 = 25 - 9 = 16, c = 4. The foci are at (+/-4, 0).

## Part V — Transformations as Functions

Transformations are functions from the plane to itself. Rigid motions (isometries) preserve distance; similarity transformations preserve shape.

### Translation

T(x, y) = (x + a, y + b). Every point moves by the same vector (a, b). Preserves distances, angles, and orientation.

### Rotation

R_theta(x, y) = (x*cos(theta) - y*sin(theta), x*sin(theta) + y*cos(theta)). Rotates counterclockwise by theta about the origin. Preserves distances and angles.

### Reflection

Across the x-axis: (x, y) -> (x, -y). Across the y-axis: (x, y) -> (-x, y). Across y = x: (x, y) -> (y, x). Preserves distances but reverses orientation.

### Dilation

D_k(x, y) = (kx, ky) for scale factor k > 0. Preserves angles but scales all distances by k. Preserves shape (similarity) but not size (unless k = 1).

### Composition

Transformations compose: applying R then T gives T(R(x, y)). The composition of two reflections across parallel lines is a translation; the composition of two reflections across intersecting lines is a rotation by twice the angle between the lines.

## Part VI — Trigonometry

### The Unit Circle

The unit circle x^2 + y^2 = 1 defines the trigonometric functions: for an angle theta measured counterclockwise from the positive x-axis, the point on the unit circle is (cos(theta), sin(theta)).

**Key values:**

| theta (degrees) | theta (radians) | sin(theta) | cos(theta) | tan(theta) |
|---|---|---|---|---|
| 0 | 0 | 0 | 1 | 0 |
| 30 | pi/6 | 1/2 | sqrt(3)/2 | 1/sqrt(3) |
| 45 | pi/4 | sqrt(2)/2 | sqrt(2)/2 | 1 |
| 60 | pi/3 | sqrt(3)/2 | 1/2 | sqrt(3) |
| 90 | pi/2 | 1 | 0 | undefined |

### Fundamental Identities

**Pythagorean:** sin^2(theta) + cos^2(theta) = 1. Dividing by cos^2 or sin^2 gives: 1 + tan^2(theta) = sec^2(theta), 1 + cot^2(theta) = csc^2(theta).

**Angle addition:**
- sin(A + B) = sin(A)cos(B) + cos(A)sin(B)
- cos(A + B) = cos(A)cos(B) - sin(A)sin(B)
- tan(A + B) = (tan(A) + tan(B)) / (1 - tan(A)tan(B))

**Double angle:**
- sin(2A) = 2sin(A)cos(A)
- cos(2A) = cos^2(A) - sin^2(A) = 2cos^2(A) - 1 = 1 - 2sin^2(A)

**Half angle:**
- sin^2(A/2) = (1 - cos(A))/2
- cos^2(A/2) = (1 + cos(A))/2

### Inverse Trigonometric Functions

arcsin(x) is defined for x in [-1, 1] with range [-pi/2, pi/2]. arccos(x) is defined for x in [-1, 1] with range [0, pi]. arctan(x) is defined for all real x with range (-pi/2, pi/2).

**Worked example.** *Solve 2sin^2(x) - sin(x) - 1 = 0 for x in [0, 2*pi).*

Let u = sin(x). Then 2u^2 - u - 1 = 0, so (2u + 1)(u - 1) = 0. Thus u = -1/2 or u = 1.

sin(x) = 1 gives x = pi/2. sin(x) = -1/2 gives x = 7*pi/6 and x = 11*pi/6.

Solutions: x = pi/2, 7*pi/6, 11*pi/6.

## Part VII — Geometric Proof Techniques

### Synthetic Proofs

Synthetic (axiomatic) proofs reason directly from definitions, postulates, and previously proven theorems without coordinates. Euclid's *Elements* is entirely synthetic.

**Strategy:** Identify congruent or similar triangles. Most Euclidean geometry proofs reduce to showing two triangles are congruent (via SSS, SAS, ASA, AAS, or HL) or similar (via AA, SAS, or SSS similarity).

### Coordinate Proofs

Assign coordinates strategically, then compute algebraically.

**Worked example.** *Prove that the diagonals of a parallelogram bisect each other.*

**Proof.** Place the parallelogram with vertices at A = (0, 0), B = (a, 0), C = (a + b, c), D = (b, c). Midpoint of AC: ((a + b)/2, c/2). Midpoint of BD: ((a + b)/2, c/2). The midpoints are identical, so the diagonals bisect each other.

### Proof by Transformation

Show that a transformation mapping one figure to another preserves the property in question.

**Worked example.** *Prove that reflections preserve distance.*

**Proof.** The reflection across the x-axis maps (x, y) to (x, -y). The distance between (x_1, y_1) and (x_2, y_2) is sqrt((x_2 - x_1)^2 + (y_2 - y_1)^2). The distance between their images (x_1, -y_1) and (x_2, -y_2) is sqrt((x_2 - x_1)^2 + (-y_2 + y_1)^2) = sqrt((x_2 - x_1)^2 + (y_2 - y_1)^2). Equal.

### Visualization Guidance

When approaching a geometry problem:
1. **Draw an accurate figure.** Many insights come from seeing the picture. Label all known quantities.
2. **Mark equal lengths and angles.** Use tick marks for equal sides, arcs for equal angles.
3. **Draw auxiliary lines.** Common additions: altitudes, medians, angle bisectors, lines through centers, extensions of sides.
4. **Look for hidden triangles.** Especially right triangles and similar triangles.
5. **Consider extreme cases.** What happens as a point approaches a boundary?

## When to Use This Skill

- Reasoning about shapes, angles, distances, areas, or volumes
- Solving coordinate geometry problems (lines, conics, intersections)
- Working with trigonometric equations or identities
- Proving geometric properties (congruence, similarity, parallelism)
- Visualizing mathematical relationships

## When NOT to Use This Skill

- For algebraic equation solving without geometric context — use algebraic-reasoning
- For calculus-based area/volume computation — use numerical-analysis
- For proof strategy selection — use proof-techniques
- For probability in geometric settings — use mathematical-modeling

## Cross-References

- **euclid agent:** Axiomatic geometry, synthetic proofs, construction problems. Named for Euclid of Alexandria, whose *Elements* is the most influential mathematics textbook ever written.
- **euler agent:** Analytic and coordinate geometry, connections between geometry and analysis. Named for Leonhard Euler, who unified geometry with algebra and analysis.
- **proof-techniques skill:** General proof methods applicable to geometric theorems.
- **algebraic-reasoning skill:** Algebraic manipulation used in coordinate geometry proofs.
- **numerical-analysis skill:** Computational geometry and numerical methods for geometric problems.

## References

- Euclid (c. 300 BCE). *Elements*. Translated by Heath, T. L. (1908). Cambridge University Press.
- Coxeter, H. S. M. (1969). *Introduction to Geometry*. 2nd edition. Wiley.
- Hartshorne, R. (2000). *Geometry: Euclid and Beyond*. Springer UTM.
- Moise, E. E. (1990). *Elementary Geometry from an Advanced Standpoint*. 3rd edition. Addison-Wesley.
- Pedoe, D. (1988). *Geometry: A Comprehensive Course*. Dover.
- Stewart, J. (2015). *Calculus: Early Transcendentals*. 8th edition. Cengage. (Chapters on analytic geometry and trigonometry.)
