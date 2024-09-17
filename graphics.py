import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

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
    Draw a large green ground plane with a grid.
    """
    glDisable(GL_LIGHTING)  # Disable lighting for the ground

    # Draw the main ground plane
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.5, 0.0)  # Green color
    ground_size = 1000
    glVertex3f(-ground_size, -1, -ground_size)
    glVertex3f(-ground_size, -1, ground_size)
    glVertex3f(ground_size, -1, ground_size)
    glVertex3f(ground_size, -1, -ground_size)
    glEnd()

    # Draw grid lines
    glBegin(GL_LINES)
    glColor3f(0.3, 0.3, 0.3)  # Gray color for grid lines
    grid_size = 100
    step = 10
    for i in range(-grid_size, grid_size + 1, step):
        glVertex3f(i, -0.99, -grid_size)
        glVertex3f(i, -0.99, grid_size)
        glVertex3f(-grid_size, -0.99, i)
        glVertex3f(grid_size, -0.99, i)
    glEnd()

    glEnable(GL_LIGHTING)  # Re-enable lighting for other objects  # Re-enable lighting for other objects

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