from settings import Settings
import pygame
from ship import Ship
import game_functions as gf
from pygame.sprite import Group 

def run_game():
    # 初始化游戏
    pygame.init()
    # Settings 类的实例
    ai_settings = Settings()
    # 创建屏幕对象,返回屏幕大小
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))

    # 设置标题
    pygame.display.set_caption('wangker:Alien Invasion')
    # 设置背景色
    #bg_color = (230,230,230)
    # 创建飞船
    ship = Ship(ai_settings,screen)
    # 创建一个用于存储子弹的编组
    bullets = Group()
    
    # 游戏主循环
    while True:
        
        gf.check_events(ai_settings,screen,ship,bullets)
        
        ship.update()
        gf.update_bullets(bullets)
        gf.update_screen(ai_settings,screen,ship,bullets)
        # 绘制空屏幕，擦去旧屏幕，不断更新，显示最近绘制的屏幕
        
        
    
run_game()
