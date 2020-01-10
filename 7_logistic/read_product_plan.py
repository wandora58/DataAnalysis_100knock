import pandas as pd

df_material = pd.read_csv('product_plan_material.csv', index_col="製品")
print(df_material)
df_profit = pd.read_csv('product_plan_profit.csv', index_col="製品")
print(df_profit)
df_stock = pd.read_csv('product_plan_stock.csv', index_col="項目")
print(df_stock)
df_plan = pd.read_csv('product_plan.csv', index_col="製品")
print(df_plan)