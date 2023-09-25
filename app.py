"""This Streamlit application allows users to upload LiDAR .ply files and apply DBSCAN clustering
   with various parameters to visualize clusters in a 3D point cloud."""

# Import the Streamlit library and the backend module
import streamlit as st # Streamlit library for creating web applications
import backend as b # custom backend module (for point cloud processing)


# Streamlit interface
st.title('3D Point Cloud Visualization with DBSCAN Clustering') # Set the title for the web application

uploaded_file = st.file_uploader("Upload LiDAR PLY file:", type=["ply"]) # Create a file uploader for PLY files

st.subheader('Preprocessing')

# Define sliders to allow users to adjust various parameters for preprocessing:

# The user can adjust the voxel size to control the level of point cloud downsampling.
st.write('A smaller voxel size retains more detail, while a larger size reduces the data for faster processing.')
voxel_size = st.slider("Voxel Size", 0.01, 0.1, 0.04)

# The user can adjust the number of neighbours and standard deviation ratio to control the level of statistical outlier removal.
st.write("A smaller number of neighbours and standard deviation ratio makes a more aggressive data reduction identifying more points as outliers, while a larger number of neighbours and standard deviation ratio makes a more conservative data reduction.")
num_neighbours = st.slider("Number of neighbours",1,30,20)
std_ratio = st.slider("Standard deviation ratio",1,5,2)


if st.button('Visualize Preprocessing Results') and uploaded_file:
   # Save the uploaded file to a temporary directory and get the file path
    lidar_path = b.save_uploaded_file(uploaded_file)
    # Preprocesses the uploaded point cloud
    down_lidar = b.preprocess(lidar_path, voxel_size, num_neighbours, std_ratio)
    # Display the 3D scatter plot in Streamlit using plotly_chart
    st.plotly_chart((b.plot_preprocessed(down_lidar)),use_container_width=True)

st.subheader('Clustering')

# Define sliders to allow users to adjust various parameters for preprocessing:

# The user can adjust the following slider to set the threshold for identifying floor and ceiling surfaces.
st.write("A higher threshold makes the floor detection plane closer to the vertical boundary, while a lower threshold makes the floor detection plane further from the vertical boundary.")
floor_threshold = st.slider("Floor/Ceiling Threshold", 0.0, 1.0, 0.9)

# The user can adjust the following slider to set the threshold for identifying wall surfaces.
st.write("A higher threshold makes the wall detection plane closer to the horizontal boundary, while a lower threshold makes the wall detection plane further from the horizontal boundary.")
wall_threshold = st.slider("Wall Threshold", 0.0, 1.0, 0.9) 

# The user can set the distance threshold for plane segmentation. It determines when points are considered part of the same plane.
st.write('A smaller value makes the segmentation more sensitive to variations, while a larger value groups points more aggressively.')
distance_threshold = st.slider("Distance Threshold", 0.005, 0.1, 0.008)

# The user can modify this slider to adjust the number of points RANSAC takes at random when segmenting planes.
st.write('A higher value can improve plane fitting accuracy at the cost of computation time.')
ransac_n = st.slider("RANSAC Number of Points (n)", 3, 10, 5)

# The user can control the total number of iterations for various processes in the RANSAC algorithm.
st.write('Adjusting this can affect the quality of clustering and segmentation results.')
num_iterations = st.slider("Number of Iterations", 100, 2000, 300)

# Epsilon (eps) defines the neighborhood size in DBSCAN clustering.
st.write('A smaller epsilon creates tighter clusters, while a larger one results in more spread-out clusters.')
eps = st.slider("Epsilon (eps)", 0.01, 0.1, 0.05)

# The user can set the minimum number of points required to form a cluster in DBSCAN.
st.write('Increasing this value can lead to larger and denser clusters, while decreasing it results in more clusters with fewer points.')
min_points = st.slider("Minimum Points", 1, 20, 10) 

# Check if the "Visualize" button is clicked and a file is uploaded
if st.button('Visualize Clustering Results') and uploaded_file:
   # Save the uploaded file to a temporary directory and get the file path
    lidar_path = b.save_uploaded_file(uploaded_file)
    # Preprocesses the uploaded point cloud
    down_lidar = b.preprocess(lidar_path, voxel_size, num_neighbours, std_ratio)
    # Preprocess the point cloud and perform DBSCAN clustering
    points, labels = b.cluster_point_cloud(down_lidar, floor_threshold, wall_threshold, distance_threshold, ransac_n, num_iterations,eps,min_points)
    # Display the number of clusters found
    st.write(f"{len(set(labels))} clusters found.")
    # Plot the 3D point cloud with cluster labels using Plotly
    st.plotly_chart(b.plot_3d_point_cloud(points, labels))