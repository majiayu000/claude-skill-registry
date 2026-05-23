---
name: recovery-app-ui
description: Build recovery-focused UI components for 12-step companion apps including clean time trackers, daily check-ins, milestone celebrations, and progress visualizations. Use when creating sobriety counters, check-in forms, anniversary displays, step work progress bars, or any recovery-specific interface elements.
---

# Recovery App UI Components

Specialized UI patterns for 12-step recovery companion apps.

## Clean Time Tracker

Display sobriety duration with multiple time units:

```typescript
interface CleanTimeProps {
  soberDate: Date;
  onShare?: () => void;
}

function CleanTimeTracker({ soberDate, onShare }: CleanTimeProps) {
  const [duration, setDuration] = useState(() => calculateDuration(soberDate));

  useEffect(() => {
    const timer = setInterval(() => {
      setDuration(calculateDuration(soberDate));
    }, 60000); // Update every minute
    return () => clearInterval(timer);
  }, [soberDate]);

  return (
    <View className="bg-slate-900 rounded-2xl p-6 items-center">
      <Text className="text-slate-400 text-sm mb-2">Clean Time</Text>

      <View className="flex-row gap-4">
        <TimeUnit value={duration.years} label="Years" />
        <TimeUnit value={duration.months} label="Months" />
        <TimeUnit value={duration.days} label="Days" />
      </View>

      <View className="flex-row gap-2 mt-4">
        <TimeUnitSmall value={duration.hours} label="hrs" />
        <TimeUnitSmall value={duration.minutes} label="min" />
      </View>

      <TouchableOpacity onPress={onShare} className="mt-4">
        <Text className="text-violet-400">Share Progress</Text>
      </TouchableOpacity>
    </View>
  );
}

function TimeUnit({ value, label }: { value: number; label: string }) {
  return (
    <View className="items-center min-w-[70px]">
      <Text className="text-4xl font-bold text-white">{value}</Text>
      <Text className="text-slate-400 text-xs">{label}</Text>
    </View>
  );
}
```

## Daily Check-In Card

Quick emotional/symptom tracking:

```typescript
interface DailyCheckInProps {
  onSubmit: (data: CheckInData) => void;
  streak: number;
}

interface CheckInData {
  mood: number; // 1-5
  cravingIntensity: number; // 0-10
  sleepQuality: number;
  notes: string;
}

function DailyCheckIn({ onSubmit, streak }: DailyCheckInProps) {
  const [mood, setMood] = useState(3);
  const [craving, setCraving] = useState(0);

  return (
    <View className="bg-slate-800 rounded-xl p-4">
      <View className="flex-row justify-between items-center mb-4">
        <Text className="text-white font-semibold">Daily Check-In</Text>
        <StreakBadge count={streak} />
      </View>

      {/* Mood Selector */}
      <Text className="text-slate-400 text-sm mb-2">How are you feeling?</Text>
      <View className="flex-row justify-between">
        {[1, 2, 3, 4, 5].map((value) => (
          <MoodButton
            key={value}
            value={value}
            selected={mood === value}
            onPress={() => setMood(value)}
          />
        ))}
      </View>

      {/* Craving Slider */}
      <Text className="text-slate-400 text-sm mt-4 mb-2">
        Craving intensity: {craving}/10
      </Text>
      <Slider
        value={craving}
        onValueChange={setCraving}
        minimumValue={0}
        maximumValue={10}
        step={1}
        minimumTrackTintColor="#8b5cf6"
        maximumTrackTintColor="#334155"
      />

      <Button
        title="Save Check-In"
        onPress={() => onSubmit({ mood, cravingIntensity: craving })}
      />
    </View>
  );
}

function MoodButton({ value, selected, onPress }: MoodButtonProps) {
  const emojis = ['😢', '😕', '😐', '🙂', '😊'];

  return (
    <TouchableOpacity
      onPress={onPress}
      className={`w-12 h-12 rounded-full items-center justify-center ${
        selected ? 'bg-violet-600' : 'bg-slate-700'
      }`}
    >
      <Text className="text-2xl">{emojis[value - 1]}</Text>
    </TouchableOpacity>
  );
}

function StreakBadge({ count }: { count: number }) {
  return (
    <View className="flex-row items-center bg-orange-500/20 px-3 py-1 rounded-full">
      <Text className="text-orange-400 mr-1">🔥</Text>
      <Text className="text-orange-400 font-semibold">{count}</Text>
    </View>
  );
}
```

## Milestone Celebration

Anniversary and achievement displays:

```typescript
interface Milestone {
  id: string;
  title: string;
  days: number;
  icon: string;
  achieved: boolean;
  achievedAt?: Date;
}

function MilestoneCard({ milestone }: { milestone: Milestone }) {
  if (!milestone.achieved) {
    return (
      <View className="bg-slate-800/50 rounded-xl p-4 opacity-50">
        <Text className="text-slate-500">{milestone.title}</Text>
        <Text className="text-slate-600 text-sm">{milestone.days} days</Text>
      </View>
    );
  }

  return (
    <View className="bg-gradient-to-br from-violet-600 to-purple-700 rounded-xl p-4">
      <View className="flex-row items-center">
        <Text className="text-4xl mr-3">{milestone.icon}</Text>
        <View>
          <Text className="text-white font-bold text-lg">{milestone.title}</Text>
          <Text className="text-violet-200 text-sm">
            Achieved {formatDate(milestone.achievedAt!)}
          </Text>
        </View>
      </View>
    </View>
  );
}

function MilestoneCelebration({ milestone, onDismiss }: CelebrationProps) {
  const confettiRef = useRef<ConfettiCannon>(null);

  useEffect(() => {
    confettiRef.current?.start();
  }, []);

  return (
    <Modal animationType="fade" transparent>
      <View className="flex-1 bg-black/80 justify-center items-center p-6">
        <View className="bg-slate-900 rounded-2xl p-6 items-center w-full max-w-sm">
          <Text className="text-6xl mb-4">{milestone.icon}</Text>
          <Text className="text-white text-2xl font-bold text-center">
            {milestone.title}
          </Text>
          <Text className="text-slate-400 text-center mt-2">
            Congratulations on {milestone.days} days of recovery!
          </Text>
          <Button title="Continue" onPress={onDismiss} className="mt-6" />
        </View>
        <ConfettiCannon ref={confettiRef} count={100} origin={{ x: 200, y: 0 }} />
      </View>
    </Modal>
  );
}
```

## Step Work Progress

Visual progress through 12 steps:

```typescript
function StepWorkProgress({ currentStep, completedSteps }: StepProgressProps) {
  return (
    <View className="bg-slate-800 rounded-xl p-4">
      <Text className="text-white font-semibold mb-4">Step Work Progress</Text>

      <View className="flex-row flex-wrap gap-2">
        {Array.from({ length: 12 }, (_, i) => i + 1).map((step) => (
          <StepIndicator
            key={step}
            step={step}
            status={
              completedSteps.includes(step)
                ? 'completed'
                : step === currentStep
                ? 'current'
                : 'locked'
            }
          />
        ))}
      </View>
    </View>
  );
}

function StepIndicator({ step, status }: StepIndicatorProps) {
  const styles = {
    completed: 'bg-green-600',
    current: 'bg-violet-600 ring-2 ring-violet-400',
    locked: 'bg-slate-700',
  };

  return (
    <View
      className={`w-10 h-10 rounded-full items-center justify-center ${styles[status]}`}
    >
      {status === 'completed' ? (
        <Check size={20} color="white" />
      ) : (
        <Text className="text-white font-semibold">{step}</Text>
      )}
    </View>
  );
}
```

## Emergency Support Button

Prominent help access:

```typescript
function EmergencySupportButton({ onPress }: { onPress: () => void }) {
  const scale = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  const pulse = () => {
    scale.value = withSequence(
      withSpring(1.1),
      withSpring(1)
    );
  };

  return (
    <Animated.View style={animatedStyle}>
      <TouchableOpacity
        onPress={() => {
          pulse();
          onPress();
        }}
        className="bg-red-600 rounded-full px-6 py-4 flex-row items-center justify-center"
      >
        <Phone size={20} color="white" />
        <Text className="text-white font-bold ml-2">Get Help Now</Text>
      </TouchableOpacity>
    </Animated.View>
  );
}
```

## Design Principles

1. **Calming colors** - Use slate, violet, and soft tones (avoid triggering reds)
2. **Gentle celebrations** - Milestones should feel supportive, not overwhelming
3. **Privacy-first** - Sensitive data behind biometric/auth gates
4. **Quick access** - Emergency resources one tap away
5. **Non-judgmental** - Neutral language, no shame-based messaging
6. **Accessibility** - Large touch targets, high contrast, screen reader support
