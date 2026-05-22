---
name: frontend-angular-form
description: Use when creating reactive forms with validation, async validators, dependent validation, and FormArrays using platform patterns.
infer: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Angular Form Development Workflow

Use when creating/modifying reactive forms with validation, async validators, dependent validation, or FormArrays.

## Decision Tree

```
What type of form?
├── Basic form (no auth)    → PlatformFormComponent
├── Form with auth context  → AppBaseFormComponent (typical choice)
├── With async validation   → AppBaseFormComponent + ifAsyncValidator
├── Cross-field validation  → AppBaseFormComponent + dependentValidations
└── Dynamic fields          → AppBaseFormComponent + FormArray config
```

## Workflow

1. **Search** existing forms: `grep "{Feature}FormComponent" --include="*.ts"`
2. **Read** design system docs (see Read Directives below)
3. **Define** ViewModel interface for form data
4. **Implement** `initialFormConfig()` with controls, validators, dependentValidations
5. **Implement** `initOrReloadVm()` for create/edit mode data loading
6. **Add** `onSubmit()` with `validateForm()` guard
7. **Template** with BEM classes on all form elements
8. **Verify** checklist below

## Key Rules

- Always call `validateForm()` before submit
- Use `ifAsyncValidator(condition, validator)` - never run async validators unconditionally
- Configure `dependentValidations` for cross-field re-validation
- FormArrays use `{ modelItems, itemControl }` config pattern
- Use `formControls('name')` to access control in template
- Loading state: `isLoading$('save')()` in template

## File Location

```
src/Frontend/apps/{app-name}/src/app/features/{feature}/
├── {feature}-form.component.ts|html|scss
```

## ⚠️ MUST READ Before Implementation

**IMPORTANT: You MUST read these files before writing any code. Do NOT skip.**

1. **⚠️ MUST READ** `.claude/skills/shared/angular-design-system.md` — hierarchy, SCSS, platform APIs
2. **⚠️ MUST READ** `.claude/skills/shared/bem-component-examples.md` — BEM form examples
3. **⚠️ MUST READ** `.claude/skills/frontend-angular-form/references/form-patterns.md` — basic, async, dependent, FormArray patterns
4. **⚠️ MUST READ** target app design system: `docs/design-system/03-form-patterns.md`

## Anti-Patterns

- Missing `validateForm()` before submit
- Async validator without `ifAsyncValidator` conditional wrapper
- Missing `[formGroupName]="i"` in FormArray template loops
- Form elements without BEM classes
- Missing error messages for validation rules

## Verification Checklist

- [ ] `initialFormConfig` returns form configuration
- [ ] `initOrReloadVm` handles create + edit modes
- [ ] `validateForm()` called before submit
- [ ] Async validators wrapped with `ifAsyncValidator`
- [ ] `dependentValidations` configured for cross-field rules
- [ ] FormArrays use `modelItems` + `itemControl`
- [ ] Error messages for all validation rules
- [ ] All form elements have BEM classes


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
