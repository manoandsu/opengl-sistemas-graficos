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
        self.isosceles = isosceles
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
        #print(self.face_vertices , '--------------------------------------------------')
        # Propriedades de iluminação
        self.light_position = [-5.5, -5.75, 10, 1.0]
        self.ambient_color = [253/255, 184/255, 19/255, 1.0]
        self.diffuse_color = [1.0, 1.0, 1.0, 1.0]
        self.specular_color = [1.0, 1.0, 1.0, 1.0]
        self.shininess = 50.0


    def calculate_face_normal(self, face_index):
        v1 = self.face_vertices[face_index]
        v2 = self.face_vertices[face_index + 1]
        v3 = self.face_vertices[face_index + 2]

        edge1 = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
        edge2 = (v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2])

        normal = (
            edge1[1] * edge2[2] - edge1[2] * edge2[1],
            edge1[2] * edge2[0] - edge1[0] * edge2[2],
            edge1[0] * edge2[1] - edge1[1] * edge2[0]
        )

        length = (normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2) ** 0.5
        return (normal[0] / length, normal[1] / length, normal[2] / length)

    def calculate_quad_normal_avg(self, quad_index):
        normal_sum = [0.0, 0.0, 0.0]
        for j in range(4):
            normal = self.calculate_face_normal((quad_index + j) // 2)
            normal_sum[0] += normal[0]
            normal_sum[1] += normal[1]
            normal_sum[2] += normal[2]

        return (
            normal_sum[0] / 4,
            normal_sum[1] / 4,
            normal_sum[2] / 4
        )

    def draw(self):
        glPushMatrix()
        
        self._apply_transforms()
        glEnable(GL_NORMALIZE)  # Normaliza as normais automaticamente
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # Configurações de iluminação
        glLightfv(GL_LIGHT0, GL_POSITION, self.light_position)
        glLightfv(GL_LIGHT0, GL_AMBIENT, self.ambient_color)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.diffuse_color)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.specular_color)

        # Configuração do material
        # glMaterialfv(GL_FRONT, GL_AMBIENT, self.color + (1.0,))
        # glMaterialfv(GL_FRONT, GL_DIFFUSE, self.color + (1.0,))
        # glMaterialfv(GL_FRONT, GL_SPECULAR, self.specular_color)
        # glMaterialf(GL_FRONT, GL_SHININESS, self.shininess)

        glBegin(GL_TRIANGLES)
        glColor3f(*self.color)
        for vertex in self.triangle_vertices:
            if self.isosceles:
                if self.triangle_vertices.index(vertex) > 2:
                    glNormal3f(-1.0, 0.0, 0.0)
                else:
                    glNormal3f(1.0, 0.0, 0.0)
            else:
                if self.triangle_vertices.index(vertex) > 2:
                    glNormal3f(0.0, 0.0, 1.0)
                else:
                    glNormal3f(0.0, 0.0, -1.0)

            glVertex3f(*vertex)
        glEnd()

        glBegin(GL_QUADS)
        for i in range(0, len(self.face_idces), 4):
            glColor3f(*self.color)
            normal_avg = self.calculate_quad_normal_avg(i)
            #print(normal_avg, "---------------------------------")
            glNormal3f(*normal_avg)
            for j in range(4):
                glVertex3f(*self.face_vertices[i + j])
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