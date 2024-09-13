import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy
pygame.init()



class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')
BLOCK_SIZE = 20
SPEED = 2000
font = pygame.font.SysFont('arial', 25)

class SnakeGame():  

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.score = 0
        self.direction = Direction.RIGHT
        self.frame_iteration = 0
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(BLOCK_SIZE*2), self.head.y)
                      ]

        
        self.food = None
        self.place_food()
    
    def place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self.place_food()

    def move(self, action):
        x = self.head.x
        y = self.head.y
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if numpy.array_equal(action, [1,0,0]):
            new_dir = clock_wise[idx]
        elif numpy.array_equal(action, [0,1,0]):
            new_idx = (idx + 1)%4
            new_dir = clock_wise[new_idx]
        else:
            new_idx = (idx-1)%4
            new_dir = clock_wise[new_idx]
        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)

    def reset(self):
        self.score = 0
        self.frame_iteration = 0
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(BLOCK_SIZE*2), self.head.y)
                      ]
        self.food = None
        self.place_food()
    
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        
        if pt in self.snake[1:]:
            return True
        
        return False
    def play_step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.move(action)
        self.snake.insert(0, self.head)
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            reward = -10
            game_over = True
            return reward, game_over, self.score
        if self.head == self.food:
            self.score += 1
            reward = 10
            self.place_food()
        else:
            self.snake.pop(-1)
        self.update_ui()
        self.clock.tick(SPEED)
        return reward, game_over, self.score
    
    def update_ui(self):
        self.display.fill((0,0,0))

        for pt in self.snake:
            pygame.draw.rect(self.display, (255, 34, 55), pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, (50, 200, 0), pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
        
        pygame.draw.rect(self.display, (0, 255, 0), pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score " + str(self.score), True, (255, 255, 255))
        self.display.blit(text, (0,0))
        pygame.display.flip()