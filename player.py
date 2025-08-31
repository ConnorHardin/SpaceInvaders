import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,x_constraint, y_constraint,speed):
        super().__init__()
        file_path = './data/ship.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_x_constraint = x_constraint
        self.max_y_constraint = y_constraint
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600

        self.lasers = pygame.sprite.Group()

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.rect.x += self.speed
        elif keys[pygame.K_a]:
            self.rect.x -= self.speed
        elif keys[pygame.K_w]:
            self.rect.y -= self.speed
        elif keys[pygame.K_s]:
            self.rect.y += self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def constraint(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.max_x_constraint:
            self.rect.right = self.max_x_constraint

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.max_y_constraint:
            self.rect.bottom = self.max_y_constraint

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center,-8,self.rect.bottom))

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()