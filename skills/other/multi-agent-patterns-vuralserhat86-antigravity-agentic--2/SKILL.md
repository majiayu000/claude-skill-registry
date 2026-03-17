---
name: multi_agent_patterns
router_kit: AIKit
description: Çoklu agent mimarisi tasarımı, orchestration patterns ve agent collaboration rehberi.
metadata:
  skillport:
    category: architecture
    tags: [agents, algorithms, artificial intelligence, automation, chatbots, cognitive services, deep learning, embeddings, frameworks, generative ai, inference, large language models, llm, machine learning, model fine-tuning, multi agent patterns, natural language processing, neural networks, nlp, openai, prompt engineering, rag, retrieval augmented generation, tools, vector databases, workflow automation]      - patterns
---

# 🤖 Multi-Agent Patterns

> Çoklu agent mimarisi ve orchestration rehberi.

---

## 📋 Ne Zaman Multi-Agent?

| Durum | Single Agent | Multi-Agent |
|-------|--------------|-------------|
| Basit görev | ✅ | ❌ |
| Context limit aşılıyor | ❌ | ✅ |
| Farklı uzmanlıklar | ❌ | ✅ |
| Paralel işlem | ❌ | ✅ |
| Complex workflow | ❌ | ✅ |

---

## 🏗️ Mimari Patterns

### 1. Orchestrator Pattern
```
        ┌─────────────┐
        │ Orchestrator│
        └──────┬──────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
┌───────┐  ┌───────┐  ┌───────┐
│Agent 1│  │Agent 2│  │Agent 3│
│Coder  │  │Tester │  │Reviewer│
└───────┘  └───────┘  └───────┘
```

**Kullanım:** Complex workflows, task delegation

### 2. Pipeline Pattern
```
┌───────┐    ┌───────┐    ┌───────┐
│ Parse │ -> │Process│ -> │ Output│
└───────┘    └───────┘    └───────┘
```

**Kullanım:** Sequential processing, data transformation

### 3. Specialist Pattern
```
        ┌─────────────┐
        │   Router    │
        └──────┬──────┘
               │ (task type)
    ┌──────────┼──────────┐
    ▼          ▼          ▼
┌───────┐  ┌───────┐  ┌───────┐
│  SQL  │  │  API  │  │  UI   │
│Expert │  │Expert │  │Expert │
└───────┘  └───────┘  └───────┘
```

**Kullanım:** Domain-specific expertise

### 4. Debate Pattern
```
┌───────┐         ┌───────┐
│Agent A│ <-----> │Agent B│
│(Pro)  │ debate  │(Con)  │
└───────┘         └───────┘
         \       /
          \     /
           \   /
        ┌───────┐
        │ Judge │
        └───────┘
```

**Kullanım:** Decision making, option evaluation

---

## 🔧 Implementation

### Agent Definition
```python
class Agent:
    def __init__(self, name, role, skills):
        self.name = name
        self.role = role
        self.skills = skills
    
    def process(self, task):
        # Agent logic
        pass
```

### Orchestrator
```python
class Orchestrator:
    def __init__(self, agents):
        self.agents = agents
    
    def route(self, task):
        # Determine which agent handles task
        agent = self.select_agent(task)
        return agent.process(task)
    
    def select_agent(self, task):
        # Routing logic
        pass
```

---

## 📊 Communication Patterns

| Pattern | Açıklama |
|---------|----------|
| **Direct** | Agent → Agent |
| **Broadcast** | Orchestrator → All Agents |
| **Pub/Sub** | Topic-based messaging |
| **Request/Response** | Sync communication |
| **Event-driven** | Async, event queue |

---

## ⚠️ Best Practices

1. **Clear Roles**: Her agent'ın net görevi olsun
2. **Minimal Overlap**: Görev çakışması olmasın
3. **Fallback**: Agent fail olursa plan B
4. **Monitoring**: Her agent'ı izle
5. **Context Sharing**: Gerekli bilgiyi paylaş

---

*Multi-Agent Patterns v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [AutoGen Documentation](https://microsoft.github.io/autogen/) & [CrewAI](https://docs.crewai.com/)

### Aşama 1: Role Definition
- [ ] **Persona Design**: Her agent için net bir "System Message" yaz (Sen nesin, ne yaparsın, ne yapmazsın).
- [ ] **Tools**: Agent'a sadece ihtiyacı olan tool'ları ver (LLM'in halüsinasyon riskini azaltır).
- [ ] **Hierarchy**: Kim kime rapor verecek? (Manager -> Worker) yoksa (Peer-to-Peer) mi?

### Aşama 2: Interaction Pattern
- [ ] **Chat Topology**: "Group Chat" (Herkes konuşur) vs "Nested Chats" (Alt gruplar) seçimi yap.
- [ ] **Handoffs**: Görev devir teslimi için açık tetikleyiciler (Trigger phrases) belirle.
- [ ] **Human-in-the-loop**: Kritik kararlar için "User Proxy Agent" veya onay mekanizması ekle.

### Aşama 3: Execution & Output
- [ ] **Consolidation**: Sonuçları birleştiren bir "Summarizer Agent" ata.
- [ ] **Validation**: Çıktının formata uygunluğunu (JSON/Markdown) kontrol eden validator ekle.
- [ ] **Cost Control**: Maksimum tur (Max Turns) ve token limitlerini ayarla.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Agentlar birbirinin sözünü kesiyor mu (Turn-taking bozuk mu)? |
| 2 | Sonsuz döngüye (Infinite Loop) girme riski var mı? |
| 3 | Karmaşık görevler doğru alt parçalara bölündü mü? |
