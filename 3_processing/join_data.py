import pandas as pd
from dateutil.relativedelta import relativedelta

# 顧客データと利用履歴データの結合

# データの読み込み
uselog = pd.read_csv('use_log.csv')
customer = pd.read_csv('customer_master.csv')
class_master = pd.read_csv('class_master.csv')
campaign_master = pd.read_csv('campaign_master.csv')

# 顧客データ
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

# 顧客ごとの月利用回数
uselog['usedate'] = pd.to_datetime(uselog['usedate'])
uselog['usemonth'] = uselog['usedate'].dt.strftime('%Y%m')
uselog_months = uselog.groupby(['usemonth', 'customer_id'], as_index=False).count()
uselog_months.rename(columns={'log_id':'count'}, inplace=True)
del uselog_months['usedate']

# 顧客ごとの月利用回数の平均、中央値、最大、最小値を算出
uselog_customer = uselog_months.groupby('customer_id').agg(['mean', 'median', 'max', 'min'])['count']
uselog_customer = uselog_customer.reset_index(drop=False)

# 顧客ごとに月/曜日の別に集計を行い、最大値が 4 以上の曜日が 1ヶ月でもあった顧客はフラグを 1 とする
uselog['weekday'] = uselog['usedate'].dt.weekday
uselog_weekday = uselog.groupby(['customer_id', 'usemonth', 'weekday'], as_index=False).count()[['customer_id', 'usemonth', 'weekday', 'log_id']]
uselog_weekday.rename(columns={'log_id':'count'}, inplace=True)

# 顧客ごと定期利用しているかのフラグ
uselog_weekday = uselog_weekday.groupby('customer_id', as_index=False).max()[['customer_id', 'count']]
uselog_weekday['routing_flg'] = 0
uselog_weekday['routing_flg'] = uselog_weekday['routing_flg'].where(uselog_weekday['count'] < 4, 1)

# データの結合
join_data = pd.merge(customer_join, uselog_customer, on='customer_id', how='left')
join_data = pd.merge(join_data, uselog_weekday[['customer_id', 'routing_flg']], on='customer_id', how='left')

# 欠損値確認
# print(join_data.isnull().sum())

# データの出力
del customer_join['class']
del customer_join['campaign_id']
dump_data = join_data[['customer_id', 'name', 'gender', 'start_date', 'end_date', 'membership_period', 'is_deleted', 'class_name', 'campaign_name', 'price', 'mean', 'median', 'max', 'min', 'routing_flg']]
dump_data.to_csv('dump_data.csv', index=False)
