import pandas as pd

# データの結合

#--------------------顧客台帳-----------------------
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


#--------------------売り上げ------------------------
# データ読み込み
uriage_data = pd.read_csv('uriage.csv')

# 商品名の補正
uriage_data['item_name'] = uriage_data['item_name'].str.upper()
uriage_data['item_name'] = uriage_data['item_name'].str.replace('  ','')
uriage_data['item_name'] = uriage_data['item_name'].str.replace(' ','')

# 欠損値補間 → 期間中変動が無いため、他の同じ商品の単価から補間
fig_is_null = uriage_data['item_price'].isnull()
for trg in list(uriage_data.loc[fig_is_null, 'item_name'].unique()):
    price = uriage_data.loc[(~fig_is_null) & (uriage_data['item_name']==trg), 'item_price'].max()
    uriage_data['item_price'].loc[(fig_is_null) & (uriage_data['item_name']==trg)] = price

# 月ラベルの生成
uriage_data['purchase_date'] = pd.to_datetime(uriage_data['purchase_date'])
uriage_data['purchase_month'] = uriage_data['purchase_date'].dt.strftime('%Y%m')

#-------------------データの結合-----------------------
join_data = pd.merge(uriage_data, kokyaku_data, left_on='customer_name', right_on='顧客名', how='left')
join_data = join_data.drop('customer_name', axis=1)

#-------------------データの出力-----------------------
dump_data = join_data[['purchase_date', 'purchase_month', 'item_name', 'item_price', '顧客名', 'かな', '地域', 'メールアドレス', '登録日']] # 整形
dump_data.to_csv('dump_data.csv', index=False)
