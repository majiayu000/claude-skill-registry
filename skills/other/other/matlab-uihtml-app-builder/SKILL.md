---
name: matlab-uihtml-app-builder
description: Build interactive web applications using HTML/JavaScript interfaces with MATLAB computational backends via the uihtml component. Use when creating HTML-based MATLAB apps, JavaScript MATLAB interfaces, web UIs with MATLAB, interactive MATLAB GUIs, or when user mentions uihtml, HTML, JavaScript, web apps, or web interfaces.
license: MathWorks BSD-3-Clause (see LICENSE)
---

# MATLAB uihtml App Builder

This skill provides comprehensive guidelines for building interactive web applications that combine HTML/JavaScript interfaces with MATLAB computational backends using the uihtml component. This architecture leverages modern web UI capabilities while harnessing MATLAB's powerful calculation engine.

## When to Use This Skill

- Building interactive MATLAB apps with HTML/JavaScript interfaces
- Creating web-based UIs for MATLAB applications
- Developing modern, responsive MATLAB GUIs using web technologies
- When user mentions: uihtml, HTML, JavaScript, web app, web interface, interactive GUI
- Combining web UI design with MATLAB computational power
- Creating calculator apps, data visualizers, or form-based MATLAB tools

## Core Architecture

### The Four Components

1. **HTML Interface** - User interface with buttons, forms, displays
2. **JavaScript Logic** - Event handling and UI interactions
3. **MATLAB Backend** - Computational engine and data processing
4. **uihtml Component** - Bridge between HTML and MATLAB

### Communication Patterns

The uihtml component enables bidirectional communication between JavaScript and MATLAB through several mechanisms:

#### Pattern 1: MATLAB → JavaScript (Data Property)

**Use Case**: Sending data from MATLAB to update the HTML interface

```matlab
% MATLAB side
h.Data = "Hello World!";
```

```javascript
// JavaScript side
htmlComponent.addEventListener("DataChanged", function(event) {
    document.getElementById("display").innerHTML = htmlComponent.Data;
});
```

#### Pattern 2: JavaScript → MATLAB (Events)

**Use Case**: Triggering MATLAB functions from user interactions

```javascript
// JavaScript side - send event to MATLAB
htmlComponent.sendEventToMATLAB("Calculate", expression);
```

```matlab
% MATLAB side - receive and handle event
h.HTMLEventReceivedFcn = @handleEvent;

function handleEvent(src, event)
    eventName = event.HTMLEventName;
    eventData = event.HTMLEventData;
    % Process event...
end
```

#### Pattern 3: MATLAB → JavaScript (Custom Events)

**Use Case**: Sending computed results or status updates to JavaScript

```matlab
% MATLAB side - send custom event to JavaScript
sendEventToHTMLSource(h, "ResultChanged", result);
```

```javascript
// JavaScript side - listen for custom event
htmlComponent.addEventListener("ResultChanged", function(event) {
    document.getElementById("display").textContent = event.Data;
});
```

#### Pattern 4: Complex Data Transfer

**Use Case**: Passing structured data between MATLAB and JavaScript

```matlab
% MATLAB side - struct data gets JSON encoded automatically
itemData = struct("ItemName","Apple","Price",2,"Quantity",10);
h.Data = itemData;
```

```javascript
// JavaScript side - access as object properties
htmlComponent.Data.ItemName  // "Apple"
htmlComponent.Data.Price     // 2
htmlComponent.Data.Quantity  // 10
```

## Critical Rules

### Security Requirements

- **ALWAYS** set `HTMLSource = 'trusted'` when using local HTML files:
  ```matlab
  h.HTMLSource = fullfile(pwd, 'myapp.html');
  % This is treated as trusted automatically for local files
  ```

- **MUST** validate all input from JavaScript before processing in MATLAB
- **NEVER** use `eval()` on user input without strict sanitization
- **ALWAYS** restrict allowed characters in user input for expressions

### Error Handling

**ALWAYS wrap MATLAB event handlers in try-catch blocks:**

```matlab
function handleEvent(src, event)
    eventName = event.HTMLEventName;
    eventData = event.HTMLEventData;

    try
        % Process the event
        result = processData(eventData);

        % Send result back to JavaScript
        sendEventToHTMLSource(src, 'ResultEvent', result);

    catch ME
        % Handle errors gracefully
        fprintf('Error: %s\n', ME.message);
        sendEventToHTMLSource(src, 'ErrorEvent', ME.message);
    end
end
```

### Data Validation

**ALWAYS validate user input before processing:**

```matlab
function result = validateExpression(expression)
    allowedChars = '0123456789+-*/.() ';
    if ~all(ismember(expression, allowedChars))
        error('Invalid characters in expression');
    end
    % Additional validation...
    result = true;
end
```

### File Organization

**Follow this directory structure:**

```
project/
├── app.m           # Main MATLAB function
├── app.html        # HTML interface
├── README.md       # Usage instructions
└── examples/       # Additional examples (optional)
```

## Complete Examples

### Example 1: Simple Calculator App

**MATLAB Side (calculator.m):**

```matlab
function calculator()
    % Create main figure
    fig = uifigure('Name', 'Calculator', 'Position', [100 100 400 500]);

    % Create HTML component
    h = uihtml(fig, 'Position', [25 25 350 450]);
    h.HTMLSource = fullfile(pwd, 'calculator.html');
    h.HTMLEventReceivedFcn = @(src, event) handleEvent(src, event);
end

function handleEvent(src, event)
    eventName = event.HTMLEventName;
    eventData = event.HTMLEventData;

    try
        switch eventName
            case 'Calculate'
                % Validate input
                expression = char(eventData);
                allowedChars = '0123456789+-*/.() ';

                if ~all(ismember(expression, allowedChars))
                    error('Invalid characters in expression');
                end

                % Evaluate safely
                result = eval(expression);

                % Send result back
                sendEventToHTMLSource(src, 'Result', num2str(result));

            case 'Clear'
                sendEventToHTMLSource(src, 'Result', '0');
        end

    catch ME
        fprintf('Error: %s\n', ME.message);
        sendEventToHTMLSource(src, 'Error', 'Invalid expression');
    end
end
```

**HTML Side (calculator.html):**

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
        }

        .calculator {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }

        .display {
            width: 100%;
            height: 60px;
            font-size: 24px;
            text-align: right;
            padding: 10px;
            border: 2px solid #ccc;
            border-radius: 5px;
            margin-bottom: 10px;
            background: #f9f9f9;
        }

        .buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }

        button {
            padding: 20px;
            font-size: 18px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            background: #667eea;
            color: white;
            transition: background 0.3s;
        }

        button:hover {
            background: #764ba2;
        }

        .operator {
            background: #ff6b6b;
        }

        .operator:hover {
            background: #ee5a52;
        }
    </style>

    <script type="text/javascript">
        let currentExpression = '';

        function setup(htmlComponent) {
            window.htmlComponent = htmlComponent;

            // Listen for results from MATLAB
            htmlComponent.addEventListener("Result", function(event) {
                document.getElementById("display").value = event.Data;
                currentExpression = event.Data;
            });

            htmlComponent.addEventListener("Error", function(event) {
                document.getElementById("display").value = "Error";
                currentExpression = '';
            });
        }

        function appendToDisplay(value) {
            currentExpression += value;
            document.getElementById("display").value = currentExpression;
        }

        function clearDisplay() {
            currentExpression = '';
            document.getElementById("display").value = '0';
            window.htmlComponent.sendEventToMATLAB("Clear", "");
        }

        function calculate() {
            if (currentExpression) {
                window.htmlComponent.sendEventToMATLAB("Calculate", currentExpression);
            }
        }
    </script>
</head>
<body>
    <div class="calculator">
        <input type="text" id="display" class="display" value="0" readonly>
        <div class="buttons">
            <button onclick="appendToDisplay('7')">7</button>
            <button onclick="appendToDisplay('8')">8</button>
            <button onclick="appendToDisplay('9')">9</button>
            <button class="operator" onclick="appendToDisplay('/')">/</button>

            <button onclick="appendToDisplay('4')">4</button>
            <button onclick="appendToDisplay('5')">5</button>
            <button onclick="appendToDisplay('6')">6</button>
            <button class="operator" onclick="appendToDisplay('*')">*</button>

            <button onclick="appendToDisplay('1')">1</button>
            <button onclick="appendToDisplay('2')">2</button>
            <button onclick="appendToDisplay('3')">3</button>
            <button class="operator" onclick="appendToDisplay('-')">-</button>

            <button onclick="appendToDisplay('0')">0</button>
            <button onclick="appendToDisplay('.')">.</button>
            <button onclick="calculate()">=</button>
            <button class="operator" onclick="appendToDisplay('+')">+</button>

            <button style="grid-column: span 4; background: #ff6b6b;" onclick="clearDisplay()">Clear</button>
        </div>
    </div>
</body>
</html>
```

### Example 2: Data Visualization App

**MATLAB Side (visualizer.m):**

```matlab
function visualizer()
    fig = uifigure('Name', 'Data Visualizer', 'Position', [100 100 800 600]);

    % Create HTML component for controls
    h = uihtml(fig, 'Position', [25 400 750 175]);
    h.HTMLSource = fullfile(pwd, 'controls.html');
    h.HTMLEventReceivedFcn = @(src, event) handleEvent(src, event, fig);

    % Create axes for plotting
    ax = uiaxes(fig, 'Position', [25 25 750 350]);
    xlabel(ax, 'X');
    ylabel(ax, 'Y');
    title(ax, 'Interactive Plot');
end

function handleEvent(src, event, fig)
    eventName = event.HTMLEventName;
    eventData = event.HTMLEventData;

    try
        switch eventName
            case 'UpdatePlot'
                % Parse parameters from JavaScript
                params = eventData;
                frequency = params.frequency;
                amplitude = params.amplitude;
                plotType = params.plotType;

                % Generate data
                x = linspace(0, 4*pi, 200);

                switch plotType
                    case 'sine'
                        y = amplitude * sin(frequency * x);
                    case 'cosine'
                        y = amplitude * cos(frequency * x);
                    case 'both'
                        y = amplitude * sin(frequency * x);
                        y2 = amplitude * cos(frequency * x);
                end

                % Find axes and plot
                ax = findobj(fig, 'Type', 'axes');
                cla(ax);

                if strcmp(plotType, 'both')
                    plot(ax, x, y, 'LineWidth', 2);
                    hold(ax, 'on');
                    plot(ax, x, y2, 'LineWidth', 2);
                    hold(ax, 'off');
                    legend(ax, 'Sine', 'Cosine');
                else
                    plot(ax, x, y, 'LineWidth', 2);
                end

                grid(ax, 'on');

                % Send confirmation
                sendEventToHTMLSource(src, 'PlotUpdated', 'Success');
        end

    catch ME
        fprintf('Error: %s\n', ME.message);
        sendEventToHTMLSource(src, 'Error', ME.message);
    end
end
```

**HTML Side (controls.html):**

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            margin: 0;
            padding: 20px;
        }

        .controls {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
        }

        .control-group {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 8px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }

        input[type="range"] {
            width: 100%;
        }

        select, button {
            width: 100%;
            padding: 8px;
            border-radius: 5px;
            border: none;
            font-size: 14px;
        }

        button {
            background: #3498db;
            color: white;
            cursor: pointer;
            margin-top: 10px;
            transition: background 0.3s;
        }

        button:hover {
            background: #2980b9;
        }
    </style>

    <script type="text/javascript">
        function setup(htmlComponent) {
            window.htmlComponent = htmlComponent;

            htmlComponent.addEventListener("PlotUpdated", function(event) {
                console.log("Plot updated successfully");
            });
        }

        function updatePlot() {
            const frequency = parseFloat(document.getElementById("frequency").value);
            const amplitude = parseFloat(document.getElementById("amplitude").value);
            const plotType = document.getElementById("plotType").value;

            const params = {
                frequency: frequency,
                amplitude: amplitude,
                plotType: plotType
            };

            window.htmlComponent.sendEventToMATLAB("UpdatePlot", params);
        }

        function updateFreqLabel(value) {
            document.getElementById("freqValue").textContent = value;
        }

        function updateAmpLabel(value) {
            document.getElementById("ampValue").textContent = value;
        }
    </script>
</head>
<body>
    <div class="controls">
        <div class="control-group">
            <label>Frequency: <span id="freqValue">1</span></label>
            <input type="range" id="frequency" min="0.1" max="5" step="0.1" value="1"
                   oninput="updateFreqLabel(this.value)">
        </div>

        <div class="control-group">
            <label>Amplitude: <span id="ampValue">1</span></label>
            <input type="range" id="amplitude" min="0.1" max="5" step="0.1" value="1"
                   oninput="updateAmpLabel(this.value)">
        </div>

        <div class="control-group">
            <label>Plot Type:</label>
            <select id="plotType">
                <option value="sine">Sine</option>
                <option value="cosine">Cosine</option>
                <option value="both">Both</option>
            </select>
        </div>
    </div>

    <button onclick="updatePlot()">Update Plot</button>
</body>
</html>
```

### Example 3: Form Processing App

**MATLAB Side (formProcessor.m):**

```matlab
function formProcessor()
    fig = uifigure('Name', 'Form Processor', 'Position', [100 100 600 400]);

    h = uihtml(fig, 'Position', [25 25 550 350]);
    h.HTMLSource = fullfile(pwd, 'form.html');
    h.HTMLEventReceivedFcn = @(src, event) handleEvent(src, event);
end

function handleEvent(src, event)
    eventName = event.HTMLEventName;
    eventData = event.HTMLEventData;

    try
        switch eventName
            case 'SubmitForm'
                % Extract form data
                name = eventData.name;
                email = eventData.email;
                age = eventData.age;

                % Validate data
                if isempty(name) || isempty(email)
                    error('Name and email are required');
                end

                if ~contains(email, '@')
                    error('Invalid email address');
                end

                if age < 0 || age > 120
                    error('Invalid age');
                end

                % Process data (example: save to file or database)
                fprintf('Processing form:\n');
                fprintf('  Name: %s\n', name);
                fprintf('  Email: %s\n', email);
                fprintf('  Age: %d\n', age);

                % Send success message
                result = struct('status', 'success', ...
                               'message', 'Form submitted successfully!');
                sendEventToHTMLSource(src, 'FormResult', result);

            case 'ClearForm'
                sendEventToHTMLSource(src, 'FormCleared', '');
        end

    catch ME
        fprintf('Error: %s\n', ME.message);
        result = struct('status', 'error', 'message', ME.message);
        sendEventToHTMLSource(src, 'FormResult', result);
    end
end
```

## Best Practices

### UI Design Principles

- **Use CSS Grid or Flexbox** for responsive layouts that adapt to different window sizes
- **Implement hover effects** for better user experience and visual feedback
- **Provide clear visual feedback** for user actions (button clicks, form submission, errors)
- **Use semantic HTML elements** (button, input, form) for better accessibility
- **Apply professional color schemes** using CSS gradients and modern design patterns

### Performance Optimization

- **Minimize data transfer** between HTML and MATLAB - send only necessary data
- **Use appropriate data types** - numbers, strings, structs (converted to JSON)
- **Implement loading indicators** for long MATLAB operations
- **Cache results** when appropriate using persistent variables in MATLAB
- **Batch multiple updates** instead of sending many small events

### Error Handling Strategy

**JavaScript Side:**
```javascript
htmlComponent.addEventListener("Error", function(event) {
    // Display user-friendly error messages
    alert("Error: " + event.Data);
});
```

**MATLAB Side:**
```matlab
try
    result = processInput(input);
    sendEventToHTMLSource(src, 'Success', result);
catch ME
    fprintf('Error: %s\n', ME.message);
    sendEventToHTMLSource(src, 'Error', 'Processing failed');
end
```

### Testing Strategy

1. **Unit Testing** - Test MATLAB functions independently
   ```matlab
   % Test individual processing functions
   assert(validateExpression('2+2'), 'Validation should pass');
   ```

2. **Integration Testing** - Test HTML-MATLAB communication
   ```matlab
   % Test event handling with sample data
   testEvent = struct('HTMLEventName', 'Calculate', 'HTMLEventData', '2+2');
   handleEvent(h, testEvent);
   ```

3. **User Testing** - Test complete user workflows
   - Try all button combinations
   - Test edge cases and invalid inputs
   - Verify visual feedback is clear

4. **Error Testing** - Test error conditions
   - Invalid input characters
   - Empty input fields
   - Network/timeout scenarios

### Debugging Tips

- **MATLAB Side**: Use `fprintf()` to log events and data
  ```matlab
  fprintf('Received event: %s with data: %s\n', eventName, eventData);
  ```

- **JavaScript Side**: Use browser developer tools (F12) to debug
  ```javascript
  console.log("Sending to MATLAB:", data);
  ```

- **Test each communication direction separately**
  - First test MATLAB → JavaScript (Data property)
  - Then test JavaScript → MATLAB (events)
  - Finally test bidirectional flow

- **Verify data types and formats**
  ```matlab
  fprintf('Data type: %s\n', class(eventData));
  fprintf('Data value: %s\n', string(eventData));
  ```

## Common Patterns

### Pattern 1: Calculator Pattern
- JavaScript builds expression strings from button clicks
- Send expression to MATLAB via `sendEventToMATLAB`
- MATLAB safely evaluates with input validation
- Results sent back via `sendEventToHTMLSource`
- Display results in real-time

### Pattern 2: Data Visualization Pattern
- JavaScript handles user interaction (sliders, dropdowns)
- Send parameters to MATLAB for computation
- MATLAB processes data and updates plots
- Can use uiaxes for MATLAB plots or send data for JavaScript plotting
- Support real-time updates and animations

### Pattern 3: Form Processing Pattern
- JavaScript collects form data into structured object
- Send entire form data as single event
- MATLAB validates each field
- Process data (save, compute, export)
- Send confirmation or error messages back
- Update UI based on results

### Pattern 4: Real-time Monitoring Pattern
- MATLAB continuously generates data (simulation, sensor reading)
- Send updates via `sendEventToHTMLSource` at intervals
- JavaScript updates display in real-time
- Implement start/stop/pause controls
- Use efficient data formats (arrays, structs)

## Implementation Checklist

Before deploying a uihtml app, verify:

- [ ] HTML file exists in correct location
- [ ] `HTMLSource` property set to correct file path
- [ ] `HTMLEventReceivedFcn` callback defined
- [ ] JavaScript `setup(htmlComponent)` function implemented
- [ ] Event listeners added for MATLAB→JS communication
- [ ] Try-catch blocks wrap all MATLAB event handling
- [ ] Input validation implemented for all user data
- [ ] Error events sent back to JavaScript for user feedback
- [ ] CSS styling applied for professional appearance
- [ ] Responsive design tested at different window sizes
- [ ] All user interactions provide visual feedback
- [ ] Loading indicators shown for long operations
- [ ] File organization follows project structure
- [ ] Documentation (README) created with usage instructions

## Troubleshooting

**Issue**: HTML file not loading in uihtml component
- **Solution**: Check file path is absolute or relative to current directory
  ```matlab
  h.HTMLSource = fullfile(pwd, 'app.html');  % Absolute path
  ```

**Issue**: Events not triggering MATLAB callback
- **Solution**: Verify `HTMLEventReceivedFcn` is set before HTML loads
- **Solution**: Check JavaScript is calling `sendEventToMATLAB` correctly

**Issue**: Data not updating in JavaScript
- **Solution**: Ensure `DataChanged` event listener is registered in `setup()`
- **Solution**: Verify MATLAB is setting `h.Data` property, not sending event

**Issue**: JavaScript errors in browser console
- **Solution**: Open browser dev tools (F12) to see detailed error messages
- **Solution**: Ensure `htmlComponent` is passed to `setup()` function
- **Solution**: Check for typos in element IDs and function names

**Issue**: MATLAB errors not displayed to user
- **Solution**: Implement error event handling in both MATLAB and JavaScript
- **Solution**: Use try-catch in MATLAB and send error messages via `sendEventToHTMLSource`

**Issue**: Slow performance when sending data
- **Solution**: Reduce frequency of updates (throttle events)
- **Solution**: Send only changed data, not entire datasets
- **Solution**: Use appropriate data types (numbers vs strings)

**Issue**: Complex data structures not transferring correctly
- **Solution**: Use MATLAB structs (automatically converted to JSON)
- **Solution**: Avoid nested cell arrays; use struct arrays instead
- **Solution**: Test data transfer with simple examples first

**Issue**: Styling not appearing correctly
- **Solution**: Verify CSS is in `<style>` block inside `<head>`
- **Solution**: Check for CSS syntax errors
- **Solution**: Use browser dev tools to inspect computed styles

## Additional Resources

- MATLAB Documentation: `doc uihtml`
- HTML/CSS/JavaScript: MDN Web Docs
- Event handling: `doc sendEventToHTMLSource`
- Figure creation: `doc uifigure`
- Debugging: Use browser Developer Tools (F12)
