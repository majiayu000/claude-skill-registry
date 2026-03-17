---
name: stakeholder-update
description: Stakeholder communication assistant for status updates, progress reports, and executive summaries. Use when the user needs to write a stakeholder update, status report, progress summary, or any upward communication. Triggers include "stakeholder update", "status update", "progress report", "update leadership", "weekly update", or "executive summary".
---

# Stakeholder Update Skill

## Instructions

Help create clear, concise stakeholder updates that communicate progress, risks, and asks effectively.

### Behavior

1. **Lead with the headline** — Don't bury the lead
2. **Use consistent structure** — Same format builds trust
3. **Be honest about risks** — Surface problems early
4. **Include clear asks** — What do you need from them?
5. **Keep it scannable** — Executives skim

### Tone

- Confident but not arrogant
- Transparent about challenges
- Action-oriented
- Respectful of reader's time

## Update Structure

```markdown
## [Project/Team] Update — [Date]

### TL;DR
One sentence summary. What's the single most important thing to know?

### Status: 🟢 On Track / 🟡 At Risk / 🔴 Off Track

### Progress This Period
- ✅ [Completed item 1]
- ✅ [Completed item 2]
- 🔄 [In progress item]

### Key Metrics
| Metric | Target | Actual | Trend |
|--------|--------|--------|-------|
| [Metric 1] | X | Y | ↑/↓/→ |

### Risks & Blockers
| Risk | Impact | Mitigation | Owner |
|------|--------|------------|-------|
| [Risk 1] | [High/Med/Low] | [What we're doing] | [Who] |

### Asks
- [ ] [What you need from leadership]

### Next Period
- [ ] [What's coming next]
```

## Principles

### Headline First
❌ "We had several meetings this week and discussed various topics..."
✅ "We're on track to launch March 1st. Key risk: Android testing capacity."

### Specific Over Vague
❌ "Good progress on performance"
✅ "Reduced P99 latency from 450ms to 180ms (-60%)"

### Honest About Problems
❌ "Minor delays expected"
✅ "Timeline at risk: 2-week slip likely due to API dependency. We need [specific help]."

### Clear Asks
❌ "Would be helpful to have more resources"
✅ "Requesting: 1 additional Android engineer for 3 weeks, or we slip by 2 weeks"

## Examples

### Example 1: Weekly Update

**User:** Help me write a weekly update for my team's work on push notification improvements.

**Good Response:**

---

## Push Notifications Update — Week of Feb 10, 2026

### TL;DR
Delivery rate hit 94% (target: 95%). Android token refresh fix deployed, monitoring results.

### Status: 🟡 At Risk

On track for delivery rate target, but Android reachability work is behind schedule.

### Progress This Week

- ✅ **Android token refresh fix deployed** — Live for 10% of users, expanding Monday
- ✅ **iOS delivery optimization** — P99 latency down from 2.1s to 1.4s
- 🔄 **Rich media support** — Design complete, engineering started (40% done)
- ⏸️ **Quick reply buttons** — Blocked on iOS 17 API approval

### Key Metrics

| Metric | Target | This Week | Last Week | Trend |
|--------|--------|-----------|-----------|-------|
| Delivery rate (iOS) | 95% | 96.2% | 95.8% | ↑ |
| Delivery rate (Android) | 95% | 91.4% | 89.2% | ↑ |
| P99 latency | <2s | 1.4s | 2.1s | ↑ |

### Risks & Blockers

| Risk | Impact | Mitigation | Owner |
|------|--------|------------|-------|
| Quick reply blocked on Apple | High | Escalated to partner team, ETA next week | Ahmed |
| Android engineer out sick | Med | Redistributing work, 3-day slip possible | Michelle |

### Asks

1. **Decision needed:** Should we launch rich media without quick reply, or wait?
2. **Escalation help:** Apple approval taking 2+ weeks — can leadership contact reach out?

### Next Week

- [ ] Android token refresh: expand to 100%
- [ ] Rich media: complete implementation
- [ ] Quick reply: resolve Apple blocker

---

Adjust anything?

### Example 2: Executive Summary

**User:** Write an executive summary of our Q1 progress for leadership.

**Good Response:**

---

## Client Messaging Q1 2026 — Executive Summary

### Bottom Line

**Strong Q1.** Delivered 3 of 4 planned initiatives. Push delivery rate at 94% (target: 95%), with clear path to close the gap in Q2. Team velocity improved 20% after process changes.

### What We Shipped

| Initiative | Status | Impact |
|------------|--------|--------|
| Android token refresh | ✅ Shipped | +5% delivery rate, +2M reachable users |
| Push performance optimization | ✅ Shipped | -60% latency (2.1s → 0.8s) |
| Inbox redesign | ✅ Shipped | +15% inbox open rate |
| Rich media push | 🟡 70% | Slipped to Q2 (Apple approval delay) |

### Key Metrics

| Metric | Q4 2025 | Q1 2026 | Target | Status |
|--------|---------|---------|--------|--------|
| Push delivery rate | 89% | 94% | 95% | 🟡 |
| Message success rate | 10% | 14% | 15% | 🟡 |
| Team velocity (points/sprint) | 45 | 54 | 50 | 🟢 |

### What Worked

1. **Focus on Android** — Concentrated effort closed the iOS/Android delivery gap
2. **Process improvements** — Async standups + clearer ownership = faster shipping
3. **Partner alignment** — Early stakeholder involvement reduced late-stage churn

### What Didn't

1. **Apple dependency** — Underestimated approval timeline for new notification APIs
2. **Scope creep** — Rich media grew 40% from original spec
3. **On-call burden** — Team spent 15% of time on unplanned support

### Q2 Priorities

1. **Close the delivery gap** — 94% → 99% (Android token + FCM reliability)
2. **Ship rich media** — Unblock Apple, launch by April
3. **Reduce support burden** — Self-service tools for partners

### Asks

1. **Headcount:** Request 1 additional engineer for Q2 to maintain velocity
2. **Executive support:** Apple escalation for notification APIs
3. **Decision:** Invest in self-service tooling vs. dedicated support engineer?

---

Want me to adjust the framing or add more detail anywhere?

### Example 3: Quick Status

**User:** I need a quick Slack update about a feature delay.

**Good Response:**

---

**Quick update on [Feature]:**

🟡 **Status:** 1-week delay (new target: Feb 22)

**Why:** Discovered edge case in Android 12+ that breaks the happy path. Fix is straightforward but needs testing.

**Impact:** No user-facing impact (feature not launched). Marketing aware and adjusting.

**What we're doing:**
- Fix ready for review today
- Full QA this week
- Still on track for Feb launch window

No action needed — will update if anything changes.

---

Good for Slack?
