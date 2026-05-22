---
name: feature-implementation
description: Comprehensive checklist for implementing new features in Ishkul. Ensures all aspects are covered including frontend, backend, tests, E2E tests, infrastructure, and documentation. Use when starting work on a new feature or enhancement.
---

# Feature Implementation Checklist

This skill provides a comprehensive checklist for implementing new features across the Ishkul platform.

## Pre-Implementation

Before starting:
1. Understand the feature requirements
2. Identify affected areas (frontend, backend, database, etc.)
3. Plan the implementation approach

## Implementation Checklist

### Frontend Changes
- [ ] UI components in `frontend/src/components/`
- [ ] Screens in `frontend/src/screens/`
- [ ] State management in `frontend/src/state/` (Zustand stores)
- [ ] Types in `frontend/src/types/`
- [ ] Navigation updates in `frontend/src/navigation/`
- [ ] Services for API calls in `frontend/src/services/`

### Backend Changes
- [ ] Handlers in `backend/internal/handlers/`
- [ ] Routes in `backend/cmd/server/main.go`
- [ ] Firebase/Firestore operations in `backend/pkg/firebase/`
- [ ] Business logic implementation

### Unit Tests (MANDATORY)
- [ ] Frontend screen tests: `frontend/src/screens/__tests__/`
- [ ] Frontend component tests: `frontend/src/components/__tests__/`
- [ ] Backend handler tests: `backend/internal/handlers/*_test.go`
- [ ] State transition tests for React components

### Integration Tests
- [ ] API endpoint integration tests
- [ ] Service interaction tests

### E2E Tests
- [ ] Playwright tests for web: `e2e/`
- [ ] Maestro tests for mobile: `.maestro/`
- [ ] Newman/Postman API tests: `tests/postman/`

### Infrastructure
- [ ] Firebase/Firestore rules: `firebase/`
- [ ] Environment variables added to `.env.example`
- [ ] Cloud Run configuration updates
- [ ] GitHub Actions workflow updates if needed

### Documentation
- [ ] Update CLAUDE.md if architecture changed
- [ ] Update relevant docs in `docs/` folder
- [ ] Clear commit messages explaining changes

## Verification Commands

### Frontend
```bash
cd frontend
npm run type-check  # TypeScript validation
npm run lint        # ESLint
npm test           # Unit tests
npm start          # Local testing
```

### Backend
```bash
cd backend
gofmt -w .         # Format code
go vet ./...       # Static analysis
go test ./...      # Unit tests
go run cmd/server/main.go  # Local testing
```

### E2E Tests
```bash
# Web E2E
cd e2e && npm test

# Mobile E2E
maestro test .maestro/flows/smoke-test.yaml

# API Tests
newman run tests/postman/ishkul-api.collection.json
```

## Adding New Screens (Quick Reference)

1. Create screen: `frontend/src/screens/NewScreen.tsx`
2. Add navigation: `frontend/src/navigation/AppNavigator.tsx`
3. Update types: `frontend/src/types/app.ts`
4. Create tests: `frontend/src/screens/__tests__/NewScreen.test.tsx`
5. Run verification: `npm run type-check && npm test`

## Adding New API Endpoints (Quick Reference)

1. Create handler: `backend/internal/handlers/new_handler.go`
2. Create tests: `backend/internal/handlers/new_handler_test.go`
3. Add route: `backend/cmd/server/main.go`
4. Run verification: `gofmt -w . && go vet ./... && go test ./...`
5. Test locally: `go run cmd/server/main.go`
