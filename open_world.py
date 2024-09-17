import random
import math

import pygame
from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *


from camera import Camera
from player import Player
from agent import Agent
from graphics import setup_lighting, draw_scene, render_text
from consts import Consts

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