class Setting_menu():
    def __init__(self, width, height, screen, title_font, sub_font, sett):
        self.width = width
        self.height = height
        self.screen = screen
        self.count = 0  # 标记选中的序号
        self.num = 3  # 选项数量
        self.show = True  # 标记是否显示
        self.sub_font = sub_font
        self.flag_list = [1, 1, 0]
        if sett.set_music:
            self.flag_list[0] = 0
        if sett.set_sound:
            self.flag_list[1] = 0
        color = (255, 200, 200)
        self.title = title_font.render('Setting Menu', False, color)
        self.option = []
        self.option.append(sub_font.render('Music on', False, color))
        self.option.append(sub_font.render('Sound on', False, color))
        self.option.append(sub_font.render('Exit', False, color))
        chosen_color = (200, 200, 255)
        self.chosen_option = []
        self.chosen_option.append(sub_font.render('Music on?', False, chosen_color))
        self.chosen_option.append(sub_font.render('Sound on?', False, chosen_color))
        self.chosen_option.append(sub_font.render('Exit?', False, chosen_color))
        self.sw_option = []
        self.sw_option.append(sub_font.render('Music off', False, color))
        self.sw_option.append(sub_font.render('Sound off', False, color))
        self.chsw_option = []
        self.chsw_option.append(sub_font.render('Music off?', False, chosen_color))
        self.chsw_option.append(sub_font.render('Sound off?', False, chosen_color))
        print("1")

    def up(self):
        self.count = (self.num + self.count - 1) % self.num

    def down(self):
        self.count = (self.count + 1) % self.num

    def display(self):
        if self.show:
            title_rect = self.title.get_rect(center=(self.width / 2, self.height / 3))
            self.screen.blit(self.title, title_rect)
            for i in range(self.num):
                if i != self.count:
                    if self.flag_list[i] == 0:
                        rect = self.option[i].get_rect(center=(self.width / 2, self.height * (3 + i) / (3 + self.num)))
                        self.screen.blit(self.option[i], rect)
                    elif self.flag_list[i] == 1:
                        rect = self.sw_option[i].get_rect(
                            center=(self.width / 2, self.height * (3 + i) / (3 + self.num)))
                        self.screen.blit(self.sw_option[i], rect)
                else:
                    if self.flag_list[i] == 0:
                        rect = self.chosen_option[i].get_rect(
                            center=(self.width / 2, self.height * (3 + i) / (3 + self.num)))
                        self.screen.blit(self.chosen_option[i], rect)
                    elif self.flag_list[i] == 1:
                        rect = self.chsw_option[i].get_rect(
                            center=(self.width / 2, self.height * (3 + i) / (3 + self.num)))
                        self.screen.blit(self.chsw_option[i], rect)

    def switch(self,sett):
        cc = self.count
        self.flag_list[cc] = 1 - self.flag_list[cc]
        if cc == 0:
            sett.set_music = not sett.set_music
        elif cc == 1:
            sett.set_sound = not sett.set_sound
