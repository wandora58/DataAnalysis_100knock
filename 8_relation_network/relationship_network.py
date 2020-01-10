import pandas as pd

df_links = pd.read_csv("links.csv")
df_links


import networkx as nx
import matplotlib.pyplot as plt

# グラフオブジェクトの作成
G = nx.Graph()

# 頂点の設定
NUM = len(df_links.index)
for i in range(1,NUM+1):
    node_no = df_links.columns[i].strip("Node")
    #print(node_no)
    G.add_node(str(node_no))

# 辺の設定
for i in range(NUM):
    for j in range(NUM):
        #print(i,j)
        if df_links.iloc[i][j]==1:
            G.add_edge(str(i),str(j))

# 描画
nx.draw_networkx(G,node_color="k", edge_color="k", font_color="w")
plt.show()

