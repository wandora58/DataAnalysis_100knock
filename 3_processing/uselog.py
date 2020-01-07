import pandas as pd

# 顧客の絞り込み

# データの読み込み
uselog = pd.read_csv('use_log.csv')

# 顧客ごとの月利用回数
uselog['usedate'] = pd.to_datetime(uselog['usedate'])
uselog['usemonth'] = uselog['usedate'].dt.strftime('%Y%m')
uselog_months = uselog.groupby(['usemonth', 'customer_id'], as_index=False).count()
uselog_months.rename(columns={'log_id':'count'}, inplace=True)
del uselog_months['usedate']

# 顧客ごとに絞り込み、平均、中央値、最大、最小値を算出
uselog_customer = uselog_months.groupby('customer_id').agg(['mean', 'median', 'max', 'min'])['count']
uselog_customer = uselog_customer.reset_index(drop=False)


#---------------------------------------------------------

# 定期利用しているか
# 毎週同じ曜日に来ている = 定期的に来ていると判断
# 顧客ごとに月/曜日の別に集計を行い、最大値が 4 以上の曜日が 1ヶ月でもあった顧客はフラグを 1 とする

uselog['weekday'] = uselog['usedate'].dt.weekday
uselog_weekday = uselog.groupby(['customer_id', 'usemonth', 'weekday'], as_index=False).count()[['customer_id', 'usemonth', 'weekday', 'log_id']]
uselog_weekday.rename(columns={'log_id':'count'}, inplace=True)

# 顧客ごとに最大値を取得し、その最大値が 4 以上ならフラグを立てる
uselog_weekday = uselog_weekday.groupby('customer_id', as_index=False).max()[['customer_id', 'count']]
uselog_weekday['routing_flg'] = 0
uselog_weekday['routing_flg'] = uselog_weekday['routing_flg'].where(uselog_weekday['count'] < 4, 1)
print(uselog_weekday.head())
