from boat import Boat
from math import pi, sqrt,sin,cos
from bullet import Bullet
from random import uniform
class Alien(Boat):#外星人以飞船作为子类，向飞船靠近
    def __init__(self, lenth=100.0, cen_pos=(0,0), shape=..., theta=0, color=..., v=(0,0), bullet_v=2, a=0.1,cooldown = 5,distance = 100,health=100,bullet_number = 1,bullet_scatter=pi,bullet_type=0):
        super().__init__(lenth, cen_pos, shape, theta, color, v, bullet_v, a,cooldown,bullet_number,health,bullet_scatter,bullet_type)
        self.distance = distance #设定的控制距离
        self.bullet_time = 0

    def need_speedup(self,playercen_pos):
        if sqrt((self.cen_pos[0]-playercen_pos[0])**2+(self.cen_pos[1]-playercen_pos[1])**2)>self.distance:
            return True
        else:
            return False

    def attack(self):
        self.bullet_time += 1
        if self.bullet_time == self.cooldown:
            b = Bullet(v = (self.bullet_v*sin(self.theta)+self.v[0],self.bullet_v*cos(self.theta)+self.v[1]),theta=self.theta,color = self.color,pos=(self.cen_pos[0]+sin(self.theta)*self.lenth,self.cen_pos[1]+cos(self.theta)*self.lenth))
            self.bullet_time = 0
            #子弹发射产生反作用力（亦即产生反方向的速度）
            delta_v = 1
            self.v=(self.v[0]-sin(self.theta)*delta_v,self.v[1]-cos(self.theta)*delta_v)
            return b
        else:
            return None

    def display(self, screen, to_pos, playerv):
        super().display(screen, to_pos, playerv)
        self.rect.update(self.cen_pos[0] - self.rel2 / 2, self.cen_pos[1] - self.rel2 / 2, self.rel2, self.rel2)
#设置
def alien_summon(r,cen_pos,alien_color=(249,165,241),side_num = 4):
    # r为生成半径,cen_pos为屏幕中心坐标
    alpha = uniform(0,2*pi)
    cen_pos = (cen_pos[0]+sin(alpha)*r,cen_pos[1]+cos(alpha)*r)
    return Alien(30,cen_pos,[i for i in range(side_num)],0,alien_color,cooldown=30) #设置外星人召唤
