import pandas as pd
from dateutil.relativedelta import relativedelta

# 顧客ごとの月別利用回数
uselog = pd.read_csv('use_log.csv')
uselog['usedate'] = pd.to_datetime(uselog['usedate'])
uselog['usemonth'] = uselog['usedate'].dt.strftime('%Y%m')
uselog_months = uselog.groupby(['usemonth', 'customer_id'], as_index=False).count()
uselog_months.rename(columns={'log_id':'count'}, inplace=True)
del uselog_months['usedate']

# 訓練データと教師データの作成
year_months = list(uselog_months['usemonth'].unique())
train_data = pd.DataFrame()
for i in range(6, len(year_months)):
    tmp = uselog_months.loc[uselog_months['usemonth']==year_months[i]]
    tmp.rename(columns={'count':'count_pred'}, inplace=True)
    for j in range(1, 7):
        tmp_before = uselog_months.loc[uselog_months['usemonth']==year_months[i-j]]
        del tmp_before['usemonth']
        tmp_before.rename(columns={'count':'count_{}'.format(j-1)}, inplace=True)
        tmp = pd.merge(tmp, tmp_before, on='customer_id', how='left')
    train_data = pd.concat([train_data, tmp], ignore_index=True)

# 欠損値処理
train_data = train_data.dropna()
train_data = train_data.reset_index(drop=True)

# 特徴生成　会員期間の付与
customer = pd.read_csv('dump_data.csv')
train_data = pd.merge(train_data, customer[['customer_id', 'start_date']], on='customer_id', how='left')
train_data['now_date'] = pd.to_datetime(train_data['usemonth'], format='%Y%m')
train_data['start_date'] = pd.to_datetime(train_data['start_date'])
train_data['period'] = 0
for i in range(len(train_data)):
    delta = relativedelta(train_data['now_date'][i], train_data['start_date'][i])
    train_data['period'][i] = delta.years*12 + delta.months

# データの出力
train_data.to_csv('train_data.csv', index=False)



