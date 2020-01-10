import networkx as nx
import matplotlib.pyplot as plt

# グラフオブジェクトの作成
G = nx.Graph()

# 頂点の設定
G.add_node('nodeA')
G.add_node('nodeB')
G.add_node('nodeC')

# 辺の設定
G.add_edge('nodeA', 'nodeB')
G.add_edge('nodeA', 'nodeC')
G.add_edge('nodeB', 'nodeC')

# 座標の設定
position = {}
position['nodeA'] = (0, 0)
position['nodeB'] = (1, 1)
position['nodeC'] = (0, 1)

# 描画
nx.draw(G, position)

# 表示
plt.show()