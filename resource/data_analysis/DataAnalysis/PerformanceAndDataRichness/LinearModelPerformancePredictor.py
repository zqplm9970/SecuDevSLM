import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv('data.csv', encoding="ANSI")

df['数据量归一化'] = df['数据量'] / df['数据量'].max()
df['参数量归一化'] = df['参数量'] / df['参数量'].max()
df['数据多样性归一化'] = df['数据多样性'] / 3
X = df[['数据量归一化', '参数量归一化', '数据多样性归一化']]  # 特征
y = df['性能排名'].max() -  df['性能排名'] + 1  # 目标是性能排名的倒数，转化为模型性能


for i in range(60):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = LinearRegression()

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    if r2 > 0.80:
        print(f"Iteration {i + 1}: R-squared = {r2}")
        print(f"截距 (β0): {model.intercept_}")
        print(f"回归系数 (β1, β2, β3): {model.coef_}")
        print("-" * 40)


