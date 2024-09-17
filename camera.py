import math
from OpenGL.GL import *
from OpenGL.GLU import *

class Camera:
    """
    Represents the camera in 3D space, following the player.
    
    Attributes:
        distance (float): Current distance from the player.
        height (float): Height above the player.
        rot_x (float): Vertical rotation (pitch).
        rot_y (float): Horizontal rotation (yaw).
        fov (float): Field of view in degrees.
        min_fov (float): Minimum field of view.
        max_fov (float): Maximum field of view.
        top_down (bool): Whether the camera is in top-down view mode.
        top_down_height (float): Height of the camera in top-down view.

    Coordinate system:
    - Positive X: right
    - Positive Y: up
    - Positive Z: forward (into the screen/field of view)
    """

    def __init__(self, distance=5, height=2):
        self.distance = distance
        self.height = height
        self.rot_x = 15  # Initial downward tilt
        self.rot_y = 0   # Initial horizontal rotation (facing positive z-axis)
        self.fov = 45.0
        self.min_fov = 10.0
        self.max_fov = 120.0
        self.top_down = False
        self.top_down_height = 100  # Height for top-down view

    def rotate(self, dx, dy):
        """
        Rotate the camera based on mouse movement or key presses.
        Only applies in normal view mode.
        """
        if not self.top_down:
            rot_speed = 0.2
            self.rot_x += dy * rot_speed
            self.rot_y += dx * rot_speed
            self.rot_x = max(-90, min(90, self.rot_x))  # Clamp vertical rotation
            self.rot_y %= 360  # Keep horizontal rotation between 0 and 359 degrees

    def zoom(self, amount):
        """
        Adjust the camera's zoom level by changing the field of view.
        """
        self.fov += amount
        self.fov = max(self.min_fov, min(self.max_fov, self.fov))
        self.update_projection()

    def update_projection(self):
        """
        Update the projection matrix based on the current field of view.
        """
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, 800/600, 0.1, 2000.0)  # Assuming 800x600 window size
        glMatrixMode(GL_MODELVIEW)

    def reset(self):
        """
        Reset the camera to its initial state and align with positive z-axis.
        """
        self.distance = 5
        self.height = 2
        self.rot_x = 15  # Slight downward tilt
        self.rot_y = 0   # Facing positive z-axis (forward)
        self.fov = 45.0
        self.top_down = False
        self.update_projection()

    def toggle_top_down(self):
        """
        Toggle between normal view and top-down view.
        """
        self.top_down = not self.top_down
        if self.top_down:
            self.rot_x = -90  # Look straight down
            self.rot_y = 0
        else:
            self.reset()  # Return to normal view

    def get_position(self, player_pos):
        """
        Calculate the camera's position based on player position and camera attributes.

        Args:
            player_pos (Vector3): The player's position.

        Returns:
            tuple: The camera's position (x, y, z).
        """
        if self.top_down:
            return (player_pos[0], player_pos[1] + self.top_down_height, player_pos[2])
        else:
            angle_y = math.radians(self.rot_y)
            camera_x = player_pos[0] - self.distance * math.sin(angle_y)
            camera_y = player_pos[1] + self.height
            camera_z = player_pos[2] - self.distance * math.cos(angle_y)
            return (camera_x, camera_y, camera_z)