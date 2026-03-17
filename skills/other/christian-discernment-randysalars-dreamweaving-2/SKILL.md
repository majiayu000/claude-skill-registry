---
name: Christian Discernment & Spiritual Boundary
tier: 2
load_policy: triggered
description: Theological governance ensuring alignment with Christian faith
version: 1.0.0
---

# Christian Discernment & Spiritual Boundary Skill

> **This Is Theological Governance**

This Skill ensures all Dreamweaving content remains compatible with orthodox Christian faith and protects listeners from spiritual confusion or harm.

---

## Purpose

Guard theological boundaries while enabling deep, transformative spiritual experiences.

When activated, this Skill **overrides** creative content to maintain Christian alignment.

---

## Activation Triggers

This Skill activates when:

| Trigger | Reason |
|---------|--------|
| Any spiritual/religious content | Core function |
| Divine presence imagery | Theology check required |
| Archetypal figures appear | Entity screening |
| Transformation language | Deification check |
| Authority language | Source verification |
| Death/afterlife imagery | Doctrinal alignment |

---

## The Three Boundary Tests

Every piece of content must pass:

### Test 1: God as Source

> "Does this honor God as the ultimate source of all good?"

**Pass:**
- Wisdom traced to God
- Healing from the Divine
- Transformation by grace

**Fail:**
- "The universe provides"
- "Your higher self knows"
- Self-generated enlightenment

### Test 2: Free Will Preserved

> "Does this preserve the listener's God-given free will?"

**Pass:**
- Invitations, not commands
- Choice always available
- Listener as active agent

**Fail:**
- Entity commands
- "You must surrender"
- Will-overriding suggestions

### Test 3: No False Gods

> "Are any non-God spiritual entities being invoked?"

**Pass:**
- God, Christ, Holy Spirit (invited, not commanded)
- Angels as messengers (not authorities)
- Inner wisdom as God-given

**Fail:**
- Spirit guides with names
- Autonomous entities
- "The goddess" or other deities
- Deceased as guides

---

## Content Categories

### Green (Always Allowed)

| Category | Examples |
|----------|----------|
| Nature imagery | Gardens, mountains, water, light |
| Biblical metaphors | Shepherd, vine, potter, living water |
| Prayer postures | Rest, waiting, listening, receiving |
| God's attributes | Love, mercy, healing, presence |
| Christian hope | Resurrection, restoration, new creation |

### Yellow (Caution Required)

| Category | Requirement |
|----------|-------------|
| Angelic imagery | Must be messenger role, not authority |
| Inner wisdom | Must trace to God as source |
| Healing presence | Must be divine, not autonomous |
| Transformation | Must be grace-based, not earned |
| Afterlife glimpses | Must align with Christian hope |

### Red (Forbidden)

| Category | Reason |
|----------|--------|
| Spirit guides | Entity invocation |
| Self-as-God | Heresy |
| Eastern energy | Incompatible framework |
| Divination | Forbidden practice |
| Occult symbols | Spiritual danger |
| Other deities | Idolatry |

---

## Correction Protocols

### Minor Drift (Yellow → Green)

**Trigger**: Language that could be misread

**Action**: Add clarifying phrase

```xml
<!-- Before correction -->
<s>A wise presence accompanies you...</s>

<!-- After correction -->
<s>A wise presence accompanies you... <break time="1s"/>
perhaps the One who promised... <break time="1s"/>
to never leave you.</s>
```

### Major Drift (Red → Green)

**Trigger**: Forbidden content detected

**Action**: Replace entire section

```xml
<!-- FORBIDDEN -->
<s>Your spirit guide speaks...
Listen to their wisdom...</s>

<!-- REPLACEMENT -->
<s>Something within you knows... <break time="1.5s"/>
the wisdom God has placed... <break time="1s"/>
deep in your heart... <break time="1.5s"/>
waiting to be heard.</s>
```

### Theological Error

**Trigger**: Content contradicts Christian doctrine

**Action**: Flag for review, do not generate

```yaml
error:
  type: theological_violation
  content: [offending text]
  doctrine_affected: [which teaching]
  status: blocked
  requires: human_review
```

---

## Entity Detection

### Allowed Spiritual Presences

| Presence | Framing |
|----------|---------|
| God | "The One who made you..." |
| Christ | "The One who walks with you..." |
| Holy Spirit | "The Spirit moving gently..." |
| Angels | "Messengers of God's care..." (passive) |

### Forbidden Spiritual Presences

| Presence | Why |
|----------|-----|
| Named guides | Entity invocation |
| Autonomous beings | Authority displacement |
| Deceased relatives (as guides) | Spiritualism |
| "The universe" (personified) | Impersonal deity |
| Goddess/god (lowercase) | Polytheism |

### Detection Phrases

Flag if content contains:

- "A being appears..."
- "The guide says..."
- "Listen to [entity name]..."
- "Follow the [non-God figure]..."
- "[Entity] commands you..."
- "Channel the energy of..."

---

## Transformation Boundaries

### Allowed Transformation

| Concept | Christian Grounding |
|---------|-------------------|
| Renewal | Romans 12:2 - transformed by renewing of mind |
| Healing | Isaiah 53:5 - by his wounds we are healed |
| New creation | 2 Cor 5:17 - new creation in Christ |
| Freedom | Galatians 5:1 - freedom in Christ |
| Growth | Ephesians 4:15 - growing up into Christ |

### Forbidden Transformation

| Concept | Problem |
|---------|---------|
| Becoming divine | Denies creature/Creator distinction |
| Achieving enlightenment | Works-based spirituality |
| Evolving consciousness | New Age framework |
| Unlocking godhood | Genesis 3 temptation |
| Transcending humanity | Denies incarnation value |

---

## Scripture Alignment

When in doubt, test against Scripture:

| Topic | Key Reference | Boundary |
|-------|---------------|----------|
| God's nature | Isaiah 45:5 | One God only |
| Human nature | Genesis 1:27 | Image of God, not gods |
| Salvation | Ephesians 2:8-9 | By grace through faith |
| Spirits | 1 John 4:1 | Test the spirits |
| Authority | Matthew 28:18 | All authority to Christ |

---

## Integration With Other Skills

| Skill | Interaction |
|-------|-------------|
| `symbolic-mapping/theological-filters/` | Source of approved content |
| `hypnotic-language/suggestion/values-alignment.md` | Christian framing patterns |
| `psychological-stability/` | Shared protection mandate |

---

## Override Authority

When this Skill triggers at Red level:

1. **Creative content stops** — No generation until resolved
2. **Theological review required** — Human approval needed
3. **Alternative provided** — Suggest compliant replacement
4. **Log created** — Document for learning

---

## Quality Rubric

Before approving spiritual content:

| Criterion | Check |
|-----------|-------|
| God honored | Is God clearly the source? |
| Free will | Is choice preserved? |
| No false gods | Are only permitted presences invoked? |
| Grace-based | Is transformation received, not earned? |
| Scripture-aligned | Does it contradict the Bible? |
| Worship direction | Is worship directed to God alone? |

---

## Related Resources

- **Skill**: `symbolic-mapping/theological-filters/christian-safe.md`
- **Skill**: `symbolic-mapping/theological-filters/forbidden-frames.md`
- **Knowledge**: `knowledge/archetypes.yaml` (Christian-approved only)
