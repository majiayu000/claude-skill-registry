---
name: mobile-ui
description: Mobile UI patterns, gestures, animations, and platform-specific design.
---

# Mobile UI

## Animations

### Reanimated

```typescript
import Animated, {
  useAnimatedStyle,
  useSharedValue,
  withSpring,
} from 'react-native-reanimated';

function AnimatedCard() {
  const scale = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  const onPressIn = () => {
    scale.value = withSpring(0.95);
  };

  const onPressOut = () => {
    scale.value = withSpring(1);
  };

  return (
    <Pressable onPressIn={onPressIn} onPressOut={onPressOut}>
      <Animated.View style={[styles.card, animatedStyle]}>
        {/* content */}
      </Animated.View>
    </Pressable>
  );
}
```

## Gestures

```typescript
import { Gesture, GestureDetector } from 'react-native-gesture-handler';

function SwipeableCard() {
  const translateX = useSharedValue(0);

  const pan = Gesture.Pan()
    .onUpdate((e) => {
      translateX.value = e.translationX;
    })
    .onEnd(() => {
      if (Math.abs(translateX.value) > THRESHOLD) {
        // Swipe action
      }
      translateX.value = withSpring(0);
    });

  return (
    <GestureDetector gesture={pan}>
      <Animated.View style={animatedStyle} />
    </GestureDetector>
  );
}
```

## Bottom Sheet

```typescript
import BottomSheet from '@gorhom/bottom-sheet';

function MyBottomSheet() {
  const snapPoints = useMemo(() => ['25%', '50%', '90%'], []);

  return (
    <BottomSheet snapPoints={snapPoints}>
      <View>{/* content */}</View>
    </BottomSheet>
  );
}
```

## Platform Design

### iOS

- Use SF Symbols for icons
- Respect safe areas
- Native feel: swipe to go back

### Android

- Material Design 3
- Status bar styling
- Back button handling
