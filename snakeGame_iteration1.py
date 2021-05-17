#16/04/2021
#Ben Rogers 13J5
#DIP Programming internal - AS91906 and AS91907 (3.7/3.8)

#snake game iteration one
#================================== !!this will only contain the game itself!! ==================================

#imports:
import sys
import pygame 

#create fruit function 
class FRUIT:
    def __init__(self):
        #following lines determine position on screen
        self.x = 5
        self.y = 4
        self.pos = pygame.math.Vector2(self.x,self.y)

    def draw_fruit(self):
        #creates fruit object
        fruit_rect = pygame.Rect(self.pos.x, self.pos.y, cell_size, cell_size)
        pygame.draw.rect(screen, (126,166,114), fruit_rect)

pygame.init()
#cell_size and cell_number control size of the game (shown in "screen")
cell_size = 40
cell_number = 15
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
#starts game clock - used to control ticks and movements (updates)
clock = pygame.time.Clock()

#calls fruit to run
fruit = FRUIT()

#starts game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #pygame closes, and deactivates pygame library
            pygame.quit()
            #terminates program
            sys.exit()
    #gives screen the green colour
    screen.fill((175,215,70))
    #calls the draw_fruit function, which puts fruit on the screen
    fruit.draw_fruit()
    #this pulls the game screen up on the user's screen
    pygame.display.update()
    #sets game tick speed
    clock.tick(60)