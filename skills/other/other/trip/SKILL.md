# Trip Skill

Quick-create a trip planning note.

## Trigger

- `/trip <destination>` - Create trip note for destination
- `/trip <destination> <dates>` - Create with dates (e.g., "Paris 15-20 March")

## Workflow

1. Parse destination and optional dates from input
2. Create note using template: `+Templates/Trip.md`
3. Set filename: `Trip - <Destination>.md` (or `Trip - <Destination> <Year>.md` if year provided)
4. Pre-fill:
   - `destination`: From input
   - `country`: Infer from destination if obvious
   - `startDate`/`endDate`: If dates provided
   - `travellers`: Default to empty list (user fills in)
   - `status`: `idea` (default)
5. Open note for editing

## Examples

```
/trip Paris
→ Creates "Trip - Paris.md" with destination: Paris, country: France

/trip Barcelona 10-14 April 2026
→ Creates "Trip - Barcelona 2026.md" with dates filled in

/trip Lake District
→ Creates "Trip - Lake District.md" with country: UK
```

## Template Location

`+Templates/Trip.md`
