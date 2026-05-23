---
name: taxonomic-classification
description: Naming and classifying organisms through binomial nomenclature, the Linnaean hierarchy, type specimens, and the rules governing taxonomic authority and revision. Covers the structure of a scientific name, the ranks from domain to subspecies, the codes (ICZN, ICN, ICNP), and the modern phylogenetic refinements that reshape the classical system. Use when the task is to place a known organism in its formal hierarchy or to reason about how names change over time.
type: skill
category: nature-studies
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/nature-studies/taxonomic-classification/SKILL.md
superseded_by: null
---
# Taxonomic Classification

Every organism has at least one name. Most have several: a common name that varies by language and region, a scientific name that is globally stable, a taxonomic position within a hierarchy that lets it be related to other organisms, and a reference specimen that anchors the name to a particular physical example. Taxonomic classification is the discipline of assigning and maintaining these names. It is not an activity of the field — the field identifier reaches the right species, and the taxonomist places that species in its rank, verifies its authority, and reconciles its name across traditions.

**Agent affinity:** linnaeus (binomial naming, rank assignment, hierarchy construction)

**Concept IDs:** nature-plants-fungi, nature-animals-birds, nature-ecology-habitats

## The Structure of a Scientific Name

A valid scientific name consists of the genus, the specific epithet, and optionally the authority and year.

```
Quercus   alba   L.
 genus   epithet  authority (Carl Linnaeus)
```

Formatting rules are strict and universally observed:

- **Genus** is capitalized and italicized: *Quercus*.
- **Specific epithet** is lowercase and italicized: *alba*.
- **Authority** is the person who first validly published the name, written in plain text: L. (standard abbreviation for Linnaeus).
- **Subspecies, variety, or form** follow the epithet with a connector: *Quercus alba* var. *repanda*.

A full binomial unambiguously identifies a species across all languages and all local names. *Castor canadensis* is the same animal in Portuguese, Japanese, and Cree, even though the common name differs everywhere.

## The Linnaean Hierarchy

Carl Linnaeus (1707–1778) proposed the nested system of ranks that still underlies formal classification. The major ranks, in descending order:

| Rank | Example (Humans) | Example (Eastern Gray Squirrel) |
|---|---|---|
| Domain | Eukarya | Eukarya |
| Kingdom | Animalia | Animalia |
| Phylum | Chordata | Chordata |
| Class | Mammalia | Mammalia |
| Order | Primates | Rodentia |
| Family | Hominidae | Sciuridae |
| Genus | *Homo* | *Sciurus* |
| Species | *sapiens* | *carolinensis* |

Intermediate ranks exist whenever the core ranks are insufficient. Subphylum, superfamily, tribe, subgenus, subspecies — any rank can be subdivided when the phylogeny demands it.

### Which ranks are obligatory

In practice, every described organism is placed in at least kingdom, phylum (or division, for plants and fungi), class, order, family, genus, and species. Other ranks are optional and appear only where structural needs demand them.

### Monophyly as the modern constraint

A valid rank in modern taxonomy must be **monophyletic**: it must contain a common ancestor and all of that ancestor's descendants, and nothing else. This constraint has forced large revisions to the Linnaean system, because many classical groups (Reptilia, Pisces, "Protista") turned out to be paraphyletic or polyphyletic and had to be split or subsumed.

A group that contains an ancestor but not all descendants is **paraphyletic** — the classical Reptilia (which excluded birds) is the standard example. A group that combines descendants of multiple ancestors is **polyphyletic** — "warm-blooded animals" combining mammals and birds is the textbook example. Neither is considered valid in modern phylogenetic systematics.

## The Nomenclatural Codes

Different kingdoms are governed by different codes. The codes are legal documents, not scientific theories — they settle questions of priority, authority, and validity.

| Code | Governs | Key body |
|---|---|---|
| **ICZN** (International Code of Zoological Nomenclature) | Animals | International Commission on Zoological Nomenclature |
| **ICN** (International Code of Nomenclature for algae, fungi, and plants) | Plants, algae, fungi | International Association for Plant Taxonomy |
| **ICNP** (International Code of Nomenclature of Prokaryotes) | Bacteria, archaea | International Committee on Systematics of Prokaryotes |
| **ICVCN** (International Code of Virus Classification and Nomenclature) | Viruses | International Committee on Taxonomy of Viruses |

Each code specifies:

1. **Priority.** The earliest validly published name has precedence. Later names become synonyms.
2. **Validity requirements.** Publication standards, type specimens, diagnostic descriptions.
3. **Homonymy rules.** The same name cannot be used for two different organisms within a kingdom.
4. **Revision procedures.** How a name can be changed, split, or merged, and who has the authority.

## Type Specimens

Every validly published species name is anchored to a **type specimen** — a physical example deposited in a recognized collection. The type specimen is the reference that the name always points to, even if later work reveals that the original description covered more than one species.

### Types of types

- **Holotype**: the single specimen designated by the original author as the name-bearing specimen.
- **Paratype**: additional specimens cited in the original description but not the single name-bearing one.
- **Lectotype**: a specimen selected later to serve as the name-bearing specimen when the original author did not designate a holotype.
- **Neotype**: a replacement designated when the original types are lost or destroyed.
- **Syntype**: one of several specimens cited equally in a description lacking a holotype.

When a species is split, the name stays with whichever new species contains the holotype. The other new species needs a new name with its own type. This rule is the reason taxonomic revisions are constrained — the code does not let authors reassign names freely.

## Authority and Citation

The authority is the person (or people) who first validly published the name. Standard practice is to cite the authority after the species name, usually in parentheses if the species has been moved to a different genus since the original description.

### Examples

- *Quercus alba* L. — Originally described by Linnaeus in the genus *Quercus*. No move, no parentheses.
- *Felis concolor* (Linnaeus, 1771) — Originally described by Linnaeus as *Felis concolor*, later moved to *Puma*. Full citation: *Puma concolor* (Linnaeus, 1771). Parentheses indicate the move.
- *Diplodocus carnegii* Hatcher, 1901 — Described by John Bell Hatcher in 1901. No move.

For botanical names, the codes use the `ex` and `in` conventions to handle complex authority histories:

- *Trifolium repens* L. — Standard.
- *Thlaspi alpestre* L. sensu auct. eur. non L. — "In the sense of European authors, not in the sense of Linnaeus himself," flagging that the name has been misapplied.

## Synonymy and Revision

Names change. Species get split when a formerly single species is recognized as two; species get merged when what looked like two are found to be one. Genera move; families dissolve; orders fragment.

### Synonyms

A **synonym** is a name that is no longer the accepted name but was once applied to the same species. Databases like Catalogue of Life, WoRMS, GBIF, and Tropicos maintain synonym lists so that legacy literature can be mapped to current taxonomy.

There are two classes of synonym:

- **Objective synonyms** share the same type specimen. One of them must be suppressed by priority.
- **Subjective synonyms** share the same species in the opinion of a particular taxonomist. Different taxonomists may disagree about whether two names are synonymous.

### Revisions

A taxonomic revision reassesses a group and publishes the new arrangement. Revisions happen when:

1. New species are discovered.
2. Phylogenetic analysis (morphological or molecular) reveals the existing arrangement is not monophyletic.
3. Type specimens are reexamined and found not to match their published descriptions.
4. Previously undetected homonymy is discovered.

A revision is only authoritative after it is accepted by the taxonomic community, which typically happens through citation and adoption by databases over months to years.

## Common Name vs Scientific Name

Common names are unstable. The same species is called different things in different regions. The same name is applied to different species across regions. Common names are also political — whales that were once "blackfish" are now "killer whales" or "orcas" depending on the speaker.

Scientific names serve three roles that common names cannot:

1. **Stability across languages.** *Ursus arctos* is the same brown bear in Kazakh, Portuguese, and Inuktitut.
2. **Stability across time.** A 1930s field guide and a 2020s database can both refer to *Ursus arctos* without ambiguity.
3. **Phylogenetic information.** The genus *Ursus* tells you the species is a bear; the family Ursidae places it among bears generally; the order Carnivora places it among meat-eaters.

Common names should still be used for communication with non-specialists. But records and research should carry the scientific name as the primary key.

## When to Use This Skill

- The user has an identified organism and wants the full taxonomic breakdown.
- The user is confused about why a species they remember from an old guide has a different name now.
- The user needs to resolve a synonymy — "is *X* the same as *Y*?"
- The user is preparing a species list for a field trip or checklist and needs to standardize names.
- The user is citing a species in writing and needs the correct authority and formatting.

## When NOT to Use This Skill

- The user wants to identify an unknown organism (promote to `field-identification`).
- The user wants to understand behavior or ecology (promote to `species-interaction-tracking` or `ecosystem-mapping`).
- The user wants to know where the species lives geographically (partial overlap with `ecosystem-mapping`).
- The user wants to make a nature-journal entry (promote to `nature-journaling`).

## Decision Guidance

Begin every classification request by asking:

1. **Is the name current?** Check a modern authority (GBIF, Catalogue of Life, ITIS, or the group-specific database) before offering a taxonomy.
2. **What was the previous name?** If the name has changed, note the synonym so the user can reconcile with older literature.
3. **What rank is the user operating at?** A species-level question is different from a family-level question.
4. **Is the phylogeny contested?** Some groups (fungi, protists, many insect orders) have ongoing taxonomic instability. Flag this honestly rather than presenting one authority as settled.

## Cross-References

- **linnaeus agent:** Binomial naming, hierarchy construction, authority reconciliation.
- **peterson agent:** Gives a field ID that then needs classification.
- **von-humboldt-nat agent:** Biogeographic context for where a species fits in regional assemblages.
- **field-identification skill:** Produces the organism name that this skill then classifies.
- **ecosystem-mapping skill:** Places classified species in their habitats and assemblages.

## References

- Linnaeus, C. (1753). *Species Plantarum*. Laurentius Salvius.
- Linnaeus, C. (1758). *Systema Naturae*, 10th ed. Laurentius Salvius. (Starting point for zoological nomenclature under the ICZN.)
- International Code of Zoological Nomenclature, 4th edition (1999), with subsequent amendments.
- International Code of Nomenclature for algae, fungi, and plants (Shenzhen Code, 2018).
- Hennig, W. (1966). *Phylogenetic Systematics*. University of Illinois Press. (Founding text of cladistic methodology.)
- Mayr, E. (1942). *Systematics and the Origin of Species*. Columbia University Press.
- GBIF Backbone Taxonomy (https://www.gbif.org/). Living reference database.
- Catalogue of Life (https://www.catalogueoflife.org/). Species list and synonymy.
