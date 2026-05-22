---
name: testing-methodology
# prettier-ignore
description: Use when writing tests, verifying functionality, QA, test scenarios, user testing, or browser automation tests
version: 1.0.0
---

<objective>
Ensure testing approaches mirror how real users experience the product. Tests should catch issues before users do, verify from an end-user perspective, and establish clear verification loops that build confidence.
</objective>

<when-to-use>
Auto-triggers when:
- Writing tests for features or components
- Verifying functionality works correctly
- Discussing QA approaches or test coverage
- Debugging user-reported issues
- Planning test scenarios
</when-to-use>

<core-principles>

## Test From User Perspective

Write tests that mirror actual user workflows, not implementation details. Users don't
care about internal state - they care whether their task completes successfully.

<test-pattern>
describe('User completes checkout', () => {
  it('purchases items successfully', async () => {
    await user.addItemToCart('Premium Plan');
    await user.proceedToCheckout();
    await user.enterPaymentDetails(validCard);
    await user.confirmPurchase();

    expect(await user.seesConfirmation()).toBe(true);
    expect(await user.receivesEmail()).toBe(true);

}); }); </test-pattern>

<test-pattern>
describe('User searches for content', () => {
  it('finds and opens previous item', async () => {
    await user.searchFor('project proposal');
    await user.selectFirstResult();

    expect(await user.seesItemDetails()).toBe(true);
    expect(await user.canEditItem()).toBe(true);

}); }); </test-pattern>

<test-pattern>
describe('User schedules message', () => {
  it('schedules team notification', async () => {
    await user.openComposer();
    await user.typeMessage('Team standup tomorrow');
    await user.selectSchedule('tomorrow at 9am');

    expect(await user.seesScheduledConfirmation()).toBe(true);

}); }); </test-pattern>

## Persona-Based Testing

Create specific user personas with distinct goals and test from their perspective.
Different users have different needs, constraints, and behaviors.

<persona-examples>
// Power user persona - efficiency focused
const powerUser = {
  goal: 'Complete tasks quickly using keyboard shortcuts',
  constraints: 'Avoids mouse, expects instant feedback',
  testFocus: 'Keyboard navigation, shortcut coverage, performance'
};

// Mobile user persona - on-the-go access const mobileUser = { goal: 'Quick actions on
small screen while distracted', constraints: 'Touch targets, limited attention, unstable
connection', testFocus: 'Touch interaction, offline capability, simplified flows' };

// First-time user persona - discovering capabilities const firstTimeUser = { goal:
'Understand what the product does and accomplish first task', constraints: 'No prior
knowledge, needs clear guidance', testFocus: 'Onboarding clarity, discoverability,
helpful empty states' };

// Returning user persona - picking up where they left off const returningUser = { goal:
'Resume previous work without friction', constraints: 'May not remember exact details
from last session', testFocus: 'Context restoration, history access, continuity' };
</persona-examples>

## Observe-Fix-Verify Loop

When testing reveals issues, follow a systematic verification cycle that builds
confidence the fix actually works.

<verification-loop>
// Observe: Reproduce the issue reliably
async function reproduceIssue() {
  const result = await performAction();
  // Document exact steps and environment where it fails
  return result;
}

// Fix: Address root cause async function implementFix() { // Make targeted change based
on observed behavior await applyFix(); }

// Verify: Confirm fix works async function verifyFix() { const result = await
performAction(); expect(result).toMatchExpectedBehavior();

// Test edge cases that might still break await testRelatedScenarios(); }

// Re-verify: Ensure fix holds under different conditions async function reVerifyFix() {
await verifyFix(); await testWithDifferentData(); await testUnderLoad(); await
testAfterRestart(); } </verification-loop>

## Test What Users Experience

Verify observable outcomes, not internal implementation. If users can't see it, consider
whether testing it adds value.

<observable-outcomes>
// Test user-visible behavior
test('user sees error when email invalid', async () => {
  await user.enterEmail('invalid-email');
  await user.submitForm();

expect(await user.seesErrorMessage('valid email address')).toBe(true); expect(await
user.formIsNotSubmitted()).toBe(true); });

// Test user-visible state changes test('user sees upload progress', async () => { const
upload = user.uploadFile(largeFile);

expect(await user.seesProgressIndicator()).toBe(true); await upload.complete();
expect(await user.seesSuccessMessage()).toBe(true); });

// Test user-visible side effects test('user receives confirmation email', async () => {
await user.completePurchase();

const email = await user.checkEmail(); expect(email.subject).toContain('Order
Confirmation'); expect(email.body).toContain(user.orderDetails); });
</observable-outcomes>

## Test Failure Scenarios

Users encounter errors, network issues, and edge cases. Test that the experience
degrades gracefully.

<failure-scenarios>
// Network failure during critical operation
test('preserves user work when connection drops', async () => {
  await user.typeMessage('Important message content');
  await network.disconnect();
  await user.clickSend();

expect(await user.seesOfflineMessage()).toBe(true); expect(await
user.messageIsSavedLocally()).toBe(true);

await network.reconnect(); expect(await user.messageAutoRetries()).toBe(true); });

// Invalid input recovery test('helps user fix validation errors', async () => { await
user.enterPassword('weak'); await user.submitForm();

expect(await user.seesSpecificGuidance()).toBe(true); expect(await
user.passwordFieldRetainsFocus()).toBe(true); });

// Service unavailable fallback test('continues working when external service down',
async () => { await externalService.goOffline(); await user.performCriticalAction();

expect(await user.actionCompletes()).toBe(true); expect(await
user.seesWarningAboutLimitedFeatures()).toBe(true); }); </failure-scenarios>

</core-principles>

<browser-testing>

When using browser automation for end-to-end testing:

Use natural user interactions - click, type, wait for elements to appear. Avoid
manipulating URLs directly or accessing internal state.

Wait for observable changes - wait for elements to be visible, text to appear,
animations to complete. Users don't see intermediate states.

Take screenshots at key moments - before actions, after actions, when things look wrong.
Visual evidence helps debug failures.

Check console for errors - errors that users don't see but affect functionality should
still be caught.

Verify across viewports - test at mobile, tablet, and desktop sizes. Users access from
different devices.

</browser-testing>

<test-organization>

Group tests by user workflows, not by technical components:

```javascript
// Organized by user workflows
describe('User authentication flow', () => {
  describe('New user signup', () => { ... });
  describe('Returning user login', () => { ... });
  describe('Password recovery', () => { ... });
});

describe('User manages content', () => {
  describe('Creating new content', () => { ... });
  describe('Editing existing content', () => { ... });
  describe('Deleting content', () => { ... });
});
```

This organization mirrors how users think about the product, making tests easier to
understand and maintain.

</test-organization>

<quality-signals>

Well-tested code demonstrates these characteristics:

Tests describe user goals, not implementation details. Test names read like user
stories.

Tests catch real user issues before deployment. High correlation between test failures
and actual bugs.

Tests run quickly enough to provide rapid feedback. Developers run them frequently
during development.

Tests remain stable as implementation changes. Refactoring doesn't require rewriting
tests.

Tests document expected behavior clearly. New team members learn the product by reading
tests.

</quality-signals>
