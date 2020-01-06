import pandas as pd
import matplotlib.pyplot as plt

# グラフで可視化

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

# object → datetime に変換
join_data['payment_date'] = pd.to_datetime(join_data['payment_date'])
join_data['payment_month'] = join_data['payment_date'].dt.strftime('%Y%m')

# pivot_table を利用した集計
graph_data = pd.pivot_table(join_data, index='payment_month', columns='item_name', values='price', aggfunc='sum')

# グラフに描画
plt.plot(list(graph_data.index), graph_data['PC-A'], label='PC-A')
plt.plot(list(graph_data.index), graph_data['PC-B'], label='PC-B')
plt.plot(list(graph_data.index), graph_data['PC-C'], label='PC-C')
plt.plot(list(graph_data.index), graph_data['PC-D'], label='PC-D')
plt.plot(list(graph_data.index), graph_data['PC-E'], label='PC-E')
plt.legend() # 凡例表示
plt.show() # 表示
