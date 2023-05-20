import pygame
import os
pygame.font.init()
pygame.mixer.init()


WIDTH,HEIGHT=900,500
WIN=pygame.display.set_mode((WIDTH,HEIGHT))

SSW = 60 #Spaceship Width
SSH = 50 #Spaceship Height

HEALTH_FONT = pygame.font.SysFont('Broadway',22)
WINNER_FONT= pygame.font.SysFont('Broadway',70)

RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')
BULLET_COLLISION_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH,HEIGHT))

YLW_SPCSHP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
RED_SPCSHP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YLW_SPCSHP_IMAGE,(SSW,SSH)),90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPCSHP_IMAGE,(SSW,SSH)),-90)

FPS = 60
RED_VELOC = 5
YELLOW_VELOC = 5

RED_HIT= pygame.USEREVENT+1
YELLOW_HIT= pygame.USEREVENT+2



def draw(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health,red_wins,yellow_wins):
    WIN.blit(SPACE,(0, 0))
    if red_health>=5:
        red_health_text = HEALTH_FONT.render("HEALTH: " + str(red_health),1,(0,255,0))
    else:
        red_health_text = HEALTH_FONT.render("HEALTH: " + str(red_health),1,(255,0,0))
    if yellow_health>=5:
        yellow_health_text = HEALTH_FONT.render("HEALTH: " + str(yellow_health),1,(0,255,0))
    else:
        yellow_health_text = HEALTH_FONT.render("HEALTH: " + str(yellow_health),1,(255,0,0))
    red_wins_text = HEALTH_FONT.render("Player 2 Wins: "+str(red_wins),1,(255,255,255))
    yellow_wins_text = HEALTH_FONT.render("Player 1 Wins: "+str(yellow_wins),1,(255,255,255))
    
    WIN.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10,10))
    WIN.blit(yellow_health_text,(10,10))
    WIN.blit(red_wins_text,(WIDTH - red_wins_text.get_width() - 10,50))
    WIN.blit(yellow_wins_text,(10,50))
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()

def red_movement(red,pressed_key,joysticks):
    if (pressed_key[pygame.K_LEFT] or (bool(joysticks) and joysticks[0].get_axis(0)<0)) and red.x >WIDTH/2 - 10:
            red.x-=RED_VELOC
    if (pressed_key[pygame.K_RIGHT] or (bool(joysticks) and joysticks[0].get_axis(0)>0)) and red.x<=WIDTH-SSH-5:
            red.x+=RED_VELOC
    if (pressed_key[pygame.K_UP] or (bool(joysticks) and joysticks[0].get_axis(1)<0)) and red.y>=5:
            red.y-=RED_VELOC
    if (pressed_key[pygame.K_DOWN] or (bool(joysticks) and joysticks[0].get_axis(1)>0)) and red.y<=HEIGHT-SSW-5:
            red.y+=RED_VELOC


def yellow_movement(yellow,pressed_key,joysticks):
    if (pressed_key[pygame.K_a] or (bool(joysticks) and joysticks[1].get_axis(0)<0)) and yellow.x >5:
            yellow.x-=YELLOW_VELOC
    if (pressed_key[pygame.K_d] or (bool(joysticks) and joysticks[1].get_axis(0)>0)) and yellow.x < WIDTH/2 -30 -SSH:
            yellow.x+=YELLOW_VELOC
    if (pressed_key[pygame.K_w] or (bool(joysticks) and joysticks[1].get_axis(1)<0)) and yellow.y>5:
            yellow.y-=YELLOW_VELOC
    if (pressed_key[pygame.K_s] or (bool(joysticks) and joysticks[1].get_axis(1)>0)) and yellow.y < HEIGHT - SSW -5:
            yellow.y+=YELLOW_VELOC

def handle_bullets(red_bullets, yellow_bullets, red, yellow):
    for bullet in red_bullets:
        bullet.x-=12
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        if bullet.x<=0:
            red_bullets.remove(bullet)
    for bullet in yellow_bullets:
        bullet.x+=12
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        if bullet.x >= WIDTH:
            yellow_bullets.remove(bullet)

def shoot_red(red, red_bullets):
    if(len(red_bullets)<=6):
        BULLET_FIRE_SOUND.play()
        bullet = pygame.Rect(red.x, red.y + SSW/2 -2, 7, 7)
        red_bullets.append(bullet)
def shoot_yellow(yellow, yellow_bullets):
    if len(yellow_bullets)<=3:
        BULLET_FIRE_SOUND.play()
        bullet = pygame.Rect(yellow.x + SSH, yellow.y + SSW/2 -3, 7, 7)
        yellow_bullets.append(bullet)

def draw_winner(text):
    wintext = WINNER_FONT.render(text,1,(255,255,255))
    WIN.blit(wintext,(WIDTH//2 - wintext.get_width()//2,HEIGHT//2 - wintext.get_height()//2))
    pygame.display.update()
    pygame.time.delay(1500)


def main():
    red = pygame.Rect(800,200,SSW,SSH)
    yellow = pygame.Rect(0,200,SSW,SSH)
    red_bullets = []
    yellow_bullets = []
    red_health = 15
    yellow_health = 15
    red_wins = 0
    yellow_wins = 0
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        pressed_key=pygame.key.get_pressed()
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    shoot_red(red, red_bullets)
                if event.key == pygame.K_q and len(yellow_bullets)<=3:
                   shoot_yellow(yellow, yellow_bullets)
            if event.type==pygame.JOYBUTTONDOWN:
                if joysticks[0].get_button(3):
                    shoot_red(red,red_bullets)
                if joysticks[1].get_button(3):
                    shoot_yellow(yellow,yellow_bullets)
                if joysticks[0].get_button(5):
                    global RED_VELOC
                    RED_VELOC = 10
                if joysticks[1].get_button(5):
                    global YELLOW_VELOC
                    YELLOW_VELOC = 10
            if event.type==pygame.JOYBUTTONUP:
                if not joysticks[0].get_button(5):
                    RED_VELOC = 5
                if not joysticks[1].get_button(5):
                    YELLOW_VELOC = 5
            if event.type == RED_HIT:
                red_health-=1
                BULLET_COLLISION_SOUND.play()
            if event.type == YELLOW_HIT:
                BULLET_COLLISION_SOUND.play()
                yellow_health-=1
        winner_text = ""
        if red_health <= 0:
            winner_text="Player 1 Wins!!"
        if yellow_health <= 0:
            winner_text="Player 2 Wins!!"
        if winner_text != "":
            red_bullets.clear()
            yellow_bullets.clear()
            draw_winner(winner_text)
            
            if(red_health<=1):
                yellow_wins+=1
            elif(yellow_health<=1):
                red_wins+=1
            red_health = yellow_health = 15
                
        
        

        red_movement(red,pressed_key,joysticks)
        yellow_movement(yellow,pressed_key,joysticks)
        draw(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health,red_wins,yellow_wins)
        handle_bullets(red_bullets, yellow_bullets, red, yellow)
        

    pygame.quit()

if __name__ == "__main__":
    main()