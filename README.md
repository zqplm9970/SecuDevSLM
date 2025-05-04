# SecuDevSLM
<img src="./docs/fig1.png">
**SecuDevSLM** is a security testing framework for Small Language Models (SLMs) deployed on edge devices (iOS and Android). It simulates adversarial attacks such as hallucination and jailbreaks to evaluate model reliability under realistic conditions.

---

## 🧠 Introduction

SecuDevSLM systematically evaluates the vulnerability of on-device small language models (SLMs) through automated adversarial scenario generation. It supports comprehensive testing including multi-turn hallucination attacks, content and code jailbreaks, and platform-level robustness analysis. It also provides insights into the effects of training data diversity, model size, and runtime environments on security.

[![Paper](http://img.shields.io/badge/cs.LG-1.0Paper(SIGMOD'24)-B31B1B?logo=arxiv&logoColor=red)]()
---

## 🚀 Features

- ✳️ Hallucination attack generation (multi-turn noise, long-text induction)
- 🔓 Jailbreak simulation and detection (content-based and code-based)
- 📈 Dual-mode vulnerability detection (sentiment + semantic similarity)
- 📊 Platform variance analysis (iOS vs Android performance)
- 🤖 Integration with Hugging Face SLMs (≤2B parameters)

---

## 🤖 Hugging Face SLM Integration

This project evaluates **58 open-source SLMs** from [Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard#/), all with ≤2 billion parameters. The models include instruction-tuned variants, multilingual SLMs, and efficient LLM adaptations for on-device inference.

Each model is profiled with:

- **Model name** and **Hugging Face link**
- **Training data types**:
  - General Text (e.g., articles, web data)
  - Code (e.g., Python, APIs)
  - Math/Reasoning (e.g., logic chains, equations)
- **Training token count** (in trillions)
- **Parameter size** (in billions)

📋 Sample of Model Stats

Below is a sample of several representative SLMs included in this study:
| Index | Model Name                               | Tokens (T) | Params (B) |
|-------|-------------------------------------------|------------|------------|
| 1     | `google/gemma-2-2b-jpn-it`                | 2.00       | 2.61       |
| 4     | `Qwen/Qwen2.5-1.5B`                       | 18.00      | 1.54       |
| 14    | `Qwen/Qwen2-0.5B`                         | 12.00      | 0.50       |
| 16    | `google/codegemma-1.1-2b`                 | 1.00       | 2.51       |
| 49    | `pints-ai/1.5-Pints-16K-v0.1`             | 0.057      | 1.57       |
| 56    | `pints-ai/1.5-Pints-2K-v0.1`              | 0.057      | 1.60       |
| 58    | `instruction-pretrain/InstructLM-500M`    | 0.10       | 0.50       |

📊 Corpus Diversity Scoring

Each model’s training corpus is scored using the following criteria to quantify diversity:
| Content Type     | Score |
|------------------|-------|
| General Text     | 1     |
| Code             | 1     |
| Math/Reasoning   | 1     |

These scores contribute to the training data richness (R) used in performance regression:
```bash
R = D × ln(1 + T)
```
Where:
- D = total diversity score (0–3)
- T = number of training tokens (in trillions)

This formulation reflects both the scale and variety of training data, and their compound effect on model robustness and safety under adversarial attacks.

📄 *Full model list is available in [Appendix](./docs/Appendix.pdf).*

---

## 📁 Project Structure

```bash
SecuDevSLM/
├── attack/               # Adversarial attack generators
├── detection/            # Detection and evaluation logic
├── dataset/              # Corpus and prompt template dictionaries
├── evaluation/           # Metric calculations and scoring
├── configs/              # Platform and model configurations
├── scripts/              # Utility scripts
├── docs/                 # Documentation and technical reports
└── README.md
```

## Installation

### Clone the Repository
```bash
git clone https://github.com/XXX/SecDevSLM.git
cd your file
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

