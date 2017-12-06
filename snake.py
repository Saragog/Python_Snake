# gra snake
# Author Andrzej Dackiewicz
# Date 02 12 2017
#
#   This project is a continuation of work over basic snake project showed
#   during the DaftCode's Python for beginners class
#   The purpose is to improve the authors personal Python skills and to have some fun :D
#

import random
import pygame, sys
import pygame.mixer
from pygame.locals import *


GAME_CELL_SIZE_PX = 20  # HAS TO BE AN EVEN NUMBER
assert (int(GAME_CELL_SIZE_PX/2)*2) == GAME_CELL_SIZE_PX

GAME_CELLS_X = 50
GAME_CELLS_Y = 25
random.seed(a=1)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

colours = {}
colours['BACKGROUND'] = (0, 0, 0)
colours['HEAD'] = (200, 200, 200)
colours['BODY1'] = (255, 0, 0)
colours['FOOD'] = (199, 191, 111)
colours['BODY2'] = (0, 255, 0)
colours['BODY3'] = (0, 0, 255)

#mixer m = new mixer()

def draw_segment(surface, x, y, colour):
    position = (
            x * GAME_CELL_SIZE_PX,
            y * GAME_CELL_SIZE_PX,
            GAME_CELL_SIZE_PX,
            GAME_CELL_SIZE_PX
    )
    pygame.draw.rect(surface, colour, position)


def draw_food(surface, x, y):
    position = (
        x * GAME_CELL_SIZE_PX + GAME_CELL_SIZE_PX//2,
        y * GAME_CELL_SIZE_PX + GAME_CELL_SIZE_PX//2)
    pygame.draw.circle(surface, colours.get('FOOD'), position, GAME_CELL_SIZE_PX//2)


class Snake:
    vectors = {
        'UP': (0, -1),
        'DOWN': (0, 1),
        'LEFT': (-1, 0),
        'RIGHT': (1, 0),
    }

    def __init__(self, food):
        self.segments = [[0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [7, 5], [8, 5], [9, 5], [10, 5], [11, 5], [12, 5]]
        self.direction = 'RIGHT'
        self.food = food
        self.is_fullscreen_on = False
        self.just_ate = False

    def _normalize_segments(self):
        for segment in self.segments:
            if segment[0] >= GAME_CELLS_X:
                segment[0] -= GAME_CELLS_X
            if segment[0] < 0:
                segment[0] += GAME_CELLS_X
            if segment[1] >= GAME_CELLS_Y:
                segment[1] -= GAME_CELLS_Y
            if segment[1] < 0:
                segment[1] += GAME_CELLS_Y

    def move(self):
        vector = self.vectors.get(self.direction, (0, 0))
        # wypadałoby zalogować, że brakuje jakiegos klucza...
        first_segment = self.segments[-1]
        if self.just_ate == False:
            self.segments.pop(0)
        self.just_ate = False
        self.segments.append(
            # TODO: a może da się sprytniej? Coś z zip?
            [first_segment[0] + vector[0], first_segment[1] + vector[1]]
        )
        self._normalize_segments()
        self.try_to_eat()

    def is_game_over(self):
        if self.segments[-1] in self.segments[:-1]:
          print("--- Waz zjadl sam siebie ---\n", 'Reset gry')
          return True
        else:
          return False
        
    def draw(self, surface):
        segments = self.segments
        last_used_colour = -1
        for segment in reversed(segments):
          if last_used_colour == -1:
            colour = colours['HEAD']
          elif last_used_colour == 0:
            colour = colours['BODY1']
          elif last_used_colour == 1:
            colour = colours['BODY2']
          elif last_used_colour == 2:
            colour = colours['BODY3']
          last_used_colour = (last_used_colour + 1) % 3
          draw_segment(surface, *segment, colour)

    def process_event(self, event):
        # te stałe stringi wypadałoby do jakiś constów przenieść
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
              if not self.direction == 'RIGHT':
                self.direction = 'LEFT'
            elif event.key == K_RIGHT:
              if not self.direction == 'LEFT':
                self.direction = 'RIGHT'
            elif event.key == K_UP:
              if not self.direction == 'DOWN':
                self.direction = 'UP'
            elif event.key == K_DOWN:
              if not self.direction == 'UP':
                self.direction = 'DOWN'
            elif event.key == pygame.K_f:
              if not self.is_fullscreen_on:
                self.is_fullscreen_on = True
                pygame.display.set_mode((0,0),pygame.FULLSCREEN)
              else:
                self.is_fullscreen_on = False
                pygame.display.set_mode(
                (GAME_CELLS_X * GAME_CELL_SIZE_PX, GAME_CELLS_Y * GAME_CELL_SIZE_PX)
    )
                  

    def try_to_eat(self):
        if (
            self.segments[-1][0] == self.food.x
            and self.segments[-1][1] == self.food.y     # snakes head is where food is :D
        ):
            self.food.spawn_food(self.segments)
            self.just_ate = True


class FoodProvider:
    def __init__(self):
        self.spawn_food()

    def _get_new_coords(self, possible_food_positions):
        random_position = random.choice(possible_food_positions)
        print(type(possible_food_positions))
        self.x = random_position[0]
        self.y = random_position[1]
        
    def draw(self, surface):
        draw_food(surface, self.x, self.y)

    def spawn_food(self, snake_segments = []):
    
        print(type(snake_segments))
    
        possible_food_positions = []
        for x in range(0, GAME_CELLS_X):
          for y in range(0, GAME_CELLS_Y):
            possible_food_positions.append((x, y))
        
        for segment in snake_segments:
          x_seg_pos = segment[0]
          y_seg_pos = segment[1]
          possible_food_positions.remove((x_seg_pos, y_seg_pos))
        print(type(possible_food_positions))
        self._get_new_coords(possible_food_positions)
        

def draw_background(surface):
    position = (
        0, 0,
        GAME_CELLS_X * GAME_CELL_SIZE_PX, GAME_CELLS_Y * GAME_CELL_SIZE_PX
    )
    pygame.draw.rect(surface, colours.get('BACKGROUND'), position)

def show_menu():
    is_menu_opened = True
    
    
def run_game():
    pygame.init()
    pygame.mixer.quit()
    FPS = 10  # Frames Per Second
    fpsClock = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode(
        (GAME_CELLS_X * GAME_CELL_SIZE_PX, GAME_CELLS_Y * GAME_CELL_SIZE_PX),
        pygame.RESIZABLE
    )
    pygame.display.set_caption('PySnake')
    is_menu_opened = True
    show_menu()
    food = FoodProvider()
    snake = Snake(food=food)
    while True:
        for event in pygame.event.get():
            print('event: {}'.format(event))
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if is_menu_opened:
                        pygame.quit()
                        sys.exit()
                    else:
                        is_menu_opened = True
            snake.process_event(event)
        if is_menu_opened:
            show_menu()
        else:
            draw_background(DISPLAYSURF)
            snake.draw(DISPLAYSURF)
            food.draw(DISPLAYSURF)
            snake.move()
            if snake.is_game_over() == True:
                snake = Snake(food = food)
            pygame.display.update()
            fpsClock.tick(FPS)

if __name__ == '__main__':
    run_game()