import pandas as pd

# データの読み込み

uselog = pd.read_csv('use_log.csv')
print('ジムの利用履歴', len(uselog))
print(uselog.head())

customer = pd.read_csv('customer_master.csv')
print('顧客データ', len(customer))
print(customer.head())

class_master = pd.read_csv('class_master.csv')
print('顧客区分', len(class_master))
print(class_master.head())

campaign_master = pd.read_csv('campaign_master.csv')
print('キャンペーン区分', len(campaign_master))
print(campaign_master.head())
