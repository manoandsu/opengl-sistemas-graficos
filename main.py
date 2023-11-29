from OpenGL.GL import *
from OpenGL.GLUT import *

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(500, 500)   # Set the w and h of your window
    glutCreateWindow("My OpenGL Window")
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutMainLoop()

def draw_square():
    # We have to declare the points in this sequence: bottom left, bottom right, top right, top left
    glBegin(GL_QUADS) # Begin the sketch
    glColor3f(0, 0, 0.2)
    glVertex2f(-0.75, -0.75) # Coordinates for the bottom left point
    glVertex2f(1, -1) # Coordinates for the bottom right point
    glVertex2f(1, 1) # Coordinates for the top right point
    glVertex2f(-1, 1) # Coordinates for the top left point
    glEnd() # Mark the end of drawing

def draw_triangle():
    glBegin(GL_TRIANGLES)
    glColor3f(1, 0, 0)  # Red
    glVertex2f(.5, .5)
    glColor3f(0, 1, 0)  # Green
    glVertex2f(-1, -1)
    glColor3f(0, 0, 1)  # Blue
    glVertex2f(1, -1)
    glEnd()

def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_square()
    # draw_triangle()
    glutSwapBuffers()

if __name__ == "__main__":
    main()

    
