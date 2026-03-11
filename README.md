# Medical Image Segmentation using Minimum Spanning Tree (MST)

## Overview

Medical imaging plays a critical role in modern healthcare. Techniques such as MRI, CT scans, and X-ray imaging allow doctors to observe internal structures of the human body without invasive procedures. However, these images often contain complex patterns and noise, making automated analysis challenging.

This project implements a **Minimum Spanning Tree (MST) based graph segmentation algorithm** for medical images. The algorithm divides images into meaningful regions while preserving boundaries between different structures. In addition, a **segment-based denoising technique** is applied to reduce noise while maintaining important edges.

The project demonstrates how classical graph algorithms can be applied to real-world problems in **medical image processing**.

---

## Features

- Graph-based medical image segmentation
- Minimum Spanning Tree (MST) segmentation algorithm
- Efficient **Union-Find** structure for component merging
- Segment-based image denoising
- Visualization of segmentation results
- Histogram analysis of segment distributions
- Performance evaluation using **MSE** and **PSNR**

---

## Project Structure
Assignment/
│
├── mst_segmentation.py
│
├── images/
│ ├── brain_mri.png
│ ├── chest_xray.png
│ └── ct_scan.png
│
├── results/
│ ├── brain_mri_visualization.png
│ ├── brain_mri_histogram.png
│ ├── chest_xray_visualization.png
│ ├── chest_xray_histogram.png
│ ├── ct_scan_visualization.png
│ └── ct_scan_histogram.png
│
└── README.m


---

## Algorithm Workflow

The implementation consists of four main stages:

### 1. Graph Construction
- Load and preprocess the medical image
- Convert the image to grayscale
- Treat each pixel as a graph node
- Connect neighboring pixels with weighted edges
- Edge weights represent intensity differences

### 2. MST-Based Segmentation
- Sort edges based on weight
- Use **Union-Find** to manage connected components
- Merge regions using adaptive threshold conditions

### 3. Segment-Based Denoising
- Calculate mean intensity for each segment
- Replace pixel values with the segment mean
- Preserve edges between different regions

### 4. Visualization and Analysis
- Display original image
- Display segmentation result
- Display denoised image
- Generate **segment distribution histograms**

---

## Evaluation Metrics

The segmentation algorithm is evaluated using the following metrics:

- **Number of Segments**
- **Execution Time**
- **Mean Squared Error (MSE)**
- **Peak Signal-to-Noise Ratio (PSNR)**

These metrics help analyze both segmentation quality and denoising effectiveness.

---

## Example Results

Example results obtained for the **Brain MRI image**:

| Metric | Value |
|------|------|
| Segments | 812 |
| Execution Time | 0.19 s |
| MSE | 66.84 |
| PSNR | 29.88 |

The results show that the algorithm successfully groups similar pixels while preserving important boundaries in the medical image.

---

## Technologies Used

- **Python**
- **NumPy**
- **Matplotlib**
- **SciPy**
- **scikit-image**

---

## Results

The algorithm generates the following outputs for each image:

- Segmentation visualization
- Denoised image
- Segment distribution histogram
- Quantitative performance metrics

These outputs help evaluate the effectiveness of the segmentation algorithm.

---

## Future Improvements

Possible improvements for this project include:

- Applying the algorithm to larger medical datasets
- Incorporating texture-based segmentation features
- Comparing MST segmentation with deep learning methods
- Implementing real-time segmentation systems

---

## Author

**Fahad Bin Hashim**  
S6 CS-A
Department of Computer Science and Engineering  
Saintgits College of Engineering

---

## License

This project is developed for **academic and educational purposes**.
