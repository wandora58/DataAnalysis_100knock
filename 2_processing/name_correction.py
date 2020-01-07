import pandas as pd

# 商品名の補正

# データ読み込み
uriage_data = pd.read_csv('uriage.csv') # 売り上げ履歴
print(uriage_data.head())

# 現状確認 >> 99(A~Z の 26 種類なら正しい)
print(len(pd.unique(uriage_data.item_name)))

# 揺れの補正
uriage_data['item_name'] = uriage_data['item_name'].str.upper()
uriage_data['item_name'] = uriage_data['item_name'].str.replace('  ','')
uriage_data['item_name'] = uriage_data['item_name'].str.replace(' ','')
print(uriage_data.sort_values(by=['item_name'], ascending=True))

# 確認
print(pd.unique(uriage_data.item_name))
print(len(pd.unique(uriage_data.item_name)))
