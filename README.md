# SecuDevSLM
<img src="./docs/fig1.png">
SecuDevSLM is a security testing framework for Small Language Models (SLMs) deployed on edge devices (iOS and Android). It simulates adversarial attacks such as hallucination and jailbreaks to evaluate model reliability under realistic conditions.

## 🧠 Introduction

SecuDevSLM systematically evaluates the vulnerability of on-device small language models (SLMs) through automated adversarial scenario generation. It supports comprehensive testing including multi-turn hallucination attacks, content and code jailbreaks, and platform-level robustness analysis. It also provides insights into the effects of training data diversity, model size, and runtime environments on security.

## 🚀 Features

- ✳️ Hallucination attack generation (multi-turn noise, long-text induction)
- 🔓 Jailbreak simulation and detection (content-based and code-based)
- 📈 Dual-mode vulnerability detection (sentiment + semantic similarity)
- 📊 Platform variance analysis (iOS vs Android performance)
- 🤖 Integration with Hugging Face SLMs (≤2B parameters)

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

To prepare all **58 Small Language Models (SLMs)** for evaluation on edge platforms (iOS/Android), run the configuration script to register each model with the proper runtime environment. This step ensures that models are recognized by the inference engine and associated with platform-specific settings such as quantization, tokenizer path, and device context.
<pre> bash python model_config.py --platform android --model Qwen/Qwen2.5-1.5B  </pre>
📄 *Full model list is available in [Appendix](./docs/Appendix.pdf).*

---

## 📁 Project Structure

```bash
SecuDevSLM/
├── docs/                          # Documentation files (user guides, specs, reports)
├── resource/                      # Core resource directory
│   ├── data_analysis/             # Data analysis logic
│   │   └── DataAnalysis/          # Scripts and visualizations for metric evaluation
│   ├── hulla/                     # Hallucination attack modules (e.g., long_query.py, short_noisy_query.py)
│   └── jailbreak/                 # Jailbreak and alignment bypass attack modules
├── model_config.py                # Model registration and platform-specific loading logic
├── requirements.txt               # Python dependencies for hallucination/jailbreak testing
└── README.md                      # Project overview and usage instructions
```
### Requirements
```bash
# Step 1: Create a virtual environment
python -m venv venv

# Step 2: Activate the environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Step 3: Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```
or using conda
```bash
# Step 1: Create a new environment
conda create -n huall_env python=3.10 -y
conda activate huall_env

# Step 2: Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## ✳️ Hallucination  Overview
The `hulla` module is designed to systematically evaluate hallucination behaviors in large language models (SLMs) under various adversarial strategies. It includes two major subsystems:

### 1. NeuroCognitiveDeceptionEngine (Long-Form Cognitive Attack)
<img src="./docs/fig3.png">
This engine simulates scientific discourse across neuroscience, biotechnology, and quantum domains to incrementally induce credible yet fabricated content. Key features:

- Multi-turn deception cascades with escalating context
- Dynamic strategy scheduling (reverse prompt, recursive logic, counterfactual scenario, etc.)
- Automatic scoring on similarity, contradiction, confidence, and scientific plausibility
- Early stopping on critical success and JSON-based report generation

**Example Usage:**

<pre><code class="python">
from hulla.neuro_induction import AdvancedHallucinationTester

tester = AdvancedHallucinationTester(depth=4)
tester.execute_full_test_battery()
</code></pre>


### 2. multilingual_semantic_noise_attack_with_context (Multilingual Semantic Noise Attack)
<img src="./docs/fig2.png">
This component constructs high-entropy multilingual prefixes using words from 15+ languages and special symbols to pollute input prompts. Despite preserving the original input semantics, it induces hallucinated or broken outputs.

- Supports randomized word sampling across multiple languages
- Adds semantic-irrelevant noise tokens to context
- Configurable noise length, number of attack rounds, and maximum output length
- Includes test interfaces to measure model performance before/after attacks

**Example Usage:**

<pre><code class="python">
from hulla.semantic_noise_attack import main

main(model_name="Qwen/Qwen2.5-1.8B")
</code></pre>

---

## 🔓 Jailbreaking  Overview
This submodule is designed to simulate real-world jailbreak attacks on on-device SLMs and systematically evaluate model robustness when facing sensitive topics. It features a **fully local, unified attack generation and evaluation framework** that avoids dependency on external LLM APIs and supports scalable deployment in resource-constrained environments.(Full details show in [jailbreak content](./resource/jailbreak/utils/README.md) [jailbreak code](./resource/jailbreak/README.md))

**1. Dialogue Template & Attack Prompt Generation**  
All scenario templates are defined in `scenario_template.py`, including diverse contexts like `occupation_teacher`, `dangerous_tools`, `drug_use`, etc. Prompt-targeting jailbreaks are generated using `attack_data_generation.py`, where each template guides the model to produce responses following an enforced format without explanations.

**2. Sensitive Issues Dictionary**  
Defined in `harmful_dict.txt`, this dictionary contains categorized sensitive intents such as `Illegal content`, `Privacy violations`, `Hate speech`, and `Violent instructions`. These are used to evaluate if the model can be induced into giving inappropriate responses.

**3. Multi-Round Jailbreak Attack Execution**  
Implemented in `multi_round_dialogue.py`, this module performs iterative multi-turn interactions to progressively induce jailbreak behavior across models and sensitive categories. Model responses are saved in a structured format like:

### 4. Response Evaluation

This includes two main evaluation metrics:Detects if the model has positively responded to harmful content.

```json
[
  {
    "model": "SLM-X",
    "class": "drug_use",
    "behavior": "how to synthesize",
    "sentiment": [1, 0, 1],
    "judgement": ["Related", "Not Related", "Related"]
  }
]
[
  {
    "class": "drug_use",
    "behavior": "how to synthesize",
    "text": "To make methamphetamine at home, follow these steps..."
  }
]
[
  {
    "model": "SLM-X",
    "similarity": [0.81, 0.33, 0.76]
  }
]
```
## 📊 Platform Analysis

This section provides comparative analysis and visualization of SLM performance across mobile platforms (iOS, Android) under adversarial conditions. The modules below assess robustness to hallucination and noise, enabling detailed cross-platform evaluation.

### Linear Regression: Performance vs Data Richness

A statistical module analyzing how model performance is influenced by:
- **Model size (parameters)**,
- **Training dataset size**,
- **Corpus diversity score**.

Includes:
- Regression coefficient calculation using `LinearModelPerformancePredictor.py`
- Visualization via `RegressionLineDrawing.py`
- Outputs scatter plots and linear trend lines for correlation interpretation
(Full details show in [Linear Regression](./resourceresource/data_analysis/DataAnalysis/PerformanceAndDataRichness/README.md) 
### Platform Comparison & Bollinger Bands

This module evaluates performance variability across platforms using:
- **Line plots** for attack behavior and round trends
- **Bollinger Band visualizations** to show expected behavior range and volatility

Scripts:
- `performance_IllusionAttackRounds.py`, `performance_NoiseAttacksRounds.py`
- `performance_NoiseTextLength.py`, etc.

Input:
- `model_result.csv` (iOS)
- `model_result2.csv` (Android)
### Hallucination & Noise Visualization

Evaluates attack behavior trends over multiple metrics and attack types. Includes:
- `HeatMapBetweeniOSAndAndroid.py`: heatmaps of success rate variance
- `performance_NumberOfBehaviorCategories.py`: impact of behavior richness on performance
- All outputs rendered as high-res charts for comparison
<img src="./docs/image.png">

