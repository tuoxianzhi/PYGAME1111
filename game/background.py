from random import uniform
import pygame

class Star():
    def __init__(self, r, width, hight,opt):
        self.r = r
        self.v = 4/r
        self.x = uniform(0,width)
        self.y = uniform(0,hight)

    def display(self,screen,sett,playerv):
        self.x = self.x - self.v * playerv[0]
        self.y = self.y - self.v * playerv[1]
        if(self.x< -self.r):
            self.x+=sett.screen_width
        elif(self.x>sett.screen_width+self.r):
            self.x-=sett.screen_width
        if(self.y< -self.r):
            self.y+=sett.screen_height
        elif(self.y>sett.screen_height+self.r):
            self.y-=sett.screen_height
        pygame.draw.circle(screen,(255,255,255),(self.x,self.y),self.r)        

class Background():
    def __init__(self,sett,count):
        self.star_list = []
        for i in range(count): # count 对应为星星的数量
            self.star_list.append(Star(uniform(1,4),sett.screen_width,sett.screen_height))

    def display(self,screen,sett,playerv):
        screen.fill((23,23,23))
        for star in self.star_list:
            star.display(screen,sett,playerv)


