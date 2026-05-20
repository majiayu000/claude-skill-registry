---
name: rive
description: >-
  Build interactive animations with Rive — load .riv files, control state
  machines, respond to user input, and embed runtime animations in web and
  mobile apps. Use when tasks involve interactive UI animations, character
  animations with state logic, animated icons with hover/click states, or
  game-like interactions in production apps.
license: Apache-2.0
compatibility: "Browser, React, React Native, Flutter, iOS, Android"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: design
  tags: ["rive", "animation", "state-machine", "interactive", "motion"]
---

# Rive

Interactive animation runtime. Animations are designed in the Rive editor and controlled via state machines at runtime.

## Setup

```bash
# Install the Rive web runtime and React bindings.
npm install @rive-app/canvas
npm install @rive-app/react-canvas
```

## Basic Web Playback

```typescript
// src/rive/player.ts — Load a .riv file and play it on a canvas element.
// Rive files contain artboards, animations, and state machines.
import { Rive } from "@rive-app/canvas";

export function createRivePlayer(
  canvas: HTMLCanvasElement,
  src: string,
  stateMachine: string
): Rive {
  return new Rive({
    src,
    canvas,
    stateMachines: stateMachine,
    autoplay: true,
    onLoad: () => {
      console.log("Rive file loaded");
    },
    onStateChange: (event) => {
      console.log("State changed:", event.data);
    },
  });
}
```

## State Machine Inputs

```typescript
// src/rive/inputs.ts — Read and write state machine inputs to drive animation
// transitions. Inputs are booleans, numbers, or triggers defined in Rive editor.
import { Rive, StateMachineInput } from "@rive-app/canvas";

export function getInputs(rive: Rive, stateMachineName: string) {
  const inputs = rive.stateMachineInputs(stateMachineName) || [];
  return Object.fromEntries(inputs.map((i) => [i.name, i]));
}

export function setBoolean(input: StateMachineInput, value: boolean) {
  input.value = value;
}

export function setNumber(input: StateMachineInput, value: number) {
  input.value = value;
}

export function fireTrigger(input: StateMachineInput) {
  input.fire();
}
```

## React Integration

```tsx
// src/components/RiveAnimation.tsx — React component for Rive animations.
// useRive handles lifecycle, useStateMachineInput provides input control.
import { useRive, useStateMachineInput } from "@rive-app/react-canvas";

interface Props {
  src: string;
  stateMachine: string;
  className?: string;
}

export function RiveAnimation({ src, stateMachine, className }: Props) {
  const { rive, RiveComponent } = useRive({
    src,
    stateMachines: stateMachine,
    autoplay: true,
  });

  // Access a boolean input named "isHovered"
  const hoverInput = useStateMachineInput(rive, stateMachine, "isHovered");

  return (
    <RiveComponent
      className={className}
      onMouseEnter={() => hoverInput && (hoverInput.value = true)}
      onMouseLeave={() => hoverInput && (hoverInput.value = false)}
    />
  );
}
```

## Interactive Button Example

```tsx
// src/components/RiveButton.tsx — Animated button that uses a Rive state machine
// with pressed/hover/idle states and a trigger for click feedback.
import { useRive, useStateMachineInput } from "@rive-app/react-canvas";

export function RiveButton({ src, onClick }: { src: string; onClick: () => void }) {
  const { rive, RiveComponent } = useRive({
    src,
    stateMachines: "button_state",
    autoplay: true,
  });

  const isHovered = useStateMachineInput(rive, "button_state", "isHovered");
  const isPressed = useStateMachineInput(rive, "button_state", "isPressed");

  return (
    <RiveComponent
      style={{ width: 200, height: 60, cursor: "pointer" }}
      onMouseEnter={() => isHovered && (isHovered.value = true)}
      onMouseLeave={() => {
        if (isHovered) isHovered.value = false;
        if (isPressed) isPressed.value = false;
      }}
      onMouseDown={() => isPressed && (isPressed.value = true)}
      onMouseUp={() => {
        if (isPressed) isPressed.value = false;
        onClick();
      }}
    />
  );
}
```

## Listening to Rive Events

```typescript
// src/rive/events.ts — Subscribe to Rive events emitted by state machine
// transitions, useful for triggering sound effects or UI updates.
import { Rive, EventType } from "@rive-app/canvas";

export function listenToEvents(rive: Rive) {
  rive.on(EventType.StateChange, (event) => {
    console.log("States:", event.data);
  });

  rive.on(EventType.RiveEvent, (event) => {
    const { name, properties } = event.data as any;
    console.log(`Rive event: ${name}`, properties);
  });
}
```
