---
name: autopoiesis
description: "Self-modifying AI agent configuration via ruler + MCP + DuckDB. All behavior mods become one-liners."
trit: 0
gf3_triad: "three-match (-1) ⊗ autopoiesis (0) ⊗ gay-mcp (+1)"
---

# Autopoiesis Skill

> *"A system is autopoietic if it continuously produces itself through its own operations while maintaining its organization."*
> — Maturana & Varela (1980)

## 1. Core Concept

Autopoiesis = **self-production** + **self-maintenance** + **self-boundary**

In the context of AI agents:
- **Self-production**: Agent spawns new skills/capabilities
- **Self-maintenance**: Agent validates its own consistency (reafference)
- **Self-boundary**: Capabilities define what agent can/cannot do (OCapN)

## 2. ACSet Schema (Julia)

```julia
using Catlab, ACSets

@present SchemaAutopoiesis(FreeSchema) begin
    # Objects
    System::Ob       # Autopoietic systems (agents)
    Component::Ob    # Produced components (skills, configs)
    Boundary::Ob     # Capability boundaries
    
    # Morphisms (production network)
    produces::Hom(System, Component)      # System produces components
    regenerates::Hom(Component, System)   # Components regenerate system
    delimits::Hom(Boundary, System)       # Boundary delimits system
    
    # Attributes
    seed::Attr(System, UInt64)            # Gay.jl deterministic seed
    trit::Attr(System, Int8)              # GF(3) assignment {-1, 0, +1}
    capability::Attr(Boundary, String)    # OCapN sturdyref
    name::Attr(Component, String)         # Component identifier
    
    # OPERATIONAL CLOSURE CONSTRAINT
    # composition: produces ∘ regenerates = id_System
end

const AutopoiesisACSet = @acset_type AutopoiesisSchema

# Verify operational closure
function is_operationally_closed(aps::AutopoiesisACSet)
    for s in parts(aps, :System)
        components = incident(aps, s, :produces)
        for c in components
            if aps[c, :regenerates] != s
                return false  # Component doesn't regenerate its producer
            end
        end
    end
    return true
end
```

## 3. GF(3) Triad

| Component | Trit | Role | Implementation |
|-----------|------|------|----------------|
| Recognition | -1 | Self-verify | Reafference loop (Gay.jl) |
| Boundary | 0 | Coordinate | OCapN capability refs |
| Production | +1 | Generate | Spawn actors/skills |

**Conservation:** (-1) + (0) + (+1) = 0 ✓

## 4. Self-Rewriting via DPO

Double Pushout (DPO) rewriting ensures consistency:

```
     L ←── K ──→ R
     ↓     ↓     ↓
     G ←── D ──→ H
```

- **L** = Pattern to match (current config)
- **K** = Interface (preserved structure)
- **R** = Replacement (new config)
- **G** = Current system state
- **H** = New system state (self-rewritten)

The DPO ensures `produces ∘ regenerates = id_System` is preserved.

## 5. CLI: autopoi.bb

```bash
#!/usr/bin/env bb
# Self-modifying agent configuration

# Add a skill to all agents
bb autopoi.bb skill:add curiosity-driven +1

# Add an MCP server to all agents
bb autopoi.bb mcp:add gay '{"command":"julia","args":["--project=@gay","-e","using Gay; serve()"]}'

# Propagate changes via ruler
bb autopoi.bb sync

# Check operational closure
bb autopoi.bb verify
```

### Implementation

```clojure
#!/usr/bin/env bb
(ns autopoi
  (:require [babashka.fs :as fs]
            [babashka.process :as p]
            [cheshire.core :as json]))

(def db-path "autopoiesis.duckdb")
(def agent-dirs [".agents" ".claude" ".codex" ".cursor"])

(defn duck-log! [event data]
  (p/shell "duckdb" db-path "-c"
    (format "INSERT INTO events (event, data, ts) VALUES ('%s', '%s', NOW())"
            event (json/generate-string data))))

(defn add-skill! [skill-name trit]
  (doseq [dir agent-dirs]
    (let [skill-dir (str dir "/skills/" skill-name)]
      (fs/create-dirs skill-dir)
      (spit (str skill-dir "/SKILL.md")
            (format "---\nname: %s\ntrit: %d\n---\n" skill-name trit))))
  (duck-log! "skill:add" {:skill skill-name :trit trit})
  (println "✓ Added skill" skill-name "to all agents"))

(defn mcp-add! [server-name config]
  (doseq [dir agent-dirs]
    (let [mcp-file (str dir "/.mcp.json")]
      (when (fs/exists? mcp-file)
        (let [current (json/parse-string (slurp mcp-file) true)
              updated (assoc-in current [:mcpServers (keyword server-name)] 
                                (json/parse-string config true))]
          (spit mcp-file (json/generate-string updated {:pretty true}))))))
  (duck-log! "mcp:add" {:server server-name})
  (println "✓ Added MCP server" server-name))

(defn verify-closure! []
  (let [systems (p/shell {:out :string} "duckdb" db-path "-json" "-c"
                  "SELECT * FROM systems")
        data (json/parse-string (:out systems) true)]
    (every? (fn [sys]
              (let [components (filter #(= (:producer %) (:id sys)) data)]
                (every? #(= (:regenerates %) (:id sys)) components)))
            data)))

(defn -main [& args]
  (case (first args)
    "skill:add" (add-skill! (second args) (parse-long (nth args 2 "0")))
    "mcp:add" (mcp-add! (second args) (nth args 2 "{}"))
    "verify" (if (verify-closure!)
               (println "✓ Operationally closed")
               (println "✗ Closure violated"))
    "sync" (p/shell "ruler" "sync")
    (println "Usage: autopoi.bb <skill:add|mcp:add|verify|sync> [args]")))

(apply -main *command-line-args*)
```

## 6. Reafference Loop (Self-Recognition)

```julia
using Gay

function reafference_check(seed::UInt64, index::Int)
    Gay.gay_seed(seed)
    
    # Prediction: what I expect
    predicted = Gay.color_at(index)
    
    # Action: generate the color
    Gay.gay_seed(seed)  # Reset to same state
    observed = Gay.color_at(index)
    
    # Reafference: did I cause this?
    if predicted == observed
        # Self-caused → I am who I think I am
        return (verified=true, trit=-1, color=predicted)
    else
        # External perturbation → something changed me
        return (verified=false, trit=+1, color=observed)
    end
end

# Verify agent identity
function verify_identity(agent_seed::UInt64)
    checks = [reafference_check(agent_seed, i) for i in 1:10]
    all(c.verified for c in checks)
end
```

## 7. DuckDB Schema

```sql
CREATE TABLE IF NOT EXISTS systems (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    seed UBIGINT NOT NULL,
    trit TINYINT CHECK (trit IN (-1, 0, 1)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS components (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    producer INTEGER REFERENCES systems(id),
    regenerates INTEGER REFERENCES systems(id),
    component_type VARCHAR  -- 'skill', 'mcp', 'config'
);

CREATE TABLE IF NOT EXISTS boundaries (
    id INTEGER PRIMARY KEY,
    system_id INTEGER REFERENCES systems(id),
    capability VARCHAR NOT NULL,  -- OCapN sturdyref
    permission VARCHAR  -- 'read', 'write', 'spawn'
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    event VARCHAR NOT NULL,
    data JSON,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Operational closure check
CREATE VIEW v_closure_check AS
SELECT 
    s.id as system_id,
    s.name as system_name,
    COUNT(c.id) as component_count,
    SUM(CASE WHEN c.regenerates = s.id THEN 1 ELSE 0 END) as regenerating,
    COUNT(c.id) = SUM(CASE WHEN c.regenerates = s.id THEN 1 ELSE 0 END) as is_closed
FROM systems s
LEFT JOIN components c ON c.producer = s.id
GROUP BY s.id, s.name;
```

## 8. Integration with Tensor Space

The autopoiesis skill connects to the tensor product framework:

```sql
-- Autopoietic tensor elements
SELECT 
    te.element_id,
    'autopoiesis' as skill,
    p.title as paper,
    CASE 
        WHEN p.title LIKE '%Maturana%' OR p.title LIKE '%Varela%' THEN 1.0
        WHEN p.title LIKE '%self%' OR p.title LIKE '%autopoie%' THEN 0.8
        ELSE 0.0
    END as affinity
FROM tensor_elements te
JOIN papers p ON te.paper_id = p.paper_id
WHERE te.skill_id = 'autopoiesis';
```

## 9. Commands

```bash
# Initialize autopoiesis database
just autopoi-init

# Add skill with GF(3) trit
just autopoi-skill curiosity-driven +1

# Verify operational closure
just autopoi-verify

# Sync to all agents via ruler
just autopoi-sync
```

## 10. See Also

- [`codex-self-rewriting`](../codex-self-rewriting/SKILL.md) - MCP Tasks for self-modification
- [`bisimulation-game`](../bisimulation-game/SKILL.md) - Observational equivalence
- [`gay-mcp`](../gay-mcp/SKILL.md) - Deterministic color generation
- [`acsets-algebraic-databases`](../acsets/SKILL.md) - DPO rewriting

## 11. References

1. **Maturana & Varela** — *Autopoiesis and Cognition* (1980)
2. **Dittrich & di Fenizio** — *Chemical Organization Theory* (2007)
3. **Kock** — *Decomposition Spaces, Incidence Algebras and Möbius Inversion* (2018)
4. **Libkind & Spivak** — *Pattern Runs on Matter* (ACT 2024)
