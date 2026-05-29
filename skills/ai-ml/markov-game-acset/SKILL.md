---
name: markov-game-acset
description: "markov-game-acset skill"
version: 1.0.0
---


# Markov Game ACSet: State-Dependent Open Games

> *"Repeated games are not possible (but Markov games will be soon)"*  
> — [open-games-engine Tutorial](https://github.com/CyberCat-Institute/open-game-engine), line 29

**This skill fills that gap.** Markov games as attributed C-sets with:
- State-dependent strategy spaces
- World operators as information reflow (derangement-constrained)
- GF(3) conservation across state transitions

## Core Insight: Markov Games = Open Games + State ACSet

```
┌─────────────────────────────────────────────────────────────────┐
│  MARKOV GAME = OPEN GAME × STATE CATEGORY                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Standard Open Game:                                            │
│       ┌───────────┐                                             │
│    X ─│           │─ Y    (play: strategies)                    │
│       │  Game G   │                                             │
│    R ←│           │← S    (coplay: utilities)                   │
│       └───────────┘                                             │
│                                                                 │
│  Markov Game adds STATE FUNCTOR:                                │
│       ┌───────────┐        ┌───────────┐                        │
│    X ─│           │─ Y  ───│           │─ X'                    │
│       │  Game G   │        │ Transition│                        │
│    R ←│           │← S  ←──│     T     │← R'                    │
│       └───────────┘        └───────────┘                        │
│            ↓                    ↓                               │
│         State s              State s'                           │
│                                                                 │
│  State transitions follow DERANGEMENT: σ(s) ≠ s                 │
│  No world can observe itself—information MUST reflow            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## ACSet Schema for Markov Games

```julia
using Catlab.CategoricalAlgebra
using Catlab.Present

@present SchMarkovGame(FreeSchema) begin
    # Core objects
    State::Ob
    Action::Ob
    Player::Ob
    Transition::Ob
    
    # Morphisms
    src_state::Hom(Transition, State)      # Where we came from
    tgt_state::Hom(Transition, State)      # Where we're going
    action_taken::Hom(Transition, Action)  # What triggered it
    acting_player::Hom(Action, Player)     # Who acts
    
    # Strategy space depends on state
    StrategyAtState::Ob
    strategy_state::Hom(StrategyAtState, State)
    strategy_action::Hom(StrategyAtState, Action)
    
    # Payoffs depend on (state, action profile)
    Payoff::Ob
    payoff_state::Hom(Payoff, State)
    payoff_player::Hom(Payoff, Player)
    
    # Attributes
    Name::AttrType
    Trit::AttrType
    Probability::AttrType
    Utility::AttrType
    
    state_name::Attr(State, Name)
    state_trit::Attr(State, Trit)          # GF(3) assignment
    action_name::Attr(Action, Name)
    player_name::Attr(Player, Name)
    player_trit::Attr(Player, Trit)        # MINUS/ERGODIC/PLUS
    trans_prob::Attr(Transition, Probability)
    payoff_value::Attr(Payoff, Utility)
    
    # DERANGEMENT CONSTRAINT: No self-loops in state space
    # Implemented via: src_state(t) ≠ tgt_state(t) for all t
end

@acset_type MarkovGame(SchMarkovGame, index=[:src_state, :tgt_state])
```

## Derangement Constraint on State Transitions

The key innovation: **state transitions are derangements**.

```julia
"""
Verify Markov game satisfies derangement constraint.
No state can transition to itself (σ(s) ≠ s).
"""
function is_derangement_markov(game::MarkovGame)
    for t in parts(game, :Transition)
        src = game[t, :src_state]
        tgt = game[t, :tgt_state]
        if src == tgt
            return false  # Self-loop found: VIOLATION
        end
    end
    return true
end

"""
Filter transitions to derangement subgraph.
Removes self-loops, keeping only proper reflow.
"""
function derangement_subgraph(game::MarkovGame)
    valid_transitions = filter(parts(game, :Transition)) do t
        game[t, :src_state] != game[t, :tgt_state]
    end
    # Return induced subgraph on valid transitions
    induced_subacset(game, :Transition => valid_transitions)
end
```

## GF(3) Conservation in State Space

States are colored by GF(3) trits. Transitions must conserve total trit sum:

```julia
"""
Verify GF(3) conservation across state transitions.
For each transition: trit(src) + trit(action) + trit(tgt) ≡ 0 (mod 3)
"""
function verify_gf3_transitions(game::MarkovGame)
    for t in parts(game, :Transition)
        src_trit = game[game[t, :src_state], :state_trit]
        tgt_trit = game[game[t, :tgt_state], :state_trit]
        action = game[t, :action_taken]
        player = game[action, :acting_player]
        player_trit = game[player, :player_trit]
        
        total = src_trit + player_trit + tgt_trit
        if total % 3 != 0
            @warn "GF(3) violation" transition=t src=src_trit player=player_trit tgt=tgt_trit
            return false
        end
    end
    return true
end
```

## World Operators as Information Reflow

From derangement-reflow skill: **world operators are reflow operators**.

```julia
"""
World operator W: State → State with information accounting.

Each transition t: s → s' has:
- MINUS: Information leaves s (entropy source)
- ERGODIC: Information transits via action (channel)
- PLUS: Information arrives at s' (entropy sink)

WEV (World Extractable Value) = value at Markov blanket boundaries.
"""
struct WorldOperator{G<:MarkovGame}
    game::G
    seed::UInt64
end

function apply(W::WorldOperator, state_id::Int)
    game = W.game
    
    # Find all outgoing transitions from state
    outgoing = filter(parts(game, :Transition)) do t
        game[t, :src_state] == state_id
    end
    
    # Derangement check: none should self-loop
    @assert all(t -> game[t, :tgt_state] != state_id, outgoing) "Derangement violation"
    
    # Sample next state according to transition probabilities
    probs = [game[t, :trans_prob] for t in outgoing]
    next_trans = sample_weighted(outgoing, probs, W.seed)
    
    return game[next_trans, :tgt_state]
end

"""
Tropical distance for state path.
Optimal path = minimum sum of |trit(s_i) - trit(s_{i+1})|.
"""
function tropical_path_cost(game::MarkovGame, path::Vector{Int})
    cost = 0.0
    for i in 1:(length(path)-1)
        t_i = game[path[i], :state_trit]
        t_j = game[path[i+1], :state_trit]
        if t_i == t_j
            return Inf  # Fixed point in trit space
        end
        cost += abs(t_i - t_j)
    end
    return cost
end
```

## Integration with Open Games Engine

Compose with standard open games via lens structure:

```haskell
-- Markov game as Para/Optic with state dependency
data MarkovGame s a = MarkovGame {
    states      :: [s],
    transition  :: s -> a -> Distribution s,
    payoff      :: s -> a -> Player -> Rational,
    strategies  :: s -> Player -> [a],
    
    -- Derangement: transition s a ≠ δ_s (not concentrated on s)
    isDeranged  :: s -> a -> Bool
}

-- Compose with standard open game
markovToOpen :: MarkovGame s a -> OpenGame (s, History) (s, History) a Rational
markovToOpen mg = Game {
    play = \(s, h) -> bestResponse mg s h,
    coplay = \(s, h) a -> (transition mg s a, (s, a) : h),
    equilibrium = markovNash mg
}

-- Markov-Nash equilibrium: fixed point in strategy × belief space
markovNash :: MarkovGame s a -> (s, History) -> Bool
markovNash mg (s, h) = 
    let σ = optimalStrategy mg s h
        μ = beliefUpdate mg s h
    in isEquilibrium (σ, μ) && isDeranged mg s (σ s)
```

## Example: Three-State GF(3) Markov Game

```julia
# Create triadic Markov game
game = MarkovGame()

# Add states with GF(3) trits
add_parts!(game, :State, 3,
    state_name = ["World_A", "World_B", "World_C"],
    state_trit = [-1, 0, +1]  # MINUS, ERGODIC, PLUS
)

# Add players with roles
add_parts!(game, :Player, 3,
    player_name = ["Validator", "Coordinator", "Generator"],
    player_trit = [-1, 0, +1]
)

# Add transitions (derangement: no self-loops!)
#   A → B (Validator action)
#   B → C (Coordinator action)
#   C → A (Generator action)
add_parts!(game, :Transition, 3,
    src_state = [1, 2, 3],
    tgt_state = [2, 3, 1],  # Cyclic: σ = (1 2 3)
    trans_prob = [1.0, 1.0, 1.0]
)

# Verify constraints
@assert is_derangement_markov(game) "Must be derangement"
@assert verify_gf3_transitions(game) "Must conserve GF(3)"

# Tropical path cost for full cycle
cycle = [1, 2, 3, 1]
@assert tropical_path_cost(game, cycle) == 4.0  # |−1−0| + |0−1| + |1−(−1)| = 1+1+2
```

## GF(3) Triads

```
open-games (0) ⊗ markov-game-acset (-1) ⊗ gay-mcp (+1) = 0 ✓
acsets (0) ⊗ markov-game-acset (-1) ⊗ derangement-reflow (+1) = 0 ✓
temporal-coalgebra (-1) ⊗ markov-game-acset (-1) ⊗ free-monad-gen (+1) = -1 ✗ → needs +1
bisimulation-game (-1) ⊗ open-games (0) ⊗ markov-game-acset (-1) = -2 ✗ → imbalanced
sheaf-cohomology (-1) ⊗ open-games (0) ⊗ world-extractable-value (+1) = 0 ✓
```

## Commands

```bash
# Create Markov game from spec
just markov-game-create spec.yaml

# Verify derangement constraint
just markov-game-verify-derangement game.json

# Check GF(3) conservation
just markov-game-gf3 game.json

# Compute Markov-Nash equilibrium
just markov-game-nash game.json --strategy best-response

# Visualize state graph with Gay colors
just markov-game-viz game.json --seed 0x6B26D8
```

## References

- Ghani, Hedges, Winschel, Zahn. *Compositional Game Theory* (2016)
- Shapley, Lloyd. *Stochastic Games* (1953) — original Markov games paper
- Filar, Vrieze. *Competitive Markov Decision Processes* (1997)
- CyberCat Institute. *Open Games Tutorial* — line 29: "Markov games will be soon"
- plurigrid/asi derangement-reflow skill — σ(i)≠i constraint
- AlgebraicJulia/Catlab.jl — ACSet foundations

## Related Skills

- [open-games](../open-games/SKILL.md) — Compositional game theory (trit 0)
- [acsets](../acsets/SKILL.md) — Algebraic databases (trit 0)
- [derangement-reflow](../derangement-reflow/SKILL.md) — World operators (trit 0)
- [world-extractable-value](../world-extractable-value/SKILL.md) — WEV extraction (trit 0)
- [bisimulation-game](../bisimulation-game/SKILL.md) — Observational equivalence (trit -1)