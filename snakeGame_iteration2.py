#17/05/2021
#Ben Rogers 13J5
#DIP Programming internal - AS91906 and AS91907 (3.7/3.8)

#snake game iteration two
#================================== !!this will only contain the game itself!! ==================================

#imports:
import sys
import pygame 
import random

from pygame.constants import KEYDOWN
#import time

#create snake function
class SNAKE:
    def __init__(self):
        self.body = [pygame.Vector2(5,10),pygame.Vector2(6,10),pygame.Vector2(7,10)]
        self.direction = pygame.Vector2(1,0)

    def draw_snake(self):
        for block in self.body:
            #set position in screen of snake
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            #draws snake and sets colour
            pygame.draw.rect(screen, (255,125,70), block_rect)

    def move_snake(self):
        body_copy = self.body[:-1] 
        body_copy.insert(0,body_copy[0] + self.direction)
        self.body = body_copy[:]

#create fruit function 
class FRUIT:
    def __init__(self):
        #following lines determine position on screen, randint creates random value for each axis
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = pygame.math.Vector2(self.x,self.y)

    def draw_fruit(self):
        #creates fruit object
        fruit_rect = pygame.Rect(int(self.pos.x*cell_size), int(self.pos.y*cell_size), cell_size, cell_size)
        #puts fruit on screen and sets color
        pygame.draw.rect(screen, (126,166,114), fruit_rect)
       

pygame.init()
#cell_size and cell_number control size of the game (shown in 'screen' variable)
cell_size = 40
cell_number = 15
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
#starts game clock - used to control ticks and movements (updates)
clock = pygame.time.Clock()

#i made these variables so that i can call specific sub functions, such as "fruit.draw_fruit", 
# instead of having to call the entire FRUIT() function.
fruit = FRUIT()
snake = SNAKE()

SCREEN_UPDATE = pygame.USEREVENT
#set 'game speed', basically how fast the snake moves, the number controls how long the interval 
#between each movement in milliseconds, similar to a 'tick speed', currently set to 100ms
pygame.time.set_timer(SCREEN_UPDATE,100) 

#starts game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #pygame closes, and deactivates pygame library
            pygame.quit()
            #terminates program
            sys.exit()
        
        #when SCREEN_UPDATE happens, move the snake in the current facing direction
        if event.type == SCREEN_UPDATE:
            snake.move_snake()
        
        #if any key is pressed, this code will run
        if event.type == KEYDOWN:
            #when user presses the 'up arrow' key on their keyboard, the snake will turn and face the 
            #upwards direction 
            if event.key == pygame.K_UP: 
                #this just turns the snake by changing its current co-ordinates to what it is currently, 
                #but with the y value as 1 less than its current value
                snake.direction = pygame.Vector2(0,-1) 
            #if down arrow is pressed, the snake will turn and move in the downwards direction
            if event.key == pygame.K_DOWN: 
                #same logic as the above code
                snake.direction = pygame.Vector2(0,+1) 
            #if left arrow is pressed, the snake will turn and face in the left direction
            if event.key == pygame.K_LEFT: 
                snake.direction = pygame.Vector2(-1,0) 
            #if the right arrow is pressed, the snake will turn and face in the right direction
            if event.key == pygame.K_RIGHT: 
                snake.direction = pygame.Vector2(+1,0) 
        

    #gives screen the green colour
    screen.fill((175,215,70))
    #calls the draw_fruit function, which puts fruit on the screen
    fruit.draw_fruit()
    snake.draw_snake()

    #this pulls the game screen up on the user's screen
    pygame.display.update()
    #sets game clock up
    clock.tick(60)