from pygame import *

win_width = 700
win_height = 500
display.set_caption("Лабиринт")
window = display.set_mode((win_width, win_height))
back = (119, 210, 223)#задаем цвет согласно цветовой схеме RGB



class GameSprite(sprite.Sprite):
   # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
       # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
       # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y)) 

       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
   # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
   #метод, в котором реализовано управление спрайтом по кнопкам стрелочкам клавиатуры
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       # Вызываем конструктор класса (Sprite):
        GameSprite. __init__(self, player_image, player_x, player_y,size_x, size_y)
  
        self.speed = player_speed
        
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed


    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)
            
#класс спрайта-врага   
class Enemy(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
 
  #движение врага
    def update(self):
        if self.rect.x <= 420: #w1.wall_x + w1.wall_width
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

# класс спрайта-пули  
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
 # движение врага
    def update(self):
        self.rect.x += self.speed
        # исчезает, если дойдет до края экрана
        if self.rect.x > win_width+10:
            self.kill()



#packman  = GameSprite("hero.png",100,300,80,80)

packman  = Player("hero.png",100,300,80,80,10)
w1 = GameSprite('platform2.png',100, 250, 300, 50)
w2 = GameSprite('platform2_v.png', 370, 100, 50, 400)



#создаем группу для врагов
monsters = sprite.Group()
#добавляем врагов в группу
monster1 = Enemy('cyborg.png', win_width - 80, 150, 80, 80, 5)
monster2 = Enemy('cyborg.png', win_width - 80, 230, 80, 80, 5)
#добавляем монстра в группу
monsters.add(monster1)
monsters.add(monster2)



final_sprite = GameSprite('pac-1.png', win_width - 85, win_height - 100, 80, 80)

#создаем группу для пуль
bullets = sprite.Group()


run = True
finish=False
while run:
    time.delay(50)
    window.fill(back)#закрашиваем окно цветом
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                packman.fire()
    
    if finish !=True:
        #рисуем объекты
        w1.reset()
        w2.reset()
        packman.reset()
        packman.update()

        #monster.reset()
        #monster.update()
        final_sprite.reset()

        bullets.update()
        bullets.draw(window)

        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)


        #Проверка столкновения героя с врагом и стенами
        if sprite.collide_rect(packman, w1) or sprite.collide_rect(packman, w2):
            finish = True
            #вычисляем отношение
            img = image.load('game-over_1.png')
            #d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            #window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
     
             #Проверка столкновения героя с врагом и стенами
        if sprite.spritecollide(packman, monsters, False):
            finish = True
            #вычисляем отношение
            img = image.load('game-over_1.png')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))

        #Проверка столкновения героя с фин спрайтом
        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('thumb.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0)) 

  
        


        display.update()