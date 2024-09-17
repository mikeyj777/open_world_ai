import pygame
from OpenGL.GL import *
import math
import time

from agent import Agent

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
    text_surface = font.render(text, True, (0, 0, 0))  # Black text
    text_rect = text_surface.get_rect()
    
    # Create a white background surface
    background_surface = pygame.Surface((text_rect.width + 10, text_rect.height + 10))
    background_surface.fill((255, 255, 255))  # White color
    
    # Blit the text onto the background
    background_surface.blit(text_surface, (5, 5))
    
    # Convert the entire surface (background + text) to a string
    surface_data = pygame.image.tostring(background_surface, "RGBA", True)
    
    # Save the current matrix
    glPushMatrix()
    
    # Switch to 2D rendering
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0.0, pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height(), 0.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Disable lighting for 2D rendering
    glDisable(GL_LIGHTING)
    
    # Render the text
    glRasterPos2i(x, y)
    glDrawPixels(background_surface.get_width(), background_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, surface_data)
    
    # Restore the matrices
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    
    # Re-enable lighting
    glEnable(GL_LIGHTING)

def animate_agent(agent, player, radius=40):
    """
    Animate the agent in a circular path around the player.
    
    Args:
        agent (Agent): The agent to animate.
        player (Player): The player to circle around.
        radius (float): The radius of the circular path.
    """
    # Calculate the elapsed time
    current_time = time.time()
    elapsed_time = current_time % (2 * math.pi)  # Complete a circle every 2π seconds
    
    # Calculate new position
    x = player.pos.x + radius * math.cos(elapsed_time)
    z = player.pos.z + radius * math.sin(elapsed_time)
    
    # Update agent position
    agent.pos.x = x
    agent.pos.z = z
    agent.pos.y = player.pos.y  # Keep the same y-coordinate as the player

def draw_scene(player, camera, agents):
    """
    Draw the entire scene including ground, grid, player, and agent.
    
    Args:
        player (Player): The player object.
        camera (Camera): The camera object.
        agent (Agent): The agent object.
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glPushMatrix()
    # Position and rotate the camera
    glRotatef(-camera.rot_x, 1, 0, 0)
    glRotatef(-camera.rot_y, 0, 1, 0)
    camera_pos = camera.get_position(player.pos)
    glTranslatef(-camera_pos[0], -camera_pos[1], -camera_pos[2])
    
    draw_ground()
    draw_grid(player.pos)
    
    glPushMatrix()
    glTranslatef(player.pos.x, player.pos.y, player.pos.z)
    glRotatef(-player.rot, 0, 1, 0)
    draw_cube()
    glPopMatrix()
    agent:Agent
    for agent in agents:
        agent._move(dt=0.1)
        agent.draw()
    
    glPopMatrix()