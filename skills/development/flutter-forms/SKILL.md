---
description: "Flutter forms: validation, keyboard handling, multi-step forms, async validation. Use when building forms or handling user input."
version: "1.0.0"
updated: "2026-01-07"
---

# Flutter Forms

## Basic Form

```dart
class EventForm extends StatefulWidget {
  @override
  State<EventForm> createState() => _EventFormState();
}

class _EventFormState extends State<EventForm> {
  final _formKey = GlobalKey<FormState>();
  final _titleController = TextEditingController();

  @override
  void dispose() {
    _titleController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: TextFormField(
        controller: _titleController,
        validator: (v) => v!.isEmpty ? 'Required' : null,
        textInputAction: TextInputAction.done,
      ),
    );
  }
}
```

## Validation

```dart
// Sync
validator: (value) {
  if (value == null || value.isEmpty) return 'Required';
  if (value.length < 3) return 'Min 3 characters';
  return null;
}

// Email
validator: (value) {
  final regex = RegExp(r'^[^@]+@[^@]+\.[^@]+$');
  if (!regex.hasMatch(value!)) return 'Invalid email';
  return null;
}
```

## Keyboard Handling

```dart
TextFormField(
  textInputAction: TextInputAction.next,
  onFieldSubmitted: (_) => FocusScope.of(context).nextFocus(),
)

TextFormField(
  textInputAction: TextInputAction.done,
  onFieldSubmitted: (_) => _submit(),
)
```

## Keyboard Types

```dart
TextInputType.emailAddress
TextInputType.phone
TextInputType.number
TextInputType.multiline
```

## Autofill

```dart
AutofillGroup(
  child: Column(
    children: [
      TextFormField(autofillHints: [AutofillHints.email]),
      TextFormField(autofillHints: [AutofillHints.password], obscureText: true),
    ],
  ),
)
```

## Multi-Step Forms

Use `Stepper` widget with separate `GlobalKey<FormState>` for each step.

## Related Skills
- **flutter-ui-components**: Widget patterns
- **flutter-accessibility**: Form accessibility
