---
name: classical-mechanics
description: Classical mechanics from kinematics through rotational dynamics and oscillations. Covers 1D/2D/3D motion, Newton's three laws, free-body diagrams, friction, projectile motion, circular motion, rotational mechanics, gravitation and orbits, work-energy theorem, conservation of momentum, collisions, and simple harmonic motion. Use when analyzing forces, trajectories, orbital mechanics, or any problem where objects move under deterministic forces at non-relativistic speeds.
type: skill
category: physics
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/physics/classical-mechanics/SKILL.md
superseded_by: null
---
# Classical Mechanics

Classical mechanics is the branch of physics that describes the motion of macroscopic objects under the action of forces. Founded by Newton in the *Principia* (1687) and refined through the analytical frameworks of Lagrange, Hamilton, and others, it remains the foundation for engineering, orbital mechanics, and everyday physical reasoning. This skill covers kinematics, dynamics, energy, momentum, rotation, gravitation, and oscillations with worked examples and strategy guidance.

**Agent affinity:** newton (classical mechanics, Opus)

**Concept IDs:** phys-motion-kinematics, phys-newtons-laws, phys-projectile-motion, phys-circular-motion, phys-gravitation

## Classical Mechanics at a Glance

| # | Topic | Key equations | Core idea |
|---|---|---|---|
| 1 | Kinematics (1D) | x = x_0 + v_0 t + (1/2)a t^2 | Describe motion without asking why |
| 2 | Newton's Laws | F_net = ma | Force causes acceleration |
| 3 | Free-body diagrams | Sum of forces = ma per axis | Visual decomposition of all forces |
| 4 | Friction | f_s <= mu_s N, f_k = mu_k N | Resists relative motion |
| 5 | Projectile motion | Independent x and y components | Parabolic trajectory under gravity |
| 6 | Circular motion | a_c = v^2/r, F_c = mv^2/r | Centripetal acceleration toward center |
| 7 | Rotational mechanics | tau = I alpha, L = I omega | Angular analogs of force and momentum |
| 8 | Gravitation | F = GMm/r^2, orbits via Kepler's laws | Universal attraction |
| 9 | Work-energy theorem | W_net = Delta KE | Net work equals change in kinetic energy |
| 10 | Momentum | p = mv, impulse J = F Delta t | Conserved when no external forces act |
| 11 | Collisions | Elastic: KE conserved. Inelastic: KE lost | Momentum always conserved in isolation |
| 12 | Oscillations | x(t) = A cos(omega t + phi) | Restoring force proportional to displacement |

## Topic 1 — Kinematics in One Dimension

**Core idea.** Kinematics describes *how* objects move — position, velocity, acceleration — without explaining *why*. It is the prerequisite for dynamics.

**The five kinematic equations** (constant acceleration):

1. v = v_0 + at
2. x = x_0 + v_0 t + (1/2)a t^2
3. v^2 = v_0^2 + 2a(x - x_0)
4. x = x_0 + (1/2)(v + v_0)t
5. x = x_0 + vt - (1/2)a t^2

**Strategy.** List knowns (three of five: x, x_0, v, v_0, a, t). Pick the equation that uses your three knowns and one unknown. Solve algebraically before substituting numbers.

**Worked example.** *A car accelerates from rest at 3 m/s^2 for 5 seconds. How far does it travel?*

**Solution.** Known: v_0 = 0, a = 3 m/s^2, t = 5 s. Unknown: x - x_0. Use equation 2:
x - x_0 = v_0 t + (1/2)a t^2 = 0 + (1/2)(3)(25) = 37.5 m.

**Extension to 2D/3D.** Treat each coordinate axis independently. The kinematic equations apply component-wise: x(t), y(t), z(t) each evolve under their own acceleration component.

## Topic 2 — Newton's Three Laws

**First Law (Inertia).** An object at rest stays at rest, and an object in uniform motion stays in uniform motion, unless acted on by a net external force. This defines inertial reference frames.

**Second Law (F = ma).** The net force on an object equals its mass times its acceleration: F_net = ma. This is the engine of classical mechanics — given forces, compute acceleration; given acceleration, infer forces.

**Third Law (Action-Reaction).** For every force that object A exerts on object B, object B exerts an equal and opposite force on A. These forces act on different objects and never cancel each other in a free-body diagram.

**Worked example.** *A 5 kg block is pushed across a frictionless surface by a 20 N horizontal force. Find its acceleration.*

**Solution.** F_net = ma. The only horizontal force is 20 N. So a = F/m = 20/5 = 4 m/s^2.

**Common mistake.** Applying action-reaction pairs to the same object. If you push a wall and the wall pushes back, those forces act on different objects (you and the wall). They do not cancel.

## Topic 3 — Free-Body Diagrams

**Purpose.** A free-body diagram (FBD) isolates a single object and shows every force acting on it as a vector arrow. It is the essential first step for any force problem.

**Procedure:**
1. Identify the object of interest.
2. Draw it as a dot or simple shape.
3. Draw all forces acting ON that object: weight (mg, downward), normal force (perpendicular to surface), friction (parallel to surface, opposing motion), tension, applied forces, spring forces.
4. Choose a coordinate system (often tilted for inclined planes).
5. Decompose forces into components.
6. Apply Newton's second law per axis.

**Worked example.** *A 10 kg block rests on a 30-degree incline. Find the normal force and the friction force required to keep it stationary.*

**Solution.** Tilt coordinates: x along the incline (positive up-slope), y perpendicular to incline.

Forces: Weight W = mg = 98 N (vertically down). Decompose: W_x = mg sin(30) = 49 N (down-slope), W_y = mg cos(30) = 84.9 N (into surface).

y-axis: N - W_y = 0, so N = 84.9 N.
x-axis: f_s - W_x = 0, so f_s = 49 N (up-slope).

## Topic 4 — Friction

**Static friction:** f_s <= mu_s N. The force adjusts up to a maximum before sliding begins.

**Kinetic friction:** f_k = mu_k N. Constant magnitude once sliding, always opposing relative motion.

**Key insight.** Static friction is not always at its maximum. It is whatever value is needed to prevent motion, up to the limit mu_s N. Only at the threshold of motion does f_s = mu_s N.

**Worked example.** *A 20 kg crate on a flat floor has mu_s = 0.4 and mu_k = 0.3. You push horizontally with 100 N. Does it slide? If so, what is its acceleration?*

**Solution.** Normal force: N = mg = 196 N. Maximum static friction: f_s,max = 0.4 * 196 = 78.4 N. Applied force (100 N) > f_s,max (78.4 N), so yes, it slides.

Once sliding: f_k = 0.3 * 196 = 58.8 N. Net force = 100 - 58.8 = 41.2 N. Acceleration a = 41.2/20 = 2.06 m/s^2.

## Topic 5 — Projectile Motion

**Setup.** An object launched with initial velocity v_0 at angle theta above horizontal, subject only to gravity (no air resistance).

**Decomposition:** v_0x = v_0 cos(theta), v_0y = v_0 sin(theta). Horizontal: a_x = 0. Vertical: a_y = -g.

**Key results:**
- Time of flight: T = 2 v_0 sin(theta) / g
- Maximum height: H = v_0^2 sin^2(theta) / (2g)
- Range: R = v_0^2 sin(2 theta) / g
- The range is maximized at theta = 45 degrees.
- Complementary angles (e.g., 30 and 60 degrees) give the same range.

**Worked example.** *A ball is launched at 20 m/s at 60 degrees above horizontal. Find the range and maximum height. Use g = 9.8 m/s^2.*

**Solution.** R = (20^2)(sin 120)/9.8 = (400)(0.866)/9.8 = 35.3 m. H = (20^2)(sin^2 60)/(2 * 9.8) = (400)(0.75)/19.6 = 15.3 m.

**When NOT to use these formulas.** When the launch and landing heights differ, or when air resistance matters. In those cases, return to the component equations and solve directly.

## Topic 6 — Circular Motion and Centripetal Force

**Uniform circular motion.** An object moving at constant speed v in a circle of radius r has centripetal acceleration a_c = v^2/r directed toward the center. The centripetal force is F_c = mv^2/r.

**Critical point.** Centripetal force is not a new kind of force. It is the net radial component of whatever forces are present — gravity, tension, normal force, friction.

**Worked example.** *A 1500 kg car rounds a flat curve of radius 50 m at 15 m/s. What friction force is required?*

**Solution.** The friction force provides the centripetal force: f = mv^2/r = (1500)(225)/50 = 6750 N.

**Check:** Is this achievable? f <= mu_s N = mu_s mg. So mu_s >= 6750/(1500 * 9.8) = 0.459. Dry rubber on asphalt has mu_s around 0.7, so yes.

**Non-uniform circular motion.** When speed changes, there is also a tangential acceleration a_t = dv/dt. The total acceleration is the vector sum of radial (centripetal) and tangential components.

## Topic 7 — Rotational Mechanics

**Angular analogs.** Every translational quantity has a rotational counterpart:

| Translational | Rotational | Relation |
|---|---|---|
| Displacement x | Angular displacement theta | s = r theta |
| Velocity v | Angular velocity omega | v = r omega |
| Acceleration a | Angular acceleration alpha | a_t = r alpha |
| Mass m | Moment of inertia I | I = sum(m_i r_i^2) |
| Force F | Torque tau | tau = r F sin(phi) |
| Momentum p = mv | Angular momentum L = I omega | L = r x p |

**Newton's second law for rotation:** tau_net = I alpha.

**Worked example.** *A solid disk of mass 4 kg and radius 0.3 m has a tangential force of 10 N applied at its rim. Find the angular acceleration.*

**Solution.** Moment of inertia of a solid disk: I = (1/2)MR^2 = (1/2)(4)(0.09) = 0.18 kg m^2. Torque: tau = FR = 10 * 0.3 = 3 N m. Angular acceleration: alpha = tau/I = 3/0.18 = 16.67 rad/s^2.

**Conservation of angular momentum.** When no external torque acts, L = I omega is conserved. This explains why figure skaters spin faster when they pull their arms in (I decreases, so omega increases).

## Topic 8 — Gravitation and Orbits

**Newton's law of gravitation:** F = GMm/r^2, attractive, directed along the line connecting the centers of mass.

**Gravitational field:** g = GM/r^2 (at distance r from center of mass M).

**Kepler's three laws:**
1. Orbits are ellipses with the central body at one focus.
2. A line from the planet to the star sweeps equal areas in equal times (conservation of angular momentum).
3. T^2 is proportional to a^3, where T is the orbital period and a is the semi-major axis.

**Worked example.** *A satellite orbits Earth at altitude 400 km above the surface. Find its orbital speed. R_Earth = 6.371 * 10^6 m, M_Earth = 5.972 * 10^24 kg, G = 6.674 * 10^-11 N m^2/kg^2.*

**Solution.** Orbital radius: r = R_Earth + h = 6.371 * 10^6 + 4 * 10^5 = 6.771 * 10^6 m.

For circular orbit, gravitational force provides centripetal force: GMm/r^2 = mv^2/r. So v = sqrt(GM/r).

v = sqrt(6.674e-11 * 5.972e24 / 6.771e6) = sqrt(5.889e7) = 7674 m/s, approximately 7.67 km/s.

**Escape velocity:** v_esc = sqrt(2GM/r). At Earth's surface: v_esc = 11.2 km/s.

## Topic 9 — Work-Energy Theorem

**Work done by a constant force:** W = F d cos(theta), where theta is the angle between force and displacement.

**Work-energy theorem:** W_net = Delta KE = (1/2)mv_f^2 - (1/2)mv_i^2.

**Conservative forces and potential energy.** Gravity and spring forces are conservative — the work they do depends only on initial and final positions, not the path. We define potential energy U such that W_conservative = -Delta U.

**Conservation of mechanical energy.** When only conservative forces do work: KE_i + U_i = KE_f + U_f.

**Worked example.** *A 2 kg ball is dropped from a height of 10 m. Find its speed just before hitting the ground.*

**Solution.** Using conservation of energy: mgh = (1/2)mv^2. The mass cancels: v = sqrt(2gh) = sqrt(2 * 9.8 * 10) = sqrt(196) = 14 m/s.

**When to use energy methods vs. force methods.** Energy methods are ideal when you need final speeds but not the time of travel, or when the path is complex (curved ramps, pendulums). Force methods (F = ma) are needed when you need acceleration, time, or the trajectory itself.

## Topic 10 — Conservation of Momentum

**Linear momentum:** p = mv. Total momentum of an isolated system is conserved: p_total,before = p_total,after.

**Impulse-momentum theorem:** J = F_avg * Delta t = Delta p. Relates average force to momentum change.

**Worked example.** *A 0.15 kg baseball moving at 40 m/s is hit by a bat, reversing direction to 50 m/s. The contact lasts 0.002 s. Find the average force.*

**Solution.** Delta p = m(v_f - v_i) = 0.15(-50 - 40) = 0.15(-90) = -13.5 kg m/s. F_avg = Delta p / Delta t = -13.5 / 0.002 = -6750 N. The bat exerts 6750 N on the ball.

## Topic 11 — Collisions

**Elastic collision (1D).** Both momentum and kinetic energy are conserved. For two objects:
- v_1f = ((m_1 - m_2)/(m_1 + m_2))v_1i + (2m_2/(m_1 + m_2))v_2i
- v_2f = (2m_1/(m_1 + m_2))v_1i + ((m_2 - m_1)/(m_1 + m_2))v_2i

**Perfectly inelastic collision.** Objects stick together. Maximum kinetic energy is lost. v_f = (m_1 v_1i + m_2 v_2i)/(m_1 + m_2).

**Worked example.** *A 1000 kg car at 20 m/s collides head-on with a 1500 kg truck at 10 m/s (opposite direction). They lock together. Find the final velocity.*

**Solution.** Take car's direction as positive. p_i = 1000(20) + 1500(-10) = 20000 - 15000 = 5000 kg m/s. v_f = 5000 / 2500 = 2 m/s in the car's original direction.

**Energy lost:** KE_i = (1/2)(1000)(400) + (1/2)(1500)(100) = 200000 + 75000 = 275000 J. KE_f = (1/2)(2500)(4) = 5000 J. Energy lost = 270000 J, or 98.2%.

## Topic 12 — Oscillations and Simple Harmonic Motion

**Simple harmonic motion (SHM).** Occurs when the restoring force is proportional to displacement: F = -kx.

**Solution:** x(t) = A cos(omega t + phi), where omega = sqrt(k/m), period T = 2 pi / omega.

**Energy in SHM:** E_total = (1/2)kA^2 = (1/2)mv^2 + (1/2)kx^2. Energy oscillates between kinetic and potential.

**Simple pendulum:** For small angles, T = 2 pi sqrt(L/g). Independent of mass and amplitude (for small swings).

**Worked example.** *A 0.5 kg mass on a spring (k = 200 N/m) is displaced 0.1 m and released. Find the period, maximum speed, and maximum acceleration.*

**Solution.** omega = sqrt(k/m) = sqrt(200/0.5) = sqrt(400) = 20 rad/s. T = 2 pi / 20 = 0.314 s.

Maximum speed: v_max = A omega = 0.1 * 20 = 2 m/s (at equilibrium). Maximum acceleration: a_max = A omega^2 = 0.1 * 400 = 40 m/s^2 (at maximum displacement).

**Damped oscillations.** Real oscillators lose energy to friction: x(t) = A e^(-gamma t) cos(omega' t + phi), where gamma = b/(2m) is the damping rate and omega' = sqrt(omega_0^2 - gamma^2).

**Driven oscillations and resonance.** An external periodic force at frequency omega_d produces maximum amplitude when omega_d = omega_0 (resonance). Resonance can be destructive (Tacoma Narrows Bridge) or useful (radio tuning).

## When to Use This Skill

- Any problem involving forces, motion, or trajectories at non-relativistic speeds
- Orbital mechanics and satellite problems
- Engineering statics and dynamics
- Collisions, explosions, and impulse calculations
- Oscillating systems (springs, pendulums, vibrations)
- Problems that say "find the acceleration," "find the tension," "find the speed"

## When NOT to Use This Skill

- **Speeds approaching c:** Use the relativity-astrophysics skill instead. Classical mechanics fails above roughly 0.1c.
- **Atomic/subatomic scales:** Use the quantum-mechanics skill. Classical mechanics cannot describe electron orbitals, tunneling, or spin.
- **Thermal/statistical phenomena:** Use the thermodynamics skill. Classical mechanics describes individual particles; thermodynamics describes bulk properties.
- **Electromagnetic forces beyond simple "given force" problems:** Use the electromagnetism skill for field calculations, circuits, and wave optics.

## Strategy for Solving Classical Mechanics Problems

1. **Draw a picture.** Identify objects, forces, and the coordinate system.
2. **Draw a free-body diagram** for each object of interest.
3. **Decide the approach.** Force/acceleration (Newton's second law) or energy methods? Momentum methods?
   - Need acceleration or time? Use F = ma.
   - Need speed without time? Use energy conservation.
   - Collision or explosion? Use momentum conservation.
   - Rotation? Use tau = I alpha and angular momentum.
4. **Write equations.** Apply the relevant law(s) per axis or per object.
5. **Solve symbolically** before plugging in numbers.
6. **Check units and limiting cases.** Does the answer have the right dimensions? Does it behave sensibly when m -> 0, r -> infinity, etc.?

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Forgetting to decompose forces on inclines | Forces along tilted axes don't cancel properly | Always resolve weight into parallel and perpendicular components |
| Using range formula when heights differ | R = v_0^2 sin(2 theta)/g assumes flat ground | Return to component equations for unequal launch/landing heights |
| Applying centripetal force as a separate force | It is the net radial force, not an additional one | Identify which real force(s) provide the centripetal acceleration |
| Using kinetic friction when object is stationary | Static and kinetic friction are different regimes | Check whether the object actually moves before choosing |
| Confusing angular and tangential quantities | omega and v have different units | Always use v = r omega to convert |
| Ignoring rotational kinetic energy | A rolling ball has both translational and rotational KE | Include (1/2)I omega^2 in energy conservation |

## Cross-References

- **newton agent:** Primary agent for all classical mechanics problems. Opus-class, deep problem-solving.
- **curie agent:** Department chair, coordinates across all physics sub-disciplines.
- **faraday agent:** Pedagogy specialist — can reframe classical mechanics concepts for different audiences.
- **electromagnetism skill:** For problems involving charged particles in fields (Lorentz force, cyclotron motion).
- **thermodynamics skill:** For systems where temperature, heat, and entropy matter alongside mechanical energy.
- **experimental-methods skill:** For uncertainty analysis and dimensional checking in mechanics experiments.

## References

- Halliday, D., Resnick, R., & Walker, J. (2021). *Fundamentals of Physics*. 12th edition. Wiley.
- Kleppner, D., & Kolenkow, R. (2014). *An Introduction to Mechanics*. 2nd edition. Cambridge University Press.
- Taylor, J. R. (2005). *Classical Mechanics*. University Science Books.
- Marion, J. B., & Thornton, S. T. (2004). *Classical Dynamics of Particles and Systems*. 5th edition. Brooks/Cole.
- Feynman, R. P., Leighton, R. B., & Sands, M. (1963). *The Feynman Lectures on Physics*, Vol. I. Addison-Wesley.
- Newton, I. (1687). *Philosophiae Naturalis Principia Mathematica*.
