---
name: delta-derivation
description: Extract information delta between Claude.ai conversation exports using ACSets morphisms and bisimulation verification
version: 1.0.0
---


# Delta Derivation Skill

**Trit**: -1 (MINUS - Validator)
**Color**: #007FFF (Cold Blue)
**Role**: Extract and verify conversation export deltas

---

## Core Algorithm

```bash
# 1. Extract conversations from exports
unzip -o "$RECENT_ZIP" conversations.json -d /tmp/recent_export
unzip -o "$PREVIOUS_ZIP" conversations.json -d /tmp/previous_export

# 2. Extract conversation IDs
jq -r '.[].conversation_id' /tmp/recent_export/conversations.json | sort > /tmp/recent_ids.txt
jq -r '.[].conversation_id' /tmp/previous_export/conversations.json | sort > /tmp/prev_ids.txt

# 3. Compute delta (new conversations)
comm -23 /tmp/recent_ids.txt /tmp/prev_ids.txt > /tmp/new_ids.txt

# 4. Bisimulation check (mutations in shared conversations)
jq -r '.[] | "\(.conversation_id) \(.current_node)"' /tmp/recent_export/conversations.json | sort > /tmp/recent_states.txt
jq -r '.[] | "\(.conversation_id) \(.current_node)"' /tmp/previous_export/conversations.json | sort > /tmp/prev_states.txt
comm -3 /tmp/recent_states.txt /tmp/prev_states.txt > /tmp/mutated.txt
```

---

## ACSets Schema

```clojure
(def ConversationACSet
  {:objects #{:Conversation :Message :Node}
   :morphisms {:has_mapping [:Conversation :Node]
               :parent_of [:Node :Node]
               :contains [:Node :Message]}
   :attributes {:conversation_id [:Conversation :String]
                :title [:Conversation :String]
                :create_time [:Conversation :Timestamp]
                :update_time [:Conversation :Timestamp]
                :current_node [:Conversation :UUID]}})

(defn delta-morphism [recent previous]
  "Compute injective morphism from previous → recent"
  (let [shared (set/intersection (ids recent) (ids previous))
        new-convos (set/difference (ids recent) (ids previous))
        removed (set/difference (ids previous) (ids recent))]
    {:type :injection
     :shared (count shared)
     :new (count new-convos)
     :removed (count removed)
     :new-ids new-convos}))
```

---

## Bisimulation Verification

```clojure
(defn bisimilar? [conv1 conv2]
  "Check if two conversations are observationally equivalent"
  (and (= (:conversation_id conv1) (:conversation_id conv2))
       (= (:current_node conv1) (:current_node conv2))
       (= (count (:mapping conv1)) (count (:mapping conv2)))))

(defn find-mutations [recent previous]
  "Find conversations that exist in both but have diverged"
  (let [shared-ids (set/intersection (ids recent) (ids previous))]
    (filter (fn [id]
              (not (bisimilar? (get-conv recent id)
                               (get-conv previous id))))
            shared-ids)))
```

---

## Skill Extraction

```clojure
(defn extract-skill-mentions [conversations]
  "Find skill invocations in conversation content"
  (let [patterns [#"/(\w+)"                    ; slash commands
                  #"skill[:\s]+[\"']?(\w+)"   ; skill mentions
                  #"(\w+-\w+(?:-\w+)*)"]]     ; hyphenated skill names
    (->> conversations
         (mapcat :messages)
         (mapcat (fn [msg]
                   (for [p patterns
                         m (re-seq p (:content msg ""))]
                     (second m))))
         frequencies
         (sort-by val >))))
```

---

## Full Pipeline

```bash
#!/usr/bin/env bash
# delta-derive.sh - Extract conversation export delta

set -euo pipefail

RECENT="$1"
PREVIOUS="$2"
OUTPUT="${3:-/tmp/delta_analysis.json}"

# Extract
unzip -qo "$RECENT" conversations.json -d /tmp/recent_export
unzip -qo "$PREVIOUS" conversations.json -d /tmp/previous_export

# Compute delta
jq -s '
  (.[0] | map({key: .conversation_id, value: .}) | from_entries) as $recent |
  (.[1] | map({key: .conversation_id, value: .}) | from_entries) as $prev |
  {
    recent_count: (.[0] | length),
    previous_count: (.[1] | length),
    new_conversations: [.[0][] | select(.conversation_id | in($prev) | not) | {
      id: .conversation_id,
      title: .title,
      created: .create_time,
      nodes: (.mapping | length)
    }],
    mutated_conversations: [.[0][] |
      select(.conversation_id | in($prev)) |
      select(.current_node != $prev[.conversation_id].current_node) |
      {
        id: .conversation_id,
        title: .title,
        old_node: $prev[.conversation_id].current_node,
        new_node: .current_node,
        node_delta: ((.mapping | length) - ($prev[.conversation_id].mapping | length))
      }
    ],
    delta_size_bytes: ((.[0] | tostring | length) - (.[1] | tostring | length))
  }
' /tmp/recent_export/conversations.json /tmp/previous_export/conversations.json > "$OUTPUT"

echo "Delta saved to $OUTPUT"
jq -r '"New: \(.new_conversations | length), Mutated: \(.mutated_conversations | length)"' "$OUTPUT"
```

---

## GF(3) Triadic Analysis

| Stream | Role | Analysis |
|--------|------|----------|
| MINUS (-1) | Validator | Bisimulation check, mutation detection |
| ERGODIC (0) | Coordinator | Merge results, compute frequencies |
| PLUS (+1) | Generator | Extract new conversations, skill mentions |

```clojure
(defn triadic-delta [recent previous]
  "Run delta derivation with GF(3) balanced agents"
  (let [minus (future (find-mutations recent previous))
        ergodic (future (compute-frequencies recent previous))
        plus (future (extract-new-convos recent previous))]
    {:mutations @minus
     :frequencies @ergodic
     :new-convos @plus
     :gf3-sum 0}))
```

---

## Commands

```bash
just delta-derive RECENT.zip PREVIOUS.zip   # Full delta analysis
just delta-new RECENT.zip PREVIOUS.zip      # List new conversations only
just delta-mutated RECENT.zip PREVIOUS.zip  # List mutated conversations
just delta-skills RECENT.zip PREVIOUS.zip   # Extract skill frequencies
just delta-bisim RECENT.zip PREVIOUS.zip    # Run bisimulation check
```

---

## Justfile Integration

```just
# Delta derivation commands
delta-derive recent previous:
    @~/.claude/skills/delta-derivation/delta-derive.sh "{{recent}}" "{{previous}}"

delta-new recent previous:
    @unzip -qo "{{recent}}" conversations.json -d /tmp/r && \
     unzip -qo "{{previous}}" conversations.json -d /tmp/p && \
     comm -23 <(jq -r '.[].conversation_id' /tmp/r/conversations.json | sort) \
              <(jq -r '.[].conversation_id' /tmp/p/conversations.json | sort)

delta-skills recent previous:
    @~/.claude/skills/delta-derivation/delta-derive.sh "{{recent}}" "{{previous}}" && \
     jq '.new_conversations[].title' /tmp/delta_analysis.json
```

---

## Related Skills

- `acsets-relational-thinking` (-1): Schema modeling
- `bisimulation-game` (0): Equivalence verification
- `temporal-coalgebra` (-1): Stream observation
- `compression-progress` (0): Information gain measurement

---

**Base directory**: ~/.claude/skills/delta-derivation



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.