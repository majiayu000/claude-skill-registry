---
name: nonferrous-alloys
description: Metallurgy of the major nonferrous structural and engineering alloys — aluminum, copper, titanium, nickel, magnesium, and their strengthening mechanisms. Covers precipitation (age) hardening in Al-Cu and Al-Zn-Mg systems, solid-solution strengthening in brass and bronze, alpha-beta titanium, nickel superalloys with gamma-prime, and the trade-offs in density, strength, corrosion resistance, and cost that decide when to leave steel for a lighter or more specialized metal.
type: skill
category: materials
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/materials/nonferrous-alloys/SKILL.md
superseded_by: null
---
# Nonferrous Alloys

Steel is the default structural material. Nonferrous alloys are what you use when the default is wrong. Each nonferrous family wins in a different corner of property space: aluminum for weight-sensitive structure at moderate temperature, copper for conductivity and corrosion in water, titanium for strength-to-weight in harsh environments, nickel for high-temperature creep resistance, magnesium for absolute minimum mass when the application allows. This skill surveys the major families, the strengthening mechanisms that give them their engineering properties, and the trade-offs that drive selection.

**Agent affinity:** merica (aluminum age hardening, alloy development), ashby (cross-family selection)

**Concept IDs:** materials-nonferrous-metallurgy, materials-strengthening-mechanisms, materials-alloy-design

## Strengthening Mechanisms

Before surveying the families, the four mechanisms that harden any metal:

1. **Work hardening (cold work).** Plastic deformation multiplies dislocations; interacting dislocations make further deformation harder. Yield strength rises, ductility falls. Reversible by annealing.
2. **Solid-solution strengthening.** Alloying atoms distort the lattice; dislocations pay an energy cost to glide past them. The effect scales with size mismatch and concentration. Copper-zinc (brass) and copper-tin (bronze) are classic examples.
3. **Grain refinement.** Grain boundaries obstruct dislocation motion. The Hall-Petch relation gives `sigma_y = sigma_0 + k * d^(-1/2)`, where d is the mean grain diameter. Fine-grained metals are both stronger and tougher — the rare mechanism that does not sacrifice ductility for strength.
4. **Precipitation (age) hardening.** Second-phase particles of controlled size pin dislocations. Dislocations either bow around them (Orowan mechanism) or cut through (shearing), depending on particle size and coherency. This mechanism requires solid-solubility that decreases with temperature so that the alloy can be quenched from solid solution and then reheated to nucleate fine precipitates.

The discovery of precipitation hardening is the key historical event for nonferrous engineering alloys, and it happened in aluminum.

## Aluminum Alloys

Pure aluminum is soft, low-density (2.7 g/cm^3), corrosion-resistant thanks to its self-healing oxide film, and conductive. Its defining weakness is a low melting point (660 C) and mediocre strength in the pure state — about 30 MPa yield. Age hardening transforms the story.

### The discovery of age hardening

In 1906, Alfred Wilm at the Neubabelsberg research center in Germany was trying to develop a high-strength aluminum alloy for rifle cartridge cases. He added copper and magnesium to aluminum, quenched from solid solution, and measured mechanical properties — which at first were disappointing. By chance, he let a specimen sit for several days before a follow-up measurement and found the hardness had nearly doubled. The effect became known as **aging**, and the alloy was commercialized as **Duralumin** by Durener Metallwerke. The physical explanation — fine precipitates nucleating from a supersaturated solid solution — was not understood until the 1930s.

Paul Merica was a central figure in that understanding. Working at the US National Bureau of Standards and later at International Nickel, Merica, with Waltenberg and Scott, showed in 1919 that age hardening in Al-Cu alloys corresponded to a solid-solubility limit that decreased sharply with temperature — the condition required for a supersaturated solid solution to form upon quenching and then decompose upon aging. The Merica-Waltenberg-Scott paper is the starting point for the theory of age hardening.

### The Al-Cu system (2xxx series)

Al-Cu alloys (with small additions of Mg, Mn, Si) are the aerospace structural workhorse, especially 2014, 2024, and 2219. The solid-solubility curve for copper in aluminum runs from 5.65 percent at 548 C (the eutectic) down to 0.1 percent at room temperature. Heat to 495 C to dissolve all the copper into solid solution, quench rapidly in water, then age at room temperature or 190 C. Fine GP (Guinier-Preston) zones and then theta-prime precipitates nucleate and pin dislocations. Peak strength rises from roughly 70 MPa (annealed) to about 475 MPa (T6 temper) — a sevenfold gain without any cold work.

### The Al-Zn-Mg-Cu system (7xxx series)

7075-T6 aluminum, introduced in 1943 and still the main aerospace alloy for high-strength applications, uses the Al-Zn-Mg-Cu system. The precipitating phases are MgZn2 and variants. Yield strengths reach 500 MPa. The trade-off is reduced corrosion resistance and susceptibility to stress-corrosion cracking, managed by overaging tempers (T73, T76) that sacrifice a little peak strength for a large gain in SCC resistance.

### The Al-Mg-Si system (6xxx series)

6061 and 6063 use Mg2Si as the precipitating phase. Moderate strength (yield 240 to 275 MPa), excellent extrudability, weldable, corrosion-resistant. Dominant in structural extrusions and general fabrication. Weaker than the 2xxx/7xxx series but far more forgiving.

### The non-heat-treatable series (1xxx, 3xxx, 5xxx)

Pure aluminum (1xxx), Al-Mn (3xxx), and Al-Mg (5xxx) rely on solid-solution and work hardening rather than aging. 5083 and 5086 are marine standards: strong after rolling, corrosion-resistant in seawater, weldable. Ship hulls, storage tanks, and cryogenic vessels use these alloys.

## Copper Alloys

Copper is the second-most-used metal by mass for non-structural purposes, dominant in electrical conductivity (second only to silver), corrosion resistance in water, and antimicrobial surfaces.

### Pure copper and oxygen-free copper

Unalloyed copper sits around 60 percent IACS conductivity at commercial purity and reaches 100 percent IACS at high purity. Oxygen-free electronic (OFE) copper, used where hydrogen embrittlement must be avoided, contains less than 10 ppm oxygen. Work-hardened copper wire (half-hard, hard, extra-hard tempers) supplies most of the world's electrical infrastructure.

### Brass (Cu-Zn)

Brass is the archetypal solid-solution-strengthened alloy. Alpha brass (up to 37 percent Zn, FCC structure) is ductile and suited to deep drawing. Alpha-beta brass (around 40 percent Zn) is stronger but less ductile, suited to hot working. Yellow brass (65/35) is the cartridge brass standard. Leaded free-cutting brass adds 2 to 3 percent lead for machinability.

### Bronze (Cu-Sn and variants)

Tin bronze is the historical alloy of bearings, ship fittings, and bells — 10 to 12 percent tin gives hard, wear-resistant, corrosion-resistant metal with high casting fidelity. Aluminum bronze (up to 14 percent Al) is even stronger and harder and is used in seawater pumps and ship propellers. Nickel-aluminum bronze reaches yield strengths around 350 MPa with excellent corrosion resistance in seawater.

### Cupronickel and nickel silver

Cupronickel (70/30 or 90/10 Cu-Ni) is the standard tubing material for seawater heat exchangers and condensers — biofouling-resistant, corrosion-resistant, reasonable thermal conductivity. Nickel silver (Cu-Ni-Zn, no actual silver) is used in musical instrument parts and hardware.

## Titanium Alloys

Titanium offers the best strength-to-weight ratio available in metals (density 4.5 g/cm^3, yields commonly 800 to 1100 MPa), outstanding corrosion resistance (the native oxide is exceptionally stable), and biocompatibility. Cost and processing difficulty are the drawbacks — titanium is oxygen-sensitive at temperature, difficult to machine, and expensive to refine from ore.

### Alpha, beta, and alpha-beta classifications

- **Alpha alloys.** Hexagonal close-packed structure, stabilized by aluminum and oxygen. Good creep resistance but less formable. Commercial-purity titanium and Ti-5Al-2.5Sn fall here.
- **Beta alloys.** Body-centered cubic, stabilized by V, Mo, Nb, Fe. Heat-treatable, formable, and high-strength. Examples: Ti-10V-2Fe-3Al, Ti-15V-3Cr.
- **Alpha-beta alloys.** A mix of HCP alpha and BCC beta phases, by far the most commercially important group. **Ti-6Al-4V** (Grade 5) accounts for more than half of all titanium consumption: aerospace structural components, jet engine blades at lower temperatures, medical implants.

### Why titanium is expensive

Titanium is the ninth-most-abundant element in the Earth's crust, but it cannot be reduced from its oxide by carbon — TiO2 is too stable and TiC forms instead. The Kroll process (1940) reduces titanium tetrachloride with magnesium in an inert atmosphere, producing titanium sponge that is then melted in vacuum (vacuum arc remelting or electron beam). Every step is expensive. Titanium will always cost more than aluminum until a better reduction route is commercialized.

## Nickel Alloys and Superalloys

Nickel's signature property is creep strength at high temperature. Pure nickel loses strength rapidly above 500 C; nickel-based **superalloys** retain useful strength up to about 1100 C and dominate hot sections of gas turbines.

### Inconels, Waspaloys, and the gamma-prime mechanism

Modern superalloys (Inconel 718, Waspaloy, Rene 80, CMSX-4) rely on precipitation of an ordered intermetallic **gamma-prime** phase, Ni3(Al,Ti), from the face-centered-cubic nickel matrix. The gamma-prime precipitates are coherent with the matrix, can reach high volume fractions (60 to 70 percent in single-crystal turbine blades), and provide creep resistance that persists to temperatures where most metals have long since yielded. Single-crystal casting (directional solidification) eliminates grain boundaries that would otherwise cavitate under creep. Thermal barrier coatings further raise the usable gas temperature.

### Hastelloy, Monel, and corrosion resistance

Nickel-chromium-molybdenum alloys (Hastelloy C276, C22, B3) are the reference materials for severe chemical-process environments — concentrated acids, chlorides, wet H2S. Monel (Ni-Cu) is seawater-corrosion resistant and used in marine valves, pumps, and heat exchangers.

## Magnesium Alloys

Magnesium is the lightest structural metal (1.74 g/cm^3, two-thirds the density of aluminum). Its weaknesses are low elastic modulus (45 GPa), difficult formability (HCP crystal structure), active corrosion in salt-bearing environments, and flammability of fine chips. Applications are where absolute minimum mass dominates: aerospace gearbox housings, automotive steering wheels and instrument-panel frames, laptop chassis, hand-held power tool housings. AZ91 (Mg-9Al-1Zn) is the standard die-casting alloy.

## Selection Among Nonferrous Families

A rough working table for when to leave steel.

| Need | Family | Representative alloy |
|---|---|---|
| Weight-limited structure, moderate T | Aluminum 2xxx/7xxx | 7075-T6 |
| Weight-limited structure, low cost | Aluminum 6xxx | 6061-T6 |
| Corrosion in seawater, tubing | Cupronickel / aluminum bronze | 90/10 Cu-Ni, NAB |
| Electrical conductor | Copper | OFE copper |
| Strength + biocompatibility | Titanium | Ti-6Al-4V |
| Creep resistance above 800 C | Nickel superalloy | Inconel 718, CMSX-4 |
| Absolute minimum mass | Magnesium | AZ91 |
| Severe chemical process | Nickel-chrome-moly | Hastelloy C276 |

The selection is always a trade-off. Aluminum 7075 is stronger than steel on a per-mass basis but weaker on a per-volume basis; titanium is cheaper than nickel superalloys on a per-kilogram strength basis but more expensive on a direct cost-per-kilogram basis. No nonferrous family is universally better than steel. The right question is always which constraint is hurting, and which family relaxes that constraint at the smallest cost increment.

## Cross-References

- **merica agent:** Owns aluminum age hardening and the history of alloy development for light metals.
- **ashby agent:** Applies performance indices to decide among nonferrous families.
- **iron-and-steel-processes skill:** The baseline against which every nonferrous choice is measured.
- **materials-characterization skill:** Precipitate structure in aged alloys is measured by TEM and atom probe; hardness and conductivity track processing history.

## References

- Merica, P. D., Waltenberg, R. G., & Scott, H. (1919). "Heat treatment of duralumin." *Bulletin of the US Bureau of Standards*, 15, 271-316.
- Polmear, I. J. (2005). *Light Alloys: From Traditional Alloys to Nanocrystals*. 4th edition. Butterworth-Heinemann.
- Reed, R. C. (2006). *The Superalloys: Fundamentals and Applications*. Cambridge University Press.
- Leyens, C., & Peters, M. (2003). *Titanium and Titanium Alloys: Fundamentals and Applications*. Wiley-VCH.
- Davis, J. R. (ed.) (2001). *ASM Specialty Handbook: Copper and Copper Alloys*. ASM International.
