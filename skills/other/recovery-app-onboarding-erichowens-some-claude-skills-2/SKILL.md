---
name: recovery-app-onboarding
description: Expert guidance for designing and implementing onboarding flows in recovery, wellness, and mental health applications. This skill should be used when building onboarding experiences, first-time user flows, feature discovery, or tutorial systems for apps serving vulnerable populations (addiction recovery, mental health, wellness). Activate on "onboarding", "first-time user", "tutorial", "feature tour", "welcome flow", "new user experience", "app introduction", "recovery app UX". NOT for general mobile UX (use mobile-ux-optimizer), marketing landing pages (use web-design-expert), or native app development (use iOS/Android skills).
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
category: Design & Creative
tags:
  - onboarding
  - recovery
  - wellness
  - mental-health
  - mobile-ux
  - tutorial
  - progressive-disclosure
---

# Recovery App Onboarding Excellence

Build compassionate, effective onboarding experiences for recovery and wellness applications that serve vulnerable populations with dignity and practical utility.

## When to Use

✅ **USE this skill for:**
- First-time user onboarding flows
- Feature discovery and app tours
- Progressive disclosure design
- Permission request timing and framing
- Welcome screens and value propositions
- Recovery program selection flows
- Crisis resource integration
- Privacy and anonymity communication

❌ **DO NOT use for:**
- General mobile responsive design → use `mobile-ux-optimizer`
- Marketing/conversion optimization → use `seo-visibility-expert`
- Native iOS/Android development → use platform-specific skills
- Database schema design → use `supabase-admin`

## Core Principles

### 1. Compassion First, Features Second

Recovery users are often in vulnerable states. Every onboarding decision must consider:

```
❌ ANTI-PATTERN: "Sign up to track your progress!"
✅ CORRECT: "You're taking a brave step. Let's set up a private space for your journey."

❌ ANTI-PATTERN: Requiring account creation before showing any value
✅ CORRECT: Let users explore core features anonymously, then offer accounts for persistence
```

### 2. Value Before Commitment

Show meaningful value before asking for personal information:

```
WRONG ORDER:
1. Create account
2. Enter personal details
3. Grant permissions
4. Finally see the app

RIGHT ORDER:
1. Show immediate value (meeting finder, crisis resources)
2. Demonstrate app benefits
3. Offer optional account for saved data
4. Request permissions contextually
```

### 3. Non-Judgmental Language

Avoid shame-inducing or triggering language:

```
❌ "How many days since your last relapse?"
✅ "What's your current sobriety date?"

❌ "You failed to complete..."
✅ "No worries—pick up where you left off"

❌ "Are you an alcoholic or drug addict?"
✅ "Which recovery programs interest you?"
```

## Mobile Onboarding UX (2025 Best Practices)

### Progressive Disclosure

Break complex onboarding into digestible stages:

```tsx
// ✅ GOOD: Staged onboarding with clear progress
const ONBOARDING_STAGES = [
  { id: 'welcome', required: false },    // Emotional connection
  { id: 'programs', required: false },    // Personalization
  { id: 'features', required: false },    // Value discovery
  { id: 'preferences', required: false }, // Customization
  { id: 'safety', required: false },      // Crisis setup
];

// Each stage should be:
// - Skippable (never trap users)
// - Under 60 seconds to complete
// - Visually distinct with progress indicators
// - Reversible (can go back)
```

### Permission Priming (28% Higher Grant Rate)

Never request permissions out of context:

```tsx
// ❌ BAD: Immediate system permission dialog
useEffect(() => {
  requestLocationPermission();
}, []);

// ✅ GOOD: Contextual priming before system dialog
function MeetingSearchPrimer() {
  return (
    <div className="p-4 bg-blue-50 rounded-lg mb-4">
      <MapPin className="text-blue-500 mb-2" />
      <h3>Find Meetings Near You</h3>
      <p className="text-sm text-gray-600 mb-3">
        To show meetings within walking distance, we need your location.
        Your location stays on your device.
      </p>
      <button onClick={handleEnableLocation} className="btn-primary">
        Enable Location
      </button>
      <button onClick={handleSkip} className="btn-text">
        Search by ZIP instead
      </button>
    </div>
  );
}
```

### "Everboarding" - Beyond First Launch

Onboarding isn't a one-time event:

```tsx
// Feature discovery on first use of each feature
function useFeatureOnboarding(featureId: string) {
  const [hasSeenTooltip, setHasSeen] = useLocalStorage(`onboard:${featureId}`, false);

  return {
    showTooltip: !hasSeenTooltip,
    dismissTooltip: () => setHasSeen(true),
  };
}

// Example: First time using gratitude journal
function GratitudeJournal() {
  const { showTooltip, dismissTooltip } = useFeatureOnboarding('gratitude');

  return (
    <>
      {showTooltip && (
        <FeatureTooltip
          title="Daily Gratitude"
          description="Write 3 things you're grateful for. Research shows this builds resilience."
          onDismiss={dismissTooltip}
        />
      )}
      {/* Journal UI */}
    </>
  );
}
```

### Skeleton Loaders, Never Spinners

Recovery users in crisis need immediate feedback:

```tsx
// ❌ BAD: Spinner creates anxiety
{isLoading && <Loader2 className="animate-spin" />}

// ✅ GOOD: Skeleton shows structure immediately
{isLoading && <MeetingCardSkeleton count={5} />}

// Skeleton implementation
function MeetingCardSkeleton() {
  return (
    <div className="p-4 bg-leather-800 rounded-lg animate-pulse">
      <div className="h-4 bg-leather-700 rounded w-3/4 mb-2" />
      <div className="h-3 bg-leather-700 rounded w-1/2 mb-4" />
      <div className="flex gap-2">
        <div className="h-6 w-16 bg-leather-700 rounded" />
        <div className="h-6 w-16 bg-leather-700 rounded" />
      </div>
    </div>
  );
}
```

## Recovery App Feature Categories

### Essential Features (Showcase First)

1. **Meeting Finder** - Core utility, immediate value
2. **Crisis Resources** - Life-saving, always accessible
3. **Safety Planning** - Personal support network

### Engagement Features (Second Priority)

4. **Daily Check-ins** - HALT awareness
5. **Recovery Journal** - Reflection and growth
6. **Gratitude Practice** - Positive reinforcement

### Advanced Features (Discover Over Time)

7. **Sobriety Counter** - Milestone tracking
8. **Community Forum** - Peer support
9. **Recovery Plan** - AI-assisted guidance
10. **Online Meetings** - Virtual options

### Feature Card Pattern

```tsx
interface OnboardingFeature {
  id: string;
  icon: React.ComponentType;
  title: string;
  description: string;
  highlight: string;        // Key benefit (e.g., "24/7 support available")
  color: string;            // Brand color for visual distinction
  category: 'essential' | 'engagement' | 'advanced';
}

const FEATURES: OnboardingFeature[] = [
  {
    id: 'meetings',
    icon: MapPin,
    title: 'Find Meetings Near You',
    description: 'Search thousands of AA, NA, CMA, SMART, and other recovery meetings.',
    highlight: '100,000+ meetings nationwide',
    color: 'bg-blue-500',
    category: 'essential',
  },
  {
    id: 'crisis',
    icon: Phone,
    title: 'Crisis Resources',
    description: 'One-tap access to crisis hotlines and emergency support.',
    highlight: '24/7 support available',
    color: 'bg-red-500',
    category: 'essential',
  },
  // ... more features
];
```

## Crisis Resource Integration

**Critical**: Only 45% of mental health apps include crisis resources. This is non-negotiable for recovery apps.

### Always-Visible Crisis Access

```tsx
// Crisis resources should be accessible from EVERY screen
function Navigation() {
  return (
    <nav>
      {/* Normal nav items */}
      <CrisisButton className="fixed bottom-20 right-4" />
    </nav>
  );
}

// Crisis button design
function CrisisButton({ className }: { className?: string }) {
  return (
    <Link
      href="/crisis"
      className={cn(
        'flex items-center justify-center',
        'w-14 h-14 rounded-full',
        'bg-red-600 hover:bg-red-700',
        'shadow-lg shadow-red-600/30',
        'text-white',
        className
      )}
      aria-label="Crisis resources"
    >
      <Phone size={24} />
    </Link>
  );
}
```

### Onboarding Safety Plan Step

```tsx
// Include safety planning in onboarding, but make it optional
function SafetyPlanStep() {
  return (
    <div className="space-y-4">
      <h2>Your Safety Network</h2>
      <p className="text-gray-600">
        Having support contacts ready can make all the difference.
        This is optional—you can set this up anytime.
      </p>

      <EmergencyContactInput
        label="Emergency Contact"
        placeholder="Someone who can help in a crisis"
      />

      <SupportPersonInput
        label="Support Person"
        placeholder="Sponsor, therapist, or trusted friend"
      />

      <div className="flex gap-2 mt-6">
        <button className="btn-secondary flex-1" onClick={handleSkip}>
          Set Up Later
        </button>
        <button className="btn-primary flex-1" onClick={handleSave}>
          Save Contacts
        </button>
      </div>
    </div>
  );
}
```

## Recovery Program Selection

### Inclusive Multi-Selection

Support multiple recovery pathways without judgment:

```tsx
const RECOVERY_PROGRAMS = [
  { id: 'aa', name: 'Alcoholics Anonymous', short: 'AA', color: 'bg-blue-500' },
  { id: 'na', name: 'Narcotics Anonymous', short: 'NA', color: 'bg-purple-500' },
  { id: 'cma', name: 'Crystal Meth Anonymous', short: 'CMA', color: 'bg-pink-500' },
  { id: 'smart', name: 'SMART Recovery', short: 'SMART', color: 'bg-green-500' },
  { id: 'dharma', name: 'Recovery Dharma', short: 'Dharma', color: 'bg-amber-500' },
  { id: 'ha', name: 'Heroin Anonymous', short: 'HA', color: 'bg-red-500' },
  { id: 'oa', name: 'Overeaters Anonymous', short: 'OA', color: 'bg-teal-500' },
  { id: 'other', name: 'Other/Multiple', short: 'Other', color: 'bg-gray-500' },
];

// UI should allow multiple selections
function ProgramSelection({ selected, onChange }) {
  return (
    <div className="grid grid-cols-2 gap-3">
      {RECOVERY_PROGRAMS.map((program) => (
        <ProgramCard
          key={program.id}
          program={program}
          isSelected={selected.includes(program.id)}
          onToggle={() => toggleProgram(program.id)}
        />
      ))}
    </div>
  );
}
```

## Onboarding Flow Architecture

### State Management

```tsx
interface OnboardingState {
  currentStep: number;
  completedSteps: string[];
  selectedPrograms: string[];
  meetingPreferences: {
    formats: ('in-person' | 'online' | 'hybrid')[];
    days: string[];
    times: ('morning' | 'afternoon' | 'evening')[];
  };
  safetyContacts: {
    emergency?: string;
    support?: string;
  };
  skippedSteps: string[];
}

// Persist across sessions
function useOnboardingState() {
  return useLocalStorage<OnboardingState>('onboarding', defaultState);
}
```

### Step Navigation

```tsx
function OnboardingWizard() {
  const [state, setState] = useOnboardingState();
  const currentStep = STEPS[state.currentStep];

  const goNext = () => {
    setState(prev => ({
      ...prev,
      currentStep: Math.min(prev.currentStep + 1, STEPS.length - 1),
      completedSteps: [...prev.completedSteps, currentStep.id],
    }));
  };

  const goBack = () => {
    setState(prev => ({
      ...prev,
      currentStep: Math.max(prev.currentStep - 1, 0),
    }));
  };

  const skip = () => {
    setState(prev => ({
      ...prev,
      skippedSteps: [...prev.skippedSteps, currentStep.id],
    }));
    goNext();
  };

  return (
    <div className="min-h-screen flex flex-col">
      <ProgressIndicator
        current={state.currentStep}
        total={STEPS.length}
        completedSteps={state.completedSteps}
      />

      <main className="flex-1 p-4">
        <CurrentStepComponent {...currentStep} state={state} setState={setState} />
      </main>

      <footer className="p-4 border-t border-leather-700">
        <div className="flex gap-3">
          {state.currentStep > 0 && (
            <button onClick={goBack} className="btn-secondary flex-1">
              Back
            </button>
          )}
          {currentStep.skippable && (
            <button onClick={skip} className="btn-text">
              Skip
            </button>
          )}
          <button onClick={goNext} className="btn-primary flex-1">
            {state.currentStep === STEPS.length - 1 ? 'Get Started' : 'Continue'}
          </button>
        </div>
      </footer>
    </div>
  );
}
```

## Micro-Interactions

### Entry Animations

```tsx
// Staggered entrance for lists
function StaggeredList({ items, renderItem }) {
  return (
    <div className="space-y-3">
      {items.map((item, index) => (
        <div
          key={item.id}
          className="animate-fade-in-up"
          style={{ animationDelay: `${index * 100}ms` }}
        >
          {renderItem(item, index)}
        </div>
      ))}
    </div>
  );
}
```

### Carousel Navigation

```tsx
// Swipe gesture support for mobile feature tours
function useSwipeNavigation({ onNext, onPrev, threshold = 50 }) {
  const [touchStart, setTouchStart] = useState<number | null>(null);
  const [touchEnd, setTouchEnd] = useState<number | null>(null);

  const onTouchStart = (e: React.TouchEvent) => {
    setTouchEnd(null);
    setTouchStart(e.targetTouches[0].clientX);
  };

  const onTouchMove = (e: React.TouchEvent) => {
    setTouchEnd(e.targetTouches[0].clientX);
  };

  const onTouchEnd = () => {
    if (!touchStart || !touchEnd) return;
    const distance = touchStart - touchEnd;
    if (distance > threshold) onNext();
    if (distance < -threshold) onPrev();
  };

  return { onTouchStart, onTouchMove, onTouchEnd };
}
```

## Accessibility Requirements

### WCAG AA Compliance

- **Contrast**: 4.5:1 for text &lt; 18px, 3:1 for text &gt;= 18px
- **Touch targets**: Minimum 44x44px
- **Focus indicators**: Visible outline on all interactive elements
- **Screen readers**: Announce step changes with `aria-live`

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  .animate-fade-in-up,
  .animate-slide-in {
    animation: none;
    opacity: 1;
    transform: none;
  }
}
```

## Testing Checklist

### Functional Testing
- [ ] All steps can be completed
- [ ] All steps can be skipped
- [ ] Back navigation works
- [ ] Progress persists across sessions
- [ ] Swipe gestures work on mobile
- [ ] Keyboard navigation works

### Accessibility Testing
- [ ] Screen reader announces step changes
- [ ] All interactive elements have labels
- [ ] Focus order is logical
- [ ] Color contrast meets WCAG AA
- [ ] Touch targets are 44x44px minimum

### Performance Testing
- [ ] Initial load under 2 seconds
- [ ] Step transitions under 300ms
- [ ] No layout shifts during animations
- [ ] Works offline after first load

### Emotional Testing
- [ ] Language is non-judgmental
- [ ] Skip options are clear
- [ ] No pressure tactics
- [ ] Crisis resources visible
- [ ] Privacy messaging clear

## References

See `/references/` for detailed guides:
- `competitor-analysis.md` - I Am Sober, Nomo, Sober Grid patterns
- `wellness-patterns.md` - Headspace, Calm, Daylio insights
- `crisis-integration.md` - Emergency resource best practices
