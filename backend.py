import plotly.graph_objs as go
import numpy as np
import open3d as o3d
import tempfile
import os

def is_floor_or_ceiling(normal, threshold=0.001):
    return abs(normal[1]) > threshold

def is_wall(normal, threshold=0.001):
    return abs(normal[0]) > threshold or abs(normal[2]) > threshold

def save_uploaded_file(uploaded_file):
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    return file_path

def preprocess_and_cluster_point_cloud(lidar_path, floor_threshold, wall_threshold, voxel_size, distance_threshold, ransac_n, num_iterations, eps, min_points):
    lidar = o3d.io.read_point_cloud(lidar_path)
    valid_indices = np.where(~np.isnan(np.asarray(lidar.points).any(axis=1)))[0]
    lidar = lidar.select_by_index(valid_indices)
    lidar, _ = lidar.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
    down_lidar = lidar.voxel_down_sample(voxel_size=voxel_size)

    for _ in range(5):
        if len(down_lidar.points) < 3:
            break
        plane_model, inliers = down_lidar.segment_plane(distance_threshold=distance_threshold, ransac_n=ransac_n, num_iterations=num_iterations)
        if is_wall(plane_model[:3], threshold=wall_threshold) or is_floor_or_ceiling(plane_model[:3], threshold=floor_threshold):
            down_lidar = down_lidar.select_by_index(inliers, invert=True)

    labels = np.array(down_lidar.cluster_dbscan(eps, min_points, print_progress=True))
    return np.asarray(down_lidar.points), labels

def plot_3d_point_cloud(cloud, labels):
    x, y, z = cloud.T
    scatter = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(size=3, color=labels, colorscale='Viridis'),
    )
    layout = go.Layout(
        scene=dict(
            xaxis=dict(nticks=10, range=[cloud[:, 0].min(), cloud[:, 0].max()]),
            yaxis=dict(nticks=10, range=[cloud[:, 1].min(), cloud[:, 1].max()]),
            zaxis=dict(nticks=10, range=[cloud[:, 2].min(), cloud[:, 2].max()]),
        )
    )
    return go.Figure(data=[scatter], layout=layout)