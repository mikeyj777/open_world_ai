import pygame
from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
import numpy as np

from camera import Camera
from agent import Agent
from graphics import *
from consts import Consts
from dashboard import Dashboard

def create_initial_agents(num_agents):
    """
    Create initial set of agents within the circular field.

    Args:
        num_agents (int): Number of agents to create.

    Returns:
        list: List of created Agent objects.
    """
    agents = []
    for _ in range(num_agents):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, Consts.AGENT_FIELD_RADIUS)
        x = Consts.AGENT_FIELD_CENTER[0] + radius * math.cos(angle)
        z = Consts.AGENT_FIELD_CENTER[2] + radius * math.sin(angle)
        agents.append(Agent((x, 0, z)))
    return agents

def check_and_create_connections(agents):
    """
    Check for potential connections between agents and create them if possible.

    Args:
        agents (list): List of all agents in the simulation.
    """
    for i, agent in enumerate(agents):
        for other_agent in agents[i+1:]:
            agent.connect_if_possible(other_agent)

def update_agents(agents, dt):
    """
    Update all agents and remove dead ones.

    Args:
        agents (list): List of all agents in the simulation.
        dt (float): Time step for the update.

    Returns:
        list: Updated list of agents with dead ones removed.
    """
    i = 0
    min_resources = np.inf
    while i < len(agents):
        agent = agents[i]
        agent.manage_resources()
        resources = agent.resources.get_resource_levels()
        tot_resources = sum(resources.values())
        if tot_resources < min_resources:
            min_resources = tot_resources
            min_idx = i
        if not agent.is_alive:
            del agents[i]
            continue
        agent.update(dt)
        
        i += 1

    return agents

def main():
    """
    Main function to set up and run the 3D world simulation with multiple agents.
    """
    pygame.init()
    main_display = (800, 600)
    dashboard_display = (800, 200)
    total_height = main_display[1] + dashboard_display[1]
    
    # Set up a single window with space for both OpenGL and Pygame
    screen = pygame.display.set_mode((main_display[0], total_height), pygame.DOUBLEBUF | pygame.OPENGL)
    
    # Now initialize the camera and update projection
    camera = Camera()
    camera.update_projection()
    
    # Create a separate surface for the dashboard
    dashboard_surface = pygame.Surface(dashboard_display)
    
    agents = create_initial_agents(50)  # Start with 50 agents
    
    setup_lighting()
    
    clock = pygame.time.Clock()
    
    dashboard = Dashboard(dashboard_display[0], dashboard_display[1])
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    camera.reset()
                elif event.key == pygame.K_t:
                    camera.toggle_top_down()
                elif event.key == pygame.K_LEFT:
                    dashboard.scroll(-1, len(agents))
                elif event.key == pygame.K_RIGHT:
                    dashboard.scroll(1, len(agents))

        keys = pygame.key.get_pressed()
        mods = pygame.key.get_mods()
        
        # Handle camera rotation and zoom
        if mods & pygame.KMOD_SHIFT:
            if keys[pygame.K_UP]:
                camera.zoom(-2)  # Zoom in
            elif keys[pygame.K_DOWN]:
                camera.zoom(2)  # Zoom out
        else:
            if keys[pygame.K_UP]:
                camera.rotate(0, -1)  # Rotate camera vertically
            elif keys[pygame.K_DOWN]:
                camera.rotate(0, 1)  # Rotate camera vertically
            elif keys[pygame.K_LEFT]:
                camera.rotate(-1, 0)  # Rotate camera horizontally
            elif keys[pygame.K_RIGHT]:
                camera.rotate(1, 0)  # Rotate camera horizontally
        
        dt = clock.tick(60) / 1000.0  # Get time since last frame in seconds
        
        # Update and manage agents
        check_and_create_connections(agents)
        agents = update_agents(agents, dt)
        
        # Render the main scene
        glViewport(0, dashboard_display[1], main_display[0], main_display[1])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        # Position and rotate the camera
        glRotatef(-camera.rot_x, 1, 0, 0)
        glRotatef(-camera.rot_y, 0, 1, 0)
        camera_pos = camera.get_position(Vector3(0, 0, 0))  # Assuming camera follows a point at (0,0,0)
        glTranslatef(-camera_pos[0], -camera_pos[1], -camera_pos[2])
        
        # Draw all agents and their connections
        for agent in agents:
            agent.draw()
        for agent in agents:
            agent.draw_connections()
        
        glPopMatrix()
        
        # Update and render the dashboard
        dashboard.update(agents)
        dashboard_surface.blit(dashboard.surface, (0, 0))
        
        # Switch to 2D mode for drawing the dashboard
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, main_display[0], 0, total_height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Disable depth testing and lighting for 2D rendering
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        
        # Draw the dashboard
        glRasterPos2f(0, 0)
        dashboard_data = pygame.image.tostring(dashboard_surface, "RGB", True)
        glDrawPixels(dashboard_display[0], dashboard_display[1], GL_RGB, GL_UNSIGNED_BYTE, dashboard_data)
        
        # Re-enable 3D rendering settings
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        
        # Restore the 3D projection and modelview matrices
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        
        # Swap the buffers to display everything
        pygame.display.flip()

if __name__ == "__main__":
    main()