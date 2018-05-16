# 管理飞船的大部分行为
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    # 传入 screen,ai_settings 实例 
    def __init__(self,ai_settings,screen):
        super().__init__()
        '''初始化飞船，并设置其位置'''
        self.screen = screen
        self.ai_settings = ai_settings
        
        # 载入 image
        self.image = pygame.image.load('images/ship.bmp')
        # 获取图像的外接矩形
        self.rect = self.image.get_rect()
        # 获取屏幕的外接矩形
        self.screen_rect = self.screen.get_rect()
        
        # 定义飞船位置为屏幕底部中央
        self.rect.bottom = self.screen_rect.bottom
        self.rect.centerx = self.screen_rect.centerx
        
        # 在飞船的属性 center 中存储小数值
        self.center = float(self.rect.centerx)
        # 移动标志
        self.moving_right = False
        self.moving_left = False
        
    def update(self):
        '''根据移动标志调整飞船位置'''
        if self.moving_right and self.rect.right <self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        # 使用 if，让左右优先级相等
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        # 更新 rect 对象,只存储了 center 的整数部分
        self.rect.centerx = self.center 
        
    def blitme(self):
        '''绘制飞船'''
        self.screen.blit(self.image,self.rect)
    
    def center_ship(self):
        self.center = self.screen_rect.centerx

