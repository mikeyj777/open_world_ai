import pygame
from OpenGL.GL import *
import math

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (1, 1, 1, 0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))

def draw_ground():
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

def draw_grid(player_pos):
    glDisable(GL_LIGHTING)  # Disable lighting for the grid
    glBegin(GL_LINES)
    glColor3f(0.3, 0.3, 0.3)  # Gray color for grid lines
    
    grid_size = 100
    step = 10

    # Calculate the offset to center the grid around the player
    offset_x = math.floor(player_pos[0] / grid_size) * grid_size
    offset_z = math.floor(player_pos[2] / grid_size) * grid_size

    # Draw vertical lines
    for i in range(-grid_size, grid_size + 1, step):
        x = i + offset_x
        glVertex3f(x, -0.99, -grid_size + offset_z)
        glVertex3f(x, -0.99, grid_size + offset_z)

    # Draw horizontal lines
    for i in range(-grid_size, grid_size + 1, step):
        z = i + offset_z
        glVertex3f(-grid_size + offset_x, -0.99, z)
        glVertex3f(grid_size + offset_x, -0.99, z)

    glEnd()
    glEnable(GL_LIGHTING)  # Re-enable lighting for other objects

def draw_cube():
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
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (255, 255, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)