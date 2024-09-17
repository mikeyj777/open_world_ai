"""
3D Open World Simulation using Pygame and OpenGL

This script creates a simple 3D open world with a flat green ground,
featuring a third-person view of a player character and a coordinate display.

Recent changes:
1. Adjusted initial camera angle to point just above the player's position.
2. Modified camera position calculation to maintain proper view regardless of player's y-position.

Requirements:
- Python 3.11.0
- Pygame 2.5.2
- PyOpenGL 3.1.7
"""

import pygame
from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class Player:
    """
    Represents the player character in the 3D world.
    
    Attributes:
        pos (Vector3): The position of the player in 3D space.
        rot (float): The rotation of the player (yaw only).
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
            angle (float): Angle to rotate by.
        """
        self.rot += angle
        self.rot %= 360  # Keep rotation between 0 and 359 degrees

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

def setup_lighting():
    """
    Set up basic lighting for the 3D scene.
    """
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (1, 1, 1, 0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))

def draw_ground():
    """
    Draw a large green ground plane.
    """
    glDisable(GL_LIGHTING)  # Disable lighting for the ground
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.5, 0.0)  # Green color
    ground_size = 1000
    glVertex3f(-ground_size, -1, -ground_size)
    glVertex3f(-ground_size, -1, ground_size)
    glVertex3f(ground_size, -1, ground_size)
    glVertex3f(ground_size, -1, -ground_size)
    glEnd()
    glEnable(GL_LIGHTING)  # Re-enable lighting for other objects

def draw_cube():
    """
    Draw a simple cube to represent the player.
    """
    glBegin(GL_QUADS)
    # Front face (red)
    glColor3f(1.0, 0.0, 0.0)
    glNormal3f(0, 0, 1)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    # Back face (green)
    glColor3f(0.0, 1.0, 0.0)
    glNormal3f(0, 0, -1)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    # Top face (blue)
    glColor3f(0.0, 0.0, 1.0)
    glNormal3f(0, 1, 0)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, -0.5)
    # Bottom face (yellow)
    glColor3f(1.0, 1.0, 0.0)
    glNormal3f(0, -1, 0)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    # Right face (magenta)
    glColor3f(1.0, 0.0, 1.0)
    glNormal3f(1, 0, 0)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    # Left face (cyan)
    glColor3f(0.0, 1.0, 1.0)
    glNormal3f(-1, 0, 0)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glEnd()

def render_text(text, x, y):
    """
    Render text on the screen using Pygame.
    
    Args:
        text (str): Text to render.
        x (int): X-coordinate for text position.
        y (int): Y-coordinate for text position.
    """
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (255, 255, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

def main():
    """
    Main function to set up and run the 3D world simulation.
    """
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    
    gluPerspective(45, (display[0] / display[1]), 0.1, 2000.0)
    
    player = Player((0, 0, 0))
    camera = Camera()
    
    setup_lighting()
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        keys = pygame.key.get_pressed()
        
        # Handle player movement
        if keys[pygame.K_w]:
            player.move("FORWARD")
        if keys[pygame.K_s]:
            player.move("BACKWARD")
        if keys[pygame.K_a]:
            player.move("LEFT")
        if keys[pygame.K_d]:
            player.move("RIGHT")
        
        # Handle player rotation
        if keys[pygame.K_LEFT]:
            player.rotate(-1)
        if keys[pygame.K_RIGHT]:
            player.rotate(1)
        
        # Handle camera rotation
        if keys[pygame.K_UP]:
            camera.rotate(0, -1)
        if keys[pygame.K_DOWN]:
            camera.rotate(0, 1)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        # Position and rotate the camera
        glRotatef(-camera.rot_x, 1, 0, 0)
        glRotatef(-player.rot, 0, 1, 0)
        camera_pos = player.pos - Vector3(math.sin(math.radians(player.rot)), 0, math.cos(math.radians(player.rot))) * camera.distance
        camera_pos.y = player.pos.y + camera.height  # Adjusted to maintain proper view
        glTranslatef(-camera_pos.x, -camera_pos.y, -camera_pos.z)
        
        draw_ground()
        
        glPushMatrix()
        glTranslatef(player.pos.x, player.pos.y, player.pos.z)
        glRotatef(player.rot, 0, 1, 0)
        draw_cube()
        glPopMatrix()
        
        glPopMatrix()
        
        # Render coordinate display
        coords = f"X: {player.pos.x:.2f} Y: {player.pos.y:.2f} Z: {player.pos.z:.2f}"
        render_text(coords, 10, display[1] - 40)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()