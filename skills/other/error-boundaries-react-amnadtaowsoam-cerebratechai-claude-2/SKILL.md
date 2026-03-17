# Error Boundaries in React

---

## 1. Executive Summary & Strategic Necessity

### 1.1 Context (ภาษาไทย)

Error Boundaries เป็นคุณลักษณะที่สำคัญใน React ที่ช่วยจัดการข้อผิดพลาด (Error Handling) ในแอปพลิเคชัน React โดยการจับ JavaScript errors ที่เกิดขึ้นใน component tree และแสดง fallback UI แทนที่จะทำให้ทั้งแอปพลิเคชัน crash นี่เป็นสิ่งสำคัญในการสร้างแอปพลิเคชันที่มีความเสถียรและให้ประสบการณ์ผู้ใช้ที่ดี

Error Boundaries ถูกนำเสนอใน React 16 และเป็นส่วนสำคัญของการสร้างแอปพลิเคชัน React ที่มีความทนทาน (Resilient) และสามารถกู้คืนจากข้อผิดพลาดได้อย่างสวยงาม

### 1.2 Business Impact (ภาษาไทย)

**ผลกระทบทางธุรกิจ:**

1. **ลด Downtime** - Error Boundaries ช่วยลดเวลาที่แอปพลิเคชันไม่สามารถใช้งานได้เนื่องจากข้อผิดพลาด โดยการจับและจัดการข้อผิดพลาดในระดับ component แทนที่จะทำให้ทั้งแอป crash

2. **เพิ่ม User Retention** - ผู้ใช้มักจะออกจากแอปพลิเคชันที่มีข้อผิดพลาดบ่อย Error Boundaries ช่วยให้แอปพลิเคชันยังคงใช้งานได้แม้จะมีข้อผิดพลาดในบางส่วน

3. **ลด Support Cost** - Error Reporting ที่ดีช่วยให้ทีมพัฒนาสามารถระบุและแก้ไขปัญหาได้เร็วขึ้น ทำให้ลดคำถามและปัญหาจากผู้ใช้

4. **เพิ่ม Trust** - แอปพลิเคชันที่มีการจัดการข้อผิดพลาดที่ดีสร้างความไว้วางใจให้กับผู้ใช้

5. **ปรับปรุง User Experience** - Fallback UI ที่ดีช่วยให้ผู้ใช้เข้าใจสถานการณ์และมีตัวเลือกในการกู้คืน

### 1.3 Product Thinking (ภาษาไทย)

**มุมมองด้านผลิตภัณฑ์:**

1. **Graceful Degradation** - Error Boundaries ช่วยให้แอปพลิเคชันสามารถทำงานได้แม้จะมีบางส่วนที่ไม่ทำงาน ผู้ใช้ยังสามารถใช้งานส่วนอื่นๆ ของแอปพลิเคชันได้

2. **Error Recovery** - ให้ผู้ใช้มีตัวเลือกในการกู้คืนจากข้อผิดพลาด เช่น Retry, Go Home, Contact Support

3. **Contextual Error Messages** - Error messages ต้องเข้าใจง่ายและให้ข้อมูลที่เป็นประโยชน์แก่ผู้ใช้

4. **Error Tracking** - Error reporting ต้องมี context เพียงพอสำหรับการ debug เช่น component stack, user info, environment

5. **User-Centric Design** - Fallback UI ต้องออกแบบให้ใช้งานง่ายและให้ผู้ใช้มีความรู้สึกดีแม้จะเกิดข้อผิดพลาด

---

## 2. Technical Deep Dive (The "How-to")

### 2.1 Core Logic

Error Boundaries คือ React components ที่:
1. จับ JavaScript errors ใน component tree ของตนเอง
2. Log errors สำหรับการ debug
3. แสดง fallback UI แทน component tree ที่ crashed

**สิ่งที่ Error Boundaries จับได้:**
- Rendering errors
- Errors ใน lifecycle methods
- Errors ใน constructors

**สิ่งที่ Error Boundaries ไม่จับได้:**
- Event handlers
- Asynchronous code (setTimeout, promises)
- Server-side rendering errors
- Errors ที่เกิดใน error boundary เอง

### 2.2 Architecture Diagram Requirements

```
┌─────────────────────────────────────────────────────────────────┐
│                  Error Boundary Architecture                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │              Global Error Boundary                        │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │         App Component                             │  │   │
│  │  │                                                   │  │   │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐ │  │   │
│  │  │  │   Header    │  │  Feature 1  │  │  Footer   │ │  │   │
│  │  │  └─────────────┘  └──────┬──────┘  └───────────┘ │  │   │
│  │  │                       │                          │  │   │
│  │  │  ┌─────────────────────▼──────────────────────┐  │  │   │
│  │  │  │      Feature Error Boundary               │  │  │   │
│  │  │  │  ┌─────────────┐  ┌─────────────┐        │  │   │
│  │  │  │  │ Component A │  │ Component B │        │  │   │
│  │  │  │  └─────────────┘  └─────────────┘        │  │   │
│  │  │  │                                           │  │   │
│  │  │  │  ┌─────────────┐  ┌─────────────┐        │  │   │
│  │  │  │  │ Component C │  │ Component D │        │  │   │
│  │  │  │  └─────────────┘  └─────────────┘        │  │   │
│  │  │  └───────────────────────────────────────────┘  │  │   │
│  │  │                                                   │  │   │
│  │  │  ┌─────────────────────────────────────────────┐  │  │   │
│  │  │  │      Error Reporting Service               │  │  │   │
│  │  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐ │  │   │
│  │  │  │  │  Sentry │  │LogRocket│  │ Custom  │ │  │   │
│  │  │  │  └─────────┘  └─────────┘  └─────────┘ │  │   │
│  │  │  └─────────────────────────────────────────────┘  │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │              Fallback UI Layer                            │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │   Simple    │  │   Detailed  │  │   Themed    │     │   │
│  │  │  Fallback   │  │  Fallback   │  │  Fallback   │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Implementation Workflow

**Step 1: Create Base Error Boundary Component**

```typescript
// components/ErrorBoundary.tsx
import React, { Component, ErrorInfo, ReactNode } from 'react'

interface Props {
  children: ReactNode
  fallback?: ReactNode
  onError?: (error: Error, errorInfo: ErrorInfo) => void
}

interface State {
  hasError: boolean
  error: Error | null
  errorInfo: ErrorInfo | null
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false, error: null, errorInfo: null }
  }

  static getDerivedStateFromError(error: Error): State {
    // Update state so the next render will show the fallback UI
    return { hasError: true, error, errorInfo: null }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log the error to an error reporting service
    console.error('Error caught by boundary:', error, errorInfo)
    
    // Call custom error handler
    this.props.onError?.(error, errorInfo)
    
    // Store error info for display
    this.setState({ errorInfo })
  }

  resetError = () => {
    this.setState({ hasError: false, error: null, errorInfo: null })
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback
      }
      
      // Default fallback
      return (
        <div className="error-boundary">
          <h2>Something went wrong</h2>
          {this.state.error && (
            <p className="error-message">{this.state.error.message}</p>
          )}
          <button onClick={this.resetError}>Try Again</button>
        </div>
      )
    }

    return this.props.children
  }
}
```

**Step 2: Create Error Reporting Service**

```typescript
// services/ErrorReportingService.ts
import * as Sentry from '@sentry/react'

export class ErrorReportingService {
  static async report(error: Error, errorInfo?: ErrorInfo, context?: Record<string, any>) {
    // Send to Sentry
    Sentry.withScope((scope) => {
      if (errorInfo) {
        scope.setExtra('componentStack', errorInfo.componentStack)
      }
      
      // Add custom context
      if (context) {
        Object.entries(context).forEach(([key, value]) => {
          scope.setExtra(key, value)
        })
      }
      
      scope.setTag('errorBoundary', 'true')
      Sentry.captureException(error)
    })
    
    // Also log to console in development
    if (process.env.NODE_ENV === 'development') {
      console.error('Error reported:', error, errorInfo, context)
    }
  }
  
  static setUser(user: { id: string; email?: string; username?: string }) {
    Sentry.setUser(user)
  }
  
  static setTag(key: string, value: string) {
    Sentry.setTag(key, value)
  }
  
  static clearUser() {
    Sentry.setUser(null)
  }
}
```

**Step 3: Create Fallback UI Components**

```typescript
// components/ErrorFallback.tsx
import React from 'react'

interface SimpleFallbackProps {
  error?: Error | null
  onReset?: () => void
}

export function SimpleFallback({ error, onReset }: SimpleFallbackProps) {
  return (
    <div className="error-boundary simple">
      <h2>Something went wrong</h2>
      <p>We're sorry for the inconvenience.</p>
      {error && <p className="error-message">{error.message}</p>}
      {onReset && <button onClick={onReset}>Try Again</button>}
    </div>
  )
}

interface DetailedFallbackProps {
  error?: Error | null
  errorInfo?: ErrorInfo | null
  onReset?: () => void
  eventId?: string
}

export function DetailedFallback({ error, errorInfo, onReset, eventId }: DetailedFallbackProps) {
  return (
    <div className="error-boundary detailed">
      <div className="error-icon">⚠️</div>
      <h2>Oops! Something went wrong</h2>
      
      <div className="error-details">
        <h3>Error Message</h3>
        <p>{error?.message || 'Unknown error'}</p>
        
        {errorInfo && (
          <details>
            <summary>Technical Details</summary>
            <pre>{errorInfo.componentStack}</pre>
          </details>
        )}
      </div>
      
      <div className="error-actions">
        {onReset && (
          <button onClick={onReset} className="btn-primary">
            Try Again
          </button>
        )}
        <button onClick={() => window.location.href = '/'} className="btn-secondary">
          Go Home
        </button>
        <button onClick={() => window.location.reload()} className="btn-tertiary">
          Reload Page
        </button>
      </div>
      
      {eventId && (
        <p className="error-event-id">
          Error ID: <code>{eventId}</code>
        </p>
      )}
      
      <p className="error-contact">
        Need help? <a href="/support">Contact Support</a>
      </p>
    </div>
  )
}
```

**Step 4: Implement Placement Strategy**

```typescript
// App.tsx
import { ErrorBoundary } from './components/ErrorBoundary'
import { DetailedFallback } from './components/ErrorFallback'
import { ErrorReportingService } from './services/ErrorReportingService'

function App() {
  return (
    // Global boundary for catastrophic errors
    <ErrorBoundary
      fallback={<DetailedFallback />}
      onError={(error, errorInfo) => {
        ErrorReportingService.report(error, errorInfo, {
          location: 'global',
          timestamp: new Date().toISOString(),
        })
      }}
    >
      <div className="app-layout">
        <Header />
        
        <main>
          {/* Feature-specific boundaries */}
          <ErrorBoundary
            fallback={
              <DetailedFallback
                error={null}
                onReset={() => window.location.href = '/dashboard'}
              />
            }
            onError={(error, errorInfo) => {
              ErrorReportingService.report(error, errorInfo, {
                location: 'dashboard',
                feature: 'dashboard',
              })
            }}
          >
            <Dashboard />
          </ErrorBoundary>
          
          <ErrorBoundary
            fallback={
              <DetailedFallback
                error={null}
                onReset={() => window.location.href = '/projects'}
              />
            }
            onError={(error, errorInfo) => {
              ErrorReportingService.report(error, errorInfo, {
                location: 'projects',
                feature: 'projects',
              })
            }}
          >
            <Projects />
          </ErrorBoundary>
        </main>
        
        <Footer />
      </div>
    </ErrorBoundary>
  )
}
```

---

## 3. Tooling & Tech Stack

### 3.1 Enterprise Tools

| Tool | Purpose | Version | License |
|------|---------|---------|---------|
| React | UI Library | ^18.0.0 | MIT |
| react-error-boundary | Error Boundary Library | ^4.0.0 | MIT |
| Sentry | Error Tracking | ^7.0.0 | Commercial/Free |
| LogRocket | Session Recording | ^3.0.0 | Commercial |
| TypeScript | Type Safety | ^5.0.0 | Apache 2.0 |

### 3.2 Configuration Essentials

**Sentry Setup:**
```typescript
// sentry.ts
import * as Sentry from '@sentry/react'
import { BrowserTracing } from '@sentry/tracing'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  release: process.env.NEXT_PUBLIC_APP_VERSION,
  
  integrations: [
    new BrowserTracing(),
    new Sentry.Replay({
      maskAllText: true,
      blockAllMedia: true,
    }),
  ],
  
  tracesSampleRate: 0.1,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  
  beforeSend(event) {
    // Filter out sensitive data
    if (event.request?.cookies) {
      delete event.request.cookies
    }
    return event
  },
})
```

**react-error-boundary Setup:**
```bash
npm install react-error-boundary
```

```typescript
// ErrorBoundaryProvider.tsx
import { ErrorBoundary } from 'react-error-boundary'

export function AppErrorBoundary({ children }: { children: React.ReactNode }) {
  const logError = (error: Error, info: { componentStack: string }) => {
    console.error('Error caught by boundary:', error, info)
    // Send to error tracking service
    ErrorReportingService.report(error, info)
  }

  return (
    <ErrorBoundary
      FallbackComponent={DetailedFallback}
      onError={logError}
      onReset={() => {
        // Optional: reset app state
        window.location.href = '/'
      }}
    >
      {children}
    </ErrorBoundary>
  )
}
```

---

## 4. Standards, Compliance & Security

### 4.1 International Standards

- **WCAG 2.1 Level AA** - Error messages ต้องเข้าถึงได้และเข้าใจง่าย
- **ISO 25010** - Quality Model สำหรับ Reliability และ Recoverability
- **OWASP** - Error Handling Best Practices สำหรับ Security

### 4.2 Security Protocol

Error Boundaries ต้องปฏิบัติตามหลักความปลอดภัย:

1. **No Sensitive Data in Errors** - ไม่แสดงข้อมูลที่ละเอียดอ่อนใน error messages
2. **Error Logging** - Log errors อย่างปลอดภัยโดยไม่เก็บข้อมูลส่วนบุคคล
3. **Sanitization** - Sanitize error messages ก่อนแสดงใน UI
4. **Rate Limiting** - จำกัดจำนวน errors ที่ส่งไปยัง error tracking service

```typescript
// Secure Error Reporting
export class SecureErrorReportingService {
  static sanitizeError(error: Error): Error {
    // Remove sensitive data from error message
    const sanitizedMessage = error.message
      .replace(/password=["'][^"']*["']/gi, 'password="***"')
      .replace(/token=["'][^"']*["']/gi, 'token="***"')
      .replace(/api[_-]?key=["'][^"']*["']/gi, 'api_key="***"')
    
    return new Error(sanitizedMessage)
  }
  
  static report(error: Error, errorInfo?: ErrorInfo) {
    const sanitizedError = this.sanitizeError(error)
    // Send to error tracking service
    ErrorReportingService.report(sanitizedError, errorInfo)
  }
}
```

### 4.3 Explainability

Error Boundaries ต้องสามารถอธิบายได้ว่า:

1. **Error Context** - Error เกิดขึ้นที่ไหนและเมื่อไร
2. **User Impact** - Error นี้ส่งผลกระทบต่อผู้ใช้อย่างไร
3. **Recovery Path** - ผู้ใช้สามารถกู้คืนจาก error ได้อย่างไร
4. **Debug Information** - ข้อมูลที่จำเป็นสำหรับการ debug

---

## 5. Unit Economics & Performance Metrics (KPIs)

### 5.1 Cost Calculation

| Metric | Calculation | Target |
|--------|-------------|--------|
| Error Rate | Errors / Total Requests | < 0.1% |
| Crash Rate | Crashes / Total Sessions | < 0.01% |
| Recovery Rate | Recovered Errors / Total Errors | > 95% |
| MTTR (Mean Time To Recovery) | Average recovery time | < 5 min |
| Error Reporting Latency | Time to report error | < 1s |

### 5.2 Key Performance Indicators

**Technical Metrics:**

1. **Error Rate** - จำนวน errors ต่อจำนวน requests
2. **Crash Rate** - จำนวน crashes ต่อจำนวน sessions
3. **Recovery Rate** - อัตราการกู้คืนจาก errors
4. **Error Reporting Latency** - เวลาในการ report error

**Business Metrics:**

1. **User Retention** - อัตราการกลับมาใช้งานหลังจากเกิด error
2. **Support Tickets** - จำนวน support tickets ที่เกี่ยวข้องกับ errors
3. **User Satisfaction** - ความพึงพอใจของผู้ใช้หลังจากเกิด error
4. **Time to Resolution** - เวลาในการแก้ไข errors

---

## 6. Strategic Recommendations (CTO Insights)

### 6.1 Phase Rollout

**Phase 1: Foundation (Week 1-2)**
- Create base Error Boundary component
- Setup error reporting service (Sentry)
- Create fallback UI components
- Implement global error boundary

**Phase 2: Feature-Level Boundaries (Week 3-4)**
- Add feature-level error boundaries
- Implement contextual fallback UIs
- Add error reporting for each feature
- Test error boundaries with intentional errors

**Phase 3: Advanced Features (Week 5-6)**
- Implement retry mechanisms
- Add error rate monitoring
- Create error recovery strategies
- Implement error boundary composition

**Phase 4: Optimization (Week 7-8)**
- Performance audit
- Error rate analysis
- User feedback collection
- Documentation and training

### 6.2 Pitfalls to Avoid

1. **Over-Engineering** - Error boundaries มากเกินไปทำให้โค้ดซับซ้อน
2. **Ignoring Non-Catchable Errors** - ไม่จัดการ async errors และ event handler errors
3. **Poor Fallback UI** - Fallback UI ที่ไม่เป็นประโยชน์สำหรับผู้ใช้
4. **Missing Error Context** - Error reporting ไม่มี context เพียงพอ
5. **No Recovery Mechanism** - ไม่มีวิธีให้ผู้ใช้กู้คืนจาก errors

### 6.3 Best Practices Checklist

- [ ] ใช้ global error boundary สำหรับ catastrophic errors
- [ ] ใช้ feature-level error boundaries สำหรับ better UX
- [ ] Integrate กับ error tracking service (Sentry, LogRocket)
- [ ] Provide fallback UI ที่ชัดเจนและเป็นประโยชน์
- [ ] Implement retry mechanisms
- [ ] Log errors ด้วย context เพียงพอ
- [ ] Test error boundaries ด้วย intentional errors
- [ ] Monitor error rates และ set up alerts
- [ ] Sanitize error messages ก่อนแสดงใน UI
- [ ] Document error boundary patterns

---

## 7. Implementation Examples

### 7.1 Basic Error Boundary

```jsx
class ErrorBoundary extends React.Component {
  state = { hasError: false, error: null };
  
  static getDerivedStateFromError(error) {
    // Update state so next render shows fallback UI
    return { hasError: true, error };
  }
  
  render() {
    if (this.state.hasError) {
      return <FallbackUI error={this.state.error} />;
    }
    return this.props.children;
  }
}
```

### 7.2 Error Boundary with componentDidCatch

```jsx
class ErrorBoundary extends React.Component {
  state = { hasError: false, error: null, errorInfo: null };
  
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  
  componentDidCatch(error, errorInfo) {
    // Log error to an error reporting service
    logErrorToService(error, errorInfo);
    
    // Store error info for display
    this.setState({ errorInfo });
  }
  
  render() {
    if (this.state.hasError) {
      return <FallbackUI error={this.state.error} info={this.state.errorInfo} />;
    }
    return this.props.children;
  }
}

function logErrorToService(error, errorInfo) {
  // Send to Sentry, LogRocket, etc.
  Sentry.captureException(error, {
    contexts: {
      react: {
        componentStack: errorInfo.componentStack,
      },
    },
  });
}
```

### 7.3 Complete Error Boundary Example

```jsx
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }
  
  static getDerivedStateFromError(error) {
    // Update state to render fallback UI
    return { hasError: true };
  }
  
  componentDidCatch(error, errorInfo) {
    // Log error details
    console.error('Error caught by boundary:', error, errorInfo);
    
    // Send to error tracking service
    this.logError(error, errorInfo);
    
    // Store error info
    this.setState({
      error,
      errorInfo,
    });
  }
  
  logError(error, errorInfo) {
    // Example: Send to Sentry
    if (typeof Sentry !== 'undefined') {
      Sentry.withScope((scope) => {
        scope.setExtra('componentStack', errorInfo.componentStack);
        Sentry.captureException(error);
      });
    }
  }
  
  render() {
    if (this.state.hasError) {
      return this.props.fallback({
        error: this.state.error,
        errorInfo: this.state.errorInfo,
        resetError: this.resetError.bind(this),
      });
    }
    
    return this.props.children;
  }
  
  resetError() {
    this.setState({ hasError: false, error: null, errorInfo: null });
  }
}

// Usage
<ErrorBoundary
  fallback={({ error, resetError }) => (
    <div className="error-fallback">
      <h2>Something went wrong</h2>
      <p>{error?.message}</p>
      <button onClick={resetError}>Try Again</button>
    </div>
  )}
>
  <MyComponent />
</ErrorBoundary>
```

### 7.4 Error Boundary Limitations

```jsx
class MyComponent extends React.Component {
  handleClick() {
    // Event handlers are NOT caught
    try {
      throw new Error('Event handler error');
    } catch (error) {
      // Must handle manually
      console.error(error);
    }
  }
  
  async componentDidMount() {
    // Async errors are NOT caught
    try {
      const data = await fetchData();  // Error here won't be caught
    } catch (error) {
      // Must handle manually
      console.error(error);
    }
    
    // setTimeout errors are NOT caught
    setTimeout(() => {
      throw new Error('Timeout error');  // Won't be caught
    }, 1000);
  }
  
  render() {
    return <button onClick={this.handleClick}>Click me</button>;
  }
}
```

### 7.5 Handling Non-Catchable Errors

```jsx
// For async errors, wrap in try-catch
class MyComponent extends React.Component {
  state = { data: null, error: null };
  
  async componentDidMount() {
    try {
      const data = await fetchData();
      this.setState({ data });
    } catch (error) {
      this.setState({ error });
      // Log error
      logError(error);
    }
  }
  
  render() {
    if (this.state.error) {
      return <ErrorUI error={this.state.error} />;
    }
    if (!this.state.data) {
      return <LoadingUI />;
    }
    return <DataUI data={this.state.data} />;
  }
}
```

### 7.6 Placement Strategies

**Granular (Feature-Level):**

```jsx
function App() {
  return (
    <div>
      <ErrorBoundary fallback={<ProfileError />}>
        <ProfileSection />
      </ErrorBoundary>
      
      <ErrorBoundary fallback={<FeedError />}>
        <FeedSection />
      </ErrorBoundary>
      
      <ErrorBoundary fallback={<SettingsError />}>
        <SettingsSection />
      </ErrorBoundary>
    </div>
  );
}
```

**Global (App-Level):**

```jsx
function App() {
  return (
    <ErrorBoundary fallback={<GlobalError />}>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Router>
    </ErrorBoundary>
  );
}
```

**Hybrid Approach:**

```jsx
function App() {
  return (
    // Global boundary for catastrophic errors
    <ErrorBoundary fallback={<GlobalError />}>
      <div className="app-layout">
        <Header />
        
        <main>
          {/* Feature-specific boundaries */}
          <ErrorBoundary fallback={<DashboardError />}>
            <Dashboard />
          </ErrorBoundary>
          
          <ErrorBoundary fallback={<ProjectsError />}>
            <Projects />
          </ErrorBoundary>
        </main>
        
        <Footer />
      </div>
    </ErrorBoundary>
  );
}
```

### 7.7 Fallback UI Patterns

**Simple Fallback:**

```jsx
function SimpleFallback({ error, resetError }) {
  return (
    <div className="error-boundary">
      <h2>Something went wrong</h2>
      <p>We're sorry for inconvenience.</p>
      {error && <p className="error-message">{error.message}</p>}
      <button onClick={resetError}>Try Again</button>
    </div>
  );
}
```

**Detailed Fallback:**

```jsx
function DetailedFallback({ error, errorInfo, resetError }) {
  return (
    <div className="error-boundary detailed">
      <div className="error-icon">⚠️</div>
      <h2>Oops! Something went wrong</h2>
      
      <div className="error-details">
        <h3>Error Message</h3>
        <p>{error?.message || 'Unknown error'}</p>
        
        {errorInfo && (
          <details>
            <summary>Technical Details</summary>
            <pre>{errorInfo.componentStack}</pre>
          </details>
        )}
      </div>
      
      <div className="error-actions">
        <button onClick={resetError} className="btn-primary">
          Try Again
        </button>
        <button onClick={() => window.location.href = '/'} className="btn-secondary">
          Go Home
        </button>
        <button onClick={() => window.location.reload()} className="btn-tertiary">
          Reload Page
        </button>
      </div>
      
      <p className="error-contact">
        Need help? <a href="/support">Contact Support</a>
      </p>
    </div>
  );
}
```

**Themed Fallback:**

```jsx
function ThemedFallback({ error, resetError }) {
  const theme = useTheme();
  
  return (
    <div className={`error-boundary ${theme}`}>
      <div className="error-container">
        <div className="error-illustration">
          {theme === 'dark' ? (
            <DarkErrorIllustration />
          ) : (
            <LightErrorIllustration />
          )}
        </div>
        
        <h2>Something went wrong</h2>
        <p>{error?.message}</p>
        
        <button onClick={resetError} className="btn">
          Try Again
        </button>
      </div>
    </div>
  );
}
```

### 7.8 Error Reporting Integration

**Sentry Integration:**

```jsx
import * as Sentry from '@sentry/react';

class SentryErrorBoundary extends React.Component {
  state = { eventId: null };
  
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  
  componentDidCatch(error, errorInfo) {
    // Send error to Sentry
    Sentry.withScope((scope) => {
      scope.setExtra('componentStack', errorInfo.componentStack);
      scope.setTag('errorBoundary', 'true');
      
      const eventId = Sentry.captureException(error);
      this.setState({ eventId });
    });
  }
  
  render() {
    if (this.state.hasError) {
      return (
        <FallbackUI
          eventId={this.state.eventId}
          resetError={() => window.location.reload()}
        />
      );
    }
    
    return this.props.children;
  }
}

// Initialize Sentry
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  release: process.env.APP_VERSION,
});
```

**LogRocket Integration:**

```jsx
import LogRocket from 'logrocket';

class LogRocketErrorBoundary extends React.Component {
  componentDidCatch(error, errorInfo) {
    // Log error to LogRocket
    LogRocket.captureException(error, {
      tags: {
        errorBoundary: 'true',
      },
      extra: {
        componentStack: errorInfo.componentStack,
      },
    });
  }
  
  render() {
    if (this.state.hasError) {
      return <FallbackUI />;
    }
    return this.props.children;
  }
}

// Initialize LogRocket
LogRocket.init('YOUR_APP_ID', {
  release: process.env.APP_VERSION,
  console: {
    isEnabled: process.env.NODE_ENV === 'development',
  },
});
```

**Custom Error Service:**

```jsx
class ErrorReportingService {
  static async report(error, errorInfo) {
    const payload = {
      message: error.message,
      stack: error.stack,
      componentStack: errorInfo?.componentStack,
      url: window.location.href,
      userAgent: navigator.userAgent,
      timestamp: new Date().toISOString(),
    };
    
    try {
      await fetch('/api/errors', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
    } catch (reportError) {
      console.error('Failed to report error:', reportError);
    }
  }
}

class ReportingErrorBoundary extends React.Component {
  componentDidCatch(error, errorInfo) {
    ErrorReportingService.report(error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return <FallbackUI />;
    }
    return this.props.children;
  }
}
```

### 7.9 Retry Mechanisms

**Simple Retry:**

```jsx
function RetryableComponent() {
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);
  
  const handleRetry = () => {
    setError(null);
    setRetryCount(prev => prev + 1);
  };
  
  return (
    <ErrorBoundary
      fallback={
        <div className="error-fallback">
          <h2>Error occurred</h2>
          <p>{error?.message}</p>
          <button onClick={handleRetry}>
            Retry ({retryCount})
          </button>
        </div>
      }
      onError={setError}
    >
      <ChildComponent key={retryCount} />
    </ErrorBoundary>
  );
}
```

**Exponential Backoff Retry:**

```jsx
function ExponentialRetryComponent() {
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);
  const [isRetrying, setIsRetrying] = useState(false);
  
  const handleRetry = async () => {
    setIsRetrying(true);
    setError(null);
    
    // Exponential backoff
    const delay = Math.min(1000 * Math.pow(2, retryCount), 30000);
    await new Promise(resolve => setTimeout(resolve, delay));
    
    setRetryCount(prev => prev + 1);
    setIsRetrying(false);
  };
  
  return (
    <ErrorBoundary
      fallback={
        <div className="error-fallback">
          <h2>Error occurred</h2>
          <p>{error?.message}</p>
          {isRetrying ? (
            <button disabled>Retrying...</button>
          ) : (
            <button onClick={handleRetry}>
              Retry ({retryCount})
            </button>
          )}
        </div>
      }
      onError={setError}
    >
      <ChildComponent key={retryCount} />
    </ErrorBoundary>
  );
}
```

**Smart Retry:**

```jsx
function SmartRetryComponent() {
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);
  const maxRetries = 3;
  
  const shouldRetry = error => {
    // Only retry on specific errors
    const retryableErrors = [
      'NetworkError',
      'TimeoutError',
      'ServiceUnavailable',
    ];
    return retryableErrors.some(type => error?.name?.includes(type));
  };
  
  const handleRetry = () => {
    setError(null);
    setRetryCount(prev => prev + 1);
  };
  
  return (
    <ErrorBoundary
      fallback={
        <div className="error-fallback">
          <h2>Error occurred</h2>
          <p>{error?.message}</p>
          
          {shouldRetry(error) && retryCount < maxRetries ? (
            <button onClick={handleRetry}>
              Retry ({retryCount}/{maxRetries})
            </button>
          ) : (
            <p>Please try again later or contact support.</p>
          )}
        </div>
      }
      onError={setError}
    >
      <ChildComponent key={retryCount} />
    </ErrorBoundary>
  );
}
```

### 7.10 Error Boundaries with React Query/SWR

**React Query Error Boundaries:**

```jsx
import { useQuery, QueryErrorResetBoundary } from '@tanstack/react-query';

function UserProfile() {
  const { data, error, isLoading } = useQuery({
    queryKey: ['user', 'profile'],
    queryFn: fetchUserProfile,
    retry: 3,
  });
  
  if (isLoading) return <Loading />;
  if (error) return <ErrorUI error={error} />;
  
  return <Profile data={data} />;
}

// With Error Boundary
function App() {
  return (
    <ErrorBoundary fallback={<GlobalError />}>
      <QueryErrorResetBoundary>
        <UserProfile />
      </QueryErrorResetBoundary>
    </ErrorBoundary>
  );
}
```

**SWR Error Boundaries:**

```jsx
import useSWR from 'swr';

function UserProfile() {
  const { data, error, isLoading } = useSWR('/api/user/profile', fetcher);
  
  if (isLoading) return <Loading />;
  if (error) return <ErrorUI error={error} />;
  
  return <Profile data={data} />;
}

// With Error Boundary
function App() {
  return (
    <ErrorBoundary fallback={<GlobalError />}>
      <SWRConfig value={{ onError: handleError }}>
        <UserProfile />
      </SWRConfig>
    </ErrorBoundary>
  );
}

function handleError(error) {
  // Log error
  console.error('SWR Error:', error);
  
  // Show notification
  toast.error('Failed to load data');
}
```

**Combined Approach:**

```jsx
function DataComponent() {
  const { data, error, isLoading, refetch } = useQuery({
    queryKey: ['data'],
    queryFn: fetchData,
  });
  
  if (isLoading) return <Loading />;
  
  if (error) {
    // Let error boundary handle it
    throw error;
  }
  
  return <DataView data={data} />;
}

function App() {
  return (
    <ErrorBoundary
      fallback={
        <ErrorFallback
          onRetry={() => window.location.reload()}
        />
      }
    >
      <DataComponent />
    </ErrorBoundary>
  );
}
```

### 7.11 Error Boundaries with Suspense

**Suspense + Error Boundary Pattern:**

```jsx
import { Suspense } from 'react';

function ResourceComponent() {
  const resource = useResource(resourcePromise);
  
  if (resource.status === 'pending') {
    throw resource.promise;  // Suspense catches this
  }
  
  if (resource.status === 'rejected') {
    throw resource.reason;  // Error Boundary catches this
  }
  
  return <DataView data={resource.result} />;
}

function App() {
  return (
    <ErrorBoundary fallback={<ErrorFallback />}>
      <Suspense fallback={<Loading />}>
        <ResourceComponent />
      </Suspense>
    </ErrorBoundary>
  );
}
```

**Multiple Suspense Boundaries:**

```jsx
function App() {
  return (
    <ErrorBoundary fallback={<GlobalError />}>
      <Suspense fallback={<PageLoading />}>
        <Header />
        <main>
          <ErrorBoundary fallback={<ContentError />}>
            <Suspense fallback={<SectionLoading />}>
              <Dashboard />
            </Suspense>
          </ErrorBoundary>
          
          <ErrorBoundary fallback={<ContentError />}>
            <Suspense fallback={<SectionLoading />}>
              <Feed />
            </Suspense>
          </ErrorBoundary>
        </main>
        <Footer />
      </Suspense>
    </ErrorBoundary>
  );
}
```

### 7.12 Error Boundaries in Server Components (Next.js)

**Next.js App Router:**

```jsx
// app/error.js
'use client';

export default function Error({
  error,
  reset,
}) {
  return (
    <div className="error-page">
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}

// app/global-error.js
'use client';

export default function GlobalError({ error }) {
  return (
    <html>
      <body>
        <div className="global-error">
          <h2>Application Error</h2>
          <p>{error.message}</p>
          <button onClick={() => window.location.reload()}>
            Reload Application
          </button>
        </div>
      </body>
    </html>
  );
}
```

**Next.js Pages Router:**

```jsx
// pages/_error.js
class ErrorPage extends React.Component {
  static getInitialProps({ res, err }) {
    const statusCode = res ? res.statusCode : err ? err.statusCode : 404;
    return { statusCode };
  }
  
  render() {
    const { statusCode } = this.props;
    
    return (
      <div className="error-page">
        <h1>{statusCode}</h1>
        <p>Something went wrong</p>
        <Link href="/">Go Home</Link>
      </div>
    );
  }
}

export default ErrorPage;
```

**Component-Level Error Boundary:**

```jsx
'use client';

class ComponentErrorBoundary extends React.Component {
  state = { hasError: false };
  
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  
  componentDidCatch(error, errorInfo) {
    console.error('Error in component:', error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}

// Usage in Next.js component
export default function MyComponent() {
  return (
    <ComponentErrorBoundary>
      <Content />
    </ComponentErrorBoundary>
  );
}
```

### 7.13 react-error-boundary Library

**Installation:**

```bash
npm install react-error-boundary
```

**Basic Usage:**

```jsx
import { ErrorBoundary } from 'react-error-boundary';

function App() {
  return (
    <ErrorBoundary
      FallbackComponent={ErrorFallback}
      onError={(error, errorInfo) => {
        console.error('Error:', error, errorInfo);
      }}
    >
      <MyComponent />
    </ErrorBoundary>
  );
}

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div className="error-fallback">
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      <button onClick={resetErrorBoundary}>
        Try Again
      </button>
    </div>
  );
}
```

**withErrorBoundary HOC:**

```jsx
import { withErrorBoundary } from 'react-error-boundary';

class MyComponent extends React.Component {
  render() {
    return <div>{this.props.children}</div>;
  }
}

export default withErrorBoundary(MyComponent);

// Or with custom fallback
export default withErrorBoundary(MyComponent, {
  FallbackComponent: CustomFallback,
  onError: (error, errorInfo) => {
    logError(error, errorInfo);
  },
});
```

**ErrorBoundaryType:**

```jsx
import { ErrorBoundary, ErrorBoundaryType } from 'react-error-boundary';

function App() {
  return (
    <ErrorBoundary
      type={ErrorBoundaryType.Component}
      FallbackComponent={ComponentFallback}
    >
      <MyComponent />
    </ErrorBoundary>
  );
}

function ComponentFallback({ error, resetErrorBoundary }) {
  return <div>Component error: {error.message}</div>;
}
```

### 7.14 Testing Error Boundaries

**Unit Testing:**

```jsx
import { render, screen } from '@testing-library/react';
import ErrorBoundary from './ErrorBoundary';

describe('ErrorBoundary', () => {
  it('catches errors and renders fallback', () => {
    const ThrowError = () => {
      throw new Error('Test error');
    };
    
    render(
      <ErrorBoundary fallback={<FallbackUI />}>
        <ThrowError />
      </ErrorBoundary>
    );
    
    expect(screen.getByText('Error occurred')).toBeInTheDocument();
  });
  
  it('calls onError callback', () => {
    const onError = jest.fn();
    const ThrowError = () => {
      throw new Error('Test error');
    };
    
    render(
      <ErrorBoundary fallback={<FallbackUI />} onError={onError}>
        <ThrowError />
      </ErrorBoundary>
    );
    
    expect(onError).toHaveBeenCalled();
    expect(onError.mock.calls[0][0]).toBeInstanceOf(Error);
  });
});
```

**Testing with React Testing Library:**

```jsx
import { render, screen } from '@testing-library/react';

describe('ErrorBoundary Integration', () => {
  it('renders fallback when child throws error', () => {
    const ThrowComponent = () => {
      throw new Error('Test error');
    };
    
    render(
      <ErrorBoundary fallback={<FallbackUI />}>
        <ThrowComponent />
      </ErrorBoundary>
    );
    
    expect(screen.getByText(/something went wrong/i)).toBeInTheDocument();
  });
  
  it('renders children when no error', () => {
    const SafeComponent = () => <div>Safe content</div>;
    
    render(
      <ErrorBoundary fallback={<FallbackUI />}>
        <SafeComponent />
      </ErrorBoundary>
    );
    
    expect(screen.getByText('Safe content')).toBeInTheDocument();
  });
});
```

### 7.15 Error Boundary Composition

**Nested Boundaries:**

```jsx
function App() {
  return (
    // Global boundary
    <ErrorBoundary fallback={<GlobalFallback />}>
      <div className="app">
        <Header />
        
        <main>
          {/* Feature boundaries */}
          <ErrorBoundary fallback={<DashboardFallback />}>
            <Dashboard />
          </ErrorBoundary>
          
          <ErrorBoundary fallback={<ProjectsFallback />}>
            <Projects />
          </ErrorBoundary>
          
          <ErrorBoundary fallback={<SettingsFallback />}>
            <Settings />
          </ErrorBoundary>
        </main>
        
        <Footer />
      </div>
    </ErrorBoundary>
  );
}
```

**Boundary Hierarchy:**

```jsx
// Outer boundary catches everything
<ErrorBoundary fallback={<AppFallback />}>
  <AppLayout>
    {/* Inner boundaries for specific features */}
    <ErrorBoundary fallback={<DashboardFallback />}>
      <Dashboard />
    </ErrorBoundary>
    
    <ErrorBoundary fallback={<ProjectsFallback />}>
      <Projects />
    </ErrorBoundary>
  </AppLayout>
</ErrorBoundary>
```

### 7.16 Recovering from Errors

**State Reset:**

```jsx
class RecoverableErrorBoundary extends React.Component {
  state = { hasError: false, error: null };
  
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  
  componentDidCatch(error, errorInfo) {
    // Log error
    logError(error, errorInfo);
  }
  
  resetError = () => {
    this.setState({ hasError: false, error: null });
  };
  
  render() {
    if (this.state.hasError) {
      return (
        <ErrorFallback
          error={this.state.error}
          onReset={this.resetError}
        />
      );
    }
    return this.props.children;
  }
}
```

**Route Reset:**

```jsx
function ErrorFallback({ error, onReset }) {
  const navigate = useNavigate();
  
  const handleReset = () => {
    // Reset to home or previous route
    navigate('/');
    onReset();
  };
  
  return (
    <div className="error-fallback">
      <h2>Something went wrong</h2>
      <p>{error?.message}</p>
      <button onClick={handleReset}>Go Home</button>
    </div>
  );
}
```

**Data Refresh:**

```jsx
function RefreshableErrorBoundary({ children, fallback }) {
  const [error, setError] = useState(null);
  const [retryKey, setRetryKey] = useState(0);
  
  const handleRefresh = () => {
    setError(null);
    setRetryKey(prev => prev + 1);
  };
  
  return (
    <ErrorBoundary
      fallback={
        <div className="error-fallback">
          <h2>Error occurred</h2>
          <p>{error?.message}</p>
          <button onClick={handleRefresh}>Refresh</button>
        </div>
      }
      onError={setError}
    >
      <React.Fragment key={retryKey}>
        {children}
      </React.Fragment>
    </ErrorBoundary>
  );
}
```

### 7.17 User-Friendly Error Messages

**Contextual Messages:**

```jsx
function ContextualFallback({ error, component }) {
  const getErrorMessage = () => {
    switch (component) {
      case 'Dashboard':
        return 'We couldn\'t load your dashboard. Please try again.';
      case 'Profile':
        return 'We couldn\'t load your profile. Please try again.';
      case 'Settings':
        return 'We couldn\'t save your settings. Please try again.';
      default:
        return 'Something went wrong. Please try again.';
    }
  };
  
  return (
    <div className="error-fallback">
      <h2>Oops!</h2>
      <p>{getErrorMessage()}</p>
      {error?.message && (
        <details>
          <summary>Technical details</summary>
          <p>{error.message}</p>
        </details>
      )}
    </div>
  );
}
```

**Action-Oriented Messages:**

```jsx
function ActionFallback({ error, onRetry, onGoHome, onContact }) {
  return (
    <div className="error-fallback">
      <div className="error-icon">⚠️</div>
      <h2>Something went wrong</h2>
      <p>We're sorry for inconvenience.</p>
      
      <div className="error-actions">
        <button onClick={onRetry} className="btn-primary">
          Try Again
        </button>
        <button onClick={onGoHome} className="btn-secondary">
          Go Home
        </button>
        <button onClick={onContact} className="btn-tertiary">
          Contact Support
        </button>
      </div>
    </div>
  );
}
```

### 7.18 Common Patterns

**Page-Level Boundaries:**

```jsx
function PageWrapper({ children, pageName }) {
  return (
    <ErrorBoundary
      fallback={<PageFallback pageName={pageName} />}
      onError={(error) => logPageError(pageName, error)}
    >
      {children}
    </ErrorBoundary>
  );
}

// Usage
<PageWrapper pageName="Dashboard">
  <Dashboard />
</PageWrapper>
```

**Component-Level Boundaries:**

```jsx
function ComponentWrapper({ children, componentName }) {
  return (
    <ErrorBoundary
      fallback={<ComponentFallback componentName={componentName} />}
      onError={(error) => logComponentError(componentName, error)}
    >
      {children}
    </ErrorBoundary>
  );
}

// Usage
<ComponentWrapper componentName="UserProfile">
  <UserProfile />
</ComponentWrapper>
```

**Feature-Level Boundaries:**

```jsx
function FeatureWrapper({ children, featureName }) {
  return (
    <ErrorBoundary
      fallback={<FeatureFallback featureName={featureName} />}
      onError={(error) => logFeatureError(featureName, error)}
    >
      <Suspense fallback={<FeatureLoading featureName={featureName} />}>
        {children}
      </Suspense>
    </ErrorBoundary>
  );
}

// Usage
<FeatureWrapper featureName="Dashboard">
  <Dashboard />
</FeatureWrapper>
```

### 7.19 Monitoring and Alerting

**Error Rate Monitoring:**

```jsx
class ErrorRateMonitor {
  constructor() {
    this.errors = [];
    this.startTime = Date.now();
    this.threshold = 10;  // 10 errors per minute
  }
  
  recordError(error) {
    const now = Date.now();
    this.errors.push({ error, timestamp: now });
    
    // Clean old errors (older than 1 minute)
    this.errors = this.errors.filter(e => now - e.timestamp < 60000);
    
    // Check threshold
    if (this.errors.length >= this.threshold) {
      this.alertHighErrorRate();
    }
  }
  
  alertHighErrorRate() {
    console.error('High error rate detected!');
    // Send alert to monitoring service
    sendAlert('High error rate', {
      count: this.errors.length,
      duration: Date.now() - this.startTime,
    });
  }
}

const monitor = new ErrorRateMonitor();

class MonitoredErrorBoundary extends React.Component {
  componentDidCatch(error, errorInfo) {
    monitor.recordError(error);
    logError(error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return <FallbackUI />;
    }
    return this.props.children;
  }
}
```

## 8. Related Skills

- `02-frontend/react-best-practices`
- `02-frontend/nextjs-patterns`
- `14-monitoring-observability/error-tracking`
- `01-foundations/code-review`
