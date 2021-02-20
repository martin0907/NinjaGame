import pygame
import random
import os

pygame.font.init()
width, height = (1200, 500)
pygame.display.set_caption("Ninja Game")
screen = pygame.display.set_mode((width, height))

bg = pygame.transform.scale(pygame.image.load(os.path.join("images","unnamed.png")), (width, height))
bg2 = pygame.transform.scale(pygame.image.load(os.path.join("images","bg2.jpg")), (width, height))
level3_bg = pygame.transform.scale(pygame.image.load(os.path.join("images","level3.png")), (width, height))
level4_bg = pygame.transform.scale(pygame.image.load(os.path.join("images","level4.jpg")), (width, height))

base_img = pygame.transform.scale(pygame.image.load(os.path.join("images","base.png")), (900, 50))
base_b = pygame.transform.scale(pygame.image.load(os.path.join("images","base_b.png")), (900, 50))
base_level3 = pygame.transform.scale(pygame.image.load(os.path.join("images","base_level3.png")), (900, 50))

player_img = pygame.image.load(os.path.join('images','player6.png'))
player_imgl = pygame.image.load(os.path.join('images','player6l.png'))
monster_img = pygame.image.load(os.path.join('images','monster.png'))
monster_img2 = pygame.image.load(os.path.join('images','monster2.png'))
monster_img3 = pygame.image.load(os.path.join('images','monster3.png'))
weapon_img = pygame.image.load(os.path.join('images','gun4.png'))
axe_img = pygame.image.load(os.path.join('images','axe.png'))

obs = pygame.image.load(os.path.join('images','obstacle.png'))
obstacle1 = pygame.image.load(os.path.join('images','obstacle_level2.png'))

mini_base = pygame.image.load(os.path.join('images','base_mini.png'))
mini_base1 = pygame.image.load(os.path.join('images','base_level2_mini.png'))
base_level3_mini = pygame.image.load(os.path.join('images','base_level3_mini.png'))

minor_base = pygame.image.load(os.path.join('images','base_minor.png'))
minor_base1 = pygame.image.load(os.path.join('images','base_level2_minor.png'))
base_level3_minor = pygame.image.load(os.path.join('images','base_level3_minor.png'))

bullet_speed = 6

class Background:
    def __init__(self, y, img):
        self.bg_width = bg.get_width()
        self.img = bg
        self.y = y
        self.x1 = 0
        self.x2 = self.bg_width
        self.bg_speed = 1

    def move(self):
        self.x1 -= self.bg_speed
        self.x2 -= self.bg_speed

        if self.x1 + self.bg_width < 0:
            self.x1 = self.x2 + self.bg_width
        if self.x2 + self.bg_width < 0:
            self.x2 = self.x1 + self.bg_width

        screen.blit(self.img, (self.x1, self.y))
        screen.blit(self.img, (self.x2, self.y))

class Base:
    def __init__(self, x, y, img):
        self.base_width = base_img.get_width()
        self.y = y
        self.x = x
        self.base_speed = 1
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.rect = self.mask.get_rect()

    def move(self):
        self.x -= self.base_speed

        if self.x + self.base_width  < 0:
            self.x = random.randint(200,2000) + self.base_width
        self.show()

    def show(self):
        screen.blit(self.img, (self.x, self.y))

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return (self.img.get_height() - 44)
    
class Obstacle:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.top = self.img.get_height()
        self.mask = pygame.mask.from_surface(self.img)
        self.rect = self.img.get_rect()
        self.speed = 1
    
    def show(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self, obj2, obj3, obj4):
        self.x -= self.speed
        self.y = 420

        if self.x + self.get_width() < 0:
            self.x = random.randint(1500, 2200)
        while self.collide(obj2, obj3, obj4):
            self.y = self.y - (obj2.get_height() - 4)
            self.y = self.y - obj3.get_height()
            self.y = self.y - obj4.get_height()
        self.show()
        
    def collide(self, obj1, obj2, obj3):
        return obs_collide(self, obj1, obj2, obj3)

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return (self.img.get_height() - 40) 

class Gun:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def show(self):
        screen.blit(self.img,(self.x, self.y))
        
    def move(self, speed):
        self.x += speed
        screen.blit(self.img,(self.x, self.y))

    def screen_edge(self, width):
        return not(self.x <= width and self.x >= 0)

    def collision(self, obj, objs2, obj3, obj4):
        return collide(self, obj, objs2, obj3, obj4)

    def bullet_in_monster(self, obj1):
        return playerb_collide(self, obj1)
    
    def bullet_in_player(self, obj):
        return playerb_collide(self, obj)

class Player:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.max_health = health
        self.health = 100
        self.img = [player_img, player_imgl]
        self.speed = 4
        self.bullets = []
        self.mask = pygame.mask.from_surface(self.img[0])
        self.rect = self.img[0].get_rect()
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.jump_count = 0
        self.score = 0
        self.current_level = 1
    
    def collision(self, obj, objs2, obj3, obj4):
        return collide(self, obj, objs2, obj3, obj4)
        
    def bullet_in_monster(self, obj1):
        return playerb_collide(self, obj1)

    def throw(self):
        bullet = Gun(self.x+35, self.y+35, weapon_img)
        self.bullets.append(bullet)
            
    def throw_bullets(self, speed, objs, objs2, obj1, obj3, obj4):
        for bullet in self.bullets:
            bullet.move(speed)
            if bullet.screen_edge(width):
                self.bullets.remove(bullet)
            else:
                if bullet.collision(objs, objs2, obj3, obj4):
                    self.bullets.remove(bullet)               
                    if bullet in self.bullets: 
                        self.bullets.remove(bullet)
                for obj in obj1:
                    if bullet.bullet_in_monster(obj):
                        self.bullets.remove(bullet)
                        self.score += 1
                        obj1.remove(obj)
                        
    def jump(self, objs, objs2, obj3, obj4):
        if self.move_left and self.x - self.speed > 0:
            self.x -= self.speed
            self.y = 390
            while self.collision(objs, objs2, obj3, obj4):
                self.y = self.y - (objs.get_height() - 2)
                self.y = self.y - (objs2.get_height() - 2)
                self.y = self.y - (obj3.get_height() - 2)
            screen.blit(self.img[1],(self.x, self.y)) 
   
        elif self.move_right and self.x + self.speed + self.img[1].get_width() < width:
            self.x += self.speed
            self.y = 390
            while self.collision(objs, objs2, obj3, obj4):
                self.y = self.y - (objs.get_height() - 2)
                self.y = self.y - (objs2.get_height() - 2)
                self.y = self.y - (obj3.get_height() - 2)
            screen.blit(self.img[0],(self.x, self.y))
            
        elif self.move_up:
            self.jump_count += 1
            self.y -= 30
            screen.blit(self.img[0],(self.x, self.y))
            while self.collision(objs, objs2, obj3, obj4):
                self.y = self.y - objs.get_height()
                self.y = self.y - objs2.get_height()
                self.y = self.y - obj3.get_height()
                self.y -= 46
                screen.blit(self.img[0],(self.x, self.y))
            
            if self.jump_count == 4:        
                self.jump_count = 0
                self.move_up = False
            
        else:
            self.y = 390
            while self.collision(objs, objs2, obj3, obj4):
                self.y = self.y - (objs.get_height() - 2)
                self.y = self.y - (objs2.get_height() - 2)
                self.y = self.y - (obj3.get_height()  - 2)
            screen.blit(self.img[0],(self.x, self.y))  
        
    def healthbar(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y + self.img[0].get_height() - 80, self.img[0].get_width(), 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y + self.img[0].get_height() - 80, self.img[0].get_width() * (self.health/self.max_health), 5))

    def get_width(self):
        return self.img[0].get_width()

    def get_height(self):
        return self.img[0].get_height()

class Monster:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.img = monster_img
        self.mask = pygame.mask.from_surface(self.img)
        self.width = self.img.get_width()
        self.speed = 1
        self.bullets = []
        
    def show(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self, obj, obj2, obj3, obj4):
        self.x -= self.speed
        if self.x + self.width < 0:
            self.x = 1500
        while self.collision(obj, obj2, obj3, obj4):
            self.y = self.y - obj.get_height()
            self.y = self.y - (obj2.get_height() - 4)
            self.y = self.y - (obj3.get_height() - 4)
        self.show()
        
    def bullet_in_player(self, obj):
        return playerb_collide(self, obj)

    def collision(self, obj, objs2, obj3, obj4):
        return collide(self, obj, objs2, obj3, obj4)

    def throw(self):
        bullet = Gun(self.x+35, self.y + 30, axe_img)
        self.bullets.append(bullet)
        
    def move_axe(self, speed, objs, objs2, obj, player, obj3, obj4):
        for bullet in self.bullets:    
            bullet.move(speed)
            if bullet.screen_edge(width):
                self.bullets.remove(bullet)
            else:
                if bullet.collision(objs, objs2, obj3, obj4):
                    self.bullets.remove(bullet)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                
            if bullet.bullet_in_player(obj):
                player.health -= 15
                self.bullets.remove(bullet)
                    
def collide(obj1, obj2, objs2, obj3, obj4):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    offset_x2 = objs2.x - obj1.x
    offset_y2 = objs2.y - obj1.y
    offset_x3 = obj3.x - obj1.x
    offset_y3 = obj3.y - obj1.y
    offset_x4 = obj4.x - obj1.x
    offset_y4 = obj4.y - obj1.y
    return (obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None) | (obj1.mask.overlap(objs2.mask, (offset_x2, offset_y2)) != None) | (obj1.mask.overlap(obj3.mask, (offset_x3, offset_y3)) != None) | (obj1.mask.overlap(obj4.mask, (offset_x4, offset_y4)) != None)

def playerb_collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return (obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None)

def obs_collide(obj1, obj2, obj3, obj4):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    offset_x2 = obj3.x - obj1.x
    offset_y2 = obj3.y - obj1.y
    offset_x3 = obj4.x - obj1.x
    offset_y3 = obj4.y - obj1.y
    return (obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None) | (obj1.mask.overlap(obj3.mask, (offset_x2, offset_y2)) != None) | (obj1.mask.overlap(obj4.mask, (offset_x3, offset_y3)) != None)

def key_down(event, player):
    if event.key == pygame.K_RIGHT:
        player.move_right = True
    elif event.key == pygame.K_LEFT:
        player.move_left = True
    elif event.key == pygame.K_UP:
        player.move_up = True
    elif event.key == pygame.K_SPACE:
        player.throw()

def key_up(event, player):
    if event.key == pygame.K_RIGHT:
        player.move_right = False
    elif event.key == pygame.K_LEFT:
        player.move_left = False
    elif event.key == pygame.K_UP:
        player.move_up = False
        
def moving(player):   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            key_down(event, player)
        elif event.type == pygame.KEYUP:
            key_up(event, player)

def level(player, background, base, base_mini, base_minor, obstacle):
    if player.score == 15:
        player.current_level = 2
        background.img = bg2
        base.img = base_b
        base_mini.img = mini_base1
        base_minor.img = minor_base1
        obstacle.img = obstacle1

    elif player.score == 35:
        player.current_level = 3
        background.img = level3_bg
        base.img = base_level3
        base_mini.img = base_level3_mini
        base_minor.img = base_level3_minor
        obstacle.img = obstacle1
        
    elif player.score == 75:
        player.current_level = 4
        background.img = level4_bg
        base.img = base_img
        base_mini.img = mini_base
        base_minor.img = minor_base
        obstacle.img = obs

def main():
    player = Player(390, 390)
    base = Base(1700, 412, base_img)
    base_mini = Base(800, 413, mini_base)
    base_minor = Base(1300, 413, minor_base)
    background = Background(0, bg)
    obstacle = Obstacle(1800, 420, obs)
    monsters = []
    monster_spawn = 0
    player_level = 0
    score_title = pygame.font.SysFont("comicsans", 40)
    level_title = pygame.font.SysFont("comicsans", 40)
    
    while True:
        background.move()
        base.move()
        base_mini.move()
        base_minor.move()
        obstacle.move(base, base_mini, base_minor)
        player.jump(base, obstacle, base_mini, base_minor)
        player.healthbar(screen)
        moving(player)

        level(player, background, base, base_mini, base_minor, obstacle)
        score_tittle = score_title.render(f"Score: {player.score}", 1, (255,255,255))
        screen.blit(score_tittle, (10, 40))
        level_tittle = level_title.render(f"Level: {player.current_level}", 1, (255,255,255))
        screen.blit(level_tittle, (10, 10))
        
        for monster in monsters: monster.show()
        
        if len(monsters) == 0:
            monster_spawn += 1
            for x in range(monster_spawn):
                if player.score < 15 or player.score > 34 and player.score < 74:
                    monster = Monster(random.randrange(random.randrange(800,1700),random.randrange(2100, 3500)), 385)
                    monsters.append(monster)
                elif player.score >= 15 and player.score < 35:
                    monster = Monster(random.randrange(random.randrange(800,1700),random.randrange(2100, 3500)), 383)
                    monster.img = monster_img2
                    monsters.append(monster)
                elif player.score >= 75:
                    monster = Monster(random.randrange(random.randrange(800,1700),random.randrange(2100, 3500)), 390)
                    monster.img = monster_img3
                    monsters.append(monster)

        for monster in monsters[:]:
            monster.move(base, obstacle, base_mini, base_minor)
            monster.move_axe(-bullet_speed, obstacle, base, player, player, base_mini, base_minor)

            if random.randint(0, 2*60) == 1:monster.throw()
            if player.health <= 0: pygame.quit()
            if playerb_collide(monster, player):
                player.health -= 10
                monsters.remove(monster)
                player.score += 1
            if player.health < 100: player.health += 0.001
        
        player.throw_bullets(bullet_speed, obstacle, base, monsters, base_mini, base_minor)
        pygame.display.update()

if __name__ == "__main__":
    main()