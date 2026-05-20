---
name: grammar-syntax
description: Grammar and syntactic structures across human languages -- word order typology (SVO, SOV, VSO, VOS, OVS, OSV), morphological systems (isolating, agglutinative, fusional, polysynthetic), agreement patterns (gender, number, case, person), phrase structure, clause embedding, and cross-linguistic universals. Covers constituent analysis, dependency vs. constituency grammars, grammatical relations (subject, object, oblique), ergativity vs. accusativity, tense-aspect-mood systems, and how grammar encodes meaning differently across language families. Use when analyzing sentence structure, comparing grammar systems, teaching grammatical concepts, or understanding why a learner makes transfer errors from their L1.
type: skill
category: languages
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-11
first_path: examples/skills/languages/grammar-syntax/SKILL.md
superseded_by: null
---
# Grammar & Syntax

Grammar is the structural system that governs how words combine into phrases, clauses, and sentences to express meaning. Syntax is the subfield concerned specifically with sentence structure -- the rules for word order, phrase formation, and clause combination. This skill treats grammar as a cross-linguistic phenomenon: every human language has grammar, but the specific mechanisms vary enormously. Understanding these patterns as a meta-skill accelerates learning any particular language.

**Agent affinity:** chomsky-l (generative grammar, universals, parameter theory), krashen (acquisition order, natural grammar development)

**Concept IDs:** lang-word-order-typology, lang-morphology, lang-agreement-systems, lang-syntactic-structures

## Typological Overview

### Word Order Typology

Languages are classified by the default order of Subject (S), Object (O), and Verb (V) in a simple declarative transitive sentence.

| Order | Frequency | Examples | Correlates |
|---|---|---|---|
| **SOV** | ~45% of languages | Japanese, Korean, Turkish, Hindi, Basque, Quechua | Postpositions, noun-genitive, adjective-noun |
| **SVO** | ~42% | English, Mandarin, French, Russian, Swahili, Indonesian | Prepositions, genitive-noun (variable), noun-adjective (variable) |
| **VSO** | ~9% | Arabic (Classical), Irish, Welsh, Tagalog, Maori | Prepositions, noun-genitive, noun-adjective |
| **VOS** | ~3% | Malagasy, Tzotzil, Fijian | Prepositions, noun-genitive |
| **OVS** | <1% | Hixkaryana, Urarina | Postpositions |
| **OSV** | <1% | Warao (in some constructions) | Rare and debated |

Greenberg's universals (1963) established that word order correlates with other structural properties. SOV languages strongly tend to use postpositions ("the house in" rather than "in the house"), while SVO and VSO languages tend to use prepositions. These are statistical tendencies, not absolute rules.

### Morphological Typology

Languages differ in how much information is packed into a single word.

**Isolating (analytic).** Each word carries one morpheme. Little or no inflection. Mandarin Chinese is the canonical example: "I go" is "wo qu" -- no verb conjugation, no plural marker, no case marking.

**Agglutinative.** Words are built from clearly separable morphemes, each carrying one meaning. Turkish "evlerimde" = ev (house) + ler (plural) + im (my) + de (in) = "in my houses." Each suffix is distinct and productive.

**Fusional (inflectional).** Morphemes merge together, and a single affix may carry multiple grammatical meanings simultaneously. Latin "amabam" = am- (love) + -aba- (past imperfect) + -m (first person singular). The -m ending simultaneously encodes person, number, and voice.

**Polysynthetic.** Entire sentences can be expressed as a single word with many bound morphemes. Mohawk "sahonwanhotokawahse" encodes agent, patient, verb root, aspect, and direction in one word.

No language is purely one type. English is primarily isolating but has fusional remnants ("oxen," "was/were") and some agglutination ("un-friend-li-ness").

## Grammatical Relations

### Subject and Object

Most grammatical theories assume that sentences have structural positions for grammatical relations -- subject, object, and oblique. But languages mark these relations differently:

**Nominative-accusative.** The subject of intransitive and transitive sentences is marked the same way (nominative), while the object of a transitive sentence is marked differently (accusative). English, Latin, Russian, Japanese.

**Ergative-absolutive.** The subject of an intransitive sentence and the object of a transitive sentence are marked the same way (absolutive), while the agent of a transitive sentence is marked differently (ergative). Basque, many Australian languages, Dyirbal.

**Example (Basque):**
- "Gizona etorri da" -- The man(ABS) came. (Intransitive subject = absolutive)
- "Gizonak ogia jan du" -- The man(ERG) bread(ABS) ate. (Transitive agent = ergative, object = absolutive)

Understanding ergativity prevents the common learner assumption that "subject" works the same way in every language.

### Case Systems

Case is a morphological marking on nouns (or noun phrases) that indicates their grammatical role.

| Case | Function | Example (Latin) |
|---|---|---|
| Nominative | Subject | "puella" (the girl, as subject) |
| Accusative | Direct object | "puellam" (the girl, as object) |
| Genitive | Possession | "puellae" (of the girl) |
| Dative | Indirect object | "puellae" (to/for the girl) |
| Ablative | Various (from, by, with) | "puella" (by the girl) |
| Locative | Location | Finnish "talossa" (in the house) |
| Instrumental | Means | Russian "nozhem" (with a knife) |

Some languages have 2 cases (English: nominative/objective in pronouns), others have 15+ (Finnish has 15, Hungarian has 18). Languages without case marking rely on word order or particles to signal grammatical relations.

## Agreement Systems

Agreement (or concord) is the requirement that certain words in a sentence match in grammatical features.

### Subject-Verb Agreement

Languages vary in what the verb must agree with:

- **Person and number only:** English "I run" / "she runs"
- **Person, number, and gender:** Arabic "kataba" (he wrote) / "katabat" (she wrote)
- **Person, number, and class:** Swahili uses noun class prefixes that propagate through the sentence

### Gender Systems

Gender is a noun classification system that affects agreement on articles, adjectives, verbs, and pronouns.

- **Two-gender (masculine/feminine):** French, Arabic, Hindi
- **Three-gender (masculine/feminine/neuter):** German, Russian, Latin
- **Noun class systems (5-20+ classes):** Bantu languages classify nouns by semantic and phonological criteria -- Swahili has ~18 classes including people, trees, abstract concepts, paired objects
- **No grammatical gender:** Mandarin, Turkish, Finnish, Hungarian

Gender assignment is partly semantic (biological sex for animates) and partly arbitrary (why is "table" feminine in French but masculine in German?). Learners must memorize gender for each noun.

## Tense, Aspect, and Mood

### Tense

Tense locates an event in time relative to the moment of speaking.

- **Past/present/future:** English, French, Swahili
- **Past/non-past:** Japanese, Arabic (perfective/imperfective rather than strict past/present)
- **No grammatical tense:** Mandarin, Burmese -- time is expressed through adverbs, context, or aspect markers

### Aspect

Aspect describes the internal temporal structure of an event -- whether it is completed, ongoing, habitual, or beginning.

- **Perfective:** Views the event as a completed whole. Russian "ya napisal" (I wrote, finished writing).
- **Imperfective:** Views the event as ongoing or habitual. Russian "ya pisal" (I was writing / I used to write).
- **Progressive:** Currently in progress. English "I am writing."
- **Habitual:** Regularly recurring. English "I write (every day)."

Some languages (English) express aspect periphrastically ("is writing"), others (Russian) encode it in verb morphology, and others (Mandarin) use particles ("le" for completion, "zhe" for duration).

### Mood

Mood expresses the speaker's attitude toward the reality of the event.

- **Indicative:** Asserts something as fact. "She studies linguistics."
- **Subjunctive:** Expresses doubt, wish, or non-reality. Spanish "Espero que ella estudie" (I hope she studies -- subjunctive because unrealized).
- **Imperative:** Commands. "Study!"
- **Conditional:** Dependent on a condition. French "j'etudierais" (I would study).
- **Evidential:** Marks the source of information. Turkish "-mis" indicates hearsay: "gelmis" = "apparently came." Quechua has direct-experience, inferential, and hearsay evidentials.

## Phrase Structure and Embedding

### Phrase Structure

Sentences are not flat sequences of words but hierarchical structures of phrases. A noun phrase (NP) contains a head noun with its modifiers; a verb phrase (VP) contains a head verb with its complements.

**Constituency tests** reveal phrase boundaries:
- **Substitution:** "The tall woman in the red coat" can be replaced by "she" -- it is a constituent.
- **Movement:** "In the park, the children played" -- "in the park" moved as a unit.
- **Coordination:** "The cat and the dog" -- only constituents can be conjoined with "and."

### Embedding and Recursion

Human language allows clauses to be embedded inside other clauses, in principle without limit:

"The cat [that the dog [that the child [that I know] brought] chased] ran away."

This property -- **recursion** -- is proposed by Chomsky as a defining feature of human language. It allows infinite expressiveness from finite means.

### Relative Clauses

Languages differ in how they form relative clauses:

- **Gap strategy:** English "the book [that I read __]" -- the relativized position is left empty.
- **Resumptive pronoun:** Arabic "al-kitab [allathi qara'tuhu]" (the book [that I-read-it]) -- a pronoun fills the relativized position.
- **Prenominal relative clause:** Japanese "[watashi ga yonda] hon" ([I read] book) -- the clause precedes the noun.
- **Correlative:** Hindi "jo kitab maine padhi, vo acchi thi" (which book I read, that good was) -- correlative and demonstrative in separate clauses.

## Cross-Linguistic Transfer

Understanding grammar typology explains why learners make specific errors:

| L1 Feature | L2 Feature | Predicted Transfer Error |
|---|---|---|
| SOV word order (Japanese) | SVO word order (English) | Verb placed at end: "I the book read" |
| No articles (Russian) | Definite/indefinite articles (English) | Article omission: "I saw cat" |
| Pro-drop (Spanish) | Obligatory subjects (English) | Subject omission: "Is raining" |
| No gender (Turkish) | Grammatical gender (German) | Gender assignment errors: "der Madchen" instead of "das Madchen" |
| No tense marking (Mandarin) | Obligatory tense (English) | Tense omission: "Yesterday I go" |

These are not random mistakes but systematic reflections of the learner's L1 grammar. Lado's contrastive analysis framework (see lado agent) formalizes this prediction process.

## Cross-References

- **chomsky-l agent:** Universal Grammar, principles and parameters, generative syntax trees. The theoretical framework for why languages vary in specific, constrained ways.
- **krashen agent:** Natural order of grammar acquisition -- some structures are acquired before others regardless of teaching order.
- **lado agent:** Contrastive analysis -- systematic comparison of L1 and L2 grammar to predict difficulty.
- **baker agent:** Grammar in multilingual contexts -- code-switching follows grammatical constraints.
- **phonetics-phonology skill:** Morphophonology connects grammatical changes to sound changes.
- **pragmatics-communication skill:** Grammar interacts with pragmatics -- word order may encode information structure (topic, focus) rather than grammatical relations.

## References

- Comrie, B. (1989). *Language Universals and Linguistic Typology*. 2nd edition. University of Chicago Press.
- Greenberg, J. H. (1963). "Some universals of grammar with particular reference to the order of meaningful elements." In J. H. Greenberg (Ed.), *Universals of Language*. MIT Press.
- Dixon, R. M. W. (1994). *Ergativity*. Cambridge University Press.
- Dryer, M. S. & Haspelmath, M. (Eds.). (2013). *The World Atlas of Language Structures Online*. Max Planck Institute. (wals.info)
- Tallerman, M. (2015). *Understanding Syntax*. 4th edition. Routledge.
- Chomsky, N. (1981). *Lectures on Government and Binding*. Foris Publications.
