---
name: conversational-goal-discovery
description: Chat-based goal classification (habit/distance/speed/race) with constraint clarification. Use during onboarding or when user wants to update their running goals through conversation with weekly commitment discovery.
metadata:
  short-description: Chat-based goal classification with commitments and starter plan suggestions.
  agent: cursor
---

## When Cursor should use this skill
- Early chat sessions or onboarding when the user's goal is ambiguous
- When the user asks for help choosing a plan or habit
- When user wants to clarify or update their running goals
- When implementing conversational onboarding features

## Invocation guidance
1. Provide the last N `ConversationTurn` entries and any partial onboarding answers.
2. Classify goal (`habit` | `distance` | `speed` | `race`) with confidence and blockers.
3. Return a `CoachMessage` summary plus structured `GoalDiscoveryResult`.
4. Ask clarifying questions if confidence < 0.7.
5. Suggest weekly commitment (3-4 runs for beginners, 4-5 for intermediate, 5-6 for advanced).

## Input schema (JSON)
```ts
{
  "conversation": ConversationTurn[],
  "profile": UserProfile,
  "partialOnboarding"?: Record<string, unknown>
}
```

## Output schema (JSON)
```ts
{
  "goalDiscovery": {
    "goal": Goal,
    "confidence": number,
    "blockers": string[],
    "weeklyCommitment": number,
    "preferredDays"?: string[],
    "starterPlanId"?: string,
    "summaryCard": string,
    "safetyFlags"?: SafetyFlag[]
  },
  "coachMessage": CoachMessage
}
```

## Integration points
- **Chat API**: `v0/app/api/chat/route.ts` - Conversational interface
- **Prompt context**: 
  - `v0/lib/conversationStorage.ts` - Conversation history
  - `v0/lib/onboardingPromptBuilder.ts` - Onboarding prompts
- **Handoff**: trigger plan generation via `v0/app/api/generate-plan/route.ts` when confidence ≥0.7
- **UI**: Chat screen and onboarding wizard
- **Database**: Store conversation turns in `chat_messages` table

## Safety & guardrails
- Avoid medical advice; if user mentions pain/injury, advise pause and professional consult.
- Keep responses concise (<120 words) and supportive.
- Emit `SafetyFlag` on harmful intents or ambiguous data.
- If user has injury history, recommend starting conservatively.
- Never promise specific performance outcomes or weight loss guarantees.

## Conversation flow patterns

### Goal discovery sequence
1. **Initial question**: "What brings you to running?" or "What are you hoping to achieve?"
2. **Clarify constraints**: "How many days per week can you commit?" "Any time restrictions?"
3. **Assess experience**: "What's your recent running history?"
4. **Confirm goal**: "So it sounds like [goal]. Is that right?"
5. **Suggest next step**: "Let me create a plan for you" or "Tell me more about..."

### Goal types and indicators
- **Habit**: "consistency", "build routine", "just want to run"
- **Distance**: "5K", "10K", "half marathon", "marathon", specific distance target
- **Speed**: "get faster", "PR", "improve time", pace goals
- **Race**: mentions specific race, date, or event

## Telemetry
- Emit `ai_skill_invoked` with:
  - `goal` (classified)
  - `confidence`
  - `turns_count` (conversation length)
  - `latency_ms`
- Emit `ai_user_feedback` when user responds to suggestions

## Common edge cases
- **Multiple goals**: Ask user to prioritize primary goal
- **Vague responses**: Ask specific follow-up questions
- **Unrealistic goals**: Gently adjust expectations with rationale
- **Injury mentions**: Prioritize recovery, recommend professional consultation
- **Low confidence**: Continue conversation, don't force goal classification

## Testing considerations
- Test with various conversation patterns (short, long, meandering)
- Verify confidence scoring accuracy
- Test with ambiguous or conflicting statements
- Validate SafetyFlag emission for injury mentions
- Test handoff to plan generation at confidence threshold
