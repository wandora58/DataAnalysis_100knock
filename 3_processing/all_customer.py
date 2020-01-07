import pandas as pd

# 顧客データを整形

# データの読み込み
customer = pd.read_csv('customer_master.csv')
class_master = pd.read_csv('class_master.csv')
campaign_master = pd.read_csv('campaign_master.csv')

# データの結合
customer_join = pd.merge(customer, class_master, on='class', how='left')
customer_join = pd.merge(customer_join, campaign_master, on='campaign_id', how='left')

# 加工したら確認すること
# print(len(customer_join)) # 4192
# print(customer_join.isnull().sum())

#--------------------------------------------------------

# 基礎統計量の確認

# 会員区分
print(customer_join.groupby('class_name').count()['customer_id'])

# キャンペーン区分
print(customer_join.groupby('campaign_name').count()['customer_id'])

# 性別
print(customer_join.groupby('gender').count()['customer_id'])

# すでに退会済みか
print(customer_join.groupby('is_deleted').count()['customer_id'])

# 2018年4月〜2019年3月に入会した人数
customer_join['start_date'] = pd.to_datetime(customer_join['start_date'])
customer_start = customer_join.loc[customer_join['start_date'] > pd.to_datetime('20180401')]
print('入会人数 ', len(customer_start))
