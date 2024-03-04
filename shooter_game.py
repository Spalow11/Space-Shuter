#Создай собственный Шутер!

import pygame as pg
pg.init()
pg.mixer.init()
pg.font.init()
import random
import time 



class GameSprite(pg.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(player_image), (width,height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a] and self.rect.x > 0: 
            self.rect.x -= self.speed
        if keys[pg.K_d] and self.rect.x < 640:
            self.rect.x += self.speed
        # if keys[pg.K_SPACE]:
        #     self.fire()
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 5,5,10)
        bullets.add(bullet)

    
        
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = random.randint(0,640)
            self.speed = random.randint(1,10)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
    


player = Player('rocket.png', 250, 400, 5,60,70)
enemies = pg.sprite.Group(  )
bullets = pg.sprite.Group()
for i in range(5):
    enemies.add(Enemy('ufo.png', random.randint(40,460), 0, random.randint(1,5),40,20))

asteroids = pg.sprite.Group()
for i in range(3):
    asteroids.add(Enemy('asteroid.png', random.randint(40,460),0, random.randint(1,5),40,20))



lost = 0 
score = 0
num_fire = 0
real_time = False
lifes = 3




window = pg.display.set_mode((700, 500))
pg.display.set_caption('Космический корабль')


font = pg.font.SysFont('Arial', 70)
font2 = pg.font.SysFont('Arial', 30)
win = font.render('YOU WIN!',True, (255,215, 0))
lose = font.render('YOU LOSE!',True, (255,48,48))
text_score = font2.render('Очки: ' +str(score), True,(255,255,255))
text_lifes = font2.render('Жизни: ' +str(lifes), True,(255,255,255))
        

pg.mixer.music.load('tension.ogg')
fire = pg.mixer.Sound('fire.ogg')
pg.mixer.music.play()   

backgrond = pg.transform.scale(pg.image.load('galaxy.jpg'), (700,500))
clock = pg.time.Clock()
FPS = 60
running = True
finish = False
while running:
    window.blit(backgrond,(0,0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if num_fire < 10 and real_time == False:
                num_fire += 1
                player.fire()
                fire.play()
            if num_fire >= 10 and real_time == False:
                real_time = True
                cur_time = time.time()
    if finish != True:
        

        text_lose = font2.render('Пропущено: ' +str(lost), True,(255,255,255))
        window.blit(text_lose, (10,10))
        window.blit(text_score,(10,40))
        window.blit(text_lifes,(540,10))
        bullets.update()
        bullets.draw(window)
        player.update()
        player.reset()
        asteroids.update()
        asteroids.draw(window)

        enemies.draw(window)
        enemies.update()
        if pg.sprite.groupcollide(enemies, bullets, True, True):
            score += 1
            text_score = font2.render('Очки: ' +str(score), True,(255,255,255))
            enemies.add(Enemy('ufo.png', random.randint(40,460),  0, random.randint(1,10),40,20))
        if pg.sprite.spritecollide(player, enemies, True):
            lifes -= 1
            enemies.add(Enemy('ufo.png', random.randint(40,460),  0, random.randint(1,10),40,20))
            # window.blit(lose, (200,200))
            # finish = True
        if score > 10:
            window.blit(win,(200,200))
            finish = True
        if lost > 50:
            window.blit(lose, (200,200))
            finish = True
        pg.sprite.groupcollide(asteroids, bullets, False, True)

        if pg.sprite.spritecollide(player, asteroids , True):
            lifes -= 1
            asteroids.add(Enemy('asteroid.png', random.randint(40,460),0, random.randint(1,5),40,20))
            

        if lifes == 0:
            window.blit(lose, (200,200))
            finish = True  

        text_lifes = font2.render('Жизни: ' +str(lifes), True,(255,255,255))
        

        if real_time == True:
            reload_time = time.time()
            if reload_time - cur_time <= 3:
                reload_text = font2.render('Перезарядка', True,(220,20,60))
                window.blit(reload_text, (250,450))
            else:
                num_fire = 0 
                real_time = False



        pg.display.update()
        clock.tick(FPS)
        
        