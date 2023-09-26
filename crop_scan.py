"""This script provides an interactive tool for cropping and saving a region of interest (ROI)
# from a 3D point cloud loaded from a .ply file using Open3D. Users can interactively select
# and save a portion of the point cloud within a bounding box."""

# Import the Open3D library for 3D point cloud processing
import open3d as o3d 

# Adjust your path to the point cloud file you want to use accordingly
# please use the r"" format to prevent unicode escape
FILEPATH = r"room_scan.ply" 

# Load the point cloud from the specified .ply file
point_cloud = o3d.io.read_point_cloud(FILEPATH)

def pick_points(pcd):
    
    """
    Crop and save a region of interest from a point cloud interactively.

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
    # Initialize the Open3D visualization
    vis = o3d.visualization.VisualizerWithEditing() 
    vis.create_window()
    # Add the point cloud to the visualization
    vis.add_geometry(pcd)
    # Run the interactive cropping tool
    # user picks points
    vis.run()  
    # Close the visualization window
    vis.destroy_window()

if __name__ == '__main__':
    # Call the pick_points function to interactively crop the point cloud
    pick_points(point_cloud)