import pandas as pd

# 顧客名の補正

kokyaku_data = pd.read_excel('kokyaku_daicho.xlsx')
print(kokyaku_data.head())

kokyaku_data['顧客名'] = kokyaku_data['顧客名'].str.replace('  ','')
kokyaku_data['顧客名'] = kokyaku_data['顧客名'].str.replace(' ','')
print(kokyaku_data['顧客名'])
