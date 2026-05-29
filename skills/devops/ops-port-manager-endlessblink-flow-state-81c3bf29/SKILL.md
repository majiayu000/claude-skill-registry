---
name: Resolve Port Conflicts
description: FIX port conflicts when development server won't start or tests fail. Manage port 5546 for PomoFlow, kill existing processes, and resolve server startup issues. Use when npm run dev fails, port is in use, or server won't start.
---

# Port Manager

## Instructions

### Primary Port Configuration
- **Main Application**: Port 5546 (NEVER change)
- **Storybook**: Port 6006 (separate from main app)
- **Development Server**: Always use `npm run dev`

### Server Commands
```bash
# Start main application (port 5546)
npm run dev

# Start Storybook (port 6006)
npm run storybook

# Check if server is running
curl http://localhost:5546
```

### Port Conflict Resolution
```bash
# Kill processes using port 5546
lsof -ti:5546 | xargs kill -9

# Or use pkill for node processes
pkill -f "vite.*5546"

# Restart server
npm run dev
```

### Development URLs
- Main Application: http://localhost:5546
- Storybook: http://localhost:6006
- Design System: http://localhost:5546/#/design-system

### Browser Access Patterns
Always reference the application using:
- `http://localhost:5546` for main app
- `http://localhost:6006` for Storybook
- Never hardcode other ports

### Server Health Check
```javascript
const checkServerHealth = async () => {
  try {
    const response = await fetch('http://localhost:5546')
    return response.ok
  } catch (error) {
    console.error('Server not accessible on port 5546:', error)
    return false
  }
}
```

### Testing Environment Setup
```bash
# Ensure server is running before tests
npm run dev &
sleep 5  # Wait for server to start
npm run test
```

This skill ensures consistent use of port 5546 and proper server management for the productivity application.