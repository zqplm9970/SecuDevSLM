# Linear Regression: Performance vs Data Richness

This module analyzes how **model performance** is related to **data richness**, using linear regression and visualization techniques.

---

## Objectives

- Quantify relationships between performance and:
  - Number of parameters
  - Dataset size
  - Dataset diversity
- Compute regression coefficients (slope, intercept, and Pearson r)
- Visualize best-fit lines to understand the direction and strength of correlation

---

## Folder Contents

- `data.csv`  
  A CSV file containing model-level data including:
  - `model_name`
  - `model_parameters`
  - `dataset_size`
  - `diversity_score`
  - `performance_score`

- `LinearModelPerformancePredictor.py`  
  Script to calculate linear regression coefficients between `performance_score` and each richness factor. Prints:
  - Regression slope and intercept
  - Linear coefficient

- `RegressionLineDrawing.py`  
  Script to generate **scatter plots** with fitted **regression lines**, one for each richness dimension vs performance. Saves charts for visual interpretation.

---

## Requirements

Install required Python libraries:

```bash
pip install pandas matplotlib seaborn scikit-learn
```

---

## Usage

### 1. Run regression coefficient analysis:

```bash
python LinearModelPerformancePredictor.py --input data.csv
```

This will output linear regression equations and correlation coefficients for each factor.

### 2. Plot regression lines:

```bash
python RegressionLineDrawing.py --input data.csv --output plots
```




