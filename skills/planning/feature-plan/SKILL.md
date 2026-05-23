---
name: feature-plan
description: "Plan feature implementation with technical specifications and actionable steps for solo developers"
---

# Feature Plan

Create a detailed implementation plan for the following feature.

## Feature Description

$ARGUMENTS

## Planning Framework for Solo Developers

### 1. **Feature Breakdown**

Analyze and break down into:
- User stories
- Technical requirements
- Dependencies
- Edge cases
- Success criteria

### 2. **Technical Specification**

**Architecture**
- Where does this fit in the codebase?
- Which components/pages affected?
- New vs modified files
- Database schema changes
- API endpoints needed

**Technology Choices**
- Libraries/packages needed
- Why each choice?
- Alternatives considered
- Trade-offs

**Data Flow**
```
User Action -> Frontend -> API -> Database -> Response
```

### 3. **Implementation Steps**

Break into logical, sequential tasks:

1. **Setup** - Dependencies, configuration
2. **Database** - Schema, migrations, RLS policies
3. **Backend** - API routes, validation, logic
4. **Frontend** - Components, pages, forms
5. **Integration** - Connect pieces
6. **Testing** - Unit, integration, E2E
7. **Polish** - Error handling, loading states, UX

### 4. **Risk Assessment**

Identify potential issues:
- **Technical Risks** - Complexity, unknown territory
- **Dependency Risks** - External APIs, third-party services
- **Data Risks** - Migration, backward compatibility

### 5. **Success Criteria**

Define "done":
- Feature works as specified
- Tests pass
- No console errors
- Accessible
- Responsive
- Error handling
- Loading states
- Documentation updated

## Output Format

### 1. **Feature Overview**
- What problem does this solve?
- Who is it for?
- Key functionality

### 2. **Technical Design**
- Component structure
- API endpoints
- Database schema
- State management

### 3. **Implementation Plan**

**Phase 1: Foundation**
- [ ] Task 1
- [ ] Task 2

**Phase 2: Core Feature**
- [ ] Task 3
- [ ] Task 4

**Phase 3: Polish**
- [ ] Task 5
- [ ] Task 6

### 4. **File Changes**

**New Files**
```
app/api/feature/route.ts
components/FeatureComponent.tsx
lib/feature-utils.ts
```

**Modified Files**
```
app/page.tsx (add new section)
lib/database.types.ts (add new types)
```

### 5. **Dependencies**

**npm packages to install**
```bash
npm install package-name
```

**Environment variables**
```bash
FEATURE_API_KEY=xxx
```

### 6. **Testing Strategy**

- Unit tests for utilities
- Integration tests for API
- Component tests for UI
- E2E test for full flow

### 7. **Rollout Plan**

- Feature flag if needed
- Gradual rollout strategy
- Rollback plan
- Monitoring and metrics

### 8. **Next Steps**

1. Review plan
2. Set up environment
3. Start with Phase 1
4. Test incrementally
5. Deploy to staging
6. Production deploy

Provide a clear, actionable plan that a solo developer can follow step-by-step.
