from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *
from objects import *
from matrices import *

def draw_axes(length):
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0) # X
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(length, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0) # Y
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, length, 0.0)

    glColor3f(0.0, 0.0, 1.0) # Z
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, length)

    glEnd()

    # Axes Labels
    label_text("X", length + 0.1, 0.0, 0.0, (1.0, 0.0, 0.0))
    label_text("Y", 0.0, length + 0.1, 0.0, (0.0, 1.0, 0.0))
    label_text("Z", 0.0, 0.0, length + 0.1, (0.0, 0.0, 1.0))

    # Axes values
    glColor3f(1.0, 1.0, 1.0)
    for i in range(1, int(length) + 1):
        label_text(str(i), i - 0.01, -0.05, 0.0, (1.0, 1.0, 1.0))

    for i in range(1, int(length) + 1):
        label_text(str(i), -0.05, i - 0.01, 0.0, (1.0, 1.0, 1.0))

    for i in range(1, int(length) + 1):
        label_text(str(i), -0.05, 0.0, i - 0.01, (1.0, 1.0, 1.0))

def label_text(text, x, y, z, color):
    glColor3f(*color)
    glRasterPos3f(x, y, z)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))

def main():
    DISPLAY_SIZE = (1280, 720)
    rotation_speed = 1.0
    zoom_speed = 0.1
    camera = [5, 5, 2.5]
    rotation = [0, 0, 0]
    ortho = False

    pygame.init()
    pygame.display.set_mode(DISPLAY_SIZE, DOUBLEBUF | OPENGL)

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glutInit()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_p:
                    ortho = not ortho
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 4:  # Scroll Up
                    camera[2] -= zoom_speed
                elif ev.button == 5:  # Scroll Down
                    camera[2] += zoom_speed
            elif ev.type == pygame.MOUSEMOTION:
                if ev.buttons[0]:  # Left mouse button pressed
                    rotation[1] += ev.rel[0] * rotation_speed
                    rotation[0] += ev.rel[1] * rotation_speed

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(camera[0], camera[1], camera[2], 0, 0, 0, 0, 0, 1)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if ortho:
            glOrtho(-5, 5, -5, 5, 0.1, 50.0)
        else:
            gluPerspective(45, (DISPLAY_SIZE[0]/DISPLAY_SIZE[1]), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        
        glPushMatrix()
        glRotatef(rotation[0], 1, 0, 0)
        glRotatef(rotation[1], 0, 1, 0)
        glRotatef(rotation[2], 0, 0, 1)
        pole = Pole(0.05, 1.0)
        pole.reg_transforms([ scale_matrix(1, 1, 1.5), scale_matrix(1, 1, 2) ])
        pole.draw()
        draw_axes(10.0)

        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
