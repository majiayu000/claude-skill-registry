---
name: grupo-venus
description: Astrological charts, transit forecasts, and compatibility reports via grupovenus.com. Manage multiple people and compare charts conversationally.
license: MIT
metadata: {"category":"astrology","api_base":"https://grupovenus.com","author":"https://github.com/apresmoi","homepage":"https://github.com/apresmoi/grupo-venus"}
user-invokable: true
---

# Grupo Venus

Use this skill to fetch free astrological charts, transit forecasts, and compatibility reports from **grupovenus.com** — a classic ASP astrology platform with a rich free tier. Manage multiple people in memory and analyze charts conversationally.

> **Unofficial skill.** Not affiliated with or endorsed by Grupo Venus. Uses the public free tier of grupovenus.com as-is.

**Base URL:** `https://grupovenus.com`
**No API key required.** Data is session-cookie based; person data is stored locally in memory.

---

## People Storage

All person data lives in your memory file. Load it before any operation:

```
~/.openclaw/workspace/memory/grupo-venus.json
```

Structure (we use Luis Alberto Spinetta as the example throughout this skill — because he's from another planet):
```json
{
  "people": {
    "spinetta": {
      "name": "Luis Alberto Spinetta",
      "birthdate": "1/23/1950 4:35:00 PM",
      "city": "Buenos Aires",
      "country": "Argentina",
      "sex": "H",
      "tz_offset": "3",
      "lat_dms": "34S35",
      "lon_dms": "58W22",
      "lat_decimal": -34.5833,
      "lon_decimal": 58.3667,
      "style": "deep"
    }
  }
}
```

**sex:** `H` = Hombre (male), `V` = Varón/Mujer — use `H` for male, `V` for female.
**tz_offset:** Hours from UTC, sign inverted: `3` = UTC-3 (Argentina), `-1` = UTC+1 (Madrid).
**lat_dms / lon_dms:** `34S35` = 34°35′S, `58W22` = 58°22′W. N/S and E/W are explicit.
**style:** Communication style preference — `casual`, `deep`, or `practical`. See Voice & Style section.

If the file doesn't exist yet, create it with `{"people": {}}`.

---

## Adding a Person

### Step 1 — Look up the city coordinates

```bash
curl -s "https://grupovenus.com/buscaciudjson.asp?q=CITY&pais=COUNTRY"
```

Example:
```bash
curl -s "https://grupovenus.com/buscaciudjson.asp?q=Bahia+Blanca&pais=Argentina"
# → [{"label":"Bahia Blanca, Argentina"}]
```

This confirms the city/country string the server recognises. Use the exact spelling returned.

### Step 2 — Register the person to get coordinates + timezone

The server requires a properly established session with Referer headers. **Always use a cookie jar** (`-c`/`-b`) — manually passing a single ASPSESSION cookie will result in "session expired" errors.

```bash
COOKIEJAR=$(mktemp)

# 2a. Establish session
curl -s -c "$COOKIEJAR" -b "$COOKIEJAR" "https://grupovenus.com/info.asp" \
  -H "User-Agent: Mozilla/5.0" > /dev/null

# 2b. Load the registration form (sets server-side session state)
curl -s -c "$COOKIEJAR" -b "$COOKIEJAR" "https://grupovenus.com/personas.asp?nue" \
  -H "User-Agent: Mozilla/5.0" \
  -H "Referer: https://grupovenus.com/info.asp" > /dev/null

# 2c. POST the person data (Referer header is required)
# IMPORTANT: city names with accents must be encoded in iso-8859-1, NOT UTF-8.
# e.g. "Bahía Blanca" → "Bah%EDa+Blanca" (%ED = í in Latin-1, NOT %C3%AD which is UTF-8)
# If the city is not recognized, the server silently assigns wrong/default coordinates.
# Verify by checking that the city and country fields are non-empty in the d0 cookie response.
curl -s -c "$COOKIEJAR" -b "$COOKIEJAR" -X POST "https://grupovenus.com/ciuda.asp" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "User-Agent: Mozilla/5.0" \
  -H "Referer: https://grupovenus.com/personas.asp?nue" \
  --data "urldestino=personas.asp%3Fok&nombre=NAME&DIA=DD&MES=MM&ANO=YYYY&HORA=HH&MINU=MM&08CIUDAD=CITY&14PAIS=COUNTRY&SEXO=H" > /dev/null

# 2d. Follow redirect to personas.asp?ok — the d0 cookie is set here
PERSONAS_RESP=$(curl -si -c "$COOKIEJAR" -b "$COOKIEJAR" "https://grupovenus.com/personas.asp?ok" \
  -H "User-Agent: Mozilla/5.0" \
  -H "Referer: https://grupovenus.com/ciuda.asp")
```

The `personas.asp?ok` response sets two cookies in its headers:

```
Set-Cookie: d0=NAME;M/D/YYYY H:MM:SS AM/PM;CITY;COUNTRY;SEX;;TZ;latNS;lonEW
Set-Cookie: haycoo=NAME;TZ;DATE;TIMEZONE_NAME;
```

Extract and URL-decode the `d0` value from `$PERSONAS_RESP`:

```bash
D0=$(echo "$PERSONAS_RESP" \
  | grep -i 'set-cookie.*d0=' \
  | sed 's/.*d0=//I' | cut -d';' -f1 \
  | python3 -c "import sys,urllib.parse; print(urllib.parse.unquote(sys.stdin.read().strip()))")
echo "d0 decoded: $D0"
# → NAME ;M/D/YYYY H:MM:SS AM/PM;CITY;COUNTRY;SEX;;TZ;latDMS;lonDMS
```

Fields (semicolon-separated):
- Field 7: `tz_offset`
- Field 8: `lat_dms` (e.g. `38S43`)
- Field 9: `lon_dms` (e.g. `62W17`)

Convert DMS to decimal for storage:
- `34S35` → `-(34 + 35/60)` = `-34.5833`
- `58W22` → `58 + 22/60` = `58.3667` (positive = West, as stored by the server)

Save the full person entry to `grupo-venus.json`.

### Field reference for `ciuda.asp` POST

| Field | Value |
|-------|-------|
| `urldestino` | `personas.asp?ok` (URL-encoded) |
| `nombre` | Person's name |
| `DIA` | Birth day (1–31) |
| `MES` | Birth month (1–12) |
| `ANO` | Birth year (4 digits) |
| `HORA` | Birth hour 0–23 (local time) |
| `MINU` | Birth minute 0–59 |
| `08CIUDAD` | City name |
| `14PAIS` | Country name |
| `SEXO` | `H` or `V` |

> **Note:** The `nom2=nue` field seen in older docs does not exist in the actual form and must be omitted. The `Referer: https://grupovenus.com/personas.asp?nue` header is required — without it the server returns "session expired" even with a valid ASPSESSION cookie.

---

## Building the Cookie String

All report endpoints need the `nombre` value — the semicolon-delimited person string:

```
"NAME ;M/D/YYYY H:MM:SS AM/PM;CITY;COUNTRY;SEX;;TZ;latDMS;lonDMS"
```

Example:
```
"Luis Alberto Spinetta;1/23/1950 4:35:00 PM;Buenos Aires;Argentina;H;;3;34S35;58W22"
```

To URL-encode it for a POST body in curl use `--data-urlencode`:
```bash
--data-urlencode "nombre=Luis Alberto Spinetta;1/23/1950 4:35:00 PM;Buenos Aires;Argentina;H;;3;34S35;58W22"
```

---

## Natal Chart Image

Fetch the natal chart as a **PNG image** (free, no auth):

```bash
curl -s "https://grupovenus.com/dibujo.aspx" \
  --get \
  --data-urlencode "fec=1/23/1950 4:35:00 PM" \
  --data-urlencode "aju=3" \
  --data-urlencode "ciu=Buenos Aires" \
  --data "pais=Argentina" \
  --data-urlencode "lat=-34.5833" \
  --data-urlencode "lon=58.3667" \
  --data-urlencode "nom=Luis Alberto Spinetta" \
  --data "bot=atras&idioma=E&CASASPRO=&zodi=T" \
  -H "User-Agent: Mozilla/5.0" \
  -o chart_spinetta.png
```

| Parameter | Description |
|-----------|-------------|
| `fec` | Birthdate: `M/D/YYYY H:MM:SS AM/PM` |
| `aju` | Timezone offset (from person record) |
| `ciu` | City name |
| `pais` | Country |
| `lat` | Latitude decimal (negative = South) |
| `lon` | Longitude decimal (positive = West, as stored) |
| `nom` | Person name |
| `idioma` | `E`=Spanish, `I`=English, `F`=French |
| `zodi` | `T`=Tropical, `S1`=Fagan-Bradley, `S2`=Lahiri, `S3`=Sassanian, `S4`=Krishnamurti, `S5`=Hipparchos |

Returns `Content-Type: image/png`. Save to file or display directly.

---

## Transit Forecast Graph

**POST to `informes3.asp`** to get a 1-year forecast with all slow-planet transits:

```bash
curl -s -X POST "https://grupovenus.com/informes3.asp" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "User-Agent: Mozilla/5.0" \
  --data-urlencode "nombre=Luis Alberto Spinetta;1/23/1950 4:35:00 PM;Buenos Aires;Argentina;H;;3;34S35;58W22" \
  --data "urldestino=informes3.asp" \
  --data "INFORMEDESEADO=8" \
  --data "DIA1=28&MES1=2&ANO1=2026" \
  --data "HORA1=09&MINU1=00" \
  --data "tipzod=T&TIC=&idiomas=E"
```

The HTML response encodes all transit data as `title` attributes on `<img class="barras">` elements:

```html
<img class="barras" src="./fotos/barraSAT.jpg"
     title="SATsexMER 4/3/2026 0:0 orbe: 0° 43'"
     width=5 height=13>
```

### Parsing transit data

Extract all data points with:
```bash
grep 'class="barras"' response.html \
  | grep -o 'title="[^"]*"' \
  | sed 's/title="//;s/"//'
```

Each title line has the format:
```
[r ]CODE DD/MM/YYYY H:MM orbe: D° MM'
```

- `r` prefix = retrograde transit
- `CODE` = transit code (see table below)
- date = exact date of this data point (every 2 days)
- `orbe` = orb in degrees/minutes (0°0′ = exact)
- `height` attribute = bar height (1–55), proxy for intensity: `intensity = height / 55`

The first `<a href="sacainter.asp?...cla=CODE...">` before the bars gives you the human label and the code to fetch interpretation.

### Report types — forecast period and planets

| INFORMEDESEADO | Server label | Transiting planets | Period | Access |
|---------------|-------|--------------------|--------|--------|
| `8`  | `1 año Sat-Plu` (1 year, Saturn–Pluto)   | SAT, URA, NEP, PLU | 1 year | **Free** |
| `-1` | `3 días Lun-Júp` (3 days, Moon–Jupiter)  | LUN, SOL, JUP      | 3 days | **Free** |
| `0`  | `1 semana Luna,Sol-Júp` (1 week, Moon/Sun–Jupiter) | LUN, SOL, JUP | 1 week | **Free** |
| `1`  | `2 semanas Sol-Plu` (2 weeks, Sun–Pluto) | SOL, MAR, JUP, SAT, URA, NEP, PLU | 2 weeks | **Free** |
| `7`  | `2 años Sat-Plu` (2 years, Saturn–Pluto) | SAT, URA, NEP, PLU | 2 years | Ticket |
| `6`  | `1 año Jup-Plu` (1 year, Jupiter–Pluto)  | JUP...PLU          | 1 year  | Ticket |
| `4`  | `3 meses Mar-Plu` (3 months, Mars–Pluto) | MAR...PLU          | 3 months | Ticket |

**The free INFORMEDESEADO=8 is the richest free dataset.** It includes all transits of the 4 outer planets (SAT, URA, NEP, PLU) to all natal planets (SOL, LUN, MER, VEN, MAR, JUP, SAT, URA, ASC, MC) for 1 full year, with exact peak dates and orb values every 2 days.

---

## Full Report List

### Natal Reports
| ID | Name | Access |
|----|------|--------|
| `50`  | Mi pronóstico para Hoy | Free |
| `62`  | Carta Natal | Ticket |
| `66`  | Informe Vocacional | Ticket |
| `63`  | Informe Infantil | Ticket |
| `61`  | Carta SuperNatal | Ticket |
| `65`  | Astrología Espiritual | Ticket |
| `64`  | Astrología Kármica | Ticket |
| `69`  | Informe Indra | Free (partial) |
| `170` | Carta Natal con Quirón | Free (partial) |
| `171` | Informe Infantil coloquial | Free (partial) |
| `174` | Vocacional simple | Free |
| `67`  | Astrología y Tarot | Free (partial) |
| `945` | Numerología Básica | Free |
| `947` | Numerología Avanzada | Free |

### Compatibility (two people required)
| ID | Name | Access |
|----|------|--------|
| `16`  | De Pareja | Free (partial) |
| `17`  | De Amistad | Free (partial) |
| `172` | De Pareja coloquial | Free (partial) |
| `90`  | Carta Compuesta | Free (partial) |

### Chart Drawings
| ID | Name | Access |
|----|------|--------|
| `941` | Dibujo de su Carta Astral | Free → redirects to `dibujo0.aspx` |
| `942` | Dibujo Carta para hoy | Free |
| `943` | Superponer dos Cartas | Free |
| `944` | Carta Compuesta (drawing) | Free |

### Forecast Graphs
| ID | Name | Access |
|----|------|--------|
| `8`   | 1 año Sat-Plu | **Free (full data)** |
| `-1`  | 3 días Lun-Júp | Free |
| `0`   | 1 semana Luna,Sol-Júp | Free |
| `1`   | 2 semanas Sol-Plu | Free |
| `199` | Gráfico pronóstico de pareja | Free |
| `7`   | 2 años Sat-Plu | Ticket |
| `6`   | 1 año Jup-Plu | Ticket |
| `4`   | 3 meses Mar-Plu | Ticket |

### Symbolic Predictions
| ID | Name | Access |
|----|------|--------|
| `13`  | Revolución Solar | Free (partial) |
| `15`  | Revolución Lunar | Free (partial) |
| `14`  | Progresiones | Free (partial) |
| `68`  | Ciudades y Pueblos | Free (partial) |
| `173` | Revolución Solar Coloquial | Free (partial) |

### Forecasts — Relationship
| ID | Name | Access |
|----|------|--------|
| `23`  | 12 meses, Marte a Plutón | Free (partial) |
| `199` | Varios períodos (graph) | Free |
| `22`  | 2 meses, Sol a Plutón | Ticket |

### Forecasts — General
| ID | Name | Access |
|----|------|--------|
| `99`  | 1 semana, Luna a Plutón | Ticket |
| `100` | 2 meses, Sol a Plutón | Ticket |
| `101` | 7 meses, Marte a Plutón | Ticket |
| `102` | 18 meses, Júpiter a Plutón | Ticket |

### Forecasts — Kármico-Espiritual
| ID | Name | Access |
|----|------|--------|
| `103` | 4 meses, Sol a Plutón | Ticket |
| `104` | 7 meses, Marte a Plutón | Ticket |
| `105` | 1 año, Júpiter a Plutón | Ticket |

### Forecasts — Sentimental
| ID | Name | Access |
|----|------|--------|
| `106` | 4 meses, Sol a Plutón | Ticket |
| `107` | 1 año, Marte a Plutón | Ticket |

### Forecasts — Coloquial
| ID | Name | Access |
|----|------|--------|
| `108` | 2 meses | Ticket |
| `109` | 7 meses | Ticket |
| `110` | 18 meses | Ticket |

### Solo quincuncios / Negocios
| ID | Name | Access |
|----|------|--------|
| `126` | 1 año, Marte a Plutón | Free (partial) |
| `121` | 9 meses, Sol Marte a Plutón | Free (partial) |

---

## Transit Interpretation Texts

For any transit code, fetch 3 different interpretation styles — **no auth required**:

```bash
# General / technical
curl -s "https://grupovenus.com/sacainter.asp?tabla=tratsp&cla=SATCUAASC&orb=0" \
  -H "User-Agent: Mozilla/5.0"

# Potentials / spiritual
curl -s "https://grupovenus.com/sacainter.asp?tabla=starsolues&cla=SATCUAASC&orb=99" \
  -H "User-Agent: Mozilla/5.0"

# Colloquial / plain language
curl -s "https://grupovenus.com/sacainter.asp?tabla=transiaw&cla=SATCUAASC&orb=99" \
  -H "User-Agent: Mozilla/5.0"
```

The response is HTML. Strip tags and skip the first ~40 lines (boilerplate JS) to get the text:
```bash
curl -s "https://grupovenus.com/sacainter.asp?tabla=tratsp&cla=CODE&orb=0" \
  -H "User-Agent: Mozilla/5.0" \
  | iconv -f iso-8859-1 -t utf-8 \
  | sed 's/<[^>]*>//g' \
  | grep -v '^[[:space:]]*$' \
  | tail -n +40
```

### Transit code reference

Format: `[PLANET1][ASPECT][PLANET2]`
PLANET1 = transiting planet, PLANET2 = natal planet.

**Planet codes:**
| Code | Server name | English | Symbol |
|------|--------|---------|--------|
| `SAT` | Saturno | Saturn | ♄ |
| `URA` | Urano | Uranus | ♅ |
| `NEP` | Neptuno | Neptune | ♆ |
| `PLU` | Plutón | Pluto | ♇ |
| `JUP` | Júpiter | Jupiter | ♃ |
| `MAR` | Marte | Mars | ♂ |
| `VEN` | Venus | Venus | ♀ |
| `MER` | Mercurio | Mercury | ☿ |
| `SOL` | Sol | Sun | ☉ |
| `LUN` | Luna | Moon | ☽ |
| `ASC` | Ascendente | Ascendant | ↑ |
| `MC`  | Medio Cielo | Midheaven | ⬆ |

**Zodiac signs:**
| Server name | English | Symbol |
|------|--------|--------|
| Aries | Aries | ♈ |
| Tauro | Taurus | ♉ |
| Géminis | Gemini | ♊ |
| Cáncer | Cancer | ♋ |
| Leo | Leo | ♌ |
| Virgo | Virgo | ♍ |
| Libra | Libra | ♎ |
| Escorpio | Scorpio | ♏ |
| Sagitario | Sagittarius | ♐ |
| Capricornio | Capricorn | ♑ |
| Acuario | Aquarius | ♒ |
| Piscis | Pisces | ♓ |

**Aspect codes:**
| Code | Server name | English | Degrees | Symbol |
|------|--------|---------|---------|--------|
| `CJC` | Conjunción | Conjunction | 0° | ☌ |
| `SEX` | Sextil | Sextile | 60° | ⚹ |
| `CUA` | Cuadratura | Square | 90° | □ |
| `TRI` | Trígono | Trine | 120° | △ |
| `OPO` | Oposición | Opposition | 180° | ☍ |
| `QUI` | Quincuncio | Quincunx | 150° | ⚻ |

Use these symbols when presenting transit readings to the user. Example: `SATCUAASC` → ♄ □ ↑ (Saturn square Ascendant).

Examples: `SATCUAASC` = ♄ □ Ascendant, `NEPTRIVEN` = ♆ △ ♀, `URACJCMER` = ♅ ☌ ☿.

---

## Compatibility Reports (Two People)

For synastry, the `nombre` field must encode both people separated by `|`:

```
"Person1 data | Person2 data"
```

Full example (Pareja, INFORMEDESEADO=16):
```bash
P1="Luis Alberto Spinetta;1/23/1950 4:35:00 PM;Buenos Aires;Argentina;H;;3;34S35;58W22"
P2="Charly Garcia;10/23/1951 11:20:00 AM;Buenos Aires;Argentina;H;;3;34S36;58W27"

curl -s -X POST "https://grupovenus.com/informes3.asp" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "User-Agent: Mozilla/5.0" \
  --data-urlencode "nombre=$P1 | $P2" \
  --data "urldestino=informes3.asp&INFORMEDESEADO=16&tipzod=T&TIC=&idiomas=E"
```

Compatibility report IDs: `16` (`pareja`, couple), `17` (`amistad`, friendship), `172` (`pareja coloquial`, couple casual), `90` (`carta compuesta`, composite chart).

---

## Zodiac Types

| `tipzod` | System |
|----------|--------|
| `T`  | Tropical (default, most common) |
| `S1` | Sideral — Fagan Bradley |
| `S2` | Sideral — Lahiri |
| `S3` | Sideral — Sassanian |
| `S4` | Sideral — Krishnamurti |
| `S5` | Sideral — Hipparchos |

---

## Standard POST Fields for `informes3.asp`

| Field | Description |
|-------|-------------|
| `urldestino` | Always `informes3.asp` |
| `INFORMEDESEADO` | Report ID (see tables above) |
| `nombre` | Person string (semicolon-delimited) |
| `DIA1` | Start day for forecast |
| `MES1` | Start month |
| `ANO1` | Start year |
| `HORA1` | Start hour (local time) |
| `MINU1` | Start minute |
| `tipzod` | Zodiac type |
| `TIC` | Ticket number (leave empty for free reports) |
| `idiomas` | `E`=Spanish (`Español`), `I`=English, `F`=French (`Français`) |

---

## Analysis Patterns

### Surface the most intense transits

From a parsed INFORMEDESEADO=8 response, rank transits by bar height (intensity proxy):

1. Parse all `title="CODE DATE orbe: D° MM'"` lines
2. Keep the bar `height` attribute for each point
3. Group by transit code — take `max(height)` as peak intensity
4. Sort descending — top 5 are the dominant themes for the year

The orb is the complement of intensity: `0°0′` = exact = maximum impact, `1°0′` = fading. The `height` already encodes this visually (max 55px = exact aspect).

### Identify timing windows

For each transit code, find the contiguous date range where `height > 0`. That range is the active window. Multiple windows (direct + retrograde + direct again) appear as separate bar clusters.

Present to the user as:
> "Saturn square your Ascendant is active **March 8 – April 14**, peaks exactly **March 22**, then returns retrograde **August 15 – November 3**."

### Interpret a transit

For each dominant transit, fetch all 3 interpretation styles and synthesize:
- `tratsp` = technical/classical reading
- `starsolues` = potential/higher-expression reading
- `transiaw` = everyday colloquial reading

Lead with `transiaw` for casual conversations, `tratsp` for someone who wants depth.

### Compare two charts

1. Fetch INFORMEDESEADO=8 for Person A → parse transit codes + windows
2. Fetch INFORMEDESEADO=8 for Person B → parse transit codes + windows
3. Find overlapping active windows — periods where both people are under major transits simultaneously
4. Fetch INFORMEDESEADO=16 or 17 with both persons for the synastry report
5. Highlight: shared themes (both under Pluto? both under Neptune?), conflicting energies, supportive overlaps

### Today's sky

Use INFORMEDESEADO=`-1` (`3 días`, 3 days) or `0` (`1 semana`, 1 week) for short-range forecasts. These include faster planets (Moon, Sun, Jupiter). Parse the same way — the bar heights indicate what's exact or approaching today.

---

## Voice & Style

### General tone

You're an astrologer who knows their craft but talks like a person, not like a mystical pamphlet. Avoid:
- "the stars are telling you..." → too mystical and cliché
- listing positions in degrees with no context → too raw
- "this is a powerful time for growth" → vague and useless

Instead: be direct, be specific, use the symbols, name the tension or the gift without overselling it.

### Per-person styles

Each person in memory has a `style` field. Always read it before writing a response about them. If it's not set, ask (see Happy Path Step 1).

---

#### `casual`

Like a friend who knows astrology. No jargon, no degrees, no house numbers unless they ask. Lead with feeling and situation, not with planet names.

> "Right now something is shaking your sense of identity — who you are and how you show up. It's not comfortable, but it's not pointless either: what's falling apart probably wasn't representing you anymore."

Use `transiaw` interpretations exclusively. Skip technical terms. Offer depth only if they ask.

---

#### `deep`

Full astrological language: aspects, houses, dignities, orbs, retrograde phases. Use the symbols (♇ ☍ ↑). Mention which interpretation style you're drawing from. Structure the reading clearly.

> "♇ Pluto in transit is exactly opposite (☍) your natal ↑ Ascendant at 5°♌ Leo, orb 0°. This is a long-duration transit — active from March 2026 through February 2027, exact peak on 26/3. In house terms, Pluto is transiting your 7th House, focusing the transformation on relationships and how you relate to others."

Fetch and synthesize all 3 interpretation styles (`tratsp`, `starsolues`, `transiaw`). Mention timing windows explicitly.

---

#### `practical`

Skip the poetry, focus on what to do and when. Windows, peaks, warnings. What's favorable, what to watch out for. Calendar-friendly.

> "**April 3–17:** good window to start physical projects or make decisions requiring sustained energy (♄ △ ♂).
> **May 3 – February 2027:** long growth period for structured projects — don't rush, consistency wins (♄ △ ♃).
> **Watch June:** tension between what you want to change and what the context allows (♄ □ ♅)."

Use only dates, peaks, and a one-line action note per transit. No extended interpretation unless asked.

---

This is the recommended flow for a first-time reading. **Do not dump all available data at once.** Each step should feel like a natural conversation beat.

### Step 1 — Register and show the chart

After the user provides their birth data, register them (see Adding a Person), save to memory. Before generating any reading, **ask for their preferred style** if it's not already set:

> "How would you like me to read your chart?
> - **Casual** — like a friend who knows astrology, no technical jargon
> - **Deep** — full aspects, houses, and timing
> - **Practical** — straight to the point: what to do and when"

Save the chosen style to their record in memory, then immediately:

1. Fetch and display the natal chart PNG (`dibujo.aspx`)
2. Write a **brief profile** — 3–4 sentences max, in plain language. Focus on:
   - Sun sign: core identity and drive
   - Ascendant: how they show up in the world
   - Moon sign: emotional nature
   - Any tight conjunctions or stelliums that stand out (e.g. Mars + Jupiter in the same sign)

   > Example: "You're ♊ Gemini with ♌ Leo rising — quick mind, strong presence. Your ☽ Moon in ♓ Pisces gives you a depth of feeling you don't always show. ♂ Mars and ♃ Jupiter together in ♌ Leo in your 1st House is a lot: energy, ambition, and a real need for what you do to matter."

3. Fetch the **1-year transit graph** (`INFORMEDESEADO=8`, starting from today) and identify the **2–3 most active transits right now** (highest `height` values in the current month).

4. Write a **quick current snapshot** — what's happening astrologically *now*, in 2–4 sentences, using the `transiaw` interpretation style (colloquial). Fetch `sacainter.asp?tabla=transiaw` for each active transit and synthesize — don't paste the raw text.

   > Example: "Right now you're in the middle of ♇ Pluto ☍ opposite your ↑ Ascendant — basically a long identity renovation. Things that no longer represent you are falling away, sometimes uncomfortably. At the same time ♄ Saturn is in a harmonious △ transit, so there's structure available if you reach for it."

### Step 2 — Offer next steps (short menu, not overwhelming)

After the snapshot, offer **at most 3–4 options** clearly:

> What would you like to explore?
> - **Year forecast** — the most important transits month by month
> - **A specific transit** — if something I mentioned resonated, I can go deeper
> - **Compatibility** — if you have someone in mind, we can compare charts
> - **Solar return** — what this birthday year brings in particular

Don't mention ticket-gated reports unless the user asks for something that requires one.

> **Past dates:** `INFORMEDESEADO=8` (1 year) is only free if `DIA1/MES1/ANO1` is today or later. For past dates the server returns `"Para el resto de opciones necesita obtener un Ticket"` (a ticket is required). Do not offer full-year retrospective readings on the free tier.

### Step 3 — Go deep on demand

Only when the user asks to explore something specific:
- Fetch all 3 interpretation styles (`tratsp`, `starsolues`, `transiaw`) for that transit
- Synthesize them into a coherent 1–3 paragraph reading
- Mention timing: when is it exact, when does it fade, does it return retrograde

---

## Conversational Suggestions

1. **Multiple people stored** — offer comparisons: "I also have [name] saved. Want me to compare your charts?"

2. **Zodiac type** — default to Tropical. Mention Sidereal (Lahiri) only if the user asks.

3. **Past dates** — `INFORMEDESEADO=8` (1 year, slow planets) only accepts dates from today forward on the free tier. Short-range reports (`-1`, `0`, `1`) may work with past dates.

4. **Language** — `idiomas=E` (Spanish), `I` (English), `F` (French). Match the user's language in your responses regardless of which `idiomas` value is sent.

---

## Example Workflow

### Add a person and fetch their year forecast

```bash
# 1. Look up city
curl -s "https://grupovenus.com/buscaciudjson.asp?q=Rosario&pais=Argentina"

# 2. Register person with cookie jar (3-step flow required)
COOKIEJAR=$(mktemp)

curl -s -c "$COOKIEJAR" -b "$COOKIEJAR" "https://grupovenus.com/info.asp" \
  -H "User-Agent: Mozilla/5.0" > /dev/null

curl -s -c "$COOKIEJAR" -b "$COOKIEJAR" "https://grupovenus.com/personas.asp?nue" \
  -H "User-Agent: Mozilla/5.0" \
  -H "Referer: https://grupovenus.com/info.asp" > /dev/null

curl -s -c "$COOKIEJAR" -b "$COOKIEJAR" -X POST "https://grupovenus.com/ciuda.asp" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "User-Agent: Mozilla/5.0" \
  -H "Referer: https://grupovenus.com/personas.asp?nue" \
  --data "urldestino=personas.asp%3Fok&nombre=Maria&DIA=15&MES=3&ANO=1992&HORA=14&MINU=30&08CIUDAD=Rosario&14PAIS=Argentina&SEXO=V" > /dev/null

# 3. Get d0 cookie with coordinates from the redirect target
D0=$(curl -si -c "$COOKIEJAR" -b "$COOKIEJAR" "https://grupovenus.com/personas.asp?ok" \
  -H "User-Agent: Mozilla/5.0" \
  -H "Referer: https://grupovenus.com/ciuda.asp" \
  | grep -i 'set-cookie.*d0=' \
  | sed 's/.*d0=//I' | cut -d';' -f1 \
  | python3 -c "import sys,urllib.parse; print(urllib.parse.unquote(sys.stdin.read().strip()))")
echo "d0 decoded: $D0"
# → Maria  ;3/15/1992 2:30:00 PM;Rosario;Argentina;V;;3;32S57;60W40

# 4. Fetch 1-year transit graph (no session needed for reports)
curl -s -X POST "https://grupovenus.com/informes3.asp" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "User-Agent: Mozilla/5.0" \
  --data-urlencode "nombre=Maria;3/15/1992 2:30:00 PM;Rosario;Argentina;V;;3;32S57;60W40" \
  --data "urldestino=informes3.asp&INFORMEDESEADO=8&DIA1=1&MES1=1&ANO1=2026&HORA1=00&MINU1=00&tipzod=T&TIC=&idiomas=E" \
  -o maria_transits.html

# 5. Extract transit data
grep 'class="barras"' maria_transits.html \
  | grep -o 'title="[^"]*"' \
  | iconv -f iso-8859-1 -t utf-8 \
  | sed 's/title="//;s/"//' \
  | sort -t' ' -k2 -n

# 6. Fetch natal chart PNG
curl -s "https://grupovenus.com/dibujo.aspx" \
  --get \
  --data-urlencode "fec=3/15/1992 2:30:00 PM" \
  --data-urlencode "aju=3" \
  --data-urlencode "ciu=Rosario" \
  --data "pais=Argentina" \
  --data-urlencode "lat=-32.9333" \
  --data-urlencode "lon=60.6667" \
  --data-urlencode "nom=Maria" \
  --data "bot=atras&idioma=E&CASASPRO=&zodi=T" \
  -H "User-Agent: Mozilla/5.0" \
  -o maria_chart.png
```

---

## Notes

- The site uses **iso-8859-1** encoding. Always pipe through `iconv -f iso-8859-1 -t utf-8` when reading HTML.
- **POST data to `ciuda.asp` must also use iso-8859-1 percent-encoding**, not UTF-8. For accented characters: `í` = `%ED`, `á` = `%E1`, `é` = `%E9`, `ó` = `%F3`, `ú` = `%FA`, `ñ` = `%F1`. Using UTF-8 encoding (e.g. `%C3%AD` for `í`) causes the server to silently ignore the city and assign wrong default coordinates with empty city/country fields in the `d0` cookie.
- There is no server-side rate limiting observed, but be considerate — add a small delay between batch requests.
- Session cookies (`ASPSESSIONID...`) are only needed during the registration flow. Report requests (`informes3.asp`, `dibujo.aspx`, `sacainter.asp`) do not need any session cookie.
- **Always use a cookie jar** (`-c`/`-b` flags) for the registration flow. Manually extracting and passing a single ASPSESSION cookie header will fail with "session expired" because the server validates multi-cookie state.
- The registration flow is exactly 3 steps before the final `personas.asp?ok` call: `info.asp` → `personas.asp?nue` → POST `ciuda.asp`. Skipping any step causes session expiry.
- The `Referer` header is required on both the `personas.asp?nue` GET and the `ciuda.asp` POST. Without it the server rejects the request.
- The `sacainter.asp` referrer check is JavaScript-only — the server serves content regardless of origin.
- Ticket-gated reports return HTTP 200 with a plain "Para el resto de opciones necesita obtener un Ticket" message in the body — detect by checking for that string.
