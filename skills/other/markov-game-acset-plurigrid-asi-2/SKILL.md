# markov-game-acset

Markov games as ACSets with derangement constraints on state transitions.

## Overview

Fills the "Markov games will be soon" gap from [open-games-engine Tutorial](https://github.com/CyberCat-Institute/open-game-engine).

**Origin**: PR #34 (closed, consolidated into main via #42)

## ACSet Schema

```julia
@present SchMarkovGame(FreeSchema) begin
    State::Ob
    Action::Ob
    Player::Ob
    Transition::Ob
    
    src_state::Hom(Transition, State)
    tgt_state::Hom(Transition, State)
    action::Hom(Transition, Action)
    player::Hom(Transition, Player)
    
    probability::Attr(Transition, Float64)
    reward::Attr(Transition, Float64)
end
```

## Derangement Constraint

**Key innovation**: No state can transition to itself.

```julia
# σ(s) ≠ s for all states s
is_derangement(mg::MarkovGame) = all(
    t -> src_state(mg, t) != tgt_state(mg, t),
    transitions(mg)
)
```

This ensures information MUST reflow between states.

## Stochastic Game Dynamics

```julia
function step!(game::MarkovGame, state::State, actions::Dict{Player,Action})
    valid_transitions = filter(transitions(game)) do t
        src_state(game, t) == state &&
        all(p -> action(game, t) == actions[p], players(game))
    end
    
    probs = [probability(game, t) for t in valid_transitions]
    chosen = sample(valid_transitions, Weights(probs))
    
    rewards = Dict(p => reward(game, chosen) for p in players(game))
    next_state = tgt_state(game, chosen)
    
    (next_state, rewards)
end
```

## Connection to Open Games

```
MarkovGame ─────► OpenGame
    │                │
    │ ACSet          │ Para/Optic
    │                │
    ▼                ▼
Transition ────► Play/CoPlay
```

## GF(3) Trit

**Trit: -1** (MINUS/VALIDATOR) - State validation

## Related Skills

- `open-games` - Compositional game theory
- `derangement-reflow` - World operators
- `acsets-algebraic-databases` - ACSet foundations
