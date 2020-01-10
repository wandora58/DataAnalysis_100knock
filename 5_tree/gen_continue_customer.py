import pandas as pd
from dateutil.relativedelta import relativedelta

# 継続している顧客データを作成

# データの読み込み
customer = pd.read_csv('customer.csv')
uselog_months = pd.read_csv('uselog_months.csv')

# 前月と今月の利用回数の集計
year_months = list(uselog_months['usemonth'].unique())
uselog = pd.DataFrame()
for i in range(1, len(year_months)):
    tmp = uselog_months.loc[uselog_months['usemonth']==year_months[i]]
    tmp.rename(columns={'count':'count_now'}, inplace=True)
    tmp_before = uselog_months.loc[uselog_months['usemonth']==year_months[i-1]]
    del tmp_before['usemonth']
    tmp_before.rename(columns={'count':'count_before'}, inplace=True)
    tmp = pd.merge(tmp, tmp_before, on='customer_id', how='left')
    uselog = pd.concat([uselog, tmp], ignore_index=True)

# 継続している顧客データを絞り込み、
# 前月と今月の利用回数の集計を結合させて、
# 継続している顧客データを作成
continue_customer = customer.loc[customer['is_deleted']==0]
continue_customer = pd.merge(uselog, continue_customer, on='customer_id', how='left')

# ここで継続している顧客データのみとなるため、データが欠損値が発生 → 削除
# また前月の利用回数が無いデータもある → 削除
continue_customer = continue_customer.dropna(subset=['name'])
continue_customer = continue_customer.dropna(subset=['count_before'])

# 退会した顧客データは 1ヶ月分 のデータしかないが、
# 継続した顧客データは 数ヶ月分 あるため、
# アンダーサンプリングを行う
continue_customer = continue_customer.sample(frac=1).reset_index(drop=True)
continue_customer = continue_customer.drop_duplicates(subset='customer_id')

# 確認
print(continue_customer.isnull().sum())
print(len(continue_customer))

# データの出力
continue_customer.to_csv('continue_customer.csv', index=False)
