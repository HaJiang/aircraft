#ʵ�ֳ���
from __future__ import division

import codecs
import pygame
import sys
import traceback
import my_plane
import enemy
import bullet
import supply
import background2
import boss
import boss_bullet
import random
from pygame.locals import *

#��ɫ����
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
DEEP_RED = (254,67,101)
TINT_RED = (252,157,154)

pygame.init()
pygame.mixer.init()

bg_size  = width,height = 480,700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("Fight Plane")
start_background = pygame.image.load("image/cover.png").convert()
background1 = pygame.image.load("image/background1.png").convert()

#���ɱ���ͼƬ2
boss_background = background2.Background2()
background = background1

#������Ϸ����
bullet_sound = pygame.mixer.Sound("sound/bullet_sound.wav")
bullet_sound.set_volume(0.3)
bomb_sound = pygame.mixer.Sound("sound/bomb_sound.wav")
bomb_sound.set_volume(0.3)
supply_sound = pygame.mixer.Sound("sound/supply_sound.wav")
supply_sound.set_volume(0.3)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.3)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.3)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.3)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.1)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(1)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(1)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy3_down_sound.set_volume(1)
mine_down_sound = pygame.mixer.Sound("sound/me_down.wav")
mine_down_sound.set_volume(1)
boss_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
boss_down_sound.set_volume(1)

def add_small_enemies(group1,group2,number):
    for i in range(number):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1,group2,number):
    for i in range(number):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_big_enemies(group1,group2,number):
    for i in range(number):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def add_boss_enemies(group1,group2,number):
    for i in range(number):
        e4 = boss.Boss(bg_size)
        group1.add(e4)
        group2.add(e4)

def inc_speed(target,inc):
    for each in target:
        each.speed += inc
    

def main():
    
        #ѭ���������������Ч
        pygame.mixer.music.load("sound/start_music.ogg")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)


        #=========�����ʶ==========
        
        #��ʼ�����ʶ
        START_SCREEN = True
        #��Ϸ˵�������ʶ
        HELP_SCREEN = False
        #��ʷ��¼�����ʶ
        HISTORY_SCREEN = False
        #��Ϸ�����ʶ
        GAME_SCREEN = False
        #��ͣ�����ʶ
        PAUSE_SCREEN = False
        #Boss�����ʶ
        BOSS_SCREEN = False
        #���������ʶ
        OVER_SCREEN = False


        #��ʼ���ҷ��ɻ�
        me = my_plane.MyPlane(bg_size)
        
        #��ʼ���л�Ⱥ
        enemies = pygame.sprite.Group()
        
        #��ʼ���з�С�ͷɻ�Ⱥ
        small_enemies = pygame.sprite.Group()
        add_small_enemies(small_enemies,enemies,15)
        
        #��ʼ���з����ͷɻ�Ⱥ
        mid_enemies = pygame.sprite.Group()
        add_mid_enemies(mid_enemies,enemies,4)
        
        #��ʼ���з����ͷɻ�Ⱥ
        big_enemies = pygame.sprite.Group()
        add_big_enemies(big_enemies,enemies,2)

        #��ʼ��Boss�ɻ�Ⱥ
        boss_enemies = pygame.sprite.Group()
        
        #��ʼ����ͨ�ӵ�
        bullet1 = []
        bullet1_index = 0
        BULLET1_NUM = 4
        for i in range(BULLET1_NUM):
            bullet1.append(bullet.Bullet1((me.rect.midtop[0]-4,me.rect.midtop[1])))

        #��ʼ�������ӵ�
        bullet2 = []
        bullet2_index = 0
        BULLET2_NUM = 8
        for i in range(BULLET2_NUM//2):
            bullet2.append(bullet.Bullet2((me.rect.centerx-32,me.rect.centery-2)))
            bullet2.append(bullet.Bullet2((me.rect.centerx+21,me.rect.centery-2)))

        #��ʼ��BOSS�ӵ�
        bullet_boss = []
        bullet_b_index = 0
        BULLET_B_NUM = 9
        for i in range(BULLET_B_NUM):
            bullet_boss.append(boss_bullet.BossBullet((0,0)))

        clock = pygame.time.Clock()

        #�е�ͼƬ����
        e1_destroy_index = 0
        e2_destroy_index = 0
        e3_destroy_index = 0
        me_destroy_index = 0
        boss_destroy_index = 0

        #ͳ�Ƶ÷�
        score = 0
        score_font = pygame.font.Font("font/font.ttf",36)

        #��ʼ���ɻ��޵���BUFF
        invincible_image = pygame.image.load("image/invincible.png").convert_alpha()
        invincible_rect = invincible_image.get_rect()

        #����ҷ��޵�״̬��ʱ��
        INVINCIBLE_TIMER = USEREVENT + 2

        #��Ϸ˵������
        doc_background = pygame.image.load("image/document.png").convert_alpha()
        back_image = pygame.image.load("image/back.png").convert_alpha()
        back_rect = back_image.get_rect()
        back_rect.left,back_rect.top = 400 , 10

        #��ʷ��¼����
        history_background  = pygame.image.load("image/history_back.png").convert_alpha()
        

        #"��ʼ��Ϸ"����
        start_image = pygame.image.load("image/start.png").convert_alpha()
        start_rect = start_image.get_rect()
        start_rect.left , start_rect.top = 160,350

        #����Ϸ˵��������
        help_image = pygame.image.load("image/help.png").convert_alpha()
        help_rect = help_image.get_rect()
        help_rect.left , help_rect.top = 160 , start_rect.top + 10 + start_rect.height

        #"��ʷ��¼"����
        history_image = pygame.image.load("image/history.png").convert_alpha()
        history_rect = history_image.get_rect()
        history_rect.left , history_rect.top = 160 , help_rect.top + 10 + start_rect.height

        #"�˳���Ϸ"����
        quit_image = pygame.image.load("image/quit.png").convert_alpha()
        quit_rect = quit_image.get_rect()
        quit_rect.left , quit_rect.top = 160 , history_rect.top + 10 + start_rect.height

        #��ʶ�Ƿ���ͣ��Ϸ����
        pause = False
        pause_nor_image = pygame.image.load("image/pause_nor.png").convert_alpha()
        pause_pressed_image = pygame.image.load("image/pause_pressed.png").convert_alpha()
        resume_nor_image = pygame.image.load("image/resume_nor.png").convert_alpha()
        resume_pressed_image = pygame.image.load("image/resume_pressed.png").convert_alpha()
        pause_rect = pause_nor_image.get_rect()
        pause_rect.left , pause_rect.top = width - pause_rect.width - 10,10
        pause_image = pause_nor_image

        #�����Ѷȼ���
        level = 1
        level_font = pygame.font.Font("font/font.ttf",36)
        
        #Boss��������ʶ
        BOSS_LEVEL = False

        #Boss����ʾ
        BOSS_LIVE = False

        #ÿ��ʮ�뷢��һ��������(�����ӵ���ȫ��ը��)
        bullet_supply = supply.BulletSupply(bg_size)
        bomb_supply = supply.BombSupply(bg_size)
        SUPPLYTIMER = USEREVENT
        pygame.time.set_timer(SUPPLYTIMER,30 * 1000)

        #������͵л�����������(�޵�)
        invincible_supply = supply.InvincibleSupply(bg_size)
        invincible_supply.alive = False
        
        #�����ӵ���ʱ��
        DOUBLE_BULLET_TIME = USEREVENT + 1

        #��־�Ƿ�ʹ�ó����ӵ�
        is_double_bullet = False

        #��������
        life_image = pygame.image.load("image/life.png").convert_alpha()
        life_rect = life_image.get_rect()
        life_num = 3

        #������ֹ�ظ��򿪼�¼�ļ�
        recorded = False

        #��Ϸ��������
        record_image = pygame.image.load("image/record.png").convert_alpha()
        record_image_rect = record_image.get_rect()   
            
        congrat_font1 = pygame.font.Font("font/font.ttf",48)
        congrat_font2 = pygame.font.Font("font/font.ttf",48)
        gameover_font = pygame.font.Font("font/font.ttf",48)
        again_image = pygame.image.load("image/again.png").convert_alpha()
        again_rect = again_image.get_rect()
        gameover_image = pygame.image.load("image/gameover.png").convert_alpha()
        gameover_rect = gameover_image.get_rect()

        #����ȫ��ը��
        bomb_image = pygame.image.load("image/bomb.png").convert_alpha()
        bomb_rect = bomb_image.get_rect()
        bomb_font = pygame.font.Font("font/font.ttf",48)
        bomb_num = 3

        #ͨ�ع�ϲ
        congrat = False
        
        #�����л�ͼƬ
        switch_image = True

        #������ʱ
        delay = 200

        running = True

        while running:
            #=========================================��ʼ����=================================================================
            
            if START_SCREEN:
                for event in pygame.event.get():
                    #����رհ�ť
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    #��갴��
                    if event.type == MOUSEBUTTONDOWN:
                        #�����ʼ��Ϸ�¼�
                        if event.button == 1 and start_rect.collidepoint(event.pos):
                            START_SCREEN = False
                            GAME_SCREEN = True
                            #������Ϸ����ʱ��������
                            pygame.mixer.music.load("sound/bg_music.ogg")
                            pygame.mixer.music.set_volume(0.2)
                            pygame.mixer.music.play(-1)
                            
                        #�����Ϸ˵���¼�
                        if event.button == 1 and help_rect.collidepoint(event.pos):
                            START_SCREEN = False
                            HELP_SCREEN = True

                        #�����ʷ��¼�¼�
                        if event.button == 1 and history_rect.collidepoint(event.pos):
                            START_SCREEN = False
                            HISTORY_SCREEN = True

                        #����˳���Ϸ�¼�
                        if event.button == 1 and quit_rect.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
                        
                #���Ʒ���ͼ
                screen.blit(start_background,(0,0))
                
                #���ƿ�ʼ����
                screen.blit(start_image,start_rect)

                #������Ϸ˵������
                screen.blit(help_image,help_rect)

                #������ʷ��¼����
                screen.blit(history_image,history_rect)
                
                #�����˳�����
                screen.blit(quit_image,quit_rect)

                clock.tick(60)
                
                pygame.display.flip()

            

            #===============================================��Ϸ˵������============================================================
            if HELP_SCREEN:
                for event in pygame.event.get():
                    #����رհ�ť
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    #��갴��
                    if event.type == MOUSEBUTTONDOWN:
                        #������ذ�ť
                        if event.button == 1 and back_rect.collidepoint(event.pos):
                            START_SCREEN = True
                            HELP_SCREEN = False

                #������Ϸ˵��ͼ
                screen.blit(doc_background,(0,0))

                #���Ʒ��ذ���
                screen.blit(back_image,back_rect)

                clock.tick(60)

                pygame.display.flip()

            
            #===============================================��ʷ��¼����============================================================           
            if HISTORY_SCREEN:
                for event in pygame.event.get():
                    #����رհ�ť
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    #��갴��
                    if event.type == MOUSEBUTTONDOWN:
                        #������ذ�ť
                        if event.button == 1 and back_rect.collidepoint(event.pos):
                            START_SCREEN = True
                            HISTORY_SCREEN = False

                #���Ʊ���
                screen.blit(history_background,(0,0))

                #���Ʒ��ذ���
                screen.blit(back_image,back_rect)
                            
                #��ȡ��ʷ��ߵ÷��ļ�
                with open("record.txt","r") as f:
                    best_score = f.readline()

                #��ӡ��Ѽ�¼
                best_font = pygame.font.Font("font/font2.ttf",48)
                best_text = best_font.render("Best record : "+best_score+"!",True,RED)
                best_text_rect = 20,300
                
                screen.blit(best_text,best_text_rect)
                

                clock.tick(60)

                pygame.display.flip()
                

            #===============================================��Ϸ����================================================================        
            if GAME_SCREEN:
                
                for event in pygame.event.get():
                    #����رհ�ť
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    #������ͣ
                    elif event.type == MOUSEBUTTONDOWN:
                        #�¼����������ͣ��
                        if event.button == 1 and pause_rect.collidepoint(event.pos):
                            pause = not pause
                            if pause:
                                pygame.time.set_timer(SUPPLYTIMER,0)#������ͣ
                                pygame.mixer.music.pause()#����������ͣ
                                pygame.mixer.pause()#��Ч��ͣ
                            else:
                                pygame.time.set_timer(SUPPLYTIMER,30 * 1000)#������ͣ
                                pygame.mixer.music.unpause()#����������ͣ
                                pygame.mixer.unpause()#��Ч��ͣ

                    #���������ͣ��ʱ��ɫ����
                    elif event.type == MOUSEMOTION:
                        if pause_rect.collidepoint(event.pos):
                            if pause:
                                pause_image = resume_pressed_image
                            else:
                                pause_image = pause_pressed_image
                        else:
                            if pause:
                                pause_image = resume_nor_image
                            else:
                                pause_image = pause_nor_image

                    #�ո������ȫ��ը��
                    elif event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            if bomb_num:
                                bomb_num -= 1
                                bomb_sound.play()
                                for each in enemies:
                                    if each.rect.bottom > 0 and each not in boss_enemies:
                                        each.alive = False

                    #��ʱ���Ų���
                    elif event.type == SUPPLYTIMER:
                        supply_sound.play()
                        if random.choice([True,False]):
                            bomb_supply.reset()
                        else:
                            bullet_supply.reset()

                    #�ص������ӵ�
                    elif event.type == DOUBLE_BULLET_TIME:
                        is_double_bullet = False
                        pygame.time.set_timer(DOUBLE_BULLET_TIME,0)

                    #�޵�ʱ�䵽
                    elif event.type == INVINCIBLE_TIMER:
                        me.invincible = False
                        pygame.time.set_timer(INVINCIBLE_TIMER,0)
                            
                #�����û��÷������Ѷ�
                if level == 1 and score > 1000:
                    #============
                    level = 5
                    score = 14900000
                    
                    #level = 2
                    upgrade_sound.play()
                    #����3��С�͵л���2�����ͣ�1�ܴ���
                    add_small_enemies(enemies,small_enemies,3)
                    add_mid_enemies(enemies,mid_enemies,2)
                    add_big_enemies(enemies,big_enemies,1)
                    #����С�ͷɻ��ٶ�
                    inc_speed(small_enemies,1)
                elif level == 2 and score > 300000:
                    level = 3
                    upgrade_sound.play()
                    #����5��С�͵л���3�����ͣ�2�ܴ���
                    add_small_enemies(enemies,small_enemies,5)
                    add_mid_enemies(enemies,mid_enemies,3)
                    add_big_enemies(enemies,big_enemies,2)
                    #����С�ͷɻ��ٶ�,�������ͷɻ��ٶ�
                    inc_speed(small_enemies,1)
                    inc_speed(mid_enemies,1)
                elif level == 3 and score > 600000:
                    level = 4
                    upgrade_sound.play()
                    #����5��С�͵л���3�����ͣ�2�ܴ���
                    add_small_enemies(enemies,small_enemies,5)
                    add_mid_enemies(enemies,mid_enemies,3)
                    add_big_enemies(enemies,big_enemies,2)
                    #����С�ͷɻ��ٶ�,�������ͷɻ��ٶ�
                    inc_speed(small_enemies,1)
                    inc_speed(mid_enemies,1)
                elif level == 4 and score > 1000000:
                    level = 5
                    upgrade_sound.play()
                    #����5��С�͵л���3�����ͣ�2�ܴ���
                    add_small_enemies(enemies,small_enemies,5)
                    add_mid_enemies(enemies,mid_enemies,3)
                    add_big_enemies(enemies,big_enemies,2)
                    #����С�ͷɻ��ٶ�,�������ͷɻ��ٶ�
                    inc_speed(small_enemies,1)
                    inc_speed(mid_enemies,1)
                    
                elif level == 5 and score > 1200000:
                    level = 6
                    BOSS_LEVEL = True
                    BOSS_LIVE = True
                    #��յл�Ⱥ
                    enemies.empty()
                    small_enemies.empty()
                    mid_enemies.empty()
                    big_enemies.empty()
                    
                    #��boss��ӵ��л�Ⱥ��
                    add_boss_enemies(boss_enemies,enemies,1)
                    
                
                #���Ʊ���
                if BOSS_LEVEL and not pause and life_num :
                    boss_background.move()
                    screen.blit(boss_background.image,(0,boss_background.rect.top))
                else:
                    background = background1
                    screen.blit(background,(0,0))
                    
                #������ͣ��
                screen.blit(pause_image,pause_rect)

                #û�е����ͣ�������������Ϸ
                if life_num and not pause:            
                        
                    #����û��ļ��̲���
                    key_pressed = pygame.key.get_pressed()

                    if key_pressed[K_w] or key_pressed[K_UP]:
                        me.moveup()
                    if key_pressed[K_s] or key_pressed[K_DOWN]:
                        me.movedown()
                    if key_pressed[K_a] or key_pressed[K_LEFT]:
                        me.moveleft()
                    if key_pressed[K_d] or key_pressed[K_RIGHT]:
                        me.moveright()

                    #����ȫ��ը���������Ҽ���Ƿ���
                    if bomb_supply.alive and not BOSS_LEVEL:
                        bomb_supply.move()
                        screen.blit(bomb_supply.image,bomb_supply.rect)
                        if pygame.sprite.collide_mask(me,bomb_supply):
                            get_bomb_sound.play()
                            if bomb_num < 3:
                                bomb_num += 1
                            bomb_supply.alive = False

                    #���Ƴ����ӵ��������Ҽ���Ƿ���
                    if bullet_supply.alive and not BOSS_LEVEL:
                        bullet_supply.move()
                        screen.blit(bullet_supply.image,bullet_supply.rect)
                        if pygame.sprite.collide_mask(me,bullet_supply):
                            get_bullet_sound.play()
                            is_double_bullet = True
                            pygame.time.set_timer(DOUBLE_BULLET_TIME,18 * 1000)
                            bullet_supply.alive = False
                            
                    #�ҷ��ɻ������ӵ�
                    if not (delay % 10):
                        bullet_sound.play()
                        if is_double_bullet:
                            bullets = bullet2
                            bullets[bullet2_index].reset(((me.rect.centerx-32),me.rect.centery-2))
                            bullets[bullet2_index+1].reset(((me.rect.centerx+21),me.rect.centery-2))
                            bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                        else:
                            bullets = bullet1
                            bullets[bullet1_index].reset((me.rect.midtop[0]-4,me.rect.midtop[1]))
                            bullet1_index = (bullet1_index + 1) % BULLET1_NUM

                    #BOSS�����ӵ�================
                    if not (delay % 20) and BOSS_LEVEL:
                        for e in boss_enemies:
                            
                            bullet_boss[bullet_b_index].reset((e.rect.midtop[0],e.rect.midbottom[1]))
                            bullet_boss[bullet_b_index].kind = (bullet_b_index + 1) % 3
                            bullet_b_index = (bullet_b_index + 1) % BULLET_B_NUM


                    #����ҷ��ӵ��Ƿ���ел�
                    for b in bullets:
                        if b.alive:
                            b.move()
                            screen.blit(b.image,b.rect)
                            enemies_hit = pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                            if enemies_hit:
                                for e in enemies_hit:
                                    #�������ͻ���͵л�
                                    if e in mid_enemies or e in big_enemies :
                                        e.hit = True
                                        e.energy = e.energy - 1
                                        #�����ɱ�˴��͵л��������޵�BUFF
                                        if e.energy == 0 and e in big_enemies:
                                            invincible_supply.alive = True
                                            invincible_supply.rect.left ,invincible_supply.rect.top = e.rect.midtop
                                            e.alive = False
                                            
                                        elif e.energy == 0 and e in mid_enemies:
                                            e.alive = False
                                            
                                    #����С�͵л�
                                    elif e in small_enemies:
                                        e.energy = 0
                                        e.alive = False

                                    #����Boss
                                    elif e in boss_enemies:
                                        e.energy -= 1
                                        #��ɱ��Boss
                                        if e.energy == 0 :
                                            e.alive = False
                                            
                    #���BOSS�ӵ��Ƿ�����ҷ��ɻ�,�������ӵ�
                    if BOSS_LEVEL and BOSS_LIVE:
                        
                        for b in bullet_boss:
                            if b.alive:
                                if b.kind == 0:
                                    b.move0()
                                    b.image = b.image0
                                elif b.kind ==1:
                                    b.move1()
                                    b.image = b.image1
                                elif b.kind == 2:
                                    b.move2()
                                    b.image = b.image2
                                screen.blit(b.image,b.rect)
                                me_hit = pygame.sprite.collide_mask(me,b)
                                if me_hit and not me.invincible:
                                    me.alive = False

                                        
                    #�����޵�BUFF�������Ҽ���Ƿ���(10��)
                    if invincible_supply.alive:
                        invincible_supply.move()
                        screen.blit(invincible_supply.image,invincible_supply.rect)
                        if pygame.sprite.collide_mask(me,invincible_supply):
                            #get_invincible_sound.play()
                            me.invincible = True
                            pygame.time.set_timer(INVINCIBLE_TIMER,5 * 1000)
                            invincible_supply.alive = False
                            
                    #����BOSS�л�
                    if BOSS_LEVEL:
                        for each in boss_enemies:
                            if each.alive:
                                each.move()
                                screen.blit(each.image,each.rect)
                                #����Ѫ��
                                pygame.draw.line(screen,BLACK,\
                                                 (each.rect.left,each.rect.top - 5),\
                                                 (each.rect.right,each.rect.top - 5),\
                                                 2)
                                #����������20%,��ʾ��ɫ�������ɫ
                                energy_remain = each.energy / boss.Boss.Energy
                                if energy_remain > 0.2:
                                    energy_color = GREEN
                                else:
                                    energy_color = RED
                                pygame.draw.line(screen,energy_color,\
                                                 (each.rect.left,each.rect.top - 5),\
                                                 (each.rect.left + each.rect.width * energy_remain,each.rect.top - 5),\
                                                 2)
                            else:
                                
                                
                                #����ɻ�
                                if not(delay % 20):
                                    if boss_destroy_index == 0: 
                                        enemy2_down_sound.play()
                                        BOSS_LIVE = False
                                    screen.blit(each.destroy_images[boss_destroy_index],each.rect)
                                    boss_destroy_index = (boss_destroy_index + 1 ) % 8
                                    if boss_destroy_index == 0:
                                        score += 10000
                                        #enemy3_fly_sound.stop()
                                        each.reset()
                                        
                                        #ת���������
                                        life_num = 0

                                        #��ϲ��ΪTrue
                                        congrat = True
                                        

                                
                    #���ƴ��ͷɻ�
                    if not BOSS_LEVEL:
                        for each in big_enemies:
                            if each.alive:
                                each.move()
                                if each.hit:
                                    #���ƴ򵽵���Ч
                                    screen.blit(each.image_hit,each.rect)
                                    each.hit = False
                                else:
                                    if switch_image:
                                        screen.blit(each.image1,each.rect)
                                    else:
                                        screen.blit(each.image2,each.rect)

                                #����Ѫ��
                                pygame.draw.line(screen,BLACK,\
                                                 (each.rect.left,each.rect.top - 5),\
                                                 (each.rect.right,each.rect.top - 5),\
                                                 2)
                                #����������20%,��ʾ��ɫ�������ɫ
                                energy_remain = each.energy / enemy.BigEnemy.Energy
                                if energy_remain > 0.2:
                                    energy_color = GREEN
                                else:
                                    energy_color = RED
                                pygame.draw.line(screen,energy_color,\
                                                 (each.rect.left,each.rect.top - 5),\
                                                 (each.rect.left + each.rect.width * energy_remain,each.rect.top - 5),\
                                                 2)
                                
                                #�������֣�������Ч
                                if each.rect.bottom > -50:
                                   enemy3_fly_sound.play(-1)
                            else:
                                #����ɻ�
                                if not(delay % 3):
                                    if e3_destroy_index == 0:  
                                        enemy3_down_sound.play()
                                    screen.blit(each.destroy_images[e3_destroy_index],each.rect)
                                    e3_destroy_index = (e3_destroy_index + 1 ) % 6
                                    if e3_destroy_index == 0:
                                        score += 10000
                                        enemy3_fly_sound.stop()
                                        each.reset()
                            
                    #�������ͷɻ�
                    if not BOSS_LEVEL:
                        for each in mid_enemies:
                            if each.alive:
                                each.move()
                                if each.hit:
                                    #���ƴ򵽵���Ч
                                    screen.blit(each.image_hit,each.rect)
                                    each.hit = False
                                else:
                                    screen.blit(each.image,each.rect)
                                
                                #����Ѫ��
                                pygame.draw.line(screen,BLACK,\
                                                 (each.rect.left,each.rect.top - 5),\
                                                 (each.rect.right,each.rect.top - 5),\
                                                 2)
                                #����������20%,��ʾ��ɫ�������ɫ
                                energy_remain = each.energy / enemy.MidEnemy.Energy
                                if energy_remain > 0.2:
                                    energy_color = GREEN
                                else:
                                    energy_color = RED
                                pygame.draw.line(screen,energy_color,\
                                                 (each.rect.left,each.rect.top - 5),\
                                                 (each.rect.left + each.rect.width * energy_remain,each.rect.top - 5),\
                                                 2)
                            else:
                                #����ɻ�
                                if not(delay % 3):
                                    if e2_destroy_index == 0:
                                        enemy2_down_sound.play()
                                    screen.blit(each.destroy_images[e2_destroy_index],each.rect)
                                    e2_destroy_index = (e2_destroy_index + 1) % 4
                                    if e2_destroy_index == 0:
                                        score += 6000
                                        each.reset()

                    #����С�ͷɻ�
                    if not BOSS_LEVEL:
                        for each in small_enemies:
                            if each.alive:
                                each.move()
                                screen.blit(each.image,each.rect)
                            else:
                                #����ɻ�
                                if not (delay % 3):
                                    if e1_destroy_index == 0:
                                        enemy1_down_sound.play()
                                    screen.blit(each.destroy_images[e1_destroy_index],each.rect)
                                    e1_destroy_index = (e1_destroy_index + 1) % 4
                                    if e1_destroy_index == 0:
                                        score += 1000
                                        each.reset()

                    #����ҷ��ɻ��Ƿ�ײ
                    enemies_down = pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)             
                    if enemies_down and not me.invincible:
                        me.alive = False
                        for each in enemies_down:
                            each.alive = False
                    
                    #�����ҷ��ɻ�
                    if me.alive:
                        if switch_image:
                            screen.blit(me.image1,me.rect)
                        else:
                            screen.blit(me.image2,me.rect)
                        
                    else:
                        #�ɻ�����
                        if not (delay % 3):
                            if me_destroy_index == 0:
                                mine_down_sound.play()
                            screen.blit(me.destroy_images[me_destroy_index],me.rect)
                            me_destroy_index = (me_destroy_index + 1) % 4
                            if me_destroy_index == 0:
                                life_num -= 1
                                me.reset()
                                pygame.time.set_timer(INVINCIBLE_TIMER,3 * 1000)
                                
                    #�����޵�BUFF
                    if me.invincible:
                        invincible_rect.left , invincible_rect.top = me.rect.left-14 , me.rect.top-12
                        screen.blit(invincible_image,invincible_rect)
                                
                    #���Ƶ÷���ʾ
                    score_text = score_font.render("Score : %s" % str(score),True,WHITE)
                    screen.blit(score_text,(10,5))

                    #���Ƶȼ���ʾ
                    level_text = level_font.render("Level : %s" % str(level),True,WHITE)
                    screen.blit(level_text,(10,40))

                    #����ȫ��ը������
                    if not BOSS_LEVEL:
                        bomb_text = bomb_font.render("x %d" % bomb_num,True,TINT_RED)
                        text_rect = bomb_text.get_rect()
                        screen.blit(bomb_image,(10, height - 10 - bomb_rect.height))
                        screen.blit(bomb_text,(28+bomb_rect.width,height - 5 -text_rect.height))

                    #�����ҷ���������
                    if life_num:
                        for i in range(life_num):
                            screen.blit(life_image,\
                                        (width-10-(i+1)*life_rect.width,\
                                         height-10-life_rect.height))

                    #�л�ͼƬʱ��
                    if not(delay % 5):
                        switch_image = not switch_image
                    
                    #�����ӳ� 
                    delay -= 1
                    if not delay:
                        delay = 200
                        
                #��Ϸ����
                elif life_num == 0:
                

                    
                    #��������ֹͣ
                    pygame.mixer.music.stop()
                    
                    #ֹͣȫ����Ч
                    pygame.mixer.stop()

                    #ֹͣ���Ų���
                    pygame.time.set_timer(SUPPLYTIMER,0)

                    if not recorded:
                        recorded = True
                        
                        #��ȡ��ʷ��ߵ÷��ļ�
                        with open("record.txt","r") as f:
                            record_score = int(f.readline())

                        #�����ҵ÷ָ�����ʷ�÷�
                        if score > record_score:
                            
                            with open("record.txt","w") as f:
                                f.write(str(score))

                    #==================���ƽ�������=======================================================

                    #��óɼ���ӡ
                    record_score_text = score_font.render("Best : %d" % int(record_score),True,WHITE)
                    screen.blit(record_score_text,(50,50))

                    #��ϲ������ӡ
                    if congrat:
                        congrat_text1 = congrat_font1.render("Winner winner",True,RED)
                        congrat_text_rect1 = congrat_text1.get_rect()
                        congrat_text_rect1.left, congrat_text_rect1.top = \
                                                  (width - congrat_text_rect1.width) // 2 ,height//2 - 190
                        screen.blit(congrat_text1,congrat_text_rect1)

                        congrat_text2 = congrat_font2.render("Chicken dinner",True,RED)
                        congrat_text_rect2 = congrat_text2.get_rect()
                        congrat_text_rect2.left, congrat_text_rect2.top = \
                                                  (width - congrat_text_rect2.width) // 2 ,height//2 - 150
                        screen.blit(congrat_text2,congrat_text_rect2)

                    #���ֵ÷���ʾ
                    gameover_text1 = gameover_font.render("Your Score",True,WHITE)
                    gameover_text1_rect = gameover_text1.get_rect()
                    gameover_text1_rect.left, gameover_text1_rect.top = \
                                              (width - gameover_text1_rect.width) // 2 ,height//2 - 100
                    screen.blit(gameover_text1,gameover_text1_rect)

                    gameover_text2 = gameover_font.render(str(score),True,WHITE)
                    gameover_text2_rect = gameover_text2.get_rect()
                    gameover_text2_rect.left , gameover_text2_rect.top = \
                                             (width - gameover_text2_rect.width) // 2,\
                                             gameover_text1_rect.bottom + 10
                    screen.blit(gameover_text2,gameover_text2_rect)

                    #�Ƽ�¼��ӡ��ϲ��ʶ
                    if score > record_score:
                        record_image_rect.left , record_image_rect.top = 290 , 280
                        screen.blit(record_image,record_image_rect)


                    #������Ϸ����
                    again_rect.left,again_rect.top = \
                                                   (width - again_rect.width) // 2,\
                                                   gameover_text2_rect.bottom + 50
                    screen.blit(again_image,again_rect)

                    #��Ϸ��������
                    gameover_rect.left,gameover_rect.top = \
                                                         (width - again_rect.width) // 2,\
                                                         again_rect.bottom + 10
                    screen.blit(gameover_image,gameover_rect)
                    

                    #����û�������
                    if pygame.mouse.get_pressed()[0]:
                        
                        #��ȡ�������
                        pos = pygame.mouse.get_pos()
                        
                        #���������¿�ʼ����
                        if again_rect.left < pos[0] < again_rect.right and \
                           again_rect.top < pos[1] < again_rect.bottom:
                            main()

                        #��������Ϸ��������
                        elif gameover_rect.left < pos[0] < gameover_rect.right and \
                             gameover_rect.top < pos[1] < gameover_rect.bottom:
                            pygame.quit()
                            sys.exit()
                
                #֡�ʿ���
                clock.tick(50)
                        
                pygame.display.flip()
                        

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
