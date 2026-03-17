---
name: Gameplay Concepts & Mechanics
description: Core gameplay loop focusing on crime investigation, evidence photography, and time loop mechanics. Use when working on investigation features, photo system, or game progression.
---

# Gameplay Concepts & Mechanics

## Game Overview

**Genre**: First-Person Detective / Time Loop Mystery  
**Core Loop**: Witness crime → Photograph evidence → Analyze clues → Repeat day → Solve mystery

**Setting**: Small town/village with recurring day cycle  
**Perspective**: First-person with camera mechanics  
**Time Period**: One repeating day (6 AM - 10 PM)

## Three Pillars of Gameplay

### 1. 🕵️ Crime Investigation
### 2. 📷 Photography Evidence System
### 3. ⏰ Time Loop Mechanics

---

## 1. Crime & Investigation System

### Crime Structure

**Crime Definition** (`public/data/events/*.json`):
```json
{
  "id": "crime_theft",
  "name": "The Bread Theft",
  "type": "crime",
  "triggerTime": "03:00",
  "location": {"x": 10, "y": 0, "z": 15},
  "description": "Someone stole fresh bread from the bakery",
  "suspects": ["thief", "beggar"],
  "evidence": [
    {
      "type": "photo",
      "subject": "thief",
      "location": "bakery",
      "timeWindow": ["02:45", "03:15"]
    }
  ]
}
```

### Investigation Structure

**Investigation Definition** (`public/data/investigations/*.json`):
```json
{
  "id": "bread_thief",
  "title": "Who Stole the Bread?",
  "description": "The baker reports bread missing every morning",
  "objectives": [
    {
      "id": "photograph_suspect",
      "description": "Photograph the suspect near the bakery",
      "type": "photo",
      "required": true
    },
    {
      "id": "find_witness",
      "description": "Find someone who saw the crime",
      "type": "dialogue",
      "npcId": "guard"
    }
  ],
  "solution": {
    "culprit": "thief",
    "motive": "Hunger",
    "evidence": ["photo_thief_bakery"]
  }
}
```

### Crime Types

**Theft**:
- Missing items
- Suspects with opportunity
- Evidence: photos, witness testimony

**Vandalism**:
- Damaged property
- Motive investigation
- Evidence: timing, location

**Mystery/Suspicious Activity**:
- Unusual behavior
- Pattern recognition
- Evidence: multiple observations

### Investigation States
```typescript
enum InvestigationState {
  Locked,      // Not yet discovered
  Active,      // Currently investigating
  Solved,      // Completed successfully
  Failed       // Time ran out or wrong conclusion
}
```

### Evidence Collection

**Evidence Types**:
1. **Photographs**: Visual proof of suspects/scenes
2. **Testimony**: NPC dialogue responses
3. **Physical Clues**: Items found at crime scene
4. **Timing**: When events occurred
5. **Location**: Where suspects were seen

**Evidence Chain**:
```
Observe → Photograph → Analyze → Connect → Conclude
```

### Clue System (Planned)

**Clue Properties**:
```typescript
interface Clue {
  id: string;
  type: "photo" | "dialogue" | "item" | "timing";
  content: string;
  timestamp: string;
  location: Vector3;
  relatedNPC?: string;
  importance: "critical" | "supporting" | "minor";
}
```

---

## 2. Photography Evidence System

### Photo System (`src/systems/photoSystem.ts`)

**Core Concept**: Camera is the primary investigation tool

**Features**:
- Take photos with camera view
- Photos capture: NPCs, locations, timestamps
- Limited film capacity (encourages careful shooting)
- Photos persist across time loops
- Evidence review interface

### Photo Capture

**Trigger**: Press 'C' key or Click photo button

**Photo Data Structure**:
```typescript
interface Photo {
  id: string;
  timestamp: string;           // Game time when taken
  location: {x: number, y: number, z: number};
  cameraAngle: {x: number, y: number};
  visibleNPCs: string[];       // IDs of NPCs in frame
  buildingsInFrame: string[];  // Nearby buildings
  timeOfDay: "dawn" | "morning" | "afternoon" | "evening" | "night";
  thumbnail?: string;          // Screenshot data
}
```

### Photo Analysis

**Evidence Value Calculation**:
```typescript
// Photo is valuable if:
- Taken during relevant time window
- Shows suspect near crime scene
- Captures interaction between NPCs
- Documents timeline of events
```

**Photo Scoring**:
```typescript
interface PhotoScore {
  relevance: number;    // 0-10 (related to active investigation)
  timing: number;       // 0-10 (right time window)
  composition: number;  // 0-10 (subject visibility)
  rarity: number;       // 0-10 (unusual event captured)
}
```

### Camera Mechanics

**View Mode**:
```typescript
- First-person camera switches to "photo mode"
- UI overlay with viewfinder
- Focus indicator on NPCs
- Timestamp display
- Film count remaining
```

**Photo Restrictions**:
- Limited film: 36 photos per loop
- Cannot photograph in darkness (too dark to see)
- Distance limit: Clear photos up to 20 units
- Cannot photo through walls/obstacles

### Photo Storage

**In-Game Album**:
```typescript
- Photos organized by time taken
- Filter by: NPC, location, time
- Compare photos across loops
- Mark important photos
- Add notes to photos
```

**Photo UI** (`src/ui/photoStack.ts`):
```typescript
- Polaroid-style display
- Click to enlarge
- See timestamp and location
- Compare with evidence list
```

### Evidence Photos

**Critical Evidence**:
```
✓ Suspect at crime scene during crime time
✓ Unusual NPC interactions
✓ Items out of place
✓ Contradictions with NPC testimony
```

**Supporting Evidence**:
```
○ NPC schedules/patterns
○ Location relationships
○ Timeline of events
○ Witness presence
```

---

## 3. Time Loop Mechanics

### Loop Concept

**The Core Mechanic**: Day repeats until mystery is solved

**Day Structure**:
```
06:00 - Day Start (player wakes)
08:00 - Town wakes up, NPCs start routines
12:00 - Midday, peak activity
15:00 - Afternoon, schedules continue
18:00 - Evening, some NPCs head home
21:00 - Night, reduced activity
05:59 - Day End (forced loop or manual reset)
```

### Loop States

**First Loop**:
- Player unaware of loop
- Crime occurs without warning
- NPCs behave normally
- Investigation begins

**Subsequent Loops**:
- Player retains knowledge
- Can anticipate events
- NPCs unaware of loop (same dialogue)
- Evidence accumulates

**Final Loop** (Solved):
- Player presents evidence
- Confrontation with culprit
- Resolution cutscene
- Day breaks loop / Game continues

### Loop Trigger Events

**Automatic Reset**:
```typescript
// Day ends at 10 PM
if (currentTime >= 22:00) {
  triggerLoopReset();
}
```

**Manual Reset**:
```typescript
// Player can reset via menu
// Useful if stuck or want to retry
resetToMorning();
```

**Solved Reset**:
```typescript
// After solving, day continues or loop ends
if (investigationSolved) {
  breakLoop(); // or continueWithoutLoop();
}
```

### Persistent Elements

**What Carries Over**:
✅ Photos taken (evidence album)  
✅ Dialogue options unlocked  
✅ Player knowledge (journal entries)  
✅ Investigation progress  
✅ Clue connections made  
✅ NPC relationship levels

**What Resets**:
🔄 NPC positions (back to 6 AM)  
🔄 NPC dialogue state  
🔄 World state (crimes haven't happened)  
🔄 Player position (spawn point)  
🔄 Time (6:00 AM)  
🔄 Dynamic objects (doors, items)

### Loop Counter
```typescript
interface LoopData {
  loopNumber: number;           // How many loops completed
  daysInLoop: number;           // Total days experienced
  investigationsActive: string[];
  investigationsSolved: string[];
  totalPhotos: number;
  criticalEvidenceFound: boolean;
}
```

### Meta-Progression

**Knowledge Growth**:
```
Loop 1: Witness crime, confused
Loop 2: Know when crime occurs, prepare camera
Loop 3: Know suspect patterns, strategic photos
Loop 4: Have full timeline, present evidence
```

**Player Journal**:
```typescript
interface JournalEntry {
  loop: number;
  time: string;
  content: string;
  type: "observation" | "clue" | "theory";
  relatedPhotos: string[];
}
```

---

## Gameplay Flow

### Investigation Cycle

```
1. OBSERVE
   ├─ Watch NPCs following schedules
   ├─ Notice unusual behavior
   └─ Identify suspects

2. DOCUMENT
   ├─ Take photos of evidence
   ├─ Screenshot crime scenes
   └─ Capture NPC interactions

3. ANALYZE
   ├─ Review photos in album
   ├─ Compare with NPC schedules
   └─ Build timeline

4. INTERROGATE
   ├─ Talk to NPCs
   ├─ Present photos as evidence
   └─ Unlock new dialogue

5. CONCLUDE
   ├─ Identify culprit
   ├─ Present evidence
   └─ Solve investigation

6. LOOP (if not solved)
   ├─ Reset day
   ├─ Retain knowledge
   └─ Refine approach
```

### Player Actions

**Movement**:
- WASD: Walk
- Mouse: Look
- Space: Jump (if enabled)
- Shift: Sprint (if enabled)

**Interaction**:
- E: Interact with NPCs/objects
- C: Take photo
- Tab: Open inventory/evidence
- Esc: Menu / Pause

**Investigation**:
- Photo album review
- Journal reading
- Map viewing
- NPC schedule notes

### NPC Dialogue System

**Dialogue States**:
```typescript
interface DialogueNode {
  id: string;
  text: string;
  conditions?: {
    hasPhoto?: string;        // Requires specific photo
    timeRange?: [string, string];
    loopNumber?: number;      // Unlocks after X loops
    investigationState?: string;
  };
  responses: DialogueChoice[];
}
```

**Evidence Presentation**:
```typescript
// Show photo to NPC for reaction
presentEvidence(photo: Photo, npc: NPC) {
  if (photo.visibleNPCs.includes(npc.id)) {
    // NPC recognizes themselves
    return npc.reactions.photograph_self;
  } else if (photo.relatedToNPC(npc)) {
    // Photo shows something NPC knows about
    return npc.reactions.photograph_related;
  }
}
```

---

## Data Files Structure

### Events Directory
```
public/data/events/
  ├── crime_theft.json      - Bread theft crime
  └── [future crimes]
```

### Investigations Directory
```
public/data/investigations/
  ├── bread_thief.json      - Bread theft investigation
  └── [future mysteries]
```

### Packs (Combined Content)
```
public/data/packs/
  └── bakery_scenario.json  - Complete scenario with NPCs, crime, investigation
```

---

## Planned Features

### Investigation Board
- Connect clues visually
- Timeline reconstruction
- Suspect profiles
- Evidence organization

### Advanced Photography
- Photo quality/lighting affects value
- Different lenses/zoom levels
- Photo comparison tool
- Anomaly detection

### Multiple Investigations
- Parallel mysteries
- Interconnected crimes
- Long-term mysteries spanning multiple loops

### NPC Memory
- NPCs remember player actions
- Relationship building affects dialogue
- Trust system for information sharing

---

## Development Commands

### List all events
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
ls -1 public/data/events/*.json
```

### List all investigations
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
ls -1 public/data/investigations/*.json
```

### Validate investigation JSON
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
for f in public/data/investigations/*.json; do
  echo "Checking $f..."
  node -e "JSON.parse(require('fs').readFileSync('$f'))" && echo "✓ Valid"
done
```

### Check photo system
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
grep -n "class PhotoSystem\|interface Photo" src/systems/photoSystem.ts
```

---

## Related Files
```
src/systems/photoSystem.ts              - Photo capture & storage
src/systems/npcSystem.ts                - NPC behavior & schedules
src/systems/hourlyCycle.ts              - Event triggering
src/systems/loopManager.ts              - Game loop management
src/ui/photoStack.ts                    - Photo display UI
public/data/events/                     - Crime definitions
public/data/investigations/             - Investigation definitions
public/data/packs/                      - Complete scenarios
```

---

## Design Philosophy

**Player Agency**:
- No hand-holding, figure it out
- Multiple solution paths
- Mistakes don't end game (loop resets)
- Experimentation encouraged

**Environmental Storytelling**:
- NPCs reveal story through schedules
- World design hints at relationships
- Photos tell stories without words

**Emergent Narrative**:
- Player creates their own investigation story
- Each loop can be different approach
- Personal theories and deductions

**Respect Player Time**:
- Loops are short (15-20 real minutes)
- Fast-forward options
- Clear progress indicators
- Skip known information
