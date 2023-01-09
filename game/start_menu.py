
class Start_menu():
    def __init__(self, width, height, screen,title_font,sub_font):
        self.width = width
        self.height = height
        self.screen = screen
        self.count = 0 #标记选中的序号
        self.num = 2 #选项数量
        self.show = True #标记是否显示
        self.sub_font = sub_font
        color = (255,200,200)
        self.title = title_font.render('Alien Invasion',False,color)
        self.option= []
        self.option.append(sub_font.render('Start',False,color))
        self.option.append(sub_font.render('Exit',False,color))
        chosen_color = (200,200,255)
        self.chosen_option = []
        self.chosen_option.append(sub_font.render('Start',False,chosen_color))
        self.chosen_option.append(sub_font.render('Exit',False,chosen_color))
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

