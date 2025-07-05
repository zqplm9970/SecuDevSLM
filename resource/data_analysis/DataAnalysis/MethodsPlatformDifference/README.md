# Platform Comparison: Bollinger Bands & Line Plot Visualization

This module focuses on comparing multiple models across different **platforms** (e.g., iOS, Android) under hallucination and noise conditions. It uses **Bollinger Bands** and **line plots** to visualize performance trends and variability.

---

## Objectives

- Compare hallucination robustness across different platforms and model variants
- Visualize platform-specific trends using:
  - **Line plots** (for performance metrics across categories or attack rounds)
  - **Bollinger Bands** (to highlight performance volatility over input index or time)
- Explore how factors like text length, behavior categories, or jailbreak status influence performance

---

## File Overview

- `legend.py`: Utility script to create unified legends for multi-platform visualizations
- `performance_IllusionAttackRounds.py`: Plots performance degradation across hallucination attack rounds for different platforms
- `performance_IllusionTextGenerationFramework.py`: Compares models across platforms under different generation frameworks
- `performance_iOSJailbreakBehaviors.py`: Analyzes hallucination differences between iOS and jailbroken iOS models
- `performance_NoiseAttacksRounds.py`: Visualizes platform robustness across noise attack rounds
- `performance_NoiseCharacterCategory.py`: Compares how each platform/model reacts to different character-level noise categories
- `performance_NoiseTextLength.py`: Evaluates the effect of text length on performance variability (with optional Bollinger Bands)
- `model_result.csv`: Hallucination/noise test results for iOS and jailbroken iOS models
- `model_result2.csv`: Equivalent test results for Android models


---

## Output Visualizations

- **Line plots** showing model/platform performance over:
  - Attack rounds
  - Input length
  - Frameworks
  - Categories
- **Bollinger Band charts** to show expected performance range and deviation over inputs
- **Comparative plots** for iOS vs Android vs iOS-Jailbroken

---

