from random import choice
from settings import character_list
class Start_menu():
    def __init__(self, width, height, screen,title_font,sub_font):
        self.width = width
        self.height = height
        self.screen = screen
        self.count = 0 #标记选中的序号
        self.num = 3 #选项数量
        self.show = True #标记是否显示
        self.sub_font = sub_font
        color = (255,200,200)
        self.title = title_font.render('Alien Invasion',False,color)
        self.option= []
        self.option.append(sub_font.render('Start',False,color))
        self.option.append(sub_font.render('Setting',False,color))
        self.option.append(sub_font.render('Exit',False,color))
        chosen_color = (200,200,255)
        self.chosen_option = []
        self.chosen_option.append(sub_font.render('Start!',False,chosen_color))
        self.chosen_option.append(sub_font.render('Setting',False,chosen_color))
        self.chosen_option.append(sub_font.render('Exit?',False,chosen_color))
    def up(self):
        self.count = (self.num + self.count - 1) % self.num
    def down(self):
        self.count = (self.count + 1) % self.num
    def display(self):
        if(self.show):
            title_rect = self.title.get_rect(center = (self.width/2,self.height/3))
            self.screen.blit(self.title,title_rect)
            for i in range(self.num):
                if i!=self.count:
                    rect = self.option[i].get_rect(center=(self.width/2,self.height*(3+i)/(3+self.num)))
                    self.screen.blit(self.option[i],rect)
                else:
                    rect = self.chosen_option[i].get_rect(center=(self.width/2,self.height*(3+i)/(3+self.num)))
                    self.screen.blit(self.chosen_option[i],rect)

class Choose_menu():
    def __init__(self,screen,settings):
        #这次选择之中的选项
        self.choice_list = []
        for i in range(settings.choice_count):
            #随机选择可以进入选择之中的元素，可能会出现重复的元素
            self.choice_list.append(choice(settings.choice_list))
        self.choice_text_list = []
        color = (255,200,200)
        chosen_color = (200,200,255)
        for c in self.choice_list:
            self.choice_text_list.append(settings.choice_font.render(character_list[c],False,color))
        self.chosen_text_list = []
        for c in self.choice_list:
            self.chosen_text_list.append(settings.choice_font.render(character_list[c],False,chosen_color))
        self.height = settings.screen_height
        self.width = settings.screen_width
        #标记选中的序号
        self.index = 0
        self.screen = screen

    def right(self):
        self.index += 1
        self.index %= len(self.choice_list)

    def left(self):
        self.index += len(self.choice_list)-1
        self.index %= len(self.choice_list)
        
    def get(self):
        return self.choice_list[self.index]

    def display(self):
        count = len(self.choice_list)
        for i in range(count):
            if i!=self.index:
                rect = self.choice_text_list[i].get_rect(center=(self.width*(2*i+1)/2/count,self.height/2))
                self.screen.blit(self.choice_text_list[i],rect)
            else:
                rect = self.chosen_text_list[i].get_rect(center=(self.width*(2*i+1)/2/count,self.height/2))
                self.screen.blit(self.chosen_text_list[i],rect)


