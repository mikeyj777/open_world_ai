import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Pygame with OpenGL")

# OpenGL setup
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

# Player settings
player_pos = [0, 1, 5]
player_rot = [0, 0]
move_speed = 0.1
mouse_sensitivity = 0.1

def draw_ground():
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.8, 0.2)  # Green color
    for x in range(-10, 10):
        for z in range(-10, 10):
            glVertex3f(x, 0, z)
            glVertex3f(x + 1, 0, z)
            glVertex3f(x + 1, 0, z + 1)
            glVertex3f(x, 0, z + 1)
    glEnd()

def handle_mouse_motion():
    x, y = pygame.mouse.get_pos()
    dx, dy = x - WIDTH // 2, y - HEIGHT // 2
    pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))
    
    player_rot[0] += dy * mouse_sensitivity
    player_rot[1] += dx * mouse_sensitivity
    # Limit the pitch (up/down looking angle)
    player_rot[0] = max(-90, min(90, player_rot[0]))

def handle_movement(keys):
    s = move_speed
    x, y, z = player_pos
    sin_y = math.sin(math.radians(player_rot[1]))
    cos_y = math.cos(math.radians(player_rot[1]))

    if keys[pygame.K_w]:
        x += s * sin_y
        z -= s * cos_y
    if keys[pygame.K_s]:
        x -= s * sin_y
        z += s * cos_y
    if keys[pygame.K_a]:
        x -= s * cos_y
        z -= s * sin_y
    if keys[pygame.K_d]:
        x += s * cos_y
        z += s * sin_y

    player_pos[0] = x
    player_pos[2] = z

# Main loop
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle mouse movement
    handle_mouse_motion()

    # Handle keyboard movement
    keys = pygame.key.get_pressed()
    handle_movement(keys)

    # OpenGL rendering
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Set the camera
    gluLookAt(
        player_pos[0],
        player_pos[1],
        player_pos[2],
        player_pos[0] + math.sin(math.radians(player_rot[1])),
        player_pos[1] + math.tan(math.radians(player_rot[0])),
        player_pos[2] - math.cos(math.radians(player_rot[1])),
        0, 1, 0
    )

    # Draw the ground
    draw_ground()

    # Swap the buffers
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
