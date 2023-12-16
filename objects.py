from OpenGL.GL import *
from OpenGL.GLUT import *
from matrices import *

class DrawingBase:
    def __init__(self):
        self.transforms = []

    def reg_transforms(self, transforms):
        self.transforms.extend(transforms)

    def _apply_transforms(self):    
        if len(self.transforms) == 0:
            return
        
        final_transform = self.transforms[0]
        for transform in self.transforms[1:]:
            final_transform = final_transform @ transform # equivalent to matmul

        glMultMatrixf(final_transform)
        

class Pole(DrawingBase):
    def __init__(self, radius, height):
        super().__init__()
        self.radius = radius
        self.height = height

    def draw(self):
        glColor3f(1.0, 1.0, 1.0)

        glPushMatrix()
        self._apply_transforms()
        glutSolidCylinder(self.radius, self.height, 20, 20)
        glPopMatrix()


class PoleBase(DrawingBase):
    def __init__(self, color):
        super().__init__()
        self.color = color

    def draw(self):
        glColor3f(*self.color)
        glPushMatrix()
        self._apply_transforms()
        glutSolidCube(1.0)
        glPopMatrix()


class TriangularPrism(DrawingBase):
    def __init__(self, color=(1.0, 0, 0), isosceles=False):
        super().__init__()
        self.color = color
        
        self.face_idces = [0,1,4,3,0,2,5,3,1,2,5,4]
        if isosceles:
            self.triangle_vertices = [
                (-1.0, 0.0, -1.0),
                (1.0, 0.0, -1.0),
                (-1.0, 2.0, -1.0),
                (-1.0, 0.0, 1.0),
                (1.0, 0.0, 1.0),
                (-1.0, 2.0, 1.0)
            ]
        else:
            self.triangle_vertices = [
                (-1.0, 0.0, -1.0),
                (1.0, 0.0, -1.0),
                (0.0, 1.0, -1.0),
                (-1.0, 0.0, 1.0),
                (1.0, 0.0, 1.0),
                (0.0, 1.0, 1.0)
            ]

        self.face_vertices = [self.triangle_vertices[idx] for idx in self.face_idces]

    def draw(self):
        glPushMatrix()
        self._apply_transforms()

        glBegin(GL_TRIANGLES)
        glColor3f(*self.color)
        for vertex in self.triangle_vertices:
            glVertex3f(*vertex)
        glEnd()

        glBegin(GL_QUADS)

        for vertex in self.face_vertices:
            glVertex3f(*vertex)
        glEnd()

        glPopMatrix()

class Ground(DrawingBase):
    def __init__(self, color=(1.0, 0, 0), radius=5, segments=100):
        super().__init__()
        self.color = color
        self.radius = radius
        self.segments = segments

    def draw(self):
        glPushMatrix()
        self._apply_transforms()
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(*self.color)
        glVertex3f(0.0, 0.0, 0.0)  # Center of the floor

        for i in range(self.segments + 1):
            theta = (2.0 * np.pi * i) / self.segments
            x = self.radius * np.cos(theta)
            y = self.radius * np.sin(theta)
            glVertex3f(x, y, 0.0)

        glEnd()
        glPopMatrix()