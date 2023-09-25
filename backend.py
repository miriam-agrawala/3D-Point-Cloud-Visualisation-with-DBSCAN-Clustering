"""This file contains functions for preprocessing and clustering point clouds,
   as well as for visualizing the results using Plotly."""

# Import necessary libraries for point cloud processing and visualization
import plotly.graph_objs as go # Plotly library for 3D visualization
import plotly.express as px
import numpy as np # NumPy library for numerical operations
import open3d as o3d # Open3D library for 3D point cloud processing
import tempfile # Tempfile module for temporary file handling
import os # OS module for operating system-related functions

"""Define functions for segmenting and visualizing point clouds"""

def is_floor_or_ceiling(normal, threshold=0.001):
    """Check if a plane is a floor or ceiling based on its normal vector."""
    return abs(normal[1]) > threshold # Check if the y-component of the normal vector is greater than a threshold

def is_wall(normal, threshold=0.001):
    """Check if a plane is a wall based on its normal vector."""
    return abs(normal[0]) > threshold or abs(normal[2]) > threshold # Check if the x or z-components of the normal vector are greater than a threshold

def save_uploaded_file(uploaded_file):
    """Save an uploaded file to a temporary directory and return the file path."""
    # Create a temporary directory to store the file
    temp_dir = tempfile.mkdtemp()
    # Generate the file path within the temporary directory
    file_path = os.path.join(temp_dir, uploaded_file.name)
    # Write the uploaded file's content to the file path
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    return file_path

def preprocess(lidar_path, voxel_size, num_neighbours, std_ratio):
    """Preprocess a point cloud."""
    # Read the point cloud from the specified file path
    lidar = o3d.io.read_point_cloud(lidar_path)
    # Filter out points with NaN values and select valid indices
    valid_indices = np.where(~np.isnan(np.asarray(lidar.points).any(axis=1)))[0]
    lidar = lidar.select_by_index(valid_indices)
    # Remove statistical outliers from the point cloud
    lidar, _ = lidar.remove_statistical_outlier(num_neighbours, std_ratio)
    # Downsample the point cloud using voxel downsampling
    down_lidar = lidar.voxel_down_sample(voxel_size=voxel_size)
    return down_lidar

def cluster_point_cloud(down_lidar, floor_threshold, wall_threshold, distance_threshold, ransac_n, num_iterations,eps,min_points):
    """Cluster a point cloud using DBSCAN."""
    # Iteratively segment planes from the point cloud
    for _ in range(5):
        # Check if the remaining point cloud has less than 3 points, and if so, exit the loop
        if len(down_lidar.points) < 3:
            break
        # Segment a plane using RANSAC and remove it from the point cloud
        plane_model, inliers = down_lidar.segment_plane(distance_threshold=distance_threshold, ransac_n=ransac_n, num_iterations=num_iterations)
        # Check if the segmented plane is a wall or floor/ceiling based on its normal vector
        if is_wall(plane_model[:3], threshold=wall_threshold) or is_floor_or_ceiling(plane_model[:3], threshold=floor_threshold):
            # Select and keep points that are not part of the segmented plane
            down_lidar = down_lidar.select_by_index(inliers, invert=True)
    
    # Cluster remaining points using DBSCAN
    labels = np.array(down_lidar.cluster_dbscan(eps, min_points, print_progress=True))
    return np.asarray(down_lidar.points), labels

def plot_3d_point_cloud(cloud, labels):
    """Plot a 3D point cloud with cluster labels using Plotly."""
    # Extract the x, y, and z coordinates of the points
    x, y, z = cloud.T
    # Create a 3D scatter plot with specified marker properties
    scatter = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(size=3, color=labels, colorscale='Viridis'),
    )
    # Define the layout of the 3D plot
    layout = go.Layout(
        scene=dict(
            xaxis=dict(nticks=10, range=[cloud[:, 0].min(), cloud[:, 0].max()]),
            yaxis=dict(nticks=10, range=[cloud[:, 1].min(), cloud[:, 1].max()]),
            zaxis=dict(nticks=10, range=[cloud[:, 2].min(), cloud[:, 2].max()]),
        ),
        title="DBScan Clustered Point Cloud"
    )
    # Create a Plotly figure with the scatter plot and layout
    return go.Figure(data=[scatter], layout=layout)

def plot_preprocessed(downsampled_lidar):
    """Plots filtered point clouds using Plotly."""
    # Check if the point cloud exists
    if downsampled_lidar is not None:
        # Convert Open3D point cloud to a NumPy array
        point_cloud_np = np.asarray(downsampled_lidar.points)

        # Create a 3D scatter plot using Plotly Express
        fig = px.scatter_3d(
            x=point_cloud_np[:, 0],  # X coordinates
            y=point_cloud_np[:, 1],  # Y coordinates
            z=point_cloud_np[:, 2],  # Z coordinates
            opacity=0.6,
            title="Voxel Downsampled and Statistical Outliers Removed Point Cloud",
        )

        # Set axis labels
        fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))
    return fig


