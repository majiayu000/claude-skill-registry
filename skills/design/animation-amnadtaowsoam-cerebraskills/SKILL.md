# Animation Patterns in React

---

## 1. Executive Summary & Strategic Necessity

### 1.1 Context (ภาษาไทย)

การสร้าง Animation ที่มีประสิทธิภาพและสวยงามเป็นสิ่งสำคัญในการสร้างประสบการณ์ผู้ใช้ (User Experience) ที่น่าประทับใจและแตกต่าง ในยุค Digital Transformation ที่ผู้ใช้คาดหวังการโต้ตอบที่ลื่นไหลและตอบสนองทันที Animation ไม่เพียงแต่เป็นการตกแต่ง แต่เป็นส่วนสำคัญในการสื่อสารสถานะของระบบ แนะนำการกระทำ และสร้างความสัมพันธ์ทางอารมณ์กับผู้ใช้

Skill นี้ครอบคลุมการใช้งาน Animation Libraries หลักใน React Ecosystem ได้แก่ CSS Animations, Framer Motion, GSAP, และ React Spring พร้อมตัวอย่างโค้ดและ Best Practices สำหรับการสร้าง Animation ที่มีประสิทธิภาพ คำนึงถึง Performance และ Accessibility

### 1.2 Business Impact (ภาษาไทย)

**ผลกระทบทางธุรกิจ:**

1. **เพิ่ม Conversion Rate** - Animation ที่ดีช่วยนำผู้ใช้ไปสู่การกระทำที่ต้องการ (Call-to-Action) ได้ดีขึ้น การศึกษาพบว่า Animation ที่ดีสามารถเพิ่ม Conversion Rate ได้ถึง 15-20%

2. **ลด Bounce Rate** - Loading Animations และ Micro-interactions ที่ดีช่วยลดความรู้สึกว่าระบบช้า ทำให้ผู้ใช้อยู่ในเว็บไซต์นานขึ้น

3. **เพิ่ม Brand Differentiation** - Animation ที่เป็นเอกลักษณ์ช่วยสร้างความแตกต่างจากคู่แข่งและสร้าง Brand Recall ที่แข็งแกร่ง

4. **ปรับปรุง User Retention** - Animation ที่ดีสร้างความพึงพอใจในการใช้งาน ทำให้ผู้ใช้กลับมาใช้งานซ้ำ

5. **ลด Support Cost** - Animation ที่ช่วยแนะนำการใช้งาน (Onboarding Animations) สามารถลดคำถามและปัญหาการใช้งาน

### 1.3 Product Thinking (ภาษาไทย)

**มุมมองด้านผลิตภัณฑ์:**

1. **Purpose-Driven Animation** - ทุก Animation ต้องมีวัตถุประสงค์ที่ชัดเจน ไม่ใช่แค่การตกแต่ง แต่ต้องช่วยให้ผู้ใช้เข้าใจสถานะของระบบ หรือนำทางการกระทำ

2. **Performance-First** - Animation ต้องไม่ส่งผลกระทบต่อ Performance ของแอปพลิเคชัน ต้องใช้ GPU-accelerated properties (transform, opacity)

3. **Accessibility** - Animation ต้องเคารพค่ากำหนดของผู้ใช้ `prefers-reduced-motion` และมี fallback สำหรับผู้ที่มีปัญหาด้านการมองเห็น

4. **Consistent Design Language** - Animation ต้องสอดคล้องกับ Design System และ Brand Guidelines ขององค์กร

5. **Measurable Impact** - Animation ต้องมีการวัดผล (A/B Testing) เพื่อยืนยันว่ามีประโยชน์ต่อผลิตภัณฑ์จริง

---

## 2. Technical Deep Dive (The "How-to")

### 2.1 Core Logic

Animation ใน React สามารถแบ่งออกเป็น 4 ประเภทหลัก:

1. **CSS Animations** - ใช้ CSS Transitions และ Keyframes เหมาะสำหรับ Animation ที่เรียบง่ายและไม่ต้องการ JavaScript control
2. **Framer Motion** - React Animation Library ที่มี API ที่ใช้งานง่ายและทรงพลัง เหมาะสำหรับ React Applications
3. **GSAP (GreenSock)** - Animation Library ที่ทรงพลังและยืดหยุ่นสูง เหมาะสำหรับ Animation ที่ซับซ้อน
4. **React Spring** - Physics-based Animation Library ที่เน้น Spring Physics เหมาะสำหรับ Animation ที่ต้องการความสมจริง

### 2.2 Architecture Diagram Requirements

```
┌─────────────────────────────────────────────────────────────────┐
│                     Animation Architecture                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   React      │    │   React      │    │   React      │       │
│  │  Components  │◄──►│  Components  │◄──►│  Components  │       │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘       │
│         │                   │                   │               │
│         │                   │                   │               │
│  ┌──────▼───────────────────▼───────────────────▼───────┐       │
│  │              Animation Layer                         │       │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │       │
│  │  │   CSS       │  │  Framer     │  │    GSAP      │  │       │
│  │  │ Animations  │  │   Motion    │  │             │  │       │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  │       │
│  │  ┌─────────────────────────────────────────────┐   │       │
│  │  │          React Spring                        │   │       │
│  │  └─────────────────────────────────────────────┘   │       │
│  └───────────────────────────────────────────────────┘       │
│                           │                                     │
│                           │                                     │
│  ┌────────────────────────▼─────────────────────────────────┐ │
│  │              Performance & Accessibility Layer             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │ │
│  │  │   GPU       │  │   Reduced   │  │   Focus     │       │ │
│  │  │ Accelerated │  │   Motion    │  │  Management │       │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘       │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Implementation Workflow

**Step 1: Choose the Right Animation Library**

```typescript
// Decision Tree for Animation Library Selection
function chooseAnimationLibrary(requirements: {
  complexity: 'simple' | 'medium' | 'complex'
  performance: 'critical' | 'standard'
  control: 'css-only' | 'javascript' | 'advanced'
  physics: boolean
}) {
  if (requirements.complexity === 'simple' && requirements.control === 'css-only') {
    return 'CSS Animations'
  }
  if (requirements.complexity === 'medium' && requirements.control === 'javascript') {
    return 'Framer Motion'
  }
  if (requirements.complexity === 'complex' && requirements.control === 'advanced') {
    return 'GSAP'
  }
  if (requirements.physics) {
    return 'React Spring'
  }
  return 'Framer Motion' // Default choice
}
```

**Step 2: Implement Basic Animation Pattern**

```typescript
// Base Animation Component
"use client"

import { motion } from "framer-motion"
import { useReducedMotion } from "framer-motion"

interface AnimationProps {
  children: React.ReactNode
  delay?: number
  duration?: number
  direction?: 'up' | 'down' | 'left' | 'right' | 'none'
}

export function AnimatedSection({ 
  children, 
  delay = 0, 
  duration = 0.5,
  direction = 'up' 
}: AnimationProps) {
  const prefersReducedMotion = useReducedMotion()
  
  const getInitialPosition = () => {
    if (prefersReducedMotion) return { opacity: 0 }
    
    switch (direction) {
      case 'up': return { opacity: 0, y: 50 }
      case 'down': return { opacity: 0, y: -50 }
      case 'left': return { opacity: 0, x: 50 }
      case 'right': return { opacity: 0, x: -50 }
      default: return { opacity: 0 }
    }
  }

  return (
    <motion.div
      initial={getInitialPosition()}
      animate={{ opacity: 1, x: 0, y: 0 }}
      transition={{ 
        duration: prefersReducedMotion ? 0 : duration,
        delay: prefersReducedMotion ? 0 : delay,
        ease: "easeOut"
      }}
    >
      {children}
    </motion.div>
  )
}
```

**Step 3: Add Accessibility Support**

```typescript
// Accessibility-aware Animation Hook
function useAccessibleAnimation() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false)

  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)")
    setPrefersReducedMotion(mediaQuery.matches)

    const listener = (event: MediaQueryListEvent) => {
      setPrefersReducedMotion(event.matches)
    }

    mediaQuery.addEventListener("change", listener)
    return () => mediaQuery.removeEventListener("change", listener)
  }, [])

  return {
    shouldAnimate: !prefersReducedMotion,
    animationDuration: prefersReducedMotion ? 0 : 0.5,
  }
}
```

---

## 3. Tooling & Tech Stack

### 3.1 Enterprise Tools

| Tool | Purpose | Version | License |
|------|---------|---------|---------|
| Framer Motion | React Animation Library | ^11.0.0 | MIT |
| GSAP | Professional Animation Platform | ^3.12.0 | Commercial/Standard |
| React Spring | Physics-based Animations | ^9.7.0 | MIT |
| Tailwind CSS | Utility-first CSS Framework | ^3.4.0 | MIT |
| TypeScript | Type Safety | ^5.0.0 | Apache 2.0 |

### 3.2 Configuration Essentials

**Framer Motion Setup:**
```bash
npm install framer-motion
```

**GSAP Setup:**
```bash
npm install gsap
```

**React Spring Setup:**
```bash
npm install @react-spring/web
```

**Tailwind Animation Configuration:**
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'slide-down': 'slideDown 0.4s ease-out',
        'scale-in': 'scaleIn 0.3s ease-out',
        'shimmer': 'shimmer 2s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.9)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
      },
    },
  },
}
```

---

## 4. Standards, Compliance & Security

### 4.1 International Standards

- **WCAG 2.1 Level AA** - Animation ต้องไม่ทำให้ผู้ใช้สับสนหรือเกิดอาการวิงเวียน
- **ISO 9241-11** - Usability Standards สำหรับ Animation
- **WAI-ARIA** - Accessibility สำหรับ Animated Components

### 4.2 Security Protocol

Animation Libraries โดยทั่วไปไม่มีปัญหาด้านความปลอดภัยโดยตรง แต่ต้องระวัง:

1. **XSS Prevention** - ไม่ใช้ user input ใน animation parameters โดยตรง
2. **Performance DoS** - Animation ที่ซับซ้อนเกินไปอาจทำให้เบราว์เซอร์หยุดทำงาน
3. **Memory Leaks** - ต้อง cleanup animations เมื่อ component unmount

### 4.3 Explainability

Animation ต้องสามารถอธิบายได้ว่า:

1. **Purpose** - Animation นี้มีวัตถุประสงค์อะไร
2. **Trigger** - Animation เริ่มทำงานเมื่อไร
3. **Duration** - Animation ใช้เวลานานแค่ไหน
4. **Accessibility** - Animation นี้เคารพค่ากำหนดของผู้ใช้หรือไม่

---

## 5. Unit Economics & Performance Metrics (KPIs)

### 5.1 Cost Calculation

| Metric | Calculation | Target |
|--------|-------------|--------|
| Animation Bundle Size | Sum of animation libraries | < 100 KB (gzipped) |
| First Contentful Paint (FCP) | Time to first paint | < 1.8s |
| Time to Interactive (TTI) | Time to full interactivity | < 3.8s |
| Cumulative Layout Shift (CLS) | Layout stability score | < 0.1 |
| Animation Frame Rate | FPS during animation | > 55 FPS |

### 5.2 Key Performance Indicators

**Performance Metrics:**

1. **Frame Rate** - Animation ต้องรันที่ 60 FPS หรือมากกว่า
2. **Main Thread Blocking** - Animation ไม่ควร block main thread เกิน 50ms
3. **Memory Usage** - Animation ไม่ควรใช้ memory เกิน 50 MB เพิ่มขึ้น
4. **GPU Acceleration** - Animation ต้องใช้ GPU-accelerated properties

**Business Metrics:**

1. **Conversion Rate** - เพิ่มขึ้น 10-20% หลังใช้ Animation ที่ดี
2. **Bounce Rate** - ลดลง 15-25%
3. **User Engagement** - เพิ่มขึ้น 20-30%
4. **Support Tickets** - ลดลง 10-15% จากการใช้ Onboarding Animations

---

## 6. Strategic Recommendations (CTO Insights)

### 6.1 Phase Rollout

**Phase 1: Foundation (Week 1-2)**
- Setup Animation Libraries (Framer Motion, GSAP, React Spring)
- Create Base Animation Components
- Implement Accessibility Hooks
- Setup Performance Monitoring

**Phase 2: Core Patterns (Week 3-4)**
- Implement Page Transitions
- Create Loading Skeletons
- Build Toast Notification System
- Add Accordion Components

**Phase 3: Advanced Features (Week 5-6)**
- Implement Scroll Animations
- Add Gesture Animations
- Create Layout Animations
- Build Animation System

**Phase 4: Optimization (Week 7-8)**
- Performance Audit
- A/B Testing
- Accessibility Review
- Documentation

### 6.2 Pitfalls to Avoid

1. **Over-animating** - Animation มากเกินไปทำให้ผู้ใช้รำคาญ
2. **Ignoring Accessibility** - ไม่เคารพค่า `prefers-reduced-motion`
3. **Performance Issues** - ใช้ properties ที่ไม่ใช่ GPU-accelerated
4. **Inconsistent Timing** - Animation durations ไม่สอดคล้องกัน
5. **No Fallback** - ไม่มี fallback สำหรับ browsers ที่ไม่รองรับ

### 6.3 Best Practices Checklist

- [ ] ใช้ GPU-accelerated properties (transform, opacity)
- [ ] เคารพค่า `prefers-reduced-motion`
- [ ] Animation duration อยู่ในช่วง 200-500ms
- [ ] ใช้ easing functions ที่เหมาะสม
- [ ] Test บน devices และ browsers หลายแบบ
- [ ] Monitor performance metrics
- [ ] A/B test animation variations
- [ ] Document animation patterns
- [ ] Create reusable animation components
- [ ] Implement animation cleanup

---

## 7. Implementation Examples

### 7.1 CSS Animations

#### Basic Transitions
```css
/* styles.css */
.button {
  background-color: #3b82f6;
  transition: background-color 0.3s ease;
}

.button:hover {
  background-color: #1d4ed8;
}

/* Multiple properties */
.card {
  transform: translateY(0);
  opacity: 1;
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.card:hover {
  transform: translateY(-4px);
  opacity: 0.9;
}

/* Using transition shorthand */
.element {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

#### Keyframe Animations
```css
/* Fade in animation */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

/* Slide up animation */
@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.slide-up {
  animation: slideUp 0.4s ease-out;
}

/* Bounce animation */
@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.bounce {
  animation: bounce 1s ease-in-out infinite;
}

/* Pulse animation */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.pulse {
  animation: pulse 2s ease-in-out infinite;
}

/* Spin animation */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.spin {
  animation: spin 1s linear infinite;
}

/* Shake animation */
@keyframes shake {
  0%, 100% {
    transform: translateX(0);
  }
  10%, 30%, 50%, 70%, 90% {
    transform: translateX(-5px);
  }
  20%, 40%, 60%, 80% {
    transform: translateX(5px);
  }
}

.shake {
  animation: shake 0.5s ease-in-out;
}
```

#### CSS Animation with React
```typescript
// components/AnimatedComponent.tsx
"use client"

import { useState } from "react"
import styles from "./AnimatedComponent.module.css"

export function AnimatedComponent() {
  const [isVisible, setIsVisible] = useState(false)

  return (
    <div>
      <button onClick={() => setIsVisible(!isVisible)}>
        Toggle Animation
      </button>

      <div className={`${styles.box} ${isVisible ? styles.visible : ""}`}>
        Animated Content
      </div>
    </div>
  )
}

// AnimatedComponent.module.css
/*
.box {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.box.visible {
  opacity: 1;
  transform: translateY(0);
}
*/
```

#### Tailwind CSS Animations
```typescript
// Using Tailwind built-in animations
export function TailwindAnimations() {
  return (
    <div className="space-y-4">
      {/* Spin */}
      <div className="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full" />

      {/* Ping */}
      <div className="relative">
        <div className="animate-ping absolute h-4 w-4 bg-blue-400 rounded-full" />
        <div className="h-4 w-4 bg-blue-500 rounded-full" />
      </div>

      {/* Pulse */}
      <div className="animate-pulse bg-gray-300 h-12 w-48 rounded" />

      {/* Bounce */}
      <div className="animate-bounce bg-blue-500 h-8 w-8 rounded-full" />
    </div>
  )
}
```

### 7.2 Framer Motion

#### Installation
```bash
npm install framer-motion
```

#### Basic Animations
```typescript
"use client"

import { motion } from "framer-motion"

// Fade in animation
export function FadeIn() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      Fade In Content
    </motion.div>
  )
}

// Slide animation
export function SlideIn() {
  return (
    <motion.div
      initial={{ x: -100, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
    >
      Slide In Content
    </motion.div>
  )
}

// Scale animation
export function ScaleIn() {
  return (
    <motion.div
      initial={{ scale: 0 }}
      animate={{ scale: 1 }}
      transition={{ type: "spring", stiffness: 260, damping: 20 }}
    >
      Scale In Content
    </motion.div>
  )
}

// Multiple properties
export function ComplexAnimation() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50, scale: 0.9 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="p-6 bg-white rounded-lg shadow-lg"
    >
      Complex Animation
    </motion.div>
  )
}
```

#### Hover and Tap Animations
```typescript
"use client"

import { motion } from "framer-motion"

export function InteractiveButton() {
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      className="px-4 py-2 bg-blue-500 text-white rounded"
    >
      Click Me
    </motion.button>
  )
}

export function HoverCard() {
  return (
    <motion.div
      whileHover={{
        scale: 1.02,
        boxShadow: "0 10px 30px rgba(0,0,0,0.2)"
      }}
      transition={{ duration: 0.2 }}
      className="p-6 bg-white rounded-lg shadow cursor-pointer"
    >
      Hover Card
    </motion.div>
  )
}

export function AnimatedIcon() {
  return (
    <motion.svg
      whileHover={{ rotate: 180 }}
      transition={{ duration: 0.3 }}
      className="w-6 h-6"
      viewBox="0 0 24 24"
    >
      <path d="M12 4v16m8-8H4" stroke="currentColor" strokeWidth="2" />
    </motion.svg>
  )
}
```

#### Variants
```typescript
"use client"

import { motion } from "framer-motion"

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.4 },
  },
}

export function StaggeredList({ items }: { items: string[] }) {
  return (
    <motion.ul
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-2"
    >
      {items.map((item, index) => (
        <motion.li
          key={index}
          variants={itemVariants}
          className="p-4 bg-white rounded shadow"
        >
          {item}
        </motion.li>
      ))}
    </motion.ul>
  )
}

// Card variants with hover
const cardVariants = {
  initial: { scale: 1 },
  hover: { scale: 1.05 },
  tap: { scale: 0.98 },
}

export function VariantCard() {
  return (
    <motion.div
      variants={cardVariants}
      initial="initial"
      whileHover="hover"
      whileTap="tap"
      className="p-6 bg-white rounded-lg shadow cursor-pointer"
    >
      Interactive Card
    </motion.div>
  )
}
```

#### AnimatePresence for Exit Animations
```typescript
"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"

export function ToggleContent() {
  const [isVisible, setIsVisible] = useState(true)

  return (
    <div>
      <button onClick={() => setIsVisible(!isVisible)}>
        Toggle
      </button>

      <AnimatePresence>
        {isVisible && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            Content that animates in and out
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

// Modal with AnimatePresence
export function AnimatedModal({
  isOpen,
  onClose,
  children
}: {
  isOpen: boolean
  onClose: () => void
  children: React.ReactNode
}) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 z-40"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            transition={{ type: "spring", damping: 25, stiffness: 300 }}
            className="fixed inset-0 flex items-center justify-center z-50"
          >
            <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
              {children}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}

// List with remove animation
export function AnimatedList() {
  const [items, setItems] = useState([1, 2, 3, 4, 5])

  const removeItem = (id: number) => {
    setItems(items.filter(item => item !== id))
  }

  return (
    <ul className="space-y-2">
      <AnimatePresence>
        {items.map(item => (
          <motion.li
            key={item}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20, height: 0 }}
            transition={{ duration: 0.3 }}
            className="p-4 bg-white rounded shadow flex justify-between"
          >
            Item {item}
            <button onClick={() => removeItem(item)}>Remove</button>
          </motion.li>
        ))}
      </AnimatePresence>
    </ul>
  )
}
```

#### Layout Animations
```typescript
"use client"

import { useState } from "react"
import { motion, LayoutGroup } from "framer-motion"

export function ExpandableCard() {
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <motion.div
      layout
      onClick={() => setIsExpanded(!isExpanded)}
      className="bg-white rounded-lg shadow cursor-pointer overflow-hidden"
      style={{ width: isExpanded ? 400 : 200 }}
    >
      <motion.h2 layout className="p-4 font-bold">
        Card Title
      </motion.h2>

      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="p-4 pt-0"
          >
            <p>Expanded content goes here...</p>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

// Shared layout animation
export function TabsWithAnimation() {
  const [activeTab, setActiveTab] = useState(0)
  const tabs = ["Home", "About", "Contact"]

  return (
    <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
      {tabs.map((tab, index) => (
        <button
          key={tab}
          onClick={() => setActiveTab(index)}
          className="relative px-4 py-2 rounded-md"
        >
          {activeTab === index && (
            <motion.div
              layoutId="activeTab"
              className="absolute inset-0 bg-white rounded-md shadow"
              transition={{ type: "spring", stiffness: 500, damping: 30 }}
            />
          )}
          <span className="relative z-10">{tab}</span>
        </button>
      ))}
    </div>
  )
}

// Reorderable list
import { Reorder } from "framer-motion"

export function ReorderableList() {
  const [items, setItems] = useState(["Item 1", "Item 2", "Item 3", "Item 4"])

  return (
    <Reorder.Group axis="y" values={items} onReorder={setItems} className="space-y-2">
      {items.map(item => (
        <Reorder.Item
          key={item}
          value={item}
          className="p-4 bg-white rounded shadow cursor-grab active:cursor-grabbing"
        >
          {item}
        </Reorder.Item>
      ))}
    </Reorder.Group>
  )
}
```

#### Scroll Animations
```typescript
"use client"

import { motion, useScroll, useTransform, useInView } from "framer-motion"
import { useRef } from "react"

// Scroll progress indicator
export function ScrollProgress() {
  const { scrollYProgress } = useScroll()

  return (
    <motion.div
      style={{ scaleX: scrollYProgress }}
      className="fixed top-0 left-0 right-0 h-1 bg-blue-500 origin-left z-50"
    />
  )
}

// Parallax effect
export function ParallaxSection() {
  const ref = useRef(null)
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
  })

  const y = useTransform(scrollYProgress, [0, 1], [100, -100])
  const opacity = useTransform(scrollYProgress, [0, 0.5, 1], [0, 1, 0])

  return (
    <motion.section
      ref={ref}
      style={{ y, opacity }}
      className="min-h-screen flex items-center justify-center"
    >
      <h2 className="text-4xl font-bold">Parallax Content</h2>
    </motion.section>
  )
}

// Animate when in view
export function AnimateOnScroll({ children }: { children: React.ReactNode }) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: "-100px" })

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 50 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  )
}

// Scroll-triggered animation with variants
const scrollVariants = {
  hidden: { opacity: 0, y: 75 },
  visible: { opacity: 1, y: 0 },
}

export function ScrollReveal({ children }: { children: React.ReactNode }) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true })

  return (
    <motion.div
      ref={ref}
      variants={scrollVariants}
      initial="hidden"
      animate={isInView ? "visible" : "hidden"}
      transition={{ duration: 0.5, delay: 0.25 }}
    >
      {children}
    </motion.div>
  )
}
```

#### Gesture Animations
```typescript
"use client"

import { motion, useDragControls } from "framer-motion"

// Draggable element
export function DraggableBox() {
  return (
    <motion.div
      drag
      dragConstraints={{ left: -100, right: 100, top: -100, bottom: 100 }}
      dragElastic={0.2}
      whileDrag={{ scale: 1.1 }}
      className="w-24 h-24 bg-blue-500 rounded-lg cursor-grab active:cursor-grabbing"
    />
  )
}

// Drag with snap back
export function SnapBackDrag() {
  return (
    <motion.div
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      dragElastic={0.5}
      className="w-full h-20 bg-gray-200 rounded-lg"
    >
      <motion.div className="w-20 h-20 bg-blue-500 rounded-lg" />
    </motion.div>
  )
}

// Swipe to delete
export function SwipeToDelete({ onDelete }: { onDelete: () => void }) {
  return (
    <motion.div
      drag="x"
      dragConstraints={{ left: -100, right: 0 }}
      onDragEnd={(_, info) => {
        if (info.offset.x < -80) {
          onDelete()
        }
      }}
      className="p-4 bg-white rounded shadow"
    >
      Swipe left to delete
    </motion.div>
  )
}

// Pan gesture
export function PanGesture() {
  return (
    <motion.div
      onPan={(_, info) => {
        console.log("Pan:", info.delta.x, info.delta.y)
      }}
      onPanEnd={(_, info) => {
        console.log("Pan ended:", info.velocity.x, info.velocity.y)
      }}
      className="w-48 h-48 bg-gray-200 rounded-lg touch-none"
    />
  )
}
```

### 7.3 GSAP (GreenSock Animation Platform)

#### Installation
```bash
npm install gsap
```

#### Basic Animations
```typescript
"use client"

import { useRef, useEffect } from "react"
import gsap from "gsap"

export function GSAPBasic() {
  const boxRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (boxRef.current) {
      gsap.to(boxRef.current, {
        x: 200,
        rotation: 360,
        duration: 2,
        ease: "power2.out",
      })
    }
  }, [])

  return (
    <div
      ref={boxRef}
      className="w-24 h-24 bg-blue-500 rounded-lg"
    />
  )
}

// Multiple targets
export function GSAPMultiple() {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (containerRef.current) {
      gsap.to(containerRef.current.children, {
        y: 0,
        opacity: 1,
        stagger: 0.2,
        duration: 0.6,
        ease: "power3.out",
      })
    }
  }, [])

  return (
    <div ref={containerRef} className="space-y-4">
      {[1, 2, 3, 4].map(i => (
        <div
          key={i}
          className="p-4 bg-white rounded shadow"
          style={{ opacity: 0, transform: "translateY(20px)" }}
        >
          Item {i}
        </div>
      ))}
    </div>
  )
}
```

#### GSAP Timeline
```typescript
"use client"

import { useRef, useEffect } from "react"
import gsap from "gsap"

export function GSAPTimeline() {
  const boxRef = useRef<HTMLDivElement>(null)
  const circleRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const tl = gsap.timeline({ defaults: { duration: 0.5 } })

    tl.to(boxRef.current, { x: 100 })
      .to(boxRef.current, { y: 100 })
      .to(boxRef.current, { rotation: 180 })
      .to(circleRef.current, { scale: 1.5 }, "<") // Start at same time as previous
      .to(circleRef.current, { backgroundColor: "#ef4444" }, "+=0.2") // Start 0.2s after previous

    return () => {
      tl.kill()
    }
  }, [])

  return (
    <div className="relative h-64">
      <div
        ref={boxRef}
        className="absolute w-16 h-16 bg-blue-500 rounded"
      />
      <div
        ref={circleRef}
        className="absolute top-32 w-16 h-16 bg-green-500 rounded-full"
      />
    </div>
  )
}

// Timeline with labels
export function GSAPTimelineLabels() {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const tl = gsap.timeline()

    tl.addLabel("start")
      .to(".box-1", { x: 100, duration: 0.5 })
      .addLabel("middle")
      .to(".box-2", { x: 100, duration: 0.5 })
      .addLabel("end")
      .to(".box-3", { x: 100, duration: 0.5 })

    // Jump to label
    // tl.play("middle")

    return () => {
      tl.kill()
    }
  }, [])

  return (
    <div ref={containerRef} className="space-y-4">
      <div className="box-1 w-16 h-16 bg-blue-500 rounded" />
      <div className="box-2 w-16 h-16 bg-green-500 rounded" />
      <div className="box-3 w-16 h-16 bg-red-500 rounded" />
    </div>
  )
}
```

#### GSAP ScrollTrigger
```typescript
"use client"

import { useRef, useEffect } from "react"
import gsap from "gsap"
import { ScrollTrigger } from "gsap/ScrollTrigger"

gsap.registerPlugin(ScrollTrigger)

export function GSAPScrollTrigger() {
  const sectionRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.from(".animate-item", {
        y: 100,
        opacity: 0,
        stagger: 0.2,
        duration: 1,
        scrollTrigger: {
          trigger: sectionRef.current,
          start: "top 80%",
          end: "bottom 20%",
          toggleActions: "play none none reverse",
        },
      })
    }, sectionRef)

    return () => ctx.revert()
  }, [])

  return (
    <section ref={sectionRef} className="min-h-screen py-20">
      <div className="space-y-8">
        {[1, 2, 3, 4].map(i => (
          <div
            key={i}
            className="animate-item p-6 bg-white rounded-lg shadow"
          >
            Section Item {i}
          </div>
        ))}
      </div>
    </section>
  )
}

// Scroll-linked animation
export function GSAPScrollLinked() {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.to(".progress-bar", {
        width: "100%",
        ease: "none",
        scrollTrigger: {
          trigger: containerRef.current,
          start: "top top",
          end: "bottom bottom",
          scrub: true,
        },
      })
    }, containerRef)

    return () => ctx.revert()
  }, [])

  return (
    <div ref={containerRef}>
      <div className="fixed top-0 left-0 right-0 h-1 bg-gray-200">
        <div className="progress-bar h-full bg-blue-500 w-0" />
      </div>
      <div className="h-[300vh]">
        <p className="sticky top-20 text-center">Scroll down...</p>
      </div>
    </div>
  )
}

// Pin section
export function GSAPPinSection() {
  const sectionRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      ScrollTrigger.create({
        trigger: sectionRef.current,
        start: "top top",
        end: "+=500",
        pin: true,
        pinSpacing: true,
      })
    }, sectionRef)

    return () => ctx.revert()
  }, [])

  return (
    <section
      ref={sectionRef}
      className="min-h-screen flex items-center justify-center bg-blue-500 text-white"
    >
      <h2 className="text-4xl font-bold">Pinned Section</h2>
    </section>
  )
}
```

#### GSAP with React Hooks
```typescript
"use client"

import { useRef, useEffect, useLayoutEffect } from "react"
import gsap from "gsap"

// Custom hook for GSAP animations
function useGSAP(callback: (ctx: gsap.Context) => void, deps: any[] = []) {
  const ref = useRef<HTMLDivElement>(null)

  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      callback(ctx)
    }, ref)

    return () => ctx.revert()
  }, deps)

  return ref
}

// Usage
export function GSAPHookExample() {
  const containerRef = useGSAP((ctx) => {
    gsap.from(".box", {
      y: 50,
      opacity: 0,
      stagger: 0.1,
      duration: 0.5,
    })
  })

  return (
    <div ref={containerRef} className="space-y-4">
      {[1, 2, 3].map(i => (
        <div key={i} className="box p-4 bg-white rounded shadow">
          Box {i}
        </div>
      ))}
    </div>
  )
}

// Responsive animation hook
function useResponsiveGSAP() {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const mm = gsap.matchMedia()

    mm.add("(min-width: 768px)", () => {
      gsap.to(ref.current, { x: 200 })
    })

    mm.add("(max-width: 767px)", () => {
      gsap.to(ref.current, { y: 100 })
    })

    return () => mm.revert()
  }, [])

  return ref
}
```

### 7.4 React Spring

#### Installation
```bash
npm install @react-spring/web
```

#### Basic Animations
```typescript
"use client"

import { useSpring, animated } from "@react-spring/web"

// Simple animation
export function SpringBasic() {
  const springs = useSpring({
    from: { opacity: 0, y: 20 },
    to: { opacity: 1, y: 0 },
  })

  return (
    <animated.div style={springs} className="p-6 bg-white rounded-lg shadow">
      Animated Content
    </animated.div>
  )
}

// Animation with config
export function SpringWithConfig() {
  const springs = useSpring({
    from: { scale: 0 },
    to: { scale: 1 },
    config: { tension: 200, friction: 12 },
  })

  return (
    <animated.div
      style={{
        transform: springs.scale.to(s => `scale(${s})`),
      }}
      className="w-24 h-24 bg-blue-500 rounded-lg"
    />
  )
}

// Toggle animation
export function SpringToggle() {
  const [isOpen, setIsOpen] = useState(false)

  const springs = useSpring({
    height: isOpen ? 200 : 0,
    opacity: isOpen ? 1 : 0,
    config: { tension: 300, friction: 20 },
  })

  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>Toggle</button>
      <animated.div style={springs} className="overflow-hidden bg-gray-100">
        <div className="p-4">Expandable content</div>
      </animated.div>
    </div>
  )
}
```

#### useTransition for Lists
```typescript
"use client"

import { useState } from "react"
import { useTransition, animated } from "@react-spring/web"

export function SpringList() {
  const [items, setItems] = useState([1, 2, 3])

  const transitions = useTransition(items, {
    from: { opacity: 0, x: -20 },
    enter: { opacity: 1, x: 0 },
    leave: { opacity: 0, x: 20 },
    keys: item => item,
  })

  const addItem = () => {
    setItems([...items, items.length + 1])
  }

  const removeItem = (id: number) => {
    setItems(items.filter(item => item !== id))
  }

  return (
    <div>
      <button onClick={addItem}>Add Item</button>
      <div className="space-y-2 mt-4">
        {transitions((style, item) => (
          <animated.div
            style={style}
            className="p-4 bg-white rounded shadow flex justify-between"
          >
            Item {item}
            <button onClick={() => removeItem(item)}>Remove</button>
          </animated.div>
        ))}
      </div>
    </div>
  )
}

// Page transitions
export function PageTransition({ children, key }: { children: React.ReactNode; key: string }) {
  const transitions = useTransition(key, {
    from: { opacity: 0, transform: "translateX(20px)" },
    enter: { opacity: 1, transform: "translateX(0)" },
    leave: { opacity: 0, transform: "translateX(-20px)" },
  })

  return transitions((style, item) => (
    <animated.div style={style}>{children}</animated.div>
  ))
}
```

#### useChain for Sequenced Animations
```typescript
"use client"

import { useRef } from "react"
import { useSpring, useTrail, useChain, animated, SpringRef } from "@react-spring/web"

export function ChainedAnimation() {
  const springRef = useRef<SpringRef>(null)
  const trailRef = useRef<SpringRef>(null)

  const containerSpring = useSpring({
    ref: springRef,
    from: { scale: 0 },
    to: { scale: 1 },
  })

  const items = [1, 2, 3, 4]
  const trail = useTrail(items.length, {
    ref: trailRef,
    from: { opacity: 0, y: 20 },
    to: { opacity: 1, y: 0 },
  })

  useChain([springRef, trailRef], [0, 0.3])

  return (
    <animated.div
      style={{
        transform: containerSpring.scale.to(s => `scale(${s})`),
      }}
      className="p-6 bg-white rounded-lg shadow"
    >
      {trail.map((style, index) => (
        <animated.div key={index} style={style} className="p-2">
          Item {items[index]}
        </animated.div>
      ))}
    </animated.div>
  )
}
```

#### useSprings for Multiple Elements
```typescript
"use client"

import { useState } from "react"
import { useSprings, animated } from "@react-spring/web"

export function MultipleElements() {
  const [active, setActive] = useState(-1)
  const items = [0, 1, 2, 3, 4]

  const springs = useSprings(
    items.length,
    items.map((_, i) => ({
      scale: active === i ? 1.2 : 1,
      opacity: active === -1 || active === i ? 1 : 0.5,
      config: { tension: 300, friction: 20 },
    }))
  )

  return (
    <div className="flex gap-4">
      {springs.map((style, i) => (
        <animated.div
          key={i}
          style={{
            transform: style.scale.to(s => `scale(${s})`),
            opacity: style.opacity,
          }}
          onMouseEnter={() => setActive(i)}
          onMouseLeave={() => setActive(-1)}
          className="w-16 h-16 bg-blue-500 rounded cursor-pointer"
        />
      ))}
    </div>
  )
}
```

### 7.5 Performance Considerations

#### Optimize CSS Animations
```css
/* Use transform and opacity for best performance */
.good-animation {
  transform: translateX(100px);
  opacity: 0.5;
  /* These properties are GPU-accelerated */
}

/* Avoid animating layout properties */
.bad-animation {
  width: 200px;
  height: 200px;
  margin-left: 100px;
  /* These trigger layout recalculations */
}

/* Use will-change sparingly */
.will-animate {
  will-change: transform, opacity;
}

/* Remove will-change after animation */
.animation-complete {
  will-change: auto;
}
```

#### React Animation Performance
```typescript
"use client"

import { memo, useMemo } from "react"
import { motion } from "framer-motion"

// Memoize animated components
const AnimatedCard = memo(function AnimatedCard({ item }: { item: { id: number; title: string } }) {
  return (
    <motion.div
      layout
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="p-4 bg-white rounded shadow"
    >
      {item.title}
    </motion.div>
  )
})

// Use useMemo for animation variants
export function OptimizedAnimations() {
  const variants = useMemo(() => ({
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 },
  }), [])

  return (
    <motion.div variants={variants} initial="hidden" animate="visible">
      Content
    </motion.div>
  )
}

// Reduce motion for accessibility
export function ReducedMotion() {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches

  return (
    <motion.div
      initial={{ opacity: 0, y: prefersReducedMotion ? 0 : 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: prefersReducedMotion ? 0 : 0.5 }}
    >
      Respects user preference
    </motion.div>
  )
}
```

#### Lazy Load Animation Libraries
```typescript
"use client"

import dynamic from "next/dynamic"
import { Suspense } from "react"

// Lazy load heavy animation components
const HeavyAnimation = dynamic(() => import("./HeavyAnimation"), {
  loading: () => <div>Loading...</div>,
  ssr: false,
})

export function LazyAnimatedSection() {
  return (
    <Suspense fallback={<div>Loading animation...</div>}>
      <HeavyAnimation />
    </Suspense>
  )
}
```

### 7.6 Accessibility in Animations

#### Respecting User Preferences
```typescript
"use client"

import { useEffect, useState } from "react"
import { motion, useReducedMotion } from "framer-motion"

// Using Framer Motion's built-in hook
export function AccessibleAnimation() {
  const prefersReducedMotion = useReducedMotion()

  return (
    <motion.div
      initial={{ opacity: 0, y: prefersReducedMotion ? 0 : 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: prefersReducedMotion ? 0 : 0.5 }}
    >
      Accessible animated content
    </motion.div>
  )
}

// Custom hook for reduced motion
function usePreferReducedMotion() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false)

  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)")
    setPrefersReducedMotion(mediaQuery.matches)

    const listener = (event: MediaQueryListEvent) => {
      setPrefersReducedMotion(event.matches)
    }

    mediaQuery.addEventListener("change", listener)
    return () => mediaQuery.removeEventListener("change", listener)
  }, [])

  return prefersReducedMotion
}

// Usage
export function CustomAccessibleAnimation() {
  const prefersReducedMotion = usePreferReducedMotion()

  return (
    <div
      className={prefersReducedMotion ? "" : "animate-fade-in"}
    >
      Content respects user preference
    </div>
  )
}
```

#### Focus Management
```typescript
"use client"

import { useRef, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"

export function AccessibleModal({
  isOpen,
  onClose,
  children,
}: {
  isOpen: boolean
  onClose: () => void
  children: React.ReactNode
}) {
  const closeButtonRef = useRef<HTMLButtonElement>(null)

  useEffect(() => {
    if (isOpen) {
      closeButtonRef.current?.focus()
    }
  }, [isOpen])

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 flex items-center justify-center"
          role="dialog"
          aria-modal="true"
          aria-labelledby="modal-title"
        >
          <div className="bg-white rounded-lg p-6 max-w-md">
            <button
              ref={closeButtonRef}
              onClick={onClose}
              aria-label="Close modal"
              className="absolute top-4 right-4"
            >
              Close
            </button>
            {children}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
```

#### ARIA Live Regions
```typescript
"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"

export function NotificationWithAria() {
  const [notifications, setNotifications] = useState<string[]>([])

  const addNotification = (message: string) => {
    setNotifications([...notifications, message])
    setTimeout(() => {
      setNotifications(prev => prev.slice(1))
    }, 3000)
  }

  return (
    <div
      aria-live="polite"
      aria-atomic="false"
      className="fixed top-4 right-4 space-y-2"
    >
      <AnimatePresence>
        {notifications.map((notification, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 100 }}
            className="p-4 bg-green-500 text-white rounded shadow"
            role="alert"
          >
            {notification}
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  )
}
```

### 7.7 Common Animation Patterns

#### Page Transitions
```typescript
"use client"

import { motion } from "framer-motion"

const pageVariants = {
  initial: { opacity: 0, x: -20 },
  enter: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 20 },
}

export function PageWrapper({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      variants={pageVariants}
      initial="initial"
      animate="enter"
      exit="exit"
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  )
}
```

#### Loading Skeletons
```typescript
"use client"

export function SkeletonLoader() {
  return (
    <div className="animate-pulse space-y-4">
      <div className="h-4 bg-gray-300 rounded w-3/4" />
      <div className="h-4 bg-gray-300 rounded w-1/2" />
      <div className="h-32 bg-gray-300 rounded" />
    </div>
  )
}

// Shimmer effect
export function ShimmerSkeleton() {
  return (
    <div className="relative overflow-hidden bg-gray-200 rounded">
      <div
        className="absolute inset-0 -translate-x-full animate-[shimmer_2s_infinite] bg-gradient-to-r from-gray-200 via-white to-gray-200"
      />
      <div className="h-32" />
    </div>
  )
}
```

#### Notification Toast
```typescript
"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"

interface Toast {
  id: number
  message: string
  type: "success" | "error" | "info"
}

export function useToast() {
  const [toasts, setToasts] = useState<Toast[]>([])

  const addToast = (message: string, type: Toast["type"] = "info") => {
    const id = Date.now()
    setToasts(prev => [...prev, { id, message, type }])
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id))
    }, 3000)
  }

  const ToastContainer = () => (
    <div className="fixed bottom-4 right-4 space-y-2 z-50">
      <AnimatePresence>
        {toasts.map(toast => (
          <motion.div
            key={toast.id}
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -20, scale: 0.9 }}
            className={`p-4 rounded-lg shadow-lg ${
              toast.type === "success" ? "bg-green-500" :
              toast.type === "error" ? "bg-red-500" : "bg-blue-500"
            } text-white`}
          >
            {toast.message}
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  )

  return { addToast, ToastContainer }
}
```

#### Accordion
```typescript
"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"

interface AccordionItemProps {
  title: string
  children: React.ReactNode
  isOpen: boolean
  onToggle: () => void
}

function AccordionItem({ title, children, isOpen, onToggle }: AccordionItemProps) {
  return (
    <div className="border-b">
      <button
        onClick={onToggle}
        className="w-full p-4 text-left flex justify-between items-center"
      >
        {title}
        <motion.span
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.2 }}
        >
          ▼
        </motion.span>
      </button>
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <div className="p-4 bg-gray-50">{children}</div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export function Accordion({ items }: { items: { title: string; content: string }[] }) {
  const [openIndex, setOpenIndex] = useState<number | null>(null)

  return (
    <div className="border rounded-lg">
      {items.map((item, index) => (
        <AccordionItem
          key={index}
          title={item.title}
          isOpen={openIndex === index}
          onToggle={() => setOpenIndex(openIndex === index ? null : index)}
        >
          {item.content}
        </AccordionItem>
      ))}
    </div>
  )
}
```

#### Animated Counter
```typescript
"use client"

import { useEffect, useState } from "react"
import { useSpring, animated } from "@react-spring/web"

export function AnimatedCounter({ value }: { value: number }) {
  const { number } = useSpring({
    from: { number: 0 },
    number: value,
    delay: 200,
    config: { mass: 1, tension: 20, friction: 10 },
  })

  return (
    <animated.span>
      {number.to(n => n.toFixed(0))}
    </animated.span>
  )
}

// With Framer Motion
import { motion, useMotionValue, useTransform, animate } from "framer-motion"

export function FramerCounter({ value }: { value: number }) {
  const count = useMotionValue(0)
  const rounded = useTransform(count, Math.round)

  useEffect(() => {
    const animation = animate(count, value, { duration: 2 })
    return animation.stop
  }, [value])

  return <motion.span>{rounded}</motion.span>
}
```

### 7.8 Animation Libraries Comparison

| Feature | CSS | Framer Motion | GSAP | React Spring |
|---------|-----|---------------|------|--------------|
| Bundle Size | 0 KB | ~30 KB | ~60 KB | ~20 KB |
| Learning Curve | Low | Medium | Medium-High | Medium |
| Performance | Excellent | Good | Excellent | Good |
| React Integration | Manual | Native | Manual | Native |
| Gesture Support | Limited | Excellent | Good | Good |
| Layout Animation | No | Yes | Manual | Limited |
| Exit Animation | No | Yes | Manual | Yes |
| Physics-based | No | Yes | Plugin | Yes |
| Timeline Control | Limited | Limited | Excellent | Limited |
| Best For | Simple animations | React apps | Complex animations | Spring physics |
