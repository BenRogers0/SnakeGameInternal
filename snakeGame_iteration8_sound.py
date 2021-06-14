# 10/06/2021
# Ben Rogers 13J5
# DIP Programming internal - AS91906 and AS91907 (3.7/3.8)

# snake game iteration eight- implementing sound effect when snake eats apple
# ================================== !!this will only contain the game itself!! ==================================

# imports:
import sys
import pygame
import random
from pygame.constants import KEYDOWN
from pygame.math import Vector2


# create snake function
class SNAKE:
    def __init__(self):
        self.body = [pygame.Vector2(5, 10), pygame.Vector2(
            4, 10), pygame.Vector2(3, 10)]
        self.direction = pygame.Vector2(1, 0)
        self.new_block = False

         # snake graphics:
        #what i have done here is basically just made one image, and then rotated in every direction i needed, 
        # and given different (and easy to understand) variable names to each direction
        #what these basically do is define a veriable as an image (pygame.image.load[file path]
        # basiaclly does this) (learned this from geeks for geeks:
        # https://www.geeksforgeeks.org/python-display-images-with-pygame/)

        #head graphics
        self.head_up = pygame.image.load('graphics/snake/head/snake_head_up_resized.png').convert_alpha()
        self.head_down = pygame.image.load('graphics/snake/head/snake_head_down_resized.png').convert_alpha()
        self.head_left = pygame.image.load('graphics/snake/head/snake_head_left_resized.png').convert_alpha()
        self.head_right = pygame.image.load('graphics/snake/head/snake_head_right_resized.png').convert_alpha()

        #tail graphics
        self.tail_up = pygame.image.load('graphics/snake/tail/snake_tail_up_resized.png').convert_alpha()
        self.tail_down = pygame.image.load('graphics/snake/tail/snake_tail_down_resized.png').convert_alpha()
        self.tail_left = pygame.image.load('graphics/snake/tail/snake_tail_left_resized.png').convert_alpha()
        self.tail_right = pygame.image.load('graphics/snake/tail/snake_tail_right_resized.png').convert_alpha()

        #main body (straight line) graphics
        self.body_vertical = pygame.image.load('graphics/snake/body_straight/snake_body_vertical_resized.png').convert_alpha()
        self.body_horizontal = pygame.image.load('graphics/snake/body_straight/snake_body_horizontal.png').convert_alpha()

        #corner graphics 
        # (NOTE: the "ur", "dl", etc you see here are indicative of directions, so "dr" is "down right", 
        # "ul" is "up left", etc.)
        self.body_bend_ur = pygame.image.load('graphics/snake/bend/snake_bend_ur_resized.png').convert_alpha()
        self.body_bend_ul = pygame.image.load('graphics/snake/bend/snake_bend_ul_resized.png').convert_alpha()
        self.body_bend_dr = pygame.image.load('graphics/snake/bend/snake_bend_dr_resized.png').convert_alpha()
        self.body_bend_dl = pygame.image.load('graphics/snake/bend/snake_bend_dl_resized.png').convert_alpha()

        #sound
        #this was easy enough, learned from https://eng.libretexts.org/Bookshelves/Computer_Science/Book%3A_Making_Games_with_Python_and_Pygame_(Sweigart)/03%3A_Pygame_Basics/3.22%3A_Playing_Sounds 
        # this essentially just defines a variable as a 'sound object', this sound object is taken from 
        # a file which i have downloaded and put into my "sound" file
        #eating sound:
        self.nom_sound = pygame.mixer.Sound('sound/nom.wav')
        #game over sound:
        self.game_over_sound = pygame.mixer.Sound('sound/game_over3.wav')
        #background music:
        self.background_music = pygame.mixer.Sound('sound/bg_music.mp3')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            # check the direction snake is facing
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_bend_ul, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bend_dl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_bend_ur, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_bend_dr, block_rect)
            '''
            else:
                pygame.draw.rect(screen,(255,125,70),block_rect)
            '''

        '''  
        #below is not needed for now, since it will be relpaced with images, rather than squares
        for block in self.body:
            #set position in screen of snake
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            #draws snake and sets colour
            pygame.draw.rect(screen, (255,125,70), block_rect)
        '''

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == pygame.Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == pygame.Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == pygame.Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == pygame.Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == pygame.Vector2(-1, 0):
            self.tail = self.tail_left
        elif tail_relation == pygame.Vector2(1, 0):
            self.tail = self.tail_right
        elif tail_relation == pygame.Vector2(0, -1):
            self.tail = self.tail_up
        elif tail_relation == pygame.Vector2(0, +1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            # make snake not expand forever by stopping the new blocks
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_nom(self):
        self.nom_sound.play()

    def game_over_sound(self):
        self.game_over_sound.play()

# create fruit function


class FRUIT:
    def __init__(self):
        # following lines determine position on screen, randint creates random value for each axis
        self.randomize_fruit_pos()

    def draw_fruit(self):
        # creates fruit object
        fruit_rect = pygame.Rect(
            int(self.pos.x*cell_size), int(self.pos.y*cell_size), cell_size, cell_size)
        '''#puts fruit on screen and sets color
        pygame.draw.rect(screen, (126,166,114), fruit_rect)
        above can be 'commented' out since i am changing to an image, instead of the draw function now.
        '''
        # draws image, 'apple', to the fruit_rect position
        screen.blit(apple, fruit_rect)

    def randomize_fruit_pos(self):
        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(0, cell_number-1)
        self.pos = pygame.math.Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        # if snake head (first part of body) is on smae place as fruit
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize_fruit_pos()
            self.snake.add_block()
            self.snake.nom_sound.play()

    def check_fail(self):
        # check if snake x and y values are in valid positions, i.e. not out of bounds, otherwise game over
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.game_over_sound.play()
        pygame.quit()
        sys.exit()

    def draw_grass(self):
        grass_color = (160,200,30)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen, grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect= pygame.Rect(col * cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen, grass_color,grass_rect)



    def draw_score(self):
        score_text = str(len(self.snake.body)-3) # calculates score as length of snake body, -3 for starting size
        score_box = score_font.render(score_text, True, (56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_box.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,apple_rect.width + score_rect.width,apple_rect.height)

        pygame.draw.rect(screen,(167,209,61), bg_rect)
        screen.blit(score_box,score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen,(10,50,10),bg_rect,2)


pygame.init()
# cell_size and cell_number control size of the game (shown in 'screen' variable)
cell_size = 40
cell_number = 15
screen = pygame.display.set_mode(
    (cell_number * cell_size, cell_number * cell_size))
# starts game clock - used to control ticks and movements (updates)
clock = pygame.time.Clock()
# replacing blue square with image
#apple: https://www.stockio.com/free-icon/fruity-icons-apple 
apple = pygame.image.load('graphics/fruit/apple_resized.png').convert_alpha()

score_font = pygame.font.Font('font_file/BalooTammudu2-Medium.ttf',40)

SCREEN_UPDATE = pygame.USEREVENT
# set 'game speed', basically how fast the snake moves, the number controls how long the interval
# between each movement in milliseconds, similar to a 'tick speed', currently set to 100ms, this 
# was because it looks like smooth movement, rather than 'jittering' movement i get when it is a slower speed, 
# at 150ms+
pygame.time.set_timer(SCREEN_UPDATE, 100)

main_game = MAIN()

# starts game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # pygame closes, and deactivates pygame library
            pygame.quit()
            # terminates program
            sys.exit()

        # when SCREEN_UPDATE happens, move the snake in the current facing direction
        if event.type == SCREEN_UPDATE:
            main_game.update()

        # if any key is pressed, this code will run
        if event.type == KEYDOWN:
            # when user presses the 'up arrow' key on their keyboard, the snake will turn and face the
            # upwards direction
            if event.key == pygame.K_UP:
                '''
                i had to add this line below to stop the snake from going back on itslef and instantly get a
                game over, I added a similar line to every direction, essentially what it does is checks
                if the snake is moving in the opposite direction to the attempted movement, if the snake isn't
                moving in the opposite direction, then the direction changes, otherwise the snake continues
                downwards.
                '''
                if main_game.snake.direction.y != 1:
                    # this just turns the snake by changing its current co-ordinates to what it is currently,
                    # but with the y value as 1 less than its current value
                    main_game.snake.direction = pygame.Vector2(0, -1)
            # if down arrow is pressed, the snake will turn and move in the downwards direction
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    # same logic as the above code
                    main_game.snake.direction = pygame.Vector2(0, +1)
            # if left arrow is pressed, the snake will turn and face in the left direction
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = pygame.Vector2(-1, 0)
            # if the right arrow is pressed, the snake will turn and face in the right direction
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = pygame.Vector2(+1, 0)

    # gives screen the green colour
    screen.fill((175, 215, 70))
    # calls the draw_fruit function, which puts fruit on the screen
    main_game.draw_elements()
    # this pulls the game screen up on the user's screen
    pygame.display.update()
    # sets game clock up
    clock.tick(60)
