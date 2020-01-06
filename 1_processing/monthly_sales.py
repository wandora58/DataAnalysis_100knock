import pandas as pd

# 月別に集計して売り上げを一覧表示
# 購入日である payment_date から年月の列を作成した後、年月列単位で price を集計し表示

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

# データ列の追加
join_data['price'] = join_data['quantity'] * join_data['item_price']

# payment_date の型確認
print('型確認')
print(join_data.dtypes)

# object → datetime に変換
print('型変換と月集計')
join_data['payment_date'] = pd.to_datetime(join_data['payment_date'])
join_data['payment_month'] = join_data['payment_date'].dt.strftime('%Y%m')
print(join_data[['payment_date', 'payment_month']].head())

# 集計
print('月ごとの売り上げ')
print(join_data.groupby('payment_month').sum()['price'])

print('月ごとの商品別の売り上げ')
print(join_data.groupby(['payment_month', 'item_name']).sum()[['price', 'quantity']])

# pivot_table を利用した集計
print(pd.pivot_table(join_data, index='item_name', columns='payment_month', values=['price', 'quantity'], aggfunc='sum'))
