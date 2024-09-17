from OpenGL.GL import *
from OpenGL.GLU import *

class Camera:
    """
    Represents the camera in 3D space, following the player.
    
    Attributes:
        distance (float): Distance from the player.
        height (float): Height above the player.
        rot_x (float): Vertical rotation (pitch).
    """

    def __init__(self, distance=5, height=2):
        self.distance = distance
        self.height = height
        self.rot_x = 15  # Initial downward tilt (changed from 30 to 15)

    def rotate(self, dx, dy):
        """
        Rotate the camera based on mouse movement or key presses.
        
        Args:
            dx (float): Change in horizontal rotation.
            dy (float): Change in vertical rotation.
        """
        rot_speed = 0.2
        self.rot_x += dy * rot_speed
        self.rot_x = max(-90, min(90, self.rot_x))  # Clamp vertical rotation