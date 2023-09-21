"""This Streamlit application allows users to upload LiDAR .ply files and apply DBSCAN clustering
   with various parameters to visualize clusters in a 3D point cloud."""

# Import the Streamlit library and the backend module
import streamlit as st # Streamlit library for creating web applications
import backend as b # custom backend module (for point cloud processing)


# Streamlit interface
st.title('3D Point Cloud Visualization with DBSCAN Clustering') # Set the title for the web application

uploaded_file = st.file_uploader("Upload LiDAR PLY file:", type=["ply"]) # Create a file uploader for PLY files

# Define sliders to allow users to adjust various parameters:

# The user can adjust the following slider to set the threshold for identifying floor and ceiling surfaces.
# A higher value makes it more strict, while a lower value considers more points as part of the floor or ceiling.
floor_threshold = st.slider("Floor/Ceiling Threshold", 0.0, 1.0, 0.9)
# The user can adjust the following slider to set the threshold for identifying wall surfaces.
# Increasing it makes the detection more strict, while decreasing it identifies more points as part of walls.
wall_threshold = st.slider("Wall Threshold", 0.0, 1.0, 0.9) 
# The user can adjust the voxel size to control the level of point cloud downsampling.
# A smaller voxel size retains more detail, while a larger size reduces the data for faster processing.
voxel_size = st.slider("Voxel Size", 0.01, 0.1, 0.04)
# The user can set the distance threshold for plane segmentation. It determines when points are considered part of the same plane.
# A smaller value makes the segmentation more sensitive to variations, while a larger value groups points more aggressively.
distance_threshold = st.slider("Distance Threshold", 0.005, 0.1, 0.008) 
# The user can modify this slider to adjust the number of iterations RANSAC performs when segmenting planes.
# A higher value can improve plane fitting accuracy at the cost of computation time.
ransac_n = st.slider("RANSAC N", 3, 10, 5)
# The user can control the total number of iterations for various processes in the algorithm.
# Adjusting this can affect the quality of clustering and segmentation results.
num_iterations = st.slider("Number of Iterations", 100, 2000, 300) 
# Epsilon (eps) defines the neighborhood size in DBSCAN clustering.
# A smaller epsilon creates tighter clusters, while a larger one results in more spread-out clusters.
eps = st.slider("Epsilon (eps)", 0.01, 0.1, 0.05) 
# The user can set the minimum number of points required to form a cluster in DBSCAN.
# Increasing this value can lead to larger and denser clusters, while decreasing it results in more clusters with fewer points.
min_points = st.slider("Minimum Points", 1, 20, 10) 

# Check if the "Visualize" button is clicked and a file is uploaded
if st.button('Visualize') and uploaded_file:
    # Save the uploaded file to a temporary directory and get the file path
    lidar_path = b.save_uploaded_file(uploaded_file)
    # Preprocess the point cloud and perform DBSCAN clustering
    points, labels = b.preprocess_and_cluster_point_cloud(lidar_path, floor_threshold, wall_threshold, voxel_size, distance_threshold, ransac_n, num_iterations,eps,min_points)
    # Display the number of clusters found
    st.write(f"{len(set(labels))} cluster found")
    # Plot the 3D point cloud with cluster labels using Plotly
    st.plotly_chart(b.plot_3d_point_cloud(points, labels))
