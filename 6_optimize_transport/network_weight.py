import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# データ読み込み
df_weight = pd.read_csv('network_weight.csv')
df_position = pd.read_csv('network_position.csv')
print(df_weight)
print(df_position)

# エッジの重みリスト化
size = 10
edge_weights = []
for i in range(len(df_weight)):
    for j in range(len(df_weight.columns)):
        edge_weights.append(df_weight.iloc[i][j]*size)

# グラフオブジェクトの作成
G = nx.Graph()

# 頂点の設定
for i in range(len(df_weight.columns)):
    G.add_node(df_weight.columns[i])

# 辺の設定
for i in range(len(df_weight.columns)):
    for j in range(len(df_weight.columns)):
        G.add_edge(df_weight.columns[i], df_weight.columns[j])

# 座標の設定
position = {}
for i in range(len(df_weight.columns)):
    node = df_weight.columns[i]
    position[node] = (df_position[node][0], df_position[node][1])

# 描画
nx.draw(G, position, with_labels=True,font_size=16, node_size = 1000, node_color='k', font_color='w', width=edge_weights)

# 表示
plt.show()


