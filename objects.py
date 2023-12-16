from OpenGL.GL import *
from OpenGL.GLUT import *
from matrices import *

class DrawingBase:
    def __init__(self):
        self.transforms = []
        pass

    def reg_transforms(self, transforms):
        self.transforms.extend(transforms)

    def _apply_transforms(self):    
        if len(self.transforms) == 0:
            print("called apply transform with empty transform list")
            return
        
        final_transform = self.transforms[0]
        for transform in self.transforms[1:]:
            final_transform = final_transform @ transform # equivalent to matmul
            # final_transform.dot(transform)

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
