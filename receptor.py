import random
import uuid

class Receptor:
    """
    Represents a receptor on an agent that can connect to other agents.

    Attributes:
        angle (int): The angle of the receptor. Valid angles are 0, 15, 30, 45, 60, 75, and 90 degrees.
    """

    
    VALID_ANGLES = [0, 15, 30, 45, 60, 75, 90]

    def __init__(self):
        self.angle = random.choice(self.VALID_ANGLES)
        self.id = f'{uuid.uuid4()}'
        self.connected_receptor_id = None

    def can_connect(self, other_receptor):
        """
        Check if this receptor can connect to another receptor.
        receptors can connect if their angles sum to 90 and there is no stored property for a connected receptor id
        Args:
            other_receptor (Receptor): The receptor to check for connection.

        Returns:
            bool: True if the receptors can connect, False otherwise.  
            
        """
        angle_ok = self.angle + other_receptor.angle == 90
        no_agent_id_me = self.connected_receptor_id is None
        no_agent_id_other = other_receptor.connected_receptor_id is None
        
        return (angle_ok and no_agent_id_me and no_agent_id_other)