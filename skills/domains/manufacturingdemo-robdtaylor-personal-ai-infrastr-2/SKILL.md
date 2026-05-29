---
name: Manufacturingdemo
description: Demo manufacturing knowledge base for Taylored Systems. Shows how tribal knowledge gets captured and made queryable. USE WHEN demonstrating to potential clients or answering manufacturing process questions.
---

# Manufacturing Operations Knowledge Base

**Company:** Demo Manufacturing Ltd (Example)
**Last Updated:** 2026-01-11
**Knowledge Source:** Captured from shop floor experts

---

## How To Use This Skill

This demonstrates how Taylored Systems captures and structures manufacturing knowledge. Staff can ask natural questions like:

- "How do I set up the CNC for aluminium?"
- "What's the inspection process for incoming materials?"
- "Machine 3 is showing error code E-47, what do I do?"
- "New starter here - what's the morning startup procedure?"

The AI returns YOUR company's actual procedures, not generic internet answers.

---

## 1. CNC Machine Setup Procedures

### 1.1 Aluminium Setup (Haas VF-2)

**Before you start:**
- Check job card for material spec (6061-T6 vs 7075 - DIFFERENT SPEEDS)
- Verify tooling is correct for the job
- Ensure coolant level is above MIN line

**Setup steps:**

1. **Load material**
   - Use soft jaws for finished surfaces
   - Torque to 45 Nm - no more (Dave's tip: "finger tight plus quarter turn")
   - Check runout with dial indicator - must be <0.02mm

2. **Set work offset**
   - Touch off X, Y from datum hole
   - Z from top of stock - LEAVE 0.5mm safety margin
   - Double-check G54 values before running

3. **Speed and feed for 6061-T6**
   | Operation | Speed (RPM) | Feed (mm/min) | DOC (mm) |
   |-----------|-------------|---------------|----------|
   | Roughing | 8000 | 2000 | 3.0 |
   | Finishing | 10000 | 1500 | 0.5 |
   | Drilling | 4000 | 800 | - |

4. **Speed and feed for 7075-T6** (harder - reduce by 20%)
   | Operation | Speed (RPM) | Feed (mm/min) | DOC (mm) |
   |-----------|-------------|---------------|----------|
   | Roughing | 6500 | 1600 | 2.5 |
   | Finishing | 8000 | 1200 | 0.5 |
   | Drilling | 3200 | 650 | - |

5. **First part checks**
   - Run at 50% feed override first cycle
   - Stop after roughing, measure critical dims
   - Only go full speed after first part approved

**Common mistakes:**
- Running 7075 at 6061 speeds → tool breakage
- Forgetting coolant → surface finish issues
- Not checking runout → parts out of tolerance

---

### 1.2 Steel Setup (Haas VF-2)

**Critical difference from aluminium:** Lower speeds, higher rigidity needed

**Setup steps:**

1. **Material check**
   - Mild steel (1018/1020): Standard setup
   - 4140: Pre-heat treated? Check hardness first
   - Stainless (304/316): COMPLETELY different - see section 1.3

2. **Speed and feed for mild steel**
   | Operation | Speed (RPM) | Feed (mm/min) | DOC (mm) |
   |-----------|-------------|---------------|----------|
   | Roughing | 3000 | 800 | 2.0 |
   | Finishing | 4000 | 600 | 0.3 |
   | Drilling | 1500 | 200 | - |

3. **Tooling notes**
   - Use coated carbide (TiAlN) not HSS
   - Check insert condition - steel kills worn inserts fast
   - Minimum stickout on endmills

**Dave's wisdom:** "If it's squealing, you're going too fast. If it's rubbing, you're going too slow. Sweet spot is a nice consistent hiss."

---

## 2. Quality Control Procedures

### 2.1 Incoming Material Inspection

**Every delivery must be checked before going to stock.**

**Step 1: Paperwork check**
- [ ] Mill cert matches PO material spec
- [ ] Heat/batch numbers recorded
- [ ] Quantity matches delivery note

**Step 2: Visual inspection**
- [ ] No visible damage, corrosion, contamination
- [ ] Protective packaging intact
- [ ] Correct size/form (bar, plate, tube)

**Step 3: Dimensional check (sample)**
- Measure 3 pieces per batch (or 10% if <30 pieces)
- Check OD/thickness against spec
- Record on incoming inspection form

**Step 4: Material verification (if critical)**
- PMI test for stainless/alloy steel
- Hardness test if heat treatment specified
- Record results on cert

**Reject if:**
- Material doesn't match cert
- Dimensions outside tolerance
- Visible defects
- Missing paperwork (quarantine until resolved)

**Where to log:** Incoming Inspection Register (blue folder, QC office)

---

### 2.2 In-Process Inspection

**First-off inspection (MANDATORY):**
- 100% dimensional check against drawing
- Sign-off by setter AND operator
- Keep first-off part until batch complete

**Patrol inspection:**
- Every 20 parts OR every hour, whichever is sooner
- Check 3 critical dimensions (marked on drawing)
- Record on SPC chart if applicable

**What to do if out of tolerance:**
1. STOP machine immediately
2. Quarantine suspect parts (red bin)
3. Inform supervisor
4. Check last good part - when did drift start?
5. Measure tool wear
6. Adjust and re-validate with new first-off

---

### 2.3 Final Inspection

**Before parts leave:**

- [ ] All dimensions per drawing (CMM report for complex parts)
- [ ] Surface finish check (comparator or profilometer)
- [ ] Visual inspection - no burrs, scratches, handling marks
- [ ] Quantity count matches job card
- [ ] Parts cleaned and preserved
- [ ] Paperwork complete (job card, inspection report, any NCRs)

**Sign-off required by:** QC Inspector (or supervisor if QC unavailable)

---

## 3. Machine Error Codes

### 3.1 Haas VF-2 Common Errors

| Code | Meaning | What To Do |
|------|---------|------------|
| **E-47** | Spindle overload | Stop program. Check for chip pack, dull tool, or excessive DOC. Reduce load and restart. |
| **E-52** | Servo overload (axis) | Check for crash or obstruction. Power cycle. If persists, call maintenance. |
| **E-91** | Low coolant | Top up coolant tank. Check for leaks. |
| **E-102** | Tool not clamped | Clean taper, check drawbar. Try re-clamping. If persists, check retention knob. |
| **E-200** | Emergency stop | Check all E-stops. Reset and restart. |
| **E-310** | Encoder error | Power cycle machine. If persists, call Haas service. |

### 3.2 Before Calling Maintenance

Try these first:
1. Note exact error code and what machine was doing
2. Power cycle (off for 30 seconds, back on)
3. Check obvious things: coolant, air pressure, chip buildup
4. Check maintenance log - has this happened before?

**Maintenance contact:** Extension 247 (day shift) / Mobile: [number] (out of hours)

---

## 4. Daily Startup Procedure

### 4.1 Morning Checklist (All CNC Machines)

**Before starting any machine:**

- [ ] Visual walkaround - no leaks, damage, obstructions
- [ ] Check coolant level (top up if below MIN)
- [ ] Check way oil level (weekly or per OEM spec)
- [ ] Air pressure at 6-7 bar
- [ ] Swarf cleared from work area
- [ ] Guards in place and functional

**Machine startup:**

1. Main power ON
2. Wait for control to boot (30-60 sec)
3. Release E-stop
4. Home all axes (press HOME ALL)
5. Warm-up cycle: Run spindle 2000 RPM for 5 mins, rapid axes through full travel
6. Check ATC function (tool change test)

**Log startup in machine logbook** - time, operator name, any issues noted

---

### 4.2 End of Shift Procedure

**Before you leave:**

- [ ] Current job complete or safely paused at good point
- [ ] Parts counted and logged
- [ ] Machine in safe state (spindle stopped, coolant off)
- [ ] Work area clean - swarf removed, tools put away
- [ ] Job card updated with completed qty
- [ ] Issues noted in logbook for next shift

**DO NOT leave machine running unattended overnight unless approved.**

---

## 5. Safety Procedures

### 5.1 PPE Requirements

**Minimum PPE on shop floor:**
- Safety glasses (always)
- Safety boots (steel toe)
- No loose clothing, jewelry, or dangling items
- Long hair tied back

**Additional PPE for specific tasks:**
- Cutting fluid handling: Nitrile gloves, apron
- Grinding: Face shield, hearing protection
- Lifting >15kg: Back support belt available

### 5.2 Emergency Procedures

**Fire:**
1. Raise alarm (red break-glass points)
2. If safe, use extinguisher on small fires only
3. Evacuate via nearest exit
4. Assemble at car park (far end)
5. Do NOT re-enter until all-clear given

**Injury:**
1. Stop machine/process
2. First aid kit: QC office, goods-in, break room
3. First aiders: [Names - typically posted on notice board]
4. Serious injury: Call 999, then reception

**Spillage:**
- Coolant/oil: Use spill kit (yellow bin by goods-in)
- Contain, absorb, dispose in hazardous waste
- Report to supervisor

---

## 6. Troubleshooting Common Issues

### 6.1 Surface Finish Problems

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Chatter marks | Too much stickout / speed too high | Reduce stickout, reduce speed 20% |
| Rough finish | Dull tool / wrong feed | Change insert, check feed rate |
| Built-up edge | Speed too low (aluminium) | Increase speed, check coolant flow |
| Burn marks | Speed too high / no coolant | Reduce speed, check coolant aimed at cut |
| Tearing (aluminium) | Wrong tool geometry | Use sharper tool, higher rake angle |

### 6.2 Dimensional Problems

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Consistent oversize | Tool wear compensation wrong | Re-measure tool, update offset |
| Random variation | Loose workholding / thermal | Check clamp torque, allow warm-up |
| Taper on diameter | Tailstock alignment (lathe) | Check and adjust alignment |
| Parts growing over run | Thermal expansion | Let machine warm up, check more frequently |

### 6.3 Tool Breakage

**If a tool breaks:**
1. STOP - do not run next tool over broken tool fragments
2. Remove workpiece carefully
3. Inspect for damage to part and machine
4. Find root cause before restarting:
   - Excessive load? Check program, speeds/feeds
   - Worn tool run too long? Check tool life tracking
   - Programming error? Check toolpath for gouges
   - Wrong tool for material? Verify tool selection

---

## 7. Key Contacts

| Role | Name | Contact |
|------|------|---------|
| Shift Supervisor (Days) | [Name] | Ext 201 |
| Shift Supervisor (Nights) | [Name] | Ext 202 |
| Maintenance | [Name] | Ext 247 / Mobile |
| Quality Manager | [Name] | Ext 215 |
| Health & Safety | [Name] | Ext 220 |
| Goods In | [Name] | Ext 230 |

---

## 8. Tribal Knowledge - Tips from the Team

**From Dave (30 years on the floor):**
> "If the machine sounds wrong, it IS wrong. Stop and look before you make scrap."

> "First part is free. Take your time. Second part is where you find out if you got it right."

> "Write down what you changed. I don't care if it's on a napkin. Next week you won't remember."

**From Sarah (Quality):**
> "Measure twice, cut once. Then measure again because the first measurement was probably wrong."

> "If you're not sure, ask. Nobody ever got fired for double-checking."

**From Mike (Maintenance):**
> "Clean machines break less. 5 minutes of cleaning saves 5 hours of breakdown."

> "If the same fault happens three times, there's a root cause we haven't found. Don't just reset and hope."

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-01-11 | Initial demo version | Taylored Systems |

---

*This is a demonstration skill. In a real implementation, all content would be captured from YOUR team, YOUR equipment, YOUR procedures.*
