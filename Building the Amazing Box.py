from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random
import time

W_Width,W_Height=500,500
dotList=[]
ball_size=5
new=False

blink=False
spacebar="no"
speed=0.1

class Point:
    def __init__(self):
        self.x=0
        self.y=0
        self.z=0

def cross_product(a,b):
    cp=Point()
    cp.x=a.y*b.z-a.z*b.y
    cp.y=a.z*b.x-a.x*b.z
    cp.z=a.x*b.y-a.y*b.x
    return cp

def convert_coordinate(x,y):
    global W_Width,W_Height
    a=x-(W_Width/2)
    b=(W_Height/2)-y
    return a,b

def draw_points(x,y,size):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x,y)

def keyboard_listener(key,x,y):
    global spacebar
    if key==b' ':
      if spacebar=="yes":
          spacebar="no"
          print("Start")
      else:
          spacebar="yes"
          print("Stop")
    glutPostRedisplay()

def special_key_listener(key,x,y):
    global speed,spacebar
    if spacebar=="no":
        if key==GLUT_KEY_UP:
            speed+=0.01
            print(f"Speed Increased:{speed:.2f}")
        if key==GLUT_KEY_DOWN and speed > 0:
            speed-=0.01
            print(f"Speed Decreased:{speed:.2f}")
        glutPostRedisplay()

def mouse_listener(button,state,x,y):
    global new,blink,spacebar
    if spacebar=="no":
        if(button==GLUT_LEFT_BUTTON and state==GLUT_DOWN):
            blink=True
        if(button==GLUT_RIGHT_BUTTON and state==GLUT_DOWN):
            new=convert_coordinate(x, y)
            add_value=0
            new1=new+(add_value,)
            dotList.append(new1)
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    if dotList:
        global blink
        for i in range(len(dotList)):
            if len(dotList[i])==3:
                c1,c2,c3=dotList[i]
            else:
                c1,c2,c3,rgb=dotList[i]
            glPointSize(ball_size)
            glBegin(GL_POINTS)
            if c3==0:
                r,g,b=random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)
                glColor3f(r,g,b)
                dotList[i]=(c1,c2,1,(r,g,b))
            else:
                glColor3f(*rgb)
            glVertex2f(c1,c2)
            glEnd()
    glutSwapBuffers()

def animate():
    glutPostRedisplay()
    global dotList,speed,blink,spacebar
    if spacebar=="no":
        for i in range(len(dotList)):
            if not blink:
                c1,c2,c3,rgb=dotList[i]
                dx,dy=random.uniform(-1,1)*speed,random.uniform(-1,1)*speed
                c1+=dx
                c2+=dy
                c1=max(-250,min(c1,250))
                c2=max(-250,min(c2,250))
                dotList[i]=(c1,c2,c3,rgb)
            else:
                glClearColor(0.0, 0.0, 0.0, 1.0)
                glClear(GL_COLOR_BUFFER_BIT)
                glutSwapBuffers()
                spacebar="yes"
                time.sleep(1)
                spacebar="no"
                blink=False

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Building the Amazing Box")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboard_listener)
glutSpecialFunc(special_key_listener)
glutMouseFunc(mouse_listener)
glutMainLoop()
