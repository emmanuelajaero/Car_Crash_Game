#Imports
import pygame, sys
from pygame.locals import *
import random, time

#Initialzing 
pygame.init()

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
HIGHEST_SCORE = 0
SPEED = 5
SCORE = 0
LIFE = 6
LEVEL = 1

#return highest_score
def get_highest_score(file_name):
    game_file = {}
    try:
        game_file = open(file_name, "r")    #Open file for reading
        data = game_file.read()
        game_file.close()
        game_file = data
    except Exception:
        game_file = open(file_name, "w")    #if the file doesn't exit() create the file
        game_file.close()
        game_file = ""    
    game_file = game_file.split("\n")   #split the opened file by new line
    if len(game_file) > 0:              #if the file is not empty return the content
        try:
            return int(game_file[0])
        except Exception:
            return 0
    return 0                           #return zero if no content


#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
pause_game = font.render("PAUSE", True, BLACK)

#background music
pygame.mixer.music.load("background.wav")  #load the music file
pygame.mixer.music.play(-1)    #play the music in loop

#load backgroud image
background = pygame.image.load("AnimatedStreet.png")

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.surf = pygame.Surface((42, 70))
        self.rect = self.surf.get_rect(center = (random.randint(40,SCREEN_WIDTH-40)
                                                 , 0))

      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.surf = pygame.Surface((40, 75))
        self.rect = self.surf.get_rect(center = (160, 520))
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
       #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -5)
       #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(0,5)
        
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                  

#Setting up Sprites        
P1 = Player()
E1 = Enemy()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

#Adding a new User event 
# INC_SPEED = pygame.USEREVENT + 1
# pygame.time.set_timer(INC_SPEED, 1000)


HIGHEST_SCORE = get_highest_score("highest_score.txt")  #update the global variable for highest_score
#Game Loop
running = True
while running:
      
    #Cycles through all events occuring  
    for event in pygame.event.get():
        # if event.type == INC_SPEED:
        #       SPEED += 0.5      
        if event.type == QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            #if the key pressed is p to pause
            if event.key == pygame.K_p:
                DISPLAYSURF.blit(pause_game, (SCREEN_WIDTH//4,250))    #write pause on screen
                highest_score = font_small.render("press p to play", True, BLACK)
                DISPLAYSURF.blit(highest_score, (SCREEN_WIDTH//3,320))
                pygame.display.update()                         #update the screen
                
                #start loop till player decide to restart
                keep_loop = True
                while keep_loop:
                    #track events
                    for event in pygame.event.get():
                        #catch key press
                        if event.type == pygame.KEYDOWN:
                            #catch p press
                            if event.key == pygame.K_p:     #break from the loop
                                keep_loop = False
                                break


    #update the screen with background and score data
    DISPLAYSURF.blit(background, (0,0))
    highest_score = font_small.render("HIGH SCORE:"+str(HIGHEST_SCORE), True, BLACK)
    DISPLAYSURF.blit(highest_score, (10,10))
    scores = font_small.render("SCORE:"+str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,30))
    lifes = font_small.render("LIFES:"+str(LIFE), True, BLACK)
    DISPLAYSURF.blit(lifes, (10,50))
    levels = font_small.render("LEVEL:"+str(LEVEL), True, BLACK)
    DISPLAYSURF.blit(levels, (10,70))

    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    #To be run if collision occurs between Player and Enemy
    # if pygame.sprite.spritecollideany(P1, enemies):
    #       pygame.mixer.Sound('crash.wav').play()
    #       time.sleep(1)
                   
    #       DISPLAYSURF.fill(RED)
    #       DISPLAYSURF.blit(game_over, (30,250))
          
    #       pygame.display.update()
    #       for entity in all_sprites:
    #             entity.kill() 
    #       time.sleep(2)
    #       pygame.quit()
    #       sys.exit()        


    #look for collision between player and enemies
    player_hit = pygame.sprite.spritecollide(P1, enemies, False)
    #check if there is a hit
    if len(player_hit) > 0: #check for the specific enemy collided with
        # pygame.mixer.Sound('crash.wav').play()
        # time.sleep(1)
        for enemy_sprite in player_hit:
            pygame.mixer.Sound('crash.wav').play()  #load explosion sound

            time.sleep(1)

            LIFE -= 1                             #decrement the playing life
            enemy_sprite.kill()                             #remove the enemy involved in the collision
            enemy = Enemy() #create a new enemy
            all_sprites.add(enemy)  #add the enemy to the sprite group for update
            enemies.add(enemy)  #add the enemy to the sprite group for that keeps track of the enemies sprite


    #check if life has finished 
    if LIFE <= 0:     #if life is now zero
        # gameover = font_small.render("GAME OVER", True, BLACK)
        # DISPLAYSURF.blit(gameover, (SCREEN_WIDTH//3,300))
        DISPLAYSURF.blit(game_over, (30,250))
        restart_instr = font_small.render("press q to quit and r to restart", True, BLACK)
        DISPLAYSURF.blit(restart_instr, (SCREEN_WIDTH//7,330))
        pygame.display.update()

        #fetch the initial highest score in storage
        HIGHEST_SCORE = get_highest_score("highest_score.txt")
        if SCORE > HIGHEST_SCORE: #check if the current score is more than the iniitial highest_score then update the stored highest score
            # update the stored highest score with the new highest score
            score_file = open("highest_score.txt", "w")
            score_file.write(str(SCORE))
            score_file.close()
            HIGHEST_SCORE = SCORE
        
        #wait for user to either quit or replay the game
        keep_loop = True
        while keep_loop:
            #track events
            for event in pygame.event.get():
                #check if key press event occured
                if event.type == pygame.KEYDOWN:
                    #if q is pressed quit the game by setting running to False this will cause the game loop to end
                    if event.key == pygame.K_q:
                        running = False
                        keep_loop = False
                    #if r key is pressed restart the game by initializing the gaming parameters to the original values
                    if event.key == pygame.K_r:
                        keep_loop = False
                        HIGHEST_SCORE = get_highest_score("highest_score.txt")  #update the global variable for highest_score
                        SPEED = 5           #enemy SPEED = 5
                        SCORE = 0           #score to 0
                        LIFE = 6            #remaing life to 6
                        LEVEL = 1           #current level to 1

                        all_sprites.empty()     #clear all the sprite fron the screen
                        enemies.empty()     #remove all the enemies sprite
                        P1 = Player()       #initialize the player object(sprite)
                        all_sprites.add(P1)     #include the player sprite in the group of sprites
                        enemy = Enemy()     #create on new enemy
                        all_sprites.add(enemy)  #set the enemy for screen update
                        enemies.add(enemy)  #add the enemy to the group that keeps track of the enemies
                        break
    LEVEL_NEW = SCORE//10 if SCORE//10 > 0 else 1
    if LEVEL_NEW != LEVEL:
        LEVEL = LEVEL_NEW
        SPEED += LEVEL



    pygame.display.update()
    FramePerSec.tick(FPS)
    
#Update high score before quiting the game
HIGHEST_SCORE = get_highest_score("highest_score.txt")
if SCORE > HIGHEST_SCORE:
    # print("current : ", current_score, "\nhigh : ", highest_score)
    score_file = open("highest_score.txt", "w")
    score_file.write(str(SCORE))
    score_file.close()
    HIGHEST_SCORE = SCORE

#close the python program
pygame.quit()


