# 3D Point Cloud Visualisation with DBSCAN Clustering

The object of this project was to create a scan using a LiDAR sensor and use the resulting point cloud to create a 3D model of an environment, that could be segmented in different items.

In the resulting program, the user can upload a LiDAR scan of an environment of their choice into a webapplication and use different handles to find the optimal parameters for an image segmentation. The more accurate the scan captures the environment the better the segmentation will be!

To use the program, please download the "backend.py", "crop_scan.py" and "streamlit.py" and save them in the same folder. After running the streamlit.py in an IDE (like VS Code), a webapplication window will open. There, you can upload your LiDAR Scan in .ply format via drag and drop. Set the handles to your desired values and press "Visualize". A 3D model of your scan with a segmentation will open in a new window.  

When running the "crop_scan.py" another interactive window will open: you can select and save a portion of the point cloud using a bounding box.  


### Background Knowledge
The different parameters that can be changed to obtain the segmentation are: Floor/Ceiling Threshold, Wall Threshold, Voxel Size, Distance Threshold, Ransac N, Number of Iterations, Epsilon (eps) and Minimum Points. Adjusting each of these parameters has a different effect:    

**Floor/Ceiling Threshold:** Sets the threshold for identifying floor and ceiling surfaces. A higher value makes it more strict, while a lower value considers more points as part of the floor or ceiling.  
**Wall Treshold:** Sets the threshold for identifying wall surfaces. Increasing it makes the detection more strict, while decreasing it identifies more points as part of walls.  
**Voxel Size:** Adjusts the voxel size to control the level of point cloud downsampling. A smaller voxel size retains more detail, while a larger size reduces the data for faster processing.  
**Distance Treshold:** Plane segmentation. It determines when points are considered part of the same plane. A smaller value makes the segmentation more sensitive to variations, while a larger value groups points more aggressively.  
**RANSAC N:** Total number of iterations for various processes in the algorithm. Adjusting this can affect the quality of clustering and segmentation results.  
**Epsilon (eps):** Defines the radius of the neighborhood in DBSCAN clustering. A smaller epsilon creates tighter clusters, while a larger one results in more spread-out clusters. If chosen too small, a higher number of clusters will be created (and more data points will be taken as noise). Whereas, if chosen too big, small clusters will merge into one big cluster and details will be lost.  
**Minimum points:** Minimum number of points required to form a cluster in DBSCAN. Increasing this value can lead to larger and denser clusters, while decreasing it results in more clusters with fewer points. The value should be at least one greater than the number of dimensions in the dataset.

For preprocessing an algorithm called **RANSAC** (RANdom SAmple Consensus) is used. It is an iterative algorithm used for robust model fitting in the presence of outliers. It is widely used in computer vision, image processing and computer graphics. The main objective of RANSAC is to estimate parameters of a mathematical model from a set of data points, where some of the data points may be outliers. In the context of computer vision, it can be used to fit geometric shapes to noisy data.  

The technique used for clustering is the **DBSCAN** (Density-Based Spatial Clustering of Applications with Noise). Clustering itself is an unsupervised learning technique to group data points based on specific characteristics. DBSCAN groups densely grouped data points into a single cluster and can identify clusters in large spatial datasets by looking at the local density of the data points, while also being robust to outliers. It requires two parameters: Epsilon and minPoints (Minimum Points). Epsilon is the radius of the circle to be created around each data point to check the density and minPoints is the minimum number of data points required inside that circle for that data point to be classified as a Core point. In higher dimenensions, the circle becomes a hypersphere.
