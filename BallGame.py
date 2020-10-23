import csv
import pygame
from pygame.draw import *
from random import *

pygame.init()
pygame.font.init()
Name = input("Type your name: ")

FPS = 50
width = 900  # ширина экрана
length = 500  # высота экрана
max_rad = 50  # максимальный радиус мишени
# min_rad = 20  # минимальный радиус мишени
max_speed = 10  # максимум скорости шариков по модулю

screen = pygame.display.set_mode((width, length))
'''Константы цветов'''
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)  # цвет экрана
WHITE = (255, 255, 255)  # цвет счетчика
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]  # цвета мишеней


class Ball:
    def __init__(self):
        self.rad = randint(10, max_rad)
        self.cord = [randint(self.rad, width - self.rad),
                     randint(self.rad, length - self.rad)]
        self.color = choice(COLORS)
        self.speed = [randint(- max_speed, max_speed),
                      randint(- max_speed, max_speed)]

    def draw(self):
        circle(screen, self.color, self.cord, self.rad)

    def move(self):
        if 0 + self.rad < self.cord[0] + self.speed[0] < width - self.rad:
            a = 1
        else:
            a = -1
        if 0 + self.rad < self.cord[1] + self.speed[1] < length - self.rad:
            b = 1
        else:
            b = -1
        self.speed = [a * self.speed[0], b * self.speed[1]]
        self.cord = [self.cord[0] + self.speed[0],
                     self.cord[1] + self.speed[1]]

    def hit(self, hit_cords):
        dist = ((self.cord[0] - hit_cords[0]) ** 2 +
                (self.cord[1] - hit_cords[1]) ** 2)
        if dist <= (self.rad ** 2):
            self.color = choice(COLORS)
            self.speed = [randint(-10, 10), randint(-10, 10)]
            self.rad = randint(10, max_rad)
            score.increase(1)


class Counter:
    def __init__(self):
        self.count = 0

    def increase(self, prize):
        self.count += prize

    def draw(self):
        surface_counter = labelFont.render(str(self.count), False, WHITE)
        screen.blit(surface_counter, (0, 0))


pygame.display.update()
clock = pygame.time.Clock()
finished = False
score = Counter()
labelFont = pygame.font.SysFont('Comic Sans MS', 100)
balls = [Ball() for i in range(10)]
for ball in balls:
    ball.draw()
    ball.move()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in balls:
                ball.hit(event.pos)
    for ball in balls:
        ball.draw()
        ball.move()
    score.draw()
    pygame.display.update()
    screen.fill(BLACK)

data = [{Name: score.count}]
with open('records.csv', 'a') as f:
    writer = csv.DictWriter(f, fieldnames=list(data[0].keys()),
                            quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    for d in data:
        writer.writerow(d)

pygame.quit()
