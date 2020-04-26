import pygame
import sys, os
from random import randint

pygame.init()
screen = pygame.display.set_mode((800, 600))

class Player():
    def __init__(self, _x, _y, _dir, path, hpath, bpath):
        self.shot = pygame.mixer.Sound("music/shoot.wav")
        self.riding = pygame.mixer.Sound("music/riding.wav")
        self.img = pygame.image.load(path)
        self.heart = pygame.image.load(hpath)
        self.bullet_path = bpath
        self.x = _x
        self.y = _y
        self.ind = 0
        self.direction = _dir # 0 = down, 1 = right&down, 2 = right, 3 = right&up, 4 = up, 5 = left&up, 6 = left, 7 = left&down
        if _dir == 2:
            self.rot = 1
        else:
            self.rot = 0
            self.ind = 1
            self.img = pygame.transform.flip(self.img, 1, 0)
        self.speed = 1
        self.lives = 3
        self.sdc = 0 #sound of driving counter
        self.sdcd = 20 #sound of driving cooldown
        self.counter = 40
        self.cooldown = 40
        
    def update(self, dx, dy, p): # dx: -1 = left, 0 = none, 1 = right; dy: -1 = down, 0 = none, 1 = up
        if self.counter < self.cooldown:
            self.counter += 1
        if self.sdc < self.sdcd:
            self.sdc += 1
        if dy == 1 and dx == 0:
            self.direction = 0
        elif dy == 1 and dx == 1:
            self.direction = 1
        elif dy == 0 and dx == 1:
            self.direction = 2
        elif dy == -1 and dx == 1:
            self.direction = 3
        elif dy == -1 and dx == 0:
            self.direction = 4
        elif dy == -1 and dx == -1:
            self.direction = 5
        elif dy == 0 and dx == -1:
            self.direction = 6
        elif dy == 1 and dx == -1:
            self.direction = 7
        temp_speed = self.speed
        if dx != 0 and dy != 0:
            temp_speed /= 1.4142
        play = False
        if dx == 1:
            if abs(self.y - p.y) >= 64 or self.x > p.x or (self.x < p.x and p.x - self.x >= 64 + temp_speed):
                self.x += temp_speed
                if self.sdc == self.sdcd:
                    play = True
                    self.sdc = 0
            elif self.x > 800 or self.x < -64:
                self.y -= randint(64, 200)
        elif dx == -1:
            if abs(self.y - p.y) >= 64 or self.x < p.x or (self.x > p.x and self.x - p.x >= 64 + temp_speed):
                self.x -= temp_speed
                if self.sdc == self.sdcd:
                    play = True
                    self.sdc = 0
            elif self.x > 800 or self.x < -64:
                self.y += randint(64, 200)            
        if dy == 1:
            if abs(self.x - p.x) >= 64 or self.y > p.y or (self.y < p.y and p.y - self.y >= 64 + temp_speed):
                self.y += temp_speed
                if self.sdc == self.sdcd:
                    play = True
                    self.sdc = 0
            elif self.y > 600 or self.y < -64:
                self.x -= randint(64, 400)
        elif dy == -1:
            if abs(self.x - p.x) >= 64 or self.y < p.y or (self.y > p.y and self.y - p.y >= 64 + temp_speed):
                self.y -= temp_speed
                if self.sdc == self.sdcd:
                    play = True
                    self.sdc = 0
            elif self.y > 600 or self.y < -64:
                self.x += randint(64, 400) 
        if play:
            self.riding.play()
        elif self.sdc == self.sdcd:
            self.riding.stop()
        if self.x < -70:
            self.x += 900
        elif self.x > 840:
            self.x -= 900
        if self.y < -70:
            self.y += 700
        elif self.y > 640:
            self.y -= 700
    
    def shooting(self):
        global bullets
        if self.counter >= self.cooldown:
            self.counter = 0
            if not self.direction:
                bullets += [Bullet(self.x + (64 - 8) / 2, self.y + 62, 0, self.bullet_path, self.ind)]
                self.shot.play()
            elif self.direction == 1:
                bullets += [Bullet(self.x + 62, self.y + 62, 1, self.bullet_path, self.ind)]
                self.shot.play()
            elif self.direction == 2:
                bullets += [Bullet(self.x + 62, self.y + (64 - 8) / 2, 2, self.bullet_path, self.ind)]
                self.shot.play()
            elif self.direction == 3:
                bullets += [Bullet(self.x + 62, self.y - 24 / 1.4142 + 2, 3, self.bullet_path, self.ind)]
                self.shot.play()
            elif self.direction == 4:
                bullets += [Bullet(self.x + (64 - 8) / 2, self.y - 22, 4, self.bullet_path, self.ind)]
                self.shot.play()
            elif self.direction == 5:
                bullets += [Bullet(self.x - 24 / 1.4142 + 2, self.y - 24 / 1.4142 + 2, 5, self.bullet_path, self.ind)]
                self.shot.play()
            elif self.direction == 6:
                bullets += [Bullet(self.x - 22, self.y + (64 - 8) / 2, 6, self.bullet_path, self.ind)]
                self.shot.play()
            elif self.direction == 7:
                bullets += [Bullet(self.x - 24 / 1.4142 + 2, self.y + 62, 7, self.bullet_path, self.ind)]
                self.shot.play()
        
        
    def draw(self):
        global screen
        if self.rot == 0 and 1 <= self.direction <= 3 or self.rot == 1 and 5 <= self.direction <= 7:
            self.img = pygame.transform.flip(self.img, 1, 0)
            self.rot = 1 - self.rot
        screen.blit(self.img, (int(self.x), int(self.y)))
    
    def draw_lives(self):
        global screen
        if self.ind == 0:
            for i in range(self.lives):
                screen.blit(self.heart, (i * 16, 0))
        else:
            for i in range(self.lives):
                screen.blit(self.heart, (768 - i * 16, 0))            

class Bullet():
    def __init__(self, _x, _y, _dir, path, host): # 0 = down, 1 = right&down, 2 = right, 3 = right&up, 4 = up, 5 = left&up, 6 = left, 7 = left&down
        self.x = _x
        self.y = _y
        print(os.getcwd())
        self.hit = pygame.mixer.Sound("music/hit.wav")
        self.speed = 2
        self.host = host
        self.direction = _dir
        self.active = True
        self.img = pygame.image.load(path)  
        if self.direction == 0:
            self.img = pygame.transform.rotate(self.img, 180)        
        elif self.direction == 1:
            self.img = pygame.transform.rotate(self.img, 225)
        elif self.direction == 2:
            self.img = pygame.transform.rotate(self.img, 270)
        elif self.direction == 3:
            self.img = pygame.transform.rotate(self.img, 315)  
        elif self.direction == 4:
            self.img = pygame.transform.rotate(self.img, 0)
        elif self.direction == 5:
            self.img = pygame.transform.rotate(self.img, 45)
        elif self.direction == 6:
            self.img = pygame.transform.rotate(self.img, 90)
        elif self.direction == 7:
            self.img = pygame.transform.rotate(self.img, 135)
        
    def update(self):
        if self.active:
            temp_speed = self.speed
            if self.direction % 2:
                temp_speed /= 1.4142
            if not self.direction:
                self.y += temp_speed
            elif self.direction == 1:
                self.y += temp_speed
                self.x += temp_speed
            elif self.direction == 2:
                self.x += temp_speed
            elif self.direction == 3:
                self.x += temp_speed
                self.y -= temp_speed
            elif self.direction == 4:
                self.y -= temp_speed
            elif self.direction == 5:
                self.x -= temp_speed
                self.y -= temp_speed
            elif self.direction == 6:
                self.x -= temp_speed
            else:
                self.x -= temp_speed
                self.y += temp_speed
            if self.x < -50 or self.x > 850 or self.y < -50 or self.y > 650:
                self.active = False
    
    def collision_check(self):
        global p
        if self.active:
            if p[1 - self.host].x - self.x < 8 and p[1 - self.host].x - self.x > -64 and p[1 - self.host].y - self.y < 24 and p[1 - self.host].y - self.y > -64:
                self.active = False
                p[1 - self.host].lives -= 1
                self.hit.play()
            
    def draw(self):
        if self.active:
            screen.blit(self.img, (int(self.x), int(self.y)))        

pygame.font.init()
font = pygame.font.Font("pictures/minecraft.ttf", 40)

def cleaner():
    global bullets
    sz = len(bullets)
    i = 0
    while (i < sz):
        if not bullets[i].active:
            bullets.pop(i)
            sz -= 1
            i -= 1
        i += 1
        
def initialisation():
    global p, bullets, gom
    gom = pygame.mixer.Sound("music/gameover.wav")
    p = [Player(100, 300, 2, "pictures/tank1.png", "pictures/like1.png", "pictures/bullet1.png"), Player(650, 300, 6, "pictures/tank2.png", "pictures/like2.png", "pictures/bullet2.png")]
    bullets = []    
    
clock = pygame.time.Clock()        
def main():
    global p, bullets, screen, font    
    background = pygame.image.load("pictures/background.png")  
    gameover = pygame.image.load("pictures/gameover.png")
    conditions1 = [0, 0, 0, 0] #down, up, left, right
    conditions2 = [0, 0, 0, 0]    
    exit = 0 # 1 - player2 destroyed, 2 - player1 destroyed
    while exit == 0:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_w:
                    conditions1[0] = 1 - conditions1[0]
                    conditions1[1] = 0
                elif e.key == pygame.K_s:
                    conditions1[0] = 0
                    conditions1[1] = 1 - conditions1[1]
                elif e.key == pygame.K_a:
                    conditions1[3] = 0
                    conditions1[2] = 1 - conditions1[2]
                elif e.key == pygame.K_d:
                    conditions1[2] = 0
                    conditions1[3] = 1 - conditions1[3]
                elif e.key == pygame.K_UP:
                    conditions2[0] = 1 - conditions2[0]
                    conditions2[1] = 0
                elif e.key == pygame.K_DOWN:
                    conditions2[0] = 0
                    conditions2[1] = 1 - conditions2[1]
                elif e.key == pygame.K_LEFT:
                    conditions2[3] = 0
                    conditions2[2] = 1 - conditions2[2]
                elif e.key == pygame.K_RIGHT:
                    conditions2[2] = 0
                    conditions2[3] = 1 - conditions2[3]
                elif e.key == pygame.K_RETURN:
                    p[0].shooting()
                elif e.key == pygame.K_SPACE:
                    p[1].shooting()
            
        x1 = conditions1[3] - conditions1[2]
        y1 = conditions1[1] - conditions1[0]
        x2 = conditions2[3] - conditions2[2]
        y2 = conditions2[1] - conditions2[0]
        
        p[0].update(x1, y1, p[1])
        p[1].update(x2, y2, p[0])
        cleaner()
        
        for i in range(len(bullets)):
            bullets[i].update()
            bullets[i].collision_check()
        
        screen.blit(background, (0, 0))
        
        p[0].draw()
        p[1].draw()
        
        p[0].draw_lives()
        p[1].draw_lives()
        
        if p[1].lives == 0:
            exit = 1
        elif p[0].lives == 0:
            exit = 2
        
        for i in range(len(bullets)):
            bullets[i].draw()   
                
        pygame.display.flip()   
    
    gom.play()
    
    while exit != 0:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                exit = 0
                
        if exit != 0:
            screen.fill((255, 255, 255))
            screen.blit(gameover, (270, 50))
            if exit == 1:
                screen.blit(font.render("Player 1 won!", -1, (255, 100, 100)), (270, 300))
            elif exit == 2:
                screen.blit(font.render("Player 2 won!", -1, (100, 255, 100)), (270, 300))
            screen.blit(font.render("Press any key to continue...", -1, (100, 100, 100)), (150, 350))
            
            pygame.display.flip()
    
class Menu():
    def __init__(self):
        self.punkts = [("Play", 280, 300, (0, 0, 0), (200, 0, 200)),
                       ("Quit", 370, 400, (0, 0, 0), (200, 200, 0))]
        self.font = pygame.font.Font("pictures/minecraft.ttf", 50)
        self.bigfont = pygame.font.Font("pictures/minecraft.ttf", 120)
        self.active = 0
    
    def update(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    self.active = (len(self.punkts) + self.active - 1) % len(self.punkts)
                elif e.key == pygame.K_DOWN:
                    self.active = (self.active + 1) % len(self.punkts)
                elif e.key == pygame.K_RETURN:
                    if self.active == 0:
                        initialisation()
                        main()
                    elif self.active == 1:
                        pygame.quit()
                        sys.exit()                        
    
    def draw(self):
        global screen
        screen.fill((255, 255, 255))
        screen.blit(self.bigfont.render("TANKS", 1, (0, 200, 200)), (180, 50))
        for i in range(len(self.punkts)):
            if i == self.active:
                screen.blit(self.font.render(self.punkts[i][0], 1, self.punkts[i][4]), (self.punkts[i][1], self.punkts[i][2]))
            else:
                screen.blit(self.font.render(self.punkts[i][0], 1, self.punkts[i][3]), (self.punkts[i][1], self.punkts[i][2]))
        pygame.display.flip()
                
menu = Menu()
while True:
    menu.update()
    menu.draw()
