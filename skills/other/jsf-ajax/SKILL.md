---
name: jsf-ajax
description: >
  JSF AJAX update rules for the HMIS project. Use when working on AJAX updates,
  p:commandButton update attributes, PrimeFaces AJAX callbacks, partial page rendering,
  or debugging AJAX update failures. Critical rules to prevent silent AJAX failures.
user-invocable: true
---

# JSF AJAX Update Guidelines

## Critical Rules

1. **AJAX UPDATE RULE**: NEVER use plain HTML elements (div, span) with id attributes for AJAX updates - use JSF components (`h:panelGroup`, `p:outputPanel`) instead
2. **RENDERED ATTRIBUTE RULE**: NEVER use `rendered` on plain HTML elements - JSF ignores it; use `h:panelGroup layout="block"` instead
3. **COMPONENT REFERENCES**: Use `p:resolveFirstComponentWithId` for updates: `update=":#{p:resolveFirstComponentWithId('componentId',view).clientId}"`
4. **NO CSS/jQuery SELECTORS**: NEVER use `@(.class)`, `@(#id)`, `@parent` in `update` or `process` attributes. Use `@this`, `@form`, explicit IDs, or `:#{p:resolveFirstComponentWithId(...)}`

## Wrong vs Correct

```xhtml
<!-- WRONG - Plain HTML, AJAX silently fails -->
<div id="stockSelection">
    <!-- content -->
</div>
<p:commandButton update="stockSelection" />

<!-- CORRECT - JSF component, AJAX works -->
<h:panelGroup id="stockSelection">
    <div><!-- content --></div>
</h:panelGroup>
<p:commandButton update="stockSelection" />
```

## Updating Growl/Messages

The growl component is in `template.xhtml` outside forms. Use absolute ID with colon prefix:

```xhtml
<!-- CORRECT -->
<p:commandButton action="#{bean.save}" update="myTable :growl" />

<!-- WRONG - Do NOT use CSS selectors -->
<p:commandButton update="@(.ui-growl)" />
```

## JSF Components for AJAX Updates

- `h:panelGroup` - Lightweight wrapper, no HTML output
- `p:outputPanel` - PrimeFaces panel, renders as `<span>` or `<div>`
- `h:div` - Renders as HTML `<div>`
- `h:form` - For updating entire form sections
- `p:panel` - Full-featured panel with header/footer

## Debugging

1. Check browser console for JavaScript errors
2. Verify target element is a JSF component (not plain HTML)
3. Use browser dev tools to confirm JSF-generated id
4. Test with `h:panelGroup` wrapper if updates fail
5. Check component hierarchy - nested components affect id resolution

For complete reference, read [developer_docs/jsf/ajax-update-guidelines.md](../../developer_docs/jsf/ajax-update-guidelines.md).
