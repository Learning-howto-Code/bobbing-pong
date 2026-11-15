import pygame
import time
import cv2 as cv


pygame.init()
screen=pygame.display.set_mode((1280,720))
pygame.display.set_caption("My Game")
clock=pygame.time.Clock()
running = True
dt=0

state ="start"
ball_pos = pygame.Vector2(1080, 720/2)

ball = pygame.Rect(ball_pos.x, ball_pos.y, 10, 10)
player = pygame.Rect(100, 300, 10, 100)
bot = pygame.Rect(1200,300,10,100)

font = pygame.font.Font(None,72)
ball_speed_x = 20
ball_speed_y = 2

player_speed_x=0
player_speed_y=0

bot_speed_x=0
bot_speed_y=0

bot_score = 0
player_score = 0
# key moving
box_height=1
def keys():
    global player_speed_x, player_speed_y
    player.x=box_height
    return player_speed_x, player_speed_y
def bot_move():
    global bot_speed_x, bot_speed_y
    if bot.y<ball_pos.y:
        bot_speed_y=3
        bot.y +=bot_speed_y
    if bot.y>ball_pos.y:
        bot_speed_y=-3
        bot.y +=bot_speed_y


faceCascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")

OUTPUT_SIZE_WIDTH = 775
OUTPUT_SIZE_HEIGHT = 600
rectangleColor = (0, 0, 255)

capture = cv.VideoCapture(0)
if not capture.isOpened():
    raise SystemExit("Could not open camera")

def face():
        rc, fullSizeBaseImage = capture.read()
        baseImage = cv.resize(fullSizeBaseImage, (640, 480))   # was 320x240
        resultImage = baseImage.copy()

        gray = cv.cvtColor(baseImage, cv.COLOR_BGR2GRAY)
        gray = cv.equalizeHist(gray)                           # helps with dim or uneven light

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,     # finer size steps
            minNeighbors=4,      # a bit less strict
            minSize=(20, 20),    # allow small, distant faces
        )

        # find the biggest face
        maxArea = 0
        x = y = w = h = 0
        for (_x, _y, _w, _h) in faces:
            if _w * _h > maxArea:
                x, y, w, h = _x, _y, _w, _h
                maxArea = _w * _h

        # draw once, after the loop
        if maxArea > 0:
            cv.rectangle(resultImage, (x - 10, y - 20), (x + w + 10, y + h + 20), rectangleColor, 2)

        largeResult = cv.resize(resultImage, (OUTPUT_SIZE_WIDTH, OUTPUT_SIZE_HEIGHT))

        if maxArea > 0:
            center_y = y + h / 2
            y_norm = center_y / baseImage.shape[0]       # 0 = top, 1 = bottom
            y_norm = max(0.0, min(1.0, y_norm))
            print(round(y_norm, 3))
            y_norm = (y_norm-.2)/.3
        else:
            y_norm = 0.5  # Default value if no face is detected
        return y_norm


while running:
    for event in pygame.event.get(): # closees pygame
        if event.type == pygame.QUIT:
            running = False
    if player_score==9 or bot_score==9:
        state="end"
    if state=="start":
        screen.blit(pygame.image.load("img/start.png").convert(),(0,0))
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            player_score=0
            bot_score=0
            state="game"
    elif state=="end":
        if bot_score>player_score:
            screen.blit(pygame.image.load("img/lose.png").convert(),(0,0))
        else:
            screen.blit(pygame.image.load("img/win.png").convert(),(0,0))
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            player_score=0
            bot_score=0
            state="start"
    if state=="game":
        

        screen.fill("black")  # Fill the screen with black color

        text = font.render(str(player_score), True, "white")
        screen.blit(text,(1280/2-100,50))

        text = font.render(str(bot_score), True, "white")
        screen.blit(text,(1280/2+100,50))

        pygame.draw.circle(screen, "white", ball_pos,10)
        pygame.draw.rect(screen, "white", player)
        pygame.draw.rect(screen,"white", bot)
        bot_move()
        player.centery=face()*720
        print(player_speed_x, player_speed_y)


    # collision checks
        if player.colliderect(ball):
            if player_speed_x==0:
                ball_speed_x = -ball_speed_x
            else:
                ball_speed_x = -abs(player_speed_x)*1.2
            if player_speed_y==0:
                ball_speed_y = ball_speed_y
            else:
                ball_speed_y=ball_speed_y+abs(player_speed_y)-7
        if bot.colliderect(ball):
            if bot.colliderect(ball):
                if bot_speed_x==0:
                    ball_speed_x = -ball_speed_x
                else:
                    ball_speed_x = -abs(bot_speed_x)*1.2
                if bot_speed_y==0:
                    ball_speed_y = ball_speed_y
                else:
                    ball_speed_y=ball_speed_y+abs(bot_speed_y)-7
        
        if ball_pos.y<0 or ball_pos.y>720:
            ball_speed_y=-ball_speed_y
        if ball_pos.x<0: #ball lost on your side
            time.sleep(.3)
            bot_score +=1
            ball_pos.update((1280/2, 720/2))
            ball_speed_x = 20
            ball_speed_y = 2
        if ball_pos.x>1280: # ball lost on bot side
            player_score +=1
            ball_pos.update((1280/2, 720/2))
            ball_speed_x = 20
            ball_speed_y = 2
        ball_pos.x -=ball_speed_x
        ball_pos.y -=ball_speed_y
        ball.center = ball_pos
        

    pygame.display.flip()   # Update the display
    clock.tick(60)   
pygame.quit()    
