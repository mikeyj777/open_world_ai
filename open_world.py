# Requires: 
# - Python 3.11.0
# - Pygame 2.5.2
# - PyOpenGL 3.1.7

import pygame
from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *

class Player:
    def __init__(self, pos):
        self.pos = Vector3(pos)
        self.rot = Vector3(0, 0, 0)

    def move(self, direction):
        move_speed = 0.5
        match direction:
            case "LEFT":
                self.pos.x -= move_speed
            case "RIGHT":
                self.pos.x += move_speed
            case "UP":
                self.pos.z -= move_speed
            case "DOWN":
                self.pos.z += move_speed

    def rotate(self, x, y, z):
        self.rot += Vector3(x, y, z)

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 1, 1, 0))

def draw_ground():
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.5, 0.0)  # Darker green color
    ground_size = 1000  # Increased size for "infinite" effect
    glVertex3f(-ground_size, 0, -ground_size)
    glVertex3f(-ground_size, 0, ground_size)
    glVertex3f(ground_size, 0, ground_size)
    glVertex3f(ground_size, 0, -ground_size)
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    
    gluPerspective(45, (display[0] / display[1]), 0.1, 2000.0)  # Increased far clipping plane
    glTranslatef(0.0, -1.0, -10)
    
    player = Player((0, 1, 0))
    
    setup_lighting()
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move("LEFT")
        if keys[pygame.K_RIGHT]:
            player.move("RIGHT")
        if keys[pygame.K_UP]:
            player.move("UP")
        if keys[pygame.K_DOWN]:
            player.move("DOWN")
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        glTranslate(-player.pos.x, -player.pos.y, -player.pos.z)
        draw_ground()
        glPopMatrix()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()