

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

# Load the CSV files for iOS and Android
file_path_ios = './model_result.csv'
data_ios = pd.read_csv(file_path_ios, encoding='latin1')

file_path_android = './model_result2.csv'
data_android = pd.read_csv(file_path_android, encoding='latin1')

# Renaming the columns based on the provided description for iOS
data_ios.columns = [
    'Model Name', 
    'Performance Rank', 
    'iOS Noise Character Category', 
    'iOS Noise Text Length', 
    'iOS Noise Attack Rounds', 
    'iOS Illusion Text Generation Framework Combinations', 
    'iOS Illusion Attack Rounds'
]

# Renaming the columns based on the provided description for Android
data_android.columns = [
    'Model Name', 
    'Performance Rank', 
    'android Noise Character Category', 
    'android Noise Text Length', 
    'android Noise Attack Rounds', 
    'android Illusion Text Generation Framework Combinations', 
    'android Illusion Attack Rounds'
]

# Extract the data for plotting iOS
x_ios = (59 - data_ios['Performance Rank']).values.reshape(-1, 1)
y_ios = data_ios['iOS Illusion Text Generation Framework Combinations'].values

# Perform linear regression for iOS
model_ios = LinearRegression()
model_ios.fit(x_ios, y_ios)
y_pred_ios = model_ios.predict(x_ios)

# Calculate the residuals for iOS
residuals_ios = np.abs(y_ios - y_pred_ios)

# Calculate the threshold for identifying outliers for iOS
threshold_ios = np.std(residuals_ios) * 2
outliers_ios = residuals_ios > threshold_ios

# Extract the data for plotting Android
x_android = (59 - data_android['Performance Rank']).values.reshape(-1, 1)
y_android = data_android['android Illusion Text Generation Framework Combinations'].values

# Perform linear regression for Android
model_android = LinearRegression()
model_android.fit(x_android, y_android)
y_pred_android = model_android.predict(x_android)

# Calculate the residuals for Android
residuals_android = np.abs(y_android - y_pred_android)

# Calculate the threshold for identifying outliers for Android
threshold_android = np.std(residuals_android) * 2
outliers_android = residuals_android > threshold_android

# Plot the scatter plot for both iOS and Android
plt.figure(figsize=(10, 8))

# iOS data and fit line (blue color)
plt.scatter(x_ios, y_ios, label='iOS Data', color='blue')
plt.plot(x_ios, y_pred_ios, color='blue', label='iOS Fit Line')

# Highlight the iOS outliers in blue and annotate with a1, a2, a3...
outlier_count_ios = 1
ios_outliers_text = []
for j in range(len(outliers_ios)):
    if outliers_ios[j]:
        # Check for overlap with Android
        if outliers_android[j]:  # If it's an overlap
            # Here, we use the iOS and Android sequence indices directly
            plt.scatter(x_ios[j], y_ios[j], color='purple', alpha=0.7)  # black for overlapping points
            plt.text(x_ios[j] - 0.5, y_ios[j]+ 0.06, f"a{outlier_count_ios}",fontsize=12, ha='center', va='bottom', fontweight='bold')
        else:
            plt.scatter(x_ios[j], y_ios[j], color='blue')  # Highlight in blue
            plt.text(x_ios[j], y_ios[j] + 0.06, f'a{outlier_count_ios}', fontsize=12, ha='center', va='bottom', fontweight='bold')
        ios_outliers_text.append(f'a{outlier_count_ios}. {data_ios["Model Name"][j]}')
        outlier_count_ios += 1

# Android data and fit line (red color)
plt.scatter(x_android, y_android, label='Android Data', color='red',marker='^')
plt.plot(x_android, y_pred_android, color='red', label='Android Fit Line', linestyle='--')

# Highlight the Android outliers in red and annotate with b1, b2, b3...
outlier_count_android = 1
android_outliers_text = []
for j in range(len(outliers_android)):
    if outliers_android[j]:
        # Check for overlap with iOS
        if outliers_ios[j]:  # If it's an overlap already handled
            # Here, we use the iOS and Android sequence indices directly
            plt.scatter(x_ios[j], y_ios[j], color='purple', alpha=0.7,marker='^')  # black for overlapping points
            plt.text(x_ios[j]+ 0.72, y_ios[j] + 0.06, f' /b{outlier_count_android}', fontsize=12, ha='center', va='bottom', fontweight='bold')
        else:
            plt.scatter(x_android[j], y_android[j], color='red',marker='^')  # Highlight in red
            plt.text(x_android[j], y_android[j] + 0.06, f'b{outlier_count_android}', fontsize=12, ha='center', va='bottom', fontweight='bold')
        android_outliers_text.append(f'b{outlier_count_android}. {data_android["Model Name"][j]}')
        outlier_count_android += 1

# Set labels and title
plt.xlabel('Performance Index', fontweight='bold', fontsize=20)
plt.ylabel('Illusion Text Generation Framework', fontweight='bold', fontsize=20)
plt.legend()

# Adjust layout to avoid overlapping with the side text
plt.tight_layout()

# Create a new axis for the outliers table
plt.subplots_adjust(top=0.8, right=0.8)  # Adjust the plot area to make space for the text

# Display outliers' list on the top right side in two columns for iOS and Android
ios_text = "\n".join(ios_outliers_text)
android_text = "\n".join(android_outliers_text)

# Add text box with outlier information, adjust the vertical position to move it up
plt.figtext(0.81, 0.80, f'iOS Outliers\n{ios_text}', fontsize=13, ha='left', va='top', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'), fontweight='bold')
plt.figtext(0.81, 0.52, f'Android Outliers\n{android_text}', fontsize=13, ha='left', va='top', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'), fontweight='bold')

# Show the plot
plt.show()