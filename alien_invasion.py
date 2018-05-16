from settings import Settings
import pygame
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien 
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

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
    # 创建 play 按钮
    play_button = Button(ai_settings,screen,'paly')
    # 创建用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)
    # 创建飞船
    ship = Ship(ai_settings,screen)
    # 创建一个用于存储子弹的编组
    bullets = Group()
    # 创建外星人
    aliens = Group()
    # 创建外星人群
    gf.creat_fleet(ai_settings,screen,ship,aliens)
    
    
    # 游戏主循环
    while True:
        
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,
            bullets)
        if stats.game_active:
        
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,bullets,aliens)
            gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)
        gf.update_screen(ai_settings,
            screen,stats,sb,ship,aliens,bullets,play_button)
        # 绘制空屏幕，擦去旧屏幕，不断更新，显示最近绘制的屏幕
        
        
    
run_game()
