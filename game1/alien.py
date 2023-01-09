import random

from boat import Boat
from math import pi, sqrt, sin, cos,log
from bullet import Bullet
from random import uniform,randint,choice
level_color = (255, 0, 0), (255, 128, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (128, 0, 255)
max_l=7


class Alien(Boat):  # 外星人以飞船作为子类，向飞船靠近
    def __init__(self, lenth=100.0, cen_pos=(0, 0), side_num = 10, theta=0.0, v=(0, 0), bullet_v=2, a=0.1,
                 cooldown=5, distance=100, health=100, bullet_scatter=pi, bullet_type=0, level=1):
        self.xp=10
        bullet_number = randint(1,int(1+log(level)))
        super().__init__(lenth, cen_pos, [i for i in range(side_num)], theta, level_color[(level % max_l) - 1], v, bullet_v, a,
                         cooldown,bullet_number, health, bullet_scatter, bullet_type)
        self.cooldown = cooldown * 10 / level
        self.health=self.health*level*5
        self.damage=self.damage+self.damage*level*0.2
        self.xp=int(self.xp+self.xp*level*0.5)
        self.distance = int(distance/(log(level)+1))  # 设定的控制距离
        self.bullet_time = 0
        self.bullet_number = bullet_number
        self.distance = distance  # 设定的控制距离
        self.level = level

    def need_speedup(self, playercen_pos):
        if sqrt((self.cen_pos[0] - playercen_pos[0]) ** 2 + (self.cen_pos[1] - playercen_pos[1]) ** 2) > self.distance:
            return True
        else:
            return False

    def attack(self):
        self.bullet_time += 1
        if self.bullet_time == self.cooldown:
            return super().attack()
        else:
            return None

    def display(self, screen, to_pos, playerv):
        super().display(screen, to_pos, playerv)
        self.rect.update(self.cen_pos[0] - self.rel2 / 2, self.cen_pos[1] - self.rel2 / 2, self.rel2, self.rel2)


class Summoner(Boat):
    def __init__(self,cen_pos,level):
        # 召唤师为六角星
        alpha = uniform(0, 2 * pi)
        r = 1000
        cen_pos = (cen_pos[0] + sin(alpha) * r, cen_pos[1] + cos(alpha) * r)
        super().__init__(90, cen_pos, [i for i in range(3)], 0, choice(level_color), bullet_v = 0,
                         cooldown = 300, bullet_number = 0, health = level * 1000,a = 0.05)
        self.level = level
        self.distance = 500
        self.summon_time = 240
        self.xp = 25*level

    def need_speedup(self, playercen_pos):
        if sqrt((self.cen_pos[0] - playercen_pos[0]) ** 2 + (self.cen_pos[1] - playercen_pos[1]) ** 2) > self.distance:
            return True
        else:
            return False

    def display(self, screen, to_pos, playerv):
        # 避免绘制原本的火焰长度
        self.fire_lenth = 0
        super().display(screen, to_pos, playerv)
        temp = (to_pos[0]-self.cen_pos[0],to_pos[1]-self.cen_pos[1])
        theta,self.theta = self.theta,self.theta + pi
        super().display(screen, (self.cen_pos[0]-temp[0],self.cen_pos[1]-temp[1]), (0,0))
        self.theta = theta
        self.rect.update(self.cen_pos[0] - self.rel2 / 2, self.cen_pos[1] - self.rel2 / 2, self.rel2, self.rel2)
        self.summon_time += 1

    def summon(self):
        alien_list = []
        if self.summon_time >= self.cooldown:
            self.summon_time -= self.cooldown
            theta = self.theta
            for i in range(6):
                alien_list.append(Alien(self.lenth/3,
                                    (self.cen_pos[0]+sin(theta)*self.lenth*2/3,self.cen_pos[1]+cos(theta)*self.lenth*2/3),
                                    3,theta,level = self.level,v = self.v))
                theta = (theta + pi/3)%(2*pi)
        return alien_list





# 设置
def alien_summon(r, cen_pos, alien_color=(249, 165, 241), side_num=4, level=1):
    # r为生成半径,cen_pos为屏幕中心坐标
    alpha = uniform(0, 2 * pi)
    cen_pos = (cen_pos[0] + sin(alpha) * r, cen_pos[1] + cos(alpha) * r)
    ret = randint(1, 100)
    t = randint(3, side_num)
    return Alien(30.0, cen_pos, t, 0, cooldown=30,
                 level=max((level-1 if ret<=30 else( level if ret<=90 else level+1)),1)) # 设置外星人召唤
