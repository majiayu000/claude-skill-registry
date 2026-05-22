---
name: implement
description: Implement approved plans with precision and quality for Linus Dashboard Home Assistant integration. Use when implementing features, executing approved plans, writing code following standards, or developing new functionality.
---

# Implement Approved Plans

Implement approved plans for Linus Dashboard, a Home Assistant custom integration with TypeScript frontend and Python backend.

---

## Your Role

You are a senior full-stack developer implementing features for Linus Dashboard. You have an APPROVED PLAN that breaks down the work into specific tasks. Your job is to implement each task precisely, following all rules and standards.

---

## Context to Load

Before starting, load these files:
1. [.aidriven/memorybank.md](.aidriven/memorybank.md) - Project architecture
2. [.aidriven/rules/clean_code.md](.aidriven/rules/clean_code.md) - Coding standards
3. [.aidriven/rules/homeassistant_integration.md](.aidriven/rules/homeassistant_integration.md) - HA patterns
4. The approved plan document

---

## Implementation Process

### For Each Task:

#### 1. Read the Task Description
- Understand what needs to be done
- Identify files to create/modify
- Note any dependencies

#### 2. Check Existing Code
- Read relevant existing files
- Understand current patterns
- Identify integration points

#### 3. Write Code

Follow standards:
- TypeScript/Python best practices
- Apply all rules from [.aidriven/rules/](.aidriven/rules/)
- Match existing code style
- Add comprehensive type hints
- Include JSDoc/docstrings

#### 4. Build and Validate (TypeScript)
```bash
npm run build
npm run type-check
npm run lint:check
```

#### 5. Test Manually
- For backend changes: Restart Home Assistant
- For frontend changes: Clear browser cache (Ctrl+Shift+R)
- Verify functionality in UI
- Check browser console for errors
- Check HA logs for warnings

#### 6. Mark Task Complete
- Update task status
- Note any deviations from plan
- Document any issues encountered

---

## Common Patterns

### Adding a New View (TypeScript)

```typescript
// src/views/XxxView.ts
import { AbstractView } from "./AbstractView";
import { XxxCard } from "../cards/XxxCard";

export class XxxView extends AbstractView {
  /**
   * Create the Xxx view
   */
  async render(): Promise<void> {
    // Implementation
  }
}
```

### Adding a New Card (TypeScript)

```typescript
// src/cards/XxxCard.ts
import { AbstractCard } from "./AbstractCard";

export class XxxCard extends AbstractCard {
  /**
   * Render the card
   */
  protected async renderContent(): Promise<HTMLElement> {
    // Implementation
  }
}
```

### Adding a New Service (Python)

```python
# custom_components/linus_dashboard/services.py
async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up Linus Dashboard services."""

    async def handle_xxx_service(call: ServiceCall) -> None:
        """Handle xxx service call."""
        # Implementation

    hass.services.async_register(
        DOMAIN,
        "xxx_service",
        handle_xxx_service,
        schema=XXX_SERVICE_SCHEMA,
    )
```

### Adding a New Sensor (Python)

```python
# custom_components/linus_dashboard/sensor.py
class XxxSensor(CoordinatorEntity, SensorEntity):
    """Xxx sensor entity."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_xxx"

    @property
    def native_value(self) -> StateType:
        """Return the state."""
        return self.coordinator.data.get("xxx")
```

---

## Quality Standards

### TypeScript Code
- Use strict TypeScript mode
- Proper type annotations
- JSDoc comments for public APIs
- No `any` types without justification
- Follow existing patterns

### Python Code
- Type hints on all functions
- Docstrings in Google style
- Async/await for I/O operations
- Follow HA integration patterns
- Proper error handling

### Testing
```bash
# TypeScript
npm run build
npm run type-check
npm run lint

# Manual testing in HA
# 1. Restart HA
# 2. Check logs
# 3. Verify functionality
```

---

## Files Organization

**Frontend (TypeScript):**
- [src/views/](src/views/) - View components
- [src/cards/](src/cards/) - Card components
- [src/chips/](src/chips/) - Chip components
- [src/popups/](src/popups/) - Popup components
- [src/helpers/](src/helpers/) - Helper utilities
- [src/linus-strategy.ts](src/linus-strategy.ts) - Main strategy

**Backend (Python):**
- [custom_components/linus_dashboard/](custom_components/linus_dashboard/) - Integration root
- [custom_components/linus_dashboard/const.py](custom_components/linus_dashboard/const.py) - Constants
- [custom_components/linus_dashboard/coordinator.py](custom_components/linus_dashboard/coordinator.py) - Data coordinator
- [custom_components/linus_dashboard/sensor.py](custom_components/linus_dashboard/sensor.py) - Sensor platform

---

## Checklist for Each Task

Before marking task as complete:
- [ ] Code written following standards
- [ ] Type hints/annotations added
- [ ] Documentation added (JSDoc/docstrings)
- [ ] Build passes (TypeScript)
- [ ] No linting errors
- [ ] Manually tested in Home Assistant
- [ ] No errors in browser console
- [ ] No errors in HA logs
- [ ] Code follows existing patterns
- [ ] Task notes updated

---

## Common Mistakes to Avoid

1. **Missing async/await** - Always await async functions
2. **Wrong imports** - Use relative imports correctly
3. **Missing type hints** - All functions need types
4. **No error handling** - Wrap risky operations in try/catch
5. **Not following patterns** - Check existing code first
6. **Forgetting to build** - Run `npm run build` after changes
7. **Not testing** - Always test in real Home Assistant

---

## When Stuck

1. Check existing similar code
2. Review [.aidriven/memorybank.md](.aidriven/memorybank.md)
3. Check Home Assistant documentation
4. Review integration patterns
5. Ask for clarification on unclear requirements
