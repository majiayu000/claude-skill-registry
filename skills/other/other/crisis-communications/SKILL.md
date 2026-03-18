---
name: crisis-communications
description: Crisis communication and rapid response workflows for journalists and communications professionals. Use when covering breaking news events, managing organizational communications during crises, coordinating rapid fact-checking efforts, or developing crisis response plans. Essential for newsrooms, PR teams, and anyone who needs to communicate accurately under time pressure.
---

# Crisis communications

Frameworks for accurate, rapid communication during high-pressure situations.

## When to activate

- Breaking news requires immediate coverage
- Organization faces public crisis or controversy
- Misinformation is spreading rapidly and needs countering
- Emergency situation requires coordinated communication
- Rapid fact-checking is needed before publication
- Preparing crisis response plans before incidents occur

## Breaking news protocol

### First 30 minutes checklist

```markdown
## Breaking news response

**Event**: [Brief description]
**Time detected**: [HH:MM]
**Initial source**: [Where we learned of this]

### Immediate actions (0-10 min)
- [ ] Verify event is real (minimum 2 independent sources)
- [ ] Alert editor/team lead
- [ ] Check wire services (AP, Reuters, AFP)
- [ ] Monitor official accounts (agencies, officials)
- [ ] DO NOT publish unverified claims

### Verification phase (10-30 min)
- [ ] Primary source contacted/confirmed
- [ ] Location verified (if applicable)
- [ ] Official statement obtained or requested
- [ ] Eyewitness accounts gathered (note: unverified)
- [ ] Social media claims flagged for verification

### First publication decision
- [ ] What we KNOW (confirmed facts only)
- [ ] What we DON'T know (be explicit)
- [ ] What we're working to confirm
- [ ] Attribution clear for every claim
```

### Newsroom escalation matrix

```python
from enum import Enum
from dataclasses import dataclass
from typing import List

class CrisisLevel(Enum):
    LEVEL_1 = "routine"      # Single reporter can handle
    LEVEL_2 = "elevated"     # Editor involvement needed
    LEVEL_3 = "major"        # Multiple reporters, editor oversight
    LEVEL_4 = "critical"     # All hands, executive involvement

@dataclass
class BreakingEvent:
    description: str
    level: CrisisLevel
    confirmed_facts: List[str]
    unconfirmed_claims: List[str]
    sources_contacted: List[str]
    assigned_reporters: List[str]

    def escalation_needed(self) -> bool:
        """Determine if event needs escalation."""
        triggers = [
            len(self.unconfirmed_claims) > 5,  # Too many unknowns
            "fatalities" in self.description.lower(),
            "official" in self.description.lower(),
            "government" in self.description.lower(),
        ]
        return any(triggers)

ESCALATION_TRIGGERS = {
    CrisisLevel.LEVEL_2: [
        "Multiple fatalities confirmed",
        "Major public figure involved",
        "Legal/liability concerns",
        "Significant local impact",
    ],
    CrisisLevel.LEVEL_3: [
        "National news potential",
        "Active danger to public",
        "Major institution affected",
        "Coordinated misinformation detected",
    ],
    CrisisLevel.LEVEL_4: [
        "Mass casualty event",
        "Government/democracy implications",
        "Our organization directly involved",
        "Imminent physical threat",
    ],
}
```

## Rapid verification framework

### The 5-minute verification

When time is critical, prioritize these checks:

```markdown
## Rapid verification checklist

### Source check (1 min)
- [ ] Who is claiming this?
- [ ] Are they in position to know?
- [ ] Have they been reliable before?

### Corroboration (2 min)
- [ ] Does anyone else confirm?
- [ ] Check wire services
- [ ] Check official sources

### Red flags (1 min)
- [ ] Too perfect/dramatic?
- [ ] Matches known false narratives?
- [ ] Single source only?

### Decision (1 min)
- [ ] PUBLISH: Multiple credible sources, no red flags
- [ ] HOLD: Needs more verification
- [ ] MONITOR: Developing, don't publish yet
```

### Verification triage system

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class VerificationStatus(Enum):
    UNVERIFIED = "unverified"
    PARTIALLY_VERIFIED = "partially_verified"
    VERIFIED = "verified"
    DEBUNKED = "debunked"
    UNCERTAIN = "uncertain"

@dataclass
class Claim:
    text: str
    source: str
    first_seen: datetime
    urgency: int  # 1-5, higher = more urgent to verify
    status: VerificationStatus = VerificationStatus.UNVERIFIED
    verification_notes: str = ""
    verifier: Optional[str] = None

class VerificationQueue:
    """Manage claims awaiting verification."""

    def __init__(self):
        self.claims = []

    def add_claim(self, claim: Claim):
        self.claims.append(claim)
        self._sort_by_priority()

    def _sort_by_priority(self):
        """Urgent claims first, then by time seen."""
        self.claims.sort(
            key=lambda c: (-c.urgency, c.first_seen)
        )

    def next_claim(self) -> Optional[Claim]:
        """Get highest priority unverified claim."""
        for claim in self.claims:
            if claim.status == VerificationStatus.UNVERIFIED:
                return claim
        return None

    def update_status(self, claim: Claim,
                      status: VerificationStatus,
                      notes: str,
                      verifier: str):
        claim.status = status
        claim.verification_notes = notes
        claim.verifier = verifier
```

## Crisis communication templates

### Holding statement

For when you need to say something but facts are incomplete:

```markdown
## Initial statement template

[Organization] is aware of [brief description of situation].

We are actively [gathering information / investigating / monitoring the situation].

[If applicable: The safety of [stakeholders] is our top priority.]

We will provide updates as verified information becomes available.

For media inquiries: [contact]
For [affected parties]: [resource/hotline]

Last updated: [timestamp]
```

### Correction/clarification

```markdown
## Correction notice

**Correction [or Clarification]**: An earlier version of this [article/statement/post] [stated/implied] [incorrect information].

[If factual error]: The correct information is: [accurate facts].

[If misleading]: To clarify: [accurate context].

This [article/statement] has been updated to reflect accurate information.

We regret the error.

[Timestamp of correction]
```

### Retraction (when necessary)

```markdown
## Retraction notice

**Retraction**: [Publication name] is retracting [article title], published on [date].

[Brief explanation of what was wrong]: Our reporting [stated/relied on] [problematic element]. Subsequent verification revealed [why it was wrong].

[What you're doing about it]: We have [removed/updated] the article and are reviewing our editorial processes.

[Accountability]: We apologize to [affected parties] and our readers.

The full text of the original article is available [here/on request] for transparency.

Questions: [contact]
```

## Social media crisis response

### Monitoring during crisis

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict
from collections import Counter

@dataclass
class CrisisMention:
    platform: str
    content: str
    author: str
    timestamp: datetime
    sentiment: str  # positive, negative, neutral, misinformation
    reach: int  # followers/potential impressions
    requires_response: bool = False

class CrisisMonitor:
    """Track crisis-related social mentions."""

    def __init__(self, crisis_keywords: List[str]):
        self.keywords = crisis_keywords
        self.mentions: List[CrisisMention] = []

    def add_mention(self, mention: CrisisMention):
        self.mentions.append(mention)

    def get_dashboard(self) -> dict:
        """Real-time crisis overview."""
        recent = [m for m in self.mentions
                  if (datetime.now() - m.timestamp).seconds < 3600]

        return {
            'total_mentions_1h': len(recent),
            'sentiment_breakdown': self._sentiment_counts(recent),
            'top_platforms': self._platform_counts(recent),
            'misinformation_count': len([
                m for m in recent
                if m.sentiment == 'misinformation'
            ]),
            'high_reach_negative': [
                m for m in recent
                if m.sentiment == 'negative' and m.reach > 10000
            ],
            'pending_responses': len([
                m for m in self.mentions
                if m.requires_response
            ])
        }

    def _sentiment_counts(self, mentions: List[CrisisMention]) -> Dict:
        return dict(Counter(m.sentiment for m in mentions))

    def _platform_counts(self, mentions: List[CrisisMention]) -> Dict:
        return dict(Counter(m.platform for m in mentions))
```

### Response decision tree

```markdown
## Should we respond to this?

### High priority (respond quickly)
- [ ] Factual misinformation spreading rapidly
- [ ] Direct question from journalist
- [ ] Affected party seeking help
- [ ] Influential account spreading false info

### Medium priority (respond thoughtfully)
- [ ] General negative sentiment
- [ ] Questions about our response
- [ ] Comparisons to competitors' handling

### Low priority / Do not engage
- [ ] Obvious trolling
- [ ] Bad faith actors
- [ ] Pile-on with no new claims
- [ ] Emotional venting (let it pass)

### Never respond
- [ ] While angry
- [ ] With unverified information
- [ ] In a way that escalates conflict
- [ ] By deleting legitimate criticism
```

## Internal crisis coordination

### Communication chain

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class CrisisTeamMember:
    name: str
    role: str
    phone: str
    email: str
    backup: Optional['CrisisTeamMember'] = None

@dataclass
class CrisisLog:
    """Maintain record of all crisis decisions."""
    entries: List[dict] = None

    def __post_init__(self):
        self.entries = self.entries or []

    def log(self, action: str, decision_maker: str,
            rationale: str, outcome: str = "pending"):
        self.entries.append({
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'decision_maker': decision_maker,
            'rationale': rationale,
            'outcome': outcome
        })

    def export_for_postmortem(self) -> str:
        """Generate timeline for after-action review."""
        lines = ["# Crisis Response Timeline\n"]
        for entry in self.entries:
            lines.append(
                f"**{entry['timestamp']}** - {entry['action']}\n"
                f"- Decision by: {entry['decision_maker']}\n"
                f"- Rationale: {entry['rationale']}\n"
                f"- Outcome: {entry['outcome']}\n"
            )
        return '\n'.join(lines)
```

### Status update template

For keeping stakeholders informed:

```markdown
## Crisis status update #[X]

**As of**: [timestamp]
**Next update**: [scheduled time]

### Current situation
[2-3 sentence summary of where things stand]

### What we know
- [Confirmed fact 1]
- [Confirmed fact 2]

### What we're working on
- [Action item 1] - [owner]
- [Action item 2] - [owner]

### Key decisions made
- [Decision] - [rationale]

### Immediate next steps
1. [Next action]
2. [Next action]

### Resources needed
- [Resource/support needed]

---
**Contact**: [Crisis lead name and number]
```

## Post-crisis review

### After-action checklist

```markdown
## Post-crisis review template

### Timeline reconstruction
- When did we first learn of the crisis?
- When did we first respond publicly?
- Key decision points and timing

### What went well
- [Specific success 1]
- [Specific success 2]

### What could improve
- [Gap or failure 1] → [Recommended fix]
- [Gap or failure 2] → [Recommended fix]

### Process questions
- Did escalation work as intended?
- Were the right people involved?
- Did we have accurate information when needed?
- Was external communication timely and accurate?

### Specific improvements
- [ ] Update crisis protocol to address [gap]
- [ ] Train team on [identified weakness]
- [ ] Add [resource/tool] for future incidents

### Documentation
- All communications archived: [ ] Yes
- Decision log complete: [ ] Yes
- Media coverage compiled: [ ] Yes
```

## Misinformation rapid response

### Counter-messaging framework

```markdown
## Misinformation response checklist

### Before responding
- [ ] Is this claim spreading significantly?
- [ ] Will our response reach the affected audience?
- [ ] Could responding amplify the false claim?

### The response formula
1. **Lead with truth** (don't repeat the myth first)
2. **Be specific** about what's accurate
3. **Explain briefly** why the false claim is wrong
4. **Provide source** for accurate information

### Example structure
GOOD: "The event starts at 7pm at City Hall. Some posts incorrectly listed the time as 5pm."

BAD: "Some people are saying the event is at 5pm. That's wrong. It's actually at 7pm."
(Repeating the myth first reinforces it)
```

## Journalist safety during crisis

```markdown
## Field safety checklist

### Before deployment
- [ ] Editor knows your location and check-in schedule
- [ ] Emergency contacts updated
- [ ] Phone charged, backup battery
- [ ] First aid basics reviewed
- [ ] Exit routes identified

### During coverage
- [ ] Regular check-ins maintained
- [ ] Location sharing active
- [ ] Press credentials visible
- [ ] Recording when safe to do so
- [ ] Not taking unnecessary risks for story

### If situation escalates
- [ ] Leave immediately if directed
- [ ] Follow crowd flow, don't fight it
- [ ] Protect equipment but not at personal risk
- [ ] Contact newsroom ASAP
```

## Related skills

- **source-verification** - Verify claims during fast-moving events
- **social-media-intelligence** - Monitor spread of information
- **interview-transcription** - Document statements accurately

---

## Skill metadata

| Field | Value |
|-------|-------|
| Version | 1.0.0 |
| Created | 2025-12-26 |
| Author | Claude Skills for Journalism |
| Domain | Communications, Journalism |
| Complexity | Advanced |
