from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *
from objects import *
from matrices import *

LIGHT_POSITION = [-5, -5, 5]
LIGHT_VALUES = [.15, 1, 1]
font = None

def draw_axes(length):
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0) # X
    glVertex3f(-length, 0.0, 0.0)
    glVertex3f(length, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0) # Y
    glVertex3f(0.0, -length, 0.0)
    glVertex3f(0.0, length, 0.0)

    glColor3f(0.0, 0.0, 1.0) # Z
    glVertex3f(0.0, 0.0, -length)
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

    # for i in np.linspace(0, length + 1, 100):
    #     label_text(f'{i:.2f}', -0.05, 0.0, i - 0.01, (1.0, 1.0, 1.0))


def label_text(text, x, y, z, color):
    glColor3f(*color)
    glRasterPos3f(x, y, z)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))

def drawText(x, y, text):                                                
    textSurface = font.render(text, True, (255, 255, 66, 255), (0, 66, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def draw_light_source():
    glPushMatrix()
    glTranslate(*LIGHT_POSITION)
    glutSolidSphere(.1, 10, 10)
    glPopMatrix()

def setup_lighting():
    global LIGHT_VALUES
    glLightfv(GL_LIGHT0, GL_POSITION, LIGHT_POSITION)
    k_a, k_d, k_s = LIGHT_VALUES
    glLightfv(GL_LIGHT0, GL_AMBIENT, (k_a, k_a, k_a, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (k_d, k_d, k_d, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (k_s, k_s, k_s, 1))
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (.2, .2, .2, 1))
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)
    draw_light_source()

def draw_scene():
    for i, val in enumerate(LIGHT_VALUES):
        drawText(140 + i * 100, 120, f'{val:.2f}')
        
    ground = Ground((0.1, 0.53, 0), 5, 10)
    ground.reg_transforms([
        translation_matrix(-2, -2, 0)
    ])
    ground.draw()

    pole_radius = 0.025

    pole_offset_x = 1
    pole_offset_z = .3
    pole_base_height = 0.5
    left_pole = Pole(pole_radius, 1.0)
    left_pole.reg_transforms([ 
        scale_matrix(1, 1, 2.5), 
        translation_matrix(-pole_offset_x, 0, pole_base_height)
    ])
    left_pole.draw()

    right_pole = Pole(pole_radius, 1.0)
    right_pole.reg_transforms([ 
        scale_matrix(1, 1, 2.5), 
        translation_matrix(pole_offset_x, 0, pole_offset_z)
    ])
    right_pole.draw()

    left_pole_base = PoleBase((1, 1, 1))
    left_pole_base.reg_transforms([ 
        scale_matrix(1, 0.75, pole_base_height),
        translation_matrix(-pole_offset_x, 0, pole_offset_z)
    ])
    left_pole_base.draw()

    right_pole_base = PoleBase((1, 1, 1))
    right_pole_base.reg_transforms([
        scale_matrix(1, 0.75, pole_base_height),
        # translation_matrix(0, 0, pole_base_height),
        translation_matrix(pole_offset_x, 0, pole_offset_z)
    ])
    right_pole_base.draw()


    # center pole
    center_pole_z_offset = -.25
    center_pole = Pole(pole_radius, 1.0)
    center_pole.reg_transforms([
        translation_matrix(0, center_pole_z_offset, .2),
        scale_matrix(1, 1, 2.75) 
    ])
    center_pole.draw()

    center_pole_base = PoleBase((1, .1, 0))
    center_pole_base.reg_transforms([
        scale_matrix(1, 0.75, pole_base_height + 0.1),
        translation_matrix(0, center_pole_z_offset, pole_offset_z + 0.05)
    ])
    center_pole_base.draw()

    center_prism = TriangularPrism(color=(1, .1, 0), rectangle=True, normal=True)
    center_prism.reg_transforms([
        rotation_matrix(-90, (0, 1, 0)),
        scale_matrix(0.5, 0.25, 0.2),
        translation_matrix(0, 0.12, 0.45)
    ])
    center_prism.draw()

    center_prism_base = PoleBase((1, .1, 0))
    center_prism_base.reg_transforms([
        scale_matrix(1, 1, .2),
        translation_matrix(0, .12, .15)
    ])
    center_prism_base.draw()

    # logo prism
    logo_prism = TriangularPrism(color=(0.68, 0.65, 0.51), rectangle=False, normal=True)
    logo_prism.reg_transforms([
        scale_matrix(0.5, 0.5, 1.5),
        rotation_matrix(-30, (0, 0, 1)),
        translation_matrix(-3.5, -3.75, 1.5)
    ])
    logo_prism.draw()


def main():
    global LIGHT_POSITION, font, LIGHT_VALUES
    DISPLAY_SIZE = (1280, 720)
    rotation_speed = 0.2
    camera = [-10, 7, 3.5]
    rotation = [0, 0, 0]
    ortho = False
    pygame.init()
    pygame.display.set_mode(DISPLAY_SIZE, DOUBLEBUF | OPENGL)
    font = pygame.font.SysFont('arial', 32)

    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
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
                elif ev.key == pygame.K_l:
                    LIGHT_POSITION = (
                        LIGHT_POSITION[0] * np.cos(rotation_speed) - LIGHT_POSITION[1] * np.sin(rotation_speed),
                        LIGHT_POSITION[0] * np.sin(rotation_speed) + LIGHT_POSITION[1] * np.cos(rotation_speed),
                        LIGHT_POSITION[2] * .95
                    )
                elif ev.key == pygame.K_k:
                    LIGHT_POSITION = (
                        LIGHT_POSITION[0] * np.cos(-rotation_speed) - LIGHT_POSITION[1] * np.sin(-rotation_speed),
                        LIGHT_POSITION[0] * np.sin(-rotation_speed) + LIGHT_POSITION[1] * np.cos(-rotation_speed),
                        LIGHT_POSITION[2] * 1.05
                    )
                elif ev.key == pygame.K_q:
                    LIGHT_VALUES[0] = min(LIGHT_VALUES[0] * 1.1, 1)
                elif ev.key == pygame.K_a:
                    LIGHT_VALUES[0] *= 0.9
                elif ev.key == pygame.K_w:
                    LIGHT_VALUES[1] = min(LIGHT_VALUES[1] * 1.1, 1)
                elif ev.key == pygame.K_s:
                    LIGHT_VALUES[1] *= 0.9
                elif ev.key == pygame.K_e:
                    LIGHT_VALUES[2] = min(LIGHT_VALUES[2] * 1.1, 1)
                elif ev.key == pygame.K_d:
                    LIGHT_VALUES[2] *= 0.9
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 4:  # Scroll Up
                    camera = [coord * 0.9 for coord in camera]
                elif ev.button == 5:  # Scroll Down
                    camera = [coord * 1.1 for coord in camera]
            elif ev.type == pygame.MOUSEMOTION:
                if ev.buttons[0]:  # Left mouse button pressed
                    rotation[1] -= ev.rel[0] * rotation_speed
                    rotation[0] -= ev.rel[1] * rotation_speed

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(camera[0], camera[1], camera[2], 0, 0, 0, 0, 0, 1)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if ortho:
            glOrtho(-5, 5, -5, 5, 0.1, 50.0)
        else:
            gluPerspective(45, (DISPLAY_SIZE[0]/DISPLAY_SIZE[1]), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
        glPushMatrix()
        glRotatef(rotation[0], 1, 0, 0)
        glRotatef(rotation[1], 0, 1, 0)
        glRotatef(rotation[2], 0, 0, 1)

        setup_lighting()
        draw_scene()
        # draw_axes(100.0)

        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
