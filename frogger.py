from re import I
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from textures import loadTexture
from gameobject import GameObject
import random
from playsound import playsound
from threading import Thread

cars = []
car_texture = []

trunks = []
trunk_texture = []

crocodilles = []
crocodille_texture = []

frog_gameobject = GameObject()
frog_texture = []
FROG_IDLE = 0
FROG_JUMP = 1

background_texture = []

counter_elements = 0

width = 420
height = 500
x = 0
y = 0

flag_left = False
flag_right = False
flag_up = False
flag_down = False
flag_water = False

#Función musica de fondo
def play_background():
    playsound("Resources/ozuna.wav")

def draw_background():
    global width, height, x, y
    glBindTexture(GL_TEXTURE_2D, background_texture[0])
    glBegin(GL_POLYGON)
    glTexCoord2f(0,0)
    glVertex2d(x,y)
    glTexCoord2f(1,0)
    glVertex2d(x + width,y)
    glTexCoord2f(1,1)
    glVertex2d(x + width,y + height)
    glTexCoord2f(0,1)
    glVertex2d(x,y + height)
    glEnd()

def draw_frog():
    global frog_gameobject
    x,y = frog_gameobject.get_position()
    w,h = frog_gameobject.get_size()
    #Verificar si la rana avanza hacia adelante o a un lado
    if frog_gameobject.is_turn():
        pin_y_start, pin_y_end = (0,1) if frog_gameobject.is_mirrored() else (1,0)
        glBindTexture(GL_TEXTURE_2D, frog_gameobject.get_frame_to_draw())
        glBegin(GL_POLYGON)
        glTexCoord2f(0,pin_y_start)
        glVertex2d(x,y)
        glTexCoord2f(0,pin_y_end)
        glVertex2d(x+w,y)
        glTexCoord2f(1,pin_y_end)
        glVertex2d(x+w,y+h)
        glTexCoord2f(1,pin_y_start)
        glVertex2d(x,y+h)
        glEnd()
    else:
        pin_y_start, pin_y_end = (1,0) if frog_gameobject.is_backwards() else (0,1)
        glBindTexture(GL_TEXTURE_2D, frog_gameobject.get_frame_to_draw())
        glBegin(GL_POLYGON)
        glTexCoord2f(0,pin_y_start)
        glVertex2d(x,y)
        glTexCoord2f(1,pin_y_start)
        glVertex2d(x+w,y)
        glTexCoord2f(1,pin_y_end)
        glVertex2d(x+w,y+h)
        glTexCoord2f(0,pin_y_end)
        glVertex2d(x,y+h)
        glEnd()
    
def draw_cars():
    global cars
    for i in range(len(cars)):
        car_gameobject = cars[i]
        x,y = car_gameobject.get_position()
        w,h = car_gameobject.get_size()
        pin_x_start, pin_x_end = (0,1)
        glBindTexture(GL_TEXTURE_2D, car_gameobject.get_frame_to_draw())
        glBegin(GL_POLYGON)
        glTexCoord2f(pin_x_start,0)
        glVertex2d(x,y)
        glTexCoord2f(pin_x_end,0)
        glVertex2d(x+w,y)
        glTexCoord2f(pin_x_end,1)
        glVertex2d(x+w,y+h)
        glTexCoord2f(pin_x_start,1)
        glVertex2d(x,y+h)
        glEnd()

def draw_trunks():
    global trunks
    for i in range(len(trunks)):
        trunk_gameobject = trunks[i]
        x,y = trunk_gameobject.get_position()
        w,h = trunk_gameobject.get_size()
        pin_x_start, pin_x_end = (0,1)
        glBindTexture(GL_TEXTURE_2D, trunk_gameobject.get_frame_to_draw())
        glBegin(GL_POLYGON)
        glTexCoord2f(pin_x_start,0)
        glVertex2d(x,y)
        glTexCoord2f(pin_x_end,0)
        glVertex2d(x+w,y)
        glTexCoord2f(pin_x_end,1)
        glVertex2d(x+w,y+h)
        glTexCoord2f(pin_x_start,1)
        glVertex2d(x,y+h)
        glEnd()

def draw_crocodilles():
    global crocodilles
    for i in range(len(crocodilles)):
        crocodille_gameobject = crocodilles[i]
        x,y = crocodille_gameobject.get_position()
        w,h = crocodille_gameobject.get_size()
        pin_x_start, pin_x_end = (1,0)
        glBindTexture(GL_TEXTURE_2D, crocodille_gameobject.get_frame_to_draw())
        glBegin(GL_POLYGON)
        glTexCoord2f(pin_x_start,0)
        glVertex2d(x,y)
        glTexCoord2f(pin_x_end,0)
        glVertex2d(x+w,y)
        glTexCoord2f(pin_x_end,1)
        glVertex2d(x+w,y+h)
        glTexCoord2f(pin_x_start,1)
        glVertex2d(x,y+h)
        glEnd()


def keyPressed ( key, x, y):
    global flag_left, flag_right, flag_up, flag_down, flag_water
    if key == b'\x1b':
        glutLeaveMainLoop()
    if key == b'w':
        flag_up = True
        flag_water = True
    if key == b's':
        flag_down = True
        flag_water = True
    if key == b'a':
        flag_left = True
        flag_water = True
    if key == b'd':
        flag_right = True
        flag_water = True

def check_collisions():
    global cars, frog_gameobject, trunks, width, flag_water, crocodilles
    pos_x, pos_y = frog_gameobject.get_position()
    for i in range(len(cars)):
        if frog_gameobject.is_collision(cars[i]):
            frog_gameobject.respawn()
    if(pos_y == 200 or pos_y == 300):
        for i in range(len(trunks)):
            if frog_gameobject.is_collision_trunk(trunks[i]):
                frog_gameobject.static_move()
                flag_water = False
        if(flag_water):
            frog_gameobject.respawn()
    if(pos_y == 250):
        for i in range(len(crocodilles)):
            if frog_gameobject.is_collision_crocodille(crocodilles[i]):
                frog_gameobject.static_move_left()
                flag_water = False
        if(flag_water):
            frog_gameobject.respawn()
    if(pos_y > 450):
        frog_gameobject.respawn()
                
def init():
    glClearColor ( 0.5725, 0.5647, 1.0, 0.0 )
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def reshape(width, height):
    global w, h
    glViewport ( 0, 0, width, height )
    glMatrixMode ( GL_PROJECTION )
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    w = width
    h = height
    glMatrixMode ( GL_MODELVIEW )
    glLoadIdentity()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    draw_background()
    draw_trunks()
    draw_crocodilles()
    draw_frog()
    draw_cars()
    
    glutSwapBuffers()

def timer_move_frog(value):
    global frog_gameobject, flag_left, flag_right, flag_up, flag_down, width, height, flag_water
    global FROG_IDLE, FROG_JUMP
    state = frog_gameobject.get_state()
    input = {'x': 0, 'y': 0}
    if flag_up:
        flag_up = False
        input['y'] = 1
    if flag_down:
        flag_down = False
        input['y'] = -1
    if flag_right:
        flag_right = False
        input['x'] = 1
    elif flag_left:
        flag_left = False
        input['x'] = -1
    if(frog_gameobject.move(input, width, height)):
        flag_water = True

    if input['y'] == 1:
        if state != FROG_JUMP:
            frog_gameobject.change_state(FROG_JUMP)
        if frog_gameobject.is_backwards():
            frog_gameobject.set_backwards(False)
        if frog_gameobject.is_turn():
            frog_gameobject.set_turn(False)
    elif input['y'] == -1:
        if state != FROG_JUMP:
            frog_gameobject.change_state(FROG_JUMP)
        if not frog_gameobject.is_backwards():
            frog_gameobject.set_backwards(True)
        if frog_gameobject.is_turn():
            frog_gameobject.set_turn(False)
    else: 
        if state == FROG_JUMP:
            frog_gameobject.change_state(FROG_IDLE)
    if input['x'] == -1:
        if state != FROG_JUMP:
            frog_gameobject.change_state(FROG_JUMP)
        if frog_gameobject.is_mirrored():
            frog_gameobject.set_mirror(False)
        if not frog_gameobject.is_turn():
            frog_gameobject.set_turn(True)
    elif input['x'] == 1:
        if state != FROG_JUMP:
            frog_gameobject.change_state(FROG_JUMP)
        if not frog_gameobject.is_mirrored():
            frog_gameobject.set_mirror(True)
        if not frog_gameobject.is_turn():
            frog_gameobject.set_turn(True)
    else:
        if state == FROG_JUMP:
            frog_gameobject.change_state(FROG_IDLE)

    check_collisions()
    glutPostRedisplay()
    glutTimerFunc(10, timer_move_frog, 1)

def timer_animate_frog(value):
    global frog_gameobject
    frog_gameobject.animate()
    glutPostRedisplay()
    glutTimerFunc(200, timer_animate_frog,1)

def timer_move_car(id_car):
    global cars, width
    for i in range(len(cars)):
        if cars[i].get_id() == id_car:
            cars[i].static_move()
            if(car_out()):
                break
            glutPostRedisplay()
            glutTimerFunc(10, timer_move_car, id_car)
            
            
def car_out():
    global cars, width
    is_out = False
    for i in range(len(cars)):
        x,y = cars[i].get_position()
        if x == width+40:
            cars.pop(i)
            is_out = True
            break
    return is_out

def timer_animate_car(id_car):
    global cars
    for i in range(len(cars)):
        if cars[i].get_id() == id_car:
            cars[i].animate()
            glutPostRedisplay()
            glutTimerFunc(200, timer_animate_car, id_car)

def timer_create_car(value):
    global cars, car_texture, counter_elements
    id_car = counter_elements

    random_y = random.choice([55,105,405])

    car = GameObject(id_car,-40,random_y,40,40, car_texture)
    counter_elements += 1
    cars.append(car)
    #glutPostRedisplay()
    timer_animate_car(id_car)
    timer_move_car(id_car)
    glutTimerFunc(random.randint(500,1000), timer_create_car, 1)

def timer_move_trunk(id_trunk):
    global trunks, width
    for i in range(len(trunks)):
        if trunks[i].get_id() == id_trunk:
            trunks[i].static_move()
            if(trunk_out()):
                break
            glutPostRedisplay()
            glutTimerFunc(10, timer_move_trunk, id_trunk)
            
            
def trunk_out():
    global trunks, width
    is_out = False
    for i in range(len(trunks)):
        pos_x,pos_y = trunks[i].get_position()
        if  pos_x == width+80:
            trunks.pop(i)
            is_out = True
            break
    return is_out

def timer_animate_trunk(id_trunk):
    global trunks
    for i in range(len(trunks)):
        if trunks[i].get_id() == id_trunk:
            trunks[i].animate()
            glutPostRedisplay()
            glutTimerFunc(200, timer_animate_trunk, id_trunk)

def timer_create_trunk(value):
    global trunks, trunk_texture, counter_elements
    id_trunk = counter_elements

    random_y = random.choice([200,300])

    trunk = GameObject(id_trunk,-80,random_y,100,40, trunk_texture)
    counter_elements += 1
    trunks.append(trunk)
    #glutPostRedisplay()
    timer_animate_trunk(id_trunk)
    timer_move_trunk(id_trunk)
    glutTimerFunc(random.randint(1000,3000), timer_create_trunk, 1)

def timer_move_crocodille(id_crocodille):
    global crocodilles, width
    for i in range(len(crocodilles)):
        if crocodilles[i].get_id() == id_crocodille:
            crocodilles[i].static_move_left()
            if(crocodille_out()):
                break
            glutPostRedisplay()
            glutTimerFunc(10, timer_move_crocodille, id_crocodille)
            
            
def crocodille_out():
    global crocodilles, width,x
    is_out = False
    for i in range(len(crocodilles)):
        pos_x,pos_y = crocodilles[i].get_position()
        if pos_x == x-160:
            crocodilles.pop(i)
            is_out = True
            break
    return is_out

def timer_animate_crocodille(id_crocodille):
    global crocodilles
    for i in range(len(crocodilles)):
        if crocodilles[i].get_id() == id_crocodille:
            crocodilles[i].animate()
            glutPostRedisplay()
            glutTimerFunc(200, timer_animate_crocodille, id_crocodille)

def timer_create_crocodille(value):
    global crocodilles, crocodille_texture, counter_elements
    id_crocodille = counter_elements

    trunk = GameObject(id_crocodille,500,255,160,40, crocodille_texture)
    counter_elements += 1
    crocodilles.append(trunk)
    #glutPostRedisplay()
    timer_animate_crocodille(id_crocodille)
    timer_move_crocodille(id_crocodille)
    glutTimerFunc(random.randint(2000,3000), timer_create_crocodille, 1)
    

def main():
    global frog_texture, frog_gameobject, counter_elements
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(x, y)
    glutCreateWindow("Frogger")
    glutDisplayFunc(display)
    glutReshapeFunc ( reshape )
    glutKeyboardFunc( keyPressed )
    init()

    thread_stomp = Thread(target=play_background)
    thread_stomp.start()

    background_texture.append(loadTexture('Resources/background.png'))
    frog_texture.append([loadTexture("Resources/frog.png")])
    frog_texture.append([loadTexture("Resources/frogJump.png")])
    frog_gameobject = GameObject(counter_elements,190,0,40,40,frog_texture)
    counter_elements += 1

    car_texture.append([loadTexture('Resources/car1.png')])
    trunk_texture.append([loadTexture('Resources/wood.png')])
    crocodille_texture.append([loadTexture('Resources/crocodille.png'),loadTexture('Resources/crocodille2.png')])

    timer_move_frog(0)
    timer_animate_frog(0)
    timer_create_car(0)
    timer_create_trunk(0)
    timer_create_crocodille(0)

    glutMainLoop()

main()