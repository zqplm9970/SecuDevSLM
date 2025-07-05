import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
import matplotlib as mpl

file1 = "./model_result.csv"  
file2 = "./model_result2.csv"  

# 标签定义
x_label = "Performance Ranking"  
y_label_file1 = "iOS Noise Text Length"  
y_label_file2 = "Android Noise Text Length"  

df1 = pd.read_csv(file1, encoding='ANSI')
df2 = pd.read_csv(file2, encoding='ANSI')

def calculate_bollinger_bands(data, window=5):
    moving_avg = []
    upper_band = []
    lower_band = []

    for i in range(len(data)):
        if i+2 < window:
            window_data = data[:i+2]
        else:
            window_data = data[i+2-window:i+2]
        
        moving_avg.append(window_data.mean())
        std_dev = window_data.std()
        upper_band.append(moving_avg[-1] + 2 * std_dev)
        lower_band.append(moving_avg[-1] - 2 * std_dev)

    return pd.Series(moving_avg), pd.Series(upper_band), pd.Series(lower_band)


plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('seaborn-v0_8-whitegrid')  


fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
fig.patch.set_facecolor('white')  


ios_data = df1.sort_values(by="性能排名")
android_data = df2.sort_values(by="性能排名")


ios_moving_avg, ios_upper_band, ios_lower_band = calculate_bollinger_bands(ios_data["ios噪声文本长度"])
android_moving_avg, android_upper_band, android_lower_band = calculate_bollinger_bands(android_data["android噪声文本长度"])


ax.plot(ios_data["性能排名"], ios_data["ios噪声文本长度"], 
        color='blue', label=f'iOS', marker='o', markersize=8, 
        linewidth=2, alpha=0.9, markerfacecolor='blue', markeredgecolor='blue')


ax.plot(android_data["性能排名"], android_data["android噪声文本长度"], 
        color='red', label=f'Android', marker='^', markersize=8, 
        linewidth=2, alpha=0.9, markerfacecolor='red', markeredgecolor='red')

ax.plot(ios_data["性能排名"], ios_moving_avg, color='blue', linestyle=':', label=f'iOS Moving Average')
ax.fill_between(ios_data["性能排名"], ios_upper_band, ios_lower_band, color='blue', alpha=0.2, hatch='///', label=f'iOS Bollinger Bands ({ios_upper_band.iloc[-1]:.2f} - {ios_lower_band.iloc[-1]:.2f})')

ax.plot(android_data["性能排名"], android_moving_avg, color='red', linestyle='--', label=f'Android Moving Average')
ax.fill_between(android_data["性能排名"], android_upper_band, android_lower_band, color='red', alpha=0.2, hatch='O', label=f'Android Bollinger Bands ({android_upper_band.iloc[-1]:.2f} - {android_lower_band.iloc[-1]:.2f})')

ax.set_xlabel(x_label, fontsize=30, fontweight='bold')
ax.set_ylabel("Noise Text Length", fontsize=30, fontweight='bold')

import matplotlib.font_manager as fm

ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

ax.grid(True, linestyle='-', linewidth=0.5, alpha=0.7, color='lightgray')

y_min = min(ios_data["ios噪声文本长度"].min(), android_data["android噪声文本长度"].min())
y_max = max(ios_data["ios噪声文本长度"].max(), android_data["android噪声文本长度"].max())
ax.set_ylim(0, y_max * 1.1)  

title1 = "b"
plt.title(title1, fontsize=30, fontweight='bold', pad=15)

for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)
    spine.set_color('black')

plt.tight_layout()

plt.show()
