---
name: prompt_optimizer
router_kit: AIKit
description: Mevcut promptların token kullanımını ve başarı oranını optimize etme.
metadata:
  skillport:
    category: ai
    tags: [agents, algorithms, artificial intelligence, automation, chatbots, cognitive services, deep learning, embeddings, frameworks, generative ai, inference, large language models, llm, machine learning, model fine-tuning, natural language processing, neural networks, nlp, openai, prompt engineering, prompt optimizer, rag, retrieval augmented generation, tools, vector databases, workflow automation]      - prompt-refinement
---

# ⚡ Prompt Optimizer

> Prompt verimliliğini artırma ve token maliyeti düşürme metodolojisi.

---

*Prompt Optimizer v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Anthropic - Prompt Engineering Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)

### Aşama 1: Analysis & Benchmarking
- [ ] **Analyze**: Mevcut promptun nerede hata yaptığını veya neden çok token harcadığını belirle.
- [ ] **Baseline**: Başarı oranını ve ortalama token sayısını kaydet.

### Aşama 2: Rewriting & Compression
- [ ] **Clarity**: Gereksiz yan cümleleri at, net emir kipleri kullan.
- [ ] **Compression**: Anlam kaybı olmadan token sayısını azalt (Stopwords temizliği vb.).
- [ ] **Prompt Chaining**: Tek bir dev prompt yerine görevleri küçük, zincirleme promptlara böl.

### Aşama 3: Verification (A/B Test)
- [ ] **Test**: Optimize edilmiş promptu eskisiyle aynı inputlar üzerinde kıyasla.
- [ ] **Score**: Yanıt doğruluğu, hızı ve maliyeti üzerinden puanla.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Token tasarrufu >%20 sağlandı mı? |
| 2 | Başarı oranı (Accuracy) düştü mü? |
| 3 | Modelin çıktı formatı tutarlı kalmaya devam ediyor mu? |
