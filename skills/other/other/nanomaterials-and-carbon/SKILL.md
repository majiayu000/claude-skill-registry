---
name: nanomaterials-and-carbon
description: Carbon allotropes and nanoscale materials — graphite, diamond, fullerenes (C60 and family), carbon nanotubes, graphene, and the broader class of low-dimensional materials. Covers synthesis routes (arc discharge, laser ablation, CVD, exfoliation), structural characterization, exceptional mechanical and electronic properties, and the gap between laboratory demonstrations and structural-scale applications.
type: skill
category: materials
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/materials/nanomaterials-and-carbon/SKILL.md
superseded_by: null
---
# Nanomaterials and Carbon

Carbon is the most versatile structural element in chemistry and one of the most versatile in materials science. Depending on how its four valence electrons are arranged, it forms the softest common lubricant (graphite), the hardest bulk material (diamond), the strongest known material in thin-film form (graphene), and a growing family of low-dimensional structures — fullerenes, nanotubes, nanoribbons, carbon nitrides — each with its own bonding signature and property set. This skill covers the carbon allotropes and the broader nanomaterials landscape they anchor, from the Kroto-Curl-Smalley discovery of C60 in 1985 to modern chemical vapor deposition of graphene.

**Agent affinity:** smalley (fullerenes and carbon nanotubes), ashby (nanomaterial performance in selection charts)

**Concept IDs:** materials-carbon-allotropes, materials-nanoscale-properties, materials-low-dimensional

## The Carbon Allotropes

Carbon's electronic structure allows sp, sp2, and sp3 hybridization. Each hybridization produces a distinct bonding geometry, and the geometries produce distinct allotropes.

- **Diamond** (sp3) — each carbon tetrahedrally bonded to four others, forming a three-dimensional covalent network. Hardness ~70 to 100 GPa (Vickers), highest known; thermal conductivity ~2000 W/m*K, highest of any bulk material; optically transparent; electrical insulator (band gap 5.5 eV). Synthesized industrially by HPHT (high-pressure, high-temperature, modeled on natural formation) and CVD (low pressure, chemical deposition on a substrate).
- **Graphite** (sp2) — planar hexagonal layers of carbon, weakly bonded between layers by van der Waals forces. In-plane modulus ~1 TPa, inter-plane modulus ~35 GPa — extreme anisotropy. Excellent dry lubricant because the layers shear. Electrical conductor in-plane. Graphite is the common, everyday form of carbon; everything below is some variation on rolling, cutting, or curving graphite sheets.
- **Amorphous carbon** (mixed sp2/sp3) — carbon black, soot, glassy carbon, diamond-like carbon films. No long-range order. Properties vary with sp3 fraction.
- **Fullerenes** (sp2, curved) — closed cages of carbon atoms, the smallest stable one being C60. Below.
- **Carbon nanotubes** (sp2, rolled) — a graphene sheet rolled into a cylinder. Single-walled or multi-walled. Below.
- **Graphene** (sp2, sheet) — a single layer of graphite. Below.

## C60 and the Fullerene Family

In 1985, Harold Kroto, Robert Curl, and Richard Smalley published their discovery of a carbon species of mass 720 in the laser-vaporization products of graphite, and proposed a soccer-ball structure — 60 carbons at the vertices of a truncated icosahedron — to explain its stability. They named it **buckminsterfullerene** after the geodesic domes of Buckminster Fuller. The 1996 Nobel Prize in Chemistry recognized the discovery.

C60 has 12 pentagons and 20 hexagons, satisfying Euler's formula for a closed polyhedron. Every carbon is equivalent and three-coordinated with sp2-hybridized bonds. The diameter is about 0.7 nm. Larger fullerenes (C70, C76, C78, C84, and onward) exist; the general family is called the fullerenes. Production in bulk became possible with the Kraetschmer-Huffman arc-discharge method (1990), which made gram quantities available and opened the field to chemical and materials investigation.

Fullerene properties of note:

- **Electronic** — C60 is a molecular semiconductor. When doped with alkali metals (K3C60, Rb3C60), it becomes a metal and then a superconductor at temperatures up to ~33 K.
- **Mechanical** — individual C60 molecules are extraordinarily hard in compression; a fullerite film approaches diamond-like hardness for short times.
- **Chemistry** — C60 accepts up to six electrons in solution, acting as an electron sink. Functionalization chemistry is rich.

Fullerenes remain laboratory and high-value-application materials (organic photovoltaics as PCBM, research-scale quantum materials). Their commercial impact is smaller than their scientific importance.

## Carbon Nanotubes

A single-walled carbon nanotube (SWCNT) can be imagined as a graphene sheet rolled into a seamless cylinder with a hemispherical fullerene cap at each end. The rolling vector (chirality) determines whether the tube is metallic or semiconducting — an electronic property set by pure geometry. Multi-walled carbon nanotubes (MWCNTs) are concentric nested cylinders.

Discovered (or more precisely, identified with modern resolution) by Sumio Iijima in 1991, nanotubes quickly became the most-cited nanomaterial of the 1990s and 2000s because their properties are extraordinary:

- **Tensile strength** — individual SWCNTs reach 50 to 100 GPa, the highest recorded for any material. About 50 times that of steel by mass.
- **Elastic modulus** — Young's modulus near 1 TPa, comparable to diamond.
- **Electrical conductivity** — metallic SWCNTs carry current densities above 10^9 A/cm^2 without failure.
- **Thermal conductivity** — above 3000 W/m*K for isolated tubes, among the highest known.

### Production routes

- **Arc discharge** — the original method (Iijima). Pulls tubes from a plasma between graphite electrodes. Low yield but high quality for research.
- **Laser ablation** — vaporization of graphite target by pulsed laser in a furnace. Produces uniform SWCNTs.
- **CVD** — chemical vapor deposition over metal catalyst particles, the dominant industrial method. Scales to kilograms and allows substrate-aligned growth.
- **HiPco** (high-pressure CO disproportionation) — Smalley's group's route, producing clean SWCNTs at kilogram-per-day scale.

### Applications versus promise

Despite two decades of hype, carbon nanotubes have not become a structural material in the J.E. Gordon sense. The gap is between individual tube properties and bulk composite properties. A composite of nanotubes in a polymer matrix cannot exceed the modulus of the matrix by more than the load-transfer efficiency allows, and load transfer to nanotubes is limited by their smooth, hard-to-bond surfaces. The CNT-polymer composite modulus has grown slowly against the growth of high-performance carbon fiber composites, which remain the dominant choice for structural aerospace.

Current commercial uses: conductive additives in batteries, EMI-shielding coatings, field-emission displays, sensor electrodes, and as a component in some polymer composites for electrostatic dissipation. Structural use at the weight-saving scale originally imagined remains research.

## Graphene

Graphene is a single two-dimensional layer of graphite. Its existence as a stable monolayer was experimentally demonstrated by Andre Geim and Kostya Novoselov in 2004, using adhesive tape to mechanically exfoliate graphite flakes onto a silicon oxide substrate and identifying monolayers by optical contrast. The 2010 Nobel Prize in Physics recognized the work.

Graphene's property set is as extraordinary as the nanotubes it contains:

- **Electronic** — a zero-gap semimetal with a linear (Dirac-cone) band structure, producing massless-fermion-like charge carriers and carrier mobilities above 200,000 cm^2/V*s in suspended samples. A playground for condensed-matter physics.
- **Mechanical** — in-plane Young's modulus ~1 TPa, breaking strength ~130 GPa, the stiffest and strongest material measured.
- **Thermal** — thermal conductivity above 5000 W/m*K for suspended graphene.
- **Optical** — absorbs exactly pi * alpha ~ 2.3 percent of visible light per layer, where alpha is the fine-structure constant.

### Production routes

- **Mechanical exfoliation** — adhesive tape on graphite. Produces the highest-quality single layers for research but not scalable.
- **Chemical vapor deposition** on copper foil — now the industry standard. Produces large-area polycrystalline films that can be transferred to other substrates.
- **Liquid-phase exfoliation** of graphite in surfactants or solvents — produces flake dispersions at kilogram scale, used in conductive coatings, inks, and additives.
- **SiC decomposition** — graphitization of silicon carbide wafer surfaces, producing graphene directly on a semiconductor substrate.
- **Graphene oxide reduction** — oxidation of graphite to soluble graphene oxide followed by chemical or thermal reduction. Produces defective but processable material at scale.

### The applications reality check

Graphene has followed the same trajectory as nanotubes: extraordinary intrinsic properties, slow translation to bulk applications. Transparent conductive films compete with ITO but have not displaced it. Battery and supercapacitor electrodes use graphene as an additive. Composite reinforcement is growing but modest. The field-effect transistor application suffers from the zero band gap — useful for high-frequency analog electronics but not for digital logic. The biggest commercial application remains as a conductive additive in lithium-ion batteries.

## Beyond Carbon — Other 2D and Nano Materials

The graphene discovery opened a search for other 2D materials that can be exfoliated or grown in monolayer form.

- **Hexagonal boron nitride (h-BN)** — insulating, atomically flat, lattice-matched to graphene. Used as gate dielectric in graphene devices.
- **Transition metal dichalcogenides (TMDs)** — MoS2, WS2, MoSe2, WSe2. Direct band gaps in the monolayer (unlike graphene's zero gap), opening optoelectronic applications.
- **MXenes** — 2D transition metal carbides and nitrides with metallic conductivity, active in batteries and EMI shielding.
- **Phosphorene** — exfoliated black phosphorus, anisotropic in-plane.
- **Silicene, germanene, stanene** — analogues of graphene for silicon, germanium, tin. Stability is marginal and production remains research.

## The Structural Gap

All of these materials share a feature Ashby would note: their intrinsic properties per-unit-mass or per-unit-volume place them in the upper left of every Ashby chart, yet their impact on structural engineering has been slower than their property numbers predicted in 1990 or 2005. Three reasons recur.

1. **Load transfer.** A nanotube or graphene flake has to be bonded to its matrix for its strength to matter in a composite. Surface chemistry is not cooperative.
2. **Scale and cost.** Mass production of high-quality nanomaterials is expensive. Structural applications demand low cost per kilogram; high-performance carbon fiber is usually the winning alternative.
3. **Defect sensitivity.** Intrinsic properties are measured on nearly defect-free samples. Practical bulk materials carry defects that reduce the numbers substantially.

The structural applications that have succeeded (EMI shielding, electrode coatings, polymer additives at low weight fractions) are the ones where a small amount of nanomaterial changes an electrical or functional property rather than a mechanical one.

## Cross-References

- **smalley agent:** Primary agent for fullerene and nanotube topics.
- **ashby agent:** Places nanomaterials in performance space against traditional metals, polymers, and composites.
- **materials-characterization skill:** TEM, Raman, and XRD techniques critical to nanomaterials work.
- **materials-selection skill:** The framework within which any nanomaterial must justify displacement of an incumbent.

## References

- Kroto, H. W., Heath, J. R., O'Brien, S. C., Curl, R. F., & Smalley, R. E. (1985). "C60: Buckminsterfullerene." *Nature*, 318, 162-163.
- Iijima, S. (1991). "Helical microtubules of graphitic carbon." *Nature*, 354, 56-58.
- Novoselov, K. S., Geim, A. K., Morozov, S. V., et al. (2004). "Electric field effect in atomically thin carbon films." *Science*, 306, 666-669.
- Kraetschmer, W., Lamb, L. D., Fostiropoulos, K., & Huffman, D. R. (1990). "Solid C60: a new form of carbon." *Nature*, 347, 354-358.
- Nicolosi, V., Chhowalla, M., Kanatzidis, M. G., Strano, M. S., & Coleman, J. N. (2013). "Liquid exfoliation of layered materials." *Science*, 340, 1226419.
- Smalley, R. E. (2005). "Future global energy prosperity: the terawatt challenge." *MRS Bulletin*, 30, 412-417.
