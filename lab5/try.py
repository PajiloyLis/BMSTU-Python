import pygame
import numpy as np
from time import sleep
from math import pi
from constants import *

# Получение даты
def get_text(time):
    months = {1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN",
              7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 0: "DEC"}
    month = months[(START_MONTH + time//500) % 12]
    year = START_YEAR + (START_MONTH + time//500)//12
    return f"{month:s} {year:d}"

# Расстояние между объектами
def get_distance(a, b):
    return np.sqrt(np.sum((a-b)*(a-b)))

# Планеты
class Planet:
    def __init__(self, name, coord, size, rel_period):
        self.coord = coord
        name_text = pygame.font.SysFont("Arial", 14)
        self.name = name_text.render(name, False, "white")
        self.pic = pygame.image.load(name+".png")
        self.pic = pygame.transform.scale(self.pic, (size, size))
        if name == "saturn":
            self.pic = pygame.transform.scale(self.pic, (size/0.5625, size))
        self.turn_matrix = np.array([[np.cos(rel_period*ANGLE), -np.sin(rel_period*ANGLE)],
                                     [np.sin(rel_period*ANGLE), np.cos(rel_period*ANGLE)]])

    def draw(self):
        self.coord = np.matmul(self.coord-GELIOCENTER,
                               self.turn_matrix)+GELIOCENTER
        x, y = self.pic.get_rect().center
        if self.coord[0]+x > 0 and self.coord[1] + y > 0 and self.coord[1]-y < screen.get_size()[1]:
            screen.blit(self.pic, (self.coord[0]-x, self.coord[1]-y))
            screen.blit(self.name, (self.coord[0]+x, self.coord[1]+y))

# Спутник
class Voyager:
    def __init__(self, name, coord, time_start):
        self.coord = coord
        name_text = pygame.font.SysFont("Arial", 14)
        self.r = 5
        self.pic = pygame.draw.circle(screen, "red", self.coord, self.r)
        self.name = name_text.render(name+"-1", False, "white")
        self.fly_time = 0
        self.time_start = time_start
        self.last_direction = None

    # Полет внутри системы
    def solar_system_fly(self, d_s, cur_time, cnt):
        self.fly_time = cur_time-self.time_start
        self.coord += d_s
        self.last_direction = d_s
        if not cnt % 15:
            self.pic = pygame.draw.circle(screen, "red", self.coord, self.r)
        screen.blit(self.name, (self.coord[0]+10, self.coord[1]+10))

    # Полет вне системы
    def outer_fly(self, cnt):
        self.coord += self.last_direction
        if not cnt % 15:
            if self.pic.bottom < 200:
                self.r *= 1.5
            x, y = self.pic.center
            if self.coord[0]+x > 0 and self.coord[1] + y > 0:
                self.pic = pygame.draw.circle(
                    screen, "red", self.coord, self.r)
        x, y = self.pic.center
        if self.coord[0]+x > 0 and self.coord[1] + y > 0 and self.coord[1]-y < screen.get_size()[1]:
            screen.blit(self.name, (self.coord[0]+10, self.coord[1]+10))

# Создание окна и добавление фона
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
back = pygame.image.load("back.jpeg")
back = pygame.transform.scale(back, screen.get_size())
screen.blit(back, (0, 0))

# Отрисовка солнца
sun = pygame.image.load("sun.png")
sun = pygame.transform.scale(sun, (SUN_D, SUN_D))
screen.blit(sun, GELIOCENTER-np.array([SUN_D/2, SUN_D/2]))


# Создание и отрисовка планет
mercury = Planet("mercury", GELIOCENTER+MERCURY_DIST,
                 STD_SIZE//15, REL_MERCURY_PERIOD)
mercury.draw()
venus = Planet("venus", GELIOCENTER+VENUS_DIST,
               STD_SIZE//5, REL_VENUS_PERIOD)
venus.draw()
earth = Planet("earth", GELIOCENTER+EARTH_DIST,
               STD_SIZE//5, REL_EARTH_PERIOD)
earth.draw()
mars = Planet("mars", GELIOCENTER+MARS_DIST,
              STD_SIZE//10, REL_MARS_PERIOD)
mars.draw()
jupiter = Planet("jupiter", GELIOCENTER+JUPITER_DIST,
                 STD_SIZE*4//5, REL_JUPITER_PERIOD)
jupiter.draw()
saturn = Planet("saturn", GELIOCENTER+SATURN_DIST,
                STD_SIZE, REL_SATURN_PERIOD)
saturn.draw()
uranus = Planet("uranus", GELIOCENTER+URANUS_DIST,
                STD_SIZE*2//5, REL_URANUS_PERIOD)
uranus.draw()
neptun = Planet("neptun", GELIOCENTER+NEPTUN_DIST,
                STD_SIZE*2//5, REL_NEPTUN_PERIOD)
neptun.draw()

# Отрисовка начальной даты
date = pygame.font.SysFont("Arial", 32, bold=True)
text = date.render("AUG 1977", False, "white")
screen.blit(text, (0, 0))

voyager = None

clock = pygame.time.Clock()
running = True
# Счетчик кадров и начало отсчета времени
frame_counter = 0
start = pygame.time.get_ticks()
while running:
    screen.blit(back, (0, 0))
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Получение времени работы программы и даты для отрисовки
    cur_time = pygame.time.get_ticks()
    cur_date = get_text(cur_time - start)
    text = date.render(get_text(pygame.time.get_ticks()-start), False, "white")

    # Запуск спутника
    if cur_date == "SEP 1977" and voyager == None:
        voyager = Voyager("Voyager", earth.coord, cur_time/1000)
    
    # Отрисовка объектов
    screen.blit(text, (0, 0))
    screen.blit(sun, GELIOCENTER-np.array([SUN_D/2, SUN_D/2]))
    mercury.draw()
    venus.draw()
    earth.draw()
    mars.draw()
    jupiter.draw()
    saturn.draw()
    uranus.draw()
    neptun.draw()
    
    if voyager != None:
        if get_distance(voyager.coord, GELIOCENTER) < get_distance(JUPITER_DIST, np.zeros(2)):
            delta_s = (jupiter.coord - voyager.coord) / \
                (FPS*(TIME_TO_JUP-voyager.fly_time))
            voyager.solar_system_fly(delta_s, cur_time/1000, frame_counter)
        elif get_distance(voyager.coord, GELIOCENTER) < SATURN_DIST[0]:
            delta_s = (saturn.coord - voyager.coord) / \
                (FPS*(TIME_TO_SATURN-voyager.fly_time))
            voyager.solar_system_fly(delta_s, cur_time/1000, frame_counter)
        else:
            voyager.outer_fly(frame_counter)

    frame_counter += 1
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
