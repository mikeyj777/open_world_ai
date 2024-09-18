import random
import math
import uuid
from pygame.math import Vector3
from OpenGL.GL import *

from receptor import Receptor
from agent_resources import Resources
from consts import Consts

class Agent:
    """
    Represents an agent in the 3D world simulation.

    Attributes:
        pos (Vector3): The position of the agent in 3D space.
        receptors (list): List of Receptor objects.
        resources (Resource): Resource object managing the agent's resources.
        connected_agents (list): List of connected Agent objects.
        is_bad (bool): Whether the agent is a "bad" agent.
        velocity (Vector3): The agent's current velocity.
    """

    def __init__(self, pos):
        self.id = f'{uuid.uuid4()}'
        self.pos = Vector3(pos)
        self.receptors = self._generate_receptors()
        self.resources = Resources()
        self.connected_agents = []
        self.is_bad = random.random() < 0.05  # 5% chance of being a bad agent
        self.velocity = Vector3(random.uniform(-1, 1), 0, random.uniform(-1, 1)).normalize()
        self.is_alive = True

    def _generate_receptors(self):
        num_receptors = max(0, int(random.gauss(5, 3)))
        return [Receptor() for _ in range(num_receptors)]

    def update(self, dt):
        """
        Update the agent's state, including movement and resource management.

        Args:
            dt (float): Time step for the update.
        """
        self._share_resources()
        self._move()

    def _move(self, dt):
        """
        Move the agent within the circular field, bouncing off the boundaries.

        agents connected to other agents do not move.

        Args:
            dt (float): Time step for the movement.
        """
        if len(self.connected_agents) > 0:
            return

        new_pos = self.pos + self.velocity * dt

        # Check if the new position is outside the circular field
        distance_to_center = (new_pos - Vector3(Consts.AGENT_FIELD_CENTER)).length()
        if distance_to_center > Consts.AGENT_FIELD_RADIUS:
            # Calculate the normal vector at the point of collision
            normal = (new_pos - Vector3(Consts.AGENT_FIELD_CENTER)).normalize()
            # Reflect the velocity vector
            self.velocity = self.velocity.reflect(normal)
            new_pos = self.pos + self.velocity * dt

        self.pos = new_pos

    def manage_resources(self):
        """
        Manage the agent's resources, including generation and metabolism.
        """
        for resource_type in Resources.TYPES:
            if random.random() < 0.1:  # 10% chance to generate each resource
                self.resources.generate(resource_type, random.uniform(0.1, 0.3))
            if random.random() < 0.2:  # 20% chance to metabolize each resource
                self.resources.metabolize(resource_type, 0.1)

        # Check if the agent should die - if it is depleted of two or more resources
        if sum(1 for r in Resources.TYPES if self.resources.get_amount(r) == 0) >= 2:
            self._die()

    def _share_resources(self):
        """
        Share resources with connected agents.
        """
        for connected_agent in self.connected_agents:
            for resource_type in Resources.TYPES:
                if self.is_bad:
                    self._strip_resources(connected_agent, resource_type)
                else:
                    self._balance_resources(connected_agent, resource_type)

    def _strip_resources(self, other_agent, resource_type):
        """
        Strip resources from the connected agent (bad agent behavior).

        Args:
            other_agent (Agent): The agent to strip resources from.
            resource_type (str): The type of resource to strip.
        """
        amount = min(0.01, other_agent.resources.get_amount(resource_type))
        other_agent.resources.metabolize(resource_type, amount)
        self.resources.generate(resource_type, amount)

    def _balance_resources(self, other_agent, resource_type):
        """
        Balance resources with the connected agent (normal agent behavior).

        Args:
            other_agent (Agent): The agent to balance resources with.
            resource_type (str): The type of resource to balance.
        """
        my_amount = self.resources.get_amount(resource_type)
        other_amount = other_agent.resources.get_amount(resource_type)

        if my_amount > other_amount + 2:
            transfer = min(0.01, my_amount - other_amount - 2)
            self.resources.metabolize(resource_type, transfer)
            other_agent.resources.generate(resource_type, transfer)

    def _die(self):
        """
        Handle the death of the agent.
        """
        for connected_agent in self.connected_agents:
            connected_agent.connected_agents.remove(self)
            for connected_receptor in connected_agent.receptors:
                id = connected_receptor.id
                for receptor in self.receptors:
                    if receptor.connected_receptor_id == id:
                        connected_receptor.connected_receptor_id = None
        
        for receptor in self.receptors:
            receptor.connected_receptor_id = None
        
        self.receptors.clear()
        self.connected_agents.clear()
        self.is_alive = False

    def draw(self):
        """
        Draw the agent as a cube in the 3D world.
        """
        glPushMatrix()
        glTranslatef(self.pos.x, self.pos.y, self.pos.z)
        
        # Draw a cube to represent the agent
        glColor3f(0.0, 0.0, 1.0)  # Blue color
        glBegin(GL_QUADS)
        # Front face
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        # Back face
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        # Top face
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, -0.5)
        # Bottom face
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        # Right face
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        # Left face
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glEnd()
        
        glPopMatrix()

    def connect_if_possible(self, other_agent):
        """
        Test if the agent can connect to another agent.

        Args:
            other_agent (Agent): The other agent to test connectivity with.
            distance (float): The distance between the agents.
        """

        if other_agent in self.connected_agents:
            return
        
        direction = self.pos - other_agent.pos
        distance = direction.length()

        if distance < Consts.MIN_DISTANCE_BETWEEN_AGENTS_FOR_CONNECTION and \
            len(self.connected_agents) < len(self.receptors) and \
            len(other_agent.connected_agents) < len(other_agent.receptors):
                for receptor in self.receptors:
                    for other_receptor in other_agent.receptors:
                        if not receptor.can_connect(other_receptor):
                            continue
                        receptor.connected_receptor_id = other_receptor.id
                        other_receptor.connected_receptor_id = receptor.id
                        self.connected_agents.append(other_agent)
                        other_agent.connected_agents.append(self)
                        break
                    

    def draw_connections(self):
        """
        Draw connections to other agents.
        """
        glColor3f(1.0, 1.0, 0.0)  # Yellow color for connections
        glLineWidth(2.0)
        glBegin(GL_LINES)
        
        for connected_agent in self.connected_agents:
            direction = connected_agent.pos - self.pos
            distance = direction.length()
            
            if distance > 0:
                # Normalize the direction vector
                direction /= distance
                
                # Calculate the angle in the XZ plane
                angle = math.degrees(math.atan2(direction.z, direction.x))
                
                # Adjust the angle to be between 45 and 135 degrees in 15-degree increments
                adjusted_angle = 45 + 15 * round((angle - 45) / 15)
                adjusted_angle = max(45, min(135, adjusted_angle))
                
                # Calculate the endpoint of the connection line
                connection_length = min(distance, 5)  # Limit the length of the connection line
                end_x = self.pos.x + connection_length * math.cos(math.radians(adjusted_angle))
                end_z = self.pos.z + connection_length * math.sin(math.radians(adjusted_angle))
                
                glVertex3f(self.pos.x, self.pos.y, self.pos.z)
                glVertex3f(end_x, self.pos.y, end_z)
        
        glEnd()