import pygame
import sys
from math import sqrt
from settings import Settings#设置rougelike选项与强化选项
from menu import Start_menu,Choose_menu#构造开始菜单
from boat import Boat,Player#构建游戏玩家太空船
from alien import Alien,alien_summon#构造敌人
from game_ui import Game_UI#就行血量显示
from setting_menu import Setting_menu#设置菜单
from over_menu import Over_menu#结束菜单
import background#随机算法形成动态星空背景
set_music=True#音乐开关
set_sound=True#音效开关
def level_up(screen,sett,player):#升级菜单：升级强化
    menu = Choose_menu(screen,sett) #打开菜单
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_a or event.key==pygame.K_LEFT:
                    menu.left()
                if event.key==pygame.K_d or event.key==pygame.K_RIGHT:
                    menu.right()
                if event.key==pygame.K_RETURN:
                    #调用player实现升级，但是，要是修改的是alien的属性该怎么办？
                    player.level_up(sett,menu.get())
                    sett.choice_list.remove(menu.get())
                    return
        #进行升级选择
        screen.fill(sett.bg_color)
        menu.display()
        pygame.display.flip()
def overmenu(score,ai_settings,screen):
    ovmu = Over_menu(ai_settings.screen_width,ai_settings.screen_height,screen,pygame.font.SysFont('Comic Sans MS',50),pygame.font.SysFont('Comic Sans MS',24),score)
    global set_music
    global set_sound
    filepath=r".\music\alien-spaceship_daniel_simion.mp3"#打开mp3文件播放结束背景音乐
    pygame.mixer.stop()
    pygame.mixer.init()
    pygame.mixer.music.load(filepath)#加载MP3文件
    pygame.mixer.music.play(loops=-1)#播放mp3文件
    pygame.mixer.music.set_volume(1 if set_music else 0)
    while True:
        pygame.mixer.music.set_volume(1 if set_music else 0)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_w or event.key==pygame.K_UP:
                    ovmu.up()
                if event.key==pygame.K_s or event.key==pygame.K_DOWN:
                    ovmu.down()
                if event.key==pygame.K_RETURN:
                    if ovmu.count == 0:
                        pygame.mixer.music.stop()
                        run_game(screen,ai_settings)
                    elif ovmu.count == 1:
                        sys.exit()#选择重新开始或者退出游戏
        screen.fill(ai_settings.bg_color)
        #screen.blit(text_surface,text_rect)
        ovmu.display()
        pygame.display.flip()

def run_game(screen,sett):
    score=0
    bkg=background.Background(sett,50)
    filepath=r".\music\alien-spaceship_daniel_simion.mp3"#打开游戏运行音乐
    if(set_music):
        pygame.mixer.init()
        pygame.mixer.music.load(filepath)#加载MP3文件
        pygame.mixer.music.play(loops=-1)#播放mp3文件
        pygame.mixer.music.set_volume(1 if set_music else 0)
    # screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    lenth = 50/sqrt(3) # 50为三角形边长
    player_color = (249,241,165)#设置游戏颜色
    alien_color = (249,165,241)#设置外星人颜色
    player = Player(lenth,(sett.screen_width/2,sett.screen_height/2),[0,1,2,3,4,0,2,4,1,3],0)
    attack_flag = False#是否射击
    speedup_flag = False#是否加速
    player_bullet_list = []#友军子弹
    alien_bullet_list = []#敌军子弹
    alien_list = []#敌军
    #玩家当前经验
    xp = 0
    #升级所需要的经验
    level_xp = 100
    for i in range(3,10):
        alien_list.append(alien_summon(500,player.cen_pos,side_num=i))
    bullet_time = 0 #标记玩家子弹准备时间
    ui = Game_UI(sett)
    while True:
        print(set_sound)
        if(speedup_flag and set_sound):
            file_path="./music/alien-spaceship_daniel_simion.mp3"
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(filepath))
        else:
            pygame.mixer.Channel(0).stop()
        if(not set_sound):
            pygame.mixer.Channel(1).stop()#设置是否关闭音效
        bkg.display(screen,sett,player.v)
        # screen.fill()
        clock = pygame.time.Clock()#定时触发
        clock.tick(60)#六十帧
        if len(alien_list)==0:
            for i in range(3,10):
                alien_list.append(alien_summon(500,player.cen_pos,side_num=i))#加入外星人
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                #为了贴近现实逻辑，把飞船设置成头部开炮，尾部引擎控制方向
                if event.button == 1:#鼠标左键点击——射击
                    attack_flag = True
                    speedup_flag = True
                    bullet_time = 0
                if event.button == 3:#鼠标右键点击——加速
                    speedup_flag = True
            if event.type ==pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    attack_flag = False
                if event.button == 3:
                    speedup_flag = False
        # screen.fill((23,23,23))
        if attack_flag and bullet_time%player.cooldown == 0:
            for b in player.attack():
                player_bullet_list.append(b)
            bullet_time = 0
        bullet_time += 1
        #射击
        for alien in alien_list:
            t = alien.attack()
            if t!=None:
                alien_bullet_list.append(t)
        if speedup_flag:
            player.speedup()#加速
        player.display(screen,pygame.mouse.get_pos(),player.v)
        for alien in alien_list:
            alien.display(screen,player.cen_pos,player.v)
            if alien.need_speedup(player.cen_pos):
                alien.speedup()
                #外星人升级
            if alien.death():
                score=score+player.level*10
                alien_list.remove(alien)
                #击杀外星人之后增加对应的经验
                alien_xp = 10
                xp+=alien_xp
        for b in alien_bullet_list:
            b.display(screen,player.v)
            if pygame.sprite.collide_circle(player, b):
                b.hit(player)
                player.attacked(hiter=b)
            if b.death():
                alien_bullet_list.remove(b)
        for b in player_bullet_list:
            b.display(screen,player.v)
            for alien in alien_list:
                if pygame.sprite.collide_circle(alien,b):
                    b.hit(alien)
                    alien.attacked(b)
            if b.death():
                player_bullet_list.remove(b)
        for alien in alien_list:
            if pygame.sprite.collide_circle(alien,player):
                player.attacked(alien)
                alien.attacked(player)
        # if b.death():
        #     player_bullet_list.remove(b)
        #需要升级
        if(xp>level_xp):
            score=score+100
            xp -= level_xp
            level_xp +=100
            attack_flag = False
            speedup_flag = False
            level_up(screen,sett,player)
        ui.display(screen,player,sett)
        pygame.display.flip()
        if player.death():
            overmenu(score,sett,screen)
def run_setting(ai_settings,semu):#设置界面开启音乐与音效
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    menu = semu
    flag=0
    pygame.display.set_caption("Alien Invasion")
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_w or event.key==pygame.K_UP:
                    menu.up()
                if event.key==pygame.K_s or event.key==pygame.K_DOWN:
                    menu.down()
                if event.key==pygame.K_RETURN:
                    if menu.count == 0:
                        menu.switch()
                    elif menu.count == 1:
                        # print("changege")
                        menu.switch()
                    elif menu.count == 2:
                        return#上下移动选择
        screen.fill(ai_settings.bg_color)
        #screen.blit(text_surface,text_rect)
        menu.display()
        pygame.display.flip()
def show_menu():
    surface=pygame.image.load("./icon.png")
    pygame.display.set_icon(surface)
    pygame.init()
    ai_settings = Settings()
    # set_music=True
    # set_sound=True
    global set_music
    global set_sound
    filepath=r".\music\alien-spaceship_daniel_simion.mp3"#打开始界面MP3
    pygame.mixer.init()
    pygame.mixer.music.load(filepath)#加载MP3文件
    pygame.mixer.music.play(loops=-1)#播放mp3文件
    pygame.mixer.music.set_volume(1 if set_music else 0)

    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    menu = Start_menu(ai_settings.screen_width,ai_settings.screen_height,screen,pygame.font.SysFont('Comic Sans MS',50),pygame.font.SysFont('Comic Sans MS',24))
    semu = Setting_menu(ai_settings.screen_width,ai_settings.screen_height,screen,pygame.font.SysFont('Comic Sans MS',50),pygame.font.SysFont('Comic Sans MS',24))
    pygame.display.set_caption("Alien Invasion")


    while True:
        pygame.mixer.music.set_volume(1 if set_music else 0)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_w or event.key==pygame.K_UP:
                    menu.up()
                if event.key==pygame.K_s or event.key==pygame.K_DOWN:
                    menu.down()
                if event.key==pygame.K_RETURN:
                    if menu.count == 0:
                        print("game start")
                        pygame.mixer.music.stop()
                        run_game(screen,ai_settings)
                    elif menu.count == 1:
                        print("settings")
                        run_setting(ai_settings,semu)
                        set_music=not semu.flag_list[0]
                        set_sound=not semu.flag_list[1]
                    elif menu.count == 2:
                        sys.exit()#上下移动选择
        screen.fill(ai_settings.bg_color)
        #screen.blit(text_surface,text_rect)
        menu.display()
        pygame.display.flip()
show_menu()
