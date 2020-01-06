import pandas as pd

# 購入明細の横結合
# 主軸データは最も粒度が細かい transaction_detail
# 付加したいデータは transaction の payment_data と customer_id
# transaction の price は一回の購買データの合計金額であり、
# transaction_detail と item_master から算出されるため二重計上になってしまうため結合しない

print('購入明細')
transaction_1 = pd.read_csv('transaction_1.csv')  # 購入明細1
transaction_2 = pd.read_csv('transaction_2.csv')  # 購入明細2
transaction = pd.concat([transaction_1, transaction_2], ignore_index=True)
print(transaction.head())

print('購入明細の詳細')
transaction_detail_1 = pd.read_csv('transaction_detail_1.csv')  # 購入明細の詳細1
transaction_detail_2 = pd.read_csv('transaction_detail_2.csv')  # 購入明細の詳細2
transaction_detail = pd.concat([transaction_detail_1, transaction_detail_2], ignore_index=True)
print(transaction_detail.head())

print('購入明細の横結合')
join_data = pd.merge(transaction_detail,
                    transaction[['transaction_id', 'payment_date', 'customer_id']],
                    on='transaction_id', how='left')
print(join_data.head())
