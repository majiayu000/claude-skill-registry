---
name: cultural-research
description: "Use this to autonomously populate Martinique_DB. Takes a cultural topic from the 6 CoT circles, runs a deep research loop using gpt-researcher or web search, structures findings into DB-ready entries, and loops until coverage is sufficient."
---

# Cultural Research Loop — Martinique_DB Population

Autonomously research and populate a cultural knowledge circle in Martinique_DB. This skill applies the Karpathy autoresearch pattern to knowledge base construction: run overnight, wake up to a populated DB.

## The 6 Cultural Circles (from reflexion_structuree_cot.md)

Priority order for population:
1. **Cercle 1** — L'individu (daily life, demographics, habits)
2. **Cercle 2** — La communauté (family, social structure, annual traditions)
3. **Cercle 3** — La culture profonde (language, music, food, arts)
4. **Cercle 4** — Le territoire (geography, communes, flora/fauna)
5. **Cercle 5** — Histoire & identité (historical timeline, intellectual thought)
6. **Cercle 6** — Économie & enjeux contemporains (economy, current issues, health)

## Research Loop

```
LOOP FOREVER (until manually stopped or coverage target met):

1. Check coverage report — which sub-topics in the target circle are empty or thin?
2. Pick the thinnest sub-topic
3. Run research (gpt-researcher / web search / Wikipedia FR)
4. Structure findings into DB entries (see Entry Format below)
5. Write entries to martinique_db/data/<circle>/<topic>.json
6. Update coverage report
7. If circle coverage >= 80%, advance to next circle
```

## Entry Format

Every entry in Martinique_DB must include these metadata fields:

```json
{
  "id": "unique slug",
  "title": "string",
  "content": "string — the actual knowledge, 100-500 words",
  "category": "cercle_1 | cercle_2 | cercle_3 | cercle_4 | cercle_5 | cercle_6",
  "sub_category": "string — e.g. 'gastronomie', 'musique', 'commune'",
  "language": "fr | creole | bilingual",
  "source": "oral | web | institutional | wikipedia",
  "reliability": "verified | tradition | estimate",
  "temporality": "historical | current | evolving",
  "geo": "string — commune, zone (nord/sud/centre), or 'all'",
  "entities": ["list of named entities — people, places, events"],
  "relations": [{"entity": "string", "relation": "string", "target": "string"}],
  "created_at": "ISO date"
}
```

## Research Sources Priority

1. Wikipedia FR (Martinique pages) — structured, reliable
2. Collectivité de Martinique official site
3. France-Antilles archives
4. Academic sources (CNRS, université Antilles)
5. ATV / RCI / Martinique La 1ère
6. YouTube: transcribe via faster-whisper for oral/musical content

## Coverage Metric

Coverage = number of non-empty sub-topics / total sub-topics in circle × 100.

Target: 80% coverage per circle before advancing. Store in `martinique_db/coverage.json`.

## NEVER STOP rule

Once the loop has started, do NOT pause to ask if you should continue. The human may be asleep. Run until manually interrupted or 80% coverage is reached for all 6 circles.
