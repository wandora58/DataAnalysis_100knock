import pandas as pd

# 最新の顧客データを整形

# データの読み込み
customer = pd.read_csv('customer_master.csv')
class_master = pd.read_csv('class_master.csv')
campaign_master = pd.read_csv('campaign_master.csv')

# データの結合
customer_join = pd.merge(customer, class_master, on='class', how='left')
customer_join = pd.merge(customer_join, campaign_master, on='campaign_id', how='left')

# 最新月(2019年3月)に在籍している顧客を絞り込み
customer_join['end_date'] = pd.to_datetime(customer_join['end_date'])
customer_newer = customer_join.loc[(customer_join['end_date'] >= pd.to_datetime('20190331')) | (customer_join['end_date'].isna())]

# 確認
# print(customer_newer['end_date'].unique())

#-----------------------------------------------------------------
# 基礎統計量の確認

# 会員区分
print(customer_newer.groupby('class_name').count()['customer_id'])

# キャンペーン区分
print(customer_newer.groupby('campaign_name').count()['customer_id'])

# 性別
print(customer_newer.groupby('gender').count()['customer_id'])
