from pygame import *
from random import *

win_width = 750
win_height = 600
display.set_caption = ('Шутер')
window = display.set_mode((win_width, win_height))
img_back = 'space.jpg'

background = transform.scale(image.load(img_back), (win_width, win_height))

run = True
finish = False
scored = 0
health = 3

class GameSprite(sprite.Sprite):
    def __init__(self, play_image, x, y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(play_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def paint(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, play_image, x, y, size_x, size_y, speed):
        GameSprite. __init__(self, play_image, x, y, size_x, size_y)
        self.speed = speed
    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('rock.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

class Bullet(GameSprite):
    def __init__(self, play_image, x, y, size_x, size_y, speed):
        GameSprite.__init__(self, play_image, x, y, size_x, size_y)
        self.speed = speed
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()
monsters = sprite.Group()

for i in range(1, 5):
    monster = Enemy('asteroid.jpg', randint(30, win_width ), -30, 25, 30, randint(1, 2))
    monsters.add(monster)

ship = Player('1.png', 400, 480, 75, 100, 5)
while run:
    time.delay(10)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                    ship.fire()

    if finish !=True:
        window.blit(background,(0,0))
        ship.paint()      
        ship.move()
        ship.update()
        bullets.update()
        bullets.draw(window)
        monsters.draw(window)
        monsters.update()
    
        colission = sprite.groupcollide(monsters, bullets, True, True)
        
        for col in colission:
            monster = Enemy('asteroid.jpg', randint(30, win_width ), -40, 25, 30, randint(10, 11))
            monsters.add(monster)
            scored +=1
            print(scored)
        
        death = sprite.spritecollide(ship, monsters, True)
        for dh in death:
            monster = Enemy('asteroid.jpg', randint(30, win_width ), -40, 25, 30, randint(10, 11))
            monsters.add(monster)
            health -=1
            print(health)
            if health <1:
                finish = True
                over = image.load('over.jpg')
                #ov = over.get_width() // over.get_height()
                window.blit(transform.scale(over, (win_width , win_height)), (0, 0))


        display.update()
