---
name: ai-coaching
description: Multi-turn conversational AI for intent extraction, clarification, and generation readiness detection. Guides users through articulating creative intent with structured parameter extraction.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: ai
  time: 8h
  source: drift-masterguide
---

# AI Coaching System

Multi-turn conversational AI that guides users through articulating intent.

## When to Use This Skill

- Building AI assistants that need to understand complex user intent
- Need structured parameter extraction from conversation
- Want to detect when user intent is ready for action
- Implementing clarification flows for ambiguous input

## Core Concepts

The coach helps users articulate WHAT they want, not HOW to achieve it. It extracts structured intent through conversation, tracks ambiguities, and signals readiness only after user confirmation.

```
User Input → Intent Parser → Schema Update → Readiness Check → Coach Response
```

## Implementation

### Python

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
import re


class ReadinessState(str, Enum):
    NOT_READY = "not_ready"
    NEEDS_CLARIFICATION = "needs_clarification"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    READY = "ready"


@dataclass
class AmbiguousAnnotation:
    text: str
    possible_intents: List[str]
    resolved: bool = False
    resolution: Optional[str] = None


@dataclass
class CreativeIntentSchema:
    """Structured representation of user's creative intent."""
    asset_type: str
    mood: Optional[str] = None
    scene_elements: List[Dict] = field(default_factory=list)
    display_texts: List[Dict] = field(default_factory=list)
    ambiguous_annotations: List[AmbiguousAnnotation] = field(default_factory=list)
    turn_count: int = 0
    user_confirmed_vision: bool = False
    last_coach_summary: Optional[str] = None

    def get_readiness(self) -> ReadinessState:
        if self.turn_count == 0:
            return ReadinessState.NOT_READY
        
        unresolved = [a for a in self.ambiguous_annotations if not a.resolved]
        if unresolved:
            return ReadinessState.NEEDS_CLARIFICATION
        
        if not self.user_confirmed_vision:
            return ReadinessState.AWAITING_CONFIRMATION
        
        return ReadinessState.READY

    def is_ready(self) -> bool:
        return self.get_readiness() == ReadinessState.READY

    def get_clarification_questions(self) -> List[str]:
        return [
            f'Should "{a.text}" be rendered as an image or displayed as text?'
            for a in self.ambiguous_annotations if not a.resolved
        ]


class IntentParser:
    """Parses messages to extract and update intent."""
    
    CONFIRMATION_PATTERNS = [
        r"\b(yes|yeah|sure|ok|perfect|great|looks good|exactly)\b",
        r"\b(let's go|do it|generate|create it)\b",
    ]

    def parse_initial_request(
        self,
        description: str,
        asset_type: str,
        mood: Optional[str] = None,
    ) -> CreativeIntentSchema:
        schema = CreativeIntentSchema(asset_type=asset_type, mood=mood)
        
        # Extract quoted text as display text
        quoted = re.findall(r'"([^"]+)"', description)
        for text in quoted:
            schema.display_texts.append({"text": text})
        
        if description and not quoted:
            schema.scene_elements.append({"description": description})
        
        return schema

    def parse_user_message(
        self,
        message: str,
        schema: CreativeIntentSchema,
    ) -> tuple[CreativeIntentSchema, bool]:
        schema.turn_count += 1
        
        is_confirmation = self._is_confirmation(message)
        if is_confirmation:
            schema.user_confirmed_vision = True
        
        # Resolve ambiguities from user response
        message_lower = message.lower()
        for amb in schema.ambiguous_annotations:
            if not amb.resolved:
                if "text" in message_lower or "display" in message_lower:
                    amb.resolved = True
                    amb.resolution = "display_text"
                elif "render" in message_lower or "image" in message_lower:
                    amb.resolved = True
                    amb.resolution = "render"
        
        return schema, is_confirmation

    def _is_confirmation(self, message: str) -> bool:
        message_lower = message.lower().strip()
        return any(re.search(p, message_lower) for p in self.CONFIRMATION_PATTERNS)


@dataclass
class StreamChunk:
    type: str  # "token", "intent_ready", "done", "error"
    content: str = ""
    metadata: Optional[Dict[str, Any]] = None


class CoachService:
    """Orchestrates coaching conversations."""
    
    MAX_TURNS = 10

    def __init__(self, llm_client, session_store):
        self.llm = llm_client
        self.sessions = session_store
        self.parser = IntentParser()

    async def start_session(
        self,
        user_id: str,
        asset_type: str,
        description: str,
        mood: Optional[str] = None,
    ):
        # Initialize intent schema
        schema = self.parser.parse_initial_request(description, asset_type, mood)
        
        # Build system prompt
        system_prompt = f"""You are a creative coach helping users design {asset_type} assets.

RULES:
1. Ask clarifying questions to understand their vision
2. Summarize what you understand after each exchange
3. When vision is clear, say [INTENT_READY]
4. Never say [INTENT_READY] on first turn
5. Focus on WHAT they want, not HOW"""

        first_message = f'User wants to create a {asset_type}. Description: "{description}"'
        
        # Stream LLM response
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": first_message},
        ]
        
        full_response = ""
        async for token in self.llm.stream_chat(messages):
            full_response += token
            yield StreamChunk(type="token", content=token)
        
        # First turn is NEVER ready
        yield StreamChunk(
            type="intent_ready",
            metadata={
                "is_ready": False,
                "readiness_state": ReadinessState.NOT_READY.value,
                "clarification_questions": schema.get_clarification_questions(),
            },
        )
        
        yield StreamChunk(type="done", metadata={"turns_remaining": self.MAX_TURNS - 1})

    async def continue_chat(
        self,
        session_id: str,
        message: str,
        schema: CreativeIntentSchema,
    ):
        if schema.turn_count >= self.MAX_TURNS:
            yield StreamChunk(type="error", content="Turn limit reached")
            return
        
        schema, is_confirmation = self.parser.parse_user_message(message, schema)
        
        # Stream response...
        full_response = ""
        async for token in self.llm.stream_chat([...]):
            full_response += token
            yield StreamChunk(type="token", content=token)
        
        readiness = schema.get_readiness()
        
        yield StreamChunk(
            type="intent_ready",
            metadata={
                "is_ready": schema.is_ready(),
                "readiness_state": readiness.value,
                "is_confirmation": is_confirmation,
            },
        )
```

### TypeScript

```typescript
enum ReadinessState {
  NOT_READY = 'not_ready',
  NEEDS_CLARIFICATION = 'needs_clarification',
  AWAITING_CONFIRMATION = 'awaiting_confirmation',
  READY = 'ready',
}

interface AmbiguousAnnotation {
  text: string;
  possibleIntents: string[];
  resolved: boolean;
  resolution?: string;
}

interface CreativeIntentSchema {
  assetType: string;
  mood?: string;
  sceneElements: Array<{ description: string }>;
  displayTexts: Array<{ text: string }>;
  ambiguousAnnotations: AmbiguousAnnotation[];
  turnCount: number;
  userConfirmedVision: boolean;
}

function getReadiness(schema: CreativeIntentSchema): ReadinessState {
  if (schema.turnCount === 0) return ReadinessState.NOT_READY;
  
  const unresolved = schema.ambiguousAnnotations.filter(a => !a.resolved);
  if (unresolved.length > 0) return ReadinessState.NEEDS_CLARIFICATION;
  
  if (!schema.userConfirmedVision) return ReadinessState.AWAITING_CONFIRMATION;
  
  return ReadinessState.READY;
}

const CONFIRMATION_PATTERNS = [
  /\b(yes|yeah|sure|ok|perfect|great|looks good)\b/i,
  /\b(let's go|do it|generate|create it)\b/i,
];

function isConfirmation(message: string): boolean {
  return CONFIRMATION_PATTERNS.some(p => p.test(message));
}
```

## Usage Examples

```python
# Start coaching session
async for chunk in coach.start_session(
    user_id="user_123",
    asset_type="thumbnail",
    description="gaming video thumbnail",
    mood="energetic",
):
    if chunk.type == "token":
        print(chunk.content, end="")
    elif chunk.type == "intent_ready":
        if chunk.metadata["is_ready"]:
            # Proceed to generation
            pass
        else:
            # Show clarification questions
            for q in chunk.metadata.get("clarification_questions", []):
                print(f"Coach asks: {q}")
```

## Best Practices

1. Never mark intent as ready on first turn - always ask questions
2. Require explicit user confirmation before proceeding
3. Track and resolve ambiguities explicitly
4. Summarize understanding after each exchange
5. Limit total turns to prevent infinite conversations
6. Stream responses for better UX

## Common Mistakes

- Auto-confirming intent without user acknowledgment
- Not tracking ambiguous terms that need clarification
- Allowing ready state on first turn
- Not persisting session state for reconnections
- Forgetting turn limits

## Related Patterns

- prompt-engine (prompt construction)
- ai-generation-client (generation execution)
- sse-streaming (response streaming)
