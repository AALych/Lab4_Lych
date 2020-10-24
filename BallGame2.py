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
# Константы цветов
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
    # Класс мишени шарик
    def __init__(self):
        """
        задаются обязательные параметры экземляра
        self.rad - радиус шарика
        self.cord - координаты центра
        self.color - цвет шарика
        self.speed - его скорость
        """
        self.rad = randint(10, max_rad)
        self.cord = [randint(2 * self.rad, width - 2 * self.rad),
                     randint(2 * self.rad, length - 2 * self.rad)]
        self.color = choice(COLORS)
        self.speed = [randint(- max_speed, max_speed),
                      randint(- max_speed, max_speed)]

    def draw(self):
        # функция рисования шарика
        circle(screen, self.color, self.cord, self.rad)

    def move(self):
        """
        Функция движения мишени
        Параметры a и b задают смену направления скорости по оси абсцисс и по
        оси ординат соответсвенно при столкновении со стенкой
        """

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
        """
        Функция, решающая попали ли мы по мишени или нет
        hit_cords - координаты щелчка мыши
        dist - расстояние между центром мишени и щелчком
        """
        dist = ((self.cord[0] - hit_cords[0]) ** 2 +
                (self.cord[1] - hit_cords[1]) ** 2)
        if dist <= (self.rad ** 2):
            """
            Если по мишени попали, то рисуется новый шарик 
            и увеличивается счет
            """
            self.color = choice(COLORS)
            self.speed = [randint(-10, 10), randint(-10, 10)]
            self.rad = randint(10, max_rad)
            self.cord = [randint(2 * self.rad, width - 2 * self.rad),
                         randint(2 * self.rad, length - 2 * self.rad)]
            score.increase(1)


class Square:
    def __init__(self):
        self.wid = randint(30, 50)
        self.length = randint(30, 50)
        self.x = randint(self.wid, width - self.wid)
        self.y = randint(self.length, length - self.length)
        self.color = choice(COLORS)
        self.speed = [randint(- max_speed, max_speed),
                      randint(- max_speed, max_speed)]

    def draw(self):
        rect(screen, self.color, (self.x, self.y, self.wid, self.length))

    def move(self):
        if self.wid < self.x + self.speed[0] < width - self.wid:
            a = 1
        else:
            a = -1
        if self.length < self.y + self.speed[1] < length - self.length:
            b = 1
        else:
            b = -1
        self.speed = [a * self.speed[0], b * self.speed[1]]
        self.x += self.speed[0]
        self.y += self.speed[1]

    def hit(self, hit_cords):
        if (abs(self.x - hit_cords[0]) < self.wid and
                abs(self.y - hit_cords[1]) < self.length):
            self.wid = randint(10, 30)
            self.length = randint(10, 30)
            self.x = randint(self.wid, width - self.wid)
            self.y = randint(self.length, length - self.length)
            self.color = choice(COLORS)
            self.speed = [randint(- max_speed, max_speed),
                          randint(- max_speed, max_speed)]
            score.increase(5)


class Counter:
    """
    Класс счетчика очков
    """

    def __init__(self):
        # В начале счет равен 0
        self.count = 0

    def increase(self, points):
        """
        Функция, увеличивающая счет пи попадании
        points - количество очков, начисляемое за попадание
        """
        self.count += points

    def draw(self):
        # Функция рисования самого счетчика
        surface_counter = labelFont.render(str(self.count), False, BLACK)
        screen.blit(surface_counter, (0, 0))


pygame.display.update()
clock = pygame.time.Clock()
finished = False
rect(screen, WHITE, (0, 0, width, length))
score = Counter()  # создание экземпляра счетчика
labelFont = pygame.font.SysFont('Comic Sans MS', 100)  # задание шрифта счетчика
balls = [Ball() for i in range(10)]  # создание экземпляров мишени шарик
squares = [Square() for k in range(3)]  # и мишени квадрат
for square in squares:
    square.draw()
    square.move()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            """
            Для каждой мишени проверяется, попал ли игрок по ней
            """
            for ball in balls:
                ball.hit(event.pos)
            for square in squares:
                square.hit(event.pos)
    # Циклы движения мишеней
    for ball in balls:
        ball.draw()
        ball.move()
    for square in squares:
        square.draw()
        square.move()
    score.draw()  # Рисование (обновление) счетчика
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
