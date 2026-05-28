---
name: Form Builder
slug: form-builder
description: Create fillable forms, surveys, and interactive documents with validation and data collection
category: document-creation
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "create form"
  - "build survey"
  - "generate form"
  - "make questionnaire"
  - "fillable form"
tags:
  - forms
  - surveys
  - questionnaires
  - data-collection
  - interactive
---

# Form Builder

The Form Builder skill automates the creation of fillable forms, surveys, questionnaires, and interactive documents. It handles various form types including registration forms, feedback surveys, applications, intake forms, and assessment tools. The skill supports multiple output formats (PDF with fillable fields, HTML forms, Google Forms integration) with validation rules, conditional logic, and data collection capabilities.

Generate professional forms with proper field types, validation, styling, and submission handling for any data collection need.

## Core Workflows

### Workflow 1: Create PDF Fillable Form
**Purpose:** Generate a PDF with interactive fillable fields

**Steps:**
1. Define form structure and fields
2. Set field types (text, checkbox, radio, dropdown, date)
3. Add validation rules for each field
4. Configure field properties (required, maxLength, etc.)
5. Apply styling and layout
6. Add instructions and help text
7. Generate PDF with fillable fields
8. Test form functionality

**Implementation:**
```javascript
const { PDFDocument, PDFTextField, PDFCheckBox, PDFDropdown, rgb } = require('pdf-lib');
const fs = require('fs');

async function createFillablePDFForm(formData, outputPath) {
  const pdfDoc = await PDFDocument.create();
  const page = pdfDoc.addPage([612, 792]); // Letter size

  const { width, height } = page.getSize();
  const fontSize = 11;
  const labelFontSize = 10;

  // Add title
  page.drawText(formData.title, {
    x: 50,
    y: height - 50,
    size: 18,
    color: rgb(0.2, 0.2, 0.2)
  });

  // Add instructions
  if (formData.instructions) {
    page.drawText(formData.instructions, {
      x: 50,
      y: height - 80,
      size: 10,
      color: rgb(0.4, 0.4, 0.4),
      maxWidth: width - 100
    });
  }

  let currentY = height - 120;

  // Add form fields
  for (const field of formData.fields) {
    // Draw field label
    page.drawText(field.label + (field.required ? ' *' : ''), {
      x: 50,
      y: currentY,
      size: labelFontSize,
      color: rgb(0, 0, 0)
    });

    currentY -= 25;

    // Create field based on type
    switch (field.type) {
      case 'text':
      case 'email':
      case 'number':
        const textField = pdfDoc.getForm().createTextField(field.name);
        textField.addToPage(page, {
          x: 50,
          y: currentY,
          width: 300,
          height: 20,
          borderColor: rgb(0.5, 0.5, 0.5),
          borderWidth: 1
        });
        if (field.placeholder) {
          textField.setText(field.placeholder);
        }
        if (field.maxLength) {
          textField.setMaxLength(field.maxLength);
        }
        break;

      case 'textarea':
        const textArea = pdfDoc.getForm().createTextField(field.name);
        textArea.addToPage(page, {
          x: 50,
          y: currentY - 40,
          width: 500,
          height: 60,
          borderColor: rgb(0.5, 0.5, 0.5),
          borderWidth: 1
        });
        textArea.enableMultiline();
        currentY -= 40;
        break;

      case 'checkbox':
        field.options.forEach((option, index) => {
          const checkbox = pdfDoc.getForm().createCheckBox(`${field.name}_${index}`);
          checkbox.addToPage(page, {
            x: 50,
            y: currentY - (index * 20),
            width: 12,
            height: 12,
            borderColor: rgb(0.5, 0.5, 0.5),
            borderWidth: 1
          });

          page.drawText(option, {
            x: 70,
            y: currentY - (index * 20) + 2,
            size: 10,
            color: rgb(0, 0, 0)
          });
        });
        currentY -= field.options.length * 20;
        break;

      case 'radio':
        const radioGroup = pdfDoc.getForm().createRadioGroup(field.name);
        field.options.forEach((option, index) => {
          radioGroup.addOptionToPage(option, page, {
            x: 50,
            y: currentY - (index * 20),
            width: 12,
            height: 12,
            borderColor: rgb(0.5, 0.5, 0.5),
            borderWidth: 1
          });

          page.drawText(option, {
            x: 70,
            y: currentY - (index * 20) + 2,
            size: 10,
            color: rgb(0, 0, 0)
          });
        });
        currentY -= field.options.length * 20;
        break;

      case 'dropdown':
        const dropdown = pdfDoc.getForm().createDropdown(field.name);
        dropdown.addOptions(field.options);
        dropdown.addToPage(page, {
          x: 50,
          y: currentY,
          width: 200,
          height: 20,
          borderColor: rgb(0.5, 0.5, 0.5),
          borderWidth: 1
        });
        break;

      case 'date':
        const dateField = pdfDoc.getForm().createTextField(field.name);
        dateField.addToPage(page, {
          x: 50,
          y: currentY,
          width: 150,
          height: 20,
          borderColor: rgb(0.5, 0.5, 0.5),
          borderWidth: 1
        });
        dateField.setText('MM/DD/YYYY');
        break;
    }

    // Add help text if provided
    if (field.helpText) {
      page.drawText(field.helpText, {
        x: 370,
        y: currentY + 5,
        size: 8,
        color: rgb(0.6, 0.6, 0.6),
        maxWidth: 200
      });
    }

    currentY -= 40;

    // Add new page if running out of space
    if (currentY < 100) {
      const newPage = pdfDoc.addPage([612, 792]);
      currentY = height - 50;
    }
  }

  // Add submit button placeholder (text)
  page.drawText('Please save and email this completed form to: ' + formData.submitEmail, {
    x: 50,
    y: 50,
    size: 9,
    color: rgb(0.3, 0.3, 0.3)
  });

  const pdfBytes = await pdfDoc.save();
  fs.writeFileSync(outputPath, pdfBytes);

  return outputPath;
}
```

### Workflow 2: Generate HTML Form
**Purpose:** Create interactive HTML form with client-side validation

**Steps:**
1. Define form structure and fields
2. Generate HTML markup
3. Add CSS styling for professional appearance
4. Implement JavaScript validation
5. Handle form submission
6. Add accessibility features (ARIA labels, keyboard navigation)
7. Make responsive for mobile devices
8. Test across browsers

**Implementation:**
```javascript
function generateHTMLForm(formData, outputPath) {
  const html = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${formData.title}</title>
  <style>
    * { box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      max-width: 700px;
      margin: 40px auto;
      padding: 20px;
      background: #f5f5f5;
    }
    .form-container {
      background: white;
      padding: 40px;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
      color: #333;
      margin-bottom: 10px;
    }
    .instructions {
      color: #666;
      margin-bottom: 30px;
      font-size: 14px;
    }
    .form-group {
      margin-bottom: 25px;
    }
    label {
      display: block;
      margin-bottom: 8px;
      font-weight: 600;
      color: #333;
    }
    .required { color: #e74c3c; }
    input[type="text"],
    input[type="email"],
    input[type="number"],
    input[type="tel"],
    input[type="date"],
    textarea,
    select {
      width: 100%;
      padding: 10px 12px;
      border: 1px solid #ddd;
      border-radius: 4px;
      font-size: 14px;
      transition: border-color 0.3s;
    }
    input:focus,
    textarea:focus,
    select:focus {
      outline: none;
      border-color: #3498db;
    }
    textarea {
      resize: vertical;
      min-height: 100px;
    }
    .help-text {
      font-size: 12px;
      color: #888;
      margin-top: 5px;
    }
    .checkbox-group,
    .radio-group {
      margin-top: 8px;
    }
    .checkbox-item,
    .radio-item {
      margin-bottom: 8px;
    }
    .checkbox-item input,
    .radio-item input {
      width: auto;
      margin-right: 8px;
    }
    .error {
      color: #e74c3c;
      font-size: 12px;
      margin-top: 5px;
      display: none;
    }
    .error.visible {
      display: block;
    }
    input.invalid,
    textarea.invalid,
    select.invalid {
      border-color: #e74c3c;
    }
    button[type="submit"] {
      background: #3498db;
      color: white;
      padding: 12px 30px;
      border: none;
      border-radius: 4px;
      font-size: 16px;
      cursor: pointer;
      transition: background 0.3s;
    }
    button[type="submit"]:hover {
      background: #2980b9;
    }
    button[type="submit"]:disabled {
      background: #bdc3c7;
      cursor: not-allowed;
    }
    .success-message {
      display: none;
      background: #27ae60;
      color: white;
      padding: 15px;
      border-radius: 4px;
      margin-bottom: 20px;
    }
    @media (max-width: 600px) {
      body { padding: 10px; }
      .form-container { padding: 20px; }
    }
  </style>
</head>
<body>
  <div class="form-container">
    <div class="success-message" id="successMessage">
      Form submitted successfully! Thank you.
    </div>

    <h1>${formData.title}</h1>
    ${formData.instructions ? `<p class="instructions">${formData.instructions}</p>` : ''}

    <form id="mainForm" action="${formData.submitUrl || '#'}" method="${formData.method || 'POST'}">
      ${formData.fields.map(field => generateFieldHTML(field)).join('\n')}

      <div class="form-group">
        <button type="submit" id="submitBtn">Submit</button>
      </div>
    </form>
  </div>

  <script>
    ${generateValidationScript(formData)}
  </script>
</body>
</html>
  `;

  fs.writeFileSync(outputPath, html, 'utf8');
  return outputPath;
}

function generateFieldHTML(field) {
  const requiredAttr = field.required ? 'required' : '';
  const requiredLabel = field.required ? '<span class="required">*</span>' : '';

  switch (field.type) {
    case 'text':
    case 'email':
    case 'number':
    case 'tel':
    case 'date':
      return `
        <div class="form-group">
          <label for="${field.name}">${field.label} ${requiredLabel}</label>
          <input
            type="${field.type}"
            id="${field.name}"
            name="${field.name}"
            placeholder="${field.placeholder || ''}"
            ${requiredAttr}
            ${field.maxLength ? `maxlength="${field.maxLength}"` : ''}
            ${field.pattern ? `pattern="${field.pattern}"` : ''}
          >
          ${field.helpText ? `<div class="help-text">${field.helpText}</div>` : ''}
          <div class="error" id="${field.name}-error">${field.errorMessage || 'This field is required'}</div>
        </div>
      `;

    case 'textarea':
      return `
        <div class="form-group">
          <label for="${field.name}">${field.label} ${requiredLabel}</label>
          <textarea
            id="${field.name}"
            name="${field.name}"
            placeholder="${field.placeholder || ''}"
            ${requiredAttr}
            ${field.maxLength ? `maxlength="${field.maxLength}"` : ''}
          ></textarea>
          ${field.helpText ? `<div class="help-text">${field.helpText}</div>` : ''}
          <div class="error" id="${field.name}-error">This field is required</div>
        </div>
      `;

    case 'select':
      return `
        <div class="form-group">
          <label for="${field.name}">${field.label} ${requiredLabel}</label>
          <select id="${field.name}" name="${field.name}" ${requiredAttr}>
            <option value="">-- Select --</option>
            ${field.options.map(opt => `<option value="${opt}">${opt}</option>`).join('\n')}
          </select>
          ${field.helpText ? `<div class="help-text">${field.helpText}</div>` : ''}
          <div class="error" id="${field.name}-error">Please select an option</div>
        </div>
      `;

    case 'checkbox':
      return `
        <div class="form-group">
          <label>${field.label} ${requiredLabel}</label>
          <div class="checkbox-group">
            ${field.options.map((opt, idx) => `
              <div class="checkbox-item">
                <input type="checkbox" id="${field.name}_${idx}" name="${field.name}" value="${opt}">
                <label for="${field.name}_${idx}">${opt}</label>
              </div>
            `).join('\n')}
          </div>
          ${field.helpText ? `<div class="help-text">${field.helpText}</div>` : ''}
        </div>
      `;

    case 'radio':
      return `
        <div class="form-group">
          <label>${field.label} ${requiredLabel}</label>
          <div class="radio-group">
            ${field.options.map((opt, idx) => `
              <div class="radio-item">
                <input type="radio" id="${field.name}_${idx}" name="${field.name}" value="${opt}" ${requiredAttr}>
                <label for="${field.name}_${idx}">${opt}</label>
              </div>
            `).join('\n')}
          </div>
          ${field.helpText ? `<div class="help-text">${field.helpText}</div>` : ''}
          <div class="error" id="${field.name}-error">Please select an option</div>
        </div>
      `;

    default:
      return '';
  }
}

function generateValidationScript(formData) {
  return `
    const form = document.getElementById('mainForm');
    const submitBtn = document.getElementById('submitBtn');
    const successMessage = document.getElementById('successMessage');

    // Validation rules
    const validationRules = {
      email: /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/,
      phone: /^[\\d\\s\\-\\(\\)]+$/
    };

    // Real-time validation
    form.addEventListener('input', (e) => {
      validateField(e.target);
    });

    // Form submission
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      // Validate all fields
      let isValid = true;
      const fields = form.querySelectorAll('input, textarea, select');

      fields.forEach(field => {
        if (!validateField(field)) {
          isValid = false;
        }
      });

      if (!isValid) {
        return;
      }

      // Disable submit button
      submitBtn.disabled = true;
      submitBtn.textContent = 'Submitting...';

      try {
        // Collect form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        // Submit to server
        ${formData.submitUrl ? `
        const response = await fetch('${formData.submitUrl}', {
          method: '${formData.method || 'POST'}',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });

        if (response.ok) {
          successMessage.style.display = 'block';
          form.reset();
        } else {
          alert('Submission failed. Please try again.');
        }
        ` : `
        // No submit URL - just show success
        console.log('Form data:', data);
        successMessage.style.display = 'block';
        form.reset();
        `}

      } catch (error) {
        alert('An error occurred. Please try again.');
        console.error(error);
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit';
      }
    });

    function validateField(field) {
      const errorEl = document.getElementById(field.name + '-error');
      if (!errorEl) return true;

      let isValid = true;
      let errorMessage = '';

      // Required check
      if (field.hasAttribute('required') && !field.value.trim()) {
        isValid = false;
        errorMessage = 'This field is required';
      }

      // Email validation
      if (field.type === 'email' && field.value && !validationRules.email.test(field.value)) {
        isValid = false;
        errorMessage = 'Please enter a valid email address';
      }

      // Pattern validation
      if (field.hasAttribute('pattern') && field.value) {
        const pattern = new RegExp(field.getAttribute('pattern'));
        if (!pattern.test(field.value)) {
          isValid = false;
          errorMessage = 'Please enter a valid value';
        }
      }

      // Update UI
      if (isValid) {
        field.classList.remove('invalid');
        errorEl.classList.remove('visible');
      } else {
        field.classList.add('invalid');
        errorEl.textContent = errorMessage;
        errorEl.classList.add('visible');
      }

      return isValid;
    }
  `;
}
```

### Workflow 3: Survey/Questionnaire Generator
**Purpose:** Create comprehensive surveys with multiple question types and logic

**Steps:**
1. Define survey structure and sections
2. Add various question types (multiple choice, rating, text, etc.)
3. Implement conditional logic (skip patterns)
4. Add validation rules
5. Configure answer choices and scales
6. Design results collection and analysis
7. Generate survey in preferred format
8. Set up response tracking

**Implementation:**
```javascript
async function generateSurvey(surveyData, outputPath) {
  const survey = {
    title: surveyData.title,
    description: surveyData.description,
    sections: surveyData.sections.map(section => ({
      title: section.title,
      questions: section.questions.map((q, idx) => ({
        id: `q${section.id}_${idx + 1}`,
        type: q.type,
        text: q.text,
        required: q.required !== false,
        options: q.options,
        validation: q.validation,
        conditionalLogic: q.conditionalLogic
      }))
    })),
    settings: {
      allowAnonymous: surveyData.allowAnonymous !== false,
      showProgress: surveyData.showProgress !== false,
      randomizeQuestions: surveyData.randomizeQuestions || false,
      allowMultipleSubmissions: surveyData.allowMultipleSubmissions || false
    }
  };

  // Generate HTML survey
  const html = generateSurveyHTML(survey);
  fs.writeFileSync(outputPath, html, 'utf8');

  return {
    surveyPath: outputPath,
    questionCount: survey.sections.reduce((sum, s) => sum + s.questions.length, 0),
    settings: survey.settings
  };
}

function generateSurveyHTML(survey) {
  return `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${survey.title}</title>
  <style>
    /* Survey-specific styles */
    body {
      font-family: Arial, sans-serif;
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
      background: #f9f9f9;
    }
    .survey-container {
      background: white;
      padding: 40px;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .progress-bar {
      height: 8px;
      background: #e0e0e0;
      border-radius: 4px;
      margin-bottom: 30px;
    }
    .progress-fill {
      height: 100%;
      background: #4CAF50;
      border-radius: 4px;
      transition: width 0.3s;
    }
    .section {
      margin-bottom: 40px;
    }
    .section-title {
      font-size: 20px;
      font-weight: bold;
      margin-bottom: 20px;
      color: #333;
    }
    .question {
      margin-bottom: 30px;
      padding: 20px;
      background: #f5f5f5;
      border-radius: 6px;
    }
    .question-text {
      font-size: 16px;
      margin-bottom: 15px;
      color: #333;
    }
    .required-indicator {
      color: #e74c3c;
    }
    .rating-scale {
      display: flex;
      gap: 10px;
      justify-content: center;
      margin: 20px 0;
    }
    .rating-option {
      width: 50px;
      height: 50px;
      border: 2px solid #ddd;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.3s;
    }
    .rating-option:hover {
      border-color: #4CAF50;
      background: #f0f0f0;
    }
    .rating-option.selected {
      background: #4CAF50;
      color: white;
      border-color: #4CAF50;
    }
    button.submit-survey {
      background: #4CAF50;
      color: white;
      padding: 15px 40px;
      border: none;
      border-radius: 6px;
      font-size: 16px;
      cursor: pointer;
      width: 100%;
      margin-top: 20px;
    }
    button.submit-survey:hover {
      background: #45a049;
    }
  </style>
</head>
<body>
  <div class="survey-container">
    <h1>${survey.title}</h1>
    <p>${survey.description}</p>

    ${survey.settings.showProgress ? `
    <div class="progress-bar">
      <div class="progress-fill" id="progressFill" style="width: 0%"></div>
    </div>
    ` : ''}

    <form id="surveyForm">
      ${survey.sections.map(section => `
        <div class="section">
          <h2 class="section-title">${section.title}</h2>
          ${section.questions.map(q => generateQuestionHTML(q)).join('\n')}
        </div>
      `).join('\n')}

      <button type="submit" class="submit-survey">Submit Survey</button>
    </form>
  </div>

  <script>
    // Survey logic and submission
    ${generateSurveyScript(survey)}
  </script>
</body>
</html>
  `;
}

function generateQuestionHTML(question) {
  const requiredMark = question.required ? '<span class="required-indicator">*</span>' : '';

  switch (question.type) {
    case 'multipleChoice':
      return `
        <div class="question" data-question-id="${question.id}">
          <div class="question-text">${question.text} ${requiredMark}</div>
          ${question.options.map((opt, idx) => `
            <div>
              <input type="radio" id="${question.id}_${idx}" name="${question.id}" value="${opt}" ${question.required ? 'required' : ''}>
              <label for="${question.id}_${idx}">${opt}</label>
            </div>
          `).join('\n')}
        </div>
      `;

    case 'rating':
      const scale = question.scale || 5;
      return `
        <div class="question" data-question-id="${question.id}">
          <div class="question-text">${question.text} ${requiredMark}</div>
          <div class="rating-scale">
            ${Array.from({ length: scale }, (_, i) => i + 1).map(num => `
              <div class="rating-option" data-value="${num}" onclick="selectRating('${question.id}', ${num})">
                ${num}
              </div>
            `).join('\n')}
          </div>
          <input type="hidden" name="${question.id}" id="${question.id}" ${question.required ? 'required' : ''}>
        </div>
      `;

    case 'text':
      return `
        <div class="question" data-question-id="${question.id}">
          <div class="question-text">${question.text} ${requiredMark}</div>
          <textarea name="${question.id}" rows="4" style="width: 100%; padding: 10px;" ${question.required ? 'required' : ''}></textarea>
        </div>
      `;

    case 'checkbox':
      return `
        <div class="question" data-question-id="${question.id}">
          <div class="question-text">${question.text} ${requiredMark}</div>
          ${question.options.map((opt, idx) => `
            <div>
              <input type="checkbox" id="${question.id}_${idx}" name="${question.id}" value="${opt}">
              <label for="${question.id}_${idx}">${opt}</label>
            </div>
          `).join('\n')}
        </div>
      `;

    default:
      return '';
  }
}

function generateSurveyScript(survey) {
  return `
    function selectRating(questionId, value) {
      // Remove previous selection
      const container = document.querySelector(\`[data-question-id="\${questionId}"]\`);
      container.querySelectorAll('.rating-option').forEach(opt => {
        opt.classList.remove('selected');
      });

      // Add new selection
      event.target.classList.add('selected');
      document.getElementById(questionId).value = value;
    }

    // Form submission
    document.getElementById('surveyForm').addEventListener('submit', async (e) => {
      e.preventDefault();

      const formData = new FormData(e.target);
      const responses = Object.fromEntries(formData);

      console.log('Survey responses:', responses);

      // Submit to server or save locally
      alert('Thank you for completing the survey!');
      e.target.reset();
    });

    // Progress tracking
    ${survey.settings.showProgress ? `
    const questions = document.querySelectorAll('.question');
    const progressFill = document.getElementById('progressFill');

    document.addEventListener('input', updateProgress);

    function updateProgress() {
      let answered = 0;
      questions.forEach(q => {
        const inputs = q.querySelectorAll('input, textarea');
        const hasAnswer = Array.from(inputs).some(input => {
          if (input.type === 'radio' || input.type === 'checkbox') {
            return input.checked;
          }
          return input.value.trim() !== '';
        });
        if (hasAnswer) answered++;
      });

      const progress = (answered / questions.length) * 100;
      progressFill.style.width = progress + '%';
    }
    ` : ''}
  `;
}
```

### Workflow 4: Form Data Processing
**Purpose:** Handle form submissions and process collected data

**Steps:**
1. Set up submission endpoint
2. Validate submitted data
3. Process and sanitize inputs
4. Store data in database or spreadsheet
5. Send confirmation email
6. Generate summary reports
7. Export data for analysis

### Workflow 5: Multi-Page Form with Progress
**Purpose:** Create long forms split into multiple pages with progress tracking

**Steps:**
1. Divide form into logical sections
2. Create page navigation
3. Implement progress bar
4. Save progress between pages
5. Add validation at each step
6. Allow going back to edit
7. Submit all data at the end

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| PDF fillable form | "create fillable PDF form" |
| HTML form | "generate HTML form with [fields]" |
| Survey | "build survey about [topic]" |
| Contact form | "create contact form" |
| Registration form | "make registration form" |
| Feedback form | "generate feedback survey" |
| Multi-step form | "create multi-page form" |

## Best Practices

- **Clear Labels:** Use descriptive, concise labels for all fields
- **Logical Grouping:** Group related fields together
- **Required Fields:** Clearly mark required fields with asterisks
- **Help Text:** Provide guidance for complex fields
- **Validation:** Implement both client-side and server-side validation
- **Error Messages:** Show clear, helpful error messages
- **Accessibility:** Include ARIA labels, keyboard navigation
- **Mobile Responsive:** Ensure forms work on all devices
- **Progress Indicators:** Show progress for long forms
- **Save Progress:** Allow users to save and resume
- **Confirmation:** Show success message after submission
- **Security:** Use CSRF protection, sanitize inputs

## Common Patterns

**Contact Form:**
```javascript
{
  fields: [
    { name: 'name', type: 'text', label: 'Full Name', required: true },
    { name: 'email', type: 'email', label: 'Email', required: true },
    { name: 'phone', type: 'tel', label: 'Phone Number' },
    { name: 'subject', type: 'text', label: 'Subject', required: true },
    { name: 'message', type: 'textarea', label: 'Message', required: true }
  ]
}
```

**Event Registration:**
```javascript
{
  fields: [
    { name: 'attendeeName', type: 'text', required: true },
    { name: 'email', type: 'email', required: true },
    { name: 'ticketType', type: 'select', options: ['General', 'VIP'], required: true },
    { name: 'dietaryRestrictions', type: 'checkbox', options: ['Vegetarian', 'Vegan', 'Gluten-Free'] },
    { name: 'specialRequests', type: 'textarea' }
  ]
}
```

## Dependencies

Install required packages:
```bash
npm install pdf-lib        # For PDF forms
npm install express        # For form submission handling
npm install validator      # For input validation
npm install nodemailer     # For email confirmations
```

## Error Handling

- **Validation Errors:** Show specific field-level errors
- **Network Errors:** Handle submission failures gracefully
- **Data Loss:** Auto-save progress to prevent data loss
- **Browser Compatibility:** Test across different browsers

## Advanced Features

**Conditional Logic:**
```javascript
conditionalLogic: {
  showIf: { field: 'employment', value: 'employed' },
  hideIf: { field: 'student', value: 'yes' }
}
```

**File Upload:**
```javascript
{
  name: 'resume',
  type: 'file',
  accept: '.pdf,.doc,.docx',
  maxSize: 5242880 // 5MB
}
```

**Auto-Save:**
```javascript
setInterval(() => {
  const formData = new FormData(form);
  localStorage.setItem('formDraft', JSON.stringify(Object.fromEntries(formData)));
}, 30000);
```