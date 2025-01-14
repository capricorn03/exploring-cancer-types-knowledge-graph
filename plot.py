
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
import ast

from sklearn.manifold import TSNE

nodes = pd.read_csv("export.csv")
nodes['louvain'] = pd.Categorical(nodes.louvain)

# Convert the embedding generated by neo4j to a literal list and use
# tSNE to project that to two dimensions for plotting.
embedding = nodes.embedding.apply(lambda x: ast.literal_eval(x))
embedding = embedding.tolist()
embedding = pd.DataFrame(embedding)
tsne = TSNE()
X = tsne.fit_transform(embedding)
nodes = pd.concat([nodes, pd.DataFrame(X)], axis=1)

# Merge the embedding data with the cancer statistics
cancer_stats = pd.read_csv("globocan_2022.csv")
cancer_stats['label'] = cancer_stats['label'].apply(lambda x: f'"{x}"')
cancer_stats = pd.merge(
    cancer_stats,
    nodes,
    how="inner",
    on="label"
)

mosaic = np.array([
    ['tsne','tsne-stat'],
    ['mort','incid']
])

fig, axes = plt.subplot_mosaic(mosaic, layout="constrained")
axes['tsne'].scatter(
    X[:,0],
    X[:,1],
    c  = cm.tab20(Normalize()(nodes['louvain'].cat.codes))
)
axes['tsne-stat'].scatter(
    cancer_stats[0],
    cancer_stats[1],
    s = 1000*Normalize()(cancer_stats['incidence']),
    c  = cm.tab20(Normalize()(cancer_stats['louvain'].cat.codes)),
    alpha = Normalize()(cancer_stats['mortality']),
)
axes['tsne-stat'].scatter(
    cancer_stats[0],
    cancer_stats[1],
    s = 1000*Normalize()(cancer_stats['incidence']),
    facecolors  = "none",
    edgecolors = cm.tab20(Normalize()(cancer_stats['louvain'].cat.codes)),
)
for i,row in cancer_stats.iterrows():
    axes['tsne-stat'].text(
        row[0],
        row[1],
        s = row.site,
        # c = cm.tab20(Normalize()(cancer_stats['louvain'].cat.codes))
    )
axes['incid'].barh(
    width=cancer_stats['incidence'],
    y=cancer_stats['label'],
    color = cm.tab20(Normalize()(cancer_stats['louvain'].cat.codes))
)
axes['mort'].barh(
    width=cancer_stats['mortality'],
    y=cancer_stats['label'],
    color = cm.tab20(Normalize()(cancer_stats['louvain'].cat.codes))
)
plt.show()

# Explore clusters
nodes["louvain"].value_counts()
nodes[nodes.louvain == 331]["label"].values
nodes[nodes.louvain == 2168]["label"].values
nodes[nodes.louvain == 174]["label"].values
nodes[nodes.louvain == 1426]["label"].values

nodes[nodes.louvain == 1167]["label"]
nodes[nodes["label"].str.contains("pancrea")]
nodes[nodes["label"].str.contains("pancrea")].louvain.value_counts().head()

nodes[nodes["label"].str.contains("liver")].louvain.value_counts().head()

cancer_stats[cancer_stats.site=="Liver"]
cancer_stats[cancer_stats.site=="Oropharynx"]
cancer_stats[cancer_stats.site=="Nasopharynx"]
cancer_stats[cancer_stats.site=="Hypopharynx"]
cancer_stats[cancer_stats.site=="Larynx"]

nodes[nodes.louvain == 766]["label"].values
