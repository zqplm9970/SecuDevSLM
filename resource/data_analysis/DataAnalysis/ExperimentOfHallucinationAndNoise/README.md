# Hallucination and Noise Attack Experiment Visualization

This module focuses on visualizing model behavior under **hallucination attacks** and **noise perturbation scenarios**. It includes tools to analyze and compare model performance across various conditions, such as input length, behavioral complexity, text framework, and platform differences (iOS vs Android).

---

## Objectives

- Investigate how hallucination and noise impact model outputs and performance
- Analyze behavioral robustness across various factors (text length, behavior categories, noise rounds, etc.)
- Compare the vulnerability and variation of model behavior between mobile platforms

---

## Folder Contents

`dataRichness_performance_NumberOfBehaviors.py` Analyzes how data richness and number of behavior categories impact performance

`performance_IllusionAttacksRound.py` Evaluates how performance varies across rounds of hallucination attacks 

`performance_IllusionTextGenerationFramework.py` Compares hallucination behavior across different text generation frameworks 

`performance_NoiseAttacksRounds.py` | Evaluates model robustness under multiple rounds of **noise-based attacks** 

`performance_NoiseCharacterCategory.py` Examines how performance varies across different categories of character-level noise

`performance_NoiseTextLength.py` Analyzes the relationship between input text length and robustness under noise attacks 

`performance_NumberOfBehaviorCategories.py` Visualizes how the number of behavior categories influences hallucination vulnerability 

`HeatMapBetweeniOSAndAndroid.py` Generates a heatmap showing differences in hallucination success rates between iOS and Android 

`model_1.csv` Binary results (e.g., 0/1) indicating whether hallucination occurred for each input on iOS vs Android 

`model_result.csv` Detailed test results on iOS under hallucination and noise attacks 

`model_result2.csv` Detailed test results on Android under hallucination and noise attacks 

---

## Output Types

- Heatmaps comparing mobile platform susceptibility
- Scatter plots showing performance correlations with data richness and behavior complexity

All output figures are saved in high resolution and can be used in reports or publications.






