import random

class Receptor:
    """
    Represents a receptor on an agent that can connect to other agents.

    Attributes:
        angle (int): The angle of the receptor. Valid angles are 0, 15, 30, 45, 60, 75, and 90 degrees.
    """

    VALID_ANGLES = [0, 15, 30, 45, 60, 75, 90]

    def __init__(self):
        self.angle = random.choice(self.VALID_ANGLES)

    def can_connect(self, other_receptor):
        """
        Check if this receptor can connect to another receptor.

        Args:
            other_receptor (Receptor): The receptor to check for connection.

        Returns:
            bool: True if the receptors can connect, False otherwise.
        """
        return self.angle + other_receptor.angle == 90