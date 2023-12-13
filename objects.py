from OpenGL.GL import *
from OpenGL.GLUT import *
from matrices import *

class DrawingBase:
    def __init__(self):
        pass

    def apply_transforms(self, r_matrix, s_matrix, t_matrix):    
        glPushMatrix()
        glMultMatrixf(s_matrix.dot(t_matrix).dot(r_matrix))
        

class Pole(DrawingBase):
    def __init__(self, radius, height):
        super().__init__()
        self.radius = radius
        self.height = height

    def draw(self, prop, r_matrix, s_matrix, t_matrix):
        glColor3f(1.0, 1.0, 1.0)

        self.apply_transforms(r_matrix, s_matrix, t_matrix)
        # glMultMatrixf(translation_matrix([pos[0], pos[1], pos[2] + 0.5 * prop[2]]))
        # glTranslatef(pos[0], pos[1], pos[2] + 0.5 * prop[2])
        glutSolidCylinder(self.radius * prop[0], self.height * prop[1], 20, 20)
        glPopMatrix()