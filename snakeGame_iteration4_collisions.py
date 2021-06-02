#21/05/2021
#Ben Rogers 13J5
#DIP Programming internal - AS91906 and AS91907 (3.7/3.8)

#snake game iteration four
#================================== !!this will only contain the game itself!! ==================================

#imports:
import sys
import pygame 
import random
from pygame.constants import KEYDOWN


#create snake function
class SNAKE:
    def __init__(self):
        self.body = [pygame.Vector2(5,10),pygame.Vector2(4,10),pygame.Vector2(3,10)]
        self.direction = pygame.Vector2(1,0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            #set position in screen of snake
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            #draws snake and sets colour
            pygame.draw.rect(screen, (255,125,70), block_rect)

    def move_snake(self):
        if self.new_block == True: 
            body_copy = self.body[:] 
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            #make snake not expand forever by stopping the new blocks
            self.new_block = False 
        else:
            body_copy = self.body[:-1] 
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
    def add_block(self):
        self.new_block = True

#create fruit function 
class FRUIT:
    def __init__(self):
        #following lines determine position on screen, randint creates random value for each axis
        self.randomize_fruit_pos()

    def draw_fruit(self):
        #creates fruit object
        fruit_rect = pygame.Rect(int(self.pos.x*cell_size), int(self.pos.y*cell_size), cell_size, cell_size)
        #puts fruit on screen and sets color
        pygame.draw.rect(screen, (126,166,114), fruit_rect)

    def randomize_fruit_pos(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = pygame.math.Vector2(self.x,self.y)
        

class MAIN:
    def __init__(self):    
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake() 

    def check_collision(self):
        #if snake head (first part of body) is on smae place as fruit
        if self.fruit.pos == self.snake.body[0]: 
            self.fruit.randomize_fruit_pos()
            self.snake.add_block()

    def check_fail(self):
        #check if snake x and y values are in valid positions, i.e. not out of bounds, otherwise game over
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

pygame.init()
#cell_size and cell_number control size of the game (shown in 'screen' variable)
cell_size = 40
cell_number = 15
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
#starts game clock - used to control ticks and movements (updates)
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
#set 'game speed', basically how fast the snake moves, the number controls how long the interval 
#between each movement in milliseconds, similar to a 'tick speed', currently set to 100ms
pygame.time.set_timer(SCREEN_UPDATE,100) 

main_game = MAIN()

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
            main_game.update() 
        
        #if any key is pressed, this code will run
        if event.type == KEYDOWN:
            #when user presses the 'up arrow' key on their keyboard, the snake will turn and face the 
            #upwards direction 
            if event.key == pygame.K_UP: 
                '''
                i had to add this line below to stop the snake from going back on itslef and instantly get a
                game over, I added a similar line to every direction, essentially what it does is checks
                if the snake is moving in the opposite direction to the attempted movement, if the snake isn't
                moving in the opposite direction, then the direction changes, otherwise the snake continues
                downwards.
                '''
                if main_game.snake.direction.y != 1:
                    #this just turns the snake by changing its current co-ordinates to what it is currently, 
                    #but with the y value as 1 less than its current value
                    main_game.snake.direction = pygame.Vector2(0,-1) 
            #if down arrow is pressed, the snake will turn and move in the downwards direction
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1: 
                    #same logic as the above code
                    main_game.snake.direction = pygame.Vector2(0,+1) 
            #if left arrow is pressed, the snake will turn and face in the left direction
            if event.key == pygame.K_LEFT: 
                if main_game.snake.direction.x !=1:
                    main_game.snake.direction = pygame.Vector2(-1,0) 
            #if the right arrow is pressed, the snake will turn and face in the right direction
            if event.key == pygame.K_RIGHT: 
                if main_game.snake.direction.x !=-1:
                    main_game.snake.direction = pygame.Vector2(+1,0) 
        

    #gives screen the green colour
    screen.fill((175,215,70))
    #calls the draw_fruit function, which puts fruit on the screen
    main_game.draw_elements()
    #this pulls the game screen up on the user's screen
    pygame.display.update()
    #sets game clock up
    clock.tick(60)