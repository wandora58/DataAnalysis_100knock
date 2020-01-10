import pandas as pd

# 生産工場データの読み込み
factories = pd.read_csv("tbl_factory.csv", index_col=0)

# 倉庫データの読み込み
warehouses = pd.read_csv("tbl_warehouse.csv", index_col=0)

# 倉庫と工場の輸送コストデータの読み込み
cost = pd.read_csv("rel_cost.csv", index_col=0)

# 工場への部品輸送実績
trans = pd.read_csv("tbl_transaction.csv", index_col=0)

# 輸送実績にコストデータを結合
join_data = pd.merge(trans, cost, left_on=["ToFC","FromWH"], right_on=["FCID","WHID"], how="left")

# 工場データを付与
join_data = pd.merge(join_data, factories, left_on="ToFC", right_on="FCID", how="left")

# 倉庫データを付与
join_data = pd.merge(join_data, warehouses, left_on="FromWH", right_on="WHID", how="left")

# カラムの並び替え
join_data = join_data[["TransactionDate","Quantity","Cost","ToFC","FCName","FCDemand","FromWH","WHName","WHSupply","WHRegion"]]

# 関東データを抽出
kanto = join_data.loc[join_data["WHRegion"]=="関東"]
print(kanto.head())

# 東北データを抽出
tohoku = join_data.loc[join_data["WHRegion"]=="東北"]
print(tohoku.head())

# 支社のコスト合計を算出
print("関東支社の総コスト: " + str(kanto["Cost"].sum()) + "万円")
print("東北支社の総コスト: " + str(tohoku["Cost"].sum()) + "万円")

# 支社の総輸送個数
print("関東支社の総部品輸送個数: " + str(kanto["Quantity"].sum()) + "個")
print("東北支社の総部品輸送個数: " + str(tohoku["Quantity"].sum()) + "個")

# 部品一つ当たりの輸送コスト
tmp = (kanto["Cost"].sum() / kanto["Quantity"].sum()) * 10000
print("関東支社の部品１つ当たりの輸送コスト: " + str(int(tmp)) + "円")
tmp = (tohoku["Cost"].sum() / tohoku["Quantity"].sum()) * 10000
print("東北支社の部品１つ当たりの輸送コスト: " + str(int(tmp)) + "円")

# 支社の平均輸送コスト
cost_chk = pd.merge(cost, factories, on="FCID", how="left")
print("関東支社の平均輸送コスト：" + str(cost_chk["Cost"].loc[cost_chk["FCRegion"]=="関東"].mean()) + "万円")
print("東北支社の平均輸送コスト：" + str(cost_chk["Cost"].loc[cost_chk["FCRegion"]=="東北"].mean()) + "万円")
