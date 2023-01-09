import pygame
from math import sqrt

class Bullet:
    def __init__(self,r = 5,v = (0,0),pos = (0,0),theta = 0.0,color =(291,241,265),lifetime = 1000,damage = 5,delta_vk=0.1):
        self.r = r # 设置子弹半径
        self.v = v # 子弹速度
        self.pos = pos #子弹位置
        self.theta = theta #子弹朝向(非圆形情况下使用)
        self.color = color
        self.lifetime = lifetime
        self.r2=self.r*sqrt(2)
        self.rect = pygame.Rect(self.pos[0] - self.r2 / 2, self.pos[1] - self.r2 / 2, self.r2, self.r2)
        self.damage = damage
        #速度改变量的系数
        self.delta_vk = delta_vk
    #子弹射击速度计算
    def display(self,screen,playerv):
        pygame.draw.circle(screen,self.color,self.pos,self.r)
        self.pos = (self.pos[0] + self.v[0]-playerv[0],self.pos[1]+self.v[1]-playerv[1])
        self.rect.update(self.pos[0] - self.r / 2, self.pos[1] - self.r / 2, self.r, self.r)
        self.lifetime-=1



    def death(self):
        if self.lifetime <= 0:
            return True
        else: return False
    #子弹飞行超过一定时间后消亡
    def hit(self, hited):
        self.lifetime = -1#撞击后消亡
