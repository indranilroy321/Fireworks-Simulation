import pygame
import pyautogui
import random
from pygame import mixer

class Rocket:
    def __init__(self, rocket_x, rocket_y, rocket_y_decr, rocket_color, rocket_explo_x, rocket_explo_y, ball):
        self.rocket_x = rocket_x
        self.rocket_y = rocket_y
        self.rocket_y_decr = rocket_y_decr
        self.rocket_color = rocket_color
        self.rocket_length = 5
        self.rocket_breath = 10
        self.state = "MOVING"
        self.rocket_explo_x = rocket_explo_x
        self.rocket_explo_y = rocket_explo_y
        self.ball = ball
        self.balls_left = False
        self.crackling = True

    def draw_rocket(self, screen):
        pygame.draw.rect(screen, self.rocket_color, (self.rocket_x, self.rocket_y, self.rocket_length, self.rocket_breath))

    def play_crackling(self, crackling):
        crackling.play()

class Balls:
    def __init__(self, color, center_x, center_y, radius, width, center_x_move, center_y_move, radius_down, x_dir, y_dir):
        self.color = color
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.width = width
        self.center_x_move = center_x_move
        self.center_y_move = center_y_move
        self.radius_down = radius_down
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.ball_state = "ALIVE"

    def draw_ball(self, screen, color, center_x, center_y, radius, width):
        pygame.draw.circle(screen, color, [center_x, center_y], radius, width)

def create_balls(ball, no_of_balls, rocket_explo_x, rocket_explo_y):
    center_x, center_y = rocket_explo_x, rocket_explo_y

    for i in range(no_of_balls):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        radius = random.randint(1, 15)
        center_x_move = random.randint(-5, 5)
        center_y_move = random.randint(-5, 5)
        radius_down = random.randint(1, 10)
        x_dir = random.randint(-1, 1)
        y_dir = random.randint(-1, 1)
        b = Balls(color, center_x, center_y, radius, 0, center_x_move, center_y_move, radius_down, x_dir, y_dir)
        ball.append(b)

    return ball

def create_rockets(rockets, no_of_rockets):
        for i in range(no_of_rockets):
            rocket_explo_x = random.randint(0, page_width)
            rocket_explo_y = random.randint(0, int(page_depth / 2))
            rocket_x = rocket_explo_x
            rocket_y = page_depth
            rocket_y_decr = random.randint(1, 10)
            rocket_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            ball = []
            ball = create_balls(ball, no_of_balls, rocket_explo_x, rocket_explo_y)

            r = Rocket(rocket_x, rocket_y, rocket_y_decr, rocket_color, rocket_explo_x, rocket_explo_y, ball)
            rockets.append(r)
        return rockets



# Driver Code
pygame.init()
# page_width, page_depth = 800, 600
page_width, page_depth = pyautogui.size()
page_depth = int(page_depth * .95)

# rocket state = MOVING, BRUNING, DEAD
# ball state = ALIVE, DEAD
no_of_rockets = 100
no_of_balls = 1000
rockets = []
rockets = create_rockets(rockets, no_of_rockets)

screen = pygame.display.set_mode((page_width, page_depth))
pygame.display.set_caption("Fireworks Simulation")

crackling = mixer.Sound('Fireworks-Crackling4.mp3')

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(100)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i in rockets:
        if i.state != "DEAD":
            if i.rocket_y <= i.rocket_explo_y:
                i.state = "BURNING"
                i.balls_left = False

                for j in i.ball:
                    if j.radius < 1:
                        j.ball_state = "DEAD"
                        del j
                    else:
                        i.balls_left = True

                if i.balls_left == False:
                    i.state = "DEAD"
                    del i

    for i in rockets:
        if i.state == "MOVING":
            i.draw_rocket(screen)
            i.rocket_y -= i.rocket_y_decr
        elif i.state == "BURNING":
            if i.crackling == True:
                i.play_crackling(crackling)

            for j in i.ball:
                if j.ball_state == "ALIVE":
                    choice_flag = random.randint(0, 1)
                    if choice_flag == 0:
                        j.center_x = j.center_x + j.center_x_move
                        j.center_y = j.center_y + j.center_y_move
                    else:
                        center_x_move = random.randint(1, 20)
                        center_y_move = random.randint(1, 20)

                        j.center_x = j.center_x + j.x_dir * center_x_move
                        j.center_y = j.center_y + j.y_dir * center_y_move

                    if j.radius > 0:
                        down_flag = random.randint(0, 2)
                        if down_flag == 1:
                            j.radius = j.radius - j.radius_down

                    j.draw_ball(screen, j.color, j.center_x, j.center_y, j.radius, 0)

            i.crackling = False


    pygame.display.flip()
pygame.display.update()




