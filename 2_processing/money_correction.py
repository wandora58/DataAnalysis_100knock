import pandas as pd

# 金額の補正

# データ読み込み
uriage_data = pd.read_csv('uriage.csv') # 売り上げ履歴
print(uriage_data.head())

# 商品名の補正
uriage_data['item_name'] = uriage_data['item_name'].str.upper()
uriage_data['item_name'] = uriage_data['item_name'].str.replace('  ','')
uriage_data['item_name'] = uriage_data['item_name'].str.replace(' ','')

# 欠損値があるか無いか確認
print(uriage_data.isnull().any(axis=0))

# 欠損値補間 → 期間中変動が無いため、他の同じ商品の単価から補間
fig_is_null = uriage_data['item_price'].isnull()
for trg in list(uriage_data.loc[fig_is_null, 'item_name'].unique()):
    price = uriage_data.loc[(~fig_is_null) & (uriage_data['item_name']==trg), 'item_price'].max()
    uriage_data['item_price'].loc[(fig_is_null) & (uriage_data['item_name']==trg)] = price

# 検証
print(uriage_data.isnull().any(axis=0))
for trg in list(uriage_data['item_name'].sort_values().unique()): # 商品名のソートした重複なしリスト
    print(trg + ' max:' + str(uriage_data.loc[uriage_data['item_name']==trg]['item_price'].max()) + ' min:' + str(uriage_data.loc[uriage_data['item_name']==trg]['item_price'].min(skipna=False)))
