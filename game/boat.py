from math import atan2, cos, pi, sin, sqrt
import pygame
from bullet import Bullet
class Boat():#太空船——（玩家与敌军的原型）
    def __init__(self, lenth = 100.0 ,cen_pos =(0,0) ,shape = [0,1,2],theta = 0,color = (291,241,165),v = (0,0),bullet_v = 10, a = 0.1,cooldown = 5,health = 100,bullet_number = 1,bullet_scatter = pi/3,bullet_type = 0,damage=5,delta_vk=0.1):
        self.lenth = lenth #定义大小
        self.cen_pos = cen_pos #中心位置
        self.shape = shape
        self.color = color
        self.theta = theta #初始角度
        self.omega = 0.05 #限定每帧转过的角度
        self.v = v #飞船速度
        self.bullet_v = bullet_v #子弹出膛速度
        self.a = a
        self.cooldown = cooldown #射击时子弹冷却时间
        self.speed = 1
        self.fire_lenth = 0 #火焰长度
        self.side_num = max(shape)+1
        self.rel = cos(pi / self.side_num) * self.lenth
        self.rel2 = self.rel * sqrt(3)
        self.rect = pygame.Rect(self.cen_pos[0] - self.rel2 / 2, self.cen_pos[1] - self.rel2 / 2, self.rel2, self.rel2)
        self.behit = 0  # 被撞击后会改变的参量
        self.bullet_damage = 5
        self.bullet_number = bullet_number
        self.bullet_scatter = bullet_scatter
        self.bullet_type = bullet_type
        self.health = health
        self.shielded = 0
        self.blutting = 1
        self.damage=damage
        self.delta_vk=delta_vk

    def display(self,screen,to_pos,playerv):
        m = self.side_num
        self.cen_pos = (self.cen_pos[0]+self.v[0]-playerv[0],self.cen_pos[1]+self.v[1]-playerv[1])
        alpha = atan2(to_pos[0]-self.cen_pos[0],to_pos[1]-self.cen_pos[1])
        self.v = (self.v[0]*0.99,self.v[1]*0.99)
        if alpha<0:alpha+=2*pi
        if(min(2*pi-abs(alpha-self.theta),abs(alpha-self.theta))<=self.omega):
            self.theta = alpha
        elif 0 < alpha - self.theta < pi or -2*pi < alpha-self.theta < -pi:
            self.theta += self.omega
            if self.theta >= 2*pi:
                self.theta -= 2*pi
        else:
            self.theta -= self.omega
            if self.theta < 0:
                self.theta += 2*pi
        point_list = []
        theta = self.theta
        for i in range(m):
            point_list.append((self.cen_pos[0]+sin(theta)*self.lenth,self.cen_pos[1]+cos(theta)*self.lenth))
            theta+=2*pi/m
        
        poly_point_list = [point_list[i] for i in self.shape]
        width = 5
        pygame.draw.aalines(screen,self.color,True,poly_point_list)
        #绘制中心点
        pygame.draw.circle(screen,self.color,self.cen_pos,width)
        #绘制炮管
        pygame.draw.circle(screen,(0,0,255),point_list[0],width)
        #绘制尾焰
        fire_point_list = []
        if(len(point_list)%2==0):
            n = len(point_list)//2
            fire_point_list.append(((point_list[n-1][0]+point_list[n][0])/2,((point_list[n-1][1]+point_list[n][1])/2)))
            fire_point_list.append(point_list[n])
            fire_point_list.append(((point_list[n+1][0]+point_list[n][0])/2,((point_list[n+1][1]+point_list[n][1])/2)))
            theta = pi + self.theta
            lenth = self.lenth + self.fire_lenth
            fire_point_list.append((self.cen_pos[0]+sin(theta)*lenth,self.cen_pos[1]+cos(theta)*lenth))
        else:
            n = len(point_list)//2
            fire_point_list.append(point_list[n+1])
            fire_point_list.append(point_list[n])
            theta = pi + self.theta
            lenth = self.fire_lenth
            fire_point_list.append(((point_list[n][0]+point_list[n+1][0])/2+sin(theta)*lenth,(point_list[n][1]+point_list[n+1][1])/2+cos(theta)*lenth))
        self.fire_lenth *= 0.95
        pygame.draw.polygon(screen,self.color,fire_point_list)

    def speedup(self):
        self.v=(self.v[0]+sin(self.theta)*self.a,self.v[1]+cos(self.theta)*self.a)
        self.fire_lenth = self.fire_lenth+4

    def attack(self):
        b_list = []
        if self.bullet_number == 1:
            b_list.append(Bullet(v = (self.bullet_v*sin(self.theta)+self.v[0],self.bullet_v*cos(self.theta)+self.v[1]),theta=self.theta,color = self.color,pos=(self.cen_pos[0]+sin(self.theta)*self.lenth,self.cen_pos[1]+cos(self.theta)*self.lenth),damage=self.bullet_damage))
        else:
            match self.bullet_type:
                case 0:
                    #对应散射的情况
                    theta = self.theta-self.bullet_scatter/2
                    theta = (theta + 2*pi)%(2*pi)
                    delta_theta = self.bullet_scatter/(self.bullet_number-1)
                    for i in range(self.bullet_number):
                        b_list.append(Bullet(v = (self.bullet_v*sin(theta)+self.v[0],self.bullet_v*cos(theta)+self.v[1]),theta=theta,color = self.color,pos=(self.cen_pos[0]+sin(self.theta)*self.lenth,self.cen_pos[1]+cos(self.theta)*self.lenth),damage=self.bullet_damage))
                        theta += delta_theta
                        theta %= 2*pi
                case 1:
                    #平射
                    if self.bullet_number%2 == 1:
                        #奇数的情况，则中心点发出弹药
                        b_list.append(Bullet(v = (self.bullet_v*sin(self.theta)+self.v[0],self.bullet_v*cos(self.theta)+self.v[1]),theta=self.theta,color = self.color,pos=(self.cen_pos[0]+sin(self.theta)*self.lenth,self.cen_pos[1]+cos(self.theta)*self.lenth),damage=self.bullet_damage))
                    #再分开处理两边的情况
                    num = self.bullet_number//2
                    theta = 2*pi/self.side_num
                    theta = (self.theta - theta + 2*pi)%(2*pi)
                    p0 = (self.cen_pos[0]+sin(theta)*self.lenth,self.cen_pos[1]+cos(theta)*self.lenth)
                    p1 = (self.cen_pos[0]+sin(self.theta)*self.lenth,self.cen_pos[1]+cos(self.theta)*self.lenth)
                    for i in range(num):
                        b_list.append(Bullet(v = (self.bullet_v*sin(self.theta)+self.v[0],self.bullet_v*cos(self.theta)+self.v[1]),theta=self.theta,color = self.color,pos=(p0[0]*(num-i)/num+p1[0]*i/num,p0[1]*(num-i)/num+p1[1]*i/num),damage=self.bullet_damage)) 
                    theta = 2*pi/self.side_num
                    theta = (self.theta + theta)%(2*pi)
                    p0 = (self.cen_pos[0]+sin(theta)*self.lenth,self.cen_pos[1]+cos(theta)*self.lenth)
                    for i in range(num):
                        b_list.append(Bullet(v = (self.bullet_v*sin(self.theta)+self.v[0],self.bullet_v*cos(self.theta)+self.v[1]),theta=self.theta,color = self.color,pos=(p0[0]*(num-i)/num+p1[0]*i/num,p0[1]*(num-i)/num+p1[1]*i/num),damage=self.bullet_damage)) 
        #反冲力 
        delta_v = 0.5
        self.v=(self.v[0]-sin(self.theta)*delta_v,self.v[1]-cos(self.theta)*delta_v)
        return b_list

    def attacked(self, hiter):
        self.behit += 1
        self.health -= hiter.damage
        # 子弹撞击后产生的速度改变量
        delta_v = (hiter.v[0]-self.v[0],hiter.v[1]-self.v[1])
        self.v=(self.v[0]+hiter.delta_vk*delta_v[0],self.v[1]+hiter.delta_vk*delta_v[1])

        # pygame.mixer.music.stop()#播放mp3文件
        filepath=r".\music\player_hit.wav"#打开mp3文件
        # pygame.mixer.music.pygame.mixer.Channel(0).load(filepath)#加载MP3文件
        # pygame.mixer.music.play(loops=0,start=0,fade_ms=0)#播放mp3文件

        pygame.mixer.Channel(1).play(pygame.mixer.Sound(filepath))

    def death(self):
        if self.health > 0:
            return False
        return True#死亡发生事情
    def shield(self):
        pass

class Player(Boat):
    def __init__(self, lenth=100.0, cen_pos=(0, 0), shape=[0, 1, 2], theta=0, color=(249, 241, 165), v=(0, 0), bullet_v=10, a=0.1, cooldown=5, health=100,bullet_number = 1,bullet_scatter = pi/3,bullet_type=0):
        super().__init__(lenth, cen_pos, shape, theta, color, v, bullet_v, a, cooldown, health,bullet_number,bullet_scatter,bullet_type)
        self.level = 1
    
    def level_up(self,sett,index):
        self.level += 1
        #以下部分需要在python3.10以上使用
        match index:
            case 0:
                #子弹伤害增加
                self.bullet_damage *= 2
            case 1:
                #发射速度加快
                #在cooldown值小于1的情况下，这样的升级将不再有效
                self.cooldown /=2
            case 2:
                #子弹发射数量上升，散射
                self.bullet_number *= 2
                #进一步提升数量
                sett.choice_list.append(4)
                #减小子弹散射
                sett.choice_list.append(5)
            case 3:
                #子弹可以弹射
                #这需要给子弹赋予属性
                return
            case 4:
                #子弹发射数量进一步上升
                self.bullet_number *= 2
            case 5:
                #减小子弹散射
                self.bullet_scatter /=2
                sett.choice_list.append(6)
            case 6:
                #取消子弹散射
                self.bullet_type = 1
