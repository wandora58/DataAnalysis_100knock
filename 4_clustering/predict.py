import pandas as pd
from sklearn import linear_model
import sklearn.model_selection

# データ読み込み(入会が 2018/4 以降を対象とする)
train_data = pd.read_csv('train_data.csv')
train_data['start_date'] = pd.to_datetime(train_data['start_date'])
train_data = train_data.loc[train_data['start_date']>=pd.to_datetime('20180401')]

# 訓練データと教師データに分ける
X = train_data[['count_0', 'count_1', 'count_2', 'count_3', 'count_4', 'count_5', 'period']]
y = train_data['count_pred']

# 検証データに分割
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y)

# モデル定義
model = linear_model.LinearRegression()

# モデル訓練
model.fit(X_train, y_train)

# 訓練精度と検証精度
print(model.score(X_train, y_train))
print(model.score(X_test, y_test))

# 説明変数の寄与係数確認
coef = pd.DataFrame({'feature_names':X.columns, 'coefficient':model.coef_})
print(coef)

