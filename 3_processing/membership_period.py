import pandas as pd
from dateutil.relativedelta import relativedelta

# 会員期間を追加

# データの読み込み
customer = pd.read_csv('customer_master.csv')
class_master = pd.read_csv('class_master.csv')
campaign_master = pd.read_csv('campaign_master.csv')

# データの結合
customer_join = pd.merge(customer, class_master, on='class', how='left')
customer_join = pd.merge(customer_join, campaign_master, on='campaign_id', how='left')

# 会員期間計算用の列を追加(まだ退会していない顧客(NA)は 20190430 で埋める)
customer_join['calc_date'] = pd.to_datetime(customer_join['end_date'])
customer_join['calc_date'] = customer_join['calc_date'].fillna(pd.to_datetime('20190430'))

# 会員期間の計算
customer_join['membership_period'] = 0
customer_join['start_date'] = pd.to_datetime(customer_join['start_date'])
for i in range(len(customer_join)):
    delta = relativedelta(customer_join['calc_date'].iloc[i], customer_join['start_date'].iloc[i])
    customer_join['membership_period'].iloc[i] = delta.years*12 + delta.months
del customer_join['calc_date']
del customer_join['class']
print(customer_join.head())
