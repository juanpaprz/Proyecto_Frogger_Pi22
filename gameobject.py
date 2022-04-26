
import re


class GameObject:
    """Clase para objectos como Mario y Goomba"""
    #__position = {'x': 0, 'y': 0}
    #__last_position = {'x': 0, 'y': 0}
    #__size = {'x': 0, 'y': 0}
    #animator = [] #Lista bidimensional con los Frames del objeto
    #__index_state = 0 #Indice del estado del personaje a animar
    #__latest_frame = 0 #Indice del frame a dibujar
    #__mirror = False #mirror es False cuando voltea hacia la derecha
    #__velocity = {'x': 0, 'y': 0}
    #__MAX_VELOCITY = 10
    
    def __init__(self, id_element=0,x=0, y=0, w=0, h=0, frames = []):
        self.__position = {'x': 0, 'y': 0}
        self.__last_position = {'x': 0, 'y': 0}
        self.__size = {'x': 0, 'y': 0}
        self.animator = [] #Lista bidimensional con los Frames del objeto
        self.__index_state = 0 #Indice del estado del personaje a animar
        self.__latest_frame = 0 #Indice del frame a dibujar
        self.__mirror = False #mirror es False cuando voltea hacia la derecha
        self.__backwards = False
        self.__turn = False
        self.__velocity = {'x': 0, 'y': 0}
        self.__MAX_VELOCITY = 10
        self.__jumping = False
        self.__initialPosX = 190
        self.__initialPosY = 0
        
        self.__id_element = id_element
        self.__position['x'] = x
        self.__position['y'] = y
        self.__last_position['x'] = x
        self.__last_position['y'] = y
        self.__size['x'] = w
        self.__size['y'] = h
        self.animator = frames

    def static_move_left(self):
        self.__velocity['x'] = -1
        self.__position['x'] += self.__velocity['x']

    def static_move(self):
        self.__velocity['x'] = 1
        self.__position['x'] += self.__velocity['x']


        

    def respawn(self):
        self.__position['y'] = self.__initialPosY
        self.__position['x'] = self.__initialPosX
        self.change_state(0)


    def move(self, input, scr_w, scr_h):
        if input['y'] == 1:
            self.__position['y'] += 50
        elif input['y'] == -1:
            self.__position['y'] -= 50
        if input['x'] == 1:
            self.__position['x'] += 50
        elif input['x'] == -1:
            self.__position['x'] -= 50
        
        #Ver si colisiona con la pantalla
        if self.__position['x'] + self.__size['x'] > scr_w:
            self.__position['x'] = scr_w - self.__size['x']
            self.__velocity['x'] *= 0
            return True
        if self.__position['x']  < 0:
            self.__position['x'] = 0
            self.__velocity['x'] *= 0
            return True
        if self.__position['y'] + self.__size['y'] > scr_h:
            self.__position['y'] = scr_h - self.__size['y']
            self.__velocity['y'] *= 0
        if self.__position['y']  < 0:
            self.__position['y'] = 0
            self.__velocity['y'] *= 0
       

    def is_collision(self,obj):
        if not isinstance(obj, GameObject):
            raise Exception('La función requiere un GameObject')
        col_x = self.__position['x'] < obj.__position['x'] + obj.__size['x'] and self.__position['x'] + self.__size['x'] > obj.__position['x']
        col_y = self.__position['y'] < obj.__position['y'] + obj.__size['y'] and self.__position['y'] + self.__size['y'] > obj.__position['y']
        return col_x and col_y
    
    def is_collision_trunk(self,obj):
        if not isinstance(obj, GameObject):
            raise Exception('La función requiere un GameObject')
        col_x = self.__position['x'] + self.__size['x'] < obj.__position['x'] + obj.__size['x'] and self.__position['x'] > obj.__position['x']
        col_y = self.__position['y'] < obj.__position['y'] + obj.__size['y'] and self.__position['y'] + self.__size['y'] > obj.__position['y']
        return col_x and col_y

    def is_collision_crocodille(self,obj):
        if not isinstance(obj, GameObject):
            raise Exception('La función requiere un GameObject')
        col_x = self.__position['x'] + self.__size['x'] < obj.__position['x'] + obj.__size['x'] and self.__position['x'] > obj.__position['x'] + (obj.__size['x']/4)
        col_y = self.__position['y'] < obj.__position['y'] + obj.__size['y'] and self.__position['y'] + self.__size['y'] > obj.__position['y']
        return col_x and col_y

    def change_state(self, index):
        if index >= len(self.animator):
            raise Exception('El índice está fuera del límite permitido.')
        self.__index_state = index
        self.__latest_frame = 0
    
    def get_state(self):
        return self.__index_state

    def animate(self):
        if len(self.animator[self.__index_state]) == 1:
            return
        self.__latest_frame = 0 if self.__latest_frame >= (len(self.animator[self.__index_state]) - 1) else self.__latest_frame + 1

    def get_frame_to_draw(self):
        return self.animator[self.__index_state][self.__latest_frame]
    
    def get_position(self):
        return self.__position['x'], self.__position['y']

    def set_position(self, pos):
        self.__position = pos
    
    def get_size(self):
        return self.__size['x'], self.__size['y']

    def set_mirror(self, value):
        self.__mirror = value

    def is_mirrored(self):
        return self.__mirror

    def set_backwards(self, value):
        self.__backwards = value

    def is_backwards(self):
        return self.__backwards

    def set_turn(self, value):
        self.__turn = value

    def is_turn(self):
        return self.__turn
    
    def get_id(self):
        return self.__id_element
    
    def get_velocity(self):
        return self.__velocity

    def is_jumping(self):
        return self.__jumping
        

