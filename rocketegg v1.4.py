x = 100
y = 50
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
from math import sqrt
import os
import random
import pygame
from pygame.locals import *
import math

# GLOBAL CONSTANTS

# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
LIGHT_BLUE = (0,235,247)
 
# Screen dimensions
SCREEN_WIDTH  = 1440
SCREEN_HEIGHT = 900

#ENDBLOCK CLASS
class EndBlock(pygame.sprite.Sprite):
    
    def __init__(self):


        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load("endblockbrick.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

        
# WALL CLASS
class Wall(pygame.sprite.Sprite):

    def __init__(self, level):

        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load("wallbrick"+str(level)+".png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        
# TURRET CLASS
class Turret(pygame.sprite.Sprite):

    def __init__(self, x, y):


        pygame.sprite.Sprite.__init__(self)

        self.imageMaster = pygame.image.load("turret_graphic.png")
        self.imageMaster.convert()
        self.imageMaster.set_colorkey(WHITE)

        self.rect = self.imageMaster.get_rect()
        self.rect.center = (x, y)
        self.dir = 0
        self.count = 0

        
    def update(self, rocketegg, shell_list, all_sprites_list):
        self.rotate()
        self.follow_rocket(rocketegg)
        self.check_fire(rocketegg, shell_list, all_sprites_list)
        
    def follow_rocket(self, rocketegg):
    
        dx = self.rect.centerx - (rocketegg.rect.x + 20) 
        dy = self.rect.centery - (rocketegg.rect.y + 29)
        dy *=-1
        radians=math.atan2(dy,dx)
        self.dir=radians * 180/math.pi
        self.dir +=180
        self.distance=math.sqrt((dx *dx) + (dy *dy))

    def rotate(self):
        oldCenter=self.rect.center
        self.image=pygame.transform.rotate(self.imageMaster,self.dir)
        self.rect=self.image.get_rect()
        self.rect.center=oldCenter
        
    def check_fire(self, rocketegg, shell_list, all_sprites_list):
        self.count += 1
        if self.distance < 10000 and self.count == 30:
            self.shell = Shell(self.rect.centerx, self.rect.centery, self.dir)
            shell_list.add(self.shell)
            all_sprites_list.add(self.shell)
            self.count = 0

#SHELL CLASS
class Shell(pygame.sprite.Sprite):
    
    def __init__(self, turretrectx, turretrecty, turretdir):
        
        pygame.sprite.Sprite.__init__(self)

        
        self.imageMaster=pygame.image.load("shell_graphic.png")
        self.imageMaster.convert()
        self.imageMaster.set_colorkey(WHITE)
        self.rect = self.imageMaster.get_rect()


        self.speed = 10
        self.dir = turretdir
        self.x = turretrectx
        self.y = turretrecty
        self.image = pygame.transform.rotate(self.imageMaster,self.dir)
        
    def update(self):
        self.calcVector()
        self.calPos()
        self.rect.center=(self.x,self.y)
        
    def calcVector(self):
        radians=self.dir *math.pi/180
        self.dx=math.cos(radians) * self.speed
        self.dy=math.sin(radians) * self.speed
        self.dy *=-1
    def calPos(self):
        self.x +=self.dx
        self.y +=self.dy

# ROCKET CLASS
class Rocket(pygame.sprite.Sprite):

    # -- Attributes
    # Set speed vector of player
    change_x = 0
    change_y = 0
    acc_x = 0
    acc_y = 0
    rocket_health = 1000
    # -- Methods
    def __init__(self):
        """ Constructor function """
 
        pygame.sprite.Sprite.__init__(self)
 

        self.image = pygame.image.load("rocket.png").convert()
        self.image.set_colorkey(LIGHT_BLUE)

        self.rect = self.image.get_rect()

        
    def update_rocket(self, wall_list, endblock_list):

        #Calculate Gravity
        self.calc_grav()
        #Calculate X Dir Air Resistance
        self.air_resist()
        
        moving_right = False
        moving_left = False
        moving_up = False
        moving_down = False
        
        # Move left/right based on Acceleration
        self.change_x += self.acc_x
        self.rect.x += self.change_x
        counter = 0
        
        #CHECK FOR WALL COLLISIONS HORIZONTAL
        wall_hit_list = pygame.sprite.spritecollide(self, wall_list, False)
        if len(wall_hit_list) > 0:
            self.rocket_health += - 1
        for wall in wall_hit_list:
            counter += 1           

            if self.change_x > 0:
                self.rect.right = wall.rect.left - 5
                moving_right = True
            elif self.change_x < 0:
                self.rect.left = wall.rect.right + 5
                moving_left = True

        if moving_right == True:
            self.change_x = 0
            self.acc_x = -1
        if moving_left == True:
            self.change_x = 0
            self.acc_x = 1


        self.change_y += self.acc_y
        self.rect.y += self.change_y
        counter = 0
        #CHECK FOR WALL COLLISIONS VERTICAL
        wall_hit_list = pygame.sprite.spritecollide(self, wall_list, False)
        if len(wall_hit_list) > 0:
            self.rocket_health += - 1
        for wall in wall_hit_list:
            counter += 1
            if self.change_y > 0:
                self.rect.bottom = wall.rect.top -10
                moving_down = True
            elif self.change_y < 0:
                self.rect.top = wall.rect.bottom + 5
                moving_up = True
                
        if moving_up == True:
            self.acc_y = 0.75
            self.change_y = 0
        if moving_down == True:
            self.acc_y = -1
            self.change_y = 0

 
    def calc_grav(self):

        if self.acc_y == 0:
            self.acc_y = 0.25
        if self.acc_y < 0:
            self.acc_y += 0.25

    def air_resist(self):

        if self.acc_x > 0:
            self.acc_x += -0.25
        elif self.acc_x < 0:
            self.acc_x += 0.25

        if self.change_x > 5:
            self.change_x = 5
        if self.change_x < -5:
            self.change_x = -5
            
        if self.change_x > 0 and self.acc_x == 0:
            self.change_x += -0.5
        elif self.change_x < 0 and self.acc_x == 0:
            self.change_x += 0.5
            
        if self.change_y > 5:
            self.change_y = 5
        if self.change_y < -5:
            self.change_y = -5
            
    def go_left(self):
        self.acc_x = -1
 
    def go_right(self):
        self.acc_x = 1

    def go_up(self):
        self.acc_y = -1

        
##################################################################################        
##################################################################################
################################## GAME CLASS ####################################
##################################################################################
##################################################################################
        
class Game(object):
    
    wall_list = None
    turret_list = None
    all_sprites_list = None
    shell_list = None
    rocket = None
    game_over = False
    level = []
    level_number = 0

    def __init__(self):

        self.game_over = False
        self.level_number = 0
        
        #Create the sprite lists
        self.wall_list = pygame.sprite.Group()
        self.endblock_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.turret_list = pygame.sprite.Group()
        self.shell_list = pygame.sprite.Group()

        #LOAD LEVELS
        for i in range(5):
            l1 = open("level" + str(i) + ".txt","r")
            self.level.append(l1)
        self.level.append("NULL")
        
        #CREATE THE ROCKET
        self.rocketegg = Rocket()
        self.all_sprites_list.add(self.rocketegg)

    def process_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        
    
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[K_LEFT]:
            self.rocketegg.go_left()
        if keys_pressed[K_RIGHT]:
            self.rocketegg.go_right()
        if keys_pressed[K_UP]:
            self.rocketegg.go_up()
        return False
    
    def run_logic(self):

        #UPDATE ROCKET
        self.rocketegg.update_rocket(self.wall_list, self.endblock_list)

        if self.check_end_block() == True:

            if self.level[self.level_number] != "NULL":
                self.load_new_level()
            else:
                self.game_over = True

        #UPDATE TURRETS
        if self.turret_present == True:
            self.turret_list.update(self.rocketegg, self.shell_list, self.all_sprites_list)

        #UPDATE SHELLS
        self.shell_list.update()

        #COLLISIONS BETWEEN ROCKET AND SHELLS
        shell_rocket_hit_list = pygame.sprite.spritecollide(self.rocketegg, self.shell_list, False)
        for shell in shell_rocket_hit_list:

            self.shell_list.remove(shell)
            self.all_sprites_list.remove(shell) 
            self.rocketegg.rocket_health += -1
    
        if self.rocketegg.rocket_health < 0:
            self.game_over = True
                
        #COLLISIONS BETWEEN SHELLS AND WALLS
        shell_wall_hit_list = pygame.sprite.groupcollide(self.shell_list, self.wall_list, False, False)
        for shell in shell_wall_hit_list:
            self.shell_list.remove(shell)
            self.all_sprites_list.remove(shell)
            
    def check_end_block(self):
        for endblock in self.endblock_list:
            if self.rocketegg.rect.colliderect(endblock):
                return True
        return False

    def load_new_level(self):


        #REMOVE THE WALL_LIST AND ENDBLOCK_LIST FROM ALL_SPRITES_LIST
        self.all_sprites_list.remove(self.wall_list)
        self.all_sprites_list.remove(self.endblock_list)
        self.all_sprites_list.remove(self.shell_list)
        self.all_sprites_list.remove(self.turret_list)


        for wall in self.wall_list:
            self.wall_list.remove(wall)
        for endblock in self.endblock_list: 
            self.endblock_list.remove(endblock)
        for shell in self.shell_list:
            self.shell_list.remove(shell)
        for turret in self.turret_list:
            self.turret_list.remove(turret)
        
        #CREATE THE NEW WALL_LIST AND ENDBLOCK_LIST
        #AND TURRET_LIST
        x = -16
        y = 0
        self.turret_present = False
        for line in self.level[self.level_number]:
            for col in line:
                if col == "W":
                    wall = Wall(self.level_number)
                    wall.rect.x = x
                    wall.rect.y = y
                    self.wall_list.add(wall)
                    self.all_sprites_list.add(wall)
                if col == "E":
                    self.endblock = EndBlock()
                    self.endblock.rect.x = x
                    self.endblock.rect.y = y
                    self.endblock_list.add(self.endblock)
                    self.all_sprites_list.add(self.endblock)
                if col == "R":
                    #REPOSITION THE ROCKET FOR THE NEW LEVEL
                    self.rocketegg.rect.topleft = (x, y)
                if col == "T":
                    self.turret_present = True
                    self.turret = Turret(x,y)
                    self.turret_list.add(self.turret)
                    self.all_sprites_list.add(self.turret)
                x += 16
            y += 16
            x = -16
        self.level[self.level_number].seek(0)
        self.level_number = self.level_number + 1
                
    def display_frame(self, screen):
        screen.fill(WHITE)



        if not self.game_over:
            self.all_sprites_list.draw(screen)
        pygame.display.set_caption("Rocket Health: " + str(self.rocketegg.rocket_health))  
        pygame.display.flip()

        
    def player_lose(self):
        if self.game_over == True and self.rocketegg.rocket_health == 0 or self.rocketegg.rocket_health < 0:
            return True
    def player_win(self):
        if self.game_over == True and self.rocketegg.rocket_health > 0:
            return True


##################################################################################        
##################################################################################
################################## MENU CLASS ####################################
##################################################################################
##################################################################################

class Main_Menu(object):

    menu_image = []
    
    def __init__(self):

        #LOAD THE MENU SCREENS
        for i in range(6):
            load = pygame.image.load("menu_image" +str(i) +".png")
            self.menu_image.append(load)
        
        self.start_game = True        
        self.image_load = 0
        self.current_image = self.menu_image[self.image_load]
        
    #MENU EVENT PROCESSING   
    def process_events(self):
        self.current_image = self.menu_image[self.image_load]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.image_load == 0 or self.image_load == 1:
                        self.image_load = 0
                        self.current_image = self.menu_image[self.image_load]
                    elif self.image_load == 2 or self.image_load == 3:
                        self.image_load = 2
                        self.current_image = self.menu_image[self.image_load]
                    elif self.image_load == 4 or self.image_load == 5:
                        self.image_load = 4
                        self.current_image = self.menu_image[self.image_load]
                    self.start_game = True

                if event.key == pygame.K_DOWN:
                    if self.image_load == 0 or self.image_load == 1:
                        self.image_load = 1
                        self.current_image = self.menu_image[self.image_load]
                    elif self.image_load == 2 or self.image_load == 3:
                        self.image_load = 3
                        self.current_image = self.menu_image[self.image_load]
                    elif self.image_load == 4 or self.image_load == 5:
                        self.image_load = 5
                        self.current_image = self.menu_image[self.image_load]
                    self.start_game = False
                if event.key == pygame.K_RETURN:
                    if self.start_game == True:
                        return True
                    elif self.start_game == False:
                        pygame.quit() 
        return False 
            
    #DISPLAY MENU        
    def display_frame(self, screen):

        screen.blit(self.current_image, (0,0))
        pygame.display.flip()
        
        
    
def main():

    pygame.init()
    
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    
    pygame.display.set_caption("ROCKET EGG v1.4")
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()
    
    main_menu = Main_Menu()



    done = False
    menu_done = False
    clock = pygame.time.Clock()


    game = Game()
    game.load_new_level()
    
    # Main game loop
    while not done:
        #Menu Loop
        while not menu_done:
            
            if  menu_done == False and game.game_over == True:
                game.level_number = 0
                game.load_new_level()
                game.rocketegg.rocket_health = 7
                game.game_over = False
            elif menu_done == False and game.game_over == False:
                menu_done = main_menu.process_events()
                main_menu.display_frame(screen)   
            clock.tick(60)

        #Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()
        
        #Update object positions, check for collisions
        game.run_logic()


              
        #Draw the current frame
        game.display_frame(screen)

        if (game.player_win()):
            menu_done = False
            main_menu.image_load = 2
                
        if (game.player_lose()):
            menu_done = False
            main_menu.image_load = 4
                
            
        # Pause for the next frame
        clock.tick(60)
 
    # Close window and exit
    pygame.quit()
 
# Call the main function, start up the game
if __name__ == "__main__":
    main()
