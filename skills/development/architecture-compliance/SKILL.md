---
name: architecture-compliance
description: Ensure code follows strict layer boundaries and dependency rules
version: 1.0.0
author: Saberloop Project
usage: |
  Use this skill for architecture-related tasks:
  - Validating new module placement against layer boundaries
  - Checking dependency rule compliance
  - Generating dependency graphs for visualization
  - Identifying and fixing circular dependencies
  - Architectural refactoring to improve layer separation
  
  Examples:
  "Validate new service architecture using the architecture-compliance skill"
  "Check dependency rules for new component using the architecture-compliance skill"
  "Fix architecture violations using the architecture-compliance skill"

# Architecture Compliance Validation Skill

## Overview

This skill ensures code follows Saberloop's strict layer boundaries and dependency rules as enforced by dependency-cruiser, maintaining clean architecture and preventing technical debt accumulation.

## Architecture Layers

### Layer Definitions

| Layer | Directory | Purpose | Allowed Dependencies |
|--------|------------|---------|-------------------|
| Views | `src/views/` | UI components, Services, Core utilities, State |
| Components | `src/components/` | Core utilities, State |
| Services | `src/services/` | API layer, Database, Core utilities |
| API | `src/api/` | Core utilities |
| Core | `src/core/` | External libraries only |

### Dependency Flow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Views      │───▶│   Components   │───▶│    Services     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         │                        │                        ▼
         │                        │                ┌─────────────────┐
         │                        │                │       API       │
         │                        ▼                └─────────────────┘
         │                ┌─────────────────┐                │
         │                │   Services     │◀───────────────┤
         ▼                └─────────────────┘                │
┌─────────────────┐                        │                │
│    Core       │◀───────────────────────┤                ▼
└─────────────────┘                        │        ┌─────────────────┐
                                          │        │   Core Utils    │
                                          │        └─────────────────┘
                                          ▼
                                 ┌─────────────────┐
                                 │ External Libs  │
                                 └─────────────────┘
```

## When to Use This Skill

Use this skill when ANY of these are true:
- [ ] Adding new modules or files
- [ ] Refactoring existing code
- [ ] Moving code between layers
- [ ] Adding new dependencies
- [ ] Architecture violations detected
- [ ] Planning major refactoring

## Architecture Rules

### Enforced Rules (from `.dependency-cruiser.cjs`)

#### Immediate Enforcement (Errors)

| Rule | Description | Violation Example |
|-------|-------------|------------------|
| `no-view-to-view` | Views should not import other views (except BaseView) | `import HomeView from './HomeView.js'` |
| `views-should-not-import-db` | Views must use services layer instead of direct db access | `import { saveTopic } from '@/core/db.js'` |
| `components-should-not-import-api` | Components should be presentational, receive callbacks as props | `import { apiCall } from '@/api/'` |
| `api-should-not-import-db` | API layer should receive credentials as parameters | `import { getDb } from '@/core/db.js'` |

### Additional Best Practices

#### Import Patterns

**Correct:**
```javascript
// Views using services
import { quizService } from '@/services/quiz-service.js';

// Services using API
import { generateQuiz } from '@/api/api.real.js';

// Core utilities only using external libs
import { openDB } from 'idb';
```

**Incorrect:**
```javascript
// Views importing API (skip service layer)
import { generateQuiz } from '@/api/api.real.js';

// Services importing other services directly
import { otherService } from '@/services/other-service.js';

// API accessing database directly
import { saveQuiz } from '@/core/db.js';
```

#### Layer Boundary Patterns

| Layer | Should Import | Should Not Import |
|-------|----------------|-------------------|
| Views | Services, Components, Core, State | API, Database, Other Views |
| Components | Core, State | Services, API, Database |
| Services | API, Core, Database | Views, Other Services |
| API | Core | Database, Services, Views |
| Core | External libraries only | Internal layers |

## Compliance Validation Process

### Step 1: Current State Analysis

```bash
# Run architecture validation
npm run arch:test

# Generate dependency graph
npm run arch:graph

# Check for circular dependencies
npm run arch:test | grep -i circular

# Analyze specific file
npx depcruise src/views/QuizView.js --output-type dot
```

### Step 2: Identify Violations

#### Common Violation Patterns

1. **View Importing API Directly**
```javascript
// VIOLATION
import { generateQuiz } from '@/api/api.real.js';

export default class QuizView extends BaseView {
  async createQuiz() {
    const quiz = await generateQuiz(topic); // Direct API access
  }
}
```

2. **Component Making API Calls**
```javascript
// VIOLATION
import { fetchQuiz } from '@/api/api.real.js';

export function QuizComponent() {
  const [quiz, setQuiz] = useState(null);
  
  useEffect(() => {
    fetchQuiz().then(setQuiz); // API call in component
  }, []);
}
```

3. **API Accessing Database**
```javascript
// VIOLATION
import { saveQuiz } from '@/core/db.js';

export async function generateQuiz(topic) {
  const quiz = createQuizData(topic);
  await saveQuiz(quiz); // Direct DB access
  return quiz;
}
```

### Step 3: Fix Architecture Violations

#### Fix Pattern 1: Views → Services → API

```javascript
// BEFORE (Violation)
import { generateQuiz } from '@/api/api.real.js';

export default class QuizView extends BaseView {
  async createQuiz() {
    const quiz = await generateQuiz(topic);
  }
}

// AFTER (Compliant)
import { quizService } from '@/services/quiz-service.js';

export default class QuizView extends BaseView {
  async createQuiz() {
    const quiz = await quizService.generateQuiz(topic);
  }
}

// In quiz-service.js
import { generateQuiz } from '@/api/api.real.js';

export const quizService = {
  async generateQuiz(topic) {
    return await generateQuiz(topic);
  }
};
```

#### Fix Pattern 2: Components → Props/Callbacks

```javascript
// BEFORE (Violation)
import { fetchQuiz } from '@/api/api.real.js';

export function QuizComponent({ topic }) {
  const [quiz, setQuiz] = useState(null);
  
  useEffect(() => {
    fetchQuiz(topic).then(setQuiz);
  }, [topic]);
}

// AFTER (Compliant)
export function QuizComponent({ topic, onQuizGenerated }) {
  const [quiz, setQuiz] = useState(null);
  
  useEffect(() => {
    onQuizGenerated(topic).then(setQuiz);
  }, [topic, onQuizGenerated]);
}

// Parent provides API access
import { fetchQuiz } from '@/services/quiz-service.js';

export function ParentComponent() {
  const handleQuizGenerated = async (topic) => {
    return await fetchQuiz(topic);
  };
  
  return <QuizComponent topic="science" onQuizGenerated={handleQuizGenerated} />;
}
```

#### Fix Pattern 3: API → Parameter Passing

```javascript
// BEFORE (Violation)
import { saveQuiz } from '@/core/db.js';

export async function generateQuiz(topic) {
  const quiz = createQuizData(topic);
  await saveQuiz(quiz); // Direct DB access
  return quiz;
}

// AFTER (Compliant)
export async function generateQuiz(topic, dbConnection = null) {
  const quiz = createQuizData(topic);
  
  // Accept DB connection as parameter
  if (dbConnection) {
    await dbConnection.save(quiz);
  }
  
  return quiz;
}

// Service layer provides DB connection
import { getDatabase } from '@/core/db.js';

export const quizService = {
  async generateQuiz(topic) {
    const db = await getDatabase();
    return await generateQuiz(topic, db);
  }
};
```

### Step 4: Validation and Testing

```bash
# Re-run architecture validation
npm run arch:test

# Should show no violations
# ✅ No dependency rule violations found

# Check specific patterns
npx depcruise src/ --config .dependency-cruiser.cjs --output-type err

# Generate updated graph
npm run arch:graph
dot -Tpng dependency-graph.dot -o architecture-fixed.png
```

## Advanced Architecture Patterns

### Service Layer Design

#### Proper Service Structure

```javascript
// src/services/quiz-service.js
import { generateQuiz } from '@/api/api.real.js';
import { saveQuiz, loadQuiz } from '@/core/db.js';
import { logger } from '@/utils/logger.js';

export const quizService = {
  // High-level operations
  async createQuiz(topic, options = {}) {
    logger.info('Creating quiz', { topic, options });
    
    try {
      const quiz = await generateQuiz(topic, options);
      await saveQuiz(quiz);
      return quiz;
    } catch (error) {
      logger.error('Quiz creation failed', { topic, error });
      throw error;
    }
  },

  async loadQuiz(id) {
    const quiz = await loadQuiz(id);
    logger.debug('Quiz loaded', { id, questions: quiz?.questions?.length });
    return quiz;
  },

  // Business logic validation
  validateQuiz(quiz) {
    if (!quiz.questions || quiz.questions.length === 0) {
      throw new Error('Quiz must have at least one question');
    }
    if (quiz.questions.length > 20) {
      throw new Error('Quiz cannot have more than 20 questions');
    }
    return true;
  }
};
```

#### Dependency Injection Pattern

```javascript
// Allow services to receive dependencies
export class QuizService {
  constructor(apiClient, database, logger) {
    this.api = apiClient;
    this.db = database;
    this.logger = logger;
  }

  async createQuiz(topic) {
    this.logger.info('Creating quiz', { topic });
    const quiz = await this.api.generateQuiz(topic);
    await this.db.saveQuiz(quiz);
    return quiz;
  }
}

// Factory for creating services
export function createQuizService() {
  return new QuizService(
    apiReal,
    getDatabase(),
    logger
  );
}
```

### Component Design Patterns

#### Presentational Components

```javascript
// Only handle UI, receive data via props
export function QuizCard({ 
  quiz, 
  onQuizStart, 
  onQuizShare, 
  isDisabled = false 
}) {
  return (
    <div className="quiz-card" data-testid="quiz-card">
      <h3>{quiz.title}</h3>
      <p>{quiz.description}</p>
      <div className="quiz-actions">
        <button 
          onClick={() => onQuizStart(quiz.id)}
          disabled={isDisabled}
          data-testid="start-quiz-btn"
        >
          Start Quiz
        </button>
        <button 
          onClick={() => onQuizShare(quiz.id)}
          data-testid="share-quiz-btn"
        >
          Share
        </button>
      </div>
    </div>
  );
}

// Container component handles logic
import { quizService } from '@/services/quiz-service.js';

export function QuizContainer({ quizId }) {
  const [quiz, setQuiz] = useState(null);
  
  useEffect(() => {
    quizService.loadQuiz(quizId).then(setQuiz);
  }, [quizId]);

  const handleStart = () => {
    // Navigate to quiz
  };

  const handleShare = () => {
    // Share quiz
  };

  return quiz ? (
    <QuizCard 
      quiz={quiz}
      onQuizStart={handleStart}
      onQuizShare={handleShare}
    />
  ) : null;
}
```

## Dependency Analysis Tools

### Using Dependency Cruiser

```bash
# Full analysis
npx depcruise src/ --config .dependency-cruiser.cjs --output-type html

# Specific directory
npx depcruise src/views/ --config .dependency-cruiser.cjs

# Specific file with details
npx depcruise src/views/QuizView.js --config .dependency-cruiser.cjs --output-type err

# Custom focus
npx depcruise src/ --config .dependency-cruiser.cjs --focus "src/views"
```

### Visualizing Architecture

```bash
# Generate DOT graph
npm run arch:graph

# Convert to PNG (requires graphviz)
dot -Tpng dependency-graph.dot -o architecture.png

# Convert to SVG for web
dot -Tsvg dependency-graph.dot -o architecture.svg

# Focus on specific module
npx depcruise src/ --config .dependency-cruiser.cjs --output-type dot | 
  dot -Tpng -o focused-architecture.png
```

### Circular Dependency Detection

```bash
# Find circular dependencies
npm run arch:test | grep -A5 -B5 "circular"

# Visualize cycles
npx depcruise src/ --config .dependency-cruiser.cjs --output-type dot | 
  dot -Tpng -o cycles.png

# Fix by extracting common interface
// Create shared interface
// src/core/interfaces.js
export const EventEmitter = {
  on(event, handler) { /* ... */ },
  emit(event, data) { /* ... */ }
};
```

## Migration Strategies

### Legacy Code Migration

#### Step 1: Identify Violations
```bash
# Find all files with violations
npx depcruise src/ --config .dependency-cruiser.cjs --output-type json > violations.json

# Analyze patterns
jq '.violations[].rule' violations.json | sort | uniq -c
```

#### Step 2: Plan Refactoring

```markdown
## Migration Plan: [Module Name]

### Current Issues
- [ ] View importing API directly: [files]
- [ ] Component making service calls: [files]
- [ ] Service coupling: [files]

### Refactoring Steps
1. Extract business logic to services
2. Create service interfaces
3. Update views to use services
4. Update components to be presentational
5. Add dependency injection where needed
```

#### Step 3: Incremental Migration

```javascript
// Phase 1: Add service layer (keep old code)
import { legacyAPICall } from './legacy.js';
import { newService } from '@/services/new-service.js';

export default class QuizView extends BaseView {
  async createQuiz() {
    // Use new service for new features
    if (this.isNewFlow) {
      return await newService.createQuiz(this.topic);
    }
    
    // Keep legacy for old flow
    return await legacyAPICall(this.topic);
  }
}

// Phase 2: Migrate all callers
// Phase 3: Remove legacy code
```

## Quality Metrics

### Architecture Health Indicators

| Metric | Target | How to Measure |
|--------|--------|-----------------|
| Dependency rule violations | 0 | `npm run arch:test` |
| Circular dependencies | 0 | Dependency cruiser output |
| Layer coupling | Low | Dependency graph analysis |
| Service layer coverage | 100% | All API calls through services |
| Component purity | High | No API calls in components |

### Automated Checks

```javascript
// In CI/CD pipeline
"arch:test": "depcruise src/ --config .dependency-cruiser.cjs --output-type err --max-depth 10",

"arch:validate": "npm run arch:test && echo '✅ Architecture compliance passed' || echo '❌ Architecture violations found'",
```

## Integration with Other Skills

This skill integrates with:
- **epic-hygiene-process** - For architecture compliance fixes during hygiene
- **testing-suite-management** - For testing architecture fixes
- **pwa-feature-development** - For validating new feature architecture
- **feature-flag-management** - For architectural impact of flag changes

---

**Version:** 1.0.0  
**Last Updated:** 2026-01-15  
**Compatible with:** Saberloop v2.0.0+