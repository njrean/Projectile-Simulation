import pygame as py
from pygame import Vector2 as V2
import math
from os import path
import csv

ob_resource = 'object/'
input_font = 'otherfile/BAHNSCHRIFT.ttf'
list_resutout = ['distance(m)', 'angle(degree)', 'spring displacement(m)', 'initial y-axis(m)',
                'highest y-axis(m)', 'farthest x-axis(m)', 'time at highest-point(s)', 'time at farthest-point(s)',
                'time at basket(s)', 'initial velocity(m/s)', 'collided velocity(m/s)', 'spring constant(N/m)',
                'mass of ball(kg)', 'mass of collided part(kg)']
file_info = 'otherfile/info.txt'

def multilineRender(screen, name, x,y, font, colour=(128,128,128), justification="left"):
    f = open(name, 'r')
    text = f.readlines()
    text = '\n'.join(text)
    f.close()
    text = text.strip().replace('\r','').split('\n')
    justification = justification[0].upper()
    max_width = 0
    text_bitmaps = []
    font = py.font.Font(font, 12)
    # Convert all the text into bitmaps, calculate the justification width
    for t in text:
        text_bitmap = font.render(t, True, colour)
        text_width  = text_bitmap.get_width()
        text_bitmaps.append((text_width, text_bitmap))
        if (max_width < text_width): max_width = text_width
    # Paint all the text bitmaps to the screen with justification
    for (width, bitmap) in text_bitmaps:
        xpos = x
        width_diff = max_width - width
        if (justification == 'R'):  # right-justify
            xpos = x + width_diff
        elif (justification == 'C'): # centre-justify
            xpos = x + (width_diff // 2)
        screen.blit(bitmap, (xpos, y) )
        y += bitmap.get_height()

def savefile_append_row(name, header, data):
    lines = 0
    file_name = name
    if path.isfile(file_name):
        file = open(file_name)
        for l in file:
            if not l.strip():
                lines += 1
        file.close()

    with open(file_name, 'a+', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(str(lines+1))
        writer.writerow(header)
        for d in data:
            writer.writerow(d)
        writer.writerow('')
    f.close()

class Button:
    def __init__(self, name, x, y, screen_pos = (0,0)):
        self.positon = (x, y)
        self.button = py.image.load(ob_resource + name+'.png')
        self.selected = py.image.load(ob_resource + name+'.2.png')
        self.ob = self.button.get_rect(topleft=(x+screen_pos[0],y+screen_pos[1])) #for get postion
        self.state = False
    def blit(self, screen, check):
        if check or self.state: screen.blit(self.selected, self.positon)
        else: screen.blit(self.button, self.positon)
    def mouse_detect(self):
        self.state = True if self.ob.collidepoint(py.mouse.get_pos()) else False
    def mouse_click(self, event):
        if self.ob.collidepoint(event.pos): return True

class Textbox:
    def __init__(self, x, y, w, h, font, fsize, fcolor, text ='', screen_pos=(0,0)):
        self.rec = py.Rect(x, y, w, h)
        self.rec2 = py.Rect(x+screen_pos[0], y+screen_pos[1], w, h)
        self.font = py.font.Font(font, fsize)
        self.pos = (x, y)
        self.fcolor = fcolor
        self.fcolor_de = fcolor
        self.text = text
        self.text_sur = self.font.render(self.text, True, self.fcolor)
        self.active = False
    def draw(self, screen, color=None):
        self.text_sur = self.font.render(self.text, True, self.fcolor)
        py.draw.rect(screen, color or self.fcolor, self.rec, 1, border_radius=10)
        screen.blit(self.text_sur, self.text_sur.get_rect(center = self.rec.center))
    def display(self, screen, textcolor = (81, 81, 81), boxcolor = 'white', bordercolor = (112, 112, 112), border=3):
        self.text_sur = self.font.render(self.text, True, textcolor)
        py.draw.rect(screen, boxcolor, self.rec, 0, border_radius=border)
        py.draw.rect(screen, bordercolor, self.rec, 1, border_radius=border)
        screen.blit(self.text_sur, self.text_sur.get_rect(center = self.rec.center))
        
class Intxt(Textbox):
    def __init__(self, x, y, w, h, font, fsize, fcolor, text, screen_pos, allow=True, general_active=True):
        super().__init__(x, y, w, h, font, fsize, fcolor, text, screen_pos)
        self.allow = allow
        self.general_active = general_active
    def check_event(self, event):
        if self.allow:
            if event.type == py.MOUSEBUTTONDOWN:
                if self.rec2.collidepoint(event.pos):
                    self.active = True
                else: self.active = False
                if self.active:
                    self.fcolor = (117, 110, 222)
                else: self.fcolor = self.fcolor_de
            if event.type == py.KEYDOWN:
                if self.active:
                    if event.key == py.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif self.general_active:
                        self.text += event.unicode
                    elif (event.unicode.isnumeric() or event.unicode == ".") and len(self.text) < 9:
                        self.text += event.unicode

class Optionbox(Textbox):
    def __init__(self, x, y, w, h, font, fsize, fcolor, text, option_list , unit_list, selection = 0, screen_pos = (0,0)):
        super().__init__(x, y, w, h, font, fsize, fcolor, text, screen_pos=screen_pos)
        self.option_list = option_list
        self.unit_list = unit_list
        self.selected = selection
        self.start_draw = False
        self.option_active = -1
    def display_option(self, screen):
        py.draw.rect(screen, (255, 211, 69) if self.active and not self.start_draw else (212, 211, 233), self.rec)
        text = self.font.render(self.option_list[self.selected], 1, (81, 81, 81))
        screen.blit(text, text.get_rect(center = self.rec.center))
        if self.start_draw and len(self.option_list) != 0:
            for i, txt in enumerate(self.option_list):
                new_rec = self.rec.copy()
                new_rec.x += self.rec.width * (i+1)
                text = self.font.render(txt, 1, self.fcolor)
                if i == len(self.option_list)-1 :
                    py.draw.rect(screen, (255, 211, 69) if i == self.option_active else (212, 211, 233), new_rec, border_top_right_radius=3, border_bottom_right_radius=3)
                else: py.draw.rect(screen, (255, 211, 69) if i == self.option_active else (212, 211, 233), new_rec)
                screen.blit(text, text.get_rect(center = new_rec.center))
    def update(self, event):
        self.active = self.rec2.collidepoint(py.mouse.get_pos()) and not (len(self.option_list) == 1)
        for i in range(len(self.option_list)):
            new_rec = self.rec2.copy()
            new_rec.x += self.rec2.width * (i+1)
            if new_rec.collidepoint(py.mouse.get_pos()):
                self.option_active = i
                break
        if not self.active and self.option_active == -1:
            self.start_draw = False
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
            if self.active:
                self.start_draw = not self.start_draw
            elif self.start_draw and self.option_active >= 0:
                self.selected = self.option_active
                self.start_draw = False

class Window:
    def __init__(self,x, y, w, h, screen_on):
        self.surf = py.Surface((w, h), py.SRCALPHA)
        self.pos = (x, y)
        self.screen_on = screen_on
        self.list_button = []
        self.list_textbox = []
        self.list_intxt = []
        self.list_optionbox = []
    def display(self):
        for textbox in self.list_textbox: textbox.display(self.surf)
        for intxt in self.list_intxt: intxt.draw(self.surf)
        for optionbox in self.list_optionbox: optionbox.display_option(self.surf)
        self.screen_on.blit(self.surf, self.pos)
    def __all_update(self, event):
        for button in self.list_button: button.mouse_detect()
        for intxt in self.list_intxt: intxt.check_event(event)
        for optionbox in self.list_optionbox: optionbox.update(event)
        
class Cannon:
    def __init__(self):
        self.arm_cannon = py.image.load(ob_resource+'arm_cannon.png')
        self.base_cannon = py.image.load(ob_resource+'base_cannon.png')
        self.angle = 0
    def cannon_status(self, angle):
        return True if self.angle == angle else False
    def rotatepivoted(self, angle):
        image = py.transform.rotate(self.arm_cannon, angle)
        rect = image.get_rect()
        rect.center = (391, 299)
        return image, rect
    def draw(self, surface, angle):
        if angle != self.angle:
            self.angle = self.angle + 1 if angle>self.angle else self.angle - 1
        (image, rect) = self.rotatepivoted(self.angle)
        surface.surf.blit(image, (rect.x-surface.pos[0],rect.y-surface.pos[1]))
        surface.surf.blit(self.base_cannon, (349-surface.pos[0], 284-surface.pos[1]))

class Ball:
    def __init__(self, x=0, y=0, u=0, angle=0, timestep = 0.01):
        self.a = angle
        self.pos = V2(x, y)
        self.in_pos = V2(x, y)
        self.u = V2(u*math.cos(angle), u*math.sin(angle))
        self.acc = V2(0, -9.81)
        self.time = 0
        self.timestep = timestep
        self.ymax = 0.21+(0.342*math.sin(angle))+(u**2*(math.sin(angle)**2)/(2*9.81))
        self.xmax = u*math.cos(angle)*(u*math.sin(angle)+math.sqrt((u*math.sin(angle))**2+2*9.81*y))/9.81
        self.ratio = min(208/self.ymax, 642/self.xmax)
        self.ball = py.image.load('object//ball.png')
        self.scale_line_x = py.image.load('object//scalex.png')
        self.scale_line_y = py.image.load('object//scaley.png')
        self.basket = py.image.load('object//basket.png').convert_alpha()
        self.basket.set_alpha(190)
        self.list = []
        self.scale()
    def scale(self):
        self.pos_scale = [[[],[]], [[],[]]]
        for x in range(math.ceil(682/(0.5*self.ratio))):
            self.pos_scale[0][0].append(404-335+(0.5*x*self.ratio))
            self.pos_scale[0][1].append(Textbox(404-335+(0.5*self.ratio*x)-7, 683-392, 14, 11, input_font, 11, (99,99,99), str(0.5*x)))
        for y in range(math.ceil(247/(0.5*self.ratio))):
            self.pos_scale[1][0].append(677-392-(0.5*y*self.ratio))
            self.pos_scale[1][1].append(Textbox(380-335, 677-392-(0.5*y*self.ratio)-5.5, 14, 11, input_font, 11, (99,99,99), str(0.5*y)))
    def update(self):
        if self.pos.y-0.02 >= 0:
            self.pos = self.in_pos + (self.u*self.time) + (0.5*self.acc*self.time*self.time)
            self.list.append([self.time, self.pos.x, self.pos.y])
            self.time = self.time+self.timestep
    def blit(self, surfaceball, screen1, distance):
        self.update()
        for i, x in enumerate(self.pos_scale[0][0]):
            screen1.blit(self.scale_line_x, (x, 677-392))
            self.pos_scale[0][1][i].draw(screen1, 'white')
        for i, y in enumerate(self.pos_scale[1][0]):
            screen1.blit(self.scale_line_y, (399-335, y))
            self.pos_scale[1][1][i].draw(screen1, 'white')
        for i in self.list:
            py.draw.circle(screen1, (0, 0, 0), [404-335+(i[1]*self.ratio), 677.5-392-(i[2]*self.ratio)], 2)
        surfaceball.surf.blit(self.ball, [391-6.5-surfaceball.pos[0]+(90.464*math.cos(self.a))+(self.pos.x*257), 299.5-6.5-surfaceball.pos[1]-(90.464*math.sin(self.a))-(self.pos.y*257)+(self.in_pos.y*257)])
        surfaceball.surf.blit(self.basket, [391-29.5-surfaceball.pos[0]+(90.464*math.cos(self.a))+(distance*257), 249.5-surfaceball.pos[1]])

class ValueSet:
    def __init__(self, adjust = 0, distance = 0):
        self.adjust = adjust #angle or spring displacement
        self.d = distance   # distance
        self.s = 0          # spring displacement
        self.a = 0          # angle
        self.u1 = 0         # velocity shoot
        self.u2 = 0         # velocity collide
        self.t = 0          # time at basket
        self.y0 = 0         # height at start point
        self.yt = 0.41      # height of basket
        self.s0 = 0.02      # initial displacement = 2 cm
        self.k = 719.43     # spring constant
        self.m1 = 0.024     # mass of ball
        self.m2 = 0.15455   # mass of collided part
        self.xmax = 0
        self.ymax = 0
        self.shooter = Cannon()
    def set(self, adjust, d):
        self.adjust = adjust
        self.d = d
        self.s,self.a,self.u1,self.u2,self.t,self.y0, self.ymax, self.xmax = 0,0,0,0,0,0,0,0                                   
    def find_angle(self): 
        self.s = self.adjust
        getx = 0
        getval = [0, 0, 0, 0, 0]
        for a in range(450,900, 2):
            a = (a/10)*math.pi/180
            y0 = 0.21+(0.342*math.sin(a))
            t = math.sqrt((self.d*math.tan(a)-self.yt+y0)/(9.81/2))
            u1 = self.d/(math.cos(a)*t)
            u2 = (self.m1+self.m2)*u1/self.m2
            x = ((-self.k*self.s0)+(self.m2*9.81*math.sin(a))+math.sqrt(((self.k*self.s0)-(self.m2*9.81*math.sin(a)))**2+(self.k*self.m2*u2**2)))/self.k
            if x >= self.s:
                if abs(self.s-x) < abs(self.s-getx):
                    getval = [a, y0, t, u1, u2] if getx != 0 else [0,0,0,0,0]
                break
            getx = x
            getval = [a, y0, t, u1, u2]
        self.a,self.y0,self.t,self.u1,self.u2  = getval[0],getval[1],getval[2],getval[3],getval[4]
    def find_displacement(self): #adjust is angle (radius)
        self.a = self.adjust
        self.y0 = 0.21+(0.342*math.sin(self.a))
        self.t = math.sqrt((self.d*math.tan(self.a)-self.yt+self.y0)/(9.81/2))
        self.u1 = self.d/(math.cos(self.a)*self.t)
        self.u2 = (self.m1+self.m2)*self.u1/self.m2
        self.s = ((-self.k*self.s0)+(self.m2*9.81*math.sin(self.a))+math.sqrt(((self.k*self.s0)-(self.m2*9.81*math.sin(self.a)))**2+(self.k*self.m2*self.u2**2)))/self.k
    def add_resualt(self, box_angle, box_displace, box_distance, box_velocity, box_time, box_xmax, box_ymax):
        box_angle.text = '%.2f' %(self.a*180/math.pi) + ' degree' if self.a != 0 else ''
        box_displace.text = '%.2f' %(self.s*100) + ' cm' if self.s != 0 else ''
        box_distance.text = '%.2f' %self.d + ' m' if self.d != 0 else ''
        box_velocity.text = '%.2f' %self.u1 + ' m/s' if self.u1 != 0 else ''
        box_time.text = '%.2f' %self.t + ' s' if self.t != 0 else ''
        box_xmax.text = '%.2f' %self.xmax + ' m' if self.xmax != 0 else ''
        box_ymax.text = '%.2f' %self.ymax + ' m' if self.ymax != 0 else ''
    def calculate(self, check1, adjust, d, box_angle, box_displace, box_distance, box_velocity, box_time, box_xmax, box_ymax):
        self.set(adjust, d)
        if check1: #set angle find displacement
            self.find_displacement()
        else: #set displacement fin anggle
            self.find_angle()
        tymax = self.u1*math.sin(self.a)/9.81
        txmax = ((self.u1*math.sin(self.a))+math.sqrt((self.u1*math.sin(self.a))**2+(2*9.81*self.y0)))/9.81
        self.xmax = self.u1*math.cos(self.a)*txmax
        self.ymax = self.y0+(self.u1*math.sin(self.a)*tymax)-(0.5*9.81*(tymax**2))
        if self.xmax != 0: 
            self.ball = Ball(0, self.y0, self.u1, self.a) 
            self.add_resualt(box_angle, box_displace, box_distance, box_velocity, box_time, box_xmax, box_ymax)

    def get_all_value(self):
        tymax = self.u1*math.sin(self.a)/9.81
        txmax = ((self.u1*math.sin(self.a))+math.sqrt((self.u1*math.sin(self.a))**2+(2*9.81*self.y0)))/9.81
        ymax = self.y0+(self.u1*math.sin(self.a)*tymax)-(0.5*9.81*(tymax**2))
        xmax = self.u1*math.cos(self.a)*txmax
        return [self.d, self.a*180/math.pi, self.s, self.y0, ymax, xmax, tymax, txmax, self.t, self.u1, self.u2, self.k, self.m1, self.m2]

class Game:
    def __init__(self):
        py.init()
        py.display.set_caption("Shooter Simulation") #set top caption of program
        icon = py.image.load(ob_resource +'icon.png')
        py.display.set_icon(icon)
        sc_x, sc_y = 1165, 720 #screen size
        self.screen = py.display.set_mode((sc_x, sc_y))
        self.clock = py.time.Clock() #limit frame rate
        
    def __setting(self):
        self.calculate = ValueSet()
        #!!own surface
        self.main_surf = Window(0, 0, 1165, 720, self.screen)
        self.graph_surf = Window(335, 387, 819, 324, self.screen)
        self.simulate_surf = Window(335, 56, 814, 309, self.screen)
        self.export_surf = Window(257.5, 185, 650, 350, self.screen)
        self.info_surf = Window(257.5, 185, 650, 350, self.screen)

         #!!in main window
        self.screen.fill((217, 217, 222)) #fill color of screen
        self.main_background = py.image.load(ob_resource +'main_background.png')
        #Button
        self.start = Button('start', 116, 352) #Start
        self.reset = Button('reset', 202, 413) #Reset
        self.angle = Button('angle', 42, 124) #Angle
        self.spring = Button('spring', 178, 124) #Spring
        self.export = Button('export', 202, 669) #Export
        self.info = Button('info', 1093, 15)
        #BoxOuput 
        self.out_angle = Textbox(20, 499, 113, 20, input_font, 14, (81, 81, 81))
        self.out_displace = Textbox(177, 499, 113, 20, input_font, 14, (81, 81, 81))
        self.out_distance = Textbox(20, 554, 113, 20, input_font, 14, (81, 81, 81))
        self.out_velocity = Textbox(177, 609, 113, 20, input_font, 14, (81, 81, 81))
        self.out_time = Textbox(20, 664, 113, 20, input_font, 14, (81, 81, 81))
        self.out_xmax = Textbox(177, 554, 113, 20, input_font, 14, (81, 81, 81))
        self.out_ymax = Textbox(20, 609, 113, 20, input_font, 14, (81, 81, 81))
        self.out_warning = Textbox(42, 171, 229, 25, input_font, 14, (81, 81, 81))
        #BoxInput
        self.box_ad = Intxt(44, 205, 126, 36, input_font, 20, (112, 112, 112), "", (0, 0), False, False) #input angle or spring displacement
        self.box_dis = Intxt(145, 253, 126, 36, input_font, 20, (112, 112, 112), "", (0, 0), True, False) #input distance
        self.box_unit1 = Optionbox(145, 300, 46, 27, input_font, 13, (81, 81, 81), '', ['mm', 'cm', 'm'], [10**-3, 10**-2, 1], 2)
        self.box_unit2 = Optionbox(178, 211, 46, 24, input_font, 13, (81, 81, 81), '', ['-'], [1])
        self.main_surf.list_button = [self.start, self.reset, self.angle, self.angle, self.spring, self.export, self.info] 
        self.main_surf.list_textbox = [self.out_angle, self.out_displace, self.out_distance, self.out_velocity, self.out_time, self.out_xmax, self.out_ymax, self.out_warning]
        self.main_surf.list_intxt = [self.box_ad, self.box_dis]
        self.main_surf.list_optionbox = [self.box_unit1, self.box_unit2]

        #!!in graph window & simulate window
        self.graph_background = py.image.load(ob_resource +'graph_background.png')
        self.simulate_background = py.image.load(ob_resource +'simulate_background.png')

        #!!in export window
        self.ex_background = py.image.load(ob_resource +'ex_background.png')
        self.ex_quit = Button('quit', 607, 10, self.export_surf.pos)
        self.ex_graph = Button('ex_graph', 52, 111, self.export_surf.pos)
        self.ex_value = Button('ex_value', 258, 111, self.export_surf.pos)
        self.ex_result = Button('ex_result', 464, 111, self.export_surf.pos)
        self.ex_confirm = Button('ex_confirm', 255, 287, self.export_surf.pos)
        self.file_name = Intxt(161, 217, 268, 36, input_font, 14, (112, 112, 112), '', self.export_surf.pos)
        self.file_type = Optionbox(442, 217, 50, 36, input_font, 14, (81, 81, 81), '', [''], [''], 0, self.export_surf.pos)
        self.export_surf.list_button = [self.ex_quit, self.ex_graph, self.ex_value, self.ex_result, self.ex_confirm]
        self.export_surf.list_intxt = [self.file_name]
        self.export_surf.list_optionbox = [self.file_type]

        #!! in info window
        self.info_background = py.image.load(ob_resource + 'info_background.png') 
        self.info_quit = Button('quit', 607, 10, self.info_surf.pos)
        self.info_surf.list_button = [self.info_quit]
      
    def __render_dp(self, but_check, ex_check):
        #!!main surface
        self.main_surf.surf.blit(self.main_background, (0, 0)) #background
        self.angle.blit(self.main_surf.surf ,but_check[0])
        self.spring.blit(self.main_surf.surf, but_check[1])
        self.start.blit(self.main_surf.surf, False)
        self.reset.blit(self.main_surf.surf, but_check[3])
        self.export.blit(self.main_surf.surf, but_check[2])
        self.info.blit(self.main_surf.surf, but_check[4])
        self.main_surf.display()

        #!!graph surface & simulate surface
        self.graph_surf.surf.blit(self.graph_background, (0, 0)) #Graph background
        self.simulate_surf.surf.blit(self.simulate_background, (0, 0)) #Simulate background
        #!!shooter & ball
        self.calculate.shooter.draw(self.simulate_surf, int(self.calculate.a*180/math.pi))
        if but_check[3] and self.calculate.shooter.cannon_status(int(self.calculate.a*180/math.pi)) and 'ball' in dir(self.calculate):
            self.calculate.ball.blit(self.simulate_surf ,self.graph_surf.surf, self.calculate.d)
        self.graph_surf.display()
        self.simulate_surf.display()

        #!!export suface
        if but_check[2]:
            self.export_surf.surf.blit(self.ex_background, (0,0))
            self.ex_quit.blit(self.export_surf.surf, False)
            self.ex_graph.blit(self.export_surf.surf, ex_check[0])
            self.ex_value.blit(self.export_surf.surf, ex_check[1])
            self.ex_result.blit(self.export_surf.surf, ex_check[2])
            self.ex_confirm.blit(self.export_surf.surf, False)
            self.export_surf.display()
        #!!info surface
        elif but_check[4]:
            self.info_surf.surf.blit(self.info_background, (0,0))
            multilineRender(self.info_surf.surf, file_info, 32, 75, input_font, (81, 81, 81))
            self.info_quit.blit(self.info_surf.surf, False)
            self.info_surf.display()

    def __update(self, event, but_check):
        if but_check[2]:
            self.export_surf._Window__all_update(event)
        elif but_check[4]:
            self.info_surf._Window__all_update(event)
        else: self.main_surf._Window__all_update(event)

    def __run(self):
        running = True
        but_check = [False, False, False, False, False, False] #button angle, spring, export, check simulate, info, start
        ex_check = [False, False, False] #export window graph, value, result
        self.__setting()
       
        while running:
            if but_check[0] or but_check[1]:
                self.box_ad.allow = True
                if but_check[0]:
                    self.out_warning.text = 'Angle 15 to 80 degree' if self.box_unit2.selected == 0 else 'Angle 0.26 to 1.39 radius'
                else: self.out_warning.text = 'Displacement 50 to 130 mm' if self.box_unit2.selected == 0 else 'Displacement 5 to 13 cm'
            else:
                self.box_ad.allow = False
                self.box_ad.text = ''
                self.box_unit2.option_list = ['-']
                self.box_unit2.unit_list = [1]
                self.box_unit2.selected = 0
                self.out_warning.text = 'Select Angle or Displacement'

            for event in py.event.get():
                self.__update(event, but_check)  
                if event.type == py.MOUSEBUTTONDOWN:
                    if self.angle.mouse_click(event) and not but_check[2]: #want to find angle 
                        but_check[0] = not but_check[0]
                        if but_check[0]:
                            but_check[1] = not but_check[0]
                            self.box_unit2.option_list = ['degree', 'radius']
                            self.box_unit2.selected = 0
                            self.box_unit2.unit_list = [math.pi/180, 1]
                            
                    elif self.spring.mouse_click(event) and not but_check[2]: #want to find spring displacement
                        but_check[1] = not but_check[1]
                        if but_check[1]:
                            but_check[0] = not but_check[1]
                            self.box_unit2.option_list = ['mm', 'cm']
                            self.box_unit2.selected = 1
                            self.box_unit2.unit_list = [10**-3, 10**-2]

                    elif self.start.mouse_click(event) and not but_check[2]: #press start simulation
                        but_check[5] = True
                        if 'ball' in dir(self.calculate) : del self.calculate.ball
                        if (but_check[0] or but_check[1]) and self.box_ad.text != '' and self.box_dis.text != '':
                            adjust = float(self.box_ad.text)*self.box_unit2.unit_list[self.box_unit2.selected]
                            d = float(self.box_dis.text)*self.box_unit1.unit_list[self.box_unit1.selected]
                            if but_check[0] and math.pi/12 <= adjust <= 4*math.pi/9 and 1 <= d <= 4:
                                self.calculate.calculate(but_check[0], adjust, d, self.out_angle, self.out_displace, self.out_distance, self.out_velocity, self.out_time, self.out_xmax, self.out_ymax)
                                but_check[3] = True
                            elif but_check[1] and 0.05 <= adjust <= 0.13 and 1 <= d <=  4:
                                self.calculate.calculate(but_check[0], adjust, d, self.out_angle, self.out_displace, self.out_distance, self.out_velocity, self.out_time, self.out_xmax, self.out_ymax)
                                but_check[3] =True
                            
                    elif self.reset.mouse_click(event) and not but_check[2]: #press reset
                        but_check[:3] = [False, False, False]
                        but_check[3] = False
                        self.box_dis.text = ''
                        self.calculate.set(0, 0)
                        if 'ball' in dir(self.calculate): del self.calculate.ball
                        self.calculate.add_resualt(self.out_angle, self.out_displace, self.out_distance, self.out_velocity, self.out_time, self.out_xmax, self.out_ymax)
                        
                    elif self.export.mouse_click(event) and not but_check[2] and self.calculate.a != 0: #press export
                        but_check[2] = True
                    
                    elif self.info.mouse_click(event) and not but_check[2]: #press info
                        but_check[4] = True

                    if self.info_quit.mouse_click(event):
                        but_check[4] = False

                    if self.ex_quit.mouse_click(event):
                        but_check[2],but_check[5], ex_check = False, False, [False, False, False]
                        self.file_type.selected = 0
                        self.file_type.option_list = ['']
                        self.file_name.text = ''

                    elif but_check[2]:
                        if self.ex_graph.mouse_click(event): 
                            ex_check = [True, False, False]
                            self.file_type.option_list = ['.jpg', '.png']
                        elif self.ex_value.mouse_click(event): 
                            ex_check = [False, True, False]
                            self.file_type.option_list = ['.txt', '.csv']
                        elif self.ex_result.mouse_click(event): 
                            ex_check = [False, False, True]
                            self.file_type.option_list = ['.txt', '.csv']
                        elif self.ex_confirm.mouse_click(event) and self.file_name.text != '':
                            if ex_check[0]:
                                py.image.save(self.graph_surf.surf, self.file_name.text+self.file_type.option_list[self.file_type.selected])
                            elif ex_check[1]:
                                list_pair = self.calculate.ball.list
                                savefile_append_row(self.file_name.text+self.file_type.option_list[self.file_type.selected], ['time', 'x', 'y'], list_pair)
                            elif ex_check[2]:
                                list_result = [self.calculate.get_all_value()]
                                savefile_append_row(self.file_name.text+self.file_type.option_list[self.file_type.selected], list_resutout, list_result)
                    
                elif event.type == py.QUIT:
                    py.quit()
                    exit()

            self.__render_dp(but_check, ex_check)

            py.display.update() #update display
            self.clock.tick(60)
