from pygame import *
from random import randint

window = display.set_mode((800,600))
display.set_caption('Шутер')
background = transform.scale(image.load("galaxy.jpg"),(800,600))
global miss
miss=0
global hits
hits=0
global mat
mat =0
font.init()
font1=font.SysFont('Arial',36)
font2=font.SysFont('Arial',36)
font3=font.SysFont('Arial',36)
font4=font.SysFont('Arial',36)
class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y, player_speed,width,height):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(width,height))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Enemy(GameSprite):
    def update(self):
        global miss
        self.rect.y+=self.speed
class Meteorit(GameSprite):
    def update(self):
        self.rect.y+=self.speed
class Bullet(GameSprite):
    def fire(self):
        self.rect.y-=self.speed
clock = time.Clock()
FPS=60
player=GameSprite('rocket.png',350,500,10,100,100)
ufo_enemy=Enemy('ufo.png',randint(0,700),randint(0,5),randint(1,9),128,64)
bullet=Bullet('bullet.png',player.rect.x,player.rect.y,20,10,10)
meteo = Meteorit('1233.png',randint(0,700),randint(0,5),5,128,64)

bullet.rect.x=-10
mixer.init()
mixer.music.load('123.mp3')
mixer.music.play()
monsters=sprite.Group()
monsters.add(ufo_enemy)
bullets=sprite.Group()
bullets.add(bullet)
meteorits=sprite.Group()
meteorits.add(meteo)
def new_enemy():
    ufo_enemy=Enemy('ufo.png',randint(0,700),randint(0,5),5,128,64)
    monsters.add(ufo_enemy)
def new_meteo():
    meteo=Meteorit('1233.png',randint(0,700),randint(0,5),5,128,64)
    meteorits.add(meteo)
game=True
while game:
    window.blit(background,(0,0))
    text_lose=font1.render("Пропущенно:"+ str(miss), 1,(255,255,255))
    text_hits=font2.render("Счёт:"+ str(hits),1 ,(255,255,255))
    window.blit(text_hits,(1,25))
    window.blit(text_lose,(1,1))
    bullets.update()
    monsters.update()
    meteorits.update()
    bullets.draw(window)
    monsters.draw(window)
    meteorits.draw(window)
    keys_pressed = key.get_pressed()
    clock.tick(FPS)
    player.reset()
    ufo_enemy.reset()
    bullet.reset()
    meteo.reset()
    bullet.fire()
    for e in event.get():
        if e.type == QUIT:
            game = False
    for ufo_enemy in monsters:
        if sprite.collide_rect(bullet,ufo_enemy):
            bullet.remove(bullets)
            ufo_enemy.remove(monsters)
            if len(monsters) <= 2:
                new_enemy()
            hits+=1     
    for meteo in meteorits:
        if sprite.collide_rect(player,meteo): 
            meteo.remove(meteorits)
            sleep(10000000)  
            text_vse = font4.render('А фсё, бабах, взрыв...',1,(255,0,255))
    for meteo in meteorits:
        if sprite.collide_rect(meteo,player):
            meteo.remove(meteorits)            
            mat+=1     
    for ufo_enemy in monsters:
        if ufo_enemy.rect.y>500:
            ufo_enemy.rect.x=randint(0,700)
            ufo_enemy.rect.y=0
            miss+=1
            if len(monsters) <= 2:
                new_enemy()
    for meteo in meteorits:
        if meteo.rect.y>500:
            meteo.rect.x=randint(0,700)
            meteo.rect.y=0
            if len(meteorits) <= 2:
                new_meteo()
    if player.rect.x>=700:
        player.rect.x-=10
    if player.rect.x<=0:
        player.rect.x+=10
    if keys_pressed[K_a]:
        player.rect.x-=10
    if keys_pressed[K_d]:
        player.rect.x+=10
    if keys_pressed[K_SPACE]:
        bullet.fire()
        bullet=Bullet('bullet.png',player.rect.x,player.rect.y,20,10,10)
        bullet.rect.x=player.rect.x+45
    display.update()