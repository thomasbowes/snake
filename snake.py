# imports
import pygame
import random
import sys

# Global Variables
SCREEN_SIZE = (495, 495)

BLOCK_WIDTH = 15

#un hard code
GRID_SIZE = (495/15, 495/15)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BACKGROUND_COLOUR = (50, 50, 50)

SNAKE_COLOUR = (71, 222, 111)

# Snake
class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((GRID_SIZE[0] // 2) * BLOCK_WIDTH, (GRID_SIZE[1] // 2) * BLOCK_WIDTH)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.colour = SNAKE_COLOUR

    def get_pos(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):

        curr = self.get_pos()
        x, y = self.direction
        new = (((curr[0] + (x * BLOCK_WIDTH)) % SCREEN_SIZE[0]), (curr[1] + (y * BLOCK_WIDTH)) % SCREEN_SIZE[1])

        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()


    def reset(self):
        self.length = 1
        self.positions = [((GRID_SIZE[0] // 2) * BLOCK_WIDTH, (GRID_SIZE[1] // 2) * BLOCK_WIDTH)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (BLOCK_WIDTH, BLOCK_WIDTH))
            pygame.draw.rect(surface, self.colour, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)

    def handle_keys(self):
        # maybe remoce
        direction_chosen = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and not direction_chosen:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)




class Snack(object):
    def __init__(self):
        self.position = (0, 0)
        self.colour = (223, 163, 49)
        self.new_random_position()

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (BLOCK_WIDTH, BLOCK_WIDTH))
        pygame.draw.rect(surface, self.colour, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

    def new_random_position(self):
        self.position = (random.randint(0, GRID_SIZE[0] -1) * BLOCK_WIDTH, random.randint(0, GRID_SIZE[1] -1) * BLOCK_WIDTH)

class board(object):
    pass

def draw_board(surface):
    surface.fill(BACKGROUND_COLOUR)

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    draw_board(surface)
    snake = Snake()
    snack = Snack()

    myfont = pygame.font.SysFont("monospace",16)


    score = 0

    while (True):
        clock.tick(10)
        snake.handle_keys()
        draw_board(surface)
        snake.move()

        if (snake.get_pos() == snack.position):
            snake.length += 1
            score += 1
            snack.new_random_position()

        snake.draw(surface)
        snack.draw(surface)
        screen.blit(surface, (0,0))
        text = myfont.render("Score {0}".format(score), 1, (255, 255, 255))
        screen.blit(text, (5, 10))
        pygame.display.update()

main()
