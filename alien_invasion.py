import sys # 退出游戏 

from settings import Settings
import pygame

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
    
    # 游戏主循环
    while True:
        
        # 监视键盘和鼠标事件
        for even in pygame.event.get():
            # 退出游戏
            if even.type == pygame.QUIT:
                sys.exit()
        # 绘制屏幕
        screen.fill(ai_settings.bg_color)
        # 绘制空屏幕，擦去旧屏幕，不断更新，显示最近绘制的屏幕
        pygame.display.flip()
    
run_game()
