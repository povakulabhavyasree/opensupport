---
title: AI Call Center OpenEnv
emoji: 🎧
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# 📞 Call-Center OpenEnv: Multi-Turn AI Support Simulator

[![Hackathon: Meta + Hugging Face](https://img.shields.io/badge/Hackathon-Meta%20%2B%20Hugging%20Face-ff6b6b)](https://huggingface.co/docs/openenv)
[![OpenEnv: Supported](https://img.shields.io/badge/OpenEnv-Supported-00c8ff)](https://github.com/huggingface/openenv)

**Call-Center OpenEnv** is a high-fidelity, multi-turn RL environment designed for training and evaluating AI customer support agents. Built for the Meta + Hugging Face OpenEnv Hackathon, it simulates complex, high-stakes customer interactions with granular, multi-dimensional rewards.

---

## 🌟 Why This Environment?

Training a support agent isn't just about "getting the answer right." It's about **empathy, patience, and resolution**. This environment goes beyond simple text-matching by evaluating the agent's "soft skills" and technical accuracy simultaneously.

### 🚀 Real-World Utility
- **Automated Support Training**: Train RL agents to handle angry customers without human supervision.
- **Enterprise Benchmarking**: Compare different LLMs (Llama 3, Qwen, GPT-4) on their ability to resolve complex, multi-issue support tickets.
- **De-escalation Training**: Specifically rewards agents for calming down "Furious" customer states through validated empathy techniques.

### 🧠 Unique Features
1. **Multi-Turn Persistent State**: Unlike single-shot environments, the customer remembers previous turns, enabling complex follow-ups and cascading issues.
2. **Granular AI-Driven Grading**: Scoring is calculated on a 0.1 scale across four pillars: **Correctness, Politeness, Completeness, and Emotional Intelligence**.
3. **Realistic Data Injection**: Tasks include dynamic Order IDs, product-specific logic, and platinum-tier customer escalation policies.
4. **Multilingual Interaction**: Supports and rewards localized greetings (e.g., Tamil "Vanakkam!") while maintaining core English resolution logic.
5. **Intelligent Termination**: The environment detects when the agent has successfully "closed" the loop or if the customer is satisfied enough to end the call early.

---

## 🛠 Project Structure

- `environment.py`: The core OpenEnv-compliant multi-turn gym.
- `grader.py`: The logic engine for granular reward calculation and penalties.
- `tasks.py`: High-fidelity customer personas and scenario definitions.
- `inference.py`: Automated AI agent run logic using Hugging Face Router API.
- `openenv.yaml`: Configuration for OpenEnv compatibility.

---

## 🚦 Getting Started

### 1. Prerequisites
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
```bash
export HF_TOKEN="your_huggingface_token"
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="meta-llama/Llama-3.1-70B-Instruct" # Or any router model
```

### 3. Run Automated Training
```bash
python3 inference.py
```

---

## 📊 Scoring System (0.0 - 1.0)

| Criterion | Max Score | Description |
| :--- | :--- | :--- |
| **Correctness** | 0.3 | Accuracy of data (Order IDs, times, policies) |
| **Politeness** | 0.2 | Professionalism and courtesy |
| **Completeness** | 0.3 | Addressing all aspects of the customer's issue |
| **Emotion** | 0.2 | Empathy and de-escalation success |

**Penalties**:
- Short responses (< 30 chars): `-0.2`
- Rude/Dismissive: `-0.4`
- Irrelevant content: `-0.2`


## 🚀 Key Highlights

- Multi-turn conversational AI environment
- Emotion-aware customer handling (calm, neutral, angry)
- Multilingual support (English + Tamil)
- Real-world customer support simulation
- Designed for training AI agents in business automation (NexaFlow vision)

<<<<<<< HEAD

=======
>>>>>>> ac96f62 (add server folder for openenv)
## 🔗 API Endpoints (OpenEnv Validation)

This environment is deployed as a REST API using FastAPI and is compatible with OpenEnv automated checks.

### Available Endpoints

- `POST /reset`
  - Resets the environment
  - Returns initial observation

- `POST /step`
  - Takes an action (agent response)
  - Returns:
    - observation
    - reward
    - done
    - info

### Deployment

The API is served using:
- FastAPI
- Uvicorn
- Docker (Hugging Face Spaces)

This ensures compatibility with OpenEnv validators and real-time evaluation pipelines.

---

## 🏆 Hackathon Goals Met:
- ✅ **Realistic Simulation**: Multi-issue "Hard" tasks with Order ID tracking.
- ✅ **Granular Rewards**: 0.1 increment scoring with transparency.
- ✅ **Multi-Turn Support**: Full history tracking and conditional follow-ups.
- ✅ **OpenEnv Compliance**: Ready for `openenv.yaml` integration.

---
*Created for the Meta + Hugging Face OpenEnv Hackathon 2024.*
*Author: Pradeep Kumar*
# callcenter-openenv
