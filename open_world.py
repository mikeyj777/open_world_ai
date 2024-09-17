import pygame
from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *
import math

from camera import Camera
from player import Player
from graphics import setup_lighting, draw_ground, draw_grid, draw_cube, render_text

def main():
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
        camera_pos.y = player.pos.y + camera.height
        glTranslatef(-camera_pos.x, -camera_pos.y, -camera_pos.z)
        
        draw_ground()
        draw_grid(player.pos)  # Pass player position to draw_grid
        
        glPushMatrix()
        glTranslatef(player.pos.x, player.pos.y, player.pos.z)
        glRotatef(player.rot, 0, 1, 0)
        draw_cube()
        glPopMatrix()
        
        glPopMatrix()
        
        # Render coordinate display
        coords = f"X: {player.pos.x:.2f} Y: {player.pos.y:.2f} Z: {player.pos.z:.2f}"
        render_text(coords, 10, 60)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()