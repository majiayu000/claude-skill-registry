---
name: b2c-forms
description: Guide for creating forms with validation in Salesforce B2C Commerce (SFRA patterns)
---

# Forms Skill

This skill guides you through creating forms with validation in Salesforce B2C Commerce using the SFRA patterns.

## Overview

B2C Commerce forms consist of three parts:

1. **Form Definition** - XML file defining fields, validation, and actions
2. **Controller Logic** - Server-side form handling and processing
3. **Template** - ISML template rendering the HTML form

## File Location

Forms are defined in the cartridge's `forms` directory:

```
/my-cartridge
    /cartridge
        /forms
            /default              # Default locale
                profile.xml
                contact.xml
                address.xml
            /de_DE               # German-specific (optional)
                address.xml
```

## Form Definition (XML)

### Basic Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<form xmlns="http://www.demandware.com/xml/form/2008-04-19">
    <field formid="email" label="form.email.label" type="string"
           mandatory="true" max-length="50"
           regexp="^[\w.%+-]+@[\w.-]+\.\w{2,6}$"
           parse-error="form.email.invalid"/>

    <field formid="password" label="form.password.label" type="string"
           mandatory="true" min-length="8" max-length="255"
           missing-error="form.password.required"/>

    <field formid="rememberMe" label="form.remember.label" type="boolean"/>

    <action formid="submit" valid-form="true"/>
    <action formid="cancel" valid-form="false"/>
</form>
```

### Field Types

| Type | Description | HTML Input |
|------|-------------|------------|
| `string` | Text input | `<input type="text">` |
| `integer` | Whole number | `<input type="number">` |
| `number` | Decimal number | `<input type="number">` |
| `boolean` | Checkbox | `<input type="checkbox">` |
| `date` | Date value | `<input type="date">` |

### Field Attributes

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `formid` | Field identifier (required) | `formid="email"` |
| `label` | Resource key for label | `label="form.email.label"` |
| `type` | Data type (required) | `type="string"` |
| `mandatory` | Required field | `mandatory="true"` |
| `max-length` | Max string length | `max-length="100"` |
| `min-length` | Min string length | `min-length="8"` |
| `regexp` | Validation pattern | `regexp="^\d{5}$"` |
| `default` | Default value | `default="US"` |
| `min` | Min numeric value | `min="0"` |
| `max` | Max numeric value | `max="100"` |
| `format` | Date format | `format="yyyy-MM-dd"` |

### Validation Error Messages

```xml
<field formid="email" type="string" mandatory="true"
       regexp="^[\w.%+-]+@[\w.-]+\.\w{2,6}$"
       missing-error="form.email.required"
       parse-error="form.email.invalid"
       range-error="form.email.toolong"
       value-error="form.email.error"/>
```

| Attribute | When Triggered |
|-----------|----------------|
| `missing-error` | Mandatory field is empty |
| `parse-error` | Value doesn't match regexp or type |
| `range-error` | Value outside min/max range |
| `value-error` | General validation failure |

### Grouped Fields

```xml
<group formid="address">
    <field formid="street" label="form.address.street" type="string" mandatory="true"/>
    <field formid="city" label="form.address.city" type="string" mandatory="true"/>
    <field formid="postalCode" label="form.address.zip" type="string" mandatory="true"/>
</group>
```

Access in controller: `form.address.street.value`

### Actions

```xml
<!-- Only validate if valid-form="true" -->
<action formid="submit" valid-form="true"/>

<!-- Skip validation -->
<action formid="cancel" valid-form="false"/>
<action formid="back" valid-form="false"/>
```

## Controller Logic (SFRA)

### Rendering a Form

```javascript
'use strict';

var server = require('server');
var csrfProtection = require('*/cartridge/scripts/middleware/csrf');

server.get('Show',
    csrfProtection.generateToken,
    function (req, res, next) {
        var form = server.forms.getForm('profile');
        form.clear();  // Reset previous values

        res.render('account/profile', {
            profileForm: form
        });
        next();
    }
);

module.exports = server.exports();
```

### Processing Form Submission

```javascript
server.post('Submit',
    server.middleware.https,
    csrfProtection.validateAjaxRequest,
    function (req, res, next) {
        var form = server.forms.getForm('profile');

        // Check validation
        if (!form.valid) {
            res.json({
                success: false,
                fields: getFormErrors(form)
            });
            return next();
        }

        // Access form values
        var email = form.email.value;
        var firstName = form.firstName.value;

        // Process and save data
        this.on('route:BeforeComplete', function () {
            var Transaction = require('dw/system/Transaction');
            Transaction.wrap(function () {
                customer.profile.email = email;
                customer.profile.firstName = firstName;
            });
        });

        res.json({ success: true });
        next();
    }
);

// Helper to extract form errors
function getFormErrors(form) {
    var errors = {};
    Object.keys(form).forEach(function (key) {
        if (form[key] && form[key].error) {
            errors[key] = form[key].error;
        }
    });
    return errors;
}
```

### Prepopulating Forms

```javascript
server.get('Edit', function (req, res, next) {
    var form = server.forms.getForm('profile');
    form.clear();

    // Prepopulate from existing data
    var profile = req.currentCustomer.profile;
    form.firstName.value = profile.firstName;
    form.lastName.value = profile.lastName;
    form.email.value = profile.email;

    res.render('account/editProfile', {
        profileForm: form
    });
    next();
});
```

### Accessing Raw Form Data

```javascript
server.post('Submit', function (req, res, next) {
    // Access raw POST data directly
    var email = req.form.email;
    var firstName = req.form.firstName;

    // Useful when not using form definitions
    next();
});
```

## Template (ISML)

### Basic Form Template

```html
<form action="${pdict.actionUrl}" method="POST" name="profile-form"
      class="form-horizontal" data-action="${URLUtils.url('Profile-Submit')}">

    <!-- CSRF Token -->
    <input type="hidden" name="${pdict.csrf.tokenName}" value="${pdict.csrf.token}"/>

    <div class="form-group ${pdict.profileForm.email.mandatory ? 'required' : ''}">
        <label for="email" class="form-control-label">
            ${Resource.msg('form.email.label', 'forms', null)}
        </label>
        <input type="email"
               id="email"
               name="email"
               class="form-control ${pdict.profileForm.email.error ? 'is-invalid' : ''}"
               value="${pdict.profileForm.email.value || ''}"
               <isif condition="${pdict.profileForm.email.mandatory}">required</isif>
               maxlength="${pdict.profileForm.email.maxLength || 50}"/>
        <isif condition="${pdict.profileForm.email.error}">
            <div class="invalid-feedback">${pdict.profileForm.email.error}</div>
        </isif>
    </div>

    <button type="submit" class="btn btn-primary">
        ${Resource.msg('button.submit', 'forms', null)}
    </button>
</form>
```

### Form with Groups

```html
<fieldset>
    <legend>${Resource.msg('form.address.title', 'forms', null)}</legend>

    <div class="form-group">
        <label for="street">${Resource.msg('form.address.street', 'forms', null)}</label>
        <input type="text" id="street" name="address_street"
               value="${pdict.addressForm.address.street.value || ''}"/>
    </div>

    <div class="form-group">
        <label for="city">${Resource.msg('form.address.city', 'forms', null)}</label>
        <input type="text" id="city" name="address_city"
               value="${pdict.addressForm.address.city.value || ''}"/>
    </div>
</fieldset>
```

### AJAX Form Submission

```html
<script>
$('form[name="profile-form"]').on('submit', function(e) {
    e.preventDefault();
    var $form = $(this);

    $.ajax({
        url: $form.data('action'),
        type: 'POST',
        data: $form.serialize(),
        success: function(response) {
            if (response.success) {
                window.location.href = response.redirectUrl;
            } else {
                displayErrors(response.fields);
            }
        }
    });
});

function displayErrors(fields) {
    Object.keys(fields).forEach(function(field) {
        var $field = $('[name="' + field + '"]');
        $field.addClass('is-invalid');
        $field.siblings('.invalid-feedback').text(fields[field]);
    });
}
</script>
```

## Localization

Form labels and errors use resource bundles:

**forms.properties:**
```properties
form.email.label=Email Address
form.email.required=Email is required
form.email.invalid=Please enter a valid email address

form.password.label=Password
form.password.required=Password is required

button.submit=Submit
button.cancel=Cancel
```

**forms_de_DE.properties:**
```properties
form.email.label=E-Mail-Adresse
form.email.required=E-Mail ist erforderlich
```

## Custom Validation

### In Form Definition

```xml
<field formid="password" type="string"
       validation="${require('*/cartridge/scripts/validation').validatePassword(formfield)}"
       range-error="form.password.weak"/>
```

### Validation Script

```javascript
// scripts/validation.js
exports.validatePassword = function (formfield) {
    var value = formfield.value;
    if (value && value.length < 8) {
        return false;  // Triggers range-error
    }
    if (!/[A-Z]/.test(value) || !/[0-9]/.test(value)) {
        return false;
    }
    return true;
};
```

## Best Practices

1. **Always use CSRF protection** for form submissions
2. **Clear forms** before displaying to reset state
3. **Use resource keys** for labels and errors (localization)
4. **Validate server-side** even with client-side validation
5. **Use `route:BeforeComplete`** for database operations
6. **Return JSON** for AJAX form submissions

## Detailed Reference

For comprehensive form patterns:
- [Form XML Reference](references/FORM-XML.md) - Complete XML schema and validation patterns
