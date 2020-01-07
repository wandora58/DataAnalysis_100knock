import pandas as pd

# 日付の補正

# データの読み込み
kokyaku_data = pd.read_excel('kokyaku_daicho.xlsx')

# 顧客名の補正
kokyaku_data['顧客名'] = kokyaku_data['顧客名'].str.replace('  ','')
kokyaku_data['顧客名'] = kokyaku_data['顧客名'].str.replace(' ','')

# 数値となっている場所の特定
flg_is_serial = kokyaku_data['登録日'].astype('str').str.isdigit()

# 数値から日付に変換
fromSerial = pd.to_timedelta(kokyaku_data.loc[flg_is_serial, '登録日'].astype('float'), unit='D') + pd.to_datetime('1900/01/01')

# 元のデータにも / が入っているため書式変換
fromString = pd.to_datetime(kokyaku_data.loc[~flg_is_serial, '登録日'])

# データの結合
kokyaku_data['登録日'] = pd.concat([fromSerial, fromString])

# 登録年月の算出
kokyaku_data['登録月'] = kokyaku_data['登録日'].dt.strftime('%Y%m')
rslt = kokyaku_data.groupby('登録月').count()['顧客名']
print(rslt)
