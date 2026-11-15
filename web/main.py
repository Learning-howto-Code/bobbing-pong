import asyncio
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

start_img = pygame.image.load("img/start.png").convert()
win_img = pygame.image.load("img/win.png").convert()
lose_img = pygame.image.load("img/lose.png").convert()
font = pygame.font.Font(None, 72)

ball_pos = pygame.Vector2(1080, 720 / 2)
ball = pygame.Rect(ball_pos.x, ball_pos.y, 10, 10)
player = pygame.Rect(100, 300, 10, 100)
bot = pygame.Rect(1200, 300, 10, 100)

ball_speed_x = 20
ball_speed_y = 2
player_speed_x = player_speed_y = 0
bot_speed_x = bot_speed_y = 0
bot_score = player_score = 0
state = "start"


def keys():
    global player_speed_x, player_speed_y
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_DOWN]:
        player.y += 10
        player_speed_y = 10
    if pressed[pygame.K_UP]:
        player.y -= 10
        player_speed_y = -10
    if pressed[pygame.K_LEFT]:
        player.x -= 10
        player_speed_x = -10
    if pressed[pygame.K_RIGHT] and player.x < 1280 / 2:
        player.x += 10
        player_speed_x = 10
    return player_speed_x, player_speed_y


def bot_move():
    global bot_speed_y
    if bot.y < ball_pos.y:
        bot_speed_y = 5
        bot.y += bot_speed_y
    if bot.y > ball_pos.y:
        bot_speed_y = -5
        bot.y += bot_speed_y


async def main():
    global state, ball_speed_x, ball_speed_y, player_score, bot_score
    global player_speed_x, player_speed_y
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if state == "start":
                    player_score = bot_score = 0
                    state = "game"
                elif state == "end":
                    state = "start"

        if player_score == 9 or bot_score == 9:
            state = "end"

        if state == "start":
            screen.blit(start_img, (0, 0))

        elif state == "end":
            screen.blit(lose_img if bot_score > player_score else win_img, (0, 0))

        elif state == "game":
            screen.fill("black")
            screen.blit(font.render(str(player_score), True, "white"), (1280 / 2 - 100, 50))
            screen.blit(font.render(str(bot_score), True, "white"), (1280 / 2 + 100, 50))
            pygame.draw.circle(screen, "white", ball_pos, 10)
            pygame.draw.rect(screen, "white", player)
            pygame.draw.rect(screen, "white", bot)

            bot_move()
            player_speed_x, player_speed_y = keys()

            # collision checks
            if player.colliderect(ball):
                if player_speed_x == 0:
                    ball_speed_x = -ball_speed_x
                else:
                    ball_speed_x = -abs(player_speed_x) * 1.2
                if player_speed_y != 0:
                    ball_speed_y = ball_speed_y + abs(player_speed_y) - 7
            if bot.colliderect(ball):
                if bot_speed_x == 0:
                    ball_speed_x = -ball_speed_x
                else:
                    ball_speed_x = -abs(bot_speed_x) * 1.2
                if bot_speed_y != 0:
                    ball_speed_y = ball_speed_y + abs(bot_speed_y) - 7

            if ball_pos.y < 0 or ball_pos.y > 720:
                ball_speed_y = -ball_speed_y
            if ball_pos.x < 0:
                await asyncio.sleep(0.3)     # was time.sleep
                bot_score += 1
                ball_pos.update(1280 / 2, 720 / 2)
                ball_speed_x, ball_speed_y = 20, 2
            if ball_pos.x > 1280:
                player_score += 1
                ball_pos.update(1280 / 2, 720 / 2)
                ball_speed_x, ball_speed_y = 20, 2

            ball_pos.x -= ball_speed_x
            ball_pos.y -= ball_speed_y
            ball.center = ball_pos

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)   # hand control back to the browser every frame

    pygame.quit()


asyncio.run(main())