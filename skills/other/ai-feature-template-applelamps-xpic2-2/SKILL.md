---
name: ai-feature-template
description: Create new AI-powered features using xAI Grok. Use when user mentions "new AI feature", "add Grok", "create prompt", "AI analysis", or "generate with AI".
---

# Creating AI Features with xAI Grok

This project uses xAI's Grok model for AI-powered features with X (Twitter) search capabilities.

## Instructions

1. **Create API route** at `app/api/<feature-name>/route.ts`

2. **Use this template for Grok with X search**:
```typescript
import { NextRequest, NextResponse } from 'next/server';

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

// Define your AI persona and instructions
const systemPrompt = `You are [PERSONA NAME], a [ROLE DESCRIPTION].

Your task is to [WHAT TO DO] based on the X account data.

Output Requirements:
- [REQUIREMENT 1]
- [REQUIREMENT 2]
- [FORMAT INSTRUCTIONS]

CRITICAL: Output ONLY the result. No preamble, no explanations.`;

export async function OPTIONS() {
  return NextResponse.json(null, { headers: corsHeaders });
}

export async function POST(req: NextRequest) {
  try {
    const { handle } = await req.json();

    const HANDLE_REGEX = /^[a-zA-Z0-9_]{1,15}$/;
    if (!handle || !HANDLE_REGEX.test(handle)) {
      return NextResponse.json(
        { error: 'Invalid X handle format.' },
        { status: 400, headers: corsHeaders }
      );
    }

    const xaiApiKey = process.env.XAI_API_KEY;
    if (!xaiApiKey) {
      return NextResponse.json(
        { error: 'XAI_API_KEY not configured' },
        { status: 500, headers: corsHeaders }
      );
    }

    // Build 6-month date range for X search
    const today = new Date();
    const toDate = today.toISOString().split('T')[0];
    const sixMonthsAgo = new Date(today.getTime() - 182 * 24 * 60 * 60 * 1000);
    const fromDate = sixMonthsAgo.toISOString().split('T')[0];

    const response = await fetch('https://api.x.ai/v1/chat/completions', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${xaiApiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        // DO NOT CHANGE - grok-4-1-fast required for X search
        model: 'grok-4-1-fast',
        messages: [
          { role: 'system', content: systemPrompt },
          {
            role: 'user',
            content: `Analyze @${handle}'s posts and [SPECIFIC INSTRUCTION].`,
          },
        ],
        search_parameters: {
          mode: 'on',
          sources: [{ type: 'x' }],
          from_date: fromDate,
          to_date: toDate,
        },
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('xAI API error:', response.status, errorText);
      return NextResponse.json(
        { error: `xAI API error: ${response.status}` },
        { status: response.status, headers: corsHeaders }
      );
    }

    const data = await response.json();
    const result = data.choices?.[0]?.message?.content;

    if (!result) {
      return NextResponse.json(
        { error: 'No result generated' },
        { status: 500, headers: corsHeaders }
      );
    }

    return NextResponse.json({ result }, { headers: corsHeaders });
  } catch (error) {
    console.error('Error:', error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500, headers: corsHeaders }
    );
  }
}
```

3. **Add frontend handler** in `app/page.tsx`:
```typescript
const handleNewFeature = async () => {
  setIsLoading(true);
  try {
    const response = await fetch('/api/feature-name', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ handle: normalizedHandle }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error);
    setResult(data.result);
    toast.success('Generated!');
  } catch (err) {
    toast.error('Failed');
  } finally {
    setIsLoading(false);
  }
};
```

## Existing AI Prompts (Reference)

| Feature | Persona | Output |
|---------|---------|--------|
| analyze-account | Art Director | 4-6 sentence image prompt |
| roast-account | Dr. Burn Notice | 300-400 word therapy letter |
| fbi-profile | FBI Analyst | Classified behavioral report |

## Prompt Best Practices

- Define clear persona with voice/tone
- Specify exact output format and length
- Include "Output ONLY..." to prevent preamble
- Add examples for complex outputs
- Use "CRITICAL RULES" section for must-follow instructions

## Examples

- "Create a horoscope generator" → New route with astrologer persona
- "Add personality summary" → New route with psychologist persona

## Guardrails

- Always use `grok-4-1-fast` model for X search capability
- Include 6-month date range for search parameters
- Never log or expose API keys
- Handle API errors gracefully with user-friendly messages
- Test prompts for safety/appropriateness before deploying
