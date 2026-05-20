---
name: organic-chemistry
description: Carbon chemistry, functional groups, IUPAC nomenclature, isomerism, reaction mechanisms (substitution, elimination, addition), polymers, and biochemistry basics. Covers hydrocarbon classes (alkanes, alkenes, alkynes, aromatics), common functional groups (alcohols, aldehydes, ketones, carboxylic acids, esters, amines, amides), stereochemistry, condensation and addition polymerization, and the four biomolecule classes (carbohydrates, lipids, proteins, nucleic acids). Use when analyzing organic structures, predicting reaction products, or connecting chemistry to biology.
type: skill
category: chemistry
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/chemistry/organic-chemistry/SKILL.md
superseded_by: null
---
# Organic Chemistry

Organic chemistry is the study of carbon-containing compounds and their reactions. Carbon's ability to form four stable covalent bonds, catenate (bond to itself in chains and rings), and hybridize in three ways (sp3, sp2, sp) generates an essentially infinite diversity of molecular architectures. This skill covers hydrocarbon families, functional groups, nomenclature, reaction mechanisms, polymers, and the biochemistry of life's molecules.

**Agent affinity:** pauling (bonding/molecular chemistry, primary for mechanisms and structure), franklin (materials/applied chemistry, for polymer and materials topics)

**Concept IDs:** chem-polymers, chem-biochemistry-basics

## Why Carbon is Special

| Property | Consequence |
|---|---|
| 4 valence electrons, forms 4 bonds | Tetrahedral (sp3), trigonal planar (sp2), or linear (sp) geometries |
| Similar electronegativity to H, O, N | Forms stable covalent bonds with life's key elements |
| Strong C-C bonds (347 kJ/mol) | Chains of hundreds to millions of carbons are stable |
| Multiple bond capability (C=C, C-triple-C) | Rigidity, planarity, and reactivity variation |

Over 20 million organic compounds are known — dwarfing all inorganic compounds combined.

## Hydrocarbon Families

| Family | General formula | Bonding | Hybridization | Saturation |
|---|---|---|---|---|
| Alkanes | CnH(2n+2) | All single bonds | sp3 | Saturated |
| Cycloalkanes | CnH(2n) | All single bonds, ring | sp3 | Saturated |
| Alkenes | CnH(2n) | One C=C double bond | sp2 at C=C | Unsaturated |
| Alkynes | CnH(2n-2) | One C-triple-C triple bond | sp at triple bond | Unsaturated |
| Aromatics | Variable | Delocalized pi ring | sp2 | Unsaturated |

**Benzene (C6H6)** is the archetypal aromatic. Its 6 pi electrons are delocalized across the ring, creating exceptional stability (aromaticity). The resonance energy of benzene is approximately 150 kJ/mol — it does not undergo the addition reactions typical of alkenes.

## IUPAC Nomenclature

### Alkane Naming Rules

1. Find the longest continuous carbon chain — this is the parent name.
2. Number the chain from the end nearest the first substituent.
3. Name substituents as prefixes with their position numbers.
4. Use di-, tri-, tetra- for multiple identical substituents.
5. List substituents alphabetically (ignoring di-, tri- prefixes).

### Worked Example: Naming a Branched Alkane

**Structure:** A 6-carbon chain with methyl groups on carbons 2 and 4.

**Step 1.** Parent chain: hexane (6 carbons).
**Step 2.** Number from the end that gives the lowest locants: positions 2 and 4 (not 3 and 5).
**Step 3.** Two methyl substituents at positions 2 and 4.
**Name:** 2,4-dimethylhexane.

### Worked Example: Naming an Alkene

**Structure:** A 5-carbon chain with a double bond between carbons 1 and 2, and a methyl group on carbon 3.

**Step 1.** Parent chain includes the double bond: pentene.
**Step 2.** Number from the end nearest the double bond: 1-pentene.
**Step 3.** Methyl at position 3.
**Name:** 3-methyl-1-pentene.

## Functional Groups

Functional groups are the reactive sites of organic molecules. They determine chemical behavior.

| Group | Structure | Found in | Example |
|---|---|---|---|
| Hydroxyl | -OH | Alcohols | Ethanol (CH3CH2OH) |
| Carbonyl | C=O | Aldehydes (terminal), ketones (internal) | Formaldehyde (HCHO), acetone (CH3COCH3) |
| Carboxyl | -COOH | Carboxylic acids | Acetic acid (CH3COOH) |
| Ester | -COO- | Esters | Ethyl acetate (CH3COOCH2CH3) |
| Amino | -NH2 | Amines | Methylamine (CH3NH2) |
| Amide | -CONH2 | Amides | Acetamide (CH3CONH2) |
| Ether | -O- | Ethers | Diethyl ether (CH3CH2OCH2CH3) |
| Halide | -X (F, Cl, Br, I) | Alkyl halides | Chloromethane (CH3Cl) |
| Thiol | -SH | Thiols | Ethanethiol (CH3CH2SH) |
| Phosphate | -OPO3^2- | Phosphoesters | ATP, DNA backbone |

**Priority for naming:** carboxylic acid > ester > amide > aldehyde > ketone > alcohol > amine. The highest-priority group becomes the suffix; lower-priority groups are prefixes.

## Isomerism

### Structural (Constitutional) Isomers

Same molecular formula, different connectivity. C4H10 has two structural isomers: butane (straight chain) and 2-methylpropane (branched).

### Geometric (Cis-Trans) Isomers

Arise from restricted rotation around C=C double bonds. Cis: identical groups on the same side. Trans: on opposite sides. For more complex cases, use E/Z notation based on Cahn-Ingold-Prelog priority rules (higher atomic number = higher priority; Z = same side, E = opposite).

**Worked example.** *2-butene has cis and trans isomers.*

cis-2-butene: both CH3 groups on the same side of the double bond. Boiling point: 3.7 C.
trans-2-butene: CH3 groups on opposite sides. Boiling point: 0.9 C.

The cis isomer has a higher boiling point because it has a net dipole moment (polar); the trans isomer's dipoles cancel (nonpolar).

### Enantiomers (Optical Isomers)

Mirror-image molecules that are non-superimposable. Require a chiral center — typically a carbon bonded to four different groups. Enantiomers have identical physical properties except they rotate plane-polarized light in opposite directions. They can have dramatically different biological activity (thalidomide: one enantiomer treats nausea, the other causes birth defects).

## Reaction Mechanisms

### Substitution Reactions

**SN2 (bimolecular nucleophilic substitution):** One step. Nucleophile attacks as leaving group departs. Backside attack causes inversion of configuration. Rate = k[substrate][nucleophile]. Favored by: strong nucleophile, primary substrate, polar aprotic solvent.

**SN1 (unimolecular nucleophilic substitution):** Two steps. (1) Leaving group departs, forming carbocation. (2) Nucleophile attacks. Rate = k[substrate]. Favored by: tertiary substrate (stable carbocation), polar protic solvent. Produces racemic mixture.

### Worked Example: SN2 vs. SN1 Prediction

**Problem.** Predict the mechanism for: CH3Br + OH- -> CH3OH + Br-

**Analysis.** Substrate is primary (methyl — no branching). Strong nucleophile (OH-). Backside attack is unhindered. This is textbook SN2.

**Problem.** Predict the mechanism for: (CH3)3CBr + H2O -> (CH3)3COH + HBr

**Analysis.** Substrate is tertiary (three methyl groups block backside attack). Weak nucleophile (H2O). The t-butyl carbocation (CH3)3C+ is stable (three hyperconjugating methyls). This is SN1.

### Elimination Reactions

**E2:** One step. Strong base removes a proton while the leaving group departs. Anti-periplanar geometry required. Competes with SN2 (use bulky base to favor E2).

**E1:** Two steps via carbocation. Competes with SN1. Zaitsev's rule: the more substituted alkene is the major product (more stable).

### Addition Reactions

**Alkene addition.** Electrophilic addition to C=C:

- HX addition: Markovnikov's rule — H adds to the carbon with more hydrogens. Anti-Markovnikov with peroxide (radical mechanism).
- Halogenation (Br2): adds across double bond, anti-addition.
- Hydration (H2O/H+): Markovnikov addition of OH.
- Hydrogenation (H2/Pt): syn-addition, converts alkene to alkane.

### Worked Example: Markovnikov Addition

**Problem.** Predict the major product of HBr addition to propene (CH3CH=CH2).

**Step 1.** H+ adds to the less-substituted carbon (CH2 end), forming a secondary carbocation on the middle carbon: CH3CH+CH3.

**Step 2.** Br- attacks the carbocation: CH3CHBrCH3 (2-bromopropane).

**Markovnikov's rule in modern terms:** the electrophile (H+) adds to form the more stable carbocation intermediate. Secondary > primary carbocation stability explains the regiochemistry.

## Polymers

### Addition (Chain-Growth) Polymers

Monomers with C=C bonds undergo chain addition. No atoms are lost.

**Example:** Polyethylene. n CH2=CH2 -> -(CH2-CH2)n-

Other addition polymers: polypropylene (PP), polystyrene (PS), polyvinyl chloride (PVC), polytetrafluoroethylene (PTFE/Teflon).

### Condensation (Step-Growth) Polymers

Monomers with two functional groups react, releasing a small molecule (usually H2O) at each step.

**Example:** Nylon 6,6. Hexamethylenediamine (H2N-(CH2)6-NH2) + adipic acid (HOOC-(CH2)4-COOH) -> amide bonds (-CONH-) + H2O at each linkage.

**Example:** Polyester (PET). Ethylene glycol + terephthalic acid -> ester bonds (-COO-) + H2O.

### Worked Example: Identifying Polymer Type

**Problem.** Classify the polymerization of styrene (C6H5CH=CH2).

**Analysis.** Styrene has a C=C double bond. The pi bond opens and monomers chain-link. No small molecule is released. This is addition polymerization, producing polystyrene.

**Problem.** Classify the formation of a polyamide from a diamine and a diacid.

**Analysis.** Each linkage forms an amide bond and releases H2O. Two different functional groups react. This is condensation polymerization.

## Biochemistry Basics

The four classes of biomolecules are all organic:

### Carbohydrates

**Monomers:** Monosaccharides (glucose C6H12O6, fructose, galactose).
**Polymers:** Disaccharides (sucrose, lactose), polysaccharides (starch, cellulose, glycogen).
**Bond:** Glycosidic linkage (C-O-C between sugar units). Formed by condensation; broken by hydrolysis.
**Function:** Energy storage (starch, glycogen), structural (cellulose in plant cell walls).

### Lipids

**Not true polymers** — diverse hydrophobic molecules. Fats/oils = glycerol + 3 fatty acids (ester bonds). Phospholipids = glycerol + 2 fatty acids + phosphate group (cell membranes). Steroids = four fused rings (cholesterol, hormones).
**Saturated vs. unsaturated:** Saturated fatty acids have no C=C bonds (solid at RT). Unsaturated have one or more C=C (liquid at RT, kinked chains reduce packing).

### Proteins

**Monomers:** 20 amino acids (H2N-CHR-COOH), each with a unique R group.
**Bond:** Peptide bond (amide linkage, -CO-NH-) formed by condensation.
**Levels of structure:** Primary (sequence), secondary (alpha-helix, beta-sheet from H-bonding), tertiary (3D fold from R-group interactions), quaternary (multi-subunit assembly).
**Function:** Enzymes (catalysis), structural (collagen, keratin), transport (hemoglobin), immune (antibodies).

### Nucleic Acids

**Monomers:** Nucleotides (sugar + phosphate + nitrogenous base).
**DNA:** Deoxyribose sugar. Bases: A, T, G, C. Double helix with complementary base pairing (A-T, G-C via hydrogen bonds).
**RNA:** Ribose sugar. Bases: A, U, G, C. Single-stranded.
**Bond:** Phosphodiester linkage (sugar-phosphate backbone).
**Function:** DNA stores genetic information. RNA translates it into proteins (mRNA, tRNA, rRNA).

### Worked Example: Hydrolysis of a Dipeptide

**Problem.** What products form when the dipeptide Gly-Ala is hydrolyzed?

**Reaction.** The peptide bond (-CO-NH-) between glycine and alanine is broken by adding water.

H2N-CH2-CO-NH-CH(CH3)-COOH + H2O -> H2N-CH2-COOH + H2N-CH(CH3)-COOH

Products: glycine and alanine (the two free amino acids). This is the reverse of condensation — the water molecule that was lost during peptide bond formation is restored.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Ignoring carbon's implicit hydrogens | Structural formulas often omit H atoms | Each carbon forms 4 bonds total; fill remaining with H |
| Markovnikov without considering carbocation stability | The rule is about the intermediate, not memorized patterns | Always identify which carbocation is more stable |
| Confusing SN1/SN2 conditions | Wrong mechanism predicts wrong stereochemistry and product | Check substrate class (primary vs. tertiary), nucleophile strength, solvent |
| Writing 5 bonds on carbon | Carbon NEVER exceeds 4 bonds (no expanded octet) | Count bonds carefully in every structure |
| Confusing structural and geometric isomers | Structural = different connectivity; geometric = same connectivity, different spatial arrangement | Ask: are the atoms connected the same way? |
| Treating condensation and addition polymers the same | Different mechanisms, different properties | Condensation releases small molecules; addition does not |

## Cross-References

- **pauling agent:** Molecular structure, bonding, and reaction mechanisms. Primary agent for organic structure and mechanism problems.
- **franklin agent:** Polymer science and materials applications of organic chemistry.
- **chemical-bonding skill:** Hybridization, sigma/pi bonds, and VSEPR directly underpin organic molecular geometry.
- **reactions-stoichiometry skill:** Organic reactions follow the same mass-balance and yield calculations.
- **analytical-methods skill:** Spectroscopic identification (IR, NMR, mass spec) is the primary tool for organic structure determination.
- **materials-chemistry skill:** Polymer properties connect to bulk material behavior and green chemistry.

## References

- Clayden, J., Greeves, N., & Warren, S. (2012). *Organic Chemistry*. 2nd edition. Oxford University Press.
- McMurry, J. (2016). *Organic Chemistry*. 9th edition. Cengage Learning.
- Bruice, P. Y. (2017). *Organic Chemistry*. 8th edition. Pearson.
- Nelson, D. L. & Cox, M. M. (2017). *Lehninger Principles of Biochemistry*. 7th edition. W. H. Freeman.
- Vollhardt, K. P. C. & Schore, N. E. (2014). *Organic Chemistry: Structure and Function*. 7th edition. W. H. Freeman.
- IUPAC. (2013). *Recommendations on Organic Nomenclature*. International Union of Pure and Applied Chemistry.
