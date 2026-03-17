---
name: ai-ml-technologies
description: Master AI, machine learning, LLMs, prompt engineering, and blockchain development. Use when building AI applications, working with LLMs, or developing smart contracts.
sasmp_version: "1.3.0"
bonded_agent: 05-ai-emerging-technologies
bond_type: PRIMARY_BOND
---

# AI & Emerging Technologies Skill

## Quick Start - OpenAI API

```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")

# Simple completion
response = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": "You are helpful assistant"},
    {"role": "user", "content": "Explain machine learning"}
  ],
  temperature=0.7,
  max_tokens=500
)

print(response.choices[0].message.content)
```

## Core Technologies

### AI & LLMs
- OpenAI API (GPT-4)
- Claude API (Anthropic)
- Open-source LLMs (Llama, Mistral)
- LangChain for applications
- Vector databases (Pinecone, Weaviate)

### Machine Learning
- TensorFlow / PyTorch
- scikit-learn
- XGBoost
- Hugging Face Transformers

### Blockchain & Web3
- Solidity for smart contracts
- Web3.js / Ethers.js
- Hardhat development
- Foundry

### Game Engines
- Unity (C#)
- Unreal Engine (C++)
- Godot (GDScript)

## Best Practices

1. **AI Ethics** - Consider societal impact
2. **Testing** - Rigorous evaluation
3. **Monitoring** - Track model performance
4. **Documentation** - Clear decision records
5. **Security** - Smart contract auditing
6. **Cost Optimization** - Minimize API usage
7. **Version Control** - Track models and prompts
8. **Responsible AI** - Bias and fairness

## Resources

- [OpenAI Documentation](https://platform.openai.com/docs)
- [LangChain Documentation](https://langchain.readthedocs.io/)
- [Solidity Documentation](https://docs.soliditylang.org/)
- [Pytorch Documentation](https://pytorch.org/)
