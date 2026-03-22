---
name: brouter
description: "Generate GPX bike routes via brouter.de. Use when the user wants a bike route as a GPX file between two places, optionally specifying a routing profile. https://github.com/si-gr/brouter-skill"
---

# brouter

This OpenClaw skill queries the **brouter.de** webservice and generate GPX bike tracks.

## Usage

### Natural language prompts

You can trigger this skill with prompts like:

- "Create a GPX for a bike route from [origin] to [destination] (profile: [profile])."
- "Give me a quiet route from Prenzlauer Berg to Kreuzberg as a GPX."
- "I need a fast bike route from Berlin Hauptbahnhof to Alexanderplatz as a GPX file."

### Parameters to extract

When using this skill, identify:

- **origin**: Free-text description of the starting location.
- **destination**: Free-text description of the end location.
- **profile** : One of the supported brouter profiles below.

Parse all location data to coordinates before using `index.js`. Never use free-text descriptions of locations directly as input for `index.js`. Use coordinates as origin and destination input for `index.js`.

### Heuristics for choosing a profile

- Prefer **`trekking`** when the user does not specify a preference.
- Prefer **`trekking-fast`** when the user asks for a *fast* or *time-efficient* route.
- Prefer **`trekking-safe`** or **`shortbike`** when the user asks for a *quiet*, *safe*, or *kid-friendly* route.
- Prefer **`fastbike`** when the user mentions *road bike*, *speed*, or being an *experienced cyclist*.
- Prefer **`moped`** only if the user explicitly indicates using a moped or similar vehicle.

## Agent implementation: coordinates

When this skill is triggered, the agent should **first derive coordinates** from the user's origin and destination, then use `index.js` to make structured request to brouter.de

### 1. Derive coordinates from user input

1. Extract plain-text locations:
   - `origin` — starting point
   - `destination` — end point
2. If the user already supplies coordinates (e.g. `13.4244,52.5388`), use them directly.
3. Otherwise, geocode the locations into `lon,lat` pairs
4. Ensure the final values are strings in the form:
   - `"<lon>,<lat>"` (longitude first, then latitude)

### 2. Use `index.js`

Once you have `start` and `end` as `lon,lat` strings and a chosen `profile`, use the `index.js` as follows:

```
cd workspace/skills/brouter && node -e "(async () => { const run = require('./index'); const result = await run({ start: '<lon>,<lat>', end: '<lon>,<lat>', profile: '<profile>' }); console.log(result); })().catch(err => console.error(err));"
```

Reply to the user with the response file found in routes/ folder.

See the earlier **"Derive coordinates from user input"** section for
recommended heuristics when turning user prompts into coordinates.

