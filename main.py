from pygame import *
import random

init()

size = (500, 700)
window = display.set_mode(size)
display.set_caption('Falling candy')
clock = time.Clock()

font_text = font.Font('04B_30__.TTF', 23)

# клас всіх спрайтів
class GameSprite:
    def __init__(self, img, x, y, width, height, speed=5):
        self.img = transform.scale(image.load(img), (width, height))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    # метод який відображає обʼєкти класа на іровому екрані
    def reset(self):
        window.blit(self.img, (self.rect.x, self.rect.y))
    # метод для перевірки колізій малює навколо зображення червоний прямокутник
    def draw_rect(self):
        draw.rect(window, (255, 0, 0), self.rect, 5)

    def fall(self):
        self.rect.y += self.speed
        if self.rect.y >= 700:
            self.rect.y = random.randint(-400, -1)
            self.rect.x = random.randint(0, 450)
            self.speed = random.randint(3, 10)

player = GameSprite('img/basket.png', 200, 600, 100, 100)

# створюємо список мусору
trashs = list()
for i in range(2):
    trash = GameSprite('img/banka.png', random.randint(0, 250), random.randint(-1500, -600), 50, 50, random.randint(5, 10))
    trashs.append(trash)
# cтворюємо список цукерок
candys= list()
img_candy = ['img/super_candy.png', 'img/super_candy2.png','img/super_candy3.png', 'img/super_candy4.png']
for i in range(10):
    candy = GameSprite(random.choice(img_candy), random.randint(0, 250), random.randint(-400, -1), 50, 40, random.randint(3, 6))
    candys.append(candy)
floor = transform.scale(image.load('img/floor.png'), (500, 70))
game = True
score = 0
high_score = 0
heals = 3
finish = False

logo = transform.scale(image.load('img/cat.png'), (80, 80))
# початковий екран
def menu():
    start = True
    while start:
        for e in event.get():
            if e.type == QUIT:
                quit()
            if e.type == MOUSEBUTTONDOWN:
                start = False

        # фон
        window.fill((153, 255, 254))
        window.blit(logo, (20, 200))
        font_star = font.Font('04B_30__.TTF', 30)
        text_start = font_star.render('click to start', True, (225, 178, 25))
        window.blit(text_start, (100, 200))

        display.update()
        clock.tick(60)

menu()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        # ресет гри коли клікаємо по еркану і гра закінчена
        if e.type == MOUSEBUTTONDOWN and finish:
            trashs = list()
            for i in range(2):
                trash = GameSprite('img/banka.png', random.randint(0, 250), random.randint(-1500, -600), 50, 50, random.randint(5, 10))
                trashs.append(trash)
            candys = list()
            for i in range(10):
                candy = GameSprite(random.choice(img_candy), random.randint(0, 250), random.randint(-400, -1), 50, 40, random.randint(3, 6))
                candys.append(candy)
            floor = transform.scale(image.load('img/floor.png'), (500, 70))
            score = 0
            heals = 3
            finish = False
        # пауза
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                menu()

    # фон
    window.fill((153, 255, 254))
    if not finish:
        # пересування
        keys = key.get_pressed()
        if keys[K_a]:
            player.rect.x -= 5
        if keys[K_d]:
            player.rect.x += 5
        # відображення полу
        window.blit(floor,(0,630))

        # відображення гравця
        player.reset()
        # player.draw_rect()

        # відображення сміття
        for trash in trashs:
            trash.fall()
            trash.reset()
            #trash.draw_rect()
            # якщо сміття доторкнулася о гравця віднімаємо його життя та переносимо мусор на інші кординати
            if trash.rect.colliderect(player):
                heals-=1
                trash.rect.y = random.randint(-1000, -300)
                trash.rect.x = random.randint(0, 450)

        # відображення цукерок
        for candy in candys:
            candy.fall()
            candy.reset()
            #candy.draw_rect()
            # перевірка на доторкання цукерки та гравця
            if candy.rect.colliderect(player):
                score += 1
                if score > high_score:
                    high_score = score
                candy.rect.y = random.randint(-500, -10)
                candy.rect.x = random.randint(0, 450)

            # перевірка на програш
            if heals <= 0:
                finish = True

            # відображення тексту
            text_score = font_text.render(f'score: {score}', True, (225, 178, 25))
            window.blit(text_score, (320, 20))

            text_health = font_text.render(f'Health: {heals}', True, (225, 178, 25))
            window.blit(text_health, (10, 20))
   # якщо ми програли відображаєио це:
    if finish:
        font_end = font.Font('04B_30__.TTF', 40)
        text_lose = font_end.render('Game over!', True, (225, 178, 25))
        text_hight_score = font_text.render(f'hight score: {high_score}', True, (225, 178, 25))
        window.blit(text_lose, (90, 200))
        window.blit(text_hight_score, (140, 300))


    display.update()
    clock.tick(60)