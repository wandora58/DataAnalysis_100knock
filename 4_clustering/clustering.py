import pandas as pd
import numpy
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# クラスタリングを行い、顧客ごとグルーピングする

# データの読み込み
customer = pd.read_csv('dump_data.csv')
customer_clustering = customer[['mean', 'median', 'max', 'min', 'membership_period']]

# K-meansを用いたクラスタリング
sc = StandardScaler()
customer_clustering_sc = sc.fit_transform(customer_clustering)

kmeans = KMeans(n_clusters=4, random_state=0)
clusters = kmeans.fit(customer_clustering_sc)
customer_clustering['cluster'] = clusters.labels_

# クラスタリング結果を分析
customer_clustering.columns = ['月内平均値', '月内中央値', '月内最大値', '月内最小値', '会員期間', 'cluster']
print(customer_clustering.groupby('cluster').mean())

# 主成分分析
X = customer_clustering_sc
pca = PCA(n_components=2)
x_pca = pca.fit_transform(X)
pca_df = pd.DataFrame(x_pca)
pca_df['cluster'] = customer_clustering['cluster']

# グラフに壁画
# colors = ['red','blue','yellow','pink']
# for i in customer_clustering['cluster'].unique():
#     tmp = pca_df.loc[pca_df['cluster']==i]
#     plt.scatter(tmp[0], tmp[1], c=colors[i])
# plt.show()

# 継続顧客と退会顧客の集計
customer_clustering = pd.concat([customer_clustering, customer], axis=1)
print(customer_clustering.groupby(['cluster', 'is_deleted'], as_index=False).count()[['cluster', 'is_deleted', 'customer_id']])

# 定期利用しているかどうか
print(customer_clustering.groupby(['cluster', 'routing_flg'], as_index=False).count()[['cluster', 'routing_flg', 'customer_id']])


