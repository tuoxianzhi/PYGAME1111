import pygame


class Settings():
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (23, 23, 23)
        # 升级时的选择数量
        self.choice_count = 3
        # 升级时可以选择的列表，可以考虑在升级时进行更新。
        # 有一个问题，不同级别的选项出现概率是不同的
        # 所以之后还需要设计多个列表？
        self.choice_list = [0, 1, 2, 7, 9, 12, 13]
        # 用于记录一些特性，可以转递给子弹以使其实现。
        self.chosen_list = []
        self.choice_font = pygame.font.SysFont("华文楷体", 24)
        self.set_music = True  # 音乐开关
        self.set_sound = True  # 音效开关
        self.vampire=0.1

character_list = []
character_list.append("子弹伤害上升")  # 0
character_list.append("子弹射击速度提升")  # 1
character_list.append("一次发射的子弹数量上升")  # 2
character_list.append("子弹可以弹射")  # 3,未实现
character_list.append("一次发射的子弹数量上升+")  # 4
character_list.append("减小子弹散射")  # 5
character_list.append("取消子弹散射，改为平射")  # 6
character_list.append("增加选择数量")  # 7
character_list.append("增加选择数量+") # 8
character_list.append("吸血") # 9
character_list.append("子弹伤害上升") # 10
character_list.append("吸血+") # 11
character_list.append("转向速度上升") # 12
character_list.append("推进速度上升") # 13
