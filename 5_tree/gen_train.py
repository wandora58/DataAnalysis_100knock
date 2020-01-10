import pandas as pd
from dateutil.relativedelta import relativedelta

# データの読み込み
continue_customer = pd.read_csv('continue_customer.csv')
exit_customer = pd.read_csv('exit_customer.csv')
exit_customer.rename(columns={'exitmonth':'usemonth'}, inplace=True)
del exit_customer['exit_date']

# データの縦結合
train_data = pd.concat([continue_customer, exit_customer], ignore_index=True)

# 予測する月までの在籍期間を追加
train_data['period'] = 0
train_data['now_date'] = pd.to_datetime(train_data['usemonth'], format='%Y%m')
train_data['start_date'] = pd.to_datetime(train_data['start_date'])
for i in range(len(train_data)):
    delta = relativedelta(train_data['now_date'][i], train_data['start_date'][i])
    train_data['period'][i] = int(delta.years*12 + delta.months)

# 説明変数は キャンペーン区分、クラス名、性別、1ヶ月前の利用回数、定期利用しているか、在籍期間
# 目的変数は 退会しているかどうか
target_col = ['campaign_name', 'class_name', 'gender', 'count_before', 'routing_flg', 'period', 'is_deleted']
train_data = train_data[target_col]

# 文字列型の変数を処理できるように整形
train_data = pd.get_dummies(train_data)
del train_data['campaign_name_通常']
del train_data['class_name_ナイト']
del train_data['gender_M']

# データの出力
train_data.to_csv('train_data.csv', index=False)

