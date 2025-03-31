import pygame

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

    def solar_system_fly(self, d_s, cur_time, cnt):
        self.fly_time = cur_time-self.time_start
        self.coord += d_s
        self.last_direction = d_s
        if not cnt % 15:
            self.pic = pygame.draw.circle(screen, "red", self.coord, self.r)
        screen.blit(self.name, (self.coord[0]+10, self.coord[1]+10))

    def outer_fly(self, cnt):
        self.coord += self.last_direction
        if not cnt % 15:
            if self.pic.bottom < 200:
                self.r *= 1.5
            x, y = self.pic.center
            if self.coord[0]+x > 0 and self.coord[1] + y > 0:
                self.pic = pygame.draw.circle(screen, "red", self.coord, self.r)
        x, y = self.pic.center
        if self.coord[0]+x > 0 and self.coord[1] + y > 0 and self.coord[1]-y < screen.get_size()[1]:
            screen.blit(self.name, (self.coord[0]+10, self.coord[1]+10))