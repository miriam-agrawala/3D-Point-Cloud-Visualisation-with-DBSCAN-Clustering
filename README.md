# LiDAR

The object of this project was to create a scan using a LiDAR sensor and use the resulting point cloud to create a 3D model of an environment, that could be segmented in different items.

In the resulting program, the user can upload a LiDAR scan of an environment of their choice into a webapplication and use different handles to find the optimal parameters for an image segmentation. The more accurate the scan captures the environment the better the segmentation will be!


### Background Knowledge
The different parameters that can be changed to obtain the segmentation are: Floor/Ceiling Threshold, Wall Threshold, Voxel Size, Distance Threshold, Ransac N, Number of Iterations, Epsilon (eps) and Minimum Points. Adjusting each of these parameters has a different effect:
Floor/Ceiling Threshold: Sets the threshold for identifying floor and ceiling surfaces. A higher value makes it more strict, while a lower value considers more points as part of the floor or ceiling.  
Wall Treshold: Sets the threshold for identifying wall surfaces. Increasing it makes the detection more strict, while decreasing it identifies more points as part of walls.
Voxel Size: Adjusts the voxel size to control the level of point cloud downsampling. A smaller voxel size retains more detail, while a larger size reduces the data for faster processing.
Distance Treshold: Plane segmentation. It determines when points are considered part of the same plane. A smaller value makes the segmentation more sensitive to variations, while a larger value groups points more aggressively.
RANSAC N: Total number of iterations for various processes in the algorithm. Adjusting this can affect the quality of clustering and segmentation results.
Epsilon (eps): Defines the neighborhood size in DBSCAN clustering. A smaller epsilon creates tighter clusters, while a larger one results in more spread-out clusters.
Minimum points: Minimum number of points required to form a cluster in DBSCAN. Increasing this value can lead to larger and denser clusters, while decreasing it results in more clusters with fewer points.
