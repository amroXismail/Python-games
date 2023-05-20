from pickle import FALSE
from platform import platform
from re import A
import pygame as pyg
import os

pyg.font.init()
pyg.mixer.init(frequency=22050, size=-8, channels=2, buffer=4096)



HEALTH_FONT = pyg.font.SysFont('Broadway',22)
WINNER_FONT= pyg.font.SysFont('Broadway',70)

ONE_BULLET_AUTO_SOUND = pyg.mixer.Sound('Assets/One bullet auto.mp3')
AUTO_FIRE_SOUND1 = pyg.mixer.Sound('Assets/Auto fire.mp3')
AUTO_FIRE_SOUND2 = pyg.mixer.Sound('Assets/Auto fire.mp3')
PISTOL_FIRE_SOUND = pyg.mixer.Sound('Assets/Pistol Fire.mp3')
BODY_COLLISION_SOUND = pyg.mixer.Sound('Assets/Body impact.mp3')
PLATFORM_COLLISION_SOUND = pyg.mixer.Sound('Assets/Concrete impact.mp3')
BOX_COLLISION_SOUND = pyg.mixer.Sound('Assets/Metal impact.mp3')
EMPTY_MAG_SOUND = pyg.mixer.Sound('Assets/Empty mag.mp3')
JETPACK_SOUND = pyg.mixer.Sound('Assets/Jetpack2.mp3')
RELOAD_SOUND_AUTO1 = pyg.mixer.Sound('Assets/Reload.mp3')
RELOAD_SOUND_AUTO2 = pyg.mixer.Sound('Assets/Reload.mp3')
RELOAD_SOUND_PISTOL1 = pyg.mixer.Sound('Assets/Reload2.mp3')
RELOAD_SOUND_PISTOL2 = pyg.mixer.Sound('Assets/Reload2.mp3')

GUN_COCKING_SOUND = pyg.mixer.Sound('Assets/Gun Cocking.mp3')
FOOTSTEPS_SOUND2 = pyg.mixer.Sound('Assets/Footsteps.mp3')
FOOTSTEPS_SOUND1 = pyg.mixer.Sound('Assets/Footsteps.mp3')
MUSIC = pyg.mixer.Sound('Assets/Joshua McLean - Mountain Trials ♫.mp3')

AUTO_MAG = 30
PISTOL_MAG = 10

AUTO = 1
PISTOL = 2
ICE_MONSTER_PISTOL_SIZE = (85,85)
ICE_MONSTER_AUTO_SIZE = (129,85)

FLYING_PISTOL_SURF = pyg.transform.scale(pyg.image.load(os.path.join('Assets','ice monster pistol gun flying.png')),ICE_MONSTER_PISTOL_SIZE)
FLYING_AUTO_SURF = pyg.transform.scale(pyg.image.load(os.path.join('Assets','ice monster machine gun flying.png')),ICE_MONSTER_AUTO_SIZE)

WALKING_PISTOL_LIST_SURF = [
pyg.transform.scale(pyg.image.load(os.path.join('Assets','ice monster pistol gun still.png')),ICE_MONSTER_PISTOL_SIZE),
pyg.transform.scale(pyg.image.load(os.path.join('Assets','ice monster pistol gun animation 1.png')),ICE_MONSTER_PISTOL_SIZE),
pyg.transform.scale(pyg.image.load(os.path.join('Assets','ice monster pistol gun animation 2.png')),ICE_MONSTER_PISTOL_SIZE),
pyg.transform.scale(pyg.image.load(os.path.join('Assets','ice monster pistol gun animation 3.png')),ICE_MONSTER_PISTOL_SIZE)
]
WALKING_AUTO_LIST_SURF = [
pyg.transform.scale(pyg.image.load(os.path.join('Assets','ice monster machine gun still.png')),ICE_MONSTER_AUTO_SIZE),
pyg.transform.scale(pyg.image.load(os.path.join('Assets','ice monster machine gun animation 1.png')),ICE_MONSTER_AUTO_SIZE),
pyg.transform.scale(pyg.image.load(os.path.join('Assets','ice monster machine gun animation 2.png')),ICE_MONSTER_AUTO_SIZE),
pyg.transform.scale(pyg.image.load(os.path.join('Assets','ice monster machine gun animation 3.png')),ICE_MONSTER_AUTO_SIZE)
]

GUN_WIDTH = FLYING_AUTO_SURF.get_width() - FLYING_PISTOL_SURF.get_width()
JET_WIDTH = FLYING_PISTOL_SURF.get_width()/5

class character:
    auto_mag = AUTO_MAG
    pistol_mag = PISTOL_MAG
    current_weapon = AUTO
    current_index=0
    def __init__(self,animation_list_pistol_surf,flying_pistol_surf,animation_list_auto_surf,flying_auto_surf,pos) -> None:
        self.animation_list_pistol_surf = animation_list_pistol_surf
        self.flying_pistol_surf = flying_pistol_surf
        self.animation_list_auto_surf = animation_list_auto_surf
        self.flying_auto_surf = flying_auto_surf
        self.pos = pos
        self.current_surf = animation_list_auto_surf[0]
  
    
    def shoot(self):
        if self.current_weapon == AUTO:
            if self.auto_mag > 0:
                self.auto_mag -= 1
        elif self.current_weapon == PISTOL:
            if self.pistol_mag > 0:
                PISTOL_FIRE_SOUND.play()
                self.pistol_mag -=1
    def animate(self):
        if self.current_weapon == AUTO:
            if self.current_index == self.animation_list_auto_surf.__len__()-1:
                self.current_index = 0
            else:
                self.current_index+=1
            self.current_surf = self.animation_list_auto_surf[self.current_index]
        elif self.current_weapon == PISTOL:
            if self.current_index == self.animation_list_pistol_surf.__len__()-1:
                self.current_index = 0
            else:
                self.current_index+=1
                self.current_surf = self.animation_list_pistol_surf[self.current_index]
    def animate_reverse(self):
        if self.current_weapon == AUTO:
            if self.current_index==0:
                self.current_index = self.animation_list_auto_surf.__len__()-1
            else:
                self.current_index-=1
            self.current_surf = self.animation_list_auto_surf[self.current_index]
        elif self.current_weapon == PISTOL:
            if self.current_index==0:
                self.current_index = self.animation_list_auto_surf.__len__()-1
            else:
                self.current_index-=1
            self.current_surf = self.animation_list_pistol_surf[self.current_index]
    def reset_index(self):
        self.current_index=0
        if(self.current_weapon == AUTO):
            self.current_surf = self.animation_list_auto_surf[self.current_index]
        elif (self.current_weapon == PISTOL):
            self.current_surf = self.animation_list_pistol_surf[self.current_index]
    def jetpack(self):
        if self.current_weapon == AUTO:
            self.current_surf = self.flying_auto_surf
        elif self.current_weapon == PISTOL:
            self.current_surf = self.flying_pistol_surf
    def switch_weapon(self):
        GUN_COCKING_SOUND.play()
        if self.current_weapon == AUTO:
            self.current_weapon = PISTOL
            if self.current_surf == self.flying_auto_surf:
                self.current_surf = self.flying_pistol_surf
            elif self.current_surf == self.animation_list_auto_surf[self.current_index]:
                self.current_surf = self.animation_list_pistol_surf[self.current_index]
        elif self.current_weapon == PISTOL:
            self.current_weapon = AUTO
            if self.current_surf == self.flying_pistol_surf:
                self.current_surf = self.flying_auto_surf
            elif self.current_surf == self.animation_list_pistol_surf[self.current_index]:
                self.current_surf = self.animation_list_auto_surf[self.current_index]
    def reload(self):
        if self.current_weapon == AUTO and self.auto_mag < AUTO_MAG:
            self.auto_mag = AUTO_MAG
        elif self.current_weapon == PISTOL and self.pistol_mag < PISTOL_MAG:
            self.pistol_mag = PISTOL_MAG




FPS = 30
CUBE_VELOC = 20

WIDTH,HEIGHT=1200,600
WIN=pyg.display.set_mode((WIDTH,HEIGHT))

HEALTH_FONT = pyg.font.SysFont('Broadway',22)
WINNER_FONT= pyg.font.SysFont('Broadway',70)

AUTO_BULLET_SIZE = (10,20)
PISTOL_BULLET_SIZE = (15,30)

CAVE = pyg.transform.scale(pyg.image.load(os.path.join('Assets','ice cave.png')),(WIDTH,HEIGHT))

AUTO_BULLET_ONE = pyg.transform.rotate(pyg.transform.scale(pyg.image.load(os.path.join('Assets','Bullet.png')),AUTO_BULLET_SIZE),-90)
PISTOL_BULLET_ONE = pyg.transform.rotate(pyg.transform.scale(pyg.image.load(os.path.join('Assets','Bullet.png')),PISTOL_BULLET_SIZE),-90)
AUTO_BULLET_TWO = pyg.transform.rotate(pyg.transform.scale(pyg.image.load(os.path.join('Assets','Bullet.png')),AUTO_BULLET_SIZE),90)
PISTOL_BULLET_TWO = pyg.transform.rotate(pyg.transform.scale(pyg.image.load(os.path.join('Assets','Bullet.png')),PISTOL_BULLET_SIZE),90)

FALL_SPEED = 5
JETPACK_SPEED = 16
MOV_SPEED = 10

AUTO_BULLET_SPEED=25
PISTOL_BULLET_SPEED=18

PLAYER_HEALTH = 100
RATE_OF_FIRE = 10
BURST = 25
JUMP_SPEED = 45
ACC = 5
BLUE_CUBE_SIZE = (80,80)
PLATFORMS_SIZE = (870,500)
PLATFORMS = pyg.transform.scale(pyg.image.load(os.path.join('Assets','icy platforms2.png')),PLATFORMS_SIZE)
PLATFORM1 = pyg.surface.Surface.subsurface(PLATFORMS,50,55,PLATFORMS_SIZE[0]*50/100,PLATFORMS_SIZE[1]*23/100)
PLATFORM1_INV = pyg.transform.flip(PLATFORM1,1,0)
PLATFORM2 = pyg.surface.Surface.subsurface(PLATFORMS,PLATFORMS_SIZE[0]*60/100,55,PLATFORMS_SIZE[0]*35/100,PLATFORMS_SIZE[1]*15/100)
BLUE_CUBE = pyg.transform.scale(pyg.image.load(os.path.join('Assets','blue cube.jpg')),BLUE_CUBE_SIZE)

PLAYER1_HIT_AUTO = pyg.USEREVENT+1
PLAYER1_HIT_PISTOL = pyg.USEREVENT+2
PLAYER2_HIT_AUTO = pyg.USEREVENT+3
PLAYER2_HIT_PISTOL = pyg.USEREVENT+4

def handle_bullets(player1rect,player2rect,player1_bullets,player2_bullets,Lplat1_rect,Lplat2_rect,Lplat3_rect,Rplat1_rect,Rplat2_rect,Rplat3_rect,blue_box_rect):
    for bullet in player1_bullets:
        if bullet.size == AUTO_BULLET_SIZE:
            bullet.x += AUTO_BULLET_SPEED
        elif bullet.size == PISTOL_BULLET_SIZE:
            bullet.x += PISTOL_BULLET_SPEED
        if bullet.x >= WIDTH:
            if bullet in player1_bullets:
                player1_bullets.remove(bullet)
        if player2rect.colliderect(bullet):
            if bullet.size == AUTO_BULLET_SIZE:
                pyg.event.post(pyg.event.Event(PLAYER2_HIT_AUTO))
            elif bullet.size == PISTOL_BULLET_SIZE:
                pyg.event.post(pyg.event.Event(PLAYER2_HIT_PISTOL))
            BODY_COLLISION_SOUND.play()
            if bullet in player1_bullets:
                player1_bullets.remove(bullet)
        if blue_box_rect.colliderect(bullet):
            BOX_COLLISION_SOUND.play()
            if bullet in player1_bullets:
                player1_bullets.remove(bullet)
        if Lplat1_rect.colliderect(bullet):
            PLATFORM_COLLISION_SOUND.play()
            if bullet in player1_bullets:
                player1_bullets.remove(bullet)
        if Lplat2_rect.colliderect(bullet):
            PLATFORM_COLLISION_SOUND.play()
            if bullet in player1_bullets:
                player1_bullets.remove(bullet)
        if Lplat3_rect.colliderect(bullet):
            PLATFORM_COLLISION_SOUND.play()
            if bullet in player1_bullets:
                player1_bullets.remove(bullet)
        if Rplat1_rect.colliderect(bullet):
            PLATFORM_COLLISION_SOUND.play()
            if bullet in player1_bullets:
                player1_bullets.remove(bullet)
        if Rplat2_rect.colliderect(bullet):
            PLATFORM_COLLISION_SOUND.play()
            if bullet in player1_bullets:
                player1_bullets.remove(bullet)
        if Rplat3_rect.colliderect(bullet):
            PLATFORM_COLLISION_SOUND.play()
            if bullet in player1_bullets:
                player1_bullets.remove(bullet)



    for bullet in player2_bullets:
        if bullet.size == AUTO_BULLET_SIZE:
            bullet.x -= AUTO_BULLET_SPEED
        elif bullet.size == PISTOL_BULLET_SIZE:
            bullet.x -= PISTOL_BULLET_SPEED 
        if bullet.x <= 0:
            if bullet in player2_bullets:
                player2_bullets.remove(bullet)
        if player1rect.colliderect(bullet):
            if bullet.size == AUTO_BULLET_SIZE:
                pyg.event.post(pyg.event.Event(PLAYER1_HIT_AUTO))
            elif bullet.size == PISTOL_BULLET_SIZE:
                pyg.event.post(pyg.event.Event(PLAYER1_HIT_PISTOL))
            BODY_COLLISION_SOUND.play()
            if bullet in player2_bullets:
                player2_bullets.remove(bullet)
        if blue_box_rect.colliderect(bullet):
            BOX_COLLISION_SOUND.play()
            if bullet in player2_bullets:
                player2_bullets.remove(bullet)
        if Lplat1_rect.colliderect(bullet):
            PLATFORM_COLLISION_SOUND.play()
            if bullet in player2_bullets:
                player2_bullets.remove(bullet)
        if Lplat2_rect.colliderect(bullet):
            PLATFORM_COLLISION_SOUND.play()
            if bullet in player2_bullets:
                player2_bullets.remove(bullet)
        if Lplat3_rect.colliderect(bullet):
            PLATFORM_COLLISION_SOUND.play()
            if bullet in player2_bullets:
                player2_bullets.remove(bullet)
        if Rplat1_rect.colliderect(bullet):
            PLATFORM_COLLISION_SOUND.play()
            if bullet in player2_bullets:
                player2_bullets.remove(bullet)
        if Rplat2_rect.colliderect(bullet):
            PLATFORM_COLLISION_SOUND.play()
            if bullet in player2_bullets:
                player2_bullets.remove(bullet)
        if Rplat3_rect.colliderect(bullet):
            PLATFORM_COLLISION_SOUND.play()
            if bullet in player2_bullets:
                player2_bullets.remove(bullet)



def draw(blue_box_pos,player1,player2,player1_bullets,player2_bullets,player1health,player2health,player1wins,player2wins,player1automag,player2automag,player1pistolmag,player2pistolmag):
    WIN.blit(CAVE,(0, 0))
    if player1health>=50:
        player1health_text = HEALTH_FONT.render("HEALTH: " + str(player1health),1,(0,255,0))
    else:
        player1health_text = HEALTH_FONT.render("HEALTH: " + str(player1health),1,(255,0,0))
    if player2health>=50:
        player2health_text = HEALTH_FONT.render("HEALTH: " + str(player2health),1,(0,255,0))
    else:
        player2health_text = HEALTH_FONT.render("HEALTH: " + str(player2health),1,(255,0,0))
    player1wins_text = HEALTH_FONT.render("Player 1 Wins: "+str(player1wins),1,(240,175,55))
    player2wins_text = HEALTH_FONT.render("Player 2 Wins: "+str(player2wins),1,(240,175,55))
    player1automag_text = HEALTH_FONT.render("Auto mag: "+str(player1automag),1,(255,255,255))
    player1pistolmag_text = HEALTH_FONT.render("Pistol mag: "+str(player1pistolmag),1,(255,255,255))
    player2automag_text = HEALTH_FONT.render("Auto mag: "+str(player2automag),1,(255,255,255))
    player2pistolmag_text = HEALTH_FONT.render("Pistol mag: "+str(player2pistolmag),1,(255,255,255))
    WIN.blit(player2health_text,(WIDTH - player2health_text.get_width() - 10,10))
    WIN.blit(player1health_text,(10,10))
    WIN.blit(player2wins_text,(WIDTH - player1wins_text.get_width() - 10,50))
    WIN.blit(player1wins_text,(10,50))
    WIN.blit(player1automag_text,(30+player1wins_text.get_width(),10))
    WIN.blit(player1pistolmag_text,(30+player1wins_text.get_width(),50))
    WIN.blit(player2automag_text,(WIDTH - player2wins_text.get_width() - 40 - player2automag_text.get_width(),10))
    WIN.blit(player2pistolmag_text,(WIDTH - player2wins_text.get_width() - 40 - player2automag_text.get_width(),50))
    WIN.blit(PLATFORM1,(WIDTH-PLATFORM1.get_width(),HEIGHT-PLATFORM1.get_height()))
    WIN.blit(PLATFORM1_INV,(0,HEIGHT-PLATFORM1.get_height()))
    WIN.blit(PLATFORM2,(WIDTH/1.5,HEIGHT/2))
    WIN.blit(PLATFORM2,(0,HEIGHT/2))
    WIN.blit(PLATFORM2,(WIDTH/1.5,HEIGHT/5))
    WIN.blit(PLATFORM2,(0,HEIGHT/5))
    WIN.blit(BLUE_CUBE,blue_box_pos)
    WIN.blit(player1.current_surf,player1.pos)
    WIN.blit(player2.current_surf,player2.pos)
    WIN.blit(AUTO_BULLET_ONE,(0,0))
    for bullet in player1_bullets:
        if bullet.size == AUTO_BULLET_SIZE:
            WIN.blit(AUTO_BULLET_ONE,(bullet.x,bullet.y))
        elif bullet.size == PISTOL_BULLET_SIZE:
            WIN.blit(PISTOL_BULLET_ONE,(bullet.x,bullet.y))
    for bullet in player2_bullets:
        if bullet.size == AUTO_BULLET_SIZE:
            WIN.blit(AUTO_BULLET_TWO,(bullet.x,bullet.y))
        elif bullet.size == PISTOL_BULLET_SIZE:
            WIN.blit(PISTOL_BULLET_TWO,(bullet.x,bullet.y))

    pyg.display.update()

def draw_winner(text):
    wintext = WINNER_FONT.render(text,1,(212,175,55))
    WIN.blit(wintext,(WIDTH//2 - wintext.get_width()//2,HEIGHT//2 - wintext.get_height()//2))
    pyg.display.update()
    pyg.time.delay(1500)

def main():
    MUSIC.set_volume(0.3)
    MUSIC.play(-1)
    #game variables
    player1 = character(WALKING_PISTOL_LIST_SURF,FLYING_PISTOL_SURF,WALKING_AUTO_LIST_SURF,FLYING_AUTO_SURF,[110,HEIGHT-PLATFORM1.get_height()-ICE_MONSTER_AUTO_SIZE[1]])
    player2 = character([pyg.transform.flip(x,1,0) for x in WALKING_PISTOL_LIST_SURF],pyg.transform.flip(FLYING_PISTOL_SURF,1,0),[pyg.transform.flip(x,1,0) for x in WALKING_AUTO_LIST_SURF],pyg.transform.flip(FLYING_AUTO_SURF,1,0),[WIDTH-220,HEIGHT-PLATFORM1.get_height()-ICE_MONSTER_AUTO_SIZE[1]])
    player1rect = pyg.Rect(player1.pos,player1.current_surf.get_size())
    player2rect = pyg.Rect(player2.pos,player2.current_surf.get_size())
    Lplat1_rect = pyg.Rect((WIDTH-PLATFORM1.get_width(),HEIGHT-PLATFORM1.get_height()),PLATFORM1.get_size())
    Lplat2_rect = pyg.Rect((0,HEIGHT-PLATFORM1.get_height()),PLATFORM2.get_size())
    Lplat3_rect = pyg.Rect((WIDTH/1.5,HEIGHT/2),PLATFORM2.get_size())
    Rplat1_rect = pyg.Rect((0,HEIGHT/2),PLATFORM1.get_size())
    Rplat2_rect = pyg.Rect((WIDTH/1.5,HEIGHT/5),PLATFORM2.get_size())
    Rplat3_rect = pyg.Rect((0,HEIGHT/5),PLATFORM2.get_size())
    player1_bullets = []
    player2_bullets = []
    
    blue_box_pos = [(WIDTH/2) - BLUE_CUBE_SIZE[1]/2,0]
    blue_box_rect = pyg.Rect(blue_box_pos,BLUE_CUBE_SIZE)
    going_up = False
    one_jump_speed = JUMP_SPEED
    one_falling = True
    one_jetpacking = False
    one_burst = True
    one_jumping = False
    one_fall_speed = FALL_SPEED
    two_jump_speed = JUMP_SPEED
    two_falling = True
    two_jetpacking = False
    two_burst = True
    two_jumping = False
    auto1_reloading=False
    pistol1_reloading = False
    auto2_reloading=False
    pistol2_reloading = False
    two_fall_speed = JUMP_SPEED
    player1health = PLAYER_HEALTH
    player2health = PLAYER_HEALTH
    framecount = 0
    player1wins = 0
    player2wins = 0
    pressed_key=pyg.key.get_pressed()
    pyg.joystick.init()
    joysticks = [pyg.joystick.Joystick(x) for x in range(pyg.joystick.get_count())]
    clock = pyg.time.Clock()
    run = True
    #game main loop
    while(run):
        clock.tick(FPS)

        pressed_key=pyg.key.get_pressed()
        #game events
        if pressed_key[pyg.K_q] or (bool(joysticks) and joysticks[0].get_button(5)):
            if player1.current_weapon == AUTO and (framecount%(FPS/RATE_OF_FIRE)==0) and not auto1_reloading:
                if player1.auto_mag>0:
                    ONE_BULLET_AUTO_SOUND.play()
                    player1_bullets.append(pyg.Rect(player1.pos[0]+player1.current_surf.get_width(), player1.pos[1] + ICE_MONSTER_AUTO_SIZE[1]*125/310, AUTO_BULLET_SIZE[0], AUTO_BULLET_SIZE[1]))
                    if AUTO_FIRE_SOUND1.get_num_channels() == 0:
                        AUTO_FIRE_SOUND1.play(-1)
                    player1.shoot()
                if player1.auto_mag == 0 and AUTO_FIRE_SOUND1.get_num_channels()>0:
                    AUTO_FIRE_SOUND1.stop()
        if pressed_key[pyg.K_d] or (bool(joysticks) and joysticks[0].get_axis(0)>0):
            if FOOTSTEPS_SOUND1.get_num_channels() == 0 and not one_jetpacking and not one_falling:
                FOOTSTEPS_SOUND1.set_volume(3000)
                FOOTSTEPS_SOUND1.play(-1)
            if player1.pos[0] + FLYING_AUTO_SURF.get_width() < WIDTH/2 - BLUE_CUBE.get_width():
                player1.pos[0]+=MOV_SPEED
            if not one_jetpacking:
                player1.animate()
        if pressed_key[pyg.K_a] or (bool(joysticks) and joysticks[0].get_axis(0)<0):
            if FOOTSTEPS_SOUND1.get_num_channels() == 0 and not one_jetpacking and not one_falling:
                FOOTSTEPS_SOUND1.set_volume(3000)
                FOOTSTEPS_SOUND1.play(-1)
            if player1.pos[0] + JET_WIDTH >0:
                player1.pos[0]-=MOV_SPEED
            if not one_jetpacking:
                player1.animate()
        if pressed_key[pyg.K_w] or (bool(joysticks) and joysticks[0].get_button(4)):
            if FOOTSTEPS_SOUND1.get_num_channels() != 0:
                FOOTSTEPS_SOUND1.stop()
            if one_burst:
                player1.pos[1]-=BURST
                one_burst=False
                player1.jetpack()
            if player1.pos[1] > 0:
                player1.pos[1]-=JETPACK_SPEED
            if JETPACK_SOUND.get_num_channels() == 0:
                JETPACK_SOUND.set_volume(0.4)
                JETPACK_SOUND.play(-1)
            one_jetpacking = True
            one_falling = False


        if pressed_key[pyg.K_LSHIFT] or (bool(joysticks) and joysticks[1].get_button(5)):
            if player2.current_weapon == AUTO and (framecount%(FPS/RATE_OF_FIRE)==0) and not auto2_reloading:
                if player2.auto_mag>0:
                    ONE_BULLET_AUTO_SOUND.play()
                    player2_bullets.append(pyg.Rect(player2.pos[0], player2.pos[1] + ICE_MONSTER_AUTO_SIZE[1]*125/310, AUTO_BULLET_SIZE[0], AUTO_BULLET_SIZE[1]))
                    if AUTO_FIRE_SOUND2.get_num_channels() == 0:
                        AUTO_FIRE_SOUND2.play(-1)
                    player2.shoot()
                if player2.auto_mag == 0 and AUTO_FIRE_SOUND2.get_num_channels()>0:
                    AUTO_FIRE_SOUND2.stop()
        if pressed_key[pyg.K_RIGHT] or (bool(joysticks) and joysticks[1].get_axis(0)>0):
            if FOOTSTEPS_SOUND2.get_num_channels() == 0 and not two_jetpacking and not two_falling:
                FOOTSTEPS_SOUND2.set_volume(3000)
                FOOTSTEPS_SOUND2.play(-1)
            if player2.pos[0]+player2.current_surf.get_width()-JET_WIDTH < WIDTH:
                player2.pos[0]+=MOV_SPEED
            if not two_jetpacking:
                player2.animate()
        if pressed_key[pyg.K_LEFT] or (bool(joysticks) and joysticks[1].get_axis(0)<0):
            if FOOTSTEPS_SOUND2.get_num_channels() == 0 and not two_jetpacking and not two_falling:
                FOOTSTEPS_SOUND2.set_volume(3000)
                FOOTSTEPS_SOUND2.play(-1)
            if player2.pos[0]+player2.current_surf.get_width() - ICE_MONSTER_AUTO_SIZE[0] > WIDTH/2 + BLUE_CUBE.get_width()/2 +JET_WIDTH*2:
                player2.pos[0]-=MOV_SPEED
            if not two_jetpacking:
                player2.animate()
        if pressed_key[pyg.K_UP] or (bool(joysticks) and joysticks[1].get_button(4)):
            if FOOTSTEPS_SOUND2.get_num_channels() != 0:
                FOOTSTEPS_SOUND2.stop()
            if two_burst:
                player2.pos[1]-=BURST
                two_burst=False
                player2.jetpack()
            if player2.pos[1] > 0:
                player2.pos[1]-=JETPACK_SPEED
            if JETPACK_SOUND.get_num_channels() == 0:
                JETPACK_SOUND.set_volume(0.4)
                JETPACK_SOUND.play(-1)
            two_jetpacking = True
            two_falling = False
        


        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                run = False

            if event.type == pyg.JOYBUTTONDOWN or event.type == pyg.KEYDOWN:
                if (bool(joysticks) and joysticks[0].get_button(3)) or (event.type == pyg.KEYDOWN and event.key == pyg.K_r):
                    if AUTO_FIRE_SOUND1.get_num_channels()>0:
                        AUTO_FIRE_SOUND1.stop()
                    if (player1.current_weapon == AUTO) and (player1.auto_mag<AUTO_MAG) and (not auto1_reloading):
                        RELOAD_SOUND_AUTO1.play()
                        auto1_reloading=True
                    elif player1.current_weapon == PISTOL and player1.pistol_mag<PISTOL_MAG and not pistol1_reloading:
                        RELOAD_SOUND_PISTOL1.play() 
                        pistol1_reloading = True
                    player1.reload()
                if (bool(joysticks) and joysticks[0].get_button(5)) or (event.type == pyg.KEYDOWN and event.key == pyg.K_q):
                    if player1.current_weapon == PISTOL and not pistol1_reloading:
                        if player1.pistol_mag>0:
                            player1_bullets.append(pyg.Rect(player1.pos[0]+player1.current_surf.get_width(),player1.pos[1] + ICE_MONSTER_AUTO_SIZE[1]*125/310,PISTOL_BULLET_SIZE[0],PISTOL_BULLET_SIZE[1]))
                        else:
                            EMPTY_MAG_SOUND.play()
                        player1.shoot()
                    if player1.current_weapon == AUTO and player1.auto_mag==0:
                        EMPTY_MAG_SOUND.play()
                        
                if ((bool(joysticks) and joysticks[0].get_button(1)) or (event.type == pyg.KEYDOWN and event.key == pyg.K_s)) and player1.pos[1]+ICE_MONSTER_PISTOL_SIZE[1] < HEIGHT - PLATFORM1.get_height() and not one_falling and not one_jumping and not one_jetpacking:
                    player1.pos[1]+=10
                if (bool(joysticks) and joysticks[0].get_button(2)) or (event.type == pyg.KEYDOWN and event.key == pyg.K_t):
                    if not one_jumping and not one_falling and not one_jetpacking:
                        one_jumping = True
                if (bool(joysticks) and joysticks[0].get_button(0)) or (event.type == pyg.KEYDOWN and event.key == pyg.K_e):
                    player1.switch_weapon()


                
                
                if (bool(joysticks) and joysticks[1].get_button(3)) or  (event.type == pyg.KEYDOWN and event.key == pyg.K_m):
                    if AUTO_FIRE_SOUND2.get_num_channels()>0:
                        AUTO_FIRE_SOUND2.stop()
                    if player2.current_weapon == AUTO and (player2.auto_mag<AUTO_MAG) and (not auto2_reloading):
                        RELOAD_SOUND_AUTO2.play()
                        auto2_reloading = True
                    elif player2.current_weapon == PISTOL and (player2.pistol_mag<PISTOL_MAG) and (not pistol2_reloading):
                        RELOAD_SOUND_PISTOL2.play()
                        pistol2_reloading= True
                    player2.reload()
                if (bool(joysticks) and joysticks[1].get_button(5)) or  (event.type == pyg.KEYDOWN and event.key == pyg.K_LSHIFT):
                    if player2.current_weapon == PISTOL and not pistol2_reloading:
                        if player2.pistol_mag>0:
                            player2_bullets.append(pyg.Rect(player2.pos[0],player2.pos[1] + ICE_MONSTER_AUTO_SIZE[1]*125/310,PISTOL_BULLET_SIZE[0],PISTOL_BULLET_SIZE[1]))
                        else:
                            EMPTY_MAG_SOUND.play()
                        player2.shoot()
                    if player2.current_weapon == AUTO and player2.auto_mag==0:
                        EMPTY_MAG_SOUND.play()
                if ((bool(joysticks) and joysticks[1].get_button(1)) or  (event.type == pyg.KEYDOWN and event.key == pyg.K_DOWN)) and player2.pos[1]+ICE_MONSTER_PISTOL_SIZE[1] < HEIGHT - PLATFORM1.get_height() and not two_falling and not two_jumping and not two_jetpacking:
                    player2.pos[1]+=10
                if (bool(joysticks) and joysticks[1].get_button(2)) or  (event.type == pyg.KEYDOWN and event.key == pyg.K_RCTRL):
                    if not two_jumping and not two_falling and not two_jetpacking:
                        two_jumping = True
                if (bool(joysticks) and joysticks[1].get_button(0)) or  (event.type == pyg.KEYDOWN and event.key == pyg.K_RALT):
                    player2.switch_weapon()
                    if player2.current_weapon == AUTO:
                        player2.pos[0]-=GUN_WIDTH
                    elif player2.current_weapon == PISTOL:
                        player2.pos[0]+=GUN_WIDTH




            if event.type == pyg.JOYBUTTONUP or event.type == pyg.KEYUP:
                if (bool(joysticks) and not joysticks[0].get_button(5)) or (event.type == pyg.KEYUP and event.key == pyg.K_q):
                    if AUTO_FIRE_SOUND1.get_num_channels() > 0:
                        AUTO_FIRE_SOUND1.stop()
                if (event.type == pyg.KEYUP and event.key == pyg.K_d):
                    FOOTSTEPS_SOUND1.stop()
                    if not one_jetpacking:
                        player1.reset_index()
                if (event.type == pyg.KEYUP and event.key == pyg.K_a):
                    FOOTSTEPS_SOUND1.stop()
                    if not one_jetpacking:
                        player1.reset_index()
                if (bool(joysticks) and not joysticks[0].get_button(6)) or (event.type == pyg.KEYUP and event.key == pyg.K_w):
                    player1.reset_index()
                    JETPACK_SOUND.stop()
                    one_jetpacking = False
                    one_falling = True
                    one_burst=True


                if (bool(joysticks) and not joysticks[1].get_button(5)) or  (event.type == pyg.KEYUP and event.key == pyg.K_LSHIFT):
                    if AUTO_FIRE_SOUND2.get_num_channels() > 0:
                        AUTO_FIRE_SOUND2.stop()
                if ((bool(joysticks) and not joysticks[1].get_axis(0)>0) or  (event.type == pyg.KEYUP and event.key == pyg.K_RIGHT)):
                    FOOTSTEPS_SOUND2.stop()
                    if not two_jetpacking:
                        player2.reset_index()
                if ((bool(joysticks) and not joysticks[1].get_axis(0)<0) or  (event.type == pyg.KEYUP and event.key == pyg.K_LEFT)) :
                    FOOTSTEPS_SOUND2.stop()
                    if not two_jetpacking:
                        player2.reset_index()
                if (bool(joysticks) and not joysticks[1].get_button(6)) or (event.type == pyg.KEYUP and event.key == pyg.K_UP):
                    player2.reset_index()
                    JETPACK_SOUND.stop()
                    two_jetpacking = False
                    two_falling = True
                    two_burst=True
            if(bool(joysticks) and joysticks[0].get_axis(0)==0.0):
                FOOTSTEPS_SOUND1.stop()
                if not one_jetpacking:
                    player1.reset_index()
            if(bool(joysticks) and joysticks[1].get_axis(0)==0.0):
                FOOTSTEPS_SOUND2.stop()
                if not two_jetpacking:
                    player2.reset_index()

            if event.type == PLAYER1_HIT_AUTO:
                player1health-=2
            if event.type == PLAYER1_HIT_PISTOL:
                player1health-=4
            if event.type == PLAYER2_HIT_AUTO:
                player2health -= 2
            if event.type == PLAYER2_HIT_PISTOL:
                player2health-=4

        

        if RELOAD_SOUND_AUTO1.get_num_channels() == 0:
            auto1_reloading = False
        if RELOAD_SOUND_PISTOL1.get_num_channels() == 0:
            pistol1_reloading = False
        if RELOAD_SOUND_AUTO2.get_num_channels() == 0:
            auto2_reloading = False
        if RELOAD_SOUND_PISTOL2.get_num_channels() == 0:
            pistol2_reloading = False
        

        #one_jumping
        if one_jumping:
            if one_jump_speed>0:
                player1.pos[1]-=one_jump_speed
                one_jump_speed-=ACC
            elif one_jump_speed == 0:
                one_jump_speed = JUMP_SPEED
                one_jumping = False 
        #two_jumping
        if two_jumping:
            if two_jump_speed>0:
                player2.pos[1]-=two_jump_speed
                two_jump_speed-=ACC
            elif two_jump_speed == 0:
                two_jump_speed = JUMP_SPEED
                two_jumping = False


        #player 1 gravity deactivation
        if (player1.pos[1]+ICE_MONSTER_AUTO_SIZE[1] == HEIGHT - PLATFORM1.get_height() and (-ICE_MONSTER_AUTO_SIZE[0]*2/5 <= player1.pos[0] <= PLATFORM1.get_width()-ICE_MONSTER_AUTO_SIZE[0]*1/5) ) or (player1.pos[1]+ICE_MONSTER_AUTO_SIZE[1] == HEIGHT/2 and (-ICE_MONSTER_AUTO_SIZE[1]/5 < player1.pos[0] < PLATFORM2.get_width()-ICE_MONSTER_AUTO_SIZE[1]*2/5)) or (player1.pos[1]+ICE_MONSTER_AUTO_SIZE[1] == HEIGHT/5 and (-ICE_MONSTER_AUTO_SIZE[1]/5 < player1.pos[0] < PLATFORM2.get_width()-ICE_MONSTER_AUTO_SIZE[1]*2/5)) or one_jetpacking or one_jumping:
            one_falling = False
            one_fall_speed = FALL_SPEED
        else:
            one_falling=True


       


        if one_falling:
            #player 1 gravity
            
            if 0 < (HEIGHT - PLATFORM1.get_height()) - (player1.pos[1]+ICE_MONSTER_AUTO_SIZE[1]) < one_fall_speed+ACC and (-ICE_MONSTER_AUTO_SIZE[0]*2/5 <= player1.pos[0] <= PLATFORM1.get_width()-ICE_MONSTER_AUTO_SIZE[0]*1/5) :
                    player1.pos[1] = HEIGHT - PLATFORM1.get_height() - ICE_MONSTER_AUTO_SIZE[1]

            elif 0 < (HEIGHT/2) - (player1.pos[1]+ICE_MONSTER_AUTO_SIZE[1]) < one_fall_speed+ACC and (-ICE_MONSTER_AUTO_SIZE[1]/5 < player1.pos[0] < PLATFORM2.get_width()-ICE_MONSTER_AUTO_SIZE[1]*2/5):
                    player1.pos[1] = HEIGHT/2 - ICE_MONSTER_AUTO_SIZE[1]

            elif 0 < (HEIGHT/5) - (player1.pos[1]+ICE_MONSTER_AUTO_SIZE[1]) < one_fall_speed+ACC and (-ICE_MONSTER_AUTO_SIZE[1]/5 < player1.pos[0] < PLATFORM2.get_width()-ICE_MONSTER_AUTO_SIZE[1]*2/5):
                    player1.pos[1] = HEIGHT/5 - ICE_MONSTER_AUTO_SIZE[1]
            else:
                    player1.pos[1]+= one_fall_speed
                    one_fall_speed += ACC


         #player 2 gravity deactivation
        if (player2.pos[1]+ICE_MONSTER_AUTO_SIZE[1] == HEIGHT - PLATFORM1.get_height() and (WIDTH - PLATFORM1.get_width()<= player2.pos[0] + player2.current_surf.get_width() - JET_WIDTH <= WIDTH + JET_WIDTH*2 ) ) or (player2.pos[1]+ICE_MONSTER_AUTO_SIZE[1] == HEIGHT/2 and (WIDTH/1.5 + PLATFORM2.get_width()/9 < player2.pos[0] + player2.current_surf.get_width() - JET_WIDTH < WIDTH/1.5 + PLATFORM2.get_width() + JET_WIDTH*2 -5)) or (player2.pos[1]+ICE_MONSTER_AUTO_SIZE[1] == HEIGHT/5 and (WIDTH/1.5 + PLATFORM2.get_width()/9 < player2.pos[0] + player2.current_surf.get_width() - JET_WIDTH < WIDTH/1.5 + PLATFORM2.get_width() + JET_WIDTH*2 -5)) or two_jetpacking or two_jumping:
            two_falling = False
            two_fall_speed = FALL_SPEED
        else:
            two_falling=True

        if two_falling:
            #player 2 gravity

            if 0 < (HEIGHT - PLATFORM1.get_height()) - (player2.pos[1]+ICE_MONSTER_AUTO_SIZE[1]) < two_fall_speed+ACC and (WIDTH - PLATFORM1.get_width()<= player2.pos[0] + player2.current_surf.get_width() - JET_WIDTH <= WIDTH + JET_WIDTH*2 ) :
                    player2.pos[1] = HEIGHT - PLATFORM1.get_height() - ICE_MONSTER_AUTO_SIZE[1]

            elif 0 < (HEIGHT/2) - (player2.pos[1]+ICE_MONSTER_AUTO_SIZE[1]) < two_fall_speed+ACC and (WIDTH/1.5 + PLATFORM2.get_width()/9 < player2.pos[0] + player2.current_surf.get_width() - JET_WIDTH < WIDTH/1.5 + PLATFORM2.get_width() + JET_WIDTH*2 -5):
                    player2.pos[1] = HEIGHT/2 - ICE_MONSTER_AUTO_SIZE[1]

            elif 0 < (HEIGHT/5) - (player2.pos[1]+ICE_MONSTER_AUTO_SIZE[1]) < two_fall_speed+ACC and (WIDTH/1.5 + PLATFORM2.get_width()/9 < player2.pos[0] + player2.current_surf.get_width() - JET_WIDTH < WIDTH/1.5 + PLATFORM2.get_width() + JET_WIDTH*2 -5):
                    player2.pos[1] = HEIGHT/5 - ICE_MONSTER_AUTO_SIZE[1]
            else:
                    player2.pos[1]+= two_fall_speed
                    two_fall_speed += ACC

        



        #box movement
        if blue_box_pos[1]+BLUE_CUBE_SIZE[1] >= HEIGHT:
            going_up = True
        if blue_box_pos[1] <= 0:
            going_up = False
        if not going_up:
            blue_box_pos[1]+= CUBE_VELOC
        else:
            blue_box_pos[1]-= CUBE_VELOC



        player1rect.x,player1rect.y = player1.pos
        player2rect.x,player2rect.y = player2.pos
        blue_box_rect.x,blue_box_rect.y = blue_box_pos



        handle_bullets(player1rect,player2rect,player1_bullets,player2_bullets,Lplat1_rect,Lplat2_rect,Lplat3_rect,Rplat1_rect,Rplat2_rect,Rplat3_rect,blue_box_rect)

        if framecount==30:
            framecount=0
        else:
            framecount+=1
        #update game
        winner_text=""
        draw(blue_box_pos,player1,player2,player1_bullets,player2_bullets,player1health,player2health,player1wins,player2wins,player1.auto_mag,player2.auto_mag,player1.pistol_mag,player2.pistol_mag)
        if player2health <= 0:
            winner_text="Player 1 Wins!!"
            player1wins+=1
        if player1health <= 0:
            winner_text="Player 2 Wins!!"
            player2wins +=1
        if winner_text != "":
            player1_bullets.clear()
            player2_bullets.clear()
            draw_winner(winner_text)
            winner_text=""
            player1health = player2health = PLAYER_HEALTH


    pyg.quit()


if __name__ == "__main__":
    main()