---
name: orbital-mechanics
description: Classical orbital mechanics from Kepler to Hohmann. Covers the six orbital elements, Kepler's three laws, vis-viva, orbit types (circular, elliptical, parabolic, hyperbolic), transfer orbits, gravity assists, the two-body problem, and practical methods for computing ephemerides. Use when reasoning about planet motion, spacecraft trajectories, comet orbits, exoplanet transits, or binary star dynamics.
type: skill
category: astronomy
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/astronomy/orbital-mechanics/SKILL.md
superseded_by: null
---
# Orbital Mechanics

Orbital mechanics is the branch of celestial mechanics that answers: where will this object be at time t, given its position and velocity now? The foundational discoveries were Kepler's three laws (1609, 1619) and Newton's derivation of them from universal gravitation (1687). Modern practice adds perturbation theory for multi-body problems and relativistic corrections for high-precision ephemerides. This skill covers the classical core: the six orbital elements, Kepler's laws, the vis-viva equation, orbit types, transfer orbits, gravity assists, and a handful of strategies for computing positions in practice.

**Agent affinity:** hubble (catalog cross-reference), payne-gaposchkin (binary star orbits and dynamical masses)

**Concept IDs:** astro-keplers-laws, astro-earth-moon-sun-geometry, astro-planetary-motion

## The Two-Body Problem

Two point masses interacting only via gravity produce a relative motion that is exactly solvable. The relative orbit is a conic section — circle, ellipse, parabola, or hyperbola — with the total mass concentrated at one focus.

**Assumptions:**

- Only two bodies (all others negligible)
- Point masses (or spherically symmetric)
- No radiation pressure, atmosphere, or non-gravitational forces
- Newtonian gravity (relativistic correction needed for Mercury's perihelion, binary pulsars)

When these assumptions hold, the motion is fully determined by six constants — the **orbital elements** — and an epoch.

## The Six Orbital Elements

An orbit in three-dimensional space has six degrees of freedom. There are many choices of six numbers; the classical set is:

| Element | Symbol | Meaning |
|---|---|---|
| Semi-major axis | a | Size of the orbit |
| Eccentricity | e | Shape — how elongated (0 = circle, <1 = ellipse, 1 = parabola, >1 = hyperbola) |
| Inclination | i | Tilt of the orbit plane relative to a reference plane |
| Longitude of ascending node | Omega | Where the orbit crosses the reference plane going up |
| Argument of periapsis | omega | Angle from ascending node to closest approach |
| True anomaly | nu | Current angular position from periapsis |

For solar-system work the reference plane is usually the ecliptic. For Earth satellites it is the equator. For exoplanets around a host star, the plane is defined by observation geometry.

**An alternative sixth element.** The true anomaly is time-dependent. For cataloging a fixed orbit you can substitute the **time of perihelion passage** (T_0) or the **mean anomaly at epoch** (M_0), and derive nu from them at any later time using Kepler's equation.

## Kepler's Three Laws

### First law (1609)

Planets move in elliptical orbits with the Sun at one focus.

**Consequence:** Circular orbits are a special case (e = 0). Most orbits are slightly elliptical — Earth's eccentricity is 0.017. Mercury is 0.206. Pluto is 0.249. Halley's comet is 0.967.

### Second law (1609) — Equal areas in equal times

The line from the Sun to a planet sweeps out equal areas in equal time intervals.

**Consequence:** A planet moves fastest at perihelion (closest to the Sun) and slowest at aphelion. This is equivalent to conservation of angular momentum.

**Formula:** dA/dt = L / (2m) where L is the orbital angular momentum. For Earth the ratio of perihelion to aphelion speeds is about 1.034, matching the eccentricity.

### Third law (1619) — Period and size

The square of the orbital period is proportional to the cube of the semi-major axis:

    T^2 = (4 pi^2 / G * M_total) * a^3

For planets around the Sun, using years and AU:

    T^2 = a^3

where T is in years and a is in AU. Jupiter has a = 5.2 AU, so T = 5.2^1.5 ~ 11.86 years. Checks.

**Binary stars.** The same law applies with M_total = M_1 + M_2. Measuring a and T gives the total mass. Measuring the two stars' individual orbits around the barycenter gives the mass ratio, separating the two masses.

## The Vis-Viva Equation

The workhorse of orbital mechanics:

    v^2 = G * M * (2/r - 1/a)

where v is orbital speed, r is current distance from the focus, and a is the semi-major axis. **Vis-viva** is Latin for "living force" — an old name for kinetic energy.

**Corollaries:**

- **Circular orbit** (r = a): v_circ = sqrt(G M / r). For Earth at 1 AU, this gives 29.78 km/s.
- **Escape velocity** (a = infinity): v_esc = sqrt(2 G M / r) = v_circ * sqrt(2). For Earth surface, 11.2 km/s.
- **Parabolic trajectory** (e = 1): v_esc marginally exceeded, approaches zero at infinity.
- **Hyperbolic trajectory** (a negative in the vis-viva convention): v at infinity is nonzero — you leave and keep going.

**Use.** Given a spacecraft's position and desired speed, vis-viva tells you what semi-major axis you are on, which fixes period and future positions.

## Orbit Types

### Circular (e = 0)

Constant speed, constant distance. Low Earth orbit, geostationary orbit, most spacecraft parking orbits. Not strictly realized in nature but a useful idealization.

### Elliptical (0 < e < 1)

Closed orbit. All planets, most asteroids, most comets, most moons, most binary stars. The two special points are **perihelion** (closest to focus) and **aphelion** (farthest).

For orbits around bodies other than the Sun, the terminology changes: perigee/apogee (Earth), perijove/apojove (Jupiter), periastron/apastron (star), perihelion/aphelion (Sun). The root is the body name.

### Parabolic (e = 1)

Marginally unbound. Never repeats. Speed at infinity equals zero. A theoretical boundary case — real "parabolic" comets are typically slightly elliptical or slightly hyperbolic.

### Hyperbolic (e > 1)

Unbound. The object visits once and leaves forever. Interstellar objects like 1I/Oumuamua (2017) and 2I/Borisov (2019) follow hyperbolic orbits through the Solar System.

## Kepler's Equation

To get position as a function of time in an elliptical orbit, you need to solve Kepler's transcendental equation:

    M = E - e * sin(E)

where M is the **mean anomaly** (linear in time, M = 2 pi * t / T), E is the **eccentric anomaly** (an intermediate angular parameter), and e is eccentricity.

**Solution.** Kepler's equation has no closed-form solution. You iterate. Newton's method converges rapidly:

    E_{n+1} = E_n - (E_n - e * sin(E_n) - M) / (1 - e * cos(E_n))

Start with E_0 = M for small eccentricities or E_0 = pi for high eccentricities. Typically 3-6 iterations bring it to machine precision.

Once you have E, convert to true anomaly:

    tan(nu/2) = sqrt((1+e)/(1-e)) * tan(E/2)

and finally position in the orbital plane is r = a * (1 - e * cos(E)).

## Transfer Orbits — Hohmann

The Hohmann transfer is the minimum-energy trajectory between two coplanar circular orbits. Proposed by Walter Hohmann in 1925 — twenty years before anyone could use it.

**Procedure.** To go from a lower circular orbit of radius r_1 to a higher one of radius r_2:

1. Apply a prograde burn at r_1 that raises apoapsis to r_2. New semi-major axis: a_t = (r_1 + r_2) / 2.
2. Coast on the transfer ellipse half an orbit to apoapsis.
3. Apply a second prograde burn at r_2 that raises periapsis from r_1 to r_2, circularizing.

**Delta-v total:**

    dv_1 = sqrt(G M / r_1) * (sqrt(2 r_2 / (r_1 + r_2)) - 1)
    dv_2 = sqrt(G M / r_2) * (1 - sqrt(2 r_1 / (r_1 + r_2)))
    dv_total = dv_1 + dv_2

**Cost.** Earth to Mars Hohmann transfer: about 5.59 km/s total delta-v from low Earth orbit. Transit time: about 259 days.

**Trade-offs.** Hohmann is energy-optimal but slow. Faster transfers (bi-elliptic, bi-parabolic, or direct high-thrust) spend more propellant for shorter flight time. The Mars launch windows every 26 months arise from the need for Earth and Mars to align for the next Hohmann transfer.

## Gravity Assist (Slingshot)

A spacecraft that flies past a moving planet gains or loses heliocentric speed. In the planet's frame, speed in and speed out are equal (elastic encounter); in the Sun's frame, the spacecraft picks up a component of the planet's velocity.

**Mathematics.** The turn angle during the flyby depends on the closest approach, planet mass, and approach speed. The heliocentric speed change can be up to 2 * v_planet for a grazing encounter with 180-degree turn, but realistic trajectories give smaller gains.

**Examples:**

- Voyager 2 used Jupiter-Saturn-Uranus-Neptune gravity assists to reach all four outer planets.
- Galileo took a Venus-Earth-Earth-Gravity-Assist (VEEGA) path to Jupiter.
- Cassini took Venus-Venus-Earth-Jupiter-Saturn.
- Parker Solar Probe uses repeated Venus flybys to progressively lower perihelion.

Gravity assists are "free" delta-v harvested from planetary orbital motion, paid for (on long enough timescales) by tiny shifts in the planet's orbit.

## Binary Star Dynamics

The orbital-mechanics framework applies directly to binary stars, with G M replaced by G * (M_1 + M_2).

**Visual binaries.** If both stars and the barycenter are resolved, you measure the full orbit. The orbital period and semi-major axis give M_total. The mass ratio M_1/M_2 comes from the ratio of the two stars' distances from the barycenter. Individual masses follow.

**Spectroscopic binaries.** If the orbit is unresolved but radial velocity variations are visible, you measure the orbital period and velocity amplitudes. For a double-lined spectroscopic binary (both components seen), this gives M_1 sin^3(i) and M_2 sin^3(i). Inclination (i) is unknown unless the binary also eclipses, in which case sin(i) ~ 1 and you get true masses.

**Eclipsing binaries.** An orbital plane nearly edge-on produces periodic brightness dips as one star blocks the other. Eclipsing spectroscopic binaries are the gold standard for stellar masses and radii — the Algol system, for example, gave the first stellar radii.

## Perturbations and the Real Solar System

Pure two-body orbits are exact. The real Solar System has eight planets and many smaller bodies, so orbits deviate from perfect ellipses in predictable ways:

- **Secular perturbations** — slow drifts in eccentricity, inclination, node, and perihelion caused by averaged effects of other bodies.
- **Periodic perturbations** — oscillations that average out over a long enough interval.
- **Resonances** — integer ratios between orbital periods cause dramatic effects (Jupiter-Saturn 5:2, Kirkwood gaps in the asteroid belt, Pluto-Neptune 3:2).

For spacecraft navigation you also need non-gravitational forces: solar radiation pressure (important for Cassini, Voyagers), outgassing (comets), atmospheric drag (low Earth orbit), and general relativistic corrections (Mercury's 43 arcsec/century anomalous perihelion advance).

## Worked Example — Period of a Geostationary Satellite

A geostationary satellite has an orbital period equal to one sidereal day (23h 56m 4s = 86164 s) so that it appears stationary over one point on Earth's equator.

**Kepler's third law (SI units):**

    a^3 = (G M_Earth / (4 pi^2)) * T^2

With G M_Earth = 3.986 x 10^14 m^3/s^2 and T = 86164 s:

    a^3 = (3.986e14 / 39.478) * (86164)^2 = 7.496e22 m^3
    a = 4.216e7 m = 42,164 km

Subtracting Earth's radius (6378 km) gives altitude 35,786 km. This is the geostationary altitude, and every communications satellite at that height has this orbit.

## Strategy Selection Heuristics

| Problem | Method |
|---|---|
| Period given size | Kepler's third law |
| Size given period | Invert Kepler's third law |
| Speed at a point | Vis-viva |
| Position vs. time | Kepler's equation + true anomaly |
| Mass of binary | Kepler's third with total mass |
| Delta-v for transfer | Vis-viva at both endpoints |
| Long-term orbit evolution | Perturbation theory |
| Three-body motion | Numerical integration (no closed form) |

## When Two-Body Mechanics is Not Enough

- **Sun-Jupiter-asteroid** — classical restricted three-body problem. Chaotic in general.
- **Binary pulsars** — relativistic corrections (Shapiro delay, periastron precession, gravitational radiation).
- **Close binaries** — tidal deformation, mass transfer via Roche-lobe overflow.
- **Trojan asteroids** — L4 and L5 Lagrange points, stable only in the three-body context.
- **Space-mission design** — multiple bodies, non-gravitational forces, mission constraints require trajectory optimization tools like GMAT or STK.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Mixing unit systems | G has many unit conventions | Pick SI or Gaussian and stay consistent |
| Assuming circular orbits for eccentric ones | Velocity and period are wrong | Use vis-viva for exact speed |
| Ignoring Earth's equatorial bulge | J2 perturbation shifts satellite orbits | Apply secular corrections or use SGP4 |
| Treating parabolic as hyperbolic | Different escape conditions | Check e carefully |
| Forgetting barycenter in binaries | Mass ratio errors | Always reference to barycenter, not either star |

## Cross-References

- **hubble agent:** Distance from galaxy spectra assumes well-calibrated distances from orbital-mechanics-based methods (eclipsing binaries, Cepheids).
- **payne-gaposchkin agent:** Spectroscopic binary orbit analysis for mass determinations.
- **celestial-coordinates skill:** Ecliptic coordinate system for solar-system work.
- **distance-ladder skill:** Dynamical parallax from visual binary orbits.

## References

- Murray, C. D., & Dermott, S. F. (1999). *Solar System Dynamics*. Cambridge University Press.
- Curtis, H. D. (2020). *Orbital Mechanics for Engineering Students*. 4th edition. Butterworth-Heinemann.
- Vallado, D. A. (2013). *Fundamentals of Astrodynamics and Applications*. 4th edition. Microcosm Press.
- Battin, R. H. (1999). *An Introduction to the Mathematics and Methods of Astrodynamics*. Revised edition. AIAA.
- Hohmann, W. (1925). *Die Erreichbarkeit der Himmelskoerper*. Oldenbourg.
- Danby, J. M. A. (1992). *Fundamentals of Celestial Mechanics*. 2nd edition. Willmann-Bell.
