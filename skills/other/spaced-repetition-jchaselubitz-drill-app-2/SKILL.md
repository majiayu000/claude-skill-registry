---
name: spaced-repetition
description: This document describes the translation-based spaced repetition system, its data model, and study flow.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# Spaced Repetition Architecture

This document describes the translation-based spaced repetition system, its data
model, and study flow.

## Overview

- The SRS system is translation-pair based. Each `translation` row (a phrase
  pair) produces two cards:
  - `primary_to_secondary`
  - `secondary_to_primary`
- Cards store only scheduling state and foreign keys. The displayed text is
  pulled live from `phrase` rows.
- A deck contains translation pairs. Cards are scoped to a single deck.

## Data Model (WatermelonDB)

### Tables

- `deck`
  - Stores user-created decks and a default deck.
- `deck_translation`
  - Join table linking `deck` and `translation`.
- `srs_card`
  - Scheduling state for each direction of a translation pair.
- `srs_review_log`
  - Append-only review history for analytics and future FSRS upgrades.

### Key Fields

- `srs_card`
  - `deck_id`, `translation_id`, `direction`
  - `state` (`new`, `learning`, `review`, `relearning`)
  - `due_at`, `interval_days`, `ease`, `reps`, `lapses`, `step_index`
  - `last_reviewed_at` (timestamp of last review)
  - `suspended` (boolean; suspended cards are excluded from review queues)
  - `stability`, `difficulty` (nullable; reserved for future FSRS)
- `srs_review_log`
  - `srs_card_id`, `deck_id`, `translation_id`, `direction`
  - `reviewed_at`, `rating` (`failed`, `hard`, `good`, `easy`)
  - before/after snapshots: `state_*`, `interval_*`, `ease_*`, `due_*`

## Scheduling

- Scheduling is SM-2 inspired (Anki-aligned) with learning steps.
- **Learning phase (new cards)**:
  - Failed: 1 minute (resets to step 0)
  - Hard: 5 minutes (stays at current step, doesn't advance)
  - Good: Single step of 10 minutes, then graduates to 1 day (after completing the step)
  - Easy: 4 days (immediately graduates to review state)
- **Relearning phase** (after lapsing a review card):
  - Failed: Reset to step 0 (10 minutes)
  - Hard: Stay at current step (10 minutes)
  - Good: Advance through steps, then return to review state with interval reset to max(1 day, previous interval)
  - Easy: Immediately return to review state with interval reset to max(1 day, previous interval)
- **Review phase**:
  - Failed: -0.20 ease penalty, interval resets to 1 day (via multiplier of 0), enters relearning
  - Hard: -0.15 ease, interval × 1.2 (minimum 1 day)
  - Good: interval × ease (no ease change, minimum 1 day)
  - Easy: +0.15 ease, interval × ease × 1.3 (minimum 1 day)
- Ease factor defaults to 2.5 and is clamped to minimum 1.3 (matching Anki).
- **Future day scheduling**: Cards scheduled for future days (after graduating from learning or in review phase) are scheduled at the start of that day (`dayStartHour`), not at a specific time. This ensures cards are available throughout the entire day.
- Learning/relearning steps use precise timestamps to support intra-day intervals (minutes).
- Review history is logged for each rating event with before/after snapshots.

## Daily Limits and Rollover

- Daily limits are per-deck:
  - `maxNewPerDay` - Maximum number of cards in 'new' state that can be seen for
    the first time each day
  - `maxReviewsPerDay` - Maximum number of review sessions for cards in
    'learning', 'review', or 'relearning' states each day
- Day rollover is computed with a configurable `dayStartHour` (default: 4am).
- Counts are derived from `srs_review_log` using the day start boundary:
  - New cards are counted by `state_before = 'new'` in the review log
  - Reviews are counted by `state_before != 'new'` in the review log
- `getDailyLimitsRemaining()` returns `{ newRemaining, reviewsRemaining, newDone, reviewsDone }`
- **Important**: Daily limits are applied when the session queue is initially
  built. Cards reinserted later in the same session (because they are still due
  today) are not re-checked against daily limits.
- Suspended cards (`suspended = true`) are excluded from all review queues.

## Study Queue

The queue is built per deck following these rules:

1. **New cards**: Only shown if under the daily limit (`maxNewPerDay`)
   - Fetches cards in 'new' state that are due (`due_at <= now`)
   - Excludes suspended cards (`suspended = false`)
   - Limited to `maxNewPerDay - newCardsReviewedToday`
   - Sorted by `created_at` ascending (oldest first)

2. **Review cards**: Only shows cards that are actually due
   - Fetches cards in 'learning', 'review', or 'relearning' states where
     `due_at <= now`
   - Excludes suspended cards (`suspended = false`)
   - Limited to `maxReviewsPerDay - reviewsCompletedToday`
   - Sorted by `due_at` ascending (most overdue first)

3. **Queue behavior**:
   - New and review cards are combined
   - The combined list is sorted by `due_at` and then adjusted to maintain
     minimum spacing between cards with the same `translation_id` (see
     Translation Pair Separation section)
   - During a session, the in-memory queue is updated in place (no automatic
     reload when exhausted)

### Example Scenario

Assume a deck with:

- 44 cards in 'new' state
- Settings: `maxNewPerDay = 20`, `maxReviewsPerDay = 200`

**Day 1 (First Session)**:

- User sees 20 new cards (maxNewPerDay limit)
- Each card reviewed with 'good' transitions to 'learning' state with a single
  step (10 minutes)
- Remaining 24 new cards are NOT shown - they wait for subsequent days
- Session ends once no cards remain due today in the in-memory queue

**Day 1 (10+ minutes later)**:

- The 20 'learning' cards are now due for their next review
- User starts a new session and sees those 20 cards again (as reviews, not new
  cards)
- After completing the learning step (rating 'good' again), cards graduate to
  'review' state and are scheduled for the start of tomorrow

**Day 2**:

- User starts a new session and sees 20 more new cards (next batch from the 24
  remaining)
- Plus any cards from Day 1 that are due for review
- Pattern continues until all new cards have been introduced

**Day 3**:

- User starts a new session and sees final 4 new cards
- Plus any reviews that are scheduled for today
- No new cards remain after this

## UI Flow

- Review tab:
  - Deck picker, daily counts, and Start Review.
- Review session:
  - Prompt (front), reveal (back), rate with 4 buttons.
- Deck management:
  - Create/select decks, set active deck.
- Phrase detail:
  - Each translation pair can be assigned to a deck, which creates/updates its
    two cards.

## Review Session Flow (Queue Creation and Updates)

This section reflects the current implementation in `ReviewSessionScreen.tsx`
and `lib/srs/queue.ts`.

### Session Lifecycle

The review session follows a specific lifecycle:

1. **Screen Focus** → Session initializes (if not already initialized)
2. **Review Loop** → User rates cards, queue updates, next card loads
3. **Session End** → All cards scheduled for tomorrow or later
4. **Screen Blur** → Session state resets completely

When the screen loses focus (user navigates away), all session state is reset
via `useFocusEffect`. This ensures a fresh session starts when the user returns,
incorporating any new due cards.

### Session Initialization

On mount (or re-focus), `initializeSession()` runs once:

```
initializeSession()
├── Compute tomorrowStartMs via getNextStudyDayStart(now, dayStartHour)
├── getDailyLimitsRemaining(db, { deckId, now, dayStartHour, maxNewPerDay, maxReviewsPerDay })
│   ├── Query srs_review_log for reviews since day start
│   ├── Count new cards reviewed (state_before = 'new')
│   ├── Count reviews completed (state_before != 'new')
│   └── Return { newRemaining, reviewsRemaining, newDone, reviewsDone }
├── getReviewQueue(db, { deckId, nowMs, reviewsRemaining, newRemaining })
│   ├── Fetch review cards (learning/review/relearning) where due_at <= now
│   ├── Fetch new cards where due_at <= now (up to newRemaining)
│   ├── Combine and pass through sortCardsMaintainingSeparation()
│   └── Return sorted queue
├── Store sessionCards and compute initial stats
├── countCardsStillDueToday(db, { cardIds, tomorrowStartMs })
└── Hydrate and display first card
```

> **Known limitation**: `tomorrowStartMs` is calculated once at session start
> and does not update during the session. If a user reviews across the
> `dayStartHour` boundary (e.g., starts at 3:50 AM and continues past 4:00 AM
> with default settings), the "due today" threshold becomes stale. This is
> acceptable because users rarely review across day boundaries, and the session
> resets when the screen loses focus.

### Loading the Next Card

`loadNextCard(queue, startIndex)` finds and displays the next due card:

```
loadNextCard(queue, startIndex)
├── If queue is empty → setCurrentItem(null), end session
├── getNextDueCardIndex({ queue, nowMs, startIndex })
│   └── Linear scan from startIndex, return first card where dueAt <= nowMs
├── If null and startIndex > 0 → Wrap around: getNextDueCardIndex({ queue, nowMs, startIndex: 0 })
│   └── Cards earlier in queue may have become due after being rescheduled
├── If still null → No due cards, setCurrentItem(null), end session
├── Re-fetch card from database (ensures fresh scheduling data)
├── hydrateCard(freshCard)
│   ├── Fetch translation, primary phrase, secondary phrase
│   ├── Determine front/back based on card.direction
│   └── Return { card, translation, front, back } or null on failure
├── If hydration fails → Remove card from queue, recursively try next
└── Set currentItem, showBack=false, update currentIndex
```

**Key behaviors:**

- **Wrap-around search**: If no due card is found from `startIndex` forward,
  searches from index 0 to catch cards that became due earlier in the queue
- **Fresh data**: Cards are re-fetched from the database before display to avoid
  stale scheduling data
- **Graceful hydration failure**: If a card can't be hydrated (missing
  translation/phrases), it's removed from the queue and the next card is tried

### Per-Rating Update Flow

When the user rates a card, `handleRate(rating)` executes:

```
handleRate(rating)
├── scheduleSm2Review(cardState, rating, nowMs, dayStartHour)
│   ├── Compute new { state, dueAt, intervalDays, ease, reps, lapses, stepIndex }
│   └── For future days, use getFutureDayStartMs() to schedule at day start
├── db.write()
│   ├── Update srs_card with new scheduling fields
│   └── Create srs_review_log entry with before/after snapshots
├── Decide reinsertion:
│   ├── If update.dueAt < tomorrowStartMs → Re-fetch card from DB
│   └── Otherwise → Card exits queue (scheduled for tomorrow+)
├── applyCardRescheduleToQueue({ queue, currentCardId, refreshedCard, tomorrowStartMs, currentIndex })
│   ├── Remove current card from queue
│   ├── If still due today → insertCardMaintainingSeparation(queue, refreshedCard)
│   └── Compute nextStartIndex (accounting for queue shifts)
├── Update sessionCards with new queue
├── countCardsStillDueToday(db, { cardIds, tomorrowStartMs })
├── Update sessionStats.remainingToday
├── Track completed cards:
│   └── If update.dueAt >= tomorrowStartMs → Add card.id to completedCardIds Set
├── If remainingToday === 0 → Session complete, setCurrentItem(null)
└── Otherwise → loadNextCard(newQueue, nextStartIndex)
```

### Queue Index Management

`applyCardRescheduleToQueue()` handles the complexity of maintaining correct
indices after queue mutations:

```
applyCardRescheduleToQueue({ queue, currentCardId, refreshedCard, tomorrowStartMs, currentIndex })
├── Remove current card: newQueue = queue.filter(c => c.id !== currentCardId)
├── If card still due today:
│   ├── insertCardMaintainingSeparation(newQueue, refreshedCard)
│   ├── Find reinsertedIndex
│   └── If reinsertedIndex <= currentIndex → nextStartIndex = currentIndex + 1
│       (Card inserted at/before our position, need to skip over it)
├── If nextStartIndex >= newQueue.length → Clamp (handled by wrap-around in loadNextCard)
└── Return { queue: newQueue, nextStartIndex }
```

### Translation Pair Separation

To avoid showing both directions of a translation pair too close together (e.g., "dog
→ perro" then "perro → dog"), two algorithms maintain minimum spacing:

- **Minimum spacing**: Cards with the same `translation_id` must be at least
  `MIN_CARD_SPACING` (4) positions apart in the queue.

**`sortCardsMaintainingSeparation(cards)`** - Initial queue sorting:

```
1. Sort cards by due_at ascending
2. Iterate looking for spacing violations (cards with same translation_id within MIN_CARD_SPACING positions)
3. For each violation found:
   a. Look ahead up to searchRange (max(10, MIN_CARD_SPACING * 2)) positions for a swap candidate
   b. Swap only if:
      - Candidate has different translation_id
      - Swap won't create new violations
      - Urgency difference < 1 hour (maintains reasonable order)
   c. If no forward candidate, look backward up to searchRange positions
   d. Fallback: Swap forward even if it creates new violations (to make progress)
4. Repeat until no violations found or max iterations reached (queue.length * 3)
```

**`insertCardMaintainingSeparation(queue, card)`** - Reinsertion during session:

```
1. Find ideal position based on card.dueAt (maintain urgency order)
2. Check if insertion would violate spacing (same translation_id within MIN_CARD_SPACING positions)
3. If violation would occur:
   a. Search forward for next valid position that maintains spacing
   b. If no forward position found, search backward
   c. Insert at first valid position found
4. If no valid position found (edge case: all cards have same translation_id) → Append to end
```

**Note**: The spacing algorithm prioritizes maintaining urgency order (by `due_at`)
while ensuring translation pairs are well-separated. If pairs are naturally far
apart temporally, they may appear closer in the queue, but this is acceptable
since they're not due at similar times anyway.

### Session Statistics

The session tracks:

- `totalInSession`: Number of cards in the initial queue
- `remainingToday`: Cards still due before `tomorrowStartMs` (recalculated after
  each rating)
- `completedCardIds`: Set of unique card IDs scheduled for tomorrow or later

`completedCardIds.size` represents unique cards completed, not total reviews. A
card reviewed multiple times during learning steps only counts once when it
finally graduates to tomorrow.

## Key Files

- Schema/migrations: `database/schema.ts`, `database/migrations.ts`
- Models: `database/models/Deck.ts`, `database/models/DeckTranslation.ts`,
  `database/models/SrsCard.ts`, `database/models/SrsReviewLog.ts`
- Scheduler/queue: `lib/srs/sm2.ts`, `lib/srs/queue.ts`, `lib/srs/time.ts`
- Screens: `features/review/screens/ReviewHomeScreen.tsx`,
  `features/review/screens/ReviewSessionScreen.tsx`,
  `features/review/screens/DecksScreen.tsx`
- Phrase integration: `features/phrase/screens/PhraseDetailScreen.tsx`

## Future Extensions

- FSRS scheduling: use `srs_review_log` plus `stability`/`difficulty` fields to
  migrate.
- Multi-deck assignment per translation (optional).
- Additional card templates (cloze, hints, or extra metadata on cards).
