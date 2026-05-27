---
name: Conversational UI
description: Building conversational user interfaces for AI-powered applications, including chat interfaces, voice interactions, and multi-modal communication.
---

# Conversational UI

> **Current Level:** Expert (Enterprise Scale)
> **Domain:** AI Integration / User Interface

---

## Overview

Conversational UIs provide natural language interfaces for AI-powered applications, enabling users to interact through chat, voice, and multi-modal communication. They combine natural language understanding, context management, and intuitive design to deliver seamless, human-like interactions.

---

## 1. Executive Summary & Strategic Necessity

* **Context:** ในปี 2025-2026 Conversational UI ด้วย ReAct Pattern และ LLM Integration ช่วย Natural Language Interfaces ที่มีอัตโนมาติการทำงานอัตโนมาติ (Conversational Interfaces) ใน Enterprise Scale

* **Business Impact:** Conversational UI ช่วยลด Downtime ของระบบ Customer Support ผ่านการตอบคำถามอัตโนมาติการสนทนา (Reduce friction), ลดต้นทุนการจัดการทีม (Increase engagement), เพิ่มอัตรากำไร Gross Margin ผ่านการทำงานอัตโนมาติ (Automated workflows), และปรับประสบทการทำงาน (Consistent experience)

* **Product Thinking:** Conversational UI ช่วยแก้ปัญหา (Pain Point) ความต้องการมีระบบสนทนาอัตโนมาติ (Users need natural interfaces) ผ่านการทำงานอัตโนมาติ (Intuitive conversations)

---

## 2. Technical Deep Dive (The "How-to")

* **Core Logic:** Conversational UI ใช้ ReAct Pattern และ LLM Integration ช่วย Natural Language Interfaces ทำงานอัตโนมาติ:
  1. **Input Processing**: วิเคคิดความต้องการ (Text, Voice, Multi-modal input)
  2. **Context Management**: จัดเก็บ Conversation history ด้วย Memory (Short-term, Long-term)
  3. **Response Generation**: สร้างคำตอบ ด้วย LLM (GPT-4, Claude)
  4. **Output Rendering**: แสดงผลลัพธ์ผ่าน UI Components (Chat bubbles, Voice synthesis)
  5. **State Management**: จัดการสถานะของ Conversation และ User session

* **Architecture Diagram Requirements:** แผนผังระบบ Conversational UI ต้องมีองค์ประกอบ:
  1. **LLM Integration**: Language Model สำหรับการคิดคิด (OpenAI GPT-4, Anthropic Claude)
  2. **Input Processing Layer**: ประสบคิดความต้องการ (Text input, Voice recognition, Image processing)
  3. **Context Management**: Memory system สำหรับการจัดเก็บ Conversation history (Redis, Vector DB)
  4. **Response Generation**: LLM สำหรับการสร้างคำตอบ (GPT-4, Claude)
  5. **Output Rendering**: UI Components สำหรับการแสดงผล (Chat bubbles, Voice synthesis)
  6. **API Gateway**: REST API ด้วย Rate limiting และ Authentication
  7. **Observability**: Logging, Monitoring, Tracing สำหรับการ debug และปรับสิทท

* **Implementation Workflow:** ขั้นตอนการนำ Conversational UI ไปใช้งานจริง:
  1. **Planning Phase**: กำหนด Requirement และเลือก Model ที่เหมาะสม
  2. **UI Design**: ออกแบบ UI Components สำหรับการแสดงผล (Chat bubbles, Voice buttons)
  3. **Input Processing**: สร้าง Input processing layer (Text, Voice, Multi-modal)
  4. **Response Generation**: สร้าง Response generation system ด้วย LLM
  5. **Output Rendering**: สร้าง Output rendering layer (Chat bubbles, Voice synthesis)
  6. **Testing Phase**: Unit test, Integration test, E2E test ด้วยจริง Scenario
  7. **Deployment**: Deploy ด้วย API Gateway, Set up Rate limiting, Configure Monitoring
  8. **Optimization**: Tune prompts, Optimize token usage, Cache embeddings
  9. **Maintenance**: Monitor performance, Update UI Components, Handle edge cases

---

## 3. Tooling & Tech Stack

* **Enterprise Tools:** เครื่องมือระดับอุตสาหกรรมที่เลือกใช้สำหรับ Conversational UI ใน Enterprise Scale:
  1. **OpenAI**: GPT-4, GPT-3.5-turbo, Embeddings (text-embedding-3-small, text-embedding-3-large)
  2. **Anthropic**: Claude 3 Opus, Claude 3 Sonnet, Claude 3 Haiku
  3. **React**: UI Framework สำหรับสร้าง Chat interfaces
  4. **Next.js**: Full-stack framework สำหรับ Server-side rendering
  5. **LangChain**: Framework สำหรับสร้าง Conversational AI (Python, JavaScript)
  6. **Redis**: Cache สำหรับ Short-term Memory และ Rate limiting
  7. **PostgreSQL**: Database สำหรับการจัดเก็บ Conversation History และ User data
  8. **Prometheus**: Monitoring สำหรับ Metrics (Token usage, Latency, Error rate)
  9. **Grafana**: Visualization dashboard สำหรับ Observability
  10. **Web Speech API**: Browser API สำหรับ Voice recognition และ Synthesis

* **Configuration Essentials:** การตั้งค่าสำคัญสำหรับให้ระบบเสถียร Conversational UI:
  1. **Model Configuration**: เลือก Model ตาม Use case (GPT-4 สำหรับ Complex reasoning, GPT-3.5-turbo สำหรับ Speed)
  2. **Token Budget**: ตั้ง max_tokens ตาม Budget และ Context window (4,000-8,000 tokens)
  3. **Temperature Settings**: 0.0-0.3 สำหรับ Creativity, 0.7 สำหรับ Deterministic
  4. **Rate Limiting**: 10-100 requests/minute ตาม User tier และ API limits
  5. **Timeout Configuration**: 30-60 seconds สำหรับ Chatbot execution, 5-10 seconds สำหรับ Tool calls
  6. **Memory Configuration**: 10-20 messages สำหรับ Short-term, 100-500 documents สำหรับ Vector search
  7. **Retry Policy**: Exponential backoff (base: 2, max: 5) ด้วย Jitter
  8. **Logging Level**: INFO สำหรับ Production, DEBUG สำหรับ Development
  9. **Monitoring**: Track success rate, token usage, latency, error rate ต่อเป้าหลาย
  10. **Secret Management**: Use Environment variables หรือ Secret Manager (AWS Secrets Manager, HashiCorp Vault)

---

## 4. Standards, Compliance & Security

* **International Standards:** มาตรฐานที่เกี่ยวข้อง:
  1. **ISO/IEC 27001**: Information Security Management - สำหรับการจัดการ Secrets และ Access Control
  2. **ISO/IEC 27017**: Code of Practice for Information Security Controls - สำหรับ Secure Development
  3. **GDPR**: General Data Protection Regulation - สำหรับการจัดการ Personal Data และ User Consent
  4. **SOC 2 Type II**: Security Controls - สำหรับการ Audit และ Compliance
  5. **OWASP Top 10**: Web Application Security - สำหรับการป้องกัน Prompt Injection และ Data Exposure

* **Security Protocol:** กลไกการป้องกัน Conversational UI:
  1. **Input Validation**: Validate และ Sanitize ทุก Input ก่อน LLM หรือ Tools (Prevent prompt injection, SQL injection)
  2. **Output Sanitization**: Filter sensitive information จาก LLM output (PII, Secrets, Internal URLs)
  3. **Tool Permission Model**: RBAC (Role-Based Access Control) สำหรับ Tools - บาง Tools Admin permission, บาง Tools เปิดให้ทุก User
  4. **Audit Trail**: Log ทุก Chatbot action, Tool call, และ Decision ด้วย Timestamp, User ID, และ Result (สำหรับ Forensics และ Compliance)
  5. **Rate Limiting**: Per-user และ Per-API rate limits สำหรับป้องกัน Abuse (100-1000 requests/hour)
  6. **Secure Communication**: mTLS สำหรับ internal services, TLS 1.3 สำหรับ external APIs
  7. **Secret Rotation**: Rotate API keys ทุก 30-90 วัน (Automated key rotation)
  8. **Sandboxing**: Run Tools ใน isolated environment (Docker containers, Lambda functions)
  9. **Content Filtering**: Block malicious content, Adult content, และ Violations (Content moderation APIs)
  10. **Data Encryption**: Encrypt sensitive data ที่ rest ใน Database (AES-256 หรือ Customer-managed keys)

* **Explainability:** (สำหรับ AI) ความสามารถในการอธิบายผลลัพธ์ผ่านเทคนิค:
  1. **Chain of Thought Logging**: เก็บ Thought process ของ Chatbot สำหรับ Debugging และ Transparency
  2. **Tool Call Tracing**: Log ทุก Tool call ด้วย Input, Output, และ Execution time
  3. **Decision Reasoning**: บันทึกเหตุผลการตัดสินใจของ Chatbot (Why chose this response?)
  4. **Confidence Scoring**: ให้คะแนน (0-1) กับทุก Decision สำหรับการประเมิน
  5. **Human-in-the-Loop**: จัดการ Approval สำหรับ critical actions ด้วย Audit trail

---

## 5. Unit Economics & Performance Metrics (KPIs)

* **Cost Calculation:** สูตรการคำนวณต้นทุนต่อหน่วย Conversational UI:
  1. **LLM Cost per Request** = (Input Tokens + Output Tokens) × Price per 1K tokens
     - GPT-4: $0.03/1K input + $0.06/1K output
     - GPT-3.5-turbo: $0.001/1K input + $0.002/1K output
     - Claude 3 Opus: $0.015/1K input + $0.075/1K output
  2. **Tool Execution Cost** = API calls × Cost per call
     - Database Query: $0.001 per query (PostgreSQL RDS)
     - External API: $0.01-0.10 per call (varies by service)
  3. **Vector Search Cost** = $0.001 per query (Pinecone)
  4. **Total Cost per Conversation** = LLM Cost + Tool Costs + Vector Search Cost
  5. **Monthly Cost** = (Cost per Conversation × Conversations per Month) + Infrastructure Costs
  6. **Infrastructure Costs** = Compute ($20-100/month) + Storage ($0.023/GB/month) + Monitoring ($10/month)

* **Key Performance Indicators:** ตัวชี้วัดความสำเร็จทางเทคนิค:
  1. **Success Rate**: อัตราการสำเร็จของ Chatbot (Target: >95%)
  2. **Average Latency**: เวลาการตอบกลับ (Target: <5 seconds สำหรับ single-turn, <30 seconds สำหรับ multi-turn)
  3. **Token Usage per Request**: เฉลี่ย Token เฉลี่ย Request (Target: <2,000 tokens)
  4. **Tool Call Success Rate**: อัตราการสำเร็จของ Tool calls (Target: >98%)
  5. **Average Tool Execution Time**: เวลาการทำงาน Tool (Target: <2 seconds)
  6. **User Satisfaction Score**: 1-5 rating จาก User feedback (Target: >4.0)
  7. **Error Rate**: อัตราการ Error (Target: <1%)
  8. **Concurrent Users**: จำนวยผู้ใช้งานพร้อมกัน (Peak: 100-1,000 concurrent sessions)
  9. **Cache Hit Rate**: อัตราการ Cache hit (Target: >80% สำหรับ repeated queries)
  10. **Agent Iterations per Request**: จำนวย iteration เฉลี่ย Request (Target: <5 iterations)

---

## 6. Strategic Recommendations (CTO Insights)

* **Phase Rollout:** คำแนะนำในการทยอยเริ่มใช้งาน Conversational UI เพื่อลดความเสี่ยง:
  1. **Phase 1: MVP (1-2 เดือน)**: Deploy Simple Conversational UI ด้วย 1-2 Tools (Text input, Simple response) สำหรับ Internal team ก่อนเปิดให้ Public
     - **Goal**: Validate Conversational UI architecture และ gather feedback
     - **Success Criteria**: >80% success rate, <10s latency
     - **Risk Mitigation**: Rate limiting, Manual review ก่อน Auto-approve
  2. **Phase 2: Beta (2-3 เดือน)**: Expand ด้วย 5-10 Tools และ Memory system (Voice input, Multi-modal) สำหรับ Selected customers
     - **Goal**: Test scalability และ Tool reliability
     - **Success Criteria**: >90% success rate, <5s latency
     - **Risk Mitigation**: Canary deployment, Feature flags, Gradual rollout
  3. **Phase 3: GA (3-6 เดือน)**: Full rollout ด้วย 10-20 Tools, Advanced Memory, และ Multi-agent orchestration
     - **Goal**: Enterprise-grade reliability และ Performance
     - **Success Criteria**: >95% success rate, <3s latency, 99.9% uptime
     - **Risk Mitigation**: Load testing, Disaster recovery, Blue-green deployment

* **Pitfalls to Avoid:** ข้อควรระวังที่มักจะผิดพลาดในระดับ Enterprise Scale:
  1. **Over-engineering**: สร้าง Conversational UI ที่ซ้อนเกินไป (Too many tools, Complex memory) → เริ่มจาก Simple และ iterate
  2. **No Rate Limiting**: ไม่มี Rate limits ทำให้ Cost blowout และ API abuse → Implement per-user และ per-endpoint limits ด้วย Redis
  3. **Infinite Loops**: Chatbot วนลูปไม่มีทางออก (Max iterations = ∞) → Set max_iterations=10 และ timeout=60s
  4. **Ignoring Tool Errors**: Tool failures crash Chatbot → Wrap Tools ด้วย try-catch และ return fallback response
  5. **No Context Management**: ส่งทุก message เป็น Independent → Implement sliding window และ summary
  6. **Hardcoding API Keys**: Keys ใน code ที่เปิดให้ Public → Use Environment variables หรือ Secret Manager
  7. **No Observability**: ไม่มี Logging/Tracing → Add structured logging ด้วย correlation IDs
  8. **Skipping Validation**: ไม่ Validate Tool inputs/outputs → Implement schema validation และ sanitization
  9. **Poor Prompt Design**: Vague prompts ทำให้ Chatbot hallucinate → Use specific, testable prompts ด้วย examples
  10. **Single Point of Failure**: ไม่มี Redundancy หรือ Fallback → Deploy multiple instances ด้วย Load balancer

---

## Core Concepts

### 1. Conversational UI Concepts

### What is Conversational UI?

```markdown
# Conversational UI Concepts

## Definition
A conversational user interface (CUI) is a UI that mimics chatting with a real human.

## Key Characteristics
- **Natural Language**: Users speak naturally
- **Context Awareness**: Remembers previous interactions
- **Multi-turn**: Supports extended conversations
- **Intuitive**: No training required

## Types of Conversational UI
- **Text-based**: Chat interfaces, messaging apps
- **Voice-based**: Voice assistants, phone systems
- **Multi-modal**: Combines text, voice, and visual elements
```

### UI Components

```markdown
# UI Components

## Chat Interface
- **Message Bubbles**: Display messages
- **Input Field**: User input area
- **Send Button**: Submit messages
- **Typing Indicator**: Show when bot is typing
- **Quick Replies**: Suggested responses

## Voice Interface
- **Microphone Button**: Start voice input
- **Voice Feedback**: Show voice recognition status
- **Text-to-Speech**: Speak responses
- **Visual Feedback**: Show voice activity

## Multi-modal Interface
- **Image Upload**: Share images
- **File Sharing**: Send documents
- **Rich Cards**: Display structured content
- **Action Buttons**: Quick actions
```

---

## 2. Chat Interface Design

### Chat Component

```typescript
// Chat Interface Component
'use client'

import { useState, useRef, useEffect } from 'react'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      // Get AI response
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage.content, history: messages })
      })

      const data = await response.json()

      // Add assistant message
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error sending message:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="chat-interface">
      <div className="messages-container">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.role}`}
          >
            <div className="message-content">
              {message.content}
            </div>
            <div className="message-time">
              {message.timestamp.toLocaleTimeString()}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-container">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          rows={1}
          disabled={isLoading}
        />
        <button
          onClick={handleSend}
          disabled={!input.trim() || isLoading}
        >
          Send
        </button>
      </div>
    </div>
  )
}
```

### Message Bubble Styles

```css
/* Message Bubble Styles */
.message {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
  max-width: 80%;
}

.message.user {
  align-self: flex-end;
  align-items: flex-end;
}

.message.assistant {
  align-self: flex-start;
  align-items: flex-start;
}

.message-content {
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  word-wrap: break-word;
}

.message.user .message-content {
  background-color: #007bff;
  color: white;
  border-bottom-right-radius: 0.25rem;
}

.message.assistant .message-content {
  background-color: #f0f0f0;
  color: #333;
  border-bottom-left-radius: 0.25rem;
}

.message-time {
  font-size: 0.75rem;
  color: #666;
  margin-top: 0.25rem;
}

.typing-indicator {
  display: flex;
  gap: 0.25rem;
  padding: 0.75rem 1rem;
  background-color: #f0f0f0;
  border-radius: 1rem;
  border-bottom-left-radius: 0.25rem;
}

.typing-indicator span {
  width: 0.5rem;
  height: 0.5rem;
  background-color: #666;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-0.25rem);
  }
}
```

---

## 3. Voice Interface Design

### Voice Recognition

```typescript
// Voice Recognition Component
'use client'

import { useState, useEffect, useRef } from 'react'

export default function VoiceInterface() {
  const [isListening, setIsListening] = useState(false)
  const [transcript, setTranscript] = useState('')
  const recognitionRef = useRef<any>(null)

  useEffect(() => {
    // Initialize speech recognition
    if (typeof window !== 'undefined' && 'webkitSpeechRecognition' in window) {
      const SpeechRecognition = (window as any).webkitSpeechRecognition
      recognitionRef.current = new SpeechRecognition()
      recognitionRef.current.continuous = false
      recognitionRef.current.interimResults = true
      recognitionRef.current.lang = 'en-US'

      recognitionRef.current.onresult = (event: any) => {
        let finalTranscript = ''
        let interimTranscript = ''

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript
          if (event.results[i].isFinal) {
            finalTranscript += transcript
          } else {
            interimTranscript += transcript
          }
        }

        setTranscript(finalTranscript || interimTranscript)
      }

      recognitionRef.current.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error)
        setIsListening(false)
      }

      recognitionRef.current.onend = () => {
        setIsListening(false)
      }
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop()
      }
    }
  }, [])

  const toggleListening = () => {
    if (!recognitionRef.current) {
      alert('Speech recognition is not supported in this browser')
      return
    }

    if (isListening) {
      recognitionRef.current.stop()
    } else {
      recognitionRef.current.start()
    }
    setIsListening(!isListening)
  }

  return (
    <div className="voice-interface">
      <button
        onClick={toggleListening}
        className={`voice-button ${isListening ? 'listening' : ''}`}
      >
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
          <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
          <line x1="12" y1="19" x2="12" y2="23" />
          <line x1="8" y1="23" x2="16" y2="23" />
        </svg>
      </button>
      {transcript && (
        <div className="transcript">
          {transcript}
        </div>
      )}
    </div>
  )
}
```

### Text-to-Speech

```typescript
// Text-to-Speech Component
'use client'

import { useState, useEffect } from 'react'

export default function TextToSpeech({ text }: { text: string }) {
  const [isSpeaking, setIsSpeaking] = useState(false)

  const speak = () => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = 'en-US'
      utterance.rate = 1
      utterance.pitch = 1

      utterance.onstart = () => setIsSpeaking(true)
      utterance.onend = () => setIsSpeaking(false)
      utterance.onerror = () => setIsSpeaking(false)

      window.speechSynthesis.speak(utterance)
    } else {
      alert('Text-to-speech is not supported in this browser')
    }
  }

  const stop = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel()
      setIsSpeaking(false)
    }
  }

  useEffect(() => {
    return () => {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel()
      }
    }
  }, [])

  return (
    <button
      onClick={isSpeaking ? stop : speak}
      className="tts-button"
    >
      {isSpeaking ? 'Stop' : 'Speak'}
    </button>
  )
}
```

---

## 4. Multi-modal Interface Design

### Image Upload Component

```typescript
// Image Upload Component
'use client'

import { useState, useRef } from 'react'

export default function ImageUpload({ onImageUpload }: { onImageUpload: (file: File) => void }) {
  const [preview, setPreview] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      // Create preview
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result as string)
      }
      reader.readAsDataURL(file)

      // Call callback
      onImageUpload(file)
    }
  }

  const handleClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="image-upload">
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        style={{ display: 'none' }}
      />
      <button onClick={handleClick} className="upload-button">
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
          <circle cx="8.5" cy="8.5" r="1.5" />
          <polyline points="21 15 16 10 5 21" />
        </svg>
        Upload Image
      </button>
      {preview && (
        <div className="image-preview">
          <img src={preview} alt="Preview" />
          <button
            onClick={() => setPreview(null)}
            className="remove-button"
          >
            Remove
          </button>
        </div>
      )}
    </div>
  )
}
```

### Rich Card Component

```typescript
// Rich Card Component
interface RichCard {
  title: string
  description?: string
  image?: string
  actions?: Array<{
    label: string
    value: string
  }>
}

export default function RichCard({ card }: { card: RichCard }) {
  const handleAction = (value: string) => {
    // Handle action
    console.log('Action:', value)
  }

  return (
    <div className="rich-card">
      {card.image && (
        <img src={card.image} alt={card.title} className="card-image" />
      )}
      <div className="card-content">
        <h3 className="card-title">{card.title}</h3>
        {card.description && (
          <p className="card-description">{card.description}</p>
        )}
        {card.actions && card.actions.length > 0 && (
          <div className="card-actions">
            {card.actions.map((action, index) => (
              <button
                key={index}
                onClick={() => handleAction(action.value)}
                className="card-action-button"
              >
                {action.label}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
```

---

## 5. Quick Replies

### Quick Replies Component

```typescript
// Quick Replies Component
interface QuickReply {
  label: string
  value: string
}

export default function QuickReplies({
  replies,
  onSelect
}: {
  replies: QuickReply[]
  onSelect: (reply: QuickReply) => void
}) {
  return (
    <div className="quick-replies">
      {replies.map((reply, index) => (
        <button
          key={index}
          onClick={() => onSelect(reply)}
          className="quick-reply-button"
        >
          {reply.label}
        </button>
      ))}
    </div>
  )
}
```

---

## 6. Conversation State Management

### State Management with React Context

```typescript
// Conversation Context
'use client'

import { createContext, useContext, useState, ReactNode } from 'react'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface ConversationContextType {
  messages: Message[]
  addMessage: (message: Omit<Message, 'id' | 'timestamp'>) => void
  clearMessages: () => void
}

const ConversationContext = createContext<ConversationContextType | undefined>(undefined)

export function ConversationProvider({ children }: { children: ReactNode }) {
  const [messages, setMessages] = useState<Message[]>([])

  const addMessage = (message: Omit<Message, 'id' | 'timestamp'>) => {
    const newMessage: Message = {
      ...message,
      id: Date.now().toString(),
      timestamp: new Date()
    }
    setMessages(prev => [...prev, newMessage])
  }

  const clearMessages = () => {
    setMessages([])
  }

  return (
    <ConversationContext.Provider value={{ messages, addMessage, clearMessages }}>
      {children}
    </ConversationContext.Provider>
  )
}

export function useConversation() {
  const context = useContext(ConversationContext)
  if (!context) {
    throw new Error('useConversation must be used within ConversationProvider')
  }
  return context
}
```

---

## 7. Typing Indicators

### Typing Indicator Component

```typescript
// Typing Indicator Component
export default function TypingIndicator() {
  return (
    <div className="typing-indicator">
      <span></span>
      <span></span>
      <span></span>
    </div>
  )
}
```

```css
/* Typing Indicator Styles */
.typing-indicator {
  display: flex;
  gap: 0.25rem;
  padding: 0.75rem 1rem;
  background-color: #f0f0f0;
  border-radius: 1rem;
  border-bottom-left-radius: 0.25rem;
  width: fit-content;
}

.typing-indicator span {
  width: 0.5rem;
  height: 0.5rem;
  background-color: #666;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-0.25rem);
  }
}
```

---

## 8. Message Formatting

### Markdown Rendering

```typescript
// Markdown Renderer Component
'use client'

import ReactMarkdown from 'react-markdown'

export default function MarkdownRenderer({ content }: { content: string }) {
  return (
    <div className="markdown-content">
      <ReactMarkdown>{content}</ReactMarkdown>
    </div>
  )
}
```

```css
/* Markdown Styles */
.markdown-content {
  line-height: 1.6;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3 {
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}

.markdown-content p {
  margin-bottom: 0.5rem;
}

.markdown-content code {
  background-color: #f0f0f0;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-family: monospace;
}

.markdown-content pre {
  background-color: #f0f0f0;
  padding: 1rem;
  border-radius: 0.5rem;
  overflow-x: auto;
}

.markdown-content ul,
.markdown-content ol {
  margin-left: 1.5rem;
  margin-bottom: 0.5rem;
}
```

---

## 9. Accessibility

### Accessibility Features

```typescript
// Accessible Chat Interface
'use client'

import { useState, useRef, useEffect } from 'react'

export default function AccessibleChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const handleSend = async () => {
    if (!input.trim()) return

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    }
    setMessages(prev => [...prev, userMessage])
    setInput('')

    // Announce to screen readers
    announceToScreenReader(`You sent: ${input}`)

    try {
      // Get AI response
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage.content, history: messages })
      })

      const data = await response.json()

      // Add assistant message
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, assistantMessage])

      // Announce to screen readers
      announceToScreenReader(`Assistant said: ${data.response}`)
    } catch (error) {
      console.error('Error sending message:', error)
      announceToScreenReader('Error sending message')
    }
  }

  const announceToScreenReader = (message: string) => {
    const announcement = document.createElement('div')
    announcement.setAttribute('aria-live', 'polite')
    announcement.setAttribute('aria-atomic', 'true')
    announcement.className = 'sr-only'
    announcement.textContent = message
    document.body.appendChild(announcement)

    setTimeout(() => {
      document.body.removeChild(announcement)
    }, 1000)
  }

  return (
    <div className="accessible-chat">
      <div
        className="messages-container"
        role="log"
        aria-live="polite"
        aria-atomic="false"
      >
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.role}`}
            role="article"
            aria-label={`${message.role} message`}
          >
            <div className="message-content">
              {message.content}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form className="input-form" onSubmit={(e) => { e.preventDefault(); handleSend() }}>
        <label htmlFor="message-input" className="sr-only">
          Type your message
        </label>
        <input
          id="message-input"
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          aria-label="Message input"
        />
        <button type="submit" aria-label="Send message">
          Send
        </button>
      </form>
    </div>
  )
}
```

```css
/* Screen Reader Only */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

---

## 10. Mobile Responsive Design

### Responsive Chat Interface

```css
/* Responsive Chat Interface */
.chat-interface {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.input-container {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #e0e0e0;
}

.input-container textarea {
  flex: 1;
  min-height: 40px;
  max-height: 120px;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  resize: none;
}

/* Mobile Styles */
@media (max-width: 768px) {
  .messages-container {
    padding: 0.5rem;
  }

  .message {
    max-width: 90%;
  }

  .input-container {
    padding: 0.5rem;
  }

  .input-container textarea {
    font-size: 16px; /* Prevent zoom on iOS */
  }
}
```

---

## Quick Start

### Minimal Chat Interface

```typescript
// Minimal Chat Interface
'use client'

import { useState } from 'react'

export default function SimpleChat() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! How can I help you?' }
  ])
  const [input, setInput] = useState('')

  const handleSend = async () => {
    if (!input.trim()) return

    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: input }])
    setInput('')

    // Get AI response
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      })

      const data = await response.json()

      // Add assistant message
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }])
    } catch (error) {
      console.error('Error:', error)
    }
  }

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <div style={{ marginBottom: '20px' }}>
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              padding: '10px',
              margin: '5px 0',
              backgroundColor: msg.role === 'user' ? '#007bff' : '#f0f0f0',
              color: msg.role === 'user' ? 'white' : 'black',
              borderRadius: '10px',
              maxWidth: '80%',
              marginLeft: msg.role === 'user' ? 'auto' : '0'
            }}
          >
            {msg.content}
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', gap: '10px' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type your message..."
          style={{ flex: 1, padding: '10px' }}
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  )
}
```

### Installation

```bash
npm install react-markdown
# or
yarn add react-markdown
```

### Next Steps

1. Add conversation memory for multi-turn conversations
2. Implement voice recognition and text-to-speech
3. Add image upload and multi-modal support
4. Set up analytics and monitoring
```

---

## Production Checklist

- [ ] **Error Handling**: Implement try-catch blocks for all operations
- [ ] **Rate Limiting**: Add rate limits to prevent API abuse
- [ ] **Token Budget**: Set maximum token limits per conversation
- [ ] **Timeout**: Configure timeouts to prevent infinite loops
- [ ] **Logging**: Set up structured logging for all interactions
- [ ] **Monitoring**: Add metrics for success rate, latency, token usage
- [ ] **Security**: Validate and sanitize all inputs
- [ ] **Cost Tracking**: Monitor API costs per conversation
- [ ] **Memory Management**: Implement context window for conversation history
- [ ] **Fallback Strategy**: Implement fallback mechanisms for failures
- [ ] **Accessibility**: Ensure WCAG 2.1 AA compliance
- [ ] **Mobile Responsive**: Test on various screen sizes
- [ ] **Input Validation**: Validate all inputs before processing
- [ ] **Output Sanitization**: Filter sensitive data from outputs
- [ ] **Retry Logic**: Implement exponential backoff for retries
- [ ] **Observability**: Add tracing and correlation IDs

---

## Anti-patterns

### ❌ Don't: No Accessibility

```typescript
// ❌ Bad - No accessibility features
<div className="message">{message.content}</div>
```

```typescript
// ✅ Good - Accessible message
<div
  className="message"
  role="article"
  aria-label={`${message.role} message`}
>
  {message.content}
</div>
```

### ❌ Don't: No Error Handling

```typescript
// ❌ Bad - No error handling
const handleSend = async () => {
  const response = await fetch('/api/chat')
  const data = await response.json()
  setMessages(prev => [...prev, data.response])
}
```

```typescript
// ✅ Good - With error handling
const handleSend = async () => {
  try {
    const response = await fetch('/api/chat')
    if (!response.ok) throw new Error('Request failed')
    const data = await response.json()
    setMessages(prev => [...prev, data.response])
  } catch (error) {
    console.error('Error:', error)
    // Show error to user
  }
}
```

### ❌ Don't: No Mobile Optimization

```css
/* ❌ Bad - Fixed width */
.chat-interface {
  width: 600px;
}
```

```css
/* ✅ Good - Responsive */
.chat-interface {
  width: 100%;
  max-width: 600px;
}

@media (max-width: 768px) {
  .chat-interface {
    padding: 0.5rem;
  }
}
```

---

## Integration Points

- **LLM Integration** (`06-ai-ml-production/llm-integration/`) - Setting up LLM providers
- **Chatbot Integration** (`20-ai-integration/chatbot-integration/`) - Backend chatbot logic
- **Voice Recognition** (`20-ai-integration/conversational-ui/`) - Voice input/output
- **Error Handling** (`03-backend-api/error-handling/`) - Production error patterns
- **Frontend Development** (`02-frontend/`) - UI frameworks and patterns

---

## Further Reading

- [OpenAI Chat Completions](https://platform.openai.com/docs/guides/chat)
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)
- [React Patterns](https://reactpatterns.com/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Conversational Design](https://www.nngroup.com/articles/conversation-design/)
