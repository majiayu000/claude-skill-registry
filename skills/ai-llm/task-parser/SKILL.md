---
name: AI Task Parser
description: Parse natural language task input and extract structured data (title, due date, priority, category) using Google Gemini AI
version: 1.0.0
tags: [ai, nlp, task-parsing, gemini]
---

# AI Task Parser Skill

## Purpose

This skill enables natural language task creation. Users can type "Buy groceries tomorrow at 5pm" and the AI will automatically extract:
- Title: "Buy groceries"
- Due date: Tomorrow at 5pm
- Priority: Based on keywords
- Category: Based on context

## How It Works

### 1. User Input
User types natural language in task input field

### 2. AI Processing
Send to Gemini API with structured prompt

### 3. Structured Output
Receive JSON with parsed fields

### 4. Auto-fill Form
Populate task form with extracted data

## Implementation

### Backend Endpoint

```python
from fastapi import APIRouter, HTTPException
import google.generativeai as genai
import json
import os
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/ai", tags=["ai"])

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@router.post("/parse-task")
async def parse_task(input_text: str):
    """Parse natural language task input"""
    
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    You are a task parsing assistant. Parse the following task input and extract structured data.
    
    Input: "{input_text}"
    
    Extract and return ONLY a JSON object with these fields:
    - title: The main task description (string)
    - due_date: ISO 8601 datetime or null (string|null)
    - priority: "low", "medium", or "high" (string)
    - category: Best matching category from: Work, Personal, Learning, Others (string)
    - tags: Comma-separated relevant tags (string)
    
    Rules:
    - If no time specified, assume end of day
    - "tomorrow" = next day
    - "next week" = 7 days from now
    - Infer priority from urgency words (urgent=high, soon=medium, someday=low)
    - Return ONLY valid JSON, no markdown or explanation
    
    Example input: "Buy milk tomorrow at 5pm"
    Example output: {{"title": "Buy milk", "due_date": "2025-12-19T17:00:00", "priority": "medium", "category": "Personal", "tags": "shopping, groceries"}}
    """
    
    try:
        response = model.generate_content(prompt)
        parsed_data = json.loads(response.text.strip())
        
        return {
            "success": True,
            "data": parsed_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI parsing failed: {str(e)}")
```

### Frontend Component

```typescript
// components/SmartTaskInput.tsx
import { useState } from 'react';
import { Sparkles } from 'lucide-react';

interface SmartTaskInputProps {
  onParse: (data: any) => void;
}

export const SmartTaskInput = ({ onParse }: SmartTaskInputProps) => {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleParse = async () => {
    if (!input.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch('/api/ai/parse-task', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input_text: input })
      });
      
      const result = await response.json();
      if (result.success) {
        onParse(result.data);
        setInput('');
      }
    } catch (error) {
      console.error('AI parsing failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="smart-input-container">
      <div className="relative">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleParse()}
          placeholder="Try: 'Buy groceries tomorrow at 5pm' ✨"
          className="w-full px-4 py-3 pr-12 bg-slate-800 border border-slate-700 rounded-lg text-slate-100"
        />
        <button
          onClick={handleParse}
          disabled={loading || !input.trim()}
          className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-purple-400 hover:text-purple-300"
        >
          {loading ? (
            <div className="animate-spin">⏳</div>
          ) : (
            <Sparkles className="w-5 h-5" />
          )}
        </button>
      </div>
      <p className="text-xs text-slate-400 mt-1">
        💡 Use natural language - AI will parse it for you!
      </p>
    </div>
  );
};
```

## Usage

1. Add Gemini API key to `.env`:
```
GEMINI_API_KEY=your_api_key_here
```

2. Install dependencies:
```bash
pip install google-generativeai
```

3. Import and use in TaskForm:
```typescript
import { SmartTaskInput } from './SmartTaskInput';

<SmartTaskInput
  onParse={(data) => {
    setFormData({
      title: data.title,
      due_date: data.due_date,
      priority: data.priority,
      category: data.category,
      tags: data.tags
    });
  }}
/>
```

## Examples

| Input | Parsed Output |
|-------|--------------|
| "Buy milk tomorrow" | title: "Buy milk", due_date: tomorrow EOD, priority: medium |
| "Urgent: Submit report by Friday 3pm" | title: "Submit report", due_date: Friday 3pm, priority: high |
| "Learn React next week" | title: "Learn React", due_date: +7 days, priority: low, category: Learning |
| "Call mom tonight at 8" | title: "Call mom", due_date: today 8pm, priority: medium, category: Personal |

## Benefits

- ⚡ **Faster task creation** - No manual field filling
- 🧠 **Smart parsing** - AI understands context
- 🎯 **Accurate** - Gemini Pro's language understanding
- ✨ **Delightful UX** - Magic-like experience

## API Cost

- Gemini Pro: Free tier (60 requests/minute)
- Cost-effective for hackathon/demo
- Can upgrade to paid tier for production
