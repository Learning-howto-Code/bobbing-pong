import pygame
import time

pygame.init()
screen=pygame.display.set_mode((1280,720))
pygame.display.set_caption("My Game")
clock=pygame.time.Clock()
running = True
dt=0

ball_pos = pygame.Vector2(1080, 720/2)

ball = pygame.Rect(ball_pos.x, ball_pos.y, 10, 10)
player = pygame.Rect(100, 300, 10, 100)
bot = pygame.Rect(1200,300,10,100)

font = pygame.font.Font(None,72)
ball_speed_x = 10
ball_speed_y = 2

player_speed_x=0
player_speed_y=0

bot_speed_x=0
bot_speed_y=0

bot_score = 0
player_score = 0
# key moving
def keys():
    global player_speed_x, player_speed_y
    keys=pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        player.y +=10
        player_speed_y=10
    if keys[pygame.K_UP]:
        player.y -=10
        player_speed_y=-10
    if keys[pygame.K_LEFT]:
        player.x -=10
        player_speed_x=-10
    if keys[pygame.K_RIGHT] and player.x <1280/2:
        player.x +=10
        player_speed_x=10
    return player_speed_x, player_speed_y
def bot_move():
    global bot_speed_x, bot_speed_y
    if bot.y<ball_pos.y:
        bot_speed_y=5
        bot.y +=bot_speed_y
    if bot.y>ball_pos.y:
        bot_speed_y=-5
        bot.y +=bot_speed_y
while running:

    for event in pygame.event.get(): # closees pygame
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")  # Fill the screen with black color

    text = font.render(str(player_score), True, "white")
    screen.blit(text,(1280/2-100,50))

    text = font.render(str(bot_score), True, "white")
    screen.blit(text,(1280/2+100,50))

    pygame.draw.circle(screen, "white", ball_pos,10)
    pygame.draw.rect(screen, "white", player)
    pygame.draw.rect(screen,"white", bot)
    bot_move()
    player_speed_x, player_speed_y=keys() 
    print(player_speed_x, player_speed_y)


# collision checks
    if player.colliderect(ball):
        if player_speed_x==0:
            ball_speed_x = -ball_speed_x
        else:
            ball_speed_x = -abs(player_speed_x)*1.2
        if player_speed_y==0:
            ball_speed_y = -ball_speed_y
        else:
            ball_speed_y=-ball_speed_y*abs(player_speed_y)*.2
    if bot.colliderect(ball):
         if bot.colliderect(ball):
            if bot_speed_x==0:
                ball_speed_x = -ball_speed_x
            else:
                ball_speed_x = -abs(bot_speed_x)*1.2
            if bot_speed_y==0:
                ball_speed_y = -ball_speed_y
            else:
                ball_speed_y=-ball_speed_y*abs(bot_speed_y)*.2
    
    if ball_pos.y<0 or ball_pos.y>720:
        ball_speed_y=-ball_speed_y
    if ball_pos.x<0: #ball lost on your side
        time.sleep(1)
        bot_score +=1
        ball_pos = (1280/2, 720/2)
        ball_speed_x = 10
        ball_speed_y = 2
    if ball_pos.x>1280: # ball lost on bot side
        player_score +=1
        ball_pos = (1280/2, 720/2)
        ball_speed_x = 10
        ball_speed_y = 2
    ball_pos.x -=ball_speed_x
    ball_pos.y -=ball_speed_y
    ball.center = ball_pos
    pygame.display.flip()   # Update the display
    clock.tick(60)   

    dt=clock.tick(60) / 1000  
pygame.quit()      
