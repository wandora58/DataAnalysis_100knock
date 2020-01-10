from sklearn.tree import DecisionTreeClassifier
import sklearn.model_selection
import pandas as pd

# データの読み込み
train_data = pd.read_csv('train_data.csv')
exit = train_data.loc[train_data['is_deleted']==1]
conti = train_data.loc[train_data['is_deleted']==0].sample(len(exit))

# 教師データと訓練データの作成
X = pd.concat([exit, conti], ignore_index=True)
y = X['is_deleted']
del X['is_deleted']
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y)

# 決定木モデル
model = DecisionTreeClassifier(random_state=0)
model.fit(X_train, y_train)
print('test ', model.score(X_test, y_test))
print('train ', model.score(X_train, y_train))

# 過学習を起こしているのモデルのチューニング
model = DecisionTreeClassifier(random_state=0, max_depth=5)
model.fit(X_train, y_train)
print('after tunning')
print('test ', model.score(X_test, y_test))
print('train ', model.score(X_train, y_train))

# モデルに寄与している変数(特徴量)を確認
importance = pd.DataFrame({'feature_names': X.columns, 'coefficient': model.feature_importances_})
print(importance)