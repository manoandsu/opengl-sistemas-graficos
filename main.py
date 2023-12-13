from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *
from objects import      Pole
from matrices import *

DISPLAY_SIZE = (1280, 720)

def draw_axes(length):
    glBegin(GL_LINES)

    # X-axis (red)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(length, 0.0, 0.0)

    # Y-axis (green)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, length, 0.0)

    # Z-axis (blue)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, length)

    glEnd()

def main():
    button_down = False
    pygame.init()
    
    pygame.display.set_mode(DISPLAY_SIZE, DOUBLEBUF | OPENGL)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (DISPLAY_SIZE[0]/DISPLAY_SIZE[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)  
    modelMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    
    glutInit()

    t_matrix = translation_matrix([0, 0, 0])
    s_matrix = scale_matrix(1, 1, 1)
    r_matrix = rotation_matrix(0, [1, 0, 0])
    while True:
        glPushMatrix()
    
        # Configuração PYGAME para visualização
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 4:
                    glTranslatef(0.0, 0.0, 0.5) 
                if ev.button == 5:
                    glTranslatef(0.0, 0.0, -0.5)

            keys = pygame.key.get_pressed()
            if keys[K_s]:
                glTranslatef(0.0, 0.5, 0.0)
            if keys[K_d]:
                glTranslatef(-0.5, 0.0, 0.0)
            if keys[K_w]:
                glTranslatef(0.0, -0.5, 0.0)
            if keys[K_a]:
                glTranslatef(0.5, 0.0, 0.0)
            if keys[K_1]:
                r_matrix = rotation_matrix(45, [0, 0, 1])
            if keys[K_2]:
                s_matrix = scale_matrix(1, 1.7, 1)
            if keys[K_3]:
                t_matrix = translation_matrix([1, 0, 0])
            if ev.type == pygame.MOUSEMOTION:
                if button_down == True:
                    glRotatef(ev.rel[1], 1, 0, 0)
                    glRotatef(ev.rel[0], 0, 1, 0)

        for event in pygame.mouse.get_pressed():
            if pygame.mouse.get_pressed()[0] == 1:
                button_down = True
            elif pygame.mouse.get_pressed()[0] == 0:
                button_down = False


        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMultMatrixf(modelMatrix)
        modelMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        glLoadIdentity()
        glTranslatef(0, 0, -5)
        glMultMatrixf(modelMatrix)
        quadrado = Pole(0.05, 4.0)
        quadrado.draw((1.0, 1.0, 1.0), r_matrix, s_matrix, t_matrix)
        draw_axes(200.0)
        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
