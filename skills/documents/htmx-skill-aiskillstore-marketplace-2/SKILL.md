---
name: htmx-skill
description: Documentation for the htmx JavaScript library (attributes, events, headers, API, extensions, examples, migration guides, server examples). Use when you need accurate htmx syntax/behavior or to locate the right reference page for an htmx question.
---

# htmx Reference

Use the index below to open the most specific page for the user's question.
Search the local `references/` folder with `rg` when unsure which page contains the answer.

## Reference Index

### General

- **Events**: Documentation page
  - Reference: [events.md](references/events.md)

- **Javascript API**: This documentation describes the JavaScript API for htmx, including methods and properties for configuring the behavior of htmx, working with CSS classes, AJAX requests, event handling, and DOM manipulation. The API provides helper functions primarily intended for extension development and event management.
  - Reference: [api.md](references/api.md)

### Attributes

- **hx-boost**: The hx-boost attribute in htmx enables progressive enhancement by converting standard HTML anchors and forms into AJAX requests, maintaining graceful fallback for users without JavaScript while providing modern dynamic page updates for those with JavaScript enabled.
  - Reference: [attributes/hx-boost.md](references/attributes/hx-boost.md)

- **hx-confirm**: The hx-confirm attribute in htmx provides a way to add confirmation dialogs before executing requests, allowing you to protect users from accidental destructive actions. This documentation explains how to implement confirmation prompts and customize their behavior through event handling.
  - Reference: [attributes/hx-confirm.md](references/attributes/hx-confirm.md)

- **hx-delete**: The hx-delete attribute in htmx will cause an element to issue a DELETE request to the specified URL and swap the returned HTML into the DOM using a swap strategy.
  - Reference: [attributes/hx-delete.md](references/attributes/hx-delete.md)

- **hx-disable**: The hx-disable attribute in htmx will disable htmx processing for a given element and all its children.
  - Reference: [attributes/hx-disable.md](references/attributes/hx-disable.md)

- **hx-disabled-elt**: The hx-disabled-elt attribute in htmx allows you to specify elements that will have the `disabled` attribute added to them for the duration of the request.
  - Reference: [attributes/hx-disabled-elt.md](references/attributes/hx-disabled-elt.md)

- **hx-disinherit**: The hx-disinherit attribute in htmx lets you control how child elements inherit attributes from their parents. This documentation explains how to selectively disable inheritance of specific htmx attributes or all attributes, allowing for more granular control over your web application's behavior.
  - Reference: [attributes/hx-disinherit.md](references/attributes/hx-disinherit.md)

- **hx-encoding**: The hx-encoding attribute in htmx allows you to switch the request encoding from the usual `application/x-www-form-urlencoded` encoding to `multipart/form-data`, usually to support file uploads in an AJAX request.
  - Reference: [attributes/hx-encoding.md](references/attributes/hx-encoding.md)

- **hx-ext**: The hx-ext attribute in htmx enables one or more htmx extensions for an element and all its children. You can also use this attribute to ignore an extension that is enabled by a parent element.
  - Reference: [attributes/hx-ext.md](references/attributes/hx-ext.md)

- **hx-get**: The hx-get attribute in htmx will cause an element to issue a GET request to the specified URL and swap the returned HTML into the DOM using a swap strategy.
  - Reference: [attributes/hx-get.md](references/attributes/hx-get.md)

- **hx-headers**: The hx-headers attribute in htmx allows you to add to the headers that will be submitted with an AJAX request.
  - Reference: [attributes/hx-headers.md](references/attributes/hx-headers.md)

- **hx-history**: The hx-history attribute in htmx allows you to prevent sensitive page data from being stored in the browser's localStorage cache during history navigation, ensuring that the page state is retrieved from the server instead when navigating through history.
  - Reference: [attributes/hx-history.md](references/attributes/hx-history.md)

- **hx-history-elt**: The hx-history-elt attribute in htmx allows you to specify the element that will be used to snapshot and restore page state during navigation. In most cases we do not recommend using this element.
  - Reference: [attributes/hx-history-elt.md](references/attributes/hx-history-elt.md)

- **hx-include**: The hx-include attribute in htmx allows you to include additional element values in an AJAX request.
  - Reference: [attributes/hx-include.md](references/attributes/hx-include.md)

- **hx-indicator**: The hx-indicator attribute in htmx allows you to specify the element that will have the `htmx-request` class added to it for the duration of the request. This can be used to show spinners or progress indicators while the request is in flight.
  - Reference: [attributes/hx-indicator.md](references/attributes/hx-indicator.md)

- **hx-inherit**: The hx-inherit attribute in htmx allows you to explicitly control attribute inheritance behavior between parent and child elements, providing fine-grained control over which htmx attributes are inherited when the default inheritance system is disabled through configuration.
  - Reference: [attributes/hx-inherit.md](references/attributes/hx-inherit.md)

- **hx-on**: The hx-on attributes in htmx allow you to write inline JavaScript event handlers directly on HTML elements, supporting both standard DOM events and htmx-specific events with improved locality of behavior.
  - Reference: [attributes/hx-on.md](references/attributes/hx-on.md)

- **hx-params**: The hx-params attribute in htmx allows you to filter the parameters that will be submitted with an AJAX request.
  - Reference: [attributes/hx-params.md](references/attributes/hx-params.md)

- **hx-patch**: The hx-patch attribute in htmx will cause an element to issue a PATCH request to the specified URL and swap the returned HTML into the DOM using a swap strategy.
  - Reference: [attributes/hx-patch.md](references/attributes/hx-patch.md)

- **hx-post**: The hx-post attribute in htmx will cause an element to issue a POST request to the specified URL and swap the returned HTML into the DOM using a swap strategy.
  - Reference: [attributes/hx-post.md](references/attributes/hx-post.md)

- **hx-preserve**: The hx-preserve attribute in htmx allows you to keep an element unchanged during HTML replacement. Elements with hx-preserve set are preserved by `id` when htmx updates any ancestor element.
  - Reference: [attributes/hx-preserve.md](references/attributes/hx-preserve.md)

- **hx-prompt**: The hx-prompt attribute in htmx allows you to show a prompt before issuing a request. The value of the prompt will be included in the request in the `HX-Prompt` header.
  - Reference: [attributes/hx-prompt.md](references/attributes/hx-prompt.md)

- **hx-push-url**: The hx-push-url attribute in htmx allows you to push a URL into the browser location history. This creates a new history entry, allowing navigation with the browser's back and forward buttons.
  - Reference: [attributes/hx-push-url.md](references/attributes/hx-push-url.md)

- **hx-put**: The hx-put attribute in htmx will cause an element to issue a PUT request to the specified URL and swap the returned HTML into the DOM using a swap strategy.
  - Reference: [attributes/hx-put.md](references/attributes/hx-put.md)

- **hx-replace-url**: The hx-replace-url attribute in htmx allows you to replace the current URL of the browser location history.
  - Reference: [attributes/hx-replace-url.md](references/attributes/hx-replace-url.md)

- **hx-request**: The hx-request attribute in htmx allows you to configure the request timeout, whether the request will send credentials, and whether the request will include headers.
  - Reference: [attributes/hx-request.md](references/attributes/hx-request.md)

- **hx-select**: The hx-select attribute in htmx allows you to select the content you want swapped from a response.
  - Reference: [attributes/hx-select.md](references/attributes/hx-select.md)

- **hx-select-oob**: The hx-select-oob attribute in htmx allows you to select content from a response to be swapped in via an out-of-band swap. The value of this attribute is comma separated list of elements to be swapped out of band.
  - Reference: [attributes/hx-select-oob.md](references/attributes/hx-select-oob.md)

- **hx-swap**: The hx-swap attribute in htmx allows you to specify the 'swap strategy', or how the response will be swapped in relative to the target of an AJAX request. The default swap strategy is `innerHTML`.
  - Reference: [attributes/hx-swap.md](references/attributes/hx-swap.md)

- **hx-swap-oob**: The hx-swap-oob attribute in htmx allows you to specify that some content in a response should be swapped into the DOM somewhere other than the target, that is 'out-of-band'. This allows you to piggyback updates to other elements on a response.
  - Reference: [attributes/hx-swap-oob.md](references/attributes/hx-swap-oob.md)

- **hx-sync**: The hx-sync attribute in htmx allows you to synchronize AJAX requests between multiple elements.
  - Reference: [attributes/hx-sync.md](references/attributes/hx-sync.md)

- **hx-target**: The hx-target attribute in htmx allows you to target a different element for swapping than the one issuing the AJAX request.
  - Reference: [attributes/hx-target.md](references/attributes/hx-target.md)

- **hx-trigger**: The hx-trigger attribute in htmx allows you to specify what triggers an AJAX request. Supported triggers include standard DOM events, custom events, polling intervals, and event modifiers. The hx-trigger attribute also allows specifying event filtering, timing controls, event bubbling, and multiple trigger definitions for fine-grained control over when and how requests are initiated.
  - Reference: [attributes/hx-trigger.md](references/attributes/hx-trigger.md)

- **hx-validate**: The hx-validate attribute in htmx will cause an element to validate itself using the HTML5 Validation API before it submits a request.
  - Reference: [attributes/hx-validate.md](references/attributes/hx-validate.md)

- **hx-vals**: The hx-vals attribute in htmx allows you to add to the parameters that will be submitted with an AJAX request.
  - Reference: [attributes/hx-vals.md](references/attributes/hx-vals.md)

- **hx-vars**: The hx-vars attribute in htmx allows you to dynamically add to the parameters that will be submitted with an AJAX request. This attribute has been deprecated. We recommend you use the hx-vals attribute that provides the same functionality with safer defaults.
  - Reference: [attributes/hx-vars.md](references/attributes/hx-vars.md)

### Examples

- **A Customized Confirmation UI**: Documentation page
  - Reference: [examples/confirm.md](references/examples/confirm.md)

- **Active Search**: Documentation page
  - Reference: [examples/active-search.md](references/examples/active-search.md)

- **Animations**: Documentation page
  - Reference: [examples/animations.md](references/examples/animations.md)

- **Async Authentication**: Documentation page
  - Reference: [examples/async-auth.md](references/examples/async-auth.md)

- **Bulk Update**: Documentation page
  - Reference: [examples/bulk-update.md](references/examples/bulk-update.md)

- **Cascading Selects**: Documentation page
  - Reference: [examples/value-select.md](references/examples/value-select.md)

- **Click to Edit**: Documentation page
  - Reference: [examples/click-to-edit.md](references/examples/click-to-edit.md)

- **Click to Load**: Documentation page
  - Reference: [examples/click-to-load.md](references/examples/click-to-load.md)

- **Custom Modal Dialogs**: Documentation page
  - Reference: [examples/modal-custom.md](references/examples/modal-custom.md)

- **Delete Row**: Documentation page
  - Reference: [examples/delete-row.md](references/examples/delete-row.md)

- **Dialogs**: Documentation page
  - Reference: [examples/dialogs.md](references/examples/dialogs.md)

- **Edit Row**: Documentation page
  - Reference: [examples/edit-row.md](references/examples/edit-row.md)

- **Experimental moveBefore() Support**: Documentation page
  - Reference: [examples/move-before/details.md](references/examples/move-before/details.md)

- **File Upload**: Documentation page
  - Reference: [examples/file-upload.md](references/examples/file-upload.md)

- **Infinite Scroll**: Documentation page
  - Reference: [examples/infinite-scroll.md](references/examples/infinite-scroll.md)

- **Inline Validation**: Documentation page
  - Reference: [examples/inline-validation.md](references/examples/inline-validation.md)

- **Keyboard Shortcuts**: Documentation page
  - Reference: [examples/keyboard-shortcuts.md](references/examples/keyboard-shortcuts.md)

- **Lazy Loading**: Documentation page
  - Reference: [examples/lazy-load.md](references/examples/lazy-load.md)

- **Modal Dialogs in Bootstrap**: Documentation page
  - Reference: [examples/modal-bootstrap.md](references/examples/modal-bootstrap.md)

- **Modal Dialogs with UIKit**: Documentation page
  - Reference: [examples/modal-uikit.md](references/examples/modal-uikit.md)

- **Preserving File Inputs after Form Errors**: Documentation page
  - Reference: [examples/file-upload-input.md](references/examples/file-upload-input.md)

- **Progress Bar**: Documentation page
  - Reference: [examples/progress-bar.md](references/examples/progress-bar.md)

- **Reset user input**: Documentation page
  - Reference: [examples/reset-user-input.md](references/examples/reset-user-input.md)

- **Sortable**: Documentation page
  - Reference: [examples/sortable.md](references/examples/sortable.md)

- **Tabs (Using HATEOAS)**: Documentation page
  - Reference: [examples/tabs-hateoas.md](references/examples/tabs-hateoas.md)

- **Tabs (Using JavaScript)**: Documentation page
  - Reference: [examples/tabs-javascript.md](references/examples/tabs-javascript.md)

- **Updating Other Content**: Documentation page
  - Reference: [examples/update-other-content.md](references/examples/update-other-content.md)

- **Web Components**: Documentation page
  - Reference: [examples/web-components.md](references/examples/web-components.md)

### Extensions

- **Building htmx Extensions**: Documentation page
  - Reference: [extensions/building.md](references/extensions/building.md)

- **htmx 1.x Compatibility Extension**: Documentation page
  - Reference: [extensions/htmx-1-compat.md](references/extensions/htmx-1-compat.md)

- **htmx Head Tag Support Extension**: Documentation page
  - Reference: [extensions/head-support.md](references/extensions/head-support.md)

- **htmx Idiomorph Extension**: Documentation page
  - Reference: [extensions/idiomorph.md](references/extensions/idiomorph.md)

- **htmx Preload Extension**: Documentation page
  - Reference: [extensions/preload.md](references/extensions/preload.md)

- **htmx Response Targets Extension**: Documentation page
  - Reference: [extensions/response-targets.md](references/extensions/response-targets.md)

- **htmx Server Sent Event (SSE) Extension**: Documentation page
  - Reference: [extensions/sse.md](references/extensions/sse.md)

- **htmx Web Socket extension**: Documentation page
  - Reference: [extensions/ws.md](references/extensions/ws.md)

### Headers

- **HX-Location Response Header**: Use the HX-Location response header in htmx to trigger a client-side redirection without reloading the whole page.
  - Reference: [headers/hx-location.md](references/headers/hx-location.md)

- **HX-Push Response Header (Deprecated)**: The HX-Push response header in htmx is deprecated. Use HX-Push-Url instead.
  - Reference: [headers/hx-push.md](references/headers/hx-push.md)

- **HX-Push-Url Response Header**: Use the HX-Push-Url response header in htmx to push a URL into the browser location history.
  - Reference: [headers/hx-push-url.md](references/headers/hx-push-url.md)

- **HX-Redirect Response Header**: Use the HX-Redirect response header in htmx to trigger a client-side redirection that will perform a full page reload.
  - Reference: [headers/hx-redirect.md](references/headers/hx-redirect.md)

- **HX-Replace-Url Response Header**: Use the HX-Replace-Url response header in htmx to replace the current URL in the browser location history without creating a new history entry.
  - Reference: [headers/hx-replace-url.md](references/headers/hx-replace-url.md)

- **HX-Trigger Response Headers**: Use the HX-Trigger family of response headers in htmx to trigger client-side actions from an htmx response.
  - Reference: [headers/hx-trigger.md](references/headers/hx-trigger.md)


## Usage Notes

- Prefer attribute/event/header-specific pages over general guides.
- For API or configuration questions, check `api.md` in addition to specific pages.
- Open the referenced file to confirm details before answering if the description seems too brief.
