import pygame
from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *
import math

from camera import Camera
from player import Player
from agent import Agent
from graphics import setup_lighting, draw_ground, draw_grid, draw_cube, render_text
from consts import Consts

def main():
    """
    Main function to set up and run the 3D world simulation.

    This function initializes Pygame and OpenGL, creates the player, camera, and agent,
    and runs the main game loop. It handles user input for player movement,
    camera control, and rendering the 3D world including the agent.

    Coordinate system:
    - Positive X: right
    - Positive Y: up
    - Positive Z: forward (into the screen/field of view)

    Controls:
    - W/A/S/D: Move player forward/left/backward/right
    - Left/Right arrows: Rotate player
    - Up/Down arrows: Rotate camera vertically
    - Left/Right arrows (when not moving player): Rotate camera horizontally
    - Shift + Up/Down arrows: Zoom camera in/out
    - C: Reset camera to initial position and orientation
    """
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    
    gluPerspective(45, (display[0] / display[1]), 0.1, 2000.0)
    
    player = Player((0, 0, 0))
    camera = Camera()
    # Place the agent 40 units away on the z-axis (4 grid squares in front) and centered on x-axis
    agent = Agent((0, 0, -40))
    
    setup_lighting()
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    camera.reset()  # Reset camera when 'C' is pressed

        keys = pygame.key.get_pressed()
        mods = pygame.key.get_mods()
        
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
        
        # Handle camera rotation and zoom
        if mods & pygame.KMOD_SHIFT:
            if keys[pygame.K_UP]:
                camera.zoom(0.1)  # Zoom out
            elif keys[pygame.K_DOWN]:
                camera.zoom(-0.1)  # Zoom in
        else:
            if keys[pygame.K_UP]:
                camera.rotate(0, -1)  # Rotate camera vertically
            elif keys[pygame.K_DOWN]:
                camera.rotate(0, 1)  # Rotate camera vertically
            elif keys[pygame.K_LEFT]:
                camera.rotate(-1, 0)  # Rotate camera horizontally
            elif keys[pygame.K_RIGHT]:
                camera.rotate(1, 0)  # Rotate camera horizontally
        
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
        
        agent.draw()  # Draw the agent
        
        glPopMatrix()
        
        # Render coordinate display
        coords = f"X: {player.pos.x:.2f} Y: {player.pos.y:.2f} Z: {player.pos.z:.2f} Rot: {player.rot:.2f}"
        render_text(coords, Consts.COORD_DISPLAY_ANCHOR_X, Consts.COORD_DISPLAY_ANCHOR_Y)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()