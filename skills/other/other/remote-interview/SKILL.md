---
name: remote-interview
description: "Capture professional-quality remote interviews using double-ender technique and dedicated recording platforms for podcasts, media, and content production. Use when: Setting up remote podcast interviews with guests; Recording media interviews across distances; Creating customer interview content; Producing expert interviews for thought leadership; Conducting research interviews with high audio quality"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Remote Interview Recording

> Capture professional-quality remote interviews using double-ender technique and dedicated recording platforms for podcasts, media, and content production.

## When to Use This Skill

- Setting up remote podcast interviews with guests
- Recording media interviews across distances
- Creating customer interview content
- Producing expert interviews for thought leadership
- Conducting research interviews with high audio quality
- Planning equipment recommendations for interview guests

## Methodology Foundation

**Source**: NPR Engineering Standards + Remote Recording Best Practices

**Core Principle**: "Local recording is key." The gold standard for remote interviews is the "double-ender" technique—both participants record locally on their own devices, then tracks are combined in post-production. This eliminates internet compression, lag, and connection issues that plague Zoom-style recordings.

**Why This Matters**: Internet-based audio suffers from compression artifacts, dropouts, and quality degradation. By recording locally at each location, you capture broadcast-quality audio regardless of connection quality. Platforms like Riverside, Zencastr, and SquadCast automate this process while maintaining professional standards.


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## What This Skill Does

1. **Selects optimal recording approach** - Platform vs. manual double-ender
2. **Prepares guest technical setup** - Equipment, environment, troubleshooting
3. **Manages recording workflow** - Pre-checks, backup systems, session flow
4. **Ensures quality capture** - Audio levels, monitoring, issue prevention
5. **Handles post-production sync** - Aligning tracks, editing, export

## How to Use

### Plan Remote Interview Setup
```
Help me set up remote interview recording.
Interview type: [podcast/media/research]
Guest technical level: [savvy/average/low]
Quality requirements: [broadcast/professional/good enough]
Budget: [range]
```

### Prepare Guest Instructions
```
Create guest preparation guide for remote interview.
Platform: [Riverside/Zencastr/SquadCast/manual]
Recording date: [date/time]
Expected duration: [minutes]
Guest equipment: [known setup or unknown]
```

### Troubleshoot Recording Issues
```
Help diagnose/fix this remote recording issue:
Problem: [describe issue]
Platform: [which platform]
Guest setup: [what we know]
```

## Instructions

When setting up remote interviews, follow this methodology:

### Step 1: Choose Recording Approach

Select the right method based on needs and constraints.

```
## Recording Approach Decision

### Option 1: Dedicated Platform (Recommended)

Best for: Regular podcasters, non-technical guests, convenience

**Platform Comparison (2026)**:

| Feature | Riverside | Zencastr | SquadCast |
|---------|-----------|----------|-----------|
| Video Quality | 4K | 4K (paid) | 1080p |
| Audio Format | Lossless WAV | High-quality | High-quality |
| Local Recording | ✅ | ✅ | ✅ |
| Max Participants | 8 | 12 | 10 |
| Livestreaming | ✅ | ❌ | ❌ |
| AI Editing | ✅ | ✅ (ZenAI) | Via Descript |
| Hosting | ❌ | ✅ | ❌ |
| Free Tier | 2 hrs/mo | Trial only | 1 hr/mo |
| Best For | Quality-first | All-in-one | Descript users |

**Recommendation by use case**:
- Podcast + Livestream → Riverside
- Podcast + Distribution → Zencastr
- Already use Descript → SquadCast
- Budget-conscious → Zencastr trial or Riverside free

### Option 2: Manual Double-Ender

Best for: Maximum quality, technical guests, existing equipment

**Setup**:
- Host: Records on DAW (Logic, Audition, Audacity)
- Guest: Records on Voice Memos, Audacity, or phone app
- Sync: Manual alignment using clap or verbal cue
- Communication: Zoom/Meet for video only (audio muted)

**When to use**:
- Guest has professional setup already
- Maximum control over quality needed
- Platform doesn't support your use case
- Free/budget priority

### Option 3: Backup Recording (Zoom)

Best for: Casual interviews, fallback capture

**Limitations**:
- Compressed audio (not broadcast quality)
- Single-track or limited multitrack
- Connection-dependent quality

**When acceptable**:
- Informal interviews
- Backup alongside primary recording
- Guest absolutely cannot use dedicated platform
```

---

### Step 2: Equipment Hierarchy

Recommend appropriate equipment for guest's situation.

```
## Equipment Recommendations

### Tier 1: Professional (Best Quality)
- **Microphone**: XLR mic (Shure SM7B, RE20, AT4040)
- **Interface**: Focusrite Scarlett, Apollo, RodeCaster
- **Headphones**: Closed-back monitoring (Sony MDR-7506)
- **Environment**: Treated room or vocal booth
- **Result**: Broadcast quality, professional sound

### Tier 2: Prosumer (Excellent Quality)
- **Microphone**: USB mic (Rode NT-USB, Blue Yeti, AT2020 USB)
- **Headphones**: Any closed-back or good earbuds
- **Environment**: Quiet room, soft furnishings
- **Result**: Professional enough for most podcasts

### Tier 3: Minimum Viable (Good Quality)
- **Microphone**: Lavalier/clip-on mic ($25-50)
- **Headphones**: AirPods or standard earbuds
- **Environment**: Quietest room available
- **Result**: Clearly better than laptop mic

### Tier 4: Emergency (Acceptable)
- **Microphone**: Smartphone (Voice Memos, close to mouth)
- **Headphones**: Wired earbuds with inline mic
- **Environment**: Closet full of clothes (seriously)
- **Result**: Salvageable, may need heavy processing

### Tier 5: Avoid
- **Laptop mic**: Distant, echoey, picks up typing/fans
- **AirPods mic**: Inconsistent, compression artifacts
- **Speakerphone**: Echo, room noise, unusable

### Equipment Quick Guide for Guests

"For the best audio quality, here's the hierarchy:
1. Best: USB microphone (Rode, Blue Yeti, AT2020)
2. Great: Wired headset/earbuds with mic
3. Good: AirPods/wireless earbuds
4. Last resort: Phone close to face

Please avoid using your laptop's built-in microphone if possible."
```

---

### Step 3: Environment Preparation

Guide guests to optimize their recording space.

```
## Environment Checklist

### For Guests (Send Before Interview)

**Room Selection**:
□ Choose smallest room with soft furnishings
□ Bedroom or closet > living room or kitchen
□ Avoid rooms with hard surfaces (tile, glass, concrete)
□ No background noise sources (AC, appliances, traffic)

**Sound Treatment**:
□ Close all windows and doors
□ Add soft materials (blankets, pillows) if room echoes
□ Position away from walls (not in corner)
□ Test for echo: clap hands, listen for reverb

**Technical Setup**:
□ Use wired internet if possible (Ethernet > WiFi)
□ Close all other applications
□ Disable notifications (phone on silent, computer DND)
□ Charge devices or plug in
□ Restart computer before session

**During Recording**:
□ Keep phone on airplane mode
□ Don't touch desk/table (transmitted as rumble)
□ Mute when not speaking (if platform supports)
□ Keep water nearby but pour quietly

### Common Issues to Prevent

| Problem | Cause | Prevention |
|---------|-------|------------|
| Echo | Hard surfaces | Add soft materials |
| Background noise | AC, fans, traffic | Turn off, close windows |
| Rumble | Desk vibration | Mic on boom arm or separate stand |
| Plosives | "P" and "B" sounds | Pop filter or angle mic |
| Mouth noise | Dry mouth | Water, green apple before |
| Interruptions | Family, pets | Lock door, schedule quiet time |
```

---

### Step 4: Pre-Session Checklist

Steps before hitting record.

```
## Pre-Recording Checklist

### 30 Minutes Before

**Host**:
□ Test platform is working
□ Create/test room link
□ Check your audio levels
□ Prepare backup recording (Zoom, phone)
□ Review questions and flow
□ Set up notes/questions visible

**Guest Communication**:
□ Send join link with instructions
□ Remind: "Please use Chrome browser"
□ Remind: "Use headphones if possible"
□ Remind: "Choose quiet location"
□ Share expected duration

### 10 Minutes Before

**Tech Check with Guest**:
□ Test audio—ask them to speak, check waveform
□ Test video (if applicable)
□ Confirm they hear you clearly
□ Check for background noise
□ Verify recording is actually capturing

### Start of Session

**Sync Protocol** (for double-ender):
1. Both start recording
2. Host: "3, 2, 1, clap" (or snap)
3. Both clap simultaneously
4. This creates sync point for post-production

**Level Check**:
□ Ask guest to speak at normal volume
□ Verify levels not peaking (aim for -12 to -6 dB)
□ Adjust if needed

**Backup Confirmation**:
□ Verify primary recording running
□ Start backup recording (Zoom, phone)
□ Announce: "Recording has started"
```

---

### Step 5: During Recording

Manage the session for optimal capture.

```
## Recording Session Management

### Monitor Throughout

**Watch For**:
- Audio levels (not too hot, not too quiet)
- Connection warnings from platform
- Background noise appearing
- Guest technical issues

**If Issues Occur**:
- Brief technical problems: Continue, can edit later
- Major issues: Pause, troubleshoot, resume
- Unrecoverable: Stop, reschedule affected portion

### Interviewer Best Practices

**For Clean Edit**:
- Don't talk over guest (wait for them to finish)
- Use non-verbal acknowledgment (nod, smile) instead of "mm-hmm"
- If you must react verbally, do it after they complete thought
- Re-ask questions cleanly if needed for edit

**For Backup Safety**:
- At natural breaks: "Let's pause for a moment"
- Check platform shows recording active
- Confirm backup still running

### Common Mid-Session Fixes

| Issue | Quick Fix |
|-------|-----------|
| Echo appearing | Guest: mute when not speaking |
| Noise introduced | Identify source, eliminate or pause |
| Connection dropping | Both continue recording, sync later |
| Levels changed | Stop, reset levels, note timestamp |
```

---

### Step 6: Post-Recording Workflow

Handle files after session ends.

```
## Post-Recording Process

### Immediately After

**Platform Recording**:
1. Confirm recording saved/processing
2. Download all tracks (WAV preferred)
3. Verify files play correctly
4. Back up to cloud storage

**Manual Double-Ender**:
1. Collect guest's recording (file share)
2. Import both tracks to DAW
3. Find sync point (clap)
4. Align tracks precisely

### File Management

**Naming Convention**:
```
[Date]_[Guest]_[Topic]_[Track].wav

Examples:
2026-01-26_JohnSmith_AIMarketing_Host.wav
2026-01-26_JohnSmith_AIMarketing_Guest.wav
2026-01-26_JohnSmith_AIMarketing_Backup.wav
```

**Storage Structure**:
```
interviews/
├── raw/
│   ├── 2026-01-26_JohnSmith/
│   │   ├── host.wav
│   │   ├── guest.wav
│   │   └── backup.wav
├── edited/
│   └── 2026-01-26_JohnSmith_final.wav
└── published/
    └── episode-45_john-smith.mp3
```

### Quality Check

□ All tracks recorded completely
□ Audio is clear, no major issues
□ Sync point exists (clap/verbal)
□ No missing sections
□ Backup is usable if needed
```

## Examples

### Example 1: Podcast Guest Setup

**Context**: Regular podcast needs to onboard non-technical guest.

**Input**:
> Set up remote interview recording. Guest is a marketing executive, not technical. We need professional quality for weekly podcast. Using Riverside.

**Output**:

## Guest Onboarding: Riverside Setup

### Pre-Interview Email (Send 3 Days Before)

Subject: Quick setup for our interview on [Date]

Hi [Guest],

Looking forward to our conversation on [topic]! Here's everything you need for a smooth recording.

**Recording Link**: [Riverside room link]

**When**: [Date, Time, Timezone]

**Duration**: Approximately [X] minutes

**Simple Setup for Best Audio**:

1. **Browser**: Please use Chrome (works best with our platform)
2. **Headphones**: Any earbuds work—this prevents echo
3. **Location**: Quiet room with soft furnishings (bedroom works great)
4. **Internet**: Wired connection if available, strong WiFi otherwise

**5 Minutes Before**:
- Click the link, allow camera/microphone permissions
- I'll be there to do a quick tech check

No software to install—it all works in your browser.

Let me know if you have any questions!

### Day-Of Checklist (Host)

**30 min before**:
□ Open Riverside, test your setup
□ Verify recording settings (WAV, separate tracks)
□ Prepare Zoom backup link (just in case)
□ Review questions

**When guest joins**:
□ Greet, make them comfortable
□ "Can you say a few sentences? I'm checking audio levels"
□ Verify waveform shows good signal
□ "Great, your audio sounds perfect"

**Before starting**:
□ "I'm starting the recording now"
□ Click Record
□ Brief pause, then begin

### If Issues Arise

**Guest audio is echoey**:
"Could you try using headphones? Even phone earbuds work great."

**Connection seems unstable**:
"Let's try turning off your video—often helps with connection."
"Do you have a phone you could use as a backup?"

**Platform isn't working**:
"Let me send you a Zoom link as backup while we troubleshoot."

---

### Example 2: High-Stakes Media Interview

**Context**: Important media interview requiring broadcast quality.

**Input**:
> Recording interview with major tech CEO for industry publication. Must be absolute best quality. CEO has staff who can help with setup. What's the ideal approach?

**Output**:

## Premium Interview Setup: Tech CEO

### Recommended Approach: Assisted Double-Ender

Given the importance and available support, use a hybrid approach:
- **Platform**: Riverside (for convenience + automatic local recording)
- **Backup**: CEO records locally on professional equipment
- **Result**: Dual-redundant broadcast-quality capture

### Executive Brief (Send to CEO's Team)

**Subject**: Technical Setup for [Publication] Interview

**Recording Date**: [Date/Time]

**Our platform will handle most of the technical work, but for the absolute best quality, here's the ideal setup:**

**Equipment** (if available):
- USB microphone (Rode NT-USB, Blue Yeti, or similar)
- Wired earbuds or headphones
- Quiet, private room

**If professional AV support is available**:
- XLR microphone into USB interface
- Record local backup via voice recorder or DAW
- Ensure 48kHz/24-bit settings

**Minimum acceptable**:
- AirPods or headset with microphone
- Chrome browser
- Quiet location

**We will send**:
- Riverside link (no install needed)
- Brief tech check 5 minutes before

### Host Preparation

**Primary Recording**: Riverside
- Room created with guest name
- Settings: 4K video (if video), Lossless audio, Separate tracks
- Downloaded permission: Enabled

**Secondary Recording**: Local DAW
- Audio interface active
- Recording armed
- Sync clap planned

**Tertiary Backup**: Zoom
- Meeting created (not shared unless needed)
- Cloud recording enabled
- Last-resort option

### Quality Assurance Protocol

**Before Recording**:
□ Confirm guest's audio is clean (no echo, background)
□ Verify Riverside shows strong signal
□ Confirm CEO's team is recording backup locally
□ State sync phrase: "Recording starting. Three, two, one, sync."
□ Both clap simultaneously

**During Recording**:
□ Monitor Riverside waveform
□ Watch for connection warnings
□ If any issue: "Let's pause briefly to ensure we're capturing this properly"

**After Recording**:
□ Confirm Riverside saved all tracks
□ Request CEO team's local file via secure transfer
□ Compare both for best quality
□ Archive all versions

### Deliverable Quality

- **Minimum**: 48kHz/16-bit WAV
- **Preferred**: 48kHz/24-bit WAV
- **Usable backup**: 44.1kHz/16-bit or high-quality MP3

---

### Example 3: Budget Remote Recording

**Context**: New podcaster with limited budget needs to interview remote guests.

**Input**:
> I'm starting a podcast and need to record remote interviews. Don't want to spend much money. What's my best option?

**Output**:

## Budget Remote Recording Setup

### Free/Low-Cost Approach

**Best free option**: Riverside Free Tier
- 2 hours/month recording
- Watermark on video (audio clean)
- Local recording for quality
- Separate tracks

**Alternative**: Zencastr Free Trial
- 14-day full access
- Good for getting started

**Zero-cost manual method**:
- Communication: Zoom free (audio muted, video only)
- Your recording: Audacity (free) or Voice Memos
- Guest recording: Voice Memos (iPhone) or Easy Voice Recorder (Android)
- Sync: Clap at start, align in post

### Equipment on a Budget

**For you ($50-100)**:
- Audio-Technica ATR2100x-USB ($79) - excellent value
- Or: Fifine K669 USB mic ($30) - good enough to start

**For guests (free)**:
- Their phone's Voice Memos app
- Wired earbuds (prevents echo)
- Quiet room

### Budget Workflow

**Before Interview**:
1. Set up Riverside free room
2. Email guest link + instructions
3. Prepare backup plan (both record on phones)

**Guest Instructions Email**:
```
For best audio:
1. Use Chrome browser
2. Wear any headphones/earbuds
3. Find quiet spot
4. Click this link: [Riverside link]

No downloads needed! I'll be there 5 min early to check sound.
```

**During Interview**:
1. Start Riverside recording
2. Start local backup (Voice Memos on phone)
3. Have guest record on their end (as backup)
4. Do quick clap for sync

**After**:
1. Download Riverside tracks (separate)
2. Edit in Audacity (free)
3. If Riverside had issues, use backup recordings

### Upgrade Path

As podcast grows:
1. **Month 1-3**: Free tier, learn process
2. **Month 4+**: Riverside paid ($24/mo) for unlimited
3. **Month 6+**: Better equipment as revenue allows

Total starting cost: $30-80 (mic only)

## Checklists & Templates

### Guest Preparation Email Template

```
Subject: Recording Setup for [Show Name] - [Date]

Hi [Name],

Excited for our conversation on [topic]!

**Quick Setup** (5 minutes):

🎧 **Headphones**: Please use any earbuds or headphones (prevents echo)

🔇 **Quiet Space**: Find a room away from noise, soft furnishings help

💻 **Browser**: Use Chrome for best compatibility

**Join Link**: [Your platform link]

**When**: [Date, Time, Timezone]

**I'll be there 5 minutes early** to do a quick sound check.

Reply to confirm, or let me know if you have questions!

[Your name]
```

---

### Pre-Recording Checklist

```
## 30 Minutes Before

□ Platform tested and working
□ Room link created/verified
□ Your audio setup tested
□ Backup recording ready (Zoom/phone)
□ Questions/notes prepared
□ Water within reach

## When Guest Joins

□ Audio check: "Can you speak for a few seconds?"
□ Video check (if applicable)
□ Confirm headphone use
□ Listen for background noise
□ Check levels on platform

## Before "Record"

□ State: "I'm starting the recording now"
□ Click record
□ Sync clap: "3, 2, 1, [clap]"
□ Brief pause
□ Begin interview

## After Recording

□ Confirm file saved
□ Download all tracks
□ Thank guest for time
□ Send follow-up email
```

---

### Technical Troubleshooting Quick Reference

```
## Common Issues & Solutions

### Audio Problems

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Echo | No headphones | Guest: use any earbuds |
| Robotic audio | Bad connection | Turn off video, switch to phone |
| Quiet audio | Low mic gain | Platform: adjust input level |
| Distorted audio | Too loud | Move back from mic |
| Background noise | Environment | Mute between speaking |

### Connection Problems

| Symptom | Fix |
|---------|-----|
| "Connection unstable" | Turn off video |
| Freezing video | Lower quality settings |
| Keeps disconnecting | Switch to mobile hotspot |
| Won't connect at all | Try incognito window |

### Platform Problems

| Issue | Solution |
|-------|----------|
| Mic not detected | Check browser permissions |
| Recording not starting | Refresh, try again |
| Platform down | Switch to Zoom backup |
| Files won't download | Wait, try different browser |
```

## Skill Boundaries

### What This Skill Does Well
- Structuring audio production workflows
- Providing technical guidance
- Creating quality checklists
- Suggesting creative approaches

### What This Skill Cannot Do
- Replace audio engineering expertise
- Make subjective creative decisions
- Access or edit audio files directly
- Guarantee commercial success

## References

- Riverside. "14 Tips for Recording Interviews Professionally"
- NPR Training. "Audio Recording Standards"
- Buzzsprout. "How to Record Remote Podcast Interviews"
- Transom. "Recording Phone Calls and Skype"
- Podcasters' Guide to Audio Engineering

## Related Skills

- [podcast-production](../podcast-production/) - Full production workflow
- [podcast-interview](../podcast-interview/) - Interview technique
- [audio-editing](../audio-editing/) - Post-production processing
- [voice-design](../voice-design/) - When AI voice is needed instead

---

## Skill Metadata (Internal Use)

```yaml
name: remote-interview
category: audio
subcategory: recording
version: 1.0
author: MKTG Skills
source_expert: NPR Engineering, Remote Recording Best Practices
source_work: Double-Ender Technique
difficulty: beginner
estimated_value: Professional interview quality without studio
tags: [remote-recording, podcast, interview, double-ender, riverside]
created: 2026-01-26
updated: 2026-01-26
```
