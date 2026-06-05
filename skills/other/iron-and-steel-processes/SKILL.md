---
name: iron-and-steel-processes
description: Industrial production of iron and steel from ore to finished product — blast furnace, Bessemer converter, open-hearth, basic oxygen, electric arc, continuous casting, rolling, and secondary metallurgy. Covers the chemistry of decarburization, dephosphorization, and desulfurization, the metallurgy of plain carbon steels, the evolution from puddling and rolling to BOF and EAF, and the process-structure-property chain that makes mild steel the default structural material of the industrial era.
type: skill
category: materials
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/materials/iron-and-steel-processes/SKILL.md
superseded_by: null
---
# Iron and Steel Processes

Steel is the most-used engineered material on the planet by mass, and its availability, price, and quality are the consequence of about 270 years of process innovation rather than a fundamental change in chemistry. The underlying metallurgy is always the same: take iron, control the carbon content between about 0.02 and 2.1 percent by weight, and adjust a handful of alloying and impurity elements. What changes with each generation of process is how cheaply and uniformly that control is achieved. This skill walks the production chain from ore to shaped product and names the processes a materials engineer must recognize.

**Agent affinity:** bessemer (Bessemer process, converter steelmaking), cort (puddling, rolling, wrought iron)

**Concept IDs:** materials-ferrous-metallurgy, materials-process-history, materials-carbon-control

## The Iron-Carbon System

The foundation of all ferrous metallurgy is the iron-carbon phase diagram. At room temperature, pure iron is body-centered cubic (alpha-iron, ferrite). Above 912 C, iron becomes face-centered cubic (gamma-iron, austenite). Above 1394 C, it reverts to body-centered cubic (delta-iron). It melts at 1538 C. Carbon dissolves much more readily in the face-centered austenite (up to 2.1 percent at the eutectic temperature of 1147 C) than in the body-centered ferrite (0.02 percent maximum), and that solubility difference is the reason steels can be heat-treated.

The practical categories:

- **Wrought iron** — essentially pure iron (carbon below 0.08 percent) with slag stringers from its production process. Soft, ductile, easily welded, corrosion-resistant.
- **Mild steel / low-carbon steel** — 0.05 to 0.25 percent carbon. The structural workhorse: beams, plates, sheet, pipe, rebar.
- **Medium-carbon steel** — 0.25 to 0.6 percent carbon. Shafts, rails, gears, machine parts.
- **High-carbon steel** — 0.6 to 1.0 percent carbon. Springs, cutting tools, wire.
- **Cast iron** — 2.1 to about 4 percent carbon. Engine blocks, machine frames, pipe fittings; cast because it is not forgeable.

Alloying elements modify this base system. Manganese increases hardenability and deoxidizes. Silicon deoxidizes and raises yield. Sulfur and phosphorus are impurities in plain carbon steels and residuals in alloy steels. Chromium above 10.5 percent produces stainless behavior. Nickel stabilizes austenite and improves toughness. Molybdenum raises creep resistance. Vanadium refines grain.

## Primary Ironmaking — the Blast Furnace

The blast furnace has been the dominant primary ironmaking route for over 600 years. Iron ore (hematite Fe2O3 or magnetite Fe3O4), coke (from metallurgical coal), and limestone (flux) are charged at the top. Preheated air is blown through tuyeres near the bottom. The coke burns to carbon monoxide. The CO reduces iron oxide to metallic iron in the upper stack. The iron melts and collects at the bottom. Limestone decomposes to calcium oxide, which combines with silica and alumina in the ore to form a liquid slag that floats on the iron. Every few hours, the furnace is tapped — iron first, then slag — and the products are separated.

The output of the blast furnace is **pig iron** or **hot metal**: liquid iron carrying 4 to 4.5 percent carbon, 0.3 to 1.5 percent silicon, 0.5 to 1 percent manganese, and smaller amounts of sulfur and phosphorus. Pig iron is too brittle and too impure for structural use. It must be refined.

## Historical Refinement — Puddling and Rolling

Before Bessemer, the dominant route from pig iron to wrought iron was Henry Cort's **puddling** process, patented in 1783-84. Pig iron was melted in a reverberatory furnace — a hearth physically separated from the fuel — and stirred ("puddled") with iron rods to expose the melt to the oxidizing atmosphere. Carbon burned out as CO. As the carbon content fell, the melting point rose; the iron became pasty and eventually formed a spongy mass ("loop" or "bloom") that the puddler lifted out with tongs.

Cort's second innovation, often overlooked, was the grooved **rolling mill** that followed the puddling furnace. Blooms were passed through progressively shaped rolls to squeeze out slag, consolidate the metal, and form bars. Rolling replaced the slow and labor-intensive hammering that had dominated earlier wrought-iron production. The puddling-plus-rolling combination lowered wrought iron's production cost by roughly a factor of ten between 1780 and 1820 and made possible the iron bridges, rails, and structural frames of the early industrial era.

The limitation was throughput and carbon control. Puddling was a batch process operated by skilled labor, and it produced wrought iron (low carbon) rather than steel (controllable carbon). For cutlery, springs, and tools, steel was still made by the **cementation process** (diffusing carbon into wrought-iron bars) and then the **crucible process** (Huntsman, 1740s), both of which were slow and expensive.

## The Bessemer Converter — Mass Production of Steel

Henry Bessemer's 1856 patent changed what "steel" meant as a material. The converter is a large egg-shaped vessel lined with refractory, charged with molten pig iron, and tilted upright while air is blown through tuyeres in the bottom. The air oxidizes the dissolved silicon, manganese, and carbon in the melt, generating tremendous heat (the reactions are strongly exothermic) that keeps the charge molten without external fuel. A 10-ton charge can be refined in about 20 minutes.

The key chemical reactions:

- Silicon: `Si + O2 -> SiO2` (goes to slag)
- Manganese: `2 Mn + O2 -> 2 MnO` (goes to slag)
- Carbon: `2 C + O2 -> 2 CO` (leaves as gas through the mouth of the vessel, burning to CO2 in air)

The process is watched by the colour of the flame at the converter mouth. When carbon is nearly gone, the flame drops. The blow is stopped, a calculated amount of spiegeleisen (an iron-manganese-carbon master alloy) is added to recarburize to the target carbon level and deoxidize the melt, and the heat is tapped into ladles.

### The phosphorus problem

Bessemer's original "acid" converter, lined with silica-based refractory, could not remove phosphorus — the slag was acidic and could not accept phosphorus oxides. Much of European and British iron ore is phosphoric, and early Bessemer steel made from such ore was "cold-short" (brittle at room temperature). The problem was solved in 1879 by Sidney Gilchrist Thomas and Percy Gilchrist, who lined the converter with dolomite (magnesia-lime) and added lime to the charge. The lime combined with phosphorus oxides to form a basic slag that could be tapped off. The **basic Bessemer** or Thomas process opened European iron reserves to steelmaking and produced "basic slag" rich in phosphate as an agricultural byproduct.

### The open-hearth alternative

Parallel to Bessemer, the Siemens-Martin **open-hearth** process (1860s) achieved similar refinement chemistry in a regenerative reverberatory furnace. It was slower per heat but accepted large amounts of scrap, allowed more metallurgical control (samples could be taken mid-heat), and produced steel with lower residual nitrogen than Bessemer. By 1900, open-hearth had surpassed Bessemer in quantity; by 1950, open-hearth dominated; both were displaced by BOF after 1950.

## Modern Primary Steelmaking — BOF and EAF

The two dominant processes today are the **basic oxygen furnace (BOF)** and the **electric arc furnace (EAF)**.

### Basic oxygen furnace

A BOF is the spiritual descendant of Bessemer's converter, with two key improvements. First, the oxidizing gas is pure oxygen rather than air — no nitrogen to dissolve into the steel. Second, the oxygen is introduced through a water-cooled lance inserted from the top, rather than through bottom tuyeres. A 300-ton charge of hot metal plus scrap can be refined in about 40 minutes. BOF produces about 70 percent of global steel.

The chemistry is Bessemer chemistry: oxidation of silicon, manganese, and carbon, controlled by lance position and oxygen flow, with lime and fluorspar added to form a basic slag that absorbs phosphorus. Sulfur control is secondary and is finished downstream in ladle metallurgy.

### Electric arc furnace

EAF melts scrap (and increasingly direct-reduced iron or hot-briquetted iron) using a three-phase carbon electrode arc. No hot metal from a blast furnace is required. EAF accounts for about 30 percent of global steel and is dominant in countries without integrated blast-furnace infrastructure and in scrap-rich markets like the United States. The process is electrically intensive (about 400 kWh per ton) but carbon-light compared to the blast-furnace-plus-BOF route, especially when the electricity is low-carbon.

EAF is inherently more flexible than BOF — heats can be smaller, compositions can be more varied, and the furnace can be restarted quickly. Its limitation has historically been that scrap carries tramp elements (copper, tin, nickel) that cannot be removed by refining and that accumulate with each recycling loop. Modern EAF mills manage this with scrap sorting, dilution with direct-reduced iron, and grade control.

## Secondary Metallurgy — the Ladle

Neither BOF nor EAF produces finished steel. The tapped liquid steel goes to a **ladle furnace** or similar station for secondary metallurgy: final deoxidation (aluminum, silicon, calcium additions), desulfurization (lime-based slag stirring), alloying to specification, inclusion modification, and temperature control. Argon stirring homogenizes the melt. Vacuum degassing removes hydrogen and nitrogen for high-quality grades. This is where a plain "steel" becomes a specific grade with named properties.

## Casting and Shaping

Continuous casting, which replaced ingot casting in most mills between 1960 and 1990, produces slabs, blooms, or billets directly from the tundish. Rolling mills then reduce these to plate, sheet, coil, structural shapes, rail, and bar. Hot rolling refines the austenite grain structure, controls the transformation to ferrite and pearlite on the run-out table, and sets the final mechanical properties. Cold rolling hardens the material and produces surface finishes for sheet steel. Pipe and tube are made by a variety of processes (seamless mandrel mill, electric resistance welded, submerged arc welded). The coupling between process and product properties is close: the same grade rolled to different reductions and cooled on different patterns produces measurably different yield strength, ductility, and weldability.

## The Process Tree, Summarized

```
           Iron ore + coke + limestone
                     |
                Blast furnace
                     |
                  Hot metal (pig iron, 4 percent C)
                     |
           +---------+----------+
           |                    |
         BOF                 Ladle metallurgy
           |                    |
     Crude steel           Refined steel (grade-specific)
           |                    |
     Continuous caster     Continuous caster
           |                    |
     Slab / bloom / billet  Slab / bloom / billet
           |                    |
     Hot rolling           Hot rolling
           |                    |
     Sheet, plate, shapes  Sheet, plate, shapes, rail, bar
```

The EAF path starts with scrap (and optionally direct-reduced iron) and skips the blast furnace. From ladle metallurgy onward, the two routes converge.

## Process-Property Shortcuts

A working engineer's rule set for the common outcomes:

- **Structural mild steel (ASTM A36, S235, S275)** — BOF or EAF, hot rolled, no heat treatment, yield 250 MPa, UTS 400 MPa.
- **High-strength low-alloy (HSLA)** — microalloyed with Nb, V, Ti at 0.01 to 0.1 percent, thermomechanically rolled, yield 400 to 700 MPa, excellent weldability.
- **Stainless 304** — EAF + AOD (argon-oxygen decarburization) for low carbon with high chromium, 18 percent Cr, 8 percent Ni, austenitic, corrosion-resistant.
- **Tool steels** — high-carbon high-alloy, often EAF + vacuum remelting, heat treated to martensite, high hardness and wear resistance.
- **Cast iron grades** — blast furnace hot metal is adjusted in a cupola or induction furnace and cast directly, with silicon controlling graphite form (flake, nodular, compacted).

## Cross-References

- **bessemer agent:** Owns the Bessemer-converter story and the general process-structure-property chain. Chair and router.
- **cort agent:** Owns the puddling and rolling history — how wrought iron became cheap before steel did.
- **materials-selection skill:** Whether steel is the right choice for a given function, and which grade within the class.
- **structural-failure-analysis skill:** How the process history of a steel plate shows up at a failure surface decades later.

## References

- Cort, H. (1784). Patents 1351 and 1420, grooved rolls and puddling process.
- Bessemer, H. (1856). "On the manufacture of malleable iron and steel without fuel." Cheltenham BA lecture.
- Gilchrist Thomas, S. (1879). Basic Bessemer process.
- Barraclough, K. C. (1990). *Steelmaking 1850-1900*. Institute of Metals.
- Smil, V. (2016). *Still the Iron Age: Iron and Steel in the Modern World*. Elsevier.
- Bhadeshia, H. K. D. H., & Honeycombe, R. W. K. (2017). *Steels: Microstructure and Properties*. 4th edition. Butterworth-Heinemann.
