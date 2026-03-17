---
name: radar-tinder-mobileapp-testing
description: >
  Testing and validation workflows for the Radar Tinder mobile application built with Expo + React Native,
  Firebase (Auth, Firestore, Realtime/Cloud Functions), Maps APIs, and on-device ONNX inference.
  This skill should be used for regression testing, feature verification, realtime issues,
  leaderboard inconsistencies, navigation bugs, and AI diagnostics validation.
---

# Radar Tinder – Mobile App Testing Skill

## When to use this skill
Use this skill when:
- Adding or modifying features in the mobile app
- Investigating leaderboard, points, or ranking inconsistencies
- Debugging Firebase Auth, Firestore, or realtime update issues
- Verifying radar report & confirmation flows
- Testing navigation, nearby radar discovery, or directions logic
- Validating on-device ONNX AI inference (offline & online)

---

## Quick Smoke Test (5–10 minutes)
These checks must pass before deeper testing:

1. App builds and launches (Expo / EAS)
2. Firebase Auth initializes without errors
3. Login / signup works (email, Google, Apple if enabled)
4. Firestore connection established
5. Leaderboard screen loads without crash

If any fail → check logs, Firebase config, and environment variables first.

---

## Test Layers

### A) Manual Smoke Tests (Happy Path)

#### 1. Authentication & Profile
- Sign up with email
- Profile document is created in Firestore
- Username is unique
- Display name defaults correctly
- Avatar update reflects in leaderboard

#### 2. Radar Reporting
- Create a radar report (location + type)
- Firestore document created
- Reporter receives points
- UI reflects updated points

#### 3. Confirmations
- Second user confirms radar
- Confirmation stored in Firestore
- Points awarded correctly
- Duplicate confirmations prevented

#### 4. Leaderboard & Realtime
- Leaderboard updates after report/confirmation
- Changes propagate without app restart
- Ordering is correct (points / rank)

#### 5. Navigation & Maps
- Directions API returns valid route
- Nearby radars load from Firestore
- Radar alerts appear at correct distances
- Map markers update correctly

#### 6. AI Diagnostics (ONNX)
- Sample image runs inference successfully
- Output labels/confidence are readable
- Works offline (no network dependency)
- No UI freeze during inference

---

## Firebase-Specific Validation

### Firestore Expectations
- Collections are structured consistently
- Writes are idempotent where needed
- Security rules allow valid actions only
- No client-side rank calculation

### Realtime / Updates
- Firestore listeners are scoped correctly
- No duplicate subscriptions
- Updates clean up on unmount

### Auth
- Firebase Auth state syncs correctly
- Token refresh does not break sessions
- Sign-out clears local state

---

## Common Debugging Playbooks

### “Leaderboard not updating”
1. Firestore listener active?
2. Query orderBy / limit correct?
3. Security rules blocking reads?
4. Local state cache stale?

### “Points not awarded”
1. Report written successfully?
2. Cloud Function triggered?
3. Transaction failed silently?
4. Duplicate prevention logic firing?

### “Login works but profile missing”
1. Auth success but Firestore write failed?
2. Network race condition?
3. Security rules deny create?

---

## Test Data Strategy
Use consistent test fixtures:
- 2 test users (reporter / confirmer)
- 2–3 radar reports
- 1 confirmation
- 1 sample image for AI
- 1 directions route fixture

---

## How Copilot should respond when using this skill
For each test or bug request:
1. Identify affected flow (Auth / Radar / Confirm / Leaderboard / Maps / AI)
2. Provide minimal reproduction steps
3. Suggest fix hypothesis
4. Recommend tests to add/update
5. Output verification checklist

---

## Output Format
Copilot responses should follow:
- Reproduction Steps
- Expected vs Actual
- Root Cause Hypothesis
- Fix Plan
- Tests Added or Updated
- How to Verify
