# 3D Point Cloud Visualisation with DBSCAN Clustering

The object of this project was to create a scan using a LiDAR sensor and use the resulting point cloud to create a 3D model of an environment, that could be segmented in different items.

In the resulting program, the user can upload a LiDAR scan of an environment of their choice into a webapplication and use different handles to find the optimal parameters for an image segmentation. The more accurate the scan captures the environment the better the segmentation will be!

In the Streamlit GUI, you can upload your LiDAR Scan in _.ply_ format via drag and drop. Set the parameters to your desired values and press "Visualize". A 3D model of your scan with a segmentation will open in a new window.  

__Extra:__  
Run the **crop_scan.py** file to open another interactive window: you can select and save a section of the point cloud using a bounding box.  

## Installation and run

Download and install:   
```
git clone https://github.com/miriam-agrawala/3D-Point-Cloud-Visualisation-with-DBSCAN-Clustering.git
cd 3D-Point-Cloud-Visualisation-with-DBSCAN-Clustering
pip install -r requirements.txt  
```

Then, run this line in the correct directory:     
```
streamlit run app.py  
```


## Background Knowledge
The different parameters that can be changed to obtain the segmentation are: Floor/Ceiling Threshold, Wall Threshold, Voxel Size, Distance Threshold, RANSAC N, Number of Iterations, Epsilon (eps) and Minimum Points. Adjusting each of these parameters has a different effect:    

| Parameter            | Description                                                                                   |
|----------------------|-----------------------------------------------------------------------------------------------|
| **Number of Neighbours** | Sets the number of neighbours to consider when calculating the mean and standard deviation for statistical outlier removal.    |
| **Standard Deviation Ratio** | Sets threshold that controls how far a point's distance from the mean can be before it is considered a statistical outlier.    |
| **Floor/Ceiling Threshold** | Sets the threshold for identifying floor and ceiling surfaces. A higher value makes it more strict, while a lower value considers more points as part of the floor or ceiling.   |
| **Wall Threshold**        | Sets the threshold for identifying wall surfaces. Increasing it makes the detection more strict, while decreasing it identifies more points as part of walls.          |
| **Voxel Size**            | Adjusts the voxel size to control the level of point cloud downsampling. A smaller voxel size retains more detail, while a larger size reduces the data for faster processing. |
| **Distance Threshold**     | Plane segmentation. It determines when points are considered part of the same plane. A smaller value makes the segmentation more sensitive to variations, while a larger value groups points more aggressively. |
| **RANSAC N**              | Total number of iterations for various processes in the RANSAC algorithm. Adjusting this can affect the quality of clustering and segmentation results.         |
| **Epsilon (eps)**         | Defines the radius of the neighborhood in DBSCAN clustering. A smaller epsilon creates tighter clusters, while a larger one results in more spread-out clusters. If chosen too small, a higher number of clusters will be created (and more data points will be taken as noise). Whereas, if chosen too big, small clusters will merge into one big cluster and details will be lost. |
| **Minimum Points**        | Minimum number of points required to form a cluster in DBSCAN. Increasing this value can lead to larger and denser clusters, while decreasing it results in more clusters with fewer points. The value should be at least one greater than the number of dimensions in the dataset. |


For preprocessing an algorithm called **RANSAC** (RANdom SAmple Consensus) is used. It is an iterative algorithm used for robust model fitting in the presence of outliers. It is widely used in computer vision, image processing and computer graphics. The main objective of RANSAC is to estimate parameters of a mathematical model from a set of data points, where some of the data points may be outliers. During several iterations the best parameters for the model are found. In the context of computer vision, it can be used to fit geometric shapes to noisy data.  

The technique used for clustering is the **DBSCAN** (Density-Based Spatial Clustering of Applications with Noise). Clustering itself is an unsupervised learning technique to group data points based on specific characteristics. DBSCAN groups densely grouped data points into a single cluster and can identify clusters in large spatial datasets by looking at the local density of the data points, while also being robust to outliers. It requires two parameters: Epsilon and minPoints (Minimum Points). Epsilon is the radius of the circle to be created around each data point to check the density and minPoints is the minimum number of data points required inside that circle for that data point to be classified as a Core point. In higher dimenensions, the circle becomes a hypersphere.
