# 存储游戏运行函数
import sys # 退出游戏

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    '''响应按键'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    # 不知为何不能使用空格，使用箭头代替
    elif event.key == pygame.K_UP:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_DOWN:
        sys.exit()
                
def check_keyup_events(event,ship):
    '''响应松开'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
                
def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get_pos 返回 x,y 坐标
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,
                ship,aliens,bullets,mouse_x,mouse_y)
                        
# 更新屏幕                
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
        # 绘制屏幕填充
        screen.fill(ai_settings.bg_color)
        ship.blitme()
        # 重绘所有子弹,bullets.sprites 返回一个列表,包含所有精灵
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        # 绘制飞船，并确保出现在背景前方
        sb.show_score()
        
        aliens.draw(screen)
        if not stats.game_active:
            play_button.draw_button()
            
        pygame.display.flip()


def update_bullets(ai_settings,screen,stats,sb,ship,bullets,aliens):
    # 会为每个 bullet 更新
        bullets.update()
        # 遍历副本，删除条目
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
        #print(len(bullets))
        check_bullet_alien_collisions(ai_settings,screen,stats,sb,
            ship,aliens,bullets)
        

def fire_bullet(ai_settings,screen,ship,bullets):
    # 创建一颗子弹，并将其加入编组 bullets 中
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def creat_fleet(ai_settings,screen,ship,aliens):
    alien = Alien(ai_settings,screen)
    number_alien_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,
        ship.rect.height,alien.rect.height)
    # 创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            creat_alien(ai_settings,screen,aliens,alien_number,row_number)
        
    
def get_number_aliens_x(ai_settings,alien_width):
    avaliable_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(avaliable_space_x / (2 * alien_width))
    return number_alien_x

def creat_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y = (ai_settings.screen_height - 
        (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    # 检测飞船与外星人的碰撞,spritecollideany,接受一个精灵，一个编组，并返回编组的碰撞成员
    # 会调用 ship.rect
    if pygame.sprite.spritecollideany(ship,aliens):
        # print('ship hit!')
        ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
    check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_fleet_edges(ai_settings,aliens):
    '''外星人在边缘时，采取措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            chang_fleet_direction(ai_settings,aliens)
            break

def chang_fleet_direction(ai_settings,aliens):
    '''下移外星人，并改变方向'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,
        ship,aliens,bullets):
    # 检测子弹是否击中外星人,碰撞后返回 dict(bullet:alien)
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    
    if collisions:
        for aliens in collisions.values():
            
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats,sb)
        
    if len(aliens) == 0:
    # 删除现有子弹，并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        
        # 提高等级
        stats.level += 1
        sb.prep_level()
        
        creat_fleet(ai_settings,screen,ship,aliens)
    

def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
    '''响应被外星人撞到的飞船'''
    if stats.ships_left > 0:
        stats.ships_left -= 1
    
        # 清空
        aliens.empty()
        bullets.empty()
    
        # 创建新的,飞船之余中央
        creat_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        
        sb.prep_ships()
    
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
        

def check_aliens_bottom(ai_setting,screen,stats,sb,ship,aliens,bullets):
    '''检测外星人到达底部'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞结果一样
            ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)
            break
    
def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,
        bullets,mouse_x,mouse_y):
    # 检测鼠标是否在 play 按钮内
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        stats.reset_stats()
        stats.game_active = True
        
        # 重置计分牌图案
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()
        
        ai_settings.initialize_dynamic_settings()
        # 隐藏鼠标光标
        pygame.mouse.set_visible(False)
    
def check_high_score(stats,sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
