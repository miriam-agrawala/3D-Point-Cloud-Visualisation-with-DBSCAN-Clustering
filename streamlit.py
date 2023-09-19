import streamlit as st
import backend as b


# Streamlit interface
st.title('3D Point Cloud Visualization with DBSCAN Clustering')

uploaded_file = st.file_uploader("Upload LiDAR PLY file:", type=["ply"])

floor_threshold = st.slider("Floor/Ceiling Threshold", 0.0, 1.0, 0.9)
wall_threshold = st.slider("Wall Threshold", 0.0, 1.0, 0.9)
voxel_size = st.slider("Voxel Size", 0.01, 0.1, 0.04)
distance_threshold = st.slider("Distance Threshold", 0.005, 0.1, 0.008)
ransac_n = st.slider("RANSAC N", 3, 10, 5)
num_iterations = st.slider("Number of Iterations", 100, 2000, 300)
eps = st.slider("Epsilon (eps)", 0.01, 0.1, 0.05)
min_points = st.slider("Minimum Points", 1, 20, 10)

if st.button('Visualize') and uploaded_file:
    lidar_path = b.save_uploaded_file(uploaded_file)
    points, labels = b.preprocess_and_cluster_point_cloud(lidar_path, floor_threshold, wall_threshold, voxel_size, distance_threshold, ransac_n, num_iterations,eps,min_points)
    st.write(f"{len(set(labels))} cluster found")
    st.plotly_chart(b.plot_3d_point_cloud(points, labels))
