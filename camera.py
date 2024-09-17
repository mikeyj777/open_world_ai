import math

class Camera:
    """
    Represents the camera in 3D space, following the player.
    
    Attributes:
        distance (float): Current distance from the player.
        height (float): Height above the player.
        rot_x (float): Vertical rotation (pitch).
        rot_y (float): Horizontal rotation (yaw).
        initial_distance (float): Initial distance from the player.
        initial_height (float): Initial height above the player.
        min_distance (float): Minimum zoom distance.
        max_distance (float): Maximum zoom distance.

    Changes:
        - Updated reset method to align view with z-axis.
    """

    def __init__(self, distance=5, height=2):
        self.initial_distance = distance
        self.initial_height = height
        self.distance = distance
        self.height = height
        self.rot_x = 15  # Initial downward tilt
        self.rot_y = 0   # Initial horizontal rotation (facing negative z-axis)
        self.min_distance = 3  # Minimum zoom distance
        self.max_distance = 20  # Maximum zoom distance

    def rotate(self, dx, dy):
        """
        Rotate the camera based on mouse movement or key presses.
        
        Args:
            dx (float): Change in horizontal rotation.
            dy (float): Change in vertical rotation.
        """
        rot_speed = 0.2
        self.rot_x += dy * rot_speed
        self.rot_y += dx * rot_speed
        self.rot_x = max(-90, min(90, self.rot_x))  # Clamp vertical rotation
        self.rot_y %= 360  # Keep horizontal rotation between 0 and 359 degrees

    def zoom(self, amount):
        """
        Adjust the camera's zoom level.

        Args:
            amount (float): The amount to zoom in (negative) or out (positive).
        """
        self.distance += amount
        self.distance = max(self.min_distance, min(self.max_distance, self.distance))

    def reset(self):
        """
        Reset the camera to its initial state and align with z-axis.
        """
        self.distance = self.initial_distance
        self.height = self.initial_height
        self.rot_x = 15  # Slight downward tilt
        self.rot_y = 0   # Facing negative z-axis (forward in OpenGL)

    def get_position(self, player_pos):
        """
        Calculate the camera's position based on player position and camera attributes.

        Args:
            player_pos (Vector3): The player's position.

        Returns:
            tuple: The camera's position (x, y, z).
        """
        angle_y = math.radians(self.rot_y)
        camera_x = player_pos[0] - self.distance * math.sin(angle_y)
        camera_y = player_pos[1] + self.height
        camera_z = player_pos[2] - self.distance * math.cos(angle_y)
        return (camera_x, camera_y, camera_z)