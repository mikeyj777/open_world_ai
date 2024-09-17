import random
import math
from pygame.math import Vector3
from OpenGL.GL import *
from receptor import Receptor
from resource import Resource
from consts import Consts

class Agent:
    # ... (previous code remains the same)

    def draw(self):
        """
        Draw the agent as a cube in the 3D world.
        """
        glPushMatrix()
        glTranslatef(self.pos.x, self.pos.y, self.pos.z)
        
        # Draw a cube to represent the agent
        glColor3f(0.0, 0.0, 1.0)  # Blue color
        glBegin(GL_QUADS)
        # ... (cube drawing code remains the same)
        glEnd()
        
        glPopMatrix()

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