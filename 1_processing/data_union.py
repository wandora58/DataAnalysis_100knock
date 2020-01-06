import pandas as pd

# データの縦結合

print('購入明細1')
transaction_1 = pd.read_csv('transaction_1.csv')  # 購入明細の詳細
print(len(transaction_1))

print('購入明細2')
transaction_2 = pd.read_csv('transaction_2.csv')  # 購入明細の詳細
print(len(transaction_2))

print('購入明細の縦結合')
transaction = pd.concat([transaction_1, transaction_2], ignore_index=True)
print(len(transaction))
# ignore_index=True は縦連結の際、ラベルを０から振り直してくれる
