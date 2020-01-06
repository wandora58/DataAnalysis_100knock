import pandas as pd

# データの読み込み

print('顧客情報')
customer_master = pd.read_csv('customer_master.csv')  # 顧客情報
print(customer_master.head())

print('商品データ')
item_master = pd.read_csv('item_master.csv')  # 商品データ
print(item_master.head())

print('購入明細')
transaction_1 = pd.read_csv('transaction_1.csv')  # 購入明細
print(transaction_1.head())
