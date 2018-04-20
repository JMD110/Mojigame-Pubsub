import pygame
from sys import exit
from pygame.locals import *
from random import *

# 设全局变量 代表屏幕的宽高
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 400


# 创建一个子弹的类，继承pygame当中的碰撞精灵
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()  # 拿到图片的坐标
        self.rect.midleft = init_pos  # 初始化子弹的位置，因为要从玩家处发射出来，所以子弹左边起点为玩家的右边起点
        self.speed = 10  # 子弹的速度

    def move(self):
        self.rect.left += self.speed  # 用拿到的子弹图片的横坐标加上速度，移动子弹


# 定义一个玩家的类，同样继承碰撞精灵
class Player(pygame.sprite.Sprite):
    def __init__(self, player_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.img = player_img
        self.rect = self.img.get_rect()
        self.rect.topleft = init_pos
        self.speed = 8
        self.bullets = pygame.sprite.Group()  # 玩家所发射的子弹的精灵团
        self.is_hit = False  # 玩家是否被击中

    # 发射子弹
    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midright)
        self.bullets.add(bullet)

    # 因为玩家可以在四个方向上移动，分别写四个方法避免玩家走出屏幕外然后也更稀疏
    def move_up(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def move_down(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def move_left(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def move_right(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed


# 定义敌人的类 同样继承碰撞精灵
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = randint(4, 6)

    # 敌人只需要一直往左边移动就可以了，如果敌人跑了，或者敌人碰到了玩家，游戏结束
    def move(self):
        self.rect.left -= self.speed


def main():
    pygame.init()
    # 初始化游戏窗口
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # 屏幕标题--游戏名称
    pygame.display.set_caption('滑稽风小游戏')
    # 加载游戏结束的图片
    game_over = pygame.image.load_extended('./gameover.png')
    # 加载玩家的图片
    player_img = pygame.image.load_extended('./player.png')
    # 给玩家初始化一个起点位置
    player_pos = [10, 180]
    player = Player(player_img, player_pos)
    # 加载子弹的图片
    bullet_img = pygame.image.load_extended('./bullet.png')
    # 加载敌人的图片
    enemy1_img = pygame.image.load_extended('./enemy.png')
    enemy2_img = pygame.image.load_extended('./enemy2.png')
    # 定义一个敌人的精灵团体，放在精灵Group里，是因为一个屏幕上可以同时出现多个敌人
    # 都要对其是否碰撞进行判定，类似于放在一个列表中
    enemies1 = pygame.sprite.Group()
    # 定义一个死了的敌人的精灵团体，这样可以每死一个记一次分数
    enemies_down = pygame.sprite.Group()
    # 子弹的刷新频率
    shoot_frequency = 0
    # 敌人的刷新频率
    enemy_frequency = 0

    # 计分
    score = 0

    running = True

    def game_speed(score1):
        # 屏幕刷新频率 随着分数增高加快
        clock = pygame.time.Clock()
        i = 60 + score1//30
        return clock.tick(i)

    while running:
        game_speed(score)

        # 生成子弹，需要控制发射频率
        # 首先判断玩家是否被击中
        if not player.is_hit:
            # 只要玩家活着就会一直射箭 每20帧生成1发子弹 要是把20改大，一个屏幕里子弹就会减少
            if shoot_frequency % 15 == 0:
                player.shoot(bullet_img)
            shoot_frequency += 1
            # 把频率又改成0的原因是，随着频率刷新，这个数会越来越大，要是玩很久，运行效率会越来越低
            if shoot_frequency >= 15:
                shoot_frequency = 0

        # 生成敌人，需要控制生成频率
        # 意思和上面差不多，每50帧生成一个敌人，如果减小这个数，那么就会加大游戏难度
        if enemy_frequency % 50 == 0:
            # 敌人初始化的位置，用到了随机数来使敌人出现的位置随机
            # 700是屏幕的横坐标最大处，64是我自己加载的敌人图片的像素，图片是64*64
            enemy1_pos = [700, randint(0, SCREEN_HEIGHT - 64)]
            enemy1 = Enemy(enemy1_img, enemy1_pos)
            enemies1.add(enemy1)  # enemies1代表精灵团
        enemy_frequency += 1
        if enemy_frequency % 37 == 0:
            enemy2_pos = [700, randint(0, SCREEN_HEIGHT - 64)]
            enemy2 = Enemy(enemy2_img, enemy2_pos)
            enemies1.add(enemy2)
        if enemy_frequency >= 50:
            enemy_frequency = 0

        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.left > 690:  # 子弹到屏幕外就删除该子弹
                player.bullets.remove(bullet)

        for enemy in enemies1:
            enemy.move()
            # 定义玩家和敌人碰撞
            if pygame.sprite.collide_circle(enemy, player):
                enemies1.remove(enemy)
                player.is_hit = True
                break
            # 定义如果敌人跑了
            if enemy.rect.left < 0:
                enemies1.remove(enemy)
                running = False
        # 如果任一子弹与任一敌人发生碰撞则在各自精灵团中消失
        #  1,1 前面的1代表敌人消失1个，后面代表子弹消失1个 groupcllide(groupa,groupb,dokilla,dokillb)
        enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
        # 死亡敌人团中每增加一个则加10分
        for enemy_down in enemies1_down:
            enemies_down.add(enemy_down)
            score += 10
        # 定义屏幕为白底
        screen.fill((255, 255, 255))

        player.bullets.draw(screen)
        enemies1.draw(screen)
        # 计分器展现在屏幕上
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render('score : ' + str(score), True, (0, 0, 255))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]  # 在屏幕（10,10）处展示
        screen.blit(score_text, text_rect)
        if not player.is_hit:
            screen.blit(player.img, player.rect)
        else:
            running = False

        # 定义控制游戏的键位和事件，因为我最后要显示玩家的分数以及gameover的图片
        # 所以我用的sys中的exit，因为quit只能退出窗口并不会结束运行，这样设定running=False后游戏屏幕也不会消失
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            player.move_up()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.move_down()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.move_left()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.move_right()

    font = pygame.font.Font(None, 48)
    text = font.render('Score: ' + str(score), True, (0, 0, 255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    screen.blit(game_over, (0, 0))
    screen.blit(text, text_rect)

    # 设置刷新 退出游戏
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    main()
        pygame.display.update()


if __name__ == '__main__':
    main()
