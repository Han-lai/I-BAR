#------------------PCA降維-------------------------------------------------
import pandas as pd
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from joblib import dump, load
from mpl_toolkits.mplot3d import Axes3D  # 绘制3D图形
from sklearn import metrics
import matplotlib.pyplot as plt

X = pd.read_csv(r'./cocktail/tfidf/tfidf_min0.005_pos_matrix_0824.csv', encoding='utf-8') #0809做過
X = X.drop(['Unnamed: 0'], axis=1)
#-----------------------------------
X_scaled = preprocessing.scale(X)  # scale操作之后的数据零均值，单位方差（方差为1）
print('X_scaled:' ,  X_scaled)
#-----------------------------------
pca = PCA(n_components=3)  # 把维度降至3维
X_pca = pca.fit_transform(X_scaled)
# # 生成降维后的dataframe
X_pca_frame = pd.DataFrame(X_pca, columns=['pca_1', 'pca_2', 'pca_3'])  # 原始数据由(30000, 7)降维至(30000, 3)
est = KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=10000,
       n_clusters=8, n_init=10, random_state=0, tol=0.00001, verbose=0)
est.fit(X_pca)
dump(est, r'./cocktail/model/kmeans-cocktail_0824.joblib')

# # 取出聚类后的标签
kmeans_clustering_labels = pd.DataFrame(est.labels_, columns=['cluster'])  # 0-9,一共10个标签
X_pca_frame = pd.concat([X_pca_frame, kmeans_clustering_labels], axis=1)


X.index = X_pca_frame.index  # 返回：RangeIndex(start=0, stop=30000, step=1)
# 合并原数据和三个主成分的数据
X_full = pd.concat([X, X_pca_frame], axis=1)
# X_full.to_csv(r'./cocktail/model/kmeans_matrix_0824.csv',encoding='utf-8')
# print(X_full)

# clf = load(r'./cocktail/model/kmeans-cocktail_0824.joblib')

#-----------------------------------

# 生成三维图形，每个样本点的坐标分别是三个主成分的值
# 设置每个簇对应的颜色
cluster_2_color = {0: 'peru', 1: 'burlywood', 2: 'steelblue', 3: 'lightslategray', 4: 'turquoise', 5: 'darkcyan', 6: 'silver', 7: 'lightcoral',
                   8: 'yellowgreen', 9: 'olive',10: 'brown'}#,11: 'darkcyan',12: 'darkgoldenrod'} lightslategray

# 按每个聚类分组
grouped = X_full.groupby('cluster')
result_data = pd.DataFrame()
for name, group in grouped:
    # print(group)
    desp = group[['pca_1', 'pca_2', 'pca_3']].describe()  # 返回每组的数量、均值、标准差、最小值、最大值等数据
    # print(desp)
# # #  # 每组未去除异常值的个数
    print('Group:{0}, Samples before:{1}'.format(name, group['pca_1'].count()))
#
    for att in ['pca_1', 'pca_2', 'pca_3']:
        # 去异常值：箱形图

        lower25 = desp.loc['25%', att] #Q1
        upper75 = desp.loc['75%', att] #Q3
        IQR = upper75 - lower25
        # print(IQR)
        min_value = lower25 - 1.5 * IQR
        max_value = upper75 + 1.5 * IQR
#         # 使用统计中的1.5*IQR法则，删除每个聚类中的噪音和异常点
        group = group[(group[att] > min_value) & (group[att] < max_value)]
    result_data = pd.concat([result_data, group], axis=0)
    # print(result_data)
# #      # 每组去除异常值后的个数
    print('Group:{0}, Samples after:{1}'.format(name, group['pca_1'].count()))

# # # # #--------------------------------------------------------





# # # # #--------------------------------------------------------
# # # 筛选后的数据聚类可视化
    #
    colors_filtered_data = result_data.cluster.map(cluster_2_color)
    fig = plt.figure()
    ax = plt.subplot(111, projection='3d')
    ax.scatter(result_data.pca_1.values, result_data.pca_2.values, result_data.pca_3.values, c=colors_filtered_data)
    ax.set_xlabel('Component_1')
    ax.set_ylabel('Component_2')
    ax.set_zlabel('Component_3')
    plt.show()
print('Remain sample:', result_data['pca_1'].count())







#
# #-------------------------------------pca 各主成分的矩陣圖
# import pandas as pd
# from IPython.display import display
# from sklearn.preprocessing import StandardScaler
# from numpy.testing import assert_almost_equal
# import matplotlib.pyplot as plt
# from sklearn.decomposition import PCA
# #------------------PCA降維-------------------------------------------------
#
# X = pd.read_csv(r'./cocktail/tfidf/tfidf_min0.005_pos_matrix_0824.csv', encoding='utf-8') #0809做過
# X = X.drop(['Unnamed: 0'], axis=1)
# print(X.shape)
# display(X.head(5))
# # 顯示各特徵的平均與標準差
# print("各特徵平均與標準差：")
# df_stats = X.describe().loc[['mean', 'std']]
# df_stats.style.format("{:.2f}")
#
# # 將類型以外的 11 個特徵全取出
# X = X.iloc[:, 1:]  # (n_samples, n_features)
#
# # 使用 scikit-learn 內建的 API 正規化
# scaler = StandardScaler()
# Z_sk = scaler.fit_transform(X)  # 注意維度
#
#
# # 手動正規化當然也能得到跟 scikit-learn API 相同的結果
# # 注意我們有所有英雄數據（母體）而非抽樣，自由度 = 0
# Z = (X - X.mean(axis=0)) / X.std(axis=0, ddof=0)
# assert_almost_equal(Z, Z_sk)
#
# # 更新我們的 DataFrame
# X.iloc[:, 1:] = Z
#
#
# # 展示前 5 rows
# print("正規化後前五名英雄數據：")
# display(X.head(5).style\
#         .format("{:.2f}", subset=X.columns[1:]))
#
# # 顯示各特徵的平均與標準差
# print("各特徵平均與標準差：")
# df_stats = X.describe().loc[['mean', 'std']]
# df_stats.style.format("{:.2f}")
#
#
# """
# 透過 scikit-learn 將 11 維的 LOL 英雄數據降到 2 維
# """
#
#
# # 我們只要最大的兩個主成分。scikit-learn 會自動幫我們
# # 依照 eigenvalue 的大小排序共變異數矩陣的 eigenvectors
# n_components = 3
# random_state = 9527
#
# pca = PCA(n_components=n_components,
#           random_state=random_state)
#
# # 注意我們是對正規化後的特徵 Z 做 PCA
# L = pca.fit_transform(Z)  # (n_samples, n_components)
#
# # 將投影到第一主成分的 repr. 顯示在 x 軸，第二主成分在 y 軸
# plt.scatter(L[:, 0], L[:, 1])
# plt.axis('equal')
#
# """
# 解析英雄數據的前兩大主成份所代表的意涵。
# 顏色越突出代表其絕對值越大
# """
# import numpy as np
#
# pcs = np.array(pca.components_) # (n_comp, n_features)
#
# df_pc = pd.DataFrame(pcs, columns=X.columns[:])
# df_pc.index = [f"第{c}主成分" for c in['一', '二','三']]
# df_pc.style\
#     .background_gradient(cmap='bwr_r', axis=None)\
#     .format("{:.1}")
#
#
#
# # DataFrame=>png
# plt.figure('123')            # 視窗名稱
# ax = plt.axes(frame_on=False)# 不要額外框線
# ax.xaxis.set_visible(False)  # 隱藏X軸刻度線
# ax.yaxis.set_visible(False)  # 隱藏Y軸刻度線
# pd.plotting.table(ax, df_pc, loc='center') #將mytable投射到ax上，且放置於ax的中間
# plt.savefig('table.png')     # 存檔
#
# for i in range(0, r):
#     for j in range(0, c):
#         im.putpixel((i, j), (int(x[i][j][0]),int(x[i][j][1]),int(x[i][j][2])))    #將rgb轉化為畫素
#
# im.save('flag.jpg')