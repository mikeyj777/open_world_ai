import pygame
from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *

class Player:
    def __init__(self, pos):
        self.pos = Vector3(pos)
        self.rot = Vector3(0, 0, 0)

    def move(self, x, y, z):
        self.pos += Vector3(x, y, z)

    def rotate(self, x, y, z):
        self.rot += Vector3(x, y, z)

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 1, 1, 0))

def draw_ground():
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.8, 0.0)  # Green color
    glVertex3f(-10, 0, -10)
    glVertex3f(-10, 0, 10)
    glVertex3f(10, 0, 10)
    glVertex3f(10, 0, -10)
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
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
            player.move(-0.1, 0, 0)
        if keys[pygame.K_RIGHT]:
            player.move(0.1, 0, 0)
        if keys[pygame.K_UP]:
            player.move(0, 0, -0.1)
        if keys[pygame.K_DOWN]:
            player.move(0, 0, 0.1)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        glTranslate(-player.pos.x, -player.pos.y, -player.pos.z)
        draw_ground()
        glPopMatrix()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()