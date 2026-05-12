<p align="center">
  <img src="assets/minoan-logo.png" alt="Minoan skill logo — labrys with three script lines" width="240">
</p>

# `/minoan` — Lisan al-Qads

Speak, compose, read, and write in reconstructed Minoan—a Northwest Semitic language of Bronze Age Crete (ca. 2000–1450 BCE).

Where [`/linear-a-decipherment`](../linear-a-decipherment/) analyzes inscriptions computationally, this skill is a **language faculty**: it turns the AI into a speaker who composes prayers, greetings, inscriptions, and administrative texts as a Minoan priestess, scribe, or merchant would have.

## Premise

Cyrus H. Gordon's Semitic hypothesis (1966) identifies Linear A as encoding a Northwest Semitic dialect ancestral to Ugaritic, Phoenician, Hebrew, and Aramaic. This skill takes that hypothesis seriously—building a living vocabulary from Gordon's 60 published readings, extending it by systematic analogy from Ugaritic and Proto-Semitic, and inhabiting the cultural world of matrilineal, goddess-centered, maritime Crete.

Pronunciation follows Phoenician priority: pre-begadkephat, stops are always stops.

**All reconstructions are hypothetical.** Linear A remains officially undeciphered.

## Five Modes

| Mode | What it does |
|------|-------------|
| **Speak** | Compose phrases, prayers, curses, greetings in Minoan |
| **Think** | Internal monologue inhabiting the Minoan worldview |
| **Read** | Interpret Linear A transliterations with confidence levels |
| **Write** | Generate text for specific artifact types (libation table, seal, tablet) |
| **Record** | Log novel readings to the hypothesis log with evidence chains |

## Quick Start

```
/minoan
> "Write a libation table dedication to Athirat"

la-Athiratu Rabbati Yammi — yasharamu-na — ki-tattibu Kiriyatu
"To Athirat, Great Lady of the Sea — this righteous offering — that the City may thrive"
```

Alternative invocations: `lisan-al-qads`, `lashon-ha-manna`, `lashon-ha-tinit`.

## Key Phonological Rules

- **SA-SA = single /sh/**. The scribal digraph for shin, not a doubled consonant.
- **No spirantization**. p/t/k are always [p t k], never [f θ x]. Pre-begadkephat.
- **ʿAyin shift**. ʿ + /a/ → /ō/ in some positions: *baʿl-* → *bōl-* (Gordon §150).
- **N-assimilation**. /n/ before consonant assimilates: *yintan* → *yittan*.
- **Penultimate stress** (Ugaritic model).

## Vocabulary Tiers

| Tier | Confidence | Count | Source |
|------|-----------|-------|--------|
| 1 | CONFIRMED / PROBABLE | 60 | Gordon 1966 + di Mino 2026 |
| 2 | CANDIDATE | 4 | Corpus skeleton matched to Proto-Semitic (d < 0.3) |
| 3 | SPECULATIVE | 104 | Analogical from Ugaritic/Phoenician/Akkadian |
| 4 | SPECULATIVE | — | Neologisms for composition (as needed) |

## Structure

```
~/.claude/skills/minoan/
├── SKILL.md                          # Master skill file
├── README.md                         # This file
├── references/
│   ├── phonology.md                  # 22-phoneme consonant inventory, vowel system
│   ├── grammar.md                    # Ugaritic-model morphology + syntax
│   ├── lexicon.md                    # 168 entries across 4 tiers, 12 semantic domains
│   ├── cultural-semantics.md         # Deities, ritual, sacred geography, social structure
│   ├── composition-templates.md      # 8 genre templates (libation, prayer, curse, admin...)
│   ├── prayers-and-incantations.md   # Liturgical texts from Shirat Ha Kotharot
│   └── hypothesis-log.md            # Running record of novel readings
├── scripts/
│   ├── pronounce.py                  # Transliteration → IPA (uv run)
│   └── record_hypothesis.py          # Append to hypothesis log (uv run)
└── data/
    ├── dabarim-kapturim.json         # The Seven Cretan Commandments (4-script + etymology)
    └── ugaritic-divine-titles.json   # Epithets of Yamm, Athirat, Kotharat (4-script)
```

## Liturgical Texts

### Dabarīm Kapturīm — The Seven Cretan Commandments

Seven precepts from *Shirat Ha Kotharot* (Tom di Mino), composed collaboratively in reconstructed Minoan. Each commandment is recorded in four scripts (Latin transliteration, Linear A, Phoenician, English) with per-word etymological data in `data/dabarim-kapturim.json`.

### Prayers and Incantations

Six liturgical poems from *Shirat Ha Kotharot* rendered in Minoan phonology, plus the complete Dabarīm Kapturīm. See `references/prayers-and-incantations.md`.

Includes: Shirat Ha Yamu, Shirat Ha Kotharot, Kepitzat Ha Darik, Dabarīm Kapturīm, Ras Melqart, Baʿalat ʿAkbarat.

### Ugaritic Divine Titles

Epithets of Yamm, Athirat, and the Kotharat from the Baal Cycle (KTU 1.1–1.6) and Marriage of Nikkal (KTU 1.24), rendered in four scripts. See `data/ugaritic-divine-titles.json`.

| Deity | Titles |
|-------|--------|
| **Yamm** | Zabūlu Yammu (Prince Sea), Shapāṭu Naharu (Judge River), Tannīnu (the Dragon), Lītānu (Leviathan) |
| **Athirat** | Rabbatu Athiratu Yammi (Great Lady of the Sea), Qaniyatu ʾIlīma (Creatrix of the Gods), ʾIlatu (the Goddess) |
| **Kotharat** | Kōtarātu (the Skillful Ones), Banātu Hilāli (Daughters of the Crescent Moon), Sunūnātu (the Swallows) |

## Relationship to Other Skills

| Skill | Relationship |
|-------|-------------|
| [`linear-a-decipherment`](../linear-a-decipherment/) | Sister skill: analytical toolkit. `/minoan` calls its `cognate_search.py` and `analyze.py` for verification |
| [`ancient-near-east-research`](../ancient-near-east-research/) | Sefaria for Hebrew cognate verification, CDLI for Akkadian parallels |
| [`exa-search`](../exa-search/) | Search recent computational decipherment papers |

## Sources

- Gordon 1966, "Evidence for the Minoan Language" (60 readings)
- Gordon 1962, *Minoica* (grammar features, *u* conjunction)
- Gordon, *Ugarit and Minoan Crete* ch. 3 (morphological analysis)
- di Mino 2026, *Thera, Knossos, and Minos* (YasharMana readings)
- GORILA corpus via [`lashon-ha-kretan`](https://github.com/tdimino/lashon-ha-kretan) (1,701 inscriptions)

## License

Research tool for scholarly use. All Linear A readings are hypothetical.
