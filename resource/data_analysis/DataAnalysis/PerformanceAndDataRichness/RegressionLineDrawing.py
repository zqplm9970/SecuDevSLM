import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm


df = pd.read_csv('data.csv', encoding = "ANSI")
df['数据量归一化'] = df['数据量'] / df['数据量'].max()
df['参数量归一化'] = df['参数量'] / df['参数量'].max()
df['数据多样性归一化'] = df['数据多样性'] / 3
df['因变量'] = 12.803 * df['数据量归一化'] + 32.696 * df['数据多样性归一化'] + 23.856 * df['参数量归一化'] - 4.156

plt.figure(figsize=(8, 6))
x = df['因变量']
y = df['性能排名'].max() - df['性能排名'] + 1
plt.scatter(x, y, color='b', alpha=0.7)


for i in range(len(df)):
    plt.annotate(
        df['性能排名'][i],
        (x[i], y[i]),
        textcoords="offset points",
        xytext=(2.3, 0),
        ha='left',
        va='center',
        fontsize=13,
        fontweight='bold'
    )


coefficients = np.polyfit(x, y, deg=1)
poly = np.poly1d(coefficients)
regression_line = poly(x)


plt.plot(x, regression_line, color='r', label='Linear Regression')


# plt.title('Relationship between data richness and performance ranking', fontweight='bold', fontsize=20)
plt.xlabel('Model prediction performance', fontweight='bold', fontsize=20)
plt.ylabel('Actual performance of the model', fontweight='bold', fontsize=20)


font_properties = fm.FontProperties(weight='bold', size=17)  # 设置加粗和字体大小


plt.legend(loc='best', frameon=True, prop=font_properties)

plt.show()
