import open3d as o3d

# Adjust your path accordingly, please remain the r"" format to prevent unicode escape
FILEPATH = r"room_scan.ply" 

# Load the .ply file
point_cloud = o3d.io.read_point_cloud(FILEPATH)

def pick_points(pcd):
    """
    Crop and save a region of interest from a point cloud.

    This function allows you to select and save a region of interest (ROI) from a given point cloud.

    Usage:
    - Press 'F' to enable freeview mode.
    - Press 'K' to lock the camera for editing (with bounding box).
    - Press 'C' to keep the cropped item.
    - Use 'X', 'Y', or 'Z' to view the ROI from the corresponding axis.
    - Press 'S' to save the cropped item.
    - Press 'Q' to close the window

    Parameters:
    pcd (PointCloud): The input point cloud from which to extract the ROI.

    Returns:
    Cropped point cloud: A new point cloud containing only the selected region.
    """
    print("""
          1) Press 'K' to lock the camera for editing (with bounding box).
          2) Press 'C' to keep the cropped item.
          3) Press 'S' to save the cropped item.
          4) After the points is saved, press 'Q' to close the window
          """)
    vis = o3d.visualization.VisualizerWithEditing() # Initialize visualization
    vis.create_window()
    vis.add_geometry(pcd)
    vis.run()  # user picks points
    vis.destroy_window()

if '__name__' == '__main__':
    pick_points(point_cloud)