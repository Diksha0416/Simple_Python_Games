import pygame
import random
import os
pygame.init()

# colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)

# Creating Window
screen_width = 1500
screen_height = 750
gameWindow = pygame.display.set_mode((screen_width,screen_height))

#image
bgimag = pygame.image.load("back_inside.jpg")
bgimag = pygame.transform.scale(bgimag, (screen_width, screen_height)).convert_alpha()

bgimag2 = pygame.image.load("back_first.png")
bgimag2 = pygame.transform.scale(bgimag2, (screen_width, screen_height)).convert_alpha()

bgimag3 = pygame.image.load("Game_over.png")
bgimag3 = pygame.transform.scale(bgimag3, (screen_width, screen_height)).convert_alpha()

#Title
pygame.display.set_caption("SnakeswithDiksha")
pygame.display.update()


clock = pygame.time.Clock()
# game loop
font = pygame.font.SysFont(None, 55)

# Global flag to control the game exit
exit_game = False

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(colorWindow, color, snk_list, snake_size):
    for i,(x,y) in enumerate(snk_list):
        if i == len(snk_list) - 1:
           pygame.draw.rect(gameWindow, blue, [x, y, snake_size, snake_size])
        else:
           pygame.draw.rect(gameWindow, black, [x, y, snake_size, snake_size])

def welcome():
    global exit_game
    while not exit_game:
        gameWindow.fill((0,0,0))
        gameWindow.blit(bgimag2,(0,0))
        text_screen("Click space to play", (144,245,0), 550, 600)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('Game_song.mp3')
                    pygame.mixer.music.play()
                    game_loop()
        
        pygame.display.update()
        clock.tick(60)


def game_loop() :
        #Game specific variables
    global exit_game
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snake_size = 20
    food_margin = 100
    food_x = random.randint(food_margin,screen_width - food_margin)
    food_y = random.randint(food_margin,screen_height - food_margin)
    score = 0
    init_velocity = 4
    fps = 60 # kitne frames a rhe ha per sec
    snk_list = []
    snk_length = 1

    # Check if hiscore file exists
    if (not os.path.exists("highscore.txt")):
        with open ("highscore.txt", 'w') as f:
            f.write("0")
    with open("highscore.txt", "r")as f:
        hiscore = f.read()
    while not exit_game:
        if game_over:
            with open("highscore.txt", "w")as f:
                f.write(str(hiscore))
            gameWindow.blit(bgimag3,(0,0))
            text_screen("Score: " + str(score ), red, 5, 5)
            text_screen("Press Enter to play again", red, 550 ,50 )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x += init_velocity
                        velocity_y = 0
                    
                    if event.key == pygame.K_LEFT:
                        velocity_x -= init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y += init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_UP:
                        velocity_y -= init_velocity
                        velocity_x = 0

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<20 and abs(snake_y - food_y)<20:
                score +=10
                food_x = random.randint(food_margin,screen_width - food_margin)
                food_y = random.randint(food_margin,screen_height - food_margin)
    
                snk_length +=5
                if score>int (hiscore):
                    hiscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimag,(0,0))
            text_screen("Score: " + str(score ) + ' High Score:' + str(hiscore), red, 5, 5)

            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
            
            # to show atleast one block in starting
            head =[]            
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if snake_x<0 or snake_x>screen_width - snake_size or snake_y<0 or snake_y>screen_height - snake_size:
                game_over = True
                pygame.mixer.music.load('over.mp3')
                pygame.mixer.music.play()

            if head in snk_list[:-1]: # -1 refers to tail
                game_over = True
                pygame.mixer.music.load('over.mp3')
                pygame.mixer.music.play()
            plot_snake(gameWindow, black, snk_list, snake_size)
        clock.tick(fps)
        pygame.display.update()
welcome()
pygame.quit()
quit()
