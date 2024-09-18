import pygame
from OpenGL.GL import *

def setup_lighting():
    """
    Set up basic lighting for the 3D scene.
    """
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (1, 1, 1, 0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))

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