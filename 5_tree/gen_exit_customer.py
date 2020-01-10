import pandas as pd
from dateutil.relativedelta import relativedelta

# 退会した顧客データを作成

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

# 顧客データに退会申請した月を追加
exit_customer = customer.loc[customer['is_deleted']==1]
exit_customer['end_date'] = pd.to_datetime(exit_customer['end_date'])
exit_customer['exit_date'] = None
for i in range(len(exit_customer)):
    exit_customer['exit_date'].iloc[i] = exit_customer['end_date'].iloc[i] - relativedelta(months=1)
exit_customer['exitmonth'] = exit_customer['exit_date'].dt.strftime('%Y%m')

# 顧客データと前月(退会申請した月)と今月の利用回数の集計を結合
uselog.rename(columns={'usemonth':'exitmonth'}, inplace=True)
uselog['exitmonth'] = uselog['exitmonth'].astype('str')
exit_customer = pd.merge(uselog, exit_customer, on=['customer_id', 'exitmonth'], how='left')
print(exit_customer)

# ここで前月が退会申請した月のみとなるため、データが欠損値が多く発生
# 欠損値がある月はまだ退会していないので消去
# また前月の利用回数が無いデータもある → 削除
exit_customer = exit_customer.dropna(subset=['name'])
exit_customer = exit_customer.dropna(subset=['count_before'])
print(exit_customer.head())

# 確認
print(exit_customer.isnull().sum())
print(len(exit_customer))
print(len(exit_customer['customer_id'].unique()))

# データの出力
exit_customer.to_csv('exit_customer.csv', index=False)

# exitmonth : 退会申請した月
# count_now : 退会申請した月の利用回数
# count_before : 退会申請した前の月の利用回数

