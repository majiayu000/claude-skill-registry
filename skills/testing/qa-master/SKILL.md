---
name: QA Master
description: Master skill for Testing, Verification, and Auditing. Includes E2E (Playwright), Unit Tests, and UI/UX Audits.
triggers:
  - run tests
  - verify fix
  - audit application
  - check quality
---

# QA Master Skill

## 🎯 **Capabilities**
- **Testing**: Run and write Playwright E2E tests
- **Verification**: Validate bug fixes before claiming completion
- **Auditing**: Check for UI/UX consistency, Accessibility (A11y), and Code Quality

## 📜 **Verification Protocol (MANDATORY)**
Before marking any task as **DONE**, you MUST:
1.  **Technical Check**: Ensure build passes and no console errors.
2.  **Visual Check**: Verify the fix visually (screenshot or behavior).
3.  **User Confirmation**: Explicitly ask the user to confirm the fix.

## 🧪 **Testing Strategy**
- **E2E**: Use Playwright for critical user flows.
- **Unit**: Use Vitest for complex logic/composables.
- **Manual**: Provide a checklist for manual verification.

## 📢 **Audit Checklist**
- [ ] Design System consistency (Colors, Typos, Spacing)
- [ ] Console is free of errors
- [ ] No layout shifts or broken responsiveness
