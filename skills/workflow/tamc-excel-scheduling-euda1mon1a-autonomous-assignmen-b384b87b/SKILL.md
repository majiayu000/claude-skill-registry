---
name: tamc-excel-scheduling
description: "TAMC Family Medicine Residency Excel-based scheduling. Use when working with AY 25-26 block schedule spreadsheets to assign faculty half-days (C, GME, DFM) and resident half-days, validate constraints, process FMIT/HAFP blocks, apply post-call rules, and meet AT coverage. Triggers: Block schedule, faculty scheduling, resident scheduling, half-day assignments, FMIT, clinic coverage, resident supervision, AY 25-26."
audience: coworker
version: "1.5"
last_updated: "2026-01-14"
---

# TAMC Excel Faculty & Resident Scheduling

Automates faculty and resident half-day assignments directly in Excel for Family Medicine residency block schedules.

## Architecture Note

**Excel is the communication layer to code.** The Excel workbook serves as configuration input - the scheduling engine reads from it and has more detailed logic internally. Think of Excel as the "what" and the code as the "how."

## Data Model

**See:** `docs/architecture/HALF_DAY_ASSIGNMENT_MODEL.md`

The scheduling system uses **persisted half-day assignments** with actual dates (not block references). This enables:
- Natural inter-block constraint handling (PCAT/DO carries to next block automatically)
- FMIT spanning blocks without special logic
- Leap year and year boundary handled by date arithmetic

**Source Priority (when multiple sources want same slot):**
1. `preload` - FMIT, call, absences - NEVER overwritten
2. `manual` - Explicit human override
3. `solver` - Computed by CP-SAT
4. `template` - Default from WeeklyPattern

## C vs AT Distinction (CRITICAL)

**This table is the foundation of all scheduling logic.**

| Activity | Definition | Physical Capacity | AT Coverage |
|----------|------------|-------------------|-------------|
| Resident C | Resident seeing patients | Counts (max 6) | Creates demand |
| Faculty C | Faculty seeing OWN patients | Counts (max 6) | None |
| Faculty AT | Faculty supervising residents | Does NOT count | Provides |
| PCAT | Post Call Attending Time | Does NOT count | Provides (= AT) |
| DO | Direct Observation | - | Auto-assigned after call |

**Key Rules:**
- **PROC/VAS:** +1.0 AT demand (dedicated 1:1 supervision)
- **SM:** Closed loop - does NOT use AT resources, Tagawa's SM does NOT provide AT

**Terminology (CRITICAL - do not confuse):**
- **PCAT** = Post Call **Attending** Time (NOT Admin) - can precept, provides AT
- **DO** = Direct Observation (NOT Day Off) - auto-assigned PM after call

**Physical Capacity:** Max 6 people doing clinical work (C) per half-day. AT does NOT count toward this limit because AT faculty are supervising, not generating their own patient load.

## Order of Operations (Canonical)

**Phase 1: PRELOAD (locked before solver)**
1. Absences (LV, HOL, DEP, TDY)
2. FMIT - both faculty and resident
3. FMIT Fri/Sat call - auto-assigned with FMIT
4. C-I (inpatient follow-up clinic): PGY-1 Wed AM, PGY-2 Tue PM, PGY-3 Mon PM
5. Night Float - full pattern including post-call
6. aSM - Wednesday AM for SM faculty (Tagawa)
7. Conferences (HAFP, USAFP, LEC)
8. Protected time (SIM, PI, MM)

**Phase 2: SOLVER (computed)**
1. Assign Sun-Thu call (min-gap decay) → auto-generates PCAT baseline
2. Solve outpatient (residents) - solver applies rotation patterns
3. Calculate supervision demand (resident C creates demand)
4. Assign faculty AT (to meet supervision demand)
5. Assign faculty C (personal clinic, counts toward physical capacity)
6. Fill admin time (GME/DFM/SM)

## Academic Year Calendar Structure

All blocks start Thursday, end Wednesday (except Block 0 and 13).

```
Academic Year: July 1 - June 30

Block 0:  July 1 → First Thursday - 1 day
          Variable length (1-6 days)
          Purpose: Orientation, onboarding, calendar fudge factor

Blocks 1-12: Thursday → Wednesday
          Fixed 28 days each (56 half-day assignments per person)

Block 13: Thursday → June 30
          Variable length (28+ days)
          Purpose: Absorb end-of-year remainder
```

**Example AY25-26:**
- July 1, 2025 = Tuesday
- Block 0 = July 1-2 (2 days)
- Block 1 = July 3-30 (28 days, Thu-Wed)
- Block 13 absorbs remainder to reach June 30, 2026

**Block 0 Logic:**
- New intern (no preceding year rotation): Assign FLX
- Returning resident: Follow logic from preceding year rotation

**Block 13 Logic:**
- Normal assignments (not just administrative)
- Longer than standard 28 days to reach June 30

## Build Order (Recommended Workflow)

1. **FMIT/FMET first** - Lock inpatient faculty assignments
2. **Call assignments** - Distribute call with equity tracking
3. **Everything else** - Clinic, AT, admin time

## Quick Reference

**Priority Order:** FMIT > AT (clinic) > Admin (GME/DFM)

**Key Constraints:**
- Weekly clinic caps vary by faculty (0-4)
- Post-call = PCAT (AM) + DO (PM)
- FMIT weeks = no clinic, OFF Friday after
- All residents/faculty have LEC on Wednesday PM
- Mid-block rotation transitions occur at column 28 (start of week 3)

## References

- `references/excel-structure.md` - Complete workbook layout
- `references/faculty-roster.md` - Faculty caps and admin types
- `references/residents-rotations.md` - Resident rotations and codes
- `references/block10-context.md` - Block 10 specific context

## Block Template2 Structure (VERIFIED)

**This is the working document for scheduling.**

### Row Layout
| Row Range | Content |
|-----------|---------|
| 1 | Block number, Day names (THURS, FRI, SAT...) |
| 2 | Day abbreviations (THU, FRI, SAT...) |
| 3 | Date row with actual dates (2025-03-12, etc.) |
| 4 | Staff Call (faculty name when on call) |
| 5 | Resident Call |
| 6 | Headers: TEMPLATE, ROLE, PROVIDER |
| 9-13 | PGY-3 Residents (R3) |
| 14-19 | PGY-2 Residents (R2) |
| 20-25 | PGY-1 Residents (R1) |
| 31-43 | Faculty (C19/FAC, ADJ/FAC, SPEC/PSY) |
| 49-53 | TY/Float/SM |
| 55-65 | Medical Students (USU, IPAP, MS) |
| 67-68 | CP/BHC (Pharmacist, Behavioral Health) |
| 71-82 | Metrics (Appointments, AT Needed, etc.) |

### Column Layout
| Column | Content |
|--------|---------|
| 1 | First-half rotation (e.g., "FMC", "FMIT 2", "Hilo") |
| 2 | Second-half rotation if different (e.g., "Peds NF") |
| 3 | Template code (R1, R2, R3, C19, ADJ, etc.) |
| 4 | Role (PGY 1, PGY 2, PGY 3, FAC, etc.) |
| 5 | Provider name |
| 6+ | Half-day slots (AM/PM pairs per day) |

### Date-to-Column Mapping (Block 10: Mar 12 - Apr 8, 2026)
Each date uses 2 columns: AM (even col), PM (odd col+1)

| Columns | Date | Day | Week |
|---------|------|-----|------|
| 6-7 | Mar 12 | Thu | 1 |
| 8-9 | Mar 13 | Fri | 1 |
| 10-11 | Mar 14 | Sat | 1 (W) |
| 12-13 | Mar 15 | Sun | 1 (W) |
| 14-15 | Mar 16 | Mon | 2 |
| 16-17 | Mar 17 | Tue | 2 |
| 18-19 | Mar 18 | Wed | 2 (LEC col 19) |
| 20-21 | Mar 19 | Thu | 2 |
| 22-23 | Mar 20 | Fri | 2 |
| 24-25 | Mar 21 | Sat | 2 (W) |
| 26-27 | Mar 22 | Sun | 2 (W) |
| 28-29 | Mar 23 | Mon | 3 ← MID-BLOCK TRANSITION |
| 30-31 | Mar 24 | Tue | 3 |
| 32-33 | Mar 25 | Wed | 3 (LEC col 33) |
| 34-35 | Mar 26 | Thu | 3 |
| 36-37 | Mar 27 | Fri | 3 |
| 38-39 | Mar 28 | Sat | 3 (W) |
| 40-41 | Mar 29 | Sun | 3 (W) |
| 42-43 | Mar 30 | Mon | 4 |
| 44-45 | Mar 31 | Tue | 4 |
| 46-47 | Apr 01 | Wed | 4 (LEC col 47) |
| 48-49 | Apr 02 | Thu | 4 |
| 50-51 | Apr 03 | Fri | 4 |
| 52-53 | Apr 04 | Sat | 4 (W) |
| 54-55 | Apr 05 | Sun | 4 (W) |
| 56-57 | Apr 06 | Mon | 5 |
| 58-59 | Apr 07 | Tue | 5 |
| 60-61 | Apr 08 | Wed | 5 (LEC col 61) |

**Special Columns:**
- Weekend (W): 10-13, 24-27, 38-41, 52-55
- LEC (Wednesday PM): 19, 33, 47, 61
- Mid-block transition: Column 28 (Mar 23)

## Faculty Section (Rows 31-43)

**See "C vs AT Distinction" table above for foundational rules.**

Weekly caps apply to **C only** (personal clinic), NOT to AT (supervision).
If staffing is critical, faculty can do AT all day every day.

| Row | Template | Name | Min C/wk | Max C/wk | Admin | Notes |
|-----|----------|------|----------|----------|-------|-------|
| 31 | C19/FAC | Bevis, Zach | 0 | 0 | GME | APD, 100% admin |
| 32 | C19/FAC | Kinkennon, Sarah | 2 | 4 | GME | |
| 33 | C19/FAC | LaBounty, Alex* | 2 | 4 | GME | |
| 34 | C19/FAC | McGuire, Chris | 1 | 1 | DFM | 90% DFM admin |
| 35 | C19/FAC | Dahl, Brian* | 0 | 0 | GME | OUT Dec-Jun |
| 36 | C19/FAC | McRae, Zachery | 2 | 4 | GME | |
| 37 | C19/FAC | Tagawa, Chelsea | 0 | 0 | SM/AT | Sports Med faculty, can also do AT |
| 38 | C19/FAC | Montgomery, Aaron | 2 | 2 | GME | |
| 39 | C19/FAC | Colgan, Bridget | 0 | 0 | GME | DEP (deployed) |
| 40 | C19/FAC | Chu, Jimmy* | 0 | 0 | GME | FMIT weeks |
| 41 | ADJ/FAC | Napierala, Joseph | 0 | 0 | GME | FMIT/Call only |
| 42 | ADJ/FAC | Van Brunt, T. Blake | 0 | 0 | GME | FMIT/Call only |
| 43 | SPEC/PSY | Lamoureux, Anne | 2 | 2 | GME | |

**If MIN cannot be met:** WARN - flag for PD review (e.g., conference week, faculty leave)

### Faculty Weekly Target Distribution

**Target half-days per week (10 total):**

| Activity | Half-Days | Notes |
|----------|-----------|-------|
| C (Clinic) | 3 | Personal patients, has MIN/MAX caps |
| GME/DFM | 2-3 | Admin time |
| AT | 3-4 | Supervising residents (no cap) |
| PCAT/DO | 1 | If took call that week |

**If no call that week:** Extra AT slot available

**Full-day preference:** Faculty prefer full-day C (AM+PM same day) when possible - increases chances of full-day GME and better work-life balance.

## Resident Section (Rows 9-25)

### PGY-3 (Rows 9-13)
| Row | Name | Block 10 Rotation |
|-----|------|-------------------|
| 9 | Connolly, Laura | Hilo (TDY) |
| 10 | Hernandez, Christian* | NF (Night Float) |
| 11 | Mayell, Cameron* | FMC |
| 12 | Petrie, William* | FMIT 2 |
| 13 | You, Jae* | NEURO → NF |

### PGY-2 (Rows 14-19)
| Row | Name | Block 10 Rotation |
|-----|------|-------------------|
| 14 | Cataquiz, Felipe | FMIT 2 |
| 15 | Cook, Scott | SM (Sports Med) |
| 16 | Gigon, Alaine | POCUS |
| 17 | Headid, Ronald | L&D Night Float |
| 18 | Maher, Nicholas | Surg Exp |
| 19 | Thomas, Devin | Gyn Clinic |

### PGY-1 (Rows 20-25)
| Row | Name | Block 10 Rotation |
|-----|------|-------------------|
| 20 | Sawyer, Tessa | FMC |
| 21 | Wilhelm, Clara | Peds Ward → Peds NF |
| 22 | Travis, Colin | Kapiolani L&D |
| 23 | Byrnes, Katherine | Peds NF → Peds Ward |
| 24 | Sloss, Meleighe | PROC |
| 25 | Monsivais, Joshua | IM |

---

## Resident Rotation Scheduling (DETAILED)

### Rotation Code Mapping

| Rotation Name | Primary Code | Pattern | Notes |
|---------------|--------------|---------|-------|
| **Hilo** | TDY | TDY all day | Off-site, entire block |
| **NF (Night Float)** | NF | OFF (AM) / NF (PM) | Works nights, minimal day |
| **FMC** | C/CV | C (AM) / CV or C (PM) | High clinic load |
| **FMIT / FMIT 2** | FMIT | FMIT all day | Inpatient team |
| **NEURO** | NEURO | NEURO (AM) / C (PM) | Elective + clinic |
| **SM (Sports Med)** | SM | SM (AM) / C (PM) | Sports Med + clinic |
| **POCUS** | US | US (AM) / C (PM) | Ultrasound + clinic |
| **L&D Night Float** | L&D | L&D all day | Labor & Delivery nights |
| **Surg Exp** | SURG | SURG (AM) / C (PM) | Surgery + clinic |
| **Gyn Clinic** | GYN | GYN (AM) / C (PM) | Gynecology + clinic |
| **Peds Ward** | PedW | PedW all day | Pediatrics inpatient |
| **Peds NF** | PedNF | OFF (AM) / PedNF (PM) | Peds night float |
| **Kapiolani L&D** | KAP | KAP all day | Off-site L&D |
| **PROC** | PR | PR (AM) / C (PM) | Procedures + clinic |
| **IM** | IM | IM all day | Internal Medicine ward |

### All Known Resident Schedule Codes

| Code | Full Name | Usage |
|------|-----------|-------|
| C | Clinic | FM Clinic precepting |
| C30 | Clinic 30-min | 30-min appointments |
| C40 | Clinic 40-min | 40-min appointments (intern) |
| C-I | Clinic-FMIT | FMIT resident clinic day |
| C-N | Night Float Clinic | Thursday PM for oncoming NF |
| CC | Continuity Clinic | Panel patients |
| CV | Virtual Clinic | Telehealth |
| V1, V2 | Virtual 1/2 | Virtual clinic blocks |
| PR | Procedures | Procedure clinic |
| VAS, VasC | Vascular | Vascular procedures |
| ADM | Admin | Administrative time |
| FLX | Flex | Flexible/catch-up time |
| FMIT | FM Inpatient Team | Inpatient rotation |
| NF | Night Float | Night shift |
| OFF | Day Off | Post-call or scheduled off |
| TDY | Temporary Duty | Off-site rotation (Hilo, etc.) |
| LV | Leave | Vacation/sick |
| HOL | Holiday | Federal holiday |
| HC | Holiday Call | On-call on holiday |
| W | Weekend | Saturday/Sunday |
| LEC | Lecture | Protected didactics (Wed PM) |
| SIM | Simulation | Sim lab |
| MM | M&M | Morbidity & Mortality conf |
| PI | Process Improvement | QI time |
| EPIC | EPIC Training | EHR training |
| Orient | Orientation | New rotation orientation |
| Coding | Coding | Billing/coding education |
| SM | Sports Medicine | SM rotation |
| aSM | Academic Sports Med | Wednesday AM for sports rotation |
| HLC | Houseless Clinic | Monday PM for R2/R3 |
| CLC | Continuity Learning | Thursday PM, weeks 2 and 4 |
| GYN | Gynecology | GYN clinic |
| NEURO | Neurology | Neuro elective |
| OPTH | Ophthalmology | Ophth elective |
| ENT | ENT | ENT elective |
| URO | Urology | Urology elective |
| PAL | Palliative | Palliative care |
| ENDO | Endocrinology | Endo elective |
| VA | VA Clinic | VA rotation |
| NBN | Newborn Nursery | NBN rotation |
| NICU | NICU | Neonatal ICU |
| KAP | Kapiolani L&D | Off-site L&D (intern) |
| L&D | Labor & Delivery | TAMC L&D |
| LDNF | L&D Night Float | R2 L&D nights |
| IM | Internal Medicine | IM ward |
| PedW | Peds Ward | Pediatrics inpatient |
| PedNF | Peds Night Float | Peds nights |
| PedSP | Peds Subspecialty | Peds specialty |
| SURG | Surgery | Surgery rotation |
| STRAUB | Straub | Straub clinic |

### Hilo TDY Schedule (Off-site Rotation)

**Off-island rotation to Hilo, Big Island.**

**Pre-departure (Week 1):**
- **1st Thursday**: Clinic (C)
- **1st Friday**: Clinic (C)
- **Weekend**: Travel to Hilo

**During Hilo (Weeks 2-4):**
- All slots: TDY

**Return (Week 4/5):**
- **Return Tuesday**: Clinic (C) - 4th Tuesday of block
- Less travel time needed than Okinawa

**Key Points:**
- Need clinic touchpoints before leaving and after returning
- TDY = Temporary Duty (off-site, cannot be scheduled locally)
- Wednesday PM still LEC if in town

### Kapiolani L&D Schedule (Intern - PGY-1)

**Off-site rotation at Kapiolani Medical Center.**

| Day | AM | PM | Notes |
|-----|----|----|-------|
| Mon | KAP | **OFF** | Travel back from Kapiolani |
| Tue | **OFF** | **OFF** | Recovery day |
| Wed | **C** | LEC | Continuity clinic! |
| Thu | KAP | KAP | On-site |
| Fri | KAP | KAP | On-site |
| Sat | KAP | KAP | On-site |
| Sun | KAP | KAP | On-site |

**CRITICAL Pattern Summary:**
```python
def get_kapiolani(day_of_week, is_am, is_last_wed):
    if is_last_wed:
        return "LEC" if is_am else "ADV"
    if day_of_week == 1:  # Monday
        return "KAP" if is_am else "OFF"
    elif day_of_week == 2:  # Tuesday
        return "OFF"  # Both AM and PM
    elif day_of_week == 3:  # Wednesday
        return "C" if is_am else "LEC"
    else:  # Thu-Sun
        return "KAP"
```

**Key Points:**
- Mon PM = OFF (travel back)
- Tue = OFF/OFF (recovery)
- Wed AM = **C** (continuity clinic, NOT KAP!)
- Thu-Sun = KAP/KAP

### L&D Night Float Schedule (R2 - PGY-2)

**TAMC Labor & Delivery night shift rotation.**

| Day | AM | PM | Notes |
|-----|----|----|-------|
| Mon | OFF | LDNF | Sleeping days, working nights |
| Tue | OFF | LDNF | |
| Wed | OFF | LDNF | NO Wed AM clinic! |
| Thu | OFF | LDNF | |
| Fri | **C** | OFF | **FRIDAY morning clinic!** |
| Sat | W | W | Weekend |
| Sun | W | W | Weekend |

**CRITICAL: Friday clinic, NOT Wednesday!**

```python
def get_ldnf(day_of_week, is_am, is_last_wed):
    if is_last_wed:
        return "LEC" if is_am else "ADV"
    if day_of_week == 5:  # Friday
        return "C" if is_am else "OFF"  # FRIDAY clinic!
    elif day_of_week in (6, 7):  # Weekend
        return "W"
    else:  # Mon-Thu
        return "OFF" if is_am else "LDNF"
```

**Key Points:**
- **Friday AM = C** (NOT Wednesday like other rotations!)
- Mon-Thu = OFF/LDNF (sleeping days, working nights)
- R2 rotation (not intern)

### Night Float Timing (CORRECTED)

**Night Float Schedule Structure:**
- **Starts:** Thursday
- **Ends:** Wednesday (following week)
- **Post-call:** Thursday after (inter-block day)

**C-N Code (Night Float Clinic):**
- Thursday PM when oncoming to night float
- Replaces C30 for night float resident
- This preserves 2 weeks of continuity clinic
- Marcy uses C-N as cue to drop C30s from templates

```
Night Float Week Example:
Thu (start): C-N in PM (oncoming clinic)
Fri-Wed: NF (working nights)
Thu (end): OFF (post-call inter-block)
```

### Houseless Clinic (HLC)

**Schedule:**
- **Monday PM** for R2s and R3s only
- Every Monday of every rotation
- One resident (PGY-2 or PGY-3) per slot
- Staff coverage: twice a month/block (intermittent)

### Orientation Blocks (Protected Time)

**Procedures Orientation (McRae):**
- Label: **SIM** (Simulation)
- McRae needs procedures orientation time
- Sometimes booked accidentally - he says "it's fine" but should be protected

**MedsTo Orientation (Montgomery):**
- Beginning of each block (timing varies)
- Protected time for medication reconciliation training

### CLC (Continuity Learning Curriculum)

**Schedule:**
- **Thursday PM**, twice per block
- **2nd Thursday** and **4th Thursday** (NOT back-to-back weeks)
- NOT on 1st Thursday (beginning of block has problems)

```
Block Example:
Week 1 Thu PM: NOT CLC (too early)
Week 2 Thu PM: CLC ← First session
Week 3 Thu PM: NOT CLC (gap week)
Week 4 Thu PM: CLC ← Second session
```

### Mid-Block Rotation Transitions

Some residents switch rotations mid-block (at column 28 / Mar 23):

```python
# Check column 1 and 2 for rotation info
first_half = sheet.cell(row=row, column=1).value   # e.g., "Peds Ward"
second_half = sheet.cell(row=row, column=2).value  # e.g., "Peds NF"

MID_BLOCK_COL = 28  # Start of second half

def get_rotation(col, first_rot, second_rot):
    if second_rot and col >= MID_BLOCK_COL:
        return second_rot
    return first_rot
```

### Intern Continuity Clinic (Wednesday AM) - CRITICAL

**PGY-1 interns have protected Continuity Clinic on Wednesday mornings.**

This is a **HARD CONSTRAINT** - interns must see their panel patients weekly regardless of rotation.

```
Wednesday AM for PGY-1:
- Most rotations → C (Continuity Clinic)
- FMC Block 1-6 → C60 (60-min appointments, new intern)
- FMC Block 7-13 → C40 (40-min appointments, experienced intern)
- ER → C30 (30-min appointments)

Exceptions (no Wed AM clinic):
- Night Float schedules (PedW night, NF) → PedW or OFF
- Off-site (Hilo, Kapiolani) → TDY or KAP
- OB Intern → OB Cl
- Transitional → ADM
```

**Senior residents (PGY-2/3) do NOT have this constraint** - their Wed AM depends on rotation:
- FMC (R3) → ADM
- FMC (R2) → FLX
- Procedures → SIM
- Sports Med → aSM

### Resident Clinic Caps and Flex Requirements

**Clinic Half-Days per Week by PGY Level:**
| Level | Clinic Half-Days/Week | Notes |
|-------|----------------------|-------|
| PGY-1 | 1 (ideally) | Protected for learning |
| PGY-2 | 2-3 | No more than 3 |
| PGY-3 | 3-4 | Most clinic time |

**R2 on Sports Med:** Maximum 3 clinics (not 4)

**Flex Time Requirements:**
| Level | FLX Half-Days/Week |
|-------|-------------------|
| PGY-1 | 2 half-days |
| PGY-2 | 1 half-day |
| PGY-3 (FMC) | At least 1 half-day |

### Rotation Fill Patterns

```python
def fill_rotation(sheet, row, rotation, col):
    """Fill a single half-day slot based on rotation type"""
    is_am = (col % 2 == 0)  # Even columns are AM

    if rotation == 'Hilo':
        return 'TDY'
    elif rotation == 'NF':
        return 'OFF' if is_am else 'NF'
    elif rotation == 'FMC':
        return 'C' if is_am else ('CV' if col % 4 == 1 else 'C')
    elif rotation in ['FMIT', 'FMIT 2']:
        return 'FMIT'
    elif rotation == 'NEURO':
        return 'NEURO' if is_am else 'C'
    elif rotation == 'SM':
        return 'SM' if is_am else 'C'
    elif rotation == 'POCUS':
        return 'US' if is_am else 'C'
    elif rotation == 'L and D night float':
        return 'L&D'
    elif rotation == 'Surg Exp':
        return 'SURG' if is_am else 'C'
    elif rotation == 'Gyn Clinic':
        return 'GYN' if is_am else 'C'
    elif rotation == 'Peds Ward':
        return 'PedW'
    elif rotation == 'Peds NF':
        return 'OFF' if is_am else 'PedNF'
    elif rotation == 'Kapiolani L and D':
        return 'KAP'
    elif rotation == 'PROC':
        return 'PR' if is_am else 'C'
    elif rotation == 'IM':
        return 'IM'
    else:
        return rotation  # Use as-is
```

---

## Workflow

### 1. Load Block Template2 Sheet
```python
from openpyxl import load_workbook
wb = load_workbook('schedule.xlsx')
sheet = wb['Block Template2']
```

### 2. Identify Pre-Blocked Slots
**Never overwrite these codes:**
| Code | Meaning | Action |
|------|---------|--------|
| FMIT | FM Inpatient Team | Skip |
| LV | Leave | Skip |
| W | Weekend | Skip |
| PC | Post-call marker | Keep |
| PCAT | Post-Call Admin | Keep |
| DO | Day Off | Keep |
| LEC | Lecture | Skip |
| SIM | Simulation | Skip |
| HAFP | Hawaii AFP conf | Skip |
| BLS | BLS training | Skip |
| USAFP | USAFP conference | Skip |
| DEP | Deployed | Skip |
| aSM | Sports Med assist | Skip |
| PI | Process Improvement | Skip |
| MM? / MM | M&M conference | Skip |

### 3. Apply Call and Post-Call Rules

#### Call Schedule Structure
- **Row 4**: Staff Call - contains faculty name at the date column when on call
- Call is typically at the AM column (even col) of the call date

#### Call Back-to-Back Prevention (HARD CONSTRAINT)
**Rule:** Don't give faculty call on consecutive days - need gap days between call assignments.

```
BAD:  Faculty on call Mar 15 AND Mar 17 (only 1 day gap)
GOOD: Faculty on call Mar 15 AND Mar 19 (3 day gap)
```

#### Weekend Call Protection
Faculty with "W" (weekend) in their schedule row should NOT be assigned call that day.
- This is a soft preference, not a hard constraint
- Call row (Row 4) is separate from schedule row

#### FMIT Call Rules (CRITICAL)

**FMIT Week Structure:**
- **Starts**: Friday
- **Ends**: Thursday (following week)
- **PC (Post-Call/Day Off)**: Friday after FMIT ends

**During FMIT week, faculty covers:**
- Friday night call (first night of FMIT)
- Saturday night call (second night of FMIT)

**FMIT faculty CANNOT be placed on call:**
- Sunday through Thursday during FMIT (they're on inpatient service)
- The Saturday immediately AFTER their FMIT ends (need recovery)

```
Example: Faculty on FMIT Fri Mar 13 - Thu Mar 19:
  - Mar 13 (Fri)         ← FMIT starts, covers Fri call
  - Mar 14 (Sat)         ← FMIT covers Sat call
  - Mar 15-19 (Sun-Thu)  ← CANNOT be on call (on FMIT service)
  - Mar 20 (Fri)         ← PC (day off after FMIT)
  - Mar 21 (Sat)         ← CANNOT be placed on call (recovery)
```

#### FMIT Weekly Call Pattern Summary
```
FMIT week = Friday through Thursday
FMIT faculty covers:
  - Friday night call (FMIT start)
  - Saturday night call (FMIT weekend)
  - CANNOT be on call Sun-Thu (on service)
  - PC Friday after (day off)
  - CANNOT be on call Sat after (recovery)
```

#### Post-Call Rules (PCAT/DO)
Only applies to **non-FMIT** faculty:
```
If faculty on call Night N AND NOT on FMIT:
  Day N+1 AM = PCAT (Post-Call Admin Time)
  Day N+1 PM = DO (Day Off)
```

**FMIT faculty do NOT get PCAT/DO** - they continue FMIT coverage.

#### Post-FMIT Friday Off (PC)
After completing FMIT week, faculty gets Friday off:
```
FMIT ends Thursday -> Friday = PC (both AM and PM)
This Friday CANNOT have this faculty on call.
```

#### Call Assignment Pools

**AUTO-ASSIGN Pool** (Mon-Thu, Sun):
- KINKENNON
- MCGUIRE
- MCRAE
- MONTGOMERY
- TAGAWA (when not on FMIT/PC)

**MANUAL-ONLY Pool** (assigned by hand, typically Sundays):
- NAPIERALA
- VAN BRUNT
- LAMOUREUX

**SPECIAL RULES Faculty:**

| Faculty | Rule |
|---------|------|
| CHU | Week-on/week-off FMIT: No Sun-Thu call during "off" weeks; available after FMIT but not immediately |
| BEVIS | Available for call starting next week after post-FMIT (not same week) |
| LABOUNTY | Only weeks 1-2 before FMIT week; no call in week immediately preceding FMIT |

#### Sunday Call Equity Pool

Sundays are AUTO-ASSIGNABLE but tracked separately for equity. No single faculty member should be assigned every Sunday in a block.

```
Sunday equity tracking:
- Maintain separate sunday_counts vs weekday_counts
- When assigning Sunday, sort by sunday_counts (lowest first)
- Distribute evenly: aim for max 1 Sunday per faculty per block
- W (weekend) in faculty row does NOT block call assignment
```

**Important:** The "W" code in a faculty's schedule row indicates weekend/off, but call assignments (row 4) are separate. Faculty can be ON CALL on a day they have "W" in their schedule.

#### Tagawa Sports Medicine Rules

Tagawa is the Sports Medicine (SM) faculty. She does NOT do regular clinic (C).

**CRITICAL: Tagawa does SM REGARDLESS of whether residents are on SM rotation.**
- SM is Tagawa's primary clinical work (not C like other faculty)
- 2-4 SM half-days/week independent of residents
- When residents ARE on SM, they must match Tagawa's SM slots

**Key Rules:**
1. **SM requires Tagawa**: If a resident is scheduled SM, Tagawa must ALSO be SM that slot
2. **No Tagawa = No SM**: If Tagawa is blocked (FMIT, PC, LV, etc.), resident cannot do SM - change to C
3. **Weekly target**: Tagawa needs 2-4 SM slots per week (independent of residents)
4. **aSM is different**: Academic Sports Med (aSM) = ultrasound teaching, not patient care; Wed AM preload
5. **FMIT blocks SM**: When Tagawa on FMIT, there can be NO SM that week
6. **Call eligible**: Tagawa takes call with normal PCAT/DO rules
7. **SM is closed loop**: Does NOT use AT resources, Tagawa's SM does NOT provide AT for other residents

**Tagawa Schedule Codes:**
- SM = Sports Medicine (with resident)
- aSM = Academic Sports Med (teaching)
- GME = Admin time (when not SM)
- FMIT = Inpatient team (blocks SM)
- PC = Post-FMIT Friday off

**Workflow:**
1. Check if resident on SM rotation (column 1)
2. Find slots where both resident has SM AND Tagawa available
3. Assign Tagawa SM to match (3-4 per week)
4. Change resident SM → C where Tagawa unavailable

#### AT Supervision Ratios (ACGME REQUIREMENT - CANNOT VIOLATE)

**This is a HARD CONSTRAINT - minimum supervision ratios required by ACGME.**

**Resident AT Demand:**
| PGY Level | AT Demand |
|-----------|-----------|
| PGY-1 (Intern) | 0.5 AT each |
| PGY-2 | 0.25 AT each |
| PGY-3 | 0.25 AT each |

**Non-Clinic Activities = +1 AT each:**
- PROC (Procedures)
- VAS (Vascular)
- SM (Sports Med) - covered by Tagawa, not C faculty
- Any specialty clinic requiring dedicated supervision

**Calculation:**
```
Total AT Needed = (PGY-1 count × 0.5) + (PGY-2 count × 0.25) + (PGY-3 count × 0.25) + (PROC/VAS count × 1.0)

ALWAYS ROUND UP - cannot have half a faculty member
```

**Example:**
```
2 PGY-1 in clinic = 1.0 AT
2 PGY-2 in clinic = 0.5 AT
1 PROC resident  = 1.0 AT
--------------------------
Total            = 2.5 AT → Round up to 3 AT minimum
```

**Coverage codes that count as AT:**
- C (Clinic)
- PCAT (Post-Call Admin Time) - CAN precept, counts as AT
- CV (Virtual Clinic) - if precepting

**Verification:**
Check rows 91-92 in Block Template2:
- Row 91: "Total Attendings Needed" (calculated demand)
- Row 92: "# Attendings Assigned" (current coverage)

**Row 92 must be >= Row 91 for EVERY half-day slot.**

#### Balancing AT: Coverage vs Demand

**AT compliance is a two-way equation:**
```
AT Coverage >= AT Demand
```

**If coverage is short, you can EITHER:**
1. **Increase coverage** - Add faculty C (if available within caps)
2. **Decrease demand** - Reduce resident clinic load

**Reducing demand options:**
- Move resident from C → ADM/FLX (removes their AT weight)
- Move resident from PROC → C (PROC = +1.0 AT, C = only 0.25-0.5 AT)
- Reduce clinic load on days with limited faculty

**Priority: AT compliance > weekly clinic caps > GME preferences**

Faculty caps are preferences, not hard constraints. ACGME supervision IS a hard constraint. However, before going over caps, first check if reducing resident demand is feasible.

**Example - Mar 13 PM with most faculty at USAFP:**
- Only 1 faculty available (LaBounty)
- 7 residents in clinic = ~2.0 AT demand
- Solution: Move 2-3 residents from C → ADM for that slot
- Result: Reduced demand to match available coverage

#### Rotation Templates as Guidelines

Rotation templates (column 1-2) are GUIDELINES, not strict requirements. The actual schedule may vary based on:
- Faculty availability (e.g., no SM when Tagawa unavailable)
- AT demand needs
- Call/post-call blocking
- Conference/educational requirements

#### Reading FMIT Schedule
Check "FMIT Attending (2025-2026)" sheet for weekly assignments:
- Column C: Week 1 attending
- Column D: Week 2 attending
- Column E: Week 3 attending
- Column F: Week 4 attending

Example Block 10:
| Week | Dates | FMIT Attending |
|------|-------|----------------|
| 1 | Mar 13-19 | Chu |
| 2 | Mar 20-26 | Bevis |
| 3 | Mar 27-Apr 2 | Chu |
| 4 | Apr 3-9 | LaBounty |

### 4. Assign Faculty Clinic (C)
For each weekday half-day:
1. Get available faculty (not blocked, under weekly cap)
2. Sort by remaining weekly capacity (highest first)
3. Assign top 2 faculty
4. Mark cells with "C"

### 5. Fill Faculty Admin Time
For remaining empty faculty cells:
- Most faculty → "GME"
- McGuire → "DFM"

### 6. Fill Resident Schedules
For each resident:
1. Read rotation from column 1 (and column 2 if mid-block switch)
2. For each column 6-61:
   - Skip if blocked (W, LV, LEC, etc.)
   - Apply rotation pattern based on AM/PM
   - Handle mid-block transitions at column 28
3. Ensure LEC on all Wednesday PM slots (cols 19, 33, 47, 61)

### 7. Last Wednesday of Block Rules (CRITICAL)

**Final Wednesday of block (Week 5) has special rules:**

**All Residents:**
- **AM:** Lecture (LEC) - NOT clinic
- **PM:** Advising (ADV)

⚠️ **Common Error:** Scheduling morning clinic on last Wednesday - this is WRONG.

```
Last Wednesday Example (Apr 8):
  AM: LEC (Lecture) - protected
  PM: ADV (Advising)
```

### 8. Internal Medicine Last Wednesday Exception

**Special Rule for IM rotation:**
- Final Wednesday of IM rotation → **Tuesday PM** clinic instead
- Reason: Preserves continuity week count (otherwise only 3 weeks instead of 4)
- "Inverted day" logic - Thursday starts new week in scheduling
- Can be shorter (2 hours of patient care)

```
IM Resident Last Week Example:
  Tue PM: C (moved from Wed)
  Wed AM: LEC
  Wed PM: ADV
```

---

## Complete Python Code Template

```python
from openpyxl import load_workbook

# Faculty configuration (min_c = MIN clinic/wk, max_c = MAX clinic/wk)
# Weekly caps apply to C only, NOT AT (AT is unlimited)
FACULTY = {
    'Bevis': {'row': 31, 'min_c': 0, 'max_c': 0, 'admin': 'GME'},
    'Kinkennon': {'row': 32, 'min_c': 2, 'max_c': 4, 'admin': 'GME'},
    'LaBounty': {'row': 33, 'min_c': 2, 'max_c': 4, 'admin': 'GME'},
    'McGuire': {'row': 34, 'min_c': 1, 'max_c': 1, 'admin': 'DFM'},
    'Dahl': {'row': 35, 'min_c': 0, 'max_c': 0, 'admin': 'GME'},
    'McRae': {'row': 36, 'min_c': 2, 'max_c': 4, 'admin': 'GME'},
    'Tagawa': {'row': 37, 'min_c': 0, 'max_c': 0, 'admin': 'GME'},  # SM only, no personal C
    'Montgomery': {'row': 38, 'min_c': 2, 'max_c': 2, 'admin': 'GME'},
    'Colgan': {'row': 39, 'min_c': 0, 'max_c': 0, 'admin': 'GME'},
    'Chu': {'row': 40, 'min_c': 0, 'max_c': 0, 'admin': 'GME'},
    'Napierala': {'row': 41, 'min_c': 0, 'max_c': 0, 'admin': 'GME'},
    'Van Brunt': {'row': 42, 'min_c': 0, 'max_c': 0, 'admin': 'GME'},
    'Lamoureux': {'row': 43, 'min_c': 2, 'max_c': 2, 'admin': 'GME'},
}

# Resident configuration
RESIDENTS = {
    9: {'name': 'Connolly', 'pgy': 3},
    10: {'name': 'Hernandez', 'pgy': 3},
    11: {'name': 'Mayell', 'pgy': 3},
    12: {'name': 'Petrie', 'pgy': 3},
    13: {'name': 'You', 'pgy': 3},
    14: {'name': 'Cataquiz', 'pgy': 2},
    15: {'name': 'Cook', 'pgy': 2},
    16: {'name': 'Gigon', 'pgy': 2},
    17: {'name': 'Headid', 'pgy': 2},
    18: {'name': 'Maher', 'pgy': 2},
    19: {'name': 'Thomas', 'pgy': 2},
    20: {'name': 'Sawyer', 'pgy': 1},
    21: {'name': 'Wilhelm', 'pgy': 1},
    22: {'name': 'Travis', 'pgy': 1},
    23: {'name': 'Byrnes', 'pgy': 1},
    24: {'name': 'Sloss', 'pgy': 1},
    25: {'name': 'Monsivais', 'pgy': 1},
}

# Rotation to code mapping (AM, PM)
# NOTE: These are DEFAULT patterns - special days override (Wed AM intern continuity, etc.)
ROTATION_CODES = {
    'Hilo': ('TDY', 'TDY'),           # Off-island, see Hilo TDY Schedule for details
    'NF': ('OFF', 'NF'),              # Night Float - starts Thu, ends Wed
    'FMC': ('C', 'C'),                # Family Medicine Clinic
    'FMIT': ('FMIT', 'FMIT'),         # FM Inpatient Team
    'FMIT 2': ('FMIT', 'FMIT'),       # FM Inpatient Team (2nd team)
    'NEURO': ('NEURO', 'C'),          # Neurology elective + clinic
    'SM': ('SM', 'C'),                # Sports Medicine + clinic
    'POCUS': ('US', 'C'),             # Point-of-care ultrasound + clinic
    'L and D night float': ('OFF', 'LDNF'),  # R2 L&D nights - Fri AM clinic!
    'Surg Exp': ('SURG', 'C'),        # Surgery experience + clinic
    'Gyn Clinic': ('GYN', 'C'),       # Gynecology + clinic
    'Peds Ward': ('PedW', 'PedW'),    # Pediatrics inpatient
    'Peds NF': ('OFF', 'PedNF'),      # Peds Night Float
    'Kapiolani L and D': ('KAP', 'KAP'),  # Off-site L&D - see KAP schedule
    'PROC': ('PR', 'C'),              # Procedures + clinic
    'IM': ('IM', 'IM'),               # Internal Medicine ward
    'VA': ('VA', 'VA'),               # VA clinic rotation
    'ENDO': ('ENDO', 'C'),            # Endocrinology elective
    'Derm': ('DERM', 'C'),            # Dermatology elective
    'MSK': ('MSK', 'C'),              # Musculoskeletal elective
}

# Special columns
WEEKEND_COLS = {10, 11, 12, 13, 24, 25, 26, 27, 38, 39, 40, 41, 52, 53, 54, 55}
LEC_COLS = {19, 33, 47, 61}
MID_BLOCK_COL = 28

# Pre-blocked codes (never overwrite)
BLOCKED_CODES = {'FMIT', 'LV', 'W', 'PC', 'LEC', 'SIM', 'HAFP', 'BLS',
                 'PCAT', 'DO', 'USAFP', 'DEP', 'aSM', 'PI', 'MM?', 'MM',
                 'HOL', 'HC', 'TDY'}

def fill_resident_schedule(sheet, row):
    """Fill a single resident's schedule based on their rotation"""
    rot1 = sheet.cell(row=row, column=1).value
    rot2 = sheet.cell(row=row, column=2).value

    for col in range(6, 62):
        current = sheet.cell(row=row, column=col).value
        if current and str(current).strip().upper() in BLOCKED_CODES:
            continue

        if col in WEEKEND_COLS:
            sheet.cell(row=row, column=col).value = 'W'
            continue

        if col in LEC_COLS:
            sheet.cell(row=row, column=col).value = 'LEC'
            continue

        # Get rotation (handle mid-block switch)
        rotation = rot2 if (rot2 and col >= MID_BLOCK_COL) else rot1

        # Get AM/PM codes
        if rotation in ROTATION_CODES:
            am_code, pm_code = ROTATION_CODES[rotation]
            is_am = (col % 2 == 0)
            sheet.cell(row=row, column=col).value = am_code if is_am else pm_code
        else:
            sheet.cell(row=row, column=col).value = rotation
```

---

## Manual Scheduling Workflow (Reference)

This is the typical workflow when scheduling by hand. The automated system should follow a similar approach:

### Step 1: Load Non-Negotiables
- Absences (LV)
- FMIT assignments
- Conferences (HAFP, USAFP)
- Holidays (HOL)
- Protected time (LEC, SIM)

### Step 2: Assign Sun-Thu Call
- Distribute call equitably across auto-assign pool
- Track weekday and Sunday counts separately
- Sunday = separate equity pool (max 1 per faculty per block)
- **Result: Generates PCAT for every working day AM** (baseline 1 AT)

### Step 3: Load Resident Templates
- Apply rotation patterns from columns 1-2
- These are GUIDELINES, not strict requirements
- Adjust based on availability (e.g., no SM if Tagawa blocked)

### Step 4: Calculate AT Demand
- See AT Supervision Ratios above
- Check rows 91-92 for demand vs coverage

### Step 5: Assign Faculty Clinic (C)
- Prioritize slots with higher resident load
- **Prefer full-day C when possible** (faculty preference)
  - Full-day C increases chances of getting full-day GME
  - Better work-life balance for faculty
- Keep physical clinic ≤6 people

### Step 6: Fill Admin Time
- GME for most faculty
- DFM for McGuire
- Fill remaining empty slots after C assignments

### Physical Clinic Constraint

**See "C vs AT Distinction" table for authoritative rules.**

Max 6 people doing clinical work (C) per half-day slot. AT does NOT count toward this limit.

**Why this matters:** Staffing constraints limit how many patients can be seen. More than 6 physicians overwhelms support staff.

---

## Validation Checklist

After completing assignments:
- [ ] No faculty exceeds weekly C cap (MIN and MAX)
- [ ] Post-call blocks (PCAT/DO) applied correctly
- [ ] FMIT faculty have no C on FMIT days
- [ ] No assignments on weekends (W columns)
- [ ] LEC on all Wednesday PM slots (cols 19, 33, 47, 61)
- [ ] **PGY-1 interns have Continuity Clinic on Wednesday AM (C/C40/C60)**
- [ ] Resident rotations match column 1/2 rotation names
- [ ] Mid-block transitions applied at column 28
- [ ] Pre-blocked codes not overwritten
- [ ] **ACGME: AT coverage >= AT demand (Row 92 >= Row 91) for every slot**
- [ ] **Physical clinic: ≤6 people doing clinical work per slot**
- [ ] Sunday call distributed (max 1 per faculty)
- [ ] **No back-to-back call (need gap days between assignments)**
- [ ] **Night float starts Thursday, ends Wednesday, post-call Thursday**
- [ ] **C-N used for oncoming night float (Thursday PM)**
- [ ] **Last Wednesday: AM=LEC, PM=ADV (no morning clinic)**
- [ ] **IM residents: Tuesday PM clinic instead of final Wednesday**
- [ ] **R2 clinic caps: no more than 3 per week**
- [ ] **HLC assigned Monday PM for R2/R3**
- [ ] **CLC on 2nd and 4th Thursday PM (not back-to-back)**

## Common Issues

**"Not enough coverage"**: Check if faculty are on leave (LV), USAFP, or DEP.

**"Weekly cap exceeded"**: Recalculate weekly totals. Caps are PER WEEK, not total.

**"Post-call conflict"**: If faculty on call Sunday, Monday AM/PM both blocked.

**"Wrong rotation code"**: Check column 1 for rotation name, verify mapping exists.

**"Mid-block not switching"**: Ensure column 2 has second rotation and col >= 28.

---

## ROSETTA Stone Testing Approach

**Ground truth file:** `docs/scheduling/Block10_ROSETTA_CORRECT.xlsx`

This file contains the CORRECT Block 10 schedule with all patterns applied correctly. Use it for TDD:

1. Parse ROSETTA to get expected values
2. Run expansion service to get actual values
3. Compare cell-by-cell
4. Fix until all tests pass

**Test files:**
- `backend/tests/scheduling/test_expansion_vs_rosetta.py` - 24 parameterized tests
- `backend/app/utils/rosetta_parser.py` - Parses ROSETTA xlsx

**Run tests:**
```bash
cd backend
pytest tests/scheduling/test_expansion_vs_rosetta.py -v
```

**Key patterns verified by ROSETTA:**
| Resident | Rotation | Key Pattern |
|----------|----------|-------------|
| Travis, Colin | KAP | Mon PM=OFF, Tue=OFF/OFF, Wed AM=C |
| Headid, Ronald | LDNF | Fri AM=C (not Wed!), Mon-Thu=OFF/LDNF |
| Sloss, Meleighe | PROC | Wed AM=C (intern continuity) |
| Monsivais, Joshua | IM | Wed AM=C, works weekends |
| You, Jae | NEURO→NF | Mid-block transition at col 28 |
| Wilhelm, Clara | PedW→PedNF | Mid-block + intern continuity |
| Byrnes, Katherine | PedNF→PedW | Reverse mid-block |

**Priority rules (highest first):**
1. Last Wednesday → LEC/ADV (cols 60-61)
2. Wednesday PM → LEC (cols 19, 33, 47)
3. Rotation-specific patterns (KAP, LDNF, NF)
4. Intern Wed AM continuity (PGY-1 → C)
5. Mid-block transitions (col 28+)
6. Default rotation pattern

---

## Edge Cases and Resolutions

### Call/Post-Call Boundary Conditions

| Edge Case | Resolution |
|-----------|------------|
| Call before FMIT | Min 3-day buffer; prefer no call week before FMIT |
| PCAT/DO inter-block | Carries over via actual dates (Wednesday call → Thursday PCAT in next block) |
| Call on last day of block | PCAT/DO applies to first day of next block automatically |

### FMIT Week Boundary Conditions

| Edge Case | Resolution |
|-----------|------------|
| FMIT spanning blocks | Date-based, not block-tied; solver handles naturally |
| Post-FMIT PC in next block | Actual dates handle this (e.g., FMIT ends Thu → PC Fri may be in next block) |
| FMIT + Wednesday call prohibition | Cannot take Sun-Thu call during FMIT week |

### SM/Tagawa Dependencies

| Edge Case | Resolution |
|-----------|------------|
| Multiple SM residents same slot | Max 2 residents; Tagawa supervises both; must match half-day |
| Tagawa post-call + SM scheduled | Medium constraint - avoid if possible, not a hard fail |
| Tagawa on FMIT + SM residents | No SM that week; convert resident SM → C |

### FMIT Clinic (C-I) by PGY Level

| PGY Level | C-I Day | Notes |
|-----------|---------|-------|
| PGY-1 | Wednesday AM | Hard constraint - intern continuity preserved |
| PGY-2 | Tuesday PM | FMIT resident clinic day |
| PGY-3 | Monday PM | FMIT resident clinic day |

C-I is **PRELOADED**, not solved. These slots are locked before solver runs.

### Inter-Block Continuity

| Scenario | Handling |
|----------|----------|
| NF post-call inter-block | NF ends Wednesday → post-call Thursday = next block start |
| PCAT/DO from Wed call | Thursday AM/PM may be in next block |
| Rotation ending mid-week | Date arithmetic handles naturally |

### Physical Capacity

| Constraint | Limit |
|------------|-------|
| Clinical work per half-day | Max 6 people (residents + faculty in C/CV/PR/VAS) |
| AT supervision | Does NOT count toward physical limit |

### Holidays and Special Days

| Scenario | Resolution |
|----------|------------|
| CLC on holiday | Skip; does NOT reschedule to another day |
| HLC on holiday | Skip; does NOT reschedule |
| Intern continuity on holiday | Skip; continuity does NOT reschedule |

### Resident Call System (Separate from Faculty)

Resident call is Chief-assigned and follows different rules:
- L&D 24-hour call (Friday)
- Night Float coverage
- Weekend call patterns

**Note:** Resident call is tracked in `resident_call_preloads` table, separate from faculty call.

---

## Related Documents

- `docs/architecture/HALF_DAY_ASSIGNMENT_MODEL.md` - Data model specification
- `.claude/Scratchpad/session-104-half-day-model.md` - Design session notes
- `references/faculty-roster.md` - Faculty caps and constraints
- `references/residents-rotations.md` - Resident rotation patterns
