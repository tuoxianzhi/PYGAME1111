import pygame
import sys
from math import sqrt
from settings import Settings  # 加载选项
from menu import Start_menu, Choose_menu  # 构造开始菜单
from boat import Boat, Player  # 构建游戏玩家太空船
from alien import Alien, alien_summon,Summoner  # 构造敌人
from game_ui import Game_UI  # 当前血量显示
from setting_menu import Setting_menu  # 设置菜单
from over_menu import Over_menu  # 结束菜单
import background  # 随机算法形成动态星空背景

def level_up(screen, sett, player):  # 升级菜单：升级强化
    menu = Choose_menu(screen, sett)  # 打开菜单
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    menu.left()
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    menu.right()
                if event.key == pygame.K_RETURN:
                    # 调用player实现升级，但是，要是修改的是alien的属性该怎么办？
                    player.level_up(sett, menu.get())
                    sett.choice_list.remove(menu.get())
                    return
        # 进行升级选择
        screen.fill(sett.bg_color)
        menu.display()
        pygame.display.flip()


def overmenu(score, sett, screen):
    ovmu = Over_menu(sett.screen_width, sett.screen_height, screen,
                     pygame.font.SysFont('Comic Sans MS', 50), pygame.font.SysFont('Comic Sans MS', 24), score)
    filepath = r".\music\alien-spaceship_daniel_simion.mp3"  # 打开mp3文件播放结束背景音乐
    pygame.mixer.init()
    pygame.mixer.music.load(filepath)  # 加载MP3文件
    pygame.mixer.music.play(loops=-1)  # 播放mp3文件
    pygame.mixer.music.set_volume(1 if sett.set_music else 0)
    # 因为升级会改变sett之中的一些参量，所以在一局游戏结束之后，需要将其再一次的初始化
    sett.__init__()
    while True:
        pygame.mixer.music.set_volume(1 if sett.set_music else 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    ovmu.up()
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    ovmu.down()
                if event.key == pygame.K_RETURN:
                    if ovmu.count == 0:
                        pygame.mixer.music.stop()
                        run_game(screen, sett)
                    elif ovmu.count == 1:
                        sys.exit()  # 选择重新开始或者退出游戏
        screen.fill(sett.bg_color)
        # screen.blit(text_surface,text_rect)
        ovmu.display()
        pygame.display.flip()

# 游戏菜单
def run_game(screen, sett):
    # 记录游戏分数
    score = 0
    # 生成游戏背景对象
    bkg = background.Background(sett, 50)
    # 加载游戏bgm
    filepath = r".\music\alien-spaceship_daniel_simion.mp3"  # 打开游戏运行音乐
    if sett.set_music:
        pygame.mixer.init()
        pygame.mixer.music.load(filepath)  # 加载MP3文件
        pygame.mixer.music.play(loops=-1)  # 播放mp3文件
        pygame.mixer.music.set_volume(1 if sett.set_music else 0)
    lenth = 50 / sqrt(3)  # 50为三角形边长
    player_color = (249, 241, 165)  # 设置游戏颜色
    alien_color = (249, 165, 241)  # 设置外星人颜色
    # 生成玩家飞船
    player = Player(lenth, (sett.screen_width / 2, sett.screen_height / 2), [0, 1, 2, 3, 4, 0, 2, 4, 1, 3], 0)
    summmor = Summoner(player.cen_pos,10)
    # 记录玩家飞船是否处于设计状态和加速状态
    attack_flag = False
    speedup_flag = False
    # 友方子弹列表
    player_bullet_list = []
    # 敌方子弹列表
    alien_bullet_list = []
    # 敌方飞船列表
    alien_list = [alien_summon(500, player.cen_pos, side_num=i,level=player.level) for i in range(3, 10)]
    summmor_list = []
    # 升级所需要的经验
    level_xp = 100
    # 标记玩家子弹准备时间
    bullet_time = 0
    # 加载游戏ui显示
    ui = Game_UI(sett)
    # 火箭声音
    rocket_sound_path = "./music/Rocket_Sound.mp3"
    rocket_channel = pygame.mixer.Channel(0)
    flag = True
    while True:
        # 判定是否应当播放火箭声音
        if speedup_flag and sett.set_sound:
            # 判定当前是否已经在播放火箭声音
            if not rocket_channel.get_busy():
                rocket_channel.play(pygame.mixer.Sound(rocket_sound_path))
        else:
            rocket_channel.stop()
        # 将背景写入缓冲区，并使背景根据玩家速度来更新星星的位置
        bkg.display(screen, sett, player.v)
        # 通过clock来实现60帧
        pygame.time.Clock().tick(60)
        # 当外星人清空时，添加新的外星人
        if len(alien_list) == 0 and len(summmor_list)==0:
            for i in range(7):
                alien_list.append(alien_summon(500, player.cen_pos, side_num=10,level=player.level))  # 加入外星人
            # 到达固定等级之后开始生成召唤师
            for i in range(player.level-7):
                summmor_list.append(Summoner(player.cen_pos,player.level))
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if event.type==pygame.KEYDOWN:
            #     if event.key==pygame.K_a or event.key==pygame.K_LEFT:
            #         player.v=(-1,0)*player.speed
            #         # player.cen_pos
            #     if event.key==pygame.K_d or event.key==pygame.K_RIGHT:
            #         player.v=(1,0)*player.speed
            #         # pass
            #     if event.key==pygame.K_w or event.key==pygame.K_UP:
            #         player.v=(0,1)*player.speed
            #         # menu.up()
            #     if event.key==pygame.K_s or event.key==pygame.K_DOWN:
            #         player.v=(0,-1)*player.speed
            #         # menu.down()
            # 按下鼠标的情况
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 为了贴近现实逻辑，把飞船设置成头部开炮，尾部引擎控制方向
                if event.button == 1:  # 鼠标左键点击——射击
                    attack_flag = True
                    bullet_time = 0
                if event.button == 3:  # 鼠标右键点击——加速
                    speedup_flag = True
            # 鼠标抬起的情况
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    attack_flag = False
                if event.button == 3:
                    speedup_flag = False
        # 子弹时间充分，进行射击
        if bullet_time >= player.cooldown:
            for b in player.attack():
                player_bullet_list.append(b)
            bullet_time = 0
        # 玩家意欲攻击时，进行攻击准备
        if attack_flag:
            bullet_time += 1
        # 玩家意欲加速时，进行加速
        if speedup_flag:
            player.speedup()
        # 敌方射击
        for alien in alien_list:
            t = alien.attack()
            if t is not None:
                for b in t:
                    alien_bullet_list.append(b)
        for summmor in summmor_list:
            for a in summmor.summon():
                alien_list.append(a)
        # 将玩家飞船写入缓冲区
        player.display(screen, pygame.mouse.get_pos(), player.v)
        # 将外星飞船写入缓冲区
        for alien in alien_list:
            alien.display(screen, player.cen_pos, player.v)
            # 对外星人进行加速
            if alien.need_speedup(player.cen_pos):
                alien.speedup()
            # 判定是否需要移除外星人
            if alien.death():
                score = score + alien.level * 10
                # 击杀外星人之后增加对应的经验
                player.xp += alien.xp
                alien_list.remove(alien)
        for summmor in summmor_list:
            summmor.display(screen, player.cen_pos, player.v)
            if summmor.need_speedup(player.cen_pos):
                summmor.speedup()
            if summmor.death():
                score += summmor.level * 50
                player.xp += summmor.xp
                summmor_list.remove(summmor)
        # 将子弹写入缓冲区
        for b in alien_bullet_list:
            b.display(screen, player.v)
            # 对子弹进行碰撞检测
            if pygame.sprite.collide_circle(player, b):
                b.hit(player)
                player.attacked(hiter=b)
            if b.death():
                alien_bullet_list.remove(b)
        for b in player_bullet_list:
            b.display(screen, player.v)
            for alien in alien_list:
                if pygame.sprite.collide_circle(alien, b):
                    b.hit(alien)
                    alien.attacked(b)
            for summmor in summmor_list:
                if pygame.sprite.collide_circle(summmor, b):
                    b.hit(summmor)
                    summmor.attacked(b)
            # 子弹之间进行碰撞检测
            for b1 in alien_bullet_list:
                if pygame.sprite.collide_circle(b1, b):
                    b1.hit(b)
            if b.death():
                player_bullet_list.remove(b)
        # 对玩家飞船和敌方飞船进行碰撞检测
        for alien in alien_list:
            if pygame.sprite.collide_circle(alien, player):
                player.attacked(alien)
                alien.attacked(player)
        for summmor in summmor_list:
            if pygame.sprite.collide_circle(summmor, player):
                player.attacked(summmor)
                summmor.attacked(player)
        # 需要升级
        if player.xp >= level_xp:
            score = score + 100
            player.xp -= level_xp
            level_xp += 100
            attack_flag = False
            speedup_flag = False
            level_up(screen, sett, player)
        # ui界面输出到缓冲区
        ui.display(screen, player, sett,level_xp)
        pygame.display.flip()
        # 如果玩家死亡，跳转到结束菜单
        if player.death():
            overmenu(score, sett, screen)


def run_setting(screen,sett):  # 设置
    # 生成一个设置菜单类，并确定其中的字体
    menu = Setting_menu(sett.screen_width, sett.screen_height, screen,
                        pygame.font.SysFont('Comic Sans MS', 50), pygame.font.SysFont('Comic Sans MS', 24), sett)
    while True:
        # 处理时间
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # 上下移动选择
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    menu.up()
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    menu.down()
                if event.key == pygame.K_RETURN:
                    # 对对应选项进行更新
                    if menu.count == 0 or menu.count == 1:
                        menu.switch(sett)
                    # 退出
                    else:
                        return
        screen.fill(sett.bg_color)
        menu.display()
        pygame.display.flip()


def show_menu():
    # 初始化pygame
    pygame.init()
    # 加载运行图标
    surface = pygame.image.load("./icon.png")
    pygame.display.set_icon(surface)
    # 设定窗口标题
    pygame.display.set_caption("Alien Invasion")
    # 初始化一个设置类
    sett = Settings()
    # 设置屏幕长和宽
    screen = pygame.display.set_mode((sett.screen_width, sett.screen_height))
    # 加载bgm
    filepath = r".\music\alien-spaceship_daniel_simion.mp3"  # 打开始界面MP3
    pygame.mixer.init()
    pygame.mixer.music.load(filepath)  # 加载MP3文件
    pygame.mixer.music.play(loops=-1)  # 播放mp3文件，并设置其为循环播放
    pygame.mixer.music.set_volume(1 if sett.set_music else 0) # 设置音量
    # 加载开始菜单类，并定义字体
    menu = Start_menu(sett.screen_width, sett.screen_height, screen,
                      pygame.font.SysFont('Comic Sans MS', 50), pygame.font.SysFont('Comic Sans MS', 24))
    while True:
        # pygame.mixer.music.set_volume(1 if sett.set_music else 0)
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # 处理上下选择的情况
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    menu.up()
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    menu.down()
                # 选中的情况
                if event.key == pygame.K_RETURN:
                    # 选中开始游戏
                    if menu.count == 0:
                        print("game start")
                        pygame.mixer.music.stop()
                        run_game(screen, sett)
                    # 选中游戏设置
                    elif menu.count == 1:
                        print("settings")
                        run_setting(screen,sett)
                        if not sett.set_music:
                            pygame.mixer.music.stop()
                        elif not pygame.mixer.music.get_busy():
                            pygame.mixer.music.play(loops=-1)
                    # 选中退出
                    elif menu.count == 2:
                        sys.exit()
        # 填充背景颜色
        screen.fill(sett.bg_color)
        # 将菜单输出到缓冲区之中
        menu.display()
        # 绘制缓冲区
        pygame.display.flip()


if __name__ == "__main__":
    # 开始游戏
    show_menu()
