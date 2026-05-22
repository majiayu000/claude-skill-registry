---
name: lorcana-test-generation
description: Generate basic happy-path tests for Lorcana card abilities. Tests verify ability behavior only - NO property validation tests. Use when implementing or updating card tests. Effects are tested separately in the engine.
---

# Lorcana Test Generation

Generate test files for Lorcana card definitions using `LorcanaTestEngine`.

## When to Use

- User requests to generate tests for a card
- After card migration is complete
- User wants to update existing tests
- User asks to test a specific ability

## Process

### Input

**Card File**: Path to card definition (e.g., `src/cards/001/characters/007-heihei-boat-snack.ts`)

### Workflow

1. **Read Card Definition**
   - Load card file from `src/cards/001/`
   - Extract abilities array

2. **Identify Ability Types**
   - Keyword: Simple presence check
   - Triggered: When/whenever triggers
   - Activated: Cost → effect abilities
   - Static: Continuous effects

3. **Generate Tests (Interactive)**
   - For each ability: show template, ask for confirmation
   - User can: generate, skip, or customize
   - Compile confirmed tests into single file

4. **Write Test File**
   - Create at same location as card: `{file}.test.ts`
   - Use `LorcanaTestEngine` and `PLAYER_ONE` from `@tcg/lorcana/testing`

## Test Templates

### Keyword Test
```typescript
it("has [Keyword] keyword", () => {
  const testEngine = new LorcanaTestEngine({ play: [cardUnderTest] });
  const card = testEngine.getCardModel(cardUnderTest);
  expect(card.hasKeyword()).toBe(true);
});
```

### Triggered Test (When You Play)
```typescript
it("triggers effect when played", () => {
  const testEngine = new LorcanaTestEngine({ hand: [cardUnderTest] });
  const before = testEngine.getZone("hand", PLAYER_ONE).length;

  testEngine.playCard(cardUnderTest.id);

  const after = testEngine.getZone("hand", PLAYER_ONE).length;
  expect(after).toBe(before + 1); // Drew 1, played 1
});
```

### Activated Test
```typescript
it("activates ability when cost is paid", () => {
  const testEngine = new LorcanaTestEngine({ play: [cardUnderTest] });

  // Exert to activate
  testEngine.quest(cardUnderTest.id);

  const state = testEngine.getCardMeta(cardUnderTest.id);
  expect(state?.state).toBe("exerted");
});
```

## What NOT to Test

**Do NOT test property values** (cost, strength, willpower, lore, cardNumber, etc.) - these are data, not behavior.

## Output Format

```
Test Generation Complete
========================
Card: [Name] - [Version]
File: src/cards/001/characters/xxx-name.test.ts

Tests Generated: X
- Keywords: Y
- Triggered: Z
- Activated: W
- Skipped: V

Run Tests: bun test src/cards/001/characters/xxx-name.test.ts
```

## Example Session

```
> write-card-test 007-heihei-boat-snack

Reading card: src/cards/001/characters/007-heihei-boat-snack.ts
Found 1 ability

[Ability 1/1: Keyword - Support]
Test: hasSupport() verification

Generate test? (yes/no/customize) yes

✓ Test file created
File: src/cards/001/characters/007-heihei-boat-snack.test.ts

Run: bun test src/cards/001/characters/007-heihei-boat-snack.test.ts
```

## Completion Report

```
Test Generation: Complete
========================
File: src/cards/001/characters/xxx-name.test.ts
Tests: X generated

Next Steps:
- Run: bun test src/cards/001/characters/xxx-name.test.ts
- Verify all tests pass
- Commit changes
```
