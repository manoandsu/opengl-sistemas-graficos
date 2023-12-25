from OpenGL.GL import *
from OpenGL.GLUT import *
from matrices import *
from time import sleep

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
        glPushMatrix()
        self._apply_transforms()
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, (.1, .1, .1, 1))
        glMaterial(GL_FRONT_AND_BACK, GL_EMISSION, (0, 0, 0, 1))
        glColor3fv((1, 1, 1))
        glutSolidCylinder(self.radius, self.height, 20, 20)
        glPopMatrix()


class PoleBase(DrawingBase):
    def __init__(self, color=(1, 1, 1)):
        super().__init__()
        self.color = color

    def draw(self):
        glPushMatrix()
        self._apply_transforms()
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, (.1, .1, .1, 1))
        glMaterial(GL_FRONT_AND_BACK, GL_EMISSION, (0, 0, 0, 1))
        glColor3fv(self.color)
        glutSolidCube(1.0)
        glPopMatrix()


class TriangularPrism(DrawingBase):
    def __init__(self, color=(1.0, 0, 0), rectangle=False, normal=False):
        super().__init__()
        self.color = color
        self.rectangle = rectangle
        self.face_idces = [0,1,4,3,  2,0,3,5,  1,2,5,4]
        self.normal = normal
        self.normal_vectors = np.array([ [0, -1, 0], [-1, 1, 0], [1, 1, 0] ])
        if rectangle:
            self.triangle_vertices = [
                (-1.0, 0.0, -1.0), #0 A
                (1.0, 0.0, -1.0),  #1 B
                (-1.0, 2.0, -1.0), #2 C
                (-1.0, 0.0, 1.0),  #3 D
                (1.0, 0.0, 1.0),   #4 E
                (-1.0, 2.0, 1.0)   #5 F
            ]
        else:
            self.triangle_vertices = np.array([
                [-1.0, 0.0, -1.0],  #0 A
                [1.0, 0.0, -1.0],   #1 B
                [0.0, 1.0, -1.0],   #2 C
                [-1.0, 0.0, 1.0],   #3 D
                [1.0, 0.0, 1.0],    #4 E
                [0.0, 1.0, 1.0]     #5 F
            ])

        self.face_vertices = [self.triangle_vertices[idx] for idx in self.face_idces]
        self.light_position = [-5.5, -5.75, 10, 1.0]
        self.ambient_color = [253/255, 184/255, 19/255, 1.0]
        self.diffuse_color = [1.0, 1.0, 1.0, 1.0]
        self.specular_color = [1.0, 1.0, 1.0, 1.0]
        self.shininess = 50.0

    def draw(self):
        glPushMatrix()
        
        self._apply_transforms()

        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, (.1, .1, .1, 1))
        glMaterial(GL_FRONT_AND_BACK, GL_EMISSION, (0, 0, 0, 1))
        glColor3fv(self.color)
        glBegin(GL_TRIANGLES)
        for i, vertex in enumerate(self.triangle_vertices):
            if self.normal:
                normal = np.array([0.0, 0.0, -1.0])
                if self.rectangle:
                    normal = np.array([0.0, 0.0, -1.0])

                if i > 2:
                    normal *= -1

                glNormal3fv(normal)
            # glNormal3fv(vertex + np.array([0, 0, 1 if i > 2 else -1]))
            glVertex3fv(vertex)
        glEnd()

        glBegin(GL_QUADS)
        for i in range(0, len(self.face_idces), 4):
            normal = self.normal_vectors[i//4]
        
            for j in range(4):
                vertex = self.face_vertices[i+j]
                glNormal3fv(normal + vertex)
                glVertex3fv(vertex)
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
        
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glMaterial(GL_FRONT, GL_SPECULAR, (.1, .1, .1, 1))
        glMaterial(GL_FRONT, GL_EMISSION, (0, 0, 0, 1))
        glColor3fv(self.color)
        
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, 0.0)

        for i in range(self.segments + 1):
            theta = (2.0 * np.pi * i) / self.segments
            x = self.radius * np.cos(theta)
            y = self.radius * np.sin(theta)
            glNormal3f(x, y, 1.0)
            glVertex3f(x, y, 0.0)


        glEnd()
        glPopMatrix()