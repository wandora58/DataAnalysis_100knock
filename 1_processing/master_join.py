import pandas as pd

# customer_master と item_master の横結合

# データの読み込み
transaction_1 = pd.read_csv('transaction_1.csv')  # 購入明細1
transaction_2 = pd.read_csv('transaction_2.csv')  # 購入明細2
transaction = pd.concat([transaction_1, transaction_2], ignore_index=True)

transaction_detail_1 = pd.read_csv('transaction_detail_1.csv')  # 購入明細の詳細1
transaction_detail_2 = pd.read_csv('transaction_detail_2.csv')  # 購入明細の詳細2
transaction_detail = pd.concat([transaction_detail_1, transaction_detail_2], ignore_index=True)

customer_master = pd.read_csv('customer_master.csv')  # 顧客情報
item_master = pd.read_csv('item_master.csv')  # 商品データ

# データの結合
join_data = pd.merge(transaction_detail,
                    transaction[['transaction_id', 'payment_date', 'customer_id']],
                    on='transaction_id', how='left')

join_data = pd.merge(join_data, customer_master, on='customer_id', how='left')
join_data = pd.merge(join_data, item_master, on='item_id', how='left')
print(join_data.head())
