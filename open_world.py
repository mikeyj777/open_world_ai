import pygame
from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

from camera import Camera
from agent import Agent
from graphics import setup_lighting, render_text
from consts import Consts

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
            if len(agent.connected_agents) < len(agent.receptors) and \
               len(other_agent.connected_agents) < len(other_agent.receptors):
                for receptor in agent.receptors:
                    for other_receptor in other_agent.receptors:
                        if receptor.can_connect(other_receptor):
                            agent.connected_agents.append(other_agent)
                            other_agent.connected_agents.append(agent)
                            break
                    if other_agent in agent.connected_agents:
                        break

def update_agents(agents, dt):
    """
    Update all agents and remove dead ones.

    Args:
        agents (list): List of all agents in the simulation.
        dt (float): Time step for the update.

    Returns:
        list: Updated list of agents with dead ones removed.
    """
    alive_agents = []
    for agent in agents:
        agent.update(dt)
        if agent.resources.get_amount("sugar") > 0 and agent.resources.get_amount("spice") > 0:  # Simplified death check
            alive_agents.append(agent)
        else:
            # Remove connections to this agent
            for connected_agent in agent.connected_agents:
                connected_agent.connected_agents.remove(agent)
    return alive_agents

def main():
    """
    Main function to set up and run the 3D world simulation with multiple agents.
    """
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    
    camera = Camera()
    camera.update_projection()  # Set initial projection
    
    agents = create_initial_agents(50)  # Start with 50 agents
    
    setup_lighting()
    
    clock = pygame.time.Clock()
    
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
        
        # Render the scene
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
        
        # Render information display
        info = f"Agents: {len(agents)} | FPS: {clock.get_fps():.2f}"
        render_text(info, Consts.COORD_DISPLAY_ANCHOR_X, Consts.COORD_DISPLAY_ANCHOR_Y)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()