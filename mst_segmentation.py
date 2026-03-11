import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color
import time
import os


# -------------------------------------------------
# Create results folder
# -------------------------------------------------

RESULTS_DIR = "results"

if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)


# -------------------------------------------------
# Task 1 : Graph Construction
# -------------------------------------------------

def load_image(path):

    img = io.imread(path)

    # Handle RGBA images (4 channels)
    if len(img.shape) == 3 and img.shape[2] == 4:
        img = img[:, :, :3]   # remove alpha channel

    # Convert RGB → grayscale
    if len(img.shape) == 3:
        img = color.rgb2gray(img)

    img = (img * 255).astype(np.uint8)

    return img


def build_graph(image):

    h, w = image.shape

    edges = []

    for i in range(h):
        for j in range(w):

            node = i*w + j

            # vertical edge
            if i+1 < h:

                weight = abs(int(image[i,j]) - int(image[i+1,j]))

                edges.append((weight, node, (i+1)*w + j))

            # horizontal edge
            if j+1 < w:

                weight = abs(int(image[i,j]) - int(image[i,j+1]))

                edges.append((weight, node, i*w + (j+1)))

    return edges


# -------------------------------------------------
# Union Find Structure
# -------------------------------------------------

class UnionFind:

    def __init__(self, n):

        self.parent = list(range(n))
        self.size = [1]*n
        self.intensity = [0]*n

    def find(self, x):

        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])

        return self.parent[x]

    def union(self, x, y, weight, k):

        rx = self.find(x)
        ry = self.find(y)

        if rx == ry:
            return False

        threshold_x = self.intensity[rx] + k/self.size[rx]
        threshold_y = self.intensity[ry] + k/self.size[ry]

        if weight <= min(threshold_x, threshold_y):

            if self.size[rx] < self.size[ry]:
                rx, ry = ry, rx

            self.parent[ry] = rx

            self.size[rx] += self.size[ry]

            self.intensity[rx] = max(self.intensity[rx], weight)

            return True

        return False


# -------------------------------------------------
# Task 2 : MST Segmentation
# -------------------------------------------------

def mst_segmentation(image, k=300):

    h, w = image.shape

    n = h*w

    edges = build_graph(image)

    edges.sort()

    uf = UnionFind(n)

    for weight, u, v in edges:

        uf.union(u, v, weight, k)

    labels = np.zeros(n)

    for i in range(n):

        labels[i] = uf.find(i)

    labels = labels.reshape(h, w)

    return labels


# -------------------------------------------------
# Task 3 : Segment-based Denoising
# -------------------------------------------------

def denoise(image, labels):

    output = image.copy()

    segments = {}

    for i in range(labels.shape[0]):
        for j in range(labels.shape[1]):

            l = labels[i,j]

            if l not in segments:

                segments[l] = []

            segments[l].append(image[i,j])

    means = {k:np.mean(v) for k,v in segments.items()}

    for i in range(labels.shape[0]):
        for j in range(labels.shape[1]):

            output[i,j] = means[labels[i,j]]

    return output


# -------------------------------------------------
# Metrics
# -------------------------------------------------

def mse(original, denoised):

    return np.mean((original - denoised)**2)


def psnr(original, denoised):

    m = mse(original, denoised)

    if m == 0:
        return 100

    return 20*np.log10(255/np.sqrt(m))


# -------------------------------------------------
# Task 4 : Visualization
# -------------------------------------------------

def visualize(original, labels, denoised, name):

    plt.figure(figsize=(12,4))

    plt.subplot(1,3,1)
    plt.title("Original Image")
    plt.imshow(original, cmap='gray')
    plt.axis("off")

    plt.subplot(1,3,2)
    plt.title("Segmentation")
    plt.imshow(labels, cmap='nipy_spectral')
    plt.axis("off")

    plt.subplot(1,3,3)
    plt.title("Denoised Image")
    plt.imshow(denoised, cmap='gray')
    plt.axis("off")

    save_path = os.path.join(RESULTS_DIR, name + "_visualization.png")

    plt.savefig(save_path)

    plt.close()

    print("Saved:", save_path)


# -------------------------------------------------
# Segment Histogram
# -------------------------------------------------

def histogram(labels, name):

    plt.figure()

    plt.hist(labels.flatten(), bins=50)

    plt.title("Segment Distribution Histogram")

    plt.xlabel("Segment ID")

    plt.ylabel("Frequency")

    save_path = os.path.join(RESULTS_DIR, name + "_histogram.png")

    plt.savefig(save_path)

    plt.close()

    print("Saved:", save_path)


# -------------------------------------------------
# Run Experiment
# -------------------------------------------------

def run(image_path):

    img = load_image(image_path)

    start = time.time()

    labels = mst_segmentation(img)

    denoised = denoise(img, labels)

    end = time.time()

    segments = len(np.unique(labels))

    name = image_path.split(".")[0]

    print("\nResults for:", image_path)

    print("Segments:", segments)

    print("Execution Time:", round(end-start,3))

    print("MSE:", mse(img, denoised))

    print("PSNR:", psnr(img, denoised))

    visualize(img, labels, denoised, name)

    histogram(labels, name)


# -------------------------------------------------
# Main
# -------------------------------------------------

def main():

    images = [
        "brain_mri.png",
        "chest_xray.png",
        "ct_scan.png"
    ]

    for img in images:

        run(img)


if __name__ == "__main__":
    main()