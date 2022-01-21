import cv2
import numpy as np
from sklearn.cluster import KMeans


class DominantColors:

    CLUSTERS = None
    IMAGE = None
    COLORS = None
    LABELS = None

    def __init__(self, image, clusters=3):
        self.CLUSTERS = clusters
        self.IMAGE = image

    def dominantColors(self):

        #read image
        img = cv2.imread(self.IMAGE)

        #convert to rgb from bgr
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        #reshaping to a list of pixels
        img = img.reshape((img.shape[0] * img.shape[1], 3))

        #save image after operations
        self.IMAGE = img

        #using k-means to cluster pixels
        kmeans = KMeans(n_clusters=self.CLUSTERS)
        kmeans.fit(img)

        #the cluster centers are our dominant colors.
        self.COLORS = kmeans.cluster_centers_

        #save labels
        self.LABELS = kmeans.labels_

        #returning after converting to integer from float
        return self.COLORS.astype(int)

def supprBackgroundColorResult(colors):
    idx = 0
    idx_sum = 0
    for i in range(0, len(colors)):
        sum = colors[i][0] + colors[i][1] + colors[i][2]
        if idx_sum < sum:
            idx = i
            idx_sum = sum

    return np.delete(colors, idx, 0)

img = 'choco.png'
clusters = 2  # au minimum vu qu'il y a le blanc du fond
dc = DominantColors(img, clusters)
colors = dc.dominantColors()

colors = supprBackgroundColorResult(colors)
print(colors)
