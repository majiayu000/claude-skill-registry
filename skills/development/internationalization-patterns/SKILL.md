---
name: Internationalization Patterns
description: Internationalization (i18n) and localization (l10n) patterns using GetX Translations for multi-language Flutter applications
version: 1.0.0
---

# Internationalization Patterns with GetX

Complete guide to implementing multi-language support in Flutter applications using GetX's powerful internationalization system.

## Setup

### Define Translations

Create a translations class extending `Translations`:

```dart
// lib/core/i18n/app_translations.dart
import 'package:get/get.dart';

class AppTranslations extends Translations {
  @override
  Map<String, Map<String, String>> get keys => {
        'en_US': EnUS.keys,
        'ar_SA': ArSA.keys,
        'fr_FR': FrFR.keys,
        'es_ES': EsES.keys,
      };
}

// English translations
class EnUS {
  static const keys = {
    // Common
    'app_name': 'My App',
    'common_save': 'Save',
    'common_cancel': 'Cancel',
    'common_delete': 'Delete',
    'common_edit': 'Edit',
    'common_loading': 'Loading...',
    'common_error': 'An error occurred',

    // Authentication
    'auth_login_title': 'Login',
    'auth_login_email': 'Email',
    'auth_login_password': 'Password',
    'auth_login_submit': 'Sign In',
    'auth_login_forgot_password': 'Forgot Password?',
    'auth_logout': 'Logout',

    // Validation
    'validation_email_required': 'Email is required',
    'validation_email_invalid': 'Please enter a valid email',
    'validation_password_required': 'Password is required',
    'validation_password_min_length': 'Password must be at least @length characters',

    // Errors
    'error_network': 'Network error. Please check your connection.',
    'error_server': 'Server error. Please try again later.',
    'error_unauthorized': 'Invalid email or password',
    'error_not_found': 'Resource not found',

    // Profile
    'profile_title': 'Profile',
    'profile_edit': 'Edit Profile',
    'profile_settings': 'Settings',
    'profile_logout': 'Logout',

    // Settings
    'settings_title': 'Settings',
    'settings_language': 'Language',
    'settings_theme': 'Theme',
    'settings_notifications': 'Notifications',

    // Pluralization
    'items_count_zero': 'No items',
    'items_count_one': 'One item',
    'items_count_other': '@count items',
  };
}

// Arabic translations
class ArSA {
  static const keys = {
    // Common
    'app_name': 'تطبيقي',
    'common_save': 'حفظ',
    'common_cancel': 'إلغاء',
    'common_delete': 'حذف',
    'common_edit': 'تعديل',
    'common_loading': 'جار التحميل...',
    'common_error': 'حدث خطأ',

    // Authentication
    'auth_login_title': 'تسجيل الدخول',
    'auth_login_email': 'البريد الإلكتروني',
    'auth_login_password': 'كلمة المرور',
    'auth_login_submit': 'تسجيل الدخول',
    'auth_login_forgot_password': 'نسيت كلمة المرور؟',
    'auth_logout': 'تسجيل الخروج',

    // Validation
    'validation_email_required': 'البريد الإلكتروني مطلوب',
    'validation_email_invalid': 'يرجى إدخال بريد إلكتروني صحيح',
    'validation_password_required': 'كلمة المرور مطلوبة',
    'validation_password_min_length': 'يجب أن تكون كلمة المرور @length أحرف على الأقل',

    // Errors
    'error_network': 'خطأ في الشبكة. يرجى التحقق من الاتصال.',
    'error_server': 'خطأ في الخادم. يرجى المحاولة لاحقاً.',
    'error_unauthorized': 'البريد الإلكتروني أو كلمة المرور غير صحيحة',
    'error_not_found': 'المورد غير موجود',

    // Profile
    'profile_title': 'الملف الشخصي',
    'profile_edit': 'تعديل الملف الشخصي',
    'profile_settings': 'الإعدادات',
    'profile_logout': 'تسجيل الخروج',

    // Settings
    'settings_title': 'الإعدادات',
    'settings_language': 'اللغة',
    'settings_theme': 'المظهر',
    'settings_notifications': 'الإشعارات',

    // Pluralization
    'items_count_zero': 'لا توجد عناصر',
    'items_count_one': 'عنصر واحد',
    'items_count_other': '@count عنصر',
  };
}
```

### Configure GetMaterialApp

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'core/i18n/app_translations.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: 'My App',
      translations: AppTranslations(),
      locale: Get.deviceLocale, // Use device locale
      fallbackLocale: const Locale('en', 'US'), // Fallback to English
      initialRoute: AppRoutes.home,
      getPages: AppPages.pages,
    );
  }
}
```

## Usage in Widgets

### Basic Translation

```dart
// Using .tr extension
Text('auth_login_title'.tr)  // Displays "Login" in English, "تسجيل الدخول" in Arabic

// Alternative syntax
Text(Get.find<AppLocalizations>().translate('auth_login_title'))
```

### Translation with Parameters

```dart
// Translation key with placeholder
'validation_password_min_length': 'Password must be at least @length characters'

// Usage with parameter
Text('validation_password_min_length'.trParams({'length': '8'}))
// Displays: "Password must be at least 8 characters"
```

### Pluralization

```dart
// Define plural forms in translations
'items_count_zero': 'No items',
'items_count_one': 'One item',
'items_count_other': '@count items',

// Usage
String getItemsCountText(int count) {
  if (count == 0) {
    return 'items_count_zero'.tr;
  } else if (count == 1) {
    return 'items_count_one'.tr;
  } else {
    return 'items_count_other'.trParams({'count': count.toString()});
  }
}

// Or use a helper
extension PluralExtension on String {
  String trPlural(int count) {
    final key = this;
    if (count == 0) {
      return '${key}_zero'.tr;
    } else if (count == 1) {
      return '${key}_one'.tr;
    } else {
      return '${key}_other'.trParams({'count': count.toString()});
    }
  }
}

// Usage
Text('items_count'.trPlural(items.length))
```

## Locale Management

### Change Locale at Runtime

```dart
class SettingsController extends GetxController {
  final currentLocale = const Locale('en', 'US').obs;

  void changeLanguage(String languageCode, String countryCode) {
    final locale = Locale(languageCode, countryCode);
    currentLocale.value = locale;
    Get.updateLocale(locale);

    // Optionally save to local storage
    final storage = Get.find<GetStorage>();
    storage.write('locale', '$languageCode\_$countryCode');
  }
}

// Usage in UI
DropdownButton<String>(
  value: controller.currentLocale.value.languageCode,
  items: const [
    DropdownMenuItem(value: 'en', child: Text('English')),
    DropdownMenuItem(value: 'ar', child: Text('العربية')),
    DropdownMenuItem(value: 'fr', child: Text('Français')),
    DropdownMenuItem(value: 'es', child: Text('Español')),
  ],
  onChanged: (languageCode) {
    String countryCode = _getCountryCode(languageCode!);
    controller.changeLanguage(languageCode, countryCode);
  },
)
```

### Persist Locale Preference

```dart
class LocaleService {
  final GetStorage _storage;

  LocaleService(this._storage);

  /// Get saved locale or device locale
  Locale getLocale() {
    final savedLocale = _storage.read<String>('locale');
    if (savedLocale != null) {
      final parts = savedLocale.split('_');
      return Locale(parts[0], parts.length > 1 ? parts[1] : '');
    }
    return Get.deviceLocale ?? const Locale('en', 'US');
  }

  /// Save locale preference
  void saveLocale(Locale locale) {
    _storage.write('locale', '${locale.languageCode}_${locale.countryCode}');
  }
}

// In main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await GetStorage.init();

  final localeService = LocaleService(GetStorage());
  final savedLocale = localeService.getLocale();

  runApp(MyApp(initialLocale: savedLocale));
}
```

## RTL Support

### Detect RTL Languages

```dart
bool isRTL(Locale locale) {
  final rtlLanguages = ['ar', 'he', 'fa', 'ur'];
  return rtlLanguages.contains(locale.languageCode);
}
```

### Configure Text Direction

```dart
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: 'My App',
      translations: AppTranslations(),
      locale: Get.deviceLocale,
      fallbackLocale: const Locale('en', 'US'),
      // Automatically set text direction based on locale
      builder: (context, child) {
        return Directionality(
          textDirection: isRTL(Get.locale!)
              ? TextDirection.rtl
              : TextDirection.ltr,
          child: child!,
        );
      },
      initialRoute: AppRoutes.home,
      getPages: AppPages.pages,
    );
  }
}
```

### RTL-Aware Widgets

```dart
// Use EdgeInsetsDirectional instead of EdgeInsets
Padding(
  padding: const EdgeInsetsDirectional.only(start: 16.0, end: 8.0),
  child: Text('Hello'),
)

// Use AlignmentDirectional instead of Alignment
Align(
  alignment: AlignmentDirectional.centerStart, // Start instead of left
  child: Text('Aligned Text'),
)

// Use leading/trailing instead of left/right in Row
Row(
  children: [
    const Icon(Icons.arrow_forward), // Will flip in RTL
    const SizedBox(width: 8),
    Text('Next'),
  ],
)
```

## Date and Number Formatting

### Date Formatting

```dart
import 'package:intl/intl.dart';

class DateFormatter {
  static String formatDate(DateTime date, Locale locale) {
    final formatter = DateFormat.yMMMd(locale.toString());
    return formatter.format(date);
  }

  static String formatTime(DateTime time, Locale locale) {
    final formatter = DateFormat.jm(locale.toString());
    return formatter.format(time);
  }

  static String formatDateTime(DateTime dateTime, Locale locale) {
    final formatter = DateFormat.yMMMd(locale.toString()).add_jm();
    return formatter.format(dateTime);
  }
}

// Usage
final formattedDate = DateFormatter.formatDate(DateTime.now(), Get.locale!);
// English: "Jan 15, 2024"
// Arabic: "١٥‏/٠١‏/٢٠٢٤"
```

### Number Formatting

```dart
import 'package:intl/intl.dart';

class NumberFormatter {
  static String formatNumber(num value, Locale locale) {
    final formatter = NumberFormat.decimalPattern(locale.toString());
    return formatter.format(value);
  }

  static String formatCurrency(num value, Locale locale, String currencySymbol) {
    final formatter = NumberFormat.currency(
      locale: locale.toString(),
      symbol: currencySymbol,
    );
    return formatter.format(value);
  }

  static String formatPercent(num value, Locale locale) {
    final formatter = NumberFormat.percentPattern(locale.toString());
    return formatter.format(value);
  }
}

// Usage
final price = NumberFormatter.formatCurrency(99.99, Get.locale!, '\$');
// English: "$99.99"
// French: "99,99 \$"
```

## Translation Key Organization

### Naming Convention

```
[feature].[screen].[widget].[state]

Examples:
- auth.login.email.label
- auth.login.email.hint
- auth.login.email.error.required
- auth.login.email.error.invalid
- profile.settings.language.title
- profile.settings.language.description
- common.button.save
- common.button.cancel
- common.error.network
- common.error.server
```

### Hierarchical Structure

```dart
class TranslationKeys {
  // Common
  static const commonSave = 'common.button.save';
  static const commonCancel = 'common.button.cancel';
  static const commonLoading = 'common.loading';

  // Authentication
  static const authLoginTitle = 'auth.login.title';
  static const authLoginEmail = 'auth.login.email.label';
  static const authLoginEmailHint = 'auth.login.email.hint';
  static const authLoginEmailRequired = 'auth.login.email.error.required';

  // Profile
  static const profileTitle = 'profile.title';
  static const profileEdit = 'profile.edit';
}

// Usage
Text(TranslationKeys.authLoginTitle.tr)
```

## Testing Translations

### Test Translation Keys

```dart
void main() {
  test('all translation keys exist in all languages', () {
    final translations = AppTranslations();
    final languages = translations.keys.keys.toList();

    // Get keys from first language
    final referenceKeys = translations.keys[languages.first]!.keys.toSet();

    // Check all other languages have same keys
    for (final lang in languages.skip(1)) {
      final langKeys = translations.keys[lang]!.keys.toSet();

      // Missing keys
      final missingKeys = referenceKeys.difference(langKeys);
      expect(missingKeys, isEmpty,
          reason: 'Language $lang is missing keys: $missingKeys');

      // Extra keys
      final extraKeys = langKeys.difference(referenceKeys);
      expect(extraKeys, isEmpty,
          reason: 'Language $lang has extra keys: $extraKeys');
    }
  });
}
```

## Best Practices

1. **Translation Keys**:
   - Use hierarchical dot notation
   - Keep keys descriptive and consistent
   - Avoid hardcoded strings in UI code
   - Define constants for frequently used keys

2. **Locale Management**:
   - Persist user's locale preference
   - Fallback to device locale when appropriate
   - Provide locale switching in settings
   - Test with different locales

3. **RTL Support**:
   - Use directional classes (EdgeInsetsDirectional, AlignmentDirectional)
   - Test UI with RTL languages (Arabic, Hebrew)
   - Flip icons and layouts appropriately
   - Consider RTL implications in custom widgets

4. **Formatting**:
   - Use `intl` package for dates and numbers
   - Format currency with correct symbols and positions
   - Handle pluralization correctly
   - Consider cultural differences (date formats, number separators)

5. **Performance**:
   - Load only needed translations
   - Cache formatted strings when appropriate
   - Avoid translating in build methods unnecessarily
   - Use const where possible

6. **Maintenance**:
   - Keep translations in sync across languages
   - Use translation management tools for large projects
   - Involve native speakers for quality translations
   - Test translations with real content (not Lorem Ipsum)
