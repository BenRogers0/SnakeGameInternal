# 12/06/2021
# Ben Rogers 13J5
# DIP Programming internal - AS91906 and AS91907 (3.7/3.8)

# snake game iteration eleven- implementing different screens

#note that i have referenced sources of where i have learned most of the code used in this program, 
# before begining any coding, I firstly read up on the basics, whcih was mostly done at this 
# source: https://realpython.com/pygame-a-primer/,
# this included .blit(), surfaces, rects, images, among other things, more complex tasks are referenced 
# if i had to learn how to do this

# imports:
import sys
import pygame
import random
from pygame.constants import KEYDOWN
#vector2 is a 2 dimensional vector, basically allows me to use 2d shapes in my program (squares, rectangles, etc)
from pygame.math import Vector2

# create snake class
#the idea of having seperate classes for snake, fruit, and main was simply just so i could keep my code simple by
# seperating the two main problems i have, this also makes it easy to find things when coding, and it also helped 
# when i could easily reference each class with self.fruit, and self.snake
class Snake:
    def __init__(self):
        #define 'body' as a 2d vector at position (x,y)
        self.body = [pygame.Vector2(5, 50), pygame.Vector2(4, 50), pygame.Vector2(3, 50)]
        #makes the snake not move by setting the direction to not increase on either axis
        self.direction = pygame.Vector2(0, 0)
        #stops the snake form infinitely carrying on with a large tail
        self.new_body_block = False

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
        #background music:
        self.background_music = pygame.mixer.Sound('sound/bg_music.mp3')

    #makes snake shape
    def draw_snake(self):
        #update directions of head and tail, ensures that the body parts are facing the correct direction with graphics, 
        # just so it looks clean and professional
        self.update_head()
        self.update_tail()
        
        #enumerate gives a value to each body piece so i can use them later, it basically replaces the need for me
        # to create an incrementing variable (such as n = n+1)
        #learned from: https://realpython.com/python-enumerate/ 
        for index, block in enumerate(self.body):
            #set position of snake
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            #body_rect is the square where the body is, and the position is based on the position variables 
            # of each body part
            body_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            #if head block (0 is head block), make the head graphic on that rect object
            if index == 0:
                screen.blit(self.head, body_rect)
            #if tail block, make the rect object be the body graphic, basically replace last square with tail image
            elif index == len(self.body) - 1:
                screen.blit(self.tail, body_rect)
            else:
                #these variables are extremely important, they help with directions, and was essential in getting 
                # the right graphics, to explain these variabels, it essentially gives the block before, or after 
                # a certain blocks position, a variable, if it is the previous block, or the block coming before 
                # the current block, it is given previous_block, and the same with the next block, if it is the 
                # next block coming up, then it is given the next_block variable
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                #if x is a constant it then the horizontal axis stays the same, meaning the block is moving directly
                # up or down so the vertical body image is put in the place of that rect pieces
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, body_rect)
                #same logic as above, but for horizontal axis, so if the previous block and next block are the on 
                # the same y value, then the snake must be moving straight left or right (horizontally), so place 
                # the horizontal image on that body piece 
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, body_rect)

                #corner logic:
                else:
                    #checks which direction it is going by seeing if x or y value is increasing or decreasing 
                    # for the previous and next blocks
                    #up left
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_bend_ul, body_rect)
                    #down left
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bend_dl, body_rect)
                    #up right
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_bend_ur, body_rect)
                    #down right
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_bend_dr, body_rect)
        
    #upadates head direction, basically checks what direction it is facing, and makes image with the correct 
    # orientation display
    def update_head(self):
        head_direction = self.body[1] - self.body[0]
        #sets head as the left direction if facing left
        if head_direction == pygame.Vector2(1, 0):
            self.head = self.head_left
        #sets head as the right direction if facing right
        elif head_direction == pygame.Vector2(-1, 0):
            self.head = self.head_right
        #sets head as the up direction if facing up
        elif head_direction == pygame.Vector2(0, 1):
            self.head = self.head_up
        #sets head as the down direction if facing down
        elif head_direction == pygame.Vector2(0, -1):
            self.head = self.head_down

    #updates tail direction, similarly to the way it works for the head
    def update_tail(self):
        tail_direction = self.body[-2] - self.body[-1]
        #left
        if tail_direction == pygame.Vector2(-1, 0):
            self.tail = self.tail_left
        #right
        elif tail_direction == pygame.Vector2(1, 0):
            self.tail = self.tail_right
        #up
        elif tail_direction == pygame.Vector2(0, -1):
            self.tail = self.tail_up
        #down
        elif tail_direction == pygame.Vector2(0, +1):
            self.tail = self.tail_down

    #this moves the snake
    def move_snake(self):
        #this code what makes the body grow, if this variable is set to true 
        # (in add_block function, when fruit is eaten), the body will grow by one square
        if self.new_body_block == True:
            #define body_copy as a clone of body_copy
            #learned from https://openbookproject.net/thinkcs/python/english3e/lists.html 
            body_copy = self.body[:]
            #insert a copy of the body as the first item in that list
            body_copy.insert(0, body_copy[0] + self.direction)
            #make body = to the appended body_copy list
            self.body = body_copy[:]
            # make snake not expand forever by stopping the new blocks
            self.new_body_block = False
        #else move the snake
        else:
            #similar logic as above essentially, just adds a block and takes a blcok away to show movement
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        #sets new block as true so that the code to add a body block runs
        self.new_body_block = True

    def play_nom(self):
        #play eating sound
        self.nom_sound.play()

    def play_music(self):
        #play background music, the (-1) makes it infinite (id i had done 0, or left it blank, it would play 
        # only once)
        self.background_music.play(-1)
        
    def reset(self):
        #puts the snake back into the original position and sets to original size of 3, and makes the snake not move in any direction
        self.body = [Vector2(3,7),Vector2(2,7),Vector2(1,7)]
        self.direction = Vector2(0,0)
        

# create fruit class
class Fruit:
    def __init__(self):
        #randomize fruit position at the start so that the fruit starts somewhere random 
        self.randomize_fruit_pos()

    def randomize_fruit_pos(self):
        # following lines determine position on screen, randint creates random value for each axis, 
        # -1 makes sure it doesnt 'spawn' off screen
        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(0, cell_number-1)
        #gives the position a variable as "pos" (short for position)
        self.pos = Vector2(self.x, self.y)


#create main class
class Main:
    def __init__(self):
        #set highscore to 0 at start, so it doesn't carry through each playthrough/life
        self.highscore = 0
        #these help me call things from the other classes easily by doing self.(class) to get any 
        # variable or function from the other classes
        self.snake = Snake()
        self.fruit = Fruit()
        #play background music at start so it continually plays throughout the game
        self.snake.play_music()

    def update(self):
        #calls all the updating functions that aren't to do with graphics, basically moves snake, and 
        # checks for death conditions (game over conditions)
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    #following are just drawing each different fruit
    #creates function to draw the grape image on the fruit position

    def draw_grapes(self):
        # draws image, 'grape', to the fruit_rect position
        fruit_rect = pygame.Rect(int(self.fruit.pos.x*cell_size), int(self.fruit.pos.y*cell_size), cell_size, cell_size)
        screen.blit(grapes, fruit_rect)
    
    #creates function to draw the banana image on the fruit position
    def draw_banana(self):
        fruit_rect = pygame.Rect(int(self.fruit.pos.x*cell_size), int(self.fruit.pos.y*cell_size), cell_size, cell_size)
        screen.blit(banana, fruit_rect)
    
    #creates function to draw the cherry image on the fruit position
    def draw_cherries(self):
        fruit_rect = pygame.Rect(int(self.fruit.pos.x*cell_size), int(self.fruit.pos.y*cell_size), cell_size, cell_size)
        screen.blit(cherries, fruit_rect)

    #creates function to draw the strawberry image on the fruit position
    def draw_strawberry(self):
        fruit_rect = pygame.Rect(int(self.fruit.pos.x*cell_size), int(self.fruit.pos.y*cell_size), cell_size, cell_size)
        screen.blit(strawberry, fruit_rect)

    #creates function to draw the watermelon image on the fruit position
    def draw_watermelon(self):
        fruit_rect = pygame.Rect(int(self.fruit.pos.x*cell_size), int(self.fruit.pos.y*cell_size), cell_size, cell_size)
        screen.blit(watermelon, fruit_rect)

    def draw_apple(self):
        fruit_rect = pygame.Rect(int(self.fruit.pos.x*cell_size), int(self.fruit.pos.y*cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    #draws the main parts of the game, grass background, snake body, and score box
    def draw_objects(self):
        self.draw_grass()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        # if snake head collides (hits) a fruit, move the fruit somewhere else, grow snake length, 
        # and play eating sound
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize_fruit_pos()
            self.snake.add_block()
            self.snake.nom_sound.play()

        #this fixes an issue that has been annoying me for a while, which is that the apple sometimes 'spawns' 
        # underneath the snake, which makes it hard to see, so i changed this
        for block in self.snake.body[1:]:
            #basically, if any part, aside from the head, is in the same position as the fruit, the fruit will 
            # move somewhere else (this will be called until a new place is found)
            if block == self.fruit.pos:
                self.fruit.randomize_fruit_pos()
        
    def check_fail(self):
        # check if snake x and y values are in valid positions, i.e. not out of bounds, otherwise game over
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.snake.reset()
        #check if the the head block hits the rest of the body, if this is the case, game over
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.snake.reset()

    #draws the checkerboard pattern
    def draw_grass(self):
        #sets darker colour
        GRASS_COLOUR = (160,200,30)
        
        for row in range(cell_number):
            #check if the row is an even number (% 2 == 0 checks if it is a multiple of 2, so an even number)
            if row % 2 == 0:
                for col in range(cell_number):
                    #check if the colum is an even number (same as above)
                    if col % 2 == 0:
                        #all these locations (places where the even columns and rows intersect) will be the
                        # darker grass colour defined above
                        grass_rect = pygame.Rect(col * cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen, GRASS_COLOUR,grass_rect)
            else:
                #same as above, but for column
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect= pygame.Rect(col * cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen, GRASS_COLOUR,grass_rect)

    def draw_score(self):
        n = (len(self.snake.body)-3) # calculates score as length of snake body, -3 for starting size
        #this is the code that chooses the fruit, i just used some simple code here, since this gets the job down, 
        # and simulates some randomness
        #if score is divisible by 6, draw watermelon 
        if   (n % 6 == 0):
            self.draw_watermelon()
        #if score is divisible by 5, draw grapes 
        elif (n % 5 == 0):
            self.draw_grapes()
        #if score is divisible by 4, draw strawberry 
        elif (n % 4 == 0):
            self.draw_strawberry()
        #if score is divisible by 3, draw cherries 
        elif (n % 3 == 0):
            self.draw_cherries()
        #if score is divisible by 2, draw banana 
        elif (n % 2 == 0):
            self.draw_banana()
        #if any other number (prime number etc.) draw apple (this was the main shape, so it made sense here)
        else:
            self.draw_apple()

        #this is the code for the score box
        score_text = str(len(self.snake.body)-3) #score calculation, as mentioned above
        
        #render() makes the text able to be shown in pygame, learned from:
        #https://pygame.readthedocs.io/en/latest/4_text/text.html 
        score_box = font.render(score_text, True, (56,74,12))
        #positions the box
        score_x = int(cell_size * cell_number - 80)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_box.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        #draws the box and the apple inside the box
        screen.blit(score_box,score_rect)
        screen.blit(apple,apple_rect)
        
        #shows user's position, these scores were gathered from my friends playing the game and getting scores
        if n < 5:
            position_text = str("10th") 
        elif n < 8:
            position_text = str(" 9th")
        elif n < 10:
            position_text = str(" 8th")
        elif n < 14:
            position_text = str(" 7th")
        elif n < 16:
            position_text = str(" 6th")
        elif n < 20:
            position_text = str(" 5th")
        elif n < 23:
            position_text = str(" 4th")
        elif n < 25:
            position_text = str(" 3rd")
        elif n < 35:
            position_text = str(" 2nd")
        else:
            position_text = str(" 1st!")
        
        #creates and draws the position box 
        position_box = font.render(position_text, True, (56,74,12))
        position_rect = pygame.Rect(30,10,60,60)
        screen.blit(position_box, position_rect)
        
        #if current score is greater than highscore, update highscore to be current score
        if n > self.highscore:
            self.highscore = n
        #make a highscore box
        highscore_text = "High score: " + str(self.highscore)
        highscore_box = font.render(highscore_text, True, (56,74,12))
        highscore_rect = pygame.Rect(310,10,60,60)
        screen.blit(highscore_box, highscore_rect)
        
pygame.init()
# cell_size and cell_number control size of the game (shown in 'screen' variable)
cell_size = 40
cell_number = 15
#set screen variable
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
# starts game clock - used to control ticks and movements (updates)
clock = pygame.time.Clock()
# replacing blue square with different images


# these are all the different fruits the user can pick up, sourced from stockio.com 
# by "AomAm"- https://www.behance.net/gallery/37953745/FREE-FRUITY-ICONS
#NOTE: These have been allowed for for personal and commercial use

#apple: https://www.stockio.com/free-icon/fruity-icons-apple 
apple = pygame.image.load('graphics/fruit/apple_resized.png').convert_alpha()
#banana https://www.stockio.com/free-icon/fruity-icons-banana 
banana = pygame.image.load('graphics/fruit/banana_resized.png').convert_alpha()
#grapes: https://www.stockio.com/free-icon/fruity-icons-grape 
grapes = pygame.image.load('graphics/fruit/grapes_resized.png').convert_alpha()
#cherries: https://www.stockio.com/free-icon/fruity-icons-cherry 
cherries = pygame.image.load('graphics/fruit/cherries_resized.png').convert_alpha()
# strawberry: https://www.stockio.com/free-icon/fruity-icons-strawberry
strawberry = pygame.image.load('graphics/fruit/strawberry_resized.png').convert_alpha()
#watermelon: https://www.stockio.com/free-icon/fruity-icons-watermelon 
watermelon = pygame.image.load('graphics/fruit/watermelon_resized.png').convert_alpha()

#font i have used for all text in my program, sourced from google fonts:
#https://fonts.google.com/specimen/Baloo+Tammudu+2 
font = pygame.font.Font('font_file/BalooTammudu2-Medium.ttf',40)

screen_update = pygame.USEREVENT
# set 'game speed', basically how fast the snake moves, the number controls how long the interval
# between each movement in milliseconds, similar to a 'tick speed', currently set to 100ms, this 
# was because it looks like smooth movement, rather than 'jittering' movement i get when it is a slower speed, 
# at 150ms+ (it still does have some jiterring movement, however it is minimal at this speed while still being
# playable)
pygame.time.set_timer(screen_update, 100)

#helps me call things from the main class when i need to
main_game = Main()

# starts loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # pygame closes, and deactivates pygame library
            pygame.quit()
            # terminates program
            sys.exit()

        # when screen_update happens, move the snake in the current facing direction
        if event.type == screen_update:
            main_game.update()

        # if any key is pressed, this code will run
        if event.type == KEYDOWN:
            # when user presses the 'up arrow' key on their keyboard, the snake will turn and face the
            # upwards direction
            if event.key == pygame.K_UP:
                '''
                i had to add this line below to stop the snake from going back on itself and instantly get a
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
    screen.fill((172, 212, 63))
    # calls everything to be drawn
    main_game.draw_objects()
    # this pulls the game screen up on the user's screen
    pygame.display.update()
    # sets game clock up
    clock.tick(60)
