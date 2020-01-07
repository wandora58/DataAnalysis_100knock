import pandas as pd
import matplotlib.pyplot as plt

# データの読み込み　
import_data = pd.read_csv('dump_data.csv')

# 定期利用している顧客
print(import_data.groupby('routing_flg').count()['customer_id'])

# 会員期間のヒストグラム
plt.hist(import_data['membership_period'])
plt.show()

# 短期的に退会する顧客と長期的な顧客との違いを把握
customer_end = import_data.loc[import_data['is_deleted']==0]
print(customer_end.describe())

customer_stay = import_data.loc[import_data['is_deleted']==1]
print(customer_stay.describe())
