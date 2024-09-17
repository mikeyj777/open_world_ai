from pygame.math import Vector3
import math

class Player:
    """
    Represents the player character in the 3D world.
    
    Attributes:
        pos (Vector3): The position of the player in 3D space.
        rot (float): The rotation of the player (yaw only).

    Coordinate system:
    - Positive X: right
    - Positive Y: up
    - Positive Z: forward (into the screen/field of view)
    """

    def __init__(self, pos):
        self.pos = Vector3(pos)
        self.rot = 0  # Yaw rotation

    def move(self, direction):
        """
        Move the player in a given direction, taking into account its current rotation.
        
        Args:
            direction (str): Direction to move ("FORWARD", "BACKWARD", "LEFT", or "RIGHT").
        """
        move_speed = 0.2
        forward = Vector3(math.sin(math.radians(self.rot)), 0, math.cos(math.radians(self.rot)))
        right = Vector3(forward.z, 0, -forward.x)
        
        match direction:
            case "FORWARD":
                self.pos += forward * move_speed
            case "BACKWARD":
                self.pos -= forward * move_speed
            case "LEFT":
                self.pos -= right * move_speed
            case "RIGHT":
                self.pos += right * move_speed

    def rotate(self, angle):
        """
        Rotate the player.
        
        Args:
            angle (float): Angle to rotate by (positive is clockwise).
        """
        self.rot += angle
        self.rot %= 360  # Keep rotation between 0 and 359 degrees