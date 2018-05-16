import pygame
from pygame.sprite import Sprite
class Alien(Sprite):
    def __init__(self,ai_settings,screen):
        '''初始化外星人并设置起始位置'''
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # 加载外星人图像，设置 rect 属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        
        # 每个外星人最初在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #  存储外星人准确位置
        self.x = float(self.rect.x)
    
    def blite(self):
        '''绘制外星人'''
        self.screen.blit(self.image,self.rect)
    
    def update(self):
        '''向右移动'''
        self.x += (self.ai_settings.alien_speed_factor *
            self.ai_settings.fleet_direction)
        self.rect.x = self.x
    
    def check_edges(self):
        '''外星人在屏幕边缘，返回 True'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        
        
