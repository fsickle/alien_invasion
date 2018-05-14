# 存储游戏运行函数
import sys # 退出游戏

import pygame
from bullet import Bullet

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    '''响应按键'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    # 不知为何不能使用空格，使用箭头代替
    elif event.key == pygame.K_UP:
        fire_bullet(ai_settings,screen,ship,bullets)
                
def check_keyup_events(event,ship):
    '''响应松开'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
                
def check_events(ai_settings,screen,ship,bullets):
    '''响应鼠标和键盘事件'''
    # 监视键盘和鼠标事件
    for event in pygame.event.get():
        # 退出游戏
        if event.type == pygame.QUIT:
            sys.exit()
        # 对键盘左右箭头响应
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
                        
# 更新屏幕                
def update_screen(ai_settings,screen,ship,bullets):
        # 绘制屏幕填充
        screen.fill(ai_settings.bg_color)
        ship.blitme()
        # 重绘所有子弹,bullets.sprites 返回一个列表,包含所有精灵
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        # 绘制飞船，并确保出现在背景前方
        
        pygame.display.flip()


def update_bullets(bullets):
    # 会为每个 bullet 更新
        bullets.update()
        # 遍历副本，删除条目
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
        #print(len(bullets))

def fire_bullet(ai_settings,screen,ship,bullets):
    # 创建一颗子弹，并将其加入编组 bullets 中
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)
