import pandas as pd

import_data = pd.read_csv('dump_data.csv')
print(import_data.head())

# 月ごとの商品別購入数
byItem = import_data.pivot_table(index='purchase_month', columns='item_name', aggfunc='size', fill_value=0)
print(byItem)

# 月ごとの商品別売り上げ
byPrice = import_data.pivot_table(index='purchase_month', columns='item_name', values='item_price', aggfunc='sum', fill_value=0)
print(byPrice)

# 月ごとの顧客別購入数
byCustomer = import_data.pivot_table(index='purchase_month', columns='顧客名', aggfunc='size', fill_value=0)
print(byCustomer)
