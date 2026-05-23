---
name: speak-ci-integration
description: |
  Configure Speak CI/CD integration with GitHub Actions and automated testing.
  Use when setting up automated testing, configuring CI pipelines,
  or integrating Speak language learning tests into your build process.
  Trigger with phrases like "speak CI", "speak GitHub Actions",
  "speak automated tests", "CI speak".
allowed-tools: Read, Write, Edit, Bash(gh:*)
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Speak CI Integration

## Overview
Set up CI/CD pipelines for Speak language learning integrations with automated testing.

## Prerequisites
- GitHub repository with Actions enabled
- Speak test API key (sandbox environment)
- npm/pnpm project configured
- Test audio samples for speech recognition tests

## Instructions

### Step 1: Create GitHub Actions Workflow
Create `.github/workflows/speak-integration.yml`:

```yaml
name: Speak Integration Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  SPEAK_API_KEY: ${{ secrets.SPEAK_API_KEY }}
  SPEAK_APP_ID: ${{ secrets.SPEAK_APP_ID }}

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/lcov.info

  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    env:
      SPEAK_API_KEY: ${{ secrets.SPEAK_API_KEY_TEST }}
      SPEAK_APP_ID: ${{ secrets.SPEAK_APP_ID_TEST }}
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run Speak integration tests
        run: npm run test:integration
        timeout-minutes: 10

  speech-recognition-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    env:
      SPEAK_API_KEY: ${{ secrets.SPEAK_API_KEY_TEST }}
      SPEAK_APP_ID: ${{ secrets.SPEAK_APP_ID_TEST }}
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      # Download test audio files
      - name: Cache test audio
        uses: actions/cache@v4
        with:
          path: tests/fixtures/audio
          key: test-audio-v1

      - name: Download test audio fixtures
        run: npm run download:test-audio

      - name: Run speech recognition tests
        run: npm run test:speech
        timeout-minutes: 15
```

### Step 2: Configure Secrets
```bash
# Set Speak API credentials
gh secret set SPEAK_API_KEY --body "sk_test_***"
gh secret set SPEAK_APP_ID --body "app_***"

# Separate test environment credentials
gh secret set SPEAK_API_KEY_TEST --body "sk_sandbox_***"
gh secret set SPEAK_APP_ID_TEST --body "app_sandbox_***"
```

### Step 3: Create Integration Tests
```typescript
// tests/integration/speak.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { SpeakClient, AITutor, LessonSession } from '@speak/language-sdk';

describe('Speak Integration', () => {
  let client: SpeakClient;
  let session: LessonSession | null = null;

  beforeAll(() => {
    client = new SpeakClient({
      apiKey: process.env.SPEAK_API_KEY!,
      appId: process.env.SPEAK_APP_ID!,
      language: 'es',
    });
  });

  afterAll(async () => {
    if (session) {
      await session.end();
    }
  });

  it.skipIf(!process.env.SPEAK_API_KEY)('should verify API health', async () => {
    const health = await client.health.check();
    expect(health.healthy).toBe(true);
  });

  it.skipIf(!process.env.SPEAK_API_KEY)('should start a lesson session', async () => {
    const tutor = new AITutor(client, {
      targetLanguage: 'es',
      nativeLanguage: 'en',
      proficiencyLevel: 'beginner',
    });

    session = await tutor.startSession({
      topic: 'greetings',
      duration: 5,
    });

    expect(session.id).toBeDefined();
    expect(session.status).toBe('active');
  });

  it.skipIf(!process.env.SPEAK_API_KEY)('should get tutor prompt', async () => {
    if (!session) {
      throw new Error('Session not initialized');
    }

    const prompt = await session.getPrompt();
    expect(prompt.text).toBeTruthy();
    expect(prompt.audioUrl).toMatch(/^https:\/\//);
  });

  it.skipIf(!process.env.SPEAK_API_KEY)('should submit response and get feedback', async () => {
    if (!session) {
      throw new Error('Session not initialized');
    }

    const feedback = await session.submitResponse({
      text: 'Hola, me llamo Juan',
    });

    expect(feedback.pronunciationScore).toBeGreaterThanOrEqual(0);
    expect(feedback.pronunciationScore).toBeLessThanOrEqual(100);
    expect(feedback.message).toBeTruthy();
  });
});
```

### Step 4: Speech Recognition CI Tests
```typescript
// tests/integration/speech.test.ts
import { describe, it, expect, beforeAll } from 'vitest';
import { readFile } from 'fs/promises';
import { join } from 'path';
import { SpeakClient } from '@speak/language-sdk';

describe('Speech Recognition', () => {
  let client: SpeakClient;

  beforeAll(() => {
    client = new SpeakClient({
      apiKey: process.env.SPEAK_API_KEY!,
      appId: process.env.SPEAK_APP_ID!,
      language: 'es',
    });
  });

  it.skipIf(!process.env.SPEAK_API_KEY)('should recognize Spanish speech', async () => {
    // Load test audio file
    const audioPath = join(__dirname, '../fixtures/audio/hola-spanish.wav');
    const audioBuffer = await readFile(audioPath);

    const result = await client.speech.recognize(audioBuffer.buffer);

    expect(result.transcript.toLowerCase()).toContain('hola');
    expect(result.confidence).toBeGreaterThan(0.5);
  });

  it.skipIf(!process.env.SPEAK_API_KEY)('should score pronunciation', async () => {
    const audioPath = join(__dirname, '../fixtures/audio/buenos-dias.wav');
    const audioBuffer = await readFile(audioPath);

    const result = await client.speech.score({
      audio: audioBuffer.buffer,
      expectedText: 'Buenos días',
      detailed: true,
    });

    expect(result.overall).toBeGreaterThanOrEqual(0);
    expect(result.overall).toBeLessThanOrEqual(100);
    expect(result.words).toHaveLength(2);
  });
});
```

### Step 5: Add Test Audio Download Script
```typescript
// scripts/download-test-audio.ts
import { writeFile, mkdir } from 'fs/promises';
import { join } from 'path';

const FIXTURES_DIR = join(__dirname, '../tests/fixtures/audio');

const TEST_AUDIO_FILES = [
  {
    name: 'hola-spanish.wav',
    url: 'https://example.com/test-audio/hola-spanish.wav',
  },
  {
    name: 'buenos-dias.wav',
    url: 'https://example.com/test-audio/buenos-dias.wav',
  },
  // Add more test files as needed
];

async function downloadTestAudio() {
  await mkdir(FIXTURES_DIR, { recursive: true });

  for (const file of TEST_AUDIO_FILES) {
    const response = await fetch(file.url);
    const buffer = await response.arrayBuffer();
    await writeFile(join(FIXTURES_DIR, file.name), Buffer.from(buffer));
    console.log(`Downloaded: ${file.name}`);
  }
}

downloadTestAudio();
```

## Output
- Automated test pipeline
- PR checks configured
- Coverage reports uploaded
- Speech recognition tests included
- Release workflow ready

## Error Handling
| Issue | Cause | Solution |
|-------|-------|----------|
| Secret not found | Missing configuration | Add secret via `gh secret set` |
| Tests timeout | Audio processing slow | Increase timeout or mock |
| Auth failures | Invalid key | Check secret value |
| Audio fixture missing | Not downloaded | Run download script |
| Flaky speech tests | Audio quality | Use high-quality fixtures |

## Examples

### Release Workflow
```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-latest
    env:
      SPEAK_API_KEY: ${{ secrets.SPEAK_API_KEY_PROD }}
      SPEAK_APP_ID: ${{ secrets.SPEAK_APP_ID_PROD }}
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'

      - run: npm ci
      - run: npm test
      - run: npm run test:integration

      - name: Verify Speak production readiness
        run: |
          npm run speak:health-check
          npm run speak:smoke-test

      - run: npm run build
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Branch Protection
```yaml
# Required status checks
required_status_checks:
  strict: true
  contexts:
    - "unit-tests"
    - "integration-tests"
    - "speech-recognition-tests"
```

### Mock-Based Fast Tests
```typescript
// tests/unit/speak-mocked.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mockSpeakClient } from '../mocks/speak-mock';

vi.mock('@speak/language-sdk', () => ({
  SpeakClient: vi.fn().mockImplementation(() => mockSpeakClient),
}));

describe('Speak Client (Mocked)', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should initialize client', () => {
    // Fast test without network
  });
});
```

## Resources
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Speak CI Guide](https://developer.speak.com/docs/ci)
- [Vitest CI Configuration](https://vitest.dev/guide/ci)

## Next Steps
For deployment patterns, see `speak-deploy-integration`.
