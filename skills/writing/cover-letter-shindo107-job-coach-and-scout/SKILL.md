---
name: cover-letter
description: Generate a voice-matched cover letter for a specific job. Analyzes your writing samples and creates a personalized letter that sounds like you.
argument-hint: [company-name]
---

# Cover Letter Workflow

**Load and execute:** `workflows/cover-letter/workflow.md`

Read the entire workflow file and execute it step by step. This workflow:

1. Checks for existing voice profile (`profile/voice_profile.json`)
2. If no profile exists, analyzes writing samples to create one
3. Loads your Resume Corpus, job posting, and tailored resume
4. Generates a draft cover letter matching your authentic voice
5. Conducts iterative refinement based on your feedback
6. Saves the final letter to `applications/cover_letters/`

**Voice Profile Integration:**
- If `/init` already created `profile/voice_profile.json` from your writing samples, this workflow uses it directly
- If no voice profile exists, the workflow analyzes `profile/writing_samples/*` and creates the profile
- The voice profile captures tone, sentence structure, vocabulary, and signature phrases

Follow all steps exactly as written. Focus on capturing the user's authentic voice while highlighting what hiring managers need to see.

$ARGUMENTS
