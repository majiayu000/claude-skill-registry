---
name: ios-merchant-feature-declaration
description: Declare new iOS Feature cases by collecting details via interactive form and automatically updating all required files (Feature.swift, FeatureInfo.swift, Localizable.strings, ScreenID, Routes). Use when "add new feature", "declare new feature", "create feature case", "add feature to menu", or "new feature declaration".
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# iOS Merchant Feature Declaration

Interactively declare new Feature cases in the iOS app by collecting all necessary information via a form, then automatically updating all required files across Domain and Presentation layers.

## When to Activate

- "add new feature"
- "declare new feature"
- "create feature case"
- "add feature to menu"
- "new feature declaration"
- "register new feature"

## Interactive Process

### Step 1: Collect Feature Details

Use `AskUserQuestion` to collect all necessary information in a single form:

**Required Information:**
1. Feature name (camelCase, e.g., "balanceHistory")
2. Vietnamese description (e.g., "Lịch sử số dư")
3. English description (e.g., "Balance History")
4. Permission code (optional 5-digit number from backend, or empty if no permission)
5. Category placement (select from available categories)
6. Has icon? (yes/no)

**Conditional Information:**
- If has icon: Icon name (kebab-case, e.g., "balance-history-icon")
- Needs deep linking? (yes/no)
- If needs deep linking: Deep link path (e.g., "balance/history")

**Available Categories:**
- counterService - Counter services (home screen)
- onlineServices - Online services (home screen)
- utilityServices - Utility services (home screen)
- leftAccountCategories - Account section (side menu)
- leftCounterCategories - Counter section (side menu)
- leftOnlineCategories - Online section (side menu)
- leftUtilityCategories - Utility section (side menu)
- leftInstallmentConversionCategories - Installment section (side menu)
- none - No category (internal feature)

### Step 2: Validate Inputs

Before proceeding, validate:
- Feature name is camelCase (first letter lowercase)
- Permission code is empty OR 5-digit number
- Category is valid
- Icon name (if provided) is kebab-case
- Deep link path (if provided) follows format: `[category]/[feature]`

If validation fails, show errors and ask user to correct.

### Step 3: Update Domain Files

Update these files automatically using Edit tool:

#### 3.1 Feature.swift (5 locations)

**File:** `Domain/Model/Others/Feature.swift`

**Location 1:** Add feature case (in appropriate section with comment)
**Location 2:** Add permission code in `code` computed property
**Location 3:** Add FeatureInfo mapping in `getInfo()` method
**Location 4:** Add to category array (if category specified)
**Location 5:** Add identifier in `identifier` computed property

Use templates from `templates.md`.

#### 3.2 FeatureInfo.swift

**File:** `Domain/Model/Others/FeatureInfo.swift`

Add static property with icon and localized title (only if has icon).
Use template from `templates.md`.

#### 3.3 Localization Files

**Files:**
- `PayooMerchant/Resources/Localization/vi.lproj/Localizable.strings`
- `PayooMerchant/Resources/Localization/en.lproj/Localizable.strings`

Add localization keys:
- `menu.label.[feature-name-kebab]` - For menu items
- `home.label.feature-[feature-name-kebab]` - For home screen

Use append approach to avoid breaking existing content.

### Step 4: Update Deep Linking (if needed)

If deep linking is enabled:

#### 4.1 ScreenID.swift

**File:** `Domain/Model/Setting/ScreenID.swift`

Add screen ID case with deep link path.

#### 4.2 Route.swift

**File:** `PayooMerchant/Library/DeepLink/Route.swift`

Add route case and URL mapping (4 locations: enum case, init URL mapping, Equatable, getPermissionFeature).

Use templates from `templates.md`.

### Step 5: Update Presentation Layer Files (CRITICAL)

**IMPORTANT:** These files have exhaustive switch statements and MUST be updated to avoid compilation errors.

#### 5.1 DeepLinkNavigator.swift

**File:** `PayooMerchant/Library/DeepLink/DeepLinkNavigator.swift`

Add case to `getViewController(from destination:)` switch statement.
- Return placeholder (e.g., `makeHomeViewController()`) until actual controller is implemented
- Add TODO comment for future implementation

#### 5.2 Feature+Ext.swift

**File:** `PayooMerchant/Models/Feature+Ext.swift`

Add to `navigationBarTitle` computed property:
- If feature has navigation bar title: add specific case
- If no navigation bar title: add to nil-returning cases list

#### 5.3 AppDelegateViewModel.swift

**File:** `PayooMerchant/AppDelegateViewModel.swift`

Add to route filtering switch (around line 171):
- If feature requires permission check: add specific case with permission check
- If no permission required: add to the list of cases that return `true`

Use templates from `templates.md`.

### Step 6: Generate Boilerplate Code

Generate code snippets for manual implementation (don't auto-update these):

1. **ViewControllerFactory method** - Show code snippet
2. **DependencyContainer registration** - Show code snippet
3. **Navigator extension** (if deep linking) - Show code snippet

Use templates from `templates.md`.

### Step 7: Validation

Before presenting results, verify:
- All files were updated successfully
- No syntax errors introduced
- Feature name is unique (not already declared)
- Permission code is unique (if provided)

### Step 8: Present Results

Show comprehensive summary:

```markdown
✅ Feature Declared: [FeatureName]

📋 Collected Details:
  - Name: [featureName]
  - Vietnamese: [vietnameseDesc]
  - English: [englishDesc]
  - Permission Code: [code or "None"]
  - Category: [category]
  - Icon: [iconName or "None"]
  - Deep Link: [path or "None"]

📁 Files Updated:
  ✅ Domain/Model/Others/Feature.swift (5 locations)
  ✅ Domain/Model/Others/FeatureInfo.swift (if has icon)
  ✅ PayooMerchant/Resources/Base.lproj/Localizable.strings (Vietnamese)
  ✅ PayooMerchant/Resources/en.lproj/Localizable.strings (English)
  ✅ PayooMerchant/Library/DeepLink/DeepLinkNavigator.swift (CRITICAL)
  ✅ PayooMerchant/Models/Feature+Ext.swift (CRITICAL)
  ✅ PayooMerchant/AppDelegateViewModel.swift (CRITICAL)
  [✅ Domain/Model/Setting/ScreenID.swift] (if deep linking)
  [✅ PayooMerchant/Library/DeepLink/Route.swift - 4 locations] (if deep linking)

📝 Manual Steps Required:

1. Add Icon Assets (if has icon):
   - Location: PayooMerchant/Resources/Assets.xcassets/
   - Create: [iconName].imageset/
   - Add images: 1x, 2x, 3x (24x24, 48x48, 72x72 pt)

2. Add ViewControllerFactory Method:
   [Show code snippet]

3. Register in DependencyContainer:
   [Show code snippet]

4. Create ViewController and ViewModel:
   - [FeatureName]ViewController.swift
   - [FeatureName]ViewModel.swift
   - Follow MVVM + RxSwift Input/Output pattern

[5. Add Navigator Extension (if deep linking):
   [Show code snippet]]

✅ Verification Checklist:
  - [ ] Build project successfully
  - [ ] Run SwiftLint (bundle exec fastlane lint)
  - [ ] Test without permission (should hide feature)
  - [ ] Test with permission (should show feature)
  - [ ] Verify Vietnamese and English text
  - [ ] Test icon displays correctly
  - [ ] Test deep link (if applicable)
  - [ ] Test navigation to feature

🔗 Next Steps:
  1. Add icon assets to Assets.xcassets
  2. Implement ViewController and ViewModel
  3. Add factory method to ViewControllerFactory
  4. Register ViewModel in DependencyContainer
  5. Test thoroughly before committing

📚 Reference: NEW_FEATURE_DECLARATION_PLAN.md
```

## Validation Rules

### Feature Name
- Must be camelCase (first letter lowercase)
- Must start with a letter
- Can only contain letters and numbers
- Must be unique (check existing Feature cases)

### Permission Code
- Empty string (no permission) OR
- Exactly 5 digits
- Must be unique if provided

### Category
- Must be one of the predefined categories
- Use "none" for internal features

### Icon Name
- Must be kebab-case (lowercase with hyphens)
- Should end with "-icon" suffix
- Example: "balance-history-icon"

### Deep Link Path
- Format: `[category]/[feature]` or `[category]/[feature]/[subfeature]`
- Must be kebab-case
- Example: "balance/history"

---

See `templates.md` for code templates.
See `examples.md` for complete example.
