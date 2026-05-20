---
name: add-cave
description: Add a new cave to the Jaskiniowy Kataster Tatr Zachodnich project. Creates the full directory structure, SRV files, _RAW/ folder, and KATASTER.wpj entry.
argument-hint: <cave-id> <valley-path> [source-zip]
---

Add a new cave to the kataster project.

Arguments: $ARGUMENTS
Expected format: `<cave-id> "<valley/subdir/path>" [/path/to/source.zip]`
Example: `/add-cave T.D-08.07 "Dolina Koscieliska/Organy" /tmp/MROZN.SRV.zip`

---

## Step 1 — Look up cave data in PIG database (single call)

The cave ID is ASCII — search for it directly with a single grep:

```bash
grep '"<cave-id>"' doc/jaskinie_polski_pig_dump.jsonl
```

Parse the returned JSON for:
- `name` → CAVE_NAME (use ASCII equivalents for diacritics: ą→a, ć→c, ł→l, ó→o, ś→s, ź/ż→z, ę→e, ń→n)
- `latitude`, `longitude`, `absolute_height_masl` → entrance coordinates
- `other_names`, `authors_of_study`, `editorial` → for README and metadata

If not found by ID, try searching by partial ASCII name.

## Step 2 — Convert coordinates to DMS (single Node.js call)

Run one Node.js command to produce both the DMS string and verify the location:

```bash
node -e "
const lat = <latitude>; const lon = <longitude>;
const toDMS = (v) => {
  const d = Math.floor(v), m = Math.floor((v-d)*60);
  const s = (((v-d)*60-m)*60).toFixed(3).padStart(6,'0');
  return d+':'+String(m).padStart(2,'0')+':'+s;
};
console.log('N'+toDMS(lat)+'  E'+toDMS(lon));
"
```

## Step 3 — Determine directory path

Valley path from arguments (use ASCII, no diacritics in directory names):
`Jaskinie-poligony/<valley-path>/<Cave Name ASCII>/`

Check if the valley subdirectory already exists. Match the style of neighbouring caves in that directory.

## Step 4 — Handle source files

If a source ZIP was provided:
1. Extract: `unzip -o <source.zip> -d /tmp/<cave_ascii>_raw/`
2. List contents: `find /tmp/<cave_ascii>_raw -not -path "*/__MACOSX*" -type f`
3. Read each survey file to understand its format (units, station naming, number of readings)

## Step 5 — Create directory structure

```bash
mkdir -p "Jaskinie-poligony/<valley-path>/<Cave Name>/_RAW"
```

Copy source files to `_RAW/` preserving original names (never rename raw files):
```bash
cp /tmp/<cave_ascii>_raw/<file> "Jaskinie-poligony/<valley-path>/<Cave Name>/_RAW/"
```

## Step 6 — Create _RAW/README.md

Use Polish language. Required fields:
- **Źródło** — origin / who provided the data
- **Autorzy pomiarów** — survey authors (from PIG `authors_of_study`)
- **Data pomiaru** — survey date (from PIG or source file headers)
- **Data pozyskania** — date the file was obtained (from file timestamp if unknown)
- **Dodał** — who added it to _RAW/ (ask user if unknown)
- **Kompletność** — completeness notes (format, number of files, missing data)
- **## Pliki** — list every file in _RAW/ with a one-line description

Leave any genuinely unknown fields as `nieznany` / `nieznane`.

## Step 7 — Determine station prefix

From cave ID `T.X-NN.MM` → prefix = `tXNNMM` (e.g., T.D-08.07 → `td0807`).
Or use a short cave name abbreviation (e.g., MROZN) — check what style neighbouring caves use.

## Step 8 — Create CAVE_M.SRV

```
#[
CAVE_ID         "T.X-NN.MM"
CAVE_NAME       "Cave Name ASCII"
UPDATE_DATE     <today YYYY-MM-DD>
PROJECT_NAME    "Kataster jaskin tatrzanskich"
COORDINATOR     "Dariusz Lubomski"
COORDINATOR_EMAIL "darek.lubomski@gmail.com"
REFERENCE_SYSTEM "WGS84"
COORDINATE_SYSTEM "UTM"
DATA_SOURCE     "Panstwowy Instytut Geologiczny"
LICENSE         "http://creativecommons.org/licenses/by-sa/2.0/"
#]

#prefix <PREFIX>
#flag   <STATION>   /<Cave Label>
#note   <STATION>   /<Cave Label>
#fix    <STATION>   E<lon-dms>  N<lat-dms>  <elevation>m
```

`<STATION>` is the entrance station name in the survey (e.g. `td0807.1.3`).
If the entrance station is unknown, comment out all three lines and add a TODO note:
```
; #flag  ???  /<Cave Label>
; #note  ???  /<Cave Label>
; #fix   ???  E<lon-dms>  N<lat-dms>  <elevation>m  ; TODO: uzupelnic numer stacji wejscia
```

## Step 9 — Create CAVE_S.SRV

```
#[
CAVE_ID         "T.X-NN.MM"
CAVE_NAME       "Cave Name ASCII"
SURVEY_ID       <PREFIX>
SURVEY_NAME     "<Cave Name ASCII>"
UPDATE_DATE     <today YYYY-MM-DD>
PROJECT_NAME    "Kataster jaskin tatrzanskich"
COORDINATOR     "Dariusz Lubomski"
COORDINATOR_EMAIL "darek.lubomski@gmail.com"
DATA_SOURCE     "<source or nieznane>"
LICENSE         "http://creativecommons.org/licenses/by-sa/2.0/"

TEAM "<authors from PIG or nieznany>"
INSTRUMENT "<instrument or nieznany>"
#]

#prefix <PREFIX>
#date <YYYY-MM-DD>
#units meters order=DAV
#units A=D V=D

;<Section description>

FROM    TO      DISTANCE    AZIMUTH     INCLINATION
0       1       4.61        293         2
1       2       2.06        303         7

;Splay shots (cross-sections)

0       -       5.52        51          8
0       -       5.47        265         76
```

`SURVEY_ID` and `SURVEY_NAME` are inside `#[...]` which is a block comment — Walls ignores it entirely. These fields are project convention only; omit them if unknown.

If the raw source file contains multiple readings per shot, note this and leave measurements as TODO:
```
; TODO: przetworzyc pomiary z _RAW/<filename>
; Plik zrodlowy zawiera pomiary potrojne — wymagaja usrednienia lub konwersji.
; Stacje numerowane od <first-station> — numer stacji otworu nieznany.
```

## Step 10 — Update KATASTER.wpj

**IMPORTANT: Ask the user to close Walls before this step.** Walls overwrites the .wpj file when it saves, discarding any manually added entries.

Find the correct `.BOOK` parent in KATASTER.wpj. The path hierarchy corresponds to the directory structure:
- Each `.BOOK` with `.PATH <dir>` builds the cumulative path from the project root
- Surveys without their own `.PATH` inherit the parent book's path

Insert a new `.BOOK` block for the cave in the correct location:

```
.BOOK	<Cave Name ASCII>
.NAME	<SHORT_ID>
.PATH	<Cave Name ASCII>
.STATUS	8
.SURVEY	<Cave Name ASCII> meta
.NAME	<PREFIX>_M
.STATUS	8
.SURVEY	<Cave Name ASCII> pomiary
.NAME	<PREFIX>_S
.STATUS	8
.ENDBOOK
```

Use `Edit` tool with sufficient surrounding context to make the match unique.
Verify with: `grep -n "<PREFIX>" KATASTER.wpj`

## Step 11 — Summary

Report to the user:
- Files created (list all paths)
- Data filled in vs left as TODO/unknown
- Any fields needing manual follow-up (entrance station, instrument, who added raw files)
- Reminder: if Walls was open, it may overwrite the .wpj entry — check after reopening
