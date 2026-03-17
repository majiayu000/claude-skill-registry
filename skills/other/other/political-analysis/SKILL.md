---
name: political-analysis
description: Extract political and legal entities from narrative text. Use when analyzing governments, laws, courts, crimes, punishments, treaties, constitutions, and legal systems.
---
# political-analysis

Domain skill for political and legal system extraction.

## Entity Types

| Type | Description |
|------|-------------|
| `government` | Ruling body or political system |
| `law` | Law, regulation, or decree |
| `legal_system` | Legal framework or justice system |
| `court` | Court or judicial body |
| `judge` | Judge or magistrate |
| `jury` | Jury or decision panel |
| `lawyer` | Lawyer, advocate, or legal representative |
| `crime` | Crime or offense |
| `punishment` | Punishment or penalty |
| `evidence` | Evidence or proof |
| `witness` | Witness or testimony |
| `treaty` | Treaty or international agreement |
| `constitution` | Constitution or founding document |

## Extraction Rules

1. **Government structure**: Type (monarchy, democracy, theocracy, oligarchy), who rules
2. **Laws**: What is legal/illegal, penalties, enforcement
3. **Legal proceedings**: Trials, hearings, verdicts, judicial process
4. **Crimes**: Type, severity, accused, victim
5. **Treaties**: Parties involved, terms, enforcement mechanisms

## Output Format

Write to `entities/society.json` (society-team file):

```json
{
  "governments": [
    {
      "id": 1,
      "world_id": 1,
      "nation_id": 10,
      "region_id": null,
      "city_id": null,
      "name": "Eldorian Council",
      "description": "Oligarchic council of elders ruling Eldoria",
      "government_type": "oligarchy",
      "head_of_state_id": null,
      "head_of_government_id": null,
      "cabinet_member_ids": [],
      "branches": ["Executive", "Legislative", "Judicial"],
      "legislative_body_id": null,
      "legitimacy_source": "Popular mandate",
      "approval_rating": 62,
      "corruption_level": 2,
      "domestic_policy_ids": [],
      "foreign_policy_ids": [],
      "economic_policy_ids": [],
      "ministries": ["Justice", "Defense"],
      "ministry_head_ids": [],
      "military_control": "Direct",
      "seat_of_government_id": null,
      "allied_governments": [],
      "rival_governments": [],
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00",
      "version": 1
    }
  ],
  "laws": [
    {
      "id": 2,
      "world_id": 1,
      "legal_system_id": 5,
      "nation_id": 10,
      "region_id": null,
      "name": "Anti-Magic Decree",
      "description": "Forbids use of dark magic within city walls",
      "law_type": "criminal",
      "severity": "felony",
      "text": "Use of dark magic within city walls is prohibited.",
      "summary": "Bans dark magic in the city",
      "applies_to": ["Citizens", "Visitors"],
      "exceptions": [],
      "penalties": ["Imprisonment"],
      "minimum_penalty": "1 year",
      "maximum_penalty": "10 years",
      "enforcement_agency": "Royal Guard",
      "statute_of_limitations": "None",
      "enacted_date": "2026-02-01",
      "repealed_date": null,
      "is_active": true,
      "enacting_body": "Council Decree",
      "amendment_ids": [],
      "related_law_ids": [],
      "precedent_case_ids": [],
      "constitution_article_id": null,
      "treaty_id": null,
      "created_at": "2026-02-14T10:00:00+00:00",
      "updated_at": "2026-02-14T10:00:00+00:00",
      "version": 1
    }
  ],
  "next_id": 3
}
```

## Key Considerations

- **Implicit laws**: Cultural norms not written as statutes
- **Power corruption**: Official systems vs actual power (de jure vs de facto)
- **Multiple legal systems**: Different groups may have different laws
- **Cross-references**: If needed, track relationships separately in drafts, but final JSON must match `LoreData.from_dict`.
