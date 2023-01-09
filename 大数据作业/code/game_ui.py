import pygame
class Game_UI():#血条UI
    def __init__(self,setting):
        #血量显示
        self.health_background = (10,10,setting.screen_width/4,40)
        self.background_color = (230,230,230)
    def display(self,screen,player,sett,level_xp=100):
        pygame.draw.rect(screen,self.background_color,self.health_background)
        if player.health > 0:
            health_rect = (10,10,self.health_background[2]*player.health/player.full_health,40)
            pygame.draw.rect(screen,player.color,health_rect)
        lv = pygame.font.SysFont('Comic Sans MS',24).render(f"lv {player.level},{player.xp}/{level_xp}",False,(255,255,255))
        rect = lv.get_rect(center = (sett.screen_width/2,10))
        screen.blit(lv,rect)


