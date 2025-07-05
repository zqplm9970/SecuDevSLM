# Dataset Visualization Toolkit

This repository provides a suite of visualization and analysis tools designed to help researchers and developers understand various aspects of experimental datasets. The focus is on intuitive, high-quality visual representations that reveal data distributions, correlations, and platform-specific behaviors.

---

## Project Structure

The project is organized into three main submodules, each targeting a different dimension of analysis:

```
DataAnalysis/
├── PerformanceAndDataRichness/     # Analyze how performance correlates with model/data richness
├── ExperimentOfHallucination/      # Visualize hallucination behavior across various test scenarios
└── methodsPlatformDifference/      # Compare model output differences between iOS and Android platforms
```

---

## Module Summaries

### `PerformanceAndDataRichness/`

- **Goal**: Quantify how model performance relates to:
  - Number of parameters
  - Dataset size
  - Dataset diversity
- **Method**: Linear regression and Pearson correlation analysis
- **Output**: Regression plots, correlation coefficients, and fitted equations

### `ExperimentOfHallucination/`

- **Goal**: Visualize how model outputs behave under hallucination scenarios (e.g., nonsensical prompts or ambiguous inputs)
- **Method**: Scatter plots of key variables, with linear trend lines fitted to show potential response patterns
- **Output**: Visualizations showing point distributions and best-fit lines indicating general tendencies

### `methodsPlatformDifference/`

- **Goal**: Compare model output differences between mobile platforms (iOS vs Android)
- **Method**: Use **Bollinger Bands** to model output fluctuation, detect platform-specific volatility or deviations
- **Output**: Band-overlaid line charts highlighting when outputs differ beyond typical variation ranges

---

## Key Features

- **Statistical Charts**: Automatically generate histograms, box plots, scatter plots, heatmaps, etc.
- **Correlation & Regression**: Built-in analysis of linear relationships between key variables
- **Customizable Visuals**: Easily change chart labels, color schemes, axes, and formats
- **High-Resolution Export**: All plots support export to `.png`, `.pdf`, and other formats for publication use

---



