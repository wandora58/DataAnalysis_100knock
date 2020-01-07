import pandas as pd

print('売り上げ履歴')
uriage_data = pd.read_csv('uriage.csv')
print(uriage_data.head())

print('顧客台帳')
kokyaku_data = pd.read_excel('kokyaku_daicho.xlsx')
print(kokyaku_data.head())
